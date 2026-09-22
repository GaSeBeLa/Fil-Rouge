# Tuto 1 — Hacher les mots de passe (Argon2id)

> 🎯 **Objectif** : à la fin, un `POST /users` stocke une empreinte Argon2id,
> plus jamais le mot de passe en clair.
>
> ⏱️ Compter 1 à 2 h. Étapes 1 à 4 faisables seul, sans réunion.
>
> 📋 Couvre les étapes `B1` et `B2` du plan. Applique `ADR-016`.
>
> ⚠️ **Note rédigée avec l'IA.** Les mesures du §2 et les briques Argon2 ont
> été **exécutées** le 22/09 (conteneur `python:3.12-slim`). Le code
> d'intégration FastAPI, lui, est **écrit mais pas exécuté** : c'est à vous de
> le faire tourner. Sources au §10.
>
> 📅 22 septembre 2026. Suite : `md/tuto-2-authentification-jwt.md`.

---

## 0. Avant de commencer

### 0.1 Prérequis

| Quoi | Comment vérifier |
|---|---|
| La base tourne | `docker ps` → `fil_rouge_immobilier_db` |
| L'API répond | http://localhost:8000/docs |
| Vous êtes à jour | `git pull` |

### 0.2 Constater le problème soi-même

Ne faites pas ce tuto sans avoir vu le problème. Ça prend 30 secondes.

**1.** Créer un compte de test :

```bash
curl -s -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"email":"tuto1@exemple.fr","password":"MotDePasseEnClair123","is_activated":true,"id_role":1}'
```

Noter l'`id` renvoyé.

**2.** Ouvrir psql, depuis `docker/` :

```bash
docker exec -it fil_rouge_immobilier_db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

**3.** Regarder ce que la base a gardé :

```sql
SELECT id, email, password FROM "user" WHERE email = 'tuto1@exemple.fr';
```

❌ Vous lisez **`MotDePasseEnClair123`**, en toutes lettres.

**4.** Nettoyer — `NN` = l'`id` de l'étape 1 :

```bash
curl -s -X DELETE http://localhost:8000/users/NN
```

➡️ Voilà ce qu'on vient corriger.

### 0.3 Ce qu'on ne touche pas

- ❌ Le schéma SQL — `password VARCHAR(255)` est déjà au bon format.
- ❌ Les 24 comptes migrés — leur placeholder est volontaire et inerte.
- ❌ Les 17 autres tables.

✅ On touche 4 fichiers, dont 2 nouveaux.

---

## 1. Installer la dépendance

Dans `API/requirements.txt`, sous `python-dotenv` :

```
argon2-cffi
```

Puis reconstruire l'image, depuis `docker/` :

```bash
docker compose build api && docker compose up -d api
```

Vérifier :

```bash
docker exec fil_rouge_immobilier_api pip show argon2-cffi
```

Attendu : `Version: 25.1.0` ou supérieure.

### 💡 Pourquoi `argon2-cffi` et pas `pwdlib` ?

La doc officielle de FastAPI utilise aujourd'hui `pwdlib[argon2]`. Les deux
sont valables — **`pwdlib` installe `argon2-cffi` et s'en sert en dessous**
(vérifié : il produit bien des empreintes `$argon2id$`).

On reste sur `argon2-cffi` direct parce que :

- `ADR-016` le nomme explicitement ;
- `pwdlib` n'apporte qu'une abstraction multi-algorithmes, dont on n'a pas
  besoin — un seul algorithme est décidé ;
- une dépendance de moins.

⚠️ **Si le groupe préfère `pwdlib`**, attention : l'ordre des arguments est
**inversé**. `pwdlib` → `verify(mot_de_passe, empreinte)`. `argon2-cffi` →
`verify(empreinte, mot_de_passe)`. Une inversion silencieuse fait échouer
toutes les connexions.

---

## 2. Calibrer les paramètres

`ADR-016` fixe une cible : **250 à 500 ms par hachage**.

### 2.1 Pourquoi c'est lent exprès

Un hachage rapide est un hachage cassable. Si votre machine fait un hachage en
1 ms, un attaquant avec un GPU en fait des millions par seconde sur une base
volée.

🎯 250-500 ms, c'est le point d'équilibre : imperceptible pour l'utilisateur,
ruineux pour une attaque par dictionnaire.

### 2.2 Les paramètres par défaut ne suffisent pas

Mesuré le 22/09 dans `python:3.12-slim`, moyenne de 3 hachages :

| `time_cost` | `memory_cost` | Temps | Dans la cible ? |
|---|---|---|---|
| 3 | 64 Mo *(défaut)* | **139 ms** | ❌ trop rapide |
| 4 | 64 Mo | 135 ms | ❌ |
| 2 | 128 Mo | 145 ms | ❌ |
| 3 | 128 Mo | 202 ms | 🟡 limite basse |
| 1 | 256 Mo | 170 ms | ❌ |
| **2** | **256 Mo** | **297 ms** | ✅ |

💡 **Ce qui saute aux yeux** : augmenter `time_cost` seul ne sert presque à
rien (139 → 135 ms, dans le bruit de mesure). C'est `memory_cost` qui pèse.
Normal — c'est exactement le principe *memory-hard* d'Argon2.

### 2.3 Mesurer chez vous

⚠️ **Ne recopiez pas ces valeurs.** Elles dépendent du processeur. Mesurez sur
la machine qui fera tourner l'API :

```bash
docker exec fil_rouge_immobilier_api python -c "
from argon2 import PasswordHasher
import time
for t, m in [(3,65536), (3,131072), (2,262144), (3,262144)]:
    ph = PasswordHasher(time_cost=t, memory_cost=m, parallelism=4)
    d = []
    for _ in range(3):
        s = time.perf_counter(); ph.hash('test'); d.append((time.perf_counter()-s)*1000)
    print('t=%d m=%d Mo -> %.0f ms' % (t, m//1024, sum(d)/3))
"
```

Retenez la première ligne qui dépasse **250 ms**.

### 2.4 ⚠️ Le coût caché de la mémoire

`memory_cost=262144` veut dire **256 Mo par hachage en cours**.

- 10 connexions simultanées → **2,5 Go** de pointe.
- 20 → 5 Go.

C'est exactement ce que prévoit `ADR-016` : *« surveiller la consommation
mémoire côté serveur si beaucoup de hashs sont calculés en parallèle »*.

➡️ **Conséquence** : l'endpoint de connexion devra être **rate-limité**
(tuto 2). Sans ça, il suffit d'envoyer 100 requêtes de login pour saturer la
RAM du serveur. Un hachage coûteux protège les mots de passe **et** ouvre un
vecteur de déni de service.

---

## 3. Créer `security.py`

Nouveau fichier : `API/src/app/utils/security.py`

```python
"""
security.py — Hachage et vérification des mots de passe (ADR-016).

============================================================================
COMMENT LIRE CE FICHIER
============================================================================
Un mot de passe en clair ne doit exister QUE dans la variable locale d'une
requête, jamais en base, jamais en log, jamais en cache.

Les paramètres ci-dessous sont calibrés pour ~250-500 ms sur la machine qui
exécute l'API (ADR-016). Ils se MESURENT, ils ne se recopient pas : voir
md/tuto-1-hachage-mots-de-passe.md §2.3.

Les paramètres sont inscrits DANS l'empreinte produite (format PHC). Les
durcir plus tard n'invalide donc aucune empreinte existante : c'est ce que
gère needs_rehash().
============================================================================
"""

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

# À remplacer par VOS valeurs mesurées (§2.3).
_hasher = PasswordHasher(
    time_cost=2,
    memory_cost=262144,  # 256 Mo
    parallelism=4,
)


def hash_password(plain: str) -> str:
    """Renvoie l'empreinte PHC d'un mot de passe en clair."""
    return _hasher.hash(plain)


def verify_password(stored: str, plain: str) -> bool:
    """
    Compare un mot de passe en clair à une empreinte stockée.

    Utilise la vérification à temps constant d'argon2-cffi : jamais un `==`,
    dont la durée dépend du nombre de caractères corrects (timing attack).

    InvalidHashError couvre les 24 comptes migrés, dont le placeholder n'est
    pas une empreinte valide : ils ne peuvent tout simplement pas se
    connecter, ce qui est le comportement voulu.
    """
    try:
        return _hasher.verify(stored, plain)
    except (VerifyMismatchError, InvalidHashError):
        return False


def needs_rehash(stored: str) -> bool:
    """
    Vrai si l'empreinte a été produite avec des paramètres plus faibles que
    les paramètres courants. À appeler après une connexion RÉUSSIE : c'est le
    seul moment où l'on dispose du mot de passe en clair pour re-hacher.
    """
    try:
        return _hasher.check_needs_rehash(stored)
    except InvalidHashError:
        return False
```

### ⚠️ Trois pièges dans ce fichier

**1. `verify()` lève une exception, elle ne renvoie pas `False`.** Sans le
`try`, un mauvais mot de passe fait planter l'API en `500` au lieu de renvoyer
une erreur propre.

**2. `InvalidHashError` n'est pas optionnelle.** Les 24 comptes migrés portent
`$2b$12$MIGRATED_PLACEHOLDER_MUST_RESET`, qui n'est pas une empreinte Argon2
valide. Sans ce cas, toute tentative de connexion sur ces comptes plante.

**3. L'ordre des arguments.** `verify(empreinte, clair)` — pas l'inverse. En
inverser deux fait échouer 100 % des connexions, sans message clair.

### 3.1 Vérifier tout de suite

```bash
docker exec fil_rouge_immobilier_api python -c "
import sys; sys.path.insert(0, '/app/src')
from app.utils.security import hash_password, verify_password, needs_rehash
h = hash_password('MotDePasseEnClair123')
print('empreinte :', h)
print('longueur  :', len(h), '(la colonne accepte 255)')
print('bon mdp   :', verify_password(h, 'MotDePasseEnClair123'))
print('mauvais   :', verify_password(h, 'autre'))
print('placeholder:', verify_password('\$2b\$12\$MIGRATED_PLACEHOLDER_MUST_RESET', 'x'))
print('rehash    :', needs_rehash(h))
print('sel unique:', h != hash_password('MotDePasseEnClair123'))
"
```

⚠️ Le chemin `/app/src` dépend de votre `docker-compose.yml`. S'il ne passe
pas, adaptez-le.

**Attendu :**

```
empreinte : $argon2id$v=19$m=262144,t=2,p=4$...
longueur  : 98 (la colonne accepte 255)
bon mdp   : True
mauvais   : False
placeholder: False
rehash    : False
sel unique: True
```

💡 **Lisez l'empreinte.** `m=262144,t=2,p=4` y figure en clair : les paramètres
voyagent avec elle. C'est ce qui rend le durcissement possible sans casser
l'existant.

💡 **`sel unique: True`** : deux hachages du **même** mot de passe donnent deux
empreintes **différentes**. C'est le sel, généré automatiquement. Aucune
colonne à ajouter.

---

## 4. `B2` — séparer entrée et sortie

### 4.1 Le problème actuel

Dans `API/src/app/routes/user_router.py` :

```python
response_model=User,      # modèle d'ENTRÉE  (POST, PUT)
read_model=UserPublic,    # modèle de SORTIE (sans password)
```

🟡 La sortie est protégée. L'entrée, non : `User` est le **modèle de table**.
Un client de l'API peut donc poster `id` et `created_at` — des champs que le
serveur devrait seul décider.

❌ **Règle** : un modèle de table ne doit jamais servir de schéma d'entrée.

### 4.2 Ajouter les schémas

Dans `API/src/app/models/user_model.py`, à la suite de `UserPublic` :

```python
class UserCreate(SQLModel):
    """
    Ce que l'API ACCEPTE pour créer un compte.

    `password` est ici le mot de passe EN CLAIR : c'est la seule forme sous
    laquelle il entre dans le système. Il est haché dans UserService.create()
    et n'atteint jamais la base tel quel.

    Ni `id` ni `created_at` : le serveur les décide.
    """
    email: str = Field(max_length=150)
    password: str = Field(min_length=12)
    is_activated: Optional[bool] = None
    id_role: int


class UserUpdate(SQLModel):
    """
    Modification partielle. Tout est optionnel : on ne change que ce qui est
    fourni. Un `password` présent est haché comme à la création.
    """
    email: Optional[str] = Field(default=None, max_length=150)
    password: Optional[str] = Field(default=None, min_length=12)
    is_activated: Optional[bool] = None
    id_role: Optional[int] = None
```

⚠️ **`min_length=12` est une proposition, pas une décision.** L'OWASP
privilégie la longueur sur la complexité (pas d'obligation de majuscule ou de
caractère spécial). C'est la question 6 de
`md/securite-mots-de-passe-et-droits.md` : à trancher en réunion.

Puis exporter dans `API/src/app/models/__init__.py`, à côté de `UserPublic`.

---

## 5. Hacher dans le service

C'est **le** point du tuto. Tout le reste en découle.

### 5.1 Pourquoi dans le service

L'architecture le prévoit déjà. C'est écrit dans l'en-tête de
`base_service.py` :

> *« une sous-classe comme UserService peut surcharger create() pour hasher le
> mot de passe avant d'appeler super().create(), sans que les routers ni les
> repositories n'aient à changer »*

| Couche | Pourquoi pas elle |
|---|---|
| Router | ne connaît pas le métier ; un autre appelant le contourne |
| Repository | trop bas : il écrit, il ne décide pas |
| **Service** | ✅ la couche de la règle métier |

### 5.2 Le code

`API/src/app/services/user_service.py` — le fichier fait 7 lignes
aujourd'hui :

```python
from sqlmodel import Session

from ..models import User, UserCreate, UserUpdate
from ..repositories.user_repository import UserRepository
from ..utils.security import hash_password
from .base_service import BaseService


class UserService(BaseService[User]):
    """
    Seul endroit du projet qui transforme un mot de passe en clair en
    empreinte. Si un mot de passe en clair atteint la base, c'est qu'un
    chemin d'écriture contourne cette classe.
    """

    def __init__(self, repository: UserRepository):
        super().__init__(repository, not_found_detail="Utilisateur introuvable")

    def create(self, session: Session, item: UserCreate) -> User:
        user = User(
            email=item.email,
            password=hash_password(item.password),
            is_activated=item.is_activated,
            id_role=item.id_role,
        )
        return self.repository.create(session, user)

    def update(self, session: Session, item_id: int, data: UserUpdate) -> User:
        existing = self.get_by_id(session, item_id)
        changes = data.model_dump(exclude_unset=True)

        if "password" in changes:
            changes["password"] = hash_password(changes["password"])

        for field, value in changes.items():
            setattr(existing, field, value)

        return self.repository.save(session, existing)
```

### ⚠️ Deux points à adapter

**1. `self.repository.save(...)`** n'existe peut-être pas sous ce nom. Ouvrez
`base_repository.py` et utilisez la méthode réelle.

**2. `BaseService` expose `replace()`, pas `update()`.** Regardez ce que
`build_crud_router` appelle pour le `PUT`, et alignez le nom — sinon votre
méthode n'est jamais appelée et le mot de passe repasse en clair, sans aucune
erreur visible.

💡 **C'est le piège le plus dangereux du tuto** : une surcharge mal nommée
échoue en silence. D'où le test du §7, qui vérifie le `PUT` autant que le
`POST`.

---

## 6. Brancher le router

`API/src/app/routes/user_router.py` :

```python
from ..models import User, UserCreate, UserPublic
from ..repositories.user_repository import UserRepository
from ..services.user_service import UserService
from .crud_router import build_crud_router

router = build_crud_router(
    service=UserService(UserRepository()),
    prefix="/users",
    tag="user",
    # ENTRÉE : UserCreate — ni id, ni created_at, et un mot de passe
    # en clair qui sera haché par le service (ADR-016).
    response_model=UserCreate,
    # SORTIE : UserPublic — `password` ne sort jamais.
    read_model=UserPublic,
)
```

⚠️ `build_crud_router` utilise le **même** `response_model` pour le `POST` et
le `PUT`. Si vous voulez `UserUpdate` sur le `PUT`, il faudra soit ajouter un
paramètre à la fabrique, soit sortir les routes `/users` du générique. **Ne
modifiez pas `crud_router.py` à la légère : il sert les 18 tables.**

---

## 7. Vérifier

### 7.1 Redémarrer

```bash
docker compose up -d --build api
```

### 7.2 Le test qui compte

**1.** Créer un compte :

```bash
curl -s -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"email":"tuto1-final@exemple.fr","password":"MotDePasseAssezLong123","is_activated":true,"id_role":1}'
```

✅ La réponse ne doit contenir **aucun** champ `password`.

**2.** Dans psql :

```sql
SELECT id, email, password FROM "user" WHERE email = 'tuto1-final@exemple.fr';
```

✅ Attendu : une chaîne commençant par **`$argon2id$v=19$m=...`**

❌ Si vous lisez encore le mot de passe en clair : le service n'est pas appelé.
Relisez le §5.2, point 2.

**3.** Tester le `PUT` — c'est là que ça casse le plus souvent :

```bash
curl -s -X PUT http://localhost:8000/users/NN -H "Content-Type: application/json" -d '{"email":"tuto1-final@exemple.fr","password":"UnAutreMotDePasse456","is_activated":true,"id_role":1}'
```

✅ En base, toujours une empreinte `$argon2id$`, et **différente** de la
précédente.

**4.** Nettoyer :

```bash
curl -s -X DELETE http://localhost:8000/users/NN
```

### 7.3 La checklist

| # | Vérification | ✅ |
|---|---|---|
| 1 | `POST` → empreinte `$argon2id$` en base | ☐ |
| 2 | `PUT` avec mot de passe → empreinte, pas du clair | ☐ |
| 3 | Aucune réponse de l'API ne contient `password` | ☐ |
| 4 | Deux comptes, même mot de passe → empreintes différentes | ☐ |
| 5 | Un hachage prend entre 250 et 500 ms | ☐ |
| 6 | La base est revenue à **24 comptes** | ☐ |

---

## 8. Les 24 comptes existants

Rien d'urgent : leur placeholder interdit déjà toute connexion.

Deux choses à faire **plus tard**, pas maintenant :

| Quoi | Quand |
|---|---|
| Remplacer le placeholder `$2b$` (bcrypt) par une vraie empreinte Argon2id | à l'écriture du seed |
| Créer de **vrais** comptes `Manager` et `Admin` — aujourd'hui : 1 manager placeholder bloqué (migration du 22/09), 0 admin | après ce tuto |

⚠️ **Ne créez pas de compte admin avant d'avoir fini ce tuto.** Son mot de
passe partirait en clair.

---

## 9. Ce que ce tuto ne fait PAS

Il faut être clair là-dessus.

| Fait ✅ | Pas fait ❌ |
|---|---|
| Les mots de passe sont hachés | On ne peut toujours pas **se connecter** |
| L'empreinte ne sort jamais de l'API | Aucune route n'est protégée |
| `verify_password` existe | Personne ne l'appelle encore |

➡️ **Un mot de passe haché sans authentification ne protège rien du tout.**
Les ~90 routes restent ouvertes à qui connaît l'URL.

**Suite obligatoire : `md/tuto-2-authentification-jwt.md`.**

---

## 10. Sources

| Affirmation | Source |
|---|---|
| Argon2id, `argon2-cffi`, cible 250-500 ms, `check_needs_rehash`, rate-limiting | Confluence, *Journal de décisions*, `ADR-016` (04/09/2026) |
| `password VARCHAR(255)` | `docker/init-v2/01_create_fil_rouge_immobilier.sql`, table `user` |
| Le service est le bon endroit | `API/src/app/services/base_service.py`, en-tête |
| `UserPublic` protège la sortie | `API/src/app/models/user_model.py` |
| Les temps du §2.2 | mesurés le 22/09, `python:3.12-slim`, `argon2-cffi 25.1.0` |
| `pwdlib` s'appuie sur `argon2-cffi` | mesuré le 22/09 : `pip install "pwdlib[argon2]"` installe `argon2-cffi 25.1.0` et produit des empreintes `$argon2id$` |
| La doc FastAPI utilise `pwdlib[argon2]` | [fastapi.tiangolo.com — OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), consulté le 22/09/2026 |

⚠️ **`ADR-016` est au statut « proposé » depuis le 04/09.** Ce tuto applique
une décision non encore validée. À faire passer en réunion.

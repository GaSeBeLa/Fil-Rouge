# Tuto 2 — Authentification et droits d'accès (JWT)

> 🎯 **Objectif** : à la fin, il faut se connecter pour appeler l'API, et
> chacun ne voit que ce qui le concerne.
>
> ⏱️ Compter 3 à 5 h. Plus long et plus délicat que le tuto 1.
>
> 📋 Couvre l'étape `B3` du plan.
>
> 🔴 **Aucun ADR ne couvre ce sujet.** Les 24 décisions du journal vont du SGBD
> au hachage, mais **aucune** ne traite de l'authentification. Ce tuto
> **propose** JWT ; il ne tranche pas. Voir §1.3.
>
> ⚠️ **Note rédigée avec l'IA.** Les briques PyJWT du §1.2 ont été
> **exécutées** le 22/09. Le code d'intégration FastAPI est **écrit mais pas
> exécuté**. Sources au §11.
>
> 📅 22 septembre 2026. Prérequis : `md/tuto-1-hachage-mots-de-passe.md`.

---

## 0. Avant de commencer

### 0.1 Le tuto 1 doit être fini

⚠️ **Ne commencez pas sans ça.** Ce tuto a besoin de `verify_password()`, qui
vient du tuto 1.

Vérifier en 10 secondes, dans psql :

```sql
SELECT count(*) FROM "user" WHERE password LIKE '$argon2id$%';
```

- `0` → le tuto 1 n'est pas fini (ou aucun compte n'a encore été recréé).
- ✅ Au moins 1 → vous pouvez continuer.

### 0.2 Deux chantiers, pas un

| Partie | Question | Sections |
|---|---|---|
| **Authentification** | *qui es-tu ?* | §2 à §5 |
| **Autorisation** | *as-tu le droit ?* | §6 à §8 |

Elles se font **dans cet ordre**. Impossible de vérifier un droit sans savoir
qui demande.

---

## 1. Les concepts

### 1.1 `401` et `403` ne veulent pas dire la même chose

| Code | Nom | Sens réel |
|---|---|---|
| `401` | Unauthorized | *je ne sais pas qui tu es* — mal nommé |
| `403` | Forbidden | *je sais qui tu es, et tu n'as pas le droit* |

💡 Renvoyer `403` à un visiteur non connecté est une erreur courante. Un jury
la repère.

### 1.2 Anatomie d'un JWT — mesurée

Un JWT est une chaîne en trois parties séparées par des points :
`header.payload.signature`.

Exécuté le 22/09 avec `PyJWT 2.14.0` :

| Mesure | Résultat |
|---|---|
| Parties | **3** |
| Longueur pour 3 claims | **140 caractères** |
| Payload décodé **sans la clé** | `{"sub":"7","role":"Hunter","exp":1790071132}` |
| Décodage avec la bonne clé | ✅ |
| Décodage avec une mauvaise clé | ❌ `InvalidSignatureError` |
| Décodage d'un jeton expiré | ❌ `ExpiredSignatureError` |

### ⚠️ Le point que tout le monde rate

Regardez la troisième ligne. **Le payload a été lu sans aucune clé**, avec un
simple décodage base64.

➡️ **Un JWT est signé, pas chiffré.** La signature prouve qu'il n'a pas été
**modifié**. Elle ne le rend pas **secret**.

❌ Ne mettez jamais dans un JWT : mot de passe, empreinte, email, données
personnelles, montant de rémunération.

✅ Mettez-y : `sub` (l'id utilisateur), `exp` (l'expiration), le rôle.

### 1.3 🔴 Ce que le groupe doit trancher AVANT

JWT n'est pas la seule option, et rien n'est décidé.

| Option | Avantage | Inconvénient |
|---|---|---|
| **JWT** *(proposé ici)* | aucun état serveur, standard, bien documenté dans FastAPI | **jeton non révocable** avant son expiration |
| **Session en base** | révocation immédiate | une table et une requête de plus par appel |
| **Clé d'API** | trivial à implémenter | pas d'utilisateur, pas d'expiration — inadapté |

⚠️ **Le défaut du JWT est structurel** : rien n'est stocké côté serveur, donc
**on ne peut pas invalider un jeton émis**. Un jeton volé reste valide jusqu'à
son `exp`. Le seul garde-fou est une durée courte.

➡️ **Ce tuto part sur JWT** — c'est le choix documenté par FastAPI et le plus
rapide à livrer. **Mais ce choix mérite un ADR**, avec sa durée d'expiration.
À porter en réunion.

---

## 2. Installer et configurer

### 2.1 La dépendance

Dans `API/requirements.txt` :

```
pyjwt
```

💡 **`pyjwt`, pas `python-jose`.** La doc officielle de FastAPI utilise
aujourd'hui PyJWT. Beaucoup de tutoriels en ligne montrent encore
`python-jose`, qui n'est plus la recommandation.

Reconstruire, depuis `docker/` :

```bash
docker compose build api && docker compose up -d api
```

### 2.2 La clé secrète

Cette clé signe les jetons. Qui la possède peut fabriquer un jeton valide pour
n'importe quel compte, y compris admin.

**Générer :**

```bash
openssl rand -hex 32
```

**Ajouter à `docker/.env`** (jamais versionné) :

```
JWT_SECRET_KEY=<le résultat de la commande ci-dessus>
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

**Et à `docker/.env.exemple`**, avec des valeurs factices :

```
JWT_SECRET_KEY=change-moi-genere-avec-openssl-rand-hex-32
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

Puis exposer ces variables au service `api` dans `docker-compose.yml`.

### ⚠️ Trois règles sur cette clé

**1. Jamais en dur dans le code.** C'est la règle 5 du `CLAUDE.md` du projet :
*« Aucun secret ni `.env` dans git »*. Une clé committée est une clé publique,
y compris après suppression — elle reste dans l'historique.

**2. Au moins 32 octets.** Mesuré : avec une clé de 12 octets, PyJWT émet un
`InsecureKeyLengthWarning` (RFC 7518 §3.2). `openssl rand -hex 32` donne la
bonne longueur.

**3. Changer la clé invalide tous les jetons.** C'est d'ailleurs le seul moyen
de tout révoquer d'un coup — l'option nucléaire, qui déconnecte tout le monde.

---

## 3. Le module `auth.py`

Nouveau fichier : `API/src/app/utils/auth.py`

```python
"""
auth.py — Émission et lecture des jetons JWT.

============================================================================
COMMENT LIRE CE FICHIER
============================================================================
Ce module ne connaît ni FastAPI, ni la base : il fabrique et relit des
jetons, rien d'autre. Les dépendances FastAPI vivent dans dependencies.py.

RAPPEL : un JWT est SIGNÉ, pas CHIFFRÉ. Son contenu est lisible par
n'importe qui (vérifié : un simple décodage base64 suffit). On n'y met donc
que l'id utilisateur, son rôle et l'expiration — jamais une donnée
sensible.
============================================================================
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # KeyError au démarrage si absente
ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", "60"))


def create_access_token(user_id: int, role: str) -> str:
    """Émet un jeton pour un utilisateur donné."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),   # la spec JWT impose une chaîne
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def read_access_token(token: str) -> Optional[dict]:
    """
    Renvoie le payload, ou None si le jeton est invalide, expiré, ou signé
    avec une autre clé. InvalidTokenError couvre tous ces cas.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        return None
```

### ⚠️ Deux pièges

**1. `os.environ[...]` et non `os.environ.get(...)`** pour la clé. Un `.get()`
renvoie `None` si la variable manque, et l'API démarre avec une signature
cassée — sans rien dire. Avec les crochets, elle refuse de démarrer. **Une
panne bruyante vaut mieux qu'une faille silencieuse.**

**2. `algorithms=[ALGORITHM]` au décodage est obligatoire.** Sans cette liste,
un attaquant peut soumettre un jeton déclarant `alg: none` et se faire passer
pour qui il veut. C'est une attaque classique contre les JWT. PyJWT s'en
protège si — et seulement si — vous passez la liste.

---

## 4. La route de connexion

Nouveau fichier : `API/src/app/routes/auth_router.py`

```python
"""
auth_router.py — Connexion et émission du jeton.

Seule route publique de l'API avec le health-check.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ..conf.database import get_session
from ..models import User
from ..utils.auth import create_access_token
from ..utils.security import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    # OAuth2PasswordRequestForm impose le nom "username" : c'est notre email.
    user = session.exec(
        select(User).where(User.email == form.username)
    ).first()

    # UN SEUL message pour les deux cas. Distinguer « email inconnu » de
    # « mot de passe faux » permettrait d'énumérer les comptes existants.
    if user is None or not verify_password(user.password, form.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_activated is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte désactivé",
        )

    role = session.get(Role, user.id_role)
    token = create_access_token(user.id, role.wording)
    return {"access_token": token, "token_type": "bearer"}
```

⚠️ Il manque l'import de `Role` — à ajouter. C'est volontaire : ne collez pas
ce code sans le lire.

Puis dans `main.py` :

```python
app.include_router(auth_router.router)
```

### ⚠️ Le piège du compte inexistant

```python
if user is None or not verify_password(...)
```

Python évalue de gauche à droite : si `user is None`, `verify_password` n'est
**jamais appelé**. La réponse revient donc bien plus vite pour un email
inconnu que pour un email connu — et cet écart, mesurable, permet d'énumérer
les comptes.

💡 **C'est une vraie faille**, appelée *user enumeration by timing*. La parade
propre est de hacher une valeur bidon dans le cas `None`, pour égaliser les
temps. À décider en groupe : c'est un raffinement, pas un bloquant pour un
projet d'école — mais savoir l'expliquer en soutenance vaut des points.

---

## 5. Savoir qui appelle

Nouveau fichier : `API/src/app/utils/dependencies.py`

```python
"""
dependencies.py — Les dépendances FastAPI de sécurité.

get_current_user  -> AUTHENTIFICATION : qui es-tu ?        (401)
require_role      -> AUTORISATION     : as-tu le droit ?   (403)
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from ..conf.database import get_session
from ..models import User
from .auth import read_access_token

# tokenUrl sert à Swagger : c'est ce qui fait apparaître le bouton
# « Authorize » sur /docs.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Jeton invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = read_access_token(token)
    if payload is None:
        raise credentials_error

    user = session.get(User, int(payload["sub"]))
    if user is None:
        raise credentials_error

    return user
```

### 💡 Pourquoi relire l'utilisateur en base

Le rôle est déjà dans le jeton. Pourquoi une requête de plus ?

Parce qu'un jeton est **figé à l'émission**. Si on rétrograde un `Admin` en
`Client`, son jeton continue d'affirmer `Admin` jusqu'à expiration.

| Source du rôle | Rapide | À jour |
|---|---|---|
| Le jeton | ✅ | ❌ |
| La base | ❌ | ✅ |

➡️ Pour un projet noté sur la rigueur : **la base**. La requête est indexée sur
la clé primaire, le coût est négligeable.

---

## 6. Fermer les 90 routes d'un coup

### 6.1 Le levier

Les ~90 opérations de l'API sont générées par **une seule fabrique**,
`build_crud_router`. Une dépendance posée sur l'`APIRouter` qu'elle construit
s'applique donc à **toutes les routes des 18 tables**.

Dans `API/src/app/routes/crud_router.py` :

```python
from ..utils.dependencies import get_current_user

def build_crud_router(...) -> APIRouter:
    router = APIRouter(
        prefix=prefix,
        tags=[tag],
        # Vaut pour les 5 routes de chacune des 18 tables : sans jeton
        # valide, rien ne passe. Les droits fins, eux, sont dans les
        # services (§7, §8).
        dependencies=[Depends(get_current_user)],
    )
```

⚠️ **`crud_router.py` sert les 18 tables.** Toute erreur ici casse toute
l'API. Faites-en un commit isolé, facile à annuler.

### 6.2 Vérifier immédiatement

```bash
curl -s -o /dev/null -w "sans jeton -> %{http_code}\n" http://localhost:8000/users
```

✅ Attendu : **`401`**. Si vous obtenez `200`, la dépendance n'est pas active.

⚠️ **Le health-check et `/auth/login` doivent rester publics.** Vérifiez-le :

```bash
curl -s -o /dev/null -w "docs -> %{http_code}\n" http://localhost:8000/docs
```

---

## 7. Les droits par rôle (RBAC)

### 7.1 La dépendance

À ajouter dans `dependencies.py` :

```python
def require_role(*allowed: str):
    """
    Fabrique une dépendance qui n'accepte que certains rôles.

        @router.get("/payments", dependencies=[Depends(require_role("Admin"))])

    403, pas 401 : l'utilisateur EST identifié, il n'a simplement pas le
    droit.
    """
    def checker(
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ) -> User:
        role = session.get(Role, user.id_role)
        if role is None or role.wording not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Droits insuffisants",
            )
        return user
    return checker
```

### 7.2 ⚠️ Le rôle ne suffit JAMAIS

C'est le point le plus important des deux tutos.

Bruno et Sophie sont tous deux `Hunter`. Ils ont le **même rôle**. Un contrôle
limité au rôle autorise donc Bruno à lire `/payments/12` — la rémunération de
Sophie.

➡️ C'est une **élévation de privilège horizontale**, famille **IDOR**. C'est
la faille la plus fréquente sur une API CRUD comme la nôtre.

✅ Il faut **deux** contrôles :

| Niveau | Question | Où |
|---|---|---|
| **RBAC** | ce rôle voit-il ce type de ressource ? | `require_role` (§7.1) |
| **Ownership** | cette ligne est-elle **la sienne** ? | le service (§8) |

---

## 8. Les droits sur ses propres données

### 8.1 Filtrer dans le `WHERE`

```python
class PaymentService(BaseService[Payment]):

    def list_for(self, session: Session, user: User, role: str):
        statement = select(Payment)

        if role == "Hunter":
            # Restriction DANS la requête, pas après.
            statement = statement.where(Payment.id_hunter == user.id)
        elif role == "Manager":
            # Ses chasseurs : ceux dont hunter.id_realestatemanager est lui.
            # Lien ajouté le 22/09 (voir §8.2). Les deux colonnes portent
            # des id de "user", comme toutes les FK du schéma.
            mine = select(Hunter.id_user).where(
                Hunter.id_realestatemanager == user.id
            )
            statement = statement.where(Payment.id_hunter.in_(mine))
        elif role == "Client":
            raise HTTPException(status_code=403, detail="Droits insuffisants")
        # Admin : aucune restriction.

        return session.exec(statement).all()
```

⚠️ La branche `Manager` n'a **pas été exécutée** : elle est écrite à la main,
à vérifier au moment de l'implémenter (étape 7 du plan).

💡 **Pourquoi dans le `WHERE` et pas après ?**

Charger 500 lignes puis en écarter 499 en Python, c'est **lire 499 lignes
qu'on n'avait pas le droit de lire**. Elles transitent en mémoire, elles
peuvent finir dans un log ou un message d'erreur. La restriction appartient à
la requête SQL.

⚠️ Et le `GET /payments/{id}` demande le même soin : un identifiant deviné
suffit, sinon.

### 8.2 ✅ Résolu le 22/09 : le lien manager → chasseur existe

Le matin, ce paragraphe décrivait un obstacle : `hunter` n'avait aucune
colonne vers son manager, et la règle « un manager voit la paie de ses
chasseurs » ne pouvait pas s'écrire. Deux pistes étaient proposées — **A**,
une colonne sur `hunter` ; **B**, dériver le lien des `search_request`.

**Tranché l'après-midi** (MPD 03 4, commit `51f4761`) — piste **A**, en plus
strict :

| Quoi | Valeur |
|---|---|
| Colonne | `hunter.id_realestatemanager`, **`NOT NULL`** |
| Cible | `real_estate_manager(id_user)` — donc un id de `"user"` |
| Cardinalité | Hunter (1,1) — RealEstateManager (0,n) |
| ADR | brouillon `md/adr-025-lien-chasseur-manager.md`, à valider |
| Base locale d'avant le 22/09 | `docker compose down -v && docker compose up -d`, ou `docker/migrations/2026-09-22_hunter_manager.sql` |

➡️ C'est ce que la branche `Manager` du §8.1 utilise.

### 8.3 Un seul compte Manager, et c'est un placeholder

Mesuré le matin : `Manager` **0**, `Admin` **0**.

Depuis l'après-midi : `Manager` **1** — `manager.migration@chassimmo.fr`
(user 25), créé par la migration parce que la colonne est `NOT NULL` et que
la source n'a aucun manager. Compte **bloqué** (même placeholder que les 24
autres), nom bidon, **pas une personne**. Les 6 chasseurs pointent vers lui.
`Admin` : toujours **0**.

➡️ La règle est écrite, mais elle reste **ni démontrable, ni testable** avec
un seul manager. Il faut de vrais comptes — **après le tuto 1**, sinon leur
mot de passe part en clair.

Proposition : **1 admin, 2 managers**. Deux, pour pouvoir montrer qu'un manager
ne voit pas les chasseurs de l'autre.

---

## 9. Le rate-limiting

⚠️ **Ce n'est pas optionnel**, et ça vient du tuto 1.

Un hachage Argon2id calibré consomme ~256 Mo et ~300 ms. Sans limite, **100
requêtes de login suffisent à saturer la RAM du serveur**.

`ADR-016` l'écrit : *« prévoir du rate-limiting sur les endpoints
d'authentification »*.

Le minimum : limiter `/auth/login` par adresse IP, et verrouiller un compte
après N échecs.

💡 **Le paradoxe à savoir expliquer** : un hachage coûteux protège les mots de
passe **et** crée un vecteur de déni de service. C'est le genre de compromis
qu'un jury aime entendre formuler.

---

## 10. Vérifier

### 10.1 Le parcours complet

**1.** Sans jeton :

```bash
curl -s -o /dev/null -w "sans jeton -> %{http_code}\n" http://localhost:8000/users
```

✅ `401`

**2.** Se connecter — noter que c'est du **form-data**, pas du JSON :

```bash
curl -s -X POST http://localhost:8000/auth/login -d "username=tuto1-final@exemple.fr&password=MotDePasseAssezLong123"
```

✅ Un `access_token`.

**3.** Avec le jeton :

```bash
curl -s -o /dev/null -w "avec jeton -> %{http_code}\n" http://localhost:8000/users -H "Authorization: Bearer <COLLER_LE_JETON>"
```

✅ `200`

**4.** Avec un jeton trafiqué — changer un caractère :

```bash
curl -s -o /dev/null -w "jeton trafique -> %{http_code}\n" http://localhost:8000/users -H "Authorization: Bearer XXX.YYY.ZZZ"
```

✅ `401`

### 10.2 Lire son propre jeton

Instructif, et ça prend 5 secondes :

```bash
docker exec fil_rouge_immobilier_api python -c "
import base64
p = '<COLLER_LE_JETON>'.split('.')[1]
print(base64.urlsafe_b64decode(p + '=' * (-len(p) % 4)).decode())
"
```

✅ Vous lisez `sub`, `role` et `exp` **sans aucune clé**. C'est normal — §1.2.

❌ Si vous y lisez autre chose (un email, une empreinte), retirez-le.

### 10.3 La checklist

| # | Vérification | ✅ |
|---|---|---|
| 1 | Sans jeton → `401` sur toutes les routes de données | ☐ |
| 2 | `/auth/login` et `/docs` restent publics | ☐ |
| 3 | Bon identifiant → un jeton | ☐ |
| 4 | Mauvais mot de passe → `401`, **même message** qu'email inconnu | ☐ |
| 5 | Jeton trafiqué ou expiré → `401` | ☐ |
| 6 | Rôle insuffisant → `403` (pas `401`) | ☐ |
| 7 | Le chasseur A ne lit pas le `payment` du chasseur B → `403` | ☐ |
| 8 | Le payload ne contient aucune donnée sensible | ☐ |
| 9 | La clé est dans `.env`, absente de git | ☐ |
| 10 | Les comptes de test sont supprimés | ☐ |

⚠️ **La ligne 7 est celle qui compte.** C'est la seule qui prouve l'ownership.
Les autres ne prouvent que l'authentification.

---

## 11. Ce qui reste ouvert

### 11.1 À décider en réunion

| # | Question | Bloque quoi |
|---|---|---|
| 1 | JWT, ou session en base ? | tout ce tuto |
| 2 | Durée du jeton ? *(proposition : 1 h)* | §2.2 |
| 3 | ~~Piste A ou B pour le lien manager → chasseur ?~~ **tranché le 22/09**, reste à valider l'ADR-025 | §8.2 |
| 4 | Combien de comptes Manager / Admin ? *(proposition : 2 et 1)* | §8.3 |
| 5 | La matrice « qui voit quoi » | §7, §8 |
| 6 | Longueur minimale d'un mot de passe ? | tuto 1, §4.2 |

### 11.2 Hors périmètre, assumé

- *Refresh token* — complexité en plus, non exigée.
- Inscription publique, « mot de passe oublié » — non exigés.
- HTTPS — un JWT en HTTP clair est interceptable, mais le projet n'est pas
  déployé.

### 11.3 Deux ADR à écrire

- **Le mécanisme d'authentification** — rien n'existe aujourd'hui.
- **La matrice d'accès** — c'est un arbitrage du groupe, il doit être tracé.

💡 Et `ADR-016` (Argon2id) est toujours « proposé » depuis le 04/09.

---

## 12. Sources

| Affirmation | Source |
|---|---|
| PyJWT est la bibliothèque de la doc FastAPI, `ALGORITHM = "HS256"`, `openssl rand -hex 32` | [fastapi.tiangolo.com — OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), doc officielle, consultée le 22/09/2026 |
| 3 parties, 140 car., payload lisible sans clé, `InvalidSignatureError`, `ExpiredSignatureError` | mesurés le 22/09, `PyJWT 2.14.0` sur `python:3.12-slim` |
| Avertissement si la clé fait moins de 32 octets | mesuré : `InsecureKeyLengthWarning`, RFC 7518 §3.2 |
| Rate-limiting sur les endpoints d'authentification | Confluence, `ADR-016` |
| Les ~90 routes viennent d'une seule fabrique | `API/src/app/routes/crud_router.py` |
| Lien `hunter` → `real_estate_manager` depuis le 22/09 après-midi (absent le matin) | `docker/init-v2/01_create_fil_rouge_immobilier.sql`, table `hunter` ; `md/adr-025-lien-chasseur-manager.md` |
| 0 compte `Manager`, 0 compte `Admin` le matin ; 1 manager placeholder l'après-midi | mesuré en base le 22/09 ; `docker/init-v2/README.md` §3.6 |
| Aucun ADR sur l'authentification | Confluence, *Journal de décisions* — `ADR-001` à `ADR-024` relus le 22/09 |
| Aucun secret dans git | `CLAUDE.md` du projet, règle 5 |

# Mots de passe et droits d'accès — ce qu'il reste à faire

> 📖 **Pour tout le groupe.** Niveau supposé : SQL, Python, Docker. Aucune
> notion de sécurité applicative supposée — hachage, JWT et RBAC sont
> expliqués ici.
>
> ⚠️ **Note rédigée avec l'IA.** Elle ne fait pas foi : sources au §8. Les
> extraits de code sont des **esquisses non testées**, pas du code à coller.
>
> 📅 22 septembre 2026. Couvre les étapes `B1`, `B2` et `B3` du plan.

---

## 1. Le constat, mesuré le 22/09

| Vérification | Résultat |
|---|---|
| Comptes en base | **24** — 18 `Client`, 6 `Hunter` |
| Comptes `Manager` / `Admin` | **0** et **0** ⚠️ |
| Mot de passe haché | ❌ aucun mécanisme |
| Route protégée | ❌ aucune, sur ~90 opérations |
| Dépendance de hachage | ❌ absente de `requirements.txt` |

### 1.1 Ce qui protège déjà — le passé

Les 24 comptes repris de l'ancien système portent tous la même valeur :

```
$2b$12$MIGRATED_PLACEHOLDER_MUST_RESET
```

Ce n'est **pas** un mot de passe, ni même un hachage valide. C'est un
placeholder délibéré : aucune entrée ne pourra jamais lui correspondre, donc
aucune connexion n'est possible sur ces comptes. Le choix est documenté dans
`02_migration.sql`. Bon réflexe, et toujours en place.

✅ Second point acquis : `UserPublic` empêche `password` de sortir dans les
réponses de l'API. Corrigé le 21/09.

### 1.2 Ce qui ne protège rien — le présent

Test effectué le 22/09 sur la base de dev :

| Étape | Résultat |
|---|---|
| `POST /users` avec `"password": "MotDePasseEnClair123"` | créé |
| `SELECT password FROM "user"` sur la ligne créée | **`MotDePasseEnClair123`** ❌ |
| `DELETE /users/{id}` | `200`, retour à 24 comptes |

La valeur est persistée telle quelle. `UserService` hérite de `BaseService`
sans rien surcharger — `create()` passe l'objet au repository sans le toucher.

➡️ **Le placeholder protège les données migrées. Rien ne protège ce qui sera
écrit ensuite.**

### 1.3 Détail à corriger au passage

Le placeholder commence par `$2b$`, préfixe **bcrypt**. Or `ADR-016` retient
**Argon2id**, dont le préfixe est `$argon2id$`. La valeur est inerte, donc sans
risque, mais elle contredit la décision. À remplacer quand le seed sera écrit.

---

## 2. `B1` — hacher les mots de passe

### 2.1 Hachage, pas chiffrement

Deux opérations souvent confondues :

| | Chiffrement | Hachage |
|---|---|---|
| Réversible | ✅ avec la clé | ❌ jamais |
| Sortie | taille variable | taille fixe |
| Usage ici | ❌ à proscrire | ✅ le bon outil |

On ne veut **pas** pouvoir retrouver le mot de passe. Une base chiffrée reste
déchiffrable par qui détient la clé — et la clé finit toujours quelque part
près de la base.

**Le principe** : on ne stocke que l'empreinte. À la connexion, on hache
l'entrée et on compare les deux empreintes. Le mot de passe en clair n'existe
que le temps de la requête, en mémoire.

### 2.2 Pourquoi pas SHA-256

Réflexe courant, et c'est un piège.

SHA-256 est conçu pour être **rapide** — qualité pour vérifier l'intégrité d'un
fichier, défaut rédhibitoire ici. Un GPU grand public calcule des **milliards**
de SHA-256 par seconde. Une attaque par dictionnaire sur une base volée devient
triviale.

Il faut une fonction **délibérément coûteuse** : une KDF *(Key Derivation
Function)*. Son temps de calcul est un paramètre, pas un accident.

### 2.3 Argon2id — décidé, confirmé le 22/09

`ADR-016` (04/09, statut *proposé*) retient **Argon2id** via `argon2-cffi`.
Vainqueur de la *Password Hashing Competition*, recommandé par l'OWASP.

Trois paramètres de coût :

| Paramètre | Effet |
|---|---|
| `time_cost` | nombre de passes — coût CPU |
| `memory_cost` | mémoire occupée par hachage |
| `parallelism` | threads utilisés |

💡 **`memory_cost` est le paramètre décisif.** Argon2 est *memory-hard* : il
exige beaucoup de RAM par calcul. Les GPU et ASIC ont énormément de cœurs mais
peu de mémoire par cœur — leur avantage s'effondre. C'est ce qui le sépare de
bcrypt.

🎯 **Cible retenue par l'ADR : 250 à 500 ms par hachage**, sur la machine qui
exécute l'API. Les valeurs ne se recopient pas depuis un blog, elles se
**mesurent** chez nous — c'est le matériel qui décide.

⚠️ Coût assumé : chaque connexion consomme ~0,3 s de CPU et plusieurs dizaines
de Mo. C'est voulu, et c'est aussi pourquoi l'endpoint de login **doit** être
rate-limité — sinon il devient un vecteur de déni de service.

### 2.4 Le sel, en deux lignes

Un **sel** est une valeur aléatoire ajoutée avant hachage. Sans lui, deux
comptes de même mot de passe produisent la même empreinte, ce qui ouvre les
attaques par table précalculée (*rainbow tables*).

✅ `argon2-cffi` génère le sel seul et l'inclut dans la chaîne de sortie, au
format PHC : `$argon2id$v=…$m=…,t=…,p=…$<sel>$<empreinte>`.

➡️ **Rien à gérer côté application, et aucune colonne à ajouter.** Les
paramètres voyagent avec l'empreinte : un hachage produit avec d'anciens
réglages reste vérifiable après leur changement.

### 2.5 Ce qu'il faut écrire

**1.** `requirements.txt` → ajouter `argon2-cffi`.

**2.** Un module dédié, `app/utils/security.py` :

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_ph = PasswordHasher()  # paramètres à calibrer, cf. §2.3

def hash_password(plain: str) -> str:
    return _ph.hash(plain)

def verify_password(stored: str, plain: str) -> bool:
    try:
        _ph.verify(stored, plain)
        return True
    except VerifyMismatchError:
        return False
```

⚠️ **Ne jamais comparer avec `==`.** `verify()` est à temps constant : sa durée
ne dépend pas du nombre de caractères corrects. Un `==` classique s'arrête au
premier octet différent, ce qui laisse fuir de l'information par le temps de
réponse (*timing attack*).

**3.** Surcharger `UserService.create()` et `.replace()`.

💡 L'architecture a été pensée pour ça — c'est écrit dans l'en-tête de
`base_service.py` : *« une sous-classe comme UserService peut surcharger
create() pour hasher le mot de passe avant d'appeler super().create(), sans que
les routers ni les repositories n'aient à changer »*. Il n'y a plus qu'à le
faire.

**4.** `check_needs_rehash()` après une connexion réussie : si les paramètres
ont durci depuis, on re-hache à la volée, sans rien demander à l'utilisateur.

**5.** Aucun `print`, aucun log, aucune exception ne doit contenir le mot de
passe en clair.

### 2.6 `B2` — séparer entrée et sortie

État actuel dans `user_router.py` :

```python
response_model=User,      # modèle d'ENTRÉE  (POST, PUT)
read_model=UserPublic,    # modèle de SORTIE (sans password)
```

🟡 **La moitié est faite.** La sortie est propre. L'entrée, non : `User` est le
modèle de table, donc le client de l'API peut poster `id`, `created_at`,
`id_role` — et le mot de passe brut.

➡️ Il manque un `UserCreate` (email, mot de passe en clair, rôle) et un
`UserUpdate`. Le modèle de table ne doit jamais servir de schéma d'entrée.

---

## 3. `B3a` — authentification

### 3.1 Deux mots à ne pas confondre

| | Question | Code HTTP |
|---|---|---|
| **Authentification** | *qui es-tu ?* | `401 Unauthorized` |
| **Autorisation** | *as-tu le droit ?* | `403 Forbidden` |

Aujourd'hui, ni l'une ni l'autre. Elles se traitent dans cet ordre.

### 3.2 Le jeton JWT

Renvoyer email + mot de passe à chaque requête est exclu. À la place :

1. `POST /auth/login` → vérification du mot de passe → **un jeton signé**.
2. Chaque requête suivante porte `Authorization: Bearer <jeton>`.

**Un JWT, c'est trois parties en base64url**, séparées par des points :
`header.payload.signature`.

⚠️ **Signé ≠ chiffré.** Le `payload` est lisible par n'importe qui — il suffit
de le décoder. La signature garantit qu'il n'a pas été **modifié**, pas qu'il
est secret. **Aucune donnée sensible dans un JWT.**

Claims utiles ici : `sub` (id utilisateur), `exp` (expiration), et le rôle.

💡 **Conséquence importante** : un JWT est *stateless*. Rien n'est stocké côté
serveur, donc **on ne peut pas révoquer un jeton émis**. Un jeton volé reste
valide jusqu'à son `exp` — d'où l'intérêt d'une durée courte. C'est le
compromis à assumer, et une question du §5.

### 3.3 Ce qu'il faut écrire

| # | Quoi |
|---|---|
| 1 | `POST /auth/login`, via `OAuth2PasswordRequestForm` (intégré à FastAPI) |
| 2 | Signature du jeton avec une clé lue dans `.env` — **jamais en dur** |
| 3 | Une dépendance `get_current_user()` : décode, vérifie, charge l'utilisateur |
| 4 | Sinon : `401` |

⚠️ **Un message d'erreur unique** pour « email inconnu » et « mot de passe
faux ». Deux messages distincts permettent d'énumérer les comptes existants.

---

## 4. `B3b` — autorisation

### 4.1 Le piège central

❌ **Vérifier le rôle ne suffit pas.**

Deux chasseurs portent le même rôle `Hunter`. Un contrôle limité au rôle
autorise le chasseur A à lire le `/payments/{id}` du chasseur B.

C'est une **élévation de privilège horizontale** (famille IDOR) — la faille la
plus fréquente sur une API CRUD comme la nôtre, et exactement là qu'un jury
appuie.

✅ **Deux contrôles, systématiquement :**

| Niveau | Question | Mécanisme |
|---|---|---|
| **RBAC** | ce rôle peut-il accéder à ce type de ressource ? | le `role` de l'utilisateur |
| **Ownership** | cette ligne précise est-elle la sienne ? | `WHERE id_hunter = :current` |

### 4.2 Où poser le contrôle

- ❌ Pas dans le router : il ne connaît pas le métier, et un autre appelant le contourne.
- ❌ Pas dans le repository : trop bas, il ne connaît pas l'utilisateur courant.
- ✅ **Dans le service** — la couche prévue pour la règle métier.

💡 **Filtrer dans le `WHERE`, pas après le chargement.** Charger 500 lignes puis
en écarter 499 en Python, c'est lire des données qu'on n'a pas le droit de
lire. La restriction appartient à la requête SQL.

⚠️ **Point d'architecture** : les ~90 routes sont générées par
`build_crud_router`. Un `dependencies=[Depends(get_current_user)]` posé sur
l'`APIRouter` qu'il construit protège **les 18 tables d'un coup**. L'ownership,
lui, reste à écrire service par service.

### 4.3 Le tableau à remplir

Les cases 🟡 sont à trancher en réunion.

| Ressource | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| Son propre compte | ✅ | ✅ | ✅ | ✅ |
| Le compte d'un autre | ❌ | 🟡 ses clients ? | 🟡 | ✅ |
| `payment` le concernant | — | ✅ | — | ✅ |
| `payment` d'un autre chasseur | ❌ | ❌ | 🟡 les siens ? | ✅ |
| `commission_scale` | ❌ | 🟡 le sien ? | 🟡 | ✅ |
| `estate`, `picture` | ✅ | ✅ | ✅ | ✅ |
| `mandate`, `sale` | 🟡 les siens | 🟡 les siens | 🟡 | ✅ |

### 4.4 ⚠️ Un obstacle mesuré : le lien manager → chasseur n'existe pas

Vérifié dans le schéma le 22/09 :

- `hunter` n'a **aucune** colonne `id_manager`.
- `real_estate_manager` n'a **aucune** référence vers `hunter`.
- Aucune table de liaison entre les deux.

➡️ **La phrase « son manager » n'a aujourd'hui aucun support en base.** On ne
peut pas écrire la règle, faute de savoir qui encadre qui.

Le seul endroit où les deux se croisent est `search_request`, qui porte à la
fois `id_hunter` et `id_realestatemanager`. Deux pistes :

| Piste | Principe | Coût |
|---|---|---|
| **A** | ajouter `hunter.id_manager` (FK nullable) | une migration, mais explicite et durable |
| **B** | dériver le lien des `search_request` communes | zéro migration, mais indirect et fragile |

💡 Recommandation : **piste A**. Un rattachement hiérarchique est un fait métier
stable, pas une conséquence d'un historique de dossiers.

### 4.5 Ce qu'il faut écrire

| # | Quoi |
|---|---|
| 1 | Le tableau du §4.3, validé, puis porté en ADR |
| 2 | Une dépendance `require_role(*roles)` → `403` sinon |
| 3 | Le filtrage par appartenance dans les services concernés |
| 4 | Des tests qui prouvent qu'un accès interdit renvoie bien `403` |

---

## 5. À décider en réunion

1. 👔 **Combien de comptes `Manager` et `Admin` ?** Zéro des deux aujourd'hui.
   Proposition : **1 admin, 2 managers** — deux, pour pouvoir démontrer qu'un
   manager ne voit pas les chasseurs de l'autre.
2. 🔗 **Piste A ou B pour le lien manager → chasseur ?** (§4.4)
3. ⏱️ **Durée de validité du jeton ?** Sans révocation possible (§3.2), c'est le
   seul garde-fou. Proposition : 1 h, sans *refresh token* — hors périmètre.
4. 🔑 **Que fait-on des 24 comptes migrés ?** Leur serrure est bouchée, rien ne
   presse. Proposition : mots de passe hachés dans le seed, pour pouvoir se
   connecter en démo.
5. 📋 **Périmètre** : inscription publique, changement de mot de passe, reset par
   email ? Chacun est un chantier. Le sujet ne les exige pas.
6. 📏 **Politique de mot de passe** : longueur minimale ? Refus des mots de passe
   connus comme compromis ? L'OWASP privilégie la longueur sur la complexité.

---

## 6. Plan et dépendances

| # | Étape | Dépend de | Poids |
|---|---|---|---|
| 0 | ~~Créer le rôle `Admin`~~ | — | ✅ **fait le 22/09** |
| 1 | `argon2-cffi` + `security.py` + calibrage | rien | 🟢 |
| 2 | `UserCreate` / `UserUpdate`, hachage dans le service | 1 | 🟢 |
| 3 | Créer les comptes `Manager` et `Admin` | 2 | 🟢 |
| 4 | `POST /auth/login` + JWT + `get_current_user` | 2 | 🟠 |
| 5 | `401` par défaut sur `build_crud_router` | 4 | 🟢 |
| 6 | `require_role` — RBAC | 5 + §4.3 validé | 🟠 |
| 7 | Filtrage par appartenance | 6 + §4.4 tranché | 🔴 |
| 8 | Tests `401` / `403` / accès légitime | base de test (`A2`) | 🟠 |

⚠️ **Le verrou réel est ailleurs** : l'étape 8 attend la **base de test isolée**
(`A2`). Sans elle, chaque test écrit dans la base de dev. On peut implémenter la
sécurité sans `A2`, mais pas la **prouver** — et en soutenance, seule la preuve
compte.

💡 **Les étapes 1 et 2 ne dépendent de rien.** Elles peuvent démarrer tout de
suite, sans attendre la réunion.

---

## 7. Pour la soutenance

### 7.1 Une affirmation à corriger

Le point d'étape du 21/09 écrit : *« Le cahier des charges demande que la paie
d'un chasseur ne soit visible que par lui et son manager. »*

⚠️ **C'est inexact.** En remontant à la source, la phrase vient d'un **exemple
de rédaction** dans un modèle de document — la section s'intitule « Exigences
non fonctionnelles **(extrait)** ». Ce n'est pas une exigence client.

Présenter un exemple pédagogique comme une contrainte contractuelle est
attaquable, et vérifiable en trente secondes par un jury.

### 7.2 L'argument solide

Le **RGPD** est explicitement exigé, et le sujet précise que ces exigences « ne
sont **pas optionnelles** ; leur absence est pénalisante en jury ». Il demande
la protection des données **dès la conception**.

➡️ **Formulation à retenir** : on restreint les accès au titre du principe de
minimisation (RGPD). Le détail du « qui voit quoi » est un **arbitrage du
groupe**, tracé dans un ADR — celui du §4.3.

C'est exact, et bien plus difficile à contester.

### 7.3 Deux décisions à faire avancer

- `ADR-016` (Argon2id) : **« proposé » depuis le 04/09**. À valider.
- La matrice d'accès du §4.3 : mérite son propre ADR.

---

## 8. Sources et vérification

| Affirmation | Source |
|---|---|
| Argon2id retenu, via `argon2-cffi`, cible 250-500 ms | Confluence, *Journal de décisions*, `ADR-016` |
| `password VARCHAR(255)` déjà dimensionné | `docker/init-v2/01_create_fil_rouge_immobilier.sql`, table `user` |
| Le placeholder des 24 comptes | `docker/init-v2/02_migration.sql`, bloc `1. USERS` |
| `UserPublic` protège la sortie | `API/src/app/models/user_model.py` |
| `User` sert encore de modèle d'entrée | `API/src/app/routes/user_router.py` |
| Aucun hachage dans le service | `API/src/app/services/user_service.py` — 7 lignes |
| L'architecture prévoit la surcharge | `API/src/app/services/base_service.py`, en-tête |
| Les ~90 routes sont génériques | `API/src/app/routes/crud_router.py` |
| Aucun lien `hunter` ↔ `real_estate_manager` | schéma de référence, ces deux tables |
| Le rôle `Admin` manquait | `docker/migrations/2026-09-22_role_admin.sql` |
| Le RGPD n'est pas optionnel | `BASE/Readme.md`, section RGPD |
| L'exigence d'accès est un **exemple** | `BASE/documents utiles/CAHIER-DES-CHARGES-TECHNIQUE.md`, « Exigences non fonctionnelles (extrait) » |

### 8.1 Rejouer le comptage des rôles

Depuis `docker/`, ouvrir une session psql :

```bash
docker exec -it fil_rouge_immobilier_db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

Puis :

```sql
SELECT r.id, r.wording, count(u.id)
FROM role r LEFT JOIN "user" u ON u.id_role = r.id
GROUP BY r.id, r.wording ORDER BY r.id;
```

Attendu : **4 lignes** — Client 18, Hunter 6, Manager 0, Admin 0. `\q` pour
sortir.

### 8.2 Rejouer la preuve du §1.2

⚠️ Ces trois étapes **écrivent dans la base de dev**. La troisième n'est pas
optionnelle.

**1.** Créer un compte de test, et noter l'`id` renvoyé :

```bash
curl -s -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"email":"test-preuve-hash@exemple.fr","password":"MotDePasseEnClair123","is_activated":true,"id_role":1}'
```

**2.** Lire ce qui a été persisté, dans la session psql du §8.1 :

```sql
SELECT id, email, password FROM "user"
WHERE email = 'test-preuve-hash@exemple.fr';
```

Attendu : **`MotDePasseEnClair123`**, en clair. C'est le problème.

**3.** Nettoyer — remplacer `NN` par l'`id` de l'étape 1 :

```bash
curl -s -X DELETE http://localhost:8000/users/NN
```

Attendu ensuite : 24 comptes.

---

## Lexique

| Terme | Définition |
|---|---|
| **KDF** | fonction de dérivation de clé — lente par construction |
| **Argon2id** | la KDF retenue ; *memory-hard*, donc hostile aux GPU |
| **Sel** | aléa par mot de passe ; neutralise les tables précalculées |
| **Format PHC** | encodage standard qui embarque paramètres, sel et empreinte |
| **Timing attack** | fuite d'information par le temps de réponse |
| **JWT** | jeton signé, lisible, non révocable, porté par `Authorization: Bearer` |
| **Stateless** | aucun état serveur — d'où l'impossibilité de révoquer |
| **RBAC** | contrôle d'accès par rôle |
| **Ownership** | contrôle d'appartenance de la ligne |
| **IDOR** | accès à la ressource d'autrui via son identifiant |
| **401 / 403** | non authentifié / authentifié mais sans droit |
| **Minimisation** | principe RGPD : n'accéder qu'au strictement nécessaire |
| **ADR** | décision d'architecture tracée, sur Confluence |

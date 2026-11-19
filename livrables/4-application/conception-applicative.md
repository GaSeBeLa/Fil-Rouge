# 🧱 Dossier de conception applicative — API Fil Rouge Immobilier

> **Dossier de conception applicative + maquettes** (BC03).
> Exigé par `GRILLE-EVALUATION.md` (StarterPack - BASE) : « Maquettes + patterns justifiés, 3-5 pages ».
> État du code : dépôt `Fil-Rouge-API`, commit **`db2ae3c`** (2026-11-19). **96 opérations**, recomptées par `app.openapi()`.
> Les maquettes : [`maquettes-espace-acquereur.html`](./maquettes-espace-acquereur.html), dans ce dossier.
> Brouillon du Glaude, **à relire par le groupe**.

---

## 1. Ce que l'on construit

- Une **API REST** (FastAPI + SQLModel, sur PostgreSQL 16) pour un service de **chasse immobilière** : un particulier dépose une demande, un chasseur lui trouve des biens, une vente rémunère le chasseur.
- **Pas de site web** dans le périmètre : l'API est le produit. Les maquettes du § 5 montrent ce qu'un futur site afficherait, et **quelle route** nourrit chaque écran.
- Autour de l'API : Airflow importe les annonces, Elasticsearch sert la recherche de biens, MinIO garde les fichiers (schémas `livrables/3-architecture/03` et `04`).

## 2. L'architecture : trois couches

Une requête traverse trois couches, **toujours dans le même ordre** (`API/src/app/main.py`, en-tête) :

| Couche | Dossier | Son seul travail | Ce qu'elle ne connaît pas |
| --- | --- | --- | --- |
| **Route** | `routes/` | recevoir la requête HTTP, vérifier les droits, traduire une erreur métier en code HTTP | la base |
| **Service** | `services/` | les règles métier : hacher un mot de passe, calculer une rémunération, « le sien » | FastAPI, HTTP |
| **Repository** | `repositories/` | lire et écrire en base, par SQLModel | les règles, HTTP |

- ➡️ Une couche ne parle qu'à **celle du dessous**. Le trajet complet d'une requête, avec ses codes 401, 422, 403, 404 et 200 : `livrables/3-architecture/02-trajet-requete.md`.
- **Pourquoi** : on peut changer une règle métier sans toucher au HTTP, et **tester un service sans base**. Les 194 tests unitaires le font, avec une base factice (`rapport-tests.md`, § 3.1).

## 3. Les patterns, et pourquoi chacun

| Pattern | Où dans le code | Le problème qu'il règle |
| --- | --- | --- |
| **Fabrique de routeurs** | `routes/crud_router.py`, `build_crud_router` | les 4 routes (liste, lire, créer, modifier) sont identiques pour les 21 tables CRUD : écrites **une fois**, pas 21 |
| **Repository générique** | `repositories/base_repository.py`, `BaseRepository[Modèle]` | le CRUD de base, typé par table ; une table ajoute ses requêtes à elle (`UserRepository.get_by_email`) |
| **Service + crochets** | `services/base_service.py` | un service surcharge un seul geste : `UserService.create` hache le mot de passe ; `visible_rows` dit « le sien » |
| **Injection de dépendances** | `Depends(...)` de FastAPI : `get_session`, `get_principal`, `require_api_key` | la session, le compte connecté et la clé arrivent tout prêts ; un test les remplace (`dependency_overrides`) |
| **Modèles d'entrée et de sortie séparés** | `UserCreate`, `UserUpdate`, `UserPublic` | `password` entre, mais **ne sort jamais** ; le PUT accepte des champs facultatifs |
| **Erreurs métier traduites à un seul endroit** | `utils/exceptions.py`, puis `crud_router.py` | un service lève `NotFoundError`, `ConflictError` ou `ForbiddenError` ; seule la route les change en 404, 409 ou 403 |
| **Fermé par défaut** | `require_roles` ; `read_roles`, `write_roles`, `create_roles` | une route qui ne dit pas ses rôles est **fermée à tous** (403), jamais ouverte par oubli |
| **Middleware** | `conf/logging.py`, `access_log_middleware` | une ligne JSON par requête (méthode, chemin, code, durée, rôle), sans mot de passe, ni jeton, ni email |
| **La base juge** | les `CHECK` de `docker/init-v3/01` | les formats et les règles croisées vivent en SQL : ni l'API, ni un script SQL direct ne les contournent |

### Les choix écartés

| Écarté | Pourquoi |
| --- | --- |
| `PATCH` | `PUT` remplace la ligne : plus simple à raisonner pour un projet de cette taille (`main.py`) |
| `DELETE` | effacer = **désactiver et anonymiser**, jamais supprimer : le RGPD et la comptabilité (ADR-049) |
| Le rôle écrit dans le jeton | un compte désactivé garderait ses droits jusqu'à la fin du jeton ; on le relit en base à chaque appel (ADR-052) |
| Une validation Python des formats | elle doublerait les `CHECK` de la base, avec le risque qu'ils divergent |

## 4. Extraits de code commentés

### 4.1 Une table entière en une déclaration

```python
# routes/picture_router.py
router = build_crud_router(
    service=PictureService(PictureRepository()),
    prefix="/pictures",
    tag="picture",
    response_model=Picture,
    read_roles=ALL_ROLES,           # tout compte connecté lit les photos
    write_roles=(ADMIN,),           # seul l'Admin les modifie
    create_roles=(HUNTER, MANAGER), # un chasseur ou un manager les ajoute
)
```

- 4 routes, les droits par rôle et les codes d'erreur, en **10 lignes**. Les rôles se lisent dans l'annexe d'ADR-027.
- Les commentaires de fin de ligne sont ajoutés pour cette note ; le code porte les siens, plus longs.

### 4.2 Une règle métier, à sa place

```python
# services/base_service.py:97 — le crochet ; un service le surcharge
# pour ne rendre que « les siennes » (ADR-027, point 2)
def visible_rows(self, viewer: "Principal") -> Optional[ColumnElement[bool]]:
```

- Le filtre part **dans la requête SQL** (`where`), jamais en Python après coup : une liste ne charge jamais les lignes d'un autre (`base_repository.py`, en-tête).

### 4.3 L'entrée revalidée avant la base

- Un modèle de table SQLModel **ne valide pas** ce qu'on lui donne. Mesuré le 2026-10-05 : un prix `199999.5` était arrondi en silence à 200 000.
- `_validated` (`crud_router.py`) revalide le corps avec `model_validate` : une entrée invalide rend **422**, avant d'atteindre la base.

## 5. Les maquettes

Six écrans, dessinés dans [`maquettes-espace-acquereur.html`](./maquettes-espace-acquereur.html). Sous chaque écran : la route de l'API qui le nourrit.

| Écran | Pour qui | Route de l'API | User story |
| --- | --- | --- | --- |
| 1. Déposer une demande | visiteur | `POST /search-requests/submit` | 01, @formulaire |
| 2. Finaliser son compte | particulier | `POST /auth/activate` | 01, @creation-compte |
| 3. Les biens proposés | particulier | `GET /estate-proposed` | 02 |
| 4. La fiche d'un bien, et sa décision | particulier | `GET /estates/{id}`, `GET /pictures`, `PUT /estate-proposed/{id}` | 02 |
| 5. Mes demandes | chasseur | `GET /search-requests` (« les siennes ») | 04 |
| 6. Les suggestions du jour | chasseur | `POST /search-requests/{id}/suggestions` | 05 |

- Les maquettes suivent la **note d'accessibilité PSH** : étiquettes visibles, cibles d'au moins 24 px, texte alternatif des photos (`picture.alt_text`), erreurs dites en texte.

## 6. Limites

- ⚠️ **Pas de front** : les maquettes sont des dessins, pas des écrans codés.
- ⚠️ L'en-tête de `main.py` est en partie périmé : « 11 fois », et « pas encore nécessaire » pour le hachage, qui est fait depuis (`UserService`). Le schéma a **22** tables ; **21** ont un routeur CRUD commun (compté le 2026-11-19).

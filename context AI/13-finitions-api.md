> **QUAND LIRE** : on joue une fiche `FIN*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache FIN<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier FIN — Finitions de l'API : erreurs et Swagger

**Ouvert.** le 2026-10-14.

**À quoi il sert.** L'API marche, mais ses erreurs n'aident pas : tout refus de
la base rend la même phrase `409`, une panne imprévue part en `500` sans trace
lisible, et le Swagger ne dit pas quel numéro mettre dans `id_client` (TODO 10).

**Estimé.** 4 fiches · ≈20 $ — ≈5,05 $/fiche sur 4 clos (le 2026-10-14).

**Fait.** Rien. Ouvert le 2026-10-14, cadré en 2 fiches, `FIN1` à jouer.

**Session** : da42f1a3-d291-47c1-a710-979822a907ab

## Le socle commun

Le code vit dans `../Fil-Rouge-API/` ; tout chemin ci-dessous s'y lit.
Vérification : depuis `../Fil-Rouge-API/docker/`,
`docker compose exec -T api python -m pytest -q` (911 passed, 8 skipped,
6 xfailed au 2026-10-13) ; du Python touché passe `pyright`.

| Symbole | Fichier | Ce qu'il fait aujourd'hui |
|---|---|---|
| `_WRITE_CONFLICT_DETAIL`, `_DELETE_CONFLICT_DETAIL` | `API/src/app/repositories/base_repository.py` | les deux seules phrases d'un refus de la base |
| `_commit_or_raise`, `insert_pending` | idem | attrapent `IntegrityError`, `rollback`, lèvent `ConflictError(<phrase>)` |
| `ConflictError` | `API/src/app/utils/exceptions.py` | erreur neutre, traduite en `409` par les routes (`HTTPException(409, detail=str(exc))`) |
| `validation_error_without_input` | `API/src/app/main.py` | seul gestionnaire d'erreur de l'app (`422`) ; aucun pour `Exception` |
| `_probe_new_signup` | `API/src/app/services/signup_service.py` | DRO11 : un email connu rejoue le chemin d'un email neuf, même réponse pour tous |

Décisions de Seb (Discord, 2026-10-14) :
- **409 = phrase + nom (A)** : le pilote est `psycopg2` ; `exc.orig.pgcode`
  (`23505` unique, `23503` clé étrangère, `23514` CHECK) et
  `exc.orig.diag.constraint_name` disent quoi et où. Une phrase en français
  par sorte, suivie du nom de la contrainte ; quelques contraintes courantes
  (email du compte, par exemple) ont leur phrase propre. Le nom manque :
  la phrase de la sorte seule, jamais un message vide.
- **500 = message neutre + numéro (A)** : un numéro court
  (`uuid4().hex[:8]`), écrit dans la réponse et dans le log avec la pile
  (`logging.getLogger(__name__).exception`).
- **2 fiches, préfixe `FIN`.**

Invariants :
- ❌ **Jamais la valeur refusée dans la réponse** : ni `diag.message_detail`,
  ni `str(exc.orig)` — ils recopient l'email ou l'id d'un autre (fuite).
- L'inscription garde **la même réponse** pour un email connu et un inconnu :
  les tests de DRO11 restent verts sans être modifiés.
- Aucun code HTTP ne change ; aucun paquet ajouté (`logging` de la bibliothèque standard).

Hors du chantier : les `409` des règles métier (`ConflictError` levée avec sa
propre phrase par un service) gardent leur texte ; pas de traduction des `422`.

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `FIN1` | Nommer la règle dans le `409` et tracer les `500` | rien |
| `FIN2` | Dire « numéro du compte » dans le Swagger | rien |

Les deux fiches sont indépendantes et peuvent se jouer dans n'importe quel ordre.

---

<!-- FICHE:FIN1 -->
## FIN1 [x] — Nommer la règle dans le `409` et tracer les `500`

**Session** : d91d2486-ccc7-4872-9632-f6e1b9331d93
**Dépend de** : rien.
**Fichiers** : `API/src/app/repositories/base_repository.py`, un nouveau `API/src/app/utils/constraint_messages.py`, `API/src/app/main.py`, `API/tests/test_base_repository.py`, `API/tests/test_crud_router.py`, `API/tests/integration/test_users_db.py`, un nouveau `API/tests/integration/test_erreurs_api.py`.

**Prompt**
1. Dans `constraint_messages.py`, écris `conflict_detail(exc: IntegrityError, deleting: bool) -> str`
   selon le socle : phrase de la sorte (`pgcode`), puis le nom de la
   contrainte ; un petit dictionnaire nom → phrase pour les contraintes
   courantes, à choisir en lisant `docker/init-v3/01_create_fil_rouge_immobilier.sql`
   (les `UNIQUE` d'un formulaire, d'abord l'email). Une suppression bloquée (`23503` en
   `delete`) dit « encore référencée par <contrainte> ».
2. `_commit_or_raise` et `insert_pending` lèvent `ConflictError(conflict_detail(...))`.
   Supprime les deux constantes devenues mortes ; grep de leur texte dans les
   deux dépôts (« Ramasser sa poubelle »), les tests qui le recopient suivent.
3. Dans `main.py`, un gestionnaire pour `Exception` : numéro, log avec la pile,
   `500` `{"detail": "Erreur interne. Référence : <numéro>."}`. ⚠️ À vérifier
   avant d'écrire le test : Starlette relance l'exception après la réponse,
   d'où `TestClient(app, raise_server_exceptions=False)`.
4. Commentaires, en-têtes et doc Swagger des routes qui citent l'ancienne phrase : à jour.

**Critère de fin**
`test_erreurs_api.py` vert, avec trois cas : un email en double sur
`POST /users` → `409` dont le `detail` nomme la contrainte et **ne contient
pas** l'email envoyé ; un `id_client` inexistant → `409` qui nomme la clé
étrangère ; une route forcée à lever `RuntimeError` → `500` avec une
référence, la même référence dans `caplog`. Suite complète verte, compte brut
avant et après ; `pyright` 0 erreur sur les fichiers touchés. Mutants :
`conflict_detail` rend une phrase fixe → le test du doublon tombe ; retirer
le gestionnaire `Exception` → le test du `500` tombe.
<!-- /FICHE -->

---

<!-- FICHE:FIN2 -->
## FIN2 [ ] — Dire « numéro du compte » dans le Swagger

**Dépend de** : rien.
**Fichiers** : les modèles de `API/src/app/models/` qui portent `id_client`, `id_hunter`, `id_realestatemanager` ou `id_author` (8 au 2026-10-14 : à recompter par grep), `API/src/app/models/search_request_model.py`, un nouveau test `API/tests/test_openapi_ids.py`.

**Prompt**
1. Grep des champs `id_client`, `id_hunter`, `id_realestatemanager`, `id_author`
   dans `models/` : la liste mesurée va au compte rendu.
2. Sur chacun, `Field(description=...)` : « Numéro du compte (`user.id`) du
   client » (du chasseur, du manager, de l'auteur), et pour les trois
   premiers « pas `client.id` » (resp. `hunter.id`, `real_estate_manager.id`) : la table de profil a
   son propre `id`, c'est le piège soulevé par Gabriel le 2026-10-14.
   Ne change ni le type, ni la clé étrangère.
3. `search_request_model.py`, commentaire de `status` : compte d'abord, sur
   la base de dev, `SELECT status, count(*) FROM search_request GROUP BY status`
   et relis le `CHECK` de `status` dans `01_create_fil_rouge_immobilier.sql` ;
   réécris le commentaire d'après ces deux mesures (l'audit du 2026-10-12, P6,
   disait `launched`, pas `confirmed`), sans « hypothèse à confirmer » s'il est tranché.

**Critère de fin**
`test_openapi_ids.py` vert : il parcourt `app.openapi()` et vérifie que
chaque champ `id_client`, `id_hunter`, `id_realestatemanager` de chaque schéma
porte « user.id » dans sa description (compte brut des champs vérifiés).
Suite complète verte, compte brut ; `pyright` 0 erreur sur les fichiers
touchés. Mutant : retirer la description d'un seul modèle → le test tombe.
<!-- /FICHE -->

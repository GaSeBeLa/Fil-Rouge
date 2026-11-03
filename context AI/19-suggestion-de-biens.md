> **QUAND LIRE** : on joue une fiche `SUG*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache SUG<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier SUG — Moteur de suggestion de biens et cohérence des propositions

**Ouvert.** le 2026-11-03.

**À quoi il sert.** Le chasseur demande des biens qui collent aux critères de son client, sans biens vendus ni déjà vus.
Le chantier ferme aussi trois trous de cohérence trouvés par Gabriel : la signature sans critères, le PUT libre du client, et l'offre mêlée à la proposition.

**CLOS** le 2026-11-03. Ne se rejoue pas — ne sert plus qu'à relire son socle.

**Fait.** SUG1..SUG8 (2026-11-03) : Moteur de suggestion POST /search-requests/{id}/suggestions (10 biens max, sans vendus ni déjà vus), état de la sélection, décision et offre du client, mandat refusé sans critères — estimé non noté · cadré 8 · joué 8 fiches 25,63 $.

**Session** : 1abb9954-636f-4727-aa4a-97bd9123c07f

## Le socle commun

- **Où.** Le code vit dans `../Fil-Rouge-API/` (chemins `API/…` et `docker/…` ci-dessous). Les décisions et leurs sources sont dans `md/journal/2026-11-02-suggestion-de-biens.md` (§ 2, 4, 7, 8, 8.1). Elles sont votées sur Discord : on ne les rediscute pas en fiche.
- **Convention.** Une règle entre tables vit dans le service, sans trigger : `ConflictError` rend 409, `ForbiddenError` rend 403. Un PUT remplace la ligne entière. L'API n'a **pas de DELETE** (`API/src/app/routes/crud_router.py`, en-tête).
- **Tests.** Depuis `../Fil-Rouge-API/docker/` : `docker compose up -d`, puis `bash docker/create_test_db.sh` depuis `../Fil-Rouge-API/`, puis `docker compose exec -T api python -m pytest -q -p no:cacheprovider`. Seb a autorisé Docker et la recréation de `fil_rouge_test` (Discord, 2026-11-03). La base de dev n'est **pas** touchée, et `docker-compose.yml` ne se modifie pas.
  - Fixtures : `db_client` (`API/tests/integration/conftest.py`), `acting_as` (`API/tests/conftest.py`).
  - Liste des tests à garder verts : `vlp.py concernes`.
- **Schéma.** `docker/init-v3/01_create_fil_rouge_immobilier.sql` fait foi. Une colonne neuve va **à la fois** dans ce fichier et dans une migration `docker/migrations/v2-vers-v3/<NN>_<nom>.sql`, au numéro suivant le plus grand (49 au 2026-11-03).
  - La migration s'écrit sur le modèle de `48_historique-des-prix.sql` : en-tête POURQUOI / POUR QUI / QUOI / COMMENT, rejouable sans erreur.
  - Le banc `API/tests/integration/test_banc_v2_v3.py` doit rester IDENTIQUE.
- **Ce qui sert de modèle, à réutiliser sans le recréer.**

| Symbole | Fichier | Ce qu'il fait |
|---|---|---|
| `fields_changed_outside` | `API/src/app/services/base_service.py` | rend les champs changés hors d'une liste permise |
| `SearchRequestService.replace_visible` | `API/src/app/services/search_request_service.py` | 403 sur un champ que le rôle ne change pas (`ASSIGN_FIELDS`) |
| `EstateProposedService._check_proposal` | `API/src/app/services/estate_proposed_service.py` | P19 : un bien proposé doit être dans la sélection de la demande |
| `MandateService._launch_request` | `API/src/app/services/mandate_service.py` | la signature passe la demande à `launched` |
| `SignupService.submit` | `API/src/app/services/signup_service.py` | crée compte, fiche client et demande en une transaction |
| `build_query` | `API/src/app/services/estate_search_service.py` | requête `bool` d'Elasticsearch, sur l'index `estates` |
| `estates_for_sale` | `API/src/app/scripts/seed_volume.py` | les biens jamais vendus (`sale.id_estate`) |
| route `/{item_id}/payment` | `API/src/app/routes/sale_router.py` | modèle d'une route d'action hors CRUD |
| `handles_request` | `API/src/app/services/hunter_rows.py` | ce chasseur suit-il cette demande ? |

- **Ramasser sa poubelle** (`CLAUDE.md`). Chaque fiche met à jour, dans le même commit :
  - les en-têtes et docstrings touchés ;
  - `API/README.md` si une route ou une table change ;
  - la matrice `md/securite/matrice-droits-crud-par-role.md` si un droit change.
- **Dehors.**
  - Les droits du chasseur IA (ADR-058) : ce sera le chantier suivant, voté le 2026-11-03.
  - Les documents de la phase 4.
  - Le DAG de nuit.
  - `recherche_ref` à l'import.
  - Le chargement de `recherches.csv`.

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `SUG1` | Limiter le PUT du client à sa note et son commentaire | rien |
| `SUG2` | Refuser la signature d'un mandat sans critères | rien |
| `SUG3` | Faire naître la demande déposée avec budget et type | rien |
| `SUG4` | Donner un état à chaque bien de la sélection | rien |
| `SUG5` | Enregistrer la décision du client sur un bien proposé | rien |
| `SUG6` | Ouvrir la route de l'offre du client | `SUG1`, `SUG5` |
| `SUG7` | Traduire des critères en requête Elasticsearch | rien |
| `SUG8` | Ouvrir la route des suggestions | `SUG4`, `SUG7` |

- SUG1, SUG2, SUG3 et SUG7 sont indépendantes.
- SUG4 et SUG5 touchent toutes deux le SQL v3 et le banc : elles se jouent l'une **après** l'autre, jamais en parallèle.

---

<!-- FICHE:SUG1 -->
## SUG1 [x] — Limiter le PUT du client à sa note et son commentaire

**Session** : 673e24d2-f496-48d7-b069-a1ee74532d62
**Dépend de** : rien.
**Fichiers** : `API/src/app/services/estate_proposed_service.py`, `API/tests/integration/test_propositions_visites.py` (ajout pur), `md/securite/matrice-droits-crud-par-role.md`.

**Prompt**
Aujourd'hui, un client peut tout réécrire par `PUT /estate-proposed/{id}` : statut, montant, `comment_hunter`. Gabriel l'a testé, et l'API rend 200.
- Surcharge `replace_visible` dans `EstateProposedService`, sur le modèle de `SearchRequestService.replace_visible`.
- Pour le rôle `Client`, seuls `client_priority` et `comment_client` peuvent changer. Tout autre champ changé rend 403 (`fields_changed_outside`).
- Le chasseur garde ses droits actuels.
- Écris d'abord le test : un client qui passe `proposition_status` à `accepted` reçoit 403, et la ligne est inchangée en base. Un client qui change `client_priority` reçoit 200.

**Critère de fin**
- Le nouveau test échoue avant le code, sortie recopiée, puis passe.
- Mutant : retirer `proposition_status` du contrôle, par exemple en ajoutant ce champ à la liste permise. Le test 403 doit retomber.
- Toute la suite reste verte ; donner le nombre de `passed`.
<!-- /FICHE -->

---

<!-- FICHE:SUG2 -->
## SUG2 [x] — Refuser la signature d'un mandat sans critères

**Session** : 673e24d2-f496-48d7-b069-a1ee74532d62
**Dépend de** : rien.
**Fichiers** : `API/src/app/services/mandate_service.py`, `API/tests/integration/test_signature_vente.py`, `API/src/app/scripts/seed_demo.py`, `API/src/app/scripts/seed_volume.py`, et les tests qui signent un mandat sans critères (à lister par `grep -rln signature_date API/tests`).
**Tests** : modifiés — les tests qui signent un mandat sans aucun `criteria` doivent d'abord en créer un : la règle M1 (votée le 2026-11-03) rend cette signature impossible.

**Prompt**
- Dans `MandateService`, à la pose de `signature_date` (dans `create` comme dans `replace`, là où `_launch_request` est appelé) : si la demande `id_search_request` n'a **aucune** ligne `criteria`, lève `ConflictError("La demande n'a aucun critère : le mandat ne peut pas être signé.")`.
- Un mandat sans `signature_date` (statut `pending_signature`) reste possible sans critères.
- Écris d'abord les tests d'intégration :
  - signature sans critères → 409, et la demande n'est pas passée à `launched` ;
  - signature avec un critère → 201 ;
  - mandat non signé sans critères → 201.
- Puis adapte les seeds et les tests existants qui signent sans critères.

**Critère de fin**
- Les tests neufs sont rouges avant le code, puis verts.
- Mutant : supprimer la vérification. Le test 409 retombe.
- `seed_volume` et `seed_demo` tournent sur `fil_rouge_test` sans 409.
- Toute la suite reste verte ; donner le nombre de `passed`.
<!-- /FICHE -->

---

<!-- FICHE:SUG3 -->
## SUG3 [x] — Faire naître la demande déposée avec budget et type

**Session** : 673e24d2-f496-48d7-b069-a1ee74532d62
**Dépend de** : rien.
**Fichiers** : `API/src/app/services/signup_service.py`, `API/src/app/routes/signup_router.py` (en-tête), `API/tests/integration/test_demande_avant_compte.py`.
**Tests** : modifiés — les formulaires des tests existants doivent porter les deux champs devenus obligatoires (vote M2 du 2026-11-03).

**Prompt**
- Ajoute à `SearchRequestSubmission` deux champs obligatoires :
  - `budget_max`, un `int` > 0, en euros ;
  - `estate_type`, pris dans les 10 types du `CHECK` de `criteria`.
- Dans `SignupService.submit`, crée dans la même transaction la 1ʳᵉ version de `criteria` de la demande :
  - `id_author` = le compte du visiteur (vote du 2026-11-03), sans `id_previous_version` ;
  - `country_iso` = celui du formulaire.
- Un email déjà connu : la demande et ses critères se rattachent à son compte. La réponse reste la même pour tous : « Demande reçue. », sans id.
- Écris d'abord les tests :
  - un dépôt crée exactement 1 `criteria`, avec le bon budget, le bon type et le bon auteur ;
  - un budget nul rend 422 ;
  - un échec de la base n'écrit rien.

**Critère de fin**
- Les tests sont rouges avant le code, puis verts.
- Mutant : ne plus créer le `criteria`. Le test « 1 criteria » retombe.
- Toute la suite reste verte ; donner le nombre de `passed`.
<!-- /FICHE -->

---

<!-- FICHE:SUG4 -->
## SUG4 [x] — Donner un état à chaque bien de la sélection

**Session** : 673e24d2-f496-48d7-b069-a1ee74532d62
**Dépend de** : rien.
**Fichiers** :
- `docker/init-v3/01_create_fil_rouge_immobilier.sql` (table `estate_searchrequest`) ;
- `docker/migrations/v2-vers-v3/50_etat-de-la-selection.sql` (neuf) ;
- `API/src/app/models/estate_search_request_model.py` ;
- `API/src/app/services/estate_proposed_service.py` ;
- `API/src/app/scripts/seed_demo.py`, `API/src/app/scripts/seed_volume.py` ;
- `API/tests/integration/test_constraints_db.py` (ajout pur), `API/README.md`.

**Tests** : modifiés — les tests qui proposent un bien de la sélection doivent d'abord le marquer `kept` (règle P19 renforcée, acceptée par Seb le 2026-11-03).

**Prompt**
- Ajoute `status VARCHAR(20) NOT NULL DEFAULT 'suggested' CHECK (status IN ('suggested', 'kept', 'dismissed'))` à `estate_searchrequest`, dans le SQL v3 **et** dans la migration 50.
- Les lignes existantes passent à `kept` : elles ont été choisies par un chasseur.
- Le chasseur change l'état par le PUT, qui existe déjà.
- Renforce P19 dans `EstateProposedService._check_proposal` : on ne propose qu'un bien de la sélection **au statut `kept`**. Sinon, 409.
- Les seeds marquent `kept` les biens qu'ils proposent.
- Tests d'abord :
  - un statut hors liste est refusé par la base ;
  - proposer un bien `suggested` ou `dismissed` rend 409 ;
  - proposer un bien `kept` rend 201.

**Critère de fin**
- Les tests sont rouges avant le code, puis verts.
- Mutant : accepter `suggested` dans `_check_proposal`. Le test 409 retombe.
- Le banc v2/v3 rend IDENTIQUES.
- Toute la suite reste verte ; donner le nombre de `passed`.
<!-- /FICHE -->

---

<!-- FICHE:SUG5 -->
## SUG5 [x] — Enregistrer la décision du client sur un bien proposé

**Session** : 673e24d2-f496-48d7-b069-a1ee74532d62
**Dépend de** : rien. À jouer après SUG4 : même SQL, même banc.
**Fichiers** :
- `docker/init-v3/01_create_fil_rouge_immobilier.sql` (table `estate_proposed`) ;
- `docker/migrations/v2-vers-v3/51_decision-du-client.sql` (neuf) ;
- `API/src/app/models/estate_proposed_model.py` ;
- `API/src/app/services/estate_proposed_service.py` ;
- les deux seeds ;
- `API/tests/integration/test_constraints_db.py` (ajout pur), `API/README.md`.

**Prompt**
- Ajoute à `estate_proposed` (vote M4 et § 8.1 du journal) :
  - `client_decision VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (IN ('pending', 'interested', 'declined'))` ;
  - `client_decided_at TIMESTAMP` ;
  - `decline_reason VARCHAR(20)`, en liste fermée : `too_expensive`, `too_far`, `too_small`, `wrong_type`, `other`.
- Trois `CHECK` :
  - `decline_reason` seulement si `client_decision = 'declined'` ;
  - `client_decided_at` non nul dès que `client_decision <> 'pending'` ;
  - celui de Gabriel : `proposition_status <> 'proposed'` ⇒ `client_decision = 'interested'`.
- La migration passe d'abord à `interested` les lignes au-delà de `proposed`, puis pose les `CHECK`.
- Le client change ces trois champs par son PUT : ajoute-les aux champs permis de SUG1, si SUG1 est jouée.
- Les seeds écrivent `interested` sur leurs offres.
- Tests d'abord : un test par `CHECK`, refusé puis accepté.

**Critère de fin**
- Les tests sont rouges avant le code, puis verts.
- Mutant : retirer le `CHECK` de Gabriel. Son test retombe.
- Le banc v2/v3 rend IDENTIQUES.
- Toute la suite reste verte ; donner le nombre de `passed`.
<!-- /FICHE -->

---

<!-- FICHE:SUG6 -->
## SUG6 [x] — Ouvrir la route de l'offre du client

**Session** : 673e24d2-f496-48d7-b069-a1ee74532d62
**Dépend de** : `SUG1`, `SUG5`.
**Fichiers** : `API/src/app/routes/estate_proposed_router.py`, `API/src/app/services/estate_proposed_service.py`, `API/tests/integration/test_propositions_visites.py` (ajout pur), `API/README.md`, `md/securite/matrice-droits-crud-par-role.md`.

**Prompt**
- Ajoute `POST /estate-proposed/{item_id}/offer`, réservée au rôle `Client` et au client du mandat (`owns_mandate`). Prends modèle sur la route `/{item_id}/payment` de `sale_router.py`.
- Corps : `amount_proposition`, un `int` > 0, en euros.
- Elle exige le statut `proposed` ; sinon, 409.
- Elle écrit en une fois :
  - le montant ;
  - `proposition_status = 'offer_pending'` ;
  - `client_decision = 'interested'` et `client_decided_at` à maintenant.
- Le PUT du client reste limité (SUG1). Le montant n'y passe pas.
- Tests d'abord :
  - l'offre d'un client rend 200, avec les 4 champs écrits ;
  - l'offre d'un autre client rend 404 (« le sien ») ;
  - une seconde offre sur `offer_pending` rend 409 ;
  - un chasseur rend 403.

**Critère de fin**
- Les tests sont rouges avant le code, puis verts.
- Mutant : ne plus vérifier le statut `proposed`. Le test 409 retombe.
- Toute la suite reste verte ; donner le nombre de `passed`.
<!-- /FICHE -->

---

<!-- FICHE:SUG7 -->
## SUG7 [x] — Traduire des critères en requête Elasticsearch

**Session** : 673e24d2-f496-48d7-b069-a1ee74532d62
**Dépend de** : rien.
**Fichiers** : `API/src/app/services/suggestion_query.py` (neuf), `API/tests/test_suggestion_query.py` (neuf), `airflow/src/search/mapping.py` (lu seulement : les noms des champs de l'index).

**Prompt**
Écris une fonction pure, `query_from_criteria(criteria, excluded_ids)`. Elle rend un dict de requête `bool` pour l'index `estates`.
- **`filter`**, les critères durs :
  - `town` (ou `postal_code`) et `estate_type` ;
  - `price` ≤ `budget_max` (et ≥ `budget_min` s'il est donné) ;
  - `surface` ≥ `surface_min` ;
  - `nb_rooms` ≥ `rooms_min`, `nb_bedrooms` ≥ `bedrooms_min` ;
  - `energy_class` dans les lettres ≤ `energy_class_max`.
- **`should`**, des bonus de score : `has_garden`, `has_elevator`, `has_cellar`, `has_garage`, `parking_spaces`. Le score monte, rien n'est exclu.
- **`must_not`** : les `_id` de `excluded_ids`.
- Un critère absent (`None`) n'ajoute rien.
- Les critères absents de l'index (balcon, terrasse, vue, piscine, calme, lumineux) ne s'inventent pas : dis-le dans la docstring.
- Tests d'abord, sans Elasticsearch : un test par critère, un pour l'exclusion, un pour « tout `None` ».

**Critère de fin**
- `pytest API/tests/test_suggestion_query.py` est rouge avant le code, puis vert ; donner le nombre de tests.
- Mutant : `lte` en `gte` sur le prix. Le test du budget retombe.
- `pyright` rend 0 erreur sur le fichier neuf.
<!-- /FICHE -->

---

<!-- FICHE:SUG8 -->
## SUG8 [x] — Ouvrir la route des suggestions

**Session** : 673e24d2-f496-48d7-b069-a1ee74532d62
**Dépend de** : `SUG4`, `SUG7`.
**Fichiers** :
- `API/src/app/routes/search_request_router.py`, ou un routeur neuf branché dans `API/src/app/main.py` ;
- `API/src/app/services/suggestion_service.py` (neuf) ;
- `API/tests/integration/test_suggestions.py` (neuf) ;
- `API/README.md`, `md/securite/matrice-droits-crud-par-role.md`.

**Prompt**
- Ajoute `POST /search-requests/{item_id}/suggestions`, réservée au chasseur qui suit la demande (`handles_request`). Sinon, 404.
- Étapes :
  - lire la **dernière** version de `criteria`, celle qu'aucune autre ne cite en `id_previous_version`. Aucune : 409 ;
  - exclure les biens vendus (`sale.id_estate`) et ceux déjà dans `estate_searchrequest` pour cette demande, quel que soit leur statut ;
  - interroger Elasticsearch par `query_from_criteria` (SUG7), 10 résultats au plus ;
  - écrire chaque bien en `estate_searchrequest`, avec `status = 'suggested'` et `id_hunter` = le chasseur.
- Elle rend la liste écrite.
- Elasticsearch absent : 503, comme `GET /estates/search`. Le log nomme l'échec.
- Tests d'abord, avec un faux client Elasticsearch injecté (voir `_es` dans `estate_search_router.py`) :
  - un bien vendu n'est pas écrit ;
  - un bien déjà `dismissed` n'est pas réécrit ;
  - jamais plus de 10 ;
  - un autre chasseur rend 404 ;
  - une demande sans critères rend 409.

**Critère de fin**
- Les tests sont rouges avant le code, puis verts.
- Mutant : retirer l'exclusion des vendus. Le test « vendu » retombe.
- Toute la suite reste verte ; donner le nombre de `passed`.
- La route apparaît dans le Swagger (`GET /openapi.json`).
<!-- /FICHE -->

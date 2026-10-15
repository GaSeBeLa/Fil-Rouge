> **QUAND LIRE** : on joue une fiche `FLX*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache FLX<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier FLX — Flux de données : Airflow et Elasticsearch

**Ouvert.** le 2026-10-15.

**À quoi il sert.** Le livrable BC05 demande des flux de données : Airflow importe
les annonces et nourrit l'OLAP, Elasticsearch sert la recherche de biens et les logs.

**Fait.** Rien. Cadré le 2026-10-15 en 12 fiches (13 depuis `FLX13`, faker de volume, ajoutée le même jour avant `FLX6`), `FLX1` à jouer **après la fusion de PRF**.

**Session** : f022f081-0f47-40d8-a130-39e8bee7a307

## Le socle commun

Le code vit dans `../Fil-Rouge-API/` ; tout chemin ci-dessous s'y lit. **Aucune
fiche ne se joue avant la fusion du chantier PRF** (migrations 45 à 47, `estate_service.py`).
Vérification API : depuis `docker/`, `docker compose exec -T api python -m pytest -q`
(à mesurer au début de chaque fiche). Tests Airflow : `pytest airflow/tests -q`, **sans**
Airflow, sans Docker, sans MinIO (cours Airflow, exo 8). Python touché : `pyright`.

**Décisions de Seb** (Discord, 2026-10-15, questions `flux-1` à `flux-15`) :
- **Airflow 2.11.2**, `LocalExecutor` (cours : 2.9.3 ; Airflow 2 est en fin de vie
  depuis le 2026-04-22 — [doc officielle](https://airflow.apache.org/docs/apache-airflow/stable/installation/supported-versions.html), à dire à l'oral) ;
- **profils Compose** (oui de Seb pour `docker/docker-compose.yml`, **seulement**
  dans `FLX1`, `FLX7`, `FLX10`) : sans profil `db`, `api` ; profil `airflow` :
  `minio`, `minio-setup`, `airflow-init`, `airflow-webserver`, `airflow-scheduler` ;
  profil `elk` : `elasticsearch`, `kibana`, `logstash`. Tout : `--profile "*"` ;
- **MinIO** (déjà là : `minio`, `minio-setup`) : buckets `bronze`, `silver`, `gold`
  gardés (= raw, cleansed, curated du cours), **`quarantine`** ajouté ;
- **base d'Airflow** : une base `airflow` dans **notre** PostgreSQL (service `db`),
  jamais mêlée à `fil_rouge_immobilier` ; **OLAP** : schéma `olap` de `fil_rouge_immobilier` ;
- **clé d'une annonce : `estate.reference`**, déjà `VARCHAR(50) NOT NULL UNIQUE` et
  déjà remplie par la référence d'annonce (2556 biens sur 2556, compté le 2026-10-15) ;
  **pas** de colonne `source_reference` (question `flux-16`, tranchée A par Seb le
  2026-10-15, MPD corrigé) ; **`estate_price_history`** (migration **48**) : `id INTEGER GENERATED ALWAYS AS
  IDENTITY PRIMARY KEY` (comme tout le schéma, jamais `SERIAL`), `created_at TIMESTAMP
  NOT NULL DEFAULT (now() AT TIME ZONE 'utc')`, `id_estate INTEGER NOT NULL REFERENCES
  estate(id) ON DELETE RESTRICT`, `price INTEGER NOT NULL CHECK (price >= 0)`,
  `seen_at DATE NOT NULL`, `CONSTRAINT uq_estate_price_history_estate_seen UNIQUE
  (id_estate, seen_at)` — recopiés du MPD de Gabriel (Discord, 2026-10-15) ;
- **OLAP** = le modèle du sujet (`documents utiles/OLAP.md`, StarterPack) : `fait_ventes`
  (une ligne par vente) et `dim_temps`, `dim_chasseur`, `dim_client`, `dim_bien`,
  `dim_secteur` ; **aucun nom, e-mail ni téléphone** dans `olap` ;
- **index `estates`** rempli par un DAG ; route **`GET /estates/search`**, mêmes rôles
  que la lecture des biens (`read_roles=ALL_ROLES`, `routes/estate_router.py`) ;
  **jamais** `estate_contact` dans l'index (ADR-054) ;
- **horaires** : `annonces_import` à 2 h, `olap_refresh` à 3 h, `estates_index` à 4 h
  (cron), lançables à la main.

**Comment le cours écrit un DAG** (synthèse : `md/flux/cours-airflow-synthese.md`) :
`with DAG(...)` + `PythonOperator`, **pas de TaskFlow** ; `start_date=datetime(2026, 10, 1)`,
`catchup=False`, `retries=2`, `retry_delay=timedelta(minutes=5)`, `execution_timeout` ;
la date logique `ds` ; **le DAG orchestre, `airflow/src/` transforme** ; une validation
rend `(True, "")` ou `(False, "raison")`, un rejet part en quarantaine avec
`_reject_reason`, `_reject_ts`, `_source_file` ; rejouer ne crée aucun doublon.

| Nom | Où | Rôle |
|---|---|---|
| `airflow/dags/`, `airflow/src/`, `airflow/tests/` | `Fil-Rouge-API` (neufs, `FLX2`) | DAG, métier, tests |
| `minio_default`, `fil_rouge_db`, `elasticsearch_default` | connexions Airflow, par `AIRFLOW_CONN_*` | identifiants lus dans `docker/.env` |
| `normalised/normalised.py` | dépôt **Fil-Rouge** | nettoyage des annonces existant (ancien schéma) |
| `outils/generer_annonces.py` | StarterPack - BASE (**lecture seule**) | annonces sales ; écrit dans `<parent du script>/fixtures/annonces/` |
| `ELK-ElasticSearch-Logstash-Kibana/` | `COURS_ENGI_IA/TP-intro-elasticsearch-kibana/` | kit du TP : compose 9.5.4, `setup`, `ingest.py`, `web.conf` |

**Une fiche de schéma** change `docker/init-v3/01` **et** écrit sa migration jumelle dans
`docker/migrations/v2-vers-v3/` ; le banc (`test_banc_v2_v3`) garde les deux alignés.
Secrets : `docker/.env` (jamais lu ni commité), noms ajoutés à `docker/.env.exemple`.

Hors du chantier : le déploiement sur le VPS (TODO 9) ; la refonte de `normalised/` ;
reconnaître le même bien chez deux agences ; Airflow 3 ; Confluence et le MPD (le groupe).

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `FLX1` | Découper le compose en profils et faire démarrer Airflow | PRF fusionné |
| `FLX2` | Poser `airflow/`, ses connexions et un DAG d'essai | `FLX1` |
| `FLX3` | Nettoyer et valider une annonce, sans Airflow | `FLX2` |
| `FLX4` | Importer les annonces chaque nuit, sans doublon | `FLX3` |
| `FLX5` | Créer le schéma `olap` en étoile | `FLX2` |
| `FLX13` | Fabriquer du volume : des centaines de ventes fausses | `FLX5` |
| `FLX6` | Rafraîchir l'OLAP chaque nuit | `FLX13` |
| `FLX7` | Faire démarrer Elasticsearch et Kibana | `FLX1` |
| `FLX8` | Remplir l'index `estates` chaque nuit | `FLX4`, `FLX7` |
| `FLX9` | Chercher un bien par `GET /estates/search` | `FLX8` |
| `FLX10` | Envoyer les logs de l'API dans Elasticsearch | `FLX7` |
| `FLX11` | Montrer le trafic et les biens dans Kibana | `FLX8`, `FLX10` |
| `FLX12` | Écrire la doc, le schéma du flux et les ADR | toutes |

Après `FLX2`, les branches annonces (`FLX3`-`FLX4`) et OLAP (`FLX5`-`FLX6`) sont
indépendantes ; `FLX7` et `FLX10` se jouent dès `FLX1`. Migrations : 48 en
`FLX4`, 49 en `FLX5`.

---

<!-- FICHE:FLX1 -->
## FLX1 [x] — Découper le compose en profils et faire démarrer Airflow

**Session** : 53337d1c-79b2-439c-8cea-3a6e446e0d7b
**Dépend de** : PRF fusionné.
**Fichiers** : `docker/docker-compose.yml`, `docker/.env.exemple`,
`docker/init-v3/07_airflow-base.sh` (neuf), `airflow/Dockerfile` (neuf),
`API/README.md` (§ lancement) — et rien d'autre.

**Prompt**
Pose les profils du socle : `minio` et `minio-setup` passent au profil `airflow`,
`db` et `api` restent sans profil. Ajoute `airflow-init`, `airflow-webserver` (port
8080) et `airflow-scheduler`, sur le modèle du lab du cours (`lab/docker-compose.yml`,
résumé dans la synthèse), avec l'image **`apache/airflow:2.11.2`** : vérifie d'abord
sur Docker Hub que ce tag existe, et sur la doc officielle d'Airflow comment ajouter
des paquets (image étendue `airflow/Dockerfile` ou `_PIP_ADDITIONAL_REQUIREMENTS`) ;
cite la page et sa date en commentaire. Versions figées, comme `API/requirements.txt`.
La base `airflow` et son rôle naissent dans `07_airflow-base.sh` (script d'init de
l'image postgres, lit `AIRFLOW_DB_PASSWORD`) ; pour une base existante, le README
donne la commande `psql` équivalente. Ajoute `AIRFLOW_DB_PASSWORD`,
`AIRFLOW_ADMIN_PASSWORD`, `AIRFLOW_FERNET_KEY` à `.env.exemple`, vides. Le README
dit : `docker compose up -d` (db + api), `--profile airflow`, `--profile "*"`, et
que **MinIO ne démarre plus seul**.

**Critère de fin**
Depuis `docker/` : `docker compose up -d` puis `docker compose ps --format "{{.Service}}"`
liste **2** services (`db`, `api`) ; `docker compose --profile airflow up -d` puis
`curl -s localhost:8080/health` rend `"metadatabase": {"status": "healthy"}` et
`"scheduler": {"status": "healthy"}` ; `psql -l` montre `airflow` à côté de
`fil_rouge_immobilier`. pytest de l'API : même compte qu'au début de la fiche.
<!-- /FICHE -->

---

<!-- FICHE:FLX2 -->
## FLX2 [x] — Poser `airflow/`, ses connexions et un DAG d'essai

**Session** : 53337d1c-79b2-439c-8cea-3a6e446e0d7b
**Dépend de** : `FLX1`.
**Fichiers** : `airflow/dags/smoke_dag.py`, `airflow/src/__init__.py`,
`airflow/src/config.py`, `airflow/tests/conftest.py`, `airflow/tests/test_config.py`,
`airflow/README.md` (tous neufs), `docker/docker-compose.yml` (volumes et
`AIRFLOW_CONN_*` des 3 services Airflow : suite de `FLX1`), `docker/.env.exemple`,
`docker/init-v3/README.md` ou `API/README.md` (§ Airflow) — et rien d'autre.

**Prompt**
Monte `airflow/dags` et `airflow/src` dans les 3 services Airflow, comme le lab
(`/opt/airflow/dags`, `/opt/airflow/src`, `PYTHONPATH`). Déclare les connexions
`minio_default` et `fil_rouge_db` par `AIRFLOW_CONN_*`, valeurs tirées de `docker/.env`.
`minio-setup` crée aussi le bucket **`quarantine`**. `src/config.py` lit les
variables d'environnement (endpoint MinIO, buckets, URL de la base), sans valeur
secrète par défaut. `smoke_dag` (manuel, `schedule=None`) a 2 tâches : écrire un
petit objet dans `bronze/smoke/{ds}.json`, puis lire `SELECT count(*) FROM estate`.
Les tests suivent le lab (`lab/tests/conftest.py` : `src/` dans le `sys.path`,
variables factices). `airflow/README.md` : arborescence, commande des tests,
comment lancer un DAG à la main.

**Critère de fin**
`pytest airflow/tests -q` vert, compte affiché ; `docker compose exec airflow-scheduler
airflow dags test smoke_dag 2026-10-15` finit en `success` et affiche le nombre de
biens ; `mc ls` montre l'objet `bronze/smoke/2026-10-15.json` et le bucket
`quarantine`. Mutant : `config.py` qui lit une mauvaise variable → `test_config` tombe.
<!-- /FICHE -->

---

<!-- FICHE:FLX3 -->
## FLX3 [x] — Nettoyer et valider une annonce, sans Airflow

**Session** : 53337d1c-79b2-439c-8cea-3a6e446e0d7b
**Dépend de** : `FLX2`.
**Fichiers** : `airflow/src/annonces/clean.py`, `airflow/src/annonces/validate.py`,
`airflow/tests/test_annonces_clean.py`, `airflow/tests/test_annonces_validate.py`
(neufs) ; lus seulement : `normalised/normalised.py` (dépôt Fil-Rouge),
`docker/init-v3/01_create_fil_rouge_immobilier.sql` (table `estate`) — et rien d'autre.

**Prompt**
Porte la logique de `normalised.py` vers des fonctions pures qui rendent une ligne
prête pour **`estate` v3** (noms de colonnes de `01`, prix en **euros** `int`) :
colonnes renommées (`surface`/`surface_m2`…), dates en plusieurs formats, prix
avec `€`, booléens texte, `reference` → `source_reference`. Recopie les règles de
`normalised.py`, ne les réinvente pas ; un écart avec `01` se dit dans le compte
rendu. `validate_annonce(row) -> tuple[bool, str]` vérifie les colonnes `NOT NULL`
et les `CHECK` de `estate` (relevés par grep, cités en commentaire).
`split_valid(rows)` rend `(valides, rejets)` ; un rejet porte `_reject_reason`,
`_reject_ts`, `_source_file`. Dédoublonnage « le dernier gagne » sur
`source_reference`. **Jamais** de contact du vendeur dans la ligne `estate`.

**Critère de fin**
`pytest airflow/tests -q` : les tests de `clean` et `validate` passent, compte
affiché ; dont un test d'idempotence (deux passages = même sortie) et un test par
règle de rejet. Mesure sur `normalised/annonces/annonces.csv` : N lus, N valides,
N rejetés par raison, comptes bruts. Mutant : le prix en K€ (÷ 1000) → le test du
prix tombe.
<!-- /FICHE -->

---

<!-- FICHE:FLX4 -->
## FLX4 [x] — Importer les annonces chaque nuit, sans doublon

**Session** : 53337d1c-79b2-439c-8cea-3a6e446e0d7b
**Dépend de** : `FLX3`.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql`,
`docker/migrations/v2-vers-v3/48_historique-des-prix.sql` (neuve),
`API/src/app/models/estate_model.py`, `airflow/tools/generer_annonces.py` (copie),
`airflow/src/annonces/load.py`, `airflow/dags/annonces_import_dag.py`,
`airflow/tests/test_annonces_load.py` — et rien d'autre.

**Prompt**
Schéma : `estate_price_history` exactement comme le socle, dans `01` et en
migration 48 ; le modèle SQLModel suit. La clé d'annonce est `estate.reference`
(`flux-16`). Copie `generer_annonces.py` **à l'identique** dans
`airflow/tools/` (en-tête : source, date) ; la tâche la recopie dans `<tmp>/outils/`
et la lance : elle écrit dans `<tmp>/fixtures/annonces/`, jamais dans le StarterPack.
DAG `annonces_import` (`0 2 * * *`) : générer → `bronze/annonces/{ds}/` (brut, jamais
réécrit) → nettoyer et valider (`FLX3`) → `silver/annonces/{ds}.json` et
`quarantine/annonces/{ds}.json` → `load.py` : `INSERT … ON CONFLICT (reference)
DO UPDATE` sur `estate`, et une ligne `estate_price_history` (`ON CONFLICT DO
NOTHING`) par bien vu ce jour-là. `id_author` : le compte prévu par ADR-047 pour
l'import (lis-le).

**Critère de fin**
`docker compose exec airflow-scheduler airflow dags test annonces_import 2026-10-15`
deux fois : `estate` gagne N lignes au 1er passage, **0** au 2e ; `estate_price_history`
compte N lignes ce jour, pas 2N ; objets `bronze`, `silver`, `quarantine` listés.
pytest API et banc v2/v3 verts, comptes affichés. Mutant : `ON CONFLICT DO NOTHING`
sur `estate` → le test du prix mis à jour tombe.
<!-- /FICHE -->

---

<!-- FICHE:FLX5 -->
## FLX5 [x] — Créer le schéma `olap` en étoile

**Session** : 53337d1c-79b2-439c-8cea-3a6e446e0d7b
**Dépend de** : `FLX2`.
**Fichiers** : `docker/init-v3/08_olap.sql`, `docker/migrations/v2-vers-v3/49_schema-olap.sql`
(neufs), `docker/init-v3/README.md` ; lus : `documents utiles/OLAP.md` (StarterPack),
`01_create_fil_rouge_immobilier.sql` (`sale`, `payment`, `mandate`, `visit`, `estate`,
`hunter`, `client`) — et rien d'autre.

**Prompt**
Relie chaque colonne du modèle du sujet à sa source réelle, dans une table
« colonne `olap` → colonne OLTP → calcul » en tête de `08_olap.sql` : `montant_bien`,
`honoraires`, `commission_chasseur`, `nb_visites_avant_achat`, `delai_semaines`,
`mandat_exclusif`. Une mesure sans source se dit, elle ne s'invente pas.
Crée le schéma `olap` : `fait_ventes` (grain : une vente, `sale.id` gardé comme
clé naturelle unique) et les 5 dimensions, clés de substitution `GENERATED ALWAYS
AS IDENTITY` (comme `01`). RGPD :
les dimensions personnes n'ont **que** des numéros et des attributs non
identifiants (ancienneté, IA ou non, ville) ; ni nom, ni e-mail, ni téléphone.
`dim_temps` au jour. Montants : `INTEGER` pour les prix, `NUMERIC(12,2)` pour
honoraires et commission (règle 4). Migration 49 jumelle ; le banc suit.
Envoie à Gabriel (Discord) les colonnes, types, clés et cardinalités, au format
déjà utilisé le 2026-10-15.

**Critère de fin**
`\dt olap.*` liste **6** tables ; grep `name|email|phone` dans `08_olap.sql` : 0
colonne (comptes affichés) ; banc v2/v3 et pytest API verts, comptes affichés.
<!-- /FICHE -->

---

<!-- FICHE:FLX13 -->
## FLX13 [ ] — Fabriquer du volume : des centaines de ventes fausses

**Dépend de** : `FLX5`.
**Fichiers** : `API/src/app/scripts/seed_volume.py`, `API/tests/unit/test_seed_volume.py`
(neufs), `API/README.md` (§ seed) ; lus : `API/src/app/scripts/seed_demo.py` (modèle),
`services/payment_calculation_service.py`, `01_create_fil_rouge_immobilier.sql` (`sale`,
`mandate`, `visit`, `payment`) — et rien d'autre.

**Prompt**
Décision de Seb (Discord, 2026-10-15, bouton `faker-volume:A` ; volume : question
`flux-18`) : avec **1** vente en base, `fait_ventes` et Kibana sont vides. Écris
`seed_volume.py` sur le modèle de `seed_demo.py` (ADR-055, ADR-046 corrigé) : il
**passe par les services** de l'API, Faker `fr_FR` à **graine fixe**, e-mails en
`example.com`, aucune personne réelle ; il **refuse** d'écrire dans `fil_rouge_test`
et aucun test d'intégration ne l'appelle. Par vente : un client neuf, sa demande,
un mandat signé (6 mois, exclusif ou non), des offres, des visites `'client'`
datées dans le mandat, la vente (bien jamais vendu, `uq_sale_estate`) et son
paiement par `PaymentCalculationService.build_payment` — **aucun montant tiré au
hasard** (honoraires par `calculer_honoraires`). Chasseurs et managers : une
poignée, réutilisés. Dates étalées sur deux ans, jamais dans le futur. Option
`--sales N`, défaut fixé par `flux-18` ; un deuxième lancement ne double rien
(marqueur, comme `seed_demo`). Les fonctions pures (dates, tirages) se testent
sans base.

**Critère de fin**
Lancé sur la base de dev : `SELECT count(*) FROM sale` passe de **1** à 1 + N,
`payment` pareil (comptes affichés) ; relancé : comptes inchangés. Tests unitaires
verts ; pytest API vert, comptes affichés.
<!-- /FICHE -->

---

<!-- FICHE:FLX6 -->
## FLX6 [ ] — Rafraîchir l'OLAP chaque nuit

**Dépend de** : `FLX13`.
**Fichiers** : `airflow/src/olap/extract.py`, `airflow/src/olap/transform.py`,
`airflow/src/olap/load.py`, `airflow/dags/olap_refresh_dag.py`,
`airflow/tests/test_olap_transform.py` (neufs) — et rien d'autre.

**Prompt**
DAG `olap_refresh` (`0 3 * * *`) : extraire de l'OLTP les lignes utiles (vues par
`FLX5`), calculer les mesures en Python pur (`transform.py`, testé sans base),
charger dimensions puis faits **dans une seule transaction** : vider et recharger
(`TRUNCATE … RESTART IDENTITY` puis `INSERT`), donc rejouable. Un rapport qualité
par passage : lignes lues, chargées, rejetées par raison (`invalid_count`,
`pass_rate`, cours CRS06), écrit dans `gold/olap/{ds}.json`. Une vente sans
paiement garde une commission vide, elle n'est pas rejetée. Pas de nom, d'e-mail
ni de téléphone extrait : la requête ne les sélectionne même pas.

**Critère de fin**
`airflow dags test olap_refresh 2026-10-15` deux fois : `SELECT count(*) FROM
olap.fait_ventes` = `SELECT count(*) FROM sale`, identique aux 2 passages (comptes
affichés) ; tests de `transform` verts. Mutant : le délai en jours au lieu de
semaines → le test du délai tombe.
<!-- /FICHE -->

---

<!-- FICHE:FLX7 -->
## FLX7 [ ] — Faire démarrer Elasticsearch et Kibana

**Dépend de** : `FLX1`.
**Fichiers** : `docker/docker-compose.yml`, `docker/.env.exemple`, `API/README.md`
(§ profils) ; lu : `TP1 - Introduction/kit-TP/docker-compose.yml` du kit ELK — et
rien d'autre.

**Prompt**
Ajoute au profil `elk` les services du kit du TP1 : `es-setup` (fixe le mot de
passe de `kibana_system`, puis s'arrête), `elasticsearch` (un nœud, sécurité
active, TLS coupé comme le TP), `kibana`. Version **9.5.4** par `STACK_VERSION`,
limites de mémoire du kit (`ES_MEM_LIMIT=2g`, `KB_MEM_LIMIT=1g`), ports sur
`127.0.0.1` seulement. Mots de passe `ELASTIC_PASSWORD` et `KIBANA_PASSWORD` dans
`.env.exemple`, vides. Le README donne la RAM du kit (≈ 4 Go pour ES + Kibana +
Logstash, TP1) et les deux erreurs connues : `vm.max_map_count`, code 137
(`.wslconfig`).

**Critère de fin**
`docker compose --profile elk up -d` puis `curl -s -u elastic:… localhost:9200/_cluster/health`
rend `"status":"green"` ou `"yellow"` ; `curl -s localhost:5601/api/status` rend
`"level":"available"` ; `docker compose up -d` seul lance toujours **2** services.
<!-- /FICHE -->

---

<!-- FICHE:FLX8 -->
## FLX8 [ ] — Remplir l'index `estates` chaque nuit

**Dépend de** : `FLX4`, `FLX7`.
**Fichiers** : `airflow/src/search/mapping.py`, `airflow/src/search/documents.py`,
`airflow/dags/estates_index_dag.py`, `airflow/tests/test_search_documents.py`
(neufs), `docker/docker-compose.yml` (connexion `elasticsearch_default` des services
Airflow : suite de `FLX1`, déjà autorisée), `docker/.env.exemple` — et rien d'autre.

**Prompt**
Mapping `estates` sur le modèle du TP1 : `"dynamic": "strict"`, analyseur `french`
sur les textes, `keyword` pour ville, code postal et type, intervalles pour prix et
surface, `geo_point` depuis latitude et longitude (les deux ou aucune : migration
31). `documents.py` : une ligne `estate` → un document, `_id` = `estate.id` ;
liste blanche de champs, **jamais** `estate_contact`. DAG `estates_index`
(`0 4 * * *`) : créer l'index s'il manque, `helpers.bulk`, puis retirer de l'index
les `_id` absents de `estate`. Client Python `elasticsearch` à la version du TP
(9.5.1), à revérifier sur PyPI. Un compte Elasticsearch dédié, droits limités à
`estates`, jamais `elastic`.

**Critère de fin**
`airflow dags test estates_index 2026-10-15` deux fois : `GET estates/_count` =
`SELECT count(*) FROM estate`, identique aux 2 passages (comptes affichés) ; tests
de `documents` verts. Mutant : ajouter un champ de contact au document → le test
de la liste blanche tombe.
<!-- /FICHE -->

---

<!-- FICHE:FLX9 -->
## FLX9 [ ] — Chercher un bien par `GET /estates/search`

**Dépend de** : `FLX8`.
**Fichiers** : `API/src/app/routes/estate_search_router.py`,
`API/src/app/services/estate_search_service.py`,
`API/tests/test_estate_search.py` (neufs), `API/src/app/main.py`,
`API/requirements.txt`, `docker/docker-compose.yml` (variables ES du service
`api` : autorisé avec `FLX7`), `API/README.md` — et rien d'autre.

**Prompt**
Route `GET /estates/search` : `q` (texte libre), `city`, `postal_code`, `type`,
`price_min`, `price_max`, `surface_min`, `lat`, `lon`, `radius_km`, `page`,
`size` ; requête `bool` du TP1 (texte dans `must`, le reste dans `filter`). Rôles :
`ALL_ROLES`, comme `routes/estate_router.py`. ⚠️ Inclus ce routeur **avant**
celui des biens dans `main.py` : sinon `/estates/{id}` capte `search` et rend 422.
Elasticsearch absent ou en panne : **503** lisible, et l'erreur est loggée — jamais
de liste vide silencieuse. La réponse rend les `id` et les champs de l'index ; le
détail d'un bien reste `GET /estates/{id}`.

**Critère de fin**
`pytest -q` : tests de `test_estate_search.py` verts (client Elasticsearch
simulé), compte total affiché ; un test 401 sans jeton ; un test 503 quand le
client lève une erreur de connexion. Contre la pile lancée : une recherche sur une
ville du seed rend au moins 1 bien. Mutant : routeur inclus après celui des biens
→ le test de la route tombe.
<!-- /FICHE -->

---

<!-- FICHE:FLX10 -->
## FLX10 [ ] — Envoyer les logs de l'API dans Elasticsearch

**Dépend de** : `FLX7`.
**Fichiers** : `API/src/app/conf/logging.py` (neuf), `API/src/app/main.py`,
`docker/logstash/pipeline/api.conf`, `docker/logstash/pipelines.yml` (neufs),
`docker/docker-compose.yml` (service `logstash`, volume des logs de l'API),
`docker/.env.exemple`, `API/README.md` — et rien d'autre.

**Prompt**
L'API écrit ses logs d'accès en **JSON, une ligne par requête** (méthode, chemin,
code, durée, rôle — **jamais** le jeton, le mot de passe ni un e-mail) dans un
volume nommé, en plus de la console. Logstash (profil `elk`, kit du TP2 : heap
512m, `mem_limit: 1g`) lit ce fichier en lecture seule, codec `json`, et écrit
dans le data stream **`logs-api-default`** avec des noms ECS (`http.request.method`,
`url.path`, `http.response.status_code`, `event.duration`). Compte dédié
`logstash_internal`, droits limités à `logs-api-*` (TP2). Le volume des logs n'est
pas monté dans le dépôt.

**Critère de fin**
Après 10 appels à l'API : `GET logs-api-default/_count` ≥ 10 ; un document montre
`http.response.status_code` ; grep `password|token|email` dans 1 document : 0.
pytest API : même compte qu'au début. Mutant : logger le corps de la requête de
`/auth/login` → le test « pas de mot de passe dans le log » tombe.
<!-- /FICHE -->

---

<!-- FICHE:FLX11 -->
## FLX11 [ ] — Montrer le trafic et les biens dans Kibana

**Dépend de** : `FLX8`, `FLX10`.
**Fichiers** : `docker/kibana/dashboards.ndjson` (neuf, export des objets),
`API/README.md` (§ Kibana : importer, ouvrir) — et rien d'autre.

**Prompt**
Dans Kibana, deux vues de données (`logs-api-*`, `estates`) et un tableau de bord
Lens sur le modèle du TP2 : nombre de requêtes, taux d'erreur, trafic par code HTTP
dans le temps, routes les plus appelées ; une carte des biens (`geo_point`) et le
prix moyen par ville. Exporte les objets dans `dashboards.ndjson` ; le README dit
comment les réimporter (Stack Management → Saved Objects, ou l'API `_import`).

**Critère de fin** (visuel)
Seb ouvre http://localhost:5601, importe `dashboards.ndjson`, et voit le tableau de
bord rempli : courbes du trafic et carte des biens. La séance s'arrête et lui rend
la main.
<!-- /FICHE -->

---

<!-- FICHE:FLX12 -->
## FLX12 [ ] — Écrire la doc, le schéma du flux et les ADR

**Dépend de** : toutes.
**Fichiers** (dépôt **Fil-Rouge**) : `md/flux/cours-airflow-synthese.md`,
`md/flux/cours-elasticsearch-synthese.md` (déjà copiées au cadrage),
`md/flux/schema-du-flux.md` (neuf), `md/adr/adr-059-*.md` à `adr-06x-*.md`
(neufs), `livrables/` (dossier du livrable BC05 : à trouver par `ls`),
`context AI/08-etat.md` — et rien d'autre.

**Prompt**
Schéma du flux, **avec les vrais noms** (promis à Laurence le 2026-10-15) :
annonces → `bronze`/`silver`/`quarantine` → `estate` → `estates` → `GET
/estates/search` ; OLTP → `olap` ; API → Logstash → `logs-api-default` → Kibana ;
les 3 DAG et leurs heures ; la RAM par profil (mesurée par `docker stats`). En
Mermaid, une phrase par flèche. ADR, un par décision du socle qui n'en a pas :
Airflow 2.11.2 en fin de vie, MinIO et ses buckets, Elasticsearch copie de
PostgreSQL, profils Compose, `estate.reference` comme clé d'annonce (`flux-16`) et historique des prix. Remplis la
« Décision » de `OLAP.md` dans notre livrable (pas dans le StarterPack).

**Critère de fin**
Les fichiers existent ; chaque ADR cite ses sources (`Discord flux-<n>`, cours,
doc officielle) ; le schéma se rend sur GitHub (Mermaid valide : `npx -y
@mermaid-js/mermaid-cli` ou aperçu GitHub) ; grep `TODO|à remplir` dans les
fichiers neufs : 0.
<!-- /FICHE -->

# Cours Airflow (Robin Hotton, 27/08) — synthèse pour le projet

- Dossier lu : `Supports de cours-20260827 AIRFLOW/`.
- Abréviations des sources :
  - `CRS05` = `CRS/05-orchestration-airflow.pdf` (de même `CRS01`, `CRS02`, `CRS03`, `CRS04`, `CRS06`, `CRS07`).
  - `lab/` = `lab-Minio-Airflow-20260827/`.
  - « p. N » = numéro de page du PDF.
- Lu le 15/10/2026, en lecture seule. Le fichier `lab/.env` n'a **pas** été ouvert.

---

## 1. La version et l'installation du lab

### La version d'Airflow

- **Image Docker du lab : `apache/airflow:2.9.3`** (`lab/docker-compose.yml`, l. 3).
- Le `.venv` local contient **`apache_airflow-2.11.2`** (`lab/.venv/Lib/site-packages/apache_airflow-2.11.2.dist-info`).
  - ⚠️ Ce n'est **pas** la version qui tourne : le `.venv` sert à l'éditeur et aux tests (`lab/requirements.txt`, l. 3).
  - Le `requirements.txt` ne liste même pas Airflow (l. 9-14) : `boto3`, `pandas`, `pytest`, `ruff`.
- Le cours se situe en **Airflow 2** : « Depuis Airflow 2.0, les opérateurs cloud sont dans des packages séparés » (`CRS05` p. 12) ; `days_ago()` « déprécié depuis Airflow 2.2 » (`CRS05` p. 7).

### L'exécuteur

- **`LocalExecutor`** (`lab/docker-compose.yml` l. 6 ; `CRS05` p. 3 : « Notre lab utilise LocalExecutor »).
- Le cours cite aussi Celery et Kubernetes, sans les utiliser (`CRS05` p. 3).
- Conséquence relevée dans le code : avec LocalExecutor, chaque tâche tourne dans un **processus séparé**, donc une variable globale n'est pas partagée entre tâches ; d'où XCom (`lab/airflow/dags/orders_pipeline_dag.py` l. 10-13).

### Les services du `docker-compose.yml`

| Service | Image | Ports | Volumes | Rôle |
| --- | --- | --- | --- | --- |
| `minio` | `minio/minio:RELEASE.2024-10-13T13-34-11Z` | `9000` (API S3), `9001` (console) | `minio_data:/data` | stockage objet, chiffrement SSE-S3 par clé KMS locale |
| `minio-init` | `minio/mc:RELEASE.2024-10-02T08-27-28Z` | aucun | `./scripts:/scripts:ro` | une fois : crée le bucket `data-lake` + règle lifecycle |
| `datasets-init` | `python:3.11.10-slim` | aucun | `./setup_datasets.py`, `./scripts` (lecture seule) | une fois, profil `datasets` : charge les jeux de données |
| `postgres` | `postgres:16.4-alpine` | **aucun** (non exposé) | `postgres_data:/var/lib/postgresql/data` | base de métadonnées d'Airflow |
| `airflow-init` | `apache/airflow:2.9.3` | aucun | communs Airflow (voir dessous) | une fois : `db migrate` + compte admin |
| `airflow-webserver` | `apache/airflow:2.9.3` | `8080` | communs Airflow | interface web |
| `airflow-scheduler` | `apache/airflow:2.9.3` | aucun | communs Airflow | planificateur |

- Source : `lab/docker-compose.yml` l. 56-202.
- Volumes communs aux 3 services Airflow (l. 38-46) :
  - `./airflow/dags` → `/opt/airflow/dags`
  - `./airflow/src` → `/opt/airflow/src`
  - `./scripts` → `/opt/airflow/scripts` (lecture seule)
  - volumes nommés `airflow_data` et `airflow_logs`.
- Tous les services sont sur un réseau nommé **`lab-net`** (l. 204-209).
- Paquets ajoutés au démarrage, sans image sur mesure (l. 37) : `boto3==1.34.162`, `apache-airflow-providers-amazon==8.10.0`, `pandas==2.2.2`.
- Autres réglages utiles (l. 9-34) :
  - `LOAD_EXAMPLES: "false"`, `DAGS_ARE_PAUSED_AT_CREATION: "true"`.
  - `PYTHONPATH: /opt/airflow:/opt/airflow/src`.
  - Connexion `minio_default` déclarée par la variable d'environnement `AIRFLOW_CONN_MINIO_DEFAULT` (format JSON).
  - Journaux des tâches envoyés dans MinIO : `s3://data-lake/airflow-logs/`.
- Ordre de démarrage : MinIO + PostgreSQL, puis `minio-init`, `datasets-init`, `airflow-init`, puis webserver + scheduler (`ANNEXES/setup-lab.pdf` p. 1).
- Prérequis : Docker Desktop ≥ 24, Docker Compose ≥ 2.20 (`setup-lab.pdf` p. 1).

### La base de métadonnées d'Airflow

- **PostgreSQL 16** (`postgres:16.4-alpine`), base, utilisateur et mot de passe `airflow` dans `.env.example` (l. 16-18).
- Connexion : `postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres/${POSTGRES_DB}` (`docker-compose.yml` l. 8).
- Le README est clair : « **Pas de Postgres métier** : les données vivent dans MinIO. Postgres ne sert qu'à Airflow » (`lab/README.md` l. 64).

### La RAM conseillée

- ❌ **Le cours ne donne aucune RAM** pour le lab.
- Seule mention : Colab « 12 Go RAM » pour les TP Spark, hors de ce lab (`lab/README.md` l. 62).

### Écarts repérés dans les documents du cours

- ⚠️ Le README du lab décrit un passage par « staging Parquet » et une écriture dans `gold/` (l. 189, 209). Le code réel passe par **XCom** et écrit dans **`curated/`** (`orders_pipeline_dag.py` l. 10-16, 67).
- ⚠️ Le README parle de « 6 conteneurs » (l. 13) ; le compose en déclare **7**.
- ⚠️ La correction de l'exo 5 ne téléverse pas le fichier rejeté en quarantaine : elle n'écrit que le `.error.json` (`COR/exo5-correction.pdf` p. 2).

---

## 2. L'architecture enseignée

### Le data lake MinIO

- MinIO = stockage objet open source, compatible avec l'API AWS S3 (`CRS02` p. 16).
- **Un seul bucket : `data-lake`**, un seul compte (`CRS02` p. 16-17 ; `setup-lab.pdf` p. 2).
- Chiffrement SSE-S3 déjà actif sur le bucket (`CRS03` p. 9).

### Les zones — noms exacts

- **`raw/`, `cleansed/`, `curated/`** (`CRS02` p. 4).
  - ⚠️ Le nom est **`cleansed`**, pas « staged ».
- Équivalence donnée par le cours : **Bronze / Silver / Gold** = Raw / Cleansed / Curated, « strictement équivalent » (`CRS02` p. 5 ; `CRS07` p. 8).
- Plus une zone **`quarantine/`** pour les rejets (`CRS04` p. 6 ; `CRS06` p. 12).
- Ce que fait chaque zone :
  - **Raw** : données brutes, **jamais modifiées** après ingestion ; source de vérité qui permet de tout rejouer (`CRS02` p. 4 ; `CRS04` p. 6).
  - **Cleansed** : typage, dédoublonnage, filtrage des lignes invalides, normalisation, enrichissement léger (`CRS02` p. 4).
  - **Curated** : données agrégées pour un usage précis : BI, ML, API (`CRS02` p. 5).
- Schéma : Bronze en « schema on read » (on accepte tout), Silver et Gold en « schema on write » (on valide et on impose le schéma) (`CRS06` p. 4 ; `CRS07` p. 8).

### Le partitionnement des clés

- Style Hive : `raw/sales/year=2026/month=03/…` (`CRS02` p. 6 ; `CRS04` p. 7).
- Les commandes suivent un autre motif : `raw/orders/2026/03/orders_2026-03-01.json` (`setup-lab.pdf` p. 2).

### Le chemin des données dans le pipeline `orders_pipeline`

1. `extract_bronze` lit les JSON Lines du jour dans `raw/orders/AAAA/MM/` (`lab/airflow/src/extract.py` l. 25-57).
2. `transform_silver` valide, dédoublonne, calcule `total_price` ; les rejets vont dans `quarantine/orders/{ds}.json` (`transform.py` l. 78-101 ; `load.py` l. 42-46).
3. `load_gold` agrège le chiffre d'affaires par statut et écrit `curated/ca_by_status_{ds}.json` (`load.py` l. 21-39).
- ⚠️ Rien n'est écrit dans `cleansed/` : la couche Silver passe d'une tâche à l'autre par **XCom**, en mémoire (`orders_pipeline_dag.py` l. 10-16, 88-95).
- Le cours limite XCom aux petits volumes : « pas pour des datasets entiers » (`CRS05` p. 3). Ici, 200 événements par jour (`orders_pipeline_dag.py` l. 10).

---

## 3. Comment le cours écrit un DAG

### Style

- **Opérateurs classiques uniquement** : `with DAG(...)` + `PythonOperator` (`CRS05` p. 4-6 ; `cheatsheet-airflow.pdf` p. 2 ; les 3 DAG du lab).
- **Pas de TaskFlow** (`@dag` / `@task`) : aucune occurrence dans le cours, les exos ni le lab.
- Autres briques montrées : `BashOperator`, `TaskGroup` (`CRS05` p. 8), trigger rules `ONE_FAILED` / `ALL_DONE` pour alerter ou nettoyer (`CRS05` p. 11).
- Dépendances avec `>>` ; listes pour le parallèle : `t1 >> [t2, t3]` (`cheatsheet-airflow.pdf` p. 3).

### Les réglages

- **`schedule`** : expression cron, `"0 6 * * *"` = tous les jours à 6 h ; `None` = déclenchement manuel (`CRS05` p. 13 ; `minio_conn_id_example.py` l. 96).
- **`start_date`** : toujours `datetime(2026, 3, 1)`, jamais `days_ago()` (`CRS05` p. 7).
- **`catchup=False`** partout : ne pas rejouer les intervalles passés au démarrage (`CRS05` p. 13).
- **`retries: 2`**, **`retry_delay: timedelta(minutes=5)`** dans `default_args` (`CRS05` p. 4, 15).
- **`execution_timeout`** conseillé sur chaque tâche (`CRS05` p. 15) — mais absent du DAG du lab.
- **Date logique `context["ds"]`** : la période traitée, pas l'heure réelle ; chaque run ne traite que sa date (`CRS05` p. 7, 14).
  - Le DAG du lab accepte aussi une date passée au déclenchement : `conf["ds"]` (`orders_pipeline_dag.py` l. 38-40).

### Connections et Variables

- **Connection** = accès à un service (identifiants) ; **Variable** = paramètre de configuration, pas un secret (`CRS05` p. 9-10 ; `EX/exo7` p. 2).
- Lecture : `BaseHook.get_connection("minio_default")` et `Variable.get("BUCKET", default_var="data-lake")` (`COR/exo7-correction.pdf` p. 1).
- Création : dans l'interface (Admin → Connections) **ou** par variable d'environnement `AIRFLOW_CONN_<ID>` dans le compose (`CRS05` p. 9 ; `docker-compose.yml` l. 28).
- Dans un conteneur, on vise le **nom du service** (`http://minio:9000`), pas `localhost` (`EX/exo7` p. 3).
- Deux façons d'accéder au stockage, montrées côte à côte (`CRS05` p. 12 ; `lab/README.md` l. 219-222) :
  - client `boto3` direct, construit dans `src/config.py` à partir de variables d'environnement ;
  - `S3Hook(aws_conn_id="minio_default")`, via le provider Amazon.

### Le code métier séparé du DAG

- Règle : « Le DAG orchestre, il ne transforme pas » (`CRS05` p. 14).
- Le métier vit dans **`airflow/src/`** : `config.py`, `extract.py`, `transform.py`, `load.py` ; il se teste sans Airflow (`CRS05` p. 15, 18).
- Le DAG ne contient que de petites fonctions qui appellent `src/` (`orders_pipeline_dag.py` l. 43-69).
- Import : `sys.path.insert(0, "/opt/airflow")` puis `from src.extract import extract_bronze` (l. 31-35).

### Extrait du DAG `orders_pipeline`

Source : `lab/airflow/dags/orders_pipeline_dag.py`, l. 78-86 et 88-92, 97 (15 lignes).

```python
with DAG(
    dag_id="orders_pipeline",
    description="Pipeline commandes : Bronze -> Silver -> Gold (Python pur, src/)",
    schedule="0 6 * * *",             # cron : tous les jours a 6h
    start_date=datetime(2026, 3, 1),  # toujours datetime(), jamais days_ago()
    catchup=False,                    # pas de backfill automatique
    default_args=default_args,
    tags=["orders", "bronze-silver-gold", "pure-python"],
) as dag:
    t_bronze = PythonOperator(task_id="extract_bronze",
                              python_callable=task_extract_bronze)
    t_silver = PythonOperator(task_id="transform_silver",
                              python_callable=task_transform_silver,
                              op_args=[t_bronze.output])  # XComArg des events Bronze
    t_bronze >> t_silver >> t_gold
```

---

## 4. La qualité des données

### Les contrôles enseignés (`CRS06` p. 6-8)

- **Null** : champs obligatoires absents ou `None`.
- **Type** : `float(price)`, `int(quantity)` qui ne lèvent pas d'erreur.
- **Plage** : prix > 0, quantité ≥ 1.
- **Unicité** : pas de doublon sur la clé métier (`event_id`).
- **Règles métier** : statut dans une liste autorisée (`pending`, `completed`, `cancelled`, `refunded`).

### Les principes

- **Fail fast** : rejeter le plus tôt possible ; plus c'est tard, plus ça coûte (`CRS06` p. 3).
- **Data contract** : un fichier YAML versionné dans Git qui décrit schéma, contraintes, fraîcheur ; traduit en dict Python lu par les contrôles (`CRS06` p. 9-11).
- **Quarantaine** : « Ne jamais supprimer » un rejet ; on l'isole avec sa raison (`_reject_reason`, `_reject_timestamp`, `_source_file`) (`CRS06` p. 12).
- Chaque règle renvoie ses invalides ; un **rapport** donne `invalid_count` et `pass_rate` par règle (`CRS06` p. 14).
- Indicateurs à surveiller : nombre de lignes (alerte si chute > 20 %), taux de nuls, fraîcheur, **taux de quarantaine (alerte > 1 %)**, durée (`CRS05` p. 20).
- Validation sous forme de tuple `(True, "")` ou `(False, "raison")`, sans exception pour un rejet métier (`CRS04` p. 9).

### Dans le code du lab

- `validate_event()` enchaîne : champs manquants, nuls, types, plages, statut (`lab/airflow/src/transform.py` l. 46-75).
- `transform_silver()` renvoie `(valides, invalides annotés)` ; les invalides portent `_reject_reason` et `_reject_ts` (l. 78-101).
- Dédoublonnage : « le dernier gagne », par écrasement dans un dict (l. 21-33).

### Le fichier mauvais `transactions_2026-03-17_bad.csv`

- ⚠️ Il sert à l'**exo 5** (ingestion, cours 04), **pas à l'exo 8**.
- Contenu : en-tête `id,date,status` — la colonne **`amount` manque** (`lab/data/transactions_2026-03-17_bad.csv`).
- Ce que le cours en fait (`EX/exo5-ingestion-lifecycle.pdf` p. 4-5 ; `COR/exo5-correction.pdf` p. 2) :
  - `validate_csv()` détecte les colonnes manquantes (`id, date, amount, status` obligatoires) ;
  - le fichier part dans **`quarantine/sales/year=…/month=…/day=…/`** avec un **`.error.json`** qui donne la raison ;
  - le script **ne plante pas** : `try/except` par fichier ;
  - un journal `ingestion_AAAAMMJJ_HHMMSS.json` liste chaque fichier : `file`, `s3_key`, `status`, `timestamp`.

---

## 5. Les tests (exo 8)

- **pytest sur les fonctions de `src/`**, sans Airflow, sans Docker, sans MinIO (`EX/exo8-tests-pipeline.pdf` p. 2 ; `CRS06` p. 17).
- On teste des **listes de dicts** écrites à la main (`CRS05` p. 18).
- **8 tests attendus** (`EX/exo8` p. 4-8 ; `COR/exo8-correction.pdf` p. 3-4) :
  - `deduplicate` garde le dernier ;
  - `compute_total_price` (dont le cas prix 0) ;
  - `filter_valid_status` ;
  - `validate_event` × 4 : cas valide, prix négatif, champ manquant, statut faux ;
  - **idempotence** : deux passages sur les mêmes données donnent le même résultat.
- Exercice de contrôle : casser `compute_total_price` exprès, voir le test échouer, réparer (`EX/exo8` p. 7).
- Le lab ajoute un `conftest.py` qui met `airflow/src` dans le `sys.path` et pose des variables d'environnement factices (`lab/tests/conftest.py` l. 24-31).
- Le lab teste aussi `config.py` : lecture des variables d'environnement (`lab/tests/airflow_src/test_config.py`).
- ❌ **Non couvert** : tester le DAG lui-même (import, structure), ni les accès au stockage.
  - Le README des tests le propose en piste : `moto` pour simuler S3, `airflow.utils.dag_test` / `pytest-airflow` pour les DAG (`lab/tests/README.md`).
- CI GitHub Actions montrée en « référence marché », non faite en cours (`CRS05` p. 21).

---

## 6. Ce qui se transpose au projet

Légende : ✅ vient du cours · 💡 mon avis.

### Commun aux deux flux

- ✅ **Séparer DAG et métier** : un dossier `src/` testable sans Airflow (`CRS05` p. 14-15).
- ✅ **Tests pytest sur listes de dicts**, dont un test d'idempotence (`EX/exo8`).
- ✅ **Identifiants hors du code** : Connection Airflow ou variables d'environnement venant d'un `.env` (`EX/exo7` ; `docker-compose.yml`).
- ✅ `catchup=False`, `retries`, `start_date` fixe, `execution_timeout` (`CRS05` p. 7, 13, 15).
- ✅ **Idempotence** : relancer ne crée pas de doublon (`CRS05` p. 14 ; `CRS04` p. 10).
- 💡 Le lab met la base d'Airflow dans **son propre conteneur PostgreSQL**. Pour le projet, deux choix :
  - un 2e conteneur PostgreSQL rien que pour Airflow (comme le cours) ;
  - ou une **base séparée** dans le PostgreSQL du projet. Dans les deux cas, ne pas mélanger les tables d'Airflow et celles de l'API.
- 💡 Les services Airflow doivent rejoindre le **réseau docker de l'API** pour joindre PostgreSQL par son nom de service (même logique que `minio:9000`, `EX/exo7` p. 3).
- 💡 Le cours ne dit pas comment Airflow écrit dans PostgreSQL. Il faudra ajouter le provider **`apache-airflow-providers-postgres`** (`PostgresHook`) ou un pilote (`psycopg`) dans `_PIP_ADDITIONAL_REQUIREMENTS`.

### Flux A — Import des annonces

- ✅ **Reprendre tel quel** :
  - la zone **raw** immuable pour les annonces brutes ;
  - `validate_*()` qui renvoie `(bool, raison)` ;
  - la **quarantaine avec raison** (`_reject_reason`, horodatage, fichier source) ;
  - le dédoublonnage « le dernier gagne » sur une clé ;
  - le journal d'ingestion par fichier (exo 5).
- 💡 **À adapter** :
  - **champs renommés** : une table de correspondance (alias → nom canonique) avant la validation. Le cours ne fait que rejeter un fichier dont une colonne manque (exo 5).
  - **dates en vrac** : une fonction qui essaie plusieurs formats ; le cours n'en montre qu'un (`strptime("%Y-%m-%d")`, `CRS04` p. 7).
  - **clé de dédoublonnage** : les annonces n'ont pas d'`event_id` fiable. Il faut une clé métier (adresse + surface + prix ? référence d'annonce ?), à décider.
  - **idempotence du chargement** : dans PostgreSQL, ce n'est plus « écraser une clé S3 », c'est un `INSERT … ON CONFLICT` sur une contrainte d'unicité de `estate`.
  - **où mettre raw et quarantaine** : MinIO (comme le cours) ou de simples dossiers / tables de PostgreSQL.
- ❌ **Non couvert** : charger dans une table relationnelle ; respecter les clés étrangères de `estate` ; normaliser des champs texte libres.

### Flux B — Alimentation OLAP

- ✅ **Reprendre tel quel** :
  - la logique **Bronze → Silver → Gold** (extraire, nettoyer, agréger) ;
  - le cloisonnement par **date logique `ds`** ;
  - le rapport qualité par règle (`invalid_count`, `pass_rate`) — utile pour la **note qualité** du livrable ;
  - les indicateurs de suivi (nombre de lignes, nuls, taux de quarantaine) (`CRS05` p. 20).
- ✅ Le cours décrit l'extraction d'une base : **dump complet** ou **chargement incrémental sur `updated_at`** (`CRS04` p. 2).
- 💡 **À adapter** :
  - la « Gold » devient un **schéma en étoile** dans PostgreSQL (une table de faits, des dimensions), pas un JSON dans `curated/`.
  - choisir dump complet ou incrémental : l'incrémental suppose une colonne `updated_at` dans les tables de l'API.
  - garder l'OLAP dans un **schéma ou une base à part** de la base transactionnelle.
- ❌ **Non couvert par le cours** :
  - la **modélisation en étoile** (faits, dimensions, clés de substitution, dimensions qui changent dans le temps) ;
  - le chargement dans un entrepôt relationnel ;
  - le **RGPD appliqué** : pseudonymiser ou retirer noms, e-mails, téléphones avant l'OLAP. Le cours ne cite le RGPD que pour les amendes et le chiffrement (`CRS01` p. 6 ; `CRS03` p. 2, 9, 13).

---

## 7. Les questions qui restent pour le groupe

1. **Version d'Airflow** : le cours est en **2.9.3**. On garde la même, ou une plus récente ? À vérifier sur la doc officielle avant de figer.
2. **Base d'Airflow** : un 2e conteneur PostgreSQL, ou une base séparée dans le PostgreSQL existant ?
3. **MinIO ou pas ?** Faut-il un data lake pour les zones raw et quarantaine, ou des tables PostgreSQL suffisent-elles ? (Le cours tourne entièrement autour de MinIO.)
4. **Clé de dédoublonnage des annonces** : quels champs disent « c'est la même annonce » ?
5. **Que faire d'une annonce rejetée** : quarantaine seule, ou correction puis rejeu (`CRS06` p. 12) ?
6. **Dates en vrac** : quels formats accepte-t-on ? Une date illisible = rejet ou champ vide ?
7. **OLAP** : quelle table de faits (mandats ? ventes ? visites ?) et quelles dimensions ?
8. **Extraction** : dump complet ou incrémental ? Les tables ont-elles une colonne `updated_at` ?
9. **RGPD** : quelles colonnes personnelles n'entrent jamais dans l'OLAP, et lesquelles sont pseudonymisées ?
10. **Fréquence** : à quelle heure tournent les deux DAG ? Ou seulement à la main (`schedule=None`) ?
11. **Tests** : s'en tenir aux tests du cours (fonctions de `src/`), ou ajouter un test d'import des DAG ?
12. **RAM** : le cours n'en donne pas. Combien la machine de chacun peut-elle donner à Docker, avec l'API et PostgreSQL déjà lancés ?

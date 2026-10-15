# Elasticsearch : ce que dit le cours, et ce qu'on en tire pour le projet

Lu le 15/10/2026, en lecture seule.

## Les sources lues

- Dossier du TP : `COURS_ENGI_IA/TP-intro-elasticsearch-kibana/` (dossier des cours, hors dépôt).
- Référence retenue : le dépôt du formateur **`ELK-ElasticSearch-Logstash-Kibana/`** (2 commits : `042dc9f init`, `01fd2bf add: kit TP2`).
  - `Readme.md` : le support de cours, 1 054 lignes. Cité « Cours » ci-dessous.
  - `TP1 - Introduction/Readme.md` : énoncé du TP1. Cité « TP1 ».
  - `TP2 - Logstash/Readme.md` : énoncé du TP2. Cité « TP2 ».
  - Les kits : `docker-compose.yml`, `.env.example`, `ingest.py`, `search.py`, `es_client.py`, `docker-compose.override.yml`, `pipelines.yml`, `offres.conf`, `web.conf`.
- Autres dossiers, vus sans tout lire :
  - `tp_elasticsearch_kibana/` : le travail rendu de l'étudiant (TP1 + TP2), avec `test_alerte.py`.
  - `TP1-ELK-Corrigés/` et `OLD-TP-intro-elasticsearch-kibana/` : corrigé et ancienne version du TP1.
  - Tous portent `STACK_VERSION=9.5.4` dans leur `.env.example`.
- Aucun PDF dans le dossier du TP. Deux images (`infographie_ELK_stack.png`, `infographie_ELK_comparaison.png`) non lues.
- Ailleurs dans `COURS_ENGI_IA/` : **aucun autre cours** sur Elasticsearch, Kibana ou Logstash (recherche par nom de fichier).

---

## 1. La version et l'installation

### Versions

- ✅ **Elasticsearch, Kibana, Logstash : 9.5.4.** Les trois doivent avoir la même version (Cours, l. 3 et l. 81 ; TP2, l. 38-41).
- ✅ Client Python **`elasticsearch==9.5.1`**, Python ≥ 3.10 (TP1, l. 37 ; `kit-TP/requirements.txt`).
- ✅ Version fixée par la variable **`STACK_VERSION=9.5.4`** (`TP1 - Introduction/kit-TP/.env.example`, l. 2).

### Services du compose (`TP1 - Introduction/kit-TP/docker-compose.yml`)

- **`elasticsearch`** (l. 7-30)
  - Image : `docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}`.
  - Port : `127.0.0.1:9200:9200`, local seulement.
  - Volume : `esdata:/usr/share/elasticsearch/data`.
  - Un seul nœud : `discovery.type=single-node`.
  - Healthcheck sur `_cluster/health` (vert ou jaune).
- **`setup`** (l. 33-57) : service éphémère.
  - Même image qu'Elasticsearch.
  - Il fixe le mot de passe du compte `kibana_system`, puis s'arrête.
- **`kibana`** (l. 59-79)
  - Image : `docker.elastic.co/kibana/kibana:${STACK_VERSION}`.
  - Port : `127.0.0.1:5601:5601`.
  - Volume : `kibanadata:/usr/share/kibana/data`.
  - Démarre après la fin de `setup`.
- **`logstash`**, ajouté au TP2 (`TP2 - Logstash/kit-TP/docker-compose.override.yml`, l. 5-26)
  - Image : `docker.elastic.co/logstash/logstash:${STACK_VERSION}`.
  - Profil Compose `logstash` : il ne démarre que si on le nomme (`docker compose up -d logstash`).
  - Port : `127.0.0.1:9600:9600`, l'API de supervision.
  - Volumes : `pipelines.yml`, le dossier `pipeline/`, `./data` en lecture seule, et `lsdata`.

### Sécurité

- ✅ **Activée** : `xpack.security.enabled=true` (compose, l. 14).
- ✅ **TLS coupé** côté HTTP et transport (l. 15-16) : « choix de laboratoire » (Cours, l. 963).
- ✅ Licence gratuite **Basic** (l. 17). Elle couvre tout le TP : sécurité, Discover, Lens, ES|QL, Logstash (Cours, l. 87).
- ✅ Mots de passe dans **`.env`, jamais versionné**. Un secret versionné coûte −2 points (TP1, l. 740).
- ✅ Logstash écrit avec un compte dédié **`logstash_internal`**, rôle `logstash_writer`, droits limités à `offres` et `logs-web-*` (TP2, l. 114-127). Jamais le compte `elastic` (Cours, l. 867).

### RAM

- ✅ Poste : **Docker avec 4 Go de RAM libres** (TP1, l. 245).
- ✅ Limites du kit : **`ES_MEM_LIMIT=2g`**, **`KB_MEM_LIMIT=1g`** (`.env.example`, l. 7-8). Heap Java d'Elasticsearch : `-Xms1g -Xmx1g` (compose, l. 18).
- ✅ Logstash : heap `512m`, `mem_limit: 1g` (override, l. 15 et 23).
- ✅ Sous Windows, si le conteneur meurt (code 137) : `memory=6GB` dans `.wslconfig` (TP1, l. 364-366).
- ✅ Erreur classique au démarrage : `vm.max_map_count` trop bas, à monter à 262 144 (TP1, l. 360-362).

💡 Total ES + Kibana + Logstash : environ **4 Go**. Ajoutés à PostgreSQL, à l'API et à Airflow, ça pèse lourd sur un portable.

---

## 2. Ce que le TP fait

### TP1 : un moteur de recherche d'offres d'emploi

- **Données** : 5 000 offres d'emploi IT fictives, générées par `data/generate_offres.py --seed 42` (TP1, l. 315-343).
  - 13 champs : `id`, `titre`, `entreprise`, `description`, `competences`, `ville`, `localisation` (lat/lon), `contrat`, `teletravail`, `experience_annees`, `salaire_min`, `salaire_max`, `date_publication`.
- **Entrée** : un **script Python**, `ingest.py`.
  - Il crée l'index, puis charge le fichier NDJSON avec `helpers.bulk` (`kit-TP/ingest.py`, l. 1-50).
  - L'`_id` vient de l'`id` métier : relancer ne crée **pas de doublon** (Cours, l. 414-416).
- **Index et mapping** : un index **`offres`**, 1 shard, 0 réplique, `"dynamic": "strict"` (TP1, l. 461-480).
  - Texte en français avec l'analyseur `french` (`titre`, `description`).
  - `keyword` pour les filtres et facettes (`ville`, `contrat`…).
  - Sous-champs : `titre.brut` pour trier, `competences.texte` pour chercher.
  - `geo_point` pour `localisation`.
  - Nombres et dates pour les intervalles.
- **Requêtes** (TP1, parties 3 et 4)
  - `match` contre `term` ; `multi_match` avec poids (`titre^3`) ; tolérance aux fautes (`fuzziness`).
  - Requête `bool` : texte dans `must`, critères exacts dans `filter`.
  - Recherche par distance (`geo_distance`), pagination, surlignage.
  - Agrégations : salaire moyen par ville, offres par mois, tranches de salaire.
  - Bonus : ES|QL.
- **Mini-défi** : `search.py`, un moteur de recherche en ligne de commande, avec filtres et facettes (TP1, l. 712-723).
- **Kibana** : Discover sur l'index, et en option un graphique Lens dans un tableau de bord (TP1, ex. 2.4 et 4.5).

### TP2 : des logs web, une enquête, un tableau de bord

- **Partie 1** : recharger les mêmes offres avec **Logstash** (`offres.conf`).
  - Entrée `file`, codec `json`, sortie `elasticsearch` avec `document_id => "%{id}"`.
- **Partie 2** : superviser Logstash (API `:9600`), isoler les documents refusés (*dead letter queue*), deux pipelines séparés (`pipelines.yml`).
- **Partie 3** : transformer des **logs d'accès Apache** (`web.conf`).
  - 20 700 lignes sur 7 jours, générées par `generate_access_logs.py` (TP2, l. 317-343).
  - Filtres `grok` (`COMBINEDAPACHELOG`), `date`, `useragent`.
  - Noms de champs **ECS** : `source.address`, `http.response.status_code`…
  - Sortie vers le **data stream `logs-web-default`** (`web.conf`, l. 35-44).
- **Partie 4** : enquête dans Kibana avec **KQL** et **ES|QL** (TP2, l. 438-468).
  - Retrouver un incident (erreurs 5xx), un robot (rafale de 404), les offres les plus vues, la part du mobile.
- **Partie 5** : tableau de bord **Lens** « Site de recrutement — trafic » (TP2, l. 470-482).
  - Nombre de requêtes, taux d'erreur, trafic dans le temps par code HTTP, top 10 des offres, navigateurs.
  - Une carte des offres par ville (Maps, champ `localisation`).
  - Bonus : une **règle d'alerte** « plus de 50 erreurs 5xx en 5 minutes ».

---

## 3. Les cas d'usage que le TP montre

- ✅ **Recherche dans des données métier** : barre de recherche tolérante aux fautes, pertinence, facettes (Cours, l. 46 ; TP1).
- ✅ **Analyse d'événements** : centraliser des logs, les structurer, enquêter sur un incident (Cours, l. 47 ; TP2).
- ✅ **Tableau de bord et alerte** dans Kibana (TP2, partie 5).
- ✅ **Croiser deux sources** : les offres les plus vues d'après les logs, retrouvées dans l'index `offres` en une requête (Cours, l. 462 ; TP2, ex. 4.4).
- ✅ Le cours cite aussi, sans TP : sécurité (SIEM), recherche vectorielle et hybride (Cours, l. 92).
- ✅ **Mise en garde** : Elasticsearch n'est **pas une source de vérité**. Pas de transaction, écritures visibles avec un léger retard. On y met une **copie** de données dont la référence est ailleurs, par exemple une base relationnelle (Cours, l. 94).

---

## 4. Ce qui se transpose au projet

### Piste A : la recherche de biens (`estate`)

- ✅ C'est **exactement le TP1**, avec des biens à la place des offres.
  - Un index à mapping strict, texte en français, filtres exacts, intervalles, distance (TP1, l. 461-480).
  - Recherche `bool` : texte libre + filtres, facettes, pagination, surlignage (`search.py`).
- ✅ PostgreSQL reste la référence ; l'index est une copie (Cours, l. 94).
- ✅ Prendre l'**id du bien comme `_id`** : la recharge ne crée pas de doublon (Cours, l. 414-416).
- 💡 Champs naturels : ville, type de bien, prix et surface (intervalles), position (`geo_point`), texte d'annonce (`french`).
- 💡 L'API FastAPI appellerait Elasticsearch avec le client Python, comme `search.py`, via une route de recherche.
- ⚠️ 💡 Il faut alors **tenir l'index à jour** quand un bien change en base. Le TP ne traite pas ce point : il charge un fichier une fois.

### Piste B : les logs

- ✅ C'est **le TP2** : Logstash lit un fichier de log, le découpe, l'envoie dans un data stream `logs-*` (`web.conf`).
- ✅ Les logs sont des **événements** : data stream, ajout seul, rétention limitée (Cours, l. 636-645 et l. 900-915).
- ✅ Alternatives plus légères, citées par le cours : ingest pipeline dans Elasticsearch, Filebeat ou Elastic Agent (Cours, l. 887-896).
- 💡 Cible possible : les logs d'accès de l'API FastAPI (uvicorn), ou les logs des conteneurs.
- 💡 Le format d'uvicorn n'est pas le format Apache du TP : il faudra un autre motif `grok` ou `dissect`.

### Piste C : un tableau de bord Kibana

- ✅ Le TP2 fait un tableau de bord Lens complet, avec une carte (TP2, l. 470-482).
- ✅ Kibana ne lit que ce qui est dans Elasticsearch (Cours, l. 584) : il faut d'abord un index.
- 💡 Sur des biens ou des annonces : prix moyen par ville, annonces par mois, carte des biens. Ce sont les agrégations du TP1 (ex. 4.1 à 4.3).
- 💡 Sur des logs : trafic et taux d'erreur de l'API, comme au TP2.
- 💡 Recouvrement possible avec le **modèle OLAP** : deux outils pour les mêmes indicateurs. À trancher.

### Piste D : un index alimenté par Airflow

- ✅ Le TP alimente l'index de deux façons : un **script Python** (`ingest.py`, `helpers.bulk`) et **Logstash**.
- ✅ Le cours décrit Logstash comme un **ETL de flux** (Cours, l. 672). Airflow, lui, n'est jamais cité.
- 💡 Le code de `ingest.py` (bulk, `_id` métier, lecture de la liste des erreurs) se poserait tel quel dans une tâche Airflow.
- 💡 Dans ce cas, Logstash devient inutile pour ce flux : un composant de moins.

---

## 5. Comment Elasticsearch et Airflow s'articuleraient

- ✅ **Le cours n'en dit rien.**
  - Aucune mention d'Airflow, de cron ou d'orchestration dans les trois `Readme.md` du dépôt ELK.
  - Aucune mention d'Elasticsearch dans le cours Airflow (`Supports de cours-20260827 AIRFLOW/`) : ni dans les `.md`, `.py`, `.yml`, ni dans le texte des PDF.
- ✅ Seule trace : le `.venv` du lab Airflow contient un paquet tiers **`airflow_operators` 0.11.1**, avec un `ElasticsearchBulkOperator` (`lab-Minio-Airflow-20260827/.venv/Lib/site-packages/airflow_operators/elastic.py`). C'est une bibliothèque installée, **pas du contenu de cours**. Non vérifié : qui l'a mise là, et si elle est fiable.
- 💡 Mon avis, à valider : un DAG Airflow ferait « PostgreSQL → transformation → `helpers.bulk` vers Elasticsearch ».
  - Placé après l'import des annonces, ou en DAG à part.
  - Idempotent grâce à l'`_id` métier : on peut le relancer sans risque.
  - Le fournisseur officiel `apache-airflow-providers-elasticsearch` existe : à vérifier (version, contenu) avant de choisir.

---

## 6. Les questions qui restent pour le groupe

1. **À quoi sert Elasticsearch chez nous ?** Recherche de biens, logs, tableau de bord, ou plusieurs ? Le chef de groupe ne l'a pas dit.
2. **Quelles données ?** Les biens `estate`, les annonces importées, les deux ? Avec quels champs ?
3. **Qui tient l'index à jour ?** Un DAG Airflow (par lot, avec du retard), l'API à chaque écriture (tout de suite), ou un rechargement complet ?
4. **Logstash : oui ou non ?** Utile pour des logs. Inutile si Airflow pousse lui-même les données.
5. **Kibana et le modèle OLAP** : qui sert à quoi, pour ne pas faire deux fois les mêmes indicateurs ?
6. **La RAM** : environ 4 Go de plus. Les postes du groupe tiennent-ils avec PostgreSQL, l'API et Airflow ?
7. **Le `docker-compose.yml` du projet** : il faut y ajouter les services. Ce fichier est chasse gardée : accord de Seb avant toute modif.
8. **La sécurité** : on garde celle du TP (activée, TLS coupé, compte dédié, `.env` non versionné) ?
9. **Le prof attend-il un usage précis ?** Le cours n'en impose aucun pour le projet.

# Tuto : lancer toute la pile, conteneur par conteneur

> Écrit le 2026-10-15, à la fin du chantier FLX (flux de données), à la demande
> de Sébastien. Pour toute l'équipe, débutants compris.
> Les commandes se tapent **depuis le dossier `docker/` du dépôt Fil-Rouge-API**.
> Sources : `API/README.md` (sections « Les profils », « Elasticsearch et
> Kibana », « Airflow »), `docker/.env.exemple`, `md/flux/schema-du-flux.md`,
> ADR-062 (profils).

## En bref

- Le projet tourne dans **11 conteneurs** Docker.
- Ils sont rangés en **3 groupes**, appelés **profils** :
  - **sans profil** : la base et l'API, toujours lancées ;
  - **`airflow`** : les traitements de nuit ;
  - **`elk`** : la recherche et les logs (Elasticsearch, Logstash, Kibana).
- On lance seulement ce dont on a besoin : chaque profil coûte de la mémoire.
- Tout lancer prend **≈ 5 Go** de RAM. Prévoir **6 Go** pour Docker.

## 1. Une seule fois : remplir `docker/.env`

`docker/.env` garde les mots de passe. Il n'est **jamais** dans git.
Son modèle, `docker/.env.exemple`, explique chaque ligne.

Le chantier FLX ajoute **9 lignes**. Chaque valeur se tire au hasard, avec la
commande que le modèle donne au-dessus de la ligne (`openssl rand -hex 16` ou
`-hex 32`). Seule `AIRFLOW_FERNET_KEY` a sa propre commande : une clé en base64.

| Ligne | Pour quoi | Profil |
|---|---|---|
| `AIRFLOW_DB_PASSWORD` | le compte `airflow` de PostgreSQL | `airflow` |
| `AIRFLOW_ADMIN_PASSWORD` | le compte `admin` de l'interface Airflow | `airflow` |
| `AIRFLOW_FERNET_KEY` | chiffre les mots de passe des connexions Airflow | `airflow` |
| `ELASTIC_PASSWORD` | le compte `elastic`, celui des humains | `elk` |
| `KIBANA_PASSWORD` | le compte interne de Kibana | `elk` |
| `KIBANA_ENCRYPTION_KEY` | chiffre les objets de Kibana (32 caractères au moins) | `elk` |
| `ES_INDEXER_PASSWORD` | le compte d'Airflow qui remplit l'index `estates` | `elk` |
| `ES_API_PASSWORD` | le compte de l'API qui lit l'index `estates` | `elk` |
| `LOGSTASH_INTERNAL_PASSWORD` | le compte de Logstash qui écrit les logs | `elk` |

⚠️ Les mots de passe d'Elasticsearch : **ni guillemet `"` ni antislash `\`**.
Ils entrent dans un JSON.

## 2. Dans quel ordre lancer

### Étape 1 — la base et l'API (sans profil)

```bash
docker compose up -d --build
```

- ✅ Lance `db` et `api`. C'est tout ce qu'il faut pour coder l'API.
- Swagger : http://localhost:8000/docs
- Après le pull du chantier PRF : refaire la base, puis le seed de démo
  (voir la liste « À faire », message 1/5).

### Étape 2 — Airflow (profil `airflow`)

⚠️ **Piège : `AIRFLOW_DB_PASSWORD` n'est lu qu'à la création de la base.**
Une base de dev déjà créée (le cas de toute l'équipe) n'a ni la base `airflow`
ni son rôle. Une fois, avant le premier lancement :

```bash
docker compose up -d db
docker compose exec db bash /docker-entrypoint-initdb.d/07_airflow-base.sh
```

Le script ne crée que ce qui manque : on peut le relancer sans risque.
Ensuite :

```bash
docker compose --profile airflow up -d --build
```

- Interface : http://localhost:8080, compte `admin`.
- Les DAG naissent **en pause**. Pour qu'ils tournent chaque nuit : les
  activer dans l'interface (l'interrupteur à gauche de leur nom).

### Étape 3 — Elasticsearch, Logstash, Kibana (profil `elk`)

```bash
docker compose --profile elk up -d
```

- Elasticsearch : http://localhost:9200 · Kibana : http://localhost:5601,
  compte `elastic`.
- Kibana démarre après Elasticsearch et `es-setup` : attendre que
  `curl -s localhost:5601/api/status` réponde `"level":"available"`.

**Une fois** : importer le tableau de bord de Kibana.

```bash
( set -a; . ./.env; set +a; curl -s -u "elastic:$ELASTIC_PASSWORD" -H "kbn-xsrf: true" \
  -F file=@kibana/dashboards.ndjson "localhost:5601/api/saved_objects/_import?overwrite=true" )
```

Puis Kibana → Dashboards → « Fil Rouge — trafic de l'API et biens ».

### Étape 4 — remplir les données

Dans cet ordre, car chaque étape lit ce que la précédente a écrit :

1. Des ventes en volume, pour l'OLAP (500 par défaut) :
   `docker compose exec api python -m src.app.scripts.seed_volume`
2. Les annonces : `docker compose exec airflow-scheduler airflow dags test annonces_import 2026-10-15`
3. Les chiffres de ventes : `docker compose exec airflow-scheduler airflow dags test olap_refresh 2026-10-15`
4. L'index de recherche : `docker compose exec airflow-scheduler airflow dags test estates_index 2026-10-15`

La nuit, Airflow fait 2, 3 et 4 tout seul, à **2 h**, **3 h** et **4 h**.

### Tout d'un coup

```bash
docker compose --profile "*" up -d --build
```

Les étapes « une fois » (script `07_airflow-base.sh`, import du tableau de
bord) restent à faire.

## 3. Chaque conteneur : à quoi il sert, pourquoi il est là

Mémoire mesurée au repos le 2026-10-15 vers 16 h 30 (`docker stats --no-stream`).

| Conteneur | Profil | À quoi il sert | Pourquoi il est là | Mémoire |
|---|---|---|---|---|
| `db` | aucun | PostgreSQL : les 22 tables du métier, le schéma `olap`, et la base `airflow` | toutes les données du projet | 125,9 Mio |
| `api` | aucun | l'API FastAPI, port 8000 | ce que l'app appelle ; c'est le cœur du projet | 108,4 Mio |
| `minio` | `airflow` | un stockage de fichiers (comme Amazon S3) : buckets `bronze`, `silver`, `gold`, `quarantine` | garder chaque étape du nettoyage des annonces, pour pouvoir relire et rejouer | 133,5 Mio |
| `minio-setup` | `airflow` | crée les 4 buckets, puis s'arrête | une seule fois au démarrage | — |
| `airflow-init` | `airflow` | crée les tables d'Airflow et le compte `admin`, puis s'arrête | une seule fois au démarrage | — |
| `airflow-webserver` | `airflow` | l'interface d'Airflow, port 8080 | voir les DAG, leurs journaux, en lancer un à la main ; **n'exécute rien** | 893,7 Mio |
| `airflow-scheduler` | `airflow` | regarde l'heure **et exécute** les tâches Python des DAG | c'est lui qui fait le travail de nuit (`LocalExecutor`) | 525 Mio |
| `elasticsearch` | `elk` | le moteur de recherche, port 9200 : index `estates` et logs de l'API | chercher un bien vite (`GET /estates/search`) et garder les logs | 1 746 Mio (plafond 2 Gio) |
| `es-setup` | `elk` | crée les comptes d'Elasticsearch (Kibana, Airflow, API, Logstash), puis s'arrête | chaque programme a son compte, limité à ce qu'il doit faire | — |
| `logstash` | `elk` | relit le journal de l'API et le range dans Elasticsearch | amener les logs jusqu'à Kibana | 648,7 Mio (plafond 1 Gio) |
| `kibana` | `elk` | les tableaux de bord, port 5601 | voir le trafic de l'API, les erreurs, la carte des biens | 914,6 Mio (plafond 1 Gio) |

ℹ️ `minio-setup`, `airflow-init` et `es-setup` font leur travail puis
s'arrêtent : **« Exited (0) » est normal**. Pas de mémoire mesurée pour eux.

## 4. Combien de mémoire

| Ce qu'on lance | Commande | Mémoire au repos |
|---|---|---|
| base + API | `docker compose up -d` | ≈ 234 Mio |
| + Airflow | `--profile airflow` | ≈ 1 552 Mio de plus |
| + ELK | `--profile elk` | ≈ 3 309 Mio de plus |
| tout | `--profile "*"` | ≈ 5,0 Gio |

- Conseil : **6 Go pour Docker** si tout tourne.
- Machine trop juste : arrêter un profil dont on ne se sert pas, par exemple
  `docker compose --profile elk stop`.
- Docker Desktop sous Windows prend sa mémoire dans WSL 2 : la régler dans
  `%UserProfile%\.wslconfig` (section `[wsl2]`, ligne `memory=8GB`), puis
  `wsl --shutdown` et relancer Docker Desktop.

## 5. Les pièges connus

- **`AIRFLOW_DB_PASSWORD` lu seulement à la création de la base** : voir
  l'étape 2.
- **MinIO ne démarre plus seul** : il faut `--profile airflow`.
- **Elasticsearch refuse de démarrer** avec
  `vm.max_map_count [65530] is too low` : lancer
  `wsl -d docker-desktop -u root sysctl -w vm.max_map_count=262144`,
  à refaire après chaque redémarrage de Windows.
- **Code de sortie 137** : le conteneur a été tué faute de mémoire. Voir la
  section 4.
- **`ELASTIC_PASSWORD` faux, ou `KIBANA_PASSWORD` vide ou trop court** :
  `es-setup` s'arrête tout de suite, en erreur, et **Kibana ne démarre pas**.
  Son log dit pourquoi : « Mot de passe elastic refusé (HTTP 401) », ou la
  réponse d'Elasticsearch (« passwords must be at least [6] characters long »).
  Lire le log : `docker compose logs es-setup`.
- **`ES_INDEXER_PASSWORD`, `ES_API_PASSWORD` ou `LOGSTASH_INTERNAL_PASSWORD`
  vide** : le compte qui va avec n'est pas créé. Kibana démarre quand même, mais
  la fonction qui s'en sert rend une erreur (par exemple `GET /estates/search`
  rend `503`).
- **Graphiques de trafic vides dans Kibana** : la période par défaut est les
  dernières 24 h. Appeler l'API quelques fois, puis rafraîchir.

## 6. Vérifier que tout marche

```bash
docker compose --profile "*" ps
```

- `db`, `api`, `minio`, `airflow-webserver`, `airflow-scheduler`,
  `elasticsearch`, `logstash`, `kibana` : **Up**, et **healthy** pour ceux qui
  ont un test de santé.
- `minio-setup`, `airflow-init`, `es-setup` : **Exited (0)**.

Pour aller plus loin : le dessin du flux, `md/flux/schema-du-flux.md`.

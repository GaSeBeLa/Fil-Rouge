# Note d'environnement technique — et son volet green IT

> Compétence : « Recommander un environnement informatique en intégrant les techniques de réduction d'impact écologique » — « Note d'environnement technique + volet green IT » (`documents utiles/TRACABILITE-COMPETENCES.md:63`, StarterPack). Phases 3 et 4, bloc BC03.
> Rédigée le 2026-11-20 par le Glaude. Tout chiffre vient du dépôt `Fil-Rouge-API` (`docker/docker-compose.yml`, `API/Dockerfile`, `API/requirements.txt`, lus le 2026-11-20) ou d'une mesure déjà publiée, citée à côté.
> Statuts : ✅ établi (lu ou mesuré) · 💡 proposé · ⚠️ limite connue.

---

## 1. L'environnement d'aujourd'hui : tout en local, sous Docker

Un seul fichier lance tout : `docker/docker-compose.yml`. Les services lourds ne démarrent qu'à la demande, par **profil** (ADR-062).

| Groupe | Services | Version | Ports | Mémoire au repos |
|---|---|---|---|---|
| **Toujours lancé** | `db` (PostgreSQL), `api` (FastAPI) | `postgres:16` ; `python:3.12-slim` | 5432 ; 8000 (Swagger : `/docs`) | **≈ 234 Mio** |
| **Profil `airflow`** | `minio`, `minio-setup`, `airflow-init`, `airflow-webserver`, `airflow-scheduler` | Airflow 2.11.2 ; MinIO épinglé par empreinte (`sha256`) | 9000, 9001 ; 8080 | **≈ 1,5 Gio** |
| **Profil `elk`** | `elasticsearch`, `es-setup`, `kibana`, `logstash` | 9.5.4 | 9200 ; 5601 ; 9600 (supervision de Logstash), ouverts sur la machine seule (`127.0.0.1`) | **≈ 3,2 Gio** |

✅ Mémoire mesurée le 2026-10-15 (ADR-062) : **5,0 Gio** avec tous les profils, **234 Mio** pour qui ne travaille que sur l'API. Le schéma : `04-pile-docker.md`.

**Les briques du code** (`API/requirements.txt`) : FastAPI 0.143.0, SQLModel 0.0.48, uvicorn 0.54.0, psycopg2-binary 2.9.13, argon2-cffi 25.1.0, PyJWT 2.15.1. Tests : pytest, 1 116 réussis (commit `31094a8`).

**Lancer** (depuis `Fil-Rouge-API/docker/`) :
- l'API seule : `docker compose up -d` ;
- avec le flux de données : `docker compose --profile airflow up -d` ;
- avec la recherche et les logs : `docker compose --profile elk up -d`.

## 2. Pourquoi ces choix

| Choix | Raison | Source |
|---|---|---|
| PostgreSQL, une instance | un seul moteur pour le métier et l'analyse (schéma `olap` à part) ; 133 Go à 2 ans y tiennent | ADR-001 ; matrice de décision (option B) |
| Docker Compose, pas Kubernetes | 4 personnes, un poste chacun, pas de production : l'orchestration lourde n'apporte rien | dossier d'architecture |
| Images à version fixe | le même environnement pour tous, et un retour arrière possible | ADR-015 |
| Profils | chacun ne lance que ce dont il a besoin | ADR-062 |
| Outils libres et gratuits | aucun coût de licence, aujourd'hui comme à la croissance | note de cadrage, § 3 bis |

⚠️ **Un écart à ADR-015** : `postgres:16` fixe la version majeure, pas la mineure (le conteneur tourne en 16.15). À épingler en `postgres:16.15` avant une mise en production.

## 3. Le volet green IT : ce qui réduit l'impact, déjà en place

- ✅ **Lancer à la demande** : 234 Mio au lieu de 5,0 Gio pour le travail courant, soit **environ 22 fois moins** de mémoire (ADR-062).
- ✅ **Traiter la nuit, pas en continu** : trois traitements planifiés (import 2 h, OLAP 3 h, index 4 h), au lieu de flux allumés en permanence.
- ✅ **Ne pas copier ce qui existe ailleurs** : les photos des annonces sont liées, pas copiées ; de 29 à 188 To de stockage évités (note 3V, § 7).
- ✅ **Des index posés après mesure, pas par défaut** : 3 index, de 15 à 100 fois plus rapides ; chaque index en plus coûterait de la place et ralentirait l'écriture (note d'indexation).
- ✅ **Elasticsearch sans copie inutile** : 1 shard, 0 réplique, mémoire bornée (`-Xmx1g`, `mem_limit` 2 Go).
- ✅ **Des images légères** : `python:3.12-slim` pour l'API.
- ✅ **Sauvegarder juste** : une copie complète par jour + les journaux WAL, plutôt qu'une copie à la minute (note d'éco-conception).

## 4. Recommandation pour la croissance (💡 proposé)

| Étape | Environnement | Déclencheur |
|---|---|---|
| Aujourd'hui | un poste, Docker Compose, profils | — |
| Mise en production | **une machine virtuelle de 8 Go de mémoire** (5,0 Gio mesurés + marge), dans un centre de données en Europe (RGPD) ; PostgreSQL épinglé ; sauvegarde quotidienne + WAL planifiée | la première agence rachetée |
| Croissance | **une réplique PostgreSQL** en lecture (reprise et lectures) ; Elasticsearch sur sa propre machine | les lectures ralentissent le métier, mesuré |
| Grand volume | **partitionner** les deux tables de liens par mois ou par pays | elles dépassent quelques dizaines de Go (84 à 87 % du volume, note 3V) |

Pour l'impact écologique, la règle reste la même à chaque étape : **ajouter une machine seulement quand une mesure le demande**, et préférer un hébergeur qui publie l'énergie et l'origine de son électricité. 💡 Le choix de l'hébergeur n'est pas fait : aucun budget n'est communiqué (note de cadrage, § 7).

## 5. Limites, dites franchement

- ⚠️ **Aucune mesure d'énergie** : on mesure la mémoire et le temps, pas les watts.
- ⚠️ **Aucune mesure de charge** : les déclencheurs du § 4 sont conçus, pas éprouvés (dossier d'architecture, § 6).
- ⚠️ **Pas de sauvegarde planifiée** aujourd'hui : la politique est écrite, pas codée (PCA/PRA).
- ⚠️ Airflow 2.11.2 est en fin de vie depuis avril 2026 (ADR-059).

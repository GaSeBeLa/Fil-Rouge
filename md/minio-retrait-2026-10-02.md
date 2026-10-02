# MinIO retiré du projet — 2026-10-02

## En une phrase

MinIO **existe toujours**, mais sa version **gratuite prête à l'emploi**
a disparu : on ne peut plus la télécharger, donc on l'a retirée du
`docker-compose.yml`.

## Ce qu'était MinIO dans le projet

- Un **stockage de fichiers** compatible S3 (le format d'Amazon).
- Prévu pour l'architecture en couches : buckets `bronze`, `silver`, `gold`.
- ✅ Dans les faits : **aucun code** du projet ne l'utilisait.
  Seul le compose créait les 3 buckets au démarrage.

## Ce qui a changé chez MinIO

| Date | Ce qui s'est passé | Source |
|---|---|---|
| 2026-04-25 | Le dépôt GitHub `minio/minio` est **archivé** : lecture seule, plus de mises à jour | [github.com/minio/minio](https://github.com/minio/minio) — dépôt officiel, lu le 2026-10-02 |
| 2026-09-11 | Les images `minio/minio` et `minio/mc` sont **supprimées** de Docker Hub | [flowershow#1382](https://github.com/flowershow/flowershow/issues/1382) — issue GitHub, 2026-09-18 |
| fin 09/2026 | Sur `quay.io`, les images demandent un **compte** | [LibreChat code-interpreter#252](https://github.com/LibreChat-AI/code-interpreter/issues/252), [bex.co](https://bex.co/blog/2026/09/25/minio-docker-hub-removal-quay-repoint) — issue et blog, vus en extrait seulement |

Le README officiel le dit lui-même :
« The MinIO community edition is now distributed as source code only. »

➡️ Ce qui reste chez MinIO :

- le **code source** (licence AGPLv3) — à compiler soi-même ;
- **AIStor Free** et **AIStor Enterprise** — leurs produits sous licence
  commerciale.

## Ce qu'on a constaté chez nous

- `docker compose up` échouait en **entier** :
  `Error response from daemon: unauthorized`.
- Raison : si **une seule** image ne se télécharge pas, Docker arrête
  **tout** — la base et l'API aussi.
- Testé le 2026-10-02 avec `docker manifest inspect` :
  - ❌ **6** images MinIO refusées (`quay.io` et Docker Hub, `minio` et `mc`)
  - ✅ `postgres:16` passe → ce n'est pas notre installation Docker.

## Ce qu'on a fait

- Retiré les services `minio`, `minio-setup` et le volume `minio_data` de
  `docker/docker-compose.yml` (commit `498f24a`).
- Résultat vérifié : `docker compose up -d` relance `db` et `api`, Swagger
  répond **HTTP 200**.
- `.env.exemple` garde `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` :
  inutilisés, sans danger.

## 🟡 À décider en groupe

Le jour où le projet aura besoin d'un stockage de fichiers, choisir un
remplaçant. Les 3 images se téléchargent (testé le 2026-10-02).

| Option | Licence | Maturité |
|---|---|---|
| SeaweedFS (`chrislusf/seaweedfs`) | Apache 2.0 | utilisé en production depuis 2015 |
| RustFS (`rustfs/rustfs`) | Apache 2.0 | encore en alpha |
| Garage (`dxflrs/garage`) | AGPL-3.0 | utilisé en production depuis 2020 |

Source du comparatif : [elest.io](https://blog.elest.io/rustfs-vs-seaweedfs-vs-garage-which-minio-alternative-should-you-pick/)
et [lowcloud](https://lowcloud.io/en/blog/minio-alternatives) — blogs, 2026,
vus en extrait seulement.

## ⚠️ Pour l'équipe

Qui a encore l'ancien compose aura la **même erreur** : faire un `git pull`.

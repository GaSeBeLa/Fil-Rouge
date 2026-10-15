### ADR-062 : Le compose se découpe en profils, et l'API seule reste légère

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 15/10/2026
* **Statut :** ✅ accepté (Sébastien, Discord, 15/10/2026, question `flux-10`). Pas encore publié sur Confluence.
* **Décideurs :** Sébastien.
* **Voir aussi :** ADR-059 (Airflow) ; ADR-060 (MinIO) ; ADR-061 (Elasticsearch)

**Contexte**

* Avec Airflow, Elasticsearch, Kibana et Logstash, le compose passe de 2 services à 11. Les machines de l'équipe ne sont pas toutes grosses.
* La doc de Compose : un service sans profil se lance toujours ; un service avec profil ne se lance que si on demande son profil.

**Options**

1. **Trois groupes : sans profil, `airflow`, `elk`.** **Retenue.**
2. Tout lancer toujours. Écartée : environ 5 Gio de mémoire pour qui ne travaille que sur l'API.
3. Un fichier compose par outil. Écartée : plusieurs fichiers à tenir d'accord, et plus dur à lancer.

**Décision**

| Commande, depuis `docker/` | Services lancés |
|---|---|
| `docker compose up -d` | `db`, `api` |
| `docker compose --profile airflow up -d` | en plus : `minio`, `minio-setup`, `airflow-init`, `airflow-webserver`, `airflow-scheduler` |
| `docker compose --profile elk up -d` | en plus : `elasticsearch`, `es-setup`, `kibana`, `logstash` |
| `docker compose --profile "*" up -d` | tout |

**Conséquences**

* Mémoire mesurée au repos le 15/10/2026 (`docker stats --no-stream`) : sans profil ≈ 234 Mio ; `airflow` ≈ 1 552 Mio ; `elk` ≈ 3 309 Mio ; tout ≈ 5,0 Gio (détail : `md/flux/schema-du-flux.md`).
* `elasticsearch`, `kibana` et `logstash` ont un plafond de mémoire (2 Gio, 1 Gio, 1 Gio). Le README de l'API conseille 6 Go pour Docker si tout tourne.
* Au jury, une phrase : « `docker compose up -d` lance l'API seule ; les outils de données se lancent à la demande, par profil ».

**Ce que cet ADR ne tranche pas**

* 🟡 La taille du serveur pour un déploiement (VPS) : hors du chantier.

**Sources**

| Affirmation | Source |
|---|---|
| Découpage en trois groupes | Sébastien, Discord, 15/10/2026, question `flux-10` |
| Règle des profils : « Services without a `profiles` attribute are always enabled », et `--profile "*"` | doc officielle, [Using profiles with Compose](https://docs.docker.com/compose/how-tos/profiles/), lue le 15/10/2026 |
| Mémoire mesurée | `docker stats --no-stream`, 15/10/2026, vers 16 h 30 |
| Services et plafonds | `docker/docker-compose.yml` (dépôt Fil-Rouge-API) |

### ADR-060 : MinIO garde les étapes du flux, en quatre buckets

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 15/10/2026
* **Statut :** ✅ accepté (Sébastien, Discord, 15/10/2026, questions `flux-2` et `flux-11`). Publié sur Confluence le 15/10/2026, dans « Proposé », pour relecture par le groupe.
* **Décideurs :** Sébastien.
* **Voir aussi :** ADR-015 (MinIO, stockage objet) ; ADR-051 (médias de la note d'avis) ; ADR-059 (Airflow)

**Contexte**

* MinIO est déjà dans le compose de l'API depuis le 01/09/2026, avec trois buckets `bronze`, `silver` et `gold`, mais rien ne s'en servait (« minio » : 0 résultat dans `API/src`, ADR-051).
* Le cours d'Airflow range les données en trois zones, `raw`, `cleansed` et `curated`, et met de côté les lignes rejetées, avec leur raison (`md/flux/cours-airflow-synthese.md`).

**Options**

1. **Garder MinIO et ses trois buckets, et ajouter `quarantine`.** **Retenue.**
2. Renommer les buckets comme le cours (`raw`, `cleansed`, `curated`). Écartée : même rôle, et les noms existants étaient déjà là.
3. Écrire les fichiers sur le disque d'Airflow. Écartée : rien ne se garde d'un conteneur à l'autre, et MinIO était prévu pour ça (ADR-015).

**Décision**

| Bucket | Zone du cours | Ce qu'il garde |
|---|---|---|
| `bronze` | `raw` | le CSV brut du générateur, tel quel : `annonces/{ds}/annonces.csv` |
| `silver` | `cleansed` | les annonces valides : `annonces/{ds}.json` |
| `quarantine` | lignes rejetées | les rejets, avec `_reject_reason`, `_reject_ts`, `_source_file` : `annonces/{ds}.json` |
| `gold` | `curated` | le bilan de chargement de l'OLAP : `olap/{ds}.json` |

* `{ds}` est la date logique du DAG : rejouer une date relit le même brut et réécrit les mêmes fichiers.
* Le service `minio-setup` crée les quatre buckets au démarrage du profil `airflow`.

**Conséquences**

* Une annonce rejetée se retrouve, avec sa raison, sans relancer le flux.
* Au jury, une phrase : « chaque étape du flux laisse sa trace dans MinIO : le brut, le propre, les rejets, le bilan ».

**Ce que cet ADR ne tranche pas**

* 🟡 La durée de garde des fichiers : rien ne les efface aujourd'hui.

**Sources**

| Affirmation | Source |
|---|---|
| Buckets gardés, `quarantine` ajouté | Sébastien, Discord, 15/10/2026, questions `flux-2` et `flux-11` |
| Zones et quarantaine du cours | `md/flux/cours-airflow-synthese.md` |
| MinIO présent, inutilisé dans l'API | ADR-051, « minio » : 0 résultat dans `API/src` |
| Chemins des fichiers | `airflow/dags/annonces_import_dag.py`, `airflow/dags/olap_refresh_dag.py` (dépôt Fil-Rouge-API) |

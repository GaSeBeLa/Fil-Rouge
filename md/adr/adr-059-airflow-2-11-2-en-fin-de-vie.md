### ADR-059 : Airflow 2.11.2, une version en fin de vie, choisie en connaissance de cause

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 15/10/2026
* **Statut :** ✅ accepté (Sébastien, Discord, 15/10/2026, question `flux-1b`, qui remplace `flux-1`). Pas encore publié sur Confluence.
* **Décideurs :** Sébastien.
* **Voir aussi :** ADR-045, limite 7 (import des annonces par un flux Airflow) ; ADR-062 (profils Compose)

**Contexte**

* Le groupe a choisi d'importer les annonces par un flux Airflow (ADR-045, limite 7, acceptée le 09/10/2026).
* Le cours d'Airflow utilise l'image `apache/airflow:2.9.3`, avec `LocalExecutor` (`md/flux/cours-airflow-synthese.md`).
* La doc officielle (page « Supported versions », lue le 15/10/2026) dit que **la branche 2 d'Airflow est en fin de vie depuis le 22/04/2026**, et que sa dernière version est la **2.11.2**. La version stable du moment est la 3.3.2.

**Options**

1. **2.9.3**, la version du cours. Écartée : plus ancienne que la dernière 2, sans rien de plus.
2. **2.11.2**, la dernière version 2. **Retenue.**
3. **3.3.2**, la version stable. Écartée : Airflow 3 change la façon d'écrire et de lancer les DAG, et le cours ne le couvre pas. Passer à Airflow 3 est hors du chantier.

**Décision**

1. L'image est `apache/airflow:2.11.2`, avec `LocalExecutor` (`airflow/Dockerfile`, dépôt Fil-Rouge-API).
2. Les DAG s'écrivent comme dans le cours : `with DAG(...)` et `PythonOperator`, sans TaskFlow.
3. La base d'Airflow est une base `airflow` dans notre PostgreSQL (service `db`), jamais mêlée à `fil_rouge_immobilier` (question `flux-3`).

**Conséquences**

* Plus aucun correctif de sécurité ne sortira pour cette version. C'est acceptable pour un projet de cours qui tourne en local, pas pour une mise en production.
* Au jury, une phrase : « Airflow 2 est en fin de vie depuis avril 2026 ; on a pris sa dernière version pour rester au plus près du cours, et le passage à Airflow 3 est le premier chantier si le projet vit. »

**Ce que cet ADR ne tranche pas**

* 🟡 Le passage à Airflow 3, et quand.

**Sources**

| Affirmation | Source |
|---|---|
| Choix de 2.11.2 | Sébastien, Discord, 15/10/2026, question `flux-1b` |
| Fin de vie le 22/04/2026, dernière version 2.11.2 | doc officielle, [Supported versions](https://airflow.apache.org/docs/apache-airflow/stable/installation/supported-versions.html), lue le 15/10/2026 |
| Image 2.9.3 et `LocalExecutor` dans le cours | `md/flux/cours-airflow-synthese.md` |
| Base `airflow` dans notre PostgreSQL | Sébastien, Discord, 15/10/2026, question `flux-3` |
| Flux Airflow accepté par le groupe | ADR-045, limite 7 |

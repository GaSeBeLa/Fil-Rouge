# Note d'éco-conception — ce qui change au 2026-11-03

> Brouillon, à relire par l'équipe (vote Q2 A du 2026-11-03). La note de
> Gabriel (Confluence, 2 sept.) garde tout son fond : l'arbitrage
> « coût de perte × coût de sauvegarde » reste juste. Ce document liste
> **seulement** ce qui a changé dans le projet depuis, pour que l'équipe
> corrige la page. Statuts : ✅ vérifié dans le code · 🟡 à décider · 💡 proposé.

## 1. Les corrections — la note dit autre chose que le code

| Ce que dit la note | Ce qui est vrai aujourd'hui | Preuve |
|---|---|---|
| « 11 tables » (Méthode suivie, point 1) | **22 tables** | `grep -c "^CREATE TABLE" docker/init-v3/01_create_fil_rouge_immobilier.sql` → 22 |
| `estate_searchrequest.media_url` | les médias vivent dans la table **`review_media`** (`media_url`, `media_type` audio ou vidéo) | même fichier, l.879-890 |
| Couche **Gold** dans MinIO | le décisionnel est un **schéma OLAP dans PostgreSQL** (`docker/init-v3/08_olap.sql`), rafraîchi par le DAG `olap_refresh` | `airflow/dags/olap_refresh_dag.py:62` |
| Bronze purgé après « ex. 7 jours » | ✅ Bronze et Silver existent dans MinIO, plus un bucket **quarantine** pour les rejets ; ⚠️ **aucune purge n'est codée** : le brut est gardé | `airflow/dags/annonces_import_dag.py:7-13, 56-79` |

## 2. Les ajouts — ce qui est né depuis septembre

| Élément | Sa nature | Arbitrage proposé 💡 |
|---|---|---|
| Index **Elasticsearch** `estates` (DAG `estates_index`, 4 h) | entièrement **reconstruit** depuis `estate` chaque nuit | **aucune sauvegarde** : comme Bronze, il se régénère |
| Logs de l'API dans **Logstash → Elasticsearch → Kibana** | volume qui grossit chaque jour | ⚠️ **aucune durée de rétention n'est réglée** (rien dans `docker/logstash/` ni `docker/kibana/`). ✅ **Voté le 2026-11-03 : 6 mois**, puis suppression — le bas de la fourchette « entre six mois et un an » de la CNIL ([recommandation journalisation, délibération n° 2021-122](https://cnil.fr/la-cnil-publie-une-recommandation-relative-aux-mesures-de-journalisation), 18 nov. 2021). ⚠️ Pas encore réglé dans Elasticsearch : à coder |
| **`estate_price_history`** (prix vu à une date) | grossit à chaque import | copie 24 h, comme `estate` ; purgée avec le bien archivé |
| **`estate_contact`** (contact du vendeur) | **donnée personnelle** | durée fixée par la note **RGPD**, que celle-ci reprend sans la redéfinir |
| **`hunter_performance`** (journal daté du score) | petit volume, sert la rémunération | copie 24 h, gardée comme le paiement (10 ans, obligation comptable, page RGPD) |

## 3. Les fréquences réelles des traitements

La note proposait « quotidien » pour l'ingestion et les agrégats. C'est ce qui
est codé, en trois DAG enchaînés la nuit :

| Heure | DAG | Ce qu'il fait |
|---|---|---|
| 2 h | `annonces_import` | bronze → silver → `estate` |
| 3 h | `olap_refresh` | rafraîchit le schéma OLAP |
| 4 h | `estates_index` | reconstruit l'index `estates` |

Source : la ligne `schedule=` de chaque fichier dans `airflow/dags/`.

## 4. Un nouvel argument éco : la suggestion à la demande

- ✅ Le moteur de suggestion (chantier SUG) se lance **quand le chasseur le
  demande** (`POST /search-requests/{id}/suggestions`), pas chaque nuit pour
  toutes les demandes.
- ➡️ C'est la règle de la note, appliquée : « une fréquence se justifie par la
  vitesse à laquelle la réalité change ». Une demande dont personne ne s'occupe
  ne coûte aucun calcul.
- 💡 Le DAG de nuit pour le chasseur IA, s'il vient, ne traitera que les
  demandes qui lui sont confiées.

## 5. Tranché le 2026-11-03 (Discord, Seb et amethyste ; Gabriel absent)

- ✅ Logs Kibana : **6 mois** (Q4 D).
- ✅ Purge de Bronze : **reste sur le papier** (Q5 A). La note doit le dire : « proposée, non codée — le brut est gardé ».

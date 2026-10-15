# Flux de données : Airflow et Elasticsearch — notes et journal
## Résultat
Trois DAG tournent chaque nuit (annonces, OLAP, index), la recherche de biens passe par GET /estates/search, et Kibana montre le trafic de l'API
## Notes
- FLX1 : up -d : 2 services (api, db) ; --profile airflow : /health metadatabase healthy, scheduler healthy ; psql -l : airflow à côté de fil_rouge_immobilier ; pytest 975 passed, 7 xfailed (= clôture PRF)
- FLX2 : Dossier airflow/, connexions MinIO et PostgreSQL, un DAG d'essai ; dépend de FLX1
- FLX3 : Nettoyer et valider une annonce en Python pur, rejets avec raison ; dépend de FLX2
- FLX4 : DAG annonces_import, source_reference et historique des prix (migrations 48, 49) ; dépend de FLX3
- FLX5 : Schéma olap : fait_ventes et 5 dimensions du sujet, sans donnée personnelle ; dépend de FLX2
- FLX6 : DAG olap_refresh, rejouable, rapport qualité ; dépend de FLX5
- FLX7 : Elasticsearch et Kibana 9.5.4 dans le profil elk ; dépend de FLX1
- FLX8 : DAG estates_index : estate vers l'index estates, sans contact du vendeur ; dépend de FLX4, FLX7
- FLX9 : Route GET /estates/search, 503 si Elasticsearch est absent ; dépend de FLX8
- FLX10 : Logs JSON de l'API, Logstash, data stream logs-api-default ; dépend de FLX7
- FLX11 : Tableau de bord Kibana : trafic et carte des biens (visuel) ; dépend de FLX8, FLX10
- FLX12 : Doc, schéma du flux avec les vrais noms, ADR ; dépend de toutes
## Journal
## Bilan

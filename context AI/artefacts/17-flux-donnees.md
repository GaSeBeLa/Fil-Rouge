# Flux de données : Airflow et Elasticsearch — notes et journal
## Résultat
Trois DAG tournent chaque nuit (annonces, OLAP, index), la recherche de biens passe par GET /estates/search, et Kibana montre le trafic de l'API
## Notes
- FLX1 : up -d : 2 services (api, db) ; --profile airflow : /health metadatabase healthy, scheduler healthy ; psql -l : airflow à côté de fil_rouge_immobilier ; pytest 975 passed, 7 xfailed (= clôture PRF)
- FLX2 : pytest airflow/tests : 10 passed (mutant : 2 failed) ; dags test smoke_dag : state=success, 2556 biens ; mc ls : bronze/smoke/2026-10-15.json (40 o) et quarantine/ ; API 975 passed, 7 xfailed
- FLX3 : pytest airflow/tests : 71 passed (mutant prix ÷ 1000 : 5 failed) ; annonces.csv : 2556 lus, 2556 valides, 0 rejeté ; étages et somme des prix (519 169 839 €) identiques à la base
- FLX4 : DAG annonces_import, clé estate.reference (flux-16) et historique des prix (migration 48) ; dépend de FLX3
- FLX5 : Schéma olap : fait_ventes et 5 dimensions du sujet, sans donnée personnelle ; dépend de FLX2
- FLX6 : DAG olap_refresh, rejouable, rapport qualité ; dépend de FLX5
- FLX7 : Elasticsearch et Kibana 9.5.4 dans le profil elk ; dépend de FLX1
- FLX8 : DAG estates_index : estate vers l'index estates, sans contact du vendeur ; dépend de FLX4, FLX7
- FLX9 : Route GET /estates/search, 503 si Elasticsearch est absent ; dépend de FLX8
- FLX10 : Logs JSON de l'API, Logstash, data stream logs-api-default ; dépend de FLX7
- FLX11 : Tableau de bord Kibana : trafic et carte des biens (visuel) ; dépend de FLX8, FLX10
- FLX12 : Doc, schéma du flux avec les vrais noms, ADR ; dépend de toutes
## Journal
- 2026-10-15 : FLX3 : la clé d'annonce est `estate.reference` (déjà VARCHAR(50) NOT NULL UNIQUE, remplie sur 2556 biens sur 2556) ; pas de `source_reference` (question flux-16, tranchée A par Seb, MPD corrigé). Migrations renumérotées : 48 = estate_price_history (FLX4), 49 = olap (FLX5).
## Bilan

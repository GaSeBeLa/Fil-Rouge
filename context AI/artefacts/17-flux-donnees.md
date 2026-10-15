# Flux de données : Airflow et Elasticsearch — notes et journal
## Résultat
Trois DAG tournent chaque nuit (annonces, OLAP, index), la recherche de biens passe par GET /estates/search, et Kibana montre le trafic de l'API
## Notes
- FLX1 : up -d : 2 services (api, db) ; --profile airflow : /health metadatabase healthy, scheduler healthy ; psql -l : airflow à côté de fil_rouge_immobilier ; pytest 975 passed, 7 xfailed (= clôture PRF)
- FLX2 : pytest airflow/tests : 10 passed (mutant : 2 failed) ; dags test smoke_dag : state=success, 2556 biens ; mc ls : bronze/smoke/2026-10-15.json (40 o) et quarantine/ ; API 975 passed, 7 xfailed
- FLX3 : pytest airflow/tests : 71 passed (mutant prix ÷ 1000 : 5 failed) ; annonces.csv : 2556 lus, 2556 valides, 0 rejeté ; étages et somme des prix (519 169 839 €) identiques à la base
- FLX4 : DAG annonces_import joué 2 fois le 15/10 : estate 2556 → 2707 (+151), historique 151 ; 2e passage +0, historique 151 ; airflow 78 passed ; API 975 passed, 7 xfailed ; banc 1 passed
- FLX5 : \dt olap.* : 6 tables ; grep name|email|phone dans 08_olap.sql : 0 ; banc 1 passed (mutant : 1 failed) ; API 975 passed, 7 xfailed
- FLX6 : dags test olap_refresh joué 2 fois : 501 lues, 501 chargées, 0 rejet ; fait_ventes 501 = sale 501 aux deux passages (max id 501) ; rapport gold/olap/2026-10-15.json ; airflow 93 passed (mutant délai en jours : 3 failed) ; API 988 passed, 7 xfailed
- FLX7 : --profile elk up -d : _cluster/health status green (1 nœud) ; api/status level available ; es-setup OK ; up -d seul : 2 services ; Kibana 981 Mio / 1 Gio ; API 988 passed, 7 xfailed
- FLX8 : DAG estates_index : estate vers l'index estates, sans contact du vendeur ; dépend de FLX4, FLX7
- FLX9 : Route GET /estates/search, 503 si Elasticsearch est absent ; dépend de FLX8
- FLX10 : Logs JSON de l'API, Logstash, data stream logs-api-default ; dépend de FLX7
- FLX11 : Tableau de bord Kibana : trafic et carte des biens (visuel) ; dépend de FLX8, FLX10
- FLX12 : Doc, schéma du flux avec les vrais noms, ADR ; dépend de toutes
- FLX13 : faker lancé sur la base de dev : sale 1 → 501, payment 1 → 501 (463 paid, 21 scheduled, 17 announced, 0 refused) ; relancé : rien écrit, 501/501 ; 13 tests unitaires verts ; API 988 passed, 7 xfailed
## Journal
- 2026-10-15 : FLX3 : la clé d'annonce est `estate.reference` (déjà VARCHAR(50) NOT NULL UNIQUE, remplie sur 2556 biens sur 2556) ; pas de `source_reference` (question flux-16, tranchée A par Seb, MPD corrigé). Migrations renumérotées : 48 = estate_price_history (FLX4), 49 = olap (FLX5).
- 2026-10-15 : flux-17 : volume ../airflow/tools monté en lecture seule (oui de Seb)
- 2026-10-15 : FLX5 : olap fermé au rôle lecteur (commission issue de payment, migration 43)
## Bilan

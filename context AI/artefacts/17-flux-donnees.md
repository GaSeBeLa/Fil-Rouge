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
- FLX8 : dags test estates_index 2 fois : estates/_count 2707 = count(estate) 2707 aux deux passages ; orphelin ajouté puis retiré (deleted 1) ; airflow_indexer : 403 hors estates, 400 sur un champ de contact ; airflow 102 passed (mutant champ de contact : 2 failed) ; API 988 passed, 7 xfailed
- FLX9 : test_estate_search 13 passed (401 sans jeton, 503 sur erreur de connexion) ; pile lancée : city=Toulouse → 1129 = 1129 en base, q=lumineux → 221, 10 km autour de Toulouse → 571 ; mutant routeur après estate_router : 5 failed ; API 1006 passed, 7 xfailed
- FLX10 : 10 appels à l'API : logs-api-default/_count 10 ; http.response.status_code présent (200×6, 404×2, 401, 403), user.roles Client×6 ; grep password|token|email sur le document du login : 0 ; mutant corps du login : 1 failed ; API 1010 passed, 7 xfailed (1006 + 4 neufs), log réel inchangé par pytest
- FLX11 : Seb a vu le tableau de bord (capture) : 211 requêtes, taux d'erreur 27,0 %, codes 200/403/401/404 empilés, /estates/search en tête (42), carte : 5 villes, prix moyen par ville Dijon 279 379 € → Limoges 93 695 € ; import README : successCount 9 ; grep secret dans le ndjson : 0 ; API 1010 passed, 7 xfailed
- FLX12 : 8 fichiers neufs (schema-du-flux.md, ADR 059 à 064, livrables/2-modelisation/olap.md) ; mermaid-cli (image Docker) : 2 schémas rendus, exit 0 ; grep TODO|à remplir : 0 ; chaque ADR cite flux-n, cours ou doc officielle ; RAM docker stats : 234 Mio / 1 552 Mio / 3 309 Mio ; API 1010 passed, 7 xfailed
- FLX13 : faker lancé sur la base de dev : sale 1 → 501, payment 1 → 501 (463 paid, 21 scheduled, 17 announced, 0 refused) ; relancé : rien écrit, 501/501 ; 13 tests unitaires verts ; API 988 passed, 7 xfailed
## Journal
- 2026-10-15 : FLX3 : la clé d'annonce est `estate.reference` (déjà VARCHAR(50) NOT NULL UNIQUE, remplie sur 2556 biens sur 2556) ; pas de `source_reference` (question flux-16, tranchée A par Seb, MPD corrigé). Migrations renumérotées : 48 = estate_price_history (FLX4), 49 = olap (FLX5).
- 2026-10-15 : flux-17 : volume ../airflow/tools monté en lecture seule (oui de Seb)
- 2026-10-15 : FLX5 : olap fermé au rôle lecteur (commission issue de payment, migration 43)
## Bilan
- Livré : Trois DAG Airflow chaque nuit (annonces, OLAP, index), recherche GET /estates/search par Elasticsearch, logs de l'API dans Kibana, schéma du flux et ADR 059 à 064
- Surpris : estate.reference portait déjà la clé d'annonce (flux-16) ; Kibana refuse un import si la version de migration dépasse celle du type
- Estimé : estimé non noté · cadré 13 · joué 13 fiches 44,72 $

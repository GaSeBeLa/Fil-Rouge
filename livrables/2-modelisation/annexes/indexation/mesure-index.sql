-- Mesure de la note d'indexation (2026-11-19). Rejouable : tout est annulé (ROLLBACK).
-- Depuis Fil-Rouge-API/docker/ : docker compose exec -T db psql -U postgres -d fil_rouge_immobilier -q < mesure-index.sql
\timing off
BEGIN;
-- Volume de démo, tel quel
SELECT 'demo' AS etape, (SELECT count(*) FROM estate_searchrequest) AS selections, (SELECT count(*) FROM search_request) AS demandes;
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM estate_searchrequest WHERE id_search_request = 42;

-- Volume projeté : ~500 000 sélections, ~100 000 demandes (annulé à la fin)
INSERT INTO search_request (id_author, id_client, id_hunter, id_realestatemanager, status)
SELECT id_author, id_client, id_hunter, id_realestatemanager, status FROM search_request, generate_series(1, 200);
INSERT INTO estate_searchrequest (id_estate, id_search_request, id_hunter)
SELECT e.id, r.id, r.id_hunter
FROM (SELECT id FROM estate ORDER BY id LIMIT 1000) e
CROSS JOIN (SELECT id, id_hunter FROM search_request WHERE id_hunter IS NOT NULL ORDER BY id LIMIT 500) r
ON CONFLICT DO NOTHING;
ANALYZE search_request; ANALYZE estate_searchrequest;
SELECT 'projete' AS etape, (SELECT count(*) FROM estate_searchrequest) AS selections, (SELECT count(*) FROM search_request) AS demandes;
SELECT 'cles' AS etape, (SELECT id_search_request FROM estate_searchrequest ORDER BY id DESC LIMIT 1) AS une_demande, (SELECT id_hunter FROM search_request WHERE id_hunter IS NOT NULL LIMIT 1) AS un_chasseur;
\echo ===== Q1 AVANT : selections d une demande
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM estate_searchrequest WHERE id_search_request = 42;
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM estate_searchrequest WHERE id_search_request = 42;
\echo ===== Q2 AVANT : selections d un chasseur
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM estate_searchrequest WHERE id_hunter = 1;
\echo ===== Q3 AVANT : demandes d un chasseur, les 20 plus recentes
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM search_request WHERE id_hunter = 1 ORDER BY created_at DESC LIMIT 20;
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM search_request WHERE id_hunter = 1 ORDER BY created_at DESC LIMIT 20;
CREATE INDEX idx_estate_searchrequest_request ON estate_searchrequest (id_search_request);
CREATE INDEX idx_estate_searchrequest_hunter ON estate_searchrequest (id_hunter);
CREATE INDEX idx_search_request_hunter_created ON search_request (id_hunter, created_at DESC);
ANALYZE search_request; ANALYZE estate_searchrequest;
SELECT pg_size_pretty(pg_relation_size('idx_estate_searchrequest_request')) AS taille_q1, pg_size_pretty(pg_relation_size('idx_estate_searchrequest_hunter')) AS taille_q2, pg_size_pretty(pg_relation_size('idx_search_request_hunter_created')) AS taille_q3;
\echo ===== Q1 APRES
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM estate_searchrequest WHERE id_search_request = 42;
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM estate_searchrequest WHERE id_search_request = 42;
\echo ===== Q2 APRES
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM estate_searchrequest WHERE id_hunter = 1;
\echo ===== Q3 APRES
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM search_request WHERE id_hunter = 1 ORDER BY created_at DESC LIMIT 20;
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM search_request WHERE id_hunter = 1 ORDER BY created_at DESC LIMIT 20;
SELECT count(*) FILTER (WHERE id_hunter = 1) AS selections_chasseur_1 FROM estate_searchrequest;
ROLLBACK;

# 📇 Note d'indexation — EXPLAIN avant / après

> **Note d'indexation** (BC05).
> Exigée par `GRILLE-EVALUATION.md` (StarterPack - BASE) : « Note d'indexation (EXPLAIN avant/après) | 1 page + captures ».
> Mesuré le **2026-11-19** sur la base de dev locale (conteneur `db`, PostgreSQL 16.15), schéma v3 (`Fil-Rouge-API`, commit `141d068`).
> Les captures : la sortie brute complète, dans `indexation/sortie-2026-11-19.txt`. Le script rejouable : `indexation/mesure-index.sql`.

---

## 1. La question

- Le schéma a déjà des index sur ses **clés uniques** : email, référence d'un bien, un paiement par vente…
- PostgreSQL **ne crée pas** d'index sur une clé étrangère. Or l'API filtre surtout par clé étrangère : « les biens proposés pour **cette demande** », « les demandes de **ce chasseur** ».
- ➡️ Ces filtres lisent-ils toute la table ? Et un index les accélère-t-il ?

## 2. Les 3 requêtes choisies

| # | La requête | Qui l'appelle |
| --- | --- | --- |
| Q1 | `estate_searchrequest WHERE id_search_request = ?` : les biens retenus pour une demande | le moteur de suggestions, à **chaque** appel (`suggestion_service.py:68`) |
| Q2 | `estate_searchrequest WHERE id_hunter = ?` : les sélections d'un chasseur | un filtre par chasseur, comme la règle « le sien » des droits |
| Q3 | `search_request WHERE id_hunter = ? ORDER BY created_at DESC LIMIT 20` : les 20 demandes les plus récentes d'un chasseur | la liste des demandes qu'un chasseur suit |

- L'index unique `uq_estate_search (id_estate, id_search_request)` existe, mais il **commence** par `id_estate` : il ne sert pas pour chercher par demande.

## 3. La méthode

1. **Volume de démo, tel quel** : 1 016 sélections, 519 demandes.
2. **Volume projeté**, dans une transaction **annulée à la fin** (`ROLLBACK`) :
   - les demandes copiées 200 fois ➡️ **104 319** demandes ;
   - 1 000 biens croisés avec 500 demandes ➡️ **500 656** sélections.
   - 💡 C'est une hypothèse d'ordre de grandeur : quelques années d'activité, avec les « milliers de mandats par semaine » de la note 3V.
3. `EXPLAIN (ANALYZE, BUFFERS)` de chaque requête, **avant** l'index puis **après**. Les requêtes Q1 et Q3 sont lancées deux fois, pour écarter l'effet du premier appel.
4. ✅ Vérifié après coup : la base est revenue à **1 016** sélections et **519** demandes, avec **0** index ajouté.

## 4. Les résultats

**Au volume de démo** : la requête Q1 lit toute la table (`Seq Scan`), en **0,28 ms** et 8 pages. ➡️ Aucun besoin d'index aujourd'hui : la table tient en mémoire.

**Au volume projeté** :

| # | Avant : plan et temps | Après : plan et temps | Gain | Pages lues | Taille de l'index |
| --- | --- | --- | --- | --- | --- |
| Q1 | `Parallel Seq Scan`, **43,5 ms** et 44,3 ms | `Bitmap Index Scan`, **1,23 ms** et 1,25 ms | environ **× 35** | 7 356 ➡️ 1 005 | 3,6 Mo |
| Q2 | `Parallel Seq Scan`, **43,4 ms** | `Bitmap Index Scan`, **2,78 ms** | environ **× 15** | 7 356 ➡️ 1 103 | 3,4 Mo |
| Q3 | `Seq Scan` + tri, **7,6 ms** et 8,5 ms | `Index Scan`, **0,08 ms** et 0,03 ms | environ **× 100** | 1 938 ➡️ 8 | 0,75 Mo |

Extrait de la capture, requête Q3 :

```text
AVANT  ->  Seq Scan on search_request (actual time=0.006..7.468 rows=804 loops=1)
           Sort Method: top-N heapsort  Memory: 26kB
           Execution Time: 7.581 ms
APRÈS  ->  Index Scan using idx_search_request_hunter_created on search_request
           (actual time=0.060..0.068 rows=20 loops=1)
           Execution Time: 0.080 ms
```

## 5. Ce qu'on en retient

- **Q3 gagne le plus** : l'index `(id_hunter, created_at DESC)` est **déjà trié**. PostgreSQL lit les 20 premières lignes et s'arrête. Il ne trie plus 804 lignes.
- **Q1 et Q2** : PostgreSQL ne lit plus que les pages utiles, environ 7 fois moins.
- **Le coût** : environ **7,8 Mo** pour les trois index, et une écriture un peu plus lente à chaque nouvelle sélection. Pour une table qu'on lit bien plus qu'on ne l'écrit, l'échange est bon.
- ⚠️ **Au volume d'aujourd'hui, le gain est nul** : le planificateur préfère lire toute la table, et il a raison. Ces index préparent la croissance. Ils ne réparent pas une lenteur constatée.

## 6. La décision

```sql
CREATE INDEX idx_estate_searchrequest_request ON estate_searchrequest (id_search_request);
CREATE INDEX idx_estate_searchrequest_hunter  ON estate_searchrequest (id_hunter);
CREATE INDEX idx_search_request_hunter_created ON search_request (id_hunter, created_at DESC);
```

✅ **Posés le 2026-11-19** (choix A de Sébastien), dépôt `Fil-Rouge-API`, commit `eda0a35` :

- dans le schéma de référence `docker/init-v3/01_create_fil_rouge_immobilier.sql` ;
- dans la migration `docker/migrations/v2-vers-v3/52_index-chasseur-et-demande.sql`, pour une base qui existe déjà ;
- prouvés par `API/tests/integration/test_index_cles_etrangeres.py`. Le banc v2/v3 échoue sans la migration (vérifié) et passe avec.

➡️ **Pour l'équipe, après un pull** : rejouer la migration 52 sur sa base de dev, ou la recréer (`docker compose down -v && docker compose up -d`).

## 7. Limites

- Les mesures viennent d'**une seule machine**, avec une base chaude (pages en mémoire, `shared hit`). Sur disque froid, les écarts seraient plus grands.
- Le volume projeté est **fabriqué** par copie : la répartition réelle des sélections entre les chasseurs peut changer les plans.
- La recherche de biens par critères (prix, ville, type) passe par **Elasticsearch**, pas par PostgreSQL : elle n'est pas dans cette note.

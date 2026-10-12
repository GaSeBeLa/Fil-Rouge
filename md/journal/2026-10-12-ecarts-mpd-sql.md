# Écarts entre le MPD et le SQL — ce qu'il faut changer dans le MPD

* **Date :** 12/10/2026
* **Demandé par :** Gabriel (Discord), fichier `MPD_CIBLE.drawio.xml` envoyé le même jour.
* **Comparé à :** `docker/init-v3/01_create_fil_rouge_immobilier.sql`, chargé dans un PostgreSQL 16 neuf, puis lu par son catalogue. Chaque écart est vérifié deux fois : dans le catalogue, et dans le fichier `01`.

## La règle : le SQL fait foi

* **Tous les changements ci-dessous se font dans le MPD**, jamais dans le SQL ni dans la base.
* Le SQL est ce qui tourne et ce qui est testé ; le MPD doit le décrire tel qu'il est.
* « 01:506 » = ligne 506 du fichier `01`, là où se trouve la ligne à recopier.
* « cellule `-51` » = la cellule `5H3ErDjLgtmFj-gvShCD-51` du fichier draw.io, pour retrouver où modifier.

## Les émojis : ce qu'ils veulent dire

| Émoji | Veut dire | Ce qu'il faut faire dans le MPD |
|---|---|---|
| ➕ | Le SQL l'a, le MPD non | **Ajouter** la ligne, recopiée telle quelle |
| ➖ | Le MPD l'a, le SQL non | **Retirer** la ligne |
| ✏️ | Les deux l'ont, mais différemment | **Corriger** la ligne du MPD pour qu'elle dise comme le SQL |
| 🟡 | Une interprétation, pas une certitude | **Décider** d'abord (Gabriel), puis changer ou non |
| 💡 | Optionnel | Le faire **seulement si** le MPD doit montrer ce genre d'objet (ici : les index) |
| ⚠️ | Attention, hors du MPD | Rien à faire dans le MPD : c'est un autre problème, signalé en passant |

* Les émojis ne disent **rien sur la gravité** : un ➕ n'est pas plus grave qu'un ➖. Ils disent seulement **quel geste** faire.
* « Vieil écart » : l'écart existait avant les changements du 12/10 ; ce n'est pas un oubli de cette journée.

---


⚠️ **La base dev n'est pas à jour** : elle date d'avant le 8/10 sur trois points (pas de table `review_media`, encore `media_url`/`media_type` dans `estate_searchrequest`, encore `renovation_budget_*` et `chk_renew*`). Je n'ai donc pas pris son catalogue comme vérité.
- À la place : le fichier 01 chargé dans un **Postgres 16 jetable** (conteneur temporaire, supprimé ensuite), puis lu par `information_schema` / `pg_catalog`.
- La base dev n'a pas été touchée. La fonction `check_mandate_exclusivity` y est pourtant identique au fichier (même md5).

**Ce que montre le MPD**
- Chaque ligne donne la colonne en DDL complet : type, NOT NULL, UNIQUE, DEFAULT, REFERENCES et le **CHECK en ligne**.
- Une dernière ligne par table liste les **CONSTRAINT nommées** (CHECK, UNIQUE, EXCLUDE).
- Les CHECK manquants comptent donc comme de vraies erreurs.
- **Aucun index** n'est montré (ni `CREATE INDEX`, ni index partiel). Ils sont listés à part, en fin de rapport.
- Le trigger U02 est décrit dans une note (cellule `eqoQllOwxs2XPU2PAXGI-4`).

**Mandate**
- ➕ `CONSTRAINT fk_mandate_request_same_client FOREIGN KEY (id_search_request, id_client) REFERENCES search_request(id, id_client) ON DELETE RESTRICT` — 01:506
- ➕ `CONSTRAINT chk_mandate_not_own_parent CHECK (id_mandate_parent <> id)` — 01:512
- ➕ `CONSTRAINT uq_mandate_id_client UNIQUE (id, id_client)` — 01:513
- ➕ `CONSTRAINT uq_mandate_id_hunter UNIQUE (id, id_hunter)` — 01:516
- ➕ `CONSTRAINT fk_mandate_parent_same_client FOREIGN KEY (id_mandate_parent, id_client) REFERENCES mandate(id, id_client) ON DELETE RESTRICT` — 01:517
- Ces 5 lignes vont dans la cellule `5H3ErDjLgtmFj-gvShCD-14`.
- ✏️ **Note du trigger U02** (`eqoQllOwxs2XPU2PAXGI-4`), deux puces à corriger — 01:587-623 :
  - « Un mandat 'canceled' libère le client » devient : 'canceled', 'completed' **et** 'lost' libèrent le client.
  - « Le renouvellement est exclu du contrôle » devient : exclu **seulement s'il est signé à l'échéance du parent** (sinon refusé).
  - À ajouter si l'on veut : un verrou `pg_advisory_xact_lock` par client (P15).

**Client**
- ✏️ `country_iso CHAR(2)` passe à **`NOT NULL`** — 01:209 — cellule `-51`
- ✏️ `address VARCHAR(150)` passe à **`NOT NULL`** — 01:215 — cellule `-54`
- ✏️ `postal_code VARCHAR(10)` passe à **`NOT NULL`** — 01:220 — cellule `-56`
- ✏️ `town VARCHAR(100)` passe à **`NOT NULL`** — 01:222 — cellule `-57`
- ➖ `CONSTRAINT ck_client_address_all_or_nothing`, absente du 01 (retirée le 12/10, commit 7acb6ea) — cellule `-62`
- ➖ `CONSTRAINT ck_client_postal_code_needs_country`, même cas — cellule `-62`

**User**
- ➕ `CONSTRAINT ck_user_email_format CHECK (email ~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$')` — 01:178
- La table n'a pas de ligne de contraintes : en créer une.

**SearchRequest**
- ➕ `CONSTRAINT chk_search_request_hunter_after_confirmed CHECK (status = 'confirmed' OR id_hunter IS NOT NULL)` — 01:332
- ➕ `CONSTRAINT uq_search_request_id_client UNIQUE (id, id_client)` — 01:336
- ➖ `CONSTRAINT chk_search_request_hunter_needs_manager` (cellule `-75`) : elle n'a **jamais été dans le 01** (git -S ne trouve aucun commit) et n'est pas dans le catalogue. C'est un vieil écart.

**Criteria**
- ➖ colonne `renovation_budget_min INTEGER` (cellule `-95`) : retirée du 01 le 9/10, commit c5e5842 (S7, ADR-032)
- ➖ colonne `renovation_budget_max INTEGER` (cellule `-96`) : même cas
- ➖ `CONSTRAINT chk_renov_budget`, dans la cellule `-135`
- ✏️ `needs_renovation BOOLEAN` devient **`BOOLEAN NOT NULL DEFAULT FALSE`** — 01:375 — cellule `-94`
- ➕ `CONSTRAINT uq_criteria_id_request UNIQUE (id, id_search_request)` — 01:437
- ➕ `CONSTRAINT fk_criteria_previous_same_request FOREIGN KEY (id_previous_version, id_search_request) REFERENCES criteria(id, id_search_request) ON DELETE RESTRICT` — 01:438
- ➕ `CONSTRAINT uq_criteria_one_successor UNIQUE (id_previous_version)` — 01:441
- ➕ `CONSTRAINT chk_criteria_not_own_previous CHECK (id_previous_version <> id)` — 01:442
- ➕ `CONSTRAINT chk_criteria_change_reason CHECK (id_previous_version IS NULL OR change_reason IS NOT NULL)` — 01:445
- Ces 5 lignes vont dans la cellule `-135`.

**Estate**
- ✏️ `needs_renovation BOOLEAN` devient **`BOOLEAN NOT NULL DEFAULT FALSE`** — 01:683 — cellule `-270`
- ➕ `CONSTRAINT chk_estate_coordinates_pair CHECK ((latitude IS NULL) = (longitude IS NULL))` — 01:705 — cellule `-278`

**EstateProposed**
- ➕ `CONSTRAINT fk_proposed_hunter_of_mandate FOREIGN KEY (id_mandate, id_hunter) REFERENCES mandate(id, id_hunter) ON DELETE RESTRICT` — 01:780 — cellule `-185`

**Sale**
- ✏️ `id_estate INTEGER NOT NULL` : **retirer `UNIQUE`** (cellule `-315`). Le 01 ne l'a jamais eu (01:856) et le catalogue non plus. C'est un vieil écart.
- 🟡 Cardinalité de l'arête Estate→Sale (`-353`) : l'étiquette côté Estate dit `0,1`, ce qui suppose ce UNIQUE.
  - Si le 01 fait foi, elle devient `0,n`.
  - À confirmer : c'est une interprétation de la convention, selon laquelle l'étiquette posée près d'une entité porte sur cette entité.

**Visit**
- ➕ `CONSTRAINT chk_visit_not_in_future CHECK (visit_date <= (clock_timestamp() AT TIME ZONE 'utc')::date + 1)` — 01:810
- La table n'a pas de ligne de contraintes : en créer une.

**Payment**
- ➕ `CONSTRAINT chk_paid_not_in_future CHECK (paid_at <= (clock_timestamp() AT TIME ZONE 'utc') + INTERVAL '5 minutes')` — 01:1044
- ➕ `CONSTRAINT uq_payment_id_hunter UNIQUE (id, id_hunter)` — 01:1089
- ✏️ `chk_refused` (cellule `-344`) : 01:1064-1085. Trois ajouts :
  - branche refus : `AND calculation_details IS NULL` (01:1073)
  - branche hors refus : `AND performance_score IS NOT NULL` (01:1082)
  - branche hors refus : `AND calculation_details IS NOT NULL` (01:1083)

**HunterPerformance**
- ➕ `CONSTRAINT chk_perf_not_in_future CHECK (scored_at <= (clock_timestamp() AT TIME ZONE 'utc') + INTERVAL '5 minutes')` — 01:1122
- ➕ `CONSTRAINT fk_perf_payment_same_hunter FOREIGN KEY (id_payment, id_hunter) REFERENCES payment(id, id_hunter) ON DELETE RESTRICT` — 01:1127
- ➕ `CONSTRAINT fk_perf_mandate_same_hunter FOREIGN KEY (id_mandate, id_hunter) REFERENCES mandate(id, id_hunter) ON DELETE RESTRICT` — 01:1130
- Ces 3 lignes vont dans la cellule `-386`.

**Tables présentes d'un seul côté**
- Aucune : 20 tables de chaque côté. `ReviewMedia` correspond bien à `review_media` (01:751).

**Contraintes par nature**
- Ces lignes sont déjà comptées dans les sections par table ; elles sont regroupées ici par nature.
- **FK composites à ajouter (6)** :
  - fk_mandate_request_same_client
  - fk_mandate_parent_same_client
  - fk_criteria_previous_same_request
  - fk_proposed_hunter_of_mandate
  - fk_perf_payment_same_hunter
  - fk_perf_mandate_same_hunter
  - Toutes relient des tables déjà reliées par une arête : **aucune arête à ajouter**, seulement la ligne CONSTRAINT.
- **UNIQUE à ajouter (6)** : uq_search_request_id_client, uq_criteria_id_request, uq_criteria_one_successor, uq_mandate_id_client, uq_mandate_id_hunter, uq_payment_id_hunter
- **UNIQUE à retirer (1)** : sale.id_estate
- **CHECK à ajouter (9)** :
  - ck_user_email_format
  - chk_search_request_hunter_after_confirmed
  - chk_criteria_not_own_previous
  - chk_criteria_change_reason
  - chk_mandate_not_own_parent
  - chk_estate_coordinates_pair
  - chk_visit_not_in_future
  - chk_paid_not_in_future
  - chk_perf_not_in_future
- **CHECK à retirer (4)** : ck_client_address_all_or_nothing, ck_client_postal_code_needs_country, chk_search_request_hunter_needs_manager, chk_renov_budget
- **CHECK à corriger (1)** : chk_refused

**💡 Index : à ajouter seulement si le MPD doit les montrer**
- Le MPD ne montre aucun index aujourd'hui. Il y en a 4 dans le 01 :
  - `CREATE UNIQUE INDEX uq_user_email_lower ON "user" (lower(email))` — 01:183
  - `CREATE UNIQUE INDEX uq_criteria_one_first_version ON criteria (id_search_request) WHERE id_previous_version IS NULL` — 01:460
  - `CREATE UNIQUE INDEX uq_perf_one_initial ON hunter_performance (id_hunter) WHERE trigger_type = 'initial'` — 01:1145
  - `CREATE INDEX idx_perf_hunter_scored_at ON hunter_performance (id_hunter, scored_at DESC)` — 01:1148 (ancien, pas un oubli du 12/10)

**Comptes**
- Tables : **20** dans le SQL, **20** dans le XML.
- Colonnes : **260** comparées (nom, type, NULL, UNIQUE, FK, DEFAULT, IDENTITY). Aucune ne manque dans le XML, **2** sont en trop.
- Arêtes : 40 dans le XML.
  - Elles couvrent les **38** FK simples du 01.
  - Les 2 restantes : `-134`, petit trait décoratif sur l'étiquette « Follows », et `-146`, arête **orpheline** sans source ni cible (à supprimer, pur nettoyage).
- Changements :
  - Colonnes : ➖ 2, ✏️ 7 (4 NOT NULL client, 2 needs_renovation, 1 UNIQUE sale.id_estate).
  - Contraintes : ➕ 21, ➖ 4, ✏️ 1.
  - Divers : 1 note trigger, 1 cardinalité à confirmer, 1 arête orpheline.
  - Index, en option : 4.

**Équivalences retenues (pas des écarts)**
- `varchar(n)` = `character varying(n)` ; `char(n)` = `character(n)` / `bpchar` ; `timestamp` = `timestamp without time zone` ; `int` = `integer`.
- Les espaces dans `NUMERIC (7, 2)` ne comptent pas.
- `BETWEEN a AND b` = `>= a AND <= b`.
- `IN (…)` = `= ANY (ARRAY[…])`, ordre des valeurs compris (proposition_status).
- `'6 months'` = `'6 mons'`.
- Les casts `::text` ne comptent pas.
- Le CHECK en ligne de `commission_scale.amount_max` correspond à `commission_scale_check`.
- Les 3 CHECK de format de code postal : les 6 regex ont été comparées une à une, **identiques**.
- Les UNIQUE de table déjà montrés en CONSTRAINT ne comptent pas comme manquants : uq_fees_effective_from, uq_hunter_rate_effective_from, uq_perf_payment, uq_perf_mandate.

**Non vérifié**
- La cardinalité Estate→Sale : voir plus haut, c'est une interprétation.
- Les autres étiquettes de cardinalité ne sont pas toutes revues. Seules les relations touchées par un UNIQUE l'ont été : Mandate→Sale, Renews, Follows, HunterPerformance→Payment/Mandate. Elles sont cohérentes.
- Le texte libre des CHECK n'est comparé que sous forme normalisée. Un écart purement cosmétique (espaces, retours à la ligne) n'est pas signalé.


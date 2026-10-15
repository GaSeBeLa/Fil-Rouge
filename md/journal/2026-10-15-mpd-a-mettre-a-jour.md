# Le MPD à mettre à jour — ce qu'il faut changer, aujourd'hui puis après le chantier PRF

* **Date :** 15/10/2026
* **Demandé par :** Gabriel (Discord)
* **MPD comparé :** `MPD_4.drawio.xml` (Gabriel, Discord, 15/10/2026, version de Confluence).
* **SQL comparé :** `docker/init-v3/01_create_fil_rouge_immobilier.sql`, dépôt Fil-Rouge-API, **au commit `9e4da81`** (HEAD du 15/10/2026, « PRF1 : Poser AbstractPerson »).
  * Lu par `git show HEAD:…`, **pas** la copie de travail : une autre séance la modifie (chantier PRF, non commité).
* **Cible du chantier PRF :** ADR-057, section « Décision » (`md/adr/adr-057-cles-et-roles-des-fiches.md`), et `context AI/16-refacto-profils.md`, section « Le socle commun ».
* **Méthode :** le XML draw.io lu par un script Python (cellules, arêtes, étiquettes et leur position). Chaque ligne du MPD comparée à la ligne du `01`, espaces et casse mis à part.

## La règle : le SQL fait foi

* **Tous les changements de la partie A se font dans le MPD**, jamais dans le SQL.
* Le SQL est ce qui tourne et ce qui est testé ; le MPD doit le décrire tel qu'il est.
* La partie B décrit le SQL **de demain** : elle ne vaut qu'une fois le chantier PRF fini (ou tout de suite, si le groupe veut un MPD cible).
* « 01:994 » = ligne 994 du fichier `01` à `9e4da81`, là où se trouve la ligne à recopier.
* « cellule `-423` » = la cellule `o8dGPHMTGd0eB4VVUW8a-423` du fichier draw.io, pour retrouver où modifier.

## Les émojis : ce qu'ils veulent dire

| Émoji | Veut dire | Ce qu'il faut faire dans le MPD |
|---|---|---|
| ➕ | Le SQL l'a, le MPD non | **Ajouter** la ligne, recopiée telle quelle |
| ➖ | Le MPD l'a, le SQL non | **Retirer** la ligne |
| ✏️ | Les deux l'ont, mais différemment | **Corriger** la ligne du MPD pour qu'elle dise comme le SQL |
| 🟡 | Une interprétation, pas une certitude | **Décider** d'abord (Gabriel), puis changer ou non |
| 💡 | Optionnel | Le faire **seulement si** on veut un MPD tout à fait aligné (ordre, forme, index) |
| ⚠️ | Attention, hors du MPD | Rien à faire dans le MPD : c'est un autre problème, signalé en passant |

* Les émojis ne disent **rien sur la gravité**. Ils disent seulement **quel geste** faire.
* ✅ = rien à changer.

## Ce que montre le MPD

* Chaque ligne d'une table donne la colonne en DDL complet : type, NOT NULL, UNIQUE, DEFAULT, REFERENCES et le CHECK en ligne.
* Une dernière ligne par table liste les **CONSTRAINT nommées**.
* Les liens n'ont **pas** de flèche ER (`endArrow=none` partout) : la cardinalité est dans les **étiquettes** (`1,1`, `0,n`…).
  * Convention lue sur tout le MPD : l'étiquette posée **près d'une table** dit combien de fois cette table participe.
  * Exemple : `Hunter` — `Mandate`, `0,n` près de `Hunter`, `1,1` près de `Mandate` (`mandate.id_hunter NOT NULL`).
* Aucun index n'est montré.
* Le trigger U02 est décrit dans une note (cellule `-457`).

---

# Partie A — écarts entre MPD_4 et le SQL d'aujourd'hui

* Bonne nouvelle : **MPD_4 est presque aligné**. Les écarts du 12/10 sont tous corrigés.
* Il reste **5 écarts à faire**, 1 à décider, et des retouches optionnelles.
* Ordre : celui des tables dans le `01`.

**role** — ✅ identique (cellule `-275`)

**"user"** — ✅ identique (cellule `-134`)
* 💡 L'index `CREATE UNIQUE INDEX uq_user_email_lower ON "user" (lower(email))` — 01:184 — n'est pas montré (voir « Index », plus bas).

**client** (cellule `-45`)
* ✏️ `ck_client_postal_code_format`, branche Irlande : le MPD a une **espace en trop** dans la classe de caractères — cellule `-62`.
  * MPD : `'^([AC-FHKNPRTV-Y][0-9]{2}|D6W)[0-9AC- FHKNPRTV-Y]{4}$'`
  * SQL, à recopier : `WHEN country_iso = 'IE' THEN postal_code ~ '^([AC-FHKNPRTV-Y][0-9]{2}|D6W)[0-9AC-FHKNPRTV-Y]{4}$'` — 01:247
  * Ce n'est pas qu'une question de forme : avec l'espace, `C- ` devient une autre plage, et le motif n'est plus le même.
  * La même regex est juste dans `criteria` (`-133`) et `estate` (`-274`).

**real_estate_manager** — ✅ identique (cellule `-157`)

**hunter** (cellule `-20`)
* ➕ Lien `Hunter` — `User` (arête `-142`, « is a ») : il manque l'étiquette **`0,1` côté `User`**.
  * Raison : `id_user INTEGER NOT NULL UNIQUE REFERENCES "user"(id) ON DELETE RESTRICT` — 01:277. Le UNIQUE fait qu'un compte a au plus une fiche `hunter`.
  * Les deux liens frères l'ont déjà : `Client` — `User` (`-44`) et `RealEstateManager` — `User` (`-185`).

**search_request** — ✅ identique (cellule `-67`)

**criteria** (cellule `-80`)
* 🟡 Lien `Criteria` — `SearchRequest` (arête `-76`, « Contains ») : l'étiquette côté `SearchRequest` dit **`1,n`** (cellule `-78`).
  * Le SQL ne garantit pas qu'une demande ait au moins un critère : rien n'oblige à créer la première version. Lu strictement, ce serait `0,n`.
  * À décider : `1,n` peut rester comme règle métier (une demande a toujours ses critères, posés par l'API).
* 💡 Ordre des colonnes : le SQL met `postal_code` (01:353) **avant** `district` (01:355) ; le MPD l'inverse (`-86`, `-87`).

**mandate** — ✅ identique (cellule `-1`)
* 💡 La ligne `-15` dit « Voir note du Trigger: U2 ». Le SQL et la note disent **U02** (01:542, note `-457`).
* La note du trigger (`-457`) dit la même chose que le SQL (01:541-624) : libération par 'canceled', 'completed', 'lost' ; renouvellement à l'échéance ; verrou par client ; extension `btree_gist`. ✅

**estate** (cellule `-229`)
* ➖ Lien `Estate` — `User` (arête `-400`, « creates ») : côté `User`, il y a **deux** étiquettes, `0,1` (cellule `-402`) et `0,n` (cellule `-404`).
  * Retirer **`-402` (`0,1`)**. Garder `0,n` : `estate.id_author` n'a pas de UNIQUE (01:702), un compte peut créer plusieurs biens.
* 💡 Ordre des colonnes : le SQL met `district` **après** `postal_code` (01:691 puis 01:695) ; le MPD le met juste après `town` (`-268`).

**picture** — ✅ identique (cellule `-220`)

**estate_contact** (cellule `-458`)
* ✏️ Lien `Estate` — `estate_contact` (arête `-469`, « Has contact ») : les deux étiquettes sont **inversées**.
  * Aujourd'hui : `1,1` (cellule `-470`) est posé près de `Estate`, `0,1` (cellule `-471`) près de `estate_contact`.
  * Il faut : **`0,1` près de `Estate`** (un bien a 0 ou 1 contact) et **`1,1` près de `estate_contact`** (un contact a toujours son bien).
  * Raison : `id_estate INTEGER NOT NULL UNIQUE REFERENCES estate(id) ON DELETE RESTRICT` — 01:754.
  * Les positions sont calculées depuis le XML (point sur l'arête + décalage) : un coup d'œil sur le dessin le confirmera.
* 💡 Nom de la table : `estate_contact` est la seule écrite en minuscules ; les 20 autres sont en PascalCase (`EstateSearchRequest`…). `EstateContact` serait cohérent.

**estate_searchrequest** — ✅ identique (cellule `-196`)
* 💡 Cellule `-202` : `REFERENCES Hunter(id_user)`, avec une majuscule. Le SQL écrit `hunter(id_user)` (01:779). PostgreSQL replie la casse : même sens, simple forme.

**review_media** — ✅ identique (cellule `-445`)

**estate_proposed** (cellule `-172`)
* 💡 `proposition_status` : le SQL liste `'accepted', 'signed', 'rejected'` (01:807-808) ; le MPD `'accepted', 'rejected', 'signed'` (`-179`). Même contrainte, ordre différent.
* 💡 Ordre des colonnes : le SQL met `client_priority` **en dernier** (01:831) ; le MPD le met après `comment_client` (`-177`).

**visit** — ✅ identique (cellule `-314`)

**parameters_fees** — ✅ identique (cellule `-296`)

**sale** — ✅ identique (cellule `-303`)
* L'arête `Estate` — `Sale` (`-350`) porte `0,1` côté `Estate` : c'est juste, `uq_sale_estate` existe (01:896). Le 🟡 du 12/10 est réglé.

**commission_scale** (cellule `-283`)
* 💡 Ordre des colonnes : le SQL met `valid_from` (01:931) **avant** `valid_until` (01:932) ; le MPD l'inverse (`-289`, `-290`).

**hunter_rate_parameters** (cellule `-409`)
* ➕ `mandate_success_rate_for_max_score NUMERIC(5,4) NOT NULL` — 01:994
  * À placer entre `points_per_mandate` (`-423`) et `window_months` (`-424`), comme dans le SQL.
  * Origine : ADR-048 ; le critère « mandats » est noté par ce réglage (commentaire 01:969-971).

**payment** (cellule `-322`)
* 💡 Ordre des colonnes : le SQL met `refusal_reason` (01:1036) **avant** `base_rate` ; le MPD le met après `performance_score` (`-335`).

**hunter_performance** (cellule `-374`)
* 💡 Ordre des colonnes : le SQL met `score` (01:1156) **avant** `scored_at` (01:1157) ; le MPD l'inverse (`-377`, `-378`).

**💡 Index : à ajouter seulement si le MPD doit les montrer**
* Le MPD n'en montre aucun. Il y en a 4 dans le `01` :
  * `CREATE UNIQUE INDEX uq_user_email_lower ON "user" (lower(email));` — 01:184
  * `CREATE UNIQUE INDEX uq_criteria_one_first_version ON criteria (id_search_request) WHERE id_previous_version IS NULL;` — 01:461
  * `CREATE UNIQUE INDEX uq_perf_one_initial ON hunter_performance (id_hunter) WHERE trigger_type = 'initial';` — 01:1190
  * `CREATE INDEX idx_perf_hunter_scored_at ON hunter_performance (id_hunter, scored_at DESC);` — 01:1193

**Ce qui a été compté**
* Tables : **21** dans le SQL, **21** dans le MPD. Chacune a sa sœur.
* Colonnes : **270** dans le SQL, **269** dans le MPD. La seule qui manque : `mandate_success_rate_for_max_score`.
* Contraintes nommées : toutes présentes, texte identique, sauf la regex irlandaise de `client`.
* Liens : **41** arêtes dans le XML.
  * **40** correspondent une à une aux **40** FK simples du SQL.
  * La 41e, `-132`, est le petit trait décoratif de l'étiquette « Follows » (`Criteria` vers elle-même) : rien à faire.
* Cardinalités : les 40 liens relus, position des étiquettes calculée. 3 écarts (`-142`, `-400`, `-469`), 1 à décider (`-76`).

**Équivalences retenues (pas des écarts)**
* Espaces et retours à la ligne, `NUMERIC (7, 2)` = `NUMERIC(7,2)`, `"user" (id)` = `"user"(id)`, `and` = `AND`.
* Les noms de tables en PascalCase (`SearchRequest` = `search_request`).

---

# Partie B — ce que le chantier PRF va changer

* **Pas encore dans le SQL** à `9e4da81`. À appliquer quand le chantier sera fini.
* Ou tout de suite, si le groupe veut un MPD cible : dans ce cas, le dire en titre du MPD.
* Source de chaque point : ADR-057, « Décision », points 1 à 5 ; et `16-refacto-profils.md`, « Le socle commun ».

## B1. Les 11 FK visent l'`id` de la fiche, plus son `id_user`

* ADR-057, Décision 1. Les **noms** de colonnes ne changent pas, seule la **cible** change.
* Dans chaque ligne, remplacer `(id_user)` par `(id)`. Le reste de la ligne ne bouge pas.

| # | Table | Colonne | Ancienne cible | Nouvelle cible | Ligne cible complète | 01 | Cellule |
|---|---|---|---|---|---|---|---|
| 1 | `hunter` | `id_realestatemanager` | `real_estate_manager(id_user)` | `real_estate_manager(id)` | `id_realestatemanager INTEGER NOT NULL REFERENCES real_estate_manager(id) ON DELETE RESTRICT` | 01:303 | `-35` |
| 2 | `search_request` | `id_client` | `client(id_user)` | `client(id)` | `id_client INTEGER NOT NULL REFERENCES client(id) ON DELETE RESTRICT` | 01:320 | `-71` |
| 3 | `search_request` | `id_hunter` | `hunter(id_user)` | `hunter(id)` | `id_hunter INTEGER REFERENCES hunter(id) ON DELETE RESTRICT` | 01:322 | `-72` |
| 4 | `search_request` | `id_realestatemanager` | `real_estate_manager(id_user)` | `real_estate_manager(id)` | `id_realestatemanager INTEGER REFERENCES real_estate_manager(id) ON DELETE RESTRICT` | 01:324 | `-73` |
| 5 | `mandate` | `id_hunter` | `hunter(id_user)` | `hunter(id)` | `id_hunter INTEGER NOT NULL REFERENCES hunter(id) ON DELETE RESTRICT` | 01:491 | `-10` |
| 6 | `mandate` | `id_client` | `client(id_user)` | `client(id)` | `id_client INTEGER NOT NULL REFERENCES client(id) ON DELETE RESTRICT` | 01:493 | `-11` |
| 7 | `estate_searchrequest` | `id_hunter` | `hunter(id_user)` | `hunter(id)` | `id_hunter INTEGER NOT NULL REFERENCES hunter(id) ON DELETE RESTRICT` | 01:779 | `-202` |
| 8 | `estate_proposed` | `id_hunter` | `hunter(id_user)` | `hunter(id)` | `id_hunter INTEGER NOT NULL REFERENCES hunter(id) ON DELETE RESTRICT` | 01:809 | `-180` |
| 9 | `commission_scale` | `id_hunter` | `hunter(id_user)` | `hunter(id)` | `id_hunter INTEGER REFERENCES hunter(id) ON DELETE RESTRICT` | 01:933 | `-291` |
| 10 | `payment` | `id_hunter` | `hunter(id_user)` | `hunter(id)` | `id_hunter INTEGER NOT NULL REFERENCES hunter(id) ON DELETE RESTRICT` | 01:1072 | `-338` |
| 11 | `hunter_performance` | `id_hunter` | `hunter(id_user)` | `hunter(id)` | `id_hunter INTEGER NOT NULL REFERENCES hunter(id) ON DELETE RESTRICT` | 01:1160 | `-380` |

* ✏️ Ces 11 lignes : **11 corrections**.
* Les **arêtes** de ces 11 liens ne bougent pas : elles relient déjà les bonnes tables. Leurs cardinalités non plus.

**Les FK composées : 5 touchent une fiche, et leur texte ne change pas** ✅
* Elles visent `search_request`, `mandate` ou `payment`, pas une fiche. Seules les **valeurs** changent, comme pour les 11.
  * `fk_mandate_request_same_client FOREIGN KEY (id_search_request, id_client) REFERENCES search_request (id, id_client)` — 01:507 — cellule `-14`
  * `fk_mandate_parent_same_client FOREIGN KEY (id_mandate_parent, id_client) REFERENCES mandate (id, id_client)` — 01:518 — cellule `-14`
  * `fk_proposed_hunter_of_mandate FOREIGN KEY (id_mandate, id_hunter) REFERENCES mandate (id, id_hunter)` — 01:817 — cellule `-183`
  * `fk_perf_payment_same_hunter FOREIGN KEY (id_payment, id_hunter) REFERENCES payment (id, id_hunter)` — 01:1172 — cellule `-383`
  * `fk_perf_mandate_same_hunter FOREIGN KEY (id_mandate, id_hunter) REFERENCES mandate (id, id_hunter)` — 01:1175 — cellule `-383`
* Leurs cibles UNIQUE ne changent pas non plus : `uq_search_request_id_client` (01:337), `uq_mandate_id_client` (01:514), `uq_mandate_id_hunter` (01:517), `uq_payment_id_hunter` (01:1134).
* La 6e FK composée du SQL, `fk_criteria_previous_same_request` (01:439), ne touche pas les fiches.

## B2. `user` : `id_role` sort, `system_role` arrive

* ADR-057, Décision 3.
* ➖ `id_role INTEGER NOT NULL REFERENCES role(id) ON DELETE RESTRICT` — 01:175 — cellule `-140`
* ➕ `system_role VARCHAR(10) CHECK (system_role IN ('Admin', 'Reader'))`, à la place de `id_role` (fixé le 15/10/2026)
  * Sans NOT NULL : vide pour un compte qui a une fiche (ADR-057, Décision 3).
* ➖ Le lien `Role` — `User` disparaît : arête `-279` (« Have a »), avec ses étiquettes `-280` (`0,n`), `-281` (`1,1`), `-282` (verbe).

## B3. Chaque fiche porte son rôle : `role_wording`

* ADR-057, Décision 4. Une ligne neuve dans chacune des 3 fiches.
* ➕ `client` (cellule `-45`) : `role_wording VARCHAR(20) NOT NULL DEFAULT 'Client' CHECK (role_wording = 'Client') REFERENCES role(wording)`
* ➕ `hunter` (cellule `-20`) : `role_wording VARCHAR(20) NOT NULL DEFAULT 'Hunter' CHECK (role_wording = 'Hunter') REFERENCES role(wording)`
* ➕ `real_estate_manager` (cellule `-157`) : `role_wording VARCHAR(20) NOT NULL DEFAULT 'Manager' CHECK (role_wording = 'Manager') REFERENCES role(wording)`
  * `'Manager'`, pas `'RealEstateManager'` : nom gardé (ADR-057, « Le nom du rôle de gestionnaire »).
* ✅ Place de la ligne : **juste après `id_user`**. Fixé le 15/10/2026 dans le socle du chantier (`context AI/16-refacto-profils.md`), pour que le SQL et le MPD disent pareil.

## B4. `role` : 3 lignes, et `wording` déjà UNIQUE

* ✅ `wording` est **déjà UNIQUE** : `wording VARCHAR(20) NOT NULL UNIQUE` — 01:164 — cellule `-278`. Une FK peut donc le viser sans rien ajouter.
* La table ne garde que 3 lignes : `'Client'`, `'Hunter'`, `'Manager'` (ADR-057, Décision 4). Ce sont des **données**, pas une colonne : rien à dessiner pour elles.
* ✏️ Le CHECK de `wording` liste aujourd'hui 5 valeurs : `CHECK (wording IN ('Admin', 'Client', 'Hunter', 'Manager', 'Reader'))` — 01:165.
  * Il passe à 3 : `CHECK (wording IN ('Client', 'Hunter', 'Manager'))`. La fiche PRF8 le dit : « `role` ne garde que `'Client'`, `'Hunter'`, `'Manager'` : son CHECK suit » (`context AI/16-refacto-profils.md`).
  * Admin et Reader vivent désormais dans `system_role`.

## B5. Le trigger « une fiche au plus par compte » : une note

* ADR-057, Décision 5 : une fiche au plus par compte, et aucune pour un compte qui a un `system_role`. Un **trigger** le garantit, sur les trois tables.
* ➕ Une note, comme celle du trigger U02 (`-457`). Texte proposé :
  * « Une fiche au plus par compte — garanti par un trigger, pas par une contrainte. »
  * « Un `user.id` ne se trouve que dans une seule des trois tables `client`, `hunter`, `real_estate_manager`. »
  * « Un compte qui a un `system_role` ('Admin' ou 'Reader') n'a aucune fiche. »
  * « Un UNIQUE ne le peut pas : il ne regarde qu'une table à la fois. »
* ✅ Les noms sont fixés le 15/10/2026 dans le socle du chantier ; la fiche PRF6 les reprend :
  * fonction `check_one_profile_per_user()` ;
  * triggers `trg_client_one_profile`, `trg_hunter_one_profile`, `trg_real_estate_manager_one_profile` (une fiche refusée si le compte a déjà une fiche ou un `system_role`) ;
  * trigger `trg_user_system_role` (un `system_role` refusé sur un compte qui a une fiche).
* Une ligne « Voir note du trigger » dans chaque fiche, comme `-15` dans `Mandate`, est 💡 optionnelle.

## B6. Les liens qui changent

* ➖ `Role` — `User` : voir B2 (arête `-279`).
* ➕ `Role` — `Client` : `0,n` près de `Role`, `1,1` près de `Client`.
* ➕ `Role` — `Hunter` : `0,n` près de `Role`, `1,1` près de `Hunter`.
* ➕ `Role` — `RealEstateManager` : `0,n` près de `Role`, `1,1` près de `RealEstateManager`.
  * Raison : `role_wording NOT NULL REFERENCES role(wording)`, sans UNIQUE (B3).
* 🟡 Le verbe de ces 3 liens neufs : Gabriel choisit. Propositions, dans la langue des autres verbes :
  * `Client` — « **Plays** » — `Role` (une fiche joue un rôle) ;
  * ou « **Has role** », plus proche de l'ancien « Have a » ;
  * le même verbe pour les 3 liens.
* `User` — fiche : **inchangé**, `1,1` près de la fiche, `0,1` près de `User`, verbe « is a ».
  * Déjà ainsi sur `-41` (`Client`) et `-184` (`RealEstateManager`).
  * Sur `-142` (`Hunter`), il manque le `0,1` côté `User` : c'est l'écart de la partie A.
  * La règle « une fiche au plus **en tout** » passe par la note du trigger (B5), pas par une cardinalité.

## B7. Ce qui ne change pas : `id_author` (4 tables)

* ADR-057, Décision 2 : un auteur peut être un Admin sans fiche. Ces 4 colonnes **restent** vers `"user"(id)`. ✅
  * `search_request.id_author INTEGER NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT` — 01:318 — cellule `-70`
  * `criteria.id_author INTEGER NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT` — 01:409 — cellule `-125`
  * `estate.id_author INTEGER REFERENCES "user"(id) ON DELETE RESTRICT` — 01:702 — cellule `-273`
  * `estate_contact.id_author INTEGER REFERENCES "user"(id) ON DELETE RESTRICT` — 01:757 — cellule `-467`
* Leurs arêtes vers `User` restent : `-192`, `-433`, `-400`, `-473`.
* Les 3 `id_user` des fiches restent aussi vers `"user"(id)` (01:204, 01:255, 01:277).


## B8. Les tables cibles, en entier

Ce que diront les 5 tables touchées après le chantier. Base : le `01` d'aujourd'hui (HEAD), plus les décisions d'ADR-057. Les lignes sans changement sont résumées par « … inchangé ».

```sql
CREATE TABLE role (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    wording    VARCHAR(20) NOT NULL UNIQUE
            CHECK (wording IN ('Client', 'Hunter', 'Manager'))
);

CREATE TABLE "user" (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at   TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    email        VARCHAR(150) NOT NULL UNIQUE,
    password     VARCHAR(255) NOT NULL,
    is_activated BOOLEAN NOT NULL DEFAULT FALSE,
    system_role  VARCHAR(10) CHECK (system_role IN ('Admin', 'Reader')),
    CONSTRAINT ck_user_email_format … inchangé
);

CREATE TABLE client (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at   … inchangé,
    id_user      INTEGER NOT NULL UNIQUE REFERENCES "user"(id) ON DELETE RESTRICT,
    role_wording VARCHAR(20) NOT NULL DEFAULT 'Client'
                 CHECK (role_wording = 'Client') REFERENCES role(wording),
    first_name   … et toutes les colonnes suivantes : inchangées
);

CREATE TABLE real_estate_manager (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at   … inchangé,
    id_user      INTEGER NOT NULL UNIQUE REFERENCES "user"(id) ON DELETE RESTRICT,
    role_wording VARCHAR(20) NOT NULL DEFAULT 'Manager'
                 CHECK (role_wording = 'Manager') REFERENCES role(wording),
    first_name   … et toutes les colonnes suivantes : inchangées
);

CREATE TABLE hunter (
    id                   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at           … inchangé,
    id_user              INTEGER NOT NULL UNIQUE REFERENCES "user"(id) ON DELETE RESTRICT,
    role_wording         VARCHAR(20) NOT NULL DEFAULT 'Hunter'
                         CHECK (role_wording = 'Hunter') REFERENCES role(wording),
    first_name           … inchangé jusqu'à is_hunter_ai,
    id_realestatemanager INTEGER NOT NULL
                         REFERENCES real_estate_manager(id) ON DELETE RESTRICT,
    CONSTRAINT ck_hunter_phone_number_format … inchangé
);
```

* Les 10 autres FK de B1 changent de la même façon : `(id_user)` devient `(id)`.
* 🟡 Ce DDL est la **cible écrite d'après l'ADR**, pas le SQL livré. À la clôture du chantier PRF, on le compare au `01` final ; un écart se corrige dans le MPD (le SQL fait foi).

---

# Partie C — hors du MPD (⚠️)

* ⚠️ L'en-tête du `01` (01:17-18) dit que le lien `hunter` — `real_estate_manager` est libellé « Manages ». Dans le MPD, ce lien dit « **Supervises** » (`-156`) ; « Manages » est le lien `RealEstateManager` — `SearchRequest` (`-151`). C'est le commentaire du SQL qui est en retard.
* ⚠️ Les `COMMENT ON COLUMN` du `01` (01:1250-1278) disent « Reference …(id_user) » et « Les FK pointent vers id_user ». Ils seront faux après PRF ; c'est au chantier de les réécrire.
* ⚠️ L'en-tête du `01` (01:108-122, « CLÉS DES SOUS-TYPES ») dit aussi que les FK visent `id_user` : même cas.
* ⚠️ `docker/init-v3/04_role-lecture-seule.sql` doit retirer `id_role` des colonnes ouvertes sur `"user"` (ADR-057, Décision 9). Pas dans le MPD.
* ⚠️ La copie de travail du `01` est modifiée et non commitée (chantier PRF en cours) : ce rapport ne l'a **pas** lue. La partie B suit l'ADR, pas ce brouillon.
* ⚠️ `MPD_4` et `vrac/v9.drawio.xml` (14/10) ne diffèrent que par l'ordre de deux lignes de `Client` (`id_user` et `created_at`) et la position de quelques étiquettes. Le MPD_4 a le bon ordre.

---

# Le compte

**Partie A — MPD_4 face au SQL d'aujourd'hui**
* ➕ **2** : `mandate_success_rate_for_max_score` ; étiquette `0,1` sur `-142`.
* ➖ **1** : étiquette `-402` en double.
* ✏️ **2** : regex irlandaise de `client` ; étiquettes inversées sur `-469`.
* 🟡 **1** : `1,n` sur `-76`.
* 💡 **14**, en détail :
  * ordre des colonnes : 6 (`criteria`, `estate`, `estate_proposed`, `commission_scale`, `payment`, `hunter_performance`) ;
  * ordre des valeurs de `proposition_status` : 1 ;
  * `Hunter(id_user)` en majuscule : 1 ;
  * « U2 » au lieu de « U02 » : 1 ;
  * nom `estate_contact` en minuscules : 1 ;
  * index : 4 ;
  * total : **14**.
* **Total A : 5 écarts à faire, 1 à décider, 14 optionnels.**

**Partie B — après le chantier PRF**
* ✏️ **12** : les 11 FK (B1) ; le CHECK de `role.wording` passe à 3 valeurs (B4).
* ➖ **2** : `user.id_role` ; l'arête `Role` — `User` et ses 3 étiquettes.
* ➕ **8** : `system_role` ; 3 `role_wording` ; 3 liens `Role` — fiche ; 1 note du trigger.
* 🟡 **3** : verbe des 3 liens neufs (compté 3). La place de `role_wording` et les noms du trigger sont fixés (B3, B5).
* 💡 **1** : la ligne « Voir note du trigger » dans les fiches.
* ✅ sans changement : 5 FK composées, 4 cibles UNIQUE, 4 `id_author`, 3 `id_user`, 3 liens `User` — fiche, `role.wording` déjà UNIQUE.
* **Total B : 22 écarts à faire, 3 à décider, 1 optionnel.**

**Partie C** : ⚠️ **6** remarques, hors du MPD.

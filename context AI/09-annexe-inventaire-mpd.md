# Annexe C1 — Inventaire des contraintes du MPD

Source : `../vrac/MPD 4 MEURISE.xml` (draw.io, hors dépôt, lecture seule).
Extraction automatique des cellules `mxCell` : HTML déséchappé, balises retirées,
espaces normalisés. Les contraintes sont recopiées **verbatim**, fautes comprises —
leur jugement revient à `C4` et `C5`. Seule retouche : `|` échappé en `\|` pour Markdown.
Chaque table finit par ses contraintes de niveau table (`CONSTRAINT …`).

## User

5 colonnes · 0 `CHECK` (0 de colonne, 0 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `email` | `VARCHAR(150)` | `NOT NULL UNIQUE` |
| `password` | `VARCHAR(255)` | `NOT NULL` |
| `id_role` | `INTEGER` | `NOT NULL REFERENCES role(id) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- aucune

## Role

2 colonnes · 1 `CHECK` (1 de colonne, 0 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `wording` | `VARCHAR(20)` | `NOT NULL UNIQUE CHECK ( wording IN ('Admin', 'Client', 'Hunter', 'Manager'))` |

**Contraintes de niveau table**

- aucune

## Client

15 colonnes · 12 `CHECK` (11 de colonne, 1 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `id_user` | `INTEGER` | `NOT NULL UNIQUE REFERENCES "user" (id) ON DELETE RESTRICT` |
| `first_name` | `VARCHAR(80)` | `NOT NULL CHECK (first_name = btrim(first_name) AND first_name <> '')` |
| `last_name` | `VARCHAR(80)` | `NOT NULL CHECK (last_name = btrim(last_name) AND last_name <> '')` |
| `country_iso` | `CHAR(2)` | `CHECK (country_iso IN ('FR', 'ES', 'DE','GB', 'IE', 'BE', 'NL', 'LU', 'IT','CH'))` |
| `gender` | `VARCHAR(10)` | `CHECK (gender IN ('male', 'female', 'other'))` |
| `phone_number` | `VARCHAR(20)` | `NOT NULL CHECK (phone_number = btrim(phone_number) AND phone_number <> '')` |
| `address` | `VARCHAR(150)` | `CHECK (address = btrim(address) AND address <> '')` |
| `address_complement` | `VARCHAR(150)` | `CHECK (address_complement = btrim(address_complement) AND address_complement <> '')` |
| `postal_code` | `VARCHAR(10)` | `CHECK (postal_code = btrim(postal_code) AND postal_code <> '')` |
| `town` | `VARCHAR(100)` | `CHECK (town = btrim(town) AND town <> '')` |
| `is_married` | `BOOLEAN` |  |
| `is_civil_solidarity_pact` | `BOOLEAN` |  |
| `nb_children` | `SMALLINT` | `CHECK (nb_children >= 0)` |
| `birth_date` | `DATE` | `CHECK (birth_date <= CURRENT_DATE)` |

**Contraintes de niveau table**

- `constraint chk_marital_status CHECK (NOT (is married AND is_civil_solidarity_pact))`

## Hunter

12 colonnes · 7 `CHECK` (7 de colonne, 0 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `id_user` | `INTEGER` | `NOT NULL UNIQUE REFERENCES "user" (id) ON DELETE RESTRICT` |
| `first_name` | `VARCHAR(80)` | `NOT NULL CHECK (first_name = btrim(first_name) AND first_name <> '')` |
| `last_name` | `VARCHAR(80)` | `NOT NULL CHECK (last_name = btrim(last_name) AND last_name <> '')` |
| `phone_number` | `VARCHAR(20)` | `NOT NULL CHECK (phone_number = btrim(phone_number) AND phone_number <> '')` |
| `country_iso` | `CHAR(2)` | `CHECK (country_iso IN ('FR', 'ES', 'DE','GB', 'IE', 'BE', 'NL', 'LU', 'IT','CH'))` |
| `gender` | `VARCHAR(10)` | `CHECK (gender IN ('male', 'female', 'other'))` |
| `company_name` | `VARCHAR(80)` | `CHECK (company_name = btrim(company_name) AND company_name <> '')` |
| `hire_date` | `DATE` | `NOT NULL` |
| `education_level` | `VARCHAR(20)` | `CHECK (education_level = btrim(education_level) AND education_level <> '')` |
| `is_cartet` | `BOOLEAN` |  |
| `certification_date` | `DATE` |  |

**Contraintes de niveau table**

- aucune

## RealEstateManager

8 colonnes · 6 `CHECK` (6 de colonne, 0 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `id_user` | `INTEGER` | `NOT NULL UNIQUE REFERENCES "user" (id) ON DELETE RESTRICT` |
| `first_name` | `VARCHAR(80)` | `NOT NULL CHECK (first_name = btrim(first_name) AND first_name <> '')` |
| `last_name` | `VARCHAR(80)` | `NOT NULL CHECK (last_name = btrim(last_name) AND last_name <> '')` |
| `phone_number` | `VARCHAR(20)` | `NOT NULL CHECK (phone_number = btrim(phone_number) AND phone_number <> '')` |
| `country_iso` | `CHAR(2)` | `CHECK (country_iso IN ('FR', 'ES', 'DE','GB', 'IE', 'BE', 'NL', 'LU', 'IT','CH'))` |
| `gender` | `VARCHAR(10)` | `CHECK (gender IN ('male', 'female', 'other'))` |
| `company_name` | `VARCHAR(80)` | `CHECK (company_name = btrim(company_name) AND company_name <> '')` |

**Contraintes de niveau table**

- aucune

## SearchRequest

6 colonnes · 0 `CHECK` (0 de colonne, 0 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `id_author` | `INTEGER` | `NOT NULL REFERENCES "user" (id) ON DELETE RESTRICT` |
| `id_client` | `INTEGER` | `NOT NULL REFERENCES client(id_user) ON DELETE RESTRICT` |
| `id_hunter` | `INTEGER` | `REFERENCES hunter(id_user) ON DELETE RESTRICT` |
| `id_realestatemanager` | `INTEGER` | `REFERENCES real_estate_manager(id_user) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- aucune

## Criteria

48 colonnes · 46 `CHECK` (30 de colonne, 16 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `change_reason` | `VARCHAR (255)` | `CHECK (change_reason = btrim(change_reason) AND change_reason <> '')` |
| `country_iso` | `CHAR(2)` | `CHECK (country_iso IN ('FR', 'ES', 'DE','GB', 'IE', 'BE', 'NL', 'LU', 'IT','CH'))` |
| `town` | `VARCHAR (100)` | `CHECK (town = btrim(town) AND town <> '')` |
| `postal_code` | `VARCHAR (10)` |  |
| `estate_type` | `VARCHAR(50)` | `NOT NULL CHECK (estate_type IN ('Appartement', 'Maison', 'Studio', 'Loft', 'Villa', 'Duplex', 'Terrain', 'Local commercial', 'Chalet', 'Château'))` |
| `typology` | `VARCHAR(50)` | `CHECK (typology IN ('Studio', 'T1 / F1', 'T1 bis / F1 bis', 'T2 / F2', 'T2 bis / F2 bis', 'T3 / F3', 'T3 bis / F3 bis', 'T4 / F4', 'T4 bis / F4 bis', 'T5 / F5', 'T5 bis / F5 bis', 'T6+ / F6+'))` |
| `budget_min` | `NUMERIC (6, 1)` | `CHECK (budget_min > 0)` |
| `budget_max` | `NUMERIC (6, 1)` | `NOT NULL CHECK (budget_max > 0)` |
| `floor` | `VARCHAR(10)` | `CHECK (floor IN ( '0','1','2','3','4','5','6','7','8','9','10 and more','last floor'))` |
| `is_new_build` | `BOOLEAN` |  |
| `needs_renovation` | `BOOLEAN` |  |
| `renovation_budget_min` | `NUMERIC (6, 1)` | `CHECK (renovation_budget_min >= 0)` |
| `renovation_budget_max` | `NUMERIC (6, 1)` | `CHECK (renovation_budget_max >= 0)` |
| `energy_class_max` | `CHAR(1)` | `CHECK (energy_class_max IN ('A', 'B', 'C', 'D', 'E', 'F', 'G'))` |
| `rooms_min` | `SMALLINT` | `CHECK (rooms_min > 0)` |
| `rooms_max` | `SMALLINT` | `CHECK (rooms_max > 0)` |
| `bedrooms_min` | `SMALLINT` | `CHECK (bedrooms_min >= 0)` |
| `bedrooms_max` | `SMALLINT` | `CHECK (bedrooms_max >= 0)` |
| `toilets_min` | `SMALLINT` | `CHECK (toilets_min >= 0)` |
| `toilets_max` | `SMALLINT` | `CHECK (toilets_max >= 0)` |
| `bathrooms_min` | `SMALLINT` | `CHECK (bathrooms_min >= 0)` |
| `bathrooms_max` | `SMALLINT` | `CHECK (bathrooms_max >= 0)` |
| `swimming_pool_min` | `SMALLINT` | `CHECK (swimming_pool_min >= 0)` |
| `swimming_pool_max` | `SMALLINT` | `CHECK (swimming_pool_max >= 0)` |
| `has_garden` | `BOOLEAN` |  |
| `nb_balcony_min` | `INTEGER` | `CHECK (nb_balcony_min >= 0)` |
| `nb_balcony_max` | `INTEGER` | `CHECK (nb_balcony_max >= 0)` |
| `nb_terrace_min` | `INTEGER` | `CHECK (nb_terrace_min >= 0)` |
| `nb_terrace_max` | `INTEGER` | `CHECK (nb_terrace_max >= 0)` |
| `is_climatised` | `BOOLEAN` |  |
| `surface_min` | `NUMERIC (7, 2)` | `CHECK (surface_min > 0)` |
| `surface_max` | `NUMERIC (7, 2)` | `CHECK (surface_max > 0)` |
| `land_surface_min` | `NUMERIC (9, 2)` | `CHECK (land_surface_min >= 0)` |
| `land_surface_max` | `NUMERIC (9, 2)` | `CHECK (land_surface_max >= 0)` |
| `has_separate_kitchen` | `BOOLEAN` |  |
| `has_cellar` | `BOOLEAN` |  |
| `has_view` | `BOOLEAN` |  |
| `is_quiet` | `BOOLEAN` |  |
| `is_bright` | `BOOLEAN` |  |
| `has_garage` | `BOOLEAN` |  |
| `has_elevator` | `BOOLEAN` |  |
| `has_chimney` | `BOOLEAN` |  |
| `parking_spaces` | `SMALLINT` | `CHECK (parking_spaces >= 0)` |
| `id_author` | `INTEGER` | `NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT` |
| `id_search_request` | `INTEGER` | `NOT NULL REFERENCES search_request(id) ON DELETE RESTRICT` |
| `id_previous_version` | `INTEGER` | `REFERENCES criteria(id) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- `CONSTRAINT chk_budget CHECK (budget_max >= budget_min)`
- `CONSTRAINT chk_renov_budget CHECK (renovation_budget_max >= renovation_budget_min)`
- `CONSTRAINT chk_rooms CHECK (rooms_max >= rooms_min)`
- `CONSTRAINT chk_bedrooms CHECK (bedrooms_max >= bedrooms_min)`
- `CONSTRAINT chk_toilets CHECK (toilets_max >= toilets_min)`
- `CONSTRAINT chk_pool CHECK (swimming_pool_max >= swimming_pool_min)`
- `CONSTRAINT chk_balcony CHECK (nb_balcony_max >= nb_balcony_min)`
- `CONSTRAINT chk_terrace CHECK (nb_terrace_max >= nb_terrace_min)`
- `CONSTRAINT chk_surface CHECK (surface_max >= surface_min)`
- `CONSTRAINT chk_land_surface CHECK (land_surface_max >= land_surface_min)`
- `CONSTRAINT ck_client_nb_children_positive CHECK (nb_children IS NULL OR nb_children >= 0)`
- `CONSTRAINT ck_client_marital_status_exclusive CHECK (NOT (is_married AND is_civil_solidarity_pact))`
- `CONSTRAINT ck_client_birth_date_past CHECK (birth_date IS NULL OR birth_date <= CURRENT_DATE)`
- `CONSTRAINT ck_client_address_all_or_nothing CHECK ( (address IS NULL AND postal_code IS NULL AND town IS NULL) OR (address IS NOT NULL AND postal_code IS NOT NULL AND town IS NOT NULL) )`
- `CONSTRAINT ck_client_postal_code_needs_country CHECK (postal_code IS NULL OR country_iso IS NOT NULL)`
- `CONSTRAINT ck_client_postal_code_format CHECK (postal_code IS NULL OR CASE WHEN country_iso IN ('FR','ES','DE','IT') THEN postal_code ~ '^[0-9]{5}$' WHEN country_iso IN ('BE','CH') THEN postal_code ~ '^[1-9][0-9]{3}$' WHEN country_iso = 'LU' THEN postal_code ~ '^[0-9]{4}$' WHEN country_iso = 'NL' THEN postal_code ~ '^[1-9][0-9]{3} [A-Z]{2}$' WHEN country_iso = 'GB' THEN postal_code ~ '^[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}$' WHEN country_iso = 'IE' THEN postal_code ~ '^([AC-FHKNPRTV-Y][0-9]{2}\|D6W) [0-9AC-FHKNPRTV-Y]{4}$' ELSE FALSE END))`

## Estate

42 colonnes · 26 `CHECK` (26 de colonne, 0 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `reference` | `VARCHAR(50)` | `NOT NULL UNIQUE CHECK (reference = btrim(reference) AND reference <> '')` |
| `country_iso` | `CHAR(2)` | `CHECK (country_iso IN ('FR', 'ES', 'DE','GB', 'IE', 'BE', 'NL', 'LU', 'IT','CH'))` |
| `estate_type` | `VARCHAR(50)` | `NOT NULL CHECK (estate_type IN ('Appartement', 'Maison', 'Studio', 'Loft', 'Villa', 'Duplex', 'Terrain', 'Local commercial', 'Chalet', 'Château'))` |
| `price` | `NUMERIC (6, 1)` | `CHECK (price >= 0)` |
| `construction_date` | `DATE` |  |
| `energy_class` | `CHAR(1)` | `CHECK (energy_class IN ('A','B','C','D','E','F','G'))` |
| `energy_class_scheme` | `VARCHAR(20)` |  |
| `energy_class_date` | `DATE` |  |
| `energy_kwh_m2` | `INTEGER` | `CHECK (energy_kwh_m2 > 0)` |
| `energy_co2_m2` | `INTEGER` | `CHECK (energy_co2_m2 > 0)` |
| `latitude` | `NUMERIC (9,6)` | `CHECK (latitude BETWEEN -90 AND 90)` |
| `longitude` | `NUMERIC (9,6)` | `CHECK (longitude BETWEEN -180 AND 180)` |
| `floor` | `VARCHAR(10)` | `CHECK (floor IN ( '0','1','2','3','4','5','6','7','8','9','10 and more','last floor'))` |
| `typology` | `VARCHAR(50)` | `CHECK (typology IN ('Studio', 'T1 / F1', 'T1 bis / F1 bis', 'T2 / F2', 'T2 bis / F2 bis', 'T3 / F3', 'T3 bis / F3 bis', 'T4 / F4', 'T4 bis / F4 bis', 'T5 / F5', 'T5 bis / F5 bis', 'T6+ / F6+'))` |
| `nb_rooms` | `SMALLINT` | `CHECK (nb_rooms > 0)` |
| `nb_bedrooms` | `SMALLINT` | `CHECK (nb_bedrooms >= 0)` |
| `nb_bathrooms` | `SMALLINT` | `CHECK (nb_bathrooms >= 0)` |
| `nb_toilets` | `SMALLINT` | `CHECK (nb_toilets >= 0)` |
| `nb_swimming_pool` | `SMALLINT` | `CHECK (nb_swimming_pool >= 0)` |
| `has_garden` | `BOOLEAN` |  |
| `nb_balcony` | `INTEGER` | `CHECK (nb_balcony >= 0)` |
| `nb_terrace` | `INTEGER` | `CHECK (nb_terrace >= 0)` |
| `is_climatised` | `BOOLEAN` |  |
| `surface` | `NUMERIC (7,2)` | `NOT NULL CHECK (surface > 0)` |
| `land_surface` | `NUMERIC (9,2)` | `CHECK (land_surface >= 0)` |
| `has_cellar` | `BOOLEAN` |  |
| `has_view` | `BOOLEAN` |  |
| `is_quiet` | `BOOLEAN` |  |
| `is_bright` | `BOOLEAN` |  |
| `has_garage` | `BOOLEAN` |  |
| `has_elevator` | `BOOLEAN` |  |
| `has_chimney` | `BOOLEAN` |  |
| `parking_spaces` | `SMALLINT` | `CHECK (parking_spaces >=0)` |
| `has_separate_kitchen` | `BOOLEAN` |  |
| `needs_renovation` | `BOOLEAN` |  |
| `town` | `VARCHAR (100)` | `NOT NULL CHECK (town = btrim(town) AND town <> '')` |
| `street` | `VARCHAR (100)` | `CHECK (street = btrim(street) AND street <> '')` |
| `street_number` | `VARCHAR (10)` | `CHECK (street_number = btrim(street_number) AND street_number <> '')` |
| `postal_code` | `VARCHAR (10)` | `CHECK (postal_code = btrim(postal_code) AND postal_code <> '')` |
| `information` | `TEXT` | `CHECK (char_length(information) <= 2000)` |

**Contraintes de niveau table**

- aucune

## Picture

4 colonnes · 0 `CHECK` (0 de colonne, 0 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `url` | `TEXT` | `NOT NULL` |
| `id_estate` | `INTEGER` | `NOT NULL REFERENCES estate(id) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- aucune

## Estate_SearchRequest

8 colonnes · 3 `CHECK` (2 de colonne, 1 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `review_hunter` | `TEXT` | `CHECK (char_length(review_hunter) <= 2000)` |
| `media_url` | `TEXT` |  |
| `media_type` | `VARCHAR (10)` | `CHECK (media_type IN ('audio' ,'video') )` |
| `id_estate` | `INTEGER` | `NOT NULL REFERENCES estate (id) ON DELETE RESTRICT` |
| `id_search_request` | `INTEGER` | `NOT NULL REFERENCES search_request (id) ON DELETE RESTRICT` |
| `id_hunter` | `INTEGER` | `NOT NULL REFERENCES Hunter(id_user) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- `CONSTRAINT chk_media CHECK ( (media_url IS NULL AND media_type IS NULL) OR (media_url IS NOT NULL AND media_type IS NOT NULL))`
- `CONSTRAINT uq_estate_search UNIQUE (id_estate, id_search_request)`

## EstateProposed

9 colonnes · 4 `CHECK` (3 de colonne, 1 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `comment_hunter` | `TEXT` | `CHECK (char_length(comment_hunter) <= 2000)` |
| `comment_client` | `TEXT` |  |
| `amount_proposition` | `NUMERIC (6, 1)` | `CHECK (amount_proposition >= 0)` |
| `proposition_status` | `VARCHAR(20)` | `NOT NULL CHECK (proposition_status IN ('proposed', 'offer_pending', 'accepted', 'rejected'))` |
| `id_hunter` | `INTEGER` | `NOT NULL REFERENCES hunter(id_user) ON DELETE RESTRICT` |
| `id_estate` | `INTEGER` | `NOT NULL REFERENCES estate(id) ON DELETE RESTRICT` |
| `id_mandate` | `INTEGER` | `NOT NULL REFERENCES mandate(id) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- `CONSTRAINT chk_offer CHECK ( proposition_status = 'proposed' AND amount_proposition IS NULL OR proposition_status <> 'proposed' AND amount_proposition IS NOT NULL )`

## Visit

6 colonnes · 1 `CHECK` (1 de colonne, 0 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `visit_date` | `DATE` | `NOT NULL` |
| `visitor_type` | `VARCHAR(10)` | `NOT NULL CHECK (visitor_type IN ('hunter', 'client'))` |
| `id_estate` | `INTEGER` | `NOT NULL REFERENCES estate(id) ON DELETE RESTRICT` |
| `id_mandate` | `INTEGER` | `NOT NULL REFERENCES mandate(id) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- aucune

## Mandate

13 colonnes · 5 `CHECK` (4 de colonne, 1 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `reference` | `VARCHAR(20)` | `NOT NULL UNIQUE CHECK (reference = btrim(reference) AND reference <> '')` |
| `status` | `VARCHAR(20)` | `NOT NULL CHECK (status IN('active', 'completed', 'expired', 'renewed', 'canceled'))` |
| `signature_date` | `DATE` |  |
| `signature_type` | `VARCHAR(20)` | `CHECK (signature_type IN ('electronic', 'paper'))` |
| `ends_at` | `DATE` | `CHECK ( (signature_date IS NULL AND ends_at IS NULL) OR (signature_date IS NOT NULL AND ends_at > signature_date) )` |
| `is_client_signed` | `BOOLEAN` | `NOT NULL DEFAULT FALSE` |
| `is_exclusive` | `BOOLEAN` | `NOT NULL` |
| `id_hunter` | `INTEGER` | `NOT NULL REFERENCES hunter(id_user) ON DELETE RESTRICT` |
| `id_client` | `INTEGER` | `NOT NULL REFERENCES client(id_user) ON DELETE RESTRICT` |
| `id_search_request` | `INTEGER` | `NOT NULL REFERENCES search_request(id) ON DELETE RESTRICT` |
| `id_mandate_parent` | `INTEGER` | `REFERENCES mandate(id) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- `CONSTRAINT chk_renewed CHECK (status <> 'renewed' OR id_mandate_parent IS NOT NULL)`

## Sale

8 colonnes · 4 `CHECK` (3 de colonne, 1 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `signature_date` | `DATE` | `NOT NULL` |
| `purchase_amount` | `NUMERIC(6,1)` | `NOT NULL CHECK (purchase_amount > 0)` |
| `fees_amount` | `NUMERIC(6,1)` | `NOT NULL CHECK (fees_amount > 0)` |
| `sale_origin` | `VARCHAR(20)` | `NOT NULL CHECK (sale_origin IN ('hunter', 'client_alone'))` |
| `id_mandate` | `INTEGER` | `NOT NULL UNIQUE REFERENCES mandate(id) ON DELETE RESTRICT` |
| `id_estate` | `INTEGER` | `NOT NULL REFERENCES estate(id) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- `CONSTRAINT chk_fees_lower_than_price CHECK (fees_amount < purchase_amount)`

## Payment

12 colonnes · 7 `CHECK` (6 de colonne, 1 de table) · 0 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `amount` | `NUMERIC(12,2)` | `NOT NULL CHECK (amount >=0)` |
| `status` | `VARCHAR(20)` | `NOT NULL CHECK (status IN ('announced', 'invoice_submitted', 'verified', 'scheduled', 'paid'))` |
| `paid_at` | `TIMESTAMP` |  |
| `base_rate` | `NUMERIC(5,4)` | `NOT NULL CHECK (base_rate > 0 AND base_rate <= 1)` |
| `final_rate` | `NUMERIC(5,4)` | `CHECK (final_rate > 0 AND final_rate <= 1)` |
| `seniority_rate` | `NUMERIC(5,4)` | `NOT NULL CHECK (seniority_rate BETWEEN 0 AND 0.10)` |
| `performance_rate` | `NUMERIC(5,4)` | `NOT NULL CHECK (performance_rate BETWEEN -0.20 AND 0.20)` |
| `id_sale` | `INTEGER` | `NOT NULL UNIQUE REFERENCES sale(id) ON DELETE RESTRICT` |
| `id_hunter` | `INTEGER` | `NOT NULL REFERENCES hunter(id_user) ON DELETE RESTRICT` |
| `id_commission_scale` | `INTEGER` | `NOT NULL REFERENCES commission_scale(id) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- `CONSTRAINT chk_paid CHECK ((status = 'paid' AND paid_at IS NOT NULL) OR (status <> 'paid' AND paid_at IS NULL))`

## CommissionScale

8 colonnes · 5 `CHECK` (3 de colonne, 2 de table) · 2 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `amount_min` | `NUMERIC(6,1)` | `NOT NULL CHECK (amount_min >= 0)` |
| `amount_max` | `NUMERIC(6,1)` | `CHECK (amount_max > amount_min)` |
| `rate` | `NUMERIC(5,4)` | `NOT NULL CHECK (rate >= 0 AND rate <= 1)` |
| `valid_until` | `DATE` |  |
| `valid_from` | `DATE` | `NOT NULL` |
| `id_hunter` | `INTEGER` | `REFERENCES hunter(id_user) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- `CONSTRAINT chk_scale_amounts CHECK (amount_max IS NULL OR amount_max > amount_min)`
- `CONSTRAINT chk_scale_period CHECK (valid_until IS NULL OR valid_until > valid_from)`
- `CONSTRAINT excl_scale_no_overlap EXCLUDE USING gist (id_hunter WITH =, numrange(amount_min, amount_max, '[)') WITH &&, daterange(valid_from, valid_until, '[]') WITH &&)`
- `CONSTRAINT excl_scale_global EXCLUDE USING gist (numrange(amount_min, amount_max, '[)') WITH &&, daterange(valid_from, valid_until, '[]') WITH &&) WHERE (id_hunter IS NULL)`

## HunterPerformance

10 colonnes · 4 `CHECK` (2 de colonne, 2 de table) · 1 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `score` | `NUMERIC(4,1)` | `NOT NULL CHECK (score BETWEEN 0 AND 100)` |
| `valid_from` | `DATE` | `NOT NULL` |
| `valid_until` | `DATE` |  |
| `trigger_type` | `VARCHAR(20)` | `NOT NULL CHECK (trigger_type IN ('initial', 'payment', 'mandate_expired'))` |
| `id_hunter` | `INTEGER` | `NOT NULL REFERENCES hunter(id_user) ON DELETE RESTRICT` |
| `id_payment` | `INTEGER` | `REFERENCES payment(id) ON DELETE RESTRICT` |
| `id_payment` | `INTEGER` | `REFERENCES payment(id) ON DELETE RESTRICT` |
| `id_mandate` | `INTEGER` | `REFERENCES mandate(id) ON DELETE RESTRICT` |

**Contraintes de niveau table**

- `CONSTRAINT chk_perf_period CHECK (valid_until IS NULL OR valid_until > valid_from)`
- `CONSTRAINT chk_perf_source CHECK ( (trigger_type = 'payment' AND id_payment IS NOT NULL AND id_mandate IS NULL) OR (trigger_type = 'mandate_expired' AND id_mandate IS NOT NULL AND id_payment IS NULL) OR (trigger_type = 'initial' AND id_payment IS NULL AND id_mandate IS NULL))`
- `CONSTRAINT excl_perf_no_overlap EXCLUDE USING gist (id_hunter WITH =, daterange(valid_from, valid_until, '[]') WITH &&)`

## ParametersFees

6 colonnes · 2 `CHECK` (2 de colonne, 0 de table) · 1 `EXCLUDE`

| colonne | type | contraintes |
|---|---|---|
| `id` | `INTEGER` | `GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` |
| `valid_from` | `DATE` | `NOT NULL` |
| `valid_until` | `DATE` |  |
| `fixed_amount` | `NUMERIC(6,1)` | `NOT NULL CHECK (fixed_amount > 0)` |
| `rate` | `NUMERIC(5,4)` | `NOT NULL CHECK (rate >= 0 and rate <= 1)` |

**Contraintes de niveau table**

- `CONSTRAINT excl_fees_no_overlap EXCLUDE USING gist (daterange(valid_from, valid_until, '[]') WITH &&)`

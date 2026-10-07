# Contraintes manquantes sur `client` — notes de travail

## 1. Constat

Le schéma de référence (`docker/init/01_create_fil_rouge_immobilier.sql:110-126`)
et le diagramme joint (`Client`, mêmes colonnes) sont identiques — pas d'écart
diagramme/SQL à signaler ici, contrairement au cas `criteria` (voir
[notes_contraintes_localisation_criteria.md](notes_contraintes_localisation_criteria.md)).

```sql
CREATE TABLE client (
    id                         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_user                    INTEGER NOT NULL UNIQUE REFERENCES "user"(id) ON DELETE RESTRICT,
    first_name                 VARCHAR(80) NOT NULL,
    last_name                  VARCHAR(80) NOT NULL,
    phone_number                VARCHAR(20) NOT NULL,
    gender                     VARCHAR(10) CHECK (gender IN ('male', 'female', 'other')),
    country_iso                CHAR(2) CHECK (country_iso IN ('FR', 'ES', 'DE', 'GB', 'IE', 'BE', 'NL', 'LU', 'IT', 'CH')),
    address                    VARCHAR(150),
    address_complement         VARCHAR(150),
    postal_code                VARCHAR(10),
    town                       VARCHAR(100),
    is_married                 BOOLEAN,
    is_civil_solidarity_pact   BOOLEAN,
    nb_children                SMALLINT,
    birth_date                 DATE
);
```

Aucune donnée réelle n'a été mesurée pour ces notes (pas de rapport
d'anomalies sur `client` dans `normalised/`, qui ne couvre que les annonces) —
l'analyse ci-dessous est une lecture statique du schéma.

Sujet mis hors scope, à traiter séparément : `phone_number` n'a de format
imposé ni sur `client`, ni sur `hunter`, ni sur `real_estate_manager`. C'est
transverse aux trois tables héritant de `user`, donc un ADR à part si besoin.

---

## 2. Contraintes proposées

```sql
-- colonnes (inchangées, rappel)
nb_children                SMALLINT,
birth_date                 DATE,

-- contraintes de table (multi-colonnes)
CONSTRAINT ck_client_nb_children_positive
    CHECK (nb_children IS NULL OR nb_children >= 0),
CONSTRAINT ck_client_marital_status_exclusive
    CHECK (NOT (is_married AND is_civil_solidarity_pact)),
CONSTRAINT ck_client_birth_date_past
    CHECK (birth_date IS NULL OR birth_date <= CURRENT_DATE),
CONSTRAINT ck_client_address_all_or_nothing
    CHECK (
        (address IS NULL AND postal_code IS NULL AND town IS NULL)
        OR (address IS NOT NULL AND postal_code IS NOT NULL AND town IS NOT NULL)
    ),
CONSTRAINT ck_client_postal_code_needs_country
    CHECK (postal_code IS NULL OR country_iso IS NOT NULL),
CONSTRAINT ck_client_postal_code_format
    CHECK (postal_code IS NULL OR CASE
        WHEN country_iso IN ('FR','ES','DE','IT') THEN postal_code ~ '^[0-9]{5}$'
        WHEN country_iso IN ('BE','CH')           THEN postal_code ~ '^[1-9][0-9]{3}$'
        WHEN country_iso = 'LU'                   THEN postal_code ~ '^[0-9]{4}$'
        WHEN country_iso = 'NL'                   THEN postal_code ~ '^[1-9][0-9]{3} [A-Z]{2}$'
        WHEN country_iso = 'GB'                   THEN postal_code ~ '^[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}$'
        WHEN country_iso = 'IE'                   THEN postal_code ~ '^([AC-FHKNPRTV-Y][0-9]{2}|D6W) [0-9AC-FHKNPRTV-Y]{4}$'
        ELSE FALSE
    END)
```

**Dans le drawio** : `ck_client_nb_children_positive` et
`ck_client_birth_date_past` se mettent sur la ligne de leur colonne (comme
`budget_min` ou `floor` sur d'autres tables) ; `ck_client_marital_status_exclusive`,
`ck_client_address_all_or_nothing`, `ck_client_postal_code_needs_country` et
`ck_client_postal_code_format` sont multi-colonnes et demandent une ligne
dédiée en bas de la table (« CONSTRAINTS »), comme pour `criteria` dans
l'ADR-021 — le format est repris à l'identique de `ck_criteria_postal_code_format`.

**Points à connaître :**

- Les quatre contraintes sont **permissives sur le NULL** : rien n'oblige à
  remplir `nb_children`, `birth_date`, ou l'adresse. Elles ne bloquent que les
  valeurs incohérentes *quand elles sont saisies*.
- `ck_client_marital_status_exclusive` n'est pas NULL-safe pour deux
  booléens NULL indépendants : si l'un des deux est NULL, `AND` renvoie NULL,
  et `NOT NULL` est NULL — PostgreSQL traite un `CHECK` qui évalue à NULL
  comme **validé** (seul FALSE le rejette). Donc `is_married = NULL` avec
  `is_civil_solidarity_pact = TRUE` passe, ce qui est voulu (statut inconnu
  ≠ statut incohérent).
- `ck_client_address_all_or_nothing` ne couvre pas `address_complement`,
  laissé libre dans tous les cas (voir limite assumée plus bas).
- Combinaisons valides pour l'adresse : rien ; ou les trois
  (`address`, `postal_code`, `town`) ensemble. Toute combinaison partielle
  (ex. `postal_code` seul) est rejetée.
- `ck_client_postal_code_format` reprend telle quelle la logique de
  `ck_criteria_postal_code_format` (ADR-021) : FR/ES/DE/IT sur 5 chiffres,
  BE/CH sur 4 chiffres, LU sur 4 chiffres, NL `1234 AB`, GB au format
  outward/inward, IE au format Eircode. `~` est **sensible à la casse** :
  l'API doit mettre en majuscules et formater NL/GB/IE avant insertion.
- Un code postal **partiel** est rejeté (« tout le 31 ») — même limite que
  sur `criteria`.
- `ck_client_postal_code_needs_country` est redondante avec le `ELSE FALSE`
  du format (un `country_iso` NULL tombe dans le ELSE), gardée pour un
  message d'erreur explicite, comme sur `criteria`.

---

## 3. Brouillon ADR-022 (à coller dans le journal Confluence)

Le journal va actuellement jusqu'à l'ADR-021 (brouillon, voir
[notes_contraintes_localisation_criteria.md](notes_contraintes_localisation_criteria.md)).

**ADR-022 : Contraintes de cohérence sur `client`**

**Date :** 10/09/2026
**Statut :** proposé
**Décideurs :** L'équipe projet

**Contexte :** `client` porte plusieurs colonnes sans aucune contrainte de
cohérence au-delà du typage : `nb_children` accepte un nombre négatif,
`is_married` et `is_civil_solidarity_pact` peuvent être vrais simultanément
alors qu'en droit français le mariage dissout automatiquement le PACS,
`birth_date` accepte une date future, `address` / `postal_code` / `town`
sont nullables indépendamment sans qu'aucune règle ne garantisse un profil
d'adresse cohérent, et `postal_code` n'a aucun format alors que
`country_iso` autorise déjà 10 pays (même situation que `criteria` dans
l'ADR-021).

**Options envisagées :**

| Sujet | Option | Motif |
|---|---|---|
| `nb_children` | Aucune contrainte | Laisse passer des valeurs négatives absurdes |
| | **`CHECK (nb_children >= 0)`** | **Retenue** : simple, aucun risque de faux positif |
| `is_married` / `is_civil_solidarity_pact` | Aucune contrainte | Autorise un état juridiquement impossible en France |
| | **`CHECK (NOT (is_married AND is_civil_solidarity_pact))`** | **Retenue** : traduit la règle métier (le mariage dissout le PACS) |
| `birth_date` | Aucune contrainte | Autorise une date de naissance future |
| | **`CHECK (birth_date <= CURRENT_DATE)`** | **Retenue** : borne minimale, ne tranche pas la question de la majorité légale |
| | Contrainte de majorité (`birth_date <= CURRENT_DATE - INTERVAL '18 years'`) | Écartée pour cet ADR : capacité juridique à contracter est une règle métier plus large (mandats, signatures), à traiter séparément si confirmée |
| `address` / `postal_code` / `town` | Aucune contrainte | Autorise un profil partiel (ex. code postal sans ville) |
| | Implication (`postal_code` ⇒ `town`) | Plus souple, mais laisse `address` seule sans `postal_code`/`town` |
| | **Tout ou rien** (les trois NULL ensemble, ou les trois renseignés ensemble) | **Retenue** : un profil d'adresse est complet ou absent, jamais partiel |
| Format du CP | France seule, `^[0-9]{5}$` | Colle aux données, mais rejette 9 pays sur 10 |
| | **Regex par pays via `country_iso`** | **Retenue** : identique à l'ADR-021 sur `criteria`, garde la cohérence entre les deux tables |
| | Regex générique | N'apporte presque aucune garantie |

**Décision :** `client` reçoit les contraintes suivantes :

- `ck_client_nb_children_positive` : `CHECK (nb_children IS NULL OR nb_children >= 0)` ;
- `ck_client_marital_status_exclusive` : `CHECK (NOT (is_married AND is_civil_solidarity_pact))` ;
- `ck_client_birth_date_past` : `CHECK (birth_date IS NULL OR birth_date <= CURRENT_DATE)` ;
- `ck_client_address_all_or_nothing` : `CHECK ((address IS NULL AND postal_code IS NULL AND town IS NULL) OR (address IS NOT NULL AND postal_code IS NOT NULL AND town IS NOT NULL))` ;
- `ck_client_postal_code_needs_country` : un code postal exige un pays ;
- `ck_client_postal_code_format` : format du code postal selon le pays, avec
  FR/ES/DE/IT sur 5 chiffres, BE/CH sur 4 chiffres, LU sur 4 chiffres, NL
  `1234 AB`, GB au format outward/inward, IE au format Eircode.

**Justification :** Ces six contraintes ferment des états incohérents que
seul un contrôle applicatif interceptait jusqu'ici (ou n'interceptait pas du
tout pour les insertions directes — fakers, migration, script). Elles ne
retirent aucune souplesse métier : un client peut toujours n'avoir renseigné
aucune adresse, aucun enfant, aucune date de naissance ; la contrainte porte
sur la cohérence de ce qui est renseigné, pas sur l'obligation de le
renseigner. Aligner le format du code postal sur l'ADR-021 évite que
`client` et `criteria` divergent sur la même règle.

**Conséquences :**

- **Schéma :** ajouter les six `CHECK` à `client` dans
  `01_create_fil_rouge_immobilier.sql`.
- **API :** un formulaire de profil client doit désormais soumettre
  `address`/`postal_code`/`town` ensemble ou aucun des trois, ne peut plus
  cocher `is_married` et `is_civil_solidarity_pact` en même temps, et doit
  mettre en majuscules / normaliser le code postal (NL, GB, IE, préfixe `L-`
  des codes LU) avant insertion — même traitement que pour `criteria`.
- **Limite assumée :** `ck_client_address_all_or_nothing` ne couvre pas
  `address_complement` (reste libre dans tous les cas — un complément
  d'adresse seul sans adresse principale n'a pas de sens mais n'est pas
  bloqué). Un code postal partiel (ex. « tout le 31 ») reste rejeté, comme
  sur `criteria`.
- **Cohérence :** reprend à l'identique la logique de format de l'ADR-021 —
  toute évolution du barème par pays (nouveau pays, format Eircode révisé…)
  doit être répercutée sur les deux tables.
- **Hors scope :** `phone_number` (format), transverse à `client`/`hunter`/
  `real_estate_manager`, à traiter dans un ADR séparé si besoin.

# ADR-022 : Contraintes de cohérence sur client

> Copié de Confluence (page 52363425, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

> Modifié en partie par ADR-053 (« Les trous de la base — les 13 choix du 12/10 ») : bandeau de la page d'origine, hors de son corps.

**Date :** 10/09/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte**

`client` porte plusieurs colonnes sans aucune contrainte de cohérence au-delà du typage : `nb_children` accepte un nombre négatif, `is_married` et `is_civil_solidarity_pact` peuvent être vrais simultanément alors qu'en droit français le mariage dissout automatiquement le PACS, `birth_date` accepte une date future, `address` / `postal_code` / `town` sont nullables indépendamment sans qu'aucune règle ne garantisse un profil d'adresse cohérent, et `postal_code` n'a aucun format alors que `country_iso` autorise déjà 10 pays (même situation que `criteria` dans l'ADR-021).

**Options envisagées**

| Sujet | Option | Motif |
| --- | --- | --- |
| `nb_children` | Aucune contrainte | Laisse passer des valeurs négatives absurdes |
|  | `CHECK (nb_children >= 0)` (retenue) | Simple, aucun risque de faux positif |
| `is_married` / `is_civil_solidarity_pact` | Aucune contrainte | Autorise un état juridiquement impossible en France |
|  | `CHECK (NOT (is_married AND is_civil_solidarity_pact))` (retenue) | Traduit la règle métier (le mariage dissout le PACS) |
| `birth_date` | Aucune contrainte | Autorise une date de naissance future |
|  | `CHECK (birth_date <= CURRENT_DATE)` (retenue) | Borne minimale, ne tranche pas la question de la majorité légale |
|  | Contrainte de majorité (`birth_date <= CURRENT_DATE - INTERVAL '18 years'`) | Écartée pour cet ADR : la capacité juridique à contracter est une règle métier plus large (mandats, signatures), à traiter séparément si confirmée |
| `address` / `postal_code` / `town` | Aucune contrainte | Autorise un profil partiel (ex. code postal sans ville) |
|  | Implication (`postal_code` ⇒ `town`) | Plus souple, mais laisse `address` seule sans `postal_code`/`town` |
|  | Tout ou rien : les trois NULL ensemble, ou les trois renseignés ensemble (retenue) | Un profil d'adresse est complet ou absent, jamais partiel |
| Format du CP | France seule, `^[0-9]{5}$` | Colle aux données, mais rejette 9 pays sur 10 déjà couverts par `country_iso` |
|  | Regex par pays via `country_iso` (retenue) | Identique à l'ADR-021 sur `criteria`, garde la cohérence entre les deux tables |
|  | Regex générique | N'apporte presque aucune garantie |

**Décision**

`client` reçoit les contraintes suivantes :

```sql
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

Les quatre premières contraintes sont permissives sur le NULL : rien n'oblige à remplir `nb_children`, `birth_date`, ou l'adresse. Elles ne bloquent que les valeurs incohérentes quand elles sont saisies. Les deux dernières reprennent à l'identique la logique de format de l'ADR-021 sur `criteria`.

**Justification**

Ces six contraintes ferment des états incohérents que seul un contrôle applicatif interceptait jusqu'ici (ou n'interceptait pas du tout pour les insertions directes — fakers, migration, script). Elles ne retirent aucune souplesse métier : un client peut toujours n'avoir renseigné aucune adresse, aucun enfant, aucune date de naissance ; la contrainte porte sur la cohérence de ce qui est renseigné, pas sur l'obligation de le renseigner. Aligner le format du code postal sur l'ADR-021 évite que `client` et `criteria` divergent sur la même règle — la redondance entre les deux `CHECK` est acceptée pour l'instant plutôt que factorisée dans une fonction SQL commune.

**Conséquences**

- **Schéma :** ajouter les six `CHECK` à `client` dans `01_create_fil_rouge_immobilier.sql`.
- **API :** un formulaire de profil client doit désormais soumettre `address`/`postal_code`/`town` ensemble ou aucun des trois, ne peut plus cocher `is_married` et `is_civil_solidarity_pact` en même temps, et doit mettre en majuscules / normaliser le code postal (NL, GB, IE, préfixe `L-` des codes LU) avant insertion — même traitement que pour `criteria`.
- **Limite assumée :** `ck_client_address_all_or_nothing` ne couvre pas `address_complement` (reste libre dans tous les cas — un complément d'adresse seul sans adresse principale n'a pas de sens mais n'est pas bloqué). Un code postal partiel (ex. « tout le 31 ») reste rejeté, comme sur `criteria`.
- **Cohérence à vérifier :** reprend à l'identique la logique de format de l'ADR-021 — toute évolution du barème par pays (nouveau pays, format Eircode révisé…) doit être répercutée sur les deux tables.
- **Hors scope :** `phone_number` (format), transverse à `client`/`hunter`/`real_estate_manager`, à traiter dans un ADR séparé si besoin.

# ADR-021 : Contraintes de localisation sur Criteria (town, postal_code, country_iso)

> Copié de Confluence (page 52330685, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 10/09/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte**

Dans le MPD v0.3, `Criteria.town` (`VARCHAR(100)`) et `Criteria.postal_code` (`VARCHAR(10)`) n'ont aucune contrainte, contrairement à `country_iso` qui a déjà son `CHECK` fermé sur dix pays (ADR-020). Rien n'empêche donc une recherche avec une ville vide ou mal saisie (`' Toulouse '`), ni un code postal sans rapport avec son pays. Les données actuelles sont 100 % françaises : 2 556 annonces sur 2 556 et 5 recherches sur 5 ont un code postal à 5 chiffres.

**Options envisagées**

| Sujet | Option | Motif |
| --- | --- | --- |
| Obligation | `town` et `postal_code` NOT NULL | Interdit une recherche par pays seul ou par pays + ville |
|  | Au moins un de `town`, `postal_code`, `country_iso` | Refuse une recherche sans localisation, mais impose une contrainte que le groupe n'a pas voulue |
|  | Tout nullable, avec implication `town`/`postal_code` ⇒ `country_iso` (retenue) | Aucune obligation de localiser une recherche, mais dès qu'on précise une ville ou un CP, le pays doit être précisé aussi |
| Format du CP | France seule, `^[0-9]{5}$` | Colle aux données actuelles, mais rejette 9 pays sur 10 déjà couverts par `country_iso` |
|  | Regex par pays via `country_iso` (retenue) | Cohérente avec la liste des pays déjà autorisés par l'ADR-020 |
|  | Regex générique | N'apporte presque aucune garantie |

**Décision**

`Criteria` reçoit les contraintes suivantes :

```sql
-- colonnes
country_iso  CHAR(2) CHECK (country_iso IN ('FR','ES','DE','GB','IE','BE','NL','LU','IT','CH')),
town         VARCHAR(100) CHECK (town = btrim(town) AND town <> ''),
postal_code  VARCHAR(10),

-- contraintes de table (multi-colonnes)
CONSTRAINT ck_criteria_town_needs_country
    CHECK (town IS NULL OR country_iso IS NOT NULL),
CONSTRAINT ck_criteria_postal_code_needs_country
    CHECK (postal_code IS NULL OR country_iso IS NOT NULL),
CONSTRAINT ck_criteria_postal_code_format
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

Aucune des trois colonnes n'est obligatoire en tant que telle : une recherche peut n'avoir aucune localisation. La seule règle est une implication — dès que `town` ou `postal_code` est saisi, `country_iso` devient obligatoire.

**Justification**

La base garantit que, dès qu'une ville ou un code postal est précisé, le pays l'est aussi — condition nécessaire pour interpréter `postal_code` (son format dépend du pays, cf. ADR-020) et pour désambiguïser `town` entre pays homonymes. Un contrôle uniquement applicatif laisserait passer les insertions directes (fakers, migration). Faire dépendre le format du code postal du pays prépare la Phase 3 (international) sans migration ultérieure. Le format français, le seul présent aujourd'hui dans les données, est strictement validé ; les neuf autres pays déjà couverts par le `CHECK` de `country_iso` le sont aussi, par anticipation.

**Conséquences**

- **API :** avant insertion, mettre `postal_code` en majuscules, supprimer les espaces en bord, formater NL/GB/IE selon leur regex et retirer le préfixe `L-` des codes postaux luxembourgeois.
- **Limite assumée :** un code postal partiel (département seul, par exemple `31`) est rejeté. Une recherche par département demanderait une colonne dédiée, hors périmètre de cette décision.
- **Matching :** si `town`, `postal_code` et `country_iso` sont NULL, la recherche ne filtre pas sur la localisation.
- **Schéma :** ajouter `country_iso`, `town` et `postal_code` à `criteria` dans `01_create_fil_rouge_immobilier.sql`, absents à ce jour alors que le MPD v0.3 les porte déjà — écart à résorber séparément.
- **Cohérence à vérifier :** un ADR antérieur place la localisation sur `SearchRequest` via des clés étrangères `id_town`/`id_area` ; le MPD v0.3 la met aussi sur `Criteria`, en texte libre. Cette décision ne tranche pas laquelle des deux approches remplace l'autre — à concilier lors d'une revue dédiée.

# Contraintes de localisation sur `Criteria` — notes

Date : 10/09/2026
Source analysée : `../vrac/MPD cible v0.3.drawio.xml` (table `Criteria`)
Statut : **proposition** — rien n'a été reporté dans le drawio, le SQL de
référence ni Confluence.

---

## 1. Mesures

- **Diagramme v0.3, table `Criteria`** : `country_iso` a déjà son CHECK (liste
  de 10 pays), mais `town VARCHAR(100)` et `postal_code VARCHAR(10)` n'ont
  **aucune contrainte**.
- **Données** :
  - `normalised/annonces_normalised.csv` : 2 556 / 2 556 `postal_code` au
    format `99999` ; `town` : 0 NULL, 0 espace en bord, longueur max 8 ;
    4 villes (Toulouse 1 129, Annecy 568, Nantes 532, Limoges 327) ;
    4 couples ville / CP distincts.
  - `normalised/recherches.csv` : 5 / 5 recherches ont ville + code postal
    (Toulouse 31000 ×2, Limoges 87000, Nantes 44000, Annecy 74000).
- **Regex testées** (Python, syntaxe compatible PostgreSQL) : 17 / 17 CP
  valides acceptés, 13 / 13 invalides rejetés, 0 écart.
- **User stories** : aucune règle métier sur la localisation
  (grep `ville|postal|town|commune|localisation|secteur` → 0 résultat).

## 2. Choix retenus (questionnaire)

| Sujet | Choix |
|---|---|
| Obligation | Aucune des trois colonnes n'est obligatoire seule ; mais `town` **ou** `postal_code` renseigné ⇒ `country_iso` obligatoire (révision du 10/09/2026) |
| Format du CP | Regex par pays, pilotée par `country_iso` |
| Compléments | `town` non vide et sans espaces en bord ; un CP exige `country_iso` ; une ville exige aussi `country_iso` |

> **Révision du 10/09/2026** : pas de contrainte « au moins un des trois »
> — les trois colonnes peuvent rester NULL ensemble (recherche sans
> localisation). La seule règle est une implication : dès que `town` ou
> `postal_code` est saisi, `country_iso` devient obligatoire.

## 3. Contraintes proposées

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

**Dans le drawio** : le CHECK de `town` se met sur sa ligne (comme
`budget_min` ou `floor`) ; les trois `CONSTRAINT` multi-colonnes demandent une
ligne dédiée en bas de la table (par exemple « CONSTRAINTS »).

**Points à connaître :**

- **Aucune obligation de remplir une localisation** : les trois colonnes
  peuvent rester NULL ensemble (recherche sans critère géographique).
- `ck_criteria_postal_code_needs_country` double le `ELSE FALSE` du format
  (un pays NULL tombe dans le ELSE) ; elle est gardée pour produire un message
  d'erreur explicite.
- Combinaisons valides : rien ; `country_iso` seul ; `country_iso` + `town` ;
  `country_iso` + `postal_code` ; les trois. **`town` ou `postal_code` sans
  `country_iso` est rejeté.**
- Un code postal **partiel** est rejeté (« tout le 31 ») : une recherche par
  département demanderait une colonne dédiée.
- `~` est **sensible à la casse** : l'API doit mettre en majuscules et
  formater NL / GB / IE, et retirer le préfixe `L-` des codes LU.

## 4. Écarts relevés

1. **Le SQL de référence est en retard** :
   `docker/init/01_create_fil_rouge_immobilier.sql`, table `criteria`, n'a ni
   `country_iso`, ni `town`, ni `postal_code`. Le diagramme v0.3 est en avance
   sur le schéma de référence.
2. **L'ADR-010 est contredit** : il place la localisation sur `SearchRequest`
   via des clés étrangères `id_town` / `id_area` ; la v0.3 la met sur
   `Criteria`, en texte libre. Le nouvel ADR doit dire s'il remplace
   l'ADR-010.

---

## 5. Brouillon ADR-021 (à coller dans le journal Confluence)

Le journal va actuellement jusqu'à l'ADR-020.

**ADR-021 : Contraintes de localisation sur `Criteria` (`town`, `postal_code`, `country_iso`)**

**Date :** 10/09/2026
**Statut :** proposé
**Décideurs :** L'équipe projet

**Contexte :** Dans le MPD v0.3, `Criteria.town` (`VARCHAR(100)`) et
`Criteria.postal_code` (`VARCHAR(10)`) n'ont aucune contrainte. Rien n'empêche
donc une recherche sans aucune localisation, une ville vide ou mal saisie
(`' Toulouse '`), ni un code postal sans rapport avec son pays. Les données
actuelles sont 100 % françaises : 2 556 annonces sur 2 556 et 5 recherches
sur 5 ont un code postal à 5 chiffres. Mais `country_iso` autorise déjà
10 pays (ADR-002, dimension internationale).

**Options envisagées :**

| Sujet | Option | Motif |
|---|---|---|
| Obligation | `town` et `postal_code` NOT NULL | Interdit une recherche par pays ou par ville seule |
| | Au moins un de `town`, `postal_code`, `country_iso` | Refuse une recherche sans localisation, mais impose une contrainte que le groupe n'a pas voulue |
| | **Tout nullable, avec implication `town`/`postal_code` ⇒ `country_iso`** | **Retenue** : aucune obligation de localiser une recherche, mais dès qu'on précise une ville ou un CP, le pays doit être précisé aussi |
| Format du CP | France seule, `^[0-9]{5}$` | Colle aux données, mais rejette 9 pays sur 10 |
| | **Regex par pays via `country_iso`** | **Retenue** : cohérente avec la liste des pays autorisés |
| | Regex générique | N'apporte presque aucune garantie |

**Décision :** Criteria reçoit les contraintes suivantes :

- `town` : `CHECK (town = btrim(town) AND town <> '')` ;
- `ck_criteria_town_needs_country` : une ville exige un pays ;
- `ck_criteria_postal_code_needs_country` : un code postal exige un pays ;
- `ck_criteria_postal_code_format` : format du code postal selon le pays, avec
  FR/ES/DE/IT sur 5 chiffres, BE/CH/LU sur 4 chiffres, NL `1234 AB`, GB au
  format outward/inward, IE au format Eircode.

Aucune des trois colonnes n'est obligatoire en tant que telle : une recherche
peut n'avoir aucune localisation. La seule règle est une implication — dès
que `town` ou `postal_code` est saisi, `country_iso` devient obligatoire.

**Justification :** La base garantit que, dès qu'une ville ou un code postal
est précisé, le pays l'est aussi — condition nécessaire pour interpréter
`postal_code` (son format dépend du pays) et pour désambiguïser `town` entre
pays homonymes. Un contrôle uniquement applicatif laisserait passer les
insertions directes (fakers, migration). Faire dépendre le code postal du
pays prépare la Phase 3 (international) sans migration. Le format français,
le seul présent aujourd'hui, est strictement validé.

**Conséquences :**

- **API :** avant insertion, mettre en majuscules, supprimer les espaces en
  bord, formater NL/GB/IE et retirer le préfixe `L-` des codes LU.
- **Limite assumée :** un code postal partiel (département, par exemple `31`)
  est rejeté. Une recherche par département demanderait une colonne dédiée.
- **Matching :** si `town`, `postal_code` et `country_iso` sont NULL, la
  recherche ne filtre pas sur la localisation.
- **Schéma :** ajouter `country_iso`, `town` et `postal_code` à `criteria`
  dans `01_create_fil_rouge_immobilier.sql`, absents à ce jour.
- **Cohérence :** révise l'ADR-010 (localisation via `id_town`/`id_area` sur
  `SearchRequest`), à marquer comme remplacé ou à concilier.

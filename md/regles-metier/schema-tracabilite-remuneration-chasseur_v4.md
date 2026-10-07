# Schéma de traçabilité du calcul de rémunération du chasseur (v4)

Schéma complet pour porter la traçabilité du calcul — 5 tables concernées, dont une nouvelle (`Hunter_Performance`).

> **Révision v4** : ajoute une contrainte d'exclusion anti-chevauchement sur `Parameters_Fees` et retire, en conséquence, la FK `Sale.id_parameters_fees` — devenue redondante avec une garantie désormais posée en base plutôt que supposée. Détail en fin de document.
>
> **Révision v3** : ajoute une contrainte d'exclusion anti-chevauchement sur `Hunter_Performance` et ajuste la précision de `score`. Confirme `Hunter.hire_date` en `NOT NULL` (génération des données par faker, donc toujours renseignée).
>
> **Révision v2** : corrige une dépendance circulaire entre `Payment` et `Hunter_Performance`, une confusion de nom/type/unité sur les honoraires (`fees_amount` vs `agency_fee`), et ajoute `Hunter.hire_date`, oubliée en v1.

## Tables

### `Sale` (modifiée — ajout de H)

```sql
fees_amount NUMERIC(6,1) NOT NULL CHECK (fees_amount > 0)   -- H, figé à la signature, en K€
```

`fees_amount` = H = `montant_fixe + pourcentage × purchase_amount`, calculé une fois à la signature à partir du `Parameters_Fees` en vigueur à cette date, puis **jamais recalculé**.

**Pas de FK vers `Parameters_Fees`** (contrairement aux v2/v3) : `Parameters_Fees` n'a pas de dimension nominative comme `Commission_scale.id_hunter` — c'est un barème global, daté, sans variante possible. Sous réserve de la contrainte d'exclusion ci-dessous, `Sale.signature_date` retrouve **toujours exactement une** ligne de `Parameters_Fees` : pas d'ambiguïté à lever, donc pas de FK nécessaire pour la traçabilité. La table reste néanmoins reliée fonctionnellement à `Sale`, documentée comme telle plutôt que représentée par une arête, pour ne pas laisser croire à un oubli lors d'une relecture du diagramme.

`NUMERIC(6,1)` reprend la convention K€ déjà en place ailleurs dans le MPD (`Criteria.budget_min`/`budget_max`, `Sale.purchase_amount`).

### `Parameters_Fees` (modifiée — anti-chevauchement)

```sql
ALTER TABLE parameters_fees
    ADD CONSTRAINT excl_fees_no_overlap EXCLUDE USING gist (
        daterange(valid_from, valid_until, '[]') WITH &&
    );
```

Sans dimension nominative (pas d'`id_hunter`), l'exclusion porte directement sur la période — deux lignes ne peuvent jamais se chevaucher, garantissant qu'une date donnée retrouve toujours exactement une ligne. C'est cette contrainte qui rend la FK sur `Sale` superflue (cf. ci-dessus), pas une simple convention de gestion.

### `Commission_scale` (inchangée)

Le barème par tranche × date × chasseur nominatif nullable — déjà conforme à l'étape 3 du document officiel.

### `Hunter_Performance` (nouvelle table)

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE hunter_performance (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at   TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    score        NUMERIC(4,1) NOT NULL CHECK (score BETWEEN 0 AND 100),
    valid_from   DATE NOT NULL,
    valid_until  DATE,
    id_hunter    INTEGER NOT NULL REFERENCES hunter(id_user) ON DELETE RESTRICT,
    trigger_type VARCHAR(20) NOT NULL CHECK (trigger_type IN ('initial','payment','mandate_expired')),
    id_payment   INTEGER REFERENCES payment(id) ON DELETE RESTRICT,
    id_mandate   INTEGER REFERENCES mandate(id) ON DELETE RESTRICT,
    CONSTRAINT chk_perf_period CHECK (valid_until IS NULL OR valid_until > valid_from),
    CONSTRAINT chk_perf_source CHECK (
        (trigger_type = 'payment'         AND id_payment IS NOT NULL AND id_mandate IS NULL) OR
        (trigger_type = 'mandate_expired' AND id_mandate IS NOT NULL AND id_payment IS NULL) OR
        (trigger_type = 'initial'         AND id_payment IS NULL     AND id_mandate IS NULL)
    ),
    CONSTRAINT excl_perf_no_overlap EXCLUDE USING gist (
        id_hunter WITH =,
        daterange(valid_from, valid_until, '[]') WITH &&
    )
);
```

`score NUMERIC(4,1)` (et non `NUMERIC(5,2)`) : une valeur entre 0 et 100 à une décimale — la précision du document de calcul, qui arrondit le score à une décimale, `NUMERIC(5,2)` était surdimensionnée.

`excl_perf_no_overlap` empêche deux lignes de se chevaucher dans le temps pour un même chasseur — sans elle, rien n'interdisait deux scores simultanément « valides » pour le même `id_hunter`, ce qui aurait rendu `Payment.performance_rate` ambigu à retrouver par date malgré la suppression de la FK directe (le même problème déjà tranché pour `Commission_scale` par contrainte PostgreSQL plutôt que par logique applicative). `daterange(..., '[]')` inclut les deux bornes : une ligne qui se termine le jour même où la suivante commence est déjà un chevauchement d'un jour, ce qui est le comportement voulu ici (pas de flou sur la date pivot).

Une ligne = un score figé à une date, avec sa cause (`trigger_type`). Pas de duplication des 5 compteurs bruts (délai, exclusivité, ventes, mandats, visites) : ils sont déjà calculables depuis `Mandate`/`Sale`/`Visit` — seul le résultat (`score`) a besoin d'être historisé, puisque c'est lui qui entre dans le calcul du taux.

Le cycle apparent avec `Payment` (`Hunter_Performance.id_payment` → `Payment`, et inversement si `Payment` référençait `Hunter_Performance`) est cassé par construction : la ligne `trigger_type = 'initial'` (sans `id_payment` ni `id_mandate`) se crée à l'embauche du chasseur, avant tout paiement. L'ordre réel est toujours : `initial` → `Payment` (calcule `performance_rate` à partir du score courant, sans FK) → nouvelle ligne `Hunter_Performance` de type `'payment'` référençant ce `Payment` déjà existant. Aucune ligne ne référence jamais une ligne pas encore créée.

### `Hunter` (modifiée — ajout de l'ancienneté)

```sql
hire_date DATE NOT NULL
```

Nécessaire au calcul de `seniority_rate = min(2% × années révolues, 10%)`. `certification_date` (déjà présente sur `Hunter`) est la date de la carte professionnelle T — une notion distincte de la date d'entrée en fonction chez GaSeBeLa, qui ne peut pas s'y substituer.

`NOT NULL` confirmé : les données étant produites par un faker (et non par une migration du legacy), chaque chasseur généré aura systématiquement une `hire_date` — pas de trou à combler ni de valeur de reprise à documenter.

### `Payment` (modifiée — trace complète du calcul, sans cycle)

```sql
id_commission_scale     INTEGER NOT NULL REFERENCES commission_scale(id) ON DELETE RESTRICT
base_rate               NUMERIC(5,4) NOT NULL CHECK (base_rate > 0 AND base_rate <= 1)   -- taux de tranche, avant majoration
seniority_rate          NUMERIC(5,4) NOT NULL CHECK (seniority_rate BETWEEN 0 AND 0.10)  -- ancienneté
performance_rate        NUMERIC(5,4) NOT NULL CHECK (performance_rate BETWEEN -0.20 AND 0.20) -- (score-50)/50×20%
-- final_rate et amount existent déjà
```

`final_rate` = `borne(base_rate × (1 + seniority_rate + performance_rate), 0.20, 0.60)`, `amount` = `arrondi_centime(final_rate × H)` où H vient de `Sale.fees_amount` via `id_sale`.

**Pas de `id_hunter_performance` sur `Payment`** (contrairement à la v1) : `performance_rate` est déjà figé numériquement, donc la FK n'apportait qu'une preuve « quelle ligne de score exacte » reconstructible par date (les périodes de validité ne se chevauchent pas par chasseur), tout en créant un cycle de dépendance avec `Hunter_Performance.id_payment`. Seule `id_commission_scale` est conservée en plus du taux figé : contrairement au score, savoir *quel barème exact* (nominatif ou par défaut) a été appliqué a une valeur probante propre en cas de litige sur l'éligibilité à un tarif personnalisé — deux barèmes différents peuvent produire le même taux, et `base_rate` seul ne permet pas de trancher lequel a servi.

## Associations et cardinalités

| Association | Cardinalités | Sens |
|---|---|---|
| `Payment (1,1) —applies to— Commission_scale (0,n)` | modifiée (était 0,1) | chaque paiement s'appuie sur exactement une ligne de barème de commission ; une ligne sert 0..n paiements |
| `Payment (0,1) —generates— Hunter_Performance (0,1)` | nouvelle | un paiement déclenche au plus une nouvelle ligne de score (la hausse) |
| `Mandate (0,1) —generates— Hunter_Performance (0,1)` | nouvelle | un mandat expiré sans vente déclenche au plus une nouvelle ligne (la baisse) |
| `Hunter (0,n) —has— Hunter_Performance (1,1)` | nouvelle | chaque ligne de score appartient à exactement un chasseur |
| `Mandate (1,1) —results in— Sale (0,1)` | inchangée | rappel du lien déjà existant |
| `Sale (0,1) —triggers— Payment (1,1)` | inchangée | rappel du lien déjà existant |

> **Retiré depuis la v1** : `Payment (1,1) —s'appuie sur— Hunter_Performance (0,n)`. Cette relation créait un cycle avec `Hunter_Performance.id_payment` et faisait doublon avec `performance_rate`, déjà figé numériquement dans `Payment`. Voir la note sous `Hunter_Performance` ci-dessus pour la manière dont le cycle apparent est cassé sans cette FK.
>
> **Retiré depuis la v3** : `Sale (0,1) —applies to— Parameters_Fees (0,n)`. Pas d'arête dans le diagramme MERISE — la relation existe au niveau métier (le barème en vigueur à `Sale.signature_date`) mais est garantie sans ambiguïté par la contrainte d'exclusion sur `Parameters_Fees`, sans avoir besoin d'une FK pour la représenter. **Choix à documenter explicitement en ADR** avant soutenance, pour qu'une table sans arête entrante ne se lise pas comme un oubli.

## Point à trancher avant de dessiner

L'« étape 0 — droit à rémunération » (mandat exclusif → toujours payé ; non-exclusif + vente seule → jamais payé ; acte hors délai des 6 mois → aucun droit) n'est **pas modélisable en `CHECK` simple** : ça croise `Mandate.is_exclusive`, `Sale.sale_origin`, `Sale.signature_date` et `Mandate.ends_at`, sur plusieurs tables. Ça devra passer par un trigger PostgreSQL ou par la couche applicative — à esquisser pour le documenter dans le MPD (en commentaire) ou à garder pour la phase 4 (API).

## Journal des corrections (v1 → v2)

Relecture faite par un collègue (via Claude), intégrée ci-dessus. Résumé pour traçabilité :

| # | Problème identifié | Verdict | Correction |
|---|---|---|---|
| 1 | `Payment.id_hunter_performance` NOT NULL crée un cycle avec `Hunter_Performance.id_payment` | Cycle réel comme *smell*, mais pas une impossibilité technique bloquante (la ligne `'initial'` casse l'ordre de création) — la vraie conclusion est que cette FK est redondante avec `performance_rate` déjà figé | FK supprimée ; seule `Hunter_Performance.id_payment` subsiste |
| 2 | `id_parameters_fees` NOT NULL sur `Sale`, et confusion `agency_fee`/`fees_amount` | Juste sur le fond (le montant figé, pas la FK, doit être obligatoire) ; la confusion de nom venait d'un manque de visibilité sur le schéma déjà en place, pas d'un désaccord | FK repassée nullable ; nom/type/unité alignés sur `fees_amount NUMERIC(6,1)` (K€, cohérent avec le reste du MPD) |
| 3 | Redondance FK + valeurs figées sur `Payment` | Vraie en degré, pas en absolu — chaque redondance se justifie au cas par cas plutôt que par une règle générale « figer XOR pointer » | `id_commission_scale` conservée (valeur probante propre en cas de litige) ; `id_hunter_performance` supprimée (aucune valeur ajoutée au-delà de `performance_rate`) |
| 4 | `Hunter.hire_date` manquant | Entièrement fondé — nécessaire au calcul de `seniority_rate`, distinct de `certification_date` (carte T) | Colonne ajoutée sur `Hunter` |
| 5 | `trigger_type` + `chk_perf_source`, non-duplication des 5 compteurs, étape 0 hors `CHECK` | Confirmés sans réserve | Inchangés |

## Journal des corrections (v2 → v3)

Deuxième relecture, deux points de vérification + une incohérence mineure :

| # | Point soulevé | Verdict | Correction |
|---|---|---|---|
| 6 | `Hunter.hire_date NOT NULL` : la donnée existe-t-elle dans `fixtures/` (migration legacy) ? | Non applicable — le projet passe par un faker de données plutôt que par la migration du legacy, donc `hire_date` sera systématiquement générée | `NOT NULL` confirmé sans réserve, aucune valeur de reprise à documenter |
| 7 | Rien ne garantit l'absence de chevauchement de périodes dans `Hunter_Performance` pour un même chasseur — `chk_perf_period` ne vérifie qu'une ligne, pas deux entre elles | Fondé — même problème déjà tranché pour `Commission_scale` (contrainte PostgreSQL plutôt que discipline applicative) | Ajout de `EXCLUDE USING gist (id_hunter WITH =, daterange(valid_from, valid_until, '[]') WITH &&)`, nécessite `CREATE EXTENSION btree_gist` |
| 8 | `score NUMERIC(5,2)` surdimensionné pour une échelle 0–100 arrondie à une décimale dans le document de calcul | Fondé | `score NUMERIC(4,1)` |

## Journal des corrections (v3 → v4)

Discussion sur la nécessité de `Sale.id_parameters_fees`, à la suite d'une remarque du collègue soulignant que l'argument utilisé pour garder `id_commission_scale` ne s'applique pas à `Parameters_Fees` (pas de dimension nominative, donc pas d'ambiguïté de valeur à lever) :

| # | Point soulevé | Verdict | Correction |
|---|---|---|---|
| 9 | La FK `Sale.id_parameters_fees` est-elle superflue, `signature_date` suffisant à retrouver la ligne applicable ? | L'argument "la date suffit" n'était pas garanti par la base — aucune contrainte n'empêchait deux lignes `Parameters_Fees` de se chevaucher, contrairement à ce qui est maintenant en place sur `Hunter_Performance` (point 7) | Ajout de `EXCLUDE USING gist (daterange(valid_from, valid_until, '[]') WITH &&)` sur `Parameters_Fees`, qui rend la FK réellement redondante ; FK retirée de `Sale` |

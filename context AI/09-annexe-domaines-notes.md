# Annexe C3 — Domaines de valeurs exigés par les notes métier

> Écrite par la fiche `C3` du chantier `09-contraintes-mpd`, le 2026-09-11.
> Source : les cinq notes métier à la racine du dépôt, et rien d'autre.
> Relue par `C4` et `C5` : c'est la **citation** qui fait autorité, pas la
> reformulation de la colonne « Règle ».

## Conventions

- **Même relevé que `C2`** : une règle par ligne ; est relevé ce qui contraint
  une valeur (liste fermée, borne, taux, palier, cohérence de dates, format,
  unité). Aucune règle par déduction.
- **Citation** : le texte de la ligne source, recopié tel quel ; `…` marque une
  coupe, en début ou en fin de ligne, jamais une retouche. Une ligne source qui
  est elle-même une ligne de tableau perd ses `|` de bord ; ses séparateurs
  internes s'écrivent `\|` (échappement Markdown, pas une retouche). Le SQL et
  les formules sont mis entre accents graves.
- **Cible** : la table, choisie parmi les 18 du MPD. Quand la note nomme une
  colonne, elle suit en « note : `nom` », **telle que la note l'écrit** — ce
  nom n'est pas vérifié dans le MPD : le rattachement reste le travail de `C4`
  et `C5`.
- **Priorité.** Trois notes ne sont pas commitées, donc récentes :
  `notes_contraintes_client.md`, `notes_contraintes_localisation_criteria.md`,
  `schema-tracabilite-remuneration-chasseur_v4.md`. Elles priment sur
  `BAREME-COMMISSION.md` et `NOTES-REMUNERATION-CHASSEUR.md`. Les
  contradictions ne sont **pas tranchées** : elles ont leur propre section.
- **Paramètre ou règle.** `NOTES-REMUNERATION-CHASSEUR.md:17` prévient que les
  valeurs chiffrées (fixe, pourcentage, tranches, poids, bornes) sont
  « *proposées* par le prof, pas imposées ». Elles sont relevées telles
  quelles ; leur statut de paramètre ne change pas leur valeur.

## `BAREME-COMMISSION.md` — préfixe B

| # | Règle | Citation | Source | Cible |
|---|---|---|---|---|
| B01 | La base de calcul vaut un montant fixe plus un pourcentage du montant d'achat. | «`Base = montant_fixe + (pourcentage × montant_achat)`» | `BAREME-COMMISSION.md:12` | `ParametersFees`, `Sale` · à rattacher |
| B02 | La rémunération du chasseur est la base multipliée par un taux qui dépend du chasseur, du montant et de la date de l'acte. | «`Rémunération_chasseur = Base × taux(chasseur, montant_achat, date_acte)`» | `BAREME-COMMISSION.md:20` | `Payment`, `CommissionScale` · à rattacher |
| B03 | Le taux dépend de la tranche du montant d'achat ; chaque tranche a son taux. | «**Montant du projet** \| on regarde la tranche dans laquelle tombe `montant_achat` → chaque tranche a son propre taux» | `BAREME-COMMISSION.md:27` | `CommissionScale` · à rattacher |
| B04 | Le barème appliqué est celui en vigueur à la date de l'acte. | «**Date** \| le barème « varie dans le temps » → il faut prendre le barème **en vigueur à la date de l'acte**, pas le barème actuel» | `BAREME-COMMISSION.md:28` | `CommissionScale` · à rattacher |
| B05 | Deux chasseurs peuvent avoir des taux différents pour la même tranche et la même date. | «**Chasseur** \| le barème est « différent pour chaque chasseur » → deux chasseurs peuvent avoir des taux différents pour la même tranche/date» | `BAREME-COMMISSION.md:29` | `CommissionScale` · à rattacher |
| B06 | La performance se calcule sur 5 indicateurs. | «La performance est recalculée à partir de 5 indicateurs bruts…» | `BAREME-COMMISSION.md:35` | `HunterPerformance` · à rattacher |
| B07 | Délai signature du mandat → acte, arrondi à la semaine inférieure ; plus court vaut mieux. | «Délai signature mandat → acte authentique, **arrondi à la semaine inférieure** \| plus court = mieux (vente rapide)» | `BAREME-COMMISSION.md:39` | `HunterPerformance` · à rattacher |
| B08 | L'exclusivité du mandat valorise la performance. | «Mandat exclusif ou non \| l'exclusivité valorise la performance (le chasseur « sécurise » la vente)» | `BAREME-COMMISSION.md:40` | `HunterPerformance` · à rattacher |
| B09 | Plus de ventes réussies vaut mieux. | «Nombre de ventes réussies \| plus = mieux» | `BAREME-COMMISSION.md:41` | `HunterPerformance` · à rattacher |
| B10 | Plus de mandats signés vaut mieux. | «Nombre de mandats signés \| plus = mieux (mesure l'activité/productivité)» | `BAREME-COMMISSION.md:42` | `HunterPerformance` · à rattacher |
| B11 | Moins de visites avant achat vaut mieux. | «Nombre de visites avant achat \| **moins il y en a, plus la rémunération monte** (efficacité du matching)» | `BAREME-COMMISSION.md:43` | `HunterPerformance` · à rattacher |
| B12 | La performance est recalculée à la hausse quand un paiement est effectué. | «…**à la hausse** quand un paiement est effectué (vente aboutie, étape 12) ;» | `BAREME-COMMISSION.md:47` | `HunterPerformance`, `Payment` · à rattacher |
| B13 | La performance est recalculée à la baisse quand un mandat arrive à échéance (6 mois) sans vente. | «…**à la baisse** quand un mandat arrive à échéance (6 mois) sans vente (étape 13).» | `BAREME-COMMISSION.md:48` | `HunterPerformance`, `Mandate` · à rattacher |
| B14 | Le score est recalculé et historisé à chaque événement : vente payée, mandat expiré. | «…un score/niveau recalculé à chaque événement (vente payée, mandat expiré), alimenté par les 5 compteurs/indicateurs ci-dessus.» | `BAREME-COMMISSION.md:56` | `HunterPerformance` · à rattacher |
| B15 | Le barème est une table par tranche de montant × date de validité × chasseur, qui rend un taux ; le montant fixe y figure « éventuellement ». | «…table par **tranche de montant × date de validité × chasseur (ou niveau ancienneté/performance)** → `taux` (et éventuellement `montant_fixe` si lui aussi variable).» | `BAREME-COMMISSION.md:57` | `CommissionScale` · note : `taux` |

## `NOTES-REMUNERATION-CHASSEUR.md` — préfixe R

| # | Règle | Citation | Source | Cible |
|---|---|---|---|---|
| R01 | Sous mandat exclusif, le chasseur est toujours payé, même si le client trouve seul. | «…Mandat exclusif → toujours payé, même si le client trouve seul.…» | `NOTES-REMUNERATION-CHASSEUR.md:22` | `Mandate`, `Payment` · à rattacher |
| R02 | Sous mandat non exclusif, le chasseur n'est payé que s'il est à l'origine de la vente. | «…Mandat non-exclusif → payé seulement si c'est le chasseur qui est à l'origine de la vente.…» | `NOTES-REMUNERATION-CHASSEUR.md:22` | `Sale`, `Payment` · à rattacher |
| R03 | Un seul chasseur est payé par vente. | «…Un seul chasseur est payé par vente (jamais de partage).…» | `NOTES-REMUNERATION-CHASSEUR.md:22` | `Sale`, `Payment` · à rattacher |
| R04 | Un acte signé après signature du mandat + 6 mois n'ouvre aucun droit. | «…Un acte signé après l'échéance du mandat (signature + 6 mois) n'ouvre aucun droit.» | `NOTES-REMUNERATION-CHASSEUR.md:22` | `Mandate`, `Sale` · à rattacher |
| R05 | Les honoraires H valent un montant fixe plus un pourcentage du prix d'achat. | «`H = montant_fixe + pourcentage × prix_achat`» | `NOTES-REMUNERATION-CHASSEUR.md:26` | `ParametersFees`, `Sale` · à rattacher |
| R06 | Le chasseur touche une part de H, jamais un pourcentage du prix du bien. | «Le chasseur touche une part de **H** (les honoraires encaissés par l'entreprise via le notaire), **jamais** un pourcentage direct du prix du bien.…» | `NOTES-REMUNERATION-CHASSEUR.md:28` | `Payment` · à rattacher |
| R07 | Le score de performance va de 0 à 100 ; c'est une moyenne pondérée de 5 critères (ligne 31). | «**Étape 2 — Score de performance (0 à 100)**» | `NOTES-REMUNERATION-CHASSEUR.md:30` | `HunterPerformance` · à rattacher |
| R08 | Critère délai, poids 25 % ; notation par paliers de semaines : ≤ 12 → 100, 13-20 → 80, 21-28 → 60, 29-36 → 40, 37-48 → 20, > 48 → 0. | «Délai mandat → acte (arrondi à la semaine inférieure) \| 25% \| ≤12 sem:100 · 13-20:80 · 21-28:60 · 29-36:40 · 37-48:20 · >48:0» | `NOTES-REMUNERATION-CHASSEUR.md:35` | `HunterPerformance` · à rattacher |
| R09 | Critère exclusivité, poids 10 % ; exclusif → 100, non exclusif → 60. | «Exclusivité du mandat \| 10% \| exclusif:100 · non-exclusif:60» | `NOTES-REMUNERATION-CHASSEUR.md:36` | `HunterPerformance` · à rattacher |
| R10 | Critère ventes sur 12 mois glissants, poids 25 % ; note = min(100 ; ventes × 20). | «Nb ventes réussies (12 mois glissants) \| 25% \| min(100 ; ventes × 20)» | `NOTES-REMUNERATION-CHASSEUR.md:37` | `HunterPerformance` · à rattacher |
| R11 | Critère mandats sur 12 mois glissants, poids 15 % ; note = min(100 ; mandats × 10). | «Nb mandats signés (12 mois glissants) \| 15% \| min(100 ; mandats × 10)» | `NOTES-REMUNERATION-CHASSEUR.md:38` | `HunterPerformance` · à rattacher |
| R12 | Critère visites, poids 25 % ; notation : ≤ 3 → 100, 4-6 → 80, 7-9 → 60, 10-12 → 40, 13-15 → 20, > 15 → 0. | «Nb visites avant achat \| 25% \| ≤3:100 · 4-6:80 · 7-9:60 · 10-12:40 · 13-15:20 · >15:0» | `NOTES-REMUNERATION-CHASSEUR.md:39` | `HunterPerformance` · à rattacher |
| R13 | Un seul taux de tranche s'applique à la totalité des honoraires ; pas de calcul progressif. | «Grille par tranche de prix, **un seul taux pour la totalité** des honoraires (pas de découpage progressif façon impôt) :» | `NOTES-REMUNERATION-CHASSEUR.md:44` | `CommissionScale` · à rattacher |
| R14 | Tranche 1 : prix < 200 000 € → 30 %. | «< 200 000 € \| 30%» | `NOTES-REMUNERATION-CHASSEUR.md:48` | `CommissionScale` · à rattacher |
| R15 | Tranche 2 : 200 000 – 349 999 € → 35 %. | «200 000 – 349 999 € \| 35%» | `NOTES-REMUNERATION-CHASSEUR.md:49` | `CommissionScale` · à rattacher |
| R16 | Tranche 3 : 350 000 – 499 999 € → 40 %. | «350 000 – 499 999 € \| 40%» | `NOTES-REMUNERATION-CHASSEUR.md:50` | `CommissionScale` · à rattacher |
| R17 | Tranche 4 : 500 000 – 749 999 € → 45 %. | «500 000 – 749 999 € \| 45%» | `NOTES-REMUNERATION-CHASSEUR.md:51` | `CommissionScale` · à rattacher |
| R18 | Tranche 5 : prix ≥ 750 000 € → 50 %. | «≥ 750 000 € \| 50%» | `NOTES-REMUNERATION-CHASSEUR.md:52` | `CommissionScale` · à rattacher |
| R19 | Le barème est daté : on prend celui en vigueur à la date de l'acte. | «Le barème est **daté** (on prend celui en vigueur à la date de l'acte)…» | `NOTES-REMUNERATION-CHASSEUR.md:54` | `CommissionScale` · à rattacher |
| R20 | Un barème nominatif prime sur le barème par défaut. | «…et peut être **propre à un chasseur** (un barème nominatif prime sur le barème par défaut).» | `NOTES-REMUNERATION-CHASSEUR.md:54` | `CommissionScale` · à rattacher |
| R21 | Le taux final est borné entre 20 % et 60 %. | «`taux_final = borne(taux_base × (1 + ancienneté + performance), 20%, 60%)`» | `NOTES-REMUNERATION-CHASSEUR.md:58` | `Payment` · à rattacher |
| R22 | Majoration d'ancienneté : 2 % par année révolue, plafonnée à 10 % (5 ans). | «`ancienneté = min(2% × années révolues, 10%)          # plafonné à 5 ans`» | `NOTES-REMUNERATION-CHASSEUR.md:59` | `Payment`, `Hunter` · à rattacher |
| R23 | Majoration de performance : (score − 50) / 50 × 20 %, soit entre −20 % et +20 %. | «`performance = (score - 50) / 50 × 20%                 # pivot à 50, ±20%`» | `NOTES-REMUNERATION-CHASSEUR.md:60` | `Payment` · à rattacher |
| R24 | Les deux majorations sont relatives et s'additionnent avant application. | «Variations **relatives** et **additionnées** avant application (pas de composition explosive).…» | `NOTES-REMUNERATION-CHASSEUR.md:62` | `Payment` · à rattacher |
| R25 | La rémunération est arrondie au centime. | «`Rémunération = arrondi_centime(taux_final × H)`» | `NOTES-REMUNERATION-CHASSEUR.md:66` | `Payment` · à rattacher |
| R26 | La marge de l'entreprise vaut H moins la rémunération, sans arrondi séparé. | «`Marge entreprise = H - Rémunération   (jamais arrondie séparément)`» | `NOTES-REMUNERATION-CHASSEUR.md:67` | `Payment` · à rattacher |
| R27 | Les éléments du calcul sont figés à la date de l'acte et jamais recalculés. | «**Traçabilité** : tous les éléments du calcul sont **figés à la date de l'acte** dans `paiements` et ne sont jamais recalculés a posteriori — même si le barème change ensuite.» | `NOTES-REMUNERATION-CHASSEUR.md:70` | `Payment` · à rattacher |
| R28 | Paramètres des honoraires dans l'exemple : fixe 3 000 €, pourcentage 2,5 % (proposés, ligne 17). | «…Honoraires : 3000 + 2,5% × 420000 = **13 500,00 €**» | `NOTES-REMUNERATION-CHASSEUR.md:74` | `ParametersFees` · à rattacher |
| R29 | Le mandat porte une date de fin valant signature + 6 mois, et son exclusivité. | «`mandats` \| existe, à compléter \| ajouter `date_fin` (signature + 6 mois) et `exclusivite`» | `NOTES-REMUNERATION-CHASSEUR.md:89` | `Mandate` · note : `date_fin`, `exclusivite` |
| R30 | Les paramètres d'honoraires (fixe et pourcentage) sont datés. | «`parametres_honoraires` \| à créer \| `montant_fixe` + `taux_pourcentage`, **datés**» | `NOTES-REMUNERATION-CHASSEUR.md:90` | `ParametersFees` · note : `montant_fixe`, `taux_pourcentage` |
| R31 | Le barème a pour clé (chasseur, période, tranche) ; chasseur NULL = barème par défaut, sinon nominatif et prioritaire. | «`baremes_commission` \| à créer \| clé = **triplet (chasseur, période, tranche)** → `taux`. `chasseur_id NULL` = barème par défaut, sinon barème nominatif qui prime» | `NOTES-REMUNERATION-CHASSEUR.md:91` | `CommissionScale` · note : `chasseur_id`, `taux` |
| R32 | Le paiement fige honoraires, score, taux de base, majorations, taux final et montant. | «`paiements` \| à créer \| **fige** tous les termes du calcul (honoraires, score, taux_base, majorations, taux_final, montant) pour ne jamais les recalculer après coup» | `NOTES-REMUNERATION-CHASSEUR.md:92` | `Payment` · à rattacher |

## `notes_contraintes_client.md` — préfixe K

| # | Règle | Citation | Source | Cible |
|---|---|---|---|---|
| K01 | Le nombre d'enfants est positif ou nul. | «`CHECK (nb_children IS NULL OR nb_children >= 0),`» | `notes_contraintes_client.md:49` | `Client` · note : `nb_children` |
| K02 | Un client n'est pas à la fois marié et pacsé. | «`CHECK (NOT (is_married AND is_civil_solidarity_pact)),`» | `notes_contraintes_client.md:51` | `Client` · note : `is_married`, `is_civil_solidarity_pact` |
| K03 | La date de naissance n'est pas dans le futur. | «`CHECK (birth_date IS NULL OR birth_date <= CURRENT_DATE),`» | `notes_contraintes_client.md:53` | `Client` · note : `birth_date` |
| K04 | Adresse, code postal et ville : tous les trois ou aucun. | «…**Tout ou rien** (les trois NULL ensemble, ou les trois renseignés ensemble) \| **Retenue** : un profil d'adresse est complet ou absent, jamais partiel» | `notes_contraintes_client.md:144` | `Client` · note : `address`, `postal_code`, `town` |
| K05 | Un code postal exige un pays. | «`CHECK (postal_code IS NULL OR country_iso IS NOT NULL),`» | `notes_contraintes_client.md:60` | `Client` · note : `postal_code`, `country_iso` |
| K06 | Format du code postal selon le pays : mêmes six branches et même `ELSE FALSE` que L05 à L11, recopiés aux lignes 62 à 70. | «…**Regex par pays via `country_iso`** \| **Retenue** : identique à l'ADR-021 sur `criteria`, garde la cohérence entre les deux tables» | `notes_contraintes_client.md:146` | `Client` · note : `postal_code` |

## `notes_contraintes_localisation_criteria.md` — préfixe L

| # | Règle | Citation | Source | Cible |
|---|---|---|---|---|
| L01 | Le pays appartient à une liste fermée de 10 codes. | «`country_iso  CHAR(2) CHECK (country_iso IN ('FR','ES','DE','GB','IE','BE','NL','LU','IT','CH')),`» | `notes_contraintes_localisation_criteria.md:44` | `Criteria` · note : `country_iso` |
| L02 | La ville n'est pas vide et n'a pas d'espace en bord. | «`town         VARCHAR(100) CHECK (town = btrim(town) AND town <> ''),`» | `notes_contraintes_localisation_criteria.md:45` | `Criteria` · note : `town` |
| L03 | Une ville exige un pays. | «`CHECK (town IS NULL OR country_iso IS NOT NULL),`» | `notes_contraintes_localisation_criteria.md:50` | `Criteria` · note : `town`, `country_iso` |
| L04 | Un code postal exige un pays. | «`CHECK (postal_code IS NULL OR country_iso IS NOT NULL),`» | `notes_contraintes_localisation_criteria.md:52` | `Criteria` · note : `postal_code`, `country_iso` |
| L05 | FR, ES, DE, IT : 5 chiffres. | «`WHEN country_iso IN ('FR','ES','DE','IT') THEN postal_code ~ '^[0-9]{5}$'`» | `notes_contraintes_localisation_criteria.md:55` | `Criteria` · note : `postal_code` |
| L06 | BE, CH : 4 chiffres, le premier non nul. | «`WHEN country_iso IN ('BE','CH')           THEN postal_code ~ '^[1-9][0-9]{3}$'`» | `notes_contraintes_localisation_criteria.md:56` | `Criteria` · note : `postal_code` |
| L07 | LU : 4 chiffres. | «`WHEN country_iso = 'LU'                   THEN postal_code ~ '^[0-9]{4}$'`» | `notes_contraintes_localisation_criteria.md:57` | `Criteria` · note : `postal_code` |
| L08 | NL : 4 chiffres (premier non nul), une espace, 2 lettres majuscules. | «`WHEN country_iso = 'NL'                   THEN postal_code ~ '^[1-9][0-9]{3} [A-Z]{2}$'`» | `notes_contraintes_localisation_criteria.md:58` | `Criteria` · note : `postal_code` |
| L09 | GB : format outward / inward. | «`WHEN country_iso = 'GB'                   THEN postal_code ~ '^[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}$'`» | `notes_contraintes_localisation_criteria.md:59` | `Criteria` · note : `postal_code` |
| L10 | IE : format Eircode. | «`WHEN country_iso = 'IE'                   THEN postal_code ~ '^([AC-FHKNPRTV-Y][0-9]{2}\|D6W) [0-9AC-FHKNPRTV-Y]{4}$'`» | `notes_contraintes_localisation_criteria.md:60` | `Criteria` · note : `postal_code` |
| L11 | Tout autre cas, pays NULL compris, rejette le code postal. | «`ELSE FALSE`» | `notes_contraintes_localisation_criteria.md:61` | `Criteria` · note : `postal_code` |
| L12 | Les trois colonnes de localisation peuvent être NULL ensemble : pas de contrainte « au moins un ». | «…**Révision du 10/09/2026** : pas de contrainte « au moins un des trois »» | `notes_contraintes_localisation_criteria.md:35` | `Criteria` · note : `town`, `postal_code`, `country_iso` |

## `schema-tracabilite-remuneration-chasseur_v4.md` — préfixe T

| # | Règle | Citation | Source | Cible |
|---|---|---|---|---|
| T01 | H est strictement positif, en K€, `NUMERIC(6,1)`, figé à la signature. | «`fees_amount NUMERIC(6,1) NOT NULL CHECK (fees_amount > 0)   -- H, figé à la signature, en K€`» | `schema-tracabilite-remuneration-chasseur_v4.md:16` | `Sale` · note : `fees_amount` |
| T02 | H est calculé une fois, avec les paramètres en vigueur à la signature, et jamais recalculé. | «…calculé une fois à la signature à partir du `Parameters_Fees` en vigueur à cette date, puis **jamais recalculé**.» | `schema-tracabilite-remuneration-chasseur_v4.md:19` | `Sale`, `ParametersFees` · note : `fees_amount` |
| T03 | Deux lignes de paramètres d'honoraires n'ont jamais de périodes qui se chevauchent, bornes incluses (`excl_fees_no_overlap`). | «`daterange(valid_from, valid_until, '[]') WITH &&`» | `schema-tracabilite-remuneration-chasseur_v4.md:28-31` | `ParametersFees` · note : `valid_from`, `valid_until` |
| T04 | Une date de signature retrouve toujours exactement une ligne de paramètres. | «…`Sale.signature_date` retrouve **toujours exactement une** ligne de `Parameters_Fees`…» | `schema-tracabilite-remuneration-chasseur_v4.md:21` | `ParametersFees`, `Sale` · note : `signature_date` |
| T05 | Le score va de 0 à 100, à une décimale (`NUMERIC(4,1)`). | «`score        NUMERIC(4,1) NOT NULL CHECK (score BETWEEN 0 AND 100),`» | `schema-tracabilite-remuneration-chasseur_v4.md:48` | `HunterPerformance` · note : `score` |
| T06 | La cause d'un score a trois valeurs : `initial`, `payment`, `mandate_expired`. | «`trigger_type VARCHAR(20) NOT NULL CHECK (trigger_type IN ('initial','payment','mandate_expired')),`» | `schema-tracabilite-remuneration-chasseur_v4.md:52` | `HunterPerformance` · note : `trigger_type` |
| T07 | La fin de validité d'un score est NULL ou postérieure à son début. | «`CONSTRAINT chk_perf_period CHECK (valid_until IS NULL OR valid_until > valid_from),`» | `schema-tracabilite-remuneration-chasseur_v4.md:55` | `HunterPerformance` · note : `valid_from`, `valid_until` |
| T08 | La cause fixe la source : `payment` → paiement seul ; `mandate_expired` → mandat seul ; `initial` → ni l'un ni l'autre. | «`(trigger_type = 'payment'         AND id_payment IS NOT NULL AND id_mandate IS NULL) OR`» | `schema-tracabilite-remuneration-chasseur_v4.md:56-59` | `HunterPerformance` · note : `trigger_type` |
| T09 | Pour un même chasseur, deux scores n'ont jamais de périodes qui se chevauchent, bornes incluses (`excl_perf_no_overlap`). | «…une ligne qui se termine le jour même où la suivante commence est déjà un chevauchement d'un jour, ce qui est le comportement voulu ici…» | `schema-tracabilite-remuneration-chasseur_v4.md:61-64, :70` | `HunterPerformance` · note : `id_hunter`, `valid_from`, `valid_until` |
| T10 | Le taux de tranche est dans ]0 ; 1], `NUMERIC(5,4)`. | «`base_rate               NUMERIC(5,4) NOT NULL CHECK (base_rate > 0 AND base_rate <= 1)   -- taux de tranche, avant majoration`» | `schema-tracabilite-remuneration-chasseur_v4.md:90` | `Payment` · note : `base_rate` |
| T11 | La majoration d'ancienneté est dans [0 ; 0,10]. | «`seniority_rate          NUMERIC(5,4) NOT NULL CHECK (seniority_rate BETWEEN 0 AND 0.10)  -- ancienneté`» | `schema-tracabilite-remuneration-chasseur_v4.md:91` | `Payment` · note : `seniority_rate` |
| T12 | La majoration de performance est dans [−0,20 ; 0,20]. | «`performance_rate        NUMERIC(5,4) NOT NULL CHECK (performance_rate BETWEEN -0.20 AND 0.20) -- (score-50)/50×20%`» | `schema-tracabilite-remuneration-chasseur_v4.md:92` | `Payment` · note : `performance_rate` |
| T13 | Le taux final est borné entre 0,20 et 0,60. | «`final_rate` = `borne(base_rate × (1 + seniority_rate + performance_rate), 0.20, 0.60)`…» | `schema-tracabilite-remuneration-chasseur_v4.md:96` | `Payment` · note : `final_rate` |
| T14 | Le montant est arrondi au centime, sur H lu dans la vente. | «…`amount` = `arrondi_centime(final_rate × H)` où H vient de `Sale.fees_amount` via `id_sale`.» | `schema-tracabilite-remuneration-chasseur_v4.md:96` | `Payment` · note : `amount` |
| T15 | Le barème croise tranche × date × chasseur nominatif, qui peut être NULL. | «Le barème par tranche × date × chasseur nominatif nullable — déjà conforme à l'étape 3 du document officiel.» | `schema-tracabilite-remuneration-chasseur_v4.md:38` | `CommissionScale` · à rattacher |
| T16 | Le chevauchement de barèmes est dit « déjà tranché » par une contrainte PostgreSQL ; aucune note n'en donne le SQL. | «…le même problème déjà tranché pour `Commission_scale` par contrainte PostgreSQL plutôt que par logique applicative…» | `schema-tracabilite-remuneration-chasseur_v4.md:70` | `CommissionScale` · à rattacher |
| T17 | Le droit à rémunération croise mandat et vente : pas de `CHECK` simple, un trigger ou l'API. | «…n'est **pas modélisable en `CHECK` simple** : ça croise `Mandate.is_exclusive`, `Sale.sale_origin`, `Sale.signature_date` et `Mandate.ends_at`, sur plusieurs tables.…» | `schema-tracabilite-remuneration-chasseur_v4.md:117` | `Mandate`, `Sale` · note : `is_exclusive`, `sale_origin`, `signature_date`, `ends_at` |

## Contradictions entre notes — préfixe X

Non tranchées : les deux valeurs sont sur la même ligne. C'est un résultat du
chantier.

| # | Règle | Citation | Source | Cible |
|---|---|---|---|---|
| X01 | **contradiction** — Rôle de l'ancienneté et de la performance. BAREME : un niveau chasseur sert de **clé** pour lire le taux dans le barème. NOTES : ils **majorent** le taux de tranche après lecture (reprise par T11 à T13). NOTES se dit remplaçante de BAREME (ligne 7). | BAREME : «…ancienneté + performance → un **niveau/score chasseur**, qui sert de clé (avec la tranche de montant et la date) pour aller chercher le taux dans le barème.» — NOTES : «`taux_final = borne(taux_base × (1 + ancienneté + performance), 20%, 60%)`» | `BAREME-COMMISSION.md:31` ; `NOTES-REMUNERATION-CHASSEUR.md:58` | `CommissionScale`, `Payment` · à rattacher |
| X02 | **contradiction** — Unité et précision de H. NOTES : euros au centime. TRACABILITE (récente) : K€ à une décimale. | NOTES : «…Honoraires : 3000 + 2,5% × 420000 = **13 500,00 €**» — TRACABILITE : «`fees_amount NUMERIC(6,1) NOT NULL CHECK (fees_amount > 0)   -- H, figé à la signature, en K€`» | `NOTES-REMUNERATION-CHASSEUR.md:74` ; `schema-tracabilite-remuneration-chasseur_v4.md:16` | `Sale` · note : `fees_amount` |

## Règles qui portent sur une période de validité

Ce sont elles que les `EXCLUDE USING gist` du MPD sont censés protéger.

| Table | Ce qui est daté | Règles | Exclusion posée dans les notes |
|---|---|---|---|
| `ParametersFees` | fixe et pourcentage des honoraires | R30, T02, T03, T04 | oui — T03, sur la seule période, bornes incluses |
| `CommissionScale` | taux par tranche, par chasseur ou par défaut | B04, B15, R19, R20, R31, T15 | annoncée seulement — T16 dit « déjà tranché », sans SQL |
| `HunterPerformance` | score du chasseur | B14, T07, T09 | oui — T09, par chasseur, bornes incluses |
| `Mandate` | validité : signature → signature + 6 mois | R04, R29, B13 | aucune ; l'exclusivité pendant la validité vient de U02 (annexe `C2`) |

Deux points pour `C5` :

- **T04 promet plus que T03.** Une exclusion garantit *au plus* une ligne par
  date. « Toujours exactement une » suppose aussi l'absence de trou entre deux
  périodes, qu'aucune note ne pose.
- **Barème par défaut et NULL.** Si l'exclusion de `CommissionScale` porte sur
  le chasseur avec `=`, comme T09, deux barèmes par défaut (chasseur NULL, R31)
  ne s'excluent pas : une comparaison qui rend NULL ne fait pas conflit.

## Remarques — non marquées « contradiction »

- **Exemple Bruno** (`NOTES-REMUNERATION-CHASSEUR.md:73`) : mandat signé le
  14/11/2025, acte le 30/07/2026, donc après signature + 6 mois. R04 dit
  « aucun droit » ; l'exemple rémunère Bruno, sans parler de renouvellement.
  Contradiction **interne** à une note, pas entre deux notes.
- **Unité des bornes de tranche** : R14 à R18 sont en euros ;
  `schema-tracabilite-remuneration-chasseur_v4.md:23` range
  `Sale.purchase_amount` dans la convention K€. Aucune note ne fixe l'unité des
  bornes du barème.

## Lu mais non relevé

- `notes_contraintes_client.md:10-28` recopie le SQL de référence, périmé et
  hors jeu (socle) : les listes de `gender` et `country_iso` sur `Client`, lues
  là seulement, ne sont pas relevées.
- Les options **écartées** par les ADR ne sont pas des exigences : majorité à
  18 ans (`notes_contraintes_client.md:141`), « au moins un des trois »
  (`notes_contraintes_localisation_criteria.md:120`).
- Les consignes à l'API (majuscules, préfixe `L-` des codes LU) ne sont pas des
  contraintes de base. Ce qui sort de la frontière du socle n'est pas relevé.

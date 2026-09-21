# Contraintes à coder dans l'API (ou en trigger)

> **Extrait de** [`09-rapport-ecarts-contraintes.md`](09-rapport-ecarts-contraintes.md)
> (étape 4 + lignes « **Coder** » des tableaux du détail).
>
> **Date** : 2026-09-11.
>
> Les décisions citées (`D1`, `D3`…) sont dans
> [`09-decisions-a-prendre.md`](09-decisions-a-prendre.md).

---

## Pourquoi ces règles ne sont pas des `CHECK`

Un `CHECK` ne voit **qu'une seule ligne d'une seule table**. Il ne peut pas :

- lire **une autre table** (ex. : comparer `Sale` et `Mandate`) ;
- **compter** des lignes (ex. : « aucune vente pour ce mandat ») ;
- comparer avec **l'ancienne valeur** (ex. : « H ne change plus jamais »).

Toutes les règles ci-dessous font l'une de ces trois choses. Elles se codent :

- dans l'API, couche **`services/`** ;
- **ou** dans un **trigger** PostgreSQL (`BEFORE INSERT` / `BEFORE UPDATE`).

---

## Les comptes

| quoi | nombre |
|---|---|
| lignes « Coder » dans les tableaux du rapport | 31 |
| codes de règle distincts derrière ces lignes | 23 |
| blocs de code ci-dessous | 9 (`C1` à `C9`) |
| règles citées dans le texte du rapport sans « Coder » | 4 (`U02`, `U30`, `R20`, `R07`–`R12`) |

Beaucoup de codes apparaissent **deux fois** dans le rapport (une fois par
table touchée). Ici, chaque règle n'apparaît qu'**une** fois.

Répartition des 31 lignes : `C1` = 11, `C2` = 5, `C3` = 1, `C4` = 6,
`C5` = 1, `C6` = 3, `C7` = 2, `C8` = 1, `C9` = 1.

---

## Ordre conseillé

1. `C2` et `C3` — **H** (sans H, pas de paiement possible)
2. `C1` — **droit au paiement**
3. `C4` et `C5` — **calcul du paiement**
4. `C6` — **score de performance**
5. `C7`, `C8` — mandats et demandes
6. `C9` — *plus tard*

---

## C1 — Avant de créer un paiement : le chasseur y a-t-il droit ?

**Codes** : `U01`, `R01`, `R02`, `R04`, `T17`, `U04`
**Tables lues** : `Payment`, `Sale`, `Mandate`
**Quand** : à la création d'un `Payment`
**Dépend de** : `D3` — **tranchée** par les sources officielles (voir
[`09-decisions-a-prendre.md`](09-decisions-a-prendre.md))

**Les vérifications, dans l'ordre** :

- [ ] **Le bon chasseur** (`U04`)
  - `Payment.id_hunter` = `Mandate.id_hunter` du mandat de la vente.
- [ ] **Mandat exclusif** (`U01`, `R01`)
  - si `Mandate.is_exclusive` → **payé**, même si
    `Sale.sale_origin = 'client_alone'` (le client a trouvé seul).
- [ ] **Mandat non exclusif** (`R02`)
  - payé **seulement si** `Sale.sale_origin = 'hunter'` ;
  - refus si `sale_origin = 'client_alone'`.
- [ ] **Dans les délais** (`R04`)
  - refus si `Sale.signature_date > ends_at` du mandat **en cours** ;
  - le mandat en cours = le **dernier de la chaîne** de renouvellements
    (celui dont `id_mandate_parent` pointe vers le précédent — `D8`) ;
  - source : `REGLES-CALCUL-REMUNERATION.md:98` (« sauf renouvellement du
    mandat ») et Gherkin officiel `10`, l. 45-50 (non renouvelé → 0,00 €).
  - ⚠ à préciser : si `Sale` pointe vers le **premier** mandat, le code doit
    chercher le mandat qui le renouvelle avant de comparer.

`T17` est la note qui résume tout ce bloc : « le droit à être payé croise
mandat et vente, pas de `CHECK` simple ».

---

## C2 — À la création d'une vente : calculer H

**Codes** : `B01`, `R05`, `T02`, `T04`
**Tables lues** : `Sale`, `ParametersFees`
**Quand** : à la création d'une `Sale`
**Dépend de** : `D1` (unité de H)

**Les étapes** :

- [ ] **Trouver les paramètres en vigueur** à la date de signature (`T02`)
  - `valid_from <= Sale.signature_date`
  - `AND (valid_until IS NULL OR Sale.signature_date <= valid_until)`
- [ ] **Exiger exactement une ligne** (`T04`)
  - l'`EXCLUDE` de `ParametersFees` garantit **au plus** une ;
  - le code doit garantir **au moins** une → erreur claire si aucune
    (trou dans les périodes).
- [ ] **Calculer H** (`B01`, `R05`)
  - `fees_amount = fixed_amount + rate × purchase_amount`
  - ⚠ l'unité (euros ou K€) dépend de `D1`.

---

## C3 — Ensuite, H ne change plus jamais

**Code** : `T02`
**Table** : `Sale`
**Quand** : à chaque modification d'une `Sale`

- [ ] Refuser toute modification de `fees_amount`.
  - trigger `BEFORE UPDATE`, ou refus dans le service.

---

## C4 — Calculer le paiement

**Codes** : `U12`, `B04`, `R19`, `B02`, `R06`, `T14` (+ `R20`)
**Tables lues** : `Payment`, `Sale`, `CommissionScale`, `Hunter`,
`HunterPerformance`
**Quand** : à la création d'un `Payment`, après `C1`
**Dépend de** : `D1` (unité de H), `D2` (acter les majorations)

**Étape 1 — choisir la tranche du barème** (`U12`, `B04`, `R19`, `R20`) :

- [ ] période en vigueur à la **date de l'acte** :
  - `valid_from <= Sale.signature_date`
  - `AND (valid_until IS NULL OR Sale.signature_date <= valid_until)`
- [ ] tranche qui contient le prix : `amount_min <= purchase_amount < amount_max`
  (`amount_max` vide = pas de plafond)
- [ ] **barème du chasseur d'abord** (`id_hunter` = le chasseur), **sinon
  barème par défaut** (`id_hunter IS NULL`) — `R20`
- [ ] exiger **au moins une** tranche (les `EXCLUDE` garantissent déjà
  **au plus** une) — `U12`
- [ ] vérifier que `Payment.id_commission_scale` pointe bien sur cette ligne
  (`B04`)

**Étape 2 — les taux** :

- [ ] `base_rate` = le `rate` de la tranche (`B04`)
- [ ] `seniority_rate` = 2 % par année complète depuis `Hunter.hire_date`,
  10 % au maximum (formule de `R22`)
- [ ] `performance_rate` = `(score − 50) / 50 × 0,20` (formule de `R23`)
- [ ] `final_rate` = `LEAST(0.60, GREATEST(0.20, round(base_rate × (1 + seniority_rate + performance_rate), 4)))`
  (formule de `R24` / `T13`)

**Étape 3 — le montant** (`B02`, `R06`, `T14`) :

- [ ] `amount = round(final_rate × <H en euros>, 2)` — au centime
- [ ] H se lit dans **`Sale.fees_amount`**, **jamais** dans
  `purchase_amount` (`R06` : le chasseur touche une part de H, pas du prix)
- [ ] ⚠ si H est en K€ (`D1`) : `<H en euros> = fees_amount × 1000`

> **Note** : les formules de `R22`, `R23` et `R24` sont aussi posées en
> `CHECK` dans le MPD (étape 3 du rapport). Le code doit **calculer** ces
> valeurs pour que ces `CHECK` passent.
>
> **À préciser** : quel score utiliser pour `performance_rate`. Le rapport
> ne le dit pas ; `R27` (« figés à la date de l'acte ») suggère le score en
> vigueur à `Sale.signature_date`.

---

## C5 — Ensuite, le paiement ne change plus jamais

**Code** : `R27`
**Table** : `Payment`
**Quand** : à chaque modification d'un `Payment`

- [ ] Refuser toute modification de ces **cinq colonnes** :
  - `base_rate`
  - `seniority_rate`
  - `performance_rate`
  - `final_rate`
  - `amount`
- trigger `BEFORE UPDATE`, ou refus dans le service.
- Le `status` (facture, programmé, payé…), lui, **doit** pouvoir changer.

---

## C6 — Score de performance

**Codes** : `U43`, `B12`, `B13` (+ calcul `R07` à `R12`)
**Tables lues** : `HunterPerformance`, `Mandate`, `Sale`, `Visit`, `Payment`
**Quand** : à chaque événement (paiement payé, mandat expiré)
**Dépend de** : `D9` (deux scores le même jour)

**Calculer le score** (`R07` à `R12`) — moyenne pondérée de 5 critères,
de 0 à 100 :

| critère | poids | règle | source |
|---|---|---|---|
| délai signature → acte (semaines, arrondi inférieur) | 25 % | ≤ 12 sem. : 100 … > 48 sem. : 0 | `R08` |
| exclusivité | 10 % | exclusif : 100, sinon 60 | `R09` |
| ventes sur 12 mois | 25 % | `min(100 ; ventes × 20)` | `R10` |
| mandats sur 12 mois | 15 % | `min(100 ; mandats × 10)` | `R11` |
| visites avant achat | 25 % | ≤ 3 : 100 … > 15 : 0 | `R12` |

Les paliers intermédiaires sont dans `NOTES-REMUNERATION-CHASSEUR.md:35-39`.
Paliers et poids sont des **paramètres**.

> ⚠ **À confirmer** (`R08`) : dans l'exemple officiel de Bruno, le délai
> (258 jours → 36 semaines) part de la **première** signature (14/11/2025),
> pas du renouvellement. Le délai remonterait donc au premier mandat de la
> chaîne `id_mandate_parent`.

**Les vérifications** :

- [ ] **Après un paiement** (`B12`) — cause `'payment'`
  - le paiement doit être au statut `'paid'` ;
  - le nouveau score doit être **≥** au score précédent.
- [ ] **Après un mandat expiré sans vente** (`U43`, `B13`) — cause
  `'mandate_expired'`
  - le nouveau score doit être **≤** au score précédent.
- [ ] Fermer la période du score précédent (`valid_until`) avant d'ouvrir
  la nouvelle (sinon l'`EXCLUDE` refuse).

---

## C7 — Renouveler un mandat

**Code** : `U07`
**Tables lues** : `Mandate`, `Sale`
**Quand** : à la création d'un mandat renouvelé
**Dépend de** : `D8` (sens de `'renewed'`)

- [ ] Refuser le renouvellement si le mandat d'origine a **au moins une
  vente** dans `Sale`.

---

## C8 — Réaffecter une demande refusée

**Code** : `U27`
**Table** : `SearchRequest`
**Quand** : à la réaffectation d'une demande
**Dépend de** : `D4` (statuts d'une demande)

- [ ] La demande doit aller à un **autre** chasseur que celui qui a refusé.
- ⚠ Aujourd'hui, **rien ne se souvient** du chasseur qui a refusé : il faut
  un historique des refus (colonne ou table), sinon la règle est impossible.

---

## C9 — *Plus tard* : offres sous le prix affiché

**Code** : `F06` (parcours futur IA)
**Tables** : `EstateProposed`, `Estate`

- [ ] `EstateProposed.amount_proposition < Estate.price`
  - deux tables → trigger ou API.

---

## Règles citées dans le texte du rapport (hors colonne « Coder »)

Elles ne sont pas marquées « Coder » dans les tableaux, mais le rapport dit
qu'une partie reste à programmer.

- **`U30` — calculer la date de fin du mandat**
  - `ends_at = signature_date + 6 mois`, calculé par l'API ou un trigger,
    jamais saisi à la main.
  - le `CHECK` de `U05` refuse une mauvaise valeur, mais ne la calcule pas.
- **`U02` — un mandat non exclusif sur un client déjà en exclusif**
  - l'`EXCLUDE` proposé ne compare que des mandats **exclusifs** entre eux ;
  - empêcher un mandat **non exclusif** de se poser sur un exclusif demande
    un trigger (ou l'API).
- **`R20` — barème nominatif d'abord** : intégré au bloc `C4`.
- **`R07` à `R12` — calcul du score** : intégré au bloc `C6`.

---

## En résumé

- **9 blocs** à programmer, qui regroupent **23 règles**.
- Le cœur, c'est l'argent : **calculer H** (`C2`), **vérifier le droit** du
  chasseur (`C1`), **calculer son paiement** (`C4`), puis **tout figer**
  (`C3`, `C5`).
- Une décision bloque encore le code : l'**unité de H** (`D1`, décidée le
  11/09 mais à reconfirmer). L'exemple de Bruno (`D3`) est réglé : pas de
  paiement après la fin du mandat, sauf renouvellement.

# Décisions à prendre en équipe

> **Extrait de** [`09-rapport-ecarts-contraintes.md`](09-rapport-ecarts-contraintes.md)
> (étape 2 + lignes « **Décider** » des tableaux du détail),
> **confronté au** « Journal de décisions (ADR) » sur Confluence
> (espace `GaSeBeLa1`, page n° `15466509`, 22 ADR, page modifiée le
> 2026-09-10).
>
> **Vérifié contre les sources officielles** du starter pack
> (`../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/`) pour `D1`, `D2`
> et `D3` : `Readme.md`, `documents utiles/REGLES-CALCUL-REMUNERATION.md`,
> `documents utiles/GLOSSAIRE-METIER.md`,
> `user-stories/10_calcul_remuneration_chasseur.feature`.
>
> **Date** : 2026-09-11.
>
> **Pourquoi ce fichier ?** Ces questions n'ont **pas de bonne réponse
> technique** : les notes se contredisent, ou ne disent rien. Il faut trancher
> **avant** d'écrire le MPD et le code.

---

## Comment l'utiliser

- Une décision = un bloc.
- Chaque bloc donne : la **question**, les **options**, **ce qui en dépend**.
- Remplir la ligne **« Décision retenue »** en réunion, avec la date.
- Une fois tranchée, **consigner la décision dans un nouvel ADR** sur
  Confluence (le prochain numéro libre est `ADR-023`).
- Les codes (`X02`, `U18`…) renvoient aux tableaux du rapport.

**Règle de lecture des sources** :

- seul un ADR au statut **« accepté »** compte comme tranché ; un ADR
  **« proposé »** n'est pas encore validé ;
- les notes d'équipe rédigées avec l'IA (`NOTES-REMUNERATION-CHASSEUR.md`,
  `BAREME-COMMISSION.md`…) **ne font pas foi** : on remonte toujours à la
  source officielle du starter pack.

---

## Les comptes

| quoi | nombre |
|---|---|
| ADR lus sur Confluence | 22 (16 acceptés, 6 proposés) |
| décisions du rapport | 12 (`D1` à `D12`) |
| → tranchées par un ADR accepté | **1** (`D8`) |
| → tranchées par les sources officielles | **1** (`D3`) |
| → décidées en réunion le 11/09/26 | **1** (`D1`, **à reconfirmer**) |
| → encore ouvertes, maintenant | **7** (`D2`, `D4`, `D5`, `D6`, `D7`, `D9`, `D10`) |
| → encore ouvertes, *plus tard* (parcours IA) | **2** (`D11`, `D12`) |
| nouvelles questions soulevées par les ADR | **2** (`N1` décidée le 11/09/26, `N2` ouverte) |
| noms à choisir (petites décisions) | 8 |
| lignes « Décider » dans les tableaux du rapport | 19 (18 codes distincts) |

---

## Tableau de bord — chaque décision face aux sources

| décision | sujet | source qui en parle | état |
|---|---|---|---|
| `D1` | unité de H | Gherkin officiel `10` (euros au centime) ; `ADR-019` ne dit rien de l'unité | **décidée** (B, 11/09/26) — ⚠ **à reconfirmer** |
| `D2` | ancienneté et performance | Gherkin officiel `10`, l. 201 (confirme B) | **ouverte** (à acter) |
| `D3` | acte signé après la fin du mandat | `REGLES-CALCUL-REMUNERATION.md:98`, Gherkin officiel `10`, l. 45-50 | **tranchée** (sources officielles) |
| `D4` | statuts d'une demande | aucun ADR | **ouverte** |
| `D5` | états d'une offre | aucun ADR | **ouverte** |
| `D6` | priorité du client | aucun ADR | **ouverte** |
| `D7` | mandat annulé et exclusivité | aucun ADR | **ouverte** |
| `D8` | sens de `'renewed'` | `ADR-010`, `ADR-013` (acceptés) | **tranchée** |
| `D9` | deux scores le même jour | aucun ADR | **ouverte** |
| `D10` | table rendez-vous | aucun ADR | **ouverte** |
| `D11` | pertinence (*plus tard*) | aucun ADR | **ouverte** |
| `D12` | types d'offre (*plus tard*) | aucun ADR | **ouverte** |
| `N1` | date de fin : stockée ou calculée ? | `ADR-004` (accepté) contredit le MPD et `ADR-018` (accepté) | **décidée** (A, 11/09/26) |
| `N2` | localisation : `SearchRequest` ou `Criteria` ? | `ADR-021` (proposé) le signale | **ouverte** |

---

## Par où commencer

**Déjà fait** : `N1` (réunion du 11/09), `D3` (sources officielles), `D8`
(ADR).

1. **`D1` — reconfirmer l'unité de H** : la décision B (K€) ne passe pas un
   exemple du Gherkin officiel (voir le bloc).
2. **`D7` — le mandat annulé** : il faut le savoir pour écrire l'exclusivité.
3. **`N2` — la localisation** : elle bloque les contraintes de `Criteria`.
4. **`D2`** : la source officielle confirme B, il suffit de l'acter.
5. Le reste peut suivre, dans l'ordre du fichier.

---

## Déjà tranché

### D8 — Que désigne le statut `'renewed'` ? → le **nouveau** mandat

**Code** : `U07`
**Tranché par** : les ADR (acceptés).

**Ce que disent les ADR** :

- **`ADR-010`** (19/08/2026) — « le nouveau mandat enregistre l'ID de
  l'ancien » via `id_mandate_parent`, vide pour un premier mandat.
- **`ADR-013`** (22/08/2026) — relation réflexive sur `Mandate` : chaque
  nouvelle version pointe vers celle qu'elle remplace.

**Conséquence** : le lien part du **nouveau** mandat vers l'**ancien**.
`chk_renewed` exige ce lien quand le statut vaut `'renewed'` : ce statut est
donc bien celui du **nouveau** mandat. C'est cohérent avec le MPD.

**Reste à faire** : rien de bloquant. Aucun ADR ne cite le mot `'renewed'`,
donc une phrase de confirmation en réunion suffit.

> **Attention** : `ADR-013` utilise aussi ce lien pour les **avenants**
> (modifications), pas seulement pour les renouvellements. Un mandat qui a un
> parent n'est donc pas forcément `'renewed'`. `chk_renewed` le permet déjà
> (il ne va que dans un sens).

---

### D3 — Un acte signé après la fin du mandat → **pas de paiement, sauf renouvellement**

**Code** : `R04`
**Tranché par** : les sources officielles du starter pack (pas par un ADR).

**D'où venait le « conflit »** :

- La note d'équipe `NOTES-REMUNERATION-CHASSEUR.md:22`, rédigée avec l'IA,
  résume la règle en « aucun droit » **et oublie l'exception**.
- Le document officiel dit : « aucun droit, **sauf renouvellement du
  mandat** » (`REGLES-CALCUL-REMUNERATION.md:98`).
- L'exemple de Bruno **n'a pas été inventé par l'IA** : il est recopié du
  document officiel (§ 10, l. 237) et du Gherkin officiel
  (`10_calcul_remuneration_chasseur.feature:255-265`).
- Ce même Gherkin contient, **avec les mêmes dates**, un scénario
  « mandat **non renouvelé** » : droit **fermé**, 0,00 € (l. 45-50).
- → Bruno est payé parce que son mandat est **renouvelé**. Sans
  renouvellement, il ne l'aurait pas été. Il n'y a donc **plus de
  contradiction**.

**Toutes les sources consultées** :

| source | ce qu'elle dit |
|---|---|
| `Readme.md:73` (énoncé) | le mandat vaut 6 mois, renouvelable |
| `Readme.md:135` (énoncé) | pas de paiement avant la fin des 6 mois → le chasseur est invité à renouveler |
| `GLOSSAIRE-METIER.md:14` | validité 6 mois, renouvelable |
| `REGLES-CALCUL-REMUNERATION.md:98` | acte après la fin : aucun droit, **sauf renouvellement** |
| `10_calcul_remuneration_chasseur.feature:45-50` | mandat **non renouvelé** + acte après la fin → **0,00 €** |
| `10_calcul_remuneration_chasseur.feature:255-265` | Bruno, mêmes dates, payé 6 231,60 € (renouvellement sous-entendu) |
| nos user stories `00:37-40` et `07:37-41` | fin = signature + 6 mois ; renouvellement à l'échéance si aucune vente |

**Aucune source** ne dit qu'on paie après la fin **sans** renouvellement.

**Règle retenue** :

- refus si `Sale.signature_date > ends_at` du mandat **en cours** ;
- le mandat en cours, c'est le **dernier de la chaîne** : celui qui
  renouvelle l'ancien via `id_mandate_parent` (`ADR-010`, `D8`).

**Reste à préciser (petits points)** :

- **Vers quel mandat pointe la vente ?**
  - si `Sale` pointe vers le mandat renouvelé → la comparaison est directe ;
  - si `Sale` pointe vers le premier mandat → le code doit chercher le mandat
    qui le renouvelle.
- **Le délai du score** : dans l'exemple, le délai de Bruno (258 jours) est
  compté depuis la **première** signature (14/11/2025), pas depuis le
  renouvellement. Si on garde cette lecture, le critère « délai » du score
  (`R08`) remonte au premier mandat de la chaîne. → à confirmer pour le
  bloc `C6`.
- ⚠ **Défaut dans le document officiel** : son code d'exemple
  (`REGLES-CALCUL-REMUNERATION.md:697`) fixe la fin du mandat de Bruno au
  2026-08-14, soit signature + **9 mois**. Ce n'est ni 6 mois, ni un
  renouvellement (qui donnerait le 2026-11-14). **À ne pas recopier.**

**À faire** : une phrase de confirmation en réunion, puis un ADR.

---

## Nouvelles questions soulevées par les ADR

### N1 — La date de fin du mandat : stockée ou calculée ?

**Codes touchés** : `U05`, `U06`, `U30`, `U42`, `R29`

**Le conflit** :

- **`ADR-004`** (accepté, 05/08/2026) a décidé :
  - d'ajouter `duration` (durée du mandat) et `renewal_count` (nombre de
    renouvellements) à `Mandate` ;
  - que la date de fin est « **non stockée en base de données car
    calculée** ».
- **Le MPD actuel** fait l'inverse :
  - il **stocke** `ends_at` ;
  - il n'a **ni** `duration`, **ni** `renewal_count` ;
  - le renouvellement passe par `id_mandate_parent` (`ADR-010`).
- **`ADR-018`** (accepté, 07/09/2026, **plus récent**) parle de la
  performance énergétique, mais s'appuie sur « le même principe que
  `mandate.ends_at` : figer la valeur constatée ». Il suppose donc que
  `ends_at` **est stocké**.
  - → **deux ADR acceptés se contredisent** (`ADR-004` et `ADR-018`).
- **Le rapport** propose un `CHECK` qui fixe `ends_at` à signature + 6 mois
  (`U05`). Ce `CHECK` n'a de sens que si `ends_at` existe.

**Les options** :

- **A — garder le MPD** (`ends_at` stocké) → écrire un ADR qui **remplace**
  `ADR-004`.
  - avantage : la date de fin est figée, comme le dit `ADR-018` (« figer la
    valeur constatée ») ;
  - `renewal_count` se retrouve en comptant la chaîne des `id_mandate_parent`.
- **B — appliquer `ADR-004`** (`duration` + calcul) → retirer `ends_at` du
  MPD et réécrire les contraintes `U05` et `U02` (l'exclusivité utilise
  `ends_at`).

**Ce qui en dépend** : la contrainte des 6 mois (`U05`), l'exclusivité
(`U02`), le droit au paiement dans les délais (`R04`), le calcul de la date
de fin (`U30`).

**Décision retenue** : Solution A : écrire un ADR qui remplace ADR-004  **Date** : 11/09/26

---

### N2 — La localisation d'une recherche : sur `SearchRequest` ou sur `Criteria` ?

**Codes touchés** : `L01` à `L12`

**Le conflit** — signalé par l'`ADR-021` lui-même, dans ses conséquences :

- un ADR plus ancien (`ADR-009`, accepté) place la localisation sur
  `SearchRequest`, par clés étrangères `id_town` / `id_area` ;
- le MPD v0.3 la met **aussi** sur `Criteria`, en texte (`town`,
  `postal_code`, `country_iso`) ;
- l'`ADR-021` écrit qu'il « ne tranche pas laquelle des deux approches
  remplace l'autre ».

**Les options** :

- **A — `Criteria`** (texte + `country_iso`) : c'est ce que vérifie le
  rapport (`L01` à `L12`).
- **B — `SearchRequest`** (clés vers des tables ville / secteur).
- **C — garder les deux**, en disant à quoi sert chacune.

**Ce qui en dépend** : toutes les contraintes de localisation de `Criteria`.

**Décision retenue** : ______________________ **Date** : ________

---

## Encore ouvert — à trancher maintenant

Aucun ADR ne traite ces décisions (vérifié sur les 22 ADR du journal).

### D1 — Unité de H (les honoraires)

**Codes** : `X02`, `T14`, `R14`, `R15`, `R16`, `R17`, `R18`

**La question** : dans quelle unité enregistre-t-on H ?

**Les options** :

- **A — euros au centime**
  - source : `NOTES-REMUNERATION-CHASSEUR.md:74`
  - attention : `NUMERIC(6,1)` s'arrête à 99 999,9 → **trop petit** en euros.
    Il faudra agrandir les types.
- **B — milliers d'euros (K€) à 0,1 près**
  - source : `schema-tracabilite-remuneration-chasseur_v4.md:16`
  - c'est ce que suit le MPD aujourd'hui.
  - attention : H est arrondi à 0,1 K€, soit **jusqu'à 50 € d'écart**, alors
    que `Payment.amount` est au centime. Il faut écrire une conversion
    (`fees_amount * 1000`).

**Ce qui en dépend** :

- `Sale.fees_amount` et `Sale.purchase_amount`
- `ParametersFees.fixed_amount` (doit suivre la même unité — `R28`)
- les bornes `amount_min` / `amount_max` de `CommissionScale` (tranches
  `R14` à `R18` : 200 000 €, 350 000 €, 500 000 €, 750 000 €)
- le calcul de `Payment.amount` (`T14`)

> `ADR-019` (proposé) confirme que H est calculé une fois à la signature
> puis figé, mais **ne dit rien de son unité**.

> ⚠ **Vérification du 11/09 contre la source officielle** — les deux
> sources des options A et B sont des notes d'équipe. Le Gherkin officiel
> (`10_calcul_remuneration_chasseur.feature`), lui, compte H **en euros au
> centime**, et **1 exemple sur 5** ne passe pas en K€ à 0,1 près :
>
> - prix 250 000 € → H = **9 250,00 €** (l. 76) ;
> - en K€ à 0,1 près, 9,25 devient **9,3**, soit 9 300 € → 50 € d'écart ;
> - le scénario d'arrondi (l. 267-272) attend **3 606,58 €** sur
>   9 250,00 € ; avec 9 300 €, on obtient **3 626,07 €** ;
> - la fonctionnalité se veut « déterministe et auditable » (l. 10).
>
> → La décision B ci-dessous est **à reconfirmer** en connaissance de cause.

**Décision retenue** : Solution B : ce n'est pas un logiciel de paye, doit rester indicatif **Date** : 11/09/26

---

### D2 — Ancienneté et performance : à quoi servent-elles ?

**Codes** : `X01` (2 lignes : `Payment` et `CommissionScale`)

**La question** : l'ancienneté et la performance du chasseur…

**Les options** :

- **A — choisissent le barème** (`BAREME-COMMISSION.md:31`)
- **B — majorent le taux** (`NOTES-REMUNERATION-CHASSEUR.md:58`)

**Ce qui en dépend** : rien à changer si on garde B.

- Le MPD suit **déjà B** : `seniority_rate` et `performance_rate` sur
  `Payment`, aucun niveau sur `CommissionScale`.
- **Source officielle** : le Gherkin
  `10_calcul_remuneration_chasseur.feature:201` écrit que le taux de base
  « est majoré par l'ancienneté et modulé par la performance » → **confirme
  B**.
- → **Il suffit de l'acter**, dans un ADR.

**Décision retenue** : ______________________ **Date** : ________

---

### D4 — Statuts d'une demande de recherche

**Codes** : `U18`, `U21`, `U26`, `U28`

**La question** : quelle liste de statuts pour une demande ?

**Ce que disent les user stories** :

- « confirmée » (`U18`)
- « acceptée » (`U28`)
- « non acceptée » (`U26`)
- « lancée » (`U21` — à la signature du mandat)

**Ce qui en dépend** :

- une **nouvelle colonne** sur `SearchRequest` (nom à choisir aussi) ;
- sa contrainte : `CHECK (<statut de la demande> IN (<…>))` ;
- la réaffectation d'une demande refusée (`U27`, à coder).

**Décision retenue** : ______________________ **Date** : ________

---

### D5 — États d'une offre d'achat

**Codes** : `U34` (maintenant), `F02` (*plus tard*)

**La question** : quels noms donner aux états qui manquent dans
`EstateProposed.proposition_status` ?

**Ce qui manque** :

- **maintenant** — « offre signée, pas encore envoyée » (`U34`).
  - `'proposed'` interdit le montant ;
  - `'offer_pending'` veut dire « déjà envoyée » (`U35`).
- ***plus tard*** — « bien choisi » et « bien écarté » (`F02`).
  - `'rejected'` ne convient pas : il exige un montant (c'est une réponse du
    vendeur, pas un choix du client).

**Ce qui en dépend** : la liste du `CHECK` sur `proposition_status`, et pour
`F02` la réécriture de `chk_offer`.

**Décision retenue** : ______________________ **Date** : ________

---

### D6 — Priorité du client

**Code** : `U32`

**La question** : quelle **échelle** pour la priorité que le client donne à
un bien de la sélection ?

**Exemples d'options** : 1 à 5 · haute / moyenne / basse · autre.

**Ce qui en dépend** : une **nouvelle colonne** sur `EstateProposed`, et son
`CHECK`.

**Décision retenue** : ______________________ **Date** : ________

---

### D7 — Un mandat annulé bloque-t-il encore le client ?

**Code** : `U02`

**La question** : un mandat **exclusif** au statut `'canceled'` empêche-t-il
encore un autre chasseur de prendre ce client, jusqu'à sa date de fin ?

**Les options** :

- **A — oui**, il bloque jusqu'à `ends_at`.
- **B — non**, l'annulation libère le client tout de suite.
  - il faut alors ajouter `AND status <> 'canceled'` dans le `WHERE` de
    l'exclusion.

**Ce qui en dépend** : la contrainte `EXCLUDE` d'exclusivité sur `Mandate`
(elle aussi touchée par `N1`).

**Décision retenue** : ______________________ **Date** : ________

---

### D9 — Deux scores de performance le même jour

**Code** : `B14`

**Le problème** : aujourd'hui, deux scores d'un même chasseur doivent être
séparés d'**au moins deux jours** (bornes `'[]'` + `valid_until > valid_from`).

**Les options** :

- **A — garder** tel quel (2 jours d'écart minimum).
- **B — `valid_until >= valid_from`** → l'écart tombe à 1 jour.
- **C — passer à une période avec l'heure** (`tsrange`) → plusieurs scores
  le même jour deviennent possibles.

**Ce qui en dépend** : `chk_perf_period` de `HunterPerformance`, et le calcul
du score (à coder).

**Décision retenue** : ______________________ **Date** : ________

---

### D10 — Faut-il une table « rendez-vous » ?

**Codes** : `U29`, `F04`

**La question** : les user stories parlent de rendez-vous, mais **aucune des
18 tables** ne les porte. Crée-t-on une table ?

**Ce qui en dépend** : une table de plus dans le MPD.

**Décision retenue** : ______________________ **Date** : ________

---

## Encore ouvert — plus tard (parcours futur IA)

Pas urgent : l'absence de ces règles n'est pas une erreur aujourd'hui.

### D11 — Échelle de pertinence

- **Code** : `F05`
- **Question** : quelle échelle pour classer les annonces par pertinence ?
- **Dépend** : une colonne sur `Estate_SearchRequest`.

**Décision retenue** : ______________________ **Date** : ________

### D12 — Types d'offre

- **Code** : `F07`
- **Question** : quels types d'offre (plus basse, au prix, …) ? La story
  laisse la liste **ouverte**.
- **Dépend** : `EstateProposed` (aujourd'hui un seul `amount_proposition`).

**Décision retenue** : ______________________ **Date** : ________

---

## Petites décisions — les noms à choisir

Le rapport écrit ces noms `<entre chevrons>` : **aucune source** ne les
donne, et aucun ADR non plus. Il suffit de se mettre d'accord.

| à nommer | table | code | nom retenu |
|---|---|---|---|
| compte activé (booléen) | `User` | `U19` | |
| statut de la demande | `SearchRequest` | `U18` | |
| priorité du client | `EstateProposed` | `U32` | |
| état « offre signée » | `EstateProposed` | `U34` | |
| table des médias d'un avis | nouvelle table | `U33` | |
| *plus tard* — chasseur IA (booléen) | `Hunter` | `F03` | |
| *plus tard* — pertinence | `Estate_SearchRequest` | `F05` | |
| *plus tard* — états « choisi » / « écarté » | `EstateProposed` | `F02` | |

---

## À savoir — ADR « proposés » qui touchent le rapport

Ils ne tranchent **aucune** des décisions ci-dessus, mais ils règlent des
points des étapes 1 et 3 du rapport. Ils restent à **valider** (statut
« proposé »).

| ADR | ce qu'il règle | lien avec le rapport |
|---|---|---|
| `ADR-019` | pas de clé entre `Sale` et `ParametersFees` ; H figé ; `btree_gist` requis | confirme `T02`, `T04` et la vérification `btree_gist` (étape 1) |
| `ADR-021` | contraintes de localisation de `Criteria`, avec leurs noms `ck_criteria_*` | donne les **nouveaux noms** des deux contraintes à renommer (`L04`, étape 3) ; ajoute `ck_criteria_town_needs_country` (`L03`) |
| `ADR-022` | six contraintes `ck_client_*` sur `Client` | confirme que `K01` à `K06` vont sur `Client` ; les copies de `K01` à `K04` posées par erreur sur `Criteria` sont à retirer ou déplacer |

---

## En résumé

- **L'exemple de Bruno n'est plus un problème** (`D3`) : la note IA avait
  oublié « sauf renouvellement ». Sans renouvellement, un acte après la fin
  du mandat ne rapporte rien.
- **L'unité de H (`D1`) est à revoir** : le choix du K€ ne retombe pas sur un
  exemple officiel (9 250 € devient 9 300 €).
- Il reste **7 décisions** à prendre maintenant, plus la localisation
  (`N2`).

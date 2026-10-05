# Questions à trancher — état au 2026-10-02

Ce document **centralise** toutes les questions ouvertes du projet.
Chacune porte sa **source**, **qui tranche**, les **options**, et une
**recommandation argumentée**.

- 🎯 **Point de départ** : la calculette de rémunération (`API/src/app/services/remuneration.py`)
  a besoin de champs que la base n'a pas, ou qu'elle range autrement.
- 📚 **Sources lues** : le schéma `docker/init-v2/01` et `02`, les modèles de
  l'API, les `.feature`, `md/`, `livrables/`, `context AI/08-etat.md`, et le
  sujet (`StarterPack - BASE`, en lecture seule).
- ⚠️ Les numéros de ligne viennent de lectures faites le 2026-10-02. Ils
  bougent si le fichier change.

---

## Mode d'emploi

### Qui tranche

| Repère | Qui | Pour quoi |
|---|---|---|
| 👥 **Groupe** | l'équipe, en réunion, tracé dans un ADR | technique, modélisation, choix internes |
| 🧑‍💼 **Jeff** | le client (formateur qui joue le commanditaire) | le métier, les chiffres, les droits |
| 📋 **PO** | le product owner | priorités, périmètre, découpage |
| 🎓 **Prof** | le formateur en tant qu'évaluateur | attendus de la soutenance |

- ⚠️ **Aucun PO n'est nommé**, ni dans le sujet, ni dans le dépôt (voir **Q-PRO-01**).
- ✅ Jeff joue le client : `md/adr-026-perimetre-authentification.md:22`.
  Le sujet le confirme : « le formateur jouant le commanditaire »
  (`NOTE-DE-CADRAGE.md:70`).

### Les statuts

- 🟡 **Ouvert** : personne n'a tranché.
- 🟠 **Position ou hypothèse à valider** : quelqu'un a proposé, ou la migration a supposé ; le groupe n'a pas acté.
- 🔵 **Appliqué, pas acté** : le code ou le schéma le fait déjà, sans ADR accepté.
- 💡 **Ma recommandation** : mon avis, argumenté. **Pas une règle.**

### Les chiffres sont des paramètres

- ✅ Le sujet le dit lui-même : « Confondre les deux, c'est présenter en
  soutenance des chiffres inventés comme des exigences client »
  (`REGLES-CALCUL-REMUNERATION.md:40`).
- ➡️ 3 000 €, 2,5 %, les tranches, les poids, les bornes : **propositions**
  du sujet, à faire valider par Jeff.

### Hors périmètre — pas de question dessus

- ❌ **L'authentification** : Jeff, le 2026-09-22, « vous ne gérez pas l'auth,
  c'est géré au dessus » (`md/adr-026-perimetre-authentification.md`).
  Le RGPD reste exigé.
- ❌ **L'acte notarié** : annoncé le 2026-10-02 (qui l'a décidé n'est pas noté).
  Pas de question sur le notaire, la collecte des honoraires, ni les pièces de l'acte.
  - ⚠️ **Nuance** : la **date** et le **prix** de l'acte restent des **entrées**
    du calcul. Ils arrivent comme données de la vente (`sale`).

### Abréviations

- `01` = `docker/init-v2/01_create_fil_rouge_immobilier.sql`
- `02` = `docker/init-v2/02_migration.sql`
- `rem.py` = `API/src/app/services/remuneration.py`
- `F00`, `F07`, `F10` = `user-stories/00_…`, `07_…`, `10_….feature`
- `RCR` = `REGLES-CALCUL-REMUNERATION.md` du sujet
- `09-dec` = `livrables/2-modelisation/09-decisions-a-prendre.md`

---

## 0. Déjà tranché — ne pas reposer

| Sujet | Décision | Date | Source |
|---|---|---|---|
| Unité monétaire | ✅ **euro**, `NUMERIC(12,2)` | 2026-09-21 | `context AI/08-etat.md:98-104` |
| Acte après la fin du mandat | ✅ **refusé, sauf renouvellement** | 2026-09-11 | `09-dec:122-178` |
| Mandat renouvelé | ✅ `'renewed'` marque le **nouveau** mandat | — | `09-dec:96-118`, `01:423` |
| Fin de mandat | ✅ `ends_at` **stocké** | 2026-09-11 | `09-dec:222` |
| Chaque chasseur a un manager | ✅ ADR-025, **accepté sur Confluence** | 2026-09-22 | `md/a-faire-a-la-main-2026-09-21.md:189-190` |
| Authentification | ❌ hors périmètre (Jeff) | 2026-09-22 | `md/adr-026-…:62-80` |
| Base de test | ✅ `fil_rouge_test`, isolée | 2026-10-02 | `08-etat.md:171-178` |
| Calculette | ✅ code du sujet, repris tel quel | 2026-10-02 | `08-etat.md:179-190` |
| Prix des biens | ✅ colonne `price_eur`, ligne à ligne | 2026-09-21 | `08-etat.md:110-113` |
| Ancien schéma `docker/init/` | ✅ obsolète, `init-v2` fait foi | 2026-09-21 | `08-etat.md:105-109` |

### Réponses de Sébastien — 2026-10-02 (page à cartes, v1 puis v2)

⚠️ Avis d'**un** membre : **à reprendre avec l'équipe lundi** pour les cartes 👥,
puis à confirmer par Jeff quand la carte le dit.

| Id | Réponse | Ce que ça entraîne |
|---|---|---|
| D1 à D4 | ✅ **garder** | Rien à défaire. |
| Q-REM-01 | 📝 pas d'option cochée : « définir la borne, informer Jeff, citer exactement la contradiction ; et changer le decimal(12,2) en numeric(12) » | Contradiction citée sur la carte (`REGLES-CALCUL-REMUNERATION.md` l. 173-174, 181, 188) ; nouvelle **Q-JEF-19**. ✅ **Décision du 2026-10-05** (le « numeric(12) » était une erreur de formulation) : les **prix** passent en **euros entiers**, type **`INTEGER`** (pas `DECIMAL`) — jusqu'à 2 147 483 647, « The type `integer` is the common choice » ([doc PostgreSQL 16](https://www.postgresql.org/docs/16/datatype-numeric.html), lue le 2026-10-05) ; la calculette, en `Decimal`, convertit avec `Decimal(prix)` (exact) ; les `EXCLUDE` du barème passent de `'[)'` à `'[]'` (`01:706`, `01:713`). Tranches `[0 ; 199 999]`, `[200 000 ; 349 999]`… : ni trou ni chevauchement, comme le tableau du sujet et `rem.py:241`. L'adaptateur de D3 devient inutile. 🟡 Colonnes « prix » à confirmer : `sale.purchase_amount` (`01:650`), `estate.price` (`01:515`), `amount_proposition` (`01:605`), `amount_min/max` (`01:691-692`). Honoraires, fixe et paiement **gardent leurs centimes** (`F10:253`). À mettre à jour : règle 4 de `CLAUDE.md`, `docker/init-v2/README.md` §1. |
| Q-REM-02 | ✅ **statut-mandat** (pas l'option recommandée) | Nouveau statut de fin sur `mandate` ; peut servir aussi à **Q-REM-14**. ⚠️ S'écarte de `RCR:100` (motif du refus dans `paiements`) : à écrire dans l'ADR. |
| Q-REM-03 | ✅ **colonne** — « à documenter et à confirmer avec Jeff » | `payment.performance_score`. |
| Q-REM-04 | ✅ **jsonb** | `payment.calculation_details JSONB`. |
| Q-REM-05 | ✅ **table** | Table `remuneration_parameters` + CHECK `01:754-755` relâchés. |
| Q-REM-06 | ✅ **recalcul** | Code du sujet intact ; écart à `F10:293` dans l'ADR ; Q-JEF-17. |
| Q-REM-07 | ✅ **client-tous** — remarque : moins de visites = meilleure note | Remarque **juste** (`RCR:55`, `RCR:147`) : mon argument « gonfle la note » était faux, corrigé en v3 (aussi Q-ACC-13). Q-JEF-08. |
| Q-REM-08 | ✅ **non-refusees** | Q-JEF-09. |
| Q-REM-09 | ✅ **signes-sans-renouv** | Q-JEF-09 ; mandats annulés à demander. |
| Q-REM-10 | ✅ **oui** | `final_rate` dans `chk_refused`. |
| Q-REM-11 | ✅ **api** | Test d'intégration montant = taux × honoraires. |
| Q-REM-12 | ✅ **c3** | C3 codée dans `sale_service`. |

**Lot de migration qui en découle** (un seul `docker compose down -v`) :
nouveau statut de `mandate` (Q-REM-02), `payment.performance_score` (Q-REM-03),
`payment.calculation_details` (Q-REM-04), table `remuneration_parameters` et
CHECK relâchés (Q-REM-05), `final_rate` dans `chk_refused` (Q-REM-10).

---

## 1. Toutes les questions, par thème

### A. Rémunération — champs absents ou ambigus en base

C'est le cœur de la demande. La calculette lit une `Vente`
(`rem.py:128-140`) et rend une `Remuneration` (`rem.py:143-159`).
Voici ce qui ne colle pas avec la base.

#### Q-REM-01 — Borne haute d'une tranche du barème : incluse ou exclue ?

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** :
  - la base **exclut** la borne haute : `numrange(amount_min, amount_max, '[)')` (`01:706`, `01:713`) ;
  - le code l'**inclut** : `prix <= l.montant_max` (`rem.py:241`) ;
  - `F10:23-27` et `parametrage_par_defaut` écrivent des bornes incluses :
    `LigneBareme(debut, d(0), d("0.30"), d(199999))` (`rem.py:304`) ;
  - ⚠️ **le sujet se contredit** : « < 200 000 € » (`RCR:173`, borne exclue),
    mais `BETWEEN montant_min AND …` en SQL (`RCR:188`, borne incluse).
- ❌ **Risque** :
  - stocké `199999` en base : un prix de **199 999,50 €** ne tombe dans **aucune** tranche ;
  - stocké `200000` et lu tel quel par le code : **deux** tranches pour 200 000 €.
- **Options** :
  - A — garder `'[)'` en base, stocker `200000`, et **convertir à la lecture** :
    `montant_max = amount_max − 0,01` dans la couche qui lit la base ;
  - B — changer le code (`<` au lieu de `<=`, `rem.py:241`) ;
  - C — passer la base en `'[]'` et stocker `199999,99`.
- 💡 **Recommandation : A.**
  - **Zéro ligne** changée dans `rem.py`, qui reste le code du sujet.
  - La conversion est exacte : les prix sont en `NUMERIC(12,2)`, au centime.
  - `'[)'` couvre **tous** les centimes, sans trou ni chevauchement ; `EXCLUDE` le garantit.
  - ❌ B **casse un test** : `test_remuneration.py:193` attend `("199999", "30")`,
    et 199 999 € ne trouverait plus de tranche (`BaremeIntrouvable`).
  - ➡️ Ajouter un test aux bornes : 199 999,99 € et 200 000,00 €.

#### Q-REM-02 — Origine « un chasseur d'une autre agence » : où la ranger ?

- 🟡 **Ouvert** · 👥 **Groupe**, après 🧑‍💼 **Jeff** (Q-JEF-03)
- **Constat** :
  - le code a **3** origines, dont `AUTRE_AGENCE` (`rem.py:54-57`) ;
  - la base n'en a que **2** : `'hunter'`, `'client_alone'` (`01:653-654`) ;
  - et `sale.fees_amount` est `NOT NULL CHECK (> 0)` (`01:652`).
- ➡️ Si l'entreprise **ne touche rien** sur une vente faite par une autre
  agence, on ne peut **pas** enregistrer cette vente : il n'y a pas
  d'honoraires à saisir.
- ⚠️ Même problème pour un mandat **non exclusif** où le **client trouve seul**
  (`'client_alone'`) : l'entreprise touche-t-elle des honoraires ?
- **Options** :
  - A — ajouter `'other_agency'` au `CHECK`, et accepter des honoraires à **0** quand l'entreprise ne touche rien
    (passer `sale.fees_amount CHECK (> 0)` à `>= 0`, `01:652`) ;
  - B — ne pas créer de `sale` : le mandat passe à un statut de fin (ex. `'lost'`, à ajouter) ;
  - C — ne rien stocker.
- 💡 **Recommandation : A**, la forme exacte dépend de Q-JEF-03.
  - Le refus doit être **tracé** sur `payment` (ADR-024, `refusal_reason = 'out_of_scope'`).
    Le sujet insiste sur « l'intérêt de stocker le motif » (`RCR:100`).
  - Or un `payment` exige une vente : `id_sale NOT NULL` (`01:756`).
  - ❌ B rangerait deux refus que le code traite pareil (`rem.py:174`) de deux façons différentes.

#### Q-REM-03 — Le score de performance doit-il être figé sur le paiement ?

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** :
  - `F10:275-287` exige de **figer** les éléments du calcul à la date de l'acte ;
  - `payment` fige les taux (`01:742-755`) mais **pas le score** ;
  - `hunter_performance.score` (`01:798`) est un score **par période**,
    recalculé **après** paiement : ce n'est pas celui qui a servi.
- **Options** :
  - A — ajouter `payment.performance_score NUMERIC(4,1)`, `NULL` si refus ;
  - B — une clé vers `hunter_performance` ;
  - C — ne rien ajouter, et le recalculer à partir de `performance_rate`.
- 💡 **Recommandation : A.**
  - Une colonne, coût nul ; la règle `F10:287` est respectée à la lettre.
  - Le sujet le liste lui-même dans `paiements` : « prix_acte, honoraires, score_performance » (`RCR:286`).
  - C ne marche que si les paramètres n'ont pas changé : c'est justement ce qu'on veut éviter.
  - B pointe vers le score **d'après**, pas celui du calcul.

#### Q-REM-04 — Faut-il figer les 5 notes et les entrées du calcul ?

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** : absents en base :
  - les **5 notes** (délai, exclusivité, ventes, mandats, visites) ;
  - les **entrées** : `nb_visites`, `annees_anciennete`, `ventes_12_mois`, `mandats_12_mois` (`rem.py:137-140`).
- ➡️ Sans elles, un paiement **ne se rejoue pas** : les visites ou les ventes
  peuvent changer après coup.
- **Options** :
  - A — une colonne `payment.calculation_details JSONB` ;
  - B — une colonne par valeur (9 colonnes) ;
  - C — rien, on redérive.
- 💡 **Recommandation : A.**
  - Le sujet : « On stocke donc **tous les termes du calcul** » (`RCR:292`).
  - Une seule colonne, lisible en soutenance.
  - B alourdit la table pour des valeurs qu'on ne requête jamais.

#### Q-REM-05 — Les paramètres de performance et de modulation : en table ou en code ?

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** :
  - **aucune table** pour les poids, les paliers, les notes, les points, la
    fenêtre de 12 mois (`rem.py:92-105`) ;
  - ni pour le taux par année, le pivot, l'amplitude, le plancher, le plafond (`rem.py:108-116`) ;
  - deux de ces valeurs sont **gravées dans des `CHECK`** :
    - `seniority_rate BETWEEN 0 AND 0.10` (`01:754`) ;
    - `performance_rate BETWEEN -0.20 AND 0.20` (`01:755`).
- ✅ Le sujet dit qu'un paramètre vit dans « une table de paramètres, jamais en dur »
  (`RCR:42-47`).
- **Options** :
  - A — une table versionnée `remuneration_parameters` (`valid_from`, `valid_until`, scalaires + `JSONB` pour les paliers) ;
  - B — garder les valeurs dans le code (`parametrage_par_defaut`, `rem.py:296`) ;
  - C — B, mais **relâcher** les deux `CHECK` à des bornes larges.
- 💡 **Recommandation : A, et relâcher les `CHECK` dans tous les cas** (voir aussi Q-REM-19).
  - Un `CHECK` à 0,10 interdit à Jeff de changer le plafond sans migration.
  - A suit la lettre du sujet ; sans elle, un score passé ne se rejoue pas.
  - Si le temps manque : C, et le dire en soutenance comme une limite connue.

#### Q-REM-06 — Le score : recalculé à chaque vente, ou lu dans `hunter_performance` ?

- 🟠 **Position à valider** (Sébastien : « le score de cette vente ») · 👥 **Groupe**, à confirmer par 🧑‍💼 **Jeff** (Q-JEF-17)
- **Constat** :
  - `F10:293` : « Le nouveau score sert de base au calcul de la prochaine rémunération » ;
  - le code **recalcule** le score avec les données de la vente (`rem.py:275-276`), sans lire de score stocké ;
  - `md/point-etape-2026-09-21.md` Q2 : « le score de cette vente » ;
  - `09-contraintes-a-coder.md:163-165` penche plutôt pour un score **stocké**.
- **Options** :
  - A — recalculer à chaque vente (le code) ; `hunter_performance` = **historique** ;
  - B — lire le dernier score de `hunter_performance`.
- 💡 **Recommandation : A.**
  - Le score dépend de la vente elle-même (délai, exclusivité, visites) :
    un score lu ailleurs ne peut pas le refléter.
  - Le code du sujet fait A ; les 55 cas sont écrits pour A.
  - ⚠️ C'est un **écart assumé** : `F10:293` dit le contraire, et deux textes du sujet se contredisent.
    Le dire dans l'ADR, et le faire confirmer par Jeff.

#### Q-REM-07 — Quelles visites comptent ?

- 🟡 **Ouvert** · 🧑‍💼 **Jeff** (Q-JEF-08), le groupe écrit la requête
- **Constat** :
  - `visit.visitor_type IN ('hunter', 'client')` (`01:631`) ;
  - `F10:259` : « le client a effectué 5 visites » ;
  - le sujet cite les deux sortes de visites (`Readme.md:100-101`).
- **Questions** : quel type ? tous les biens du mandat, ou seulement le bien vendu ? avant l'acte seulement ?
- 💡 **Recommandation** : visites `'client'`, **tous les biens** du mandat, datées **au plus tard** le jour de l'acte.
  - C'est la lecture littérale de `F10:259`.
  - Tous les biens : le critère mesure le travail du chasseur, pas le bien final.

#### Q-REM-08 — Quelles ventes comptent dans « ventes sur 12 mois » ?

- 🟡 **Ouvert** · 🧑‍💼 **Jeff** (Q-JEF-09)
- **Constat** : `RCR:470` exclut la vente en cours ; rien d'autre n'est dit.
- **Questions** : une vente refusée compte-t-elle ? une vente `client_alone` ?
- 💡 **Recommandation** : les ventes des mandats du chasseur dont le paiement
  **n'est pas refusé**, dans les 12 mois **avant** l'acte, vente en cours exclue.
  - « Ventes réussies » (`Readme.md:86`) = celles qui lui ouvrent un droit.

#### Q-REM-09 — Quels mandats comptent dans « mandats sur 12 mois » ?

- 🟡 **Ouvert** · 🧑‍💼 **Jeff** (Q-JEF-09)
- **Constat** : `F10:298` compte un mandat expiré. Rien sur `canceled`, `pending_signature`, `renewed`.
- 💡 **Recommandation** : les mandats **signés** (`signature_date` non vide)
  dans la fenêtre, **sans les renouvellements** (`id_mandate_parent IS NULL`).
  - Sinon un mandat renouvelé 3 fois compte 4 fois.
  - 🟡 Le mandat **annulé** : pas de recommandation. Le compter pousse à
    signer puis annuler pour gagner des points (`mandats × 10`, `rem.py:214`). Jeff tranche.

#### Q-REM-10 — `final_rate` doit-il être obligatoire sur un paiement non refusé ?

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** : `chk_refused` exige `base_rate`, `seniority_rate`,
  `performance_rate` non vides, mais **pas** `final_rate` (`01:778-783`).
  - `payment_model.py:11-12` dit « NULL tant qu'il n'est pas arrêté », sans règle derrière.
- 💡 **Recommandation : l'ajouter à `chk_refused`.**
  - Le premier statut est `'announced'` : le montant est déjà annoncé, donc le taux est connu.
  - Il n'existe aucun état « calculé mais pas arrêté ».

#### Q-REM-11 — Qui garantit `montant = taux × honoraires` ?

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** : rien ne vérifie `amount`, `final_rate` ni `fees_amount`
  entre eux. L'arrondi « au demi supérieur » n'existe que dans le code.
- **Options** : trigger, colonne générée, ou API seule.
- 💡 **Recommandation : l'API seule**, avec un test d'intégration.
  - La formule a un plancher, un plafond et un arrondi : un trigger la dupliquerait.
  - Une seule source de vérité : `rem.py`, déjà testé sur 55 cas.

#### Q-REM-12 — Les honoraires sont rangés sur `sale`, qu'on peut modifier

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** : `sale.fees_amount` (`01:652`) reste modifiable après paiement (`PUT /sales/{id}`).
- ✅ **Déjà prévu** : la contrainte C3 dit « Refuser toute modification de `fees_amount` »
  (`09-contraintes-a-coder.md:110-117`), par trigger ou dans le service.
- ⚠️ Le sujet range les honoraires **sur le paiement** : « prix_acte, honoraires » (`RCR:286`).
- 💡 **Recommandation : appliquer C3**, ou copier `honoraires` sur `payment` en même temps que le score (Q-REM-03).
  - La copie suit le sujet à la lettre, et rend le paiement autonome.

#### Q-REM-13 — Lien vers la ligne de `parameters_fees` utilisée ?

- 🔵 **Appliqué, pas acté** : pas de clé, choix d'ADR-019 (« proposé »)
- **Constat** : `parameters_fees.id` n'est référencé nulle part.
- 💡 **Recommandation : garder sans clé**, et accepter ADR-019.
  - Le montant est déjà figé dans `sale.fees_amount`.
  - La ligne se retrouve par la date : `EXCLUDE` (`01:681-682`) garantit qu'il y en a **au plus une** (voir Q-SCH-17 pour les trous).

#### Q-REM-14 — Le mandat « perdant » de deux mandats non exclusifs

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** : `F10:52-56` : un seul chasseur est payé ; « "Bruno" ne perçoit aucune rémunération » (`F10:56`).
  - `sale.id_mandate` est `UNIQUE` (`01:655`) : le perdant n'a **pas** de vente.
- 💡 **Recommandation** : le mandat perdant prend un **statut de fin** (à ajouter, ex. `'lost'`).
  - Les statuts actuels sont `active`, `completed`, `expired`, `renewed`, `canceled`, `pending_signature` (`01:401-403`) :
    aucun ne dit « vendu par un autre ».

#### Q-REM-15 — Date de début du barème par défaut

- 🟠 **Position à valider** (Sébastien : « reculer à 2025 ») · 👥 **Groupe**
- **Constat** : `rem.py:298` : `debut = date(2026, 1, 1)`.
  - Une vente du seed datée de 2025 lèverait `BaremeIntrouvable`.
- 💡 **Recommandation : reculer, dans le seed seulement.**
  - Le code du sujet reste intact ; les 55 cas aussi.

#### Q-REM-16 — Ancienneté : quelle date d'entrée ?

- 🟠 **Hypothèse de migration** · 🧑‍💼 **Jeff** (Q-JEF-10)
- **Constat** : `hire_date` = date de création du compte (`02:24-26`).
  - Le sujet : « Dépend de la date d'entrée du chasseur, donnée RH » (`RCR:762`).
- 💡 **Recommandation** : garder l'hypothèse, la dire en soutenance, et demander à Jeff si une vraie date existe.

#### Q-REM-17 — Statuts du paiement : quelles dates garder ?

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** : `F07:10-34` décrit 5 étapes. La base n'a que `created_at` et `paid_at` (`01:730`).
  - Absents : date d'annonce, facture (fichier, numéro), date de vérification, date programmée.
- **Options** :
  - A — une colonne de date par étape, plus `invoice_reference` ;
  - B — une table d'historique des statuts ;
  - C — rien.
- 💡 **Recommandation : A.**
  - 4 colonnes suffisent : `announced_at`, `invoice_submitted_at`, `verified_at`, `scheduled_for`.
  - B est plus propre, mais plus lourd pour un besoin de démo.
  - ⚠️ La date où l'entreprise **reçoit** les honoraires (`F07:12`) touche le circuit notarial : **hors périmètre**.

#### Q-REM-18 — Ancienneté et performance : clé du barème, ou majoration du taux ? (X01)

- 🔵 **Appliqué, pas acté** · 👥 **Groupe**
- **Constat** :
  - le schéma et le code **majorent le taux** (option B) : `payment.seniority_rate`, `performance_rate` (`01:754-755`) ;
  - `F10:201` le confirme ;
  - `09-dec:303-324` : « Il suffit de l'acter, dans un ADR. »
- 💡 **Recommandation : acter B dans un ADR, maintenant.**
  - ⚠️ Plusieurs documents disent que X01 **bloque** le branchement de la calculette
    (`08-etat.md:190`, `API/README.md:147`, `rapport-tests.md:250`). C'est trop fort : la décision est faite de fait.

#### Q-REM-19 — Borner le taux final entre 20 et 60 % en base (R21) ?

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** : `01:743-750` propose `CHECK (final_rate BETWEEN 0.20 AND 0.60)`.
  `01:131` range R21 parmi les décisions ouvertes.
- 💡 **Recommandation : ne pas activer R21.**
  - Le **bornage** est une règle (`F10:201` ; `01:749-750` : « la règle de bornage, elle, est bien métier »).
  - Mais **20 % et 60 %** sont des **paramètres** proposés (`F10:3-5`) : ils ne vont pas dans un `CHECK`.
  - Les graver dans un `CHECK` refait l'erreur relevée en Q-REM-05.
  - Le code borne déjà le taux (`rem.py:264`).

### B. Rémunération — les paramètres (valeurs de Jeff)

Toutes ces valeurs sont des **propositions du sujet** (`RCR:59`, `F10:3-5`).
Le code les porte déjà dans `parametrage_par_defaut`.

💡 **Recommandation commune** : les présenter à Jeff **en une fois**, adopter
les valeurs du sujet par défaut, et noter dans un ADR « paramètres proposés,
validés par Jeff le … ». Elles sont toutes listées en **partie 2**.

| Id | Question | Proposé par le sujet | Source |
|---|---|---|---|
| Q-PAR-01 | Honoraires : fixe et pourcentage | 3 000 € + 2,5 % | `RCR:321` (D1) |
| Q-PAR-02 | Non exclusif, client trouve seul : rien, ou indemnité ? | rien, motif tracé | `RCR:322` (D2), `RCR:100` |
| Q-PAR-03 | Barème par palier ou progressif ? | palier | `RCR:323` (D3) — ⚠️ voir plus bas |
| Q-PAR-04 | Fenêtre des critères de volume | 12 mois glissants | `RCR:324` (D4) |
| Q-PAR-05 | Ventes et mandats séparés, ou taux de transformation ? | séparés | `RCR:325` (D5) |
| Q-PAR-06 | Poids des 5 critères | 25 / 10 / 25 / 15 / 25 | `RCR:326` (D6) |
| Q-PAR-07 | Effet de l'ancienneté et de la performance | +10 % max, ±20 % | `RCR:327` (D7) |
| Q-PAR-08 | Garder le plancher de 20 %, qui ne mord jamais ? | oui | `RCR:328` (D8) |
| Q-PAR-09 | Qui crée un barème propre à un chasseur ? | à définir | `RCR:329` (D9) |
| Q-PAR-10 | Bornes et taux des tranches | 30 / 35 / 40 / 45 / 50 % | `RCR:171-177` |
| Q-PAR-11 | Arrondi du score (1 déc.) et du taux (4 déc.) | demi supérieur | `RCR:223-229` |
| Q-PAR-13 | Grilles de notes (délai, visites, exclusivité 100/60) | `F10:107-138` | `RCR:143-147` |

**Règles fixées par le sujet — à confirmer, pas à choisir** :

- ✅ **Montant arrondi au centime, au demi supérieur** : c'est une `Règle:` de
  `F10:253` (« arrondi au centime au demi supérieur »). `01:721` dit aussi « règle officielle ».
- ✅ **Honoraires HT** : `RCR:131` l'affirme, sans la mention « (paramètre) ».
  Ce n'est pas une proposition ; une simple confirmation suffit.
- ⚠️ **Palier** : le sujet **se contredit**.
  - `F10:166` en fait une `Règle:` : « sans progressivité entre tranches » ;
    `RCR:179` parle de « lecture littérale de la règle » ;
  - mais `RCR:323` le pose en décision D3.
  - ➡️ Ne demander à Jeff qu'une **confirmation**.

Arguments pour les points qui méritent plus qu'un « oui » :

- **Q-PAR-03 palier** : 💡 garder.
  - Les 55 cas de `F10` sont écrits pour un barème par palier : changer casse les tests.
  - ⚠️ Effet de seuil d'environ **600 €** à 350 000 € (`RCR:181`) : à montrer à Jeff.
- **Q-PAR-05** : 💡 garder séparés, **mais** voir Q-JEF-05.
  - Le taux de transformation (ventes ÷ mandats) est **un moyen** de faire
    **baisser** le score quand un mandat expire sans vente.
  - D'autres existent : une pénalité par mandat échu, ou ne compter que les mandats transformés.
- **Q-PAR-08 plancher** : 💡 garder.
  - Il ne coûte rien et protège si la grille baisse un jour (`RCR:215`).
- **Q-PAR-09 barème nominatif** : 💡 réservé au manager, à écrire dans le RACI.
- **Q-PAR-11 arrondi** : 💡 adopter tel quel : le code le fait déjà (`rem.py:40`, `rem.py:264`).

### C. Mandat — durée, exclusivité, renouvellement

#### Q-MAN-01 — Activer la règle « exactement 6 mois » (U05)

- 🟡 **Ouvert** (SQL prêt, commenté) · 👥 **Groupe**
- **Constat** : le `CHECK` actuel n'impose que l'ordre des dates (`01:409-410`).
  Un mandat « peut durer 10 ans ou 1 jour » (`01:431-443`).
- 💡 **Recommandation : activer.**
  - « 6 mois renouvelable » est une **règle** du sujet, pas un paramètre (`RCR:57`).
  - ⚠️ Cas de fin de mois : 31/08 + 6 mois. PostgreSQL rend le **28 ou 29/02**.
    À écrire dans l'ADR, pour que l'API calcule pareil.

#### Q-MAN-02 — Activer l'exclusivité (U02) — et le cas du mandat annulé (D7)

- 🟡 **Ouvert** · 👥 **Groupe** pour le trigger, 🧑‍💼 **Jeff** pour D7 (Q-JEF-06)
- **Constat** : trigger écrit et commenté (`01:446-496`). D7 :
  « un mandat 'canceled' libère-t-il le client tout de suite ? » (`01:463-465`).
- ❌ **Piège** : tel qu'écrit, le trigger **bloquerait le renouvellement** d'un mandat exclusif.
  - Les plages se comparent en `'[]'` (`01:483-484`), et rien n'exclut le mandat parent (`01:477-485`).
  - Un renouvellement signé à l'échéance (`F00:40`) touche la date de fin du parent : il serait refusé.
- 💡 **Recommandation : corriger, puis activer, avec D7 = B** (l'annulation libère tout de suite).
  - D'abord exclure le parent : `m.id IS DISTINCT FROM NEW.id_mandate_parent`, ou les mandats déjà finis.
  - ⚠️ Pas `m.id <> NEW.id_mandate_parent` : sans parent, cela vaut `NULL`, et le trigger ne bloquerait **plus rien**.
  - Le brouillon du trigger fait déjà B (`status <> 'canceled'`).
  - Bloquer un client sur un mandat annulé n'a pas de sens métier évident ; Jeff confirme.

#### Q-MAN-03 — Renouvellement : combien de fois, et seulement sans vente ?

- 🟡 **Ouvert** · 🧑‍💼 **Jeff** (Q-JEF-07), puis 👥 **Groupe**
- **Constat** :
  - « renouvelable si aucune vente n'a abouti » (`F00:40`) : rien ne l'impose en base (U07) ;
  - le nombre de renouvellements n'est dit nulle part ;
  - la grille du délai va jusqu'à « >48 sem. » (`RCR:143`) : elle suppose plusieurs renouvellements.
- 💡 **Recommandation** :
  - imposer « sans vente » dans `mandate_service` (pas en SQL : la règle croise deux tables) ;
  - pas de limite au nombre, tant que Jeff n'en donne pas.

#### Q-MAN-04 — Après un renouvellement : quel mandat la vente vise, et d'où part le délai ?

- 🟠 **Position à valider** (Sébastien) · 👥 **Groupe**
- **Constat** : `md/point-etape-2026-09-21.md` Q5 : « La vente pointe vers le nouveau mandat ».
  Le délai (R08) part de la **première** signature (`09-contraintes-a-coder.md:207-210`).
- 💡 **Recommandation : valider les deux.**
  - Le nouveau mandat est le seul valide à la date de l'acte.
  - Le délai depuis la 1re signature est la seule lecture compatible avec la grille « >48 sem. ».
  - ➡️ Le code devra **remonter la chaîne** `id_mandate_parent` pour trouver la 1re date.

#### Q-MAN-05 — `is_client_signed` : doublon de `signature_date` ?

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** : aucune règle n'utilise la colonne. `02:218` insère un mandat
  avec une date de signature **et** `is_client_signed = false`.
- 💡 **Recommandation** : la supprimer, ou poser `CHECK (is_client_signed = (signature_date IS NOT NULL))`.
  - Deux colonnes qui disent la même chose finissent par se contredire : `02:218` le montre déjà.

#### Q-MAN-06 — Règles qui croisent plusieurs tables (non imposées)

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat**, trois TODO dans `01` :
  - une visite peut précéder la signature du mandat (`01:635-637`) ;
  - une vente peut tomber hors de la validité du mandat, ou sur un mandat non signé (`01:660-664`) ;
  - « on peut aujourd'hui payer un chasseur qui n'est PAS celui du mandat » (`01:785-792`) ;
  - un paiement peut viser un barème **pas en vigueur** à la date de l'acte (`01:787-788`),
    ou le barème **propre à un autre chasseur**.
- 💡 **Recommandation : toutes dans l'API**, chacune avec un test d'intégration.
  - Les deux dernières sont les plus graves : c'est de l'argent versé à tort.

#### Q-MAN-07 — Annuler un mandat jamais signé : impossible

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** : `chk_status_signature` exige une date de signature dès que le
  statut n'est plus `pending_signature` (`01:426-428`).
  - ➡️ Un mandat en attente ne peut pas passer à `canceled` sans une date **inventée**.
- 💡 **Recommandation** : autoriser `canceled` **sans** date de signature dans ce `CHECK`.
  - Un client qui renonce avant de signer est un cas normal.

#### Q-MAN-08 — Réaffecter une demande refusée par un chasseur (U27)

- 🟡 **Ouvert** · 👥 **Groupe**
- **Constat** : « rien ne se souvient du chasseur qui a refusé : il faut un
  historique des refus (colonne ou table) » (`09-contraintes-a-coder.md:237-246`).
- 💡 **Recommandation** : une petite table `search_request_refusal` (demande, chasseur, date).
  - Sinon la demande peut être réaffectée au chasseur qui l'a déjà refusée.

### D. Schéma — autres questions

| Id | Question | Statut | Qui | Source |
|---|---|---|---|---|
| Q-SCH-01 | Valider l'assouplissement de `ck_client_address_all_or_nothing` | 🟠 | 👥 | `08-etat.md:114-117`, `02:64-66` |
| Q-SCH-02 | N2 : la localisation sur `search_request` ou `criteria` ? | 🟡 | 👥 | `01:294-296`, `09-dec:226-248` |
| Q-SCH-03 | D4 : statuts d'une demande de recherche | 🔵 | 👥 | `09-dec:328-347`, `01:283-285` |
| Q-SCH-04 | D5 : état manquant d'une offre (« signée, pas envoyée ») | 🟡 | 👥 | `09-dec:351-370` |
| Q-SCH-05 | D6 : échelle de priorité du client | 🟡 | 🧑‍💼 | `01:620-623`, ADR-027 Q9 (`md/adr-027-…:144`) |
| Q-SCH-06 | D9 : deux scores le même jour | 🟡 | 👥 | `01:814-816`, `09-dec:411-428` |
| Q-SCH-07 | D10 : table des rendez-vous (`U29`, `F04`) | 🟡 | 👥 | `09-dec:432-441` |
| Q-SCH-08 | D11, D12 : pertinence (`F05`), types d'offre (`F07`) | 🟡 | 📋 | `09-dec:449-464` |
| Q-SCH-09 | `created_at` absent de 4 tables | 🟡 | 👥 | `01:165-166` |
| Q-SCH-10 | Renommer `is_cartet` en `is_carte_t` | 🟡 | 👥 | `01:253-256` |
| Q-SCH-11 | Code postal non contrôlé sur `estate` | 🟡 | 👥 | `01:559-561` |
| Q-SCH-12 | Eircode avec espace | 🟠 | 👥 | `01:56-58` |
| Q-SCH-13 | Libellé du 2e lien « Manages » | 🟠 | 👥 | `docker/init-v2/README.md:427-431` |
| Q-SCH-14 | Pas d'historique des changements de manager | 🔵 | 👥 | `docker/init-v2/README.md:475-477` |
| Q-SCH-15 | Taux de tranche `>= 0` contre taux de base `> 0` | 🟡 | 👥 | `01:693`, `01:742` |
| Q-SCH-16 | `parameters_fees` sans `valid_until > valid_from` | 🟡 | 👥 | `01:676` |
| Q-SCH-17 | Trous entre deux périodes de paramètres | 🟡 | 👥 | `09-contraintes-a-coder.md` C2 |

💡 **Recommandations** :

- **Q-SCH-01** : **valider**, et déplacer l'`ALTER` dans `01`.
  - Sinon 18 clients perdent leur ville.
- **Q-SCH-02** : garder **`criteria`**, mais **écrire un ADR qui remplace ADR-009**.
  - ⚠️ ADR-009 est **accepté** et place la localisation sur `search_request` (`01:294`).
  - Un ADR accepté fait foi (`09-dec:34-35`) : le schéma actuel le contredit.
  - `criteria` est versionné : la localisation change avec les critères.
- **Q-SCH-03** : **acter** les 4 statuts déjà en base.
- **Q-SCH-04** : ajouter **`'signed'`** ; reporter `F02` au parcours IA.
- **Q-SCH-05** : **1 à 5** (`SMALLINT`), si Jeff n'a pas d'avis.
  - Le brouillon existe, et un nombre se trie.
- **Q-SCH-06** : ⚠️ passer en `'[)'` **ne suffit pas**.
  - Avec `valid_until > valid_from`, deux scores le même jour restent impossibles.
  - Seule l'option C de `09-dec:422` (`tsrange`) le permet.
  - 💡 **C** si on veut un score par paiement ; sinon **garder** : au moins un jour d'écart entre deux scores.
- **Q-SCH-07** : **ne pas créer**.
  - Aucune règle de calcul ne s'en sert ; le dire comme hors MVP.
- **Q-SCH-08** : reporter au parcours IA, comme prévu.
- **Q-SCH-09** : **ajouter** la colonne : un oubli coûte plus qu'une colonne.
- **Q-SCH-10** : **renommer maintenant**, tant que l'API n'a pas d'autre client.
- **Q-SCH-11** : **volontaire**, à dire.
  - Les annonces sont importées telles quelles.
- **Q-SCH-12** : **valider** : c'est le format affiché.
- **Q-SCH-13** : **« Supervises »**, et l'écrire.
  - Le choix serait fait, mais n'est noté nulle part (`md/a-faire-a-la-main-2026-09-21.md:213-221`).
- **Q-SCH-14** : **accepter** comme limite connue.
- **Q-SCH-15** : deux options.
  - A — resserrer la tranche à `> 0` ;
  - B — assouplir `payment.base_rate` à `>= 0`, dans l'esprit de Q-REM-05.
  - 💡 **A** : avec le plancher, une tranche à 0 % paierait quand même 20 % (`rem.py:264`). Un taux 0 n'a donc pas de sens.
- **Q-SCH-16** : **ajouter**, comme sur `commission_scale` (`01:701`).
- **Q-SCH-17** : contrôle **dans l'API**, à l'écriture.
  - La base garantit « au plus une » ligne, pas « exactement une ».

### E. Migration — hypothèses à confirmer

| Id | Hypothèse | Qui | Source |
|---|---|---|---|
| Q-MIG-01 | Sens de `taux_commission` (2,00 à 3,25) | 🧑‍💼 | `docker/init-v2/README.md:145-147` |
| Q-MIG-02 | `hire_date` = date de création du compte | 🧑‍💼 | `02:24-26` |
| Q-MIG-03 | `search_request.status = 'confirmed'` | 👥 | `docker/init-v2/README.md:161-174` |
| Q-MIG-04 | Manager fictif (user 25) | 👥 | `docker/init-v2/README.md:176-192` |
| Q-MIG-05 | `energetic_score` retiré | 👥 | `08-etat.md:118-121` |
| Q-MIG-06 | Remplir `energy_class` depuis `dpe` | 👥 | `docker/init-v2/README.md:90-91` |
| Q-MIG-07 | Téléphones `0000000000` (3 clients + le manager) | 👥 | `02:143-145` |
| Q-MIG-08 | Secteurs non migrés : `criteria.town` vide 17 fois sur 17 | 👥 | `02:70-72` |
| Q-MIG-09 | `budget_min = budget_max` 17 fois sur 17 | 👥 | `md/point-etape-2026-09-21.md` §7 |
| Q-MIG-10 | 6 mandats « actif » déjà échus au 25/07/2026 | 🧑‍💼 | `md/point-etape-2026-09-21.md:240-243` |
| Q-MIG-11 | Mot de passe fictif au préfixe bcrypt `$2b$` | 👥 | `02:97-127` |
| Q-MIG-12 | Mandat 13 ignoré : son client est un chasseur | 🧑‍💼 | `02:167` |
| Q-MIG-13 | Sens des statuts source `suspendu`, `termine` | 🧑‍💼 | `PgSQL.sql:26` du sujet |

💡 **Recommandations** :

- **Q-MIG-01** : le lire comme un **% d'honoraires**, non migré.
  - 3,25 % du prix donnerait plus que les honoraires (`RCR`, anomalie A2).
  - ⚠️ Le README du schéma l'attribue au **groupe**. Je le mets chez Jeff : c'est le sens d'une donnée du client.
- **Q-MIG-02** : voir Q-REM-16.
- **Q-MIG-03** : **`'launched'`** quand un mandat existe.
  - L'`UPDATE` est prêt, et c'est plus juste.
- **Q-MIG-04** : le remplacer dans le seed, **puis le supprimer**.
- **Q-MIG-05** : **acter** : la colonne était vide partout.
- **Q-MIG-06** : **oui**, dans `03` : donnée gratuite.
- **Q-MIG-07** : **garder**, et le signaler à l'audit.
  - La colonne est `NOT NULL` (`01:180`, `01:224`) ; le seed les remplace.
- **Q-MIG-08** : **migrer** les secteurs.
  - Sinon aucun critère n'a de lieu.
- **Q-MIG-09** : **garder**, et le signaler à l'audit.
  - On n'invente pas un minimum.
- **Q-MIG-10** : garder comme **constat d'audit** ; demander à Jeff s'ils ont été renouvelés.
- **Q-MIG-11** : sans importance (auth hors périmètre) ; le dire dans le seed.
- **Q-MIG-12** : demander si le vrai client est **Nina Girard** (user 19).
  - Même ville, même budget, et elle n'a aucun mandat.
- **Q-MIG-13** : demander ; d'ici là, `termine` → `completed`, sans preuve de vente.

### F. Rôles et droits d'accès

L'authentification est hors périmètre. Les **droits**, eux, restent un
livrable de conception (ADR-027, matrice). Ces questions décident **qui
fait quoi** dans le métier.

| Id | Question | Qui | 💡 Recommandation |
|---|---|---|---|
| Q-ACC-01 | Reposer à Jeff la question des **droits** | 🧑‍💼 | **Oui**, en une question nette (Q-JEF-14) |
| Q-ACC-02 | Que voit le manager ? | 🧑‍💼 | Ses chasseurs et leurs paiements |
| Q-ACC-03 | Qui enregistre la vente ? | 🧑‍💼 | Le manager |
| Q-ACC-04 | Qui fait avancer la facture dans ses états ? | 🧑‍💼 | Le chasseur dépose, le manager vérifie |
| Q-ACC-05 | Le client voit-il tout le catalogue ? | 🧑‍💼 | Non : les biens proposés pour lui |
| Q-ACC-06 | Le chasseur voit-il son barème ? | 🧑‍💼 | Oui : sa paie doit se comprendre |
| Q-ACC-07 | Qui fixe barèmes et honoraires ? | 🧑‍💼 | La direction seule |
| Q-ACC-08 | Désactiver plutôt que supprimer ? | 👥 | **Oui** : les clés en `RESTRICT` y poussent déjà |
| Q-ACC-09 | Quel compte lance l'import des biens ? | 👥 | Un compte technique dédié |
| Q-ACC-10 | Qui affecte une demande à un chasseur ? | 🧑‍💼 | Le manager |
| Q-ACC-11 | Où ranger la facture du chasseur ? | 👥 | Avec Q-REM-17 (`invoice_reference`) |
| Q-ACC-12 | Qui crée le compte client ? | 🧑‍💼 | Le client, par sa demande en ligne |
| Q-ACC-13 | Qui enregistre une visite du client ? | 🧑‍💼 | Le chasseur qui l'accompagne |
| Q-ACC-14 | Droits des chasseurs-IA ? | 📋 | Reporter au parcours IA |
| Q-ACC-15 | Un chasseur peut-il créer une demande ? | 🧑‍💼 | Non : la demande vient du client |
| Q-ACC-16 | Combien de comptes Admin / Manager dans le seed ? | 👥 | **1 admin, 2 managers** |
| Q-ACC-17 | Mot de passe : 12 caractères minimum ? | 👥 | **Garder 12** : déjà codé et testé |
| Q-ACC-18 | Garder `user.password` ? | 👥 | **Garder** : prêt si l'auth revient |
| Q-ACC-19 | Clé d'API proposée par Jeff, « optionnelle » | 👥 | **Ne pas faire** ; la citer comme piste |
| Q-ACC-20 | Réécrire ADR-025 sans ENF-03 | 👥 | **Oui** : ENF-03 n'est qu'un exemple |
| Q-ACC-21 | Durée de conservation avant anonymisation | 🧑‍💼 | Voir plus bas |

Sources :

- Q-ACC-01 : le 22/09, la question des droits était mêlée à l'auth (`md/adr-026-perimetre-authentification.md:116-120`).
- Q-ACC-02 à 09 : les questions 1 à 8 d'ADR-027 (`md/adr-027-…:136-144`). La n°9 est Q-SCH-05.
- Q-ACC-10 à 15 : la matrice, §6 (`md/matrice-droits-crud-par-role.md:225-239`).
  - ⚠️ La matrice a **15** questions, ADR-027 en a **9** : elles se recouvrent en partie seulement.
  - La priorité et le choix du client (matrice n°14) : voir Q-SCH-05.
- Q-ACC-16 : `md/securite…:365-367`. Q-ACC-17 : `API/src/app/models/user_model.py:59-61`.
- Q-ACC-18, 19, 20 : `md/adr-026-perimetre-authentification.md`, lignes 121-123, 92-94, 105-109.
- **Q-ACC-21** : le sujet donne déjà « **10 ans (obligation comptable)** » pour les paiements
  (`REGISTRE-RGPD.md:29`). Pour le reste : « Durée du mandat + X ans » (`REGISTRE-RGPD.md:27`).
  - 💡 Reprendre les 10 ans pour les paiements, et demander à Jeff la valeur de X.

### G. Infrastructure, tests, process

| Id | Question | Qui | Source |
|---|---|---|---|
| Q-INF-01 | Remplacer MinIO (image introuvable) | 👥 | `md/minio-images-indisponibles-2026-10-02.md:58-71` |
| Q-INF-02 | Écrire le seed `04_seed_demo.sql` | 👥 | `md/point-etape-2026-09-21.md:197` |
| Q-INF-03 | Biens de démo : 3 à 5 biens fictifs à Montpellier ? | 👥 | `md/point-etape-2026-09-21.md:160-169` |
| Q-INF-04 | Aucun test fonctionnel | 👥 | `rapport-tests.md:245-257` |
| Q-INF-05 | 15 ressources sur 18 sans test d'intégration | 👥 | `rapport-tests.md:253` |
| Q-INF-06 | Champ obligatoire manquant → `409`, pas `422` | 👥 | `API/README.md:216-218` |
| Q-INF-07 | Générateur de données en masse (phase 3) | 👥 | `md/point-etape-2026-09-21.md:199` |
| Q-INF-08 | ENF-01 (500 mandats en moins de 2 s) et ENF-03 non testés | 👥 | `rapport-tests.md:254-255` |
| Q-PRO-01 | **Qui est le PO ?** | 👥 | — |
| Q-PRO-02 | Valider les 5 réponses du point d'étape (A1) | 👥 | `md/point-etape-2026-09-21.md:106-108` |
| Q-PRO-03 | ADR à passer en « accepté », ou à écrire | 👥 | `md/a-faire-a-la-main-2026-09-21.md:96-112`, `09-dec:178` |
| Q-PRO-04 | Argon2 : ADR-016 ou ADR-017 ? | 👥 | `md/adr-024-motif-refus-remuneration.md:7-10` |
| Q-PRO-05 | Dire à Békanty que le CDC v2.0 audite l'**ancien** schéma | 👥 | `md/a-faire-a-la-main-2026-09-21.md:66-79` |
| Q-PRO-06 | Nettoyer Confluence (note drawio, compagnon d'ADR-024) | 👥 | `md/a-faire-a-la-main-2026-09-21.md:192-204` |
| Q-PRO-07 | Livrables 1 (audit) et 3 (architecture) vides | 📋 | `08-etat.md` |
| Q-PRO-08 | Format des téléphones entre tables | 👥 | `md/notes_contraintes_client.md:34-36` |

💡 **Recommandations** :

- **Q-INF-01** : d'abord décider **s'il faut** un stockage objet.
  - Rien ne lit d'images aujourd'hui.
  - Sinon, retirer le service, avec l'accord du responsable de `docker-compose.yml`.
- **Q-INF-02** : après Q-REM-15, Q-REM-06, Q-PAR-02, Q-MAN-04 et Q-INF-03.
- **Q-INF-03** : **oui**.
  - Les 2 556 biens sont hors de Montpellier, et plafonnent à 406 042 €.
- **Q-INF-04** : le sujet les exige ; commencer par le **parcours de paiement**.
- **Q-INF-05** : priorité à `payment`, `sale`, `mandate`.
- **Q-INF-06** : ajouter des modèles d'entrée Pydantic, comme pour `/users`.
- **Q-INF-07** : quand le seed est stable.
- **Q-INF-08** : ENF-01 se mesure avec le générateur (Q-INF-07) ; ENF-03 tombe avec l'auth (ADR-026).
- **Q-PRO-01** : **en nommer un**.
  - Il tranche les questions « groupe » et tient le journal d'ADR.
- **Q-PRO-02** : une réunion de 30 min : ces réponses bloquent le seed.
- **Q-PRO-03** : tout passer **en une séance**.
  - À accepter : 016, 017, 019 à 024, 026, 027.
  - À écrire : l'ADR de la décision D3 (`09-dec:178`), et celui de X01 (Q-REM-18).
  - Un ADR proposé ne fait pas foi (`09-dec:34-38`).
- **Q-PRO-04** : le **journal Confluence** fait foi ; corriger le CDC.
- **Q-PRO-05** : **oui**, vite : il qualifie de « bloquant » ce qui existe.
- **Q-PRO-06** : **oui** : le journal a « un trou » à la place d'ADR-024.
- **Q-PRO-07** : planifier ; l'audit a déjà sa matière (constats de migration).
- **Q-PRO-08** : reporter ; un ADR à part si le temps le permet.

---

## 2. Questions que seul Jeff peut trancher

À lui envoyer **en une fois**, avec la proposition du sujet en face : il
n'a plus qu'à dire « oui » ou à corriger.

### Les chiffres

- **Q-JEF-01** — Valide-t-il les **paramètres proposés** par le sujet ?
  Fixe 3 000 € + 2,5 %, tranches 30 à 50 %, poids 25/10/25/15/25,
  ancienneté +2 %/an plafonnée à +10 %, performance ±20 %, taux final entre 20 et 60 %.
  (Q-PAR-01, 04, 06, 07, 08, 10, 13)
- **Q-JEF-02** — Confirme-t-il le barème **par palier** (le taux de la tranche
  s'applique à tout) ? `F10:166` en fait une règle, `RCR:323` une décision.
  ⚠️ Le palier crée un saut d'environ 600 € à 350 000 €. (Q-PAR-03)
- **Q-JEF-03** — Mandat **non exclusif**, le client ou une autre agence vend :
  le chasseur touche-t-il **rien**, ou une indemnité ? Et l'entreprise
  touche-t-elle des honoraires dans ce cas ? (Q-PAR-02, Q-REM-02)
- **Q-JEF-04** — Confirme-t-il des honoraires **HT** ? Le sujet l'affirme (`RCR:131`).

### La performance

- **Q-JEF-05** — Le sujet dit que le score est « recalculé **à la baisse** »
  quand un mandat expire sans vente (`Readme.md:135`, `F10:295-300`).
  Avec les critères proposés, un mandat de plus **ne fait jamais baisser** le score.
  Veut-il une vraie baisse ? Si oui, **un moyen** : le taux de transformation
  (ventes ÷ mandats) ; un autre : une pénalité par mandat échu. (Q-PAR-05)
- **Q-JEF-08** — Quelles **visites** comptent : celles du client, du
  chasseur, ou les deux ? Sur tous les biens du mandat ? (Q-REM-07)
- **Q-JEF-09** — Quelles **ventes** et quels **mandats** comptent sur 12 mois ?
  Une vente refusée ? Un mandat annulé (risque : signer puis annuler pour gagner des points) ?
  Un renouvellement ? (Q-REM-08, Q-REM-09)
- **Q-JEF-17** — Le score sert-il **tel que calculé à chaque vente** (le code du sujet),
  ou le **dernier score stocké** (« Le nouveau score sert de base au calcul de la
  prochaine rémunération », `F10:293`) ? Les deux textes du sujet se contredisent. (Q-REM-06)
- **Q-JEF-10** — Existe-t-il une vraie **date d'entrée** des chasseurs (donnée RH) ? (Q-REM-16)

### Le mandat

- **Q-JEF-06** — Un mandat **exclusif annulé** libère-t-il le client tout de suite ? (Q-MAN-02)
- **Q-JEF-07** — Un mandat se renouvelle **combien de fois** ? Le délai
  compte-t-il depuis la **première** signature ? (Q-MAN-03, Q-MAN-04)
- **Q-JEF-11** — **Simple confirmation** : l'exemple « Bruno » donne un mandat
  de **9 mois** (`RCR:697`). Le groupe le lit comme un mandat **renouvelé**
  (`09-dec:136-140`). Est-ce bien ça ?

### Les données reprises

- **Q-JEF-12** — `taux_commission` (2,00 à 3,25) : pourcentage du **prix** ou des **honoraires** ? (Q-MIG-01)
- **Q-JEF-13** — Le mandat 13 vise un chasseur comme client : le vrai client est-il **Nina Girard** ?
  Que veulent dire `suspendu` et `termine` ? Les 6 mandats « actif » échus ont-ils été renouvelés ? (Q-MIG-10, 12, 13)

### Les droits et le RGPD

- **Q-JEF-14** — Le 22/09, il a tranché l'**authentification**. Mais **qui
  peut faire quoi** reste ouvert : que voit le manager, qui enregistre la vente,
  qui valide la facture, le chasseur voit-il son barème ?
  (Q-ACC-02 à 07, Q-ACC-10, 12, 13, 15)
- **Q-JEF-15** — Combien de temps garder les données avant **anonymisation** ?
  Le sujet donne 10 ans pour les paiements ; il manque le reste. (Q-ACC-21)
- **Q-JEF-18** — Quelle **échelle de priorité** pour le client sur un bien proposé ? (Q-SCH-05)
- **Q-JEF-16** — Qui peut créer un **barème propre à un chasseur**, et qui le valide ? (Q-PAR-09)
- **Q-JEF-19** — Un prix **pile sur une limite** du barème (200 000 €, 350 000 €…) : quel
  taux ? Le sujet écrit « < 200 000 € » (l. 173) mais aussi `BETWEEN` (l. 188), qui
  inclut la limite. Proposé : la limite appartient à la tranche du dessus
  (350 000 € → 40 %, comme l. 181). (Q-REM-01, ajoutée le 2026-10-02)

---

## 3. Ce qui ne va pas — erreurs, défauts, critiques

### ❌ Défauts dans le code et le schéma

- ⚠️ **`mandate_model.py:23`** : `ends_at: date` est déclaré **obligatoire**,
  alors que la base le veut **vide** pour un mandat `pending_signature` (`01:409`, `01:426-428`).
  - ✅ **Mesuré le 2026-10-02**, sur `fil_rouge_test`, transaction annulée :
    `POST /mandates` sans `ends_at` → **`201`**, `GET` → **`200`**, `ends_at: null`.
  - ➡️ **Pas de bug** : les modèles de table ne valident pas l'entrée (`API/README.md:216-218`).
  - Défaut **de documentation** seulement : l'annotation ment, et la doc Swagger peut afficher le champ comme obligatoire.
    Passer à `Optional[date] = None`.
- **`sale_model.py`** et **`payment_model.py`** ne déclarent pas `unique=True`
  sur `id_mandate` et `id_sale`, alors que la base le fait (`01:655`, `01:756`).
- **`sale_model.py:7-8`** : dit qu'une vente `client_alone` est « hors mandat ».
  Faux : `id_mandate` est `NOT NULL`.
- **`created_at`** : les modèles produisent une date **avec** fuseau ; la
  colonne est `TIMESTAMP` **sans** fuseau. La valeur stockée peut être décalée.
- **Paramètres gravés dans des `CHECK`** (`01:754-755`) : contraire à « jamais en dur » (`RCR:42-47`).
- **`amount_max` contrôlé deux fois** (`01:692` et `01:698-699`).
- **Commentaires périmés** :
  - `01:900` dit que `02` et `03` visent « l'ANCIEN schéma en K€ » ;
  - `02:189` parle encore de « K€ (colonne cible NUMERIC(6,1)) » ;
  - `02:235-236` dit que les clés de `client` et `hunter` sont `id_user` ;
  - `02:29` renvoie au « README point 5 » au lieu de §3.5.

### ⚠️ Incohérences entre documents

- **« D2 » veut dire deux choses** dans le même fichier :
  - `01:130` et `01:752` : D2 = ancienneté (numérotation du groupe) ;
  - `01:722` : D2 = « R = 0 » (numérotation du sujet, `RCR:322`).
  - ➡️ Le groupe et le sujet numérotent tous deux de **D1 à D9**. Il faut un préfixe.
- **D10 mal étiqueté** : `01:626` l'attribue aux visites ; c'est la table des rendez-vous (`09-dec:432-441`).
- **D9 décrit deux fois différemment** : `01:814-816` dit « un jour d'écart », `09-dec:413-422` dit « deux jours ».
- **D3 brouillé** : `01:665-668` dit qu'un acte tardif « peut ouvrir droit » ; la décision est « refus sauf renouvellement ».
- **D1 pas mis à jour** : `09-dec:299` dit encore « Solution B » (K€), avec sa justification « doit rester indicatif », abandonnée.
- **ADR-025** : « accepté » sur Confluence, « proposé » dans le dépôt (`md/adr-025-…:17`, `08-etat.md:152`).
- **Numéro d'ADR de la localisation** : ADR-010 dans `md/notes_contraintes_localisation_criteria.md:90`,
  ADR-009 dans `01:131` et `01:294`.
- **Comptes faux dans `08-etat.md` lui-même** : « 224 colonnes » (`08-etat.md:20`, `:133`)
  contre « 226 colonnes » (`08-etat.md:158`, et `01:891`).
- **`rapport-tests.md:253`** : « 17 des 18 ressources » à tester, alors que 3 le sont : il en reste **15**.
- **X01 présenté comme bloquant** (`08-etat.md:190`, `API/README.md:147`) : voir Q-REM-18.
- **`CLAUDE.md` et `08-etat.md`** disent que trois livrables sont vides : `4-application` contient le rapport de tests.
- **`docker/init-v2/README.md:6-7`** : « Il ne remplace rien » — alors qu'il est monté.
- **Erreur annoncée pour un paiement sans taux** : `500` selon `md/adr-024-modifications-a-faire.md:196-198`,
  `409` selon `API/README.md:213`.

### ⚠️ Défauts du sujet lui-même

- **Exemple de Bruno** : un mandat de 9 mois (`RCR:697`), alors que la règle dit 6.
  ⚠️ Notre test `test_remuneration.py:81` reprend `date(2026, 8, 14)` : c'est voulu (cas du sujet), mais à dire.
- **« Recalculé à la baisse »** : aucun critère proposé ne le permet (Q-JEF-05).
- **`PLAN-DE-TESTS.md:34`** : le test T01 applique le taux au **prix** (300 k€ × 2,5 % = 7 500 €).
  Le sujet dit pourtant : « Le taux s'applique aux honoraires `H`, jamais au prix `P` » (`RCR:169`).
- **`PLAN-DE-TESTS.md:35`** : T02 parle de « commande » et de « stock » : reste d'un autre projet.
- **« Notamment »** : la performance est « Calculée notamment sur » 5 critères (`GLOSSAIRE-METIER.md:37`) ;
  le sujet impose « exactement cinq » (`RCR:55`).
- **Borne des tranches** : « < 200 000 € » (`RCR:173`) contre `BETWEEN` en SQL (`RCR:188`). Voir Q-REM-01.
- **Palier** : `Règle:` dans `F10:166`, mais décision D3 dans `RCR:323`.
- **Score** : `F10:293` lit un score stocké ; le code du sujet le recalcule (`rem.py:275-276`). Voir Q-JEF-17.

### ⚠️ Critiques sur notre propre travail

- **J'ai écrit que X01 bloque** le branchement de la calculette (`rapport-tests.md:250`).
  C'est trop fort : la décision est faite de fait (Q-REM-18).
- **Trop d'ADR « proposés »** : une dizaine. Un ADR proposé ne fait pas foi (`09-dec:34-38`).
  En soutenance, « appliqué mais pas validé » est difficile à défendre.
- **La base ne protège pas l'argent** : on peut payer le mauvais chasseur
  (`01:785-792`), avec un montant faux (Q-REM-11), sur des honoraires modifiables (Q-REM-12).
- **Aucun test fonctionnel**, alors que le sujet en exige (`Readme.md:256`).
- **La calculette n'est pas branchée** : elle ne lit pas le barème et n'écrit pas le paiement.
- **Les 2 556 biens ne servent pas la démo** : ils sont hors de Montpellier.
- **Beaucoup de documents se recouvrent** (`md/`, `livrables/`, `context AI/`) :
  une même question y vit à trois endroits, avec trois états.

---

## 4. Autres idées

- 💡 **Un seul registre de questions** : ce fichier, avec ses identifiants
  `Q-…`, remplace les listes éparses. Une question tranchée y prend sa date
  et son ADR, puis sort de la liste.
- 💡 **Préfixer les décisions** : `DS-` pour celles du sujet, `DG-` pour
  celles du groupe. Fin de la confusion sur « D2 ».
- 💡 **Un atelier d'une heure avec Jeff** : la partie 2, imprimée, avec la
  valeur proposée en face de chaque question.
- 💡 **Une diapo « règle ou paramètre »** en soutenance : c'est le piège que
  le sujet annonce (`RCR:40`), et on a de quoi le montrer.
- 💡 **Rejouer les 55 cas contre la base**, une fois la calculette branchée :
  même tableau d'exemples, mais lu depuis `commission_scale` et écrit dans `payment`.
- 💡 **Un test de non-régression sur la borne de tranche** : 199 999,99 €
  et 200 000,00 € ; c'est là que Q-REM-01 casse.
- 💡 **Mettre à jour `08-etat.md`** après chaque séance de décision : c'est
  le fichier qu'on relit après une coupure.

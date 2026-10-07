# Questions à trancher — état au 2026-10-06

Ce document **centralise** toutes les questions ouvertes du projet.
Chacune porte sa **source**, **qui tranche**, les **options**, et une
**recommandation argumentée**.

- 🎯 **Point de départ** : la calculette de rémunération (`API/src/app/services/remuneration.py`)
  a besoin de champs que la base n'a pas, ou qu'elle range autrement.
- 📚 **Sources lues** : le schéma `docker/init-v2/01` et `02`, les modèles de
  l'API, les `.feature`, `md/`, `livrables/`, `context AI/08-etat.md`, et le
  sujet (`StarterPack - BASE`, en lecture seule).
- ⚠️ Les numéros de ligne viennent de lectures faites le 2026-10-02, **relues le
  2026-10-05** dans les parties 0, 1 (thèmes A à D) et 3 : le schéma `01` avait
  glissé de 4 lignes. Ils bougent si le fichier change.
- 🔄 Les thèmes E, F et G gardent ici leur résumé. Leur texte **enrichi et relu**
  (contexte, « En clair », ➕/➖, ce que dit le sujet du prof) est dans la page à
  cartes, version 12 (`md/questions-a-trancher-2026-10-02.html`).
- 🆕 **2026-10-06** : 3e série de réponses reportée (partie 0), statuts des
  thèmes C à G mis à jour, ADR U à Z ajoutés au pense-bête. Numéros de `01` et
  `02` relus le 2026-10-06 : inchangés depuis le 2026-10-05.

---

## Mode d'emploi

### Qui tranche

| Repère | Qui | Pour quoi |
|---|---|---|
| 👥 **Groupe** | l'équipe, en réunion, tracé dans un ADR | technique, modélisation, choix internes |
| 🧑‍💼 **Jeff** | le client (formateur qui joue le commanditaire) | le métier, les chiffres, les droits |
| 📋 **PO** | le product owner : **Jeff** (Q-PRO-01, 2026-10-06) | priorités, périmètre, découpage |
| 🎓 **Prof** | le formateur en tant qu'évaluateur | attendus de la soutenance |

- ✅ **Le PO, c'est Jeff** (Q-PRO-01, 2026-10-06). Il joue **tous les rôles sauf le
  développement** ; le développement, c'est l'équipe.
- ✅ Jeff joue le client : `md/adr-026-perimetre-authentification.md:22`.
  Le sujet le confirme : « le formateur jouant le commanditaire »
  (`NOTE-DE-CADRAGE.md:70`).

### Les statuts

- 🟡 **Ouvert** : personne n'a tranché.
- 🟠 **Position ou hypothèse à valider** : quelqu'un a proposé, ou la migration a supposé ; le groupe n'a pas acté.
- 🔵 **Appliqué, pas acté** : le code ou le schéma le fait déjà, sans ADR accepté.
- 📝 **Note sans case** : un commentaire, sans réponse cochée ; la carte **reste ouverte**.
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
- `F00` à `F10` = `user-stories/00_…` à `10_….feature` (ex. `F07` = `07_…`)
- `RCR` = `REGLES-CALCUL-REMUNERATION.md` du sujet
- `09-dec` = `livrables/2-modelisation/09-decisions-a-prendre.md`

---

## 0. Déjà tranché — ne pas reposer

| Sujet | Décision | Date | Source |
|---|---|---|---|
| Unité monétaire | ✅ **euro** ; depuis le 2026-10-05 (Q-REM-01) : prix, budgets et barème en `INTEGER`, honoraires et paiement en `NUMERIC(12,2)` | 2026-09-21, revu 2026-10-05 | `context AI/08-etat.md:98-104`, `CLAUDE.md` règle 4 |
| Acte après la fin du mandat | ✅ **refusé, sauf renouvellement** | 2026-09-11 | `09-dec:122-178` |
| Mandat renouvelé | ✅ `'renewed'` marque le **nouveau** mandat | — | `09-dec:96-118`, `01:427` |
| Fin de mandat | ✅ `ends_at` **stocké** | 2026-09-11 | `09-dec:222` |
| Chaque chasseur a un manager | ✅ ADR-025, **accepté sur Confluence** — ⚠️ **« Annulé »** dans la copie du journal d'ADR de Confluence lue le 2026-10-06. ✏️ 2026-10-07 (Q9) : le lien **se garde**, un **nouvel ADR** remplace ADR-025 (Q-ACC-20) | 2026-09-22, revu 2026-10-07 | `md/a-faire-a-la-main-2026-09-21.md:189-190` |
| Authentification | ✏️ **Réouverte** : on fournit les **outils côté back** (route de connexion, token, session, rôles, droits), **pas la page de login** ; mot de passe gardé, haché en Argon2. Avant : ❌ hors périmètre (Jeff, 22/09) | 2026-09-22, revu 2026-10-07 | Jeff, entretien du 2026-10-07 (Q-JEF-14) ; avant : `md/adr-026-…:62-80` |
| Facture du chasseur | ❌ **hors périmètre** (Jeff) : aucune trace de facture en base (Q3 du plan, « rien ») — écart au sujet (`user-stories/07_chasseur_remuneration_et_performance.feature:17-27`), à écrire dans un ADR | 2026-10-07 | Jeff, entretien du 2026-10-07 (Q-JEF-23, Q-ACC-04) |
| Base de test | ✅ `fil_rouge_test`, isolée | 2026-10-02 | `08-etat.md:171-178` |
| Calculette | ✅ code du sujet, repris tel quel | 2026-10-02 | `08-etat.md:179-190` |
| Prix des biens | ✅ colonne `price_eur`, ligne à ligne | 2026-09-21 | `08-etat.md:110-113` |
| Ancien schéma `docker/init/` | ✅ obsolète, `init-v2` fait foi | 2026-09-21 | `08-etat.md:105-109` |

### Réponses — 2026-10-02, 2026-10-05, 2026-10-06 et 2026-10-07 (pages à cartes)

- 2026-10-02 : réponses de Sébastien (D1 à D4, Q-REM-01 à 12).
- 2026-10-05 : la liste complète est renvoyée comme « nos réponses », avec
  16 nouvelles (Q-REM-13 à 19, Q-PAR-01 à 09).
- 2026-10-05, 2e série (page v10) : **24 réponses** (Q-MAN-01 à 07, Q-SCH-01 à 04
  et 06 à 17, Q-ACC-11). Q-MAN-08 est cochée mais commentée « revoir, pas répondu » :
  elle **reste ouverte**, carte réécrite. Deux fois, case et commentaire diffèrent
  (Q-SCH-06, Q-SCH-17) : **le commentaire fait foi**.
- 2026-10-06, 3e série (page v11) : **29 réponses** — 27 nouvelles, et
  **2 changées** (Q-MAN-05, Q-ACC-11). **7 notes sans case** (Q-MIG-03, 05, 07, 11,
  Q-ACC-17, 18, Q-PRO-05) : elles **restent ouvertes**. Mes avis, demandés dans
  13 notes, sont plus bas (💬 Avis demandés) : 💡 des avis, pas des règles.
- ➡️ Les cartes 🧑‍💼 restent à confirmer par Jeff : **rapport à part**
  `md/questions-pour-jeff-2026-10-05.html` (voir partie 2). Les 34 cartes que
  seul Jeff tranche s'y cochent, et nulle part ailleurs, depuis le 2026-10-05.
  🆕 2026-10-06 : Jeff **ne remplit pas** ce rapport. Le groupe lui pose les
  questions **en entretien** ; l'équipe y note ses réponses.
- 2026-10-07, 4e série : ✅ **entretien avec Jeff fait**. Ses réponses, plus
  les réponses du groupe au rapport Jeff (71 lignes) et à la page d'incohérences
  (`md/plan-action-2026-10-07.html`, Q1 à Q15, D1 à D3). Tableau à part, plus
  bas (🆕 4e série) ; les lignes plus anciennes qu'elle change portent ✏️.

| Id | Réponse | Ce que ça entraîne |
|---|---|---|
| D1 à D4 | ✅ **garder** | Rien à défaire. |
| Q-REM-01 | ✅ **Tranchée et faite le 2026-10-05** : prix et bornes du barème en **`INTEGER`** (euros entiers, sans chiffre entre parenthèses), `EXCLUDE` du barème en `'[]'`. Le « numeric(12) » du 2026-10-02 était une erreur de formulation. | Tranches `[0 ; 199 999]`, `[200 000 ; 349 999]`… : ni trou ni chevauchement ; base, code (`rem.py:241`) et tableau du sujet (l. 173-174) d'accord. Mesuré : `price_eur` = 2 556 prix, 0 avec centimes, max 406 042 €. `INTEGER` va jusqu'à 2 147 483 647 ([doc PostgreSQL 16](https://www.postgresql.org/docs/16/datatype-numeric.html), lue le 2026-10-05). ✅ Fait : schéma (`c896e39`, `abbc84e`), modèles en `int` (`d3c128c`), 422 sur un prix à virgule (`fea3c9f`) ; testé sur une base temporaire (01, 02, 03 passent ; chevauchement refusé) ; 123 tests passent. D3 (adaptateur) inutile ; Jeff informé par Q-JEF-19. Gardent leurs centimes : honoraires et paiement, `NUMERIC(12,2)` (`F10:253`). |
| Q-REM-02 | ✅ **statut-mandat** (pas l'option recommandée) | Nouveau statut de fin sur `mandate` ; peut servir aussi à **Q-REM-14**. ⚠️ S'écarte de `RCR:100` (motif du refus dans `paiements`) : à écrire dans l'ADR. |
| Q-REM-03 | ✅ **colonne** — « à documenter et à confirmer avec Jeff » | `payment.performance_score`. ✅ **LOT5, 2026-10-07** : `NUMERIC(4,1)`, de 0 à 100, vide sur un refus, non exigé ailleurs — rapport LOT1→LOT5, carte D8, gardée. |
| Q-REM-04 | ✅ **jsonb** | `payment.calculation_details JSONB`. |
| Q-REM-05 | ✅ **table** | Table `remuneration_parameters` + CHECK `01:758-759` relâchés. |
| Q-REM-06 | ✅ **recalcul** | Code du sujet intact ; écart à `F10:293` dans l'ADR ; Q-JEF-17. |
| Q-REM-07 | ✅ **client-tous** — remarque : moins de visites = meilleure note | Remarque **juste** (`RCR:55`, `RCR:147`) : mon argument « gonfle la note » était faux, corrigé en v3 (aussi Q-ACC-13). Q-JEF-08. |
| Q-REM-08 | ✅ **non-refusees** | Q-JEF-09. |
| Q-REM-09 | ✅ **signes-sans-renouv** | Q-JEF-09 ; mandats annulés à demander. |
| Q-REM-10 | ✅ **oui** | `final_rate` dans `chk_refused`. |
| Q-REM-11 | ✅ **api** | Test d'intégration montant = taux × honoraires. |
| Q-REM-12 | ✅ **c3** | C3 codée dans `sale_service`. |
| Q-INF-06 | ✅ **valider dans le routeur commun** (2026-10-05) | Fait : `_validated` (`crud_router.py`) — prix à virgule et champ manquant en 422 ; commits `d3c128c`, `fea3c9f`. |
| Q-REM-13 | ✅ **cle** (2026-10-05, pas l'option recommandée) | Clé de `sale` vers `parameters_fees` (💡 ex. `sale.id_parameters_fees`) ; `02` n'insère aucune vente, rien à remplir. **Amende ADR-019** (proposé, « sans clé »). ⚠️ ADR-019 est « accepté » dans la copie du journal d'ADR de Confluence lue le 2026-10-06 : un nouvel ADR le remplace, on ne l'amende pas. |
| Q-REM-14 | ✅ **statut** (2026-10-05) | Statut de fin sur `mandate` (`01:405-407`), ex. `'lost'`. ✅ **Un seul : `'lost'`**, pour Q-REM-02 et Q-REM-14 — tranché à LOT3, gardé le 2026-10-07 (rapport LOT1→LOT5, carte D2). |
| Q-REM-15 | ✅ **seed** (2026-10-05) | Le seed fait commencer le barème par défaut en 2025 ; `rem.py:298` garde 2026. |
| Q-REM-16 | ✅ **hypothese** (2026-10-05) | `hire_date` = date de création du compte (`02:24-26`), dite en soutenance ; Jeff dira s'il a mieux (Q-JEF-10). |
| Q-REM-17 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · ✅ **colonnes** (2026-10-05) | `announced_at`, `invoice_submitted_at`, `verified_at`, `scheduled_for` et `invoice_reference` sur `payment`. 💡 Un CHECK par date, comme `chk_paid` (`01:765-767`). Q-ACC-11, répondue le 2026-10-05 (`colonne`), rejoint ce lot. ✏️ **2026-10-06** : Q-ACC-11 changée (une table des factures) : `invoice_reference`, `invoice_submitted_at` et `verified_at` quittent `payment`, **à reprendre**. ✅ **LOT5, 2026-10-07** : `announced_at` et `scheduled_for` gardées, un CHECK chacune ; statuts `'invoice_submitted'` et `'verified'` retirés — rapport LOT1→LOT5, cartes D6 et D7, gardées. |
| Q-REM-18 | ✅ **acter** (2026-10-05) | ADR X01 (option B) à écrire. À mettre à jour avec lui : `08-etat.md` (l. 80, 195) et `API/README.md:151`, qui attendent encore « l'arbitrage de X01 ». |
| Q-REM-19 | 🧑‍💼 **Confirmée par Jeff le 2026-10-07** · ✅ **oui** (2026-10-05, pas l'option recommandée) | `CHECK (final_rate BETWEEN 0.20 AND 0.60)` à la place de `01:755`. ⚠️ **Tension avec Q-REM-05** : on relâche deux réglages (`01:758-759`) et on en grave deux autres ; si Jeff change 20 % ou 60 % (Q-JEF-01), base à recréer. À revoir après sa réponse. |
| Q-PAR-01 | ✅ **sujet** (2026-10-05) | À valider par Jeff (Q-JEF-01). |
| Q-PAR-02 | ✅ **rien** (2026-10-05) | À valider par Jeff (Q-JEF-03). ⚠️ S'il veut une indemnité : un paiement exige une vente (`01:760`), Q-REM-02 à revoir. |
| Q-PAR-03 | ✅ **palier** (2026-10-05) | À confirmer par Jeff (Q-JEF-02). |
| Q-PAR-04 | ✅ **12** (2026-10-05) | À valider par Jeff (Q-JEF-01). |
| Q-PAR-05 | ✅ **transfo** (2026-10-05, pas l'option recommandée) — « demandé a jeff comment le score baisse, le calcule ? » | Atout : un mandat sans vente fait baisser la note, comme `Readme.md:135`. Le taux remplace S₄ seulement (`RCR:160`) ; les 5 poids restent. ⚠️ Le sujet ne donne **aucune grille** de notes pour ce taux : demandée à Jeff (Q-JEF-05, reformulée). |
| Q-PAR-06 | ✅ **sujet** (2026-10-05) — « les valeurs sont donné par le client, dont on fait confiance. » | ⚠️ Nuance : le sujet les dit « proposés, non imposés par le métier » (`F10:3-5`) ; elles deviennent celles du client quand Jeff dit oui (Q-JEF-01). |
| Q-PAR-07 | ✅ **sujet** (2026-10-05) | Cohérent avec Q-REM-05 : ces valeurs sortent des CHECK. Jeff : Q-JEF-01. |
| Q-PAR-08 | ✅ **garder** (2026-10-05) | Jeff : Q-JEF-01. |
| Q-PAR-09 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · ✅ **manager** (2026-10-05) | ⚠️ Ne colle pas avec la recommandation de Q-ACC-07 (« la direction seule ») ; 💡 la direction fixe le barème par défaut, le manager les barèmes nominatifs. Jeff dira d'abord s'il en veut (Q-JEF-16, en deux temps). Va dans le RACI (`RCR:329`). |
| Q-MAN-01 | ✅ **Activer** (2026-10-05) | CHECK « exactement 6 mois » à la place de celui de `ends_at` (`01:412-414`), SQL prêt (`01:435-445`). Fin de mois : à écrire dans l'ADR L. |
| Q-MAN-02 | ✅ **Corriger, activer, l'annulation libère tout de suite** (2026-10-05) | Trigger corrigé (parent exclu, `IS DISTINCT FROM`) et activé (`01:450-499`). D7 : Jeff confirme (Q-JEF-06). ✏️ **LOT4** : parent **et** enfant d'un renouvellement exclus l'un pour l'autre ; règle par client — rapport LOT1→LOT5, cartes D3 et D4, gardées le 2026-10-07. |
| Q-MAN-03 | ✅ **Imposer « sans vente » dans l'API, sans limite de nombre** (2026-10-05) | Code seul, dans l'API. Jeff : Q-JEF-07. |
| Q-MAN-04 | ✅ **Valider les deux** (2026-10-05) | La vente pointe vers le nouveau mandat ; le délai part de la 1re signature : le code remonte `id_mandate_parent`. |
| Q-MAN-05 | ✏️ **Changée le 2026-10-06**, voir plus bas. Avant : « Poser un CHECK d'égalité » (2026-10-05) — « le mandat doit être signé par les deux partie, donc il faudrait rajouter  is_hunter_signed et date signature reflèterais la signature des deux ? qu'en pense tu ? a modifié les schemas et bdd » | CHECK case ↔ date ; `02:218` et `02:225` à corriger. Ta question (signature du chasseur) devient **Q-MAN-09**. |
| Q-MAN-06 | ✅ **Toutes dans l'API, chacune testée** (2026-10-05) — « dit nous si on a besoin de metre a jours les schémas » | Tables : non. Trois TODO de `01` à annoter « contrôlé par l'API » (`01:639-641`, `664-668`, `789-795`). Diagrammes : non. ⚠️ `RCR:98` : « sauf renouvellement du mandat ». |
| Q-MAN-07 | ✅ **Autoriser 'canceled' sans date de signature** (2026-10-05) | `chk_status_signature` modifié (`01:430-432`). |
| Q-SCH-01 | ✅ **Garder le tout-ou-rien** (2026-10-05, pas l'option recommandée) — « ajoutez un champ "non renseigné" pour les champs vides. car l'on veux pas perdre l'intégrité malgré l'import des ancienne données, (obligatoire de les migré) » | `ALTER` de `02:64-66` retiré ; 18 clients : adresse « non renseigné » ; code postal refusé par le format (`01:210`) : **Q-SCH-18**. |
| Q-SCH-02 | ✅ **Garder criteria, écrire un ADR qui remplace ADR-009** (2026-10-05) — « Ecrit sur l'ADR09 une ligne disant "modifié le , par l'adr xx" » | ADR N. La ligne sur ADR-009 se fera à la synchro Confluence, manuelle et décidée par le groupe. |
| Q-SCH-03 | ✅ **Acter les 4 statuts** (2026-10-05) | ADR O ; ferme D4. |
| Q-SCH-04 | ✅ **Ajouter 'signed'** (2026-10-05) | `proposition_status` (`01:610-612`) ; ADR O ; ferme D5. |
| Q-SCH-06 | ✅ **Journal des notes : une ligne datée par note, sans période** (2026-10-05) — case cochée différente, **le commentaire fait foi** — « Validé : journal des notes, sans périodes (ni « garder », ni tsrange). Chaque note = une ligne datée à la seconde (scored_at TIMESTAMP NOT NULL) ; la note actuelle = la dernière ligne. On retire valid_from, valid_until, chk_perf_period et excl_perf_no_overlap ; on ajoute UNIQUE (id_payment), UNIQUE (id_mandate) et un index (id_hunter, scored_at DESC). Raison : Q-REM-06 recalcule la note à chaque vente, donc deux ventes le même jour doivent passer. À faire dans le lot de migration. ADR à noter (ferme D9). » | Journal des notes : voir le commentaire. ADR P ; ferme D9. |
| Q-SCH-07 | ✅ **Ne pas créer, hors MVP** (2026-10-05) | Rien en base. ADR T (limites assumées). |
| Q-SCH-08 | ✅ **Reporter au parcours IA** (2026-10-05) | Rien maintenant. ADR T. |
| Q-SCH-09 | ✅ **Ajouter** (2026-10-05) | `created_at` sur `client`, `hunter`, `real_estate_manager`, `role` (`01:169-170`). |
| Q-SCH-10 | ✅ **Renommer maintenant** (2026-10-05) | `is_cartet` → `is_carte_t` : colonne, modèle, migration (`01:257-260`). |
| Q-SCH-11 | ✅ **Contrôler** (2026-10-05, pas l'option recommandée) | Mesuré : 2 556 codes postaux sur 2 556 au format français ; mais `country_iso` vide sur tous les biens (`01:512-513`) : `'FR'` d'abord, puis le CHECK. |
| Q-SCH-12 | 🧑‍💼 **Confirmée par Jeff le 2026-10-07** · ✅ **Sans espace** (2026-10-05, pas l'option recommandée) | ⚠️ **À confirmer.** CHECK de `01:215` (client) et `01:391` (criteria) ; GB et NL gardent leur espace (`01:213-214`). |
| Q-SCH-13 | ✅ **« Supervises », et l'écrire** (2026-10-05) | Diagramme et README du schéma (`docker/init-v2/README.md:429-433`). |
| Q-SCH-14 | ✅ **Accepter comme limite** (2026-10-05) | Rien. ADR T. |
| Q-SCH-15 | ✅ **Resserrer la tranche à > 0** (2026-10-05) | CHECK de `01:697`. |
| Q-SCH-16 | ✅ **Ajouter le CHECK** (2026-10-05) | ⏭️ **Sans objet** depuis Q-SCH-17 : `valid_until` disparaît. |
| Q-SCH-17 | ✅ **Par construction : une grille vaut jusqu'à la suivante** (2026-10-05) — case cochée différente, **le commentaire fait foi** — « Décidé : ni contrôle API ni « rien » — une grille vaut jusqu'à la suivante, par construction. parameters_fees : on retire valid_until ; valid_from est renommé effective_from (« en vigueur à partir du »). La contrainte EXCLUDE (01:685-686) est remplacée par UNIQUE (effective_from) : deux grilles ne démarrent pas le même jour. Lecture : la grille d'une vente = la dernière dont effective_from <= date de l'acte. Trou impossible ; seul cas restant : une vente avant la 1re grille, couvert par le seed (Q-REM-15). Code du sujet inchangé : l'adaptateur calcule date_fin = veille de la grille suivante. À toucher : 01:679-680 et 686, parameters_fees_model.py:26-27. Lot de migration. ADR à noter. » | Voir le commentaire. ADR Q ; rend Q-SCH-16 sans objet. |
| Q-ACC-11 | ✏️ **Changée le 2026-10-06**, voir plus bas. Avant : « invoice_reference sur payment » (2026-10-05) | Même lot que Q-REM-17 ; plus un doublon. |
| Q-MAN-08 | ✏️ cochée « Reporter », commentaire « revoir, pas répondu » (2026-10-05) ; ✅ **répondue le 2026-10-06**, voir plus bas | Carte réécrite (thème C). |
| Q-MAN-05 | ✅ **Supprimer la colonne** (2026-10-06, pas l'option recommandée) — « le mandat doit être signé par les deux partie, donc il faudrait rajouter  is_hunter_signed et date signature reflèterais la signature des deux ? qu'en pense tu ? a modifié les schemas et bdd » | ✏️ **Change la réponse du 2026-10-05** (« Poser un CHECK d'égalité »), à la suite de Q-MAN-09. `is_client_signed` est retiré (`01:415`) : modèle, API et `02` touchés. Plus de case, plus de contradiction : `MAND-0008` et `MAND-0016` (`02:218`, `02:225`) gardent leur date, reprise de la source (`date_debut`, `PgSQL.sql:130`). ADR S. |
| Q-MAN-08 | ✅ **Reporter** (2026-10-06) | Rien maintenant : la réaffectation attend que l'**affectation** soit décidée, avec Jeff (Q-JEF-14). 💡 Une ligne dans l'ADR T (limites assumées) : une demande réaffectée peut revenir au chasseur qui l'a refusée. |
| Q-MAN-09 | ✅ **Le client seul, comme le sujet** (2026-10-06, pas l'option recommandée) — « retirer is_client_signed, par juste la date de signature, on passe par le status pending signature » | Comme le sujet : seule la signature du **client** compte (`Readme.md:98`). **Le commentaire fait foi** : pas de CHECK d'égalité (l'effet écrit sous l'option) ; la case disparaît (Q-MAN-05). Restent la date `signature_date` (`01:408`) et le statut. `pending_signature` existe déjà (`01:405-407`) ; `chk_status_signature` le relie à la date : « en attente » si et seulement si pas de date (`01:430-432`). ADR S : décidé. |
| Q-SCH-18 | ✅ **Un code factice 00000, documenté** (2026-10-06) | `02` écrit `00000` pour les 18 clients repris (`02:148-165`) ; le format français l'accepte : 5 chiffres (`01:210`). Une ligne dans le README du schéma, et dans l'audit. ADR R : décidé. Jeff peut fournir les vrais codes (Q-JEF-26). |
| Q-MIG-04 | ✅ **Remplacer dans le seed, puis supprimer** (2026-10-06) | Le seed crée 2 managers (Q-ACC-16), y rattache les 6 chasseurs, puis efface le user 25 (`02:122-128`). Dans cet ordre : les clés sont en `ON DELETE RESTRICT` (`01:222-223`, `01:266-267`). 💡 Effacer, et non désactiver (Q-ACC-08) : ce compte n'a jamais servi. À dire. ⚠️ Suppose le lien chasseur → manager : ADR-025 serait « Annulé » sur Confluence (voir Q-ACC-20). |
| Q-MIG-06 | ✅ **Oui, dans 03** (2026-10-06) — « si la colone est vide, placeholder ? » | Le script d'import `03` recopie la lettre `dpe` dans `estate.energy_class` (`01:521`) : **1 623** biens sur 2 556. ⚠️ `03` est une copie retouchée de `normalised/populate_estate.sql` ; le script de retouche n'est pas dans le dépôt : comment régénérer `03`, non vérifié. 💡 Hors carte, au même passage : `criteria.energy_class_max` (`01:328`) ; 2 recherches disent « DPE C max » et « DPE D max » (`02:192`, `02:207`). |
| Q-MIG-08 | ✅ **Migrer les secteurs** (2026-10-06) — « ajoute dans criteraia, sector nullable , idem dans estate » | `02` enrichi : la ville, le code postal et le pays `'FR'` des secteurs passent dans `criteria` (`01:301-305`) ; une ville exige un pays (`01:379-380`). 🆕 Ta note : une colonne **quartier**, facultative, sur `criteria` **et** sur `estate`. 💡 Nom proposé : `district` (`sector` désignait toute la table source : ville, quartier, code postal). Facultative, comme dans la source : 2 secteurs sur 10 n'ont pas de quartier (`PgSQL.sql:37`, `:46-47`). ⚠️ Les 2 556 biens n'ont pas de quartier : le CSV n'a que `town`, `street` et `postal_code`. `estate.district` resterait vide pour eux. ADR N (la localisation) ; lot de migration. |
| Q-MIG-09 | ✅ **Laisser le minimum vide (NULL, « inconnu »)** (2026-10-06, pas l'option recommandée) | `02` : `budget_min` à **NULL** sur les 17 critères (`02:192-208`) ; la base l'accepte (`01:318`), l'API aussi (`criteria_model.py:35`). Rien d'inventé. Le commentaire périmé de `02:189` (NOT NULL, K€, `NUMERIC(6,1)`) se corrige au même passage. ADR U (données reprises). |
| Q-ACC-08 | ✅ **Oui** (2026-10-06) — « lorsqu'il y a une demande de suppression de compte, admin va rendre anonyme les données du compte et passé le compte en inactif . tout ca pour la RGPD. donne ton avis stp. » | Désactiver plutôt que supprimer. Sur une demande d'effacement, l'admin **rend anonyme** le compte, puis le passe **inactif** (ta note). ADR V. Combien de temps garder avant d'anonymiser : Jeff (Q-JEF-15). |
| Q-ACC-09 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · ✅ **L'admin** (2026-10-06, pas l'option recommandée) — « à avoir avec jeff si un hunter ou manager peut crée un bien à la main, si non les biens vont être importer via un script dans Airflow. Donc, dit moi ce que tu en pense . Es ce que l'admin aurais besoin de lancer qq chose ou le Airflow le ferais tout seul. aide nous » | ⚠️ Pas l'option recommandée (un compte technique). Ta note pose deux questions : la saisie à la main (Jeff, Q-JEF-24) et Airflow. ✅ Colonne tranchée à LOT9 (2026-10-07) : `estate.id_author` → `"user"(id)`, facultative (vide = import), clé seule ; le rôle se vérifie dans l'API. |
| Q-ACC-11 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · ✅ **Une table document** (2026-10-06, pas l'option recommandée) — « Revu le 2026-10-06 : on remplace « colonne » par une table à part pour les factures du chasseur (ex. hunter_invoice), à confirmer avec Jeff. Raisons : une facture refusée puis renvoyée doit laisser une trace ; chaque facture a son état (soumise, vérifiée, refusée) et son montant ; le sujet propose déjà un facture_id dans paiements (REGLES-CALCUL-REMUNERATION.md:288). On ne renomme pas payment : il porte le calcul de la rémunération, pas la facture, et « facture » se confondrait avec celle du particulier (03_particulier_offre_et_signature.feature:37-41). À reporter sur Q-REM-17 : invoice_reference, invoice_submitted_at et verified_at passent de payment à la table des factures. Question pour Jeff : une table de factures du chasseur, reliée au paiement, ça vous convient ? » | ✏️ **Change la réponse du 2026-10-05** (`invoice_reference` sur `payment`). Une table des factures du chasseur (ex. `hunter_invoice`), reliée au paiement : chaque envoi garde son état, sa date et son montant. ➡️ **Q-REM-17 à reprendre** : `invoice_reference`, `invoice_submitted_at` et `verified_at` quittent `payment` ; `announced_at` et `scheduled_for` y restent. À confirmer avec Jeff : Q-JEF-23. ADR J amendé. |
| Q-ACC-14 | ✅ **Reporter au parcours IA** (2026-10-06) | Rien maintenant ; même logique que Q-SCH-08. 💡 ADR T. 📋 Carte du PO : le PO, c'est **Jeff** (Q-PRO-01). À lui confirmer en une phrase. |
| Q-ACC-16 | ✅ **1 admin, 2 managers** (2026-10-06) | Seed : 1 admin (1 ligne `user`), 2 managers (`user` et `real_estate_manager`) ; les 6 chasseurs en 2 équipes ; puis le manager fictif effacé (Q-MIG-04). ⚠️ Suppose le lien chasseur → manager (ADR-025, voir Q-ACC-20). |
| Q-ACC-19 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · ✅ **La faire** (2026-10-06, pas l'option recommandée) — « a redéfinir un peut plus avec jeff. si l'on gere une clé d'api et comment. » | ⚠️ Pas l'option recommandée. Ta note : **à redéfinir avec Jeff**, une clé ou plusieurs, et comment (Q-JEF-22). Rien avant. Outil prêt : `APIKeyHeader` de FastAPI, sans dépendance à ajouter ; la clé dans `docker/.env`, jamais dans git. ADR Y. |
| Q-ACC-20 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · ✅ **Oui** (2026-10-06) — « a confirmé plus tard, on comprends pas. » | 🟡 **À confirmer plus tard** (ta note). Explication simple plus bas (💬 Avis demandés). |
| Q-INF-01 | ✅ **Décider d'abord s'il en faut un** (2026-10-06) — « il faut voir avec robin (2eme proff) mais a priori on le garde » | Rien tant que Robin (le 2e professeur) n'a pas donné son avis ; a priori, on garde MinIO. 🆕 Le 2026-10-06, `be15c04` remplace les deux images MinIO par des images `pgsty/…`, épinglées par empreinte `sha256`. Qu'elles se téléchargent : **non vérifié ici**. ⚠️ Images d'un éditeur tiers (`pgsty`), pas de MinIO lui-même : leur provenance est à connaître. L'empreinte garantit au moins qu'elles ne changent pas. Si elles marchent : `md/minio-images-indisponibles-2026-10-02.md` et `context AI/08-etat.md` sont à mettre à jour. |
| Q-INF-02 | ✅ **Après ces réponses** (2026-10-06) — « a faire apres les réponses de jeff, donc apres les deux rapports. et notre entrevue avec jeff. » | Le seed s'écrit **après l'entretien avec Jeff**, puis après le lot de migration. Toutes ses dépendances sont répondues (Q-INF-03, le 2026-10-06). Il contiendra : 1 admin et 2 managers (Q-ACC-16), le manager fictif remplacé (Q-MIG-04), des biens de démo (Q-INF-03), le barème dès 2025 (Q-REM-15). |
| Q-INF-03 | ✅ **3 à 5 biens fictifs** (2026-10-06) — « a définir au moment du seed, plusieurs par départements » | Au moment du seed : **plusieurs biens fictifs par département** (ta note). 💡 Les secteurs des clients du sujet : **Hérault (34)**, 7 sur 10 ; **Rhône (69)**, 2 ; **Loire-Atlantique (44)**, 1 (`PgSQL.sql:42-51`). Nos 2 556 biens n'ont que Nantes en commun. 💡 Un acte d'au moins **500 000 €** montre la tranche à 45 % (budget de 550 000 €, `PgSQL.sql:95`). Ferme la Q4 du point d'étape (Q-PRO-02). |
| Q-INF-04 | ✅ **Commencer par le parcours de paiement** (2026-10-06) | Après le branchement de la calculette sur la base (chantier 2), et après le lot de migration. Le scénario, de bout en bout : mandat signé → visites → vente → paiement (`PLAN-DE-TESTS.md:16`). |
| Q-INF-05 | ✅ **payment, sale, mandate d'abord** (2026-10-06) — « voir pour finir les tests d'intégration des autres table, et pourquoi ? » | D'abord `payment`, `sale` et `mandate`, **après le lot de migration** (il les change) ; puis les 12 autres (ta note). 💬 « Pourquoi ? » : réponse plus bas (💬 Avis demandés). |
| Q-INF-07 | ✅ **Quand le seed est stable** (2026-10-06) — « à explicité, » | Après le seed. 💬 Explication plus bas (💬 Avis demandés). |
| Q-INF-08 | ✅ **ENF-01 avec le générateur ; ENF-03 tombe avec l'auth** (2026-10-06) | ENF-01 : un test de charge, 500 mandats en moins de 2 s, sur les requêtes qui comptent ventes et mandats ; avec le générateur (Q-INF-07). ENF-03 : pas de test, expliqué en soutenance (l'auth est hors périmètre). 💡 Dans le rapport de tests : d'où viennent ENF-01 et ENF-03 (un « Exemple rempli » du prof, `CAHIER-DES-CHARGES-TECHNIQUE.md:74`) ; et « rémunération » à corriger en « performance » (`rapport-tests.md:254`). |
| Q-PRO-01 | ✅ **En nommer un** (2026-10-06) — « c'est Jeff » | Le PO, c'est **Jeff**. Il joue **tous les rôles sauf le développement**, qui revient à l'équipe (dit le 2026-10-06). ➡️ Les 3 cartes 📋 PO (Q-SCH-08, Q-ACC-14, Q-PRO-07) sont à lui confirmer. ⚠️ L'option disait aussi « il tient le journal d'ADR » : Jeff ne le tiendra pas. 💡 Un membre de l'équipe, nommé dans la RACI. Q-JEF-25 lui demande de valider les ADR en une séance. |
| Q-PRO-02 | ✅ **Plus tard** (2026-10-06, pas l'option recommandée) | ⚠️ Pas l'option recommandée (une réunion de 30 min). Il ne reste presque rien : Q1, Q2 et Q5 confirmées par d'autres cartes ; **Q4 répondue** le 2026-10-06 (Q-INF-03). Reste **Q3**, le motif de refus : en base, pas acté (ADR-024) ; il passera à la séance des ADR (Q-PRO-03). |
| Q-PRO-03 | ✅ **Tout en une séance** (2026-10-06) — « attendre la confirmation de jeff » | Une séance, **après toutes les réponses**, Jeff compris (Q-JEF-25). 🆕 D'après la copie du journal d'ADR de Confluence lue le 2026-10-06 : ADR-016 à 023 sont déjà **« accepté »** ; ADR-025 et la page 024 sont **« Annulé »** ; ADR-027 reste **« proposé »**. La séance porte donc sur : ADR-027, nos brouillons (024, motif de refus ; 026, périmètre de l'auth, à renuméroter 028), les ADR déjà acceptés à remplacer (019 par Q-REM-13) et les ADR du pense-bête. |
| Q-PRO-04 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · ✅ **Le journal Confluence fait foi** (2026-10-06) — « ard16 a était marqué comme annulé le 06/10 » | Le CDC suit la numérotation du journal : Argon2 = ADR-016. ⚠️ Ta note : **ADR-016 annulé le 06/10**. La copie du journal lue le même jour à 11 h 16 le dit encore « accepté » : à vérifier sur Confluence. S'il est bien annulé : le code hache toujours en Argon2 (`security.py:20-32`). À aligner après la réponse de Jeff sur le mot de passe (Q-JEF-21). |
| Q-PRO-06 | ✅ **Oui** (2026-10-06) — « je pense que l'on va découpé le Journal de décisions (ADR) en dossier et page pour chaque ADR; avec un dossier; ADR acceptée, ADR refusé, ADR proposé, etc. plus simple pour la maintenance et la lecture » | Au prochain passage manuel sur Confluence : retirer la note drawio collée avec ADR-025 ; coller la fiche ADR-024 (`md/adr-024-motif-refus-remuneration.md`, à partir de la ligne 16) ; la ligne sur ADR-009 (Q-SCH-02). 💬 Ta proposition (une page par ADR, des dossiers par statut) : avis plus bas (💬 Avis demandés). |
| Q-PRO-07 | ✅ **Planifier maintenant** (2026-10-06) — « a voir apres la réunion avec jeff » | Le planning se fait **après l'entretien avec Jeff**, qui est aussi le PO. ⚠️ Avant de planifier le livrable 3 : sa cible est la phase 3, la croissance (OLTP/OLAP, 3V, PCA/PRA, `Readme.md:241-250`), pas les trois couches de l'API (`08-etat.md:55`). ⚠️ L'audit (livrable 1) ne peut pas s'appuyer sur `normalised/rapport_anomalies.txt` : 2 lignes, « 0 anomalies ». |
| Q-PRO-08 | ✅ **Harmoniser** (2026-10-06, pas l'option recommandée) | ⚠️ Pas l'option recommandée (reporter). Le format est **déjà fixé par ADR-007** (accepté) : un seul champ international, indicatif compris, ex. `+33612345678`, validé par une « regex E.164 souple » (copie du journal d'ADR de Confluence lue le 2026-10-06). Le CHECK l'écrit dans la base, sur les 3 tables (`01:184-185`, `01:228-229`, `01:246-247`). Pas d'ADR propre : il applique ADR-007. ⚠️ Il refusera les 4 faux numéros `0000000000` : voir Q-MIG-07. |
| Q-MIG-03 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · 📝 **Note sans case** (2026-10-06) — « ajouter "suspendu" et "annulé" ? a voir avec jeff » : **reste ouverte** | 📝 Ta note rejoint **Q-JEF-13**, déjà posée à Jeff (le sens de « suspendu »). |
| Q-MIG-05 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · 📝 **Note sans case** (2026-10-06) — « ajoute un placeholder au valeurs des ancienne données, on grade la note et l'on met un place holder dans les autre valeurs » : **reste ouverte** | 📝 Ta note demande une valeur factice. Mon avis : vide. |
| Q-MIG-07 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · 📝 **Note sans case** (2026-10-06) — « ajouté +330000000000 ?, un autre placeholder ? » : **reste ouverte** | 📝 Liée à Q-PRO-08, répondue « Harmoniser » le même jour. |
| Q-MIG-11 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · 📝 **Note sans case** (2026-10-06) — « faire un ADR qui annule la gestion des mots de passe dans l'appli ? » : **reste ouverte** | 📝 Ta question est posée à Jeff : **Q-JEF-21** (garder un mot de passe ?). |
| Q-ACC-17 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · 📝 **Note sans case** (2026-10-06) — « hors scope, authentification hors scope » : **reste ouverte** | 📝 Hors périmètre, dit ta note : rien à décider de plus. |
| Q-ACC-18 | ✏️ **Revue le 2026-10-07** (voir 🆕 4e série) · 📝 **Note sans case** (2026-10-06) — « hors scope, authentification hors scope. avoir avec jeff si on garde le mot de pass dans la bdd. » : **reste ouverte** | 📝 C'est **Q-JEF-21**, posée à Jeff. Rien avant sa réponse. |
| Q-PRO-05 | 📝 **Note sans case** (2026-10-06) — « le CDC est pas fini, il faut le complété et le finir , puis voir si l'on doit en faire un pour le FIX et la suite » : **reste ouverte** | 📝 Ta note : finir le CDC d'abord. |

#### 🆕 4e série — 2026-10-07 : entretien avec Jeff, et réponses du groupe

- 🧑‍💼 = réponse de **Jeff** à l'entretien du 2026-10-07 (notée par l'équipe).
- 👥 = réponse du **groupe** : rapport Jeff (71 lignes) ou page d'incohérences
  (`md/plan-action-2026-10-07.html`, Q1 à Q15).
- « Il valide nos positions » veut dire : la position écrite sur la carte du
  rapport Jeff, sans changement.

| Id | Réponse | Ce que ça entraîne |
|---|---|---|
| Q-PAR-01, 04, 06, 07, 08, 10, 11, 13 | 👥 **sujet** (Q-PAR-04 : 12 mois ; Q-PAR-08 : garder) — 🧑‍💼 **tous validés** (Q-JEF-01) | Rien à changer. Note sur Q-PAR-06 : « les valeurs sont donné par le client, dont on fait confiance ». |
| Q-REM-19 | 🧑‍💼 20 % et 60 % validés (Q-JEF-01) | ➡️ `CHECK (final_rate BETWEEN 0.20 AND 0.60)` entre au lot. |
| Q-PAR-03 | 👥 **palier** — 🧑‍💼 validé (Q-JEF-02) | Rien. Le saut d'environ 600 € à 350 000 € est assumé. |
| Q-PAR-02, Q-REM-02 | 👥 **rien** — 🧑‍💼 « **rien pour personne** » (Q-JEF-03) | Vente par le client ou une autre agence : ni le chasseur ni l'entreprise ne touchent rien. Le statut de fin du mandat (Q-REM-02, Q-REM-14) se garde. |
| Q-JEF-04 | 🧑‍💼 honoraires **HT** validés | Rien. |
| Q-PAR-05 | 👥 **transfo** — 🧑‍💼 pas de grille : **le groupe propose la sienne** (Q-JEF-05) | ➡️ Grille de notes à écrire, marquée « proposition du groupe ». 📝 Ta note : « demandé a jeff comment le score baisse, le calcule ? » — à expliquer dans l'ADR F. |
| Q-REM-07 | 👥 **client-tous** — 🧑‍💼 validé (Q-JEF-08) | 📝 Ta note : « moins il visite, meilleure est la note ». 🟡 Sens du critère à vérifier dans le code du sujet avant l'ADR F. |
| Q-REM-08, Q-REM-09 | 👥 non refusées ; signés sans renouvellement — 🧑‍💼 validés (Q-JEF-09) | Rien. |
| Q-REM-06 | 🧑‍💼 recalculer à chaque vente : validé (Q-JEF-17) | Écart à `F10:293` assumé : ADR E. |
| Q-REM-16, Q-MIG-02 | 👥 hypothèse gardée — 🧑‍💼 validé (Q-JEF-10) | À dire en soutenance. |
| Q-MAN-02 | 🧑‍💼 l'annulation d'un exclusif **libère tout de suite** (Q-JEF-06) | Trigger d'exclusivité corrigé et activé : déjà au lot. |
| Q-MAN-03, Q-MAN-04 | 🧑‍💼 validés (Q-JEF-07) | Rien. |
| Q-JEF-11 | 🧑‍💼 Bruno : mandat **renouvelé**, comme le lit le groupe | Rien. |
| Q-MIG-01 | 👥 **honoraires** — 🧑‍💼 validé (Q-JEF-12) | % des honoraires, non migré. |
| Q-MIG-10 | 👥 **expirer** — 🧑‍💼 confirmé (Q-JEF-13) | ➡️ `02` : les 6 mandats échus passent en `'expired'`. |
| Q-MIG-12 | 👥 demander — 🧑‍💼 oui, c'est **Nina Girard** (Q-JEF-13) | ➡️ `02` : le mandat 13 se rattache à sa fiche client, déjà dans les fixtures (`PgSQL.sql:103`, rôle `client`). Ta note (« compte séparé ? ») : pas de compte en plus. |
| Q-MIG-13 | 👥 demander — 🧑‍💼 nos positions (Q-JEF-13) : `termine` → `completed`, `suspendu` → `canceled`, **pas de pause** | ➡️ La traduction de « suspendu » s'écrit dans `02` et le README. 📝 Ta note : à vérifier après le lot. |
| Q-MIG-03 | 🧑‍💼 **pas de nouvel état** (Q-JEF-13) | Les 17 demandes en `'launched'` (`02:241-246`). Ferme ta note du 2026-10-06. |
| Q-SCH-01, Q-SCH-18, Q-MIG-05, Q-MIG-07, Q-MIG-09 | 🧑‍💼 les manques sont **voulus** ; ne pas supprimer les anciennes données ; les autres peuvent être fausses (Q-JEF-26) — 👥 Q4 : **vide (NULL) si la colonne l'accepte, sinon une valeur factice documentée** ; un **faker** forké du script du sujet servira à tester les contraintes | Q-MIG-05 : colonnes d'énergie vides, `energetic_score` retiré. Q-MIG-07 : `+33000000000`, documenté. Q-MIG-09 : vide (inchangé). Q-SCH-01, Q-SCH-18 : inchangées. `PgSQL.sql` ne se touche jamais. |
| Q-ACC-02 | 👥 **ses** chasseurs et leurs paiements | Matrice ADR-027. |
| Q-ACC-03 | 👥 **le manager** enregistre la vente (Q10) | Matrice ADR-027. |
| Q-ACC-04 | ⛔ **sans objet** : facture hors périmètre (🧑‍💼) | — |
| Q-ACC-05 | 👥 **non** : le client voit les biens proposés pour lui | Matrice ADR-027. |
| Q-ACC-06 | 👥 **oui** — 🟡 ta note : « a confirmé, mais sans doute que oui ? » | Matrice ADR-027 ; à confirmer avec Jeff. |
| Q-ACC-07 | 👥 **la direction** seule | Aligne Q-PAR-09 et Q-JEF-16. |
| Q-ACC-10 | 👥 **le manager** affecte la demande | Matrice ADR-027. |
| Q-ACC-12 | 👥 **le client** crée son compte — 🟡 ta note : « a confirmé avec jeff ? » | Matrice ADR-027 ; à confirmer. |
| Q-ACC-13 | 👥 **le chasseur** enregistre la visite — 🟡 ta note : « a confirmé » | Matrice ADR-027 ; à confirmer. |
| Q-ACC-15 | 👥 **oui** (pas l'option recommandée), précisé par Q7 : **seulement pour un client qui a déjà un compte** | Une ligne dans la matrice ADR-027, pas d'ADR propre. |
| Q-PAR-09, Q-JEF-16 | ✏️ **changée** : **la direction** (avant : le manager) — 🧑‍💼 la direction | RACI à corriger. |
| Q-ACC-09, Q-JEF-24 | 🧑‍💼 un bien peut être **saisi à la main** (hors marché, courant dans l'immobilier) — 👥 Q8 : par le **chasseur et le manager** | ➡️ Une colonne d'**auteur** sur `estate`. |
| Q-ACC-08, Q-ACC-21, Q-JEF-15 | 👥 **10 ans + X** — 🧑‍💼 ajouter une route, ou modifier la route DELETE, pour **seulement anonymiser** les données personnelles d'une personne | ➡️ Route d'anonymisation dans l'API. La durée X : **le groupe la propose**, avec sa source, marquée « proposée ». |
| Q-SCH-05 | 👥 **1-5** — 🧑‍💼 de 1 à 5 (Q-JEF-18) | ➡️ Colonne `SMALLINT`, `CHECK` de 1 à 5, au lot. |
| Q-SCH-12 | 👥 sans espace **confirmé** (2026-10-07) | Au lot, sans réserve. |
| Q-ACC-11, Q-REM-17, Q-JEF-23 | 🧑‍💼 **facture hors périmètre** — 👥 Q3 : **aucune trace** | ➡️ Retirés du lot : la table des factures, `invoice_reference`, `invoice_submitted_at`, `verified_at`. Dates restantes (`announced_at`, `scheduled_for`) à revoir au lot. Écart au sujet : ADR. |
| Q-ACC-17, Q-ACC-18, Q-MIG-11, Q-JEF-21 | 🧑‍💼 l'authentification revient : **outils côté back** (Q-JEF-14) — 👥 Q2 « outils » : mot de passe **gardé**, haché en **Argon2** | 12 caractères gardés (Q-ACC-17). Le faux hash `$2b$` de la migration reste, documenté (Q4). Q-JEF-21 : réglée par Q-JEF-14. |
| Q-ACC-19, Q-JEF-22 | 🧑‍💼 **une clé par programme** (Q-JEF-22) | ➡️ Dans l'API. |
| Q-ACC-20 | 👥 Q9 : **garder** le lien chasseur → manager | ➡️ Nouvel ADR qui remplace ADR-025 (raison : l'organisation de l'entreprise). |
| Q-PRO-04 | 👥 Q2 : « dé-annuler » ADR-016 (Argon2) et ADR-026 de Confluence — « il me semble » | 🟡 À vérifier sur Confluence avant l'ADR. |
| Q-REM-01 | 🧑‍💼 informé (Q-JEF-19), pas d'objection | Rien. |
| Q-REM-03, Q-REM-04 | 🧑‍💼 confirmé (Q-JEF-20) | Rien. |
| Q-PRO-01, Q-PRO-03 | 🧑‍💼 confirmé (Q-JEF-25) : il est le PO ; ADR validés en une séance | Rien. |
| 🆕 Rôle en lecture seule | 👥 Q14 : **les deux** — un rôle PostgreSQL (`GRANT SELECT`) et un rôle applicatif « lecteur » | 🟡 À demander à Jeff sur Discord. Mot de passe du rôle dans `docker/.env`, jamais dans git. |
| Plan d'action | 👥 Q11 : **un seul lot** ; Q12 : **par thème** ; Q13, Q15 : **kit vlp**, confirmé le 2026-10-07 (étapes 2-3, puis une fiche par ADR) ; `CHANTIER.md` remis au dépôt le 2026-10-07 ; D1 : ADR après, le code cite les Q-xx ; D2 : schémas = `01` + modèles + `livrables/2-modelisation` + MPD ; D3 : tests et pyright par thème | Dernière étape : **déployer sur ton VPS**, une fois la base réparée. |
| Q-PRO-05 | — | 🟡 Reste ouverte (« le FIX »). |

**💬 Avis demandés dans tes notes du 2026-10-06** — 💡 ce sont mes avis, pas
des règles : la réponse reste au groupe. Sources relues le 2026-10-06.

- **Q-MIG-03** :
  - 💡 Ces deux états touchent surtout le **mandat** : « annulé » y existe déjà (`canceled`, `01:405-407`), « suspendu » non.
  - Ajouter un état à la **demande** rouvrirait Q-SCH-03 : 4 statuts actés le 2026-10-05 (`01:287-288`).
  - ⚠️ Sans la case « signé » (Q-MAN-05), la voie « au mandat signé » ne trie plus les 2 mandats annulés : les 17 ont une date. Il faudrait filtrer sur le statut.
  - 💡 Attendre la réponse de Jeff, puis trancher la carte.
- **Q-MIG-05** :
  - 💬 Je comprends ta note ainsi : garder la note énergie (la lettre), et mettre une valeur factice dans les autres colonnes d'énergie. Si ce n'est pas ça, dis-le.
  - ✅ **La lettre se garde** : c'est Q-MIG-06, répondue « oui » (`dpe` → `energy_class`).
  - ⚠️ `energetic_score` n'a **rien à garder** : `NULL` sur les 2 556 biens (`normalised/annonces_normalised.csv`).
  - ❌ **Une valeur factice est impossible** : `energy_kwh_m2` et `energy_co2_m2` refusent 0 (`CHECK > 0`, `01:524-525`). Un faux nombre positif se lirait comme une vraie mesure.
  - 💡 **Laisser vide (NULL)** : ces colonnes l'acceptent. Et **acter** le retrait de `energetic_score` (la recommandation) : ADR U.
- **Q-MIG-06** :
  - 💡 **Pas de valeur factice : laisser vide (NULL)** pour les 933 biens sans lettre.
  - La colonne accepte le vide (`01:521`, sans `NOT NULL`). Une lettre hors liste, comme `X`, serait refusée (CHECK de A à G).
  - Une fausse lettre se lirait comme une vraie : un bien noté « A » par défaut sortirait dans une recherche « DPE C max ».
  - Le sujet fait pareil : son générateur ne donne une lettre qu'à une partie des biens (`outils/generer_annonces.py:86`, `:282-287`).
  - ✅ Même logique que ta réponse Q-MIG-09 : vide veut dire « inconnu ».
- **Q-MIG-07** :
  - 💡 **Oui, une valeur factice, mais au bon format** : sinon le CHECK de Q-PRO-08 refusera les 4 `0000000000`.
  - Le format est déjà fixé par **ADR-007** (accepté) : un champ international, indicatif compris, ex. `+33612345678` (copie du journal d'ADR de Confluence lue le 2026-10-06).
  - ⚠️ `+330000000000` a **un zéro de trop** : un numéro français s'écrit `+33` puis **9 chiffres**, comme `+33611223344` (`02:135`). Soit `+33000000000`.
  - ⚠️ Le CHECK doit **accepter** cette valeur : un format trop strict (premier chiffre de 1 à 9) la refuserait.
  - ✅ Même logique que tes réponses Q-SCH-01 et Q-SCH-18 : la colonne reste obligatoire, la valeur factice est **documentée** (README, audit), et le seed ne la cache pas (`md/point-etape-2026-09-21.md:233`).
  - Autre voie : rendre la colonne facultative (l'option « nullable ») ; plus de valeur factice, mais le téléphone n'est plus exigé des nouveaux clients.
- **Q-MIG-11** :
  - 💡 **Attendre Jeff.** S'il dit « non » : oui, un ADR qui retire `user.password`. Coût compté le 2026-10-06 : 4 fichiers d'`API/src`, 8 de tests, 27 lignes de `02`, et `docker/migrations/2026-09-22_hunter_manager.sql:46-48`.
  - S'il dit « oui » : garder, et une phrase dans le seed sur le faux préfixe `$2b$` (la recommandation).
  - ⚠️ Ta note sur Q-PRO-04 dit ADR-016 (Argon2) annulé le 06/10 : même chantier.
- **Q-ACC-08** :
  - ✅ **D'accord**, et la base s'y prête : ses **34** clés étrangères sont toutes en `ON DELETE RESTRICT`, aucune en `CASCADE` (compté le 2026-10-06). Rien ne s'efface par ricochet.
  - ⚠️ **Rendre anonyme n'est pas vider** : nom, prénom et téléphone sont obligatoires (`01:176-179`, `01:184`), et l'e-mail est unique (`01:159`). 💡 Des valeurs neutres au bon format : « non renseigné », un e-mail unique par compte (ex. `anonyme-42@exemple.invalid`).
  - ⚠️ **`is_activated` a deux sens** : « inscription finie » (`F01:28`) et « compte actif ». Il accepte le vide, sans valeur par défaut (`01:161`). 💡 Une date `deactivated_at` (vide = actif) dirait aussi **quand** ; sinon, écrire le sens retenu.
  - ⚠️ **La route DELETE** reste ouverte sur les 18 ressources (`crud_router.py:104-111`) : à retirer pour les comptes, ou à justifier.
- **Q-ACC-09** :
  - 💬 **Airflow le ferait tout seul** : un DAG (un traitement Airflow) se lance selon un **planning**, ou **à la demande** ([doc officielle Airflow](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html), 3.3.2, lue le 2026-10-06). Planifié, l'admin n'a rien à lancer ; il peut relancer à la main après un échec.
  - 💡 **Qui écrit en base** : Airflow, avec son propre compte PostgreSQL, pas le compte de l'admin dans l'application. Les deux se concilient : **l'admin surveille, un compte technique écrit**.
  - ⚠️ Airflow n'est pas dans le projet : l'ajouter touche `docker/docker-compose.yml`, avec l'accord de son responsable. Pour l'analytique, le sujet n'impose aucun outil ETL (`Readme.md:247`).
  - ⚠️ Quel que soit le compte, `estate` ne dit pas qui a créé un bien (`01:507-569`). 💡 Une colonne d'auteur ou de source, si Jeff veut aussi la saisie à la main.
- **Q-ACC-17** :
  - ✅ D'accord : 12 est déjà codé et testé, rien à changer.
  - 💡 En soutenance, ne pas citer le NIST pour 12 (il demande 15 sans second facteur) : dire « valeur du tuto, gardée car l'auth est hors périmètre ».
  - Si Jeff fait retirer le mot de passe (Q-JEF-21), la carte devient sans objet.
- **Q-ACC-20** :
  - 💬 ADR-025 dit : **chaque chasseur a un manager**. La base l'exige (`01:266-267`).
  - Sa **raison écrite** : « pour que seul son manager voie sa paie ». C'est un contrôle d'accès (ENF-03).
  - Or ce contrôle **ne sera pas codé** : l'authentification est hors périmètre (Jeff, 22/09).
  - Réécrire, c'est **garder la règle et changer la raison** : « c'est l'organisation de l'entreprise » (un choix de modélisation).
  - ⚠️ Nouveau : la copie du journal d'ADR de Confluence lue le 2026-10-06 dit ADR-025 **« Annulé »**. Si c'est voulu, la question devient : garder le lien sans ADR, ou le retirer ? Vos réponses Q-SCH-13, Q-MIG-04 et Q-ACC-16 le gardent.
- **Q-INF-05** :
  - 💬 **Pourquoi tester chaque table** : chacune a ses propres règles dans la base (clés, CHECK, UNIQUE). Le routeur commun n'est testé qu'une fois, sans base (`API/tests/test_crud_router.py`) : ça ne prouve pas que les règles de chaque table renvoient la bonne erreur (409 ou 422).
  - 📏 Aujourd'hui, **3 ressources sur 18** sont testées contre une vraie base (`/users`, `/clients`, `/estates`) : 15 ne l'ont jamais été.
  - 💬 **Pourquoi l'argent d'abord** : une erreur y coûte de l'argent (payer le mauvais chasseur, `01:789-795`) ; `chk_refused` a 14 conditions (`01:773-787`).
  - 💬 **Pourquoi après le lot** : ces 3 tables vont changer ; des tests écrits avant seraient à refaire.
- **Q-INF-07** :
  - 💬 **Le seed** : quelques lignes lisibles, écrites à la main, pour la démo.
  - 💬 **Le générateur** : une machine qui fabrique **des milliers** de fausses lignes, pour mesurer si la base tient la charge.
  - Il sert à deux choses : la note d'indexation, avant / après (`md/point-etape-2026-09-21.md:209-211`), et ENF-01, 500 mandats en moins de 2 s (Q-INF-08).
  - Pourquoi après le seed : les deux suivent le même schéma, qui change encore (lot de migration). Écrit trop tôt, il serait à refaire.
  - Pour les biens, l'outil du prof suffit (`outils/generer_annonces.py`) ; clients, mandats et ventes sont à fabriquer nous-mêmes.
- **Q-PRO-05** :
  - ✅ D'accord pour le finir : c'est un **livrable noté** de la phase 2 (`GRILLE-EVALUATION.md:73`).
  - 💡 Le finir **sur le bon schéma** (`docker/init-v2/` : 18 tables, en euros) et **après le lot de migration** : sinon il sera faux une deuxième fois.
  - 🟡 **« Le FIX »** : je ne sais pas ce que c'est. Le lot de migration ? Une version corrective ? À préciser.
  - ➡️ Prévenir Békanty reste utile : son §12 déclare absentes 6 tables qui existent (`md/a-faire-a-la-main-2026-09-21.md:72-74`).
- **Q-PRO-06** :
  - ✅ **Une page par ADR : oui.** Le modèle du prof veut une fiche par décision (`JOURNAL-DE-DECISIONS.md:7`).
  - ⚠️ **Des dossiers par statut : plutôt non.** Un ADR change de statut (proposé, accepté, remplacé) : il faudrait le **déplacer** à chaque fois, et l'ordre des numéros se perdrait.
  - 💡 À la place : **un seul dossier**, les pages numérotées (ADR-001, ADR-002…), le **statut en tête** de chaque page, et **une page d'index** : numéro, titre, statut, date.
  - Le prof : ne jamais effacer un ADR ; un ADR remplacé porte « remplacé par ADR-xxx » (`JOURNAL-DE-DECISIONS.md:72`). L'index le montre d'un coup d'œil.

**Doublons marqués le 2026-10-05** (rien de supprimé, identifiants gardés) :
la réponse de la carte d'origine est **reportée**, pas donnée.

| Doublon | De | Réponse reportée |
|---|---|---|
| Q-MIG-02 | Q-REM-16 | garder l'hypothèse (Q-REM-16 : `hypothese`) |
| Q-ACC-11 | Q-REM-17 | ✅ plus un doublon : répondue le 2026-10-05 (`colonne`), ✏️ changée le 2026-10-06 (une table des factures) |
| Q-ACC-01 | Q-JEF-14 | oui : la question des droits est posée à Jeff |

**Lot de migration qui en découle** (un seul `docker compose down -v`,
numéros de `01` relus le 2026-10-05) :

- statut(s) de fin de `mandate` (Q-REM-02, Q-REM-14 ; `01:405-407`) ;
- `payment.performance_score` (Q-REM-03) et `payment.calculation_details` en JSONB (Q-REM-04) ;
- table `remuneration_parameters`, CHECK `01:758-759` relâchés (Q-REM-05) ;
- `final_rate` dans `chk_refused` (Q-REM-10 ; `01:782-787`) ;
- clé de `sale` vers `parameters_fees` (Q-REM-13) ;
- ~~4 dates et `invoice_reference` sur `payment` (Q-REM-17)~~ — ✏️ 2026-10-07 : facture hors périmètre ; `invoice_reference`, `invoice_submitted_at`, `verified_at` et la table des factures **retirés** ; `announced_at`, `scheduled_for` ✅ gardées à LOT5, statuts de facture retirés ;
- `CHECK (final_rate BETWEEN 0.20 AND 0.60)` (Q-REM-19 ; `01:755`) — ✅ validé par Jeff le 2026-10-07 (Q-JEF-01).
- 2e série du 2026-10-05 :
  - CHECK « exactement 6 mois » à la place de celui de `ends_at` (déjà rédigé dans le TODO U05) (Q-MAN-01 ; `01:412-414`, `01:435-445`) ;
  - Trigger d'exclusivité corrigé (le mandat parent exclu) et activé (Q-MAN-02 ; `01:450-499`) ;
  - Signature : ✏️ 2026-10-06 — `is_client_signed` retiré ; la date et le statut `pending_signature` suffisent ; MAND-0008 et MAND-0016 n'ont plus rien à corriger (Q-MAN-05, Q-MAN-09 ; `01:408`, `01:415`, `01:430-432`) ;
  - 3 TODO annotés « contrôlé par l'API » (commentaires seuls) (Q-MAN-06 ; `01:639-641`, `01:664-668`, `01:789-795`) ;
  - `chk_status_signature` : `'canceled'` permis sans date de signature (Q-MAN-07 ; `01:430-432`) ;
  - `ALTER` retiré de 02 ; 18 clients : adresse « non renseigné », code postal `00000` (Q-SCH-01, Q-SCH-18 ; `02:64-66`, `02:148-165`) ;
  - `proposition_status` : `'signed'` ajouté (Q-SCH-04 ; `01:610-612`) ;
  - `hunter_performance` en journal : `scored_at`, 2 UNIQUE, 1 index ; `valid_from`, `valid_until` et 2 contraintes retirés (Q-SCH-06 ; `01:803-825`) ;
  - `created_at` sur `client`, `hunter`, `real_estate_manager`, `role` (Q-SCH-09 ; `01:169-170`) ;
  - `is_cartet` renommé `is_carte_t` (colonne, modèle, migration) (Q-SCH-10 ; `01:257-260`) ;
  - `country_iso = 'FR'` sur les 2 556 biens, puis CHECK du code postal par pays (Q-SCH-11 ; `01:512-513`, `01:563-567`) ;
  - Eircode sans espace, sur `client` et `criteria` — ✅ confirmé le 2026-10-07 (Q-SCH-12 ; `01:215`, `01:391`) ;
  - Taux de tranche `> 0` (Q-SCH-15 ; `01:697`) ;
  - `parameters_fees` : `effective_from` et `UNIQUE` ; `valid_until` et l'`EXCLUDE` retirés (Q-SCH-17 ; `01:679-686`) ;
- 3e série du 2026-10-06 :
  - `estate.energy_class` rempli depuis `dpe` dans `03` (1 623 biens) ; vide pour les 933 autres (Q-MIG-06 ; `01:521`, `03`) ;
  - Ville, code postal et pays `'FR'` des secteurs dans `criteria` ; 🆕 une colonne quartier facultative (💡 `district`) sur `criteria` et `estate` (Q-MIG-08 ; `01:301-305`, `02:192-208`) ;
  - `budget_min` à NULL sur les 17 critères ; commentaire de `02:189` corrigé (Q-MIG-09 ; `02:189-208`) ;
  - CHECK de format des téléphones (ADR-007), 3 tables — ✏️ 2026-10-07 : les 4 `0000000000` deviennent `+33000000000`, documenté (Q-MIG-07) (Q-PRO-08 ; `01:184-185`, `01:228-229`, `01:246-247`) ;
- 🆕 4e série du 2026-10-07 :
  - 6 mandats échus en `'expired'` (Q-MIG-10) ; mandat 13 rattaché à Nina Girard (Q-MIG-12) ; `suspendu` → `canceled` écrit (Q-MIG-13) ; 17 demandes en `'launched'` (Q-MIG-03) ;
  - colonnes d'énergie vides, `energetic_score` retiré (Q-MIG-05) ;
  - priorité du client en `SMALLINT`, `CHECK` de 1 à 5 (Q-SCH-05) ;
  - colonne d'auteur sur `estate` (Q-ACC-09, Q-JEF-24) ;
  - rôle PostgreSQL en lecture seule (Q14) — 🟡 après la réponse de Jeff sur Discord ;
  - mot de passe gardé, Argon2 (Q-JEF-14) : rien à retirer.
- ✅ Plus rien n'attend Jeff (entretien du 2026-10-07), sauf le rôle en lecture seule (Q14, Discord).
- ✅ Déjà fait, hors lot : Q-REM-01 (prix en `INTEGER`), qui demande lui aussi un `down -v`.

**ADR à écrire — plus tard** ⏸️ : rien n'est rédigé maintenant ; les ADR
s'écrivent une fois **toutes les réponses** reçues (demandé le 2026-10-05).
Simple pense-bête ; 💡 regroupement proposé, numéros donnés sur Confluence.

| ADR | Ce qu'il acte | Questions | État |
|---|---|---|---|
| A | Types monétaires : prix en INTEGER, bornes du barème incluses | Q-REM-01 | décidé et fait le 2026-10-05 — remplace « tout montant en NUMERIC(12,2) » |
| B | Vente perdue : statut de fin du mandat | Q-REM-02, Q-REM-14 | décidé — **amende ADR-024** (motif de refus sur payment), écart à `RCR:100` ; ✅ Jeff : « rien pour personne » (Q-JEF-03, 2026-10-07) ; un seul statut `'lost'` (LOT3, rapport LOT1→LOT5, carte D2) |
| C | Traçabilité du calcul : figer la note et les entrées | Q-REM-03, Q-REM-04, Q-REM-11 | décidé — ✅ confirmé par Jeff (Q-JEF-20, 2026-10-07) |
| D | Paramètres de rémunération en table versionnée | Q-REM-05, Q-REM-19 | décidé — relâche deux CHECK ; Q-REM-19 en ajoute un (20-60 %), ✅ validé par Jeff (Q-JEF-01, 2026-10-07) |
| E | Note recalculée à chaque vente | Q-REM-06 | décidé — écart à `F10:293` ; ✅ validé par Jeff (Q-JEF-17, 2026-10-07) |
| F | Définition des critères de performance | Q-REM-07, Q-REM-08, Q-REM-09, Q-PAR-05 | décidé — ✅ Jeff valide (Q-JEF-08, 09) ; pas de grille : **le groupe propose la sienne** (Q-JEF-05) ; 🟡 sens du critère « visites » (ta note sur Q-REM-07) |
| G | Validation de l'entrée dans le routeur commun | Q-INF-06 | décidé et fait le 2026-10-05 |
| H | X01 : ancienneté et performance majorent le taux | Q-REM-18 | décidé le 2026-10-05 — « il suffit de l'acter » (`09-dec:303-324`) |
| I | Vente reliée à sa grille d'honoraires | Q-REM-13 | décidé — remplace ADR-019 (« sans clé »), ⚠️ « accepté » sur Confluence d'après la copie du 2026-10-06 : un nouvel ADR, pas un amendement |
| J | Étapes du paiement, **sans facture** | Q-REM-17, Q-ACC-11 | ✏️ 2026-10-07 : facture **hors périmètre** (Jeff) — table des factures et 3 colonnes retirées ; ✅ LOT5 : `announced_at` et `scheduled_for` gardées, statuts `'invoice_submitted'` et `'verified'` retirés (rapport LOT1→LOT5, cartes D6, D7) ; **écart au sujet** (`F07:17-27`, `Readme.md:132-133`, `RCR:288`) |
| K | Paramètres proposés, validés par Jeff | Q-PAR-01 à 04, 06 à 08, 10, 11, 13 | ✅ validés par Jeff (Q-JEF-01, 02, 03, 2026-10-07) |
| L | Règles du mandat : 6 mois exacts, exclusivité, renouvellement, annulation | Q-MAN-01, Q-MAN-02, Q-MAN-03, Q-MAN-04, Q-MAN-07 | décidé le 2026-10-05 — ✅ confirmé par Jeff : Q-JEF-06 (annulation), Q-JEF-07 (renouvellement), 2026-10-07 ; ✏️ LOT4 : parent et enfant d'un renouvellement exclus l'un pour l'autre (rapport LOT1→LOT5, carte D3) |
| M | Règles qui croisent plusieurs tables : dans l'API, chacune testée | Q-MAN-06 | décidé le 2026-10-05 |
| N | Localisation sur criteria : remplace ADR-009 | Q-SCH-02, Q-MIG-08 | décidé — et sur ADR-009, la ligne « modifié le …, par l'ADR xx » demandée le 2026-10-05, à la synchro Confluence ; 🆕 la colonne quartier (Q-MIG-08) |
| O | Statuts de la demande et de l'offre | Q-SCH-03, Q-SCH-04 | décidé — ferme D4 et D5 |
| P | Journal des notes du chasseur | Q-SCH-06 | décidé — ferme D9 |
| Q | Grilles d'honoraires « en vigueur à partir du » | Q-SCH-17 | décidé — rend Q-SCH-16 sans objet |
| R | Adresse client : tout-ou-rien, « non renseigné » pour les données reprises | Q-SCH-01, Q-SCH-18 | décidé — code postal `00000` (Q-SCH-18, 2026-10-06) |
| S | Signature du mandat | Q-MAN-05, Q-MAN-09 | décidé le 2026-10-06 — le client seul ; `is_client_signed` retiré ; la date et le statut `pending_signature` suffisent |
| T | Limites assumées du MVP | Q-SCH-07, Q-SCH-08, Q-SCH-14, Q-MAN-08, Q-ACC-14 | décidé — à dire en soutenance |
| U | Données reprises incomplètes : vide (NULL) ou valeur factice documentée | Q-MIG-05, Q-MIG-06, Q-MIG-07, Q-MIG-09 | ✅ décidé le 2026-10-07 : manques voulus (Jeff, Q-JEF-26) ; vide si la colonne l'accepte, sinon valeur factice documentée (Q4) ; anciennes données jamais touchées ; faker forké pour tester |
| V | Effacement d'un compte : désactiver et rendre anonyme | Q-ACC-08, Q-ACC-21 | décidé — ✏️ 2026-10-07 : une **route d'anonymisation** (Jeff, Q-JEF-15) ; 10 ans pour les paiements, durée X **proposée par le groupe** |
| W | Biens : import, et saisie à la main | Q-ACC-09 | ✏️ 2026-10-07 : saisie à la main permise (Jeff, Q-JEF-24), par le chasseur et le manager (Q8) ; colonne d'auteur sur `estate` |
| Y | Authentification : outils côté back, mot de passe, clé d'API | Q-ACC-19, Q-MIG-11, Q-ACC-17, Q-ACC-18 | ✏️ 2026-10-07 : outils d'auth côté back, pas de page de login (Jeff, Q-JEF-14) ; mot de passe gardé, Argon2 ; une clé par programme (Q-JEF-22) ; remplace notre brouillon `md/adr-026-…` (numéro déjà pris) ; 🟡 « dé-annuler » ADR-016 et ADR-026 de Confluence, à vérifier |
| Z | Lien chasseur → manager : la raison réécrite | Q-ACC-20 | ✏️ 2026-10-07 (Q9) : lien gardé, **nouvel ADR** qui remplace ADR-025 (« Annulé » sur Confluence, copie du 2026-10-06) |
| AA | Droits par rôle : réponses du groupe | Q-ACC-02 à 07, 10, 12, 13, 15, Q-PAR-09 | 🆕 2026-10-07 — pas d'ADR propre : la matrice ADR-027 se met à jour ; 🟡 Q-ACC-06, 12, 13 à confirmer avec Jeff |
| AB | Rôle en lecture seule | Q14 du plan | 🆕 2026-10-07 — rôle PostgreSQL + rôle applicatif ; 🟡 à demander à Jeff sur Discord |
| AC | Reprise des anciens mandats : Nina, statuts, échus | Q-MIG-03, Q-MIG-10, Q-MIG-12, Q-MIG-13 | 🆕 2026-10-07 — confirmé par Jeff (Q-JEF-13) ; 💡 peut rejoindre l'ADR U |

Pas d'ADR propre : Q-REM-10 (un CHECK), Q-REM-12 (C3 déjà écrite), Q-REM-15
(seed seul), Q-REM-16 (hypothèse déjà écrite, `02:24-26`), D1 à D4.
Q-PAR-09 va dans le RACI, pas dans un ADR (`RCR:329`).
2e série : pas d'ADR propre non plus pour Q-SCH-09, 10, 11, 12, 15 (un CHECK ou une
colonne chacune) et Q-SCH-13 (un libellé) ; 💡 une ligne chacune dans le README du
schéma. Q-SCH-16 : sans objet.
3e série : pas d'ADR propre pour Q-MAN-05 (dans S), Q-MIG-04 et Q-ACC-16 (le seed), Q-INF-01 à 08 (infrastructure et tests), Q-PRO-08 (il applique ADR-007), Q-PRO-01 (va dans la RACI : Jeff est le PO), Q-PRO-02, 03, 04, 06 et 07 (l'organisation du travail et du journal). La lettre X est sautée : X01 la prend déjà.

**Ce que les réponses du 2026-10-05 changent aux autres cartes** — aucune réponse
n'est changée ; quand deux réponses tirent dans deux sens, la carte le montre :

| Carte | Ce qui change |
|---|---|
| Q-SCH-06 | ✅ Case cochée « tsrange », commentaire « journal » : **le commentaire est retenu** ; une case « Journal des notes » ajoutée. |
| Q-SCH-17 | ✅ Case cochée « Rien », commentaire « par construction » : **le commentaire est retenu** ; une case ajoutée. |
| Q-SCH-16 | ⏭️ **Sans objet** : Q-SCH-17 retire la date de fin des grilles. |
| Q-SCH-12 | ⚠️ **À confirmer** : « Sans espace » laisse deux conventions dans la même colonne. |
| Q-SCH-01 | 📏 Les 18 clients repris n'ont ni adresse ni code postal ; « non renseigné » est refusé pour le code postal → Q-SCH-18. |
| Q-SCH-11 | 📏 2 556 codes postaux sur 2 556 conformes ; mais le pays des biens est vide : à remplir d'abord. |
| Q-MAN-05, Q-MAN-06 | 💬 Réponses à vos deux questions (deux signatures ? schémas à changer ?). |
| Q-MAN-08 | ✏️ **Réécrite**, sources du prof relues ; recommandation passée à « Reporter ». |
| Q-MAN-09 | 🆕 **Nouvelle** : une signature ou deux ? (ton commentaire sur Q-MAN-05). |
| Q-SCH-18 | 🆕 **Nouvelle** : le code postal des 18 clients repris (ta réponse à Q-SCH-01). |
| Q-INF-02 | 🔄 **Réduite** : il ne reste que Q-INF-03. |
| Q-PRO-02 | 🔄 **Réduite** : 3 réponses sur 5 confirmées ; restent la Q3 à acter (ADR-024) et la Q4 (Q-INF-03). |
| Q-INF-03 | 🔑 La dernière question ouverte du seed et du point d'étape. |
| Q-PRO-03 | 🔄 9 ADR de plus au pense-bête (L à T). |
| Q-PRO-06 | 🔗 La ligne sur ADR-009 (Q-SCH-02) et les ADR L à T, au même passage. |
| Q-MIG-03 | 🔗 Statuts actés (Q-SCH-03) ; 2 mandats contradictoires à corriger d'abord (Q-MAN-05) ; 🆕 une case « au mandat signé ». |
| Q-MIG-08 | ✅ Le lieu reste sur criteria (Q-SCH-02) : c'est là que les secteurs doivent arriver. |
| Q-MIG-09 | 🆕 Une case « laisser le minimum vide ». |
| Q-MIG-07, Q-PRO-08 | 🔗 Même logique que Q-SCH-01 ; un format `+33…` refuserait les 4 numéros 0000000000. |
| Q-ACC-20 | ⚠️ Relecture : ADR-025 est déjà « accepté » sur Confluence (22/09) ; ENF-03 est un exemple dans le cahier des charges, mais une exigence dans les règles de calcul. La carte montre les deux lectures. |
| Q-ACC-14 | 🔗 Cohérente avec Q-SCH-08 (reporter au parcours IA). |
| Q-ACC-11 | ✅ Répondue : rejoint Q-REM-17 ; ce n'est plus un doublon. |
| Q-PRO-05 | 🔗 Le lot de migration grossit : l'écart avec le CDC v2.0 aussi. |

**Ce que les réponses du 2026-10-06 changent aux autres cartes** — ✏️ deux
réponses changent (Q-MAN-05, Q-ACC-11) ; les autres s'ajoutent :

| Carte | Ce qui change |
|---|---|
| Q-MAN-05 | ✏️ Réponse **changée** : « Supprimer la colonne », à la suite de Q-MAN-09. Le CHECK case ↔ date n'a plus d'objet. |
| Q-ACC-11 | ✏️ Réponse **changée** : une table des factures, à confirmer avec Jeff (Q-JEF-23). |
| Q-REM-17 | 🔗 3 de ses 5 colonnes passent à la table des factures (Q-ACC-11). |
| Q-REM-13 | ⚠️ ADR-019 est « accepté » dans la copie du journal du 2026-10-06, pas « proposé » : un nouvel ADR le remplace, on ne l'amende pas. |
| Q-MIG-03 | 🔗 Ta note rejoint Q-JEF-13. ⚠️ Sans la case « signé », la voie « au mandat signé » ne trie plus les 2 mandats annulés. |
| Q-MIG-05, Q-MIG-06 | 💬 Avis : vide (NULL) plutôt qu'une valeur factice, comme ta réponse Q-MIG-09. Les colonnes d'énergie refusent 0. |
| Q-MIG-07 | 🔗 Q-PRO-08 (« Harmoniser ») : la valeur factice doit passer le format d'ADR-007. `+33000000000`, pas `+330000000000`. |
| Q-MIG-11, Q-ACC-17, Q-ACC-18 | 🔗 Toutes attendent Q-JEF-21 : garder un mot de passe ? |
| Q-ACC-20 | ⚠️ ADR-025 « Annulé » dans la copie du journal du 2026-10-06 : à vérifier avant de le réécrire. |
| Q-PRO-04 | ⚠️ ADR-016 : « annulé le 06/10 » (ta note), « accepté » dans la copie de 11 h 16 : à vérifier. |
| Q-PRO-02 | 🔄 Q4 répondue (Q-INF-03) : il ne reste que Q3 (ADR-024). |
| Q-INF-02 | 🔄 Toutes ses dépendances sont répondues ; il attend l'entretien avec Jeff, puis le lot de migration. |
| Q-SCH-08, Q-ACC-14, Q-PRO-07 | 🔗 Cartes 📋 PO : le PO, c'est Jeff (Q-PRO-01) ; à lui confirmer. |

---

## 1. Toutes les questions, par thème

### A. Rémunération — champs absents ou ambigus en base

C'est le cœur de la demande. La calculette lit une `Vente`
(`rem.py:128-140`) et rend une `Remuneration` (`rem.py:143-159`).
Voici ce qui ne colle pas avec la base.

#### Q-REM-01 — Borne haute d'une tranche du barème : incluse ou exclue ?

- ✅ **Répondue et faite le 2026-10-05 : « Prix en INTEGER + bornes '[]' (tranché le 2026-10-05) »** · 👥 **Groupe**
- **Constat** :
  - la base **excluait** la borne haute (`'[)'`) ; passée en `'[]'` le 2026-10-05 (`01:710`, `01:717`) ;
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

- ✅ **Répondue le 2026-10-02 : « Pas de vente : le mandat prend un statut de fin »** · 👥 **Groupe**, après 🧑‍💼 **Jeff** (Q-JEF-03)
- **Constat** :
  - le code a **3** origines, dont `AUTRE_AGENCE` (`rem.py:54-57`) ;
  - la base n'en a que **2** : `'hunter'`, `'client_alone'` (`01:657-658`) ;
  - et `sale.fees_amount` est `NOT NULL CHECK (> 0)` (`01:656`).
- ➡️ Si l'entreprise **ne touche rien** sur une vente faite par une autre
  agence, on ne peut **pas** enregistrer cette vente : il n'y a pas
  d'honoraires à saisir.
- ⚠️ Même problème pour un mandat **non exclusif** où le **client trouve seul**
  (`'client_alone'`) : l'entreprise touche-t-elle des honoraires ?
- **Options** :
  - A — ajouter `'other_agency'` au `CHECK`, et accepter des honoraires à **0** quand l'entreprise ne touche rien
    (passer `sale.fees_amount CHECK (> 0)` à `>= 0`, `01:656`) ;
  - B — ne pas créer de `sale` : le mandat passe à un statut de fin (ex. `'lost'`, à ajouter) ;
  - C — ne rien stocker.
- 💡 **Recommandation : A**, la forme exacte dépend de Q-JEF-03.
  - Le refus doit être **tracé** sur `payment` (ADR-024, `refusal_reason = 'out_of_scope'`).
    Le sujet insiste sur « l'intérêt de stocker le motif » (`RCR:100`).
  - Or un `payment` exige une vente : `id_sale NOT NULL` (`01:760`).
  - ❌ B rangerait deux refus que le code traite pareil (`rem.py:174`) de deux façons différentes.

#### Q-REM-03 — Le score de performance doit-il être figé sur le paiement ?

- ✅ **Répondue le 2026-10-02 : « Ajouter payment.performance_score »** · 👥 **Groupe**
- **Constat** :
  - `F10:275-287` exige de **figer** les éléments du calcul à la date de l'acte ;
  - `payment` fige les taux (`01:746-759`) mais **pas le score** ;
  - `hunter_performance.score` (`01:802`) est un score **par période**,
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

- ✅ **Répondue le 2026-10-02 : « Une colonne JSONB calculation_details »** · 👥 **Groupe**
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

- ✅ **Répondue le 2026-10-02 : « Table versionnée + relâcher les CHECK »** · 👥 **Groupe**
- ✏️ **Précisée le 2026-10-07 (LOT6)**, deux points que la réponse laissait ouverts :
  - versions : **`effective_from` + `UNIQUE`**, comme `parameters_fees` (Q-SCH-17), à la place de `valid_from` / `valid_until` de l'option A ;
  - bornes relâchées : **domaine d'un taux** — ancienneté de 0 à 1, performance de −1 à 1 ; justifié par `RCR:59` (paramètres), `RCR:199` (a ≥ 0), `RCR:203` (1 + a + p > 0).
- **Constat** :
  - **aucune table** pour les poids, les paliers, les notes, les points, la
    fenêtre de 12 mois (`rem.py:92-105`) ;
  - ni pour le taux par année, le pivot, l'amplitude, le plancher, le plafond (`rem.py:108-116`) ;
  - deux de ces valeurs sont **gravées dans des `CHECK`** :
    - `seniority_rate BETWEEN 0 AND 0.10` (`01:758`) ;
    - `performance_rate BETWEEN -0.20 AND 0.20` (`01:759`).
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

- ✅ **Répondue le 2026-10-02 : « Recalculer à chaque vente »** · 👥 **Groupe**, à confirmer par 🧑‍💼 **Jeff** (Q-JEF-17)
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

- ✅ **Répondue le 2026-10-02 : « Visites du client, tous les biens du mandat, jusqu'au jour de l'acte »** · 🧑‍💼 **Jeff** (Q-JEF-08), le groupe écrit la requête
- **Constat** :
  - `visit.visitor_type IN ('hunter', 'client')` (`01:635`) ;
  - `F10:259` : « le client a effectué 5 visites » ;
  - le sujet cite les deux sortes de visites (`Readme.md:100-101`).
- **Questions** : quel type ? tous les biens du mandat, ou seulement le bien vendu ? avant l'acte seulement ?
- 💡 **Recommandation** : visites `'client'`, **tous les biens** du mandat, datées **au plus tard** le jour de l'acte.
  - C'est la lecture littérale de `F10:259`.
  - Tous les biens : le critère mesure le travail du chasseur, pas le bien final.

#### Q-REM-08 — Quelles ventes comptent dans « ventes sur 12 mois » ?

- ✅ **Répondue le 2026-10-02 : « Les ventes non refusées »** · 🧑‍💼 **Jeff** (Q-JEF-09)
- **Constat** : `RCR:470` exclut la vente en cours ; rien d'autre n'est dit.
- **Questions** : une vente refusée compte-t-elle ? une vente `client_alone` ?
- 💡 **Recommandation** : les ventes des mandats du chasseur dont le paiement
  **n'est pas refusé**, dans les 12 mois **avant** l'acte, vente en cours exclue.
  - « Ventes réussies » (`Readme.md:86`) = celles qui lui ouvrent un droit.

#### Q-REM-09 — Quels mandats comptent dans « mandats sur 12 mois » ?

- ✅ **Répondue le 2026-10-02 : « Signés, sans les renouvellements »** · 🧑‍💼 **Jeff** (Q-JEF-09)
- **Constat** : `F10:298` compte un mandat expiré. Rien sur `canceled`, `pending_signature`, `renewed`.
- 💡 **Recommandation** : les mandats **signés** (`signature_date` non vide)
  dans la fenêtre, **sans les renouvellements** (`id_mandate_parent IS NULL`).
  - Sinon un mandat renouvelé 3 fois compte 4 fois.
  - 🟡 Le mandat **annulé** : pas de recommandation. Le compter pousse à
    signer puis annuler pour gagner des points (`mandats × 10`, `rem.py:214`). Jeff tranche.

#### Q-REM-10 — `final_rate` doit-il être obligatoire sur un paiement non refusé ?

- ✅ **Répondue le 2026-10-02 : « L'ajouter à chk_refused »** · 👥 **Groupe**
- **Constat** : `chk_refused` exige `base_rate`, `seniority_rate`,
  `performance_rate` non vides, mais **pas** `final_rate` (`01:782-787`).
  - `payment_model.py:11-12` dit « NULL tant qu'il n'est pas arrêté », sans règle derrière.
- 💡 **Recommandation : l'ajouter à `chk_refused`.**
  - Le premier statut est `'announced'` : le montant est déjà annoncé, donc le taux est connu.
  - Il n'existe aucun état « calculé mais pas arrêté ».

#### Q-REM-11 — Qui garantit `montant = taux × honoraires` ?

- ✅ **Répondue le 2026-10-02 : « L'API seule, avec un test d'intégration »** · 👥 **Groupe**
- **Constat** : rien ne vérifie `amount`, `final_rate` ni `fees_amount`
  entre eux. L'arrondi « au demi supérieur » n'existe que dans le code.
- **Options** : trigger, colonne générée, ou API seule.
- 💡 **Recommandation : l'API seule**, avec un test d'intégration.
  - La formule a un plancher, un plafond et un arrondi : un trigger la dupliquerait.
  - Une seule source de vérité : `rem.py`, déjà testé sur 55 cas.

#### Q-REM-12 — Les honoraires sont rangés sur `sale`, qu'on peut modifier

- ✅ **Répondue le 2026-10-02 : « Appliquer C3 dans sale_service »** · 👥 **Groupe**
- **Constat** : `sale.fees_amount` (`01:656`) reste modifiable après paiement (`PUT /sales/{id}`).
- ✅ **Déjà prévu** : la contrainte C3 dit « Refuser toute modification de `fees_amount` »
  (`09-contraintes-a-coder.md:110-117`), par trigger ou dans le service.
- ⚠️ Le sujet range les honoraires **sur le paiement** : « prix_acte, honoraires » (`RCR:286`).
- 💡 **Recommandation : appliquer C3**, ou copier `honoraires` sur `payment` en même temps que le score (Q-REM-03).
  - La copie suit le sujet à la lettre, et rend le paiement autonome.

#### Q-REM-13 — Lien vers la ligne de `parameters_fees` utilisée ?

- ✅ **Répondue le 2026-10-05 : « Ajouter une clé »** (voir §0) — avant : 🔵 appliqué, pas acté : pas de clé, choix d'ADR-019 (« proposé »)
- **Constat** : `parameters_fees.id` n'est référencé nulle part.
- 💡 **Recommandation : garder sans clé**, et accepter ADR-019.
  - Le montant est déjà figé dans `sale.fees_amount`.
  - La ligne se retrouve par la date : `EXCLUDE` (`01:685-686`) garantit qu'il y en a **au plus une** (voir Q-SCH-17 pour les trous).

#### Q-REM-14 — Le mandat « perdant » de deux mandats non exclusifs

- ✅ **Répondue le 2026-10-05 : « Ajouter un statut de fin (ex. 'lost') »** (voir §0) · 👥 **Groupe**
- **Constat** : `F10:52-56` : un seul chasseur est payé ; « "Bruno" ne perçoit aucune rémunération » (`F10:56`).
  - `sale.id_mandate` est `UNIQUE` (`01:659`) : le perdant n'a **pas** de vente.
- 💡 **Recommandation** : le mandat perdant prend un **statut de fin** (à ajouter, ex. `'lost'`).
  - Les statuts actuels sont `active`, `completed`, `expired`, `renewed`, `canceled`, `pending_signature` (`01:405-407`) :
    aucun ne dit « vendu par un autre ».

#### Q-REM-15 — Date de début du barème par défaut

- ✅ **Répondue le 2026-10-05 : « Reculer à 2025, dans le seed seulement »** (voir §0) — avant : 🟠 position de Sébastien, « reculer à 2025 » · 👥 **Groupe**
- **Constat** : `rem.py:298` : `debut = date(2026, 1, 1)`.
  - Une vente du seed datée de 2025 lèverait `BaremeIntrouvable`.
- 💡 **Recommandation : reculer, dans le seed seulement.**
  - Le code du sujet reste intact ; les 55 cas aussi.

#### Q-REM-16 — Ancienneté : quelle date d'entrée ?

- ✅ **Répondue le 2026-10-05 : « Garder l'hypothèse, la dire en soutenance »** (voir §0) ; reste posé à 🧑‍💼 **Jeff** (Q-JEF-10)
- **Constat** : `hire_date` = date de création du compte (`02:24-26`).
  - Le sujet : « Dépend de la date d'entrée du chasseur, donnée RH » (`RCR:762`).
- 💡 **Recommandation** : garder l'hypothèse, la dire en soutenance, et demander à Jeff si une vraie date existe.

#### Q-REM-17 — Statuts du paiement : quelles dates garder ?

- ✅ **Répondue le 2026-10-05 : « 4 colonnes de date + invoice_reference »** (voir §0) · 👥 **Groupe**
- **Constat** : `F07:10-34` décrit 5 étapes. La base n'a que `created_at` et `paid_at` (`01:724`, `01:734`).
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

- ✅ **Répondue le 2026-10-05 : « Acter B dans un ADR maintenant »** (voir §0) — avant : 🔵 appliqué, pas acté · 👥 **Groupe**
- **Constat** :
  - le schéma et le code **majorent le taux** (option B) : `payment.seniority_rate`, `performance_rate` (`01:758-759`) ;
  - `F10:201` le confirme ;
  - `09-dec:303-324` : « Il suffit de l'acter, dans un ADR. »
- 💡 **Recommandation : acter B dans un ADR, maintenant.**
  - ⚠️ Plusieurs documents disent que X01 **bloque** le branchement de la calculette
    (`08-etat.md:190`, `API/README.md:147`, `rapport-tests.md:250`). C'est trop fort : la décision est faite de fait.

#### Q-REM-19 — Borner le taux final entre 20 et 60 % en base (R21) ?

- ✅ **Répondue le 2026-10-05 : « Activer le CHECK 0,20-0,60 »**, contre ma recommandation ci-dessous (voir §0 : tension avec Q-REM-05) · 👥 **Groupe**
- **Constat** : `01:747-754` propose `CHECK (final_rate BETWEEN 0.20 AND 0.60)`.
  `01:134-137` range R21 parmi les décisions ouvertes.
- 💡 **Recommandation : ne pas activer R21.**
  - Le **bornage** est une règle (`F10:201` ; `01:753-754` : « la règle de bornage, elle, est bien métier »).
  - Mais **20 % et 60 %** sont des **paramètres** proposés (`F10:3-5`) : ils ne vont pas dans un `CHECK`.
  - Les graver dans un `CHECK` refait l'erreur relevée en Q-REM-05.
  - Le code borne déjà le taux (`rem.py:264`).

### B. Rémunération — les paramètres (valeurs de Jeff)

Toutes ces valeurs sont des **propositions du sujet** (`RCR:59`, `F10:3-5`).
Le code les porte déjà dans `parametrage_par_defaut`.

💡 **Recommandation commune** : les présenter à Jeff **en une fois**, adopter
les valeurs du sujet par défaut, et noter dans un ADR « paramètres proposés,
validés par Jeff le … ». Elles sont toutes listées en **partie 2**.

| Id | Question | Proposé par le sujet | Source | Réponse du groupe (2026-10-05) |
|---|---|---|---|---|
| Q-PAR-01 | Honoraires : fixe et pourcentage | 3 000 € + 2,5 % | `RCR:321` (D1) | ✅ sujet |
| Q-PAR-02 | Non exclusif, client trouve seul : rien, ou indemnité ? | rien, motif tracé | `RCR:322` (D2), `RCR:100` | ✅ rien |
| Q-PAR-03 | Barème par palier ou progressif ? | palier | `RCR:323` (D3) — ⚠️ voir plus bas | ✅ palier |
| Q-PAR-04 | Fenêtre des critères de volume | 12 mois glissants | `RCR:324` (D4) | ✅ 12 mois |
| Q-PAR-05 | Ventes et mandats séparés, ou taux de transformation ? | séparés | `RCR:325` (D5) | ✅ **transfo** — grille à demander |
| Q-PAR-06 | Poids des 5 critères | 25 / 10 / 25 / 15 / 25 | `RCR:326` (D6) | ✅ sujet |
| Q-PAR-07 | Effet de l'ancienneté et de la performance | +10 % max, ±20 % | `RCR:327` (D7) | ✅ sujet |
| Q-PAR-08 | Garder le plancher de 20 %, qui ne mord jamais ? | oui | `RCR:328` (D8) | ✅ garder |
| Q-PAR-09 | Qui crée un barème propre à un chasseur ? | à définir | `RCR:329` (D9) | ✅ manager |
| Q-PAR-10 | Bornes et taux des tranches | 30 / 35 / 40 / 45 / 50 % | `RCR:171-177` | 🟡 |
| Q-PAR-11 | Arrondi du score (1 déc.) et du taux (4 déc.) | demi supérieur | `RCR:223-229` | 🟡 |
| Q-PAR-13 | Grilles de notes (délai, visites, exclusivité 100/60) | `F10:107-138` | `RCR:143-147` | 🟡 |

**Règles fixées par le sujet — à confirmer, pas à choisir** :

- ✅ **Montant arrondi au centime, au demi supérieur** : c'est une `Règle:` de
  `F10:253` (« arrondi au centime au demi supérieur »). `01:725` dit aussi « règle officielle ».
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

- ✅ **Répondue le 2026-10-05 : « Activer »** · 👥 **Groupe**
- **Constat** : le `CHECK` actuel n'impose que l'ordre des dates (`01:412-414`).
  Un mandat « peut durer 10 ans ou 1 jour » (`01:435-445`).
- 💡 **Recommandation : activer.**
  - « 6 mois renouvelable » est une **règle** du sujet, pas un paramètre (`RCR:57`).
  - ⚠️ Cas de fin de mois : 31/08 + 6 mois. PostgreSQL rend le **28 ou 29/02**.
    À écrire dans l'ADR, pour que l'API calcule pareil.

#### Q-MAN-02 — Activer l'exclusivité (U02) — et le cas du mandat annulé (D7)

- ✅ **Répondue le 2026-10-05 : « Corriger, activer, l'annulation libère tout de suite »** · 👥 **Groupe** pour le trigger, 🧑‍💼 **Jeff** pour D7 (Q-JEF-06)
- **Constat** : trigger écrit et commenté (`01:450-499`). D7 :
  « un mandat 'canceled' libère-t-il le client tout de suite ? » (`01:467-469`).
- ❌ **Piège** : tel qu'écrit, le trigger **bloquerait le renouvellement** d'un mandat exclusif.
  - Les plages se comparent en `'[]'` (`01:487-488`), et rien n'exclut le mandat parent (`01:481-488`).
  - Un renouvellement signé à l'échéance (`F00:40`) touche la date de fin du parent : il serait refusé.
- 💡 **Recommandation : corriger, puis activer, avec D7 = B** (l'annulation libère tout de suite).
  - D'abord exclure le parent : `m.id IS DISTINCT FROM NEW.id_mandate_parent`, ou les mandats déjà finis.
  - ⚠️ Pas `m.id <> NEW.id_mandate_parent` : sans parent, cela vaut `NULL`, et le trigger ne bloquerait **plus rien**.
  - Le brouillon du trigger fait déjà B (`status <> 'canceled'`).
  - Bloquer un client sur un mandat annulé n'a pas de sens métier évident ; Jeff confirme.

#### Q-MAN-03 — Renouvellement : combien de fois, et seulement sans vente ?

- ✅ **Répondue le 2026-10-05 : « Imposer « sans vente » dans l'API, sans limite de nombre »** · 🧑‍💼 **Jeff** (Q-JEF-07), puis 👥 **Groupe**
- **Constat** :
  - « renouvelable si aucune vente n'a abouti » (`F00:40`) : rien ne l'impose en base (U07) ;
  - le nombre de renouvellements n'est dit nulle part ;
  - la grille du délai va jusqu'à « >48 sem. » (`RCR:143`) : elle suppose plusieurs renouvellements.
- 💡 **Recommandation** :
  - imposer « sans vente » dans `mandate_service` (pas en SQL : la règle croise deux tables) ;
  - pas de limite au nombre, tant que Jeff n'en donne pas.

#### Q-MAN-04 — Après un renouvellement : quel mandat la vente vise, et d'où part le délai ?

- ✅ **Répondue le 2026-10-05 : « Valider les deux »** · 👥 **Groupe**
- **Constat** : `md/point-etape-2026-09-21.md` Q5 : « La vente pointe vers le nouveau mandat ».
  Le délai (R08) part de la **première** signature (`09-contraintes-a-coder.md:207-210`).
- 💡 **Recommandation : valider les deux.**
  - Le nouveau mandat est le seul valide à la date de l'acte.
  - Le délai depuis la 1re signature est la seule lecture compatible avec la grille « >48 sem. ».
  - ➡️ Le code devra **remonter la chaîne** `id_mandate_parent` pour trouver la 1re date.

#### Q-MAN-05 — `is_client_signed` : doublon de `signature_date` ?

- ✅ **Répondue le 2026-10-06 : « Supprimer la colonne »** (✏️ changée ; le 2026-10-05 : « Poser un CHECK d'égalité » ; détail : partie 0) · 👥 **Groupe**
- **Constat** : aucune règle n'utilise la colonne. `02:218` insère un mandat
  avec une date de signature **et** `is_client_signed = false`.
- 💡 **Recommandation** : la supprimer, ou poser `CHECK (is_client_signed = (signature_date IS NOT NULL))`.
  - Deux colonnes qui disent la même chose finissent par se contredire : `02:218` le montre déjà.
- ➡️ **Suite du 2026-10-05** :
  - 💬 Ta question : faut-il aussi la signature du chasseur ? ✅ L'idée est juste : un mandat est un contrat à deux.
  - ⚠️ Le sujet ne parle que de la signature du **client** : `Readme.md:98` et `01_particulier_demande_et_compte.feature:35-36`. L'ajouter est un **choix à nous**, à dire en soutenance.
  - ➡️ Posée en Q-MAN-09 : 💡 deux dates plutôt que deux cases oui/non.
  - 📏 La ligne contradictoire existe **deux fois** : `MAND-0008` (`02:218`) et `MAND-0016` (`02:225`), annulés, `is_client_signed = false`, mais avec une date de signature.

#### Q-MAN-06 — Règles qui croisent plusieurs tables (non imposées)

- ✅ **Répondue le 2026-10-05 : « Toutes dans l'API, chacune testée »** · 👥 **Groupe**
- **Constat**, trois TODO dans `01` :
  - une visite peut précéder la signature du mandat (`01:639-641`) ;
  - une vente peut tomber hors de la validité du mandat, ou sur un mandat non signé (`01:664-668`) ;
  - « on peut aujourd'hui payer un chasseur qui n'est PAS celui du mandat » (`01:789-795`) ;
  - un paiement peut viser un barème **pas en vigueur** à la date de l'acte (`01:791-792`),
    ou le barème **propre à un autre chasseur**.
- 💡 **Recommandation : toutes dans l'API**, chacune avec un test d'intégration.
  - Les deux dernières sont les plus graves : c'est de l'argent versé à tort.
- ➡️ **Suite du 2026-10-05** :
  - 💬 Ta question : faut-il mettre à jour les schémas ?
  - **Les tables : non.** Les règles vivent dans l'API, avec leurs tests ; aucune colonne ne change.
  - **Trois commentaires de 01 : oui.** Ils décrivent ces règles comme « trigger ou API » : `01:639-641` (visite), `01:664-668` (vente), `01:789-795` (paiement). À annoter « contrôlé par l'API (Q-MAN-06) », dans le lot.
  - **Les diagrammes : non.** Ces règles se rangent dans `09-contraintes-a-coder.md`, pas dans le MCD.
  - ⚠️ À ne pas oublier dans l'API : « Un acte signé après cette date n'ouvre aucun droit, **sauf renouvellement du mandat** » (`RCR:98`). Le TODO D3 de `01:669-672` le rappelle.

#### Q-MAN-07 — Annuler un mandat jamais signé : impossible

- ✅ **Répondue le 2026-10-05 : « Autoriser 'canceled' sans date de signature »** · 👥 **Groupe**
- **Constat** : `chk_status_signature` exige une date de signature dès que le
  statut n'est plus `pending_signature` (`01:430-432`).
  - ➡️ Un mandat en attente ne peut pas passer à `canceled` sans une date **inventée**.
- 💡 **Recommandation** : autoriser `canceled` **sans** date de signature dans ce `CHECK`.
  - Un client qui renonce avant de signer est un cas normal.

#### Q-MAN-08 — Réaffecter une demande refusée : faut-il se souvenir de qui a refusé ?

- ✅ **Répondue le 2026-10-06 : « Reporter »** (✏️ réécrite le 2026-10-05 ; détail : partie 0) · 👥 **Groupe**
- **Constat** :
  - Le Readme dit seulement que le chasseur « peut ne pas l'accepter » (`Readme.md:124`) ; dans son schéma, un refus mène à **Fin** (`Readme.md:140`).
  - La réaffectation vient d'une user story du prof : la demande « **peut** être réaffectée à un autre chasseur » (`04_chasseur_prise_en_charge_demande.feature:21`). « Peut », pas « doit ».
  - Le prof présente ses stories comme une « synthèse de travail », pas un livrable officiel (`Readme.md:50`).
  - ⚠️ Notre contrainte C8 écrit « **doit** aller à un autre chasseur » (`09-contraintes-a-coder.md:244`) : plus fort que la story.
  - Une demande ne garde qu'**un** chasseur (`search_request.id_hunter`, `01:282`) : à la réaffectation, celui qui a refusé est oublié.
- **Options** :
  - Une table search_request_refusal (demande, chasseur, date) — Une table ; l'API refuse de réaffecter à un chasseur qui a déjà dit non.
  - Reporter — Rien maintenant ; la réaffectation attend que l'affectation soit décidée.
- 💡 **Recommandation : reporter.**
  - ➕ Rien à coder tant que l'affectation n'est pas décidée. Le statut 'rejected', acté avec les trois autres en Q-SCH-03, dit déjà qu'une demande a été refusée.
  - ➖ Si on réaffecte un jour, la demande peut revenir au chasseur qui l'a refusée : à dire comme limite en soutenance.

#### Q-MAN-09 — Signature du mandat : par le client seul, ou par les deux parties ?

- ✅ **Répondue le 2026-10-06 : « Le client seul, comme le sujet »** — le commentaire fait foi : `is_client_signed` retiré, pas de CHECK d'égalité (🆕 née le 2026-10-05 du commentaire sur Q-MAN-05 ; détail : partie 0) · 👥 **Groupe**
- **Constat** :
  - Le sujet ne parle que de la signature du client : `Readme.md:98`, `01_particulier_demande_et_compte.feature:35-36`.
  - Aujourd'hui : une case `is_client_signed` (`01:415`) et une date `signature_date` (`01:408`) ; la date fait partir les 6 mois (Q-MAN-01).
  - Deux mandats repris se contredisent déjà : `02:218` et `02:225` (case à non, date remplie).
- **Options** :
  - Deux dates : client_signed_on et hunter_signed_on — signature_date = la plus tardive des deux ; is_client_signed retiré ; un CHECK les relie.
  - Deux cases oui/non : is_client_signed et is_hunter_signed — Une colonne ajoutée ; un CHECK : date remplie si et seulement si les deux cases sont à oui.
  - Le client seul, comme le sujet — Q-MAN-05 tel quel : un CHECK d'égalité.
- 💡 **Recommandation : deux dates : client_signed_on et hunter_signed_on.**
  - ➕ On sait qui a signé et quand ; rien ne peut se contredire, un CHECK le garantit.
  - ➖ Deux colonnes de plus ; modèle, migration 02 et API à toucher ; un ajout au sujet, à justifier à l'oral.

### D. Schéma — autres questions

| Id | Question | Statut | Qui | Source |
|---|---|---|---|---|
| Q-SCH-01 | Valider l'assouplissement de `ck_client_address_all_or_nothing` | ✅ | 👥 | `08-etat.md:119-122`, `02:64-66` |
| Q-SCH-02 | N2 : la localisation sur `search_request` ou `criteria` ? | ✅ | 👥 | `01:298-300`, `09-dec:226-248` |
| Q-SCH-03 | D4 : statuts d'une demande de recherche | ✅ | 👥 | `09-dec:328-347`, `01:287-288` |
| Q-SCH-04 | D5 : état manquant d'une offre (« signée, pas envoyée ») | ✅ | 👥 | `09-dec:351-370` |
| Q-SCH-05 | D6 : échelle de priorité du client | 🟡 | 🧑‍💼 | `01:624-627`, ADR-027 Q9 (`md/adr-027-…:144`) |
| Q-SCH-06 | D9 : deux scores le même jour | ✅ | 👥 | `01:817-820`, `09-dec:411-428` |
| Q-SCH-07 | D10 : table des rendez-vous (`U29`, `F04`) | ✅ | 👥 | `09-dec:432-441` |
| Q-SCH-08 | D11, D12 : pertinence (`F05`), types d'offre (`F07`) | ✅ | 📋 | `09-dec:449-464` |
| Q-SCH-09 | `created_at` absent de 4 tables | ✅ | 👥 | `01:169-170` |
| Q-SCH-10 | Renommer `is_cartet` en `is_carte_t` | ✅ | 👥 | `01:257-260` |
| Q-SCH-11 | Code postal non contrôlé sur `estate` | ✅ | 👥 | `01:563-565` |
| Q-SCH-12 | Eircode avec espace | ⚠️ à confirmer | 👥 | `01:55-59` |
| Q-SCH-13 | Libellé du 2e lien « Manages » | ✅ | 👥 | `docker/init-v2/README.md:429-433` |
| Q-SCH-14 | Pas d'historique des changements de manager | ✅ | 👥 | `docker/init-v2/README.md:477-479` |
| Q-SCH-15 | Taux de tranche `>= 0` contre taux de base `> 0` | ✅ | 👥 | `01:697`, `01:746` |
| Q-SCH-16 | `parameters_fees` sans `valid_until > valid_from` | ⏭️ sans objet | 👥 | `01:676` |
| Q-SCH-17 | Trous entre deux périodes de paramètres | ✅ | 👥 | `09-contraintes-a-coder.md` C2 |
| Q-SCH-18 | 🆕 Code postal des 18 clients repris, avec le tout-ou-rien gardé | ✅ | 👥 | `02:148-165`, `01:186`, `01:210` |

✅ **Réponses du 2026-10-05 et du 2026-10-06** : voir la partie 0. Les recommandations ci-dessous
datent d'avant ; **la réponse fait foi**.

💡 **Recommandations** :

- **Q-SCH-01** : **valider**, et déplacer l'`ALTER` dans `01`.
  - Sinon 18 clients perdent leur ville.
- **Q-SCH-02** : garder **`criteria`**, mais **écrire un ADR qui remplace ADR-009**.
  - ⚠️ ADR-009 est **accepté** et place la localisation sur `search_request` (`01:298`).
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
- **Q-SCH-16** : **ajouter**, comme sur `commission_scale` (`01:704-705`).
- **Q-SCH-17** : contrôle **dans l'API**, à l'écriture.
  - La base garantit « au plus une » ligne, pas « exactement une ».
- **Q-SCH-18** (🆕) : **un code factice `00000`**, documenté.
  - Le tout-ou-rien reste entier, comme Q-SCH-01 le veut ; même logique que les téléphones `0000000000` (Q-MIG-07).

### E. Migration — hypothèses à confirmer

| Id | Hypothèse | Qui | Source |
|---|---|---|---|
| Q-MIG-01 | Sens de `taux_commission` (2,00 à 3,25) | 🧑‍💼 | `docker/init-v2/README.md:145-147` |
| Q-MIG-02 | 🔁 **Doublon de Q-REM-16** (2026-10-05) — `hire_date` = date de création du compte | 🧑‍💼 | `02:24-26` |
| Q-MIG-03 | 📝 `search_request.status = 'confirmed'` | 👥 | `docker/init-v2/README.md:161-174` |
| Q-MIG-04 | ✅ Manager fictif (user 25) | 👥 | `docker/init-v2/README.md:176-192` |
| Q-MIG-05 | 📝 `energetic_score` retiré | 👥 | `08-etat.md:123-126` |
| Q-MIG-06 | ✅ Remplir `energy_class` depuis `dpe` | 👥 | `docker/init-v2/README.md:90-91` |
| Q-MIG-07 | 📝 Téléphones `0000000000` (3 clients + le manager) | 👥 | `02:143-145` |
| Q-MIG-08 | ✅ Secteurs non migrés : `criteria.town` vide 17 fois sur 17 | 👥 | `02:70-72` |
| Q-MIG-09 | ✅ `budget_min = budget_max` 17 fois sur 17 | 👥 | `md/point-etape-2026-09-21.md` §7 |
| Q-MIG-10 | 6 mandats « actif » déjà échus au 25/07/2026 | 🧑‍💼 | `md/point-etape-2026-09-21.md:240-243` |
| Q-MIG-11 | 📝 Mot de passe fictif au préfixe bcrypt `$2b$` | 👥 | `02:97-127` |
| Q-MIG-12 | Mandat 13 ignoré : son client est un chasseur | 🧑‍💼 | `02:167` |
| Q-MIG-13 | Sens des statuts source `suspendu`, `termine` | 🧑‍💼 | `PgSQL.sql:26` du sujet |

✅ **Répondues le 2026-10-06** : Q-MIG-04, Q-MIG-06, Q-MIG-08, Q-MIG-09. 📝 **Notes sans case** (restent ouvertes) : Q-MIG-03, Q-MIG-05, Q-MIG-07, Q-MIG-11. Détail dans la partie 0 ; ce qui suit date d'avant, **la réponse fait foi**.

💡 **Recommandations** :

- **Q-MIG-01** : le lire comme un **% d'honoraires**, non migré.
  - 3,25 % du prix donnerait plus que les honoraires (`RCR`, anomalie A2).
  - ⚠️ Le README du schéma l'attribue au **groupe**. Je le mets chez Jeff : c'est le sens d'une donnée du client.
- **Q-MIG-02** : voir Q-REM-16.
- **Q-MIG-03** : **`'launched'`** pour les 17 demandes : toutes ont un mandat.
  - L'`UPDATE` est prêt (`02:241-246`), et c'est plus juste.
  - 🆕 2026-10-05 : une voie « au mandat signé » (15 sur 17) ; elle dépend des 2 mandats contradictoires (Q-MAN-05, Q-MAN-09).
- **Q-MIG-04** : le remplacer dans le seed, **puis le supprimer**.
- **Q-MIG-05** : **acter** : la colonne était vide partout.
- **Q-MIG-06** : **oui**, dans `03` : donnée gratuite.
- **Q-MIG-07** : **garder**, et le signaler à l'audit.
  - La colonne est `NOT NULL` (`01:184`, `01:228`, `01:246`). ⚠️ « le seed les remplace » contredit `md/point-etape-2026-09-21.md:233` (« Un seed ne doit pas les cacher ») : au groupe de dire lequel prime.
- **Q-MIG-08** : **migrer** les secteurs.
  - Sinon aucun critère n'a de lieu.
- **Q-MIG-09** : **garder**, et le signaler à l'audit.
  - ⚠️ Le minimum égal au maximum vient de **notre** migration (`02:192-208`), pas de la source.
  - 🆕 2026-10-05 : une voie « laisser le minimum vide » (NULL), que la base et l'API acceptent (`01:318`).
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
| Q-ACC-01 | 🔁 **Doublon de Q-JEF-14** (2026-10-05) — Reposer à Jeff la question des **droits** | 🧑‍💼 | **Oui**, en une question nette (Q-JEF-14) |
| Q-ACC-02 | Que voit le manager ? | 🧑‍💼 | Ses chasseurs et leurs paiements |
| Q-ACC-03 | Qui enregistre la vente ? | 🧑‍💼 | Le manager |
| Q-ACC-04 | Qui fait avancer la facture dans ses états ? | 🧑‍💼 | Le chasseur dépose, le manager vérifie |
| Q-ACC-05 | Le client voit-il tout le catalogue ? | 🧑‍💼 | Non : les biens proposés pour lui |
| Q-ACC-06 | Le chasseur voit-il son barème ? | 🧑‍💼 | Oui : sa paie doit se comprendre |
| Q-ACC-07 | Qui fixe barèmes et honoraires ? | 🧑‍💼 | La direction seule |
| Q-ACC-08 | ✅ Désactiver plutôt que supprimer ? | 👥 | **Oui** : les clés en `RESTRICT` y poussent déjà |
| Q-ACC-09 | ✅ Quel compte lance l'import des biens ? | 👥 | Un compte technique dédié |
| Q-ACC-10 | Qui affecte une demande à un chasseur ? | 🧑‍💼 | Le manager |
| Q-ACC-11 | ✅ Où ranger la facture du chasseur ? (✏️ changée le 2026-10-06 : une table des factures) | 👥 | Avec Q-REM-17 (`invoice_reference`) |
| Q-ACC-12 | Qui crée le compte client ? | 🧑‍💼 | Le client, par sa demande en ligne |
| Q-ACC-13 | Qui enregistre une visite du client ? | 🧑‍💼 | Le chasseur qui l'accompagne |
| Q-ACC-14 | ✅ Droits des chasseurs-IA ? | 📋 | Reporter au parcours IA |
| Q-ACC-15 | Un chasseur peut-il créer une demande ? | 🧑‍💼 | Non : la demande vient du client |
| Q-ACC-16 | ✅ Combien de comptes Admin / Manager dans le seed ? | 👥 | **1 admin, 2 managers** |
| Q-ACC-17 | 📝 Mot de passe : 12 caractères minimum ? | 👥 | **Garder 12** : déjà codé et testé |
| Q-ACC-18 | 📝 Garder `user.password` ? | 👥 | **Garder** : prêt si l'auth revient |
| Q-ACC-19 | ✅ Clé d'API proposée par Jeff, « optionnelle » | 👥 | **Ne pas faire** ; la citer comme piste |
| Q-ACC-20 | ✅ Réécrire ADR-025 sans ENF-03 | 👥 | **Oui** : ENF-03 vient d'un exemple (`CAHIER-DES-CHARGES-TECHNIQUE.md:74`) ; ⚠️ mais `RCR:296` et `RCR:763` le reprennent comme exigence. ⚠️ ADR-025 est déjà « accepté » sur Confluence (`md/a-faire-a-la-main-2026-09-21.md:189-190`) : ne pas le réécrire, mais écrire un nouvel ADR qui l'amende ; l'ancien ne s'efface pas (`JOURNAL-DE-DECISIONS.md:72`) |
| Q-ACC-21 | Durée de conservation avant anonymisation | 🧑‍💼 | Voir plus bas |

✅ **Répondues le 2026-10-06** : Q-ACC-08, Q-ACC-09, Q-ACC-11, Q-ACC-14, Q-ACC-16, Q-ACC-19, Q-ACC-20. 📝 **Notes sans case** (restent ouvertes) : Q-ACC-17, Q-ACC-18. Détail dans la partie 0 ; ce qui suit date d'avant, **la réponse fait foi**.

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
| Q-INF-01 | ✅ Remplacer MinIO (image introuvable) | 👥 | `md/minio-images-indisponibles-2026-10-02.md:58-71` |
| Q-INF-02 | ✅ Écrire le seed `04_seed_demo.sql` | 👥 | `md/point-etape-2026-09-21.md:197` |
| Q-INF-03 | ✅ Biens de démo : 3 à 5 biens fictifs à Montpellier ? | 👥 | `md/point-etape-2026-09-21.md:160-169` |
| Q-INF-04 | ✅ Aucun test fonctionnel | 👥 | `rapport-tests.md:245-257` |
| Q-INF-05 | ✅ 15 ressources sur 18 sans test d'intégration | 👥 | `rapport-tests.md:253` |
| Q-INF-06 | Champ obligatoire manquant → `409`, pas `422` | 👥 | `API/README.md:216-218` |
| Q-INF-07 | ✅ Générateur de données en masse (phase 3) | 👥 | `md/point-etape-2026-09-21.md:199` |
| Q-INF-08 | ✅ ENF-01 (500 mandats en moins de 2 s) et ENF-03 non testés | 👥 | `rapport-tests.md:254-255` |
| Q-PRO-01 | ✅ **Qui est le PO ?** Jeff (2026-10-06) | 👥 | — |
| Q-PRO-02 | ✅ Valider les 5 réponses du point d'étape (A1) | 👥 | `md/point-etape-2026-09-21.md:106-108` |
| Q-PRO-03 | ✅ ADR à passer en « accepté », ou à écrire | 👥 | `md/a-faire-a-la-main-2026-09-21.md:96-112`, `09-dec:178` |
| Q-PRO-04 | ✅ Argon2 : ADR-016 ou ADR-017 ? | 👥 | `md/adr-024-motif-refus-remuneration.md:7-10` |
| Q-PRO-05 | 📝 Dire à Békanty que le CDC v2.0 audite l'**ancien** schéma | 👥 | `md/a-faire-a-la-main-2026-09-21.md:66-79` |
| Q-PRO-06 | ✅ Nettoyer Confluence (note drawio, compagnon d'ADR-024) | 👥 | `md/a-faire-a-la-main-2026-09-21.md:192-204` |
| Q-PRO-07 | ✅ Livrables 1 (audit) et 3 (architecture) vides | 📋 | `08-etat.md` |
| Q-PRO-08 | ✅ Format des téléphones entre tables | 👥 | `md/notes_contraintes_client.md:34-36` |

✅ **Répondues le 2026-10-06** : Q-INF-01, Q-INF-02, Q-INF-03, Q-INF-04, Q-INF-05, Q-INF-07, Q-INF-08, Q-PRO-01, Q-PRO-02, Q-PRO-03, Q-PRO-04, Q-PRO-06, Q-PRO-07, Q-PRO-08. 📝 **Notes sans case** (restent ouvertes) : Q-PRO-05. Détail dans la partie 0 ; ce qui suit date d'avant, **la réponse fait foi**.

💡 **Recommandations** :

- **Q-INF-01** : d'abord décider **s'il faut** un stockage objet.
  - Rien ne lit d'images aujourd'hui.
  - Sinon, retirer le service, avec l'accord du responsable de `docker-compose.yml`.
- **Q-INF-02** : il ne reste que **Q-INF-03** (les 4 autres sont répondues ; Q-PAR-02 attend Jeff, Q-JEF-03).
  - Et après le lot de migration, sinon le seed serait à refaire.
- **Q-INF-03** : **oui**.
  - Les 2 556 biens sont hors de Montpellier, et plafonnent à 406 042 €.
- **Q-INF-04** : le sujet les exige ; commencer par le **parcours de paiement**.
- **Q-INF-05** : priorité à `payment`, `sale`, `mandate`.
- **Q-INF-06** : ajouter des modèles d'entrée Pydantic, comme pour `/users`.
- **Q-INF-07** : quand le seed est stable.
- **Q-INF-08** : ENF-01 se mesure avec le générateur (Q-INF-07) ; ENF-03 tombe avec l'auth (ADR-026).
- **Q-PRO-01** : **en nommer un**.
  - Il tranche les questions « groupe » et tient le journal d'ADR.
  - ✅ Répondu le 2026-10-06 : **Jeff**, qui joue tous les rôles sauf le développement.
    Le journal d'ADR sera tenu par un membre de l'équipe (💡 à nommer dans la RACI).
- **Q-PRO-02** : 3 réponses sur 5 confirmées par d'autres cartes (Q1 = Q-REM-15, Q2 = Q-REM-06, Q5 = Q-MAN-04).
  - Restent : Q3, en base mais pas actée (ADR-024 « proposé »), et Q4 = Q-INF-03.
- **Q-PRO-03** : tout passer **en une séance**.
  - À accepter : 016, 017, 019 à 024, 026, 027.
  - À écrire : l'ADR de la décision D3 (`09-dec:178`), et celui de X01 (Q-REM-18).
  - 🆕 2026-10-05 : plus les ADR L à T du pense-bête (partie 0).
  - Un ADR proposé ne fait pas foi (`09-dec:34-38`).
- **Q-PRO-04** : le **journal Confluence** fait foi ; corriger le CDC.
- **Q-PRO-05** : **oui**, vite : il qualifie de « bloquant » ce qui existe.
- **Q-PRO-06** : **oui** : le journal a « un trou » à la place d'ADR-024.
- **Q-PRO-07** : planifier ; l'audit a déjà sa matière (constats de migration).
- **Q-PRO-08** : reporter ; un ADR à part si le temps le permet.

---

## 2. Questions que seul Jeff peut trancher

➡️ **Rapport à part, depuis le 2026-10-05** : `md/questions-pour-jeff-2026-10-05.html`
(artifact « Fil Rouge — Questions pour Jeff »). Chaque question y porte **notre position**,
tirée des réponses, et ce que sa réponse change. Elles se cochent **là-bas
seulement** : la page principale n'a plus que le lien.

🆕 **Cartes déménagées le 2026-10-05** (option A) : les **34 cartes** de la
partie 1 que seul Jeff tranche (« Qui tranche » commence par Jeff, sans
« puis groupe ») ne se cochent plus que dans le rapport Jeff, rangées sous la
question qui les regroupe. Leurs 13 réponses et 2 doublons y sont reportés.
Elles restent décrites dans la partie 1 de ce registre.

🆕 **Mis à jour le 2026-10-06**, d'après la 3e série de réponses :
**6 questions ajoutées** (Q-JEF-21 à 26) et **3 complétées** (Q-JEF-13, 15, 19).
✅ Reportées le 2026-10-06 : partie 0 (réponses, avis, lot, ADR) et partie 1 (statuts).

| Question pour Jeff | Cartes rangées dessous |
|---|---|
| Q-JEF-01 | Q-PAR-01, 04, 06, 07, 08, 10, 11, 13 |
| Q-JEF-02 | Q-PAR-03 |
| Q-JEF-03 | Q-PAR-02 |
| Q-JEF-05 | Q-PAR-05 |
| Q-JEF-08 | Q-REM-07 |
| Q-JEF-09 | Q-REM-08, Q-REM-09 |
| Q-JEF-10 | Q-REM-16, Q-MIG-02 |
| Q-JEF-12 | Q-MIG-01 |
| Q-JEF-13 | Q-MIG-10, Q-MIG-12, Q-MIG-13 |
| Q-JEF-14 | Q-ACC-01 à 07, 10, 12, 13, 15 |
| Q-JEF-15 | Q-ACC-21 |
| Q-JEF-16 | Q-PAR-09 |
| Q-JEF-18 | Q-SCH-05 |

✅ **Entretien fait le 2026-10-07.** Réponses de Jeff, notées par l'équipe :

| Question | Réponse de Jeff |
|---|---|
| Q-JEF-01 | ✅ Il **valide tous** les paramètres proposés |
| Q-JEF-02, 04, 07, 08, 09, 10, 11, 12, 17, 19, 20, 22, 25 | ✅ Il **valide nos positions** (celles écrites sur les cartes) |
| Q-JEF-03 | **Rien pour personne** : ni le chasseur ni l'entreprise |
| Q-JEF-05 | Pas de grille : **le groupe propose la sienne** |
| Q-JEF-06 | L'annulation libère le client **tout de suite** |
| Q-JEF-13 | **Oui à nos positions** : Nina Girard ; `termine` → `completed` ; `suspendu` → `canceled` ; 6 échus → `expired` ; pas de pause, pas de nouvel état |
| Q-JEF-14 | « on doit fournir les outils pour une bonne gestion de l'authentification (route de connextion, token, session, role, droit, etc.) , mais l'on ne doit pas crée la page de login en elle même » |
| Q-JEF-15 | Ajouter une route, ou modifier la route DELETE, pour **seulement anonymiser** les données personnelles d'une personne |
| Q-JEF-16 | **La direction** |
| Q-JEF-18 | De **1 à 5** |
| Q-JEF-21 | Réglée par Q-JEF-14 : le mot de passe se garde |
| Q-JEF-23 | Facture **hors périmètre** |
| Q-JEF-24 | Un bien peut être **saisi à la main** (hors marché, courant dans l'immobilier) |
| Q-JEF-26 | Les manques sont **voulus** ; ne pas supprimer les anciennes données ; on peut fausser les autres (modifier le script fourni) |

Report dans la partie 0 : 🆕 4e série.

Restent sur la page principale, car le groupe tranche d'abord : Q-REM-01,
Q-REM-02, Q-REM-06, Q-MAN-02, Q-MAN-03.

🆕 2026-10-06 : Jeff **ne remplit pas** le rapport. Le groupe lui pose les
questions **en entretien**, court : la liste, rangée par thème, les questions
qui débloquent le plus d'abord, ouvre le rapport. L'équipe y note ses réponses.
Jeff joue **tous les rôles sauf le développement** : client et PO. 26 questions : 19 le 2026-10-02,
Q-JEF-20 le 2026-10-05, Q-JEF-21 à 26 le 2026-10-06.

### Les chiffres

- **Q-JEF-01** — Valide-t-il les **paramètres proposés** par le sujet ?
  Fixe 3 000 € + 2,5 %, tranches 30 à 50 %, poids 25/10/25/15/25,
  ancienneté « 0 % → +10 % (plafond à 5 ans) » (`RCR:207`), performance ±20 %,
  taux final entre 20 et 60 %, arrondis de la note (1 déc.) et du taux (4 déc.).
  (Q-PAR-01, 04, 06, 07, 08, 10, **11** — ajouté le 2026-10-05 —, 13)
  - Q-REM-19 (oui) grave 20 % et 60 % dans la base : s'il les change, base à recréer.
- **Q-JEF-02** — Confirme-t-il le barème **par palier** (le taux de la tranche
  s'applique à tout) ? `F10:166` en fait une règle, `RCR:323` une décision.
  ⚠️ Le palier crée un saut d'environ 600 € à 350 000 €. (Q-PAR-03)
- **Q-JEF-03** — Mandat **non exclusif**, le client ou une autre agence vend :
  le chasseur touche-t-il **rien**, ou une indemnité ? Et l'entreprise
  touche-t-elle des honoraires dans ce cas ? (Q-PAR-02, Q-REM-02)
- **Q-JEF-04** — Confirme-t-il des honoraires **HT** ? Le sujet l'affirme (`RCR:131`).

### La performance

- **Q-JEF-05** — 🆕 Reformulée le 2026-10-05, d'après la réponse Q-PAR-05 (transfo).
  Le sujet dit que le score est « recalculé **à la baisse** » quand un mandat
  expire sans vente (`Readme.md:135`, `F10:295-300`). Avec les critères
  proposés, un mandat de plus **ne fait jamais baisser** le score.
  Nous proposons le **taux de transformation** (ventes ÷ mandats) à la place
  de S₄ (`RCR:160`). Le valide-t-il ? Et **quelle grille de notes** : quel taux
  vaut 100 points ? Le sujet n'en donne aucune. (Q-PAR-05)
  - Détail à lui faire trancher : mandats **signés** sur 12 mois au dénominateur
    (la note baisse dès la signature), ou mandats **clos**, vendus ou échus
    (la note baisse pile à l'échéance, comme `F10:295-300`).
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
  - 🆕 Complétée le 2026-10-06 (Q-MIG-03) : un mandat peut-il être **mis en pause**,
    puis reprendre ? La **demande de recherche** peut-elle être suspendue, ou annulée ?
    Elle n'a que 4 états (`01:287-288`), le mandat 6, sans « suspendu » (`01:405-407`).
  - ⚠️ La migration traduit « suspendu » en `canceled` pour 2 mandats (`02:218`, `02:225`),
    sans l'écrire nulle part : « suspend » donne 0 résultat dans `02` et dans `docker/init-v2/README.md`.
- **Q-JEF-26** — 🆕 Ajoutée le 2026-10-06. Des données manquent dans l'ancienne base :
  le **téléphone** de 3 clients (`PgSQL.sql:94`, `:100`, `:106`), l'**adresse** et le
  **code postal** de 18 clients, le **budget minimum** des 17 demandes (`PgSQL.sql:71`).
  Peut-il les fournir ? Sinon : « non renseigné », sans rien inventer.
  (Q-SCH-01, Q-SCH-18, Q-MIG-07, Q-MIG-09)
  - 🟡 À fixer en groupe : « inconnu » s'écrit NULL quand la colonne l'accepte
    (Q-MIG-09, « vide ») ; une valeur factice seulement si elle est obligatoire
    (téléphone `01:184`, code postal `01:210`).

### Les droits et le RGPD

- **Q-JEF-14** — Le 22/09, il a tranché l'**authentification**. Mais **qui
  peut faire quoi** reste ouvert : que voit le manager, qui enregistre la vente,
  qui valide la facture, le chasseur voit-il son barème ?
  (Q-ACC-02 à 07, Q-ACC-10, 12, 13, 15)
- **Q-JEF-24** — 🆕 Ajoutée le 2026-10-06. Un bien peut-il être **saisi à la main**
  par un chasseur ou un manager, ou vient-il **seulement de l'import** ? Le sujet ne
  décrit que la sélection automatique (`F05:16`). (Q-ACC-09)
  - 💡 Airflow lance un traitement selon un planning ou à la demande
    ([doc officielle](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html),
    3.3.2, lue le 2026-10-06) : planifié, l'import tourne seul. C'est Airflow qui
    écrit en base : plutôt l'option « compte technique » de Q-ACC-09. À revoir en groupe.
- **Q-JEF-15** — Combien de temps garder les données avant **anonymisation** ?
  Le sujet donne 10 ans pour les paiements ; il manque le reste. (Q-ACC-21)
  - 🆕 Complétée le 2026-10-06 (Q-ACC-08) : pour **effacer un compte**, nous proposons
    que l'admin le **désactive**, rende **anonyme** ce qui n'est pas obligatoire, et
    **garde** ce que la loi impose (paiements, 10 ans, `REGISTRE-RGPD.md:29`).
    Le sujet pose la question sans y répondre (`REGISTRE-RGPD.md:38`).
  - ⚠️ L'API garde une route DELETE sur les 18 ressources (`API/src/app/routes/crud_router.py:104-111`) :
    à retirer, ou à justifier, si on désactive.
- **Q-JEF-18** — Quelle **échelle de priorité** pour le client sur un bien proposé ? (Q-SCH-05)
- **Q-JEF-16** — 🆕 En deux temps depuis le 2026-10-05. 1. Veut-il des
  **barèmes propres à un chasseur** (`RCR:186-193`), en plus des bonus
  d'ancienneté et de performance, qui rendent déjà le barème « différent pour
  chaque chasseur » (`Readme.md:80`) ? 2. Si oui, qui les crée, et qui les
  valide ? Notre position : le manager (Q-PAR-09). ⚠️ À accorder avec
  Q-ACC-07 (💡 « la direction seule »). (Q-PAR-09)

### Le mot de passe et la clé d'API

- **Q-JEF-21** — 🆕 Ajoutée le 2026-10-06. Notre base doit-elle garder un **mot de
  passe** pour chaque compte ? La couche « au dessus » le lira-t-elle chez nous ?
  Sinon, nous le retirons. (Q-ACC-18, Q-MIG-11)
  - ⚠️ Le brouillon d'ADR-026 dit l'inverse : la colonne reste, car Jeff a dit
    « consommés » (`md/adr-026-perimetre-authentification.md:70-72`). Sa réponse tranche.
  - Coût d'un retrait, compté le 2026-10-06 : 4 fichiers d'`API/src`, 8 fichiers
    d'`API/tests`, 27 lignes de `02`.
- **Q-JEF-22** — 🆕 Ajoutée le 2026-10-06. La **clé d'API** qu'il proposait le 22/09
  (`md/adr-026-perimetre-authentification.md:51-53`) : **une seule**, ou **une par
  programme** ? Et comment la lui remettre ? (Q-ACC-19)

### La facture du chasseur

- **Q-JEF-23** — 🆕 Ajoutée le 2026-10-06. Une facture **refusée puis renvoyée** :
  garder **chaque envoi**, ou seulement la **dernière** ? Le sujet n'en dit rien
  (`F07:18-27`, `RCR:284-289`). (Q-ACC-11, Q-REM-17)
  - ⚠️ Chez nous, `'refused'` sur un paiement veut dire « pas de droit à
    rémunération » (`01:728-729`), pas « facture refusée ».

### Pour information, et des confirmations

- **Q-JEF-19** — **Pour information** (pas une question) : un prix pile sur une
  limite du barème prend la tranche du dessus, comme votre tableau (200 000 € → 35 %,
  350 000 € → 40 %). Les prix sont stockés en euros entiers. Dites-nous si ce n'est
  pas votre lecture. (Q-REM-01, tranchée le 2026-10-05)
  - 🆕 Complétée le 2026-10-06 (note sur Q-REM-01) : la contradiction, mot pour mot.
    Le tableau dit « < 200 000 € » pour 30 %, puis « 200 000 – 349 999 € » pour 35 %
    (`RCR:173-174`) ; la requête dit `BETWEEN montant_min AND COALESCE(montant_max, 999999999)`
    (`RCR:188`), bornes incluses. Avec des centimes, 199 999,50 € ne tomberait dans aucune tranche.
- **Q-JEF-20** — 🆕 Ajoutée le 2026-10-05. **Confirmation** : chaque paiement
  garde la note de performance et le détail du calcul (les 5 notes, les visites,
  l'ancienneté…), pour pouvoir le refaire. Est-ce bien ce qu'il veut ?
  Le sujet l'exige déjà (`RCR:292`) ; la note de Q-REM-03 demandait sa
  confirmation. (Q-REM-03, Q-REM-04)
- **Q-JEF-25** — 🆕 Ajoutée le 2026-10-06. **Confirmation** : il est notre **PO** ;
  valide-t-il nos ADR **en une séance**, après ses réponses ? Seul « accepté »
  compte (`livrables/2-modelisation/09-decisions-a-prendre.md:34-35`). (Q-PRO-01, Q-PRO-03)
  - Le journal d'ADR sera tenu par un membre du groupe, à nommer dans la RACI.

---

## 3. Ce qui ne va pas — erreurs, défauts, critiques

### ❌ Défauts dans le code et le schéma

- ⚠️ **`mandate_model.py:23`** : `ends_at: date` est déclaré **obligatoire**,
  alors que la base le veut **vide** pour un mandat `pending_signature` (`01:412-414`, `01:430-432`).
  - ✅ **Mesuré le 2026-10-02**, sur `fil_rouge_test`, transaction annulée :
    `POST /mandates` sans `ends_at` → **`201`**, `GET` → **`200`**, `ends_at: null`.
  - ➡️ **Pas de bug** : les modèles de table ne valident pas l'entrée (`API/README.md:216-218`).
  - Défaut **de documentation** seulement : l'annotation ment, et la doc Swagger peut afficher le champ comme obligatoire.
    Passer à `Optional[date] = None`.
- **`sale_model.py`** et **`payment_model.py`** ne déclarent pas `unique=True`
  sur `id_mandate` et `id_sale`, alors que la base le fait (`01:659`, `01:760`).
- **`sale_model.py:7-8`** : dit qu'une vente `client_alone` est « hors mandat ».
  Faux : `id_mandate` est `NOT NULL`.
- **`created_at`** : les modèles produisent une date **avec** fuseau ; la
  colonne est `TIMESTAMP` **sans** fuseau. La valeur stockée peut être décalée.
- **Paramètres gravés dans des `CHECK`** (`01:758-759`) : contraire à « jamais en dur » (`RCR:42-47`).
- **`amount_max` contrôlé deux fois** (`01:696` et `01:702-703`).
- **Commentaires périmés** :
  - `01:904` dit que `02` et `03` visent « l'ANCIEN schéma en K€ » ;
  - `02:189` parle encore de « K€ (colonne cible NUMERIC(6,1)) » ;
  - `02:235-236` dit que les clés de `client` et `hunter` sont `id_user` ;
  - `02:29` renvoie au « README point 5 » au lieu de §3.5.

### ⚠️ Incohérences entre documents

- **« D2 » veut dire deux choses** dans le même fichier :
  - `01:134` et `01:756` : D2 = ancienneté (numérotation du groupe) ;
  - `01:726` : D2 = « R = 0 » (numérotation du sujet, `RCR:322`).
  - ➡️ Le groupe et le sujet numérotent tous deux de **D1 à D9**. Il faut un préfixe.
- **D10 mal étiqueté** : `01:630` l'attribue aux visites ; c'est la table des rendez-vous (`09-dec:432-441`), que Q-SCH-07 écarte (hors MVP).
- **D9 décrit deux fois différemment** : `01:817-820` dit « un jour d'écart », `09-dec:413-422` dit « deux jours ».
- **D3 brouillé** : `01:669-672` dit qu'un acte tardif « peut ouvrir droit » ; la décision est « refus sauf renouvellement ».
- **D1 pas mis à jour** : `09-dec:299` dit encore « Solution B » (K€), avec sa justification « doit rester indicatif », abandonnée.
- **ADR-025** : « accepté » sur Confluence, « proposé » dans le dépôt (`md/adr-025-…:17`, `08-etat.md:152`).
  - 🆕 2026-10-06 : la copie du journal d'ADR de Confluence lue le 2026-10-06 le dit **« Annulé »** ; vos réponses
    (Q-SCH-13, Q-MIG-04, Q-ACC-16) gardent le lien chasseur → manager. À vérifier (Q-ACC-20).
- 🆕 **ADR-016 (Argon2)** : « annulé le 06/10 » d'après ta note sur Q-PRO-04, « accepté » dans la
  copie du journal lue le même jour à 11 h 16. Le code hache toujours en Argon2 (`API/src/app/utils/security.py:20-32`).
- 🆕 **ADR-019** : « proposé » dans ce registre (Q-REM-13, ADR I), « accepté » dans la copie du journal du 2026-10-06.
- 🆕 **Deux ADR-026** : sur Confluence, « robustesse des mots de passe », annulé le 22/09 ;
  notre brouillon `md/adr-026-perimetre-authentification.md` devra prendre un autre numéro (028 au 2026-10-06).
- 🆕 **MinIO** : `be15c04` (2026-10-06) change les images ; `md/minio-images-indisponibles-2026-10-02.md`
  et `context AI/08-etat.md` les disent encore introuvables. Que les nouvelles se téléchargent : non vérifié.
- **N2 dit encore « ouvert »** alors que Q-SCH-02 l'a tranché le 2026-10-05 : `01:298-300`, `09-dec:248` (vide),
  `docker/init-v2/README.md:311`.
- **Numéro d'ADR de la localisation** : ADR-010 dans `md/notes_contraintes_localisation_criteria.md:90`,
  ADR-009 dans `01:136` et `01:298`.
- **Comptes faux dans `08-etat.md` lui-même** : « 224 colonnes » (`08-etat.md:20`, `:133`)
  contre « 226 colonnes » (`08-etat.md:158`, et `01:895`).
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
  (`01:789-795`) ; ➡️ contrôlé dans l'API depuis Q-MAN-06 (2026-10-05), avec un montant faux (Q-REM-11), sur des honoraires modifiables (Q-REM-12).
- **Aucun test fonctionnel**, alors que le sujet en exige (`Readme.md:256`).
- **La calculette n'est pas branchée** : elle ne lit pas le barème et n'écrit pas le paiement.
- **Les 2 556 biens ne servent pas la démo** : ils sont hors de Montpellier.
- **Beaucoup de documents se recouvrent** (`md/`, `livrables/`, `context AI/`) :
  une même question y vit à trois endroits, avec trois états.
- 🆕 **Q-PRO-08 posait une question déjà tranchée** : le format des téléphones est fixé par
  ADR-007, accepté (copie du journal d'ADR de Confluence lue le 2026-10-06). La carte ne le citait pas.
- 🆕 **Q-MIG-07 recommandait de garder les `0000000000`** : ils ne respectent pas le format d'ADR-007.

---

## 4. Autres idées

- 🆕 **2026-10-06**, ta note sur les idées : « note tes idée et propose les plus tard apres les
  entrevues ». Elles attendent l'entretien avec Jeff.
- 💡 **Un seul registre de questions** : ce fichier, avec ses identifiants
  `Q-…`, remplace les listes éparses. Une question tranchée y prend sa date
  et son ADR, puis sort de la liste.
- 💡 **Préfixer les décisions** : `DS-` pour celles du sujet, `DG-` pour
  celles du groupe. Fin de la confusion sur « D2 ».
- ✅ **Un entretien avec Jeff**, court (décidé le 2026-10-06) : la liste en tête du
  rapport Jeff, rangée par thème, les questions qui débloquent le plus d'abord.
- 💡 **Une diapo « règle ou paramètre »** en soutenance : c'est le piège que
  le sujet annonce (`RCR:40`), et on a de quoi le montrer.
- 💡 **Rejouer les 55 cas contre la base**, une fois la calculette branchée :
  même tableau d'exemples, mais lu depuis `commission_scale` et écrit dans `payment`.
- 💡 **Un test de non-régression sur la borne de tranche** : 199 999,99 €
  et 200 000,00 € ; c'est là que Q-REM-01 casse.
- 💡 **Mettre à jour `08-etat.md`** après chaque séance de décision : c'est
  le fichier qu'on relit après une coupure.

# ADR-034 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 034 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md`,
> § 3, groupe 2, l. 57). Il réunit les lettres D et K du pense-bête
> (`md/questions/questions-a-trancher.md:399`, `:406`). K entre dans D : « C'est
> une validation, pas une décision de conception » (même fichier, § 2,
> regroupement 2, l. 24).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Aucune question ne reste ouverte dans la fiche.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * **Banc v2 / v3 (`docker/compare_v2_v3.sh`), un outil d'atelier — déduit,
>   demande du code, non fait.** Il rend « DIFFÉRENTES » pour une seule raison :
>   le seed `05_parametres.sql` remplit les trois tables en base neuve
>   (1 / 5 / 1 lignes), et aucune des 14 migrations ne le fait en base migrée
>   (grep `INSERT INTO` sur les trois tables : 0). Les schémas sont identiques,
>   571 faits de chaque côté (`md/adr/2026-10-08-notes-seance-adr.md:79`).
>   Réponse déduite : **une migration v2 → v3 qui pose le même premier jeu**.
>   * Le banc vérifie « que les deux chemins mènent au même endroit »
>     (`compare_v2_v3.sh:6-8`).
>   * Sans ces lignes, une base migrée ne peut enregistrer aucune vente, donc
>     aucun paiement (`05_parametres.sql:5-8` ; `docker/init-v3/02_migration.sql:39-42`).
>   * Un banc qui rend toujours « DIFFÉRENTES » ne verrait plus un vrai écart.
>   * 💡 Garde proposée : n'insérer que dans une table vide, pour ne pas ajouter
>     une version à une base qui a déjà les siennes.
> * **Qui écrit ces tables.** « La direction seule » pour honoraires et barèmes
>   (Q-ACC-07, `questions-a-trancher.md:1036` ; Jeff, Q-JEF-16, l. 1171). Pour
>   `hunter_rate_parameters`, rien n'est écrit. 💡 La même règle, la direction :
>   une analogie, pas une source, car Q-ACC-07 ne parle que de « barèmes et
>   honoraires ». À porter dans la matrice d'ADR-027, en 💡 ; `md/securite/matrice-droits-crud-par-role.md`,
>   § 5.4 (l. 189-216), n'a aucune ligne pour cette table.
> * Les notes du jour disent que le sujet « ne dit pas qui construit le
>   `Parametrage` » (`md/adr/2026-10-08-notes-seance-adr.md:47`). C'est trop
>   fort : le sujet dit qu'une couche au-dessus du calcul le charge
>   (`REGLES-CALCUL-REMUNERATION.md:641`, `:760`). Seule la forme (un service)
>   est un choix de l'équipe. À corriger.
> * `livrables/2-modelisation/09-rapport-ecarts-contraintes.md:560-569` décrit
>   encore les bornes v2 de `seniority_rate` (0 à 0,10) et de
>   `performance_rate` (−0,20 à 0,20). Sa ligne R22 propose même de graver le
>   pas de 2 % dans un `CHECK`. À aligner ou à dater.
> * Le registre cite encore l'ancien nom `remuneration_parameters`
>   (`questions-a-trancher.md:125`, `:591`). Renommée `hunter_rate_parameters`
>   le 08/10 (G2, commit `c8418c6`).
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-034 : Les paramètres de la rémunération vivent dans trois tables datées ; leurs valeurs sont celles du sujet, validées par Jeff

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions : 02/10, 05/10, 07/10 et 08/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * le groupe : Q-REM-05 « Table versionnée + relâcher les CHECK » (02/10/2026) ; Q-REM-19 « Activer le CHECK 0,20-0,60 » (05/10/2026) ; les réponses aux cartes Q-PAR (05/10 et 07/10/2026) ; G1 et G2 (08/10/2026) ;
  * Sébastien : les versions « à partir du » et les bornes de domaine (LOT6, 07/10/2026) ; le seed et le service (« oui pour le seed », « fais le service », 08/10/2026, notes du jour) ;
  * le client, Jeff (aussi PO) : Q-JEF-01, Q-JEF-02, Q-JEF-03 et Q-JEF-04, entretien du 07/10/2026 (réponses notées par l'équipe).
* **Remplace :** rien.
* **Complète :** ADR-030 (la vente pointe sa grille d'honoraires) et ADR-024 (un refus ne porte ni taux ni version de réglages).

**Contexte**

Le sujet sépare deux choses (`REGLES-CALCUL-REMUNERATION.md:42-47`) :

* une règle vit « Dans le **code** et le **schéma** » ;
* un paramètre vit « Dans une **table de paramètres**, jamais en dur » (l. 47).

Il prévient : « Confondre les deux, c'est présenter en soutenance des chiffres inventés comme des exigences client. » (l. 40).

Le sujet dit proposer, « à valider avec le client », « toutes les valeurs numériques » (l. 59). Sa liste : le fixe, le pourcentage, les bornes de tranches, les taux, la notation des cinq critères, leurs poids, l'effet de l'ancienneté, l'amplitude de la modulation, les bornes du taux final. Les arrondis n'y sont pas.

Les user stories disent la même chose : ces valeurs « sont des paramètres proposés, non imposés par le métier » (`user-stories/10_calcul_remuneration_chasseur.feature:3-5`).

Le sujet date les honoraires et le barème : « versionnés dans le temps » (l. 129). Son modèle de tables n'en a que deux : `baremes_commission` et `parametres_honoraires` (l. 264-280).

Le code du sujet tient le calcul à part. C'est une fonction pure, qui reçoit un `Parametrage` (l. 446-453). La valeur par défaut, `parametrage_par_defaut`, est un jeu d'essai : « Cette fonction est un jeu d'essai », « en production, elle est remplacée par une lecture des tables » (l. 641).

Au 02/10/2026, la base v2 avait deux défauts (carte Q-REM-05, `questions-a-trancher.md:575-597`) :

* aucune table pour les poids, les paliers, les notes, la fenêtre, l'ancienneté, la modulation, les bornes ;
* deux valeurs proposées gravées dans des `CHECK` : `seniority_rate BETWEEN 0 AND 0.10` et `performance_rate BETWEEN -0.20 AND 0.20` (`docker/init-v2/01_create_fil_rouge_immobilier.sql:758-759`).

**Options envisagées**

Quatre questions, tranchées à des dates différentes.

A. Où vivent les réglages du taux ? (Q-REM-05, 02/10/2026)

1. **Une table versionnée.** Avantages : suit la lettre du sujet (l. 47) ; un calcul passé se rejoue. Inconvénients : une table, un modèle, une route de plus. **Retenue.**
2. **Les valeurs dans le code** (`parametrage_par_defaut`, `API/src/app/services/remuneration.py:296`). Avantage : rien à faire. Inconvénient : une valeur du client écrite « en dur ». **Écartée.**
3. **Le code, et des `CHECK` relâchés.** C'était le repli « si le temps manque ». **Écartée** : le groupe a choisi la table, que le sujet demande (l. 47).

B. Comment dater les versions ? (LOT6, 07/10/2026)

1. **`valid_from` et `valid_until`**, comme le proposait la carte Q-REM-05. Inconvénient : une date de fin saisie à la main peut laisser un trou. **Écartée.**
2. **Une date de début seule, `effective_from` + `UNIQUE`**, comme `parameters_fees` (ADR-030). Une version vaut jusqu'à la suivante. **Retenue.**

C. Que gardent les `CHECK` du paiement ? (LOT6 et Q-REM-19)

1. **Garder les bornes v2** (0,10 et ±0,20). Inconvénient : Jeff ne peut rien changer sans migration. **Écartée.**
2. **Les bornes du domaine d'un taux** : ancienneté de 0 à 1, performance de −1 à 1. **Retenue.**
3. **Pour le taux final, aucun `CHECK` sur 20 % et 60 %** : ce sont des paramètres. C'était la recommandation de Claude (`questions-a-trancher.md:740-744`). **Écartée** par le groupe le 05/10/2026. La carte ne note pas sa raison (l. 737).
4. **`CHECK (final_rate BETWEEN 0.20 AND 0.60)`.** Avantage : la base refuse de verser un taux hors des bornes. Inconvénients : deux paramètres gravés en base ; changer une borne demande deux gestes (Conséquences). **Retenue.**

D. Qui transforme les tables en `Parametrage` ?

1. **Le calcul lui-même lit la base.** Inconvénient : il n'est plus une fonction pure ; le sujet le refuse (l. 760). **Écartée.**
2. **Un service à part, dans la couche services de l'API.** Avantage : le calcul du sujet ne change pas ; les tests du calcul restent sans base. **Retenue.**

**Décision**

1. Les paramètres du calcul vivent dans trois tables :
   * `parameters_fees` : les honoraires (`fixed_amount`, `rate`) ;
   * `commission_scale` : le barème, par tranche, par défaut ou propre à un chasseur (`id_hunter`) ;
   * `hunter_rate_parameters` : les réglages du taux du chasseur (poids, paliers, notes, points, fenêtre, ancienneté, modulation, bornes). Nom choisi par le groupe le 08/10/2026 (G2).
2. `parameters_fees` et `hunter_rate_parameters` sont datées « à partir du » : `effective_from DATE NOT NULL` et `UNIQUE (effective_from)`. Une version vaut jusqu'à la veille de la suivante. `commission_scale` garde ses périodes et ses `EXCLUDE` : cinq tranches y démarrent le même jour, et une tranche peut être propre à un chasseur (ADR-030).
3. Aucun `CHECK` sur les valeurs de `hunter_rate_parameters` : ce sont des paramètres.
4. Sur `payment`, `seniority_rate` et `performance_rate` n'ont plus que les bornes du domaine : `BETWEEN 0 AND 1` et `BETWEEN -1 AND 1`.
5. Une exception, voulue : `final_rate BETWEEN 0.20 AND 0.60`. Jeff a validé ces deux bornes (Q-JEF-01).
6. Changer une valeur, c'est insérer une nouvelle version datée. Une version déjà utilisée ne devra plus se modifier : pas encore codé (Conséquences).
7. Un paiement pointe la version de réglages qui a servi : `payment.id_hunter_rate_parameters` (G1, 08/10/2026). Il pointe déjà sa tranche (`id_commission_scale`). La vente pointe sa grille d'honoraires (ADR-030).
8. Le calcul reste le code du sujet, une fonction pure. Un service, `ParametrageService`, lit les trois tables et rend le `Parametrage`. Il rend toutes les grilles d'honoraires et tout le barème : le calcul choisit selon la date de l'acte. Seuls les réglages du taux sont pris à la date (`API/src/app/services/parametrage_service.py:20-25`, `:136`). Le service n'est branché sur aucune route (l. 31-32).
9. Les arrondis et les règles restent dans le code, pas en table (voir les questions tranchées).
10. Le premier jeu de valeurs est celui du sujet (§ 14.3, l. 644-686), en vigueur à partir du 2026-01-01.

Où vit chaque valeur, et qui l'a validée :

| Valeur proposée par le sujet | Carte | Où elle vit | Validée |
|---|---|---|---|
| Honoraires : 3 000 € + 2,5 %, hors taxes | Q-PAR-01 | `parameters_fees.fixed_amount`, `.rate` | Jeff, Q-JEF-01 ; HT : Q-JEF-04 |
| Tranches : 30 / 35 / 40 / 45 / 50 % | Q-PAR-10 | `commission_scale` | Jeff, Q-JEF-01 |
| Poids des 5 critères : 25 / 10 / 25 / 15 / 25 | Q-PAR-06 | `weight_delay` … `weight_visits` | Jeff, Q-JEF-01 |
| Grilles de notes : délai, visites, exclusivité 100 / 60 | Q-PAR-13 | `delay_tiers`, `visit_tiers`, `score_exclusive`, `score_non_exclusive`, `points_per_sale`, `points_per_mandate` | Jeff, Q-JEF-01 ; `points_per_mandate` : le critère « mandats » est remplacé par le taux de transformation (Q-PAR-05, ADR-048) |
| Fenêtre : 12 mois glissants | Q-PAR-04 | `window_months` | Jeff, Q-JEF-01 |
| Ancienneté +10 % max, performance ±20 % | Q-PAR-07 | `seniority_rate_per_year`, `seniority_cap`, `score_pivot`, `score_half_range`, `performance_amplitude` | Jeff, Q-JEF-01 |
| Plancher 20 %, plafond 60 % | Q-PAR-08, Q-REM-19 | `rate_floor`, `rate_ceiling` ; et le `CHECK` de `final_rate` | Jeff, Q-JEF-01 |
| Arrondis : score 1 déc., taux 4 déc., montant au centime | Q-PAR-11 | constantes du code (`remuneration.py:39-41`) | Jeff, Q-JEF-01 |
| Barème par palier | Q-PAR-03 | règle du code | Jeff, Q-JEF-02 |
| Non exclusif, client qui trouve seul : rien | Q-PAR-02 | règle du code (ADR-024) | Jeff, Q-JEF-03 : « rien pour personne » |

Hors de cet ADR : la grille du taux de transformation (Q-PAR-05, Q-JEF-05 ; ADR-048), et qui crée un barème propre à un chasseur (Q-PAR-09, RACI).

**Justification**

* Le sujet est clair : un paramètre vit en table, « jamais en dur » (l. 47). Et ses chiffres sont des propositions « à valider avec le client » (l. 59).
* Un `CHECK` sur une valeur proposée « refait l'erreur que Q-REM-05 corrige » (`docker/init-v3/01_create_fil_rouge_immobilier.sql:835-836`). Un `CHECK` à 0,10 interdisait à Jeff de changer le plafond sans migration (`questions-a-trancher.md:595`).
* Dater les réglages permet de rejouer un paiement des années plus tard. Le sujet le demande pour tous les termes du calcul (l. 292).
* Une date de début seule rend un trou impossible. C'est le raisonnement d'ADR-030, appliqué aux réglages.
* ⚠️ **Le `CHECK` de `final_rate` grave deux paramètres en base.** Le bornage est une règle (`10_calcul_remuneration_chasseur.feature:201`) ; ses deux valeurs, elles, sont des paramètres. Le groupe a choisi le `CHECK` contre la recommandation de Claude, sans écrire sa raison (`questions-a-trancher.md:737`). 💡 Défense proposée : la valeur vit en table (`rate_floor`, `rate_ceiling`) ; le `CHECK` n'est qu'un garde-fou sur l'argent versé ; ses deux chiffres sont validés par le client (Q-JEF-01, `md/questions/2026-10-07-questions-pour-jeff.html:704`), ce ne sont donc pas des chiffres inventés. Coût assumé : deux gestes pour changer une borne.
* Le sujet veut un calcul pur, chargé par une couche au-dessus : « elle charge le `Parametrage`, appelle la fonction, insère le `Remuneration` dans `paiements` » (l. 760). Le service est cette couche. Le sujet appelle ce branchement « un exercice de branchement, pas de réécriture » (l. 341).
* La validation de Jeff change le statut des valeurs. Avant : des propositions du sujet. Après : les valeurs du client (nuance notée sur Q-PAR-06, `questions-a-trancher.md:146`).

**Conséquences**

* **Schéma :** fait. `parameters_fees` (`01:733-751`), `commission_scale` (`01:787-821`), `hunter_rate_parameters` (`01:839-871`). Sur `payment` : `final_rate` (`01:911`), bornes de domaine (`01:921-922`), clé G1 (`01:936-942`). Une base v2 y arrive par `docker/migrations/v2-vers-v3/06_parametres.sql`, `14_reglages-taux-chasseur.sql` et `15_paiement-reglages-taux.sql`.
* **API :** le CRUD existe sur les trois tables (route `/hunter-rate-parameters` pour la troisième). Le service existe : `API/src/app/services/parametrage_service.py:125-155`. Il n'est « Pas encore branché sur une route » (l. 31-32). Le branchement du calcul sur la base reste à écrire (`API/README.md:116-119`).
* **Tests :** version en vigueur à une date, et version suivante (`API/tests/integration/test_parametrage_service.py:34-53`) ; date avant la première version et tables vides : `BaremeIntrouvable` (l. 56-65). Deux versions le même jour : 409 (`test_constraints_db.py:791-797`). Taux final à 0,20 et 0,60 acceptés, 0,19 et 0,61 refusés (`:534-546`). Bornes de domaine (`:627-647`). Tests non relancés pour cet ADR.
* **Seed :** `docker/init-v3/05_parametres.sql` pose le premier jeu : 1 grille d'honoraires, 5 tranches, 1 version de réglages, au 2026-01-01 (l. 19, l. 31-80). Il ne se lance qu'à la création du volume ; pour une base déjà créée, une commande manuelle est écrite (l. 21-24). La base de test ne le rejoue pas (l. 26-27).
* **Une version déjà utilisée peut encore être modifiée.** `PUT` est ouvert sur toutes les tables (`API/src/app/routes/crud_router.py:95-102`). La suppression, elle, est bloquée par `ON DELETE RESTRICT` dès qu'un paiement ou une vente pointe la ligne (`01:935`, `01:942`, `01:765-770`). À coder dans l'API.
* **Changer 20 % ou 60 %, c'est deux gestes.** Une nouvelle version de réglages, et une migration du `CHECK` de `final_rate` (`01:905-911`). Aujourd'hui, une version avec `rate_ceiling` à 0,65 entre dans la table (le test l'insère : `test_parametrage_service.py:34-53`), mais un paiement au-dessus de 0,60 est refusé (`01:911` ; test à 0,61 : `test_constraints_db.py:541-546`).
* **Rien ne vérifie la cohérence d'une version.** Des poids dont la somme n'est pas 1, un plancher au-dessus du plafond, des paliers mal formés : tout est accepté. Le modèle type les paliers en `list[dict[str, Any]]`, sans forme imposée (`API/src/app/models/hunter_rate_parameters_model.py:48-51`). 💡 Proposé : un contrôle dans l'API à l'écriture d'une version, avec ses tests.
* **La fenêtre de 12 mois est stockée, pas utilisée.** Le calcul reçoit les comptes de ventes et de mandats déjà faits. Le sujet dit de les écrire en SQL « une fois les tables créées » (l. 761). À coder.
* **Vente avant la première version :** pas de paramètres, donc `BaremeIntrouvable`. Le seed démarre au 2026-01-01 (`05_parametres.sql:19`). Or des mandats repris datent de 2025 (`02_migration.sql:238`). Le groupe veut le barème « en 2025 » (Q-REM-15, `questions-a-trancher.md:136`) ; le seed de démonstration le posera « dès 2025 » (Q-INF-02, l. 191), pas encore écrit. D'ici là, une vente datée de 2025 lève `BaremeIntrouvable`. Même point qu'ADR-030.
* **Écart au modèle du sujet :** une troisième table, absente de son modèle (l. 264-280). Elle applique la règle de la l. 47 aux réglages. Le `Parametrage` du sujet n'a qu'un jeu de réglages (l. 446-453) : le service lui donne celui en vigueur à la date de l'acte. À dire en soutenance.

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Qui construit le `Parametrage` depuis les tables ? | Le sujet : une couche au-dessus du calcul, qui le charge. L'équipe : un service de la couche services, `ParametrageService`. | `REGLES-CALCUL-REMUNERATION.md:641`, `:760` ; Sébastien, 08/10/2026 (`2026-10-08-notes-seance-adr.md:29`) ; `API/src/app/main.py:9-18` |
| Les réglages du taux varient-ils par chasseur ? | Non : une version vaut pour tous. ✅ Confirmé par le groupe le 09/10/2026 (S8). Le taux d'un chasseur diffère par son ancienneté, son score et son barème propre. Déduit. | déduit de `REGLES-CALCUL-REMUNERATION.md:446-453` ; `Readme.md:80` ; `commission_scale.id_hunter` (`01:801`) |
| Les arrondis vont-ils en table ? | Non : ils restent des constantes du code. Le sujet ne les met pas dans sa liste de valeurs à valider ; il les appelle des « constantes ». Jeff a validé leurs valeurs (Q-JEF-01). Déduit. | déduit de `REGLES-CALCUL-REMUNERATION.md:59`, `:347` ; `remuneration.py:39-41` ; aucune colonne dans `01:839-871` |
| Le palier et le « rien » du non exclusif sont-ils des paramètres ? | Non : des règles, dans le code. Jeff les a confirmées. | `10_calcul_remuneration_chasseur.feature:166` ; Q-JEF-02 et Q-JEF-03 (`2026-10-07-questions-pour-jeff.html:884`, `:927`) |
| Une version déjà utilisée peut-elle être corrigée ? | Non : on insère une nouvelle version datée. Contrôle à coder dans l'API. Déduit. ✅ Confirmé par le groupe le 09/10/2026 (S8). | déduit de `REGLES-CALCUL-REMUNERATION.md:129`, `:292` ; écrit dans `05_parametres.sql:15-17` |
| Q-REM-19 contredit-il Q-REM-05 ? | En partie. Les deux chiffres sont validés par Jeff : ce ne sont plus des propositions, et le `CHECK` tient. Mais ils restent des paramètres gravés en base : en changer un demande deux gestes (Conséquences). | `2026-10-07-questions-pour-jeff.html:704`, `:1979` ; `questions-a-trancher.md:140`, `:223` |
| `commission_scale` passe-t-elle en « à partir du » ? | Non : elle garde ses périodes et ses deux `EXCLUDE`. | ADR-030, questions tranchées |

**Questions ouvertes** 🟡

Aucune.

**Sources**

| Affirmation | Source |
|---|---|
| Règle dans le code, paramètre en table « jamais en dur » ; « Confondre les deux » | `documents utiles/REGLES-CALCUL-REMUNERATION.md:40-47` (StarterPack) |
| Toutes les valeurs chiffrées sont « à valider avec le client » | même fichier, l. 59 |
| « paramètres proposés, non imposés par le métier » | `user-stories/10_calcul_remuneration_chasseur.feature:3-5` (StarterPack) |
| Honoraires et barème « versionnés dans le temps » | `REGLES-CALCUL-REMUNERATION.md:129` |
| Fenêtre de 12 mois, un paramètre | même fichier, l. 139 |
| Tous les termes du calcul stockés, pour rejouer | même fichier, l. 292 |
| Modèle du sujet : deux tables de paramètres | même fichier, l. 264-280 |
| Paramètres « des données, pas du code » ; « exercice de branchement » | même fichier, l. 341 |
| Arrondis : des constantes | même fichier, l. 225-229, l. 347 |
| `Parametrage` : un seul jeu de performance et de modulation | même fichier, l. 446-453 |
| « Cette fonction est un jeu d'essai », « remplacée par une lecture des tables » | même fichier, l. 641, l. 644-686 |
| « La persistance est une couche au-dessus : elle charge le `Parametrage` » | même fichier, l. 760 |
| Comptes sur 12 mois reçus déjà calculés | même fichier, l. 761 |
| Palier ; bornage 20-60 % ; arrondi au centime | `10_calcul_remuneration_chasseur.feature:166`, `:201`, `:253` |
| Barème selon ancienneté et performance | `Readme.md:80` (StarterPack) |
| Q-REM-05 : réponse, options, précision LOT6 | `md/questions/questions-a-trancher.md:575-597`, `:125` |
| Q-REM-19 : réponse, recommandation contraire, raison non notée | même fichier, l. 140, l. 735-744 |
| Q-REM-15 « en 2025 » ; Q-INF-02, seed « dès 2025 » | même fichier, l. 136, l. 191 |
| Q-PAR : propositions, réponses du groupe ; Q-PAR-05 | même fichier, l. 141-148, l. 746-768 |
| Q-PAR tous validés par Jeff ; 20 / 60 ; palier ; « rien pour personne » ; HT | même fichier, l. 222-226 |
| Réponses de Jeff, entretien du 07/10/2026 | `md/questions/2026-10-07-questions-pour-jeff.html:704`, `:884`, `:927`, `:972`, `:1979` |
| Q-PAR-10, 11, 13 : « Valeurs du sujet », 07/10/2026 | même fichier, l. 820-866 |
| Versions « à partir du » et bornes de domaine : Sébastien, LOT6 | `context AI/08-etat.md:244-248` ; `md/journal/2026-10-07-rapport-final-chantier-lot.html:491-504` |
| G2 : renommage, option A | `docker/init-v3/README.md:110-115` ; commit `c8418c6` |
| G1 : le paiement pointe ses réglages | `01_create_fil_rouge_immobilier.sql:936-942` ; commit `7fc63ed` |
| Seed et service : décision de Sébastien | `md/adr/2026-10-08-notes-seance-adr.md:29` ; commits `ef5ef90`, `3adead8` |
| Tables de paramètres, v3 | `docker/init-v3/01_create_fil_rouge_immobilier.sql:733-751`, `:787-821`, `:823-871` |
| « Aucun CHECK sur les valeurs » | même fichier, l. 835-836 |
| `final_rate` 20-60 % ; bornes de domaine | même fichier, l. 905-922 |
| Bornes v2 | `docker/init-v2/01_create_fil_rouge_immobilier.sql:758-759` |
| Seed : valeurs, date, rejouable, base de test | `docker/init-v3/05_parametres.sql:1-80` |
| Mandats repris de 2025 | `docker/init-v3/02_migration.sql:238` |
| Service : rôle, versions, ce qu'il rend, pas branché | `API/src/app/services/parametrage_service.py:1-34`, `:125-155` |
| Constantes d'arrondi ; jeu par défaut | `API/src/app/services/remuneration.py:39-41`, `:296` |
| Paliers sans forme imposée | `API/src/app/models/hunter_rate_parameters_model.py:48-51` |
| `PUT` ouvert | `API/src/app/routes/crud_router.py:95-102` |
| Branchement à écrire | `API/README.md:116-119` |
| Tests | `API/tests/integration/test_parametrage_service.py:34-79` ; `API/tests/integration/test_constraints_db.py:534-546`, `:627-647`, `:791-797` |
| Modèle d'ADR | `documents utiles/JOURNAL-DE-DECISIONS.md:19-40` (StarterPack) |

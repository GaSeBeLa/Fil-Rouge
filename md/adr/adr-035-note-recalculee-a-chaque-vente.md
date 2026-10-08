# ADR-035 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 035 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:58`,
> groupe 2). Il porte la lettre E du pense-bête (`md/questions/questions-a-trancher.md:400`).
> Il cite ADR-042 (journal des notes, lettre P) et ADR-048 (critères de
> performance, lettre F) : deux numéros proposés, écrits en brouillon le
> 08/10/2026 (`md/adr/adr-042-journal-des-notes-du-chasseur.md`,
> `md/adr/adr-048-criteres-de-performance.md`).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Aucune question ne reste ouverte.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * `livrables/2-modelisation/09-contraintes-a-coder.md`, contrainte C4 :
>   `HunterPerformance` est listée parmi les tables lues (l. 124-125), et le
>   score proposé est celui « en vigueur à `Sale.signature_date` » (l. 163-165).
>   Les deux sont contredits ici.
> * `md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:74` :
>   le paiement calcule `performance_rate` « à partir du score courant ».
>   Dépassé.
> * `md/journal/2026-09-21-point-etape.md:106-113` : la position de Sébastien
>   (« Le score de cette vente ») y est « à valider par le groupe ». Elle l'est
>   depuis le 02/10/2026.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-035 : Le score d'un paiement se recalcule à partir de la vente ; le journal des notes ne sert pas au calcul

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décision du groupe : 02/10/2026)
* **Statut :** proposé
* **Décideurs :** l'équipe projet — réponse du groupe du 02/10/2026 à la carte Q-REM-06 (« Recalculer à chaque vente ») ; validée par Jeff, client, à l'entretien du 07/10/2026 (Q-JEF-17). Avant : position de Sébastien du 21/09/2026, « à valider par le groupe »
* **Complète :** ADR-033 (le score calculé est figé sur le paiement)
* **Écart au sujet :** `F10:293`, assumé (voir Contexte)

Abréviations : RCR = `documents utiles/REGLES-CALCUL-REMUNERATION.md` ; F10 = `user-stories/10_calcul_remuneration_chasseur.feature` (StarterPack) ; `01` = `docker/init-v3/01_create_fil_rouge_immobilier.sql` ; `rem.py` = `API/src/app/services/remuneration.py`.

**Contexte**

Le sujet dit deux choses qui ne vont pas ensemble.

D'un côté, le score se calcule à partir de la vente :

* le code de référence du sujet note les 5 critères puis fait le score, à partir de la vente, sans lire de score stocké : `noter_criteres`, puis `calculer_score` (`RCR:618-619`). Notre copie, « recopié tel quel », fait de même (`rem.py:10-14`, `:275-276`) ;
* « le score `S` est calculé avant le taux parce qu'il le module, et tout est calculé à la date de l'acte » (`RCR:84`) ;
* trois critères ont la portée « vente » dans le tableau du sujet : le délai, l'exclusivité, les visites (`RCR:143`, `:144`, `:147`). La phrase qui l'annonce en compte deux (`RCR:139`) : une coquille du sujet, déduit du tableau, qui fait foi ici ;
* la modulation « Récompense le travail de cette vente et l'activité récente » (`RCR:208`).

De l'autre, un scénario lit un score gardé :

* « Les indicateurs de performance sont recalculés après le paiement » (`F10:289`) ;
* sa dernière ligne : « Et le nouveau score sert de base au calcul de la prochaine rémunération » (`F10:293`).

Nos notes penchaient pour le score gardé :

* la note v4 : le paiement calcule `performance_rate` « à partir du score courant » (`md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:74`) ;
* la contrainte C4 : le score « en vigueur à `Sale.signature_date` » (`livrables/2-modelisation/09-contraintes-a-coder.md:163-165`).

Le registre range cette contradiction parmi les défauts du sujet (`md/questions/questions-a-trancher.md:1397`).

**Options envisagées**

1. **Recalculer le score à chaque vente** (le code du sujet). `hunter_performance` devient l'historique des notes affichées.
   * Avantages : le score reflète la vente payée ; le code du sujet et ses 55 cas ne changent pas pour cette décision (le critère « mandats » change par ailleurs : ADR-048) ; pas besoin d'un « score de départ », « que le sujet ne définit nulle part » (`md/journal/2026-09-21-point-etape.md:146-147`).
   * Inconvénients : écart à la lettre de `F10:293` ; deux scores à ne pas confondre (celui du paiement, celui du journal).
   * **Retenue.**
2. **Lire la dernière note du journal** `hunter_performance`.
   * Avantage : `F10:293` suivie à la lettre.
   * Inconvénients : un score lu ailleurs ignore le délai, l'exclusivité et les visites de la vente payée ; « calculette et 55 cas à réécrire » (`md/questions/2026-10-07-questions-pour-jeff.html:1157`) ; il faut une note de départ que le sujet ne donne pas.
   * **Écartée.**

**Décision**

1. Le score d'un paiement se calcule au moment du calcul : les 5 notes, puis leur somme pondérée (`RCR:618-619` ; `rem.py:275-276`).
2. Ses entrées : la vente elle-même (délai, exclusivité, visites), et l'activité du chasseur sur les 12 mois avant l'acte, vente en cours exclue (`rem.py:139`, « hors vente en cours » ; `RCR:139`).
3. Le calcul ne lit jamais `hunter_performance`.
4. Le score calculé devra être figé sur `payment.performance_score` (ADR-033). La colonne existe ; son écriture viendra avec le branchement du calcul, pas encore codé.
5. `hunter_performance` est le journal des notes affichées au chasseur (`Readme.md:134-135`). Ses règles relèvent d'ADR-042 ; le calcul de sa note, d'ADR-048.
6. L'écart à `F10:293` est assumé, et dit en soutenance.

**Justification**

* Le code de référence du sujet fait ce choix (`RCR:618-619` ; `rem.py:275-276`). Le réécrire nous éloignerait de la référence que le sujet rejoue contre F10 (`rem.py:16-18`).
* Les critères de la vente pèsent 60 % du score : délai 25 %, exclusivité 10 %, visites 25 % (déduit de `RCR:143-147`). Un score lu ailleurs ne les verrait pas.
* Le client a tranché entre les deux textes : Jeff « valide notre position (ci-dessus), sans changement. Recalculer à chaque vente » (`md/questions/2026-10-07-questions-pour-jeff.html:1161`).
* 💡 Lecture proposée pour la soutenance, qui réduit l'écart sans l'effacer : après le paiement, les compteurs sur 12 mois sont mis à jour (`F10:292`). Le calcul suivant les recompte : la vente payée entre dans ses « ventes sur 12 mois ». L'activité passée sert donc bien de base au calcul suivant ; seule la note, elle, est recalculée.

**Conséquences**

* **Code de calcul :** rien à changer pour cette décision (`rem.py:267-293`). Le critère « mandats » change par ailleurs (Q-PAR-05, ADR-048, `rem.py:214`). Les 13 cas de modulation restent valables : ils reçoivent le score tout fait. Le cas de bout en bout calcule le score avec S₄ : il suit ADR-048 (`API/tests/test_remuneration.py:219-258`).
* **À coder, branchement :** compter les entrées à la date de l'acte. Les visites de la vente, celles du mandat avant l'achat (`RCR:147`, portée « vente » ; `rem.py:137`) ; les ventes et les mandats sur 12 mois (`rem.py:139-140` ; `F10:139-141`). Leurs définitions : Q-REM-07, Q-REM-08, Q-REM-09 (ADR-048). Années d'ancienneté : depuis `hunter.hire_date` (`01:284` ; ADR-037). Délai : depuis la première signature d'une chaîne de renouvellements (ADR-050).
* **Schéma du journal :** fait à LOT6 (`01:996-1025` ; migration `docker/migrations/v2-vers-v3/06_parametres.sql:170-189`). Deux notes le même jour passent (`API/tests/integration/test_constraints_db.py:728-736`).
* **À coder, API :** n'écrire la note `'payment'` qu'une fois le paiement payé (voir les questions tranchées). Aujourd'hui, la base accepte une note `'payment'` sur un paiement seulement annoncé : le test en pose une (`test_constraints_db.py:712-715`).
* **À coder, API :** `POST /hunter-performances` est ouvert (même test, l. 715). ADR-027 prévoit que `hunter_performance` « n'est jamais saisi à la main » (ADR-027, Décision).
* **Deux scores :** le paiement garde le sien ; le journal garde la note d'après (`01:923-925`). Un écran qui affiche les deux doit dire lequel est lequel.

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Quand s'écrit la note `'payment'` du journal ? | Quand le paiement passe à `'paid'`. Contrôle dans l'API, pas encore codé. | déduit de `Readme.md:134` (« une fois le paiement effectué ») et `F10:290` (« une rémunération marquée comme payée ») |
| Un refus donne-t-il une note `'payment'` ? | Non : un refus n'est jamais payé. Un mandat échu a son propre déclencheur, `'mandate_expired'`, hors de cet ADR. | déduit de `01:944-946`, `:965-975` ; `01:1008` |
| Deux ventes le même jour ? | Deux calculs, deux notes au journal, à la seconde près. | Q-SCH-06, `questions-a-trancher.md:161` ; `01:996-1001` ; `test_constraints_db.py:728-736` |
| La note du journal est-elle celle du paiement ? | Non. Le journal est recalculé après le paiement, compteurs mis à jour ; le paiement garde la note du calcul. | `F10:289-292` ; `01:923-925` |
| Faut-il une note de départ pour payer la première vente ? | Non : le calcul ne lit pas le journal. La ligne `'initial'` ne sert qu'à l'affichage ; sa valeur relève d'ADR-048. | déduit de `rem.py:275-276` ; `01:1007-1008` ; `md/journal/2026-09-21-point-etape.md:146-147` |
| Comment la note du journal se calcule-t-elle, hors d'une vente ? | Pas ici : c'est la définition des critères (ADR-048). Le registre note qu'« aucun critère proposé » ne permet la baisse demandée par le sujet. | `questions-a-trancher.md:401`, `:1389` ; ADR-050, Conséquences |

**Questions ouvertes** 🟡

Aucune. Ce qui reste est du code à écrire (Conséquences) et le contenu d'ADR-048.

**Sources**

| Affirmation | Source |
|---|---|
| Le code du sujet recalcule le score à partir de la vente | `documents utiles/REGLES-CALCUL-REMUNERATION.md:618-619` (StarterPack) ; notre copie, `API/src/app/services/remuneration.py:275-276`, « recopié tel quel » (l. 10-14) |
| Le critère « mandats » remplacé par le taux de transformation | Q-PAR-05, `md/questions/questions-a-trancher.md:145` ; `remuneration.py:214` ; ADR-048 |
| Entrées : « hors vente en cours » | même fichier, l. 137-140 |
| Score avant taux, tout à la date de l'acte | `documents utiles/REGLES-CALCUL-REMUNERATION.md:84` (StarterPack) |
| Portée et poids des 5 critères ; la phrase dit « Deux critères », le tableau en marque trois | `REGLES-CALCUL-REMUNERATION.md:139-147` |
| `p` « Récompense le travail de cette vente » | même fichier, l. 208 |
| Ventes et mandats comptés « dans les douze mois précédant l'acte » | `user-stories/10_calcul_remuneration_chasseur.feature:139-141` (StarterPack) |
| Scénario « recalculés après le paiement », `F10:293` | `user-stories/10_calcul_remuneration_chasseur.feature:289-293` (StarterPack) |
| Indicateurs recalculés « une fois le paiement effectué » ; à la baisse sur un mandat échu | `Readme.md:134-135` (StarterPack) |
| Q-REM-06 : options, réponse du 02/10/2026 | `md/questions/questions-a-trancher.md:599-615`, `:126` |
| Q-JEF-17 : validé par Jeff | `md/questions/2026-10-07-questions-pour-jeff.html:1152-1161` ; `questions-a-trancher.md:230` |
| Position de Sébastien du 21/09/2026 | `md/journal/2026-09-21-point-etape.md:106-113`, `:136-147` (note IA, « ne fait pas foi ») |
| Score courant (note v4), score en vigueur (C4) | `md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:74` ; `livrables/2-modelisation/09-contraintes-a-coder.md:124-125`, `:163-165` |
| Défaut du sujet : `F10:293` contre le code | `questions-a-trancher.md:1397` |
| Journal des notes : schéma, déclencheurs, index | `docker/init-v3/01_create_fil_rouge_immobilier.sql:996-1025` |
| Score du paiement ≠ note du journal | même fichier, l. 923-925 |
| Journal : modèle de l'API | `API/src/app/models/hunter_performance_model.py:1-19` |
| Q-SCH-06 : journal, deux notes le même jour | `questions-a-trancher.md:161` ; `docker/migrations/v2-vers-v3/06_parametres.sql:170-189` |
| Tests du journal | `API/tests/integration/test_constraints_db.py:710-736` |
| ADR-027 : jamais saisi à la main | journal Confluence, copie du 07/10/2026, ADR-027, Décision |
| Baisse sur mandat échu : ADR-048 | ADR-050, Conséquences |

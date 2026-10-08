# ADR-042 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 042 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:65`,
> lettre P). Il ne vaut rien tant que le groupe ne l'a pas pris sur Confluence.
>
> 💡 **Rédigé le 08/10/2026 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et
> un arbitre. Les passages marqués « déduit » sont une lecture des sources, pas
> une décision du groupe.
>
> 🗂️ **Deux points réglés hors de la fiche :**
>
> * **Aucun ADR de Confluence à marquer « remplacé ».** Aucun des 27 ADR (copie
>   du 07/10/2026) ne parle de `hunter_performance`.
> * **Les médias de la note d'avis ne sont pas dans cette fiche.** La « note »
>   de ce journal est un score de 0 à 100. La « note d'avis » est le texte du
>   chasseur sur un bien (`estate_searchrequest.review_hunter`). Deux tables,
>   deux décisions : les médias ont leur fiche, ADR-051.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * `livrables/2-modelisation/09-contraintes-a-coder.md`, contrainte C6 :
>   « Dépend de : D9 » (l. 191) et « Fermer la période du score précédent
>   (`valid_until`) » (l. 220-221) sont sans objet depuis le journal.
> * `livrables/2-modelisation/09-decisions-a-prendre.md` : D9 a encore
>   « Décision retenue » vide (l. 435) et « ouverte » au tableau de bord (l. 71).
> * MPD v8 : l'index `idx_perf_hunter_scored_at` manque
>   (`md/adr/2026-10-08-notes-seance-adr.md:114`). Il fait partie de la décision
>   (voir « Questions tranchées »).
> * `md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:40-70`
>   décrit encore les périodes et l'`EXCLUDE`. C'est une note datée : à ne plus
>   citer comme le schéma actuel.
> * Le commentaire du test `API/tests/integration/test_constraints_db.py:729-731`
>   dit qu'en v2 « il fallait un jour d'écart ». D9 dit « au moins deux jours »
>   (`livrables/2-modelisation/09-decisions-a-prendre.md:422-423`) : à aligner.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-042 : Les notes de performance du chasseur forment un journal : une ligne datée à la seconde par note, la dernière est la note actuelle

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décision du groupe : 05/10/2026)
* **Statut :** proposé
* **Décideurs :** le groupe — réponse du 05/10/2026 à la carte Q-SCH-06. La case cochée était « tsrange » ; le commentaire dit « ni « garder », ni tsrange ». Le registre retient le commentaire : « le commentaire fait foi » (`md/questions/questions-a-trancher.md:102`, `:161`, `:438`).
* **Remplace :** aucun ADR. Ferme la décision D9 de `livrables/2-modelisation/09-decisions-a-prendre.md`.
* **Lien :** suit ADR-035 (lettre E, proposé) : la note est recalculée à chaque vente (Q-REM-06).

**Contexte**

Le sujet fait bouger la note d'un chasseur deux fois :

* après un paiement, « mes indicateurs de performance sont recalculés et affichés » (`07_chasseur_remuneration_et_performance.feature:34`) ;
* à l'échéance d'un mandat sans vente, ils sont « recalculés à la baisse » (même fichier, l. 41).

En v2, `hunter_performance` était « historisé par période » (`docker/init-v2/01_create_fil_rouge_immobilier.sql:798`) :

* `valid_from DATE NOT NULL` et `valid_until DATE` (l. 803-804) ;
* `chk_perf_period` : `CHECK (valid_until IS NULL OR valid_until > valid_from)` (l. 811-812) ;
* `excl_perf_no_overlap` : deux périodes d'un même chasseur ne se chevauchent pas, bornes `'[]'` (l. 821-825).

L'`EXCLUDE` venait d'une note d'équipe : sans lui, `Payment.performance_rate` aurait été « ambigu à retrouver par date » (`md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:70`).

Le problème (D9) : avec ces bornes, deux scores d'un même chasseur doivent être séparés d'« au moins deux jours » (`09-decisions-a-prendre.md:422-423`).

Or le groupe a choisi de recalculer la note à chaque vente (Q-REM-06, validé par Jeff : Q-JEF-17). Deux ventes payées le même jour donnent deux notes le même jour. La base v2 refusait la seconde (carte Q-SCH-06, `questions-a-trancher.html:1179-1203`).

**Options envisagées**

1. **Garder** tel quel (D9, option A : « 2 jours d'écart minimum », `09-decisions-a-prendre.md:427`). Avantage : « Rien à faire. » Inconvénient : « La 2e vente du jour fait échouer l'écriture de la note : ne tient plus avec Q-REM-06. » **Écartée.**
2. **`valid_until >= valid_from`** (D9, option B) : « l'écart tombe à 1 jour » (`09-decisions-a-prendre.md:428`). Deux notes le même jour restent refusées. Passer les bornes en `'[)'` ne suffit pas non plus (`questions-a-trancher.md:952-953`). **Écartée.**
3. **Passer en `tsrange`** (D9, option C) : des périodes à l'heure près. Avantage : « Les périodes restent, à l'heure près. » Inconvénient : « Réécrire `chk_perf_period` et l'exclusion ; plus lourd que le journal pour le même résultat. » **Écartée**, bien que cochée : le commentaire du groupe l'écarte.
4. **Un journal des notes** : une ligne datée par note, sans période. Avantage : « Deux ventes le même jour passent. » Inconvénient : « La fin de validité n'est plus écrite : elle se déduit de la note suivante. Base à recréer. » **Retenue.**

(Avantages et inconvénients des options 1, 3 et 4 recopiés de la carte : `questions-a-trancher.html:1199-1201`.)

**Décision**

Le commentaire du groupe, recopié : « Chaque note = une ligne datée à la seconde (scored_at TIMESTAMP NOT NULL) ; la note actuelle = la dernière ligne. On retire valid_from, valid_until, chk_perf_period et excl_perf_no_overlap ; on ajoute UNIQUE (id_payment), UNIQUE (id_mandate) et un index (id_hunter, scored_at DESC). » (`questions-a-trancher.md:161`).

1. Une note = une ligne, datée à la seconde : `scored_at TIMESTAMP NOT NULL` (`docker/init-v3/01_create_fil_rouge_immobilier.sql:1006`).
2. Plus de période : `valid_from`, `valid_until`, `chk_perf_period` et `excl_perf_no_overlap` sortent.
3. La note actuelle d'un chasseur = sa ligne au `scored_at` le plus récent. Elle se lit par l'index `idx_perf_hunter_scored_at ON hunter_performance (id_hunter, scored_at DESC)` (`01:1023-1025`).
4. Un paiement, ou un mandat échu, donne une note et une seule : `uq_perf_payment UNIQUE (id_payment)` et `uq_perf_mandate UNIQUE (id_mandate)` (`01:1018-1020`).
5. Le reste ne change pas : `score NUMERIC(4,1)` de 0 à 100, `trigger_type` (`'initial'`, `'payment'`, `'mandate_expired'`) et `chk_perf_source` (`01:1005-1017`).
6. Une nouvelle note ajoute une ligne. Elle ne modifie pas la précédente.

**Justification**

* Deux notes le même jour passent : c'est ce que Q-REM-06 exige. Testé : une note à 9 h et une à 17 h le même jour, 201 (`API/tests/integration/test_constraints_db.py:728-736`).
* Plus simple que `tsrange` : pas de période à fermer, donc pas de mise à jour de la note précédente.
* Une note vaut jusqu'à la suivante. Même idée que les grilles d'honoraires « à partir du » (ADR-030).
* L'argument de l'`EXCLUDE` ne tient plus. Le paiement n'a plus à retrouver son score par date : il le fige lui-même, dans `payment.performance_score` (`01:923-927`, Q-REM-03 ; ADR-033, proposé).
* L'historique est gardé. Q-REM-06 l'avait annoncé : « `hunter_performance` = **historique** » (`questions-a-trancher.md:608`).

**Conséquences**

* **Schéma :** fait à LOT6 (commit `7a862ea`) : `01:996-1025`.
* **Migration v2 :** `docker/migrations/v2-vers-v3/06_parametres.sql:168-189`. Une note reprise est datée du début de sa période v2, à minuit (l. 168-169). La migration s'arrête si une date de fin v2 disait autre chose que « la veille de la note suivante » : elle serait perdue (l. 50-85).
* **Données :** 0 note en base de dev (compté le 07/10/2026, `06_parametres.sql:20-21`). La reprise n'en crée aucune : `hunter_performance` reste vide (`docker/init-v3/02_migration.sql:42`). Les chasseurs repris n'ont donc pas de note `'initial'`. Ce qu'on affiche sans note : voir ADR-048, question ouverte n° 2 (note de départ, proposée).
* Le calcul n'en souffre pas : il recalcule la note à chaque vente, sans lire cette table (ADR-035). La table sert à l'affichage (« recalculés et affichés », `07_…feature:34`) et à l'historique (`questions-a-trancher.md:608`).
* **API :** le modèle porte `scored_at` et décrit le journal (`API/src/app/models/hunter_performance_model.py:1-18`, l. 35). Le service n'a aucune règle (`services/hunter_performance_service.py`).
* **Tests :** un même paiement deux fois, 409 ; un même mandat deux fois, 409 ; deux notes le même jour, 201 (`test_constraints_db.py:710`, `:720`, `:728`).
* **Reste à coder dans l'API :** les contrôles de C6. Après un paiement, la nouvelle note est **≥** à la précédente ; après un mandat échu, **≤** (`09-contraintes-a-coder.md:212-219`). « La précédente » est désormais la dernière ligne du chasseur. La note `'mandate_expired'` s'écrit quand un mandat expire : l'expiration est elle-même à coder (ADR-046).
* **Reste à coder dans l'API :** une note écrite ne se modifie plus. Aujourd'hui, `PUT` et `DELETE` sur `/hunter-performances/{id}` sont ouverts (`API/src/app/routes/crud_router.py:95-111`). La matrice des droits dit que la table est « écrite par le système » (`md/securite/matrice-droits-crud-par-role.md:199`).
* 💡 **Égalité à la seconde** (micro-décision, hors ADR : `JOURNAL-DE-DECISIONS.md:13`) : rien n'interdit deux notes d'un même chasseur à la même seconde (pas de `UNIQUE (id_hunter, scored_at)`). « La dernière ligne » serait alors ambiguë. Proposition : départager par `id` décroissant, l'ordre d'écriture.
* **`btree_gist` reste** (`01:149`), mais plus pour cette table : il sert à l'`EXCLUDE` de `commission_scale` (`01:808-813`, ADR-030).
* **Journal :** aucun ADR remplacé. D9 est fermée.

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| `scored_at` ou `created_at` : lequel date la note ? | `scored_at`, le moment de la note. `created_at` dit quand la ligne a été écrite. Déduit : `scored_at` n'a pas de valeur par défaut, l'API la fournit ; `created_at` prend `now()`. La migration date une note reprise par sa date métier (`valid_from`), pas par `created_at`. | déduit de `01:1004`, `01:1006` ; `06_parametres.sql:168-176` ; `hunter_performance_model.py:35` (« le moment de la note, à la seconde ») |
| L'index `idx_perf_hunter_scored_at` va-t-il dans le MPD ? Les notes du jour disent « pas dans le MPD, pas décidé ». | Oui. Il fait partie de la décision du groupe (« un index (id_hunter, scored_at DESC) »). Et le sujet définit le MPD comme « Le SQL réel (types MySQL/PostgreSQL, index…) ». | `questions-a-trancher.md:161` ; `documents utiles/MCD-MERISE.md:15` (StarterPack) ; `md/adr/2026-10-08-notes-seance-adr.md:114` |
| Que veut dire chaque `trigger_type` ? | `'initial'` : « le score de départ, à l'embauche » ; `'payment'` : « recalculé à la suite d'un versement » ; `'mandate_expired'` : « recalculé parce qu'un mandat s'est éteint sans vente ». Ce sont les deux déclencheurs du sujet, plus le départ. | `hunter_performance_model.py:13-15` ; `07_…feature:29-41` ; `Readme.md:134-135` (StarterPack) |
| Le score d'un paiement passé se retrouve-t-il dans le journal ? | Non : il est figé sur le paiement. « `hunter_performance.score` est recalculé APRÈS le paiement : ce n'est pas le même. » | `01:923-927` (Q-REM-03) |
| « Le nouveau score sert de base au calcul de la prochaine rémunération » (`F10:293`) : le journal sert-il au calcul ? | Non. La note est recalculée à chaque vente ; l'écart à `F10:293` est assumé, et validé par Jeff. Il s'écrit dans ADR-035. | `questions-a-trancher.md:126`, `:230` ; `10_calcul_remuneration_chasseur.feature:289-293` (StarterPack) |
| Peut-on retirer l'extension `btree_gist` ? | Non. Le journal n'en a plus besoin, mais `excl_scale_no_overlap` de `commission_scale` compare un entier (`id_hunter WITH =`), ce qui l'exige. | `01:149` ; `01:808-813` ; ADR-030 |

**Questions ouvertes** 🟡

Aucune. Ce qui reste est du code à écrire, listé dans les Conséquences.

**Sources**

| Affirmation | Source |
|---|---|
| Indicateurs recalculés après paiement, à la baisse à l'échéance | `user-stories/07_chasseur_remuneration_et_performance.feature:29-41` ; `Readme.md:134-135` (StarterPack) |
| `F10:293` : le nouveau score sert de base au calcul suivant | `user-stories/10_calcul_remuneration_chasseur.feature:289-293` (StarterPack) |
| MPD = « Le SQL réel (types MySQL/PostgreSQL, index…) » | `documents utiles/MCD-MERISE.md:15` (StarterPack) |
| v2 : périodes, `chk_perf_period`, `excl_perf_no_overlap`, TODO D9 | `docker/init-v2/01_create_fil_rouge_immobilier.sql:798-825` |
| Origine de l'`EXCLUDE` : retrouver le taux par date | `md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:70`, `:138` |
| D9 : deux jours d'écart ; options A, B, C | `livrables/2-modelisation/09-decisions-a-prendre.md:418-435` |
| Q-SCH-06 : journal ; le commentaire fait foi | `md/questions/questions-a-trancher.md:102`, `:161`, `:438` ; `questions-a-trancher.html:1179-1203` |
| `'[)'` ne suffit pas | `questions-a-trancher.md:952-953` |
| Q-REM-06 : recalcul à chaque vente ; table = historique ; Jeff Q-JEF-17 | `questions-a-trancher.md:126`, `:230`, `:599-615` |
| Lettre P | `questions-a-trancher.md:411` |
| `hunter_performance` v3 : journal, `UNIQUE`, index | `docker/init-v3/01_create_fil_rouge_immobilier.sql:996-1025` |
| Score figé sur le paiement (Q-REM-03) | même fichier, l. 923-927 |
| `btree_gist`, `EXCLUDE` de `commission_scale` | même fichier, l. 149, l. 808-813 |
| LOT6 : commit `7a862ea` | `git log` du dépôt |
| Migration v2 : garde, conversion | `docker/migrations/v2-vers-v3/06_parametres.sql:16-18`, `:20-21`, `:50-85`, `:168-189` |
| La reprise laisse la table vide | `docker/init-v3/02_migration.sql:42` |
| Modèle de l'API | `API/src/app/models/hunter_performance_model.py:1-18`, `:35` |
| Tests | `API/tests/integration/test_constraints_db.py:710`, `:720`, `:728-736` |
| `PUT` et `DELETE` ouverts | `API/src/app/routes/crud_router.py:95-111` |
| Contrôles C6 ; période à fermer (obsolète) | `livrables/2-modelisation/09-contraintes-a-coder.md:186-221` |
| Table « écrite par le système » | `md/securite/matrice-droits-crud-par-role.md:199` |
| Index absent du MPD | `md/adr/2026-10-08-notes-seance-adr.md:114` |
| Table lue pour l'affichage ; « historique » | `07_…feature:34` (StarterPack) ; `questions-a-trancher.md:608` |
| Modèle d'ADR, micro-décisions, « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:13`, `:19-40`, `:72` (StarterPack) |

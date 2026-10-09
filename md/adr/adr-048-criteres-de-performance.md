# ADR-048 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 048 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:79`).
> Il porte la lettre F du pense-bête (`md/questions/questions-a-trancher.md:401`).
>
> 💡 **Rédigé le 2026-10-08 par Claude**, d'après les fichiers du dépôt et le
> sujet. Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Aucune question ne reste ouverte. La grille du taux est une
> proposition de l'équipe, adoptée avec la fiche : le client l'a laissée au
> groupe (Q-JEF-05). La note hors d'une vente est tranchée par déduction, à
> confirmer par le groupe.
>
> 🗂️ **Liens avec les autres brouillons** (pas la décision) :
>
> * ADR-035 renvoie ici « le calcul de sa note » et la valeur de la ligne
>   `'initial'` (`md/adr/adr-035-note-recalculee-a-chaque-vente.md:87`, `:114-115`).
> * ADR-050 renvoie ici la baisse des indicateurs quand un mandat arrive à
>   échéance sans vente (`md/adr/adr-050-renouvellement-du-mandat.md:155`).
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * `questions-a-trancher.md:228` : « 🟡 Sens du critère à vérifier dans le
>   code du sujet avant l'ADR F ». Vérifié, à clore.
> * La carte Q-REM-07 cite `01:635` pour `visitor_type` : c'était la ligne de
>   v2. En v3, c'est `01:717`.
> * ADR-035 dit « Le critère « mandats » remplacé par le taux de
>   transformation » (`adr-035-…md:126`). Cette fiche dit : le critère reste,
>   sa notation change. À aligner.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-048 : La note du chasseur — cinq critères, moins de visites vaut mieux, « mandats signés » noté par le taux de transformation

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (réponses du groupe : 02/10/2026 et 05/10/2026 ; client : 07/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * l'équipe projet : quelles visites, ventes et mandats comptent (Q-REM-07, 08, 09, le 02/10/2026) ; le taux de transformation (Q-PAR-05, le 05/10/2026) ;
  * le client (Jeff, formateur jouant le commanditaire et le PO), le 07/10/2026 : il valide les trois comptes « sans changement » (Q-JEF-08, Q-JEF-09) ; il n'a pas de grille pour le taux, « le groupe propose la sienne » (Q-JEF-05).
* **Complète :** ADR-035 (le score se recalcule à chaque vente : cet ADR dit ce qu'il compte) et ADR-050 (renouvellement du mandat).
* **Écart au sujet :** aucun critère ne change. Le critère « nombre de mandats signés » reste : « Les cinq critères sont **imposés** ; leur notation et leur pondération sont *(paramètres)* » (RCR:137). Sa **notation** change : ventes ÷ mandats, au lieu de mandats × 10. C'est la décision D5, que le sujet laisse ouverte (RCR:315, `:325`). Sa proposition était « Séparés, fidèles au Readme » (RCR:325) ; le groupe s'en écarte (Q-PAR-05). Le sujet nomme lui-même cette variante : « remplacer S₄ par le **taux de transformation** » (RCR:160).

Abréviations : RCR = `documents utiles/REGLES-CALCUL-REMUNERATION.md` ; F07, F10 = `user-stories/07_chasseur_remuneration_et_performance.feature`, `user-stories/10_calcul_remuneration_chasseur.feature` (StarterPack) ; `01` = `docker/init-v3/01_create_fil_rouge_immobilier.sql` ; `rem.py` = `API/src/app/services/remuneration.py` ; `jeff.html` = `md/questions/2026-10-07-questions-pour-jeff.html` ; `reg` = `md/questions/questions-a-trancher.md`. Une **chaîne** = un mandat et ses renouvellements (ADR-050).

**Contexte**

Le sujet impose cinq critères de performance (`Readme.md:84-88`). « La performance se calcule sur **exactement cinq critères** » (RCR:55). Leur notation et leurs poids sont des paramètres (RCR:137). Chaque critère est ramené sur une échelle 0–100 (RCR:137). Il en propose une grille (RCR:143-147).

Trois comptes restaient flous : quelles visites, quelles ventes, quels mandats. Le groupe a répondu le 02/10. Le client a validé le 07/10.

Le sujet veut aussi qu'un mandat fini sans vente fasse baisser la note :

* « Les indicateurs de performance sont alors recalculés à la baisse et affichés au chasseur » (`Readme.md:135`) ;
* F07:37-41 place cette baisse à l'échéance, quand le chasseur « est invité à renouveler » le mandat ;
* F10:295-300 : « le mandat reste compté dans le nombre de mandats signés », « aucune vente n'est comptée pour ce mandat », « le score de performance du chasseur est recalculé à la baisse ».

Or la notation proposée pour les mandats est S₄ = `min(100 ; mandats × 10)` (RCR:146). Un mandat de plus ne fait jamais baisser la note (`jeff.html:994`). Le sujet propose lui-même une variante : le taux de transformation `ventes / mandats`, qui « mérite d'être posée au client » (RCR:160). Le groupe l'a choisie le 05/10 (Q-PAR-05). Le sujet ne donne pas de grille pour ce taux. Le client non plus.

Deux points restaient à vérifier :

* le sens du critère « visites » (`reg:228`) ;
* la portée des critères : RCR:139 dit « Deux critères portent sur **la vente en cours** […], trois sur **l'activité du chasseur** » ; son tableau en range trois sur la vente (RCR:141-147).

**Options envisagées**

Sur la notation des mandats :

1. **Garder S₄ du sujet**, `mandats × 10`. Avantages : code et cas de test du sujet intacts. Inconvénient : un mandat sans vente ne fait jamais baisser la note ; la phrase du sujet reste fausse. Écartée par le groupe (Q-PAR-05).
2. **Une pénalité par mandat échu, ou ne compter que les mandats transformés.** Ces deux moyens viennent de la carte (`reg:788-790`). Le groupe n'a choisi qu'entre « séparés » et « taux » (`reg:761`). Non retenues ; raisons déduites :
   * la pénalité peut vivre dans la notation de S₄, mais demande une grille de plus (combien de points par mandat échu), que ni le sujet ni le client ne donnent ;
   * ne compter que les mandats transformés recompte les ventes, déjà dans S₃ : un mandat a au plus une vente (`01:763`).
3. **Noter « mandats signés » par le taux de transformation**, poids inchangés. Avantages : un mandat sans vente fait baisser la note ; le taux mesure « l'efficacité plutôt que le volume » (RCR:160). Inconvénients : une ligne du code du sujet change, des cas de test sont à refaire, et la grille est à écrire. **Retenue** (Q-PAR-05, 05/10/2026).

Sur le dénominateur du taux (sous-choix de l'option 3) :

* **Tous les mandats signés sur 12 mois.** Écartée : la note baisse dès la signature, et remonte à la vente (`jeff.html:994`).
* **Les chaînes closes seulement** (premier jet de cette fiche). Écartée : un renouvellement garde la chaîne ouverte, donc la note ne baisse pas à l'échéance. Or F07:37-41 place la baisse là, quand le chasseur est invité à renouveler.
* 💡 **Une chaîne entre au dénominateur à sa première issue** : vente, clôture, ou première échéance sans vente. **Retenue**, proposition de l'équipe (Décision, point 7).

**Décision**

✅ veut dire « établi par une source », pas « codé ». Aucun des comptages n'est codé (voir Conséquences).

1. ✅ **Cinq critères, poids du sujet** : délai 25 %, exclusivité 10 %, ventes 25 %, mandats 15 %, visites 25 % (RCR:143-147 ; Q-PAR-06 ; Q-JEF-01). Fenêtre : douze mois glissants avant l'acte (RCR:139 ; Q-PAR-04). Les valeurs vivent dans `hunter_rate_parameters`, jamais en dur (RCR:47 ; `01:839-871`). Trois critères portent sur la vente (délai, exclusivité, visites) ; deux sur l'activité (ventes, mandats) (Questions tranchées).
2. ✅ **Délai (S₁) et exclusivité (S₂)** : grilles du sujet (RCR:143-144 ; Q-PAR-13 ; Q-JEF-01). Le délai part de la première signature d'une chaîne de renouvellements (ADR-050).
3. ✅ **Ventes (S₃)** : `min(100 ; ventes × 20)` (RCR:145). Comptées : les ventes des mandats du chasseur, sauf celles dont le paiement est refusé, dans les 12 mois avant l'acte, vente en cours exclue (Q-REM-08 ; Q-JEF-09 ; RCR:470).
4. ✅ **Visites (S₅) : moins il y en a, meilleure est la note.** Grille du sujet : 3 ou moins → 100, plus de 15 → 0 (RCR:147). Comptées : les visites du client (`visitor_type = 'client'`, `01:717`), sur tous les biens du mandat, jusqu'au jour de l'acte (Q-REM-07 ; Q-JEF-08). Les visites de repérage du chasseur (`'hunter'`) ne comptent pas.
   * 💡 Mandat renouvelé : compter les visites de toute la chaîne, comme le délai (point 2). Sinon, renouveler remettrait le compteur à zéro.
5. ✅ **« Mandats signés » (S₄) est noté par le taux de transformation** (Q-PAR-05 ; RCR:160). Les cinq poids restent : le critère pèse 15 % (`reg:145`).
6. ✅ **Mandats comptés : signés, sans les renouvellements.** Une chaîne compte une fois (Q-REM-09 ; Q-JEF-09 ; `01:470`).
7. 💡 **La grille du taux : proposition de l'équipe, adoptée avec la fiche**, marquée « proposition du groupe ». Jeff : « pas de grille de sa part : le groupe propose la sienne » (Q-JEF-05, `jeff.html:996`).
   * **La note :** `min(100 ; 100 × T ÷ T_plein)`. `T_plein` est le taux qui donne 100 points : c'est la question posée au client (`jeff.html:989`). Valeur proposée : 100 %. `T_plein` est un réglage de `hunter_rate_parameters`, jamais en dur (RCR:47).
   * **Le dénominateur :** les chaînes comptées par Q-REM-09 (signées dans les 12 mois, une chaîne une fois) qui ont eu une **première issue** : une vente, une clôture (perdue, annulée après signature), ou une **première échéance sans vente**. La chaîne de la vente en cours est exclue des deux termes, comme sa vente (RCR:470).
   * **Le numérateur :** parmi ces chaînes, celles qui finissent par une vente dont le paiement n'est pas refusé (Q-REM-08). Le taux reste entre 0 et 1.
   * **Aucune chaîne au dénominateur :** note 0. Un critère d'activité sans activité vaut 0, comme S₃ et S₄ du sujet (`0 × 20`, `0 × 10`, RCR:145-146).
   * **Mandat annulé après signature :** il compte ; un mandat jamais signé, non. Tranchée par déduction ; confirmée par Sébastien le 2026-10-09 (Discord).
8. **La note du journal hors d'une vente** (mandat échu, note de départ). Tranchée par déduction ; confirmée par Sébastien le 2026-10-09 (Discord). Demande du code, non fait.
   * **Note de départ (`'initial'`) : 50**, le pivot. « Le pivot à 50 est le point d'équilibre » (RCR:213). Elle ne sert qu'à l'affichage (ADR-035, `md/adr/adr-035-note-recalculee-a-chaque-vente.md:114`).
   * **À l'échéance :** reprendre les cinq notes du dernier paiement payé, gardées dans `payment.calculation_details` (`01:928-931`). Recompter les deux critères d'activité (ventes, taux) à la date de l'échéance. Garder les trois notes de vente.
   * **Échéance avant toute vente payée :** les trois notes de vente valent 50 ; les deux critères d'activité sont recomptés.
   * **La règle commune :** sans activité, un critère d'activité vaut 0 (point 7) ; sans vente, un critère de vente vaut 50, le pivot (RCR:213).

**Justification**

* Le sens des visites est écrit quatre fois dans le sujet, et dans son code (voir Questions tranchées). Le sujet l'explique : « La performance récompense la **justesse du ciblage**, pas le volume d'activité » (RCR:153).
* Le taux rend la baisse possible. Avec `mandats × 10`, un mandat de plus ajoute des points (`jeff.html:994`). Le scénario F10:295-300 (mandat échu toujours compté, aucune vente, score à la baisse) y est impossible. Avec le taux, un mandat sans vente grossit le dénominateur seul. C'est l'atout noté au registre (`reg:145`).
* Le dénominateur pris à la **première issue** met la baisse à l'échéance même, comme F07:37-41 et F10:295-300. La chaîne compte une fois : Q-REM-09, validée par le client, est respectée. Une vente après renouvellement fait remonter la note.
* `T_plein` = 100 % : la note est le taux lu en pour cent, déjà sur l'échelle 0–100 du sujet (RCR:137). Aucun seuil inventé.
* Un mandat annulé après signature compte : sinon, un chasseur annulerait un mandat mal parti avant l'échéance, et éviterait la baisse. La carte Q-JEF-09 le notait : « Avec le taux de transformation, il la fait baisser » (`jeff.html:1092`).
* Les trois comptes viennent du groupe, validés par le client : « il valide notre position (ci-dessus), sans changement » (`jeff.html:1046`, `:1096`).
* Les grilles du sujet sont des paramètres « à valider avec le client » (RCR:59). Le client les a validées (Q-JEF-01, `reg:1163`).

**Conséquences**

* **Code de calcul :** une ligne du code du sujet change, la note « mandats » (`rem.py:214`). C'est un écart au code de référence, à dire en soutenance. Le reste de `noter_criteres` ne bouge pas (`rem.py:204-216`). Demande du code, non fait.
* **Comptages, à coder :** aujourd'hui, `rem.py` reçoit des nombres déjà comptés (`rem.py:137-140`). Aucun code ne compte les visites, ventes ou mandats dans la base. Recherche du 08/10/2026 : dans `API/src`, `nb_visites` n'apparaît que dans `rem.py` (et dans trois fichiers de tests). Le branchement est décrit par ADR-035.
* **Tests :** deux cas utilisent S₄ = `mandats × 10`. Ils sont à refaire, ou à garder comme « cas du sujet » : les critères de volume (`API/tests/test_remuneration.py:174-179`, scénario F10:140-152) et le calcul de bout en bout de Bruno, 73,5 (RCR:248 ; `test_remuneration.py:255`). Le score global de `:184` reçoit ses notes toutes faites : il ne dépend pas de la formule. La carte Q-JEF-05 le disait : « les cas de test qui l'utilisent sont à refaire » (`jeff.html:992`).
* **Schéma :** `hunter_rate_parameters` a `points_per_mandate`, pas de réglage `T_plein`. La base le dit : « La grille de notes du taux de transformation (Q-JEF-05) n'est pas ici : chantier API » (`01:837-838` ; même constat dans `API/src/app/models/hunter_rate_parameters_model.py:22-23`). Un réglage est à ajouter : demande du code, non fait.
* **Traçabilité :** `payment.calculation_details` garde « les 5 notes et les entrées » (`01:928-931`). Il doit garder aussi les deux termes du taux.
* **Conflit d'intérêts :** le chasseur enregistre les visites (Q-ACC-13), et moins de visites donne une meilleure note. Le contre-pouvoir proposé est dans ADR-027 : le client lit ses visites, le manager celles de son équipe.
* **Visite avant la signature :** la base l'accepte encore ; l'API devra la refuser (`01:721-725`). Sinon, une visite mal datée fausse le compte.
* **Limite qui reste, à dire en soutenance :** une seconde échéance sans vente de la même chaîne ne fait plus baisser le taux, car la chaîne compte une fois (Q-REM-09). Un taux déjà à 0 ne peut pas baisser.

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Le critère « visites » : moins, c'est mieux ? | Oui. Le sujet le dit quatre fois, et son code aussi : paliers « ordonnés du meilleur au moins bon », 3 visites → 100, plus de 15 → 0 | `Readme.md:88` (« au moins il y en a, au plus la rémunération monte ») ; RCR:55, `:153` ; F10:116 ; RCR:147 ; RCR:668-670, recopié dans `rem.py:191-196`, `:320-322` |
| Combien de critères portent sur la vente ? | Trois : délai, exclusivité, visites. Deux sur l'activité : ventes, mandats. RCR:139 dit l'inverse ; le tableau, le code et F10 tranchent. Tranchée par déduction : coquille du sujet | RCR:141-147 (colonne « Portée ») ; `rem.py:129-140` ; F10:141, `:259` ; RCR:139 |
| Quelles visites ? | Celles du client, sur tous les biens du mandat, jusqu'au jour de l'acte. `'hunter'` = visite de repérage | Q-REM-07 (`reg:619`) ; Q-JEF-08 (`jeff.html:1046`) ; F10:259 ; `01:716-719` ; `API/src/app/models/visit_model.py:4` |
| Quelles ventes ? | Celles des mandats du chasseur, paiement non refusé, 12 mois avant l'acte, vente en cours exclue | Q-REM-08 (`reg:631`) ; Q-JEF-09 (`jeff.html:1096`) ; RCR:470 ; `rem.py:139` |
| Quels mandats ? | Signés (`signature_date` non vide), sans les renouvellements (`id_mandate_parent` vide) | Q-REM-09 (`reg:640-646`) ; Q-JEF-09 ; `01:452`, `:470` |
| Le taux remplace-t-il un critère ? | Non : il note le critère « mandats signés » ; les cinq poids restent | RCR:137, `:160` ; `reg:145` |
| Les autres grilles ? | Celles du sujet, validées | RCR:143-147 ; Q-PAR-13 (`reg:222`) ; Q-JEF-01 (`reg:1163`) |
| Quelle fenêtre ? | Douze mois glissants avant l'acte | RCR:139 ; Q-PAR-04 (`reg:760`) |
| Pourquoi le taux fait-il baisser la note ? | Déduit : avec S₄, un mandat de plus ajoute des points. Avec le taux, un mandat sans vente grossit le dénominateur seul | RCR:146, `:160` ; `jeff.html:994` ; F10:298-300 |
| Où le sujet place-t-il la baisse ? | À l'échéance, quand le chasseur est invité à renouveler. D'où le dénominateur à la première issue | F07:37-41 ; `Readme.md:135` ; F10:295-300 |
| Un mandat annulé après signature compte-t-il ? | Oui : il a été signé, et Q-REM-09 compte les mandats signés. Un mandat jamais signé ne compte pas. Tranchée par déduction — à confirmer par le groupe. Jeff ne l'a pas tranché : il a validé une position qui le laissait ouvert | Q-REM-09 (`reg:640-646`) ; `jeff.html:1089`, `:1091`, `:1092`, `:1096` |
| Que vaut la note hors d'une vente ? | Départ : 50. À l'échéance : les trois notes de vente du dernier paiement, ou 50 sans paiement ; les deux critères d'activité recomptés. Tranchée par déduction — à confirmer par le groupe | RCR:139, `:143-147` (portée), `:145-146`, `:213` ; `01:928-931`, `:1007-1008` |

**Questions ouvertes** 🟡

Aucune. La grille du taux est une proposition de l'équipe, adoptée avec la fiche (Jeff l'a laissée au groupe, Q-JEF-05). Ce qui reste est du code à écrire (Conséquences).

Où l'on a cherché la grille et la note hors vente : le StarterPack (« transformation » n'apparaît, pour la note, qu'en RCR:160 et RCR:325 ; aucun scénario dans F10 ; RCR:139-160, `:208-213` ; F10:289-300 ; `Readme.md:134-135`) ; le dépôt (`reg:145`, `:227`, `:788-790`, `:1389` ; la carte Q-JEF-05, `jeff.html:987-996` ; `01:837-838` ; `01:996-1025` ; ADR-035).

**Sources**

| Affirmation | Source |
|---|---|
| Les cinq critères, sens des visites | `Readme.md:84-88` (StarterPack) |
| « exactement cinq critères » ; « moins il y en a » | `documents utiles/REGLES-CALCUL-REMUNERATION.md:55` (StarterPack) |
| Critères imposés, notation et poids en paramètres ; échelle 0–100 | même fichier, l. 137 ; aussi l. 47, l. 59 |
| Fenêtre de 12 mois ; « Deux critères portent sur la vente » | même fichier, l. 139 |
| Grille, poids et portée de chaque critère | même fichier, l. 141-147 |
| « justesse du ciblage » | même fichier, l. 153 |
| Variante : remplacer S₄ par le taux de transformation | même fichier, l. 160 |
| D5 : « Séparés, fidèles au Readme » | même fichier, l. 315, l. 325 |
| Pivot à 50 | même fichier, l. 208, l. 213 |
| Bruno : 73,5 | même fichier, l. 237-251 |
| Vente en cours exclue | même fichier, l. 470 ; `rem.py:139` |
| Paliers de visites du code du sujet | même fichier, l. 668-670 ; `rem.py:320-322` |
| Baisse à l'échéance, invité à renouveler | `Readme.md:135` ; `user-stories/07_chasseur_remuneration_et_performance.feature:37-41` ; `user-stories/10_calcul_remuneration_chasseur.feature:295-300` (StarterPack) |
| Visites : « Moins il y a eu de visites avant l'achat, meilleure est la note » ; volumes sur douze mois ; visites avant l'achat | `10_calcul_remuneration_chasseur.feature:116`, l. 141, l. 259 |
| Q-REM-07, 08, 09 : réponses du 02/10 | `md/questions/questions-a-trancher.md:127-129`, `:617-646` |
| Q-PAR-05 : transfo, le 05/10 ; « séparés » ou « taux » ; autres moyens (carte) | même fichier, l. 145, l. 227, l. 761, l. 788-790 |
| Q-PAR-13 et autres paramètres validés | même fichier, l. 222, l. 1163 |
| Jeff valide Q-REM-07, 08, 09 | `md/questions/2026-10-07-questions-pour-jeff.html:1046`, `:1096` ; `questions-a-trancher.md:228-229` |
| Jeff : pas de grille, « le groupe propose la sienne » | `2026-10-07-questions-pour-jeff.html:996` ; `questions-a-trancher.md:1166` |
| Deux lectures du dénominateur ; la question posée | même fichier, l. 994, l. 989 |
| Mandat annulé : laissé ouvert ; le taux fait baisser | même fichier, l. 1089, l. 1091, l. 1092 |
| Le code du sujet : `Vente`, `noter_criteres` | `API/src/app/services/remuneration.py:129-140`, `:191-196`, `:204-216` |
| Réglages en base, sans grille du taux | `docker/init-v3/01_create_fil_rouge_immobilier.sql:837-871` ; `API/src/app/models/hunter_rate_parameters_model.py:22-23` |
| Visites : type, date, mandat ; visite avant signature | `01:713-726` ; `API/src/app/models/visit_model.py:4` |
| Renouvellement : le nouveau mandat pointe l'ancien | `01:465-470` |
| Un mandat, au plus une vente | `01:763` |
| Journal des notes, déclencheurs | `01:1002-1021` |
| Termes du calcul gardés sur le paiement | `01:928-931` |
| Tests du sujet sur S₄ | `API/tests/test_remuneration.py:174-179`, `:184`, `:255` |
| Renvois d'ADR-035 et d'ADR-050 | `md/adr/adr-035-note-recalculee-a-chaque-vente.md:87`, `:114-115` ; `md/adr/adr-050-renouvellement-du-mandat.md:155` |

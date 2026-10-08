# ADR-037 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 037 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:60`,
> groupe 2). Il porte la lettre H du pense-bête (`md/questions/questions-a-trancher.md:403`).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Aucune question ne reste ouverte.
>
> 🎤 **Pour l'oral :** dire « X01 », pas « D2 ». Nos livrables appellent cette
> contradiction « D2 » (`livrables/2-modelisation/09-decisions-a-prendre.md:310`),
> mais le sujet nomme « D2 » une autre décision, le mandat non exclusif
> (`REGLES-CALCUL-REMUNERATION.md:322`).
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * Quatre fichiers disent encore X01 ouvert, ou bloquant : `context AI/08-etat.md`
>   (l. 84-88, l. 104, l. 199-200) ; `API/README.md:154-155` ;
>   `livrables/4-application/rapport-tests.md:250` ;
>   `docker/init-v3/01_create_fil_rouge_immobilier.sql:138` (« Décisions encore
>   ouvertes : D2 (ancienneté) »).
> * `livrables/2-modelisation/09-decisions-a-prendre.md` : D2 « ouverte (à acter) »
>   (l. 64), et « Décision retenue » vide (l. 331).
> * Le registre cite des lignes qui ont bougé : `09-dec:303-324` est
>   aujourd'hui l. 310-331 (`questions-a-trancher.md:403`, `:730`) ;
>   `08-etat.md` l. 80 et 195, et `API/README.md:151` (l. 139) sont aujourd'hui
>   l. 84-88, 199-200 et 154-155.
> * « D2 » nomme deux décisions : la nôtre (ancienneté et performance,
>   `09-decisions-a-prendre.md:310`) et celle du sujet (mandat non exclusif,
>   `REGLES-CALCUL-REMUNERATION.md:322`). Le schéma emploie les deux
>   (`01:877` pour le sujet, `01:912` pour la nôtre) : à préciser dans ses
>   commentaires.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-037 : L'ancienneté et la performance majorent le taux de la tranche ; elles ne choisissent pas le barème

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décision du groupe : 05/10/2026)
* **Statut :** proposé
* **Décideurs :** l'équipe projet — réponse du groupe du 05/10/2026 à la carte Q-REM-18 (« Acter B dans un ADR maintenant »). Le constat « il suffit de l'acter » date du 11/09/2026 (`livrables/2-modelisation/09-decisions-a-prendre.md:15`, `:329`). X01 n'a pas été posée à Jeff ; il a validé les chiffres de l'option retenue (Q-JEF-01)
* **Ferme :** la contradiction X01 entre nos deux notes d'équipe (`livrables/2-modelisation/09-rapport-ecarts-contraintes.md:103` ; options : `09-decisions-a-prendre.md:310-331`)

Abréviations : RCR = `documents utiles/REGLES-CALCUL-REMUNERATION.md` ; F10 = `user-stories/10_calcul_remuneration_chasseur.feature` (StarterPack) ; `01` = `docker/init-v3/01_create_fil_rouge_immobilier.sql` ; `rem.py` = `API/src/app/services/remuneration.py`.

**Contexte**

Le sujet impose que le taux du chasseur dépende de deux choses : « Le taux dépend de l'ancienneté et de la performance du chasseur. » (`RCR:54`).

Le Readme le dit ainsi : le barème est « différent pour chaque chasseur (en fonction de leur ancienneté et de leur performance) » (`Readme.md:80`). Cette phrase seule se lit de deux façons.

Nos deux notes d'équipe l'ont lue différemment (contradiction X01, `livrables/2-modelisation/09-rapport-ecarts-contraintes.md:103`) :

* `md/regles-metier/BAREME-COMMISSION.md:31` : ancienneté et performance donnent « un niveau/score chasseur, qui sert de clé » pour chercher le taux dans le barème. La même ligne avoue : « Ni le Readme ni les user stories ne donnent la formule exacte ».
* `md/regles-metier/NOTES-REMUNERATION-CHASSEUR.md:58-62` : elles majorent le taux de la tranche, par une formule.

Ces notes « ne font pas foi : on remonte toujours à la source officielle du starter pack » (`09-decisions-a-prendre.md:36-38`).

**Options envisagées**

1. **A — Elles choisissent le barème** : un niveau par chasseur, clé du barème avec la tranche et la date.
   * Avantage : une lecture possible de `Readme.md:80`.
   * Inconvénients : aucune source ne dit comment passer de l'ancienneté et du score à un niveau (`BAREME-COMMISSION.md:31` le reconnaît) ; une colonne de niveau sur le barème, et une grille par niveau ; contredit la règle de F10 (`F10:201`) et le § 8 du sujet ; les 13 cas de modulation seraient faux.
   * **Écartée.**
2. **B — Elles majorent le taux** : le barème donne le taux de la tranche, puis l'ancienneté et la performance le modulent.
   * Avantages : c'est la règle métier de F10 et le § 8 du sujet ; le code du sujet le fait déjà ; le schéma aussi (« Le MPD suit déjà B », `09-decisions-a-prendre.md:323-324`) ; rien à changer.
   * Inconvénient : s'éloigne d'une lecture mot à mot de `Readme.md:80`, qui parle d'un barème propre à chaque chasseur. Le barème nominatif y répond (voir Justification).
   * **Retenue.**

**Décision**

1. Le taux de la tranche `r₀` vient du barème : la tranche du prix, à la date de l'acte, dans le barème du chasseur s'il en a un, sinon dans le barème par défaut (`RCR:193` ; `rem.py:230-248`). Le barème n'a aucune colonne de niveau.
2. L'ancienneté et la performance modulent ensuite `r₀` (`RCR:199-203` ; `rem.py:251-264`) :
   * `a = min(taux par année × années révolues ; plafond)` ;
   * `p = (S − pivot) / demi-amplitude × amplitude` ;
   * `r = borne(r₀ × (1 + a + p) ; plancher ; plafond)`.
3. `a` et `p` s'additionnent avant d'être appliqués. `r` est arrondi à 4 décimales, au demi supérieur (`RCR:228` ; `rem.py:40`, `:264`).
4. `a`, `p` et `r` devront être figés sur le paiement : `seniority_rate`, `performance_rate`, `final_rate` (ADR-033). Les colonnes existent ; leur écriture viendra avec le branchement du calcul, pas encore codé.
5. Les réglages de cette formule sont des paramètres, dans `hunter_rate_parameters` (`01:859-867`). Valeurs du seed : 0,02 par an, plafond 0,10 ; pivot 50, demi-amplitude 50, amplitude 0,20 ; plancher 0,20, plafond 0,60 (`docker/init-v3/05_parametres.sql:76-78`). Leur gestion relève d'ADR-034.

**Justification**

* La source officielle tranche, en règle métier : « Le taux de base est majoré par l'ancienneté et modulé par la performance, puis borné entre 20 % et 60 % » (`F10:201`). Les règles de F10 « sont métier » ; seuls les chiffres sont proposés (`F10:3-5`).
* Le sujet donne la formule (`RCR:197-215`) et ses cas (`F10:203-250`). Pour l'option A, aucune source ne donne de formule.
* Le barème « différent pour chaque chasseur » existe déjà : c'est le barème nominatif, pour « négocier une grille avec un chasseur senior » (`RCR:193`). Il ne demande aucun niveau.
* Le code et le schéma suivent B depuis le MPD. Les 13 cas de modulation passent (`API/tests/test_remuneration.py:215-245`).
* Le client a validé les chiffres de B : « Bonus d'ancienneté : jusqu'à +10 %, atteint à 5 ans. Bonus de performance : de −20 % à +20 %. » (`md/questions/2026-10-07-questions-pour-jeff.html:697`, réponse l. 704).

**Conséquences**

* **Schéma et code :** rien à changer. `payment.seniority_rate` et `payment.performance_rate` existent (`01:912-922`) ; le barème n'a pas de niveau (`01:789-821`).
* **Tests :** les 13 cas de modulation et le cas de bout en bout (Bruno, 46,16 %, 6 231,60 €) passent (`API/tests/test_remuneration.py:215-258`). Le même calcul, avec les réglages lus en base, rend 6 231,60 € (`API/tests/integration/test_seed_parametres.py:97-116`).
* **Branchement du calcul :** X01 ne le bloque plus. Il reste à coder pour d'autres raisons (ADR-033, ADR-035).
* **À coder :** compter les années révolues à la date de l'acte, depuis `hunter.hire_date` (`01:284`). Rien ne le fait encore : le calcul reçoit un nombre déjà compté (`RCR:762`).
* **Bornes des colonnes :** `seniority_rate` de 0 à 1, `performance_rate` de −1 à 1 : le domaine d'un taux, pas les chiffres du sujet (`01:914-922`, Q-REM-05). Le `CHECK` 20 %-60 % de `final_rate` (`01:905-911`) relève d'ADR-034.

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Quelles années comptent ? | Les années révolues à la date de l'acte. | `F10:204` ; `rem.py:138` |
| Depuis quelle date ? | `hunter.hire_date`. Pour les chasseurs repris, elle vaut la date de création du compte : une hypothèse, validée par Jeff, à dire en soutenance. | `01:284` ; `docker/init-v3/README.md:290-300` ; Q-REM-16, `questions-a-trancher.md:137`, `:231` ; `2026-10-07-questions-pour-jeff.html:1180` |
| Les deux effets se composent-ils ? | Non, ils s'additionnent : 40 % × (1 + 6 % + 9,4 %) = 46,16 %. | `RCR:211` ; `F10:229-234` |
| Les bornes s'appliquent-elles avant ou après ? | Après la combinaison : 65 % ramené à 60 %, 17,60 % remonté à 20 %. | `F10:236-250` ; `rem.py:263-264` |
| Faut-il une colonne de niveau sur le barème ? | Non. | `09-decisions-a-prendre.md:323-324` ; `01:789-821` |
| Un chasseur au barème nominatif garde-t-il `a` et `p` ? | Oui : le calcul les applique après `r₀`, quel que soit le barème qui l'a donné. | déduit de `rem.py:278-281` |
| Qui crée un barème nominatif ? | La direction. Cela va dans le RACI, pas dans un ADR. | `questions-a-trancher.md:251`, `:427` |

**Questions ouvertes** 🟡

Aucune. La décision était faite de fait ; cet ADR l'écrit.

**Sources**

| Affirmation | Source |
|---|---|
| « Le taux dépend de l'ancienneté et de la performance » | `documents utiles/REGLES-CALCUL-REMUNERATION.md:54` (StarterPack) |
| Formules `a`, `p`, `r` ; amplitudes ; variations additionnées | même fichier, l. 197-215 |
| Barème nominatif, « chasseur senior » | même fichier, l. 193 |
| Arrondi du taux : 4 décimales | même fichier, l. 228 |
| Ancienneté : « donnée RH » | même fichier, l. 762 |
| Règle F10 : majoré, modulé, borné ; cas | `user-stories/10_calcul_remuneration_chasseur.feature:201-250` (StarterPack) |
| Règles métier, chiffres proposés | même fichier, l. 3-5 |
| Barème « différent pour chaque chasseur » | `Readme.md:80` (StarterPack) |
| Option A, « un niveau/score chasseur » | `md/regles-metier/BAREME-COMMISSION.md:31` |
| Option B, la formule | `md/regles-metier/NOTES-REMUNERATION-CHASSEUR.md:56-62` |
| X01 | `livrables/2-modelisation/09-rapport-ecarts-contraintes.md:103`, `:572`, `:597` |
| X01 : options, « Il suffit de l'acter », daté du 11/09/2026 | `livrables/2-modelisation/09-decisions-a-prendre.md:15`, `:89`, `:310-331` |
| Les notes d'équipe ne font pas foi | même fichier, l. 36-38 |
| Q-REM-18 : « Acter B », 05/10/2026 | `md/questions/questions-a-trancher.md:139`, `:724-733` |
| Code du taux | `API/src/app/services/remuneration.py:230-264`, `:278-281` |
| Colonnes du paiement | `docker/init-v3/01_create_fil_rouge_immobilier.sql:905-922` |
| Réglages du taux, seed | même fichier, l. 859-867 ; `docker/init-v3/05_parametres.sql:55-80` |
| Barème sans niveau | `01_create_fil_rouge_immobilier.sql:789-821` |
| Tests | `API/tests/test_remuneration.py:215-258` ; `API/tests/integration/test_seed_parametres.py:97-116` |
| Jeff valide les chiffres (Q-JEF-01) et la date d'entrée (Q-JEF-10) | `md/questions/2026-10-07-questions-pour-jeff.html:697-704`, `:1171-1180` |
| `hire_date` : hypothèse de migration | `docker/init-v3/README.md:290-300` |

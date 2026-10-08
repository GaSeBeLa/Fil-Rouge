# ADR-033 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 033 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:56`,
> groupe 2). Il porte la lettre C du pense-bête (`md/questions/questions-a-trancher.md:398`).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Aucune question ne reste ouverte.
>
> ⚠️ **La Décision 3 attend le oui du groupe.** Score et détail exigés hors
> refus : retenue par déduction. Elle renverse le 3e point de la carte D8 du
> rapport LOT1→LOT5 (« Il n'est pas obligatoire ailleurs »), prise par Claude
> seul et gardée par Sébastien le 07/10/2026
> (`md/journal/2026-10-07-rapport-lot1-a-lot5.html:542` ;
> `md/questions/questions-a-trancher.md:123` ; `context AI/08-etat.md:240-243`).
> Une décision du groupe ne se rejuge pas : si le groupe dit non, la
> Décision 3 et sa migration sortent de la fiche, et D8 reste telle quelle.
>
> 🎤 **Pour l'oral, si le groupe confirme :** « Au lot 5, le score figé a été
> posé facultatif. C'était un choix technique, signalé ouvert dans le rapport.
> Le client a confirmé que chaque paiement garde sa note. Nous fermons la
> question, avec la migration que la carte prévoyait. »
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * `livrables/2-modelisation/09-contraintes-a-coder.md`, contrainte C5
>   (l. 169-182), ne protège que « cinq colonnes » : la liste s'allonge (Décision, point 4).
>   La contrainte C4 (l. 163-165) propose le score « en vigueur à `Sale.signature_date` » :
>   contredit par ADR-035.
> * `md/journal/2026-10-07-rapport-lot1-a-lot5.html:624` et `:627` laissent deux
>   questions 🟡 au groupe (score exigé, noms des clés). La première est la
>   Décision 3, à confirmer. La seconde est une micro-décision, réglée par
>   déduction dans les Conséquences.
> * Si le groupe confirme la Décision 3 : mettre à jour le registre
>   (`questions-a-trancher.md:123`, « non exigé ailleurs »).
> * `md/questions/questions-a-trancher.md:132` dit « C3 codée dans `sale_service` ».
>   Faux aujourd'hui : `API/src/app/services/sale_service.py` fait 8 lignes, sans
>   règle. C'est la réponse du 02/10/2026 (« Appliquer C3 dans sale_service »,
>   l. 670), pas encore du code.
> * `md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:72`
>   (« Pas de duplication des 5 compteurs bruts ») est dépassé par Q-REM-04.
> * `API/tests/integration/test_constraints_db.py:606-612` écrit les clés en
>   français, « en exemple » : à aligner quand les clés seront fixées.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-033 : Un paiement garde tous les termes de son calcul, figés à la date de l'acte

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions du groupe : 02/10/2026 et 08/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * l'équipe projet, le 02/10/2026 : cartes Q-REM-03 (« Ajouter payment.performance_score »), Q-REM-04 (« Une colonne JSONB calculation_details »), Q-REM-11 (« L'API seule, avec un test d'intégration ») et Q-REM-12 (« Appliquer C3 dans sale_service ») ;
  * l'équipe projet, le 08/10/2026 : décision G1 (le paiement pointe sa version de réglages) ;
  * le client, Jeff, à l'entretien du 07/10/2026 : confirmé (Q-JEF-20) ;
  * 🟡 la Décision 3 attend le oui du groupe : elle revient sur le 3e point de la carte D8 (lot 5, 07/10/2026).
* **Complète :** ADR-024 (un refus ne porte aucun terme du calcul) et ADR-030 (la vente pointe sa grille d'honoraires)

Abréviations : RCR = `documents utiles/REGLES-CALCUL-REMUNERATION.md` ; F10 = `user-stories/10_calcul_remuneration_chasseur.feature` (StarterPack) ; `01` = `docker/init-v3/01_create_fil_rouge_immobilier.sql`.

**Contexte**

Le sujet en fait « le point le plus important du document » (`RCR:292`). Si le paiement se recalculait à l'affichage, un changement de grille en 2027 « réécrirait rétroactivement » une rémunération de 2026 (même ligne).

Sa conclusion : « On stocke donc tous les termes du calcul, y compris `bareme_id`, afin de pouvoir rejouer et expliquer le calcul des années plus tard. » (`RCR:292`).

La user story en fait une règle métier : « Les éléments du calcul sont figés à la date de l'acte authentique et ne sont jamais recalculés a posteriori » (`F10:275`). Les éléments conservés : « les honoraires, le score, le taux de base, les modulations et le taux final » (`F10:287`).

Notre schéma v2 figeait les taux, pas le score ni les entrées du calcul :

* la note d'équipe v4 refusait de garder « les 5 compteurs bruts », jugés « déjà calculables » (`md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:72`) ;
* la carte Q-REM-04 montre le contraire : « les visites ou les ventes peuvent changer après coup » (`md/questions/questions-a-trancher.md:564-565`).

ADR-019 s'appuyait sur « la règle de traçabilité déjà actée sur `Payment` » (ADR-019, Conséquences). Aucun ADR du journal ne l'acte (recherche de « traçab », « rejouer », « recalcul » dans sa copie du 07/10/2026). Cet ADR l'écrit.

Au lot 5 (07/10/2026), le score figé a été posé facultatif hors refus. Carte D8 : « Il n'est pas obligatoire ailleurs : Q-REM-03 ne le dit pas » (`md/journal/2026-10-07-rapport-lot1-a-lot5.html:542`). La carte prévoyait de le défaire « si le groupe veut le score obligatoire hors refus » (l. 549).

**Options envisagées**

Cinq questions, tranchées une à une.

A. Garder le score de performance (Q-REM-03)

1. **Une colonne `payment.performance_score`.** Avantage : `F10:287` respectée à la lettre ; le sujet la liste (`score_performance`, `RCR:286`). Inconvénient : une colonne de plus. **Retenue.**
2. **Une clé vers `hunter_performance`.** Inconvénient : elle « pointe vers le score d'après, pas celui du calcul » (`questions-a-trancher.md:556`). **Écartée.**
3. **Rien : le retrouver à partir de `performance_rate`.** Inconvénient : ne marche « que si les paramètres n'ont pas changé » (l. 555). **Écartée.**

B. Garder les 5 notes et les entrées (Q-REM-04)

1. **Une colonne `payment.calculation_details JSONB`.** Avantage : une seule colonne, lisible en soutenance. **Retenue.**
2. **Une colonne par valeur (9 colonnes).** Inconvénient : « alourdit la table pour des valeurs qu'on ne requête jamais » (l. 573). **Écartée.**
3. **Rien : on redérive** (le choix de la note v4). Inconvénient : le paiement ne se rejoue plus si une visite ou une vente change. **Écartée.**

C. Garantir `montant = taux × honoraires` (Q-REM-11)

1. **Un trigger**, ou **une colonne générée.** Inconvénient : la formule a « un plancher, un plafond et un arrondi » ; un trigger la dupliquerait (l. 665). **Écartées.**
2. **L'API seule, avec un test d'intégration.** Avantage : « Une seule source de vérité : `rem.py`, déjà testé sur 55 cas » (l. 666). **Retenue.**

D. Garder la version des réglages du taux (G1)

1. **Non : la version se retrouve par la date.** Avantage : rien à coder. Inconvénient : une limite à dire au jury (`md/journal/2026-10-08-tables-parametres-et-schema.html:512`). **Écartée.**
2. **Oui : une clé `payment.id_hunter_rate_parameters`.** Avantages : cohérent avec Q-REM-13 et `RCR:292` ; « la base protège la version utilisée » (même fichier, l. 522). **Retenue.**

E. Exiger le score et le détail hors refus ? (carte D8, lot 5)

1. **Non : facultatifs hors refus.** C'est le 3e point de la carte D8, et le schéma d'aujourd'hui. Avantage : rien à faire. Inconvénient : « Un paiement normal peut être enregistré sans score » (`rapport-lot1-a-lot5.html:544`). **Écartée par déduction — à confirmer par le groupe.**
2. **Oui : exigés hors refus, vides sur un refus.** Avantage : un paiement versé s'explique toujours. Inconvénients : une migration de plus ; des tests à compléter. **Retenue par déduction — à confirmer par le groupe.**

**Décision**

1. Un paiement non refusé garde tous les termes de son calcul. Le tableau dit où vit chaque terme du modèle du sujet (`RCR:284-289`).

| Terme du sujet (`paiements`) | Chez nous | Ce qui change ensuite |
|---|---|---|
| `vente_id`, `chasseur_id` | `payment.id_sale`, `payment.id_hunter` | rien |
| `date_calcul` | `payment.created_at` (déduit : la ligne naît du calcul) | rien |
| `prix_acte` | `sale.purchase_amount` | rien (point 5) |
| `honoraires` | `sale.fees_amount`, et sa grille `sale.id_parameters_fees` (ADR-030) | rien (point 5) |
| `score_performance` | `payment.performance_score` | rien |
| `bareme_id` | `payment.id_commission_scale` | rien |
| `taux_base` | `payment.base_rate` | rien |
| `majoration_anciennete` | `payment.seniority_rate` | rien |
| `modulation_performance` | `payment.performance_rate` | rien |
| `taux_final` | `payment.final_rate` | rien |
| `montant_remuneration` | `payment.amount` | rien |
| `statut`, `date_paiement` | `payment.status`, `payment.paid_at` | avancent avec les étapes |
| `facture_id` | aucun : la facture est hors périmètre (Q-JEF-23) | — |
| en plus : l'origine de la vente (type `Vente`, `RCR:467`) | `sale.sale_origin` | rien (point 5) |
| en plus : les 5 notes et les entrées | `payment.calculation_details` | rien |
| en plus : la version des réglages du taux | `payment.id_hunter_rate_parameters` (G1) | rien |

2. `calculation_details` porte au moins les 5 notes (délai, exclusivité, ventes, mandats, visites) et les 4 entrées : nombre de visites, années d'ancienneté, ventes et mandats sur 12 mois (Q-REM-04 ; `API/src/app/services/remuneration.py:137-140`). Son contenu exact : voir les Conséquences.
3. **Retenue par déduction — à confirmer par le groupe ; renverse le 3e point de la carte D8 ; demande une migration.** Hors refus, `performance_score` et `calculation_details` seront exigés. Sur un refus, ils resteront vides. Aujourd'hui, le schéma ne les exige pas (`chk_refused`, `01:965-983`). Les raisons sont dans la Justification.
4. Une fois le paiement écrit, seuls `status` et les dates d'étape (`announced_at`, `scheduled_for`, `paid_at`) devront changer. Tous les autres termes du tableau devront rester tels quels. Pas encore codé.
5. Les termes rangés sur la vente ne devront plus se modifier : les honoraires (C3, Q-REM-12), et aussi le prix, la date de l'acte, la grille et l'origine de la vente (déduit, voir les questions tranchées). Pas encore codé.
6. Le montant ne sera vérifié que par l'API : il sortira de `rem.py`, et un test d'intégration comparera `amount` à `final_rate × fees_amount` arrondi (Q-REM-11). Pas de trigger. Pas encore codé.
7. Figer ne veut pas dire relancer : le calcul ne se refait jamais sur un paiement existant (`RCR:764`). Les termes gardés servent à l'expliquer, et à le refaire à la main lors d'un contrôle (`RCR:292`).

**Justification**

* Le sujet l'exige en règle métier (`F10:275`). Il en fait un des « deux points qui prouvent que la règle a été comprise » (`RCR:770`).
* Le score et les entrées bougent après coup : la note du journal est recalculée après le paiement (`01:923-925`) ; les visites et les ventes peuvent changer (Q-REM-04).
* Une colonne JSONB suffit : ces valeurs se relisent, elles ne se requêtent pas.
* Le contrôle du montant reste à un seul endroit, le code du sujet (Q-REM-11).
* Le client l'a confirmé : Jeff « valide notre position (ci-dessus), sans changement » (`md/questions/2026-10-07-questions-pour-jeff.html:1919`).
* **Décision 3, à confirmer par le groupe.** Les arguments :
  * Le client a validé « Chaque paiement gardera la note de performance du chasseur, et le détail du calcul » (`2026-10-07-questions-pour-jeff.html:1912`, réponse l. 1919). Un paiement sans score ne la garderait pas.
  * Le sujet compte le score parmi les éléments conservés (`F10:287`).
  * Le taux final est déjà exigé dès l'annonce (Q-REM-10, `01:962-963`). Or le score se calcule avant le taux (`RCR:84`) : un taux connu suppose un score connu.
  * Sur un refus, rien n'est calculé : le code rend un refus sans notes (`remuneration.py:269-270`). D'où « vides sur un refus » (ADR-024).
  * Contre : D8 dit vrai, aucune réponse du groupe n'exige le score en toutes lettres (« Q-REM-03 ne le dit pas »). L'obligation est une déduction : d'où le oui du groupe attendu.
  * Les deux premiers points de D8 restent : bornes de 0 à 100, score interdit sur un refus.

**Conséquences**

* **Schéma :** fait à LOT5 pour le score et le détail (`01:923-931` ; migration `docker/migrations/v2-vers-v3/05_paiement.sql:66-72`). G1 : `01:936-942` et `chk_refused` (l. 975, 983), migration `15_paiement-reglages-taux.sql`, commit `7fc63ed`.
* **Tests :** un refus avec un score, 409 (`API/tests/integration/test_constraints_db.py:565-568`) ; G1, trois tests (l. 571-589) ; le détail se relit tel quel (l. 603-624).
* **Décision 3, si le groupe la confirme — déduit, demande du code, non fait :** exiger `performance_score` et `calculation_details` hors refus, et `calculation_details` vide sur un refus, dans `chk_refused` (`01:965-983`). Une migration v2 → v3 de plus. `payment_payload` des tests envoie un score, pas de détail (l. 507-531) : à compléter.
* **Contenu du détail — déduit, demande du code, non fait.** Une micro-décision (`JOURNAL-DE-DECISIONS.md:13`), réglée ainsi :
  * Le détail garde les 5 notes, et chaque entrée du type `Vente` que rien d'autre ne fige. Le sujet : « Le type `Vente` est la liste minimale des données d'entrée du calcul » (`RCR:766`) ; « tous les termes du calcul » (`RCR:292`).
  * Déjà figés ailleurs : le chasseur (`payment.id_hunter`) ; le prix, la date de l'acte et l'origine (sur la vente, point 5).
  * Donc, dans le détail : la date de signature qui compte pour le délai (la première de la chaîne, ADR-050), la date de fin du mandat, l'exclusivité, le nombre de visites, les années d'ancienneté, les ventes et les mandats sur 12 mois. Les trois premières se lisent sur le mandat (`01:452`, `:457`, `:458`), qui reste modifiable.
  * Si ADR-048 change les entrées du critère « mandats » (Q-PAR-05), le détail garde celles du nouveau critère.
  * Les clés sont en anglais : c'est un schéma de données (ADR-002, Décision). 💡 Noms proposés : `notes` (`delay`, `exclusivity`, `sales`, `mandates`, `visits`, comme les colonnes de poids, `01:844-848`), puis `mandate_signature_date`, `mandate_ends_at`, `is_exclusive`, `visit_count`, `seniority_years`, `sales_12_months`, `mandates_12_months`. Le service traduit, comme il le fait déjà pour les réglages (`API/src/app/services/parametrage_service.py:96-110`). Les noms se fixent dans le code, au branchement du calcul.
* **À coder, API :** la couche qui charge le paramétrage, appelle le calcul et écrit le paiement (`RCR:760`). Pas encore là : « aucun endpoint ne calcule de paiement aujourd'hui » (`parametrage_service.py:31-32`).
* **À coder, API :** refuser la modification des termes figés (points 4 et 5). Aujourd'hui, `PUT /payments/{id}` et `PUT /sales/{id}` acceptent tout (`API/src/app/routes/crud_router.py:95-102`) ; `payment_service.py` et `sale_service.py` n'ont aucune règle.
* **À coder, tests :** le test d'intégration de Q-REM-11 n'existe pas encore.
* **Suppression d'un paiement :** relève d'ADR-027 (« `mandate`, `sale` et `payment` ne s'effacent pas », ADR-027, Décision).
* **Écart au modèle du sujet :** `prix_acte` et `honoraires` restent sur la vente, pas copiés sur le paiement (`RCR:286`). La règle tient : ils sont figés sur la vente (point 5). À dire en soutenance.
* **Deux scores à ne pas confondre :** `payment.performance_score` est celui du calcul ; `hunter_performance.score` est recalculé après le paiement (`01:923-925`). Voir ADR-035.
* **Bornes du score :** `NUMERIC(4,1)`, de 0 à 100, comme `hunter_performance.score` (`01:927`, `:1005`). Choisies à LOT5 (rapport LOT1→LOT5, carte D8, gardée).

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Qui garantit `montant = taux × honoraires` ? | L'API seule, avec un test d'intégration. Pas encore écrit. | Q-REM-11, `questions-a-trancher.md:658-666` |
| Un terme figé peut-il être corrigé après coup ? | Non. Seuls le statut et les dates d'étape changent. C5 n'en nomme que cinq ; la règle vaut pour tous. Déduit. | déduit de `F10:275`, `RCR:764` ; `09-contraintes-a-coder.md:169-182` |
| Ce refus : trigger ou service ? | Dans le service, comme C3 pour la vente. Déduit. | déduit de Q-REM-12 (« Appliquer C3 dans sale_service », `questions-a-trancher.md:670`) |
| Le prix, la date de l'acte, la grille et l'origine, rangés sur la vente, sont-ils figés aussi ? | Oui. C3 ne nomme que `fees_amount`. Mais le prix choisit la tranche, la date choisit le barème, la grille donne les honoraires, l'origine ouvre ou ferme le droit d'un non-exclusif : en changer un fausserait le paiement. Déduit. | déduit de `RCR:84`, `:286`, `:292`, `:500-508` ; C3, `09-contraintes-a-coder.md:110-117` ; ADR-030 |
| Le calcul se relance-t-il si un paramètre change ? | Non : « Le résultat est figé à l'acte. » | `RCR:764` |
| Pourquoi pas de clé du paiement vers `hunter_performance` ? | Elle pointerait vers la note d'après, et créerait un cycle entre les deux tables. | `questions-a-trancher.md:556` ; `_v4.md:98` |

**Questions ouvertes** 🟡

Aucune. La Décision 3 attend le oui du groupe (voir Décideurs). Le contenu du détail est une micro-décision, réglée dans les Conséquences.

**Sources**

| Affirmation | Source |
|---|---|
| « le point le plus important », « tous les termes du calcul », `bareme_id` | `documents utiles/REGLES-CALCUL-REMUNERATION.md:292` (StarterPack) |
| Modèle `paiements` du sujet | même fichier, l. 284-289 |
| Score calculé avant le taux, tout à la date de l'acte | même fichier, l. 84 |
| Le type `Vente`, entrées du calcul ; l'origine ouvre ou ferme le droit | même fichier, l. 460-471, l. 500-508 |
| La persistance est une couche au-dessus ; jamais rejoué ; `Vente`, liste minimale des entrées | même fichier, l. 760, l. 764, l. 766 |
| « les deux points qui prouvent que la règle a été comprise » | même fichier, l. 770 |
| Règle `@tracabilite` : figés, jamais recalculés ; éléments conservés | `user-stories/10_calcul_remuneration_chasseur.feature:274-275`, `:287` (StarterPack) |
| Note v4 : pas de compteurs bruts ; pas de clé vers la note | `md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:72`, `:98` |
| Q-REM-03, Q-REM-04 : réponses et options | `md/questions/questions-a-trancher.md:540-573` |
| Q-REM-03 au registre : « non exigé ailleurs », carte D8 gardée | même fichier, l. 123 |
| Q-REM-11 : l'API seule | même fichier, l. 658-666 |
| Q-REM-12 : C3 dans le service | même fichier, l. 668-676 |
| Q-JEF-20 : confirmé par Jeff | `md/questions/2026-10-07-questions-pour-jeff.html:1910-1919` ; `questions-a-trancher.md:262` |
| G1 : options et décision | `md/journal/2026-10-08-tables-parametres-et-schema.html:511-526` ; `docker/init-v3/README.md:117-123` ; commit `7fc63ed` |
| Colonnes figées de `payment`, `chk_refused` | `docker/init-v3/01_create_fil_rouge_immobilier.sql:873-983` |
| Termes rangés sur `sale` ; `sale_origin` | même fichier, l. 753-770 |
| Dates et exclusivité du mandat | même fichier, l. 452, l. 457-458 |
| Score figé ≠ note du journal | même fichier, l. 923-925 |
| Migrations | `docker/migrations/v2-vers-v3/05_paiement.sql:66-72` ; `15_paiement-reglages-taux.sql` |
| Entrées et notes du calcul | `API/src/app/services/remuneration.py:137-140`, `:204-216`, `:267-293` |
| Calcul pas branché | `API/src/app/services/parametrage_service.py:27-32` |
| `PUT` ouvert sur toutes les tables | `API/src/app/routes/crud_router.py:95-102` |
| Tests ; fixture `payment_payload` | `API/tests/integration/test_constraints_db.py:507-531`, `:565-589`, `:603-624` |
| Carte D8 : « pas obligatoire ailleurs », « Pris par Claude, seul », « Défaire » ; questions laissées au groupe | `md/journal/2026-10-07-rapport-lot1-a-lot5.html:540-552`, `:624`, `:627` |
| Les 9 cartes du rapport LOT1→LOT5 gardées par Sébastien | `context AI/08-etat.md:240-243` |
| C3 et C5 | `livrables/2-modelisation/09-contraintes-a-coder.md:110-117`, `:169-182` |
| ADR-002 (anglais pour les schémas de données), ADR-019 (« déjà actée »), ADR-027 (pas d'effacement) | journal Confluence, copie du 07/10/2026 : ADR-002, Décision ; ADR-019, Conséquences ; ADR-027, Décision |
| Modèle d'ADR ; pas d'ADR pour les micro-décisions ; « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:13`, `:19-40`, `:72` (StarterPack) |

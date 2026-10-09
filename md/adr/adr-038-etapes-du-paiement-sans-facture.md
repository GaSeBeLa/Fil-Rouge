# ADR-038 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 038 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md`,
> § 3, groupe 2, l. 61). Il porte la lettre J du pense-bête
> (`md/questions/questions-a-trancher.md:405`).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Aucune question ne reste ouverte.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * **Qui crée le paiement et le fait avancer** : pas tranché ici
>   (`md/securite/matrice-droits-crud-par-role.md:228`, question 4). Repris
>   par la matrice d'ADR-027.
>
> * `livrables/2-modelisation/09-rapport-ecarts-contraintes.md` range encore la
>   facture dans `payment.status` (l. 471-472) et dit U38, U39 et F08
>   « couverte » (l. 548-552). Ce n'est plus vrai. À aligner ou à dater.
> * `md/securite/matrice-droits-crud-par-role.md`, § 5.4 : le chasseur
>   « envoyer sa facture » (l. 196, l. 205) et « Les 6 états d'un paiement »
>   (l. 209-214). À porter dans ADR-027.
> * L'ancienne page compagnon d'ADR-024 sur Confluence montre encore les six
>   statuts. Elle est remplacée par le nouvel ADR-024, qui écarte la facture de
>   son périmètre sans nommer cette fiche
>   (`md/adr/adr-024-motif-refus-remuneration.md:138`).
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-038 : Le paiement du chasseur a trois étapes datées et aucune facture ; écart assumé au parcours du sujet (Readme, point 11 ; user stories 07)

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions : 05/10, 06/10 et 07/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * le client, Jeff (aussi PO, Q-PRO-01) : « facture hors périmètre », entretien du 07/10/2026 (Q-JEF-23, réponse notée par l'équipe) ;
  * le groupe : Q3 du plan d'action, « aucune trace de facture en base » (07/10/2026) ; Q-REM-17, une colonne de date par étape (05/10/2026) ;
  * Sébastien : le retrait des statuts de facture (carte D6) et les deux dates (carte D7), à LOT5, gardés le 07/10/2026.
* **Remplace :** rien.
* **Complète :** ADR-024 (le statut `'refused'` et son motif).

**Contexte**

Le sujet décrit cinq étapes après la vente (`Readme.md:132-134` ; `user-stories/07_chasseur_remuneration_et_performance.feature:10-34`) :

1. l'entreprise reçoit les honoraires ; le chasseur est prévenu du paiement proche, « Et je peux préparer ma facture » (F07, l. 10-15) ;
2. le chasseur envoie sa facture ; elle est « soumise à vérification » (l. 17-21) ;
3. la facture est « vérifiée et conforme » ; le paiement est « programmé » (l. 23-27) ;
4. le paiement est fait ; la somme est « marquée comme payée » (l. 29-34) ;
5. les indicateurs de performance sont recalculés (l. 34).

Le modèle de tables du sujet garde un `facture_id` dans `paiements` (`REGLES-CALCUL-REMUNERATION.md:288`).

La base v2 suivait ces étapes avec six statuts, dont `'invoice_submitted'` et `'verified'` (`docker/init-v2/01_create_fil_rouge_immobilier.sql:730-733`). Elle n'avait que deux dates : `created_at` et `paid_at` (carte Q-REM-17, `questions-a-trancher.md:713`).

La facture a changé trois fois de place :

* **05/10/2026**, Q-REM-17 : des dates sur `payment`, plus `invoice_reference` (`questions-a-trancher.md:138`) ;
* **06/10/2026**, Q-ACC-11 : une table des factures du chasseur, « ex. hunter_invoice », « à confirmer avec Jeff » (l. 185) ;
* **07/10/2026**, Jeff : « facture hors périmètre » (`md/questions/2026-10-07-questions-pour-jeff.html:1876`).

Cet ADR ne parle que de la facture du chasseur. Celle que reçoit le particulier est un autre sujet (`03_particulier_offre_et_signature.feature:37-42`).

**Options envisagées**

Trois questions, tranchées les 05/10 et 07/10/2026.

A. Que garder de la facture du chasseur ? (Q3 du plan d'action, 07/10/2026)

1. **Une table des factures**, la réponse du 06/10 (Q-ACC-11). Avantage : la trace de chaque envoi. Inconvénients : contredit Jeff ; une table de plus. **Écartée.**
2. **Le minimum sur le paiement** : sa référence, sa date d'envoi, sa date de vérification. Avantage : les deux scénarios du sujet restent couverts. Inconvénient : une facture renvoyée écrase la précédente. C'était l'option recommandée par Claude. **Écartée.**
3. **Aucune trace de facture en base.** Avantage : moins de colonnes et de code. Inconvénient : « Deux scénarios du sujet non couverts ». **Retenue.**

B. Que deviennent les statuts de facture ? (carte D6, LOT5)

1. **Tout garder.** Contredit Jeff. **Écartée.**
2. **Garder `'verified'`** au sens « paiement vérifié par l'agence ». Un sens que personne n'a demandé. **Écartée.**
3. **Retirer `'invoice_submitted'` et `'verified'`.** **Retenue.**

C. Comment dater les étapes ? (Q-REM-17, 05/10/2026 ; carte D7, LOT5)

1. **Une table d'historique des statuts.** Plus propre, mais plus lourde pour un besoin de démo. **Écartée.**
2. **Rien** (option C de la carte Q-REM-17). **Écartée** le 05/10/2026.
3. **Une colonne de date par étape, sur `payment`.** **Retenue.** Sans facture, il en reste deux nouvelles : `announced_at` et `scheduled_for`.

**Décision**

1. La facture du chasseur est hors du périmètre. Aucune table, aucune colonne, aucun statut ne la représente.
2. Un paiement a quatre statuts : `CHECK (status IN ('refused', 'announced', 'scheduled', 'paid'))`.
3. Il devra aller de `'announced'` à `'scheduled'`, puis `'paid'`. `'refused'` est le droit fermé d'ADR-024. L'ordre des statuts n'est tenu nulle part aujourd'hui (Conséquences).
4. Une date par étape :
   * `announced_at TIMESTAMP` : le chasseur est prévenu ;
   * `scheduled_for DATE` : le jour prévu du virement ;
   * `paid_at TIMESTAMP` : le virement est fait.
5. Une date se remplit quand son étape est atteinte, et reste ensuite (`chk_announced`, `chk_scheduled`, `chk_paid`).
6. Un refus n'est ni annoncé, ni programmé, ni payé : ses trois dates restent vides.
7. Le passage à `'scheduled'` ne dépend plus d'une facture vérifiée.

**Écart assumé au sujet**

Cette décision s'écarte du sujet. Il faut le dire au jury.

| Ce que dit le sujet | Ce que fait le projet |
|---|---|
| « Et je peux préparer ma facture » (`F07:15`) | rien en base |
| « j'envoie ma facture dans le système » (`F07:17-21` ; `Readme.md:133`) | non couvert |
| paiement programmé une fois la facture « vérifiée et conforme » (`F07:23-27` ; `Readme.md:133`) | programmé sans facture |
| `facture_id` dans `paiements` (`REGLES-CALCUL-REMUNERATION.md:288`) | aucune colonne |
| montant payé « après vérification de sa facture » (`10_calcul_remuneration_chasseur.feature:281`) | le montant figé reste vrai ; la vérification n'existe pas |
| parcours futur : le système vérifie la facture seul (`09_futur_chasseur_assistance_ia.feature:60-65` ; `Readme.md:199`) | sans objet |

Ce qui reste couvert : le chasseur prévenu (l. 10-15), le paiement programmé (l. 27), le paiement fait (l. 29-33).

**Justification**

* Le client a tranché. Jeff, client et PO, a dit « facture hors périmètre » le 07/10/2026 (Q-JEF-23 ; Q-PRO-01, `questions-a-trancher.md:197`).
* Le sujet range la facture hors du calcul : « La TVA et la facturation du chasseur relèvent du cycle de paiement, pas du calcul de la part » (`REGLES-CALCUL-REMUNERATION.md:131`). Le calcul ne change donc pas.
* La règle qui compte reste tenue : le montant annoncé est le montant figé au calcul (`10_calcul_remuneration_chasseur.feature:275-280`).
* Garder un statut `'verified'` sans facture lui donnerait un sens que personne n'a demandé (carte D6).
* Une colonne par étape suffit pour une démo ; une table d'historique serait plus lourde (carte Q-REM-17, `questions-a-trancher.md:721`).

**Conséquences**

* **Schéma :** fait à LOT5. Statuts (`docker/init-v3/01_create_fil_rouge_immobilier.sql:881-886`), dates (`01:887-892`), contraintes (`01:944-956`). Une base v2 y arrive par `docker/migrations/v2-vers-v3/05_paiement.sql` (l. 8-9, l. 38-58). Compté avant d'activer : 0 paiement en base de dev (`docker/init-v3/README.md:48`).
* **API :** `payment_model.py:42-50` suit le schéma. Aucun fichier `.sql` ou `.py` de `docker/init-v3/`, `API/src/` ou `API/tests/` ne contient « invoice » (grep, 08/10/2026).
* **Tests :** `'announced'` sans date, `'scheduled'` sans date : 409 ; un paiement payé garde ses dates (`API/tests/integration/test_constraints_db.py:591-624`). Tests non relancés pour cet ADR.
* **L'ordre des statuts n'est tenu nulle part.** Le `CHECK` ne liste que les valeurs permises. `PUT /payments/{id}` est ouvert (`API/src/app/routes/crud_router.py:95-102`). Faire respecter l'ordre compare à l'ancienne valeur : à coder dans l'API, comme les autres règles de ce genre (ADR-040).
* **Ordre des dates — ✅ confirmé par le groupe le 09/10/2026 (S9), demande du code, non fait.** Le rapport du lot 5 l'a laissé ouvert : « L'ordre des dates (annonce avant virement) n'est pas vérifié » (carte D7, `md/journal/2026-10-07-rapport-lot1-a-lot5.html:528` ; question, l. 626). Réponse déduite : **un `CHECK` sur `payment`**.
  * La règle ne lit qu'une ligne : c'est le cas d'un `CHECK`, pas de l'API (`livrables/2-modelisation/09-contraintes-a-coder.md:13-19`).
  * Pour la même sorte de règle, « une fin après le début » sur la grille d'honoraires, le groupe a répondu « Ajouter le CHECK » (Q-SCH-16, `questions-a-trancher.md:171`). Le schéma le fait déjà pour le barème (`chk_scale_period`, `01:805-806`).
  * ✅ Forme retenue par le groupe le 09/10/2026 (S9) : `announced_at::date <= scheduled_for` et `announced_at <= paid_at`. `paid_at` reste libre face à `scheduled_for` : un virement peut partir avant ou après le jour prévu.
  * À faire : le `CHECK`, une migration v2 → v3, un test refusé et un accepté.
* **Q-ACC-04** (« Qui fait avancer la facture dans ses états ? ») devient sans objet (`questions-a-trancher.md:243`).
* **La date où l'entreprise reçoit les honoraires** (`F07:12`) n'est pas stockée. `sale` n'a que `signature_date` (`01:756`). Déduit : elle relève de l'acte notarié, hors périmètre (`questions-a-trancher.md:62`, `:722`). ✅ **Confirmé le 09/10/2026** (Améthyste, accord de Sébastien, Discord) : l'encaissement des honoraires par l'agence est **hors périmètre, géré par la comptabilité**. Le chasseur n'a pas besoin de cette date : il est prévenu par `payment.announced_at` (`Readme.md:132`, point 10).
* **Notifications :** `announced_at` pourrait servir de trace « chasseur prévenu ». C'est la question Q-JEF-29, posée à Jeff le 08/10/2026, sans réponse (`md/questions/questions-pour-jeff-notifications.html:393-399`). Hors de cet ADR.
* **Si Jeff remet la facture dans le périmètre**, cet ADR sera remplacé. La table des factures (Q-ACC-11) en serait le point de départ.
* **Journal :** aucun ADR existant n'est remplacé. ADR-024 écarte la facture de son périmètre (ADR-024, Conséquences).

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Faut-il garder une trace de la facture, même minimale ? | Non : aucune trace. Choix du groupe après la réponse de Jeff. | `2026-10-07-questions-pour-jeff.html:1876` ; `md/journal/2026-10-07-plan-action.html:374-376` ; `questions-a-trancher.md:256` |
| Que deviennent `'invoice_submitted'` et `'verified'` ? | Retirés. Le registre ne les tranchait pas : Sébastien a choisi à LOT5. | `md/journal/2026-10-07-rapport-lot1-a-lot5.html:507-521` ; `context AI/08-etat.md:236-243` |
| Quelles dates garder ? | `announced_at` et `scheduled_for`, en plus de `paid_at`. Leurs types : choisis par Claude, gardés par Sébastien. | `rapport-lot1-a-lot5.html:523-537` ; `questions-a-trancher.md:138` |
| Un refus porte-t-il une date d'étape ? | Non : ni annonce, ni programmation, ni paiement. | `01:944-956` ; ADR-024 |
| Le calcul de la rémunération change-t-il ? | Non : la facturation « relève du cycle de paiement, pas du calcul ». | `REGLES-CALCUL-REMUNERATION.md:131` |

**Questions ouvertes** 🟡

Aucune. L'ordre des dates est une micro-décision (`JOURNAL-DE-DECISIONS.md:13`), réglée par déduction dans les Conséquences.

**Sources**

| Affirmation | Source |
|---|---|
| Les étapes du parcours, facture comprise | `Readme.md:132-134` (StarterPack) |
| Les quatre scénarios du chasseur | `user-stories/07_chasseur_remuneration_et_performance.feature:8-34` (StarterPack) |
| `facture_id` dans `paiements` | `documents utiles/REGLES-CALCUL-REMUNERATION.md:284-289` |
| Facturation hors du calcul de la part | même fichier, l. 131 |
| Montant annoncé = montant figé ; « après vérification de sa facture » | `user-stories/10_calcul_remuneration_chasseur.feature:275-281` |
| Parcours futur : vérification autonome | `user-stories/09_futur_chasseur_assistance_ia.feature:60-65` ; `Readme.md:199` |
| Facture du particulier, autre sujet | `user-stories/03_particulier_offre_et_signature.feature:37-42` |
| Six statuts en v2 | `docker/init-v2/01_create_fil_rouge_immobilier.sql:730-733` |
| Q-REM-17 : options, réponse, revue à LOT5 | `md/questions/questions-a-trancher.md:138`, `:710-722` |
| Q-ACC-11 : une table des factures, 06/10 | même fichier, l. 185 |
| Facture hors périmètre ; Q3 « aucune trace » | même fichier, l. 88, l. 256 ; `md/questions/2026-10-07-questions-pour-jeff.html:1866-1876` |
| Les trois options de Q3 | `md/journal/2026-10-07-plan-action.html:366-379` |
| Cartes D6 et D7 | `md/journal/2026-10-07-rapport-lot1-a-lot5.html:507-537` |
| Ordre des dates : question posée, « n'est pas vérifié » | même fichier, l. 528, l. 626 ; `md/journal/2026-10-07-rapport-final-chantier-lot.html:681` |
| Un `CHECK` ne voit qu'une ligne | `livrables/2-modelisation/09-contraintes-a-coder.md:13-19` |
| Q-SCH-16 : « Ajouter le CHECK » ; `chk_scale_period` | `questions-a-trancher.md:171` ; `docker/init-v3/01_create_fil_rouge_immobilier.sql:805-806` |
| `PUT` ouvert | `API/src/app/routes/crud_router.py:95-102` |
| Décisions de LOT5 gardées par Sébastien | `context AI/08-etat.md:236-243` |
| Jeff est le PO | `questions-a-trancher.md:197` |
| Q-ACC-04 sans objet | même fichier, l. 243, l. 1033 |
| Acte notarié hors périmètre | même fichier, l. 62 |
| Statuts, dates et contraintes du paiement, v3 | `docker/init-v3/01_create_fil_rouge_immobilier.sql:873-956` |
| Migration v2 vers v3 | `docker/migrations/v2-vers-v3/05_paiement.sql:8-9`, `:38-58` ; `docker/init-v3/README.md:41-48` |
| Modèle de l'API | `API/src/app/models/payment_model.py:42-50` |
| Tests | `API/tests/integration/test_constraints_db.py:591-624` |
| Q-JEF-29, sans réponse | `md/questions/questions-pour-jeff-notifications.html:393-399` |
| ADR-024 écarte la facture de son périmètre | ADR-024, Conséquences |
| Modèle d'ADR ; pas d'ADR pour les micro-décisions | `documents utiles/JOURNAL-DE-DECISIONS.md:13`, `:19-40` (StarterPack) |

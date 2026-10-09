# ADR-032 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 032 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md`,
> § 3, groupe 1, lettre A du pense-bête).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Aucune question ne reste ouverte : la seule du premier jet est
> tranchée par déduction (voir « Questions tranchées »).
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) — documents à aligner :
>
> * `livrables/2-modelisation/09-contraintes-a-coder.md:134` écrit encore
>   `amount_min <= purchase_amount < amount_max` (borne exclue) ;
> * `docker/init-v3/02_migration.sql:15-16` et `docker/init-v3/README.md:257-262`
>   parlent encore de `320000.00` ; les `INSERT` de `criteria` dans `02`
>   (l. 208-224 et 228) aussi. Sans effet : PostgreSQL convertit `320000.00` en
>   entier sans perte.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-032 : Tous les montants en euros — prix, budgets et barème en entiers, bornes du barème incluses ; honoraires et paiement au centime

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (l'euro : 21/09/2026 ; les entiers et les bornes incluses : 05/10/2026)
* **Statut :** proposé
* **Décideurs :** l'équipe projet (carte Q-REM-01, « Groupe », tranchée le 05/10/2026) ; le client (Jeff) informé le 07/10/2026, sans objection (Q-JEF-19)
* **Remplace :** ADR-012 (« Définition des budgets min, max et renovation (Table Client) », accepté, 19/08/2026). Les budgets du client passent sur `criteria`, en entiers.

**Contexte**

ADR-012 range trois budgets sur la table `Client` : `min_budget`, `max_budget`, `renovation_budget`, « de type Numeric ». Le schéma v3 ne suit plus cet ADR :

* les budgets sont sur `criteria`, pas sur `client` ;
* ils sont quatre : `budget_min`, `budget_max`, `renovation_budget_min`, `renovation_budget_max` ;
* ils sont en `INTEGER` (`docker/init-v3/01_create_fil_rouge_immobilier.sql:353-354`, `:361-362`).

L'unité monétaire n'a jamais eu d'ADR (`md/adr/2026-10-07-liste-adr-chantier-4.md:49`). Elle a pourtant changé :

* le 11/09/2026, le groupe retient les milliers d'euros (K€) : « ce n'est pas un logiciel de paye, doit rester indicatif » (`livrables/2-modelisation/09-decisions-a-prendre.md:306`) ;
* le 21/09/2026, « `X02` tranché : l'unité monétaire est l'euro », en `NUMERIC(12,2)`, sur trois mesures (`context AI/08-etat.md:108-114`).

Reste la borne haute d'une tranche du barème (Q-REM-01). Le sujet se contredit :

* le tableau écrit « < 200 000 € » : borne exclue (`REGLES-CALCUL-REMUNERATION.md:173`) ;
* la requête écrit `BETWEEN montant_min AND COALESCE(montant_max, 999999999)` : borne incluse (même fichier, l. 188).

Avec des prix au centime, 199 999,50 € tombe dans aucune tranche, ou dans deux, selon la lecture.

**Options envisagées**

A. L'unité

1. **Milliers d'euros, `NUMERIC(6,1)`** (choix du 11/09). **Écartée** le 21/09, sur trois mesures (`docker/init-v3/README.md` § 1) :
   * 37 valeurs sur 47 des fixtures officielles dépassent 99 999,9 ;
   * 199 999 € devient 200,0 K€ et bascule à 35 % au lieu de 30 % ;
   * l'arrondi au centime exigé par le sujet est impossible au dixième de K€ (100 €).
2. **Euros.** **Retenue.**

B. Le type des prix et des bornes du barème (Q-REM-01)

1. **`NUMERIC(12,2)`, bornes exclues `'[)'`**, stocker 200 000 et convertir à la lecture (`montant_max − 0,01`). Avantage : zéro ligne changée dans le code du sujet. Inconvénient : une conversion à écrire entre la base et le code. **Écartée.** C'était l'option recommandée par Claude dans le registre.
2. **Changer le code du sujet** (`<` au lieu de `<=`). **Écartée** : un test casse, il attend 30 % à 199 999 € (`API/tests/test_remuneration.py:193`).
3. **`NUMERIC(12,2)`, bornes incluses `'[]'`, stocker 199 999,99.** Inconvénient (déduit) : les bornes stockées ne sont plus celles du sujet (`199999`, `10_calcul_remuneration_chasseur.feature:23`). **Écartée.**
4. **Euros entiers (`INTEGER`), bornes incluses `'[]'`.** **Retenue.**

**Décision**

1. Tout montant est en **euros**. Jamais en K€.
2. **`INTEGER`, euros entiers**, pour les prix, les budgets, les bornes du barème et la part fixe. Huit colonnes (les deux budgets travaux ont été retirés, S7) :
   * `estate.price`, `estate_proposed.amount_proposition`, `sale.purchase_amount` ;
   * `criteria.budget_min`, `budget_max` ;
   * `commission_scale.amount_min`, `amount_max` ; `parameters_fees.fixed_amount`.
3. **`NUMERIC(12,2)`, au centime**, pour les honoraires `sale.fees_amount` et la rémunération `payment.amount`.
4. Une tranche du barème **inclut ses deux bornes** : `numrange(amount_min, amount_max, '[]')` dans les deux `EXCLUDE` de `commission_scale`. Un prix égal à la borne basse d'une tranche tombe dans cette tranche : 200 000 € donne 35 %. Un prix égal à la borne haute reste dans la sienne : 199 999 € donne 30 %.
5. Dans l'API : `int` pour les entiers, `Decimal` pour les montants au centime, **jamais `float`**. Un prix à virgule est refusé (422) avant d'atteindre la base.
6. Les budgets vivent sur **`criteria`**, la demande versionnée. `budget_min` est facultatif.
7. Les taux ne sont pas des montants : ils restent en `NUMERIC(5,4)`, hors de cet ADR.

**Justification**

* **Les sources officielles comptent en euros.** Le barème a des bornes à l'euro près (`10_calcul_remuneration_chasseur.feature:22-27`). Le calcul arrondit au centime (même fichier, l. 253 ; `REGLES-CALCUL-REMUNERATION.md:229`). La base d'origine aussi : `budget_max NUMERIC(12,2)`, « clients uniquement (EUR) » (`fixtures/PgSQL.sql:71`, `:76`).
* **Les prix réels n'ont pas de centimes** : 0 sur 2 556 (`docker/init-v3/README.md:415`). Le plus grand vaut 406 042 € ; `INTEGER` va jusqu'à 2 147 483 647 (`md/questions/questions-a-trancher.md:121`).
* **Avec des euros entiers, le sujet ne se contredit plus** (déduit). « < 200 000 € », « jusqu'à 199 999 » et `BETWEEN 0 AND 199999` disent la même chose. La notation « [350 000 ; 500 000[ » de l'exemple (`REGLES-CALCUL-REMUNERATION.md:249`) tombe juste aussi. Ni trou, ni chevauchement.
* **Le code du sujet reste intact** : `prix <= l.montant_max` (`API/src/app/services/remuneration.py:241`), bornes `199999` (`:304`).
* **Honoraires et rémunération gardent leurs centimes** : « 3 000 € + 2,5 % du prix » tombe souvent sur des centimes (`API/src/app/models/sale_model.py:10-13`). Arrondi au demi supérieur (`REGLES-CALCUL-REMUNERATION.md:229` ; `remuneration.py:44-46`).
* **Pas de `float`** : le sujet le dit, « `Decimal`, jamais `float` » (`REGLES-CALCUL-REMUNERATION.md:339`).
* **Les budgets suivent la demande.** Le sujet range le budget dans la demande, qui « évolue dans le temps » et dont on garde « l'historique versionné » (`documents utiles/GLOSSAIRE-METIER.md:17`). Sur `client`, un budget s'écraserait à chaque changement (déduit).

**Conséquences**

* **Fait le 05/10/2026** : schéma (commits `abbc84e`, `c896e39`), modèles en `int` (`d3c128c`), 422 sur un prix à virgule (`fea3c9f`) (`questions-a-trancher.md:121`). Convention écrite en tête du schéma (`01_create_fil_rouge_immobilier.sql:66-75`) et dans l'API (`API/src/app/models/__init__.py:25-28`).
* **Tests** : un prix à virgule rend 422 et rien n'est écrit (`API/tests/integration/test_constraints_db.py:86-93`). Sans ce contrôle, PostgreSQL arrondissait 199 999,5 en silence à 200 000 (même fichier, l. 86-88). 199 999 € donne 30 %, 200 000 € donne 35 % (`test_remuneration.py:191-196`).
* **Pas de script de migration** pour ce changement : il a demandé de recréer la base (`docker compose down -v`, `questions-a-trancher.md:388`).
* **Écart à un exemple du sujet** : ses schémas d'exemple mettent `decimal budget_max` sur le client (`documents utiles/MCD-MERISE.md:44-57`, `OLTP.md:31-36`). Ce sont des exemples ; le glossaire place le budget dans la demande. À dire en soutenance.
* **Ce qui reste d'ADR-012** : la fourchette de budget d'achat, sur `criteria`. ✅ **Confirmé le 09/10/2026 (Sébastien ; deux états proposés par Améthyste)** : la règle de rapprochement est abandonnée et les budgets travaux `renovation_budget_min` et `renovation_budget_max` sont **retirés** du schéma (migration 21), car aucune règle ne les lit et le sujet n'en parle pas. `needs_renovation` reste sur `estate` et `criteria`, en **deux états** : `BOOLEAN NOT NULL DEFAULT FALSE` (`FALSE` : pas de bien à rénover ; `TRUE` : le client accepte un bien avec travaux). Tout le reste sur la rénovation est hors MVP.
* **Journal** : ADR-012 n'est pas effacé. Il passe à « remplacé par ADR-032 » (`documents utiles/JOURNAL-DE-DECISIONS.md:72`).

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| L'euro du 21/09 a-t-il été repris par le groupe ? | Oui, de fait : la réponse du groupe à Q-REM-01 parle d'« euros entiers ». La carte montrée à Jeff dit : « Notre choix : des prix en euros entiers, bornes incluses. » Sa réponse : « informé ; pas d'objection ». | `questions-a-trancher.md:121`, `:261` ; `md/questions/2026-10-07-questions-pour-jeff.html`, carte Q-JEF-19 (l. 1891-1900) |
| Le « numeric(12) » répondu le 02/10 ? | Une erreur de formulation, corrigée le 05/10 : `INTEGER`. | `questions-a-trancher.md:121` |
| Où vivent les budgets ? | Sur `criteria`, la demande versionnée. Déduit du glossaire du sujet. | `GLOSSAIRE-METIER.md:17` ; `01:353-362` |
| La part fixe des honoraires : entière ou au centime ? | Entière : le sujet donne « 3000,00 », soit 3 000. | `10_calcul_remuneration_chasseur.feature:19-20` ; `01:745-746` |
| Un prix saisi avec des centimes : arrondi ou refusé ? | Refusé, 422 (Q-INF-06). | `test_constraints_db.py:86-93` |
| Quel arrondi pour les montants au centime ? | Au centime, au demi supérieur. | `REGLES-CALCUL-REMUNERATION.md:229` ; `remuneration.py:44-46` |
| La règle de rapprochement d'ADR-012 (« additionner le prix de vente et l'estimation des travaux du bien, puis comparer ce total à la somme du `max_budget` et du `renovation_budget` ») : on la garde ? | **Non, elle tombe avec ADR-012.** ✅ Confirmé par le groupe le 09/10/2026 (S7). Raison : elle ne peut pas se calculer, car `estate` n'a pas d'estimation des travaux, seulement `needs_renovation BOOLEAN`. Les deux fourchettes restent des critères de recherche. Si la sélection des biens se code un jour, son propre ADR fixera la règle. | journal Confluence, ADR-012, Conséquences ; `01:611` ; le sujet ne parle jamais de budget travaux (recherche « travaux », « rénovation », « budget » dans le StarterPack ; seul `08_futur_particulier_assistance_ia.feature:15` cite « budget », sans règle) ; aucun code de rapprochement dans `API/` |

**Questions ouvertes** 🟡

Aucune.

**Sources**

| Affirmation | Source |
|---|---|
| ADR-012 : trois budgets Numeric sur `Client` ; règle de rapprochement | journal Confluence, copie du 07/10/2026, ADR-012, Décision et Conséquences |
| `estate` n'a pas d'estimation des travaux, seulement `needs_renovation BOOLEAN` | `docker/init-v3/01_create_fil_rouge_immobilier.sql:611` |
| Aucun ADR ne porte l'euro ; ADR-012 dépassé | `md/adr/2026-10-07-liste-adr-chantier-4.md:45-49` |
| K€ retenus le 11/09/2026 | `livrables/2-modelisation/09-decisions-a-prendre.md:263-306` |
| L'euro le 21/09/2026, trois mesures | `context AI/08-etat.md:108-114` ; `docker/init-v3/README.md:157-194` ; commit `44f9054` |
| Q-REM-01 : `INTEGER`, `'[]'`, options A, B, C | `md/questions/questions-a-trancher.md:121`, `:491-515` |
| Le sujet se contredit sur la borne | `REGLES-CALCUL-REMUNERATION.md:173-174`, `:188`, `:249` (StarterPack) ; `questions-a-trancher.md:1395` |
| Barème officiel, arrondi au centime | `user-stories/10_calcul_remuneration_chasseur.feature:18-27`, `:253` (StarterPack) |
| Précision des arrondis ; `Decimal`, jamais `float` | `REGLES-CALCUL-REMUNERATION.md:227-229`, `:339` |
| Base d'origine en euros | `fixtures/PgSQL.sql:71`, `:76` (StarterPack) |
| Budget dans la demande versionnée | `documents utiles/GLOSSAIRE-METIER.md:17` (StarterPack) |
| Exemples du sujet : `decimal budget_max` sur le client | `documents utiles/MCD-MERISE.md:44-57` ; `OLTP.md:31-36` (StarterPack) |
| Types des 12 colonnes de montant | `docker/init-v3/01_create_fil_rouge_immobilier.sql:353-354`, `:361-362`, `:570`, `:690`, `:746`, `:758`, `:760`, `:793-794`, `:878` |
| Bornes incluses dans les `EXCLUDE` | même fichier, l. 808-820 ; commentaires l. 1049-1052 |
| 0 prix avec centimes sur 2 556 | `docker/init-v3/README.md:415` |
| Jeff informé, pas d'objection | `md/questions/2026-10-07-questions-pour-jeff.html`, carte Q-JEF-19 ; `questions-a-trancher.md:261` |
| Code du sujet : `<=`, bornes `199999`, arrondi | `API/src/app/services/remuneration.py:44-46`, `:241`, `:304` |
| Modèles en `int` et `Decimal` | `API/src/app/models/__init__.py:25-28` ; `sale_model.py:10-13` |
| Tests | `API/tests/integration/test_constraints_db.py:86-93` ; `API/tests/test_remuneration.py:191-196` |
| Modèle d'ADR, « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:19-40`, `:72` (StarterPack) |

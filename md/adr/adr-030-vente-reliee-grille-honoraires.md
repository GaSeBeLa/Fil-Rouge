# ADR-030 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 030 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md`,
> § 3, groupe 1). Il réunit les lettres I et Q du pense-bête : écrire I sans Q
> laisserait ADR-019 remplacé à moitié (même fichier, § 2, regroupement 1).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Aucune question ne reste ouverte.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * `livrables/2-modelisation/09-contraintes-a-coder.md`, contrainte C2
>   (l. 88-107), décrit encore `valid_until` et l'`EXCLUDE` : à aligner.
> * Les notes du jour (`md/adr/2026-10-08-notes-seance-adr.md:119`) disent que
>   « les 2 `EXCLUDE` de `commission_scale` » dépendent de `btree_gist`. Seul
>   `excl_scale_no_overlap` en dépend (voir Conséquences) : à corriger.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-030 : La vente pointe la grille d'honoraires qui a servi ; une grille vaut « à partir du », jusqu'à la suivante

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions du groupe : 05/10/2026)
* **Statut :** proposé
* **Décideurs :** l'équipe projet — réponses du groupe du 05/10/2026 aux cartes Q-REM-13 (« Ajouter une clé ») et Q-SCH-17 (« Par construction : une grille vaut jusqu'à la suivante »)
* **Remplace :** ADR-019 (« Absence de clé étrangère entre Sale et Parameters_Fees », accepté, 10/09/2026)

**Contexte**

Le sujet veut des honoraires datés : « `F` et `t` sont versionnés dans le temps, au même titre que le barème. On applique ceux en vigueur à la date de l'acte. » (`REGLES-CALCUL-REMUNERATION.md:129`).

ADR-019 avait tranché deux points :

* pas de clé de `sale` vers `parameters_fees` : la grille se retrouve par la date de l'acte ;
* une contrainte `excl_fees_no_overlap` (`EXCLUDE USING gist`) interdit que deux périodes `[valid_from, valid_until]` se chevauchent.

Son argument : la contrainte garantit « qu'une date donnée retrouve toujours exactement une ligne ». La clé était donc jugée redondante (notes d'équipe, `md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:143-147`).

Le 05/10/2026, trois cartes du registre ont rouvert le sujet :

* **Q-SCH-17** : l'`EXCLUDE` garantit « au plus une » grille à une date, pas « exactement une ». Une date de fin saisie à la main peut laisser un jour sans grille. Une vente ce jour-là fait échouer le calcul (`BaremeIntrouvable`).
* **Q-REM-13** : sans clé, la vente ne dit pas quelle grille a donné ses honoraires.
* **Q-SCH-16** : aucun `CHECK` n'empêchait une grille de finir avant de commencer.

**Options envisagées**

Deux questions, tranchées ensemble.

A. Relier la vente à sa grille (Q-REM-13)

1. **Pas de clé**, la grille se retrouve par la date (ADR-019). Avantage : rien à changer ; le montant est déjà figé dans `sale.fees_amount`. Inconvénient : « on ne sait plus quelle grille a servi ». **Écartée.** C'était l'option recommandée par Claude dans le registre ; le groupe ne l'a pas retenue.
2. **Une clé `sale.id_parameters_fees`.** Avantage : « traçabilité complète ». Inconvénient : une colonne et un lien de plus. **Retenue.**

B. Éviter les trous entre deux grilles (Q-SCH-17)

1. **Rien** : garder `valid_from`, `valid_until` et l'`EXCLUDE`. Inconvénient : un trou ne se voit qu'à une vente, par `BaremeIntrouvable`. **Écartée.**
2. **Un contrôle dans l'API**, à l'écriture d'une grille. Avantage : le trou est refusé dès la saisie. Inconvénient : du code et des tests pour une erreur que la construction rend impossible. **Écartée.**
3. **Par construction** : une grille n'a qu'une date de début, et vaut jusqu'à la suivante. Avantages : trou impossible sans code de contrôle ; le nom `effective_from` (« en vigueur à partir du ») dit la vérité ; code du sujet inchangé. Inconvénients : base à recréer ; reste le cas d'une vente avant la toute première grille. **Retenue.**

**Décision**

1. `parameters_fees` n'a plus de date de fin. `valid_from` devient `effective_from DATE NOT NULL`. `valid_until` disparaît.
2. `UNIQUE (effective_from)` (`uq_fees_effective_from`) remplace l'`EXCLUDE` `excl_fees_no_overlap` : deux grilles ne démarrent pas le même jour.
3. Une grille vaut jusqu'à la veille de la suivante. La grille d'une vente est la dernière dont `effective_from` <= la date de l'acte (`sale.signature_date`).
4. Chaque vente pointe sa grille : `sale.id_parameters_fees INTEGER NOT NULL REFERENCES parameters_fees(id) ON DELETE RESTRICT`.
5. Le montant reste figé dans `sale.fees_amount`. La clé dit d'où il vient ; elle ne le remplace pas.
6. Le code de calcul du sujet ne change pas. Le service qui lit la table lui rend la date de fin qu'il attend : la veille de la grille suivante.
7. Cet ADR ne touche pas `commission_scale` : elle garde `valid_from`, `valid_until` et ses deux `EXCLUDE` (voir les questions tranchées).

**Justification**

* Un trou entre deux grilles devient impossible : il n'y a plus de date de fin à saisir. Aucun code de contrôle à écrire pour une erreur qui ne peut plus arriver.
* La clé suit le sujet : « On stocke donc tous les termes du calcul, y compris `bareme_id` » (`REGLES-CALCUL-REMUNERATION.md:292`), pour rejouer un calcul des années plus tard. Le même raisonnement vaut pour la grille d'honoraires.
* Elle aligne la vente sur le paiement, qui pointe déjà sa tranche (`payment.id_commission_scale`) et ses réglages (`payment.id_hunter_rate_parameters`, décision G1 du groupe du 08/10/2026).
* L'argument central d'ADR-019 était trop fort : l'`EXCLUDE` garantissait « au plus une » grille, pas « exactement une » (carte Q-SCH-17 ; déjà noté dans `livrables/2-modelisation/09-contraintes-a-coder.md:100-103`).

**Conséquences**

* **Schéma :** fait à LOT6 (`docker/init-v3/01_create_fil_rouge_immobilier.sql:733-751` et `:765-770`). Une base v2 y arrive par `docker/migrations/v2-vers-v3/06_parametres.sql` (l. 87-99 et 145-166). La migration s'arrête si une date de fin disait autre chose que « la veille de la suivante » (l. 50-85), ou si une vente précède la première grille (l. 155-165).
* **API :** `ParametersFees.effective_from` (`API/src/app/models/parameters_fees_model.py:31-32`) ; `Sale.id_parameters_fees` (`sale_model.py:35-36`). `parametrage_service.py` recalcule la date de fin (l. 65-78).
* **Tests :** deux grilles le même jour, 409 ; la grille suivante acceptée ; une vente vers une grille inconnue, 409 (`API/tests/integration/test_constraints_db.py:665-692`). La veille de la suivante : `API/tests/integration/test_parametrage_service.py:68-79`.
* **Une grille ne s'arrête pas sans être remplacée.** Voulu : une vente a toujours des honoraires (`fees_amount NOT NULL CHECK (> 0)`, `01:760`), donc il faut toujours une grille en vigueur. Pour changer les honoraires, on insère la grille suivante.
* **Reste à coder dans l'API :** que la clé désigne bien la grille en vigueur à la date de l'acte. C'est un TODO du schéma (`01:767-768`).
* **Reste à coder dans l'API :** qu'une grille déjà citée par une vente ne se modifie pas. Aujourd'hui, `PUT /parameters-fees/{id}` l'accepte (`API/src/app/routes/crud_router.py:95-102`). La suppression, elle, est bloquée par `ON DELETE RESTRICT`.
* **Écart au modèle suggéré par le sujet**, qui garde une `date_fin NULL` (`REGLES-CALCUL-REMUNERATION.md:278`). La règle (l. 129) est tenue ; seule la forme change. À dire en soutenance.
* **`btree_gist`** (`01:149`) n'a jamais servi à `parameters_fees` : son `EXCLUDE` ne comparait qu'une plage de dates (`docker/init-v2/01_create_fil_rouge_immobilier.sql:685-686`). Il sert à `excl_scale_no_overlap`, qui compare un entier (`id_hunter WITH =`, `01:808-813`). `excl_scale_global` ne compare que des plages, qui ont leur index GiST sans extension (doc PostgreSQL 16, § 8.17.10 ; commentaire `01:51-52`).
* **Seed :** la première grille démarre le 2026-01-01 (`docker/init-v3/05_parametres.sql:19`, `:31-33`). Q-REM-15 veut le barème « dès 2025 » dans le seed de démonstration, pas encore écrit (`md/questions/questions-a-trancher.md:191`). D'ici là, une vente datée de 2025 n'a pas de grille.
* **Journal :** ADR-019 n'est pas effacé. Il passe à « remplacé par ADR-030 » (`documents utiles/JOURNAL-DE-DECISIONS.md:72`).

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| La clé est-elle obligatoire ? ADR-019 l'envisageait « nullable ». | Oui, `NOT NULL`. Déduit : une vente a toujours des honoraires (`fees_amount NOT NULL`), donc une grille qui les a donnés. Fait à LOT6 ; la migration refuse une vente sans grille. | déduit de `01:760` et `01:769` ; `06_parametres.sql:155-166` |
| Q-SCH-16 : un `CHECK` « fin après début » sur `parameters_fees` ? | Sans objet : il n'y a plus de date de fin. | `questions-a-trancher.md:171`, `:440` |
| Une vente avant la toute première grille ? | Couverte par le seed (Q-REM-15) ; la migration s'arrête si le cas existe. | `questions-a-trancher.md:172` ; `06_parametres.sql:155-165` |
| Qui vérifie que la clé désigne la grille en vigueur à la date de l'acte ? | L'API, avec un test d'intégration : la règle croise deux tables (Q-MAN-06, 05/10/2026). Pas encore codé. | `01:767-768` ; `questions-a-trancher.md:408` |
| Une grille déjà utilisée par une vente peut-elle être corrigée ? | Non : on insère une nouvelle version datée. ✅ Confirmé par le groupe le 09/10/2026 (S8). Déduit : les paramètres sont « versionnés dans le temps » (l. 129) et un calcul passé doit se rejouer (l. 292). Contrôle dans l'API (Q-MAN-06), pas encore codé. | déduit de `REGLES-CALCUL-REMUNERATION.md:129`, `:292` ; même règle écrite dans `05_parametres.sql:15-17` |
| `commission_scale` passe-t-elle aussi en « à partir du » ? | Non, pas par cet ADR. Q-SCH-17 ne vise que les honoraires. `UNIQUE (effective_from)` ne convient pas au barème : 5 tranches démarrent le même jour, et une tranche peut être propre à un chasseur. Les `EXCLUDE` y restent utiles contre deux tranches qui se chevauchent. Un trou du barème lève `BaremeIntrouvable` au calcul. | déduit de `questions-a-trancher.md:172`, `05_parametres.sql:37-45`, `01:787-821`, `REGLES-CALCUL-REMUNERATION.md:273` ; `API/src/app/services/remuneration.py:243-245` |

**Questions ouvertes** 🟡

Aucune. Ce qui reste est du code à écrire, listé dans les Conséquences.

**Sources**

| Affirmation | Source |
|---|---|
| Honoraires versionnés, appliqués à la date de l'acte | `documents utiles/REGLES-CALCUL-REMUNERATION.md:129` (StarterPack) |
| Modèle du sujet avec `date_fin NULL` | même fichier, l. 278 |
| « tous les termes du calcul, y compris `bareme_id` » | même fichier, l. 292 |
| Barème : clé fonctionnelle (chasseur, période, tranche) | même fichier, l. 273 |
| ADR-019 : pas de clé, `EXCLUDE`, « exactement une ligne » | journal Confluence, copie du 07/10/2026, ADR-019 |
| Origine : clé retirée car l'`EXCLUDE` la rendait redondante | `md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:143-147` |
| Q-REM-13 : « Ajouter une clé », pas l'option recommandée | `md/questions/questions-a-trancher.md:134`, `:678-684` ; `questions-a-trancher.html:735-756` |
| Q-SCH-17 : « par construction », le commentaire fait foi | `questions-a-trancher.md:102`, `:172` ; `questions-a-trancher.html:1391-1416` |
| Q-SCH-16 sans objet | `questions-a-trancher.md:171`, `:440` |
| « au plus une », pas « exactement une » | `questions-a-trancher.html:1391-1416` ; `livrables/2-modelisation/09-contraintes-a-coder.md:100-103` |
| `parameters_fees` v3 : `effective_from`, `uq_fees_effective_from` | `docker/init-v3/01_create_fil_rouge_immobilier.sql:733-751` |
| `sale.id_parameters_fees NOT NULL`, TODO de la date | même fichier, l. 765-770 |
| `excl_fees_no_overlap` en v2 (plage seule) | `docker/init-v2/01_create_fil_rouge_immobilier.sql:685-686` |
| `commission_scale` : périodes et deux `EXCLUDE` | `docker/init-v3/01_create_fil_rouge_immobilier.sql:787-821` |
| Extension `btree_gist` | même fichier, l. 149 et l. 51-52 |
| Plages en GiST sans extension ; `btree_gist` pour les types simples | [doc PostgreSQL 16, § 8.17.9-8.17.10](https://www.postgresql.org/docs/16/rangetypes.html), doc officielle, lue le 08/10/2026 |
| G1 : `payment.id_hunter_rate_parameters` | `01_create_fil_rouge_immobilier.sql:936-942` |
| Migration v2 vers v3 | `docker/migrations/v2-vers-v3/06_parametres.sql:50-99`, `:145-166` |
| Le service rend la veille de la suivante | `API/src/app/services/parametrage_service.py:65-78` |
| Tests | `API/tests/integration/test_constraints_db.py:665-692` ; `API/tests/integration/test_parametrage_service.py:68-79` |
| Une vente a toujours des honoraires | `docker/init-v3/01_create_fil_rouge_immobilier.sql:760` |
| `PUT` ouvert sur toutes les tables | `API/src/app/routes/crud_router.py:95-102` |
| Seed au 2026-01-01 ; Q-REM-15 « dès 2025 » | `docker/init-v3/05_parametres.sql:19-33` ; `questions-a-trancher.md:136`, `:191` |
| Règles sur plusieurs tables dans l'API | Q-MAN-06, `questions-a-trancher.md:408` |
| Modèle d'ADR, « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:19-40`, `:72` (StarterPack) |

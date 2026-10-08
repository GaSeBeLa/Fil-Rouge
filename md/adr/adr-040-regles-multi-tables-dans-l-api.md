# ADR-040 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 040 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:63`,
> groupe 2, lettre M du pense-bête).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Aucune question ne reste ouverte : les neuf questions du premier jet
> sont tranchées par les sources ou par déduction (voir « Questions tranchées »).
>
> ⚠️ **Cet ADR décrit surtout du travail à faire.** Au 08/10/2026, aucune
> règle qui croise plusieurs tables n'est codée dans l'API, et aucune n'est
> testée.
>
> 📑 **Le tableau des règles est sorti de la fiche** (arbitre, 08/10/2026) :
> `md/adr/adr-040-annexe-etat-des-regles.md`, **état au 08/10/2026**, complété
> des règles d'ADR-033 à ADR-042. Un ADR fige un raisonnement ; un état devient
> faux dès qu'une règle est codée.
>
> ➡️ **Place finale du tableau : `livrables/2-modelisation/09-contraintes-a-coder.md`**
> (« Ces règles se rangent dans `09-contraintes-a-coder.md` »,
> `md/questions/questions-a-trancher.md:871`). **Tâche pour l'équipe** : l'y
> reporter, puis retirer l'annexe.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) — documents à aligner :
>
> * `livrables/2-modelisation/09-contraintes-a-coder.md` (daté du 11/09/2026) :
>   * son titre (l. 1) et l. 21-24 disent encore « dans l'API … ou dans un trigger » : Q-MAN-06 a choisi l'API ;
>   * C2 (l. 97-99) lit `valid_from` et `valid_until` sur la grille d'honoraires : il n'y a plus qu'`effective_from` (`docker/init-v3/01_create_fil_rouge_immobilier.sql:743-744`, ADR-030) ;
>   * C6 (l. 220-221) ferme le `valid_until` de la note précédente : retiré par Q-SCH-06 (`md/questions/questions-a-trancher.md:161`) ;
>   * C1 (l. 80-81, « à préciser ») et C7 (l. 230, « dépend de D8 ») : réglés par ADR-050, la vente pointe vers le dernier mandat de la chaîne ;
> * `docker/init-v3/README.md:98` compte 3 TODO « contrôlé par l'API ». Le schéma en renvoie aujourd'hui 6 à l'API (`01:624-627`, `:721-725`, `:767-768`, `:774-784`, `:936-941`, `:985-993`) ;
> * `01:134-136` dit encore que ces règles « demandent des triggers ou l'API » et que « les TODO ci-dessous portent le SQL prêt à activer ». Les TODO disent maintenant « pas de trigger » ;
> * la carte Q-MAN-06 cite d'anciens numéros de ligne de `01` (`639-641`, `664-668`, `789-795`, `669-672`). Aujourd'hui : `721-725`, `774-780`, `985-993`, `781-784`. Elle annonce aussi « trois TODO » (l. 859) pour quatre puces ;
> * `API/src/app/utils/exceptions.py:21-23` : `ConflictError` ne parle que des contraintes de la base. À élargir avec la première règle codée ;
> * `API/src/app/main.py:14-17` dit le hachage du mot de passe « pas encore nécessaire » : `UserService` le fait (`API/src/app/services/user_service.py:19-26`).
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-040 : Les règles qui croisent plusieurs tables se codent dans l'API, chacune avec son test — pas en trigger, sauf l'exclusivité

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décision du groupe : 05/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * le groupe (carte Q-MAN-06, réponse « Toutes dans l'API, chacune testée », 05/10/2026) ;
  * pour l'exception du trigger : le groupe (Q-MAN-02, ADR-039).
* **Complète :** ADR-005. Il laissait le contrôle « un compte, un seul profil » « par trigger, ou … contrôle applicatif ». Cet ADR le range dans l'API (déduit, voir Questions tranchées).
* **Voir aussi :** ADR-039 (l'exclusivité, seule exception) ; ADR-024, ADR-030, ADR-031, ADR-050, puis ADR-033, ADR-034, ADR-035, ADR-038, ADR-041, ADR-042 (règles qu'ils renvoient à l'API) ; ADR-036 (validation de l'entrée, proposé) ; ADR-047 (biens saisis à la main, proposé)

**Contexte**

Un `CHECK` ne voit qu'une ligne d'une table. Il ne peut pas lire une autre table, compter des lignes, ni comparer avec l'ancienne valeur (`livrables/2-modelisation/09-contraintes-a-coder.md:15-19`). Le livrable compte 9 blocs à coder, qui regroupent 23 règles (même fichier, l. 30-34, l. 280).

Un jeu de tests adverses, écrit à partir des `.feature`, donnait sur le schéma « 2 réussites / 14 lacunes / 1 à trancher (17 tests) ». Avec les deux règles du mandat actives (six mois, exclusivité ; LOT4) : « 5 réussites / 11 lacunes / 1 à trancher ». Le jeu n'a pas été rejoué depuis. Conclusion du schéma : « un schéma seul ne protège PAS la plupart des règles métier » (`docker/init-v3/01_create_fil_rouge_immobilier.sql:127-136`).

La carte Q-MAN-06 relève trois TODO du schéma, qui ouvrent quatre trous (`md/questions/questions-a-trancher.md:859-864`) :

* une visite peut précéder la signature du mandat ;
* une vente peut tomber hors de la validité du mandat, ou sur un mandat non signé ;
* « on peut aujourd'hui payer un chasseur qui n'est PAS celui du mandat » ;
* un paiement peut viser un barème pas en vigueur à la date de l'acte, ou le barème d'un autre chasseur.

Les deux derniers sont dans le même TODO, celui du paiement. « Les deux dernières sont les plus graves : c'est de l'argent versé à tort » (l. 866).

L'API a trois couches. Le service est l'endroit « où irait une règle » (`API/src/app/main.py:14-17`). Aujourd'hui, 19 des 20 services de table n'ont que le CRUD hérité : 8 lignes chacun. `UserService` hache le mot de passe. `ParametrageService` n'est « pas encore branché sur une route » (`API/src/app/services/parametrage_service.py:31-32`).

Le calcul de rémunération du sujet est une fonction pure. « La persistance est une couche au-dessus » (`REGLES-CALCUL-REMUNERATION.md:760`).

**Options envisagées**

1. **Toutes dans l'API, chacune testée.** Avantage : « Un seul endroit, testable. » Inconvénient : « Saisie directe en base non contrôlée. » C'était l'option recommandée par Claude. **Retenue.**
2. **Des triggers SQL.** Avantage : « La base se protège seule. » Inconvénient : « Code SQL lourd, base à recréer. » **Écartée.**

(Options et avantages : carte Q-MAN-06, `md/questions/questions-a-trancher.html:1013-1014`.)

**Décision**

1. Une règle qui croise plusieurs tables se code **dans l'API**, dans le service de la table qu'on écrit (`services/<table>_service.py`), avant l'écriture. Pas de trigger, pas de `CHECK`.
2. **Chaque règle a son test d'intégration**, sur la base de test `fil_rouge_test`. Au minimum, un cas refusé et un cas accepté (déduit, voir Questions tranchées).
3. Une règle refusée rend **409**, avec son propre message. Le service lève `ConflictError` ; le routeur commun la traduit déjà (ADR-036). Déduit, voir Questions tranchées.
4. **Un droit fermé n'est pas une erreur.** Un paiement sans droit s'enregistre `'refused'`, avec son motif (ADR-024).
5. Même traitement pour une règle sur plusieurs lignes d'une même table, ou sur l'ancienne valeur (exemple : les honoraires ne changent plus). Déduit des choix du groupe, voir Questions tranchées.
6. **Une seule exception : l'exclusivité du mandat**, par le trigger `trg_mandate_exclusivity` (ADR-039). C'est le seul trigger du schéma.
7. **Ni les tables ni les diagrammes ne changent.** Les règles se rangent dans `09-contraintes-a-coder.md`.
8. **L'argent d'abord** : les honoraires, puis le droit au paiement, puis le calcul du paiement et son gel.

**Justification**

* **Un seul endroit, testable** (carte). Les règles du paiement appellent le code du sujet, en Python : `droit_a_remuneration`, `taux_de_tranche` (`API/src/app/services/remuneration.py:166-174`, `:230-248`).
* **Pas de formule en double.** Pour le montant, la carte Q-REM-11 le dit : « un trigger la dupliquerait » ; « Une seule source de vérité : `rem.py`, déjà testé sur 55 cas » (`questions-a-trancher.md:665-666`).
* **Le sujet range la persistance au-dessus du calcul** (`REGLES-CALCUL-REMUNERATION.md:760`). Il range aussi le contrôle des droits d'accès dans « la couche applicative » (l. 763).
* **L'emplacement existe déjà.** Un service peut surcharger `create()` « sans que les routers ni les repositories n'aient à changer » (`API/src/app/services/base_service.py:8-13`). `UserService` le fait pour le mot de passe.
* **L'inconvénient accepté pèse peu aujourd'hui** (compté dans les scripts, pas en base) :
  * aucun script de `docker/init-v3/` n'écrit de visite, de vente ni de paiement. `02` n'écrit que `role`, `user`, `real_estate_manager`, `hunter`, `client`, `search_request`, `criteria`, `mandate` (`02_migration.sql:86-255`) ;
  * deux règles portent sur ce que `02` écrit en direct, et ses données les respectent. Un compte, un profil (ADR-005) : 25 comptes, 18 clients (id 7 à 24), 6 chasseurs (id 1 à 6), 1 manager (id 25), aucun en double (`02_migration.sql:132-172`). Une demande `'launched'` a un mandat signé (ADR-041) : l'`UPDATE` ne lance qu'une demande qui a un mandat (l. 275-277), et les 18 mandats ont une date de signature (l. 238-255) ;
  * le rôle en lecture seule n'écrit rien : « ni INSERT, ni UPDATE, ni DELETE » (`04_role-lecture-seule.sql:21`), testé (`API/tests/integration/test_constraints_db.py:822-826`).
* **Pourquoi l'exclusivité fait exception :**
  * Q-MAN-02 a dit « corriger, activer » le trigger déjà écrit ; ADR-039 écarte l'option API (ADR-039, Options, bloc 2) ;
  * sur le fond, les mandats s'écrivent aussi en direct : `02_migration.sql` en insère 18 (l. 238-255). Un contrôle dans l'API ne les verrait pas ; le trigger s'applique à toute écriture, API ou script. ADR-021 le disait : « Un contrôle uniquement applicatif laisserait passer les insertions directes (fakers, migration) » (journal Confluence, ADR-021, Justification).

**Conséquences**

* **État au 08/10/2026 : une seule de ces règles est codée, l'exclusivité, par trigger (ADR-039).** Aucune règle n'est codée ni testée dans l'API : les 19 services de table hors `UserService` font 8 lignes, CRUD seul.
* **Liste et état des règles :** annexe `md/adr/adr-040-annexe-etat-des-regles.md`, en attendant leur place dans `09-contraintes-a-coder.md` (Décision 7).
* **Un test existant devra changer** (déduit). `payment_payload` crée un paiement `'announced'` sur une vente du 01/03/2030, rattachée au mandat 1 (`test_constraints_db.py:489-531`). Ce mandat a fini le 01/08/2025 (`02_migration.sql:238`). Avec le contrôle des délais codé (R04), le droit est fermé :
  * l'API devra refuser ce paiement `'announced'` en 409 (Décision 3) ;
  * seul un paiement `'refused'`, de motif `'mandate_expired'`, passera pour cette vente (Décision 4) ;
  * si l'API calcule elle-même le statut, le test changera de forme : qui crée le paiement reste une case 💡 de la matrice d'ADR-027.
* 💡 **Écritures simultanées : non mesuré.** Un contrôle fait par l'API, puis l'écriture, laisse une fenêtre entre les deux. Deux requêtes au même instant pourraient passer toutes les deux. À regarder avec la première règle codée.
* 💡 **Le futur générateur de données** (Q-INF-07) écrira peut-être en base sans passer par l'API. Il devra alors respecter ces règles lui-même. ADR-021 l'avait vu (journal Confluence, ADR-021, Justification).
* **Journal** : aucun ADR n'est remplacé. ADR-005 n'est pas réécrit : on ne réécrit jamais un ADR accepté (règle du groupe ; journal Confluence, ADR-023, Conséquences). Cet ADR le complète.

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Quel code HTTP pour une règle refusée ? | **409, avec le message de la règle.** Déduit, pas décidé. Le service lève `ConflictError` ; le routeur la traduit déjà en 409, avec son message. C'est le code du trigger d'exclusivité, une règle du même genre. Le sujet ne tranche pas entre 409 et 422 ; il veut le motif exact. Un droit fermé, lui, n'est pas une erreur (ADR-024). | `crud_router.py:92-93`, `:101-102` ; `test_constraints_db.py:311-316` ; `Gherkin.md:597` (StarterPack) ; ADR-036 |
| « Toutes » : les quatre trous de la carte, ou toute règle sur plusieurs tables ? | **Toute règle sur plusieurs tables.** Déduit : la réponse dit « Toutes » ; la lettre M s'intitule « Règles qui croisent plusieurs tables » ; le groupe l'a appliquée ensuite à des règles hors carte (grille d'honoraires, réglages du taux, auteur d'un bien). | `questions-a-trancher.md:155`, `:408` ; `01:624-627`, `:767-768`, `:936-941` |
| Où, dans le code ? | Dans le service de la table écrite. Le registre le dit pour le renouvellement : « dans `mandate_service` (pas en SQL : la règle croise deux tables) ». | `main.py:14-17` ; `base_service.py:8-13` ; `questions-a-trancher.md:830` |
| Quel test, au minimum ? | Un test d'intégration sur `fil_rouge_test`, avec un cas refusé et un cas accepté. Déduit du plan de tests du sujet (cas nominal, cas d'erreur) et de la pratique du dépôt (Eircode refusé, puis accepté). | `PLAN-DE-TESTS.md:45-47` (StarterPack) ; `test_constraints_db.py:224-238` ; `API/tests/integration/conftest.py:44` |
| Une règle sur plusieurs lignes d'une même table, ou sur l'ancienne valeur : même traitement ? | **Oui, dans l'API.** Déduit : chaque fois que le groupe a placé une telle règle, c'est l'API. Les honoraires figés : « Appliquer C3 dans sale_service ». `'renewed'` ⇒ successeur : dans l'API (ADR-050, déduit). Seule exception : l'exclusivité (Q-MAN-02). | `questions-a-trancher.md:132`, `:670` ; ADR-050, Questions tranchées n° 2 ; ADR-039 |
| Pourquoi l'exclusivité reste-t-elle un trigger ? | Q-MAN-02 a dit « corriger, activer » le trigger déjà écrit. ADR-039 l'écrit, et écarte l'option API. Sur le fond, les 18 mandats repris s'écrivent en direct : seul un trigger les voit. | ADR-039, Options, bloc 2 ; `01:522-550` ; `02_migration.sql:238-255` |
| Faut-il changer les tables ou les diagrammes ? | Non. « Les tables : non » ; « Les diagrammes : non. Ces règles se rangent dans `09-contraintes-a-coder.md` ». | `questions-a-trancher.md:869-871` |
| Dans quel ordre coder ? | L'argent d'abord : les honoraires (blocs C2, C3 du livrable), puis le droit au paiement (C1), puis le calcul et le gel du paiement (C4, C5). La carte juge les trous du paiement « les plus graves ». Les tests d'intégration commencent aussi par `payment`, `sale`, `mandate` (Q-INF-05). | `questions-a-trancher.md:866`, `:194` ; `09-contraintes-a-coder.md:45-52` |
| Un compte, un seul profil (ADR-005) : trigger ou contrôle applicatif ? | **Applicatif, dans l'API.** Déduit : la règle croise trois tables (`client`, `hunter`, `real_estate_manager`), donc Q-MAN-06. ADR-005 laissait les deux voies ouvertes. | journal Confluence, ADR-005, Conséquences ; Q-MAN-06 |

**Questions ouvertes** 🟡

Aucune.

**Sources**

| Affirmation | Source |
|---|---|
| Q-MAN-06 : « Toutes dans l'API, chacune testée », 05/10/2026 | `md/questions/questions-a-trancher.md:155`, `:408`, `:856-872` ; carte, `questions-a-trancher.html:990-1014` |
| Les deux options, avantages et inconvénients | `questions-a-trancher.html:1013-1014` |
| Trois TODO, quatre trous ; « les plus graves » | `questions-a-trancher.md:859-866` |
| Un `CHECK` ne voit qu'une ligne ; 9 blocs, 23 règles ; ordre conseillé | `livrables/2-modelisation/09-contraintes-a-coder.md:15-24`, `:30-34`, `:45-52`, `:280` |
| Tests adverses : 2 réussites et 14 lacunes ; 5 et 11 après LOT4 ; pas rejoué | `docker/init-v3/01_create_fil_rouge_immobilier.sql:127-136` |
| Les TODO du schéma renvoyés à l'API | `01:624-627`, `:721-725`, `:767-768`, `:774-784`, `:936-941`, `:985-993` |
| Le seul trigger | `01:522-550` ; `md/adr/2026-10-08-notes-seance-adr.md:118` |
| Trois couches ; le service, lieu des règles | `API/src/app/main.py:10-20` ; `API/src/app/services/base_service.py:8-13` |
| 19 services de table en CRUD seul ; `UserService` ; `ParametrageService` sans route | `API/src/app/services/*_service.py` (8 lignes chacun) ; `user_service.py:19-26` ; `parametrage_service.py:31-32` |
| Le routeur traduit `ConflictError` en 409, avec son message | `API/src/app/routes/crud_router.py:92-93`, `:101-102` ; `API/src/app/utils/exceptions.py:21-23` |
| Code pur du calcul, pas branché | `API/src/app/services/remuneration.py:21-24`, `:166-183`, `:230-248` |
| Le sujet : persistance au-dessus du calcul ; contrôle d'accès applicatif ; résultat figé | `REGLES-CALCUL-REMUNERATION.md:760`, `:763`, `:764` (StarterPack) |
| Plan de tests du sujet | `documents utiles/PLAN-DE-TESTS.md:45-48`, `:54-56` (StarterPack) |
| Q-REM-11, Q-REM-12, Q-MAN-03 | `questions-a-trancher.md:131-132`, `:152`, `:658-675`, `:822-831` |
| Scripts d'init : ni visite, ni vente, ni paiement | `docker/init-v3/02_migration.sql:86-255` ; `03_populate_estate.sql`, `05_parametres.sql` (recherche des `INSERT INTO visit`, `sale`, `payment` : 0) |
| Données reprises : 25 comptes sans doublon ; 18 mandats signés, écrits en direct ; demandes lancées | `docker/init-v3/02_migration.sql:132-172`, `:238-255`, `:275-277` |
| Rôle en lecture seule | `docker/init-v3/04_role-lecture-seule.sql:19-21` ; `test_constraints_db.py:822-826` |
| Fixtures de vente et de paiement ; mandat 1 | `test_constraints_db.py:489-531` ; `02_migration.sql:238` |
| Motif `'mandate_expired'` | `01:896-900` |
| ADR-005 (trigger ou applicatif), ADR-021 (insertions directes), ADR-023 (on ne réécrit pas un ADR accepté) | journal Confluence, copie du 07/10/2026 : ADR-005, Conséquences ; ADR-021, Justification ; ADR-023, Conséquences |
| Liste et état des règles, au 08/10/2026 | `md/adr/adr-040-annexe-etat-des-regles.md` |
| Modèle d'ADR, « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:19-40`, `:72` (StarterPack) |

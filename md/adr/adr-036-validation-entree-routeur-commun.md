# ADR-036 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 036 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:59`,
> groupe 2, lettre G du pense-bête).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Aucune question ne reste ouverte : les cinq questions du premier jet
> sont tranchées par les sources, par une mesure ou par déduction (voir
> « Questions tranchées »).
>
> ⚠️ **Le registre se contredit sur cet ADR ; l'arbitre a tranché pour l'ADR.**
> La l. 402 de `md/questions/questions-a-trancher.md` inscrit G (Q-INF-06)
> parmi les ADR à écrire. La l. 431 dit : « pas d'ADR propre pour … Q-INF-01
> à 08 ». Le modèle du sujet réserve l'ADR aux choix « qu'on pourrait vous
> demander de justifier » (`JOURNAL-DE-DECISIONS.md:13`). Un jury peut demander
> pourquoi l'API rend 422 ici et 409 là : le choix se justifie, l'ADR aussi.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) — documents à aligner :
>
> * registre, l. 431 : écrire « Q-INF-01 à 05, 07, 08 » (Q-INF-06 a son ADR) ;
>
> * disent encore qu'un champ obligatoire manquant donne 409 :
>   `livrables/4-application/rapport-tests.md:203` (I14, « surface absente ») et `:210` ;
>   `docker/init-v3/README.md:618-621`. La carte Q-INF-06 cite aussi
>   `docker/init-v2/README.md:470-473`, mais `init-v2` est figé : à laisser ;
> * `API/src/app/models/estate_model.py:6-11` dit encore qu'un prix à virgule
>   « n'est pas encore refusé », et cite un test xfail qui n'existe plus
>   (devenu `test_estate_price_with_cents_returns_422`,
>   `API/tests/integration/test_constraints_db.py:89-90`) ;
> * comptent encore 18 ou 19 tables, alors qu'il y en a 20 (20 `CREATE TABLE`
>   dans `01`, 20 préfixes de route) : `API/src/app/routes/crud_router.py:2`, `:11` ;
>   `services/base_service.py:2` ; `repositories/base_repository.py:2` ;
>   `models/__init__.py:2` ; `API/tests/test_crud_router.py:13` ;
>   `API/src/app/main.py:24` (« 19 tables ») ;
>   `API/README.md:4`, `:113`, `:170`, `:199` ; `CLAUDE.md:13`, `:25` ;
> * `API/README.md:204-209` liste 18 routes : il manque `/review-media` et
>   `/hunter-rate-parameters` ;
> * registre : `questions-a-trancher.md:1076` garde Q-INF-06 sans ✅, avec une
>   référence périmée (`API/README.md:216-218`) ; `:1101` garde l'ancienne
>   recommandation (« ajouter des modèles d'entrée Pydantic, comme pour `/users` »).
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-036 : L'entrée de l'API est validée une fois, dans le routeur commun — 422 avant la base, 409 pour ce que seul PostgreSQL connaît

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décision et code : 05/10/2026)
* **Statut :** proposé
* **Décideurs :** le groupe (carte Q-INF-06, réponse « Valider dans le routeur commun », 05/10/2026) ; le code est du même jour (commit `fea3c9f`, Sébastien)
* **Complète :** ADR-032 (un prix à virgule est refusé en 422)
* **Voir aussi :** ADR-040 (règles qui croisent plusieurs tables, proposé) ; ADR-016 (mot de passe : les modèles propres à `/users`) ; ADR-021, ADR-022, ADR-031 (normaliser un code postal avant d'écrire)

**Contexte**

L'API expose 20 tables, en FastAPI et SQLModel. Toutes partagent les mêmes 5 routes, construites par une seule fabrique, `build_crud_router` (`API/src/app/routes/crud_router.py:63-113`).

Les modèles sont des modèles de table (`table=True`). Le script SQL reste « la source de vérité » des contraintes (`API/src/app/models/__init__.py:12-14`).

Le 05/10/2026, une mesure a montré un trou (`crud_router.py:27-32`) :

* un modèle de table SQLModel ne valide pas ce que FastAPI lui passe ;
* un prix `199999.5` était arrondi en silence à 200 000 par PostgreSQL. Il tombait dans la tranche du dessus du barème (`API/tests/integration/test_constraints_db.py:86-88`) ;
* un champ obligatoire manquant finissait en 409, comme un doublon.

Le sujet ne tranche pas entre 409 et 422. Il demande de tester « les cas d'erreur » (`documents utiles/PLAN-DE-TESTS.md:47`). Il veut, dans un scénario, le motif lu par l'utilisateur, pas « HTTP 422 » (`documents utiles/Gherkin.md:597`, `:851`).

**Options envisagées**

1. **Garder.** Avantage : aucun fichier touché. Inconvénient : le prix arrondi en silence, donc la mauvaise tranche. **Écartée.**
2. **Un modèle d'entrée Pydantic par table**, comme `UserCreate` et `UserUpdate` pour `/users`. Avantage : on pourrait y recopier les `CHECK`, et rendre 422 là aussi. Inconvénients, d'après la carte : « 17 modèles de plus au minimum (34 si, comme pour `/users`, création et mise à jour sont séparées) » ; « chaque règle existe en double (SQL et Python) et peut diverger ». La carte comptait 18 tables ; il y en a 20. C'était l'option recommandée par Claude. **Écartée.**
3. **Valider dans le routeur commun.** Avantage : une fonction pour toutes les tables. Inconvénient : les `CHECK` restent vus par PostgreSQL seul, donc 409, avec un message trompeur. **Retenue.**

**Décision**

1. Une seule fonction, `_validated`, revalide le corps de chaque `POST` et de chaque `PUT` avec `model_validate` (`crud_router.py:48-60`, appelée l. 91 et l. 98). Elle vaut pour les 20 ressources.
2. Une entrée invalide rend **422**, au format de FastAPI, `loc` préfixé par `"body"` (l. 55-59). Le service n'est pas appelé, la base n'est pas touchée. Cas : type faux, champ obligatoire vide (`null`) ou absent, prix à virgule, texte plus long que sa limite.
3. Ce que seul PostgreSQL connaît rend **409** : `CHECK`, `UNIQUE`, clé étrangère, trigger. Les `CHECK` ne sont pas recopiés en Python : le script SQL reste la seule source.
4. Pas de modèle d'entrée par table. Seule exception, `/users`, pour le mot de passe (ADR-016).
5. Une règle qui croise plusieurs tables n'est pas l'affaire du routeur. Elle va dans le service (ADR-040, proposé).

**Justification**

* **Mesuré, avec contre-épreuve.** Un prix à virgule rend 422 et rien n'est écrit (`test_constraints_db.py:86-93`). `surface` à `null` rend 422 (l. 96-99). Sans `_validated`, 3 tests échouent (message du commit `fea3c9f`).
* **Un seul endroit.** Le routeur commun est déjà « le seul endroit qui traduit les exceptions "métier" … en codes HTTP » (`crud_router.py:16-18`). Y ajouter la validation couvre les 20 tables sans toucher à leurs 20 fichiers.
* **Pas de règle en double.** Un `CHECK` recopié en Python pourrait diverger du SQL. Le trigger et les clés étrangères, eux, ne se recopient pas : il faut lire la base.
* **L'argent est protégé.** Un prix à virgule ne peut plus changer la tranche du barème (ADR-032).
* **Le partage 422 / 409 se lit simplement** (déduit) : 422, la requête est mal formée ; 409, la base la refuse. Pour un `CHECK`, le 409 est un compromis : la valeur est fausse, elle n'est pas en conflit. Limite acceptée, voir Conséquences.

**Conséquences**

* ✅ **Fait le 05/10/2026** : commit `fea3c9f` ; modèles en `int` le même jour (`d3c128c`, Q-REM-01). La documentation de l'API est à jour (`API/README.md:220-232`).
* **Tests** : 422 pour un prix à virgule et pour un champ obligatoire à `null` ; 409 pour trois `CHECK` du bien, prix `-1`, type `Péniche`, surface `0` (`test_constraints_db.py:86-112`). L'en-tête du fichier de tests pose la même règle (l. 39-42).
* **Le `PUT` remplace la ligne entière** sur les 19 ressources autres que `/users` : il reçoit le modèle de table (`crud_router.py:75`). Un champ obligatoire absent y rend aussi 422. Mesuré par Claude le 08/10/2026, sans base, routeur monté sur un service factice : `PUT` complet 200, sans `surface` 422, prix `199999.5` 422, service non appelé dans les deux refus. `/users` garde un `PUT` partiel (`UserUpdate`).
* **Même mesure, au `POST`** : une référence de 60 caractères rend 422 (limite `max_length=50`, `API/src/app/models/estate_model.py:37`). Au niveau du routeur, `Péniche`, un prix `-1` et un Eircode avec espace passent (201 sur le service factice) : ils sont refusés plus loin, par PostgreSQL, en 409.
* ⚠️ **Limite acceptée : le message du 409 est le même pour tout.** « Contrainte violée (valeur en double ou référence inexistante). » (`API/src/app/repositories/base_repository.py:30`). Il s'affiche aussi pour un type `Péniche`, qui n'est ni un doublon ni une référence. `API/README.md:252-254` le dit. 💡 Un message par sorte de contrainte, lu dans l'erreur de PostgreSQL : une micro-décision, hors de cet ADR (`documents utiles/JOURNAL-DE-DECISIONS.md:13`).
* **Normaliser avant d'écrire : pas fait.** ADR-021 et ADR-022 demandent que l'API formate un code postal avant d'écrire. ADR-031 demande de retirer l'espace d'un Eircode. Aujourd'hui, `D02 X285` est refusé en 409 (`test_constraints_db.py:224-229`). 💡 Un validateur déclaré sur le modèle passerait par `_validated` sans toucher au routeur. Déduit de `model_validate`, pas essayé.
* **Une règle métier codée dans un service** lève `ConflictError`, que le routeur traduit déjà en 409, avec le message du service (`crud_router.py:92-93`, `:101-102`). Le routeur n'a pas à changer (ADR-040).
* **Journal** : aucun ADR existant n'est remplacé.

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Recopier les `CHECK` en Python (`Literal`), pour rendre 422 au lieu de 409 ? | **Non.** Déduit : c'est l'option écartée par Q-INF-06, « chaque règle existe en double ». La carte d'idée I6 la repropose ; elle n'a pas de réponse, et ne rouvre pas la question tant que le groupe ne la coche pas. | `md/questions/questions-a-trancher.html:2202` ; carte I6, l. 2691-2697 |
| Un champ obligatoire vide ou absent : 409 ou 422 ? | 422, dans les deux cas. Mesuré : à `null` par un test ; absent, par `POST /roles` avec `{}`. | `test_constraints_db.py:96-99` (`"surface": None`) ; `API/README.md:225-226` (`missing` sur `wording`) |
| Le `PUT` est-il couvert, ou seulement le `POST` ? | Les deux. | `crud_router.py:91`, `:98` ; mesure sans base du 08/10/2026 (Conséquences) |
| Pourquoi `/users` a-t-il ses propres modèles d'entrée ? | Pour le mot de passe, pas pour la validation. `UserCreate` le reçoit en clair, le service le hache, `UserPublic` ne le rend jamais. Déduit. | `API/src/app/routes/user_router.py:10-17` ; `API/src/app/services/user_service.py:19-26` ; ADR-016 |
| Le sujet impose-t-il 409 ou 422 ? | Non. Recherche de `422`, `409`, `pydantic`, `fastapi` dans le StarterPack : rien sur ce choix. Il demande de tester les cas d'erreur, et d'écrire le motif lu par l'utilisateur. | `PLAN-DE-TESTS.md:47` ; `Gherkin.md:597`, `:851` (StarterPack) ; `questions-a-trancher.html:2190` |

**Questions ouvertes** 🟡

Aucune.

**Sources**

| Affirmation | Source |
|---|---|
| Q-INF-06 : « valider dans le routeur commun », 05/10/2026 | `md/questions/questions-a-trancher.md:133` ; carte, `questions-a-trancher.html:2180-2204` |
| Les trois options, leurs avantages et inconvénients | `questions-a-trancher.html:2202-2204` |
| Le trou mesuré le 05/10/2026 | `API/src/app/routes/crud_router.py:27-32` ; `test_constraints_db.py:86-88` |
| `_validated`, appelée au `POST` et au `PUT` | `crud_router.py:48-60`, `:91`, `:98` |
| Le `PUT` reçoit le modèle de table, sauf `/users` | `crud_router.py:20-25`, `:75` ; `user_router.py:13-15` |
| Le routeur seul traduit les exceptions en codes HTTP | `crud_router.py:16-18` |
| `ConflictError` → 409 ; message unique | `crud_router.py:92-93`, `:101-102`, `:110-111` ; `base_repository.py:30`, `:79-85` |
| Le script SQL, seule source des contraintes | `API/src/app/models/__init__.py:12-14`, `:19-23` |
| 20 tables, 20 ressources | `docker/init-v3/01_create_fil_rouge_immobilier.sql` (20 `CREATE TABLE`) ; `API/src/app/main.py` (20 `include_router`) |
| Tests | `API/tests/integration/test_constraints_db.py:39-42`, `:86-112`, `:224-229` |
| Commits | `fea3c9f` (05/10/2026, Sébastien Granarolo) ; `d3c128c` |
| Code HTTP documenté | `API/README.md:215-232`, `:252-254` |
| Ce que dit le sujet | `documents utiles/PLAN-DE-TESTS.md:45-48` ; `documents utiles/Gherkin.md:574`, `:597`, `:851` (StarterPack) |
| Normaliser avant d'écrire | ADR-021, Conséquences, et ADR-022, Conséquences (journal Confluence, copie du 07/10/2026) ; ADR-031, Conséquences et Questions tranchées n° 3 |
| Modèle d'ADR ; micro-décisions ; « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:13`, `:19-40`, `:72` (StarterPack) |

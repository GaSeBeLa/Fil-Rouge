> **QUAND LIRE** : on joue une fiche `DRO*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache DRO<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier DRO — Droits : moindre privilège

**Ouvert.** le 2026-10-13.

**À quoi il sert.** Le code vérifie le rôle, jamais « le sien », et ouvre par
défaut presque tout à tout compte connecté. Ce chantier ferme tout par défaut,
puis rouvre ce que la cible d'ADR-027 donne, rôle par rôle et ligne par ligne.

**Fait.** Cadré le 2026-10-13 en 10 fiches ; `DRO11` ajoutée le même jour (fuite du
formulaire, choix B de Seb), jouée avant `DRO10`.

**Session** : 5f96deba-d497-4409-80b3-b6b6e591a21c

## Le socle commun

**Où vit le code.** Dans le dépôt `../Fil-Rouge-API/` : tout chemin `API/…`
ou `docker/…` ci-dessous s'y lit. Les docs (`md/…`) sont dans Fil-Rouge.

**Les décisions du cadrage** (Seb, Discord, 13/10/2026)

- **Moindre privilège** : fermé par défaut. Chaque table déclare qui lit, qui
  crée, qui modifie. Une case que la cible ne donne pas reste **fermée**.
  L'`Admin` n'a que ce que la cible lui donne.
- **La cible** : `md/adr/adr-027-annexe-matrice-detaillee.md`, case par case,
  et `md/adr/adr-027-matrice-acces-par-role.md` (points 4 à 10). Les trois
  cases qui attendent Jeff (Q-ACC-06, 12, 13) s'appliquent comme l'annexe les
  donne ; on ajustera après lui. `estate_contact` suit ADR-054 (déjà conforme).
- **La ligne d'un autre** : `404`, comme une ligne qui n'existe pas. Une liste
  ne rend que les lignes visibles.
- **API et base** : le compte PostgreSQL `fil_rouge_reader` est fermé aussi.

**Où brancher**

| Symbole | Fichier | Ce qu'il fait |
|---|---|---|
| `build_crud_router` | `API/src/app/routes/crud_router.py` | 4 routes par table ; `read_roles`, `write_roles`, `create_roles` ; défauts `ALL_ROLES` et `WRITER_ROLES` aujourd'hui |
| `list_items`, `get_item`, `update_item`, `create_item` | même fichier, dans `build_crud_router` | seul `create_item` reçoit le compte (`principal`) aujourd'hui |
| `require_roles`, `Principal`, `get_principal` | `API/src/app/utils/roles.py` | `403` hors des rôles ; `require_roles()` vide = fermé à tous |
| `ALL_ROLES`, `WRITER_ROLES`, `ADMIN`… | même fichier | les 5 libellés de la table `role` |
| `BaseService.list_all`, `.get_by_id`, `.replace` | `API/src/app/services/base_service.py` | à étendre pour « le sien » (`DRO4`) |
| `NotFoundError`, `ForbiddenError`, `ConflictError` | `API/src/app/utils/exceptions.py` | 404, 403, 409 |
| fixtures `db_client` (connecté en `Admin`), `db_session` ; `acting_as(role, user_id)` | `API/tests/integration/conftest.py`, `API/tests/conftest.py` | se connecter sous un autre rôle |
| `print_rights_matrix.py` | `docker/tools/` | relève les rôles de chaque route (91 opérations au 13/10) |

**Les règles de l'atelier**

- Chaque fiche prouve **ce qui est interdit** : un test de refus (`403`, ou
  `404` pour « le sien ») par geste qu'elle ferme, sous le rôle refusé.
- Beaucoup de tests existants passent en `Admin` : un test qui casse parce
  qu'un droit s'est fermé se corrige en prenant le bon rôle (`acting_as`),
  jamais en rouvrant le droit.
- Vérification : depuis `docker/`, `docker compose exec -T api python -m pytest -q -p no:cacheprovider` ;
  compte brut `N passed` avant et après. `pyright` sur les fichiers touchés,
  depuis `API/`. Chaque critère nomme son test et **son mutant**.
- Chaque règle cite sa source en commentaire (`ADR-027`, `Q-ACC-xx`, `P<n>`).
- Une fiche qui change un droit met à jour la description « Qui peut » du
  Swagger (elle suit `read_roles`/`write_roles` seule) et `API/README.md`.

**Hors du chantier** : la page de login (ADR-028) ; un 6e rôle ; le traitement
planifié de l'anonymisation (V2) ; la RACI et le registre RGPD (carte « Doc
d'équipe »).

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `DRO1` | Fermer par défaut et déclarer les rôles de chaque table | rien |
| `DRO2` | Réserver l'argent à qui la cible le donne | `DRO1` |
| `DRO3` | Revoir les routes à part | `DRO1` |
| `DRO4` | Poser le mécanisme « le sien » | `DRO1` |
| `DRO5` | Limiter le Client à ses lignes | `DRO4` |
| `DRO6` | Limiter le Hunter à ses lignes | `DRO4` |
| `DRO7` | Limiter le Manager à son équipe | `DRO4`, `DRO6` |
| `DRO8` | Réserver les comptes désactivés à l'Admin | `DRO4` |
| `DRO9` | Fermer `fil_rouge_reader` sur paiements et comptes désactivés | rien |
| `DRO11` | Fermer la fuite du formulaire | `DRO3` |
| `DRO10` | Refaire le relevé et mettre la doc à jour | `DRO1` à `DRO9`, `DRO11` |

`DRO9` ne dépend de rien et peut se jouer à tout moment. `DRO2` et `DRO3`
sont parallèles ; `DRO5`, `DRO6`, `DRO8` aussi, après `DRO4`.

---

<!-- FICHE:DRO1 -->
## DRO1 [x] — Fermer par défaut et déclarer les rôles de chaque table

**Session** : 15e33082-f94c-4e7f-82b3-169a3c651e22
**Dépend de** : rien.
**Fichiers** : `API/src/app/routes/crud_router.py`, les 21 `API/src/app/routes/*_router.py` qui l'appellent, `md/adr/adr-027-annexe-matrice-detaillee.md` (lecture), les tests d'intégration qui cassent, un nouveau `API/tests/integration/test_droits_par_role.py`.

**Prompt**
Dans `build_crud_router`, les défauts de `read_roles` et `write_roles`
deviennent `()` : fermé à tous. Chaque routeur déclare alors ses rôles,
lus dans l'annexe d'ADR-027, **au niveau du rôle** :
- un rôle a un geste (R, C, U) sur une table si l'annexe le lui donne, même
  limité à « le sien » (le filtre viendra en `DRO4` à `DRO8`) ;
- `Reader` : R partout, sauf `payment` (point 8) ; aucune écriture ;
- une case « — », ou absente : fermée ;
- `criteria` : aucun U (versions, point 5) ; `hunter_performance` : ni C ni U.
Laisse **ouvert comme aujourd'hui** les tables d'argent (`parameters_fees`,
`commission_scale`, `hunter_rate_parameters`, `payment`, `sale`) : c'est `DRO2`.
Les comptes (`user`, `hunter`, `real_estate_manager`) : l'annexe donne
« U le sien » ; garde le U à `Admin` seul jusqu'à `DRO5`-`DRO7`.
Ajoute `test_droits_par_role.py` : pour chaque table, un rôle refusé reçoit
`403` en lecture, en création et en modification là où l'annexe le ferme.

**Critère de fin**
`test_droits_par_role.py` vert, avec au moins un refus par table fermée ;
suite complète verte, compte brut avant et après. Mutant : remettre
`WRITER_ROLES` en défaut de `write_roles` → au moins un test de refus tombe.
<!-- /FICHE -->

---

<!-- FICHE:DRO2 -->
## DRO2 [x] — Réserver l'argent à qui la cible le donne

**Session** : 15e33082-f94c-4e7f-82b3-169a3c651e22
**Dépend de** : `DRO1`.
**Fichiers** : `API/src/app/routes/{parameters_fees,commission_scale,hunter_rate_parameters,payment,sale}_router.py`, `API/src/app/routes/sale_router.py` (route `/payment`), `md/adr/adr-027-annexe-matrice-detaillee.md` § 4 (lecture), `API/tests/integration/test_droits_par_role.py`, les tests de paiement qui cassent.

**Prompt**
Applique l'annexe d'ADR-027, § 4 :
- `parameters_fees`, `commission_scale`, `hunter_rate_parameters` : C et U
  `Admin` seul (Q-ACC-07) ; R `Admin`, `Hunter`, `Manager`, pas `Client`.
- `payment` : jamais saisi à la main (point 10) → `POST /payments` fermé à
  tous ; U (programmé, payé) `Admin` ; R `Admin`, `Hunter`, `Manager` ; ni
  `Client` ni `Reader` (point 8).
- `POST /sales/{id}/payment` (le calcul) : `Admin` seul.
- `sale` : C `Manager` (Q-ACC-03) ; R `Client`, `Hunter`, `Manager`, `Admin`,
  `Reader` ; U fermé sauf si l'annexe le donne.
Vérifie que `PaymentService` écrit encore la note `hunter_performance` quand
l'`Admin` passe un paiement à `paid`.

**Critère de fin**
Tests de refus : un `Client` reçoit `403` sur `POST /commission-scales`,
`GET /payments`, `POST /sales/{id}/payment` ; un `Hunter` sur
`POST /sales`. Suite verte, compte brut. Mutant : remettre `Client` dans les
lecteurs de `payment` → le test `GET /payments` en `Client` tombe.
<!-- /FICHE -->

---

<!-- FICHE:DRO3 -->
## DRO3 [x] — Revoir les routes à part

**Session** : 15e33082-f94c-4e7f-82b3-169a3c651e22
**Dépend de** : `DRO1`.
**Fichiers** : `API/src/app/routes/auth_router.py`, `API/src/app/routes/signup_router.py`, `API/src/app/routes/user_router.py`, `API/src/app/routes/estate_contact_router.py`, `API/src/app/main.py` (route `/`), `API/tests/integration/test_droits_par_role.py`.

**Prompt**
Passe chaque route hors CRUD au crible du moindre privilège, et écris pour
chacune, en commentaire, pourquoi elle est ouverte à qui elle l'est :
- `GET /` (health-check) : sans clé ; ne rend rien d'autre qu'un statut ;
- `POST /auth/login`, `POST /search-requests/submit` : clé d'API sans
  jeton, par nature (ADR-028, ADR-039 du parcours) ; vérifie qu'elles ne
  rendent aucune donnée d'un autre compte ;
- `GET /auth/me` : tout compte connecté, **son** compte seul ;
- les deux anonymisations : `Admin` seul (ADR-049, ADR-054).
Toute route qui en dit plus que nécessaire se resserre ; une route qui ne
change pas le dit dans son commentaire.

**Critère de fin**
Un test par route à part : le rôle refusé, ou la réponse qui ne fuit rien
(`/auth/me` ne rend que le compte du jeton, sans `password`). Suite verte,
compte brut. Mutant : rendre l'id de l'URL dans `/auth/me` au lieu du jeton
→ le test tombe.
<!-- /FICHE -->

---

<!-- FICHE:DRO4 -->
## DRO4 [x] — Poser le mécanisme « le sien »

**Session** : 15e33082-f94c-4e7f-82b3-169a3c651e22
**Dépend de** : `DRO1`.
**Fichiers** : `API/src/app/routes/crud_router.py`, `API/src/app/services/base_service.py`, `API/src/app/services/payment_service.py` (table pilote), un nouveau `API/tests/integration/test_le_sien.py`.

**Prompt**
Le second contrôle d'ADR-027 (point 2), branché une fois pour toutes :
- `list_items`, `get_item`, `update_item` reçoivent le `Principal`, comme
  `create_item`, et le passent au service ;
- `BaseService` gagne un crochet de visibilité, surchargé par table : par
  défaut, **tout reste visible** (aucun changement de comportement ici) ;
- une liste ne rend que les lignes visibles ; une ligne non visible, en
  lecture comme en modification, lève `NotFoundError` → **404** ;
- `Admin` voit tout ; `Reader` voit ce que ses rôles lui ouvrent.
Branche une table pilote, `payment` : un `Hunter` ne voit que les siens
(`payment.id_hunter`). Le filtre se fait en SQL (dans la requête), pas en
Python après coup.

**Critère de fin**
`test_le_sien.py` : le chasseur 1 liste ses paiements seulement, reçoit `404`
sur celui du chasseur 2, en lecture et en `PUT`. Suite verte, compte brut.
Mutant : neutraliser le filtre de `payment` → le test du `404` tombe.
<!-- /FICHE -->

---

<!-- FICHE:DRO5 -->
## DRO5 [x] — Limiter le Client à ses lignes

**Session** : 15e33082-f94c-4e7f-82b3-169a3c651e22
**Dépend de** : `DRO4`.
**Fichiers** : les services de `user`, `client`, `search_request`, `criteria`, `mandate`, `estate`, `picture`, `estate_proposed`, `estate_searchrequest`, `review_media`, `visit`, `sale` dans `API/src/app/services/`, `API/src/app/routes/user_router.py`, `md/adr/adr-027-annexe-matrice-detaillee.md` § 1 à 4 (colonne Client), `API/tests/integration/test_le_sien.py`.

**Prompt**
Pour chaque table de la colonne `Client` de l'annexe, écris le crochet de
visibilité : son compte, son profil, ses demandes et critères, ses mandats,
les biens proposés pour lui (Q-ACC-05) et leurs photos, l'avis sur sa
demande, ses visites, sa vente. En écriture : il ne crée ou ne modifie que
pour lui (`id_client` = son compte, sinon `404` ou `409`, comme le service le
dit). Ouvre `PUT /users/{id}` à son propre compte, sans rôle ni activation
(annexe § 1). Le chemin d'appartenance de chaque table passe par les clés
du schéma (`docker/init-v3/01_create_fil_rouge_immobilier.sql`).

**Critère de fin**
Deux clients du seed : chacun liste ses lignes, reçoit `404` sur celles de
l'autre, table par table ; il ne change ni son rôle ni son activation.
Suite verte, compte brut. Mutant : retirer le filtre de `mandate` → le
test « mandat d'un autre client » tombe.
<!-- /FICHE -->

---

<!-- FICHE:DRO6 -->
## DRO6 [x] — Limiter le Hunter à ses lignes

**Session** : 15e33082-f94c-4e7f-82b3-169a3c651e22
**Dépend de** : `DRO4`.
**Fichiers** : les services de `client`, `hunter`, `search_request`, `criteria`, `mandate`, `estate_proposed`, `estate_searchrequest`, `review_media`, `visit`, `sale`, `commission_scale`, `hunter_performance`, `real_estate_manager` dans `API/src/app/services/`, `md/adr/adr-027-annexe-matrice-detaillee.md` (colonne Hunter), `API/tests/integration/test_le_sien.py`.

**Prompt**
Même travail que `DRO5`, colonne `Hunter` : ses clients (H3), ses demandes
(accepter, refuser), ses mandats, critères, sélections et avis, propositions,
visites, ventes, sa note ; le barème par défaut et le sien (Q-ACC-06) ; son
manager ; son propre profil en U (ses coordonnées). Les biens restent
lisibles en entier (H2, H5). Le paiement est déjà fait (`DRO4`).

**Critère de fin**
Chasseurs 1 et 2 du seed : chacun ne voit que ses lignes, `404` sur celles
de l'autre ; le barème d'un autre chasseur → `404`, le barème par défaut
visible. Suite verte, compte brut. Mutant : retirer le filtre de `client`
→ le test « client d'un autre chasseur » tombe.
<!-- /FICHE -->

---

<!-- FICHE:DRO7 -->
## DRO7 [x] — Limiter le Manager à son équipe

**Session** : 4e508779-8618-401d-b40e-17c615120929
**Dépend de** : `DRO4`, `DRO6`.
**Fichiers** : les services de `hunter`, `search_request`, `criteria`, `mandate`, `visit`, `sale`, `payment`, `hunter_performance`, `commission_scale`, `real_estate_manager` dans `API/src/app/services/`, `md/adr/adr-027-annexe-matrice-detaillee.md` (colonne Manager, « L'équipe d'un manager »), `API/tests/integration/test_le_sien.py`.

**Prompt**
L'équipe d'un manager : ses chasseurs (`hunter.id_realestatemanager`) et
les demandes qui lui sont confiées (`search_request.id_realestatemanager`).
Il lit le travail de son équipe, pas l'identité des clients : les tables
« — » de sa colonne restent fermées depuis `DRO1`. En écriture : il affecte
une demande (Q-ACC-10) et enregistre une vente (Q-ACC-03) de son équipe
seulement. Réutilise les chemins de `DRO6` (un chasseur → ses lignes) plutôt
que de les réécrire.

**Critère de fin**
Deux managers du seed (le seed 02 n'en a qu'un ? le compter d'abord, et en
créer un dans le test s'il le faut) : chacun voit son équipe, `404` sur
l'autre. Suite verte, compte brut. Mutant : retirer le filtre d'équipe de
`payment` → le test tombe.
<!-- /FICHE -->

---

<!-- FICHE:DRO8 -->
## DRO8 [x] — Réserver les comptes désactivés à l'Admin

**Session** : 4e508779-8618-401d-b40e-17c615120929
**Dépend de** : `DRO4`.
**Fichiers** : les services de `user`, `client`, `hunter`, `real_estate_manager` dans `API/src/app/services/`, `md/adr/adr-049-effacement-compte-desactiver-anonymiser.md` (lecture), `API/tests/integration/test_le_sien.py`.

**Prompt**
ADR-027, point 7 : les données personnelles d'un compte désactivé
(`"user".is_activated = FALSE`) ne sont plus lues que par l'`Admin`. Ajoute
cette règle aux crochets de visibilité des quatre tables, pour tous les
autres rôles, `Reader` compris : la ligne devient `404`, et sort des listes.
Les lignes qui la citent (un mandat, une vente) restent lisibles : seul le
profil se cache.

**Critère de fin**
Un compte désactivé dans le test : `Reader` et `Hunter` reçoivent `404` sur
son profil, `Admin` le lit. Suite verte, compte brut. Mutant : retirer la
condition `is_activated` → le test en `Reader` tombe.
<!-- /FICHE -->

---

<!-- FICHE:DRO9 -->
## DRO9 [x] — Fermer `fil_rouge_reader` sur paiements et comptes désactivés

**Session** : 4e508779-8618-401d-b40e-17c615120929
**Dépend de** : rien.
**Fichiers** : `docker/init-v3/04_role-lecture-seule.sql`, une nouvelle migration `docker/migrations/v2-vers-v3/43_<nom>.sql`, `API/tests/integration/test_contact_vendeur.py` (modèle : `test_reader_role_cannot_read_contacts`), un nouveau test dans `API/tests/integration/`.

**Prompt**
Le compte PostgreSQL d'analyse suit la cible de `Reader` :
- `REVOKE SELECT ON payment FROM fil_rouge_reader` (point 8) ;
- les comptes désactivés : une politique de sécurité par ligne (row level
  security) sur `"user"`, `client`, `hunter`, `real_estate_manager`, qui ne
  montre à `fil_rouge_reader` que les comptes actifs. ⚠️ Vérifie d'abord que
  l'API se connecte en propriétaire des tables (elle contourne alors la
  politique) : le dire en une ligne, avec la mesure.
Écris la même chose en migration 43 pour une base existante, et donne la
commande PowerShell pour la jouer (comme la 41).

**Critère de fin**
Test sous `SET LOCAL ROLE fil_rouge_reader` : `SELECT` sur `payment` →
« permission denied » ; un compte désactivé absent de `"user"`. L'API lit
toujours tout (suite verte, compte brut). Mutant : retirer le `REVOKE` → le
test tombe.
<!-- /FICHE -->

---

<!-- FICHE:DRO11 -->
## DRO11 [x] — Fermer la fuite du formulaire

**Session** : 4e508779-8618-401d-b40e-17c615120929
**Dépend de** : `DRO3`.
**Fichiers** : `API/src/app/services/signup_service.py`, `API/src/app/routes/signup_router.py`, `API/tests/integration/test_droits_par_role.py` (`test_malformed_form_gets_the_same_answer_whoever_the_email`), `API/README.md` (Limites connues).

**Prompt**
Choix B de Seb (2026-10-13), après le refus de `DRO3` par le relecteur.
`POST /search-requests/submit` juge les formats (téléphone, code postal) par
les CHECK de la base, et seulement quand une fiche s'écrit : un formulaire
mal formé rend `409` pour un email neuf, `202` pour un email connu (client,
chasseur, manager, admin). L'email se devine.
Pour un email connu, rejoue le chemin d'un email neuf dans un SAVEPOINT
(`session.begin_nested()`) : un compte jetable, puis sa fiche client avec les
champs du formulaire, `flush` pour que la base juge, puis annule le
SAVEPOINT. Un refus de la base → la même erreur que pour un email neuf ; sinon
le chemin connu continue, sans rien réécrire. Les CHECK ne se recopient pas
en Python : la base reste seul juge. Mets à jour l'en-tête du service (la
« Limite connue » disparaît) et `API/README.md`.

**Critère de fin**
`test_malformed_form_gets_the_same_answer_whoever_the_email` passe sans
`xfail`, et vérifie aussi un email de chasseur ; un formulaire bien formé
d'un email connu rend toujours `202` et ne laisse ni compte ni fiche de
plus. Suite verte, compte brut. Mutant : retirer la sonde du SAVEPOINT → le
test retombe.
<!-- /FICHE -->

<!-- FICHE:DRO10 -->
## DRO10 [ ] — Refaire le relevé et mettre la doc à jour

**Dépend de** : `DRO1`, `DRO2`, `DRO3`, `DRO4`, `DRO5`, `DRO6`, `DRO7`, `DRO8`, `DRO9`, `DRO11`.
**Fichiers** : `docker/tools/print_rights_matrix.py`, `md/securite/matrice-droits-crud-par-role.md`, `md/adr/adr-027-matrice-acces-par-role.md`, `API/README.md`, `CLAUDE.md` (Fil-Rouge, « Où on en est »).

**Prompt**
Relance `print_rights_matrix.py` et remplace le § 2 de la matrice par sa
sortie. Réécris le § 3 : les écarts fermés passent en « Conformes », ceux
qui restent sont dits. Ajoute que « le sien » est codé, table par table.
Dans ADR-027 (proposé, donc modifiable), la Conséquence « aucun contrôle de
droit n'est codé » devient fausse : corrige-la. `API/README.md` : la section
des droits et le compte de tests. Applique « Ramasser sa poubelle » : grep
de « tous sauf Reader », « pas codé », « aucun contrôle » dans les deux dépôts.

**Critère de fin**
Le § 2 de la matrice est la sortie brute de l'outil (91 opérations, ou le
nouveau compte) ; le grep des anciennes phrases ne rend plus que de
l'historique daté. Comptes bruts dans le compte rendu.
<!-- /FICHE -->

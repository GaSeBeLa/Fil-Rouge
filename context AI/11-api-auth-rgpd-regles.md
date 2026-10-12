> **QUAND LIRE** : on joue une fiche `API*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache API<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier API — API : auth, RGPD et règles métier

**À quoi il sert.** Coder dans l'API ce que les ADR acceptés le 12/10/2026
décident : connexion, rôles, clé d'API, règles entre tables, anonymisation, et
le calcul de rémunération branché sur la base.

**Ouvert.** le 2026-10-12.

**Estimé.** 14 fiches · ≈56 $ — ≈4,00 $/fiche sur 2 clos (le 2026-10-12).

**Fait.** Rien. Cadré en 12 fiches, `API1` à jouer. Base prête : schéma v3,
20 tables, 258 tests verts au 12/10.

**Session** : aded003c-7d9f-4c76-83df-6971407e7c1a

## Le socle commun

**Où brancher** (lu le 12/10/2026) :

| Symbole | Fichier | Ce qu'il fait |
|---|---|---|
| `build_crud_router` | `API/src/app/routes/crud_router.py` | fabrique les 5 routes des **20** routeurs ; seul endroit qui traduit les erreurs en HTTP |
| `BaseService.create`, `.replace` | `API/src/app/services/base_service.py` | à surcharger dans `services/<table>_service.py` pour une règle |
| `NotFoundError`, `ConflictError` | `API/src/app/utils/exceptions.py` | 404 et **409** : une règle métier refusée lève `ConflictError` |
| `hash_password`, `verify_password`, `needs_rehash` | `API/src/app/utils/security.py` | Argon2id (ADR-016) |
| `UserService`, `UserCreate`, `UserUpdate`, `UserPublic` | `services/user_service.py`, `models/user_model.py` | `password` ne sort jamais |
| `ParametrageService.charger` | `API/src/app/services/parametrage_service.py` | rend le `Parametrage` en vigueur à une date ; branché sur aucune route |
| `calculer_remuneration`, `noter_criteres` | `API/src/app/services/remuneration.py` | code du sujet, fonction pure ; reçoit des nombres déjà comptés |
| fixtures `client`, `db_client`, `db_session`, `create_user` | `API/tests/conftest.py`, `API/tests/integration/conftest.py` | `db_client` tourne sur `fil_rouge_test` |

**Les décisions qui valent partout**

- Les 5 rôles de la table `role` : `Admin`, `Client`, `Hunter`, `Manager`, `Reader` (ADR-028, point 7).
- Tant que la matrice d'ADR-027 attend Jeff, **seules les règles d'ADR acceptés** s'appliquent : `Reader` lit sans écrire (028) ; anonymiser = `Admin` (049) ; `POST /estates` = `Hunter` ou `Manager` (047) ; `hunter_performance` jamais saisi à la main (035) ; un média = le chasseur auteur de la note (051). Tout le reste : tout compte connecté.
- Une règle qui croise plusieurs tables vit dans le **service** (ADR-040), pas en trigger. Chaque règle cite son ADR ou son `P<n>` dans un commentaire.
- Les trous `P<n>` sont décrits dans `md/journal/problemes-a-regler.md` (§ « P<n>. ») ; les choix, dans `md/adr/adr-053-trous-de-la-base-decisions.md`.

**Les règles de l'atelier**

- ⚠️ **`docker/docker-compose.yml`** : toute fiche qui doit y ajouter une variable (`JWT_SECRET`, `API_KEY_<NOM>`) **s'arrête et demande le oui** de l'utilisateur. Le service `api` ne reçoit que ce que liste son bloc `environment:`.
- Aucun secret dans git : les valeurs vont dans `docker/.env`, et un exemple vide dans `docker/.env.exemple`.
- Vérification : depuis `docker/`, `docker compose exec -T api python -m pytest -q -p no:cacheprovider` ; compte brut `N passed` avant et après. `pyright` sur les fichiers Python touchés, compte brut.
- Chaque critère nomme son test et **son mutant** : le contrôle retiré exprès, et le test qui doit tomber.
- Une fiche qui change une route met à jour `API/README.md` (routes, tests).

**Hors du chantier** (ADR proposés, en attente de Jeff) : la matrice des droits (027), le renouvellement (050), l'exclusivité (039), le motif de refus (024). Le traitement planifié de l'anonymisation : V2 (ADR-049, point 9). Aucun envoi de fichier vers MinIO.

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `API1` | Se connecter et recevoir un jeton JWT | rien |
| `API2` | Brancher les rôles sur toutes les routes | `API1` |
| `API3` | Exiger une clé d'API par programme | `API1` |
| `API4` | Contrôler les entrées sur une seule ligne | rien |
| `API5` | Figer les versions et l'ordre du paiement | rien |
| `API6` | Noter l'auteur d'un bien et d'un média | `API2` |
| `API7` | Contrôler propositions et visites | rien |
| `API8` | Contrôler signature et vente | rien |
| `API9` | Enregistrer une demande avant le compte | `API1` |
| `API10` | Anonymiser un compte et fermer DELETE | `API2` |
| `API11` | Noter les mandats par le taux de transformation | rien |
| `API12` | Brancher la rémunération sur la base | `API5`, `API8`, `API11` |

Ordre voulu : auth (`API1` à `API3`), puis trous (`API4` à `API9`), puis RGPD
(`API10`), puis rémunération (`API11`, `API12`). `API4`, `API5`, `API7`, `API8`
et `API11` ne dépendent de rien : leur ordre peut changer.

---

<!-- FICHE:API1 -->
## API1 [ ] — Se connecter et recevoir un jeton JWT

**Dépend de** : rien.
**Fichiers** : `API/requirements.txt`, `API/src/app/utils/security.py`, un nouveau `API/src/app/routes/auth_router.py`, `API/src/app/main.py`, `API/src/app/services/user_service.py`, `md/adr/adr-052-jeton-jwt-60-minutes.md`, `docker/.env.exemple`, un nouveau `API/tests/test_auth.py`.

**Prompt**
Code ADR-052 : un JWT `HS256` signé avec `pyjwt`, valable **60 minutes**, sans
jeton de rafraîchissement.
- `POST /auth/login` reçoit email et mot de passe, vérifie par `verify_password`,
  re-hache si `needs_rehash`, et rend le jeton. Mauvais identifiants ou compte
  `is_activated = FALSE` : **401**, même message dans les deux cas.
- Une dépendance `get_current_user` lit le jeton (`Authorization: Bearer`) et
  **relit l'utilisateur en base** à chaque appel : son rôle et son activation du
  moment font foi. Jeton expiré, faux, ou compte désactivé : 401.
- Le secret se lit dans la variable `JWT_SECRET` ; absente, l'API refuse de
  démarrer avec un message clair. ⚠️ L'ajouter à `docker-compose.yml` :
  **arrête-toi et demande le oui**.
- Ne branche **pas** encore la dépendance sur les routes CRUD : c'est `API2`.

**Critère de fin**
`test_auth.py` : connexion réussie (200, jeton), mauvais mot de passe (401),
compte inactif (401), jeton expiré (401), compte désactivé après l'émission
du jeton (401). Mutant : retirer la relecture en base → le test « compte
désactivé après l'émission » tombe. Suite complète verte, compte brut.
<!-- /FICHE -->

---

<!-- FICHE:API2 -->
## API2 [ ] — Brancher les rôles sur toutes les routes

**Dépend de** : `API1`.
**Fichiers** : `API/src/app/routes/crud_router.py`, un nouveau `API/src/app/utils/roles.py`, `API/src/app/routes/hunter_performance_router.py`, `API/tests/conftest.py`, `API/tests/integration/conftest.py`, un nouveau `API/tests/test_roles.py`.

**Prompt**
Code le **mécanisme** des rôles (ADR-028), pas la matrice (ADR-027).
- Une dépendance `require_roles(*roles)` qui lit le rôle de `get_current_user`
  et rend **403** si le rôle n'est pas permis.
- `build_crud_router` exige un jeton sur ses routes ; `GET` ouvert à tout compte
  connecté ; `POST` et `PUT` refusés au rôle `Reader`.
- `/hunter-performances` : `POST` et `PUT` refusés à tous (ADR-035, ADR-027) ;
  le service d'`API12` l'écrira.
- Les fixtures `client` et `db_client` fournissent un utilisateur `Admin` par
  `app.dependency_overrides`, pour que les tests existants restent verts sans
  être réécrits un à un.
- `/auth/login` et `/health` restent ouverts.

**Critère de fin**
`test_roles.py` : sans jeton → 401 ; `Reader` en `POST` → 403, en `GET` → 200 ;
`POST /hunter-performances` → 403 ; `Admin` en `POST` → 201. Mutant : retirer le
contrôle du rôle dans `build_crud_router` → le test `Reader` en `POST` tombe.
Suite complète verte, même compte qu'avant plus les nouveaux.
<!-- /FICHE -->

---

<!-- FICHE:API3 -->
## API3 [ ] — Exiger une clé d'API par programme

**Dépend de** : `API1`.
**Fichiers** : un nouveau `API/src/app/utils/api_keys.py`, `API/src/app/routes/crud_router.py`, `API/src/app/routes/auth_router.py`, `docker/.env.exemple`, `API/tests/conftest.py`, un nouveau `API/tests/test_api_keys.py`.

**Prompt**
Code ADR-028, points 4 à 6 : **une clé par programme**, en plus du jeton.
- Chaque programme a sa variable : `API_KEY_<NOM>` (ex. `API_KEY_FRONT`). Au
  démarrage, l'API lit toutes les variables qui commencent par `API_KEY_`.
- L'en-tête `X-API-Key` est exigé sur toutes les routes, `/auth/login` compris ;
  `/health` reste ouvert. Clé absente ou inconnue : **401**. Comparaison à temps
  constant (`hmac.compare_digest`).
- Le nom du programme appelant est connu de la requête (pour les logs).
- ⚠️ Chaque `API_KEY_<NOM>` s'ajoute à `docker-compose.yml` : **arrête-toi et
  demande le oui**. Les clés se génèrent par `openssl rand -hex 32`, jamais dans git.
- Les fixtures de test posent une clé de test par `monkeypatch`.

**Critère de fin**
`test_api_keys.py` : sans clé → 401 ; clé inconnue → 401 ; bonne clé et bon
jeton → 200 ; bonne clé sans jeton → 401. Mutant : accepter toute clé non vide
→ le test « clé inconnue » tombe. Suite complète verte, compte brut.
<!-- /FICHE -->

---

<!-- FICHE:API4 -->
## API4 [ ] — Contrôler les entrées sur une seule ligne

**Dépend de** : rien.
**Fichiers** : `API/requirements.txt`, `API/src/app/models/user_model.py`, `API/src/app/models/estate_model.py`, `API/src/app/models/hunter_rate_parameters_model.py`, `API/src/app/models/payment_model.py`, `md/adr/adr-033-tracabilite-du-calcul.md`, `md/adr/adr-034-parametres-remuneration-table-datee.md`, un nouveau `API/tests/test_entrees.py`.

**Prompt**
Des contrôles Pydantic, qui ne lisent qu'une ligne : un refus rend **422**.
- **P2** : `email` en `EmailStr` dans `UserCreate` et `UserUpdate`
  (`email-validator` à ajouter).
- **P16** : à la saisie d'un bien, chambres ≤ pièces. Les 251 biens repris
  restent tels quels : seuls `POST` et `PUT` contrôlent.
- **P29** : une version des réglages du taux est cohérente — la somme des 5
  poids vaut 1, `rate_floor` ≤ `rate_ceiling`, paliers bien formés (bornes
  croissantes, dernière ouverte). ADR-034, Décision 3 reste : pas de `CHECK`.
- **P32** : `calculation_details` a un modèle Pydantic — les 5 notes et les 4
  entrées du calcul d'ADR-033 ; noms de clés fixés ici et recopiés dans l'ADR.

**Critère de fin**
`test_entrees.py` : un cas refusé (422) et un cas accepté par règle, soit au
moins 8 tests. Mutant : retirer le contrôle des poids → le test « somme des
poids ≠ 1 » tombe. Suite complète verte, compte brut.
<!-- /FICHE -->

---

<!-- FICHE:API5 -->
## API5 [ ] — Figer les versions et l'ordre du paiement

**Dépend de** : rien.
**Fichiers** : `API/src/app/services/parameters_fees_service.py`, `API/src/app/services/commission_scale_service.py`, `API/src/app/services/hunter_rate_parameters_service.py`, `API/src/app/services/payment_service.py`, `API/src/app/services/remuneration.py`, un nouveau `API/tests/integration/test_versions_paiement.py`.

**Prompt**
- **ADR-030, ADR-034** : une grille d'honoraires, une ligne de barème ou une
  version des réglages **déjà citée** par une vente ou un paiement ne se
  modifie plus : `PUT` → 409. Non citée : modifiable.
- **ADR-038** : le statut d'un paiement n'avance que dans l'ordre
  `'announced'` → `'scheduled'` → `'paid'` ; `'refused'` reste possible depuis
  `'announced'`. Un retour en arrière → 409. Compare à la valeur en base.
- **P33** : à l'écriture d'un paiement, recalcule le taux final depuis les taux
  stockés et la version des réglages (`taux_final` de `remuneration.py`) ;
  s'il diffère → 409. Complète ADR-033, Décision 6.

**Critère de fin**
`test_versions_paiement.py` : grille citée modifiée → 409, non citée → 200 ;
`'paid'` → `'announced'` → 409 ; taux final faux → 409. Mutant : retirer le
contrôle « déjà citée » → son test tombe. Suite complète verte, compte brut.
<!-- /FICHE -->

---

<!-- FICHE:API6 -->
## API6 [ ] — Noter l'auteur d'un bien et d'un média

**Dépend de** : `API2`.
**Fichiers** : `API/src/app/routes/estate_router.py`, `API/src/app/services/estate_service.py`, `API/src/app/routes/review_media_router.py`, `API/src/app/services/review_media_service.py`, `docker/init-v3/01_create_fil_rouge_immobilier.sql` (lecture), un nouveau `API/tests/integration/test_auteurs.py`.

**Prompt**
- **ADR-047** : `POST /estates` réservé à `Hunter` et `Manager` (403 sinon).
  `id_author` est **rempli par l'API** avec l'utilisateur du jeton ; une valeur
  envoyée par le client est ignorée. Vide reste réservé aux biens importés.
- **ADR-051** : `POST /review-media` réservé au **chasseur auteur de la note**.
  La note est une ligne de `estate_searchrequest` ; trouve son chasseur par grep
  dans `01` (lien `search_request.id_hunter`), et dis le chemin retenu dans un
  commentaire. Un autre compte → 403.
- Ces règles ont besoin de l'utilisateur courant : passe-le du routeur au
  service sans casser les autres tables.

**Critère de fin**
`test_auteurs.py` : `Hunter` crée un bien → `id_author` = son id ; `Client` →
403 ; le chasseur de la note ajoute un média → 201 ; un autre chasseur → 403.
Mutant : remplir `id_author` avec la valeur reçue → son test tombe. Suite
complète verte, compte brut.
<!-- /FICHE -->

---

<!-- FICHE:API7 -->
## API7 [ ] — Contrôler propositions et visites

**Dépend de** : rien.
**Fichiers** : `API/src/app/services/estate_proposed_service.py`, `API/src/app/services/visit_service.py`, `md/adr/adr-053-trous-de-la-base-decisions.md` (règle des visites), un nouveau `API/tests/integration/test_propositions_visites.py`.

**Prompt**
Règles entre tables, dans les services (ADR-040) ; un refus → 409.
- **P19** : un bien proposé doit être dans la sélection (`estate_searchrequest`)
  de la demande du mandat.
- **P20** : on ne propose que sur un mandat `'active'`.
- **P23** : une visite `visitor_type = 'client'` porte sur un bien **proposé
  sur ce mandat** ; les visites `'hunter'` ne sont pas contrôlées.
- **P25** : la date d'une visite tombe **dans les dates du mandat** ; le statut
  n'est pas regardé.
- **ADR-044** : une visite avant la signature du mandat est refusée (TODO du
  schéma, `01`, bloc `visit`).

**Critère de fin**
`test_propositions_visites.py` : un refus et un accepté par règle (au moins 10
tests). Mutant : retirer le contrôle P23 → le test « visite client sur un bien
non proposé » tombe. Suite complète verte, compte brut.
<!-- /FICHE -->

---

<!-- FICHE:API8 -->
## API8 [ ] — Contrôler signature et vente

**Dépend de** : rien.
**Fichiers** : `API/src/app/services/mandate_service.py`, `API/src/app/services/sale_service.py`, `docker/init-v3/01_create_fil_rouge_immobilier.sql` (lecture des TODO du bloc `sale`), un nouveau `API/tests/integration/test_signature_vente.py`.

**Prompt**
- **ADR-044** : quand un mandat reçoit sa `signature_date`, la demande liée
  passe à `'launched'`, dans la même transaction.
- Une vente sur un mandat **non signé** → 409 (TODO du schéma, bloc `sale`).
- **P27** : pour `sale_origin = 'hunter'`, exiger une offre acceptée sur ce bien
  et ce mandat (rapport de vérification : `'accepted'`, pas `'signed'` ; lis la
  valeur exacte dans `01`). `client_alone` n'est pas contrôlé.
- **P28** : à la création d'une vente, le mandat passe à `'completed'` dans la
  même transaction.
- **ADR-030** : `id_parameters_fees` désigne la grille **en vigueur à la date
  de l'acte** (TODO du schéma) ; sinon 409.

**Critère de fin**
`test_signature_vente.py` : signature → demande `'launched'` ; vente sur
mandat non signé → 409 ; vente `'hunter'` sans offre → 409 ; vente → mandat
`'completed'` ; mauvaise grille → 409. Mutant : retirer le passage à
`'completed'` → son test tombe. Suite complète verte, compte brut.
<!-- /FICHE -->

---

<!-- FICHE:API9 -->
## API9 [ ] — Enregistrer une demande avant le compte

**Dépend de** : `API1`.
**Fichiers** : un nouveau `API/src/app/routes/signup_router.py`, un nouveau `API/src/app/services/signup_service.py`, `API/src/app/main.py`, `API/src/app/utils/security.py`, `md/journal/problemes-a-regler.md` (§ P5), un nouveau `API/tests/integration/test_demande_avant_compte.py`.

**Prompt**
Code la solution recommandée de **P5**, sans changer le schéma.
- Une route `POST /search-requests/submit` reçoit le formulaire : email, nom,
  téléphone, adresse complète (P3), et la demande.
- En **une transaction** : un `user` `is_activated = FALSE` avec un mot de
  passe factice qui n'est pas une empreinte Argon2 (comme les comptes repris,
  `verify_password` le refuse), sa fiche `client`, puis la `search_request`.
- Un email déjà connu (sans tenir compte des majuscules, P2) retrouve le
  compte existant au lieu d'en créer un.
- L'activation passe par la route existante `PUT /users/{id}` (mot de passe et
  `is_activated`) : aucun nouveau mécanisme d'envoi d'email.
- Une erreur au milieu : rien n'est écrit.

**Critère de fin**
`test_demande_avant_compte.py` : formulaire neuf → 3 lignes créées, compte
inactif, connexion refusée ; même email en majuscules → pas de second compte ;
adresse manquante → 422 et 0 ligne écrite. Mutant : sortir la création de la
transaction → le test « 0 ligne écrite » tombe. Suite complète verte.
<!-- /FICHE -->

---

<!-- FICHE:API10 -->
## API10 [ ] — Anonymiser un compte et fermer DELETE

**Dépend de** : `API2`.
**Fichiers** : `API/src/app/routes/crud_router.py`, `API/src/app/routes/user_router.py`, un nouveau `API/src/app/services/anonymization_service.py`, `md/adr/adr-049-effacement-compte-desactiver-anonymiser.md` (Décisions 5 à 10), `API/tests/test_crud_router.py`, un nouveau `API/tests/integration/test_anonymisation.py`.

**Prompt**
Code ADR-049.
- **Plus aucune route `DELETE`** : retire-la de `build_crud_router` ; adapte
  les tests qui l'utilisaient.
- `POST /users/{id}/anonymize`, réservé à `Admin` : désactive le compte, puis
  rend anonyme **tout de suite** ce qu'aucune loi n'oblige à garder (tableau
  de la Décision 7 : email `anonyme-<id>@exemple.invalid`, mot de passe non
  Argon2, téléphone `+33000000000`, adresse `'anonyme'`, `'00000'`,
  `'anonyme'`, `'FR'`, naissance et situation vidées, textes écrits vidés).
- Prénom et nom attendent la fin du plus long délai : **10 ans** après la fin
  du dernier mandat de la chaîne, ou après le paiement (Décision 5). Aucun
  délai en cours : « Anonyme » tout de suite.
- La même route, rappelée plus tard, finit le travail. Pas de tâche planifiée.

**Critère de fin**
`test_anonymisation.py` : client sans mandat → tout anonyme ; chasseur payé
il y a 2 ans → nom gardé, reste anonyme ; `DELETE /clients/1` → 405 ; non
`Admin` → 403. Mutant : anonymiser le nom sans regarder le délai → son test
tombe. Suite complète verte, compte brut.
<!-- /FICHE -->

---

<!-- FICHE:API11 -->
## API11 [ ] — Noter les mandats par le taux de transformation

**Dépend de** : rien.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql`, `docker/init-v3/05_parametres.sql`, une nouvelle migration `docker/migrations/v2-vers-v3/39_taux-reussite-mandats.sql`, `API/src/app/models/hunter_rate_parameters_model.py`, `API/src/app/services/parametrage_service.py`, `API/src/app/services/remuneration.py`, `API/tests/test_remuneration.py`, `md/adr/adr-048-criteres-de-performance.md`.

**Prompt**
Code ADR-048, Décision 5 (choisi le 12/10/2026 : nom et valeur).
- Ajoute à `hunter_rate_parameters` la colonne
  `mandate_success_rate_for_max_score` : le taux de réussite des mandats
  (ventes ÷ mandats) qui donne la **note max**. Nom choisi le 12/10/2026 pour
  être compris sans l'ADR ; un `COMMENT ON COLUMN` le dit en une phrase.
  Valeur de départ : **1.0000** (100 %). Dans `01`, `05` et la migration 39 ;
  joue la migration sur `fil_rouge_immobilier` et recrée `fil_rouge_test`.
- Le critère « mandats signés » devient `min(100 ; 100 × T ÷ réglage)`, avec
  `T = ventes ÷ mandats`. Zéro mandat : demande-le avant de choisir.
- `points_per_mandate` reste en base, n'est plus lu ; ne le retire pas.
- Les cas qui utilisaient `mandats × 10` sont refaits, ou gardés et nommés
  « cas du sujet » (ADR-048, Conséquences).

**Critère de fin**
`test_remuneration.py` : 4 ventes pour 5 mandats, réglage à 100 % → 80
points ; réglage à 50 % → 100 points. Mutant : remettre `mandats × points_per_mandate` → le
test « 80 points » tombe. `\d hunter_rate_parameters` montre la colonne. Suite
complète verte, compte brut.
<!-- /FICHE -->

---

<!-- FICHE:API12 -->
## API12 [ ] — Brancher la rémunération sur la base

**Dépend de** : `API5`, `API8`, `API11`.
**Fichiers** : un nouveau `API/src/app/services/payment_calculation_service.py`, `API/src/app/routes/sale_router.py`, `API/src/app/services/parametrage_service.py`, `API/src/app/services/remuneration.py` (lecture), `md/adr/adr-035-note-recalculee-a-chaque-vente.md`, `md/adr/adr-048-criteres-de-performance.md`, un nouveau `API/tests/integration/test_calcul_paiement.py`.

**Prompt**
Code ADR-035 et ADR-048 : le calcul lit la base.
- `POST /sales/{id}/payment` : compte en base, sur la fenêtre `window_months`,
  les **visites `'client'`**, les ventes et les mandats du chasseur (ADR-048,
  règle des visites d'ADR-053) ; charge le `Parametrage` à la date de l'acte
  (`ParametrageService.charger`) ; appelle `calculer_remuneration`.
- Crée le paiement `'announced'` avec `calculation_details` au format d'`API4`.
  Une vente qui a déjà son paiement → 409.
- **ADR-035** : la note `'payment'` du chasseur ne s'écrit qu'au passage du
  paiement à `'paid'`, pas avant.
- Le code du sujet ne change pas : seuls les comptages sont nouveaux.

**Critère de fin**
`test_calcul_paiement.py` : une vente posée en base → paiement créé, montant
égal à celui de `calculer_remuneration` sur les mêmes nombres ; second appel →
409 ; note `'payment'` absente tant que non payé. Mutant : compter aussi les
visites `'hunter'` → le test du montant tombe. Suite complète verte.
<!-- /FICHE -->

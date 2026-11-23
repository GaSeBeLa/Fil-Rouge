# Audit des commentaires de Fil-Rouge-API — 2026-11-23

Demandé par Gabriel sur Discord (09 h 17) : « vérifier si tous les commentaires
qui existent dans les fichiers de code sont à jour et cohérents avec le code ».

## Méthode

- 287 fichiers suivis par git (.py, .sql, .sh, .yml), environ 46 000 lignes, au commit `b0d6143`.
- 6 relectures en parallèle, en lecture seule : API services et utils, API modèles,
  repositories et routes, API tests, Airflow et CI et compose, SQL `docker/init*`,
  SQL `docker/migrations`.
- Chaque commentaire est comparé au code, au SQL de `init-v3`, et aux ADR de `Fil-Rouge/decisions/`.
- Un échantillon de chaque rapport a été revérifié à la main (grep, lecture) : tout ce qui a été
  contrôlé est confirmé. Les numéros de ligne peuvent être décalés d'une ou deux lignes.
- « sûr » : la preuve est dans le code ou l'ADR. « probable » : à confirmer d'un coup d'œil.

## Bilan

- Environ **90 commentaires** faux ou périmés.
- **2 constats sur le code lui-même** (pas des commentaires), en fin de page.
- Aucune mention de Confluence comme source à lire dans le code Python ; quelques-unes dans le SQL.
- Aucun en-tête « brouillon » ou « rédigé par l'IA » dans le code.

Les familles d'erreurs qui reviennent :

- des **comptes figés** : 21 tables au lieu de 22, 17 critères au lieu de 18, 24 comptes migrés au lieu de 25, 4 rôles au lieu de 3 ;
- des **ADR « à écrire »** qui existent depuis : ADR-025, ADR-029, ADR-031, ADR-050 ;
- des **numéros d'ADR faux** : ADR-018 au lieu d'ADR-023 ;
- des **TODO déjà faits** dans l'API : visite avant signature, vente sous mandat signé ;
- des **chemins anciens** : `routers/` au lieu de `routes/`, `md/adr/` au lieu de `decisions/`, `API2/` au lieu de `API/` ;
- le **vocabulaire d'avant le chantier PRF** : « son compte » pour `id_client` qui est la fiche, « rôle 1 = Client », le rôle lu dans la table `role` ;
- des **numéros de ligne** cités dans `remuneration.py` ou dans les ADR, qui ont bougé.

## 1. API — services, utils, conf, scripts

Sûrs :

- `API/src/app/utils/security.py:285` — « 24 comptes migrés » ; il y en a 25 (`init-v3/02`, 25 `MIGRATED_PLACEHOLDER`).
- `API/src/app/services/mandate_service.py:17-18` — « `id_client` reste son compte » ; c'est sa fiche client (`client.id`, comparé à `viewer.profile_id` l. 71). Phrase gardée par le commit `abbf38d` du 20/11.
- `API/src/app/services/search_request_service.py:114` — « `id_hunter` reste son compte » ; c'est sa fiche (`hunter.id`).
- `API/src/app/services/remuneration.py:35-37` — le branchement sur `commission_scale`, `parameters_fees` et `payment` « pas encore écrit » ; il est fait (`parametrage_service.py`, `payment_calculation_service.py`).
- `API/src/app/services/payment_service.py:7` — « Deux contrôles » ; le texte en liste trois.
- `API/src/app/utils/exceptions.py:11-12`, `services/__init__.py:5`, `services/base_service.py:12` — dossier `routers/` ; il s'appelle `routes/`.
- `API/src/app/conf/database.py:15` — le `Depends(get_session)` « dans main.py » ; il est dans les routeurs (`routes/auth_router.py`, `utils/current_user.py`).
- `API/src/app/scripts/seed_demo.py:289` — message d'arrêt « init-v3/02 » pour les biens ; ils viennent de `init-v3/03`.

Probables :

- `API/src/app/scripts/seed_volume.py:12` — cite ADR-046 (données reprises), qui porte sur la migration, pas le seed : retirer.
- `API/src/app/scripts/seed_volume.py:18` et `seed_demo.py:7` — « aucun test ne l'appelle » ; des tests existent (`test_seed_volume.py`, `integration/test_seed_demo.py`) : « aucun test ne dépend de ses données ».
- `API/src/app/scripts/seed_demo.py:26` — « DEM2 et DEM3 y ajoutent les leurs », au futur ; c'est fait.
- `API/src/app/conf/database.py:283-284` — valeurs par défaut « celles de docker-compose.yml » ; le compose lit `docker/.env`.
- `API/src/app/services/payment_calculation_service.py:35` et `:357` — « ADR-048, point 8 » ; ce point parle de la note hors d'une vente : citer ADR-035.
- `API/src/app/services/__init__.py:3-5` — « viendraient » des règles comme hacher le mot de passe ; c'est fait (`UserService.create`), et « une fiche par compte » est tenu par un trigger.

## 2. API — modèles, repositories, routes

Sûrs :

- `API/src/app/models/__init__.py:2-3` — « 21 tables, une classe par fichier » ; 22 tables, et `EstatePriceHistory` est dans `estate_model.py`.
- `API/src/app/models/estate_model.py:7-11` — un prix à virgule « pas encore refusé », test xfail `test_estate_price_with_cents_is_refused` ; refusé en 422 par `_validated`, test `test_estate_price_with_cents_returns_422` sans xfail.
- `API/src/app/models/user_model.py:72-73` — `min_length=12` « proposition du tuto, à confirmer en réunion » ; acté par ADR-026 (remis en vigueur le 08/10) et ADR-028.
- `API/src/app/models/role_model.py:20-21` — CHECK « Admin, Client, Hunter, Manager, Reader » ; la base n'a que Client, Hunter, Manager (`init-v3/01:169`).
- `API/src/app/models/hunter_rate_parameters_model.py:13` — `remuneration.py, l. 92-116` ; les classes ont bougé : citer leurs noms.
- `API/src/app/repositories/__init__.py:3-4` — « seule cette couche touche la Session » ; `activation_service.py` et les fichiers `*_rows.py` le font aussi. Corriger la phrase ; déplacer ces appels serait un refacto, à décider.
- `API/src/app/routes/crud_router.py:38` — `md/adr/adr-027-annexe-matrice-detaillee.md` ; c'est `decisions/` qui fait foi.

Probables :

- `API/src/app/models/__init__.py:19-23` — validation Python « pas faite ici » ; elle existe (`input_check.py`, `_validated`).
- `API/src/app/repositories/base_repository.py:11`, `routes/crud_router.py:11` — `routers/` au lieu de `routes/`.
- `API/src/app/routes/__init__.py:2-3` — « une APIRouter par table » ; 4 routeurs sont à part (auth, signup, suggestion, recherche).
- `API/src/app/models/client_model.py:35` — `'non renseigne'` sans accent ; la base a `'non renseigné'`.
- `API/src/app/models/mandate_model.py:19-20` — renvoie à une remarque de `criteria_model.py` qui n'existe plus.

## 3. API — tests

Sûrs :

- `API/tests/conftest.py:11-14` — « une seule fixture : client » ; il y en a six.
- `API/tests/conftest.py:32-36` — « pas encore de fixture de base de test » ; elle est dans `tests/integration/conftest.py`.
- `API/tests/integration/conftest.py:261`, `test_auth.py:22`, `test_droits_par_role.py:430` — « rôle 1 = Client » ; depuis PRF, POST /users crée un compte sans fiche ni rôle.
- `API/tests/integration/test_roles_db.py:36` — rôle « lu dans la table role » ; il vient de `system_role` ou de la fiche.
- `API/tests/integration/test_isolation.py:7-10` — « trois choses » pour quatre puces, et « 4 rôles » pour 3.
- `API/tests/integration/test_users_db.py:11-12` — « ON DELETE RESTRICT donne 409 » ; DELETE rend 405 (ADR-049).
- `API/tests/test_security.py:143` — « a-redefinir » ; le seed met `$2b$12$MIGRATED_PLACEHOLDER_MUST_RESET`.
- `API/tests/test_user_models.py:271-273` — `min_length=12` « pas encore acté » ; acté par ADR-026.
- `API/tests/test_health.py:10` — « depuis le dossier API2/ » ; c'est `API/`.

Probables :

- `API/tests/integration/test_droits_par_role.py:240` — `md/adr/adr-027-…` au lieu de `decisions/`.
- `API/tests/test_user_service.py:133` — « 24 comptes migrés » ; 25.
- `API/tests/integration/test_constraints_db.py:1074` — « comme les 18 autres » ; 21 routeurs CRUD.
- `API/tests/test_api_keys.py:4-6, 25` — la fausse session « rend son rôle » lu dans `role` ; le rôle ne s'y lit plus.
- `API/tests/integration/conftest.py:155` — « scripts 01 + 02 » ; `create_test_db.sh` joue 01, 02 et 04.
- `API/tests/integration/test_seed_demo.py:2` — « DEM1 et DEM2 » ; DEM3 aussi.
- `API/tests/test_base_repository.py:8` — « ce sera le rôle des tests d'intégration » ; ils existent.

Vérifié juste : les 7 xfail ont une raison toujours exacte (ADR-048, taux à la place de mandats × 10).

## 4. Airflow, CI, compose, scripts

Sûrs :

- `docker/create_test_db.sh:10` — « 21 tables » ; 22.
- `airflow/tests/test_annonces_load.py:4` — « les deux tables » ; le fixture en crée trois.
- `docker/docker-compose.yml:250-253` — `es-setup` ne cite que kibana_system et airflow_indexer ; il crée aussi `api_search` et `logstash_internal`.
- `airflow/README.md:25-28` et `API/README.md:229` — la connexion `elasticsearch_default` manque à la liste.

Probables :

- `airflow/README.md:10-16` — `tools/` manque à l'arborescence.
- `airflow/src/config.py:13-14` — « les connexions … leurs noms sont ici » ; `elasticsearch_default` est dans le DAG.
- `airflow/src/annonces/clean.py:88` — « (CLAUDE.md, règle 4) » ; ce dépôt n'a pas de CLAUDE.md, et celui de Fil-Rouge a deux « 4. ».

Vérifié juste : `docker-compose.yml` lignes 66 et 68, corrigées le 23/11.

## 5. SQL de création — `docker/init-v3`, `init-v2`, `init`

⚠️ `init-v3/01_create_fil_rouge_immobilier.sql` est le script du schéma de référence (MPD) : à ne corriger qu'avec l'accord explicite de l'équipe.

⚠️ `docker/init-v2/` est figé, et `docker/init/` n'est plus monté (`CLAUDE.md` de Fil-Rouge, règle 3) : leurs constats sont notés pour mémoire, sans correction proposée.

`init-v3/01_create_fil_rouge_immobilier.sql` :

- `:29` — « À acter en ADR sur Confluence » ; acté : ADR-025, ADR-029. Même texte dans `init-v2/01:24`.
- `:564` — ADR-018 « figer la date » ; c'est ADR-023 (ADR-018 = performance énergétique). Même erreur dans `init-v2/01:411`.
- `:577` — « ADR à écrire » ; c'est ADR-050.
- `:145`, `:425` — « un ADR remplace ADR-009 » ; c'est ADR-031.
- `:974-978` — TODO visite « règle et test restent à écrire » ; fait (`visit_service.py:64`, ADR-044).
- `:1023-1024` — TODO vente, grille de l'acte « pas vérifiée » ; vérifiée (`sale_service.py`, ADR-030).
- `:1030-1036` — TODO vente « mandat signé » à écrire ; fait. Reste seulement la date de vente hors validité du mandat.
- `:76`, `:1052`, `:1082`, `:1100`, `:1120` — numéros de ligne de `remuneration.py` qui ont bougé : citer les noms de fonction.
- `:1429` — « 278 colonnes » ; 283 comptées dans le texte du script (5 colonnes ajoutées depuis).
- `:1312` — « ADR-042 l. 122 » ; l'ADR a 118 lignes (probable).
- `:854` et `08_olap.sql:21` — « (règle 4) » sans dire laquelle (probable).

`init-v3/02_migration.sql` :

- `:15`, `:52` — « 17 lignes », « 17 critères » ; 18 (la ligne 59 du même fichier dit 18).
- `:147-149` — « le tout-ou-rien les exige » ; remplacé par NOT NULL (ADR-053 P3).
- `:202-203` — `parse_typology()` « ci-dessus » ; cette fonction n'existe nulle part. Même erreur dans `init-v2/02:191` et `init/02:114`.
- `:87-88` — « user = id, email, password, created_at » ; il y a aussi `is_activated` et `system_role` (probable).
- `:4` — « 21 tables » ; 22 (probable, phrase datée).

`init-v3/README.md` :

- `:4-6` — « 18 tables … une 19e » ; 22.
- `:8-9` — `docker/init/` en place « tant que le groupe n'a pas validé le basculement » ; le compose monte `init-v3` depuis le 07/10.
- `:104` — les trois TODO « restent à écrire » ; voir plus haut.
- `:310` — « 4 lignes » dans `role` ; 3 (la ligne 315 le dit).
- `:320-323` — « 17 lignes », « 240.0 à 700.0 » ; 18 lignes, minimum 220.
- `:399-402` — « le groupe garde le tout-ou-rien » ; remplacé par NOT NULL (probable).
- `:460-478` — tableau des comptes : `role` 4 → 3 ; demandes, critères, mandats 17 → 18 ; budget minimum 240 000 → 220 000 €.
- `:505` — « les quatre scripts (01 à 04) » ; il y en a 8.
- `:520`, `:605` — « acter en ADR le lien chasseur → manager » ; fait (ADR-025, ADR-029).
- `:532` — « ADR-024 au statut proposé » ; accepté le 15/10, et pointer vers `decisions/`.
- `:597` — TODO U01/U04 « de l'en-tête du 01 » ; il est dans la table payment (probable).
- `:629`, `:635-636` — FK vers `real_estate_manager(id_user)` ; depuis PRF, vers `real_estate_manager(id)`.

`init-v2/README.md` (ancienne version, seulement les liens cassés) :

- `:325` — `md/adr-024-motif-refus-remuneration.md` n'existe plus.
- `:411` — `md/securite-mots-de-passe-et-droits.md` n'existe plus.

## 6. SQL de migration — `docker/migrations`

Sûrs :

- `2026-09-21_adr-024_payment_refusal.sql:29` — renvoie à un brouillon de `md/adr/` ; pointer vers `decisions/adr-024-refus-remuneration-motif-trace.md`.
- `2026-09-21_adr-024_payment_refusal.sql:12, 17`, `2026-09-22_hunter_manager.sql:20`, `2026-09-22_role_admin.sql:21` — « seul init-v2/ est monté » ; c'est `init-v3/` depuis octobre.
- `2026-09-22_hunter_manager.sql:9` — « À acter en ADR » ; c'est ADR-025.
- `v2-vers-v3/09_biens.sql:29` — la commande d'exemple a perdu ses retours à la ligne : copiée telle quelle, elle ne marche pas.
- `v2-vers-v3/16_mandat-renouvellement-sans-avenant.sql:9-10` — « ADR à écrire » ; c'est ADR-050.
- `v2-vers-v3/36_une-note-initiale-par-chasseur.sql:7` — « ADR-042 l. 122 » ; l'ADR a 118 lignes.
- `v2-vers-v3/44_parametres-de-depart.sql:6` — « 06 crée les trois tables » ; il en crée une et modifie les deux autres.

Probables :

- `2026-09-22_role_admin.sql:13-35` — « pour une base déjà créée » ; sur une base v3, l'INSERT Admin serait refusé : préciser « base v2 seulement ».
- `v2-vers-v3/23_client-adresse-obligatoire.sql:28` — « les deux contraintes (07) » ; une vient de 07, l'autre de `init-v2/01`.
- `v2-vers-v3/10_reprise-mandats.sql:94` — « sous mandat signé » ; le code teste seulement qu'un mandat existe.
- `v2-vers-v3/06_parametres.sql:117` — « même définition que init-v3/01 » ; plus vrai depuis les migrations 14 et 39 : ajouter « à la date du LOT6 ».

## Constats sur le code (pas des commentaires)

1. **Import Airflow : un contact entièrement sale casse tout l'import** (probable, lu, pas exécuté).
   - `airflow/src/annonces/clean.py`, `clean_contact` : si une annonce a au moins un champ de contact, mais tous mal formés (exemple : seul un email invalide), la fonction rend un contact dont les 4 champs valent `None`, au lieu de `None`.
   - `load.py`, `_load_contact`, l'écrit quand même : le CHECK `ck_estate_contact_not_empty` (`init-v3/01:841`) le refuse, et toute la transaction de l'import échoue.
   - La docstring promet le contraire : « un champ sale est vidé seul : le bien et le reste du contact sont gardés ». Aucun test ne couvre ce cas.
   - Correctif proposé, en TDD : un test rouge (un contact avec seulement un email invalide), puis `clean_contact` rend `None` quand tous les champs nettoyés sont vides.
2. **Message d'erreur faux** : `API/src/app/services/estate_search_request_service.py:38` dit « Média introuvable » pour une sélection de bien introuvable (copier-coller probable de `review_media_service.py`).

## Hors du code, repéré en passant

- `Fil-Rouge/decisions/` a deux fichiers ADR-024 : `adr-024-refus-remuneration-motif-trace.md` et `adr-024-annule-modifications-en-detail.md`.
- `Fil-Rouge/decisions/adr-055-seed-de-demo.md:5` dit encore « Publié sur Confluence ».

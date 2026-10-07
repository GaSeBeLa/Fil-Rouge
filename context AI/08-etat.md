> **QUAND LIRE** : on reprend après une longue interruption, on choisit le
> prochain chantier, ou on doute d'une décision passée. Les cinq lignes de
> `CLAUDE.md` suffisent dans la plupart des cas — ouvrir ceci seulement quand
> elles ne suffisent pas.

# État du projet — daté

## Où on en est

*(au 2026-09-21 — remplace l'état du 2026-09-07 ; l'historique est au journal)*

- **Base de données** — schéma `fil_rouge_immobilier` (**18 tables**, montants
  en **euros**) dans `docker/init-v3/`, monté par `docker/docker-compose.yml`
  depuis le 2026-10-07 (chantier LOT). `docker/init-v2/`, monté du 2026-09-21
  au 2026-10-07, est **figé**, gardé pour le banc. Chaîne complète `01` → `02`
  → `03` vérifiée sur PostgreSQL 16 : 0 erreur, 2 556 biens, 1 976 photos,
  18 clients. Les choix, les hypothèses et les 6 points ouverts sont dans
  `docker/init-v3/README.md`. `docker/init/` (12 tables, K€) reste intact mais
  n'est plus monté.
  *(au 2026-10-05)* Prix, budgets, bornes du barème et part fixe en
  `INTEGER` ; honoraires et paiement en `NUMERIC(12,2)` ; tranches du barème
  bornées `'[]'` (Q-REM-01).
- **API** — FastAPI + SQLModel, CRUD en trois couches (`routes/`, `services/`,
  `repositories/`), pas de PATCH, choix assumé. Alignée sur les **18 tables**
  depuis le 2026-09-21 : 18 modèles, 224 champs pour 224 colonnes, 18
  ressources REST, 91 opérations. Vérifié en exécution : `GET` sur les 18
  ressources, 18/18 en `200`. *(au 2026-10-05)* Prix en `int`, honoraires et
  paiement en `Decimal` ; le routeur commun revalide l'entrée du `POST` et du
  `PUT` (`422` avant la base).
- **Tests** *(au 2026-10-05)* — **123 tests**, `123 passed`, lancés dans le
  conteneur `api` : 99 unitaires sans PostgreSQL (dont les 55 cas de
  rémunération), 24 d'intégration sur la base de test isolée
  `fil_rouge_test` (`docker/create_test_db.sh`).
- **Calcul de rémunération** *(au 2026-10-02)* — `services/remuneration.py`,
  code de référence du sujet recopié tel quel ; fonction pure, **pas encore
  branchée sur la base**.
- **Métier** — les règles (mandat, rémunération, barème, performance) existent
  en Gherkin dans `user-stories/` et en notes, mais **aucune n'est
  implémentée**. Le schéma non plus ne les porte pas : `U02` (exclusivité du
  mandat) et `U05` (durée de 6 mois) sont écrits mais commentés dans le `01`.
- **Données** — `normalised/` porte `normalised.py`, les annonces normalisées,
  `populate_estate.sql` et `rapport_anomalies.txt`.
- **Livrables** — `livrables/2-modelisation/` porte trois rapports du chantier
  `C` ; les trois autres dossiers sont vides (`.gitkeep`).

## La TODO ordonnée — les chantiers possibles

C'est d'ici que `/vlp:chantier` tire ses propositions. Un chantier par entrée,
ordonné par ce qui débloque le reste.

| # | Chantier | Ce qu'il apporte | Coût estimé | Dépend de |
|---|---|---|---|---|
| 1 | Lot de migration de la base | **un seul lot, par thème** (Q11, Q12) : les changements décidés au registre, 4e série comprise (droits par rôle, reprise des anciens mandats, auteur d'un bien, CHECK 20-60 %, Eircode…). Pour chacun : schéma `01`, modèle, migration, tests, README du schéma. Ouvert le 2026-10-07 : nouveau dossier `docker/init-v3/`, 12 fiches `LOT` ; le rôle en lecture seule attend Jeff (LOT12) | 💡 ~8 à 10 fiches | rien |
| 2 | API : auth, RGPD et règles métier | les **outils d'auth** côté back (connexion, token, rôles, droits, Argon2), l'**anonymisation** d'un compte, une **clé d'API par programme**, les règles « contrôlées par l'API », et le calcul de rémunération branché sur la base (55 cas déjà verts) ; la **grille de notes** (Q-JEF-05) et la **durée X** (Q-ACC-21), à proposer par le groupe (sortis du lot le 2026-10-07) | 💡 ~5 à 7 fiches | 1 |
| 3 | Seed de démo | des données de démo générées (faker), cohérentes avec le nouveau schéma ; le décor, pas la preuve : les tests restent la preuve | 💡 2-3 fiches | 1 |
| 4 | Les ADR | **une fiche par ADR**, chacune relue (Q15) ; chaque ADR cite ses cartes et ses sources, puis se copie à la main sur Confluence | 💡 ~25 fiches | 1..3 |
| 5 | Doc d'équipe | matrice des droits, RACI, registre RGPD, rapport de tests | 💡 3-4 fiches | 1..2 |
| 6 | Livrable 2 — modélisation (MCD/MLD) | reconstruit le modèle depuis le schéma réparé, pour `livrables/2-modelisation/` | 3–4 fiches | 1 |
| 7 | Livrable 1 — audit des données | rapport de normalisation à partir de `normalised/rapport_anomalies.txt` | 3–4 fiches | rien |
| 8 | Livrable 3 — architecture | documente les trois couches et les choix (pas de PATCH, bases génériques, auth côté back) | 2–3 fiches | 2 |
| 9 | Déploiement sur le VPS | mettre l'API et la base réparée sur le VPS de l'utilisateur ; hôte, accès et méthode **à demander avant d'agir**, aucun secret dans le dépôt | 🟡 à cadrer | 1..8 |

## Journal des décisions

Une ligne par décision imprévue tranchée en cours de fiche — jamais un résumé
de ce que le code dit déjà.

- **2026-09-07** — le contexte IA (`CLAUDE.md`, `CHANTIER.md`, `context AI/`)
  est versionné : le projet se travaille à plusieurs.
- **2026-09-07** — `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/` est
  déclaré source de vérité en lecture seule ; rien n'y est jamais écrit.
- **2026-09-11** — pour le chantier `C*` seulement,
  `docker/init/01_create_fil_rouge_immobilier.sql` est déclaré **périmé** et mis
  hors jeu : l'autorité passe aux `user-stories/`, puis au MPD. Dérogation
  explicite à la règle 3 de `CLAUDE.md`, demandée par l'utilisateur qui refera
  ce fichier. Le MPD porte 18 tables, le SQL n'en a que 12.
- **2026-09-11** — la vérification `python -m pytest -q` ne tourne pas :
  `sqlmodel` absent du Python 3.14 global, aucun environnement virtuel dans
  `API/`. L'utilisateur tranche : on le signale, on n'installe rien. Les fiches
  `C*` ne touchent aucun code ; leur critère de fin fait foi.
- **2026-09-11** — `C2` : l'annexe des user stories porte une colonne
  « Citation » (texte exact de la ligne source) en plus des trois prévues, et
  laisse toutes les colonnes MPD « à rattacher » faute d'ouvrir l'inventaire
  `C1`. Offre d'achat, facture et rendez-vous n'ont aucune table parmi les 18.
- **2026-09-11** — `C3` : l'annexe des notes relève deux contradictions sans
  les trancher — `X01` (ancienneté et performance : clé du barème ou
  majoration du taux) et `X02` (unité de H : € au centime ou K€) — ainsi que
  l'exemple Bruno, payé au-delà des 6 mois que pose sa propre note. Les trois
  restent à arbitrer en `C5`.
- **2026-09-11** — `C4` : l'offre d'achat est rattachée à `EstateProposed`, la
  note d'avis à `Estate_SearchRequest` ; le rendez-vous reste sans table. Le
  rapport établit que `Client` (`is married` en deux mots) et `Criteria`
  (quatre clauses `ck_client_*` sur des colonnes absentes) ne se créent pas en
  l'état du MPD.
- **2026-09-11** — `C5` : la facture est rattachée à `Payment.status`, le
  montant collecté par le notaire à `Sale.fees_amount` ; les indicateurs de
  performance, sans colonne, sont jugés couverts quand leurs données sources
  existent. Restent à vérifier dans le MPD : l'extension `btree_gist` (exigée
  par deux `EXCLUDE`) et `HunterPerformance.id_payment`, déclaré deux fois.
- **2026-09-11** — **chantier `C` clos** (contraintes du MPD). Livré :
  l'inventaire du MPD, les annexes de règles (51 en user stories, 84 en notes)
  et `livrables/2-modelisation/09-rapport-ecarts-contraintes.md` (sorti de
  `context AI/` le jour même) — 150 verdicts sur 18 tables (84
  couvertes, 49 partielles, 16 absentes, 1 fausse), 133 règles reprises sur
  135. Laissé ouvert : `X01`, `X02` (unité de H), l'exemple Bruno, `U29` et
  `F04` sans table, `pytest` non lancé. Coût : 31 326 311 tokens sur 5
  sessions, comptées au 2026-09-11.

- **2026-09-21** — **`X02` tranché : l'unité monétaire est l'euro**, en
  `NUMERIC(12,2)`. Non par préférence, mais sur trois mesures : 37 des 47
  valeurs des fixtures officielles débordent `NUMERIC(6,1)` ; le barème de
  `10_calcul_remuneration_chasseur.feature` a des bornes à l'euro près
  (`199999` basculait à 35 % au lieu de 30 %) ; l'arrondi au centime exigé par
  la règle est impossible au dixième de K€. La décision `B` (K€) du 2026-09-11
  est réfutée. Preuves dans `docker/init-v2/README.md` §1.
- **2026-09-21** — le schéma **18 tables** est écrit dans `docker/init-v2/`,
  fusion de deux versions (la mienne et celle d'un coéquipier), et remplace
  `docker/init/` dans `docker-compose.yml`. La dérogation du 2026-09-11 — le
  SQL 12 tables déclaré périmé — **est levée** : la règle 3 de `CLAUDE.md`
  redevient pleine, en pointant `init-v2`.
- **2026-09-21** — les prix des 2 556 biens sont repris **un par un** depuis la
  colonne `price_eur` du CSV, et non par multiplication des K€ : la
  multiplication donnait `62 500` au lieu de `62 495`. **2 531 biens sur
  2 556** auraient eu un prix faux, jusqu'à 50 € d'écart.
- **2026-09-21** — la contrainte `ck_client_address_all_or_nothing` rejetait
  les 18 clients de la source (ville connue, adresse nulle). Corrigée en
  implication à sens unique, mais **l'`ALTER` est laissé visible dans le `02`**
  et non glissé dans le `01` : la correction attend une validation du groupe.
- **2026-09-21** — quatre hypothèses de migration assumées et signalées, à
  confirmer : `hire_date` = date de création du compte, `search_request.status`
  = `confirmed`, `commission_rate` non migrée (sens métier ambigu),
  `energetic_score` retirée (elle était `NULL` partout).
- **2026-09-21** — `CHANTIER.md` et `INSTALLER-LE-WORKFLOW.md` sont supprimés :
  la méthode de chantier vit désormais dans le plugin `vlp`, elle n'est plus
  recopiée dans le dépôt. L'entrée du 2026-09-07 qui cite `CHANTIER.md` reste
  telle quelle : c'est un fait daté, pas une consigne. Les deux fichiers
  restent récupérables depuis le commit `2448614`.
- **2026-09-21** — le dépôt suivait **67 fichiers `.pyc`** : sortis du suivi,
  et un `.gitignore` complet posé. Les livrables du chantier `C`, ses annexes
  et les notes métier (`md/`) sont enfin versionnés — ils ne l'étaient pas.
- **2026-09-21** — **l'API est rattrapée sur les 18 tables** (chantier 0 de la
  TODO, clos le jour de son ouverture). 6 modèles créés (`Sale`, `Payment`,
  `CommissionScale`, `HunterPerformance`, `ParametersFees`, `Visit`) et leurs
  trois couches. Mesuré : **224 champs déclarés pour 224 colonnes en base**,
  18/18 tables couvertes, 0 écart.
- **2026-09-21** — 7 des 12 modèles existants étaient **faux**, pas seulement
  incomplets : 19 colonnes manquantes, 7 colonnes inexistantes, et **14 champs
  monétaires typés `float`** sur des colonnes `NUMERIC` — dont `estate.price`.
  Tous passés en `Decimal`. Deux contraintes étaient inversées :
  `criteria.estate_type` est obligatoire et `typology` facultatif, l'inverse
  de ce que le modèle déclarait.
- **2026-09-21** — vérification en exécution, dans un conteneur jetable (rien
  installé sur le poste, conformément à la décision du 2026-09-11) : `GET` sur
  les 18 ressources, **18/18 en `200`**, 91 opérations exposées. `price`
  remonte en `"354712.00"` — le `Decimal` est préservé au centime.
  ⚠️ Cette vérification n'est **pas** un test automatisé : `pytest` ne couvre
  toujours que le health-check. Le chantier 1 reste le premier verrou.

- **2026-09-22** — **chaque chasseur a un manager** (MPD 03 4) :
  `hunter.id_realestatemanager NOT NULL`, FK vers `real_estate_manager(id_user)`.
  Choix du groupe appuyé sur l'exemple ENF-03 du sujet — un exemple de
  rédaction, pas une exigence du client — à acter : brouillon
  `md/adr-025-lien-chasseur-manager.md`. Les 6 chasseurs migrés sont rattachés
  à un **manager placeholder** (user 25), hypothèse documentée au README
  init-v2 §3.6. Mesuré, PostgreSQL 16, base neuve **et** base migrée par
  `docker/migrations/2026-09-22_hunter_manager.sql` (rejouable) : 7 cas
  adverses sur 7, même comportement des deux côtés ; API `GET /hunters` en
  `200` avec la colonne, `POST` sans manager en `409`. Le schéma compte
  désormais **226 colonnes** (le « 224 » n'avait pas suivi l'ADR-024).
- **2026-10-02** — **MinIO ne se télécharge plus** (supprimé de Docker Hub
  le 2026-09-11, `quay.io` exige un compte) : tout `docker compose up -d`
  échoue. Le compose n'est pas modifié ; on lance `docker compose up -d db api`.
  Aucun code n'utilisait MinIO. Remplaçant à choisir en groupe. Détail et
  sources : `md/minio-images-indisponibles-2026-10-02.md`.
- **2026-10-02** — **premiers tests unitaires** : 43 tests ajoutés (6
  fichiers), `44 passed` en 3,75 s dans le conteneur `api`. Hors méthode
  chantier, à la demande de l'utilisateur. Isolation par `unittest.mock` et
  `dependency_overrides`, aucune dépendance ajoutée. Mesuré : `44 passed`
  aussi **avec `db` arrêté** ; un sabotage du hachage dans
  `UserService.create` fait échouer 1 test. Ordre décidé pour la suite :
  unitaires → base de test isolée (chantier 1) → calculette (chantier 2).
- **2026-10-02** — **base de test isolée** (chantier 1, hors méthode fiches) :
  option A retenue — base `fil_rouge_test` dans le même conteneur, rejouant
  `01` + `02` (pas `03`), et chaque test annulé en fin (transaction +
  SAVEPOINT). Écartées : rollback sur la base de dev (dépend de ses données),
  SQLite (ignore `CHECK`, `NUMERIC`, `EXCLUDE`). `docker-compose.yml` non
  modifié. 22 tests d'intégration, `66 passed` au total. Mesuré : comptes des
  deux bases identiques avant/après ; contrainte `estate_price_check`
  retirée → 1 test rouge ; `db` arrêté → `44 passed, 22 skipped`.
- **2026-10-02** — **calculette de rémunération** : option A retenue —
  reprendre le module de référence du sujet plutôt que le réécrire (B,
  écartée : ne pourrait que s'écarter de la référence). Les 8 blocs `python`
  de `REGLES-CALCUL-REMUNERATION.md` §14.2-14.3 sont **extraits par script**,
  pas retapés : `diff` = 24 lignes ajoutées (docstring), 0 retirée. Noms
  laissés en français, comme la source. `10_calcul_remuneration_chasseur.feature`
  copié dans `user-stories/` (`cmp` identique). Le sujet ne fournit PAS le
  fichier de tests (2 exemples en §14.5) : `tests/test_remuneration.py`
  écrit, **55 passed** (6+5+20+8+13+3). Sabotage `ROUND_HALF_UP` →
  `ROUND_DOWN` → 1 test rouge. Non couverts : « un seul chasseur rémunéré »
  et la Règle `@tracabilite` (persistance). Reste : brancher sur la base,
  après arbitrage de `X01`.
- **2026-10-05** — **Q-REM-01 tranchée : prix en euros entiers, bornes du
  barème incluses.** La base excluait la borne haute (`'[)'`), le code
  l'incluait (`prix <= montant_max`) : un prix à 199 999,50 € tombait hors
  barème. Décision du groupe : prix, budgets, bornes du barème et part fixe
  en `INTEGER`, `EXCLUDE` du barème en `'[]'` ; honoraires et paiement restent
  `NUMERIC(12,2)` (le sujet arrondit au centime, feature 10 l. 253). Écartés :
  adaptateur `amount_max − 0,01` à la lecture, et bornes à 199 999,99.
  Mesuré : `price_eur` = 2 556 prix, 0 avec centimes ; dans une base
  temporaire, `01` → `02` → `03` sans erreur, chaque prix limite dans
  exactement une tranche, chevauchement refusé. Commits `c896e39`, `abbc84e`.
  Registre : `md/questions-a-trancher-2026-10-02.md`.
- **2026-10-05** — **le routeur commun valide l'entrée** (Q-INF-06). Mesuré :
  un modèle de table SQLModel ne valide pas ce que FastAPI lui passe —
  `199999.5` était arrondi en silence à `200000` (tranche du dessus),
  `"199999.50"` plantait (`DataError`), un champ manquant finissait en `409`.
  `_validated` (`crud_router.py`) revalide avec `model_validate` : `422`
  avant la base, `loc` préfixé par `body`. Contre-épreuve : sans elle, 3
  tests rouges. `123 passed`. pyright : aucune erreur de plus. Commits
  `d3c128c` (modèles en `int`), `fea3c9f` (validation). ⚠️ Toute l'équipe
  doit faire `docker compose down -v`, puis `bash docker/create_test_db.sh`.
- **2026-10-07** — **`CHANTIER.md` est remis à la racine** (Q13, Q15 : le
  kit `vlp` mène le lot de migration, l'API, puis les ADR). La suppression du
  2026-09-21 reposait sur un malentendu : la méthode vit dans le plugin, mais
  le projet garde son `CHANTIER.md` — sans lui, la carte du kit répond
  `AUCUN_PROJET`. Repris de `2448614` et mis à jour (schéma `init-v2`, euros,
  `docker-compose.yml`). Mesuré : `vlp.py renvois` → `CHANTIER.md 48/50`,
  12 renvois, 0 absent.
- **2026-10-07** — **un seul statut `'lost'`** pour la vente perdue, hors
  agence (Q-REM-02) comme par un collègue (Q-REM-14) : le registre ne donnait
  qu'un exemple et laissait « un ou deux ? » ouvert (ligne 134). Tranché à
  LOT3 ; le cas « collègue » se déduit de l'autre mandat vendu.
- **2026-10-07** — **trigger d'exclusivité : le couple parent-enfant exclu dans
  les deux sens**, et un mandat `'canceled'` ignoré. Q-MAN-02 n'excluait que le
  parent : mesuré à LOT4, la mise à jour du parent après son renouvellement
  était alors refusée (mutant « enfants non exclus » : le test tombe).
- **2026-10-07** — **paiement : statuts `'invoice_submitted'` et `'verified'`
  retirés** avec la facture (Q-JEF-23) ; le registre ne les tranchait pas.
  Restent `'refused'`, `'announced'`, `'scheduled'`, `'paid'`, et les deux
  dates `announced_at`, `scheduled_for` (Q-REM-17). Tranché à LOT5.
- **2026-10-07** — **les 9 décisions du rapport LOT1→LOT5 gardées** par
  Sébastien (`md/rapport-lot1-a-lot5-2026-10-07.html`, cartes D1 à D9 — pas les
  D1-D9 du schéma). Reportées au registre (Q-REM-03, 14, 17, Q-MAN-02 ; ADR B,
  J, L) ; fiche LOT4 et vérification de `CHANTIER.md` corrigées.
- **2026-10-07** — **`remuneration_parameters` versionnée par
  `effective_from` + `UNIQUE`**, comme `parameters_fees` (Q-SCH-17), et non
  `valid_from` / `valid_until` (lettre de Q-REM-05) ; **bornes relâchées au
  domaine d'un taux** (0 à 1, −1 à 1, `RCR:59, 199, 203`). Tranché par
  Sébastien à LOT6, reporté sur la carte Q-REM-05.
- **2026-10-07** — **téléphone : `'^\+[1-9]([ -]?[0-9]){1,14}$'`**. ADR-007
  (Confluence, lu à LOT7) dit « regex E.164 souple » sans la donner, et veut
  tolérer « espaces, tirets » : `+` exigé, 2 à 15 chiffres, un espace ou un
  tiret entre deux. Choix de LOT7, pas du registre ; le strict E.164 (sans
  séparateur) reste l'alternative. `client_priority` va sur `estate_proposed`
  (D6), dont la fiche ne listait pas le modèle.
- **2026-10-07** — **Eircode avec espace : la migration `08` retire l'espace**
  au lieu de s'arrêter (0 en base de dev) ; sur `estate`, un code postal sans
  pays tombe dans `ELSE FALSE`, sans CHECK « needs_country » à part ; l'Eircode
  sans espace vaut aussi sur `estate` (même CASE, Q-SCH-11). Choix de LOT8.
- **2026-10-07** — **auteur d'un bien : `estate.id_author` → `"user"(id)`**,
  facultatif (vide = import), `ON DELETE RESTRICT`, **clé seule** : le rôle
  (chasseur ou manager) se vérifie dans l'API, comme `criteria.id_author`.
  Tranché par Sébastien au questionnaire de LOT9, reporté sur la carte Q-ACC-09.
- **2026-10-07** — **reprise des mandats** (questionnaire de LOT10) : les
  demandes étaient en `'confirmed'` (la fiche les croyait en `'launched'`) ;
  **`'launched'` sous mandat**, les 18. Échus comptés à la **date fixe de
  l'audit**, 25/07/2026 : 6 ; `MAND-0013`, `0014`, `0015`, finis depuis,
  restent `'active'` (à l'application de les expirer). Nina Girard reprise
  avec **demande + critère + mandat** : 18 de chaque. Tranché par Sébastien.
- **2026-10-07** — **rôle en lecture seule** (LOT12, Q14) : oui de Jeff sur
  Discord, à justifier au jury (`docker/init-v3/README.md` §0). Mot de passe
  par **une ligne de `docker-compose.yml`** (`POSTGRES_READER_PASSWORD`, vide
  = `NOLOGIN`), oui de Sébastien. Hors liste de la fiche, nécessaires :
  `02` (ligne `'Reader'`), `create_test_db.sh` (charge le `04`) et
  `test_isolation.py` (liste des rôles). Test par `SET LOCAL ROLE`, sans mot
  de passe. Base de dev passée par la migration `12`, sans `down -v`.

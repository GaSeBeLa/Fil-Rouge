# ✅ Rapport de tests — API Fil Rouge Immobilier

> **Plan de tests et rapport d'exécution** (BC03).
> Suit le modèle du sujet : `documents utiles/PLAN-DE-TESTS.md` (StarterPack - BASE).
> Exigé par `GRILLE-EVALUATION.md:34` : « Plan de tests (unitaires + fonctionnels) | Scénarios + rapports d'exécution ».

---

## 1. Le résultat, en une ligne

**121 tests, 121 réussis, 0 échec** — en 3,46 s.

| | |
| --- | --- |
| Date de l'exécution | **2026-10-02, 14:11** |
| Version du code | commit **`8ee413e`** (branche `main`) |
| Environnement | conteneur Docker `api`, **Python 3.12.15**, PostgreSQL 16 |
| Commande | `docker compose exec api python -m pytest -v -p no:cacheprovider` (depuis `docker/`) |
| Sortie brute | `121 passed, 1 warning in 3.46s` |

⚠️ L'unique avertissement vient d'une bibliothèque (`starlette` signale que `httpx` est déprécié dans son `TestClient`). Il ne concerne pas notre code.

---

## 2. Les trois niveaux de tests

| Niveau | Nombre | Ce qu'il prouve | Base de données ? |
| --- | ---: | --- | --- |
| 🧱 **Unitaires — socle de l'API** | 44 | la logique du code : sécurité, services, erreurs | ❌ aucune |
| 🗄️ **Intégration — base de test** | 22 | les règles de PostgreSQL et leurs codes HTTP | ✅ `fil_rouge_test` |
| 💶 **Unitaires — rémunération** | 55 | les 55 cas du calcul de rémunération du sujet | ❌ aucune |
| **Total** | **121** | | |

Ils ont été écrits dans cet ordre, chaque niveau s'appuyant sur le précédent.

---

## 3. Comment les tests sont isolés

### 3.1 Les tests unitaires : aucune base

- La base est remplacée par des **objets factices** (`unittest.mock`, bibliothèque standard de Python).
- Pour les routes : `app.dependency_overrides` remplace la session PostgreSQL.
- Le hachage argon2 (~300 ms par mot de passe) est remplacé par un hacheur faible, le temps du test (fixture `fast_hasher`).
- **Aucune dépendance ajoutée** au projet.

### 3.2 Les tests d'intégration : une base à part, et tout est annulé

- **Une autre base** : `fil_rouge_test`, dans le même conteneur que la base de dev.
  - Créée par `bash docker/create_test_db.sh`.
  - Elle rejoue les scripts `01` (schéma) et `02` (rôles, comptes, correction de contrainte) de `docker/init-v2/` : **mêmes contraintes** que la base de dev.
  - Pas le `03` (2 556 biens) : aucun test n'en a besoin.
- **Tout est annulé** : chaque test tourne dans une transaction, annulée à la fin (rollback).
- `docker-compose.yml` **n'a pas été modifié**.

### 3.3 Pourquoi ce choix

| Option | Retenue ? | Raison |
| --- | --- | --- |
| Base séparée + annulation | ✅ **oui** | les tests ne dépendent jamais des données de dev |
| Annulation sur la base de dev | ❌ | les tests dépendraient de ce que contient la base de dev |
| SQLite en mémoire | ❌ | ne connaît pas les contraintes PostgreSQL (`CHECK`, `NUMERIC`, `EXCLUDE`) |

---

## 4. Les preuves que les tests prouvent quelque chose

Un test qui passe ne prouve rien s'il passerait **aussi** quand le code est faux. Chaque niveau a donc été vérifié en **cassant volontairement** le code, puis en le remettant.

| # | Vérification | Résultat attendu | Résultat obtenu | Statut |
| --- | --- | --- | --- | --- |
| P1 | Retirer le hachage du mot de passe dans `UserService.create` | au moins 1 test rouge | **1 failed, 43 passed** | ✅ |
| P2 | Arrêter le conteneur `db`, relancer les tests unitaires | tous verts | **44 passed** | ✅ |
| P3 | Supprimer la contrainte `estate_price_check` (prix ≥ 0) dans la base de test | au moins 1 test rouge | **1 failed, 21 passed** | ✅ |
| P4 | Arrêter `db`, relancer toute la suite | intégration sautée, pas en échec | **44 passed, 22 skipped** | ✅ |
| P5 | Compter les lignes des deux bases avant / après la suite | identiques | `fil_rouge_test` : 25 comptes, 18 clients, 0 bien · `fil_rouge_immobilier` : 25, 18, 2 556 — **inchangés** | ✅ |
| P6 | Remplacer l'arrondi « au demi supérieur » par « vers le bas » dans `remuneration.py` | au moins 1 test rouge | **1 failed, 54 passed** | ✅ |
| P7 | Comparer `remuneration.py` à la source du sujet (`diff`) | seule la docstring ajoutée | **24 lignes ajoutées, 0 retirée** | ✅ |

Après chaque sabotage, le code a été **restauré à l'identique** et la suite relancée.

**pyright** (vérification des types) : **0 erreur** sur tous les fichiers de tests et sur `remuneration.py`.

---

## 5. Les cas de test

Statut : ✅ réussi · ❌ échoué · ⬜ à faire.
Une ligne qui porte « × N » regroupe N cas d'un même test paramétré.

### 5.1 🧱 Unitaires — socle de l'API (44 tests)

#### Santé de l'API — `tests/test_health.py` (1)

| ID | Ce qu'on teste | Given | When | Then | Statut |
| --- | --- | --- | --- | --- | --- |
| U01 | l'API démarre | l'application FastAPI | `GET /` | `200`, `status = "ok"` | ✅ |

#### Mots de passe — `tests/test_security.py` (9)

| ID | Ce qu'on teste | Given | When | Then | Statut |
| --- | --- | --- | --- | --- | --- |
| U02 | jamais de clair | un mot de passe | `hash_password` | l'empreinte ne contient pas le mot de passe | ✅ |
| U03 | bon algorithme | un mot de passe | `hash_password` | l'empreinte commence par `$argon2id$` | ✅ |
| U04 | sel aléatoire | le même mot de passe, deux fois | `hash_password` × 2 | deux empreintes différentes | ✅ |
| U05 | bon mot de passe accepté | une empreinte | `verify_password` avec le bon mot de passe | `True` | ✅ |
| U06 | mauvais mot de passe refusé | une empreinte | `verify_password` avec un autre | `False` | ✅ |
| U07 | comptes migrés | un texte qui n'est pas une empreinte | `verify_password` | `False`, **sans exception** | ✅ |
| U08 | empreinte trop faible | une empreinte aux paramètres faibles | `needs_rehash` | `True` | ✅ |
| U09 | empreinte à jour | une empreinte aux paramètres actuels | `needs_rehash` | `False` | ✅ |
| U10 | empreinte invalide | un texte qui n'est pas une empreinte | `needs_rehash` | `False` | ✅ |

#### Service des comptes — `tests/test_user_service.py` (6)

| ID | Ce qu'on teste | Given | When | Then | Statut |
| --- | --- | --- | --- | --- | --- |
| U11 | le clair n'atteint jamais la base | un `UserCreate` | `create` | le repository reçoit une **empreinte** valide | ✅ |
| U12 | les autres champs sont recopiés | un `UserCreate` complet | `create` | email, `is_activated`, `id_role` identiques | ✅ |
| U13 | mise à jour partielle | un compte existant | `replace` avec le seul `email` | seul l'email change | ✅ |
| U14 | nouveau mot de passe haché | un compte existant | `replace` avec un `password` | l'empreinte est neuve et valide | ✅ |
| U15 | pas de remplacement complet | un compte existant | `replace` | `repository.replace` n'est **jamais** appelé | ✅ |
| U16 | compte inconnu | aucun compte | `replace` | `NotFoundError` « Utilisateur introuvable », rien n'est écrit | ✅ |

#### Service générique — `tests/test_base_service.py` (8)

| ID | Ce qu'on teste | Given | When | Then | Statut |
| --- | --- | --- | --- | --- | --- |
| U17 | liste | un repository factice | `list_all` | délègue et renvoie la liste | ✅ |
| U18 | lecture | une ligne existante | `get_by_id` | renvoie la ligne | ✅ |
| U19 | lecture d'un id inconnu | aucune ligne | `get_by_id` | `NotFoundError` avec le message de la table | ✅ |
| U20 | création | un objet | `create` | délègue au repository | ✅ |
| U21 | remplacement | une ligne existante | `replace` | transmet la ligne et les données | ✅ |
| U22 | remplacement d'un id inconnu | aucune ligne | `replace` | `NotFoundError`, **rien n'est écrit** | ✅ |
| U23 | suppression | une ligne existante | `delete` | transmet la ligne | ✅ |
| U24 | suppression d'un id inconnu | aucune ligne | `delete` | `NotFoundError`, **rien n'est supprimé** | ✅ |

#### Repository générique — `tests/test_base_repository.py` (5)

| ID | Ce qu'on teste | Given | When | Then | Statut |
| --- | --- | --- | --- | --- | --- |
| U25 | id ignoré à la création | un objet avec `id = 42` | `create` | `id` remis à `None` (PostgreSQL le génère) | ✅ |
| U26 | id jamais écrasé | une ligne `id = 1`, des données `id = 99` | `replace` | `id` reste `1`, les autres champs changent | ✅ |
| U27 | conflit à la création | une base qui lève `IntegrityError` | `create` | rollback + `ConflictError` (message d'écriture) | ✅ |
| U28 | conflit à l'enregistrement | idem | `save` | `ConflictError` (message d'écriture) | ✅ |
| U29 | conflit à la suppression | idem | `delete` | rollback + `ConflictError` (message de suppression) | ✅ |

#### Modèles des comptes — `tests/test_user_models.py` (6)

| ID | Ce qu'on teste | Given | When | Then | Statut |
| --- | --- | --- | --- | --- | --- |
| U30 | mot de passe trop court | 11 caractères | `UserCreate` | refusé (`ValidationError`) | ✅ |
| U31 | longueur minimale | 12 caractères | `UserCreate` | accepté | ✅ |
| U32 | mot de passe obligatoire | pas de mot de passe | `UserCreate` | refusé | ✅ |
| U33 | mise à jour vide | un corps `{}` | `UserUpdate` | accepté, aucun champ modifié | ✅ |
| U34 | mot de passe court en mise à jour | « court » | `UserUpdate` | refusé | ✅ |
| U35 | le mot de passe ne sort jamais | le modèle de sortie | `UserPublic` | aucun champ `password` | ✅ |

⚠️ La longueur minimale de **12 caractères** est une proposition du tuto, **pas encore actée** par le groupe (`user_model.py:59-60`). Si elle change, seuls U30, U31 et U34 changent.

#### Routes génériques — `tests/test_crud_router.py` (9)

Valent pour les **18 ressources** de l'API, qui partagent le même router.

| ID | Ce qu'on teste | Given | When | Then | Statut |
| --- | --- | --- | --- | --- | --- |
| U36 | liste | un service factice | `GET /things` | `200` | ✅ |
| U37 | id inconnu | le service lève `NotFoundError` | `GET /things/999` | `404` + message | ✅ |
| U38 | id non entier | — | `GET /things/abc` | `422`, le service **n'est pas appelé** | ✅ |
| U39 | création | un service qui crée | `POST /things` | **`201`** | ✅ |
| U40 | conflit à la création | le service lève `ConflictError` | `POST /things` | `409` + message | ✅ |
| U41 | erreurs du PUT × 2 | `NotFoundError` puis `ConflictError` | `PUT /things/1` | `404` puis `409` | ✅ |
| U42 | erreurs du DELETE × 2 | `NotFoundError` puis `ConflictError` | `DELETE /things/1` | `404` puis `409` | ✅ |

### 5.2 🗄️ Intégration — base de test (22 tests)

#### Isolation — `tests/integration/test_isolation.py` (4)

| ID | Ce qu'on teste | Given | When | Then | Statut |
| --- | --- | --- | --- | --- | --- |
| I01 | la bonne base | la connexion de test | lire son nom | `fil_rouge_test`, jamais `fil_rouge_immobilier` | ✅ |
| I02 | données de référence | la base de test | lire les rôles | `Admin`, `Client`, `Hunter`, `Manager` | ✅ |
| I03 | rien ne fuit | un compte créé par l'API | le chercher depuis **une autre connexion** | introuvable (0 ligne) | ✅ |
| I04 | un 409 ne casse pas le test | un compte, puis un doublon (`409`) | `GET /users` | le premier compte est toujours là | ✅ |

#### Comptes — `tests/integration/test_users_db.py` (8)

| ID | Ce qu'on teste | Given | When | Then | Statut |
| --- | --- | --- | --- | --- | --- |
| I05 | création | un compte valide | `POST /users` | `201`, pas de `password` dans la réponse | ✅ |
| I06 | stockage haché | un compte créé | lire la ligne **en base** | empreinte `$argon2id$`, jamais le clair | ✅ |
| I07 | email unique | un compte existant | `POST` du même email | `409` « Contrainte violée… » | ✅ |
| I08 | rôle inexistant | `id_role = 9999` | `POST /users` | `409` (clé étrangère) | ✅ |
| I09 | mise à jour partielle | un compte | `PUT` avec `is_activated` seul | email et empreinte inchangés en base | ✅ |
| I10 | id inconnu | — | `GET /users/999999` | `404` « Utilisateur introuvable » | ✅ |
| I11 | suppression | un compte libre | `DELETE`, puis `GET` | `200`, puis `404` | ✅ |
| I12 | suppression bloquée | un compte rattaché à un client | `DELETE /users/{id}` | `409` « Suppression impossible… » (`ON DELETE RESTRICT`) | ✅ |

#### Contraintes du schéma — `tests/integration/test_constraints_db.py` (10)

| ID | Ce qu'on teste | Given | When | Then | Statut |
| --- | --- | --- | --- | --- | --- |
| I13 | montant au centime | un bien à `354712.55` € | `POST`, puis `GET` | `"354712.55"` (`NUMERIC(12,2)`, en euros) | ✅ |
| I14 | contraintes du bien × 4 | prix `-1` · type `Péniche` · surface `0` · surface absente | `POST /estates` | `409` × 4 (`CHECK`, `CHECK`, `CHECK`, `NOT NULL`) | ✅ |
| I15 | référence unique | un bien existant | `POST` de la même référence | `409` | ✅ |
| I16 | ville sans adresse | un client avec une ville seule | `POST /clients` | **`201`** — la correction de `02` est bien appliquée | ✅ |
| I17 | adresse sans ville | un client avec une rue seule | `POST /clients` | `409` | ✅ |
| I18 | marié et pacsé | les deux à `true` | `POST /clients` | `409` | ✅ |
| I19 | un seul profil client par compte | un client existant | `POST` d'un 2ᵉ client sur le même compte | `409` (`UNIQUE(id_user)`) | ✅ |

⚠️ Un champ obligatoire manquant donne **`409`, pas `422`** : les modèles de table ne valident pas l'entrée, c'est PostgreSQL qui refuse. C'est le comportement actuel de l'API, documenté dans `API/README.md`.

### 5.3 💶 Unitaires — rémunération (55 tests)

- **Code testé** : `API/src/app/services/remuneration.py`.
  - C'est le **code de référence du sujet**, extrait tel quel de `REGLES-CALCUL-REMUNERATION.md` §14.2-14.3.
  - Le groupe ne l'a **pas écrit** : il l'a repris pour ne pas s'écarter de la référence.
- **Cas testés** : les tableaux du fichier `user-stories/10_calcul_remuneration_chasseur.feature`, **recopiés tels quels**.
- ⚠️ Les chiffres (fixe 3 000 €, 2,5 %, tranches, poids, bornes) sont des **paramètres proposés** par le sujet, pas des règles métier. S'ils changent, ce sont les résultats attendus qui bougent, pas les règles.

| ID | Règle du `.feature` | Ce qu'on teste | Ligne | Cas | Statut |
| --- | --- | --- | ---: | ---: | --- |
| R01 | `@droit-a-remuneration` | droit selon l'exclusivité et l'origine de la vente | 32 | 5 | ✅ |
| R02 | `@droit-a-remuneration` | acte signé après l'échéance du mandat → droit fermé, 0,00 € | 45 | 1 | ✅ |
| R03 | `@assiette` | honoraires = 3 000 € + 2,5 % du prix | 68 | 5 | ✅ |
| R04 | `@performance` | délai mandat → acte, arrondi à la semaine inférieure | 100 | 6 | ✅ |
| R05 | `@performance` | moins de visites, meilleure note | 116 | 6 | ✅ |
| R06 | `@performance` | note d'exclusivité forfaitaire | 130 | 2 | ✅ |
| R07 | `@performance` | ventes et mandats sur 12 mois glissants | 140 | 5 | ✅ |
| R08 | `@performance` | score global = 73,5 / 100 | 154 | 1 | ✅ |
| R09 | `@bareme` | un prix → une seule tranche, un seul taux | 168 | 6 | ✅ |
| R10 | `@bareme` | barème en vigueur à la date de l'acte (38 %) | 188 | 1 | ✅ |
| R11 | `@bareme` | barème du chasseur prioritaire (43 %) | 194 | 1 | ✅ |
| R12 | `@modulation` | ancienneté : +2 % par an, plafonné à 10 % | 203 | 5 | ✅ |
| R13 | `@modulation` | performance : ±20 % autour d'un score pivot de 50 | 216 | 5 | ✅ |
| R14 | `@modulation` | taux final : 46,16 % · plafond 60 % · plancher 20 % | 229, 236, 244 | 3 | ✅ |
| R15 | `@montant` | bout en bout : 13 500 € → **6 231,60 €** pour Bruno, marge 7 268,40 € | 255 | 1 | ✅ |
| R16 | `@montant` | arrondi au centime, au demi supérieur : 3 606,575 → 3 606,58 € | 267 | 1 | ✅ |
| R17 | `@assiette` | le taux s'applique aux honoraires, jamais au prix | 81 | 1 | ✅ |
| | | | **Total** | **55** | |

Répartition, identique au tableau du sujet (§14.5) : 6 + 5 + 20 + 8 + 13 + 3 = **55**.

---

## 6. Ce qui n'est pas encore testé

| Manque | Pourquoi | Statut |
| --- | --- | --- |
| **Tests fonctionnels** (un parcours métier complet, de bout en bout) | les règles métier ne sont pas encore branchées sur l'API : il n'y a pas encore de parcours à dérouler | ⬜ |
| Calcul de rémunération **branché sur la base** (lire le barème, écrire le paiement) | pas encore codé ; attend l'arbitrage de la contradiction `X01` par le groupe | ⬜ |
| « Un seul chasseur est rémunéré pour une vente » (`.feature` l. 52) | demande plusieurs mandats en base, pas une fonction pure | ⬜ |
| Règle `@tracabilite` (`.feature` l. 275-300) : montant figé, notifications | relève de la persistance | ⬜ |
| 17 des 18 ressources en intégration | seuls `/users`, `/clients` et `/estates` sont testés contre la base ; le router générique, lui, est testé pour les 18 | ⬜ |
| ENF-01 : rémunération calculée en moins de 2 s pour 500 mandats (test de charge) | le calcul n'est pas encore branché sur la base : rien à charger | ⬜ |
| ENF-03 : accès croisé aux données de rémunération | dépend des droits d'accès ; l'authentification est hors périmètre (décision du client, 2026-09-22) | ⬜ |

⚠️ Le sujet demande des tests **unitaires et fonctionnels** (`Readme.md:256`). Les **fonctionnels** restent à écrire.

---

## 7. Rejouer les tests

Depuis `Fil-Rouge/docker/`, avec les conteneurs `db` et `api` démarrés :

```bash
docker compose up -d db api
```

```bash
bash create_test_db.sh
```

```bash
docker compose exec api python -m pytest -v -p no:cacheprovider
```

- La 2ᵉ commande ne sert qu'**une fois**, puis après chaque modification de `docker/init-v2/01` ou `02`.
- Sans base de test, les 22 tests d'intégration sont **sautés**, sans échouer.
- Pour ne lancer que les tests sans base : ajouter `-m "not integration"`.

---

## 8. Traçabilité

| Commit | Contenu |
| --- | --- |
| `7f04b6e` | tests unitaires du socle de l'API |
| `5a8ca71` | base de test isolée et tests d'intégration |
| `8ee413e` | calcul de rémunération du sujet et ses 55 cas |

Détail daté des décisions : `context AI/08-etat.md`, journal du 2026-10-02.

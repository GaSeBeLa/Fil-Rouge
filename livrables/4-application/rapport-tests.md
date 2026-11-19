# ✅ Rapport de tests — API Fil Rouge Immobilier

> **Plan de tests et rapport d'exécution** (BC03).
> Suit le modèle du sujet : `documents utiles/PLAN-DE-TESTS.md` (StarterPack - BASE).
> Exigé par `GRILLE-EVALUATION.md:34` : « Plan de tests (unitaires + fonctionnels) | Scénarios + rapports d'exécution ».
> Remplace le rapport du 2026-10-12 (258 tests, commit `128e266`), toujours lisible dans l'historique git.

---

## 1. Le résultat, en une ligne

**1 123 tests : 1 116 réussis, 7 en échec attendu, 0 échec.**

| | |
| --- | --- |
| Date de l'exécution | **2026-11-19, 15:53** |
| Version du code | dépôt `Fil-Rouge-API`, commit **`31094a8`** (branche `main`) |
| Environnement | conteneur Docker `api`, **Python 3.12.16**, **PostgreSQL 16.15** |
| Commande | `docker compose exec -T api python -m pytest -rs -p no:cacheprovider` (depuis `Fil-Rouge-API/docker/`) |
| Sortie brute | `1116 passed, 7 xfailed, 1 warning in 109.25s` |

- **Les 7 échecs attendus** (`xfail`) sont des cas chiffrés du sujet que notre règle contredit **exprès** (ADR-048 : le critère « mandats signés » est noté par le taux de transformation, pas par le volume). 5 cas de `test_criteres_de_volume_cas_du_sujet`, `test_calcul_de_bout_en_bout_cas_du_sujet`, et `test_seed_gives_the_worked_example_of_the_subject`. Ils sont marqués `xfail(strict=True)` : s'ils se remettaient à passer, c'est que l'ancienne formule serait revenue, et **la suite tomberait**.
- **Plus aucun test sauté** : les tests du seed tournent maintenant dans le conteneur (ils se sautaient le 2026-10-12).

⚠️ L'unique avertissement vient d'une bibliothèque (`starlette` signale que `httpx` est déprécié dans son `TestClient`). Il ne concerne pas notre code.

---

## 2. Les trois niveaux de tests

| Niveau | Nombre | Ce qu'il prouve | Base de données ? |
| --- | ---: | --- | --- |
| 🧱 **Unitaires — socle de l'API** | 194 | la logique du code : sécurité, services, erreurs, droits | ❌ aucune |
| 💶 **Unitaires — rémunération** | 65 | les cas du calcul de rémunération du sujet | ❌ aucune |
| 🗄️ **Intégration — base de test** | 864 | les règles de PostgreSQL, les droits par rôle et leurs codes HTTP | ✅ `fil_rouge_test` |
| **Total** | **1 123** | | |

Compté le 2026-11-19 par `pytest --co` (tests collectés, `xfail` compris), fichier par fichier.

Évolution : **121** tests le 2026-10-02 · **258** le 2026-10-12 · **1 123** le 2026-11-19. La hausse vient surtout de l'intégration : les droits par rôle, testés route par route (chantier DRO), les fiches des profils (PRF), le flux de données (FLX), les suggestions de biens (SUG), le RGPD (RGP), puis le frein de connexion et l'activation du compte (2026-11-19).

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
  - Elle rejoue les scripts `01` (schéma), `02` (reprise des données) et `04` (rôle en lecture seule) de `docker/init-v3/` : **mêmes contraintes** que la base de dev (`create_test_db.sh:42-44`).
  - Pas le `03` (2 556 biens) : aucun test n'en a besoin.
- **Tout est annulé** : chaque test tourne dans une transaction, annulée à la fin (rollback).
- Les tests d'intégration portent le marqueur `integration` (`tests/integration/conftest.py:53`).

### 3.3 Pourquoi ce choix

| Option | Retenue ? | Raison |
| --- | --- | --- |
| Base séparée + annulation | ✅ **oui** | les tests ne dépendent jamais des données de dev |
| Annulation sur la base de dev | ❌ | les tests dépendraient de ce que contient la base de dev |
| SQLite en mémoire | ❌ | ne connaît pas les contraintes PostgreSQL (`CHECK`, `NUMERIC`, `EXCLUDE`) |

---

## 4. Les preuves que les tests prouvent quelque chose

Un test qui passe ne prouve rien s'il passerait **aussi** quand le code est faux. Chaque niveau a donc été vérifié en **cassant volontairement** le code, puis en le remettant.

| # | Date | Vérification | Résultat attendu | Résultat obtenu | Statut |
| --- | --- | --- | --- | --- | --- |
| P1 | 02/10 | Retirer le hachage du mot de passe dans `UserService.create` | au moins 1 test rouge | **1 failed, 43 passed** | ✅ |
| P2 | 02/10 | Arrêter le conteneur `db`, relancer les tests unitaires | tous verts | **44 passed** | ✅ |
| P3 | 02/10 | Supprimer la contrainte `estate_price_check` (prix ≥ 0) dans la base de test | au moins 1 test rouge | **1 failed, 21 passed** | ✅ |
| P4 | 02/10 | Arrêter `db`, relancer toute la suite | intégration sautée, pas en échec | **44 passed, 22 skipped** | ✅ |
| P5 | 02/10 | Compter les lignes des deux bases avant / après la suite | identiques | inchangées | ✅ |
| P6 | 02/10 | Remplacer l'arrondi « au demi supérieur » par « vers le bas » dans `remuneration.py` | au moins 1 test rouge | **1 failed, 54 passed** | ✅ |
| P7 | 02/10 | Comparer `remuneration.py` à la source du sujet (`diff`) | seule la docstring ajoutée | **24 lignes ajoutées, 0 retirée** | ✅ |
| P8 | 12/10 | Retirer la contrainte `uq_sale_estate` (P37, un bien vendu une fois) de la base de test | le test P37 rouge | **rouge sans la contrainte, vert avec** | ✅ |

- P1 à P7 datent du 2026-10-02 et n'ont **pas été refaits** le 2026-10-12 : les tests unitaires n'ont pas changé depuis (aucun commit sur `API/tests/test_*.py` après `8ee413e`).
- Après chaque sabotage, le code a été **restauré à l'identique** et la suite relancée.

---

## 5. Les cas de test

⚠️ **Le détail ci-dessous date du 2026-10-12 (258 tests)**. Les tests ajoutés depuis ne sont pas listés un par un ici : ils se lisent par fichier dans `Fil-Rouge-API/API/tests/`, et le § 2 les compte.

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

La longueur minimale de **12 caractères** est celle d'ADR-026, remis en vigueur le 2026-10-08 avec le retour de l'authentification (ADR-028).

#### Routes génériques — `tests/test_crud_router.py` (9)

Valent pour les **20 ressources** de l'API, qui partagent le même router (`API/src/app/main.py` : 20 `include_router`).

| ID | Ce qu'on teste | Given | When | Then | Statut |
| --- | --- | --- | --- | --- | --- |
| U36 | liste | un service factice | `GET /things` | `200` | ✅ |
| U37 | id inconnu | le service lève `NotFoundError` | `GET /things/999` | `404` + message | ✅ |
| U38 | id non entier | — | `GET /things/abc` | `422`, le service **n'est pas appelé** | ✅ |
| U39 | création | un service qui crée | `POST /things` | **`201`** | ✅ |
| U40 | conflit à la création | le service lève `ConflictError` | `POST /things` | `409` + message | ✅ |
| U41 | erreurs du PUT × 2 | `NotFoundError` puis `ConflictError` | `PUT /things/1` | `404` puis `409` | ✅ |
| U42 | erreurs du DELETE × 2 | `NotFoundError` puis `ConflictError` | `DELETE /things/1` | `404` puis `409` | ✅ |

### 5.2 💶 Unitaires — rémunération (55 tests)

- **Code testé** : `API/src/app/services/remuneration.py`.
  - C'est le **code de référence du sujet**, extrait de `REGLES-CALCUL-REMUNERATION.md` §14.2-14.3, à **un écart** près : le critère « mandats » (ADR-048, ci-dessous).
  - Le groupe ne l'a **pas écrit** : il l'a repris pour ne pas s'écarter de la référence.
- **Cas testés** : les tableaux du fichier `user-stories/10_calcul_remuneration_chasseur.feature`, **recopiés tels quels**.
- ⚠️ Les chiffres (fixe 3 000 €, 2,5 %, tranches, poids, bornes) sont des **paramètres proposés** par le sujet, pas des règles métier. S'ils changent, ce sont les résultats attendus qui bougent, pas les règles.
- ⚠️ ADR-048 (accepté le 2026-10-12) note le critère « mandats signés » par le **taux de transformation**, codé le 2026-10-13 (fiches API11 et API12). Les cas du sujet sur `mandats × 10` restent, nommés « cas du sujet » et marqués **en échec attendu** (`xfail(strict=True)`) : 5 lignes de R07 et R15. À côté, les cas du taux : 4 ventes pour 5 mandats → **80 points** ; Bruno refait → **6 084,45 €**.

| ID | Règle du `.feature` | Ce qu'on teste | Ligne | Cas | Statut |
| --- | --- | --- | ---: | ---: | --- |
| R01 | `@droit-a-remuneration` | droit selon l'exclusivité et l'origine de la vente | 32 | 5 | ✅ |
| R02 | `@droit-a-remuneration` | acte signé après l'échéance du mandat → droit fermé, 0,00 € | 45 | 1 | ✅ |
| R03 | `@assiette` | honoraires = 3 000 € + 2,5 % du prix | 68 | 5 | ✅ |
| R04 | `@performance` | délai mandat → acte, arrondi à la semaine inférieure | 100 | 6 | ✅ |
| R05 | `@performance` | moins de visites, meilleure note | 116 | 6 | ✅ |
| R06 | `@performance` | note d'exclusivité forfaitaire | 130 | 2 | ✅ |
| R07 | `@performance` | ventes et mandats sur 12 mois glissants | 140 | 5 | ✅ ventes · ⚠️ mandats en échec attendu (ADR-048) |
| R08 | `@performance` | score global = 73,5 / 100 | 154 | 1 | ✅ |
| R09 | `@bareme` | un prix → une seule tranche, un seul taux | 168 | 6 | ✅ |
| R10 | `@bareme` | barème en vigueur à la date de l'acte (38 %) | 188 | 1 | ✅ |
| R11 | `@bareme` | barème du chasseur prioritaire (43 %) | 194 | 1 | ✅ |
| R12 | `@modulation` | ancienneté : +2 % par an, plafonné à 10 % | 203 | 5 | ✅ |
| R13 | `@modulation` | performance : ±20 % autour d'un score pivot de 50 | 216 | 5 | ✅ |
| R14 | `@modulation` | taux final : 46,16 % · plafond 60 % · plancher 20 % | 229, 236, 244 | 3 | ✅ |
| R15 | `@montant` | bout en bout : 13 500 € → **6 231,60 €** pour Bruno, marge 7 268,40 € | 255 | 1 | ⚠️ échec attendu (ADR-048) ; avec le taux : 6 084,45 € |
| R16 | `@montant` | arrondi au centime, au demi supérieur : 3 606,575 → 3 606,58 € | 267 | 1 | ✅ |
| R17 | `@assiette` | le taux s'applique aux honoraires, jamais au prix | 81 | 1 | ✅ |
| | | | **Total** | **55** | |

Répartition, identique au tableau du sujet (§14.5) : 6 + 5 + 20 + 8 + 13 + 3 = **55**.

### 5.3 🗄️ Intégration — base de test (159 tests)

Chaque ligne regroupe les tests d'un même thème. Un refus de la base revient en **`409`** ; un champ manquant ou mal formé est arrêté par l'API en **`422`**, avant la base.

#### Isolation et comptes — `test_isolation.py` (4), `test_users_db.py` (9)

| ID | Thème | Ce qu'on vérifie | Cas | Statut |
| --- | --- | --- | ---: | --- |
| I01 | isolation | la connexion vise `fil_rouge_test`, jamais `fil_rouge_immobilier` ; les rôles de référence sont là | 2 | ✅ |
| I02 | isolation | une écriture de l'API est invisible d'une autre connexion ; un `409` ne casse pas la transaction du test | 2 | ✅ |
| I03 | comptes | création en `201` sans `password` dans la réponse ; `is_activated` absent → `false` ; empreinte `$argon2id$` en base | 3 | ✅ |
| I04 | comptes | email en double et rôle inconnu → `409` | 2 | ✅ |
| I05 | comptes | `PUT` partiel garde les autres champs ; id inconnu → `404` | 2 | ✅ |
| I06 | comptes | suppression d'un compte libre, puis `404` ; d'un compte rattaché à un client → `409` | 2 | ✅ |

#### Contraintes du schéma — `test_constraints_db.py` (102)

| ID | Table | Ce qu'on vérifie | Cas | Statut |
| --- | --- | --- | ---: | --- |
| I07 | `estate` | prix en euros entiers (centimes → `422`) ; champ manquant → `422` ; `CHECK` violés → `409` ; référence unique ; auteur connu ou inconnu ; code postal français à 5 chiffres ; Eircode sans espace ; rénovation à deux états | 20 | ✅ |
| I08 | `client` | adresse obligatoire (`422` dans l'API, refus en base) ; adresse anonymisée acceptée ; marié et pacsé refusé ; un seul profil par compte | 8 | ✅ |
| I09 | personnes | téléphone au format international accepté, national refusé | 9 | ✅ |
| I10 | `criteria` | un quartier exige une ville ; pas de budget de rénovation | 3 | ✅ |
| I11 | `mandate` | statuts permis ; signature exigée sauf annulation ; 6 mois accepté, 7 refusé ; un seul mandat exclusif à la fois ; renouvellement ; un seul successeur | 12 | ✅ |
| I12 | `review_media` | plusieurs médias par note d'avis ; type inconnu ou note absente refusés | 3 | ✅ |
| I13 | `estate_proposed` | statuts permis ; priorité dans ses bornes | 6 | ✅ |
| I14 | `payment` | taux final dans ses bornes et dans son domaine ; un paiement refusé n'a ni taux, ni note, ni détail ; un paiement accepté les a tous ; dates selon le statut ; pas de paiement dans le futur | 24 | ✅ |
| I15 | barèmes et ventes | taux de barème non nul ; une grille d'honoraires par date ; vente sur une grille connue ; **un bien vendu une seule fois (P37)** ; réglages du chasseur gardent leurs paliers, une version par date | 7 | ✅ |
| I16 | `hunter_performance` | une note par paiement et par mandat, du bon chasseur ; deux notes le même jour acceptées | 4 | ✅ |
| I17 | rôle `fil_rouge_reader` | lit tout, sauf les mots de passe ; n'écrit rien | 6 | ✅ |

#### Trous de l'audit — `test_trous_audit_db.py` (36)

Un test par règle ajoutée à la base par ADR-053 (migrations 22 à 38). Le n° renvoie à `md/journal/problemes-a-regler.md`.

| ID | Trou | Ce qu'on vérifie | Cas | Statut |
| --- | --- | --- | ---: | --- |
| I18 | P2 | email unique à la majuscule près, et bien formé | 3 | ✅ |
| I19 | P6 | une demande répondue a un chasseur | 4 | ✅ |
| I20 | P8, P9 | les versions de critères forment une ligne, sans branche ni boucle ; une nouvelle version a un motif | 6 | ✅ |
| I21 | P12 | un mandat porte sur la demande de son propre client | 2 | ✅ |
| I22 | P13 | renouvellement à l'échéance seulement, du même client, jamais de lui-même | 4 | ✅ |
| I23 | P15 | deux mandats exclusifs simultanés : la 2ᵉ transaction attend la 1ʳᵉ ; un autre client n'attend pas | 2 | ✅ |
| I24 | P17 | latitude et longitude ensemble, ou aucune | 3 | ✅ |
| I25 | P22 | un bien n'est proposé que par le chasseur du mandat | 2 | ✅ |
| I26 | P24, P34 | ni visite faite, ni note dans le futur | 6 | ✅ |
| I27 | P35, P36 | une note vient du mandat de son chasseur ; une seule note initiale par chasseur | 4 | ✅ |

#### Paramétrage et seed — `test_parametrage_service.py` (4), `test_seed_parametres.py` (4)

| ID | Ce qu'on vérifie | Cas | Statut |
| --- | --- | ---: | --- |
| I28 | la version des réglages en vigueur à la date est celle lue ; avant la 1ʳᵉ version, ou tables vides → erreur de paramétrage ; une grille finit la veille de la suivante | 4 | ✅ (3 rejoués avec le seed, voir § 1) |
| I29 | le seed remplit les 3 tables de paramètres, se rejoue, égale le paramétrage par défaut du code, et redonne l'exemple chiffré du sujet | 4 | ✅ (rejoués avec le seed, voir § 1) |

---

## 6. Ce qui n'est pas encore testé

| Manque | Pourquoi | Statut |
| --- | --- | --- |
| **Tests fonctionnels** (un parcours métier complet, de bout en bout) | écrit le 2026-11-19 : `test_parcours_particulier.py` ; la matrice des 80 scénarios, et les 3 trous qu'ils ont trouvés, réparés le même jour : `tests-fonctionnels.md` | ✅ |
| **Authentification** : connexion, JWT, rôles, droits | codée et testée le 2026-10-12 (fiches API1 à API3) ; la matrice des droits (ADR-027) codée le 2026-10-13 (chantier DRO, `test_droits_par_role.py`) ; frein aux essais en série et activation du compte le 2026-11-19 (`test_login_throttle.py`, `test_activation.py`) | ✅ |
| Trous de l'audit **côté API** (ADR-053 : P2 `EmailStr`, P5, P16, P19…) | codés et testés le 2026-10-12 (fiches API4, API7 à API9 : `test_entrees.py`, `test_propositions_visites.py`, `test_signature_vente.py`, `test_demande_avant_compte.py`) | ✅ |
| Calcul de rémunération **branché sur la base** (lire le barème, écrire le paiement) | codé et testé le 2026-10-13 (fiche API12 : `test_calcul_paiement.py`) | ✅ |
| Critère « mandats signés » noté par le taux de transformation (ADR-048) | codé le 2026-10-13 (fiche API11) ; les cas du sujet R07 et R15 restent, en échec attendu | ✅ |
| « Un seul chasseur est rémunéré pour une vente » (`.feature` l. 52) | demande plusieurs mandats en base, pas une fonction pure | ⬜ |
| Règle `@tracabilite` (`.feature` l. 275-300) : montant figé, notifications | relève de la persistance | ⬜ |
| ENF-01 : rémunération calculée en moins de 2 s pour 500 mandats (test de charge) | le calcul est branché (fiche API12) ; le test de charge n'est pas écrit | ⬜ |
| ENF-03 : accès croisé aux données de rémunération | la matrice des droits est codée et testée (chantier DRO, `test_droits_par_role.py`) | ✅ |
| Les tests du seed **dans le conteneur** | ils tournent depuis : plus aucun test sauté le 2026-11-19 (§ 1) | ✅ |

✅ Le sujet demande des tests **unitaires et fonctionnels** (`Readme.md:256`). Les **fonctionnels** sont dans [`tests-fonctionnels.md`](./tests-fonctionnels.md) (2026-11-19).

---

## 7. Rejouer les tests

Depuis `Fil-Rouge-API/docker/`, avec les conteneurs `db` et `api` démarrés :

```bash
docker compose up -d db api
```

```bash
bash create_test_db.sh
```

```bash
docker compose exec -T api python -m pytest -rs -p no:cacheprovider
```

- La 2ᵉ commande ne sert qu'**une fois**, puis après chaque modification de `docker/init-v3/`.
- Pour ne lancer que les tests sans base : ajouter `-m "not integration"`.
- Pour le détail de chaque test : ajouter `-v`.

---

## 8. Traçabilité

| Commit | Contenu |
| --- | --- |
| `7f04b6e` | tests unitaires du socle de l'API |
| `5a8ca71` | base de test isolée et tests d'intégration |
| `8ee413e` | calcul de rémunération du sujet et ses 55 cas |
| `a395b8e` | LOT12 : rôle en lecture seule et ses tests |
| `6369e45` | premier trou de l'audit testé (P2, ADR-053) |
| `00f5074` | dernier trou testé : un bien vendu une fois (P37) |
| `128e266` | version du code du rapport du 2026-10-12 |
| `e6f4b87` | frein aux mots de passe essayés en série (`Fil-Rouge-API`) |
| `141d068` | activation du compte par le particulier (`Fil-Rouge-API`) |
| `31094a8` | seed des paramètres en transaction ; version du code de cette exécution (`Fil-Rouge-API`) |

Détail daté des décisions : `context AI/08-etat.md` ; trous de l'audit : `md/journal/problemes-a-regler.md` et ADR-053.

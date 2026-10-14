> **QUAND LIRE** : on joue une fiche `BAN*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache BAN<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier BAN — Réparer le banc v2/v3

**À quoi il sert.** Le banc `docker/compare_v2_v3.sh` rend DIFFÉRENTES depuis le
08/10 sans que personne le voie ; le chantier le remet à IDENTIQUES et le met dans pytest.

**Ouvert.** le 2026-10-14.

**Fait.** Rien : diagnostic fait au cadrage (voir le socle), `BAN1` à jouer — estimé 2 fiches · cadré 3.

**Session** : 937d71c9-531a-49f9-9349-193dc854db9d

## Le socle commun

**Où.** Le code vit dans `../Fil-Rouge-API/` ; les commandes partent de
`../Fil-Rouge-API/docker/`. Ce fichier-ci reste dans `Fil-Rouge`.

**Le diagnostic** (banc lancé le 2026-10-14, exit 1, 111 s) :

- Schéma **identique** : 618 faits de chaque côté. Seul le nombre de lignes diffère.
- `commission_scale` 0 / 5, `hunter_rate_parameters` 0 / 1, `parameters_fees` 0 / 1 :
  remplies par `init-v3/05_parametres.sql` depuis le 08/10 (`e825253`) ; la migration
  `migrations/v2-vers-v3/06_parametres.sql` crée les tables sans INSERT.
- `estate_contact` 0 / 2469 : rempli par `init-v3/06_populate_estate_contact.sql`
  depuis le 13/10 (`c4dfe66`, ADR-054) ; la migration `40_contact-du-bien.sql` crée la table sans INSERT.
- ➡️ Aucun chemin n'a tort sur la structure : init-v3 a reçu des **données** sans migration jumelle.

**Décisions de l'utilisateur** (2026-10-14) :

| Sujet | Décision |
|---|---|
| Paramètres (7 lignes) | nouvelle migration **44**, sans toucher aux migrations déjà jouées |
| `estate_contact` | données de démo : le banc **ne compte pas** ses lignes ; son schéma reste comparé |
| Banc dans pytest | test d'intégration, lancé **à chaque pytest**, quelle que soit sa durée |
| Source unique | le **test** est le banc ; `compare_v2_v3.sh` se réduit à le lancer |
| `psql` | `postgresql-client` dans `API/Dockerfile` : le test joue les vrais fichiers avec le vrai `psql` |
| `docker-compose.yml` | **oui donné** pour 3 montages en lecture seule dans `api`, et rien d'autre |

**Fichiers qui exigent `psql`** (`\gset`, `\gexec`, `\if`, `\getenv`) :
`init-v3/04_role-lecture-seule.sql`, `migrations/v2-vers-v3/12_role-lecture-seule.sql`.
`psycopg2` ne sait pas les jouer : ne pas les sauter, ne pas les réécrire.

**Invariants.**

- Le banc ne vise **jamais** `fil_rouge_immobilier` ni `fil_rouge_test` (garde-fou du script, à garder).
- Ordre de chargement : les `*.sql` par nom, octet par octet (`LC_ALL=C`), comme l'entrypoint.
- Jamais `docker/.env` ni `API/.env` dans le conteneur `api`.
- Tests d'intégration : `API/tests/integration/`, marqueur `integration`, base et
  connexion par `DATABASE_URL` (`src/app/conf/database.py`) ; base injoignable → `pytest.skip` avec sa raison.

**Hors chantier.** Le seed de démo (TODO 3), une CI, le contenu de `estate_contact`.

**Vérification.** Depuis `../Fil-Rouge-API/docker/` :
`docker compose exec -T api python -m pytest -q` (926 passed, 8 skipped, 6 xfailed au 14/10).

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `BAN1` | Rendre le banc IDENTIQUES | rien |
| `BAN2` | Donner au conteneur api les fichiers SQL et psql | rien |
| `BAN3` | Faire du banc un test pytest | `BAN1`, `BAN2` |

`BAN1` et `BAN2` sont indépendantes ; `BAN3` les attend toutes les deux.

---

<!-- FICHE:BAN1 -->
## BAN1 [x] — Rendre le banc IDENTIQUES

**Session** : 990a5a18-5517-41c2-b408-e47667014e06
**Dépend de** : rien.
**Fichiers** : `../Fil-Rouge-API/docker/migrations/v2-vers-v3/44_parametres-de-depart.sql` (nouveau),
`../Fil-Rouge-API/docker/compare_v2_v3.sh`, `../Fil-Rouge-API/docker/init-v3/05_parametres.sql` (lu, pas modifié).

**Prompt**
Écris la migration 44 : les trois INSERT de `05_parametres.sql`, recopiés tels
quels (ils sont déjà rejouables : `ON CONFLICT` et `NOT EXISTS`). En-tête au format
de la migration 43 : POURQUOI (une base migrée n'a pas de barème, donc ne sait pas
calculer), POUR QUI (toute base v2 migrée ; sans effet sur une base créée par init-v3),
et la source : `05_parametres.sql`, que le banc garde aligné.

Dans `compare_v2_v3.sh`, retire du comptage de lignes les tables de démo : une
liste nommée, une seule entrée `estate_contact`, avec sa raison (ADR-054 : données
de démo, pas de faux contacts poussés par migration). Le schéma de ces tables reste comparé.
Corrige l'en-tête du script : init-v3 compte 6 fichiers, plus 3.

Dans le compte rendu, une ligne : quel chemin avait tort, et pourquoi (le socle le dit).

**Critère de fin**
`bash docker/compare_v2_v3.sh` rend `IDENTIQUES`, exit 0, avec le nombre de faits.
Mutant : sur une copie (`MIG_DIR=<copie sans 44>`), le banc rend `DIFFÉRENTES`, exit 1,
et le diff nomme `commission_scale`. Mutant 2 : sans la liste de démo, il nomme `estate_contact`.
<!-- /FICHE -->

---

<!-- FICHE:BAN2 -->
## BAN2 [ ] — Donner au conteneur api les fichiers SQL et psql

**Dépend de** : rien.
**Fichiers** : `../Fil-Rouge-API/API/Dockerfile`, `../Fil-Rouge-API/docker/docker-compose.yml`
(oui donné le 2026-10-14 pour ces montages seulement).

**Prompt**
Dans `API/Dockerfile`, installe `postgresql-client` (sans les recommandations,
cache d'apt vidé), avec un commentaire qui dit pourquoi : le banc joue des fichiers
qui exigent `psql`. Vérifie la version : `\getenv` exige `psql` 15 ou plus ; le serveur est `postgres:16`.

Dans `docker-compose.yml`, service `api`, ajoute trois montages en lecture seule :
`./init-v2` → `/api/sql/init-v2`, `./init-v3` → `/api/sql/init-v3`,
`./migrations/v2-vers-v3` → `/api/sql/v2-vers-v3`. Un commentaire : jamais `docker/` entier (il porte `.env`).
Rien d'autre ne bouge dans le compose.

Mesure le poids de l'image avant et après (`docker image ls`), et donne les deux chiffres.

**Critère de fin**
Après `docker compose build api` et `docker compose up -d api` :
`docker compose exec -T api psql --version` rend une version ≥ 15 ;
`docker compose exec -T api ls /api/sql/v2-vers-v3` liste autant de `.sql` que le dossier
hôte (40 avant BAN1, 41 après ; donner les deux comptes) ;
`docker compose exec -T api ls -a /api/sql` ne montre aucun `.env`.
La suite pytest rend toujours 926 passed.
<!-- /FICHE -->

---

<!-- FICHE:BAN3 -->
## BAN3 [ ] — Faire du banc un test pytest

**Dépend de** : `BAN1`, `BAN2`.
**Fichiers** : `../Fil-Rouge-API/API/tests/integration/test_banc_v2_v3.py` (nouveau),
`../Fil-Rouge-API/docker/compare_v2_v3.sh`.

**Prompt**
Porte le banc en Python dans un test d'intégration : il recrée deux bases jetables,
charge init-v2 puis les migrations dans l'une, init-v3 dans l'autre, en lançant
`psql` (sous-processus, `ON_ERROR_STOP=1`), puis compare leurs descriptions.
Reprends **telle quelle** la requête `decrire` du script et sa liste de tables de démo :
le test devient la seule source. Les dossiers se lisent par variables
d'environnement (`BANC_V2_DIR`, `BANC_V3_DIR`, `BANC_MIG_DIR`), défaut `/api/sql/…`.
Dossiers absents : `pytest.skip` avec la raison. Garde le garde-fou sur les noms de base.
Les bases sont supprimées dans tous les cas (fixture avec `yield`).
Un écart : le test échoue en montrant le diff.

Réduis `compare_v2_v3.sh` à lancer ce test dans le conteneur `api`, en passant les
variables `BANC_*` si elles sont posées. Mesure la durée du test, et donne-la.
Ramasse la doc qui décrit le banc : grep `compare_v2_v3` dans `../Fil-Rouge-API/`
et dans `Fil-Rouge/` (hors historique daté), chaque mention vivante mise à jour.

**Critère de fin**
`docker compose exec -T api python -m pytest -q tests/integration/test_banc_v2_v3.py` : 1 passed.
Mutant : avec `BANC_V3_DIR` sur une copie de `init-v3` où `05_parametres.sql` insère
une 6e ligne de barème, le test échoue et le diff nomme `commission_scale`.
La suite complète : un passed de plus qu'avant la fiche (comptes avant et après), durée donnée.
<!-- /FICHE -->

> **QUAND LIRE** : on joue une fiche `DEM*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache DEM<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier DEM — Seed de démo

**Ouvert.** le 2026-10-14.

**À quoi il sert.** La base de dev a les biens et les clients repris, mais le
parcours n'a jamais eu lieu : 7 tables vides et 0 compte actif sur 25 (compté le
2026-10-14). Le seed joue ce parcours pour que le Swagger et la soutenance parlent.

**Estimé.** 6 fiches · ≈29 $ — ≈4,82 $/fiche sur 6 clos (le 2026-10-14).

**Fait.** Rien. Cadré le 2026-10-14 (Seb, Discord), en 3 fiches, `DEM1` à jouer.

**Session** : da42f1a3-d291-47c1-a710-979822a907ab

## Le socle commun

Le code vit dans `../Fil-Rouge-API/` ; tout chemin ci-dessous s'y lit.
Vérification : depuis `../Fil-Rouge-API/docker/`,
`docker compose exec -T api python -m pytest -q` (927 passed, 8 skipped,
6 xfailed au 2026-10-14) ; du Python touché passe `pyright`.

**Le seed est le décor, les tests sont la preuve** : aucun test ne dépend du
seed ; le seed n'écrit jamais dans `fil_rouge_test`.

Décisions de Seb (Discord, 2026-10-14) :
- **Parcours complet (Q1 A)** : les 7 tables vides au 2026-10-14 — `estate_proposed`,
  `estate_searchrequest`, `visit`, `sale`, `payment`, `hunter_performance`,
  `review_media` — ont des lignes à la fin.
- **Un script qui appelle les services (Q2 A)** : `API/src/app/scripts/seed_demo.py`,
  sur le modèle de `create_admin.py` (`Session(engine)`, services et repositories,
  aucun appel HTTP, aucun SQL écrit à la main). Lancement :
  `docker compose exec api python -m src.app.scripts.seed_demo`.
- **Faker `fr_FR`, graine fixe (Q3 A)** : mêmes données à chaque lancement ;
  aucune date tirée de `now()`. Les montants ne viennent jamais du hasard : ils
  sortent de `PaymentCalculationService.build_payment`.
- **Comptes de démo neufs (Q4 A)** : un par rôle de `utils/roles.py` sauf
  `ADMIN` (`CLIENT`, `HUNTER`, `MANAGER`, `READER`), activés ; les 25 comptes
  repris ne bougent pas (DRO8). Mot de passe : `DEMO_PASSWORD`, lu dans
  l'environnement ; jamais dans git, jamais affiché.
- **Compose (B)** : une seule ligne `DEMO_PASSWORD: ${DEMO_PASSWORD:-}` dans la
  section `api` de `docker/docker-compose.yml` — le oui de Seb vaut pour cette
  ligne seulement.
- **Pour l'équipe, après le pull** (Seb, 2026-10-14) : chacun ajoute
  `DEMO_PASSWORD=<12 caractères au moins>` à son `docker/.env`, puis
  `docker compose up -d --build` (le paquet `faker` et la variable n'arrivent
  qu'au rebuild). Le compte rendu de chaque fiche qui touche au compose ou aux
  dépendances le redit, et l'annonce du pull aussi.

| Symbole | Fichier | Rôle dans le seed |
|---|---|---|
| `UserService.create` | `services/user_service.py` | crée un compte, mot de passe haché (Argon2) |
| `MandateService.create` | `services/mandate_service.py` | mandat signé → la demande passe à `launched` |
| `EstateProposedService`, `VisitService`, `SaleService` | `services/` | proposition, visite, vente, avec leurs règles |
| `PaymentCalculationService.build_payment` | `services/payment_calculation_service.py` | le paiement d'une vente, calculé |
| `PaymentService` | `services/payment_service.py` | `announced` → `scheduled` → `paid` ; à `paid`, la note du chasseur s'écrit (`journal_note`) |

Modèles de données valides, à relire avant d'écrire : `proposal` et `visit` dans
`tests/integration/test_propositions_visites.py`, `sale_payload` dans
`tests/integration/test_constraints_db.py`. Un refus de la base ou d'une règle
(`ConflictError`) arrête le script avec son message : on corrige les données du
seed, jamais la règle.

Hors du chantier : les tests existants, `fil_rouge_test`, le déploiement (chantier 9).

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `DEM1` | Poser le script et les comptes de démo | rien |
| `DEM2` | Jouer le parcours jusqu'à la visite | `DEM1` |
| `DEM3` | Finir le parcours : vente, paiement, note, avis | `DEM2` |

Les trois fiches se suivent : chacune part des lignes écrites par la précédente.

---

<!-- FICHE:DEM1 -->
## DEM1 [x] — Poser le script et les comptes de démo

**Session** : 4b603c61-6273-4519-a6c1-80c6873b02e1
**Dépend de** : rien.
**Fichiers** : nouveau `API/src/app/scripts/seed_demo.py`, `API/src/app/scripts/create_admin.py` (lecture, modèle), `API/requirements.txt`, `docker/docker-compose.yml` (une ligne, voir le socle), `docker/.env.exemple`, nouveau `API/tests/integration/test_seed_demo.py`.

**Prompt**
1. Ajoute `faker` à `requirements.txt`, à une version exacte lue sur PyPI le jour
   même (dire la version et la date au compte rendu).
2. `seed_demo.py` : `main()` lit `DEMO_PASSWORD` (absent ou moins de 12
   caractères : arrêt avec un message clair, rien d'écrit) ; refuse si
   `POSTGRES_DB` vaut `fil_rouge_test` ; s'arrête sans rien écrire si un compte de
   démo existe déjà. Faker `fr_FR`, graine fixe en constante.
3. Crée 4 comptes activés (`demo-client@…`, `demo-chasseur@…`, `demo-manager@…`,
   `demo-lecteur@…` ; domaine en `.invalid`) par `UserService.create`, puis leurs
   profils : client, chasseur rattaché au manager de démo, manager.
   Structure le script en étapes (une fonction par étape) : `DEM2` et `DEM3` y ajoutent les leurs.
4. La ligne du compose, et `DEMO_PASSWORD=` (sans valeur) dans `.env.exemple`.

**Critère de fin**
`test_seed_demo.py` vert, sur `fil_rouge_test` dans sa transaction annulée (les
étapes du script appelées sur `db_session`, pas `main()`) : 4 comptes créés,
activés, un par rôle ; un 2e appel n'écrit rien ; `main()` refuse
`POSTGRES_DB=fil_rouge_test`. Suite complète verte, compte brut ; `pyright` 0
erreur sur les fichiers touchés. Mutant : retirer le contrôle « déjà semé » →
le test du 2e appel tombe.
<!-- /FICHE -->

---

<!-- FICHE:DEM2 -->
## DEM2 [x] — Jouer le parcours jusqu'à la visite

**Session** : 4b603c61-6273-4519-a6c1-80c6873b02e1
**Dépend de** : `DEM1`.
**Fichiers** : `API/src/app/scripts/seed_demo.py`, `API/tests/integration/test_seed_demo.py`, `tests/integration/test_propositions_visites.py` (lecture, modèle).

**Prompt**
Ajoute les étapes, par les services du socle, sur les comptes de démo :
1. une demande de recherche du client de démo, avec ses critères ;
2. un mandat signé, confié au chasseur de démo : la demande passe à `launched` ;
3. des biens proposés (`estate_proposed`) parmi les biens existants, et leurs
   liens bien-demande (`estate_searchrequest`) ;
4. des visites dans les bornes du mandat.
Choisis les quantités pour que la démo soit lisible (quelques lignes par
table) ; dis-les au compte rendu. Dates fixes, dérivées de la graine.

**Critère de fin**
`test_seed_demo.py` : après les étapes, `estate_proposed`, `estate_searchrequest`
et `visit` ont au moins une ligne chacune ; la demande de démo vaut `launched` ;
le client de démo ne voit, par `visible_rows`, que ses visites. Suite complète
verte, compte brut ; `pyright` 0 erreur. Mutant : supprimer l'étape des visites
→ le test des visites tombe.
<!-- /FICHE -->

---

<!-- FICHE:DEM3 -->
## DEM3 [ ] — Finir le parcours : vente, paiement, note, avis

**Dépend de** : `DEM2`.
**Fichiers** : `API/src/app/scripts/seed_demo.py`, `API/tests/integration/test_seed_demo.py`, `tests/integration/test_constraints_db.py` (lecture : `sale_payload`), `API/README.md`.

**Prompt**
1. Une offre acceptée et une vente sur un bien visité, par `SaleService`
   (modèle : `sale_payload`).
2. Le paiement : `PaymentCalculationService.build_payment`, puis
   `PaymentService.create`, puis `announced` → `scheduled` → `paid` : la note du
   chasseur s'écrit d'elle-même. Un refus (paramètre manquant, note initiale
   absente : `hunter_performance` est vide au 2026-10-14) se mesure et se dit ;
   on ne l'esquive pas en écrivant la ligne à la main.
3. Un avis (`review_media`) du client de démo.
4. `API/README.md` : une section « Seed de démo » — ajouter `DEMO_PASSWORD` à
   `docker/.env`, `docker compose up -d --build`, la commande, les 4 comptes.
5. Lance le script pour de vrai sur la base de dev et compte les 7 tables.
6. Un court ADR, statut « proposé » (Seb, Discord, 2026-10-14, choix A) :
   `md/adr/adr-0NN-seed-de-demo.md` dans `Fil-Rouge`, numéro suivant le plus
   grand de `md/adr/` — données fausses (Faker, aucune personne réelle), seed
   jamais dans les tests, `faker` à version fixe ; pas de report Confluence.

**Critère de fin**
`test_seed_demo.py` : le paiement de démo existe, `paid`, et son montant est
celui que rend `build_payment` (pas une constante du test) ; une note
`hunter_performance` et un avis existent. Sur la base de dev, `count(*)` des
7 tables du socle, tous > 0, au compte rendu. Suite verte, compte brut ;
`pyright` 0 erreur. Mutant : remplacer le montant calculé par une constante → le test tombe.
<!-- /FICHE -->

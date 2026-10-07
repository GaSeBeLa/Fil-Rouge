> **QUAND LIRE** : on joue une fiche `LOT*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache LOT<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier LOT — Lot de migration (schéma v3)

**Ouvert.** le 2026-10-07.

**À quoi il sert.** Le registre a tranché les changements de schéma et de reprise
des données ; aucun n'est appliqué. Le chantier crée `docker/init-v3/`, les y
applique par thème, et prouve qu'une base v2 migrée égale une base v3 neuve.

**Fait.** Rien. Ouvert le 2026-10-07, cadré en 12 fiches, `LOT1` à jouer.

**Session** : cc3da4f0-917c-419b-81f6-b7df8f9aa6a0

## Le socle commun

**Trois dossiers, trois rôles** (décidé le 2026-10-07) :

| Chemin | Rôle | Règle |
|---|---|---|
| `docker/init-v2/` | l'ancien schéma, point de départ du banc | **figé** dès LOT1 |
| `docker/init-v3/` | la cible : `01` schéma, `02` reprise, `03` biens, `README.md` | monté par `docker-compose.yml` dès LOT1 |
| `docker/migrations/v2-vers-v3/NN_<thème>.sql` | passe une base v2 **existante** en v3 ; `NN` = numéro de fiche | en-tête comme `docker/migrations/2026-09-22_role_admin.sql` (POURQUOI, POUR QUI, COMMENT) ; une transaction |

**D'où viennent les décisions** : le registre `md/questions-a-trancher-2026-10-02.md`.
- La liste « **Lot de migration qui en découle** » (grep ce libellé).
- La carte `#### Q-XXX-NN` de chaque question citée par la fiche (grep son titre).
- ⚠️ Ses renvois `01:NNN`, `02:NNN` visent **v2** : les lire dans `docker/init-v2/`.
- Une décision absente du registre ne s'invente pas : la fiche s'arrête et demande.

**Ce que livre chaque fiche thème (LOT3 à LOT10)** :
1. `init-v3/01` (et `02`, `03` si des données changent) ;
2. sa migration `v2-vers-v3/NN_<thème>.sql` ;
3. les modèles `API/src/app/models/<table>_model.py`, confrontés à `init-v3/01` par grep ;
4. un test d'intégration **par contrainte ajoutée ou changée**, dans
   `API/tests/integration/test_constraints_db.py`, et son mutant ;
5. une ligne par changement dans `init-v3/README.md`, avec sa `Q-xx` ;
6. le banc vert.

**Le mutant d'une contrainte** joue sur la base de test, jamais sur un fichier.
Un test de **refus** tombe quand la contrainte est retirée (`DROP CONSTRAINT`,
`DROP TRIGGER`) ; un test d'**accord** tombe quand sa forme v2 est remise. Puis
`bash docker/create_test_db.sh` rétablit la base.

**Commandes** (conteneur `db` démarré) :

| But | Commande | Vert si |
|---|---|---|
| base de test (lit le dossier monté) | `bash docker/create_test_db.sh` | sort 0 |
| SQL sur la base de test | depuis `docker/` : `docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d fil_rouge_test -c "<SQL>"'` | — |
| tests | depuis `docker/` : `docker compose exec -T api python -m pytest -q` (sqlmodel manque sur la machine) | 0 failed ; compte brut au compte rendu |
| typage | `pyright <fichiers .py touchés>` | 0 errors, compté avant et après |
| banc | `bash docker/compare_v2_v3.sh` (créé par LOT2) | `IDENTIQUES`, sort 0 |

**Invariants** :
- Code et SQL citent en commentaire la `Q-xx` qui les justifie ; les ADR viennent après (D1).
- Montants : `INTEGER` pour prix, budgets, bornes, part fixe ; `NUMERIC(12,2)` pour honoraires et paiement (`CLAUDE.md`, règle 4).
- Données reprises incomplètes : **vide (NULL)** si la colonne l'accepte, sinon une **valeur factice documentée** ; aucune ancienne donnée supprimée (Q-JEF-26).
- Jamais modifiés : `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack*/` (dont `PgSQL.sql`) ; `docker/init-v2/` après LOT1 ; `docker/docker-compose.yml`, hormis la ligne du montage en LOT1 (accord du 2026-10-07, cette ligne seule).
- La base de **dev** ne se recrée qu'en LOT11 : un seul `down -v` pour l'équipe (registre).

**Hors du lot** :
- grille de notes (Q-JEF-05), durée X (Q-ACC-21), routes d'anonymisation, d'auth et de clé d'API → chantier API (TODO n° 2) ;
- seed et faker → n° 3 ; ADR → n° 4 ; `livrables/2-modelisation/` → n° 6 ;
- les notes datées de `md/` et `livrables/` : des photos d'un jour, jamais repointées.

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `LOT1` | Créer init-v3 et basculer le montage | rien |
| `LOT2` | Écrire le banc « base neuve = base migrée » | `LOT1` |
| `LOT3` | Mandat : statuts de fin et signature | `LOT2` |
| `LOT4` | Mandat : six mois exacts et exclusivité | `LOT3` |
| `LOT5` | Paiement : note figée, taux borné, dates | `LOT2` |
| `LOT6` | Paramètres de rémunération et journal des notes | `LOT5` |
| `LOT7` | Personnes : coordonnées, priorité, dates | `LOT2` |
| `LOT8` | Localisation : pays, codes postaux, secteurs | `LOT7` |
| `LOT9` | Biens : énergie et auteur | `LOT8` |
| `LOT10` | Reprendre les anciens mandats | `LOT3` |
| `LOT11` | Clore le schéma v3 | `LOT3` à `LOT10` |
| `LOT12` | Ajouter le rôle en lecture seule | `LOT11` |

Une fiche à la fois : toutes écrivent `init-v3/01`. Hors dépendances écrites,
LOT5 à LOT10 peuvent changer d'ordre.

---

<!-- FICHE:LOT1 -->
## LOT1 [x] — Créer init-v3 et basculer le montage

**Session** : f6db559a-cd2c-449e-a160-bd4fd8d0475c
**Dépend de** : rien.
**Fichiers** : `docker/init-v2/*` (lu), `docker/init-v3/*` (créé), `docker/docker-compose.yml` (une ligne), `docker/create_test_db.sh`, `CLAUDE.md`, `CHANTIER.md`, `context AI/00-INDEX.md`, `context AI/08-etat.md`, `API/README.md`, `API/src/app/models/__init__.py`, `hunter_model.py`, `parameters_fees_model.py`, `search_request_model.py`, `API/tests/integration/conftest.py`, `API/tests/integration/test_constraints_db.py` — et rien d'autre.

**Prompt**
- Avant tout, mesure : `cd API && python -m pytest -q`, compte brut noté.
- Copie `docker/init-v2/` en `docker/init-v3/`, octet pour octet. En tête de
  `init-v3/README.md`, une ligne : v3 part de v2 le 2026-10-07 (chantier LOT),
  les changements suivent par thème.
- Dans `docker/docker-compose.yml`, change **seulement** le montage
  `./init-v2:/docker-entrypoint-initdb.d` en `./init-v3:…`.
- Repointe vers `init-v3` les renvois **vivants** des fichiers listés (grep
  `init-v2`). Une mention qui parle de v2 comme d'un état passé reste.
- `CLAUDE.md` : la règle 3 et « Où on en est » disent `init-v3` ; ajoute que
  `init-v2` est figé, gardé pour le banc. `CHANTIER.md` : la contrainte
  « schéma de référence » dit `init-v3`.
- Puis `docker compose up -d db` depuis `docker/` : le conteneur se recrée,
  le volume reste (la base de dev ne bouge pas).

**Critère de fin**
- `diff -r docker/init-v2 docker/init-v3` : seule la ligne d'en-tête du README diffère (compte brut des lignes du diff).
- `git diff --stat docker/docker-compose.yml` : `1 insertion(+), 1 deletion(-)`.
- `docker compose exec db head -1 /docker-entrypoint-initdb.d/README.md` rend la ligne v3 : le montage a basculé.
- `bash docker/create_test_db.sh` puis pytest : **le même compte** qu'avant la fiche.
- `grep -rl "init-v2" --exclude-dir=.git .` hors `md/`, `livrables/`, `docker/migrations/`, `docker/init-v2/`, `__pycache__` : chaque fichier restant, avec sa raison, au compte rendu.
<!-- /FICHE -->

---

<!-- FICHE:LOT2 -->
## LOT2 [x] — Écrire le banc « base neuve = base migrée »

**Session** : f6db559a-cd2c-449e-a160-bd4fd8d0475c
**Dépend de** : `LOT1`.
**Fichiers** : `docker/compare_v2_v3.sh` (créé), `docker/create_test_db.sh` (modèle, lu), `docker/migrations/v2-vers-v3/` (créé, avec un `.gitkeep`), `docker/init-v3/README.md` — et rien d'autre.

**Prompt**
- D'abord, cherche un outil existant qui compare deux schémas PostgreSQL
  (deux recherches au plus). Présente-le — nom, version, licence, lien, s'il
  est maintenu — à côté de l'option « script maison », et laisse choisir.
- Le banc, sur le modèle de `create_test_db.sh` (même `docker compose exec -T db`,
  même garde-fou contre la base de dev) :
  1. recrée `cmp_v2_migree` : `init-v2/01`, `02`, `03`, puis chaque
     `migrations/v2-vers-v3/*.sql` par ordre de nom ;
  2. recrée `cmp_v3_neuve` : `init-v3/01`, `02`, `03` ;
  3. les fichiers passent par l'entrée standard (`psql … < fichier`) :
     `init-v2` n'est plus monté ;
  4. compare une **description triée** : colonnes (nom, type, nullable,
     défaut), contraintes (`pg_get_constraintdef`), index, triggers,
     fonctions ; et le nombre de lignes par table ;
  5. rend `IDENTIQUES` et 0, ou le diff et 1 ; supprime ses deux bases.
- ⚠️ Pas de `pg_dump -s` brut : `ADD COLUMN` met la colonne en dernier, le
  `CREATE TABLE` de v3 ailleurs ; le diff serait faux.
- Les dossiers passent en variables (`V2_DIR`, `V3_DIR`, `MIG_DIR`), par
  défaut les vrais : les mutants jouent sur une copie temporaire.
- `init-v3/README.md` : une section « Vérifier v3 » (la commande, ce qu'elle prouve).

**Critère de fin**
- `bash docker/compare_v2_v3.sh` → `IDENTIQUES`, code 0 ; durée mesurée au compte rendu.
- Mutant : une copie temporaire de v3, plus `99_mutant.sql` (`ALTER TABLE role ADD COLUMN mutant int`) → code 1, et le diff nomme `role.mutant`.
- Contre-épreuve : la même colonne ajoutée **au milieu** du `CREATE TABLE role` de la copie v3 → `IDENTIQUES`.
<!-- /FICHE -->

---

<!-- FICHE:LOT3 -->
## LOT3 [x] — Mandat : statuts de fin et signature

**Session** : f6db559a-cd2c-449e-a160-bd4fd8d0475c
**Dépend de** : `LOT2`.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (tables `mandate`, `estate_proposed`), `docker/init-v3/02_migration.sql`, `docker/migrations/v2-vers-v3/03_mandat-statuts.sql`, `API/src/app/models/mandate_model.py`, `estate_proposed_model.py`, `API/tests/integration/test_constraints_db.py`, `docker/init-v3/README.md` ; le registre (cartes Q-REM-02, Q-REM-14, Q-MAN-05, Q-MAN-07, Q-MAN-09, Q-SCH-04) — et rien d'autre.

**Prompt**
- Lis les six cartes, puis applique :
  - le statut de fin du mandat quand la vente est perdue (Q-REM-02,
    Q-REM-14) ; la valeur exacte vient de la carte ; Jeff : « rien pour
    personne » (Q-JEF-03) ;
  - `is_client_signed` retiré : la date de signature et le statut
    `pending_signature` suffisent (Q-MAN-05, Q-MAN-09) ;
  - `chk_status_signature` permet `'canceled'` sans date de signature (Q-MAN-07) ;
  - `proposition_status` accepte `'signed'` (Q-SCH-04).
- `grep -rn is_client_signed API/ docker/init-v3/` : chaque usage suit ; les
  tests qui s'en servaient changent avec lui.

**Critère de fin**
- Tests nommés au compte rendu : chaque statut ajouté accepté ; `'canceled'` sans date accepté ; un statut inconnu refusé. Chacun tombe sous son mutant (socle).
- `grep -rn is_client_signed API/src docker/init-v3/01*` : 0 ligne de code.
- Banc `IDENTIQUES` ; pytest 0 failed (compte brut) ; pyright 0 errors.
<!-- /FICHE -->

---

<!-- FICHE:LOT4 -->
## LOT4 [x] — Mandat : six mois exacts et exclusivité

**Session** : f6db559a-cd2c-449e-a160-bd4fd8d0475c
**Dépend de** : `LOT3`.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (table `mandate` et le trigger d'exclusivité), `docker/init-v3/02_migration.sql`, `docker/migrations/v2-vers-v3/04_mandat-duree-exclusivite.sql`, `API/src/app/models/mandate_model.py`, `API/tests/integration/test_constraints_db.py`, `docker/init-v3/README.md` ; le registre (cartes Q-MAN-01, Q-MAN-02) — et rien d'autre.

**Prompt**
- Remplace le CHECK de `ends_at` par « exactement 6 mois » ; il est déjà
  rédigé en commentaire (grep `U05` dans `init-v3/01`) (Q-MAN-01).
- Corrige le trigger d'exclusivité — le mandat parent exclu du contrôle — et
  **active-le** (Q-MAN-02). Un exclusif annulé libère le bien **tout de
  suite** (Q-JEF-06).
- Avant d'activer, compte sur la base de test les mandats repris qui
  violeraient l'une ou l'autre règle. Plus de 0 : arrête-toi et montre-les ;
  leur reprise ne s'invente pas.
- L'exemple de Bruno (mandat de 9 mois, `test_remuneration.py`) est voulu :
  registre, « Défauts du sujet ». Ne le « corrige » pas.

**Critère de fin**
- Tests nommés : 6 mois accepté, 7 mois refusé ; 2e exclusif actif pour le même client refusé (✏️ 2026-10-07 : la règle Q-MAN-02 vaut par client, pas par bien) ; accepté après annulation du 1er ; renouvellement (parent) accepté.
- Mutants : CHECK v2 remis → le test « 7 mois refusé » tombe ; `DROP TRIGGER` → le test « 2e exclusif refusé » tombe.
- Banc `IDENTIQUES` ; pytest 0 failed (compte brut) ; pyright 0 errors.
<!-- /FICHE -->

---

<!-- FICHE:LOT5 -->
## LOT5 [x] — Paiement : note figée, taux borné, dates

**Session** : f6db559a-cd2c-449e-a160-bd4fd8d0475c
**Dépend de** : `LOT2`.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (table `payment`), `docker/migrations/v2-vers-v3/05_paiement.sql`, `API/src/app/models/payment_model.py`, `API/tests/integration/test_constraints_db.py`, `docker/init-v3/README.md`, `user-stories/07_*.feature` (lu) ; le registre (cartes Q-REM-03, Q-REM-04, Q-REM-10, Q-REM-17, Q-REM-19) — et rien d'autre.

**Prompt**
- D'abord la question ouverte (Q-REM-17). La facture est hors périmètre
  (Q-JEF-23) ; restent `announced_at` et `scheduled_for`. Lis les étapes du
  paiement dans `user-stories/07_*.feature`, puis pose un questionnaire :
  les deux, une, ou aucune — avec ce que chaque option change. Rien
  d'ajouté avant la réponse.
- Puis applique :
  - `performance_score` figé sur le paiement (Q-REM-03) ;
  - `calculation_details` en `JSONB` (Q-REM-04) ;
  - `final_rate` dans `chk_refused` (Q-REM-10) — lis ses conditions en entier avant d'y toucher ;
  - `CHECK (final_rate BETWEEN 0.20 AND 0.60)` (Q-REM-19, validé par Jeff : Q-JEF-01).
- Rien de la facture : ni table, ni `invoice_reference`, `invoice_submitted_at`, `verified_at`.

**Critère de fin**
- Tests nommés : `final_rate` 0,19 et 0,61 refusés ; 0,20 et 0,60 acceptés ; la règle de `chk_refused` sur `final_rate`, dans les deux sens. Chacun tombe sous son mutant.
- `grep -rn "invoice" docker/init-v3/01* API/src` : 0 ligne.
- Banc `IDENTIQUES` ; pytest 0 failed, les 55 cas de rémunération compris ; pyright 0 errors.
<!-- /FICHE -->

---

<!-- FICHE:LOT6 -->
## LOT6 [x] — Paramètres de rémunération et journal des notes

**Session** : 2d7571c9-43ae-4070-aa12-3b61e30184b2
**Dépend de** : `LOT5`.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (tables `parameters_fees`, `commission_scale`, `sale`, `hunter_performance`, et la nouvelle `remuneration_parameters`), `docker/init-v3/02_migration.sql`, `docker/migrations/v2-vers-v3/06_parametres.sql`, `API/src/app/models/` (`parameters_fees_model.py`, `commission_scale_model.py`, `sale_model.py`, `hunter_performance_model.py`, `remuneration_parameters_model.py` créé, `__init__.py`), `API/src/app/main.py`, `API/tests/integration/test_constraints_db.py`, `docker/init-v3/README.md` ; le registre (cartes Q-REM-05, Q-REM-13, Q-SCH-06, Q-SCH-15, Q-SCH-17) — et rien d'autre.

**Prompt**
- Table `remuneration_parameters` d'après la carte Q-REM-05 ; relâche les
  deux CHECK qu'elle remplace (v2 `01:758-759`). Expose-la comme les 18
  autres (le motif est dans l'en-tête de `main.py`).
  ⚠️ La grille de notes (Q-JEF-05) n'y entre **pas** : chantier API. Si la
  carte exige de l'y stocker, arrête-toi et demande.
- `parameters_fees` : `effective_from` et `UNIQUE` ; `valid_until` et
  l'`EXCLUDE` retirés (Q-SCH-17).
- Taux de tranche `> 0` (Q-SCH-15).
- Clé de `sale` vers `parameters_fees` (Q-REM-13) ; les ventes reprises la
  reçoivent dans `02` et dans la migration.
- `hunter_performance` en journal : `scored_at`, 2 `UNIQUE`, 1 index ;
  `valid_from`, `valid_until` et leurs 2 contraintes retirés (Q-SCH-06).

**Critère de fin**
- Tests nommés : taux de tranche 0 refusé ; deux grilles à la même `effective_from` refusées ; vente vers une grille inconnue refusée ; doublon du journal refusé. Chacun tombe sous son mutant.
- `\dt` sur la base de test : 19 tables (compte brut).
- Banc `IDENTIQUES` ; pytest 0 failed, les 55 cas de rémunération compris ; pyright 0 errors.
<!-- /FICHE -->

---

<!-- FICHE:LOT7 -->
## LOT7 [x] — Personnes : coordonnées, priorité, dates

**Session** : 0ceba605-10f5-42b6-9317-73b2243eb990
**Dépend de** : `LOT2`.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (tables `client`, `hunter`, `real_estate_manager`, `role`), `docker/init-v3/02_migration.sql`, `docker/migrations/v2-vers-v3/07_personnes.sql`, `API/src/app/models/` (`client_model.py`, `hunter_model.py`, `real_estate_manager_model.py`, `role_model.py`), `API/tests/integration/test_constraints_db.py`, `docker/init-v3/README.md` ; le registre (cartes Q-SCH-01, Q-SCH-18, Q-PRO-08, Q-MIG-07, Q-SCH-05, Q-SCH-09, Q-SCH-10) — et rien d'autre.

**Prompt**
- 18 clients repris : adresse « non renseigné », code postal `00000` ;
  l'`ALTER` sort de `02` (Q-SCH-01, Q-SCH-18 ; v2 `02:64-66`, `02:148-165`).
- CHECK de format des téléphones, 3 tables, au format d'ADR-007 (indicatif
  `+` compris). Les 4 `0000000000` deviennent `+33000000000`, documenté au
  README (Q-PRO-08, Q-MIG-07). ⚠️ Le CHECK doit accepter `+33000000000`.
- Priorité du client en `SMALLINT`, `CHECK` de 1 à 5 (Q-SCH-05, Q-JEF-18).
- `created_at` sur `client`, `hunter`, `real_estate_manager`, `role` (Q-SCH-09).
- `is_cartet` devient `is_carte_t` : colonne, modèle, migration, et chaque
  usage (`grep -rn is_cartet`) (Q-SCH-10).

**Critère de fin**
- Tests nommés : `0612345678` refusé ; `+33612345678` et `+33000000000` acceptés ; priorité 0 et 6 refusées, 1 et 5 acceptées. Chacun tombe sous son mutant.
- `grep -rn is_cartet API/src docker/init-v3/01*` : 0 ligne.
- Banc `IDENTIQUES` ; pytest 0 failed (compte brut) ; pyright 0 errors.
<!-- /FICHE -->

---

<!-- FICHE:LOT8 -->
## LOT8 [x] — Localisation : pays, codes postaux, secteurs

**Session** : 0ceba605-10f5-42b6-9317-73b2243eb990
**Dépend de** : `LOT7`.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (tables `client`, `criteria`, `estate`), `docker/init-v3/02_migration.sql`, `docker/init-v3/03_populate_estate.sql`, `docker/migrations/v2-vers-v3/08_localisation.sql`, `API/src/app/models/` (`client_model.py`, `criteria_model.py`, `estate_model.py`), `API/tests/integration/test_constraints_db.py`, `docker/init-v3/README.md` ; le registre (cartes Q-SCH-11, Q-SCH-12, Q-MIG-08, Q-MIG-09) — et rien d'autre.

**Prompt**
- `country_iso = 'FR'` sur les biens (dans `03`, et par `UPDATE` dans la
  migration), **puis** le CHECK du code postal par pays (Q-SCH-11).
  Recompte d'abord : le registre dit 2 556 codes conformes sur 2 556
  (2026-10-05).
- Eircode sans espace, sur `client` et `criteria` (Q-SCH-12, confirmé le 2026-10-07).
- Secteurs de `criteria` : ville, code postal et pays `'FR'` ; une colonne
  quartier facultative sur `criteria` et `estate`, nom proposé `district`
  (Q-MIG-08 ; v2 `02:192-208`).
- `budget_min` à NULL sur les 17 critères repris ; corrige le commentaire de
  v2 `02:189` (Q-MIG-09).

**Critère de fin**
- `SELECT count(*) FROM estate WHERE country_iso = 'FR'` : même nombre sur les deux bases du banc, égal au total des biens (comptes bruts).
- Tests nommés : code postal FR à 4 chiffres refusé, à 5 accepté ; Eircode avec espace refusé, sans espace accepté. Chacun tombe sous son mutant.
- Banc `IDENTIQUES` ; pytest 0 failed (compte brut) ; pyright 0 errors.
<!-- /FICHE -->

---

<!-- FICHE:LOT9 -->
## LOT9 [x] — Biens : énergie et auteur

**Session** : 0ceba605-10f5-42b6-9317-73b2243eb990
**Dépend de** : `LOT8`.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (table `estate`), `docker/init-v3/03_populate_estate.sql`, `docker/migrations/v2-vers-v3/09_biens.sql`, `API/src/app/models/estate_model.py`, `API/tests/integration/test_constraints_db.py`, `docker/init-v3/README.md`, `normalised/annonces_normalised.csv` (lu) ; le registre (cartes Q-MIG-05, Q-MIG-06, Q-ACC-09) — et rien d'autre.

**Prompt**
- `energy_class` rempli depuis `dpe` dans `03` ; vide (NULL) pour les biens
  sans lettre (Q-MIG-06). Le registre compte 1 623 et 933 (2026-10-06) :
  recompte avant d'écrire.
- Colonnes d'énergie laissées vides ; `energetic_score` retiré, NULL sur
  tous les biens (Q-MIG-05).
- Colonne d'**auteur** sur `estate` : un bien peut être saisi à la main par
  un chasseur ou un manager, vide = import (Q-ACC-09, Q-JEF-24). Le
  registre n'en fixe ni le nom, ni le type, ni la clé : pose un
  questionnaire avant de l'écrire.

**Critère de fin**
- `count(energy_class)` et `count(*) WHERE energy_class IS NULL` : mêmes nombres sur les deux bases du banc, égaux au recompte (comptes bruts).
- `grep -rn energetic_score API/src docker/init-v3/01*` : 0 ligne.
- Test nommé : un auteur inconnu refusé ; il tombe sous son mutant.
- Banc `IDENTIQUES` ; pytest 0 failed (compte brut) ; pyright 0 errors.
<!-- /FICHE -->

---

<!-- FICHE:LOT10 -->
## LOT10 [x] — Reprendre les anciens mandats

**Session** : 0ceba605-10f5-42b6-9317-73b2243eb990
**Dépend de** : `LOT3`.
**Fichiers** : `docker/init-v3/02_migration.sql`, `docker/migrations/v2-vers-v3/10_reprise-mandats.sql`, `docker/init-v3/README.md`, `PgSQL.sql` du StarterPack (lu ; `find` pour son chemin) ; le registre (cartes Q-MIG-03, Q-MIG-10, Q-MIG-12, Q-MIG-13) — et rien d'autre.

**Prompt**
- Les 6 mandats échus passent en `'expired'` (Q-MIG-10).
- Le mandat 13 se rattache à la fiche client de Nina Girard, déjà dans les
  fixtures (`PgSQL.sql:103`, rôle `client`) ; pas de compte en plus (Q-MIG-12).
- `termine` → `completed`, `suspendu` → `canceled`, pas de pause : écrit dans
  `02` et au README (Q-MIG-13, Q-JEF-13).
- Les 17 demandes restent en `'launched'`, pas de nouvel état (Q-MIG-03 ;
  v2 `02:241-246`) : vérifie, sans doute rien à changer.

**Critère de fin**
- Sur les deux bases du banc, mêmes réponses (comptes bruts) : mandats repris en `'expired'` = 6 ; client du mandat 13 = Nina Girard ; demandes en `'launched'` = 17.
- Mutant : l'`UPDATE` des échus retiré d'une copie de la migration → `cmp_v2_migree` ne rend plus 6.
- Banc `IDENTIQUES` ; pytest 0 failed (compte brut).
<!-- /FICHE -->

---

<!-- FICHE:LOT11 -->
## LOT11 [x] — Clore le schéma v3

**Session** : 0ceba605-10f5-42b6-9317-73b2243eb990
**Dépend de** : `LOT3` à `LOT10`.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (3 commentaires), `docker/init-v3/README.md`, `CLAUDE.md`, le registre (liste « Lot de migration qui en découle », carte Q-MAN-06) — et rien d'autre.

**Prompt**
- Les 3 TODO annotés « contrôlé par l'API », commentaires seuls (Q-MAN-06 ;
  v2 `01:639-641`, `01:664-668`, `01:789-795`).
- Relis `init-v3/README.md` en entier : chaque ligne de la liste du registre
  y a sa ligne et sa `Q-xx`. Compte les deux, et nomme l'écart s'il y en a.
- `CLAUDE.md`, « Où on en est » : v3, et ce qui change pour l'équipe.
- La base de dev : `docker compose down -v && docker compose up -d` depuis
  `docker/`. ⚠️ Elle efface la base de dev locale : demande avant de lancer.
- Prépare le message à l'équipe : un bloc copiable, markdown Discord, moins
  de 2 000 caractères (compte-les) ; ce qu'il faut relancer chez soi.

**Critère de fin**
- Banc `IDENTIQUES` ; pytest 0 failed (compte brut, contre 123 avant le chantier) ; pyright 0 errors sur les `.py` touchés par le chantier.
- `docker compose ps` : `db` en `healthy` ; `\dt` sur la base de dev : 19 tables.
- Registre et README : mêmes comptes de changements (comptes bruts).
<!-- /FICHE -->

---

<!-- FICHE:LOT12 -->
## LOT12 [ ] — Ajouter le rôle en lecture seule

**Dépend de** : `LOT11`.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (table `role`), un script d'init `docker/init-v3/04_*` si le mot de passe doit venir de l'environnement, `docker/.env.exemple`, `docker/migrations/v2-vers-v3/12_role-lecture-seule.sql`, `API/src/app/models/role_model.py`, `API/tests/integration/test_constraints_db.py`, `docker/init-v3/README.md` ; le registre (ligne « Rôle en lecture seule ») — et rien d'autre.

**Prompt**
- ⏸️ D'abord : Jeff a-t-il répondu sur Discord (Q14) ? Demande-le. Sa réponse
  va au registre, ligne « Rôle en lecture seule ». Pas de réponse, ou
  « non » : arrête-toi, rien d'écrit.
- Si oui : un rôle PostgreSQL en lecture seule (`GRANT SELECT` sur les tables,
  présentes et futures), et un rôle applicatif « lecteur » dans `role`.
- Un rôle PostgreSQL vit dans le cluster, partagé par les bases du banc : sa
  création est idempotente.
- Son mot de passe vient de `docker/.env`, jamais de git ; la variable
  s'ajoute à `docker/.env.exemple`, sans valeur. ⚠️ Si la passer au conteneur
  touche `docker-compose.yml`, arrête-toi et demande : l'accord du
  2026-10-07 ne couvrait que le montage.

**Critère de fin**
- Connecté avec ce rôle : `SELECT` accepté, `INSERT` refusé (`permission denied`) ; test nommé, qui tombe sous le mutant `GRANT INSERT`.
- Banc `IDENTIQUES` ; pytest 0 failed (compte brut) ; pyright 0 errors.
<!-- /FICHE -->

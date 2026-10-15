> **QUAND LIRE** : on joue une fiche `PRF*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache PRF<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier PRF — Refacto des profils

**Ouvert.** le 2026-10-15.

**À quoi il sert.** Les 11 FK `id_client` / `id_hunter` / `id_realestatemanager`
portent un `user.id` (le `sub` du JWT) au lieu du numéro de la fiche, et le rôle
vit sur le compte. Le chantier fait viser la PK des fiches et sort le rôle du compte.

**Estimé.** 10 fiches · ≈48 $ — ≈4,81 $/fiche sur 7 clos (le 2026-10-15).

**CLOS** le 2026-10-15. Ne se rejoue pas — ne sert plus qu'à relire son socle.

**Fait.** PRF1..PRF9 (2026-10-15) : Les 11 FK visent la PK des fiches, le rôle vit sur la fiche ou sur user.system_role, une fiche au plus par compte (trigger), id_role retiré, ADR-057 codé — estimé 10 fiches ≈48 $ · cadré 9 · joué 9 fiches 62,51 $.

**Session** : f022f081-0f47-40d8-a130-39e8bee7a307

## Le socle commun

Le code vit dans `../Fil-Rouge-API/` ; tout chemin ci-dessous s'y lit. Vérification :
depuis `docker/`, `docker compose exec -T api python -m pytest -q` (961 passed,
7 xfailed au 2026-10-14 : à remesurer au début de chaque fiche). Après toute
modification de `docker/init-v3/01`, `02` ou `04` : `bash docker/create_test_db.sh`.
Signature changée : grep de tous les appelants, puis `pyright` sur tout `API/src`.

**Décisions de Seb** (Discord, 2026-10-15 ; maquette
https://claude.ai/artifact/YNT5ANwbWYKp6SERVvvn9K) :
- les 11 FK visent `client(id)`, `hunter(id)`, `real_estate_manager(id)` ; les
  noms de colonnes et du JSON ne changent pas, leurs **valeurs** si ;
- `id_author` (`search_request`, `criteria`, `estate`, `estate_contact`) reste
  vers `"user"(id)` : seules ces 4 colonnes et les 3 `id_user` des fiches citent `user` ;
- `user.id_role` disparaît ; `user.system_role VARCHAR(10) CHECK (system_role IN
  ('Admin', 'Reader'))`, vide pour un compte qui a une fiche ;
- chaque fiche porte `role_wording VARCHAR(20) NOT NULL DEFAULT '<Rôle>' CHECK
  (role_wording = '<Rôle>') REFERENCES role(wording)` ; `role` garde 3 lignes :
  `'Client'`, `'Hunter'`, `'Manager'` (nom gardé) ;
- **une fiche au plus par compte**, et pas de fiche pour un compte à
  `system_role` : garanti par un **trigger** ; sans fiche ni `system_role` = 403 ;
- **noms et places fixés** (le MPD cible de Gabriel les recopie, 2026-10-15) :
  `system_role` prend la place de `id_role` dans `"user"` ; `role_wording` suit
  `id_user` dans chaque fiche ; fonction `check_one_profile_per_user()`, triggers
  `trg_client_one_profile`, `trg_hunter_one_profile`,
  `trg_real_estate_manager_one_profile` et `trg_user_system_role` ;
- `AbstractPerson` : classe SQLModel sans table, champs `created_at`, `id_user`,
  `first_name`, `last_name`, `phone_number`, `country_iso` (facultatif ;
  `Client` le redéclare obligatoire), `gender` ;
- le jeton ne porte que `sub` (ADR-052) ; le numéro de fiche se lit en base à
  chaque requête, jamais dans le jeton.

| Symbole | Fichier | Rôle |
|---|---|---|
| `Principal`, `get_principal`, `require_roles` | `API/src/app/utils/roles.py` | le compte connecté et son rôle |
| `get_current_user` | `API/src/app/utils/current_user.py` | le compte du jeton |
| `requests_of`, `mandates_of`, `owns_request`… | `API/src/app/services/client_rows.py` | « le sien » du Client |
| `requests_handled_by`, `handles_mandate`… | `API/src/app/services/hunter_rows.py` | « le sien » du Hunter |
| `build_vente` | `API/src/app/services/payment_calculation_service.py` | cherche le chasseur d'une vente |
| `test_banc_v2_v3` | `API/tests/integration/test_banc_v2_v3.py` | `01` + `02` neufs = base v2 + `migrations/v2-vers-v3/*.sql` |

**Une fiche de schéma** change `docker/init-v3/01` (et `02` si des données
bougent) **et** écrit sa migration jumelle dans `docker/migrations/v2-vers-v3/` :
45 pour `PRF2`, 46 pour `PRF6`, 47 pour `PRF8`. Le banc garde les deux alignés.
**Un test qui touche une fiche** en crée une neuve où `id ≠ id_user` : dans la
base de test, les 6 `hunter` ont `id = id_user` et cachent l'erreur
(Fil-Rouge-API `7e40e8d`), jusqu'à `PRF5` ; les 18 `client` et le manager ne
l'ont pas (compté le 2026-10-15) : entre `PRF2` et `PRF3`/`PRF4`, des tests du
Client et du Manager tombent — on les compte, on ne commite pas PRF2 seul en rouge.

Hors du chantier : le MPD (`vrac/v9.drawio`) et Confluence (le groupe) ; l'ADR du
chasseur IA (ADR-058, écrit à part) ; l'avis de Robin (Seb : on n'attend pas) ;
`docker/docker-compose.yml`.

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `PRF1` | Poser `AbstractPerson` | rien |
| `PRF2` | Faire viser la PK des fiches aux 11 FK, côté base | rien |
| `PRF3` | Basculer « le sien » du Client sur `client.id` | `PRF2` |
| `PRF4` | Basculer « le sien » du Hunter et du Manager, `build_vente` et le seed | `PRF2` |
| `PRF5` | Décaler les `id` des fiches dans la base de test | `PRF3`, `PRF4` |
| `PRF6` | Ajouter `system_role`, `role_wording` et le trigger, côté base | `PRF2` |
| `PRF7` | Lire le rôle sur la fiche ou sur `system_role` | `PRF5`, `PRF6` |
| `PRF8` | Retirer `user.id_role` | `PRF7` |
| `PRF9` | Écrire l'ADR, le README, la matrice des droits | `PRF8` |

`PRF1` se joue à tout moment. `PRF3` et `PRF4` sont indépendantes l'une de l'autre.
Les migrations se suivent : `PRF2` avant `PRF6` avant `PRF8`.

---

<!-- FICHE:PRF1 -->
## PRF1 [x] — Poser `AbstractPerson`

**Session** : 2531ac4a-0b87-425d-960c-b4cd009e06ba
**Dépend de** : rien.
**Fichiers** : `API/src/app/models/abstract_person_model.py` (neuf),
`models/client_model.py`, `models/hunter_model.py`,
`models/real_estate_manager_model.py`, `models/__init__.py`,
`API/tests/test_user_models.py` — et rien d'autre.

**Prompt**
Crée `AbstractPerson(SQLModel)`, **sans** `table=True`, avec les 7 champs du socle,
recopiés des trois classes (types, `max_length`, défauts). `Client`, `Hunter` et
`RealEstateManager` en héritent et ne gardent que leurs champs propres ; `Client`
redéclare `country_iso: str` obligatoire. Les `description=` du Swagger propres à
chaque classe (ex. `HUNTER_USER` sur `id_user`) restent : redéclare le champ dans
la classe fille si besoin. Aucune table ne change. Mets à jour les docstrings
d'en-tête des trois modèles.

**Critère de fin**
Avant de toucher au code, enregistre `GET /openapi.json` ; après, il est
identique (diff vide). Le nouveau test `test_profiles_share_abstract_person`
(`tests/test_user_models.py`) vérifie l'héritage et les 7 champs ; mutant : retirer
`gender` d'`AbstractPerson` le fait tomber. pytest au même compte qu'avant
(comptes bruts), `pyright` sur les fichiers touchés : 0 erreur.
<!-- /FICHE -->

---

<!-- FICHE:PRF2 -->
## PRF2 [x] — Faire viser la PK des fiches aux 11 FK, côté base

**Session** : 2531ac4a-0b87-425d-960c-b4cd009e06ba
**Dépend de** : rien.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql`,
`docker/init-v3/02_migration.sql`,
`docker/migrations/v2-vers-v3/45_cles-vers-les-fiches.sql` (neuf), les
`foreign_key=` des modèles qui citent `client.id_user`, `hunter.id_user` ou
`real_estate_manager.id_user`, `API/tests/integration/test_fk_fiches.py` (neuf).

**Prompt**
Dans `01`, les 11 `REFERENCES … (id_user)` visent `(id)` ; réécris les
`COMMENT ON COLUMN` de fin de script. Dans `02`, les valeurs insérées dans ces
11 colonnes deviennent des numéros de fiche (jointure par `id_user`) : compte
d'abord combien de lignes les citent. La migration 45 : retire les 11 FK et les
4 FK composées (`search_request (id, id_client)`, `mandate (id, id_client)`,
`mandate (id, id_hunter)`, `payment (id, id_hunter)`), convertit les valeurs par
`UPDATE … FROM <fiche> WHERE <fiche>.id_user = <colonne>`, puis recrée le tout.
En-tête au format de `44_parametres-de-depart.sql`. Modèles : le `foreign_key=`
suit. Le nouveau test lit `pg_constraint` : aucune FK ne vise `id_user` d'une
fiche ; seules les 3 `id_user` des fiches et les 4 `id_author` visent `"user"(id)`.

**Critère de fin**
`bash docker/create_test_db.sh`, puis pytest : tout passe, banc v2/v3 compris
(comptes bruts). Mutant : remettre une `REFERENCES hunter(id_user)` dans `01` fait
tomber `test_fk_fiches`. Le compte rendu redit à l'équipe : base de dev à refaire
(`docker compose down -v && docker compose up -d`) ou migration 45 à jouer.
<!-- /FICHE -->

---

<!-- FICHE:PRF3 -->
## PRF3 [x] — Basculer « le sien » du Client sur `client.id`

**Session** : 2531ac4a-0b87-425d-960c-b4cd009e06ba
**Dépend de** : `PRF2`.
**Fichiers** : `utils/roles.py`, `utils/current_user.py`, `services/client_rows.py`,
`services/client_service.py`, `services/search_request_service.py`,
`services/mandate_service.py`, `services/anonymization_service.py`,
`services/signup_service.py` (sous `API/src/app/`), un test d'intégration neuf
`API/tests/integration/test_sien_client_fiche.py`.

**Prompt**
Le numéro de fiche se lit **une fois par requête** : `Principal` gagne
`profile_id: Optional[int]`, rempli par `get_principal` (la fiche du compte,
`None` sans fiche). Ajoute `get_current_client` dans `current_user.py` : la fiche
`Client` du compte, 403 sans fiche. Partout où « le sien » du Client compare
`id_client` à `user.id`, compare-le à `profile_id`. Les fonctions de
`client_rows.py` prennent un `client_id` (renomme le paramètre `user_id`) ; grep
de leurs appelants. `anonymization_service.py` cherche les mandats par
`client.id`. Docstrings et en-têtes suivent.

**Critère de fin**
Le test neuf crée un client dont `id ≠ id_user` (fiche bouche-trou créée avant),
avec une demande et un mandat ; il voit les siens, pas ceux d'un autre client
(404). Mutant : remettre `user.id` dans `mandates_of` le fait tomber. pytest tout
vert, `pyright` 0 erreur sur `API/src` (comptes bruts).
<!-- /FICHE -->

---

<!-- FICHE:PRF4 -->
## PRF4 [x] — Basculer « le sien » du Hunter et du Manager, `build_vente` et le seed

**Session** : 2531ac4a-0b87-425d-960c-b4cd009e06ba
**Dépend de** : `PRF2`.
**Fichiers** : sous `API/src/app/` : `utils/current_user.py`, `services/hunter_rows.py`,
`services/hunter_service.py`, `services/real_estate_manager_service.py`,
`services/estate_proposed_service.py`, `services/estate_search_request_service.py`,
`services/commission_scale_service.py`, `services/hunter_performance_service.py`,
`services/payment_service.py`, `services/payment_calculation_service.py`,
`services/mandate_service.py`, `scripts/seed_demo.py` ; test neuf
`API/tests/integration/test_sien_hunter_fiche.py`.

**Prompt**
Si `PRF3` est jouée, réutilise `Principal.profile_id` ; sinon, ajoute-le comme elle
le décrit. Ajoute `get_current_hunter` et `get_current_manager`. Partout où « le
sien » du Hunter ou du Manager compare `id_hunter` / `id_realestatemanager` à
`user.id`, compare-le à `profile_id` ; les fonctions de `hunter_rows.py` prennent
un `hunter_id`. `build_vente` et `seed_demo.py` cherchent le chasseur par
`hunter.id`. Grep des appelants de chaque signature changée.

**Critère de fin**
Le test neuf crée un chasseur et un manager dont `id ≠ id_user`, un mandat et une
vente : le chasseur voit son mandat, pas celui d'un autre (404) ; le manager voit
son chasseur ; `build_vente` rend ce chasseur. Mutant : remettre `user.id` dans
`handles_mandate` le fait tomber. Seed rejoué sur la base de dev sans erreur.
pytest tout vert, `pyright` 0 erreur sur `API/src` (comptes bruts).
<!-- /FICHE -->

---

<!-- FICHE:PRF5 -->
## PRF5 [x] — Décaler les `id` des fiches dans la base de test

**Session** : 2531ac4a-0b87-425d-960c-b4cd009e06ba
**Dépend de** : `PRF3`, `PRF4`.
**Fichiers** : `docker/create_test_db.sh`, les tests qui tombent (à nommer après mesure).

**Prompt**
Dans la base de test seulement, les fiches de `02` reçoivent des `id ≠ id_user`
(par exemple : redémarrer l'identité des 3 tables de fiche à 1001 entre `01` et
`02` ; lis d'abord comment `02` insère ces lignes). La base de dev ne change pas.
Lance pytest et **compte** les tests qui tombent : chacun supposait `id = id_user`
(voir Fil-Rouge-API `7e40e8d`) ; corrige le test, ou le code s'il s'agit d'un oubli
de `PRF3` / `PRF4`. Plus de 15 tests qui tombent : arrête-toi et rends la liste.

**Critère de fin**
Dans `fil_rouge_test`, `SELECT count(*) … WHERE id = id_user` vaut 0 pour
`client`, `hunter` et `real_estate_manager`. pytest tout vert (comptes bruts,
et le nombre de tests corrigés). Mutant : remettre `user.id` dans
`requests_of` fait tomber au moins un test existant.
<!-- /FICHE -->

---

<!-- FICHE:PRF6 -->
## PRF6 [x] — Ajouter `system_role`, `role_wording` et le trigger, côté base

**Session** : 719fade3-b24b-449b-b610-afa4674442a1
**Dépend de** : `PRF2`.
**Fichiers** : `docker/init-v3/01_create_fil_rouge_immobilier.sql`,
`docker/init-v3/02_migration.sql`, `docker/init-v3/04_role-lecture-seule.sql`,
`docker/migrations/v2-vers-v3/46_roles-des-fiches.sql` (neuf),
`models/user_model.py`, les 3 modèles de fiche, test neuf
`API/tests/integration/test_une_fiche_par_compte.py`.

**Prompt**
Ajout seulement : `user.id_role` reste. **Mesure d'abord**, en dev et en test :
comptes présents dans 2 tables de fiche ou plus ; comptes `Admin` / `Reader` qui
ont une fiche. Un compte au-dessus de 0 : arrête-toi et rends la liste. Sinon,
ajoute `system_role` (rempli depuis `id_role` pour Admin et Reader), les 3
`role_wording` du socle, et un trigger : une fiche refusée si le compte a déjà
une autre fiche ou un `system_role` ; un `system_role` refusé sur un compte qui a
une fiche. `04` ouvre `system_role` au lecteur (`GRANT SELECT (…) ON "user"`).
Modèles : les champs suivent, `role_wording` a pour défaut le rôle de la classe.

**Critère de fin**
Le test neuf : une 2e fiche pour le même compte est refusée (409) ; un
`system_role` sur un compte à fiche aussi. Mutant : supprimer le trigger le fait
tomber. Banc v2/v3 et pytest tout verts (comptes bruts).
<!-- /FICHE -->

---

<!-- FICHE:PRF7 -->
## PRF7 [x] — Lire le rôle sur la fiche ou sur `system_role`

**Session** : 719fade3-b24b-449b-b610-afa4674442a1
**Dépend de** : `PRF5`, `PRF6`.
**Fichiers** : sous `API/src/app/` : `utils/roles.py`, `services/signup_service.py`,
`services/user_service.py`, `routes/user_router.py`, `scripts/create_admin.py`,
`scripts/seed_demo.py` ; `API/tests/test_roles.py`.

**Prompt**
`get_principal` lit le rôle sur `system_role`, sinon sur la fiche du compte
(`role_wording`) ; ni l'un ni l'autre : 403. Plus aucune lecture de `id_role`
dans `API/src`. L'inscription crée la fiche, qui porte son rôle ;
`create_admin.py` pose `system_role = 'Admin'` ; `ADMIN_ONLY_FIELDS`
(`user_service.py`) remplace `id_role` par `system_role`. `id_role` s'écrit encore
(NOT NULL) jusqu'à `PRF8`.

**Critère de fin**
`grep -rn "id_role" API/src/app` ne rend plus que les écritures et le modèle (compte
brut). Tests : un compte Client, Hunter, Manager, Admin, Reader reçoit le bon rôle ;
un compte sans fiche ni `system_role` reçoit 403. Mutant : faire lire `id_role` à
`get_principal` fait tomber le test du Reader. pytest tout vert, `pyright` 0 erreur.
<!-- /FICHE -->

---

<!-- FICHE:PRF8 -->
## PRF8 [x] — Retirer `user.id_role`

**Session** : 719fade3-b24b-449b-b610-afa4674442a1
**Dépend de** : `PRF7`.
**Fichiers** : `docker/init-v3/01`, `02`, `04`,
`docker/migrations/v2-vers-v3/47_sans-id-role.sql` (neuf), `models/user_model.py`,
`models/role_model.py`, et les tests qui citent `id_role` (20 fichiers au
2026-10-15 : à recompter).

**Prompt**
Supprime `user.id_role` (colonne, FK, modèle, écritures restantes). `role` ne
garde que `'Client'`, `'Hunter'`, `'Manager'` : son CHECK suit. `04` retire
`id_role` de la liste des colonnes ouvertes au lecteur. La migration 47 fait de
même sur une base existante. Les tests qui écrivaient `id_role` passent par
`system_role` ou par une fiche.

**Critère de fin**
`grep -rnw "id_role" API docker` ne rend plus que l'historique (migrations
anciennes, `init-v2`) : compte brut. Banc v2/v3 et pytest tout verts (comptes
bruts). Mutant : remettre `'Admin'` dans le CHECK de `role` fait tomber le banc.
Base de dev refaite (`docker compose down -v && docker compose up -d` depuis
`docker/`), puis `docker compose exec api python -m src.app.scripts.seed_demo`
rejoué sans erreur (sortie recopiée). Le compte rendu redit à l'équipe : base à
refaire et seed à rejouer après le pull.
<!-- /FICHE -->

---

<!-- FICHE:PRF9 -->
## PRF9 [x] — Écrire l'ADR, le README, la matrice des droits

**Session** : 719fade3-b24b-449b-b610-afa4674442a1
**Dépend de** : `PRF8`.
**Fichiers** : `md/securite/matrice-droits-crud-par-role.md`, `../Fil-Rouge-API/API/README.md`,
`../Fil-Rouge-API/docker/init-v3/README.md` §0,
`../Fil-Rouge-API/API/src/app/models/field_descriptions.py` ; à relire seulement :
`md/adr/adr-057-cles-et-roles-des-fiches.md`.

**Prompt**
L'ADR-057 est déjà écrit (le Glaude, 2026-10-15, choix de Seb) : le relire, et
signaler tout écart avec le code livré, sans le réécrire. La matrice et les deux README disent `system_role`, le rôle par
la fiche, et « une fiche au plus ». Le Swagger dit que `id_client` est un
`client.id` (et de même pour les deux autres). Grep des anciennes phrases
(« numéro du compte », `user.id` sous ces champs) dans les deux dépôts.

**Critère de fin**
Le grep des anciennes phrases rend 0 reste vivant (compte brut) ; `GET
/openapi.json` montre la nouvelle description sous `id_client`. pytest tout vert.
<!-- /FICHE -->

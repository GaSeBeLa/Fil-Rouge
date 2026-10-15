# Qui peut faire quoi — la matrice des droits

> 📅 **13 octobre 2026, au soir** (fiche DRO10, chantier « Droits : moindre
> privilège »). Remplace la version du matin, qui disait « le sien » pas
> codé et le code plus ouvert que la cible ; et celle du 02/10, qui disait
> la matrice « pas codée », 4 rôles, 18 tables (historique git).
>
> Deux matrices, à ne pas confondre :
>
> * **La cible** : ce qu'on veut. Elle est dans ADR-027 (statut **accepté** le 15/10/2026)
>   et son annexe, case par case, avec ses sources :
>   `md/adr/adr-027-annexe-matrice-detaillee.md`. Elle n'est pas recopiée ici.
> * **Le code** : ce que l'API fait aujourd'hui. Relevé dans l'API elle-même,
>   ci-dessous (§ 2).
>
> Repères : ✅ établi · 🟡 à décider · 💡 proposé · ⚠️ écart.

## 1. L'essentiel

* **5 rôles** : `Admin`, `Client`, `Hunter`, `Manager`, `Reader`.
* **Où vit le rôle** (chantier PRF, 2026-10-15, ADR-057) : `Client`,
  `Hunter`, `Manager` sur la fiche (`role_wording`) ; `Admin` et `Reader`,
  sans fiche, dans `"user".system_role`. Une seule casquette par compte : la
  base refuse une 2ᵉ fiche (`one_profile_per_user`, `409`) ; un compte sans
  fiche ni `system_role` reçoit `403`.
* **« Le sien » se lit par le numéro de la fiche** (`client.id`,
  `hunter.id`, `real_estate_manager.id`), pas par celui du compte : les 11
  `id_client`, `id_hunter`, `id_realestatemanager` visent la fiche (PRF2).
* **91 opérations** dans l'API, relevées le 13/10/2026 au soir.
* ✅ **Codé : le premier contrôle**, le rôle. Fermé par défaut : chaque route
  dit quels rôles passent, les autres reçoivent `403` (fiche DRO1). Les rôles
  suivent l'annexe d'ADR-027, case par case ; `test_droits_par_role.py` les
  rejoue toutes.
* ✅ **Codé : le second contrôle**, « le sien » (ADR-027, point 2 ; fiches
  DRO4 à DRO7). La ligne d'un autre rend `404`, comme une ligne absente ; une
  liste ne rend que les lignes visibles. Table par table : § 3.
* ✅ **Codé : les comptes désactivés**, lus par l'`Admin` seul (point 7 ;
  fiche DRO8), et le compte PostgreSQL `fil_rouge_reader` fermé pareil, plus
  les paiements (fiche DRO9).
* 🟡 Restent quelques écarts connus, et trois cases qui attendent Jeff (§ 3
  et § 4).

## 2. Ce que fait le code (13/10/2026, au soir)

**Comment lire** :

* « tous » = tout compte connecté ;
* « tous sauf Reader » = `Admin`, `Client`, `Hunter`, `Manager` ;
* « personne » = route fermée à tous, `Admin` compris ;
* aucune route `DELETE` : une suppression rend `405` (ADR-049) ;
* le tableau ne dit que le **rôle** : ce que le service filtre en plus
  (« le sien », les champs permis), c'est le § 3.

Sortie brute de l'outil, recopiée telle quelle :

| Table (route) | Lire | Créer | Modifier |
|---|---|---|---|
| `/users` | tous | Admin | tous sauf Reader |
| `/roles` | Admin, Reader | personne | personne |
| `/hunters` | tous | Admin | Admin, Hunter |
| `/clients` | Admin, Client, Hunter, Reader | Client | Admin, Client |
| `/real-estate-managers` | Admin, Hunter, Manager, Reader | Admin | Admin, Manager |
| `/search-requests` | tous | Client, Hunter | Hunter, Manager |
| `/criteria` | tous | Client, Hunter | personne |
| `/mandates` | tous | Hunter | Admin, Client, Hunter |
| `/estates` | tous | Hunter, Manager | Admin |
| `/estate-contacts` | Admin, Hunter, Manager | Admin, Hunter, Manager | Admin, Hunter, Manager |
| `/estate-proposed` | Admin, Client, Hunter, Reader | Hunter | Client, Hunter |
| `/estate-search-requests` | Admin, Client, Hunter, Reader | Hunter | Hunter |
| `/review-media` | Admin, Client, Hunter, Reader | Hunter | Hunter |
| `/pictures` | tous | Hunter, Manager | Admin |
| `/visits` | tous | Hunter | Admin |
| `/sales` | tous | Manager | personne |
| `/parameters-fees` | Admin, Hunter, Manager, Reader | Admin | Admin |
| `/commission-scales` | Admin, Hunter, Manager, Reader | Admin | Admin |
| `/payments` | Admin, Hunter, Manager | personne | Admin |
| `/hunter-performances` | Admin, Hunter, Manager, Reader | personne | personne |
| `/hunter-rate-parameters` | Admin, Hunter, Manager, Reader | Admin | Admin |

| Route à part | Qui |
|---|---|
| `GET /` | ouvert |
| `POST /auth/login` | clé d'API seule |
| `GET /auth/me` | tous |
| `POST /search-requests/submit` | clé d'API seule |
| `POST /users/{item_id}/anonymize` | Admin |
| `POST /estate-contacts/anonymize-expired` | Admin |
| `POST /sales/{item_id}/payment` | Admin |

91 opérations relevées.

**Refaire le relevé** : le tableau sort de
`docker/tools/print_rights_matrix.py`, dans le dépôt Fil-Rouge-API, depuis
`docker/` :

* bash : `docker compose exec -T api python - < tools/print_rights_matrix.py`
* PowerShell : `Get-Content tools/print_rights_matrix.py | docker compose exec -T api python -`

Il lit les rôles de `require_roles` sur chaque route.

## 3. Le code face à la cible

La cible est l'annexe d'ADR-027.

### « Le sien », table par table

Relevé dans `API/src/app/services/` (Fil-Rouge-API) : le crochet
`visible_rows` de chaque service, branche par rôle. ✓ = filtré à ses lignes ;
« tout » = le rôle lit la table en entier ; — = la route lui est fermée (§ 2).

| Table | Client | Hunter | Manager |
|---|---|---|---|
| `user` | ✓ son compte | ✓ | ✓ |
| `client` | ✓ sa fiche | ✓ ses clients | — |
| `hunter` | ✓ son chasseur | ✓ sa fiche | ✓ ses chasseurs |
| `real_estate_manager` | — | ✓ son manager | ✓ sa fiche |
| `search_request` | ✓ | ✓ | ✓ l'équipe |
| `criteria` | ✓ | ✓ | ✓ l'équipe |
| `mandate` | ✓ | ✓ | ✓ l'équipe |
| `estate`, `picture` | ✓ biens proposés | tout (H2, H5) | tout |
| `estate_proposed` | ✓ | ✓ | — |
| `estate_searchrequest`, `review_media` | ✓ | ✓ | — |
| `visit`, `sale` | ✓ | ✓ | ✓ l'équipe |
| `payment` | — | ✓ | ✓ l'équipe |
| `hunter_performance` | — | ✓ | ✓ l'équipe |
| `commission_scale` | — | ✓ le sien et celui par défaut | ✓ l'équipe et celui par défaut 💡 |

* **L'équipe** du Manager : ses chasseurs (`hunter.id_realestatemanager`) et
  les demandes qui lui sont confiées (`search_request.id_realestatemanager`).
* **Les chemins** suivent les clés du schéma : `services/client_rows.py`,
  `hunter_rows.py`, `manager_rows.py`.
* **En écriture**, le crochet `owns` refuse une ligne qui ne serait pas à
  lui → `409` (8 services). Les champs gardés → `403` : le rôle et
  l'activation d'un compte, les coordonnées seules pour le chasseur et le
  manager, l'affectation seule pour le Manager sur une demande (Q-ACC-10).
* **`Reader`** lit ses tables en entier, sans « le sien » : la cible ne lui
  en donne pas.
* **L'`Admin`** voit tout : le crochet n'est pas appelé pour lui.

### Comptes désactivés et `fil_rouge_reader`

* ✅ Le profil d'un compte désactivé (`user`, `client`, `hunter`,
  `real_estate_manager`) n'est lu que par l'`Admin` ; `Reader` compris, il
  rend `404` (point 7 ; fiche DRO8). Les lignes qui le citent restent lisibles.
* ✅ `fil_rouge_reader`, en SQL direct : ni `payment` (point 8), ni les
  comptes désactivés (politique par ligne), ni `"user".password`, ni
  `estate_contact` (fiche DRO9 ; `docker/init-v3/04_role-lecture-seule.sql`).

### Conformes

* ✅ Le rôle, sur les 21 tables et les 7 routes à part : la grille de
  l'annexe, rejouée par `test_droits_par_role.py` (fiches DRO1 à DRO3).
* ✅ L'argent : barèmes et réglages écrits par l'`Admin` seul (Q-ACC-07) ;
  un paiement n'est jamais saisi à la main, il naît du calcul, lancé par
  l'`Admin` (point 10 ; fiche DRO2) ; ni `Client` ni `Reader` ne le lisent.
* ✅ `sale` créée par le `Manager` de l'équipe (Q-ACC-03) ; `mandate`,
  `visit` créés par le `Hunter`.
* ✅ `hunter_performance` fermé en écriture (ADR-035).
* ✅ `estate` créé par `Hunter` ou `Manager` (ADR-047) ;
  `estate_searchrequest` et `review_media` par le `Hunter` (ADR-051).
* ✅ `estate_contact` : ni `Client` ni `Reader` (ADR-054).
* ✅ Chacun corrige **son** compte, sans rôle ni activation : `PUT /users`
  rouvert au `Client`, au `Hunter` et au `Manager` avec « le sien ».
* ✅ Le formulaire du site répond pareil quel que soit l'email, formulaire
  mal formé compris (fiche DRO11).
* ✅ Aucune route `DELETE`.

### Écarts qui restent

* ⚠️ Le `Client` modifie son mandat et ses biens proposés **champ par
  champ sans limite** : l'annexe ne lui donne que signer, commenter,
  prioriser, faire une offre (P3, H6, H8). Seule l'appartenance est gardée.
* 🟡 Le `Client` ne crée pas son compte par `POST /users` (fermé : il y
  choisirait son `system_role`) : il le crée par `POST /search-requests/submit`
  (Q-ACC-12).
* 🟡 Le `Hunter` ne renouvelle pas le mandat d'un autre chasseur : la
  réaffectation attend Jeff (Q-JEF-30).
* 🟡 Une demande **confiée au manager B** mais **suivie par un chasseur de
  A** est visible des deux, et chacun peut la réaffecter. L'annexe ne dit
  rien de ce cas (relecture de DRO7).
* 💡 Le `Manager` lit aussi le barème par défaut : il vaut pour ceux de ses
  chasseurs qui n'en ont pas en propre (choix de DRO7).
* ⚠️ « Désactivé » ne distingue pas un compte **effacé** (ADR-049) d'un
  compte **jamais activé**. Les 25 comptes du seed sont désactivés : en dev,
  leurs profils sont cachés à tous sauf l'`Admin` (fiche DRO8).
* ⚠️ Le `PUT` recopie `created_at` du corps reçu, sur toute table.

## 4. Ce qui reste à décider ou à faire

* 🟡 **Jeff** : ADR-027 est accepté sans lui (15/10/2026) ; trois cases attendent encore sa
  confirmation (Q-ACC-06, 12, 13), appliquées comme l'annexe les donne. Plus
  les deux cas 🟡 du § 3 (Q-JEF-30, la demande partagée entre deux équipes).
* ➡️ Les écarts ⚠️ du § 3 sont dans `API/README.md`, « Limites connues ».

## Sources

| Affirmation | Source |
|---|---|
| La cible, case par case | `md/adr/adr-027-annexe-matrice-detaillee.md` ; `md/adr/adr-027-matrice-acces-par-role.md` |
| Le code, route par route | `docker/tools/print_rights_matrix.py` (Fil-Rouge-API), lancé le 13/10/2026 au soir : 91 opérations |
| Le mécanisme des rôles | `API/src/app/utils/roles.py` ; `API/src/app/routes/crud_router.py` (Fil-Rouge-API) |
| « Le sien », table par table | `visible_rows` et `owns` dans `API/src/app/services/*_service.py` ; `BaseService` dans `base_service.py` (Fil-Rouge-API) |
| La grille rejouée par les tests | `API/tests/integration/test_droits_par_role.py`, `test_le_sien.py` (Fil-Rouge-API) |
| `fil_rouge_reader` | `docker/init-v3/04_role-lecture-seule.sql` ; `API/tests/integration/test_lecteur_sql.py` (Fil-Rouge-API) |
| Les écarts qui restent | `API/README.md`, « Limites connues » (Fil-Rouge-API) |

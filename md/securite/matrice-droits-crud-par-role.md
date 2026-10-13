# Qui peut faire quoi — la matrice des droits

> 📅 **13 octobre 2026.** Remplace la version du 02/10, périmée : elle disait
> la matrice « pas codée », 4 rôles, 18 tables (historique git).
>
> Deux matrices, à ne pas confondre :
>
> * **La cible** : ce qu'on veut. Elle est dans ADR-027 (statut **proposé**)
>   et son annexe, case par case, avec ses sources :
>   `md/adr/adr-027-annexe-matrice-detaillee.md`. Elle n'est pas recopiée ici.
> * **Le code** : ce que l'API fait aujourd'hui. Relevé dans l'API elle-même,
>   ci-dessous (§ 2).
>
> Repères : ✅ établi · 🟡 à décider · 💡 proposé · ⚠️ écart.

## 1. L'essentiel

* **5 rôles** : `Admin`, `Client`, `Hunter`, `Manager`, `Reader`.
* **91 opérations** dans l'API, relevées le 13/10/2026.
* ✅ **Codé : le premier contrôle**, le rôle. Chaque route dit quels rôles
  passent ; les autres reçoivent `403`.
* ⚠️ **Pas codé : le second contrôle**, « le sien » (ADR-027, point 2).
  * Exemple : un `Client` lit **tous** les mandats et **tous** les paiements,
    pas seulement les siens.
  * Seules exceptions : l'auteur d'un bien, d'une note, d'un contact est pris
    dans le jeton, et seul l'auteur d'une note y ajoute un média (ADR-047,
    ADR-051, ADR-054).
* ⚠️ **Le code est plus ouvert que la cible** sur beaucoup de tables (§ 3).
  Fermer ces écarts est du code à écrire : un chantier à part.

## 2. Ce que fait le code (13/10/2026)

**Comment lire** :

* « tous » = tout compte connecté ;
* « tous sauf Reader » = `Admin`, `Client`, `Hunter`, `Manager` ;
* « personne » = route fermée à tous, `Admin` compris ;
* aucune route `DELETE` : une suppression rend `405` (ADR-049).

| Table (route) | Lire | Créer | Modifier |
|---|---|---|---|
| `/users` | tous | Admin | Admin |
| `/roles` | tous | Admin | Admin |
| `/hunters` | tous | tous sauf Reader | tous sauf Reader |
| `/clients` | tous | tous sauf Reader | tous sauf Reader |
| `/real-estate-managers` | tous | tous sauf Reader | tous sauf Reader |
| `/search-requests` | tous | tous sauf Reader | tous sauf Reader |
| `/criteria` | tous | tous sauf Reader | tous sauf Reader |
| `/mandates` | tous | tous sauf Reader | tous sauf Reader |
| `/estates` | tous | Hunter, Manager | tous sauf Reader |
| `/estate-contacts` | Admin, Hunter, Manager | Admin, Hunter, Manager | Admin, Hunter, Manager |
| `/estate-proposed` | tous | tous sauf Reader | tous sauf Reader |
| `/estate-search-requests` | tous | Hunter | tous sauf Reader |
| `/review-media` | tous | Hunter | tous sauf Reader |
| `/pictures` | tous | tous sauf Reader | tous sauf Reader |
| `/visits` | tous | tous sauf Reader | tous sauf Reader |
| `/sales` | tous | tous sauf Reader | tous sauf Reader |
| `/parameters-fees` | tous | tous sauf Reader | tous sauf Reader |
| `/commission-scales` | tous | tous sauf Reader | tous sauf Reader |
| `/payments` | tous | tous sauf Reader | tous sauf Reader |
| `/hunter-performances` | tous | personne | personne |
| `/hunter-rate-parameters` | tous | tous sauf Reader | tous sauf Reader |

| Route à part | Qui |
|---|---|
| `GET /` | ouvert (health-check) |
| `POST /auth/login` | clé d'API seule, sans jeton |
| `GET /auth/me` | tous |
| `POST /search-requests/submit` | clé d'API seule, sans jeton (demande avant le compte) |
| `POST /users/{item_id}/anonymize` | Admin |
| `POST /estate-contacts/anonymize-expired` | Admin |
| `POST /sales/{item_id}/payment` | tous sauf Reader |

**Refaire le relevé** : le tableau sort de
`docker/tools/print_rights_matrix.py`, dans le dépôt Fil-Rouge-API, depuis
`docker/` :

* bash : `docker compose exec -T api python - < tools/print_rights_matrix.py`
* PowerShell : `Get-Content tools/print_rights_matrix.py | docker compose exec -T api python -`

Il lit les rôles de `require_roles` sur chaque route. Ce qu'un service
vérifie en plus (l'auteur d'une note) n'y apparaît pas : c'est le § 1.

## 3. Les écarts entre le code et la cible

La cible est l'annexe d'ADR-027. ⚠️ = le code laisse faire ce que la cible
interdit.

### Le second contrôle, « le sien »

* ⚠️ **Nulle part en lecture.** Un `Client` lit les comptes, demandes,
  mandats, ventes et paiements de **tous** les clients ; un `Hunter`, ceux de
  tous les chasseurs.
* ⚠️ **Nulle part en écriture**, sauf l'auteur d'une note pour ses médias.

### Écritures trop ouvertes

| Table | Cible (annexe d'ADR-027) | Code |
|---|---|---|
| `parameters_fees`, `commission_scale` | **Admin** seul (Q-ACC-07) | ⚠️ tous sauf Reader |
| `hunter_rate_parameters` | **Admin** seul 💡 | ⚠️ tous sauf Reader |
| `payment` | créé par le calcul, avancé par l'**Admin** 💡 | ⚠️ tous sauf Reader, à la main |
| `POST /sales/{id}/payment` | l'**Admin** lance le calcul 💡 | ⚠️ tous sauf Reader |
| `sale` | créée par le **Manager** (Q-ACC-03) | ⚠️ tous sauf Reader |
| `mandate` | créé par le **Hunter** (H4) | ⚠️ tous sauf Reader |
| `visit` | créée par le **Hunter** (Q-ACC-13) | ⚠️ tous sauf Reader |
| `hunter`, `client`, `real_estate_manager` | chacun corrige le sien ; **Admin** crée | ⚠️ tous sauf Reader, pour tout le monde |
| `estate` (modifier) | **Admin** 💡 | ⚠️ tous sauf Reader |

### Lectures trop ouvertes

| Table | Cible | Code |
|---|---|---|
| `payment` | le chasseur, son manager, l'**Admin** ; ni `Client` ni `Reader` (ADR-027, point 8) | ⚠️ tous |
| `role` | **Admin** 💡 | ⚠️ tous |
| `client` | le client, son chasseur, l'**Admin** | ⚠️ tous |
| comptes désactivés | **Admin** seul 💡 (ADR-049) | ⚠️ tous |

### Plus fermé que la cible

* `user` : la cible laisse chacun corriger **son** compte ; le code réserve
  `PUT /users/{id}` à l'**Admin**. Fermé exprès : sans le second contrôle,
  tout compte pouvait changer le mot de passe d'un `Admin` (relecture de la
  série API, `routes/user_router.py`).

### Conformes

* ✅ `hunter_performance` fermé en écriture (ADR-035).
* ✅ `estate` créé par `Hunter` ou `Manager` (ADR-047).
* ✅ `estate_searchrequest` et `review_media` créés par le `Hunter` (ADR-051).
* ✅ `estate_contact` : ni `Client` ni `Reader` (ADR-054 ; plus récent que
  l'annexe, qui ne le cite pas).
* ✅ Comptes et rôles : `Admin` seul écrit ; effacer = anonymiser (ADR-049).
* ✅ Aucune route `DELETE`.

## 4. Ce qui reste à décider ou à faire

* 🟡 **Jeff** : ADR-027 est « proposé » ; trois cases attendent sa
  confirmation (Q-ACC-06, 12, 13 ; pense-bête de la réunion).
* ➡️ **Un chantier pour fermer les écarts du § 3** : le rôle d'abord (table
  par table, dans `build_crud_router`), puis « le sien » (un filtre par
  service). À ouvrir quand l'équipe le décide.

## Sources

| Affirmation | Source |
|---|---|
| La cible, case par case | `md/adr/adr-027-annexe-matrice-detaillee.md` ; `md/adr/adr-027-matrice-acces-par-role.md` |
| Le code, route par route | `docker/tools/print_rights_matrix.py` (Fil-Rouge-API), lancé le 13/10/2026 : 91 opérations |
| Le mécanisme des rôles | `API/src/app/utils/roles.py` ; `API/src/app/routes/crud_router.py` (Fil-Rouge-API) |
| Aucun filtre « le sien » en lecture | `API/src/app/services/` : `actor` n'est lu qu'à la création (recherche du 13/10/2026) |
| L'auteur d'une note seul y ajoute un média | `API/src/app/services/review_media_service.py` |
| `PUT /users` fermé à l'Admin, et pourquoi | `API/src/app/routes/user_router.py` |

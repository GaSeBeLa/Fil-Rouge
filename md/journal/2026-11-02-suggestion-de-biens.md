# Suggestion de biens au chasseur — décisions et pistes du 2026-11-02

> 📷 Photo du 2026-11-02 : la discussion Discord de l'après-midi (Seb,
> Gabriel, amethyste, Békanty), relue dans le code. À reprendre le
> 2026-11-03 au matin, sans doute en chantier vlp.
>
> ✅ établi (source citée) · 🟡 à décider · 💡 proposé
>
> Chemins `API/…`, `airflow/…`, `docker/…` : dépôt **Fil-Rouge-API**.
> Chemins `SP/…` : `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/`
> (lecture seule).

## 1. L'idée, en une phrase

L'idée vient d'amethyste.

1. La machine cherche les biens qui collent à la demande d'un client.
2. Elle les **suggère au chasseur** qui suit ce client.
3. Le chasseur trie les suggestions, puis **propose** au client celles qu'il garde.
4. Elle ne suggère **jamais** un bien vendu, ni un bien déjà montré à ce client.

- ✅ C'est la feature 05 : « je reçois une sélection de biens correspondant à
  cette recherche » (`SP/user-stories/05_chasseur_selection_quotidienne_biens.feature:14-17`).
- ✅ Le chasseur garde la décision. Phrase pour le jury (ADR-058) : « il
  **cherche et propose**, un humain **engage** ».

## 2. Les 4 décisions votées (4/4, Discord, 2026-11-02)

Seb, Gabriel, amethyste et Békanty ont tous choisi A, aux 4 questions.

| # | Question | Choix |
|---|---|---|
| Q1 | Droits de l'IA | **Accepter l'ADR-058**, **et** permettre au chasseur IA de **suggérer dans la demande d'un chasseur humain**. Il ne peut jamais acheter, vendre, payer, ni lire le contact du vendeur. |
| Q2 | « Déjà proposé », mais à qui ? | **À ce client seulement.** Un même bien peut convenir à deux clients. |
| Q3 | Biens refusés par le chasseur | **Ajouter une colonne d'état** dans `estate_searchrequest` (voir § 4). |
| Q4 | `recherches.csv` du prof | **Jeu de test**, pas chargé en base. |

- ⚠️ L'ADR-058 est encore « 💡 proposé » dans `md/adr/adr-058-droits-du-chasseur-ia.md`.
  - Le vote Q1 l'accepte, avec un ajout.
  - Il reste à le passer en « accepté », ici **et sur Confluence**. Confluence fait foi ; c'est au groupe de le faire.
- ⚠️ L'énoncé de la Q3 disait « il ne peut que **supprimer** la ligne ». C'est **faux** (voir § 3) : il ne peut même pas la supprimer. Le choix A n'en est que plus nécessaire.

## 3. Ce qui existe aujourd'hui (vérifié dans le code)

### Ce qui sert déjà

- ✅ **La recherche de biens**. `GET /estates/search` interroge l'index
  Elasticsearch `estates` (`API/src/app/routes/estate_search_router.py:51-68`).
  - Ses filtres : texte libre, ville, code postal, type, prix min et max, surface min, position GPS et rayon.
  - ❌ Les filtres se **tapent à la main**. La route ne lit ni `search_request`, ni `criteria`.
- ✅ **L'index `estates`**, rempli à 4 h par le DAG `estates_index`. Il ne
  contient ni le contact, ni l'adresse.
  - Champs utiles : ville, code postal, position GPS, type, prix, surface, pièces, chambres, DPE, jardin, garage, ascenseur, cave, parking, description en français (`airflow/src/search/mapping.py`).
  - ❌ **Absents de l'index** : balcon, terrasse, vue, piscine, calme, lumineux. Pourtant, `estate` a `is_quiet` et `is_bright`.
- ✅ **La sélection**. `estate_searchrequest` relie un bien à une demande.
  - `id_hunter` est obligatoire. `review_hunter` reçoit l'avis du chasseur en texte libre.
  - La clé unique `uq_estate_search (id_estate, id_search_request)` (SQL v3, l.874) assure déjà la **Q2**.
- ✅ **La règle P19**. On ne propose un bien au client que s'il est dans la
  sélection de sa demande (`API/src/app/services/estate_proposed_service.py:74-78`).
- ✅ **« Vendu »**. Un bien est vendu si son id est dans `sale`, qui a la clé
  unique `uq_sale_estate (id_estate)`. `seed_volume.py:270-279`
  (`estates_for_sale`) fait déjà ce filtre.

### Ce qui bloque

- ❌ **Créer une ligne de sélection est réservé au rôle `HUNTER`.**
  - L'id du chasseur est lu dans son jeton : `create_roles=(HUNTER,)`, ADR-051, `routes/estate_search_request_router.py`.
  - Un programme qui n'est pas un chasseur ne peut donc pas passer par cette route.
- ❌ **Il n'y a aucun DELETE dans l'API.** « aucune ligne ne se supprime par
  l'API ; un DELETE reçu rend 405 » (ADR-049, `routes/crud_router.py:58-60`).
  - Un bien refusé par le chasseur **reste** dans la sélection.
  - Rien ne dit qu'il est refusé, sauf le texte libre `review_hunter`.
- ⚠️ **Aujourd'hui, le chasseur IA a tous les droits d'un humain.**
  - C'est une fiche `hunter` avec `is_hunter_ai = TRUE`, et le rôle `Hunter`.
  - L'ADR-058 n'est pas codé.

### Les refus, aujourd'hui

| Qui refuse quoi | Où c'est stocké | État |
|---|---|---|
| Le chasseur refuse **une demande** | `search_request.status = 'rejected'` (SQL v3, l.405-409 : « la réponse d'un chasseur ») | ✅ existe |
| Le chasseur refuse **un bien** de la sélection | nulle part (pas de colonne, pas de DELETE) | ❌ à créer : Q3 |
| Le client note un bien proposé | `estate_proposed.client_priority` (1 à 5) | ✅ existe |
| Le client commente | `estate_proposed.comment_client` (texte libre) | ⚠️ illisible par une machine |
| Le client refuse un bien proposé | `estate_proposed.proposition_status = 'rejected'` | ⚠️ **ambigu** : la table sert aussi au « suivi de l'offre », donc `rejected` peut vouloir dire « le client n'en veut pas » ou « le vendeur refuse l'offre » |
| Le motif d'un refus | nulle part | ❌ aucune liste fermée |

- Le client a le droit d'écrire sur ses propositions : « le client commente,
  priorise, fait une offre » (`routes/estate_proposed_router.py:14-18`).
- 🟡 **Pas vérifié** : l'API empêche-t-elle le client de changer lui-même
  `proposition_status` ? Aucun garde-fou par champ n'a été vu dans
  `estate_proposed_service.py`.

## 4. Les propositions (💡, à valider au chantier)

### 4.1 La colonne d'état (vote Q3)

```sql
-- dans estate_searchrequest
status VARCHAR(20) NOT NULL DEFAULT 'suggested'
       CHECK (status IN ('suggested', 'kept', 'dismissed'))
```

- `suggested` : la machine l'a mis dans la liste.
- `kept` : le chasseur le garde, et pourra le proposer.
- `dismissed` : le chasseur le refuse. Il ne sera **plus jamais resuggéré**
  pour cette demande.
- Le chasseur change l'état par le `PUT`, qui existe déjà.
- 💡 P19 renforcée : on ne propose au client qu'un bien `kept`.
- 💡 Plus tard : un **motif** quand l'état est `dismissed` (trop cher, trop loin,
  trop petit, autre). C'est le signal dont la future IA aura besoin.
- Coût : le SQL v3, une migration, le modèle SQLModel, les tests, et le banc v2/v3.
- 🟡 La traçabilité, ou savoir qui a ajouté la ligne :
  - si le chasseur IA agit avec son propre compte, `id_hunter` le dit déjà ;
  - sinon, il faut une colonne `source`.

### 4.2 Le moteur de suggestion

- 💡 **Commencer par une route que le chasseur déclenche** :
  `POST /search-requests/{id}/suggestions`.
  - Elle lit la dernière version de `criteria`, et interroge Elasticsearch.
  - **Filtres durs** : ville ou CP, type, budget max, surface min, pièces, DPE max.
  - **Bonus de score** : jardin, ascenseur, cave, mots de la description.
  - **Elle exclut** les biens vendus, déjà dans la sélection, ou `dismissed`.
  - Elle écrit les **10 meilleurs** en `suggested`.
  - Aucun nouveau rôle, et elle se montre dans le Swagger.
- 💡 Plus tard, et en option : un DAG à 5 h, après `estates_index`, qui fait
  le même travail pour les demandes confiées au chasseur IA.
- ⚠️ **Ce n'est pas de l'IA**, mais une requête et des règles. Gabriel l'a
  relevé à juste titre. On l'appelle « **moteur de suggestion** ».

### 4.3 Ce qu'une IA apporterait par-dessus (pour le livrable de la phase 4, sur le papier)

1. **Apprendre les goûts réels**, pas seulement les critères écrits. Elle
   apprend de `client_priority`, des `dismissed` et des refus du client, et
   reclasse les biens par **pertinence** (feature 09,
   `SP/user-stories/09_futur_chasseur_assistance_ia.feature:35-40`).
2. **« Ressembler aux biens rejetés »** (feature 09, l.43-46). Un modèle
   transforme chaque bien en vecteur ; Elasticsearch sait chercher les plus
   proches (`dense_vector` + kNN).
3. **Comprendre le texte libre** : la description, ou `comment_client`.
4. **Expliquer au chasseur** pourquoi un bien est suggéré (un LLM), avec les
   garde-fous de l'énoncé (`SP/Readme.md:282`).

- ⚠️ Les points 1 et 2 demandent de **vrais choix de clients**. Nos données
  sont générées : un modèle n'y apprendrait que le hasard du faker.

## 5. `recherches.csv` (vote Q4 : jeu de test)

- ✅ Le générateur fabrique **d'abord une recherche**, puis N annonces **à
  partir d'elle** : même ville, même type, surface ≥ min, DPE ≤ max.
  - Voir `airflow/tools/generer_annonces.py:427-432`, et `generer_annonce_correspondante` (l.226).
- ✅ Chaque annonce porte **`recherche_ref`**, le `REC-…` de sa recherche (l.253).
- ⚠️ Notre DAG `annonces_import` lance le script dans un **dossier temporaire
  neuf**. Seul `annonces.csv` part dans MinIO bronze, et `recherches.csv` est
  **jeté** (`airflow/dags/annonces_import_dag.py:55-80`).
- ⚠️ `recherche_ref` n'apparaît nulle part dans `airflow/`, `API/src/` ni le
  SQL v3 (grep : 0 résultat). Une fois en base, le lien est **perdu**.
  - 🟡 Pas vérifié : MinIO silver la garde-t-il ?
- ❌ **Pour apprendre, il ne sert à rien.**
  - Il ne contient que les règles du générateur, aucun choix de client.
  - Ses exemples sont tous positifs, et les négatifs sont trop faciles.
- ✅ **Pour tester, il est utile.**
  - Le moteur retrouve-t-il, pour REC-X, ses annonces ? Cela donne un taux mesurable.
  - Il teste aussi le nettoyage : un prix `"406100 €"`, `surface` ou `surface_m2` (l.261-268).
- ✅ L'énoncé ne demande pas de le charger : « Utile pour disposer d'un jeu de
  données de test » (`SP/Readme.md:46`). L'entraînement n'est pas exigé
  (`SP/Readme.md:257`).
- ⚠️ Petit défaut du script :
  - son aide annonce par défaut 1 et 4 annonces, alors que le code met 100 et 1000 ;
  - à corriger dans **notre copie** (`airflow/tools/`), jamais dans le Starter Pack.

## 6. La liste pour demain matin

**Décisions** : ✅ faites (§ 2), sauf deux restes :

- 🟡 passer l'ADR-058 en « accepté », avec l'ajout de la Q1 (dépôt + Confluence) ;
- 🟡 séparer « refusé par le client » de « offre refusée par le vendeur » dans
  `estate_proposed`, et décider s'il faut un motif de refus.

**Documents de la phase 4** (`SP/Readme.md:257-260`, sans code) :

1. Le **schéma du programme d'IA** : la machine suggère, le chasseur trie, le
   client reçoit. En organigramme.
2. Le **tableau des features**. Pour chacune :
   - son nom ;
   - sa source `table.colonne` ;
   - son calcul ;
   - pourquoi elle compte.
   Exemples : écart prix/budget, distance, nombre de critères cochés.
3. Le **label** : comment on sait qu'un bien plaît (`client_priority`,
   `proposition_status`, `dismissed`, visites).
4. Une **page franche** : la v1 est faite de règles explicables ; l'IA viendra
   avec de vrais choix de clients ; les données générées ne suffisent pas.

**Code** (un chantier vlp, en TDD) :

5. La colonne `status` dans `estate_searchrequest`. Elle touche :
   - le SQL v3 et la migration ;
   - le modèle et les tests ;
   - le banc v2/v3.
6. La route `POST /search-requests/{id}/suggestions` (§ 4.2).
7. Le code de l'ADR-058 : le chasseur IA reçoit 403 sur une offre, une vente,
   un paiement ou le contact du vendeur. Un test par interdiction.
8. En option : garder `recherche_ref` à l'import, puis mesurer le moteur sur
   `recherches.csv`.
9. En option : le DAG de 5 h.
10. Corriger l'aide de `airflow/tools/generer_annonces.py`.

## Sources de la discussion

- Discord, salon `le-glaude`, le 2026-11-02, de 14 h 37 à 16 h 28 (heure UTC).
- Votes :
  - messages 1566844934575620227 (Q1), 1566845026170962051 (Q2),
    1566845030164078664 (Q3), 1566845033322250302 (Q4) ;
  - Békanty a voté A aux 4 questions par les boutons, après l'accord transmis par Seb.

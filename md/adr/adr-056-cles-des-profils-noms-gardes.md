### ADR-056 : Les clés des profils — `id` gardé, liens par `id_user`, noms gardés

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 14/10/2026
* **Statut :** 💡 proposé (Sébastien, Discord, 14/10/2026 : « on garde mais on doit le documenter ») ; refacto à venir, dépriorisée par Robin HOTTON (14/10/2026). Pas de report Confluence pour l'instant.
* **Décideurs :** Sébastien ; question soulevée par Laurence (Discord, 14/10/2026) ; refacto à venir proposée et dépriorisée par Robin HOTTON (prof, 14/10/2026, relayé par Sébastien).
* **Voir aussi :** ADR-025 et ADR-029 (lien chasseur–manager vers `real_estate_manager(id_user)`) ; ADR-027 (droits, « le sien ») ; fiche FIN2 (Swagger)

**Contexte**

* `client`, `hunter` et `real_estate_manager` portent deux clés (`docker/init-v3/01_create_fil_rouge_immobilier.sql:108-122`, dépôt Fil-Rouge-API) :
  * `id` : clé primaire technique ;
  * `id_user` : clé vers `"user"(id)`, `NOT NULL UNIQUE` (un compte, une fiche).
* `id` est gardé sur **conseil du prof** : un identifiant propre à chaque entité, pour qu'un passage vers une autre technologie (MongoDB) reste possible. Le sujet l'ouvre : « nos données ne sont pas organisées de la bonne manière ni avec la bonne technologie » (StarterPack, `Readme.md:171`).
* Les liens des autres tables visent `id_user`, jamais `id`. Comptés le 14/10/2026 dans le schéma v3 :
  * **0** clé étrangère vers `client(id)`, `hunter(id)` ou `real_estate_manager(id)` ;
  * **11** vers leur `id_user` (2 + 7 + 2).
* Ces colonnes s'appellent pourtant `id_client`, `id_hunter`, `id_realestatemanager` : le nom laisse croire qu'elles portent `client.id`. Dans la base de dev, `id ≠ id_user` pour 19 clients sur 19, 2 managers sur 2, 1 chasseur sur 7 (14/10/2026).
* Ce piège a déjà coûté :
  * un bug : le paiement cherchait le chasseur par `hunter.id` (corrigé, Fil-Rouge-API `7e40e8d`) ;
  * deux corrections du Swagger (FIN2 ; `ea67e20`).
* Laurence a proposé de renommer en `id_client_user` (ou `id_user_client`).

**Options**

1. **Garder les noms et documenter.** Coût : cet ADR, une note dans le MPD. **Retenue.**
2. **Renommer** `id_client` → `id_user_client`, et de même pour les deux autres. Coût, compté le 14/10/2026 dans Fil-Rouge-API (`API/` et `docker/`, `.py` et `.sql`) :
   * `id_client` : 32 fichiers, 190 lignes ;
   * `id_hunter` : 50 fichiers, 306 lignes ;
   * `id_realestatemanager` : 21 fichiers, 67 lignes ;
   * soit 16 colonnes, la migration v2→v3, le banc, le MPD et le seed de démo. Surtout, **les noms du JSON de l'API changent**.
   * Écartée pour l'instant.
3. **Faire viser `client.id` par les clés.** Le nom `id_client` deviendrait vrai, mais :
   * chaque contrôle « le sien » devrait joindre la table de profil ;
   * le coût est du même ordre que l'option 2.
   * **Écartée pour l'instant, retenue comme refacto à venir** : c'est le découpage proposé par Robin HOTTON (section « Refacto à venir »).

**Décision**

1. **`id` reste** dans les trois tables de profil : c'est la clé technique de la fiche. Aucune autre table ne la cite. Seules les routes `/clients/{item_id}`, `/hunters/{item_id}` et `/real-estate-managers/{item_id}` s'en servent.
2. **Les liens passent par `id_user`**, le numéro du compte. Raison : **zéro jointure pour les droits**. Le jeton donne `user.id`, et « le sien » filtre directement dessus :
   * `services/mandate_service.py:56` : `item.id_client == viewer.user.id` ;
   * `services/client_rows.py:40` : `SearchRequest.id_client == user_id`.

   Le sujet demande d'absorber de gros volumes : « plusieurs milliers de mandats par semaine » (`Readme.md:160`, `:162`).
3. **Les noms `id_client`, `id_hunter`, `id_realestatemanager` sont gardés.** Ce qu'ils contiennent est écrit à trois endroits :
   * en base : `COMMENT ON COLUMN`, en fin du script `01` ;
   * dans le Swagger, sous chaque champ (`models/field_descriptions.py`) ;
   * dans cet ADR.
4. **Règle de code** : une valeur `id_client`, `id_hunter` ou `id_realestatemanager` se cherche par `id_user` (`list_where(..., id_user=...)`), jamais par `get_by_id`. Un test qui touche un profil crée une ligne neuve où `id ≠ id_user` : dans la base de test, les profils du seed ont `id = id_user`, et cachent l'erreur.

**Conséquences**

* À l'oral, deux phrases suffisent :
  * « `id` est la clé technique, gardée pour la portabilité » ;
  * « les liens passent par le compte, ce qui évite une jointure à chaque contrôle de droits ».
* Le MPD (export v9, `vrac/v9.drawio.*`) reçoit une note qui dit la même chose (à faire par le groupe).
* Le changement de cible des clés est prévu (section « Refacto à venir »). Il se fait **avant** qu'un front appelle l'API, ou avec une v4 du schéma, jamais après.

**Refacto à venir — le découpage de Robin HOTTON (14/10/2026)**

Proposé par le prof, **dépriorisé par lui** (« vous avez des choses plus importantes à faire que cette refonte »), à garder documenté. Chantier possible n° 10 de `context AI/08-etat.md`.

1. **`user` sert à la connexion seulement.** Son `id` est une information sensible, c'est le `sub` du jeton JWT (`utils/security.py:143`), et il ne se propage pas dans les tables métier.
2. **Les 11 clés visent la PK du profil** : `client(id)`, `hunter(id)`, `real_estate_manager(id)` (l'option 3 ci-dessus). Les noms `id_client`, `id_hunter` et `id_realestatemanager` deviennent exacts, sans renommage. `user.id` ne reste que dans la colonne `id_user` des trois profils.
3. **`AbstractClient`, héritage dans le code** : une classe de base SQLModel, **sans table**. Elle porte les champs communs aux trois profils : `created_at`, `id_user`, `first_name`, `last_name`, `phone_number`, `country_iso`, `gender`. `Client`, `Hunter` et `RealEstateManager` en héritent ; les tables SQL ne changent pas. Écart à aligner d'abord : `country_iso` est obligatoire chez `Client` et facultatif chez `Hunter`.
4. **Le rôle est lié à `AbstractClient`** : le constructeur de chaque profil pose son rôle par défaut (`Client` → rôle Client, `Hunter` → Hunter, `RealEstateManager` → Manager).
5. **Ce que le chantier devra aussi faire** :
   * une migration (la 45) qui convertit les valeurs des 11 colonnes, puis rebranche les FK ;
   * « le sien » compare à l'`id` du profil connecté, lu une fois par requête ;
   * `build_vente` et le seed de démo cherchent le chasseur par `hunter.id` ;
   * la base de test donne des `id ≠ id_user` aux profils, et un test d'introspection refuse toute FK vers un profil qui ne vise pas sa PK ;
   * le Swagger (`models/field_descriptions.py`), le README, la matrice des droits et le MPD sont mis à jour ;
   * cet ADR passe à « remplacé » par celui du chantier.
6. Pour l'API, les **noms** ne changent pas, mais les **valeurs** attendues, si : un `id_client` attendra un `client.id`.

Écarté : supprimer `id` et mettre la PK sur `id_user`. Les clés ne bougeraient pas, mais cette option garde `user.id` partout, à l'opposé du point 1.

**Ce que cet ADR ne tranche pas**

* 🟡 « Éviter les jointures inutiles » n'est **pas** écrit dans le sujet (grep « jointure » dans les deux StarterPacks : 0 résultat). C'est une déduction du groupe, que le code confirme. Elle se présente comme telle.
* 🟡 L'argument MongoDB n'oblige pas à garder `id`. La doc de MongoDB accepte n'importe quelle valeur BSON comme `_id`, sauf un tableau, une regex ou `undefined`. Un entier comme `id_user` convient donc. Pour un lien un-à-un, elle conseille d'imbriquer le profil dans le document. `id` est gardé parce que c'est le conseil du prof, pas parce que MongoDB l'exige.

**Sources**

| Affirmation | Source |
|---|---|
| Option 1 retenue, à documenter | Sébastien, Discord, 14/10/2026 |
| Renommage proposé | Laurence, Discord, 14/10/2026 |
| `id` gardé sur conseil du prof | Sébastien, Discord, 14/10/2026 ; `01_create_fil_rouge_immobilier.sql:115-117` |
| 0 clé vers `id`, 11 vers `id_user` | schéma v3, grep du 14/10/2026 |
| `id ≠ id_user` dans la base de dev | requête du 14/10/2026 |
| Coût du renommage | grep `-w` dans Fil-Rouge-API, 14/10/2026 |
| « absorber les quantités de données prévues » | StarterPack - BASE, `Readme.md:162` |
| `_id` : « any BSON data type, other than an array, regex, or undefined » | [MongoDB, Documents](https://www.mongodb.com/docs/manual/core/document/), lu le 14/10/2026 |
| Un-à-un : imbriquer | [MongoDB, One-to-One Embedded](https://www.mongodb.com/docs/manual/tutorial/model-embedded-one-to-one-relationships-between-documents/), lu le 14/10/2026 |
| Bug du paiement | Fil-Rouge-API `7e40e8d` |
| Swagger expliqué | FIN2 ; Fil-Rouge-API `ea67e20` |
| Refacto à venir, dépriorisée | Robin HOTTON, message relayé par Sébastien sur Discord, 14/10/2026 ; schéma `decoupage_robin.png` (Discord, même jour) |
| `user.id` = `sub` du JWT | `API/src/app/utils/security.py:143` |
| `is_hunter_ai` déjà au schéma | `01_create_fil_rouge_immobilier.sql:300` |

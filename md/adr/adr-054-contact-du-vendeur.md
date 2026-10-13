### ADR-054 : Le contact du vendeur d'un bien — une table à part, `estate_contact`

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 13/10/2026
* **Statut :** accepté pour la table (Sébastien, Discord, 13/10/2026) ; 4 points 🟡 encore ouverts, avec un choix prudent provisoire
* **Décideurs :** Sébastien (« je valide l'ajout de la table estate_contact », Discord, 13/10/2026). Le manque a été vu par Gabriel le même jour.
* **Complète :** ADR-047 (l'auteur d'un bien) ; ADR-007 (format du téléphone) ; ADR-053, P2 (format de l'email)
* **Voir aussi :** ADR-049 (anonymisation) ; ADR-028 (droits par rôle)

**Contexte**

* Le CSV des annonces a un contact par bien : nom, téléphone, email, agence, et une case « particulier ».
* `normalised/normalised.py:428-434` nettoie ces champs, mais **aucune colonne** ne les recevait : tout était perdu à l'import.
* Comptes sur `normalised/annonces_normalised.csv` (2 556 annonces) : nom **1 542**, téléphone **1 792**, email **1 251**, agence **1 026** (6 agences) ; **87** annonces sans aucun contact.
* « particulier » : **406** « vrai » ; **166** de ces annonces ont aussi une agence, ce qui se contredit.
* Ce sont des **données personnelles d'un tiers**, le vendeur.

**Décision**

1. **Une table à part, `estate_contact`** : 0 ou 1 ligne par bien (`id_estate` `UNIQUE`). Pas 5 colonnes dans `estate` : à part, le contact se cache, s'efface ou s'anonymise sans toucher au bien.
2. **Ses colonnes** : `seller_type` (`'private'`, `'agency'` ou vide), `agency_name`, `contact_name`, `phone_number`, `email`, `id_estate`, `id_author`, `created_at`.
3. **Ce que la base refuse** :
   * un téléphone hors du format d'ADR-007 (`+33612345678`) ; le `06…` du CSV est repris en `+336…` ;
   * un email hors de la forme de `"user".email` (ADR-053, P2) ;
   * un nom ou une agence vide ou entouré d'espaces ;
   * une ligne **sans aucun renseignement** (`ck_estate_contact_not_empty`) : pas de contact connu, pas de ligne.
4. **Qui voit et écrit** : **Admin**, **Hunter** et **Manager** seulement, en lecture comme en écriture. **Client** : non, l'offre passe au vendeur « par l'intermédiaire de mon chasseur » (`user-stories/03_particulier_offre_et_signature.feature:16`). **Reader** : non plus, par minimisation.
5. **L'auteur** : comme ADR-047, `id_author` est le compte du jeton, la valeur envoyée est ignorée, un `PUT` ne la change pas ; vide = contact importé.

**Les choix prudents provisoires** 🟡

Ces points n'ont pas été tranchés par le groupe. Le code prend le choix qui ne perd ni n'invente rien ; il se change sans casser le schéma.

| Question | Choix provisoire | Pourquoi |
|---|---|---|
| Les **166** « particulier + agence » | `seller_type` **vide** | On ne devine pas lequel des deux est faux |
| « particulier » vide dans le CSV | **inconnu** (`seller_type` vide), pas « agence » | `normalised.py` change un vide en `False` ; la table, elle, ne le reprend pas |
| Une table `agency` (6 agences) | **Non** : le nom de l'agence en texte | Six noms ne valent pas une table ; à revoir s'il faut des coordonnées d'agence |
| Durée de conservation | **Pas encore codée** | Idée : anonymiser quand le bien n'est plus suivi, même geste qu'ADR-049 ; la durée reste à fixer |

**Ce qui est fait (13/10/2026, dépôt Fil-Rouge-API)**

* Schéma : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (21 tables, 270 colonnes) ; migration `docker/migrations/v2-vers-v3/40_contact-du-bien.sql` pour une base existante.
* Données : `docker/tools/generate_estate_contact.py` lit le CSV et écrit `docker/init-v3/06_populate_estate_contact.sql` : **2 469** contacts (226 `'private'`, 860 `'agency'`, 1 383 vides) ; 87 annonces sans ligne.
* API : `/estate-contacts`, 4 routes ; `routes/crud_router.py` reçoit `read_roles` pour fermer la lecture.
* Tests : `API/tests/integration/test_contact_vendeur.py`, 14 tests.

**Questions ouvertes** 🟡

1. Les **166** « particulier + agence » : croire l'agence, croire « particulier », ou laisser vide (choix provisoire) ?
2. Corriger `normalised.py` pour garder « inconnu » au lieu de `False` ?
3. Une table `agency` à part, ou le nom en texte (choix provisoire) ?
4. Combien de mois garder le contact après la fin du suivi du bien ?
5. Le compte PostgreSQL en lecture seule `fil_rouge_reader` lit aussi `estate_contact` (droit sur toutes les tables). Faut-il le lui retirer ?

⚠️ Les contacts du CSV sont faux (emails en `example.com`, une centaine de noms qui reviennent) : bons pour les tests. La règle de droits et de conservation vaut pour les vrais.

**Sources**

| Affirmation | Source |
|---|---|
| La table est validée | Sébastien, Discord, 13/10/2026 |
| Le manque à l'import | Gabriel, Discord, 13/10/2026 ; `normalised/normalised.py:428-434` |
| Les comptes du CSV | `normalised/annonces_normalised.csv`, compté le 13/10/2026 |
| Le client passe par son chasseur | `user-stories/03_particulier_offre_et_signature.feature:16` |
| Format du téléphone | ADR-007 |

### ADR-054 : Le contact du vendeur d'un bien — une table à part, `estate_contact`

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 13/10/2026
* **Statut :** accepté (Sébastien, Discord, 13/10/2026) : la table, puis les 5 questions ouvertes, tranchées le même jour. **À notifier à Jeff** (voir la fin).
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
2. **Ses colonnes** : `is_private` (vrai ou faux, obligatoire), `agency_name`, `contact_name`, `phone_number`, `email`, `id_estate`, `id_author`, `created_at`.
3. **Ce que la base refuse** :
   * un téléphone hors du format d'ADR-007 (`+33612345678`) ; le `06…` du CSV est repris en `+336…` ;
   * un email hors de la forme de `"user".email` (ADR-053, P2) ;
   * un nom ou une agence vide ou entouré d'espaces ;
   * une ligne **sans aucun renseignement** (`ck_estate_contact_not_empty`) : pas de contact connu, pas de ligne.
4. **Qui voit et écrit** : **Admin**, **Hunter** et **Manager** seulement, en lecture comme en écriture. **Client** : non, l'offre passe au vendeur « par l'intermédiaire de mon chasseur » (`user-stories/03_particulier_offre_et_signature.feature:16`). **Reader** : non plus, par minimisation.
   * Les trois rôles **créent** un contact, pas le seul Hunter : plus souple, retenu par Sébastien (Discord, 13/10/2026), contre « Hunter seul » et « Hunter et Manager, comme un bien ».
5. **L'auteur** : comme ADR-047, `id_author` est le compte du jeton, la valeur envoyée est ignorée, un `PUT` ne la change pas ; vide = contact importé.
   * Pourquoi pas déduit de `estate.id_author` (question de Gabriel, 13/10/2026) : les deux auteurs diffèrent. Les 2 556 biens importés n'ont pas d'auteur ; un contact trouvé plus tard par un chasseur doit dire lequel. Un même bien peut aussi être proposé sur plusieurs mandats, par des chasseurs différents.
   * Le vendeur n'est **pas** un `user` : ses coordonnées sont du texte dans la table. `id_author` désigne le membre de l'agence qui a noté le contact.

**Les 5 questions, tranchées le 13/10/2026** ✅

Le premier code avait pris un choix prudent provisoire (une colonne `seller_type` : `'private'`, `'agency'` ou vide). Sébastien a tranché sur la page à cartes, puis sur Discord.

| Question | Décision | Ce que ça change |
|---|---|---|
| 1. Les **166** « particulier + agence » | **On garde les deux** : `is_private` vrai **et** le nom de l'agence | Aucune perte d'information ; on ne devine pas lequel est faux |
| 2. « particulier » vide dans le CSV | **Vrai ou faux, jamais vide**, en base aussi : `is_private BOOLEAN NOT NULL` | `seller_type` est retirée ; `normalised.py` sort déjà vrai ou faux, il ne change pas |
| 3. Une table `agency` (6 agences) | **Non** : le nom de l'agence en texte | Rien à changer |
| 4. Durée de conservation | **3 ans** après la fin du suivi du bien | Écrit, **pas encore codé** |
| 5. `fil_rouge_reader` | **Retiré** : le compte d'analyse ne lit plus la table | `REVOKE` dans `04`, migration 41 |

**Ce qui est fait (13/10/2026, dépôt Fil-Rouge-API)**

* Schéma : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (21 tables, 270 colonnes) ; migration `docker/migrations/v2-vers-v3/40_contact-du-bien.sql` pour une base existante.
* Données : `docker/tools/generate_estate_contact.py` lit le CSV et écrit `docker/init-v3/06_populate_estate_contact.sql` : **2 469** contacts (`is_private` : **392** vrais, **2 077** faux) ; 87 annonces sans ligne.
* Migrations pour une base existante : 40 (la table), 41 (lecteur fermé), 42 (`seller_type` → `is_private`, puis rejouer 06).
* API : `/estate-contacts`, 4 routes ; `routes/crud_router.py` reçoit `read_roles` pour fermer la lecture.
* Tests : `API/tests/integration/test_contact_vendeur.py`, 16 tests ; suite entière **435 passed**, 8 skipped, 6 xfailed.

**Questions** ✅ toutes tranchées

Expliquées, avec leurs options, sur la page à cartes `md/journal/2026-10-13-questions-contact-vendeur.html`.

1. ~~Les **166** « particulier + agence » : croire l'agence, croire « particulier », ou laisser vide ?~~ ✅ Tranchée le 13/10/2026 : **on garde les deux** (Sébastien, Discord).
2. ~~Corriger `normalised.py` pour garder « inconnu » au lieu de `False` ?~~ ✅ Tranchée le 13/10/2026 : **vrai ou faux, jamais vide**, même en base (Sébastien, Discord). `normalised.py` le fait déjà.
3. ~~Une table `agency` à part, ou le nom en texte ?~~ ✅ Tranchée le 13/10/2026 : **le nom en texte** (Sébastien, Discord). Rien à changer.
4. ~~Combien de mois garder le contact après la fin du suivi du bien ?~~ ✅ Tranchée le 13/10/2026 : **3 ans** après la fin du suivi du bien (Sébastien, Discord). Repère : la CNIL conseille 3 ans pour un prospect ([référentiel « gestion des activités commerciales »](https://www.cnil.fr/sites/cnil/files/atoms/files/referentiel_traitements-donnees-caractere-personnel_gestion-activites-commerciales.pdf), lu le 13/10/2026) ; le vendeur n'est pas un prospect, c'est un rapprochement. **Écrit, pas encore codé** : l'effacement suivra le geste d'ADR-049 (champs vidés, ligne gardée).
5. ~~Le compte PostgreSQL en lecture seule `fil_rouge_reader` lit aussi `estate_contact`. Faut-il le lui retirer ?~~ ✅ Tranchée le 13/10/2026 : **retiré** (Sébastien, Discord). `REVOKE` dans `docker/init-v3/04_role-lecture-seule.sql`, migration `41_contact-ferme-au-lecteur.sql` pour une base existante.

⚠️ Les contacts du CSV sont faux (emails en `example.com`, une centaine de noms qui reviennent) : bons pour les tests. La règle de droits et de conservation vaut pour les vrais.

**À notifier à Jeff** 📣

Décision prise par le groupe sans lui, à lui présenter (demandé par Sébastien, Discord, 13/10/2026) :

* le contact du vendeur est gardé, dans une table à part, `estate_contact` ;
* seuls Admin, Hunter et Manager le voient ; ni le client, ni le rôle Reader, ni le compte d'analyse `fil_rouge_reader` ;
* « particulier » est vrai ou faux, gardé avec le nom de l'agence ;
* durée de conservation : 3 ans après la fin du suivi du bien, pas encore codée.

**Sources**

| Affirmation | Source |
|---|---|
| La table est validée | Sébastien, Discord, 13/10/2026 |
| Les 5 réponses | Sébastien, page à cartes `md/journal/2026-10-13-questions-contact-vendeur.html` et Discord, 13/10/2026 |
| 3 ans pour un prospect | CNIL, référentiel « gestion des activités commerciales », lu le 13/10/2026 |
| Le manque à l'import | Gabriel, Discord, 13/10/2026 ; `normalised/normalised.py:428-434` |
| Les comptes du CSV | `normalised/annonces_normalised.csv`, compté le 13/10/2026 |
| Le client passe par son chasseur | `user-stories/03_particulier_offre_et_signature.feature:16` |
| Format du téléphone | ADR-007 |

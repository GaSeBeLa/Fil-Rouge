# ADR-017 : Ajout d'un identifiant technique propre à chaque table Client, Hunter, RealEstateManager

> Copié de Confluence (page 52330664, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 07/09/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte**

Suite à l'ADR-005, la table `utilisateurs` a été séparée en `user` (racine) et trois sous-tables `Client`, `Hunter`, `RealEstateManager`, chacune reliée à `user` via un champ `id_user` (FK `UNIQUE NOT NULL`). Il reste à trancher si `id_user` doit également servir de clé primaire de ces sous-tables (schéma dit « shared primary key »), ou si chaque sous-table doit disposer de son propre identifiant technique autonome.

**Options envisagées**

- Option 1 : Utiliser `id_user` directement comme clé primaire des tables `Client`, `Hunter` et `RealEstateManager` (pas d'id technique séparé).
- Option 2 : Ajouter un identifiant technique propre à chaque sous-table (`id_client`, `id_hunter`, `id_real_estate_manager`), tout en conservant `id_user` comme simple clé étrangère (`UNIQUE NOT NULL`).

**Décision**

Option 2 retenue. Chaque table `Client`, `Hunter` et `RealEstateManager` possède son propre identifiant technique autonome, indépendant de `id_user`.

**Justification**

Découpler la clé primaire de chaque sous-table de celle de la table `user` évite de lier la génération des identifiants entre tables parentes et filles. Chaque table peut ainsi générer ses identifiants de façon totalement autonome, avec son propre mécanisme natif (séquence, auto-incrément, etc.), sans dépendre du schéma de génération de clé d'une autre table. Cette approche uniformise également la structure du modèle : toutes les tables du projet suivent la même convention (un id technique propre + des clés étrangères vers les tables liées), ce qui simplifie la lecture du schéma et la maintenance du code (ORM, migrations).

Ce découplage est également un gage de portabilité vis-à-vis du SGBD. Avec l'option 1 (clé primaire partagée), la génération de `id_client`, `id_hunter` ou `id_real_estate_manager` resterait entièrement dépendante du mécanisme de génération de `id_user`, un mécanisme dont l'implémentation (séquences, types auto-incrémentés, etc.) varie d'un SGBD à l'autre. En donnant à chaque sous-table son propre identifiant autonome, on s'assure qu'un changement futur de SGBD n'impose pas de repenser la stratégie de clé primaire des sous-tables en fonction de celle de `user`. Actuellement, sans ce nouvel id, une telle migration poserait problème.

**Conséquences**

- **Base de données :** chaque table conserve un identifiant primaire indépendant en plus du champ `id_user` (FK `UNIQUE NOT NULL`) ; une jointure via `id_user` reste nécessaire pour retrouver l'utilisateur parent (déjà le cas depuis l'ADR-005).
- **Développement :** légère cohérence supplémentaire pour les ORM et les migrations, chaque entité étant identifiable indépendamment de sa relation avec `user`.
- **Stockage :** surcoût mineur (une colonne id supplémentaire par sous-table).
- **Portabilité :** en cas de changement futur de SGBD, la stratégie de génération des clés primaires de `Client`, `Hunter` et `RealEstateManager` pourra être adaptée indépendamment de celle de `user`, sans contrainte de compatibilité entre les deux.

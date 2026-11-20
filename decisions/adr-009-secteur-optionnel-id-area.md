# ADR-009 : Caractère optionnel du secteur (id_area NULLABLE)

> Copié de Confluence (page 51578340, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 19/08/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte :** Lors de la modélisation géographique de la table `SearchRequest`, il faut définir les contraintes sur les clés étrangères liant la demande à une localisation (`id_town` pour la ville, `id_area` pour le secteur/quartier). La réalité géographique et métier est que certaines villes (notamment les petites communes ou villages) ne possèdent tout simplement pas de découpage en quartiers ou secteurs.

**Options envisagées**

- Option 1 : Rendre le champ `id_area` obligatoire (NOT NULL), ce qui obligerait à créer des quartiers fictifs (ex: "Secteur unique" ou "Toute la ville") dans la base de données pour les villes concernées.
- Option 2 : Rendre le champ `id_area` optionnel (NULLABLE).

**Décision :** Option 2 retenue. Le champ `id_area` est défini avec la mention `NULLABLE` (clé étrangère optionnelle).

**Justification :** Cette modélisation s'adapte fidèlement à la réalité du terrain. Si une ville ne possède pas de quartiers, il est illogique de forcer la saisie de cette donnée. L'utilisation du `NULLABLE` permet d'enregistrer une recherche proprement sur la ville sans polluer la base de données avec des données géographiques inventées.

**Conséquences**

- **Base de données :** La base autorisera l'enregistrement d'une recherche avec un `id_area` vide (`NULL`).
- **Développement SQL :** Les requêtes de correspondance (matching) entre les demandes et les biens devront gérer cette condition : si `id_area` est `NULL`, la recherche s'effectue uniquement sur l'`id_town`.
- **Interface utilisateur :** L'interface devra être dynamique. Si l'utilisateur sélectionne une ville qui ne possède aucun quartier répertorié dans la table `Area`, le champ de sélection du secteur devra être masqué ou désactivé pour éviter toute confusion.

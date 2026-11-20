# ADR-011 : Ajout d'une référence métier (champ reference) pour les mandats

> Copié de Confluence (page 52690971, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 19/08/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte :** La table `Mandate` utilise un identifiant technique (`id_mandate`) pour lier les données entre les tables (clés étrangères). Cependant, lors de l'impression du contrat officiel ou des échanges avec le client, il est nécessaire d'afficher un numéro de dossier lisible, formel et formaté (par exemple : "MAND-2026-08-102").

**Options envisagées**

- Option 1 : Utiliser directement la clé primaire technique (`id_mandate`) comme numéro sur les documents imprimés.
- Option 2 : Créer un champ distinct `reference` de type VARCHAR, dédié spécifiquement à l'identifiant métier du document.

**Décision :** Option 2 retenue. Ajout d'un champ `reference` dans la table `Mandate`.

**Justification :** Cette décision permet de séparer la logique technique de la logique métier. La clé primaire technique (`id_mandate`) sert au bon fonctionnement de la base de données. Le champ `reference` permet d'appliquer des règles de formatage spécifiques à l'entreprise (année, code agence, etc.) pour les documents légaux. De plus, si la base de données change un jour, la référence légale du contrat restera intacte.

**Conséquences**

- **Base de données :** Le champ `reference` devra comporter une contrainte d'unicité (`UNIQUE`) pour éviter que deux contrats n'aient le même numéro formel.
- **Développement (Back-end) :** Il faudra coder un petit algorithme ou une fonction qui générera automatiquement cette référence avec le bon format au moment de la création du mandat.

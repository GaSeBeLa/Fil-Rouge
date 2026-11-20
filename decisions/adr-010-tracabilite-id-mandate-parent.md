# ADR-010 : Traçabilité et renouvellement (id_mandate_parent)

> Copié de Confluence (page 52168202, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 19/08/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte :** Un mandat de recherche a une durée de validité limitée à 6 mois. À son expiration, un nouveau mandat est signé. Il est nécessaire de lier ces contrats entre eux pour conserver l'historique du client de manière structurée.

**Options envisagées**

- Option 1 : Créer une table externe dédiée à l'historique.
- Option 2 : Ajouter une clé étrangère réflexive `id_mandate_parent` dans la table `Mandate`.

**Décision :** Option 2 retenue. Ajout du champ `id_mandate_parent` dans la table `Mandate`, avec la contrainte `NULLABLE`.

**Justification :** C'est la méthode la plus simple. Le nouveau mandat enregistre l'ID de l'ancien. S'il s'agit du tout premier contrat pour un client, ce champ reste vide (`NULL`).

**Conséquences**

- **Base de données :** Le champ doit être `NULLABLE` pour accepter les premiers mandats.
- **Développement :** Pour afficher l'historique complet, les développeurs devront utiliser une requête SQL capable de remonter cette chaîne d'identifiants.

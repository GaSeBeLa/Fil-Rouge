# ADR-013 : Implémentation d'une relation réflexive pour l'historisation des versions (Tables Criteria et Mandate)

> Copié de Confluence (page 52297834, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 22/08/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte**

Dans le cadre du projet, certains objets métiers clés comme les critères de recherche d'un client (`Criteria`) et les contrats de mandat (`Mandate`) sont amenés à évoluer au fil du temps (avenants, modifications de prix, ajustement des besoins). Pour répondre aux exigences de traçabilité et d'historisation sans écraser les données précédentes, il est indispensable de lier les versions successives entre elles.

**Options envisagées**

- **Option 1 :** Écraser les données à chaque modification (absence totale d'historique).
- **Option 2 :** Créer des tables d'archive séparées ou utiliser un simple champ textuel de version sans lien physique direct.
- **Option 3 :** Mettre en place une relation réflexive (auto-référence) au sein de chaque table (`Criteria` et `Mandate`) via une clé étrangère pointant vers sa propre clé primaire.

**Décision**

Option 3 retenue. Implémentation d'une relation réflexive (boucle) sur la table `Criteria` et sur la table `Mandate`.

**Justification**

Cette approche structurelle garantit une traçabilité rigoureuse, explicite et homogène pour les entités dynamiques du système. Chaque nouvelle version ou avenant pointe directement vers son antécédent, ce qui assure un suivi chronologique parfait (arbre généalogique des modifications) conforme aux bonnes pratiques de modélisation et aux attentes du projet.

**Conséquences**

- **Base de données :** Présence d'une clé étrangère auto-référente au sein des tables `Criteria` et `Mandate` pour relier un enregistrement à sa version précédente.
- **Développement SQL :** Les requêtes pourront exploiter ces auto-références pour reconstituer l'historique exact des modifications et identifier rapidement les éléments actifs.
- **Gestion métier :** Traçabilité totale des évolutions contractuelles (`Mandate`) et des ajustements de prospection (`Criteria`) tout au long du cycle de vie du dossier.

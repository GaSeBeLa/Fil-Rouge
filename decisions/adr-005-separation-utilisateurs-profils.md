# ADR-005 : Séparation de utilisateurs en user/Client/Hunter/RealEstateManager

> Copié de Confluence (page 51578319, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 05/08/2026

**Statut :** accepté

**Décideurs :** L'équipe projet

**Contexte**
La table `utilisateurs` (legacy) mélangeait clients et chasseurs via une colonne `role` texte, forçant des NULL par conception (`budget_max`, `taux_commission`). Cf. registre C3, C4, C12 (chasseur enregistré comme client).

**Options envisagées**

1. Conserver une table unique, gérer les NULL côté applicatif.
2. Normaliser en séparant les profils en entités distinctes.

**Décision**
Option 2 retenue, sans entité `Person` : `utilisateurs` devient `user` dans le schéma cible (racine minimaliste : id, email, password, `id_role` → table `role`) + trois sous-tables `Hunter`, `Client`, `RealEstateManager`, chacune avec `id` technique propre, `id_user UNIQUE NOT NULL`, et ses attributs (y compris identité, redescendue depuis `user`).

**Justification**
Chaque attribut va dans l'entité qui le concerne, éliminant les NULL par conception. `role` en table de lookup plutôt qu'un CHECK figé permet d'ajouter `RealEstateManager` sans migration de schéma lourde.

**Conséquences**
Pas de contrainte XT : rien n'empêche en base qu'un `id_user` ait une ligne dans plusieurs sous-tables à la fois — anomalie C12 non structurellement impossible ici, contrairement à la v1. À traiter par trigger, ou à assumer comme contrôle applicatif et à justifier à l'oral. Identité dupliquée sur 3 tables plutôt que centralisée.

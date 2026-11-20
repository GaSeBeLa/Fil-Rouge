# ADR-004 : Choix Durée du mandat et renouvellement

> Copié de Confluence (page 52297877, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 05/08/2026
**Statut :** remplacée par ADR-023

**Décideurs :** L'équipe projet

**Contexte :** Actuellement, il n'y a pas de durée du mandat. Cf. registre des anomalies C8 (« il n'y a pas de date de fin »). On ne peut pas savoir si ce mandat est renouvelé ou non.

**Options envisagées**

- Mettre un attribut `duration` dans la table Mandate
- Mettre un attribut `renewal_count` pour savoir le nombre de fois où le mandat est renouvelé

**Décision :** Ajouter les attributs `duration` et `renewal_count`.

**Justification :** L'attribut `duration` servira à calculer la date de fin du contrat, non stockée en base de données car calculée. Il permet de changer la durée des mandats si besoin, et ce à un endroit unique dans le code sans avoir à changer les formules de calcul.

L'attribut `renewal_count` permet de savoir le nombre de renouvellements du contrat.

**Conséquences :** Ajout des attributs `duration` et `renewal_count` dans la table Mandate. Voir les schémas MCD fix, MLD fix et MPD fix.

# ADR-008 : Horodatage dans la table de jonction « SearchRequest_Criteria »

> Copié de Confluence (page 52297813, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 19/08/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte :** Lorsqu'un client formule une demande de recherche, ses critères évoluent souvent dans le temps. Par exemple, un client peut décider d'ajouter le critère « Piscine » trois semaines après sa demande initiale. Il est nécessaire de pouvoir retracer la chronologie exacte de l'ajout de ces critères pour le suivi métier.

**Options envisagées**

- Option 1 : Une table de jonction simple ne contenant que les clés étrangères (`id_search_request`, `id_criteria`), sans notion de temps.
- Option 2 : Ajouter un champ d'horodatage `created_at` (DateTime) dans la table de jonction `SearchRequest_Criteria`.

**Décision :** Option 2 retenue. Ajout du champ `created_at` de type DateTime dans la table `SearchRequest_Criteria`.

**Justification :** Cette décision permet l'historisation des données. Ajouter une date permet de savoir exactement quand le lien entre la demande et le critère a été créé. Cela offre une trace temporelle précise de l'évolution de la recherche, évitant de croire qu'un critère ajouté tardivement était présent depuis le début.

**Conséquences**

- **Développement :** Lors de chaque ajout d'un critère à une demande via l'application, le système (ou la base de données via une valeur par défaut comme `CURRENT_TIMESTAMP`) devra obligatoirement enregistrer la date et l'heure exactes.
- **Exploitation :** Il sera possible de trier l'affichage des critères par ordre chronologique d'ajout dans l'interface du chasseur immobilier, ou de faire des statistiques sur l'évolution des demandes.

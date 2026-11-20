# ADR-006 : Champ description table « Mandate »

> Copié de Confluence (page 52168181, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 05/08/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte :** Dans le système actuel, `mandats.description_recherche` stocke tous les critères de recherche du client en texte libre (TEXT), non structurés, sans historisation. Cf. registre des anomalies C10. Ce champ mélange des critères filtrables (type de bien, surface, DPE) avec des appréciations non structurables (« charme ancien », « standing »).

**Options envisagées :**

1. Conserver un champ texte libre unique, sans structuration.
2. Séparer les critères en colonnes typées (type de bien, surface, DPE) et en une table de référence pour les équipements (`Criteria`), tout en conservant un champ texte libre résiduel pour ce qui n'est pas structurable.

**Décision :** Option 2 retenue. Les critères filtrables deviennent des colonnes typées sur `SearchRequest` (`type_estate`, `surface`, `dpe` via FK vers `Dpe`). Les équipements/critères optionnels (balcon, jardin, alternatives type « ou ») passent par une table `Criteria` et une jonction `SearchRequest_Criteria`. Ce qui reste non structurable est conservé dans `SearchRequest.free_comment`.

**Justification :** Cette séparation rend les critères courants filtrables et interrogeables — ce qui était impossible avec le texte libre — tout en ne perdant aucune information : le texte original reste accessible via `free_comment` pour les appréciations subjectives. La jonction `SearchRequest_Criteria` permet en particulier de représenter des critères alternatifs (« terrasse ou jardin »), ce qu'un champ texte ou une colonne simple ne pouvaient pas exprimer.

**Conséquences :** `description_recherche` disparaît du modèle cible, remplacé par les colonnes typées de `SearchRequest` + la table `Criteria`. Migration : chaque description existante doit être relue pour en extraire les critères structurables ; ce qui ne l'est pas est reversé tel quel dans `free_comment`. Point de vigilance sur le typage de `free_comment` : `Varchar(100)` suffit aux données actuelles (64 caractères maximum mesurés) mais laisse peu de marge — `TEXT` serait plus sûr pour un champ dont la longueur n'est pas contrainte par nature.

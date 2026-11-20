# ADR-020 : Codification des pays via ISO 3166-1 alpha-2 (country_iso CHAR(2)) plutôt que le nom en clair

> Copié de Confluence (page 52625502, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 10/09/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte**

Les tables `Hunter`, `Client`, `RealEstateManager`, `Estate` et `Criteria` stockent chacune un pays via une colonne `country_iso CHAR(2)`, contrainte par un `CHECK (country_iso IN ('FR','ES','DE','GB','IE','BE','NL','LU','IT','CH'))`. Il faut trancher si cette colonne doit porter un code normalisé à deux lettres ou le nom du pays en clair (`VARCHAR`).

**Options envisagées**

- Option 1 : Nom du pays en texte (`VARCHAR`, ex. `"France"`, `"Allemagne"`).
- Option 2 : Code ISO 3166-1 alpha-2 (`CHAR(2)`, ex. `FR`, `DE`), avec `CHECK` fermé sur la liste des pays couverts.

**Décision**

Option 2 retenue. `country_iso CHAR(2)` sur toutes les tables portant une notion de pays.

**Justification**

- **Économie de stockage :** `CHAR(2)` occupe 2 octets fixes contre 6 à 20+ octets variables pour un nom de pays en `VARCHAR` (encodage UTF-8 des accents inclus). Le gain par ligne est modeste, mais se cumule sur cinq tables et un volume appelé à croître fortement en Phase 3 (international) — un gain marginal individuellement, non négligeable une fois multiplié.
- **Standard non ambigu :** ISO 3166-1 est la référence internationale. Un nom en texte libre ouvre la porte à des variantes (`France`, `france`, `FRANCE`, espace parasite) qui cassent silencieusement les `GROUP BY` et les filtres — un problème que le code fixe élimine par construction.
- **Neutralité linguistique :** cohérent avec l'ADR-002 (schémas et code en anglais, métier discuté en français) — `DE` ne varie pas selon qu'on affiche `Allemagne` ou `Germany` à l'écran. Le nom localisé relève de la couche présentation, jamais du stockage.
- **Type fixe, comparaisons et jointures plus rapides :** une colonne de longueur fixe se compare et s'indexe plus efficacement qu'une chaîne de longueur variable, et rend le `CHECK IN (...)` trivial à maintenir pour fermer la liste des pays couverts par l'agence.

**Conséquences**

- Toute nouvelle table portant une notion de pays doit reprendre `country_iso CHAR(2)` avec la même contrainte, pour rester cohérente avec l'existant.
- **Distinction à ne pas confondre avec l'ADR-007 (révisé) :** `country_iso` et `phone_number` portent tous les deux une information de pays, mais ne se traitent pas de la même façon — et ce n'est pas une incohérence. `country_iso` alimente des règles métier fermées (filtrage, statistiques, `CHECK` sur une liste connue de pays couverts par l'agence), ce qui justifie un code structuré et contraint. `phone_number` (`VARCHAR(20) NOT NULL`, indicatif inclus, cf. ADR-007) est une valeur de contact international à préserver telle quelle, jamais interrogée pour elle-même — un champ structuré y ajouterait de la rigidité sans bénéfice métier réel. Les deux décisions optimisent pour des usages différents de la même notion de pays.
- **Dette technique assumée à signaler à l'oral :** le `CHECK` est actuellement dupliqué à l'identique sur cinq tables plutôt que centralisé dans une table de référence `Country(iso_code PK, name_fr, name_en, ...)`. Ajouter un pays couvert impose aujourd'hui de modifier le `CHECK` sur chacune des cinq tables. Une table de référence serait plus robuste à terme (source unique de vérité, et permettrait d'y stocker aussi les noms localisés) — non retenue pour l'instant faute de besoin immédiat, mais à réévaluer si le nombre de pays couverts continue de croître en Phase 3.
- L'affichage du nom complet du pays dans l'interface doit passer par une table de correspondance ISO → nom localisé côté application (ou une librairie i18n standard), jamais par une valeur stockée en base.

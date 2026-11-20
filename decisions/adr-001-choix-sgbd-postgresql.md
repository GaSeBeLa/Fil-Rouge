# ADR-001 : Choix du SGBD (SQLite vs MariaDB/MySQL vs PostgreSQL)

> Copié de Confluence (page 52363362, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 30/07/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte :** Le projet doit choisir un SGBD unique dès la Phase 1, car ce choix conditionne le dialecte SQL de tous les livrables à venir (migration.sql, requêtes OLTP/OLAP, indexation). La décision doit donc être projetée sur l'ensemble du cycle de vie du projet, pas seulement sur l'existant à 3 tables :

- absorber la croissance annoncée en Phase 3 (international, milliers de mandats/semaine) ;
- supporter l'usage analytique/IA prévu en Phase 4 (OLAP, features de matching) ;
- structurer les critères de recherche actuellement en texte libre (Phase 2), ce qui suppose des types de données riches ;
- servir un backend multi-utilisateurs (particuliers, chasseurs) en accès concurrent.

**Options envisagées**

*Élimination préalable : SQLite.* SQLite est un moteur embarqué (fichier local, un seul processus d'écriture à la fois), pensé pour des applications mono-utilisateur ou des prototypes. Il ne propose ni gestion native des accès concurrents en écriture, ni partitionnement, ni réplication serveur — trois besoins déjà identifiés pour ce projet (multi-utilisateurs dès la Phase 1, croissance internationale en Phase 3). SQLite est donc écarté d'emblée, avant même la comparaison pondérée, et n'entre pas dans le tableau ci-dessous qui compare uniquement les deux candidats serveur restants.

| Critère (pondération) | MariaDB/MySQL | PostgreSQL |
| --- | --- | --- |
| Partitionnement (x3) — nécessaire pour le volume/international en Phase 3 | Existe mais moins mature en déclaratif ; gestion manuelle plus lourde à grande échelle | Partitionnement déclaratif natif (RANGE/LIST), adapté à un découpage par pays ou par période |
| Richesse des types & contraintes (x3) — critères de recherche structurés (Phase 2), JSONB en transition | Types JSON plus limités, CHECK constraints historiquement moins complets | Types JSON/JSONB indexables, CHECK/EXCLUSION constraints matures, extensions (ex. PostGIS pour la géoloc des secteurs) |
| Écosystème analytique (x2) — besoin OLAP/IA en Phase 3-4 | Fonctions analytiques plus limitées | Window functions complètes, vues matérialisées, extensions analytiques (ex. TimescaleDB) |
| Simplicité / prise en main de l'équipe (x1) | Légèrement plus familier pour certains membres | Courbe d'apprentissage un peu plus longue mais documentation abondante |
| Écosystème hébergement / coût (x1) | Très répandu chez les hébergeurs low-cost | Également largement supporté par le cloud managé (RDS, Cloud SQL, etc.) |

**Score pondéré (barème 1 à 3 par critère) :** MySQL = 24/30 · PostgreSQL = 29/30 — PostgreSQL l'emporte, porté surtout par le partitionnement et la richesse des types.

**Décision :** PostgreSQL.

**Justification :** SQLite est écarté en premier lieu car son modèle embarqué mono-écrivain est structurellement incompatible avec un backend multi-utilisateurs dès la Phase 1, et plus encore avec la croissance visée en Phase 3. Entre les deux candidats serveur restants, les deux critères qui pèsent le plus lourd pour ce projet — partitionnement (préparation de la Phase 3) et richesse des types/contraintes (préparation de la Phase 2, structuration des critères de recherche) — sont ceux où l'écart entre MySQL et PostgreSQL est le plus net. La légère perte de familiarité de l'équipe (critère mineur, pondération 1) ne compense pas cet écart. Ce choix évite également une migration de SGBD entre la Phase 1 et la Phase 3, ce qui aurait été un risque et un coût inutiles.

**Conséquences**

- Tout le SQL du projet (migration, OLTP/OLAP, indexation) sera écrit en dialecte PostgreSQL.
- Les fixtures fournies en MySQL (`fixtures/MySQL.sql`) ne serviront que de référence de lecture ; la version PostgreSQL (`fixtures/PgSQL.sql`) est la source de vérité pour le développement.
- SQLite reste envisageable uniquement pour des besoins hors périmètre (ex. tests unitaires locaux, prototypage rapide), jamais comme SGBD de production.
- Ce choix devra être réévalué si le dimensionnement 3V produit en Phase 3 révèle un besoin incompatible avec PostgreSQL (peu probable mais à vérifier).

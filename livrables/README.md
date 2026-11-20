# Livrables — projet fil rouge « Chasse immobilière »

Équipe GaSeBeLa : Sébastien, Gabriel, Laurence, Békanty.

Cette page liste **tous les livrables demandés par le sujet** et dit où trouver chacun.
La liste est tirée de trois documents du sujet : le `Readme.md` (livrables par phase), la grille d'évaluation (format visé) et la matrice de traçabilité des compétences.

## Comment c'est rangé

- **Un dossier par phase**, dans l'ordre du sujet : `1-audit/` à `4-application/`, puis `5-transverse/` et `6-pilotage/`.
- **Les livrables portent un numéro** `phase.ordre` : on les lit dans cet ordre.
- **Les appuis** (schémas, scripts de mesure, images) sont dans le sous-dossier `annexes/` de chaque phase, sans numéro.
- Le **code de l'API** est dans un second dépôt : [GaSeBeLa/Fil-Rouge-API](https://github.com/GaSeBeLa/Fil-Rouge-API).

## Phase 1 — Auditer l'existant (BC01)

| N° | Livrable | Fichier |
|---|---|---|
| 1.1 | Cartographie du SI et matrice des risques | [1.1-cartographie-si.md](1-audit/1.1-cartographie-si.md) |
| 1.2 | Registre des anomalies et des risques | [1.2-registre-anomalies-risques.md](1-audit/1.2-registre-anomalies-risques.md) |
| 1.3 | Analyse de l'existant | [1.3-analyse.md](1-audit/1.3-analyse.md) |

## Phase 2 — Répondre au besoin actuel (BC01, BC02, BC05)

| N° | Livrable | Fichier |
|---|---|---|
| 2.1 | Étude d'opportunité | [2.1-etude-opportunite.md](2-modelisation/2.1-etude-opportunite.md) |
| 2.2 | Note stratégique (axes d'évolution) | [2.2-note-strategique.md](2-modelisation/2.2-note-strategique.md) |
| 2.3 | Note de cadrage, avec la matrice des risques et leur mitigation (§ 9) | [2.3-note-de-cadrage.md](2-modelisation/2.3-note-de-cadrage.md) |
| 2.4 | Backlog priorisé (MoSCoW) | [2.4-backlog-moscow.md](2-modelisation/2.4-backlog-moscow.md) |
| 2.5 | Cahier des charges technique | [2.5-cahier-des-charges-technique.md](2-modelisation/2.5-cahier-des-charges-technique.md) |
| 2.6 | MCD / MLD cible | [mcd.md](2-modelisation/mcd.md) |
| 2.7 | Script de migration (`migration.sql`) | [2.7-migration.sql](2-modelisation/2.7-migration.sql) — copie ; la source est dans le dépôt de l'API |
| 2.8 | Note d'indexation (EXPLAIN avant/après) | [2.8-note-indexation.md](2-modelisation/2.8-note-indexation.md) |

Appuis : [3 schémas des données](2-modelisation/annexes/) et le script de mesure des index.

## Phase 3 — Absorber la croissance (BC01, BC02, BC05)

| N° | Livrable | Fichier |
|---|---|---|
| 3.1 | Note de dimensionnement 3V | [3.1-note-dimensionnement-3v.md](3-architecture/3.1-note-dimensionnement-3v.md) |
| 3.2 | Dossier d'architecture | [3.2-dossier-architecture.md](3-architecture/3.2-dossier-architecture.md) |
| 3.3 | Matrice de décision | [3.3-matrice-decision-architecture.md](3-architecture/3.3-matrice-decision-architecture.md) |
| 3.4 | Schéma analytique (OLAP) et alimentation des données | [3.4-olap.md](3-architecture/3.4-olap.md) |
| 3.5 | PCA / PRA et plan de migration | [3.5-pca-pra-plan-de-migration.md](3-architecture/3.5-pca-pra-plan-de-migration.md) |
| 3.6 | Note d'environnement technique | [3.6-note-environnement-technique.md](3-architecture/3.6-note-environnement-technique.md) |
| 3.7 | Note de qualité des données | [3.7-note-qualite-donnees.md](3-architecture/3.7-note-qualite-donnees.md) |

Appuis : [4 schémas d'architecture, la SWOT de croissance, les mesures de charge et de qualité](3-architecture/annexes/README.md).

## Phase 4 — Réaliser le parcours futur avec l'IA (BC03, BC05)

| N° | Livrable | Fichier |
|---|---|---|
| 4.1 | Dossier de conception applicative et maquettes | [4.1-conception-applicative.md](4-application/4.1-conception-applicative.md), [4.1-maquettes-espace-acquereur.html](4-application/4.1-maquettes-espace-acquereur.html) |
| 4.2 | Processus métier | [4.2-processus-metier.md](4-application/4.2-processus-metier.md) |
| 4.3 | Plan de tests : scénarios fonctionnels | [4.3-tests-fonctionnels.md](4-application/4.3-tests-fonctionnels.md) |
| 4.4 | Plan de tests : rapport d'exécution | [4.4-rapport-tests.md](4-application/4.4-rapport-tests.md) |
| 4.5 | Note de sécurité applicative | [4.5-note-securite-applicative.md](4-application/4.5-note-securite-applicative.md) |
| 4.6 | Schéma du programme d'IA | [4.6-schema-programme-ia.md](4-application/4.6-schema-programme-ia.md) (et sa version [HTML](4-application/4.6-schema-programme-ia.html)) |
| 4.7 | Conception du modèle de matching et features | [4.7-conception-matching-features.md](4-application/4.7-conception-matching-features.md) |
| 4.8 | Pipeline d'intégration continue | à venir |

Appuis : [schéma de connexion](4-application/annexes/schema-connexion-et-jeton.md), script des essais d'attaque, images des processus.

## Exigences transverses (obligatoires)

| N° | Livrable | Fichier |
|---|---|---|
| 5.1 | Registre RGPD | [5.1-registre-rgpd.md](5-transverse/5.1-registre-rgpd.md) |
| 5.2 | Note d'éco-conception | [5.2-note-eco-conception.md](5-transverse/5.2-note-eco-conception.md) |
| 5.3 | Note d'accessibilité PSH | [5.3-note-accessibilite-psh.md](5-transverse/5.3-note-accessibilite-psh.md) |
| 5.4 | Note de souveraineté et de sécurité IA | [5.4-note-souverainete-securite-ia.md](5-transverse/5.4-note-souverainete-securite-ia.md) |

## Pilotage (toutes phases, BC02)

| N° | Livrable | Fichier |
|---|---|---|
| 6.1 | Planning (Gantt) et jalons | [6.1-gantt.md](6-pilotage/6.1-gantt.md) |
| 6.2 | RACI | [6.2-raci.md](6-pilotage/6.2-raci.md) |
| 6.3 | Grille d'auto-évaluation | [6.3-grille-auto-evaluation.md](6-pilotage/6.3-grille-auto-evaluation.md) |
| 6.4 | Comptes rendus d'ateliers | à venir |

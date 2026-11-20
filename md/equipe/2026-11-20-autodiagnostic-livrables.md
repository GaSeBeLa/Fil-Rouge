# Autodiagnostic des livrables — 2026-11-20

> Demandé par Gabriel (Discord, 2026-11-20) : « relis les livrables et fais un autodiagnostic et une autocritique ; sois factuel, évite les biais de confirmation, assume tes erreurs, ne te force pas à trouver des erreurs ».
> Méthode : 3 relectures indépendantes en lecture seule (phases 1-2, phase 3, phases 4-6), chaque constat cité `fichier:ligne` ; longueur comptée en mots (~500 mots = 1 page) face au format de `GRILLE-EVALUATION.md` § 1. **10 constats revérifiés à la main par le Glaude : 10 confirmés.**

## 1. Le verdict d'ensemble

- ✅ **Le fond tient** : les calculs (matrice, 3V, indexation, tests fonctionnels) ont été refaits et sont justes ; aucun lien relatif cassé ; les chiffres d'audit sont vérifiés dans les fixtures.
- ❌ **La forme n'est pas celle d'une synthèse** : trop long, trop de travail interne, des brouillons, et des contradictions entre fichiers.
- ❌ **Une partie des erreurs vient du Glaude, ce matin** : la mise à jour du 2026-11-20 (sauvegarde, en-têtes, tests) n'a été reportée que dans une partie des fichiers, et la note d'environnement cite une source inventée.

## 2. Les erreurs du Glaude, assumées

| Erreur | Où | Fait |
|---|---|---|
| Source inventée : le dossier d'architecture ne parle jamais de Kubernetes | `3-architecture/note-environnement-technique.md:33` | vérifié : 0 occurrence |
| Mise à jour reportée à moitié : « aucune sauvegarde planifiée », « 3 traitements de nuit », « aucune mesure de charge » | SWOT l.32, 60, 66 ; dossier d'architecture l.40, 64, 142, 152 ; schéma 03 l.64 ; note d'environnement l.43 | vérifié |
| RPO de 1 h affiché, alors que la sauvegarde codée est quotidienne (RPO réel : 24 h), non dit | `pca-pra-plan-de-migration.md:61` | vérifié |
| Durée de garde : 7 jours codés, « 7, 30 et 90 jours » écrits | `note-eco-conception.md:24` | vérifié |
| Grille : « note d'environnement : pas écrite » | `grille-auto-evaluation.md:33` | vérifié |
| Nombre de tests : 1 120, 1 116 ou 1 123 selon le fichier | note de sécurité, rapport de tests, tests fonctionnels, processus, grille, note d'environnement | vérifié |

## 3. Les autres problèmes, par gravité

### Fond (faux ou contradictoire)

1. **Le MCD est vide** dans le dépôt (`2-modelisation/mcd.md` : 3 lignes « image non copiée ») ; ses justifications ne sont qu'une TODO. Livrable pivot de BC05.
2. **L'étude d'opportunité contredit le registre** : elle cite « continuité du développement » parmi les 3 risques cotés 9 (`etude-opportunite.md:48`), or R09 est coté **6** ; la scalabilité n'est pas une ligne du registre.
3. **SWOT contre 3V, matrice et dossier** : « 133 Go… un seul serveur ne suffira pas » (`swot-croissance.md:46`) contre « une instance PostgreSQL suffit ».
4. **Cardinalité bien–vente fausse** : `07-donnees-vente-et-remuneration.md:39` dessine `estate ||--o{ sale` (plusieurs ventes), le schéma a `uq_sale_estate UNIQUE (id_estate)`.
5. **Note stratégique** : « Migration vers PostgreSQL » (l.39) alors que l'existant y est déjà ; tables `offres` et « suivi des signatures » (l.33-34) inexistantes.
6. **Droits du chasseur-IA** : la note de souveraineté (l.87) les dit réduits comme un fait ; le schéma IA dit qu'ils ne sont pas codés.
7. **Petites erreurs** : niveau WCAG 2.1.1 « — » au lieu de **A** (`note-accessibilite-psh.md:28`) ; `POST /login` au lieu de `/auth/login` (`08-connexion-et-jeton.md:22`) ; « l'entreprise GaseBela » (`note-de-cadrage.md:8`) alors que c'est le nom de l'équipe ; ADR-007 contre ADR-008 pour le téléphone (registre l.97 contre CDC l.435) ; numéros de ligne du sujet décalés (cartographie).

### Forme (pas une synthèse)

- **Trop long face à la grille** : note 3V ≈ 5 pages (cible 1-2) ; dossier + matrice ≈ 6,5 pages ; registre RGPD ≈ 4,5 pages (cible : 1 tableau) ; rapport de tests ≈ 8 pages ; CDC ≈ 15 pages ; note de sécurité ≈ 4,5 pages ; PCA/PRA ≈ 5 pages.
- **Fichiers hors grille rangés avec les livrables** : `09-contraintes-a-coder`, `09-decisions-a-prendre`, `09-rapport-ecarts-contraintes` (≈ 14 000 mots, datés du 2026-09-11, « 18 tables », décision en milliers d'euros) ; `inventaire-donnees-personnelles` ; `note-eco-conception-confluence-v2` (doublon de la note courte) ; `mcd-a-mettre-a-jour` (TODO).
- **Encore en brouillon** : « À COMPLÉTER » (note de cadrage, RACI) ; « Brouillon / à relire » (dossier d'architecture, matrice, PCA/PRA, matching, accessibilité, éco-conception) ; grille d'auto-évaluation non remplie.
- **Jargon interne** dans le texte : codes de fiches (SUG, FLX, LOT, DRO, RGPD-n), choix (ENV-B, SEC-…), hashes de commit, « le Glaude », chemins `context AI/`, `md/journal/`.

### Ce qui manque au sujet

- Pipeline CI ; comptes rendus d'ateliers ; MCD (schéma + justifications) ; validation du RACI.
- Processus en Mermaid, pas en BPMN (à assumer ou à refaire).

## 4. Ce qui est bon (RAS)

- `1-audit/03-analyse.md`, `2-modelisation/olap.md`, `note-indexation.md`, `05` et `06-donnees-*`, `4-application/conception-applicative.md`, `tests-fonctionnels.md`, `processus-metier.md`, `maquettes-espace-acquereur.html`, `6-pilotage/gantt.md`, `note-eco-conception.md` (courte) : synthétiques et justes, à un chiffre périmé près.

## 5. Non vérifié

- « 83 % des surfaces » (étude d'opportunité) ; les sources externes de la note 3V ; le détail du rapport 09 (lu dans ses grandes lignes).

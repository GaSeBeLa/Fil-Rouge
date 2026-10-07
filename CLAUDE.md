# Fil Rouge Immobilier — à lire en premier, en entier, et seul

Projet fil rouge EISI Data-IA : audit de données, modélisation et API REST
(FastAPI + SQLModel sur PostgreSQL) pour un service de chasse immobilière.
Ce n'est **pas** un produit hébergé : pas de front, pas de déploiement.
Dossier `Fil-Rouge/`, dépôt git à sa racine. L'énoncé et les fixtures d'origine
vivent dans `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/` et
`../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack/` — **lecture seule, jamais
modifiés**.

## Où on en est — en cinq lignes

- Le schéma PostgreSQL **v3** (**19 tables**, montants en **euros**) est posé
  dans `docker/init-v3/` et monté par `docker compose` : chantier LOT, LOT1 à
  LOT12 faits le 2026-10-07 (LOT12 : rôle en lecture seule `fil_rouge_reader`).
  Changements par thème : `docker/init-v3/README.md` §0. `docker/init-v2/` est
  **figé**, gardé pour le banc `docker/compare_v2_v3.sh` ;
  `docker/migrations/v2-vers-v3/` mène une base v2 existante au même schéma ;
  `docker/init/` (12 tables, K€) est l'ancien schéma, plus monté.
- **Pour l'équipe, après un pull** : ajouter `POSTGRES_READER_PASSWORD=` à
  `docker/.env` (voir `.env.exemple`), puis depuis `docker/`,
  `docker compose down -v && docker compose up -d` (⚠️ efface la base de dev
  locale), puis `bash docker/create_test_db.sh`.
- L'API expose un CRUD complet en trois couches (routes / services /
  repositories) sur les **19 tables** ; le routeur commun revalide l'entrée
  (`422` avant la base). 91 opérations vérifiées en `200` contre la base
  (mesuré avant LOT6). **187 tests** : 99 unitaires sans base (dont les 55
  cas de rémunération), 88 d'intégration sur la base de test isolée
  `fil_rouge_test` (`docker/create_test_db.sh`) — voir `API/README.md` § Tests.
- Les user stories Gherkin (`user-stories/`) couvrent le parcours actuel et le
  futur parcours IA. Seul le **calcul de rémunération** est implémenté
  (`services/remuneration.py`, code du sujet, non branché sur la base).
- `normalised/` porte la normalisation des annonces et son rapport d'anomalies.
- `livrables/2-modelisation/` porte trois rapports du chantier `C` ; les trois
  autres livrables sont vides. Détail daté dans `context AI/08-etat.md`.

## Cinq règles non négociables

1. **Annoncer le plan en une ou deux phrases avant d'agir**, et poser un
   questionnaire au moindre choix ouvert.
2. **Mesurer avant de corriger**, et afficher les comptes bruts à côté du
   verdict — un instrument muet rend son propre échec indiagnosticable.
3. **Les deux dossiers `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack*/` ne se
   modifient jamais**, et `docker/init-v3/01_create_fil_rouge_immobilier.sql`
   est le schéma de référence : tout modèle SQLModel s'y confronte par grep.
   `docker/init-v2/` est figé : il ne se modifie plus.
4. **Tout montant est en euros** — jamais en K€ (`docker/init-v3/README.md`
   §1). Deux types depuis le 2026-10-05 (Q-REM-01) : prix, budgets, bornes du
   barème et part fixe en **`INTEGER`** (`int`) ; honoraires et paiement en
   **`NUMERIC(12,2)`** (`Decimal`), car le sujet arrondit au centime.
5. **Aucun secret ni `.env` dans git**, aucun chemin absolu dans le code.

Les ADR ne vivent pas dans le dépôt mais sur Confluence : le dossier
`decisions/` ne contient qu'un `.gitkeep`, et rien ne s'écrit sur Confluence
depuis le dépôt — la synchronisation est manuelle, et décidée par le groupe.

Prose et commentaires de code en français ; noms de code en anglais.
Le contexte IA (`CLAUDE.md`, `context AI/`) est **versionné** : le projet se
travaille à plusieurs. Les notes métier libres vivent dans `md/`.

## Routage — ouvrir ceci, et rien d'autre

Cette table remplace la lecture de `00-INDEX.md`. Si la tâche n'y figure pas,
et seulement dans ce cas, ouvrir l'index.

| La tâche | Ouvrir |
|---|---|
| écrire ou modifier du code de l'API | `API/README.md`, puis le fichier visé |
| lancer l'API et son Swagger | `docker compose up -d api` depuis `docker/`, puis http://localhost:8000/docs |
| créer un module, chercher où va un bout de code | `API/src/app/main.py` — son en-tête décrit les trois couches |
| vérifier une règle métier | `user-stories/<NN>_*.feature` |
| vérifier une table, une colonne, une contrainte | `docker/init-v3/01_create_fil_rouge_immobilier.sql` |
| comprendre un choix du schéma (euros, migration, hypothèses, changements v3) | `docker/init-v3/README.md` |
| relire une décision d'architecture (ADR) | **Confluence**, espace `GaSeBeLa1` — [wiki du projet](https://laurenceamethyste.atlassian.net/wiki/spaces/GaSeBeLa1/overview?homepageId=15008134). Le dossier `decisions/` du dépôt est **vide**, rien n'y est écrit |
| ouvrir un chantier, ou le découper en fiches | **lancer `/vlp:chantier`** — la méthode vit dans le kit, pas ici |
| relire une fiche `C1` à `C5` | `context AI/09-contraintes-mpd.md` — chantier **clos** le 2026-09-11, ne se rejoue pas |
| jouer une fiche `LOT1` à `LOT12` | **lancer `/vlp:tache LOT<n>`** — chantier **en cours** « Lot de migration (schéma v3) », fiches dans `context AI/10-lot-migration.md` |
| reprendre après une longue interruption | `context AI/08-etat.md` |

## Économie de contexte

La fenêtre sature par **densité de contexte**, pas par volume horaire. Donc,
dans cet ordre :

- **Un fichier de contexte ne s'ouvre que si la table ci-dessus le nomme.** Le
  voisin d'un fichier utile n'est pas utile ; il n'est que du volume.
- **Ne jamais lire le dossier de contexte en entier**, ni le README.
- **Une tâche, une session.** `/clear` entre deux tâches : une session laissée
  ouverte relit tout son passé à chaque tour.
- **Explorer et lire avec un modèle léger**, garder le lourd pour ce qui décide.
- Grep ciblé plutôt que lecture de fichier entier, dans le code comme ici.

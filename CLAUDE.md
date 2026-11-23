# Fil Rouge Immobilier — à lire en premier, en entier, et seul

Projet fil rouge EISI Data-IA : audit de données, modélisation et API REST
(FastAPI + SQLModel sur PostgreSQL) pour un service de chasse immobilière.
Ce n'est **pas** un produit hébergé : pas de front, pas de déploiement.
Dossier `Fil-Rouge/`, dépôt git à sa racine. L'énoncé et les fixtures d'origine
vivent dans `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/` et
`../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack/` — **lecture seule, jamais
modifiés**.

## Où on en est — en cinq lignes

- ⚠️ **Depuis le 2026-10-13, le code de l'API et `docker/` vivent dans le
  dépôt [Fil-Rouge-API](https://github.com/GaSeBeLa/Fil-Rouge-API)**, cloné à
  côté : `../Fil-Rouge-API/`. Ce dépôt-ci garde les docs, les ADR, les
  livrables et le suivi des chantiers. **Tout chemin `API/…` ou `docker/…`
  cité ici, dans `context AI/` ou dans `md/` se lit dans `../Fil-Rouge-API/`.**
- Le schéma PostgreSQL **v3** (**22 tables** depuis le 2026-10-15 : `estate_contact`, ADR-054, puis `estate_price_history`, FLX4 ; montants en **euros**) est posé
  dans `docker/init-v3/` et monté par `docker compose` : chantier LOT, LOT1 à
  LOT12 faits le 2026-10-07 (LOT12 : rôle en lecture seule `fil_rouge_reader`).
  Changements par thème : `docker/init-v3/README.md` §0. `docker/init-v2/` est
  **figé**, gardé pour le banc v2/v3 (`API/tests/integration/test_banc_v2_v3.py`,
  lancé à chaque pytest, ou par `docker/compare_v2_v3.sh`) ;
  `docker/migrations/v2-vers-v3/` mène une base v2 existante au même schéma ;
  `docker/init/` (12 tables, K€) est l'ancien schéma, plus monté.
- **Pour l'équipe, après un pull** : ajouter `POSTGRES_READER_PASSWORD=` à
  `docker/.env` (voir `.env.exemple`), puis depuis `docker/`,
  `docker compose down -v && docker compose up -d` (⚠️ efface la base de dev
  locale), puis `bash docker/create_test_db.sh`.
- L'API expose, en trois couches (routes / services / repositories), la
  lecture, la création et la modification sur **21 des 22 tables**, **sans
  suppression** (ADR-049 : un compte se désactive puis s'anonymise) ; le routeur
  commun revalide l'entrée (`422` avant la base). **96 opérations** (recomptées
  le 2026-11-20, livrable 4.1). **1 126 passed, 7 xfailed** (au 2026-11-20, après les en-têtes de sécurité et la signature du mandat par le client ; rapport du 2026-11-19, 1 116 :
  `livrables/4-application/4.4-rapport-tests.md`), unitaires sans base et intégration sur la base de test isolée
  `fil_rouge_test` (`docker/create_test_db.sh`) — voir `API/README.md` § Tests.
- **Les droits sont codés** (chantier DRO, 2026-10-13) : le rôle, table par
  table, puis « le sien » (la ligne d'un autre rend `404`) ; les comptes
  désactivés réservés à l'`Admin` ; `fil_rouge_reader` fermé pareil. Relevé et
  écarts : `md/securite/matrice-droits-crud-par-role.md`.
- Les user stories Gherkin (`user-stories/`) couvrent le parcours actuel et le
  futur parcours IA. Seul le **calcul de rémunération** est implémenté
  (`services/remuneration.py`, code du sujet), branché sur la base par
  `POST /sales/{id}/payment` (fiche API12).
- `normalised/` porte la normalisation des annonces et son rapport d'anomalies.
- `livrables/` est rangé par phase depuis le 2026-11-20 (choix A de Gabriel) : `1-audit/` à `6-pilotage/`, les livrables numérotés `<phase>.<ordre>` (`2.3-note-de-cadrage.md`…), les appuis sans numéro dans `<phase>/annexes/` (les 8 schémas Mermaid `schema-*.md`, SWOT, scripts de mesure, images). `livrables/README.md` est la liste officielle des 36 livrables du sujet, pour le jury. 12 pages de travail y sont copiées (le dépôt fait foi) ; les versions longues sont en `md/equipe/*-complete.md` ; les documents de travail sont dans `md/`. Détail daté dans `context AI/08-etat.md`.
- Clos le 2026-10-15 : clés vers les fiches et rôles des fiches (chantier PRF).
- Clos le 2026-10-15 : Airflow, Elasticsearch, Logstash et Kibana branchés sur l'API (chantier FLX).
- Clos le 2026-11-03 : clos sans rien livrer, recadrage à venir (chantier MER).
- Clos le 2026-11-03 : un moteur de suggestion de biens et des propositions cohérentes (chantier SUG).
- Clos le 2026-11-03 : RGPD : registre, droits et note IA (chantier RGP).

## Cinq règles non négociables

1. **Annoncer le plan en une ou deux phrases avant d'agir**, et poser un
   questionnaire au moindre choix ouvert.
2. **Mesurer avant de corriger**, et afficher les comptes bruts à côté du
   verdict — un instrument muet rend son propre échec indiagnosticable.
3. **Les deux dossiers `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack*/` ne se
   modifient jamais**, et `docker/init-v3/01_create_fil_rouge_immobilier.sql`
   (dans `../Fil-Rouge-API/`) est le schéma de référence : tout modèle SQLModel s'y confronte par grep.
   `docker/init-v2/` est figé : il ne se modifie plus.
4. **Tout montant est en euros** — jamais en K€ (`docker/init-v3/README.md`
   §1). Deux types depuis le 2026-10-05 (Q-REM-01) : prix, budgets, bornes du
   barème et part fixe en **`INTEGER`** (`int`) ; honoraires et paiement en
   **`NUMERIC(12,2)`** (`Decimal`), car le sujet arrondit au centime.
5. **Aucun secret ni `.env` dans git**, aucun chemin absolu dans le code.

**Tout vit sur GitHub depuis le 2026-11-20** (choix de Gabriel) : les ADR sont dans
`decisions/` (71 fichiers, copiés de Confluence puis complétés, index `decisions/README.md`),
et le dépôt fait foi. Confluence n'est plus mis à jour ; aucun livrable n'y renvoie.

Prose et commentaires de code en français ; noms de code en anglais.
Le contexte IA (`CLAUDE.md`, `context AI/`) est **versionné** : le projet se
travaille à plusieurs. Les notes métier libres vivent dans `md/`.

## Ramasser sa poubelle

Une modification n'est finie que quand ce qu'elle a rendu faux a disparu
(proposé par Gabriel le 2026-10-12, adopté par Sébastien le 2026-10-13).

1. Même commit : commentaires, en-têtes, docstrings et doc du code touché mis
   à jour (compte, nom, unité, renvoi `fichier:ligne`).
2. Le code mort laissé est supprimé, pas commenté.
3. Avant le commit : grep de l'ancienne valeur dans tout le dépôt (et dans
   `../Fil-Rouge-API/`) ; chaque reste vivant est corrigé ou signalé.
4. Un chiffre en commentaire se recompte ; s'il n'apporte rien, il ne s'écrit pas.
5. Exception : l'historique daté (journal, rapport, ADR, fiche close) ne se
   réécrit pas.
6. ADR : un ADR accepté ne se réécrit pas. Créer ou modifier un ADR → les ADR
   qu'il contredit passent à « remplacé par ADR-0XX », renvois mis à jour des
   deux côtés, dans `decisions/`.

## Routage — ouvrir ceci, et rien d'autre

Cette table remplace la lecture de `00-INDEX.md`. Si la tâche n'y figure pas,
et seulement dans ce cas, ouvrir l'index.

| La tâche | Ouvrir |
|---|---|
| écrire ou modifier du code de l'API | **dans `../Fil-Rouge-API/`** : `API/README.md`, puis le fichier visé |
| lancer l'API et son Swagger | `docker compose up -d api` depuis `../Fil-Rouge-API/docker/`, puis http://localhost:8000/docs |
| créer un module, chercher où va un bout de code | `../Fil-Rouge-API/API/src/app/main.py` — son en-tête décrit les trois couches |
| vérifier une règle métier | `user-stories/<NN>_*.feature` |
| vérifier une table, une colonne, une contrainte | `../Fil-Rouge-API/docker/init-v3/01_create_fil_rouge_immobilier.sql` |
| comprendre un choix du schéma (euros, migration, hypothèses, changements v3) | `../Fil-Rouge-API/docker/init-v3/README.md` |
| relire une décision d'architecture (ADR) | `decisions/README.md`, puis le fichier de l'ADR |
| ouvrir un chantier, ou le découper en fiches | **lancer `/vlp:chantier`** — la méthode vit dans le kit, pas ici |
| relire un chantier clos | `context AI/00-INDEX-archive.md` — sa ligne y nomme le fichier de fiches |
| relire une fiche `C1` à `C5` | `context AI/09-contraintes-mpd.md` — chantier **clos** le 2026-09-11, ne se rejoue pas |
| relire une fiche `LOT1` à `LOT12` | `context AI/10-lot-migration.md` — chantier « Lot de migration (schéma v3) » **clos** le 2026-10-07, ne se rejoue pas |
| relire une fiche `API1` à `API12` | `context AI/11-api-auth-rgpd-regles.md` — chantier « API : auth, RGPD et règles métier » **clos** le 2026-10-13, ne se rejoue pas |
| relire une fiche `DRO1` à `DRO11` | `context AI/12-droits-moindre-privilege.md` — chantier « Droits : moindre privilège » **clos** le 2026-10-13, ne se rejoue pas |
| relire une fiche `FIN1` à `FIN2` | `context AI/13-finitions-api.md` — chantier « Finitions de l'API : erreurs et Swagger » **clos** le 2026-10-14, ne se rejoue pas |
| relire une fiche `BAN1` à `BAN3` | `context AI/14-banc-v2-v3.md` — chantier « Réparer le banc v2/v3 » **clos** le 2026-10-14, ne se rejoue pas |
| relire une fiche `DEM1` à `DEM3` | `context AI/15-seed-demo.md` — chantier « Seed de démo » **clos** le 2026-10-14, ne se rejoue pas |
| relire une fiche `FLX1` à `FLX14` | `context AI/17-flux-donnees.md` — chantier « Flux de données : Airflow et Elasticsearch » **clos** le 2026-10-15, ne se rejoue pas ; `FLX14` (contact du vendeur à l'import), ajoutée le 2026-10-19, faite le 2026-11-02 ; le flux en un dessin : `md/flux/schema-du-flux.md` |
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

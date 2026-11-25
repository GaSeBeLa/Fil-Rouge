# Fil Rouge Immobilier — à lire en premier, en entier, et seul

Projet fil rouge EISI Data-IA : audit de données, modélisation et API REST
(FastAPI + SQLModel sur PostgreSQL) pour un service de chasse immobilière.
Ce n'est **pas** un produit hébergé : pas de front, pas de déploiement.
Dossier `Fil-Rouge/`, dépôt git à sa racine. L'énoncé et les fixtures d'origine
vivent dans `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/` et
`../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack/` — **lecture seule, jamais
modifiés**.

## Où on en est — en cinq lignes

- ⚠️ **Depuis le 2026-10-13, le code de l'API et `docker/` vivent dans
  [Fil-Rouge-API](https://github.com/GaSeBeLa/Fil-Rouge-API)**, cloné en
  `../Fil-Rouge-API/` ; ici : docs, ADR, livrables, chantiers. **Tout chemin `API/…` ou `docker/…`
  cité ici, dans `context AI/` ou dans `md/` se lit dans `../Fil-Rouge-API/`.**
- Le schéma PostgreSQL **v3** (**22 tables**, montants en **euros**) est posé
  dans `docker/init-v3/`, monté par `docker compose` ; changements par thème :
  `docker/init-v3/README.md` §0 ; historique : `context AI/08-etat.md`.
- L'API expose, en trois couches (routes / services / repositories), la
  lecture, la création et la modification sur **21 des 22 tables**, **sans
  suppression** (ADR-049 : un compte se désactive puis s'anonymise) ; le routeur
  commun revalide l'entrée (`422` avant la base). Tests : unitaires sans base,
  intégration sur la base isolée `fil_rouge_test` — voir `API/README.md` § Tests ;
  derniers comptes : `livrables/4-application/4.4-rapport-tests.md`.
- **Les droits sont codés** (DRO) : le rôle par table, puis « le sien » (sinon
  `404`) ; relevé et écarts : `md/securite/matrice-droits-crud-par-role.md`.
- Les user stories Gherkin (`user-stories/`) couvrent le parcours actuel et le
  futur parcours IA. Seul le **calcul de rémunération** est implémenté
  (`services/remuneration.py`), branché par `POST /sales/{id}/payment`.
- `livrables/` est rangé par phase (`1-audit/` à `6-pilotage/`) ;
  `livrables/README.md` est la liste officielle des livrables, pour le jury.

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

Le dépôt fait foi (ADR dans `decisions/`) ; Confluence n'est plus mis à jour.
Prose et commentaires en français, noms de code en anglais. `CLAUDE.md` et
`context AI/` sont **versionnés** ; les notes métier libres vivent dans `md/`.

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
| écrire ou modifier du code de l'API | `../Fil-Rouge-API/API/README.md`, puis le fichier visé |
| lancer l'API et son Swagger | `docker compose up -d api` depuis `../Fil-Rouge-API/docker/`, puis http://localhost:8000/docs |
| créer un module, chercher où va un bout de code | `../Fil-Rouge-API/API/src/app/main.py` — son en-tête décrit les trois couches |
| vérifier une règle métier | `user-stories/<NN>_*.feature` |
| vérifier une table, une colonne, une contrainte | `../Fil-Rouge-API/docker/init-v3/01_create_fil_rouge_immobilier.sql` |
| comprendre un choix du schéma (euros, migration, hypothèses, changements v3) | `../Fil-Rouge-API/docker/init-v3/README.md` |
| relire une décision d'architecture (ADR) | `decisions/README.md`, puis le fichier de l'ADR |
| ouvrir un chantier, ou le découper en fiches | **lancer `/vlp:chantier`** — la méthode vit dans le kit, pas ici |
| relire un chantier clos | `context AI/00-INDEX-archive.md` — sa ligne y nomme le fichier de fiches (`C1`…`C5`, `LOT1`…, `FLX14`…) |
| reprendre après une longue interruption | `context AI/08-etat.md` |

## Économie de contexte

- **Un fichier de contexte ne s'ouvre que si la table ci-dessus le nomme** ;
  jamais le dossier de contexte en entier, ni le README.
- **Une tâche, une session** : `/clear` entre deux tâches.
- **Explorer et lire avec un modèle léger**, garder le lourd pour ce qui décide.
- Grep ciblé plutôt que lecture de fichier entier, dans le code comme ici.

# Les notes de l'équipe — l'index

> Une ligne par fichier de `md/` : de quoi il parle, et s'il est encore tenu
> à jour. **Un fichier ajouté = une ligne ici.**
>
> Créé le 2026-10-07.

## Les trois types de fichier

| Type | Ce que ça veut dire |
|---|---|
| 📌 **vivant** | mis à jour au fil du projet : sa dernière version est la bonne |
| 📷 **photo** | l'état d'un jour précis : il ne bouge plus, et peut être dépassé |
| 📝 **brouillon d'ADR** | proposition d'ADR : la version qui fait foi est sur **Confluence**, espace `GaSeBeLa1` |

## ⏳ Rangement prévu

- Décidé le 2026-10-07 : les fichiers iront dans les **6 sous-dossiers**
  ci-dessous.
- Ils restent **à la racine de `md/`** jusqu'à la fin du lot de migration
  (chantier LOT), pour ne pas gêner ses commits.
- ⚠️ `docker/init-v2/README.md` est **figé** et cite deux fichiers :
  `adr-024-motif-refus-remuneration.md` et `securite-mots-de-passe-et-droits.md`.
  Après le déplacement, un **petit fichier de renvoi** restera à leur ancienne
  place.

## equipe/ — l'organisation du travail

| Fichier | De quoi il parle | Type |
|---|---|---|
| [kanban.md](kanban.md) | le kanban du développement (GitHub Projects) | 📌 vivant |
| [depots-et-branches.md](depots-et-branches.md) | dépôts, branches, protection de `main` : 4 décisions à prendre | 📌 vivant |

## questions/ — les questions à trancher

| Fichier | De quoi il parle | Type |
|---|---|---|
| [questions-a-trancher-2026-10-02.md](questions-a-trancher-2026-10-02.md) | le **registre** : chaque question et sa réponse | 📌 vivant, malgré la date du nom |
| [questions-a-trancher-2026-10-02.html](questions-a-trancher-2026-10-02.html) | la page à cartes des mêmes questions | 📌 vivant, malgré la date du nom |
| [questions-pour-jeff-2026-10-05.html](questions-pour-jeff-2026-10-05.html) | les questions pour Jeff (client et PO) | 📌 vivant, malgré la date du nom |

## adr/ — les propositions d'ADR

| Fichier | De quoi il parle | Type |
|---|---|---|
| [adr-024-motif-refus-remuneration.md](adr-024-motif-refus-remuneration.md) | ADR-024, le motif de refus d'une rémunération | 📝 brouillon d'ADR |
| [adr-024-modifications-a-faire.md](adr-024-modifications-a-faire.md) | ADR-024, les modifications à faire, en détail | 📝 brouillon d'ADR |
| [adr-025-lien-chasseur-manager.md](adr-025-lien-chasseur-manager.md) | ADR-025, le lien entre chasseur et manager | 📝 brouillon d'ADR |
| [adr-026-perimetre-authentification.md](adr-026-perimetre-authentification.md) | ADR-026, le périmètre de l'authentification | 📝 brouillon d'ADR |
| [adr-027-matrice-acces-par-role.md](adr-027-matrice-acces-par-role.md) | ADR-027, la matrice d'accès par rôle | 📝 brouillon d'ADR |
| [liste-adr-chantier-4-2026-10-07.md](liste-adr-chantier-4-2026-10-07.md) | la liste des ADR du chantier 4 | 📷 photo du 2026-10-07 |

## regles-metier/ — la rémunération et les contraintes

| Fichier | De quoi il parle | Type |
|---|---|---|
| [BAREME-COMMISSION.md](BAREME-COMMISSION.md) | le calcul du barème de commission du chasseur | 📌 vivant |
| [NOTES-REMUNERATION-CHASSEUR.md](NOTES-REMUNERATION-CHASSEUR.md) | les règles de calcul de la rémunération du chasseur | 📌 vivant |
| [schema-tracabilite-remuneration-chasseur_v4.md](schema-tracabilite-remuneration-chasseur_v4.md) | la traçabilité du calcul de rémunération (v4) | 📌 vivant |
| [notes_contraintes_client.md](notes_contraintes_client.md) | les contraintes manquantes sur la table `client` | 📌 vivant |
| [notes_contraintes_localisation_criteria.md](notes_contraintes_localisation_criteria.md) | les contraintes de localisation sur `Criteria` | 📌 vivant |

## securite/ — mots de passe et droits d'accès

| Fichier | De quoi il parle | Type |
|---|---|---|
| [securite-mots-de-passe-et-droits.md](securite-mots-de-passe-et-droits.md) | mots de passe et droits d'accès : ce qu'il reste à faire | 📌 vivant |
| [matrice-droits-crud-par-role.md](matrice-droits-crud-par-role.md) | qui peut faire quoi : la matrice d'accès par rôle | 📌 vivant |
| [tuto-1-hachage-mots-de-passe.md](tuto-1-hachage-mots-de-passe.md) | tuto : hacher les mots de passe (Argon2id) | 📌 vivant |
| [tuto-2-authentification-jwt.md](tuto-2-authentification-jwt.md) | tuto : authentification et droits d'accès (JWT) | 📌 vivant |

## journal/ — les photos d'un jour, de la plus ancienne à la plus récente

| Fichier | De quoi il parle | Type |
|---|---|---|
| [point-etape-2026-09-21.md](point-etape-2026-09-21.md) | point d'étape et plan | 📷 photo du 2026-09-21 |
| [rapport-changements-2026-09-21.md](rapport-changements-2026-09-21.md) | les changements de la séance | 📷 photo du 2026-09-21 |
| [a-faire-a-la-main-2026-09-21.md](a-faire-a-la-main-2026-09-21.md) | ce qui restait à faire à la main | 📷 photo du 2026-09-21 |
| [minio-images-indisponibles-2026-10-02.md](minio-images-indisponibles-2026-10-02.md) | MinIO ne se télécharge plus | 📷 photo du 2026-10-02 |
| [plan-action-2026-10-07.html](plan-action-2026-10-07.html) | le plan d'action après l'entretien avec Jeff | 📷 photo du 2026-10-07 |
| [rapport-lot1-a-lot5-2026-10-07.html](rapport-lot1-a-lot5-2026-10-07.html) | le rapport au groupe sur LOT1 à LOT5 | 📷 photo du 2026-10-07 |

## Les règles de nommage

- **Un fichier par sujet**, rangé dans le sous-dossier de son sujet.
- **Une photo d'un jour commence par sa date**, écrite **AAAA-MM-JJ** :
  `2026-10-07-plan-action.html`. Les fichiers se trient alors tout seuls.
- **Un fichier vivant n'a pas de date dans son nom** : il écrit « mis à jour
  le … » dans son en-tête.
- 💡 Proposé, à valider : des noms en **minuscules**, mots séparés par des
  **tirets** (pas de `MAJUSCULES`, pas de `_`).
- **Un fichier ajouté = une ligne dans cet index.**

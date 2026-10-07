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

## ✅ Rangé

- Les fichiers sont rangés dans les **6 sous-dossiers** ci-dessous
  (décidé le 2026-10-07, fait après le lot de migration).
- ⚠️ `docker/init-v2/README.md` est **figé** et cite deux fichiers à leur
  ancienne place : un **petit fichier de renvoi** y reste.
  - [`adr-024-motif-refus-remuneration.md`](adr-024-motif-refus-remuneration.md) → [`adr/adr-024-motif-refus-remuneration.md`](adr/adr-024-motif-refus-remuneration.md)
  - [`securite-mots-de-passe-et-droits.md`](securite-mots-de-passe-et-droits.md) → [`securite/securite-mots-de-passe-et-droits.md`](securite/securite-mots-de-passe-et-droits.md)

## equipe/ — l'organisation du travail

| Fichier | De quoi il parle | Type |
|---|---|---|
| [kanban.md](equipe/kanban.md) | le kanban du développement (GitHub Projects) | 📌 vivant |
| [depots-et-branches.md](equipe/depots-et-branches.md) | dépôts, branches, protection de `main` : 4 décisions à prendre | 📌 vivant |

## questions/ — les questions à trancher

| Fichier | De quoi il parle | Type |
|---|---|---|
| [questions-a-trancher.md](questions/questions-a-trancher.md) | le **registre** : chaque question et sa réponse | 📌 vivant |
| [questions-a-trancher.html](questions/questions-a-trancher.html) | la page à cartes des mêmes questions | 📌 vivant |
| [questions-pour-jeff.html](questions/questions-pour-jeff.html) | les questions pour Jeff (client et PO) | 📌 vivant |

## adr/ — les propositions d'ADR

| Fichier | De quoi il parle | Type |
|---|---|---|
| [adr-024-motif-refus-remuneration.md](adr/adr-024-motif-refus-remuneration.md) | ADR-024, le motif de refus d'une rémunération | 📝 brouillon d'ADR |
| [adr-024-modifications-a-faire.md](adr/adr-024-modifications-a-faire.md) | ADR-024, les modifications à faire, en détail | 📝 brouillon d'ADR |
| [adr-025-lien-chasseur-manager.md](adr/adr-025-lien-chasseur-manager.md) | ADR-025, le lien entre chasseur et manager | 📝 brouillon d'ADR |
| [adr-026-perimetre-authentification.md](adr/adr-026-perimetre-authentification.md) | ADR-026, le périmètre de l'authentification | 📝 brouillon d'ADR |
| [adr-027-matrice-acces-par-role.md](adr/adr-027-matrice-acces-par-role.md) | ADR-027, la matrice d'accès par rôle | 📝 brouillon d'ADR |
| [2026-10-07-liste-adr-chantier-4.md](adr/2026-10-07-liste-adr-chantier-4.md) | la liste des ADR du chantier 4 | 📷 photo du 2026-10-07 |

## regles-metier/ — la rémunération et les contraintes

| Fichier | De quoi il parle | Type |
|---|---|---|
| [BAREME-COMMISSION.md](regles-metier/BAREME-COMMISSION.md) | le calcul du barème de commission du chasseur | 📌 vivant |
| [NOTES-REMUNERATION-CHASSEUR.md](regles-metier/NOTES-REMUNERATION-CHASSEUR.md) | les règles de calcul de la rémunération du chasseur | 📌 vivant |
| [schema-tracabilite-remuneration-chasseur_v4.md](regles-metier/schema-tracabilite-remuneration-chasseur_v4.md) | la traçabilité du calcul de rémunération (v4) | 📌 vivant |
| [notes_contraintes_client.md](regles-metier/notes_contraintes_client.md) | les contraintes manquantes sur la table `client` | 📌 vivant |
| [notes_contraintes_localisation_criteria.md](regles-metier/notes_contraintes_localisation_criteria.md) | les contraintes de localisation sur `Criteria` | 📌 vivant |

## securite/ — mots de passe et droits d'accès

| Fichier | De quoi il parle | Type |
|---|---|---|
| [securite-mots-de-passe-et-droits.md](securite/securite-mots-de-passe-et-droits.md) | mots de passe et droits d'accès : ce qu'il reste à faire | 📌 vivant |
| [matrice-droits-crud-par-role.md](securite/matrice-droits-crud-par-role.md) | qui peut faire quoi : la matrice d'accès par rôle | 📌 vivant |
| [tuto-1-hachage-mots-de-passe.md](securite/tuto-1-hachage-mots-de-passe.md) | tuto : hacher les mots de passe (Argon2id) | 📌 vivant |
| [tuto-2-authentification-jwt.md](securite/tuto-2-authentification-jwt.md) | tuto : authentification et droits d'accès (JWT) | 📌 vivant |

## journal/ — les photos d'un jour, de la plus ancienne à la plus récente

| Fichier | De quoi il parle | Type |
|---|---|---|
| [2026-09-21-point-etape.md](journal/2026-09-21-point-etape.md) | point d'étape et plan | 📷 photo du 2026-09-21 |
| [2026-09-21-rapport-changements.md](journal/2026-09-21-rapport-changements.md) | les changements de la séance | 📷 photo du 2026-09-21 |
| [2026-09-21-a-faire-a-la-main.md](journal/2026-09-21-a-faire-a-la-main.md) | ce qui restait à faire à la main | 📷 photo du 2026-09-21 |
| [2026-10-02-minio-images-indisponibles.md](journal/2026-10-02-minio-images-indisponibles.md) | MinIO ne se télécharge plus | 📷 photo du 2026-10-02 |
| [2026-10-07-plan-action.html](journal/2026-10-07-plan-action.html) | le plan d'action après l'entretien avec Jeff | 📷 photo du 2026-10-07 |
| [2026-10-07-rapport-lot1-a-lot5.html](journal/2026-10-07-rapport-lot1-a-lot5.html) | le rapport au groupe sur LOT1 à LOT5 | 📷 photo du 2026-10-07 |

## Les règles de nommage

- **Un fichier par sujet**, rangé dans le sous-dossier de son sujet.
- **Une photo d'un jour commence par sa date**, écrite **AAAA-MM-JJ** :
  `2026-10-07-plan-action.html`. Les fichiers se trient alors tout seuls.
- **Un fichier vivant n'a pas de date dans son nom** : il écrit « mis à jour
  le … » dans son en-tête.
- 💡 Proposé, à valider : des noms en **minuscules**, mots séparés par des
  **tirets** (pas de `MAJUSCULES`, pas de `_`).
- **Un fichier ajouté = une ligne dans cet index.**

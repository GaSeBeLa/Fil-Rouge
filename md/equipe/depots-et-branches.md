# Dépôts et branches — proposition

> Proposé le **2026-10-07**. Statut : 🟡 **à décider par l'équipe**.
>
> Repères : ✅ établi, source citée · 💡 proposé · 🟡 à décider · ⚠️ attention.
>
> Va avec la page du kanban : [`md/equipe/kanban.md`](kanban.md).

## En bref

- Aujourd'hui : **un dépôt**, **une branche** (`main`), **aucune protection**,
  **aucune pull request**. Tout le monde pousse directement sur `main`.
- L'équipe penche pour **plusieurs dépôts**.
- 💡 Proposition :
  - **un seul dépôt** ; ou, si on tient à séparer, **deux** : le code d'un
    côté, les livrables de l'autre ;
  - des **branches courtes** fusionnées par pull request (**GitHub Flow**) ;
  - **`main` protégée** : PR obligatoire et une relecture, admins compris.
- 🟡 **4 décisions** à prendre ensemble (§ 6).

## 1. Le constat — mesuré le 2026-10-07

| Ce qu'on mesure | Résultat | Commande |
|---|---|---|
| Dépôts de l'organisation | **2**, tous les deux **publics** | `gh repo list GaSeBeLa` |
| Branches de `Fil-Rouge` | **`main` seule** | `git branch -r` |
| Protection de `main` | **aucune** (« Branch not protected »), **0** règle | `gh api repos/GaSeBeLa/Fil-Rouge/branches/main/protection` et `.../rulesets` |
| Pull requests | **0**, depuis le début | `gh pr list --state all` |
| Commits sur `main` | **145**, par **5** noms d'auteur | `git rev-list --count origin/main` |
| Propriétaires de l'organisation | **4 membres sur 5** | `gh api "orgs/GaSeBeLa/members?role=admin"` |
| Secrets dans le dépôt | **aucun** : `.env` est ignoré (`.gitignore`, ligne 6) | `git ls-files` |

Ce qui relie les dossiers entre eux :

| Lien | Nombre de fichiers | Commande |
|---|---|---|
| `API/src` → schéma SQL de `docker/` | **5** | `git grep -lE 'docker/\|init(-v[0-9])?/\|01_create' -- API/src` |
| API → user stories | **4** | `git grep -lE '\.feature\|user-stories' -- API` |
| API → registre `md/` ou carte `Q-…` | **7** | `git grep -lE 'md/\|questions-a-trancher\|Q-[A-Z]{3}-[0-9]+' -- API` |
| `livrables/` → `docker/` ou `API/` | **2** | `git grep -lE 'docker/\|API/' -- livrables` |

➡️ L'API, le schéma, les user stories et `md/` sont **liés serré**. Les
livrables le sont **peu**.

## 2. Combien de dépôts ?

| Option | Découpage | Pour | Contre |
|---|---|---|---|
| **A** | **un seul** dépôt, comme aujourd'hui | une PR change le code **et** la doc d'un coup ; aucun lien cassé ; le jury lit un seul endroit | les droits sont les mêmes partout |
| **B** | **deux** : `Fil-Rouge` (tout sauf les livrables) et `Fil-Rouge-Livrables` | les livrables du jury vivent à part, avec leur propre historique | **2** livrables renvoient au code ; le livrable 2 (MCD/MLD) se refait **depuis le schéma** (`context AI/08-etat.md`, chantier 6) : un changement de schéma = **2 PR, dans 2 dépôts** |
| **C** | **un par brique** : API, base, docs, données… | chaque brique est isolée | les liens du § 1 sont **tous** coupés ; beaucoup de coordination pour 5 personnes |

- 💡 **Mon avis : A.** Si l'équipe tient à séparer : **B**.
- ⚠️ **Jamais** de coupe entre l'API, le schéma, les user stories et `md/` :
  ce sont eux qui se citent (§ 1).
- 🟡 Pour B : garder l'historique des livrables (outil `git filter-repo`), ou
  repartir d'un dépôt neuf. À trancher si B est choisi.

## 3. Quelles branches ?

| Modèle | Branches | Pour | Contre |
|---|---|---|---|
| **GitHub Flow** | `main` + **branches courtes**, fusionnées par PR | ✅ « lightweight » d'après GitHub ; colle à la colonne **« En revue »** du kanban | pas de branche d'essai avant `main` |
| **Git Flow** | `main` (stable) + **`dev`** (intégration) + branches de fonction, de version, de correctif | `main` reste toujours propre | deux branches longues à garder d'accord ; ✅ son auteur conseille, depuis 2020, un modèle plus simple comme GitHub Flow aux équipes qui livrent en continu |
| Une branche **`doc`** permanente | — | — | ❌ la doc s'éloigne du code |

- Sur la branche `doc` : le guide Gherkin du sujet nomme ce défaut
  « Dérive » (`Gherkin.md`, ligne 31) : « Le document est écrit avant le
  développement puis n'est plus jamais mis à jour. »
- 💡 **Mon avis : GitHub Flow.** Les six étapes, d'après GitHub :
  1. créer une branche ;
  2. faire les changements ;
  3. ouvrir une pull request ;
  4. répondre à la relecture ;
  5. fusionner ;
  6. supprimer la branche.

### 💡 Nommer les branches et les commits

- Branche : **`type/numéro-de-carte-sujet`**, par exemple `feat/12-auth-token`.
  - Le numéro relie la branche à sa **carte du kanban**.
- Types : `feat` (fonction), `fix` (correctif), `docs` (doc), `test`,
  `refactor`.
- Les messages de commit gardent la forme **déjà utilisée** dans le dépôt :
  `type(portée): ce qui change`, par exemple `docs(kanban): …`.

## 4. Protéger `main` ?

💡 Les réglages proposés :

- **Pas de push direct** sur `main` : tout passe par une **pull request**.
- **1 relecture** approuvée, par une autre personne.
- **Pas de push forcé**, pas de suppression de `main`.
- **Les admins aussi.**

⚠️ À savoir avant de trancher :

- **4 membres sur 5 sont propriétaires** de l'organisation. Si les admins
  peuvent passer outre, la protection ne protège presque rien.
- Ça **change la façon de travailler** de ceux qui commitent sur `main`, en
  local puis en un seul push, comme avec le kit `vlp` : ils passeraient par
  une branche et une PR.
- 🟡 Gratuité pour un dépôt public : **indice, pas preuve**. L'API répond
  « Branch not protected » au lieu de demander une offre payante. La preuve,
  ce sera de créer la règle.

## 5. 💡 Règles pour tout nouveau dépôt

Valables quel que soit le choix du § 2 :

- Nom en **`Fil-Rouge-<brique>`**.
- **Public** : c'est un projet d'école.
- Un **README** qui dit à quoi sert le dépôt, et renvoie au kanban.
- Un **`.gitignore`** qui couvre **`.env`**, et un `.env.exemple` sans secret.
- **`main` protégée**, selon le § 4.
- **Lié au projet kanban** : <https://github.com/orgs/GaSeBeLa/projects/1>

## 6. 🟡 Les 4 décisions à prendre

| # | Question | Choix possibles | 💡 Proposé |
|---|---|---|---|
| 1 | Combien de dépôts ? | A, B ou C (§ 2) | **A** ; sinon **B** |
| 2 | Quel modèle de branches ? | GitHub Flow ou Git Flow (§ 3) | **GitHub Flow** |
| 3 | Protéger `main`, admins compris ? | oui ou non (§ 4) | **oui** |
| 4 | Rendre le **kanban** public, comme le dépôt ? | oui ou non | **oui** |

## 7. Ce qu'on vous demande

1. **Lire** cette page.
2. **Répondre aux 4 questions** du § 6 sur Discord, par exemple :
   « 1 A, 2 GitHub Flow, 3 oui, 4 oui ».

## Sources — consultées le 2026-10-07

- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
  — GitHub Docs, doc officielle : définition et six étapes.
- [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)
  — Vincent Driessen, l'auteur de Git Flow. Article du 5 janvier 2010, note
  ajoutée le 5 mars 2020.
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
  — GitHub Docs : relectures obligatoires avant fusion.
- `Gherkin.md`, ligne 31 — dans
  `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/documents utiles/`.

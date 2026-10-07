# Kanban du développement

> Proposé le **2026-10-07**. Statut : 🟡 **à valider par l'équipe**.
>
> Repères : ✅ établi, source citée · 💡 proposé · 🟡 à décider · ⏳ en attente.

## En bref

- Un tableau **kanban** pour suivre le développement, dans **GitHub Projects**.
- ✅ **Le tableau** : <https://github.com/orgs/GaSeBeLa/projects/1>
  - Créé le 2026-10-07 dans l'organisation **GaSeBeLa**, lié au dépôt
    **Fil-Rouge**. Projet **privé** : visible des membres de l'organisation.
- **5 colonnes** : Backlog → À faire → En cours → En revue → Fait.
- 🟡 **Une décision à prendre ensemble** : quelles cartes on met au départ (§ 5).

## 1. Pourquoi un kanban

- ✅ La grille d'évaluation attend un **backlog priorisé**, « MoSCoW ou équivalent ».
  - Sources : `GRILLE-EVALUATION.md` ligne 72, et `TRACABILITE-COMPETENCES.md`
    ligne 47, dans `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/documents utiles/`.
  - ➡️ Le tableau peut servir de **preuve** pour cette case.
- 💡 Voir d'un coup d'œil **qui fait quoi**, et ne pas travailler à deux sur la
  même chose.

## 2. Pourquoi GitHub Projects

| Outil | Gratuit | Pour | Contre |
|---|---|---|---|
| ✅ **GitHub Projects** (choisi) | ✅ créé sur l'offre **free** de l'organisation | à côté du **code** : une PR qui dit `Closes #12` ferme la carte | chacun a besoin d'un **compte GitHub** avec accès au projet |
| Jira | ✅ jusqu'à 10 utilisateurs | même site Atlassian que **Confluence** (les ADR) | ❌ **accès refusé (403)** le 2026-10-07 |
| Trello | ✅ jusqu'à 10 collaborateurs | le plus **simple** | séparé du code et des ADR |
| Un fichier `KANBAN.md` | ✅ | aucun outil | pas de glisser-déposer ; un commit par déplacement |

- Choix fait le **2026-10-07**.

## 3. Les colonnes

| Colonne | Ce qu'on y met |
|---|---|
| **Backlog** | les idées, le travail pas encore prêt |
| **À faire** | prêt à prendre : on sait ce qui est attendu |
| **En cours** | quelqu'un travaille dessus, et la carte lui est assignée |
| **En revue** | fini : une PR attend la relecture d'un autre membre |
| **Fait** | relu, et fusionné dans `main` |

- ✅ **Automatique**, réglage par défaut de GitHub : une issue ou une PR
  **fermée** passe en **Fait** ; une PR **fusionnée** aussi.

## 4. Les règles d'usage — 💡 proposées, à valider

1. **On s'assigne la carte** avant de commencer.
2. **Deux cartes « En cours » au plus** par personne.
   - ✅ GitHub peut afficher une limite par colonne, mais elle **n'empêche
     rien** : c'est un repère, pas un blocage.
3. **Une PR cite sa carte** : `Closes #12` dans sa description.
   - ✅ Autres mots acceptés : `fixes`, `resolves`, et leurs variantes.
   - ✅ Ça ne marche que si la PR vise la **branche par défaut** (`main`).
4. **Une autre personne relit** avant « Fait ».

## 5. 🟡 À décider ensemble : les cartes de départ

| Choix | Ce qu'on met | Ce que ça donne |
|---|---|---|
| **a** | les **9 chantiers** de la feuille de route ([`context AI/08-etat.md`](../../context%20AI/08-etat.md), section « La TODO ordonnée ») | le suivi du dev, simple |
| **b** | les **11 user stories** ([`user-stories/`](../../user-stories), fichiers `00` à `10`), chacune avec une priorité MoSCoW | le **backlog priorisé** de la grille |
| **c** | les deux : user stories = backlog, chantiers = travail en cours | les deux usages, mais plus de cartes |

- MoSCoW = **Must**, **Should**, **Could**, **Won't** (doit, devrait, pourrait,
  pas cette fois).
- 🟡 La priorité d'une user story : c'est **Jeff (PO)** qui tranche ; le groupe
  peut proposer.
- ⚠️ Certains chantiers sont déjà découpés en **fiches** avec le kit `vlp`
  (exemple : `LOT1` à `LOT12`, le lot de migration).
  - 💡 Pour ne pas suivre deux fois la même chose : **une carte par
    chantier**, pas une par fiche. La carte renvoie au fichier de fiches.

## 6. Où on en est

| Étape | État |
|---|---|
| Choisir l'outil | ✅ GitHub Projects |
| Choisir les colonnes | ✅ les 5 du § 3 |
| Créer le tableau | ✅ <https://github.com/orgs/GaSeBeLa/projects/1> |
| Droits des 4 propriétaires de l'organisation | ✅ admins du projet, d'office (doc GitHub) |
| Droits de Jeff, simple membre de l'organisation | 🟡 lecture ou écriture : à décider |
| Choisir les cartes de départ | 🟡 à décider ensemble (§ 5) |
| Écrire les cartes | ➡️ après ce choix |

## 7. Ce qu'on vous demande

1. **Lire** cette page, et réagir sur Discord.
2. **Choisir a, b ou c** pour les cartes de départ (§ 5).
3. **Valider ou changer** les règles du § 4.
4. **Ouvrir le tableau** une fois, pour vérifier que vous y avez accès.

## Sources — consultées le 2026-10-07

- GitHub Docs, doc officielle :
  - [About Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) — la vue « board », c'est-à-dire kanban.
  - [Using the built-in automations](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations) — fermée ou fusionnée → Fait, par défaut.
  - [Linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) — les mots-clés, la branche par défaut.
  - [Customizing the board layout](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/customizing-the-board-layout) — la limite de colonne n'empêche rien.
  - [Managing access to your projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/managing-access-to-your-projects) — les propriétaires de l'organisation sont admins de chaque projet.
- Atlassian, doc officielle :
  - [Explore Jira Cloud plans](https://support.atlassian.com/jira-cloud-administration/docs/explore-jira-cloud-plans/) — Jira Free : jusqu'à 10 utilisateurs (lu dans un extrait de recherche).
  - [Collaborator limit for free Workspaces](https://support.atlassian.com/trello/docs/workspace-user-limit/) — Trello Free : 10 collaborateurs par workspace.

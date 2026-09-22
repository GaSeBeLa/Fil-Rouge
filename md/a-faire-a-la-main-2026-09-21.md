# Ce qui reste à faire à la main — 21 septembre 2026

> 🎯 Les étapes que **je ne peux pas faire à ta place**, dans l'ordre.
> Chaque bloc est indépendant : tu peux t'arrêter entre deux.
> Les cases 🤖 sont celles que je reprends dès que tu me le dis.

---

## Bloc 1 — Ton dépôt (5 minutes)

### 1.1 Trois fichiers ne sont pas commités

```
 D  API/.env exemple      (supprimé par toi)
 M  API/README.md         (modifié par toi)
 ?? docker/.env.exemple   (nouveau, pas encore suivi)
```

- [ ] Décider si ces trois changements vont ensemble dans un commit.
- 🤖 Je peux le faire : dis-moi juste le message que tu veux.

### 1.2 Trois commits attendent d'être poussés

```
8684b7f  docs: detaille les modifications a faire pour l'ADR-024
9ed95c0  docs: propose l'ADR-024, motif de refus de remuneration sur payment
a45e003  docs: consigne les 5 reponses du point d'etape, et l'etape A3 bis
```

- [ ] Décider si on pousse maintenant. **Un push publie**, et ne se reprend pas.
- 🤖 Je lance `git push` dès que tu me le confirmes.

---

## Bloc 2 — Confluence (10 minutes, toi seul)

### 2.1 Trancher le numéro de l'ADR

Deux comptes différents coexistent :

| Source | Dit quoi |
|---|---|
| *Journal de décisions* | s'arrête à `ADR-023` → le suivant est `ADR-024` |
| *Cahier des Charges Technique* v2.0 | renvoie à `ADR-017` pour Argon2, que le journal numérote `ADR-016` |

- [ ] Choisir : le journal fait foi (→ `ADR-024`), ou le CDC a raison.
- [ ] Corriger celui des deux qui se trompe.

💡 **Suggestion** : le journal fait foi. C'est lui qui porte les décisions ;
le CDC ne fait qu'y renvoyer.

### 2.2 Coller l'ADR dans le journal

Page : *Journal de décisions (ADR)*, espace `GaSeBeLa1`.

1. [ ] Ouvrir `md/adr-024-motif-refus-remuneration.md`.
2. [ ] ⚠️ **Ne pas copier le haut du fichier.** Le bloc « proposition à relire
   avant publication » est une note pour nous, pas pour Confluence.
   Commencer la sélection à la ligne :
   `**ADR-024 : Traçabilité du refus de rémunération du chasseur...**`
3. [ ] Ouvrir la page Confluence, cliquer **Modifier**, descendre tout en bas.
4. [ ] Coller. Confluence convertit le markdown automatiquement au collage.
5. [ ] Vérifier que les trois tableaux et le bloc SQL sont bien rendus.
6. [ ] Publier.

### 2.3 Signaler le décalage du cahier des charges

Le CDC v2.0 a été mis à jour aujourd'hui à 08:56 par **Békanty Kouassi**.
Il audite `docker/init/` — l'**ancien** schéma à 12 tables en K€ — alors que
le projet tourne sur `docker/init-v2/`, 18 tables en euros.

- [ ] Le lui dire. Une grande partie de son §12 « écarts critiques » porte
      dans le vide : les tables `visit`, `sale`, `payment`, `commission_scale`,
      `parameters_fees` et `hunter_performance` **existent déjà**.
- [ ] Lui signaler aussi que `criteria.town` et `estate.typology` existent,
      alors que le §12 les déclare « bloquants ».

💡 Ce n'est pas du travail perdu : le §12 reste juste sur l'ancien schéma.
C'est la **cible** de l'audit qu'il faut corriger.

---

## Bloc 3 — En groupe (à la prochaine réunion)

### 3.1 Les 5 réponses du point d'étape

Aujourd'hui elles sont **ta position**, pas une décision collective. C'est écrit
tel quel dans le point d'étape.

- [ ] Faire valider les 5 réponses → ferme l'étape `A1` du plan.

### 3.2 L'ADR-024

- [ ] Le faire passer de « proposé » à « accepté ».

### 3.3 Les huit ADR en attente

`ADR-016` à `ADR-023` sont toutes au statut **« proposé »**, certaines depuis
le 04/09. Elles comprennent des décisions structurantes :

| ADR | Sujet | Depuis |
|---|---|---|
| 016 | Argon2id pour les mots de passe | 04/09 |
| 017 | Identifiant technique par table | 07/09 |
| 019 | Pas de clé étrangère `Sale` → `Parameters_Fees` | 10/09 |
| 020 | Codes pays ISO | 10/09 |
| 021 | Contraintes de localisation sur `Criteria` | 10/09 |
| 022 | Contraintes de cohérence sur `client` | 10/09 |
| 023 | Date de fin de mandat stockée | 11/09 |

- [ ] Les passer en revue en bloc. Huit décisions non validées, c'est le
      reproche le plus facile à faire en soutenance.

---

## Bloc 4 — Après validation seulement

⚠️ Ne rien commencer ici tant que le bloc 3 n'est pas fait.

### 4.1 Le code et le schéma

- 🤖 Modifier `docker/init-v2/01_create_fil_rouge_immobilier.sql` (table
  `payment`) — tout est prêt dans `md/adr-024-modifications-a-faire.md`.
- 🤖 Modifier `API/src/app/models/payment_model.py`.
- [ ] Recréer la base pour que le nouveau schéma s'applique, depuis `docker/` :

```bash
docker compose down -v
docker compose up -d
```

⚠️ Le `-v` **efface les données**. Sans conséquence aujourd'hui, puisque tout
vient des scripts. Ce ne sera plus vrai une fois le seed écrit à la main.

### 4.2 Les trois diagrammes — toi seul

Page Confluence *Schémas - MCD/MLD/MPD Cible*, en draw.io. Je ne peux pas les
modifier.

- [ ] **MCD** — entité `PAIEMENT` : ajouter l'attribut *motif de refus*.
- [ ] **MLD** — ajouter `refusal_reason` ; marquer `base_rate`,
      `seniority_rate`, `performance_rate` et `id_commission_scale` comme
      **facultatifs**.
- [ ] **MPD** — mêmes colonnes, plus la contrainte `chk_refused` en note.

💡 **Le point à ne pas rater** : sur le MLD, le lien `PAIEMENT → BARÈME`
cesse d'être obligatoire (de 1,1 à 0,1). C'est ça qu'un jury regardera, plus
que la colonne elle-même.

---

## Bloc 5 — Ce qui attend derrière

Rappel du plan du point d'étape, pour situer :

| Étape | Quoi | Bloquée par |
|---|---|---|
| `A2` | Monter une base **de test** séparée | rien — **c'est le premier verrou du projet** |
| `A3` | Reprendre la calculette du sujet et ses 55 tests | `A2` |
| `A3 bis` | L'ADR-024 et le schéma | bloc 3 |
| `A4` | Écrire le seed `04_seed_demo.sql` | `A1`, `A3`, `A3 bis` |
| `B1` | Hacher les mots de passe | plus rien ! `ADR-016` a tranché : Argon2id |

💡 `A2` ne dépend de personne et débloque tout le reste. Si tu ne fais qu'une
chose cette semaine, c'est celle-là.

---

## Ajout du 22 septembre — le lien chasseur → manager

> 📝 **Note.** Ce bloc a été ajouté le 22/09, après la séance du 21/09 que ce
> fichier décrit. Il vient du chantier de l'après-midi : `hunter` porte
> désormais `id_realestatemanager` (`NOT NULL`), commit `51f4761`. Les blocs
> 1 à 5 ci-dessus n'ont pas été retouchés.

### 6.1 Confluence — coller l'ADR-025 (toi seul)

Même page que l'ADR-024 : *Journal de décisions (ADR)*, espace `GaSeBeLa1`.

1. [x] Ouvrir `md/adr-025-lien-chasseur-manager.md`.
2. [x] ⚠️ **Ne pas copier le haut du fichier** : commencer la sélection à la
   ligne `**ADR-025 : Chaque chasseur est rattaché à un manager**`.
3. [x] ⚠️ Le numéro suppose que l'ADR-024 est bien numéroté 024 (bloc 2.1).
   Si le journal a tranché autrement, décaler.
4. [x] Coller en bas de la page, vérifier les tableaux, publier.
5. [x] En réunion : le faire passer de « proposé » à « accepté » (avec l'ADR-024,
   bloc 3.2).

✅ **Fait le 22/09** — vérifié sur Confluence : l'ADR-025 est en bas du
journal, statut **« accepté »**.

⚠️ **Deux choses vues au passage, à corriger sur Confluence (toi seul) :**

- [ ] La note de fin de fichier *« À corriger dans le drawio, hors ADR :
      `criteria.budget_max NUMERIC (12.2)`… »* a été collée avec l'ADR. Elle
      était pour nous, pas pour le journal : à retirer.
- [ ] **L'ADR-024 lui-même n'est pas dans le journal.** Entre l'ADR-023 et
      l'ADR-025 se trouve *« ADR-024 — les modifications à faire, en détail »*
      — c'est le **compagnon technique** (`md/adr-024-modifications-a-faire.md`),
      pas la décision (`md/adr-024-motif-refus-remuneration.md`, qui commence
      par `**ADR-024 : Traçabilité du refus de rémunération du chasseur**`
      avec date, statut, options). Le journal a donc un **trou** : aucun bloc
      « ADR-024 : … / Statut : … ». À remplacer par le bon fichier — le bloc
      2.2 ci-dessus dit lequel.

### 6.2 Le drawio — toi seul

Fichier `MPD 03 4.drawio.xml` (et la page Confluence *Schémas - MCD/MLD/MPD
Cible* si elle est déjà à jour).

- [x] `criteria.budget_max` : **`NUMERIC (12.2)`** → **`NUMERIC (12, 2)`**.
      Un point au lieu d'une virgule. Le script SQL lit déjà `(12, 2)`.
- [x] Décider si le lien Hunter → Manager garde le libellé **« Manages »**,
      ou passe à **« Supervises »** pour ne pas le confondre avec le lien
      SearchRequest → Manager, qui s'appelle aussi « Manages ».

🟢 **Fait le 22/09, dit par toi — non vérifiable d'ici** : le diagramme vit
dans Confluence, dont l'API ne rend pas le contenu draw.io. ⚠️ Le fichier
local `vrac/MPD 03 4.drawio.xml` (11:20) porte encore `12.2` et aucun
« Supervises » : penser à **ré-exporter** le drawio à jour, et me dire quel
libellé a été retenu pour que je l'aligne dans le script et l'ADR.

### 6.3 Ta base locale

Si ta base Docker a été créée **avant** le 22/09, elle n'a pas la colonne.
Depuis `docker/`, au choix :

```bash
docker compose down -v && docker compose up -d
```

ou, pour garder les données :

```bash
docker exec -i fil_rouge_immobilier_db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1' < migrations/2026-09-22_hunter_manager.sql
```

- [x] Vérifier ensuite : `SELECT count(*) FROM hunter WHERE id_realestatemanager IS NULL;`
      doit donner **0**.

🟢 **Fait le 22/09, dit par toi — non revérifié** : Docker Desktop était fermé
au moment du contrôle.

### 6.4 Pour le seed (`A4`)

- [ ] Prévoir de **vrais** managers, et remplacer le placeholder
      `manager.migration@chassimmo.fr` (user 25) — puis le supprimer une fois
      qu'aucun chasseur ne pointe vers lui. Voir `docker/init-v2/README.md` §3.6.

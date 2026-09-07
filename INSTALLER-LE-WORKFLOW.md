# Installer le workflow `vlp` — à faire une fois par machine

Ce projet est organisé en **chantiers et fiches**. Un chantier se découpe une
fois en fiches ; chaque fiche se joue dans une session Claude Code neuve. Les
commandes qui pilotent ça — `/vlp:chantier`, `/vlp:tache`, `/vlp:check` —
**ne sont pas dans ce dépôt**. Elles vivent dans un plugin Claude Code, à
installer chez toi une fois. Sans lui, les commandes n'existent pas.

Compte dix minutes, et tu n'y reviens plus.

---

## 1. Récupérer le kit — et choisir où il vit

Deux façons, au choix. Le résultat est le même : **un** dossier
`Claude-vlpWorkflow`, posé **à côté** de tes projets, jamais dedans.

**Par git** (préféré — il se met à jour tout seul ensuite) :

```bash
git clone https://github.com/SebastienGrana/Claude-vlpWorkFlow.git
```

**Par le zip**, si Sébastien te l'a envoyé : dézippe-le. Il contient son
`.git`, donc il reste à jour lui aussi.

Le rangement visé :

```
Documents/ProgPerso/
  Claude-vlpWorkflow/   <- le kit, UNE fois
  Fil-Rouge/            <- les projets, à côté
  UnAutreProjet/
```

> **La seule règle à retenir** : ne copie **jamais** le kit dans un projet. Une
> copie posée dans un projet est une copie que personne ne met plus à jour —
> c'est comme ça qu'il a fini par exister en six exemplaires divergents.

---

## 2. Déclarer le kit à Claude Code

Un dossier posé dans `~/.claude/skills/` et portant un `.claude-plugin/plugin.json`
se charge tout seul, dans tous tes projets. Et ce dossier peut être un **lien**
vers le kit réel — donc rien n'est copié.

**Windows** (PowerShell, aucun droit administrateur nécessaire) — remplace
`<chemin>` par l'endroit où tu as mis le kit :

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\vlp" -Target "<chemin>\Claude-vlpWorkflow"
```

**macOS ou Linux** :

```bash
ln -s "<chemin>/Claude-vlpWorkflow" ~/.claude/skills/vlp
```

Les commandes deviennent `/vlp:chantier`, `/vlp:tache`, `/vlp:check` et
`/vlp:init`, disponibles partout. Le préfixe `vlp:` évite qu'un `/tache`
venu d'ailleurs prenne la place du nôtre.

Si tu déplaces le kit plus tard, refais le lien.

---

## 3. Cloner le projet

```bash
git clone https://github.com/GaSeBeLa/Fil-Rouge.git
```

Le dépôt porte déjà tout le contexte du projet — `CLAUDE.md`, `CHANTIER.md`,
`context AI/`. Rien à configurer : c'est versionné exprès, pour qu'on lise
tous la même carte.

---

## 4. Monter l'environnement de l'API

Sans ça, la vérification (`pytest`) échoue sur un `ModuleNotFoundError`.

```bash
cd API
python -m venv .venv
```

Active-le — Windows : `.venv\Scripts\activate` ; macOS/Linux :
`source .venv/bin/activate` — puis :

```bash
pip install -r requirements.txt
```

La base tourne à part, depuis `docker/` :

```bash
docker compose up -d
```

Il te faut un `docker/.env` (`POSTGRES_USER`, `POSTGRES_PASSWORD`) et un
`API/.env` — modèle dans `API/.env exemple`. **Ces deux fichiers ne sont
jamais commités.**

---

## 5. Vérifier que tout est en place

Ouvre une session Claude Code **dans le dossier `Fil-Rouge`** — pas au-dessus —
et lance :

```
/vlp:chantier
```

Elle doit annoncer **« Fil Rouge Immobilier » sans rien te demander**, et
proposer des chantiers tirés de `context AI/08-etat.md`. Si elle demande de
quel projet il s'agit, c'est que la session a été ouverte au mauvais niveau, ou
que le lien de l'étape 2 n'a pas pris.

Et la vérification du projet, depuis `API/` :

```bash
python -m pytest -q
```

---

## Ensuite, au quotidien

| Ce que tu veux faire | La commande |
|---|---|
| ouvrir un chantier, ou le découper en fiches | `/vlp:chantier` |
| jouer une fiche du chantier en cours | `/vlp:tache` |
| douter de la cohérence du projet (page publiée, cases cochées) | `/vlp:check` |
| mettre le kit à jour | `git pull` dans `Claude-vlpWorkflow` |

**Une fiche, une session.** `/clear` entre deux fiches : une session laissée
ouverte relit tout son passé à chaque tour, et sature pour rien.

## Les trois règles du projet à connaître avant de toucher au code

Elles sont dans `CHANTIER.md`, mais autant les lire tout de suite :

1. Le dossier `Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/` est la
   **source de vérité, en lecture seule** — on l'ouvre, on n'y écrit jamais.
2. `docker/init/01_create_fil_rouge_immobilier.sql` est le **schéma de
   référence** : tout modèle SQLModel s'y confronte par grep avant modification.
3. Prose et commentaires en français, noms de code en anglais. Aucun secret ni
   `.env` dans git, aucun chemin absolu dans le code.

## Où va la feuille de route

L'état du projet et la TODO ordonnée vivent dans `context AI/08-etat.md`, et
sont publiés en page lisible :
<https://claude.ai/code/artifact/f21ec12e-cd17-4c53-9289-3c5ef94a2907>

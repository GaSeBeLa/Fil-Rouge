# Chantier courant — Fil Rouge Immobilier

> Fichier lu **en entier** par `/vlp:chantier` et `/vlp:tache`, depuis la racine du
> projet. C'est la seule table à tenir : rien à mettre à jour ailleurs quand un
> chantier s'ouvre ou se clôt. Garde-le court — vingt à trente lignes.
> Les libellés en gras se recopient **à l'identique** : ils sont lus tels quels.

- **alias** : fil-rouge
- **kit** : C:/Users/znorr/.claude/skills/vlp — pour un humain ; les commandes
  voyagent avec le plugin et n'ont plus besoin de ce chemin
- **contexte** : context AI/
- **méthode** : ${CLAUDE_PLUGIN_ROOT}/methode-chantier.md
- **chantiers possibles** : context AI/08-etat.md
- **fichier d'état** : context AI/08-etat.md
- **index** : context AI/00-INDEX.md
- **fichier de fiches courant** : aucun
- **artefact feuille de route** : https://claude.ai/code/artifact/f21ec12e-cd17-4c53-9289-3c5ef94a2907
- **artefact du chantier** : aucun
- **livraison** : aucune — le code tourne en local (`uvicorn` + base PostgreSQL
  via `docker compose up -d` depuis `docker/`)
- **vérification** : `python -m pytest -q` lancé depuis `API/` — la session
  lance la commande et lit son verdict

## Contraintes d'écriture

Les règles que toute fiche respecte, quel que soit son sujet. Trois ou quatre,
pas quinze — celles qu'on regrette de ne pas avoir écrites.

- **`../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/` est la source de
  vérité et ne se modifie jamais** : on l'ouvre en lecture pour vérifier un
  énoncé, un livrable attendu ou une fixture ; aucune écriture, aucun
  déplacement, aucune suppression, même « pour ranger ».
- Prose et commentaires de code en français ; noms de code (tables, classes,
  variables, routes) en anglais, comme le schéma SQL.
- Le schéma de référence est `docker/init/01_create_fil_rouge_immobilier.sql` :
  tout modèle SQLModel s'y confronte par grep avant modification.
- Aucun secret ni `.env` commité, aucun chemin absolu dans le code, et on
  n'édite pas les données générées (`normalised/annonces/`,
  `normalised/annonces_normalised.csv`) — on les régénère par `normalised.py`.

## Chantiers clos — ne se rejouent pas

Ils ne servent plus qu'à relire un socle d'API, si une fiche y renvoie.

| Fichier de fiches | Fiches | Clos le | Artefact |
|---|---|---|---|
| *(aucun pour l'instant)* | — | — | — |

Lettres de fiche déjà prises : *(aucune)*. Un nouveau chantier en choisit une
autre — elles ne se réemploient jamais, même après clôture. `/vlp:chantier` la
propose, l'utilisateur tranche ; c'est cette ligne qui rend le refus possible.

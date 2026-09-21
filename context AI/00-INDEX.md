# Index du contexte Fil Rouge Immobilier

**`CLAUDE.md`, à la racine, est le fichier d'entrée** : il porte l'identité du
projet, l'état en cinq lignes, les règles, et une table « tâche → fichier » qui
suffit dans presque tous les cas. Cet index-ci ne sert que lorsque la tâche n'y
figure pas.

Un fichier = un sujet. **Ne charger que ce que la tâche demande.**
Chaque fichier s'ouvre sur une ligne « QUAND LIRE » : elle seule décide. Si
elle ne décrit pas la tâche en cours, le fichier n'est pas à ouvrir, même s'il
a l'air proche.

## Stable — ce qui ne bouge presque plus

| Fichier | Lire quand |
|---|---|
| `08-etat.md` | on reprend après une interruption, ou on choisit quoi faire ensuite |
| *(hors dossier)* `${CLAUDE_PLUGIN_ROOT}/methode-chantier.md` | on ouvre un chantier, ou on le découpe en fiches — la méthode n'est pas recopiée ici, elle voyage avec le plugin `vlp` et sert tous les projets |

## Chantiers — un fichier de fiches par chantier

| Fichier | Lire quand |
|---|---|
| `09-contraintes-mpd.md` | on relit une fiche `C1` à `C5` — chantier **clos** le 2026-09-11 : les contraintes qui manquent au MPD |
| `09-annexe-*.md` | produits par les fiches `C*` — ne s'ouvrent que si une fiche les nomme |
| *(hors dossier)* `livrables/2-modelisation/09-rapport-ecarts-contraintes.md` | le livrable du chantier `C` : écarts entre le MPD et les règles métier |

## Hors contexte IA — les sources de vérité du projet

Elles ne sont pas recopiées ici : on les ouvre à leur place, et seulement quand
la tâche les nomme.

| Fichier | Lire quand |
|---|---|
| `docker/init-v2/01_create_fil_rouge_immobilier.sql` | on touche une table, une colonne, une contrainte — **18 tables, euros** |
| `docker/init-v2/README.md` | on doute d'un choix du schéma v2 : euros, migration, hypothèses assumées, points ouverts |
| `API/README.md` | on installe ou on lance l'API |
| `API/src/app/main.py` | on cherche où va un bout de code — son en-tête décrit les trois couches |
| `user-stories/<NN>_*.feature` | on vérifie une règle métier |
| `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack*/` (les deux) | on vérifie l'énoncé, un livrable attendu, une fixture — **lecture seule** |

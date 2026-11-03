# RACI — brouillon pour les phases 2 à 4

> Brouillon du 2026-11-03 (vote Q3 A) : l'équipe corrige, puis copie sur la
> page Confluence « RACI » (Békanty, 18 août). Seules les lignes **vides** de
> cette page sont proposées ici ; les lignes déjà remplies ne changent pas.
>
> **D'où vient chaque lettre**
> - **R** = ✅ l'auteur de la page Confluence, ou l'auteur des commits du
>   livrable (comptés par `git shortlog -sn`). C'est un indice : écrire une
>   page n'est pas forcément « réaliser » le livrable.
> - **A** = 💡 **ma proposition**, pour que chaque ligne ait un seul A, et
>   que ce ne soit pas la personne qui réalise. À trancher par l'équipe.
> - ❌ = le livrable n'existe pas encore : personne n'est proposé.
> - Le Product Owner et le jury gardent les lettres déjà mises sur la page.

## Phase 2 — Besoin actuel

| Livrable | Sébastien | Laurence | Békanty | Gabriel | D'où vient le R |
|---|---|---|---|---|---|
| Note stratégique (axes d'évolution) | | | R | **A** | auteur Confluence : Békanty. ✅ voté le 2026-11-03 (Q3 A) : R Békanty, au lieu de Gabriel |
| Note de cadrage | **A** | | R | | auteur Confluence : Békanty |
| Backlog priorisé (MoSCoW) | | | | | ❌ pas trouvé sur Confluence |
| MCD/MLD cible | R | **A** | | | auteur de la page « Schémas – Cible » : Sébastien |
| `migration.sql` + note d'indexation | R | | | **A** | commits de `docker/migrations/` : Sébastien 59, CaBaSS 8. ❌ note d'indexation pas trouvée |
| Cahier des charges technique | **A** | | R | | auteur Confluence : Békanty |
| Registre RGPD | | **A** | | R | auteur Confluence : Gabriel |
| Note d'accessibilité PSH | | | | | ❌ pas trouvée |

## Phase 3 — Croissance

| Livrable | Sébastien | Laurence | Békanty | Gabriel | D'où vient le R |
|---|---|---|---|---|---|
| Dossier d'architecture + matrice de décision | R | | **A** | | `livrables/3-architecture/` (8 schémas) : Sébastien. ❌ matrice pas trouvée |
| Note de dimensionnement 3V | **A** | | | R | auteur Confluence : Gabriel |
| Schéma OLAP + alimentation | R | | | **A** | `livrables/2-modelisation/olap.md`, chantier FLX : Sébastien |
| Note d'éco-conception | | **A** | | R | auteur Confluence : Gabriel |
| PCA/PRA + plan de migration | | | | | ❌ pas trouvé |

## Phase 4 — Application et IA

| Livrable | Sébastien | Laurence | Békanty | Gabriel | D'où vient le R |
|---|---|---|---|---|---|
| Dossier de conception applicative + maquettes | | | | | ❌ pas trouvé. 🟡 « pas de front » : que montrent les maquettes ? |
| Backend / API | R | C | | C | commits de Fil-Rouge-API : Sébastien 172, CaBaSS 23, Amethyste34 3. **A** : 🟡 à choisir |
| Plan de tests + exécution | R | **A** | | | `livrables/4-application/rapport-tests.md` : Sébastien |
| Schéma du programme d'IA + conception matching | R | C | | **A** | brouillons du 2026-11-03 ; Gabriel a relevé les incohérences du chantier SUG |
| Note souveraineté / sécurité IA | | | | | ❌ pas trouvée |

## Les règles de la page, vérifiées sur ce brouillon

- ✅ **Un seul A par ligne**, sur les lignes où quelqu'un est proposé.
- ⚠️ **Au moins un R par ligne** : faux pour les **5 lignes ❌** (MoSCoW, PSH, PCA/PRA, conception applicative, souveraineté), puisque le
  livrable n'existe pas. Il faut d'abord désigner qui les fera.
- ✅ **Chaque membre porte au moins un A**, sur toute la page :

| Membre | A proposés ici | A déjà sur la page |
|---|---|---|
| Sébastien | 3 | 4 (dépôt, registre, SWOT, oral M1) |
| Laurence | 4 | 4 (journal, MCD existant, étude d'opportunité, oral M2) |
| Békanty | 1 | 2 (cartographie, oral M3) |
| Gabriel | 4 | 2 (RACI phase 1, oral M4) |

- ⚠️ **Le déséquilibre se voit** : Sébastien est R sur **7 des 13 lignes** qui ont un R en
  phases 2 à 4. Le jury interroge chacun sur **tout** le projet
  (`SP/Readme.md:322`) : c'est un argument pour répartir les livrables ❌.

## 🟡 À trancher par l'équipe

1. ✅ R de la note stratégique : **Békanty** (Q3 A).
2. 💡 Les livrables ❌ et le A du backend : répartition proposée plus bas (Q6 B).
3. ✅ CaBaSS = Gabriel, ange11-K = Békanty (Q1, Q2).

## Proposition de répartition des livrables ❌ (vote Q6 B du 2026-11-03)

> 💡 Ma proposition : l'équipe corrige. Chaque livrable va à la personne qui a
> déjà écrit le document voisin, pour que l'oral se défende sans tout réapprendre.
> Identités git confirmées le 2026-11-03 (Seb, amethyste) : CaBaSS = Gabriel,
> ange11-K = Békanty, Amethyste34 = Laurence. ⚠️ L'auteur d'un commit n'est pas
> toujours l'auteur du travail : d'après Seb, l'Argon2 est de Laurence et MinIO
> de Gabriel, alors que git dit l'inverse (commit Argon2 par CaBaSS, ajout de
> MinIO par Amethyste34). Ce tableau suit Seb ; Laurence a confirmé l'Argon2
> (Discord, 2026-11-03).

| Livrable ❌ | R proposé | A proposé | Pourquoi cette personne |
|---|---|---|---|
| Backlog priorisé (MoSCoW) | Békanty | Sébastien | elle a écrit le CDC technique et la note de cadrage, d'où sortent les besoins |
| Note d'accessibilité PSH | Békanty | Laurence | l'énoncé l'attache au CDC (« intégrant l'accessibilité PSH », `SP/Readme.md:237`) |
| Matrice de décision | Laurence | Békanty | elle valide déjà l'étude d'opportunité, qui compare des options |
| PCA/PRA + plan de migration | Gabriel | Laurence | il a posé MinIO (Seb, 2026-11-03) et écrit la note d'éco-conception, dont les sauvegardes fondent le PRA |
| Note souveraineté / sécurité IA | Laurence | Gabriel | elle a fait le hachage Argon2 des mots de passe (Seb, 2026-11-03) : la sécurité des comptes ; Gabriel, auteur du RGPD, valide |
| Note d'indexation | Gabriel | Sébastien | la note d'éco-conception traite déjà des index (« Optimisation des requêtes ») |
| Conception applicative + maquettes | Laurence | Sébastien | Sébastien a codé l'API : il est C, et Laurence la présente avec un regard neuf |
| **A du backend** | — | Gabriel | 23 commits dans Fil-Rouge-API (compte CaBaSS) |

**Le R par membre, phases 2 à 4, avant et après**

| Membre | Avant | Après |
|---|---|---|
| Sébastien | 7 | 7 |
| Laurence | 0 | 3 |
| Békanty | 3 | 5 |
| Gabriel | 3 | 5 |

- ⚠️ **Laurence n'avait aucun R** en phases 2 à 4 : la proposition lui en donne 3.
- ⚠️ Sébastien reste le plus chargé, avec le code. 🟡 Pour alléger : passer le R du plan de tests à un autre membre.

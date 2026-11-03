> **QUAND LIRE** : on joue une fiche `MER*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache MER<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier MER — Modèle de données en Merise (MCD + MLD) avec Mocodo

**Ouvert.** le 2026-11-02.

**À quoi il sert.** Le livrable 2 demande le MCD et le MLD, dans la notation
Merise du cours. Une seule source texte `.mcd` (Mocodo) donne le MCD en SVG et
le MLD ; les schémas 5 à 8 du livrable 3 s'alignent dessus.

**Estimé.** 8 fiches · ≈39 $ — ≈4,83 $/fiche sur 9 clos (le 2026-11-02).

**CLOS** le 2026-11-03. Ne se rejoue pas — ne sert plus qu'à relire son socle.

Abandonnées : MER1 à MER5 abandonnées : le gros MCD Mocodo (22 entités) a été jugé illisible par Seb le 2026-11-02, MER1 et MER2 effacées à sa demande ; Merise sera recadré plus tard en petits schémas.

**Fait.** MER1..MER5 (2026-11-03) : Rien de livré : chantier clos avant sa première fiche — estimé 8 fiches ≈39 $ · cadré 5 · joué 0 fiches ? $.

**Session** : 3981bffb-3aad-4d2a-9725-537990e72dc9

## Le socle commun

**Décisions de Seb** (Discord, 2026-11-02 : questionnaire à 3 questions le matin,
puis boutons `mer:q1` à `mer:q4` l'après-midi) :

- Notation **Merise** seule : ni UML, ni « pattes d'oie ».
- Outil **Mocodo 4.3.3** (MIT, PyPI), lancé par `py -3 -m mocodo`. Déjà installé.
- Périmètre : le **MCD complet des 22 tables** du schéma v3, puis le MLD déduit.
- Le test vit **dans ce dépôt**, à côté du `.mcd`, lancé par `py -3 -m pytest`
  (pytest 9.1.1 installé). C'est le premier test du dépôt Fil-Rouge.
- Le test compare les **noms** (MER1) **et les clés étrangères** (MER2).
- Une **légende** sous chaque schéma : formes, cardinalités, couleurs.

**Les fichiers** (tous dans `livrables/2-modelisation/merise/`, dossier neuf) :

| Fichier | Ce qu'il porte |
|---|---|
| `fil_rouge.mcd` | la source unique du MCD |
| `fil_rouge.svg`, `fil_rouge_mld.md` | générés par Mocodo, commités |
| `test_mcd_sql.py` | le test MCD ↔ SQL |
| `README.md` | le MCD, le MLD, la légende, la commande qui régénère |

**Référence** : `../Fil-Rouge-API/docker/init-v3/01_create_fil_rouge_immobilier.sql`
(22 `CREATE TABLE`, de `role` à `hunter_performance`). Il fait foi ; il ne change pas.
Le test le lit par un chemin **relatif** au fichier de test ; dépôt voisin absent →
le test **échoue** avec un message qui le dit (jamais un `skip` muet).

**Mocodo, vérifié le 2026-11-02 dans un dossier temporaire** :

- `py -3 -m mocodo -i fil_rouge.mcd -t markdown` écrit `fil_rouge.svg`,
  `fil_rouge_geo.json` et `fil_rouge_mld.md`.
- Syntaxe : une entité `client: id, nom` ; une association
  `signe, 1N client, 11 mandat`.
- Le MLD markdown souligne la clé (`<u>id</u>`) et écrit une clé étrangère
  `_#id_client_` ; il **ne dit pas** quelle table elle vise.
- `--colors <chemin>` prend un fichier de couleurs : **fond crème**, jamais sombre
  (skill `rendus-visuels`).

**Conventions** : une entité ou une association porte **le nom exact de sa table**
(`user`, `estate_searchrequest`…). Une table de liaison devient une association,
une table à vie propre (identifiant, attributs, liens) une entité : le test accepte
les deux. Seule source à lire en plus : la fiche du cours
`../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/documents utiles/MCD-MERISE.md`
(lecture seule), § « Du MCD au MLD : les règles de passage ».

**Dehors** : Confluence, Discord, la publication de pages (la séance mère publie),
le SQL et le code de l'API. Les anciens MCD (`../migration/MCD - Cible.drawio.png`,
10 entités, périmé ; `../vrac/v9.drawio.xml`, 21 tables) se consultent, ne se
recopient pas.

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `MER1` | Écrire le test, puis le MCD des 22 tables | rien |
| `MER2` | Déduire le MLD et le confronter aux clés étrangères | `MER1` |
| `MER3` | Justifier chaque cardinalité | `MER1` |
| `MER4` | Refaire les schémas 5, 6, 7 en zooms du MCD | `MER1` |
| `MER5` | Refaire le schéma 8 en organigramme | rien |

`MER5` se joue quand on veut. `MER2`, `MER3`, `MER4` attendent `MER1`, puis sont
indépendantes entre elles.

---

<!-- FICHE:MER1 -->
## MER1 [ ] — Écrire le test, puis le MCD des 22 tables

**Dépend de** : rien.
**Fichiers** : `livrables/2-modelisation/merise/test_mcd_sql.py`, `fil_rouge.mcd`,
`fil_rouge.svg`, `README.md`, le fichier de couleurs crème — et rien d'autre.

**Prompt**
Écris d'abord `test_mcd_sql.py`. Il lit les noms des `CREATE TABLE` du SQL, et les
noms des entités et des associations du `.mcd`. Deux tests : chaque table a sa boîte,
et chaque boîte a sa table. Les manques s'affichent par leur nom. Lance-le sur un
`.mcd` vide : rouge.
Puis écris `fil_rouge.mcd` : les 22 tables, leurs attributs métier, l'identifiant,
les cardinalités tirées du SQL (`NOT NULL` + FK → 1,1 ; FK nullable → 0,1 ;
`UNIQUE` sur une FK → un lien 1-1). Génère le SVG avec les couleurs crème.
Le `README.md` montre le SVG, une **légende** (rectangle = entité, ovale =
association, souligné = identifiant, lecture des couples (min,max), couleurs)
et la commande qui régénère.

**Critère de fin**
`py -3 -m pytest livrables/2-modelisation/merise -q` : rouge recopié avant le
`.mcd`, puis vert, avec le compte « 22 tables, N boîtes ». Mutant : retirer
l'entité `estate_price_history` du `.mcd` → le test tombe en la nommant.
<!-- /FICHE -->

---

<!-- FICHE:MER2 -->
## MER2 [ ] — Déduire le MLD et le confronter aux clés étrangères

**Dépend de** : `MER1`.
**Fichiers** : `merise/test_mcd_sql.py` (ajout pur), `fil_rouge_mld.md`,
`fil_rouge.mcd` (si un écart vient du MCD), `README.md`.

**Prompt**
Mesure d'abord : le MLD markdown ne dit pas quelle table vise une clé étrangère.
Cherche dans `py -3 -m mocodo --help` la sortie qui le dit (un DDL SQL de Mocodo,
par exemple). Recopie ce que tu as essayé.
Puis ajoute un test : l'ensemble des couples (table, table visée) du MLD égale
celui des `REFERENCES` du SQL. Les écarts s'affichent un par un. Rouge d'abord.
Un écart vient du MCD → corrige le `.mcd`. Un écart vient d'une limite de Merise
(ex. deux clés vers la même table) → liste-le dans le `README.md`, section
« Écarts MLD ↔ SQL », avec sa raison, et exclus-le du test **par son nom**.
Ajoute le MLD au `README.md`, avec sa légende (souligné = clé primaire,
`#` = clé étrangère).

**Critère de fin**
`py -3 -m pytest livrables/2-modelisation/merise -q` vert, avec « N clés SQL,
N clés MLD, K écarts listés ». Mutant : passer un `11` en `1N` dans le `.mcd`
→ le test de clés tombe.
<!-- /FICHE -->

---

<!-- FICHE:MER3 -->
## MER3 [ ] — Justifier chaque cardinalité

**Dépend de** : `MER1`.
**Fichiers** : `merise/cardinalites.md`, `merise/test_mcd_sql.py` (ajout pur),
`README.md` (un lien).

**Prompt**
Le jury peut demander « pourquoi (1,n) et pas (0,n) ? » (fiche du cours,
« Pièges fréquents »). Écris `cardinalites.md` : une ligne par patte
d'association — association, entité, cardinalité, une phrase métier, et sa source
(contrainte du SQL, ou user story `user-stories/<NN>_*.feature`). Une
cardinalité sans source se dit « hypothèse », jamais inventée.
Test d'abord : chaque patte du `.mcd` a sa ligne, et la cardinalité écrite est
la même que dans le `.mcd`.

**Critère de fin**
`py -3 -m pytest livrables/2-modelisation/merise -q` vert, avec « N pattes,
N lignes, H hypothèses ». Mutant : supprimer une ligne de `cardinalites.md`
→ le test tombe en nommant la patte.
<!-- /FICHE -->

---

<!-- FICHE:MER4 -->
## MER4 [ ] — Refaire les schémas 5, 6, 7 en zooms du MCD

**Dépend de** : `MER1`.
**Fichiers** : `livrables/3-architecture/05-donnees-comptes-et-fiches.md`,
`06-donnees-recherche-et-mandat.md`, `07-donnees-vente-et-remuneration.md`,
`livrables/3-architecture/README.md`, les sources de zoom dans `merise/`,
`merise/test_mcd_sql.py` (ajout pur).

**Prompt**
Mesure d'abord comment Mocodo fait un sous-ensemble : `--help` ne montre pas
d'option « zoom ». Essaie, recopie ; à défaut, un `.mcd` par zoom.
Test d'abord : chaque boîte d'un zoom existe dans `fil_rouge.mcd`, avec les mêmes
cardinalités ; les trois zooms couvrent les 22 tables.
Puis remplace le bloc `erDiagram` de chaque schéma par le SVG du zoom, avec une
légende sous chacun. Garde le texte « À quoi il sert ». Mets à jour le tableau du
`README.md` du livrable 3 (colonne « Ce qu'il montre », lien vers le MCD complet).

**Critère de fin**
`py -3 -m pytest livrables/2-modelisation/merise -q` vert, avec « 3 zooms,
22 tables couvertes ». `grep -c erDiagram livrables/3-architecture/0[567]*.md`
rend 0 pour chacun. Mutant : changer une cardinalité dans un zoom → le test tombe.
<!-- /FICHE -->

---

<!-- FICHE:MER5 -->
## MER5 [ ] — Refaire le schéma 8 en organigramme

**Dépend de** : rien.
**Fichiers** : `livrables/3-architecture/08-connexion-et-jeton.md`,
`livrables/3-architecture/README.md` (si sa ligne 8 change).

**Prompt**
Le schéma 8 est un diagramme de séquence UML (`sequenceDiagram`). Refais-le en
`flowchart` Mermaid simple : les mêmes étapes, les mêmes refus (codes HTTP),
dans le même ordre. Relis le code cité par le fichier dans `../Fil-Rouge-API/`
avant d'écrire : en cas d'écart, le code fait foi. Garde le thème crème du
bloc `%%{init…}%%` des autres schémas. Ajoute sous le schéma une légende :
formes (étape, question, fin), couleurs (vert = `200`, rouge = refus).

**Critère de fin**
`grep -c sequenceDiagram livrables/3-architecture/08-connexion-et-jeton.md` rend
0, `grep -c flowchart` rend 1 ; le nombre d'étapes et de refus avant / après est
recopié (doit être égal).
<!-- /FICHE -->

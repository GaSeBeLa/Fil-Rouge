# Ranger les livrables — liste officielle et proposition

> Demandé par Gabriel (Discord, 2026-11-20) : « construis une liste officielle des livrables à partir du StarterPack, puis propose une manière de les organiser, dans un ordre logique ».
> Sources lues le 2026-11-20 : `SP/Readme.md` (l. 214-296, livrables par phase), `SP/documents utiles/GRILLE-EVALUATION.md` § 1, `SP/documents utiles/TRACABILITE-COMPETENCES.md`, `SP/documents utiles/ORGANISATION-DEPOT.md`.
> **Proposition seulement** : rien n'est déplacé tant que le groupe n'a pas choisi.

## 1. Le constat

- Les numéros de `livrables/` ont **deux sens** :
  - `1-audit/01` à `03` = l'ordre de lecture du dossier d'audit ;
  - `01` à `08` ailleurs = le n° d'une série de **8 schémas d'appui** (présentation du 16/10), répartis dans 3 dossiers. D'où `2-modelisation/` qui commence à `05`.
- Aucun fichier ne dit au jury **quel fichier répond à quel livrable**.
- Quelques livrables ne sont **pas dans la phase** où le sujet les range (étude d'opportunité, note de cadrage, OLAP).

## 2. La liste officielle (36 lignes)

Légende des sources : **R** = `Readme.md` (livrables par phase) · **G** = grille d'évaluation · **T** = traçabilité des compétences.
Statut : ✅ existe · ⚠️ incomplet ou hors de `livrables/` · ❌ manque.

### Phase 1 — Auditer l'existant (BC01)

| # | Livrable | Source | Fichier aujourd'hui | Statut |
|---|---|---|---|---|
| 1 | Cartographie du SI | R, G, T | `1-audit/01-cartographie-si.md` | ✅ |
| 2 | Registre des anomalies et risques | R, G, T | `1-audit/02-registre-anomalies-risques.md` | ✅ |
| 3 | Analyse de l'existant | R, G | `1-audit/03-analyse.md` | ✅ |

### Phase 2 — Répondre au besoin actuel (BC01, BC02, BC05)

| # | Livrable | Source | Fichier aujourd'hui | Statut |
|---|---|---|---|---|
| 4 | Étude d'opportunité | R, G, T | `1-audit/etude-opportunite.md` | ✅ (rangé en phase 1) |
| 5 | Note stratégique | G, T | `2-modelisation/note-strategique.md` | ✅ |
| 6 | Note de cadrage | R, G, T | `6-pilotage/note-de-cadrage.md` | ⚠️ pas de validation écrite (valideur : Sébastien) ; cibles des indicateurs « à valider » |
| 7 | Backlog priorisé (MoSCoW) | T | `6-pilotage/backlog-moscow.md` | ✅ |
| 8 | Cahier des charges technique | R, T | `2-modelisation/cahier-des-charges-technique.md` | ✅ |
| 9 | MCD / MLD cible | R, G, T | `2-modelisation/mcd.md` | ⚠️ vide (travail humain) |
| 10 | `migration.sql` | R, G, T | dans **Fil-Rouge-API** `docker/migrations/v2-vers-v3/` | ⚠️ aucun renvoi depuis `livrables/` → copie demandée (Gabriel, 20/11) |
| 11 | Note d'indexation (EXPLAIN avant/après) | G, T | `2-modelisation/note-indexation.md` | ✅ |

### Phase 3 — Absorber la croissance (BC01, BC02, BC05)

| # | Livrable | Source | Fichier aujourd'hui | Statut |
|---|---|---|---|---|
| 12 | Note de dimensionnement 3V | R, G, T | `3-architecture/note-dimensionnement-3v.md` | ✅ |
| 13 | Dossier d'architecture | R, G, T | `3-architecture/dossier-architecture.md` | ✅ |
| 14 | Matrice de décision | R, G, T | `3-architecture/matrice-decision-architecture.md` | ✅ |
| 15 | Schéma OLAP + alimentation | R, G, T | `2-modelisation/olap.md` | ✅ (rangé en phase 2) |
| 16 | Note qualité des données | T | `normalised/rapport_anomalies.txt` | ⚠️ hors de `livrables/` → copie demandée (Gabriel, 20/11) |
| 17 | PCA / PRA | R, T | `3-architecture/pca-pra-plan-de-migration.md` | ✅ |
| 18 | Plan de migration | R | même fichier que 17 | ✅ |
| 19 | Note d'environnement technique | T | `3-architecture/note-environnement-technique.md` | ✅ |

### Phase 4 — Réaliser le parcours futur avec l'IA (BC03, BC05)

| # | Livrable | Source | Fichier aujourd'hui | Statut |
|---|---|---|---|---|
| 20 | Dossier de conception applicative + maquettes | R, G, T | `4-application/conception-applicative.md`, `maquettes-espace-acquereur.html` | ✅ |
| 21 | Processus métier (BPMN) | T | `4-application/processus-metier.md` | ✅ (en Mermaid, pas en BPMN) |
| 22 | Plan de tests + rapports d'exécution | R, G, T | `4-application/tests-fonctionnels.md`, `rapport-tests.md` | ✅ |
| 23 | Note de sécurité + extraits de code | T | `4-application/note-securite-applicative.md` | ✅ |
| 24 | Pipeline CI + indicateurs qualité | T | — | ❌ |
| 25 | Schéma du programme d'IA | R, G, T | `4-application/schema-programme-ia.md` (+ `.html`) | ✅ |
| 26 | Conception du matching + features | R, G, T | `4-application/conception-matching-features.md` | ✅ |
| 27 | Code source commenté et testé | R | dépôt **Fil-Rouge-API** | ✅ (aucun renvoi depuis `livrables/`) |

### Transverses (obligatoires)

| # | Livrable | Source | Fichier aujourd'hui | Statut |
|---|---|---|---|---|
| 28 | Registre RGPD | R, G, T | `5-transverse/registre-rgpd.md` | ✅ |
| 29 | Note d'éco-conception | R, G, T | `5-transverse/note-eco-conception.md` | ✅ |
| 30 | Note d'accessibilité PSH | R, G, T | `5-transverse/note-accessibilite-psh.md` | ✅ |
| 31 | Note souveraineté / sécurité IA | R, G, T | `5-transverse/note-souverainete-securite-ia.md` | ✅ |

### Pilotage (toutes phases, BC02)

| # | Livrable | Source | Fichier aujourd'hui | Statut |
|---|---|---|---|---|
| 32 | Planning (Gantt) + jalons | G, T | `6-pilotage/gantt.md` | ⚠️ 3 dates à confirmer |
| 33 | Matrice des risques + mitigation | G, T | dans la note de cadrage (tableau des risques) | ✅ (pas de fichier à part) |
| 34 | RACI | G, T | `6-pilotage/raci.md` | ⚠️ « À compléter » : proposition des phases 2-4 vue par 2 membres sur 4 ; R et A du dossier professionnel à désigner |
| 35 | Comptes rendus d'ateliers | T | — | ❌ |
| 36 | Grille d'auto-évaluation | R, G | `6-pilotage/grille-auto-evaluation.md` | ⚠️ pas remplie (« pas grave », Gabriel, 20/11) |

**Compte** : 36 lignes ; ✅ 27 · ⚠️ 7 · ❌ 2.

### Dans `livrables/` sans être un livrable

- Les **8 schémas d'appui** (`01` à `08`) : ils illustrent les livrables, aucune ligne du sujet ne les demande.
- `3-architecture/swot-croissance.md` : appui du dossier d'architecture (modèle SWOT fourni, pas exigé).
- `2-modelisation/mcd-a-mettre-a-jour.md` : liste de travail sur le MCD.
- Les preuves de mesure : `indexation/`, `charge/`, `securite/` (scripts et sorties), `images/`.

## 3. La proposition de rangement

Trois principes :

1. **Un dossier par phase**, dans l'ordre du sujet (c'est déjà le cas, et c'est ce que conseille `ORGANISATION-DEPOT.md`).
2. **Seuls les livrables portent un numéro**, `<phase>.<ordre>`, dans l'ordre de lecture logique. GitHub les affiche alors dans cet ordre.
3. **Tout ce qui sert de preuve ou d'appui va dans `annexes/`** de sa phase, sans numéro.

Plus une porte d'entrée : **`livrables/README.md`** = la liste officielle ci-dessus (livrable → fichier → compétence), pour le jury.

```
livrables/
├── README.md                          ← la liste officielle, pour le jury
├── 1-audit/
│   ├── 1.1-cartographie-si.md
│   ├── 1.2-registre-anomalies-risques.md
│   └── 1.3-analyse.md
├── 2-modelisation/                    ← phase 2 : besoin actuel
│   ├── 2.1-etude-opportunite.md       ← venu de 1-audit
│   ├── 2.2-note-strategique.md
│   ├── 2.3-note-de-cadrage.md         ← venu de 6-pilotage
│   ├── 2.4-backlog-moscow.md          ← venu de 6-pilotage
│   ├── 2.5-cahier-des-charges-technique.md
│   ├── mcd.md                         ← nom gardé : travail humain, on n'y touche pas
│   ├── 2.7-migration.md               ← nouveau : renvoi court vers les scripts de Fil-Rouge-API
│   ├── 2.8-note-indexation.md
│   └── annexes/
│       ├── schema-donnees-comptes-et-fiches.md
│       ├── schema-donnees-recherche-et-mandat.md
│       ├── schema-donnees-vente-et-remuneration.md
│       └── indexation/
├── 3-architecture/                    ← phase 3 : croissance
│   ├── 3.1-note-dimensionnement-3v.md
│   ├── 3.2-dossier-architecture.md
│   ├── 3.3-matrice-decision-architecture.md
│   ├── 3.4-olap.md                    ← venu de 2-modelisation
│   ├── 3.5-pca-pra-plan-de-migration.md
│   ├── 3.6-note-environnement-technique.md
│   └── annexes/
│       ├── schema-evolution-du-schema.md, schema-trajet-requete.md,
│       │   schema-chemin-des-donnees.md, schema-pile-docker.md
│       ├── swot-croissance.md
│       ├── charge/
│       └── images/
├── 4-application/                     ← phase 4 : parcours futur avec l'IA
│   ├── 4.1-conception-applicative.md
│   ├── 4.1-maquettes-espace-acquereur.html
│   ├── 4.2-processus-metier.md
│   ├── 4.3-tests-fonctionnels.md
│   ├── 4.4-rapport-tests.md
│   ├── 4.5-note-securite-applicative.md
│   ├── 4.6-schema-programme-ia.md (+ .html)
│   ├── 4.7-conception-matching-features.md
│   └── annexes/
│       ├── schema-connexion-et-jeton.md
│       ├── securite/
│       └── images/
├── 5-transverse/
│   ├── 5.1-registre-rgpd.md
│   ├── 5.2-note-eco-conception.md
│   ├── 5.3-note-accessibilite-psh.md
│   └── 5.4-note-souverainete-securite-ia.md
└── 6-pilotage/
    ├── 6.1-gantt.md
    ├── 6.2-raci.md
    ├── 6.3-grille-auto-evaluation.md
    └── images/
```

- `mcd-a-mettre-a-jour.md` sort vers `md/equipe/` (liste de travail) — **à confirmer par le groupe**, car il parle du MCD.
- Les deux manques (comptes rendus d'ateliers, CI) prendront leur numéro quand ils seront écrits : `6.4-comptes-rendus-ateliers.md`, `4.8-pipeline-ci.md`.
- La note qualité des données reste dans `normalised/` : le README y renvoie.

## 4. Ce que ça coûte, ce que ça risque

- ~30 fichiers renommés ou déplacés par `git mv` (l'historique suit) ; **contenu inchangé**, sauf les liens.
- Tous les liens relatifs réparés par script, puis recomptés : objectif 0 lien cassé.
- Les 12 copies de Confluence gardent leur en-tête ; Confluence n'est pas touché.
- ⚠️ Les liens vers les anciens chemins **depuis l'extérieur** (Discord, Confluence) ne suivront pas : GitHub ne redirige pas un fichier renommé.
- Durée : ~45 min.

> **QUAND LIRE** : on reprend après une longue interruption, on choisit le
> prochain chantier, ou on doute d'une décision passée. Les cinq lignes de
> `CLAUDE.md` suffisent dans la plupart des cas — ouvrir ceci seulement quand
> elles ne suffisent pas.

# État du projet — daté

## Où on en est

*(au 2026-09-21 — remplace l'état du 2026-09-07 ; l'historique est au journal)*

- **Base de données** — schéma `fil_rouge_immobilier` (**18 tables**, montants
  en **euros**) dans `docker/init-v2/`, monté par `docker/docker-compose.yml`
  depuis le 2026-09-21. Chaîne complète `01` → `02` → `03` vérifiée sur
  PostgreSQL 16 : 0 erreur, 2 556 biens, 1 976 photos, 18 clients. Les choix,
  les hypothèses et les 6 points ouverts sont dans `docker/init-v2/README.md`.
  `docker/init/` (12 tables, K€) reste intact mais n'est plus monté.
- **API** — FastAPI + SQLModel, CRUD en trois couches (`routes/`, `services/`,
  `repositories/`), pas de PATCH, choix assumé. ⚠️ **12 modèles pour 18
  tables** : `sale`, `payment`, `commission_scale`, `hunter_performance`,
  `parameters_fees` et `visit` n'existent pas côté API. Toute la chaîne de
  rémunération est en base et invisible depuis l'API.
- **Tests** — seulement `test_health.py` (test de fumée, ne touche pas la
  base). `conftest.py` expose une fixture `client` ; **pas encore de fixture
  de base de test isolée** — c'est le premier verrou.
- **Métier** — les règles (mandat, rémunération, barème, performance) existent
  en Gherkin dans `user-stories/` et en notes, mais **aucune n'est
  implémentée**. Le schéma non plus ne les porte pas : `U02` (exclusivité du
  mandat) et `U05` (durée de 6 mois) sont écrits mais commentés dans le `01`.
- **Données** — `normalised/` porte `normalised.py`, les annonces normalisées,
  `populate_estate.sql` et `rapport_anomalies.txt`.
- **Livrables** — `livrables/2-modelisation/` porte trois rapports du chantier
  `C` ; les trois autres dossiers sont vides (`.gitkeep`).

## La TODO ordonnée — les chantiers possibles

C'est d'ici que `/vlp:chantier` tire ses propositions. Un chantier par entrée,
ordonné par ce qui débloque le reste.

| # | Chantier | Ce qu'il apporte | Coût estimé | Dépend de |
|---|---|---|---|---|
| 0 | Rattraper l'API sur les 18 tables | 6 modèles + couches manquants (`sale`, `payment`, `commission_scale`, `hunter_performance`, `parameters_fees`, `visit`) : sans eux, aucune règle de rémunération n'est implémentable | 4–6 fiches | rien |
| 1 | Base de test isolée + tests d'intégration CRUD | une vérification qui prouve quelque chose : aujourd'hui `pytest` ne teste que le health-check | 4–6 fiches | rien |
| 2 | Règles métier mandat / rémunération / barème | implémente les US 00 et 07 dans la couche `services/`, avec leurs tests ; reprend `U02` et `U05` laissés commentés dans le `01` | 5–7 fiches | 0, 1 |
| 3 | Livrable 2 — modélisation (MCD/MLD) | reconstruit le modèle depuis le SQL existant, pour `livrables/2-modelisation/` | 3–4 fiches | rien |
| 4 | Livrable 1 — audit des données | rapport de normalisation à partir de `normalised/rapport_anomalies.txt` | 3–4 fiches | rien |
| 5 | Livrable 3 — architecture | documente les trois couches et les choix (pas de PATCH, bases génériques) | 2–3 fiches | 1 |

## Journal des décisions

Une ligne par décision imprévue tranchée en cours de fiche — jamais un résumé
de ce que le code dit déjà.

- **2026-09-07** — le contexte IA (`CLAUDE.md`, `CHANTIER.md`, `context AI/`)
  est versionné : le projet se travaille à plusieurs.
- **2026-09-07** — `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/` est
  déclaré source de vérité en lecture seule ; rien n'y est jamais écrit.
- **2026-09-11** — pour le chantier `C*` seulement,
  `docker/init/01_create_fil_rouge_immobilier.sql` est déclaré **périmé** et mis
  hors jeu : l'autorité passe aux `user-stories/`, puis au MPD. Dérogation
  explicite à la règle 3 de `CLAUDE.md`, demandée par l'utilisateur qui refera
  ce fichier. Le MPD porte 18 tables, le SQL n'en a que 12.
- **2026-09-11** — la vérification `python -m pytest -q` ne tourne pas :
  `sqlmodel` absent du Python 3.14 global, aucun environnement virtuel dans
  `API/`. L'utilisateur tranche : on le signale, on n'installe rien. Les fiches
  `C*` ne touchent aucun code ; leur critère de fin fait foi.
- **2026-09-11** — `C2` : l'annexe des user stories porte une colonne
  « Citation » (texte exact de la ligne source) en plus des trois prévues, et
  laisse toutes les colonnes MPD « à rattacher » faute d'ouvrir l'inventaire
  `C1`. Offre d'achat, facture et rendez-vous n'ont aucune table parmi les 18.
- **2026-09-11** — `C3` : l'annexe des notes relève deux contradictions sans
  les trancher — `X01` (ancienneté et performance : clé du barème ou
  majoration du taux) et `X02` (unité de H : € au centime ou K€) — ainsi que
  l'exemple Bruno, payé au-delà des 6 mois que pose sa propre note. Les trois
  restent à arbitrer en `C5`.
- **2026-09-11** — `C4` : l'offre d'achat est rattachée à `EstateProposed`, la
  note d'avis à `Estate_SearchRequest` ; le rendez-vous reste sans table. Le
  rapport établit que `Client` (`is married` en deux mots) et `Criteria`
  (quatre clauses `ck_client_*` sur des colonnes absentes) ne se créent pas en
  l'état du MPD.
- **2026-09-11** — `C5` : la facture est rattachée à `Payment.status`, le
  montant collecté par le notaire à `Sale.fees_amount` ; les indicateurs de
  performance, sans colonne, sont jugés couverts quand leurs données sources
  existent. Restent à vérifier dans le MPD : l'extension `btree_gist` (exigée
  par deux `EXCLUDE`) et `HunterPerformance.id_payment`, déclaré deux fois.
- **2026-09-11** — **chantier `C` clos** (contraintes du MPD). Livré :
  l'inventaire du MPD, les annexes de règles (51 en user stories, 84 en notes)
  et `livrables/2-modelisation/09-rapport-ecarts-contraintes.md` (sorti de
  `context AI/` le jour même) — 150 verdicts sur 18 tables (84
  couvertes, 49 partielles, 16 absentes, 1 fausse), 133 règles reprises sur
  135. Laissé ouvert : `X01`, `X02` (unité de H), l'exemple Bruno, `U29` et
  `F04` sans table, `pytest` non lancé. Coût : 31 326 311 tokens sur 5
  sessions, comptées au 2026-09-11.

- **2026-09-21** — **`X02` tranché : l'unité monétaire est l'euro**, en
  `NUMERIC(12,2)`. Non par préférence, mais sur trois mesures : 37 des 47
  valeurs des fixtures officielles débordent `NUMERIC(6,1)` ; le barème de
  `10_calcul_remuneration_chasseur.feature` a des bornes à l'euro près
  (`199999` basculait à 35 % au lieu de 30 %) ; l'arrondi au centime exigé par
  la règle est impossible au dixième de K€. La décision `B` (K€) du 2026-09-11
  est réfutée. Preuves dans `docker/init-v2/README.md` §1.
- **2026-09-21** — le schéma **18 tables** est écrit dans `docker/init-v2/`,
  fusion de deux versions (la mienne et celle d'un coéquipier), et remplace
  `docker/init/` dans `docker-compose.yml`. La dérogation du 2026-09-11 — le
  SQL 12 tables déclaré périmé — **est levée** : la règle 3 de `CLAUDE.md`
  redevient pleine, en pointant `init-v2`.
- **2026-09-21** — les prix des 2 556 biens sont repris **un par un** depuis la
  colonne `price_eur` du CSV, et non par multiplication des K€ : la
  multiplication donnait `62 500` au lieu de `62 495`. **2 531 biens sur
  2 556** auraient eu un prix faux, jusqu'à 50 € d'écart.
- **2026-09-21** — la contrainte `ck_client_address_all_or_nothing` rejetait
  les 18 clients de la source (ville connue, adresse nulle). Corrigée en
  implication à sens unique, mais **l'`ALTER` est laissé visible dans le `02`**
  et non glissé dans le `01` : la correction attend une validation du groupe.
- **2026-09-21** — quatre hypothèses de migration assumées et signalées, à
  confirmer : `hire_date` = date de création du compte, `search_request.status`
  = `confirmed`, `commission_rate` non migrée (sens métier ambigu),
  `energetic_score` retirée (elle était `NULL` partout).
- **2026-09-21** — `CHANTIER.md` et `INSTALLER-LE-WORKFLOW.md` sont supprimés :
  la méthode de chantier vit désormais dans le plugin `vlp`, elle n'est plus
  recopiée dans le dépôt. L'entrée du 2026-09-07 qui cite `CHANTIER.md` reste
  telle quelle : c'est un fait daté, pas une consigne. Les deux fichiers
  restent récupérables depuis le commit `2448614`.
- **2026-09-21** — le dépôt suivait **67 fichiers `.pyc`** : sortis du suivi,
  et un `.gitignore` complet posé. Les livrables du chantier `C`, ses annexes
  et les notes métier (`md/`) sont enfin versionnés — ils ne l'étaient pas.


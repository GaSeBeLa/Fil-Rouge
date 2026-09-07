> **QUAND LIRE** : on reprend après une longue interruption, on choisit le
> prochain chantier, ou on doute d'une décision passée. Les cinq lignes de
> `CLAUDE.md` suffisent dans la plupart des cas — ouvrir ceci seulement quand
> elles ne suffisent pas.

# État du projet — daté

## Où on en est

*(au 2026-09-07, à l'équipement du projet)*

- **Base de données** — schéma `fil_rouge_immobilier` (12 tables) écrit dans
  `docker/init/01_create_fil_rouge_immobilier.sql`, monté au démarrage par
  `docker/docker-compose.yml`. C'est la source de vérité du modèle.
- **API** — FastAPI + SQLModel, CRUD complet sur les 12 tables, découpé en
  trois couches (`routes/`, `services/`, `repositories/`) avec des bases
  génériques. Pas de PATCH, choix assumé.
- **Tests** — seulement `test_health.py` (test de fumée, ne touche pas la
  base). `conftest.py` expose une fixture `client` ; **pas encore de fixture
  de base de test isolée** — c'est le premier verrou.
- **Métier** — les règles (mandat, rémunération, barème, performance) existent
  en Gherkin dans `user-stories/` et en notes (`BAREME-COMMISSION.md`,
  `NOTES-REMUNERATION-CHASSEUR.md`), mais **aucune n'est implémentée**.
- **Données** — `normalised/` porte `normalised.py`, les annonces normalisées,
  `populate_estate.sql` et `rapport_anomalies.txt`.
- **Livrables** — les quatre dossiers de `livrables/` sont vides (`.gitkeep`).

## La TODO ordonnée — les chantiers possibles

C'est d'ici que `/vlp:chantier` tire ses propositions. Un chantier par entrée,
ordonné par ce qui débloque le reste.

| # | Chantier | Ce qu'il apporte | Coût estimé | Dépend de |
|---|---|---|---|---|
| 1 | Base de test isolée + tests d'intégration CRUD | une vérification qui prouve quelque chose : aujourd'hui `pytest` ne teste que le health-check | 4–6 fiches | rien |
| 2 | Règles métier mandat / rémunération / barème | implémente les US 00 et 07 dans la couche `services/`, avec leurs tests | 5–7 fiches | 1 |
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

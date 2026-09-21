# Fil Rouge Immobilier — à lire en premier, en entier, et seul

Projet fil rouge EISI Data-IA : audit de données, modélisation et API REST
(FastAPI + SQLModel sur PostgreSQL) pour un service de chasse immobilière.
Ce n'est **pas** un produit hébergé : pas de front, pas de déploiement.
Dossier `Fil-Rouge/`, dépôt git à sa racine. L'énoncé et les fixtures d'origine
vivent dans `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/` et
`../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack/` — **lecture seule, jamais
modifiés**.

## Où on en est — en cinq lignes

- Le schéma PostgreSQL (**18 tables**, montants en **euros**) est posé dans
  `docker/init-v2/` et monté par `docker compose`. `docker/init/` (12 tables,
  K€) est l'ancien schéma, gardé intact, plus monté.
- L'API expose un CRUD complet en trois couches (routes / services /
  repositories) sur les **18 tables**, en `Decimal` pour tout montant.
  91 opérations vérifiées en `200` contre la base. Seul le health-check est
  testé automatiquement : la base de test isolée reste le premier verrou.
- Les user stories Gherkin (`user-stories/`) couvrent le parcours actuel et le
  futur parcours IA ; les règles métier ne sont pas encore implémentées.
- `normalised/` porte la normalisation des annonces et son rapport d'anomalies.
- `livrables/2-modelisation/` porte trois rapports du chantier `C` ; les trois
  autres livrables sont vides. Détail daté dans `context AI/08-etat.md`.

## Cinq règles non négociables

1. **Annoncer le plan en une ou deux phrases avant d'agir**, et poser un
   questionnaire au moindre choix ouvert.
2. **Mesurer avant de corriger**, et afficher les comptes bruts à côté du
   verdict — un instrument muet rend son propre échec indiagnosticable.
3. **Les deux dossiers `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack*/` ne se
   modifient jamais**, et `docker/init-v2/01_create_fil_rouge_immobilier.sql`
   est le schéma de référence : tout modèle SQLModel s'y confronte par grep.
4. **Tout montant est en euros, `NUMERIC(12,2)`** — jamais en K€. La décision
   est tranchée et prouvée : `docker/init-v2/README.md` §1.
5. **Aucun secret ni `.env` dans git**, aucun chemin absolu dans le code.

Prose et commentaires de code en français ; noms de code en anglais.
Le contexte IA (`CLAUDE.md`, `context AI/`) est **versionné** : le projet se
travaille à plusieurs. Les notes métier libres vivent dans `md/`.

## Routage — ouvrir ceci, et rien d'autre

Cette table remplace la lecture de `00-INDEX.md`. Si la tâche n'y figure pas,
et seulement dans ce cas, ouvrir l'index.

| La tâche | Ouvrir |
|---|---|
| écrire ou modifier du code de l'API | `API/README.md`, puis le fichier visé |
| créer un module, chercher où va un bout de code | `API/src/app/main.py` — son en-tête décrit les trois couches |
| vérifier une règle métier | `user-stories/<NN>_*.feature` |
| vérifier une table, une colonne, une contrainte | `docker/init-v2/01_create_fil_rouge_immobilier.sql` |
| comprendre un choix du schéma v2 (euros, migration, hypothèses) | `docker/init-v2/README.md` |
| ouvrir un chantier, ou le découper en fiches | **lancer `/vlp:chantier`** — la méthode vit dans le kit, pas ici |
| relire une fiche `C1` à `C5` | `context AI/09-contraintes-mpd.md` — chantier **clos** le 2026-09-11, ne se rejoue pas |
| reprendre après une longue interruption | `context AI/08-etat.md` |

## Économie de contexte

La fenêtre sature par **densité de contexte**, pas par volume horaire. Donc,
dans cet ordre :

- **Un fichier de contexte ne s'ouvre que si la table ci-dessus le nomme.** Le
  voisin d'un fichier utile n'est pas utile ; il n'est que du volume.
- **Ne jamais lire le dossier de contexte en entier**, ni le README.
- **Une tâche, une session.** `/clear` entre deux tâches : une session laissée
  ouverte relit tout son passé à chaque tour.
- **Explorer et lire avec un modèle léger**, garder le lourd pour ce qui décide.
- Grep ciblé plutôt que lecture de fichier entier, dans le code comme ici.

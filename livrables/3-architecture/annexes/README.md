# Les schémas d'appui

> Huit schémas en Mermaid, qui illustrent les livrables (GitHub les dessine). Ils ne sont pas des livrables du sujet : la liste officielle est dans [`livrables/README.md`](../../README.md).
> Faits pour la présentation du 2026-10-16 (schémas 1 à 4), puis complétés le 2026-11-02 (5 à 8). Chacun est rangé dans les annexes de sa phase : 1 à 4 ici, 5 à 7 en `2-modelisation/annexes/`, 8 en `4-application/annexes/`.

## Les schémas

| N° | Fichier | Ce qu'il montre | Origine |
|---|---|---|---|
| 1 | [schema-evolution-du-schema.md](schema-evolution-du-schema.md) | les versions de la base : 3, 12, 18, 22 tables | présentation |
| 2 | [schema-trajet-requete.md](schema-trajet-requete.md) | une requête dans l'API, et ses refus 401, 422, 403, 404 | présentation, complété |
| 3 | [schema-chemin-des-donnees.md](schema-chemin-des-donnees.md) | Airflow, MinIO, PostgreSQL, Elasticsearch, Kibana | présentation |
| 4 | [schema-pile-docker.md](schema-pile-docker.md) | les 11 conteneurs, leurs profils, ports, ordre de démarrage, mémoire | présentation, complété |
| 5 | [schema-donnees-comptes-et-fiches.md](../../2-modelisation/annexes/schema-donnees-comptes-et-fiches.md) (phase 2) | comptes, fiches et les 5 rôles | nouveau |
| 6 | [schema-donnees-recherche-et-mandat.md](../../2-modelisation/annexes/schema-donnees-recherche-et-mandat.md) (phase 2) | demande, critères, mandat, biens proposés et visités | nouveau |
| 7 | [schema-donnees-vente-et-remuneration.md](../../2-modelisation/annexes/schema-donnees-vente-et-remuneration.md) (phase 2) | vente, paiement du chasseur, paramètres | nouveau |
| 8 | [schema-connexion-et-jeton.md](../../4-application/annexes/schema-connexion-et-jeton.md) (phase 4) | se connecter, puis appeler une route avec son jeton | nouveau |

## Déjà ailleurs, pas recopié ici

- Le **schéma OLAP** en étoile : [`../3-architecture/3.4-olap.md`](../3.4-olap.md).
- Le **flux de données** en détail : [`../../md/flux/schema-du-flux.md`](../../../md/flux/schema-du-flux.md).
- La **traçabilité de la rémunération** : [`../../md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md`](../../../md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md).

## Les couleurs

- 🟦 Bleu : la base et l'API.
- 🟩 Vert : le profil `airflow`, ou une réponse `200`.
- 🟧 Ocre : le profil `elk`.
- 🟥 Rouge : un refus.

## Les tenir à jour

- Une table, un service ou une route change → le schéma qui la montre
  change dans le **même commit** (règle « Ramasser sa poubelle »).
- En cas d'écart, **le code fait foi** : chaque fichier nomme ses sources.

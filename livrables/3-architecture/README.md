# Livrable 3 — l'architecture en schémas

> Un fichier par schéma, en Mermaid : GitHub les dessine, et ils se relisent
> comme du texte. Créé le 2026-11-02.
>
> Les schémas 1 à 4 viennent de la présentation du 2026-10-16
> (`md/equipe/2026-10-16-presentation.md`) ; les schémas 5 à 8 manquaient.
> Le code lu est celui du dépôt **Fil-Rouge-API**, au commit `01514b2`.

## Les schémas

| N° | Fichier | Ce qu'il montre | Origine |
|---|---|---|---|
| 1 | [01-evolution-du-schema.md](01-evolution-du-schema.md) | les versions de la base : 3, 12, 18, 22 tables | présentation |
| 2 | [02-trajet-requete.md](02-trajet-requete.md) | une requête dans l'API, et ses refus 401, 422, 403, 404 | présentation, complété |
| 3 | [03-chemin-des-donnees.md](03-chemin-des-donnees.md) | Airflow, MinIO, PostgreSQL, Elasticsearch, Kibana | présentation |
| 4 | [04-pile-docker.md](04-pile-docker.md) | les 11 conteneurs, leurs profils, ports, ordre de démarrage, mémoire | présentation, complété |
| 5 | [05-donnees-comptes-et-fiches.md](05-donnees-comptes-et-fiches.md) | comptes, fiches et les 5 rôles | nouveau |
| 6 | [06-donnees-recherche-et-mandat.md](06-donnees-recherche-et-mandat.md) | demande, critères, mandat, biens proposés et visités | nouveau |
| 7 | [07-donnees-vente-et-remuneration.md](07-donnees-vente-et-remuneration.md) | vente, paiement du chasseur, paramètres | nouveau |
| 8 | [08-connexion-et-jeton.md](08-connexion-et-jeton.md) | se connecter, puis appeler une route avec son jeton | nouveau |

## Déjà ailleurs, pas recopié ici

- Le **schéma OLAP** en étoile : [`../2-modelisation/olap.md`](../2-modelisation/olap.md).
- Le **flux de données** en détail : [`../../md/flux/schema-du-flux.md`](../../md/flux/schema-du-flux.md).
- La **traçabilité de la rémunération** : [`../../md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md`](../../md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md).

## Les couleurs

- 🟦 Bleu : la base et l'API.
- 🟩 Vert : le profil `airflow`, ou une réponse `200`.
- 🟧 Ocre : le profil `elk`.
- 🟥 Rouge : un refus.

## Les tenir à jour

- Une table, un service ou une route change → le schéma qui la montre
  change dans le **même commit** (règle « Ramasser sa poubelle »).
- En cas d'écart, **le code fait foi** : chaque fichier nomme ses sources.

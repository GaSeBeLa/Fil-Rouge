### ADR-061 : Elasticsearch est une copie de PostgreSQL, refaite chaque nuit

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 15/10/2026
* **Statut :** ✅ accepté (Sébastien, Discord, 15/10/2026, questions `flux-5`, `flux-6` et `flux-14`). Publié sur Confluence le 15/10/2026, dans « Proposé », pour relecture par le groupe.
* **Décideurs :** Sébastien.
* **Voir aussi :** ADR-054 (contact du vendeur) ; ADR-027 (droits par rôle) ; ADR-062 (profils Compose)

**Contexte**

* Le groupe veut une recherche de biens par texte, par ville, par prix et autour d'un point. PostgreSQL le fait mal pour le texte en français et la distance.
* Le TP1 du cours Elasticsearch indexe des offres et les cherche : c'est le même besoin (`md/flux/cours-elasticsearch-synthese.md`).

**Options**

1. **Un index `estates` rempli chaque nuit par un DAG, lu par une route de l'API.** **Retenue.**
2. L'API écrit dans Elasticsearch à chaque création ou modification d'un bien. Écartée : deux écritures à garder d'accord, et l'API dépendrait d'Elasticsearch pour écrire.
3. Pas d'Elasticsearch : chercher dans PostgreSQL. Écartée : pas de recherche en français ni de recherche autour d'un point sans ajouter d'extension.

**Décision**

1. **PostgreSQL reste la seule source de vérité.** L'index `estates` n'est qu'une copie, qui se reconstruit.
2. Le DAG `estates_index` (4 h) copie les biens (`index`), puis retire ceux qui n'existent plus (`prune`).
3. La copie ne prend que des champs choisis : **ni contact du vendeur** (`estate_contact`, ADR-054), **ni rue, ni numéro**, ni auteur.
4. La route **`GET /estates/search`** est ouverte aux mêmes rôles que la lecture des biens (`ALL_ROLES`, question `flux-14`).
5. Chacun son compte : `airflow_indexer` écrit dans `estates`, `api_search` le lit, rien d'autre.
6. Elasticsearch arrêté : la recherche répond **503** ; le reste de l'API marche.

**Conséquences**

* Un bien créé dans la journée n'apparaît dans la recherche que la nuit suivante, au plus 24 h plus tard.
* Effacer l'index ne perd rien : un passage du DAG le refait.
* Au jury, une phrase : « la base décide, Elasticsearch ne sert qu'à chercher vite ; on peut le jeter et le refaire en une commande ».

**Ce que cet ADR ne tranche pas**

* 🟡 Faut-il une mise à jour plus fréquente que chaque nuit ?

**Sources**

| Affirmation | Source |
|---|---|
| Index rempli par un DAG | Sébastien, Discord, 15/10/2026, question `flux-5` |
| Route `GET /estates/search` | Sébastien, Discord, 15/10/2026, question `flux-6` |
| Mêmes rôles que la lecture, jamais `estate_contact` | Sébastien, Discord, 15/10/2026, question `flux-14` ; ADR-054 |
| Recherche du TP1 | `md/flux/cours-elasticsearch-synthese.md` |
| Champs copiés, comptes, 503 | `airflow/src/search/documents.py`, `API/src/app/services/estate_search_service.py`, `docker/docker-compose.yml` (dépôt Fil-Rouge-API) |

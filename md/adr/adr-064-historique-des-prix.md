### ADR-064 : Un prix revu ne se perd pas — la table `estate_price_history`

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 15/10/2026
* **Statut :** ✅ accepté (Sébastien, Discord, 15/10/2026, question `flux-12b`). Pas encore publié sur Confluence.
* **Décideurs :** Sébastien ; colonnes recopiées du MPD de Gabriel (Discord, 15/10/2026).
* **Voir aussi :** ADR-063 (clé d'une annonce) ; ADR-060 (MinIO)

**Contexte**

* Une annonce réimportée peut revenir avec un autre prix. Sébastien a demandé si l'ancien prix serait perdu.
* `estate` n'a qu'une colonne `price` : la remplacer efface l'ancien prix.

**Options**

1. **Une table `estate_price_history` : un prix par bien et par jour vu.** **Retenue.**
2. Remplacer le prix, et laisser l'historique dans les fichiers bruts de `bronze`. Écartée : l'historique existe, mais ne se lit pas en SQL.
3. Garder le premier prix. Écartée : la base afficherait un prix faux.

**Décision**

1. La table vient de la migration **48** (`48_historique-des-prix.sql`) :
   * `id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY` ;
   * `created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'utc')` ;
   * `id_estate INTEGER NOT NULL REFERENCES estate(id) ON DELETE RESTRICT` ;
   * `price INTEGER NOT NULL CHECK (price >= 0)`, en euros ;
   * `seen_at DATE NOT NULL` ;
   * `CONSTRAINT uq_estate_price_history_estate_seen UNIQUE (id_estate, seen_at)`.
2. `estate.price` garde le dernier prix vu ; chaque import note le prix du jour.

**Conséquences**

* Rejouer une date n'ajoute rien : un seul prix par bien et par jour (FLX4 : 151 lignes au premier passage, 151 après le second).
* `ON DELETE RESTRICT` : un bien qui a un historique ne s'efface pas sans effacer d'abord son historique.
* Au jury, une phrase : « le prix courant est dans `estate`, son histoire dans `estate_price_history` ».

**Ce que cet ADR ne tranche pas**

* 🟡 La durée de garde de l'historique.

**Sources**

| Affirmation | Source |
|---|---|
| Table d'historique | Sébastien, Discord, 15/10/2026, question `flux-12b` |
| Colonnes et contrainte | MPD de Gabriel, Discord, 15/10/2026 ; `docker/init-v3/`, migration 48 (dépôt Fil-Rouge-API) |
| 151 puis 151 | `context AI/17-flux-donnees.md`, fiche FLX4 |

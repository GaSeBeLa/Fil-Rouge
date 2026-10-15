### ADR-063 : La clé d'une annonce est `estate.reference`

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 15/10/2026
* **Statut :** ✅ accepté (Sébastien, Discord, 15/10/2026, question `flux-16`). Pas encore publié sur Confluence.
* **Décideurs :** Sébastien.
* **Voir aussi :** ADR-047 (biens importés et saisis à la main) ; ADR-064 (historique des prix)

**Contexte**

* L'import de chaque nuit doit reconnaître une annonce déjà vue, pour ne pas créer le même bien deux fois.
* Le cadrage prévoyait une colonne neuve, `estate.source_reference` (question `flux-12`).
* Compté le 15/10/2026 : la colonne `estate.reference` existe déjà, en `VARCHAR(50) NOT NULL UNIQUE`, et elle contient déjà la référence de l'annonce pour **2556 biens sur 2556**. La prémisse du cadrage était fausse.

**Options**

1. **Prendre `estate.reference` comme clé.** **Retenue.**
2. Ajouter `source_reference`. Écartée : une deuxième colonne pour la même valeur.
3. Clé faite de l'agence et de la référence. Écartée : la référence est déjà unique dans toute la table.

**Décision**

1. L'import cherche le bien par `reference` : trouvé, il le met à jour ; pas trouvé, il le crée.
2. Pas de colonne `source_reference`, pas de migration pour elle. Le MPD est corrigé (Gabriel).

**Conséquences**

* Rejouer l'import ne crée aucun bien en double (FLX4 : 2556 → 2707 au premier passage, + 0 au second).
* Un même bien publié par **deux agences** donne **deux lignes** : deux références différentes. Compté au cadrage : 1 seul doublon ville + adresse + surface sur 2556 annonces.
* Au jury, une phrase : « la référence de l'annonce était déjà dans la base et déjà unique ; on s'en sert comme clé, sans rien ajouter ».

**Ce que cet ADR ne tranche pas**

* 🟡 Reconnaître le même bien chez deux agences : hors du chantier.

**Sources**

| Affirmation | Source |
|---|---|
| Clé = `estate.reference` | Sébastien, Discord, 15/10/2026, question `flux-16` |
| `VARCHAR(50) NOT NULL UNIQUE`, 2556 sur 2556 | `docker/init-v3/01_create_fil_rouge_immobilier.sql` (dépôt Fil-Rouge-API) ; comptage en base du 15/10/2026 |
| Deux agences = deux lignes | Laurence, Discord, 15/10/2026 (question `flux-12`) ; comptage du cadrage |
| 2556 → 2707, puis + 0 | `context AI/17-flux-donnees.md`, fiche FLX4 |

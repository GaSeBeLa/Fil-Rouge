# ADR-019 : Absence de clé étrangère entre Sale et Parameters_Fees

> Copié de Confluence (page 52691013, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Remplacé par ADR-030** (« La vente pointe la grille d'honoraires qui a servi », dossier Proposé, publié le 09/10/2026, validation de Jeff à venir).

- La vente porte désormais une clé vers la grille d'honoraires utilisée, obligatoire (`NOT NULL`).
- Une grille vaut « à partir du » jusqu'à la suivante : `UNIQUE (effective_from)` remplace l'`EXCLUDE` `excl_fees_no_overlap`.
- Cette page n'est pas effacée : elle garde la trace de la décision d'origine.

**Date :** 10/09/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte**

`Sale.fees_amount` (H = honoraires collectés par l'entreprise) est calculé à la signature à partir du barème `Parameters_Fees` en vigueur à cette date, puis figé — jamais recalculé. La question s'est posée de savoir si `Sale` devait porter une clé étrangère explicite `id_parameters_fees` vers la ligne de barème utilisée, à l'image de `Payment.id_commission_scale`.

**Options envisagées**

- Option 1 : Ajouter une FK `Sale.id_parameters_fees`, nullable, pointant vers `parameters_fees(id)`.
- Option 2 : Ne pas ajouter de FK ; retrouver le barème applicable par `Sale.signature_date` compris dans l'intervalle `[valid_from, valid_until]` de `Parameters_Fees`, garanti sans ambiguïté par une contrainte d'exclusion.

**Décision**

Option 2 retenue. Pas de FK. Le lien entre `Sale` et `Parameters_Fees` reste implicite, retrouvable par date.

**Justification**

`Parameters_Fees` n'a pas de dimension nominative (contrairement à `Commission_scale.id_hunter`, nullable, qui autorise un barème personnalisé) : c'est un barème global, daté, sans variante possible. Une contrainte `EXCLUDE USING gist` sur `Parameters_Fees` interdit tout chevauchement de périodes, garantissant qu'une date donnée retrouve toujours exactement une ligne — sans ambiguïté à lever par une FK. À l'inverse, `Payment.id_commission_scale` est conservée : deux lignes de `Commission_scale` peuvent produire le même taux pour un même chasseur/tranche (une nominative, une par défaut), donc seule la FK permet de savoir laquelle a réellement servi en cas de litige. Le choix diffère entre les deux tables parce que la source d'ambiguïté diffère — pas par principe général de minimisation des arêtes.

**Conséquences**

- `fees_amount`, une fois figé dans `Sale`, ne sera jamais recalculé même si le barème `Parameters_Fees` correspondant est ultérieurement modifié — cohérent avec la règle de traçabilité déjà actée sur `Payment`.
- Retrouver le barème appliqué à une vente donnée nécessite une requête par date (`valid_from <= signature_date AND (valid_until IS NULL OR valid_until >= signature_date)`), pas une jointure directe.
- La contrainte `excl_fees_no_overlap` (`EXCLUDE USING gist (daterange(valid_from, valid_until, '[]') WITH &&)`, nécessite `CREATE EXTENSION btree_gist`) doit être posée avant toute insertion de données de test, faute de quoi rien n'empêche un faker de générer des périodes qui se chevauchent silencieusement.
- Si un besoin de barème d'honoraires personnalisé par chasseur apparaît un jour (symétrie avec `Commission_scale`), cette décision devra être révisée : l'ambiguïté qui justifie aujourd'hui l'absence de FK disparaîtrait.

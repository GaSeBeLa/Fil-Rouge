# ADR-023 : Stockage de la date de fin de mandat (remplace ADR-004)

> Copié de Confluence (page 52330706, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 11/09/2026 **Statut :** accepté **Décideurs :** L'équipe projet — à valider (Laurence, Jeff, formateur) **Remplace :** ADR-004 (Durée du mandat et renouvellement, 05/08/2026, accepté)

**Contexte**

ADR-004 décidait d'ajouter `duration` et `renewal_count` à `Mandate`, avec la justification suivante : « L'attribut `duration` servira à calculer la date de fin du contrat, non stockée en base de données car calculée. »

Le schéma effectivement livré fait l'inverse :

```sql
signature_date  DATE,
ends_at         DATE NOT NULL,
```

Ni `duration`, ni `renewal_count` n'existent. `ends_at` est calculé une seule fois, à l'insertion (`signature_date + INTERVAL '6 months'` dans le script de migration), puis figé — jamais recalculé. ADR-004 décrit donc l'inverse du livrable, sans trace écrite du changement.

**Options envisagées**

| Option | Description |
| --- | --- |
| 1 | Appliquer ADR-004 à la lettre : ajouter `duration`/`renewal_count`, retirer `ends_at`, recalculer à chaque lecture |
| 2 | Réviser ADR-004 : assumer `ends_at` stocké, retirer `duration`/`renewal_count` de la décision |
| 3 | Hybride : garder `ends_at` stocké *et* ajouter `duration` comme règle de calcul documentée |

**Décision**

Option 2 retenue. `ends_at` reste une colonne stockée sur `Mandate`. `duration` et `renewal_count` ne sont pas ajoutés.

**Justification**

Une date de fin de mandat est une donnée contractuelle, pas un résultat de calcul réévalué en continu. Si la règle des 6 mois change un jour (loi, décision commerciale), une date **calculée à la volée** réécrirait rétroactivement la date de fin de mandats déjà conclus, parfois déjà en litige — la base mentirait sur le passé. Une date **stockée** reste celle réellement contractée à la signature, quelle que soit l'évolution ultérieure de la règle.

`renewal_count` devient inutile en tant que colonne séparée : ADR-010 a déjà introduit `id_mandate_parent`, qui permet de retrouver le nombre de renouvellements par récursion sur la chaîne des mandats liés. Ajouter `renewal_count` dupliquerait une information déjà déductible d'une source existante — deux façons de répondre à la même question, avec le risque qu'elles se contredisent.

**Conséquences**

- **Schéma :** `duration` et `renewal_count` ne sont pas ajoutés à `Mandate`. `ends_at` reste stocké.
- **ADR-004 :** passe au statut « remplacé par ADR-023 » — son contenu n'est pas réécrit, conformément à la règle du journal de décisions (on ne réécrit jamais un ADR accepté).

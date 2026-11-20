# ADR-012 : Définition des budgets min, max et renovation (Table Client)

> Copié de Confluence (page 52363383, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Remplacé par ADR-032** (« Tous les montants en euros », dossier Proposé, publié le 09/10/2026, validation de Jeff à venir).

- Les budgets du client ne sont plus sur `Client` : ils vivent sur `criteria`, en entiers.
- Le budget rénovation et la règle de rapprochement sont retirés (décision du groupe du 09/10/2026, S7) : `needs_renovation` devient un booléen à deux états, `FALSE` par défaut.
- Cette page n'est pas effacée : elle garde la trace de la décision d'origine.

**Date :** 19/08/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte :** Pour qualifier précisément la capacité financière d'un acheteur, un montant unique est souvent insuffisant. Dans la réalité d'une recherche immobilière, un client raisonne avec une fourchette de prix (un idéal et un maximum) et prévoit parfois une enveloppe distincte si le bien nécessite des travaux.

**Options envisagées**

- Option 1 : Un seul champ `budget_global` (Numeric).
- Option 2 : Trois champs distincts (`min_budget`, `max_budget`, `renovation_budget`) de type Numeric.

**Décision :** Option 2 retenue. Ajout des champs `min_budget`, `max_budget` et `renovation_budget` dans la table `Client`.

**Justification :** Stocker une fourchette (min/max) permet de cibler les recherches avec flexibilité, évitant d'exclure des opportunités légèrement sous ou sur le prix cible. Isoler le budget rénovation est stratégique : cela permet au chasseur d'identifier des biens anciens à rénover tout en garantissant mathématiquement que l'enveloppe globale des travaux du client ne sera pas dépassée.

**Conséquences**

- **Base de données :** Le type `Numeric` est utilisé pour garantir des calculs financiers exacts (sans les erreurs d'arrondi des types flottants).
- **Développement SQL :** Les algorithmes de "matching" devront additionner le prix de vente et l'estimation des travaux du bien, puis comparer ce total à la somme du `max_budget` et du `renovation_budget`.
- **Interface utilisateur :** Le formulaire de qualification du client devra proposer ces trois champs distincts au lieu d'une seule case budget.

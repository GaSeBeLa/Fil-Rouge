# ADR-002 : Choix Langue

> Copié de Confluence (page 52592750, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 03/08/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte :** Dans le système d'informations actuel, les noms des tables et attributs sont en français (`secteurs`, `utilisateurs`, `mandats`...). À terme, l'agence GaSeBeLa envisage une dimension internationale (France, DROM, puis Espagne, Allemagne, Royaume-Uni, Irlande, BeNeLux, Italie, Suisse). Se pose la question de la langue à utiliser pour le code, les schémas et la documentation technique du modèle cible.

**Options envisagées**

| Option | Avantages | Inconvénients |
| --- | --- | --- |
| Garder le français | Continuité avec l'existant (pas de re-traduction des schémas déjà produits en Phase 1 : Cartographie, Dictionnaire des données, Registre des anomalies) ; équipe 100% francophone aujourd'hui | Standard peu adapté à une équipe internationale future ; la plupart des outils, ORM et conventions SQL sont pensés en anglais ; freine l'intégration d'éventuels développeurs non francophones lors du rachat d'agences étrangères |
| Passer à l'anglais | Convention standard de l'industrie (SQL, frameworks, ORM) ; facilite le recrutement et l'intégration de développeurs dans les futurs pays couverts ; évite une deuxième migration linguistique plus tard, quand l'international sera concret | Coût de traduction rétroactive des schémas déjà produits en français en Phase 1 ; risque de confusion transitoire le temps que toute l'équipe francophone s'aligne sur le vocabulaire anglais (ex. `mandat` → `mandate`, `chasseur` → `hunter`) ; le métier reste pensé et discuté en français avec le client (GaSeBeLa), donc un lexique de correspondance FR/EN sera nécessaire |

**Décision :** Nous choisissons la langue anglaise pour le code, les schémas de données et les commentaires de code. Le français reste la langue des échanges métier avec le commanditaire et de la documentation de contexte (Readme, comptes-rendus).

**Justification :** Le coût de traduction est ponctuel et porte sur un périmètre encore restreint (3 tables existantes) : il est nettement moins coûteux de le payer maintenant, avant la Phase 2 (conception du modèle cible, qui va largement enrichir le schéma), que de le reporter après avoir construit tout le modèle cible en français. À l'inverse, l'anglais est la convention par défaut de l'écosystème technique retenu (PostgreSQL, ORM, outillage), ce qui réduit la friction pour tout développeur futur, y compris hors de l'équipe actuelle. Le risque de confusion transitoire est jugé mineur et temporaire, à mitiger par un glossaire de correspondance FR/EN (voir `GLOSSAIRE-METIER.md`), alors que le bénéfice — éviter une deuxième migration linguistique une fois l'international engagé — est durable.

**Conséquences :** Dès la correction du système d'information actuel, c'est-à-dire le premier fix, l'anglais sera utilisé pour les schémas MERISE (MCD, MLD et MPD).

- Un glossaire de correspondance FR/EN devra être tenu à jour pour que les échanges avec le commanditaire (en français) restent traçables vers les noms techniques (en anglais).
- Les livrables de Phase 1 déjà produits en français (Cartographie, Dictionnaire des données, Registre des anomalies) ne sont pas rétroactivement traduits : ils documentent l'existant à un instant donné et gardent leur valeur telle quelle ; seul le modèle cible (Phase 2 et suivantes) est concerné par cette décision.

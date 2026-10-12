### ADR-053 : Les trous de la base — les 13 choix du 12/10, et la règle des visites

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 12/10/2026
* **Statut :** proposé
* **Décideurs :** Sébastien a coché les 13 cartes le 12/10/2026 (page à cartes « Les trous de la base à trancher », réponses collées sur Discord). La règle des visites suit le flux des sources, vérifié et retenu par le groupe le même jour (Gabriel, Discord).
* **Complète :** ADR-022 et ADR-043 (adresse du client) ; ADR-039, Décision 2 (exclusivité) ; ADR-048 (critère des visites)
* **Voir aussi :** ADR-034 (réglages du taux) ; ADR-040 (où vit une règle) ; ADR-045 (limites du MVP) ; ADR-049 (anonymisation) ; ADR-050 (renouvellement)

**Contexte**

* Gabriel a audité le schéma : 36 trous, P1 à P36 (`md/journal/problemes-a-regler.md`). Un trou = la base accepte une donnée qu'elle devrait refuser.
* La vérification du 12/10 les a tous rejoués sur PostgreSQL 16 (`md/journal/2026-10-12-verification-audit-problemes.md`). 8 étaient déjà décidés, 15 avaient une réparation prête, **13 restaient à trancher**.
* Cet ADR range ces 13 choix. Les 23 autres suivent le rapport de vérification.

**Décision**

| P | Le trou | Choix | Où |
|---|---|---|---|
| P2 | Deux comptes au même email, à la majuscule près ; aucun format | Index unique sur `lower(email)` et `CHECK` de format, **et** `EmailStr` dans l'API | base + API |
| P3 | Un client sans adresse | Adresse **obligatoire** : `NOT NULL` sur `address`, `postal_code`, `town`, `country_iso`. ✅ Codé le 12/10 (migration 23) | base |
| P12 | Un mandat sur la demande d'un autre client | `UNIQUE (id, id_client)` sur `search_request`, clé étrangère composite depuis `mandate` | base |
| P13 | Le renouvellement contourne l'exclusivité | Corriger le trigger : le parent n'est exempté que si l'enfant est signé **à son échéance** | base (trigger existant) |
| P16 | 251 biens ont plus de chambres que de pièces | Contrôle **à la saisie** ; les 251 restent tels quels | API |
| P18 | Sens de `floor` | `floor` = **l'étage du logement**, le sens de la source | doc |
| P21 | Deux offres acceptées sur un mandat | **Rien** : ADR-045 reste ; `sale.id_mandate` `UNIQUE` garde une seule vente | — |
| P23 | Une visite sur un bien jamais proposé | Vérifié pour les visites `'client'` seulement | API |
| P24 | Visite prévue ou faite ? | On n'enregistre que les visites **faites** : pas de date future | base |
| P25 | Visite hors du mandat | Contrôle des **dates** du mandat ; le statut n'est pas regardé | API |
| P28 | Le mandat reste `active` après la vente | L'API le passe à `completed` dans la transaction de la vente | API |
| P29 | Réglages du taux absurdes | Validation Pydantic à la création d'une version ; ADR-034 Décision 3 reste | API |
| P36 | Plusieurs notes `initial` | **Une seule** par chasseur : index unique partiel | base |

**La règle des visites (P23)**

Le flux suit les sources, étape par étape (retenu par le groupe le 12/10/2026).

1. Le système envoie au chasseur une sélection de biens ; il en fait sa propre sélection et la **propose** au client (`Readme.md:127` ; `05_…feature:14-23`).
2. Le client choisit les biens **à faire visiter par son chasseur**, les commente et les priorise ; le chasseur reçoit une alerte (`Readme.md:99`, `:128` ; `02_…feature:14-17` ; `05_…feature:26-29`).
3. **Visite 1** : le chasseur visite les **biens choisis**, `visitor_type = 'hunter'`. Il rédige ensuite sa note d'avis (`Readme.md:100`, `:129` ; `02_…feature:20-23` ; `06_…feature:10-15`).
4. **Visite 2** : si un bien convient, le client est invité à le visiter, ou fait directement une offre ; `visitor_type = 'client'` (`Readme.md:101` ; `02_…feature:32-35`). Le client la fait **avec son chasseur** : précision du groupe (Gabriel, Discord, 12/10/2026), la source ne le dit pas.
5. Les visites `'client'` portent sur un bien proposé sur ce mandat. L'API le vérifie ; la règle croise deux tables (ADR-040).
6. Seules les visites `'client'`, faites ensemble, comptent pour la rémunération du chasseur (ADR-048 l. 94 ; Gabriel, 12/10/2026).

Le sens des deux valeurs est écrit en base : `COMMENT ON COLUMN visit.visitor_type` (`01`, bloc des métadonnées ; migration 22).

**Lecture écartée**

* Une précision donnée sur Discord le même jour plaçait la visite du chasseur **avant** la proposition, pour se renseigner. Aucune source ne le dit : le groupe a retenu le flux des sources (Gabriel, Discord, 12/10/2026). La visite commune, elle, est gardée pour la visite 2 (point 4).

**Ce que ces choix changent dans les ADR déjà écrits**

* **ADR-022 et ADR-043 (P3).** L'adresse passe de « tout ou rien » à **obligatoire**. ADR-043 Décision 4 (« ses trois champs, ou aucun ») tombe. Les 18 clients repris gardent leurs valeurs factices (ADR-043 Décisions 2 et 3).
* **ADR-049 (P3).** L'anonymisation ne peut plus **vider** l'adresse (`adr-049:114`) : elle met une adresse neutre, comme pour le téléphone. Valeur retenue : `'anonyme'`, `'00000'`, `'anonyme'`, `'FR'` (Sébastien, Discord, 12/10/2026). `'anonyme'` plutôt que `'non renseigné'` : on distingue « effacé à sa demande » de « jamais connu ». Le pays est forcé à `'FR'` : `00000` n'est valable qu'au format français (`01`, `ck_client_postal_code_format`).
* **ADR-039, Décision 2 (P13).** Le trigger n'exempte plus le parent et l'enfant sans condition : seulement quand l'enfant est signé à l'échéance du parent. Cela met dans la base la règle « à l'échéance » d'ADR-050 Décision 4.
* **ADR-048 (P23).** Le critère compte les visites `'client'` ; la « visite de repérage » du chasseur (l. 94) est la visite 1 de la règle ci-dessus, sur un bien déjà choisi par le client.

**Conséquences**

* **Codé** : le commentaire de `visit.visitor_type` (migration 22) et P3 (migration 23). Les autres choix « base » et « API » deviennent des tâches.
* **P3, fait le 12/10/2026 :** `NOT NULL` dans `01` et la migration 23, jouées sur `fil_rouge_immobilier` ; le tout-ou-rien et `ck_client_postal_code_needs_country` retirés ; le modèle `Client` de l'API rend les quatre champs obligatoires (422 s'il en manque un) ; tests : champ manquant, `NOT NULL` en SQL, adresse neutre acceptée. Reste : le formulaire de création du client demande l'adresse.
* **P13 :** la version testée de la condition est dans le rapport de vérification (§ 2, P13), avec `COALESCE` et dans les deux sens. Un renouvellement signé **avant** l'échéance sera refusé, conforme à `00_…feature:40`.
* **P12 et P13 :** chacun demande d'abord une contrainte `UNIQUE` sur la table visée.
* **P24 :** comparer à `clock_timestamp()` ou dans l'API, pas à `now()` (même piège que P34).

**Questions ouvertes** 🟡

1. **P18, le nombre d'étages d'une maison.** Les 2 556 biens à importer sont **tous** des maisons, chalets ou châteaux : aucun appartement (`normalised/annonces/annonces.csv`, colonne `type_bien`). La source n'a **aucune colonne** de nombre d'étages, et aucun titre ni description ne le dit (recherche de « plain-pied », « R+1 », « étages », « niveaux » : 0). Ajouter `nb_floors` ferait une colonne **vide partout**, qu'aucune source ne demande. 💡 Proposé : ne pas l'ajouter.
2. ~~**P3 :** l'adresse neutre de l'anonymisation.~~ ✅ Tranchée le 12/10/2026 : `'anonyme'`, `'00000'`, `'anonyme'`, `'FR'` (Sébastien, Discord).

**Sources**

| Affirmation | Source |
|---|---|
| Les 13 choix | Sébastien, réponses à la page à cartes, Discord, 12/10/2026 |
| L'adresse neutre de l'anonymisation | Sébastien, Discord, 12/10/2026 (« j'accepte ta proposition ») |
| Les 18 clients ont adresse, code postal, ville et pays ; tous en France | `fil_rouge_immobilier`, compté le 12/10/2026 : `18\|18\|18\|18\|18`, 0 hors `FR` |
| Le flux des sources est retenu ; la visite du chasseur avant la proposition est écartée | Gabriel, Discord, 12/10/2026 |
| La visite 2 se fait avec le chasseur, et c'est elle qui compte pour la rémunération | Gabriel, Discord, 12/10/2026 |
| Le client choisit les biens à faire visiter par son chasseur ; le chasseur visite les biens choisis | `02_particulier_recherche_et_visites.feature:14-23` ; `Readme.md:99-100` |
| Un bien convient : le client est invité à le visiter | `02_particulier_recherche_et_visites.feature:32-35` ; `Readme.md:101` |
| Seules les visites client jusqu'à l'acte comptent | ADR-048 l. 94 |
| Le chasseur visite après le retour du client | `Readme.md:128-129` ; `05_chasseur_selection_quotidienne_biens.feature:32-35` |
| L'anonymisation vidait l'adresse, avant P3 | `md/adr/adr-049-effacement-compte-desactiver-anonymiser.md:114`, version du commit `a921b4e` |
| Tout ou rien ; trois champs, ou aucun | ADR-043, Décisions 1 et 4 |
| Renouvellement à l'échéance | `00_regles_metier_mandat_remuneration.feature:40` ; ADR-050, Décision 4 |
| Le trigger exempte parent et enfant | ADR-039, Décision 2 ; ADR-050 l. 114 |
| Aucun `CHECK` sur les réglages du taux | ADR-034, Décision 3 |
| Pas de contrainte sur les offres acceptées | ADR-045 l. 141 |
| Les preuves, tests et versions corrigées | `md/journal/2026-10-12-verification-audit-problemes.md` |
| `etage` = étage du logement ; aucun appartement ; aucune colonne d'étages | `normalised/normalised.py:88-93` ; `normalised/annonces/annonces.csv` (2 556 lignes, lu le 12/10/2026) |

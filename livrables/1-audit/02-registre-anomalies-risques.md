# Livrable 1 — registre des anomalies et des risques de l'existant

> Phase 1, BC01 (`SP/Readme.md:222`). Format cible : 1 tableau
> (`SP/documents utiles/GRILLE-EVALUATION.md`).
>
> Reprend la page Confluence « Registre des anomalies — Existant »
> (Sébastien, 17/08/2026), sa traçabilité des 13 remarques du consultant
> (§ 1, gardée telle quelle), et y **ajoute la cotation** probabilité × impact,
> qui n'existait que sur les images de la cartographie.
>
> Chaque chiffre est **recompté le 2026-11-19** sur `fixtures/PgSQL.sql`.
> Date de référence : **25/07/2026**.
>
> **Périmètre** : la phase 1 constate, elle ne corrige pas. L'absence des biens,
> visites, offres, actes et honoraires n'est pas une anomalie de l'existant
> (`fixtures/Readme.md`) : elle est notée comme risque métier (R03), pas comme
> défaut de structure.

## 1. Ce que contient l'existant

| Table | Lignes | Détail mesuré |
|---|---|---|
| `secteurs` | 10 | 7 dans l'Hérault (Montpellier 4, Castelnau-le-Lez, Lattes, Sète), Lyon 2, Nantes 1 ; 2 sans quartier (Castelnau-le-Lez, Lattes) |
| `utilisateurs` | 24 | 6 chasseurs (id 1 à 6), 18 clients (id 7 à 24) |
| `mandats` | 18 | statuts : `actif` 11, `termine` 3, `expire` 2, `suspendu` 2 |

## 2. Le registre coté

Probabilité (P) : 3 = constaté dans les données · 2 = rien ne l'empêche ·
1 = peu probable. Impact (I) : 3 = juridique, financier ou bloquant ·
2 = fonction dégradée · 1 = gêne. Cote = P × I.

| # | Composant | Anomalie ou risque | Preuve mesurée | Origine | P | I | Cote | Priorité |
|---|---|---|---|---|---|---|---|---|
| R01 | `mandats` | **Le statut `actif` est faux** : 6 mandats sur les 11 « actifs » ont dépassé leurs 6 mois | ids 4, 7, 9, 10, 11, 12 ; échus depuis 247, 146, 114, 72, 20 et 5 jours | 📋 C13 | 3 | 3 | **9** | 🟥 absolue |
| R02 | `utilisateurs`, `mandats` | **Un chasseur est enregistré comme client** | mandat 13 : `client_id = 3`, or l'utilisateur 3 (Inès Delacroix) est `chasseur` (`PgSQL.sql:82`, `:153`). Sa ville (Lyon) n'est pas celle du secteur (Montpellier) | 📋 C12 | 3 | 3 | **9** | 🟥 absolue |
| R03 | notaire, armoire | **Les honoraires n'existent nulle part en base** : ni montant, ni date, ni lien avec le mandat | aucune table ni colonne ; le sujet les fait collecter par le notaire (`SP/Readme.md:78`) | 📄 croisée | 3 | 3 | **9** | 🟥 absolue |
| R04 | `mandats` | Ni date de signature, ni date de fin, ni mode de signature : la durée de 6 mois n'est écrite nulle part | colonnes absentes du `CREATE TABLE mandats` | 📋 C8, C9 | 2 | 3 | 6 | 🟨 impérative |
| R05 | `utilisateurs` | Rôles mélangés : colonnes vides par conception | `taux_commission` vide sur les 18 clients, `budget_max` vide sur les 6 chasseurs ; aucun `CHECK` ne l'impose | 📋 C3, C4 | 3 | 2 | 6 | 🟨 impérative |
| R06 | `mandats` | `client_id` et `chasseur_id` visent la même table, sans contrôle du rôle | les deux FK référencent `utilisateurs(id)` ; c'est ce qui laisse passer R02 | 📋 C11 | 2 | 3 | 6 | 🟨 impérative |
| R07 | `mandats` | Critères de recherche en texte libre, sans historique | `description_recherche TEXT` sur les 18 mandats (« T3 Ecusson, budget 320000, 65m2 min… ») | 📋 C10 | 3 | 2 | 6 | 🟨 impérative |
| R08 | `utilisateurs` | Taux de commission fixe, alors que le sujet décrit un barème par tranches, variable dans le temps et par chasseur (`SP/Readme.md:80`) | 5 valeurs : 2,00 ; 2,50 ; 2,75 ; 3,00 ; 3,25 %. Elles ressemblent au taux d'honoraires (3 %) plus qu'à une part de chasseur (30 à 50 %) | 📄 croisée | 3 | 2 | 6 | 🟨 impérative |
| R09 | backend | Le code source du backend est perdu et son développeur absent : personne ne peut faire évoluer le système | `SP/Readme.md:208` | 📄 sujet | 3 | 2 | 6 | 🟨 impérative |
| R10 | armoire | Les documents papier (mandats signés ?) n'ont aucun lien avec la base | `SP/Readme.md:207` ; aucune référence de dossier en base | 🔍 propre | 2 | 3 | 6 | 🟨 impérative |
| R11 | `utilisateurs` | Email sans contrôle de format (seulement `UNIQUE`) | 0 email mal formé sur 24 : le risque n'est pas encore arrivé | 📋 C7 | 1 | 2 | 2 | 🟩 mineure |
| R12 | `utilisateurs` | Téléphone sans format ni indicatif, parfois vide | 3 clients sans téléphone (ids 10, 16, 22) ; les 21 autres en 10 chiffres français, sans indicatif : bloquant à l'international | 📋 C6 | 2 | 2 | 4 | 🟨 impérative |
| R13 | `secteurs` | Code postal en `VARCHAR(10)` sans contrôle | 10 codes, tous à 5 chiffres aujourd'hui | 📋 C1 | 2 | 1 | 2 | 🟩 mineure |
| R14 | `secteurs` | Pas d'unicité sur (ville, quartier) | 0 doublon sur 10 lignes | 📋 C2 | 1 | 2 | 2 | 🟩 mineure |
| R15 | `mandats` | Un seul secteur par mandat : pas de recherche sur plusieurs quartiers | 18 mandats, 1 secteur chacun | 🔍 propre | 1 | 2 | 2 | 🟩 mineure |
| R16 | `utilisateurs` | Données personnelles en clair, sans droits d'accès par rôle | noms, emails, téléphones des 24 personnes | 🔍 propre, RGPD | 2 | 3 | 6 | 🟨 impérative |

Priorité, aux couleurs de la grille d'auto-évaluation de Confluence :
🟥 absolue (cote 7 à 9) · 🟨 impérative (4 à 6) · 🟩 mineure (1 à 3).

Origine : 📋 annotation du consultant (n° de la traçabilité, § 3) ·
🔍 notre relecture du schéma · 📄 confrontation au sujet.

**Comptes** : 🟥 3 priorités absolues (cote 9), 🟨 9 impératives (4 à 6),
🟩 4 mineures (1 à 3) ; **16** au total.

## 3. Traçabilité des remarques du consultant

Reprise de la page Confluence, § 1. Aucune remarque n'est écartée sans motif.

| # | Remarque (citation) | Lieu | Traitement | Ligne du registre |
|---|---|---|---|---|
| C1 | « un code postal en VARCHAR sans le moindre contrôle » | `PgSQL.sql:31` | ✅ retenue | R13 |
| C2 | « aucune contrainte d'unicité sur (ville,quartier) » | `:32` | ✅ retenue | R14 |
| C3 | « clients ET chasseurs dans la MÊME table » | `:55` | ✅ retenue | R05 |
| C4 | « la moitié des colonnes est vide selon les lignes » | `:56-59` | ✅ retenue, mesurée | R05 |
| C5 | « Je n'ose imaginer les requêtes que ça oblige à écrire » | `:59-60` | ⚪ fusionnée : impression, sans code à lire | R05 |
| C6 | « Certains clients n'ont pas de téléphone » | `:88` | 🔶 nuancée : le sujet ne dit pas que le téléphone est obligatoire | R12 |
| C7 | « pas de validation de format d'email » | `:89` | ✅ retenue | R11 |
| C8 | « NI date de signature, NI date de fin, NI mode de signature » | `:113-114` | ✅ retenue | R04 |
| C9 | « Comment savent-ils quand un mandat expire ? » | `:115` | ⚪ fusionnée : conséquence de C8 | R04, R01 |
| C10 | « critères […] noyés dans un champ TEXT » | `:116-118` | ✅ retenue | R07 |
| C11 | « client_id et chasseur_id pointent tous les deux vers "utilisateurs" » | `:119-121` | ✅ retenue | R06 |
| C12 | « Celle-ci me chiffonne : client_id = 3 » | `:148-152` | ✅ retenue, vérifiée | R02 |
| C13 | « combien de mandats "actif" ont dépassé leurs 6 mois ? » | `:172-175` | ✅ chiffrée : 6 | R01 |

## 4. Observations hors registre

- Le client 19 (Nina Girard) n'a aucun mandat : un prospect, pas une anomalie.
  La migration v3 lui rattache le mandat 13 (LOT10, `Fil-Rouge-API/docker/migrations/v2-vers-v3/10_reprise-mandats.sql`).
- Le statut `suspendu` (2 mandats, dont le 16, encore dans ses 6 mois) n'a pas
  d'équivalent dans le sujet, qui ne décrit pas de pause d'un mandat.
  ✅ Tranché en phase 2 : `suspendu` devient `'canceled'` (Q-MIG-13).

## 5. Pistes — indicatives, traitées en phase 2

| Risque | Piste | Où c'est fait aujourd'hui |
|---|---|---|
| R01, R04 | date de signature, mode, fin = signature + 6 mois | `mandate.signature_date`, `chk_mandate_six_months` (LOT4) |
| R02, R05, R06 | une fiche par rôle, FK vers la fiche | tables `client`, `hunter`, `real_estate_manager` ; trigger `check_one_profile_per_user` (PRF6) |
| R03, R08 | vente, honoraires, barème, paiement | `sale`, `parameters_fees`, `commission_scale`, `payment` |
| R07 | critères typés, versionnés | `criteria` (`id_previous_version`) |
| R11 à R13 | contrôles de format | `CHECK` email, téléphone (ADR-007), code postal par pays |
| R16 | droits par rôle, rôle en lecture seule | chantier DRO, `fil_rouge_reader` |

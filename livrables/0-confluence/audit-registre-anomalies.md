> **Copie de Confluence** — page « Registre des anomalies — Existant » (id 15564822, version 13), espace GaSeBeLa1, copiée le 2026-11-19.
> La source qui fait foi reste Confluence : https://laurenceamethyste.atlassian.net/wiki/spaces/GaSeBeLa1/pages/15564822/Registre+des+anomalies+Existant. Les images, schémas draw.io et encadrés ne passent pas dans l'export : ils sont signalés par une ligne « 🖼️ Image ou schéma non copié : <nom ou légende si connue> ».

**Projet :** Chasse immobilière GaSeBeLa — Phase 1, Audit de l'existant

**Sources :** `fixtures/MySQL.sql`, `fixtures/PgSQL.sql`, `Readme.md`

**Date de référence :** 25/07/2026

**Enoncé :** **Périmètre de ce document (important) :** la Phase 1 est un audit — on **constate**, on ne **corrige** pas. Les pistes de solution mentionnées (séparation de tables, contraintes à ajouter...) sont indicatives et seront formalisées dans le modèle cible en **Phase 2**. Ce registre ne doit pas être lu comme un cahier des charges de correction.

Rappel de consigne (Readme fixtures) : les 3 tables de l'existant (`secteurs`, `utilisateurs`, `mandats`) sont **tout le périmètre attendu**. L'absence des tables biens / visites / offres / actes / honoraires **n'est pas une anomalie à documenter ici** : c'est le périmètre volontairement limité de l'existant. Voir note de contexte en fin de document.

## 1. Traçabilité des annotations du consultant

**Objectif :** prouver qu'aucune remarque du consultant n'a été ignorée, et justifier le traitement retenu pour chacune (reprise telle quelle, reformulée, ou écartée avec motif).

| **#** | **Remarque du consultant (citation)** | **Localisation** | **Statut** | **Justification** |
| --- | --- | --- | --- | --- |
| C1 | _« un code postal en VARCHAR sans le moindre contrôle »_ | secteurs.code_postal | ✅ Retenue | Constat vérifiable dans le DDL : aucune contrainte CHECK sur `code_postal` |
| C2 | « aucune contrainte d'unicité sur (ville, quartier) » | secteurs | ✅ Retenue | Constat vérifiable : la table ne porte qu'une PK sur `id`, aucune contrainte UNIQUE composite |
| C3 | « clients ET chasseurs dans la MÊME table, départagés par une colonne "role" » | utilisateurs | ✅ Retenue | Constat structurel vérifiable dans le DDL |
| C4 | _« la moitié des colonnes est vide selon les lignes »_ / _« taux_commission n'a de sens que pour un chasseur, budget_max que pour un client »_ | utilisateurs | ✅ Retenue | Conséquence directe et vérifiée de C3 (NULL par conception, confirmé sur les 24 lignes) |
| C5 | « Je n'ose imaginer les requêtes que ça oblige à écrire côté appli » | utilisateurs | ⚪ Non reprise telle quelle | Impression subjective du consultant, non vérifiable en audit (pas de code applicatif fourni) ; l'impact structurel sous-jacent est déjà couvert par C3/C4 |
| C6 | _« Certains clients n'ont pas de téléphone (NULL) »_ | utilisateurs.telephone | 🔶 Nuancée | Constat exact (3 clients concernés), mais qualifié d'anomalie _à trancher_ plutôt que de défaut certain : rien n'indique dans le Readme que le téléphone doive être obligatoire |
| C7 | « Pas de contrainte, pas de validation de format d'email non plus » | utilisateurs.email | ✅ Retenue _(ajoutée dans cette révision — absente du registre précédent)_ | Constat vérifiable : `email` n'a qu'une contrainte UNIQUE, aucune validation de syntaxe |
| C8 | _« je ne trouve NI date de signature, NI date de fin, NI mode de signature »_ | mandats | ✅ Retenue | Constat vérifiable dans le DDL : ces 3 informations sont absentes des colonnes de `mandats` |
| C9 | « Comment savent-ils quand un mandat expire ? Mystère » | mandats | ⚪ Non reprise séparément | Question rhétorique illustrant l'impact de C8, pas un constat distinct — traité comme conséquence de C8 (cf. §3) |
| C10 | « Les critères de recherche du client sont carrément noyés dans un champ TEXT » | mandats.description_recherche | ✅ Retenue | Constat vérifiable dans le DDL et les données (champ TEXT en langage naturel) |
| C11 | « client_id et chasseur_id pointent tous les deux vers "utilisateurs" sans distinction » | mandats (FK) | ✅ Retenue | Constat vérifiable dans le DDL : les deux FK référencent la même table sans discriminant |
| C12 | _« J'ai d'ailleurs un doute sur au moins une ligne \[...\] Celle-ci me chiffonne : client_id = 3 »_ | mandats, ligne id 13 | ✅ Retenue et vérifiée | Vérifié dans les données : mandat id 13, client_id=3, or l'utilisateur 3 a `role='chasseur'` (Inès Delacroix) — voir §2 |
| C13 | _« combien de mandats "actif" ont en réalité dépassé leurs 6 mois de validité ? »_ | mandats | ✅ Retenue et calculée | Question transformée en constat chiffré : 6 des 11 mandats "actif" ont dépassé 6 mois au 25/07/2026 — voir §3 |

**Aucune remarque du consultant n'a été écartée sans justification.** Les deux seules non reprises comme lignes séparées (C5, C9) sont des commentaires d'ambiance ou des questions rhétoriques redondantes avec un constat déjà tracé ailleurs — elles ne sont pas ignorées, seulement fusionnées.

## 2. Anomalies de structure constatées (audit — sans proposition de correction)

Légende Origine : 📋 Consultant = présent dans les annotations `[consultant]` des fixtures (voir traçabilité §1) · 🔍 Analyse propre = constaté par notre propre relecture du DDL, non mentionné par le consultant · 📄 Analyse croisée = déduit en confrontant le schéma aux règles métier du Readme principal.

### Table `secteurs`

| **Colonne** | **Constat** | **Origine** |
| --- | --- | --- |
| ville | Aucun contrôle sur le type des données (chiffres saisissables sans erreur) | 🔍 Analyse propre |
| quartier | Aucune contrainte d'unicité sur (ville, quartier) → doublons possibles ; aucun contrôle de format | 📋 Consultant (C2) |
| code_postal | VARCHAR(10), aucune contrainte de format ; longueur non justifiée au regard du périmètre actuel (France + DOM-TOM, codes à 5 chiffres) | 📋 Consultant (C1) |

### Table `utilisateurs`

| **Elément** | **Constat** | **Origine** |
| --- | --- | --- |
| Table entière | Rôles mélangés (client/chasseur) dans une même table via une colonne `role` ; entraîne des colonnes NULL par conception (`taux_commission` NULL sur les 18 clients, `budget_max` NULL sur les 6 chasseurs) | 📋 Consultant (C3, C4) |
| - | Aucune contrainte CHECK n'empêche de renseigner `budget_max` sur un chasseur ou `taux_commission` sur un client | 🔍 Analyse propre |
| - | Aucune garantie qu'un identifiant utilisé ailleurs comme "client" ou "chasseur" corresponde réellement au bon rôle (conséquence directe du mélange de rôles) | 🔍 Analyse propre |
| email | Contrainte UNIQUE présente, mais aucune validation de format (syntaxe non vérifiée) | 📋 Consultant (C7) |
| telephone | Aucun contrôle de format ; NULL sur 3 clients (Jean Petit, Sofia Andre, Théo Lambert) — caractère obligatoire ou non non tranché par le Readme | 📋 Consultant (C6) |
| ville | Aucun contrôle de format | 🔍 Analyse propre |
| taux_commission | Stocké comme valeur fixe (DECIMAL) par chasseur, alors que le Readme décrit un barème variable dans le temps, par tranches de montant et par chasseur (dépendant aussi de sa performance) — écart entre modèle de données et règle métier | 📄 Analyse croisée avec le Readme métier |

### Table `mandats`

| **Elément** | **Constat** | **Origine** |
| --- | --- | --- |
| Table entière | Aucune colonne de date de signature, de date de fin, ni de mode de signature | 📋 Consultant (C8) |
| secteur_id | Un seul secteur possible par mandat (pas de recherche multi-secteurs) | 🔍 Analyse propre |
| date_debut | Absence de date de fin ; la durée légale de 6 mois n'est matérialisée nulle part dans le schéma | 📋 Consultant (C8, C9) |
| description_recherche | Critères de recherche en texte libre (TEXT), non structurés ; aucune historisation de leurs évolutions (versions, dates, auteur, motif) | 📋 Consultant (C10) |
| FOREIGN KEY (client_id) REFERENCES utilisateurs(id) | Aucune garantie que la ligne référencée est un client (idem pour `chasseur_id`) | 📋 Consultant (C11) |

### Schéma de l'existant (MLD/MPD — et non MCD : types SQL et clés PK/FK déjà explicites, niveau logique/physique) :

🖼️ Image ou schéma non copié : schéma MLD/MPD de l'existant (1452 × 1765 px)

Ce schéma matérialise visuellement l'anomalie ci-dessus : les relations `client_id` et `chasseur_id` partent toutes les deux de `MANDATS` vers **la même table** `UTILISATEURS`, sans discriminant de rôle — c'est la cause structurelle qui rend possible l'incohérence détaillée au §3.

## 3. Incohérence métier détectée dans les données — ⭐ point signalé par le consultant

Le mandat **id 13** (`client_id = 3`) référence l'utilisateur d'id 3 (**Inès Delacroix**), dont le `role` est **chasseur** et non **client**. Un chasseur ne peut pas être client de son propre métier : soit une erreur de saisie, soit une conséquence de l'absence de contrainte discriminant les FK `client_id` / `chasseur_id` (cf. §2, table `mandats`).

C'est la ligne explicitement visée par l'annotation du consultant (C12 dans la traçabilité ci-dessus) :

« J'ai d'ailleurs un doute sur au moins une ligne ci-dessous (à vérifier) \[...\] Celle-ci me chiffonne : client_id = 3. »

SELECT \* FROM utilisateurs WHERE id=3;

🖼️ Image ou schéma non copié : capture du résultat de la requête (886 × 80 px)

## 4. Anomalie de donnée constatée sur l'ensemble du jeu — mandats "actif" ayant dépassé les 6 mois

Réponse chiffrée à la question du consultant (C13) : en confrontant `date_debut` + 6 mois à la date de référence (25/07/2026), **6 des 11 mandats au statut "actif"** ont en réalité dépassé leur durée légale de validité :

| id (mandat) | client_id | date_debut | Dépassement au 25/07/2026 |
| --- | --- | --- | --- |
| 4 | 10 | 2025-05-20 | oui (largement) |
| 7 | 13 | 2025-09-01 | oui |
| 9 | 15 | 2025-10-02 | oui |
| 10 | 16 | 2025-11-14 | oui |
| 11 | 17 | 2026-01-05 | oui (de peu) |
| 12 | 18 | 2026-01-20 | oui (de peu) |

Ce constat découle directement de C8/C9 : sans `date_fin` matérialisée, le statut `actif` n'a pas de valeur fiable. _Origine : la question est posée par le consultant (C13) ; le calcul chiffré ci-dessus (6 mandats identifiés, tableau détaillé) est notre propre réponse, construite en confrontant les données aux règles métier du Readme._

## Typologie de synthèse

| **Type** | **Exemple dans le registre** |
| --- | --- |
| Anomalie de structure | Rôles mélangés client/chasseur ; FK non discriminantes ; colonnes sans contrôle de format ; email non validé |
| Anomalie de donnée (constat métier) | Mandats "actif" ayant dépassé 6 mois de validité (6 cas chiffrés) |
| Incohérence métier ponctuelle | Mandat id 13 : client_id référençant un chasseur |
| Anomalie fonctionnelle | Critères de recherche non structurés (texte libre) ; barème de commission non variable |

## Pistes de traitement — indicatif, développé en Phase 2

Cette section est volontairement séparée du registre d'audit ci-dessus : elle esquisse les directions de correction, mais leur conception détaillée (MCD/MLD cible, migration.sql) relève de la Phase 2, pas de l'audit.

* Séparer `utilisateurs` en deux tables (`clients` / `chasseurs`) avec clé partagée
* Ajouter `date_fin` (ou la calculer), `date_signature`, `mode_signature` sur les mandats
* Structurer `description_recherche` en critères filtrables, historisés (version, date, auteur, motif)
* Discriminer les FK de `mandats` vers `clients(id)` / `chasseurs(id)` plutôt que vers `utilisateurs(id)`
* Remplacer `taux_commission` fixe par une table `baremes_commission` (tranches, variable dans le temps, par chasseur)
* Ajouter des contraintes de format (email, téléphone, code postal) et d'unicité (ville, quartier)

## Note de contexte — hors registre d'anomalies

Le schéma hérité ne couvre que 3 tables (`secteurs`, `utilisateurs`, `mandats`) : biens, visites, offres, actes notariés, honoraires et barèmes de commission n'existent pas dans l'existant. Ce n'est **pas une anomalie** — le Readme précise explicitement que ce périmètre restreint est volontaire et qu'il revient à l'équipe de concevoir ces tables en Phase 2. Cette absence explique cependant l'impossibilité actuelle de calculer la performance des chasseurs (délai signature → achat, nombre de visites, ventes réussies) : à garder en tête comme motivation du modèle cible, pas comme défaut à corriger sur l'existant.

De même, la présence de données personnelles en clair (`nom`, `email`, `telephone`) n'est pas en soi une anomalie de structure : elle relève de la note RGPD transverse exigée séparément par le Readme (finalité, base légale, durée de conservation, anonymisation avant exposition à une IA).

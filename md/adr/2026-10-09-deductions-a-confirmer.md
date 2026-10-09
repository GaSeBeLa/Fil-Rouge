# Déductions des ADR à confirmer — relecture du 09/10/2026

Relecture des 26 fiches (ADR-024, 027 à 051) plus ADR-052, après les réponses de Sébastien du 09/10/2026.
Méthode : recherche de « déduit » et « déduction » dans `md/adr/adr-0*.md` (140 lignes hors fiches annulées et hors ce qui est déjà confirmé), puis tri à la main.

Ce fichier ne change aucune fiche. Il liste ce qu'il reste à faire confirmer, avec sa source dans le dépôt.

## 1. La liste courte : douze déductions qui changent le comportement ou ce qu'on dit au jury

Légende de la colonne « Réponse » : à remplir par le groupe (Oui, Non, À revoir).

| N° | Fiche | La déduction | Pourquoi elle engage le groupe | Réponse |
|---|---|---|---|---|
| S1 | ADR-027 | « La direction », c'est le rôle `Admin` : il tient aussi la comptabilité et le support. | Aucun 6e rôle. Décide qui voit les paiements (D3). | |
| S2 | ADR-027 | Plus aucune route `DELETE` sur les 20 ressources (« proposition de l'équipe, adoptée avec la fiche »). | Change l'API pour tout le monde. Code non fait. | |
| S3 | ADR-049 | L'effacement passe par une route à part, `POST /users/{id}/anonymize`, réservée à l'`Admin`. Même règle pour un chasseur ou un manager. Ce que rien n'oblige à garder est rendu anonyme tout de suite. | Choix RGPD à défendre à l'oral. Code non fait. | |
| S4 | ADR-050 | Le renouvellement se fait dans l'API, en une transaction : il crée le successeur et passe l'ancien à `'renewed'`. Une vente après la fin du mandat s'enregistre, et c'est le paiement qui est refusé. | Règle métier du mandat. Rien n'est codé. | |
| S5 | ADR-041 | Une demande naît `'confirmed'`. Après un refus du vendeur, la nouvelle offre est une nouvelle ligne. | Cycle de vie de la demande et de l'offre. | |
| S6 | ADR-044 | La demande passe à `'launched'` quand le client signe le mandat. | Déclencheur d'un statut. Pas codé. | |
| S7 | ADR-032 | La règle de rapprochement d'ADR-012 (prix + travaux contre budget + budget de rénovation) est abandonnée : elle ne peut pas se calculer. | Retire une règle de recherche de biens. | |
| S8 | ADR-034 et ADR-030 | Une version de réglages ou une grille d'honoraires déjà utilisée ne se corrige pas : on insère une nouvelle version datée. Les réglages du taux valent pour tous les chasseurs. | Règle de rémunération. Contrôle à coder dans l'API. | |
| S9 | ADR-038 | L'ordre des dates du paiement est vérifié par un `CHECK` (annonce avant virement). La date où l'entreprise reçoit les honoraires n'est pas stockée. | Une migration. Un écart assumé au sujet. | |
| S10 | ADR-045 | Un chasseur-IA a les droits du rôle `'Hunter'`. La réaffectation d'un chasseur reste une limite assumée (report). | Ce qu'on dit sur l'IA au jury. | |
| S11 | ADR-046 et ADR-047 | Les 1 623 biens qui ont une lettre DPE reçoivent `energy_class_scheme = 'FR-DPE-2021'`. `POST /estates` exige un auteur. | Données et API à modifier. | |
| S12 | ADR-051 | Le média d'une note d'avis est une adresse, pas un fichier en base. Le chasseur l'écrit, le client le lit. | Droits à ajouter à la matrice d'ADR-027. | |

## 2. Les micro-décisions techniques

Réglées dans les fiches, elles relèvent de `JOURNAL-DE-DECISIONS.md:13` (« pas pour les micro-décisions »). Pas de vote nécessaire. Un seul oui global suffit.

* ADR-028 : deux clés d'API au départ ; les clés rangées dans `docker/.env` ; un compte désactivé ne se connecte pas.
* ADR-029 : le manager de la demande et celui du chasseur peuvent différer ; pas d'historique des managers.
* ADR-030 : la clé vers la grille d'honoraires est `NOT NULL` ; `commission_scale` ne passe pas en « à partir du ».
* ADR-033 : les termes figés du paiement ; le refus du changement après coup se contrôle dans le service ; `date_calcul` se lit dans `payment.created_at`.
* ADR-034 : les arrondis restent des constantes du code.
* ADR-035 : la note `'payment'` s'écrit au passage à `'paid'`.
* ADR-036 : 422 pour une requête mal formée, 409 pour ce que la base refuse ; pas de `Literal` en Python.
* ADR-040 : 409 avec le message de la règle ; un test d'intégration par règle ; « un compte, un seul profil » dans l'API.
* ADR-042 : `scored_at` date la note.
* ADR-043 : pas de vrai code postal inventé.
* ADR-047 : l'import ne passe pas par l'API.
* ADR-049 : DELETE reste un vrai DELETE ; les colonnes obligatoires reçoivent une valeur neutre.
* ADR-051 : le verbe « Accompanies » au MPD (v8 reçue sur Discord le 08/10/2026).

## 3. Les points déjà prévus pour Jeff

Ils ne sont pas dans cette liste.

* Q-ACC-06, Q-ACC-12 et Q-ACC-13 (ADR-027) : à confirmer par Jeff à la séance de validation (Q-JEF-25).
* D1b (exclusivité par recherche, ADR-039, question ouverte 1) : question envoyée à Jeff le 09/10/2026, réponse attendue.

## 4. Ce qui est déjà confirmé le 09/10/2026

D1a, D2, D3, D4, D5, D6, D7, D8 (acceptée), Q1, Q2 et Q3. Voir les fiches concernées.

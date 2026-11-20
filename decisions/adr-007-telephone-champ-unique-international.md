# ADR-007 : Stockage du numéro de téléphone en un champ unique international (indicatif inclus)

> Copié de Confluence (page 52625481, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 19/08/2026 — décision révisée le 10/09/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte :** Lors de la modélisation de la base de données pour gérer les contacts à l'international, il faut optimiser le stockage et l'exploitation des numéros de téléphone pour faciliter les requêtes statistiques ou le filtrage par pays.

**Options envisagées**

- Option 1 : Un champ unique `VARCHAR(20)`, indicatif international inclus dans le numéro (ex. `+33612345678`).
- Option 2 : Séparation en deux champs distincts typés pour isoler l'indicatif du numéro local.

**Décision :** Option 1 retenue. `phone_number VARCHAR(20) NOT NULL`, indicatif compris dans la valeur stockée.

**Justification :** Cette révision annule la décision initiale (Option 2, colonnes séparées). Deux raisons y conduisent :

- L'argument initial en faveur de la séparation — filtrer par pays sans découper une chaîne — ne tient plus : le pays est déjà capturé nommément par `country_iso` sur les mêmes tables (`Hunter`, `Client`, `RealEstateManager`). Séparer l'indicatif téléphonique devient redondant avec une colonne qui existe déjà, pas complémentaire à elle.
- `VARCHAR(20)` dépasse volontairement la borne stricte de la norme E.164 (15 chiffres + signe `+`, soit 16 caractères maximum) pour couvrir sans casse les formats de saisie moins stricts (espaces, tirets, numéros courts ou atypiques) susceptibles d'apparaître dans les sources agrégées, sans réintroduire un parsing rigide qui échouerait sur une variante régionale non anticipée.

**Conséquences**

- Un seul champ à saisir, valider et afficher : plus besoin de concaténer deux colonnes à chaque lecture (API d'envoi de SMS, affichage), contrairement à ce que l'option 2 imposait.
- Migration : les numéros déjà scindés en `country_code`/`phone_number` (si des données existent dans cet état) doivent être recomposés en une seule valeur avant insertion.
- Le formulaire de saisie doit désormais valider l'ensemble du numéro avec une regex E.164 souple, plutôt que deux champs distincts avec un menu déroulant d'indicatif.

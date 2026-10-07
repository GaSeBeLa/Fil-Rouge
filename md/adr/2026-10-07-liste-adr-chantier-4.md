# Liste des ADR du chantier 4 — 2026-10-07

Chantier 4 « Les ADR » : une fiche par ADR, chacune relue, puis copiée à la
main sur Confluence (`context AI/08-etat.md:56`). Pas encore ouvert.

Rien n'est rédigé ici : c'est la liste, pas les ADR.

## Les ADR prévus — 28 lignes

Source : le pense-bête, `md/questions/questions-a-trancher.md:393-422`.

- **A** · Prix en nombres entiers, bornes du barème incluses
- **B** · Vente perdue : un statut de fin sur le mandat
- **C** · Traçabilité du calcul : figer la note et les entrées
- **D** · Paramètres de rémunération dans une table datée
- **E** · Note recalculée à chaque vente
- **F** · Critères de performance — 🟡 la grille du groupe reste à écrire
- **G** · Validation de l'entrée dans le routeur commun
- **H** · X01 : l'ancienneté et la performance majorent le taux
- **I** · Vente reliée à sa grille d'honoraires (remplace ADR-019)
- **J** · Étapes du paiement, sans facture
- **K** · Paramètres proposés, validés par Jeff
- **L** · Règles du mandat : 6 mois, exclusivité, renouvellement, annulation
- **M** · Règles sur plusieurs tables : dans l'API, testées
- **N** · Localisation sur criteria (remplace ADR-009)
- **O** · Statuts de la demande et de l'offre
- **P** · Journal des notes du chasseur
- **Q** · Grilles d'honoraires « en vigueur à partir du »
- **R** · Adresse client : tout ou rien, « non renseigné »
- **S** · Signature du mandat : le client seul
- **T** · Limites assumées du MVP
- **U** · Données reprises incomplètes
- **V** · Effacement d'un compte : désactiver et rendre anonyme — 🟡 durée X à proposer
- **W** · Biens : import, et saisie à la main
- **Y** · Authentification : outils côté back, mot de passe, clé d'API
- **Z** · Lien chasseur → manager (remplace ADR-025)
- **AA** · Droits par rôle : mise à jour de la matrice ADR-027 — 🟡 3 réponses à confirmer avec Jeff
- **AB** · Rôle en lecture seule — 🟡 réponse de Jeff sur Discord
- **AC** · Reprise des anciens mandats

La lettre X est sautée : X01 la prend déjà.

## 💡 À ajouter — propositions, rien de tranché

- **ADR-012** : il décrit des budgets sur la table client, de type Numeric ;
  la base v3 les a sur `criteria`, en `INTEGER`
  (`docker/init-v3/01_create_fil_rouge_immobilier.sql:318-327`)
  ➡️ A le remplace.
- **L'euro** (X02, 2026-09-21) : aucun des 27 ADR ne le porte ➡️ dans A.
- **Eircode sans espace** (Q-SCH-12) : ADR-021 et ADR-022, acceptés, l'écrivent
  avec un espace ➡️ un petit ADR qui les amende.
- **ADR-027** : son contexte dit que l'authentification n'est pas faite ;
  elle revient depuis le 2026-10-07 (Q-JEF-14) ➡️ à réécrire (il n'est que
  proposé).
- **ADR-024** : aucune ligne au pense-bête ; sur Confluence, titre « Annulé »
  et phrase « validé par le groupe » ➡️ à finir, avec B dedans.
- **D3** (acte signé après la fin du mandat : pas de paiement, sauf
  renouvellement) : « puis un ADR »
  (`livrables/2-modelisation/09-decisions-a-prendre.md:178`), oublié
  ➡️ dans L.
- **Acte notarié hors périmètre** (dit le 2026-10-02 ; qui l'a décidé n'est
  pas noté, registre `:62`) ➡️ une ligne dans T.
- **Mots de passe** (Argon2 et robustesse) : ADR-016 et ADR-026 sont annulés
  sur Confluence ➡️ un nouvel ADR qui les remplace.

## Confluence, lu le 2026-10-07

- **27 ADR**, de 001 à 027 ; prochain numéro libre : **028**.
- Tous sur une seule page, « Journal de décisions » (id 15466509), modifiée le
  2026-10-07 à 14 h 11.
- Statuts : 21 acceptés, 1 remplacé (004), 1 proposé (027), 4 « annulés »
  (016, 024, 025, 026).
- ⚠️ « Annulé » n'est pas un statut du modèle du prof : proposé, accepté,
  remplacé par (`documents utiles/JOURNAL-DE-DECISIONS.md:22` et `:72`, dans
  le StarterPack BASE).

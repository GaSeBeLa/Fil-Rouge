# Lot de migration (schéma v3) — notes et journal
## Résultat
Une base v2 migrée et une base v3 neuve ont le même schéma (banc IDENTIQUES), et pytest est vert.
## Notes
- LOT1 : diff -r : 1 ligne (en-tête README, 5 lignes de diff) · compose 1 insertion(+), 1 deletion(-) · montage lu : ligne v3 · pytest 123 passed avant et après · init-v2 restant : 5 fichiers justifiés
- LOT2 : banc IDENTIQUES, 499 faits, code 0, 17,8 à 27,4 s · mutant role.mutant : code 1, diff le nomme · contre-épreuve au milieu du CREATE TABLE : IDENTIQUES · script maison choisi · pytest 123 passed
- LOT3 : 6 tests nommés, 6/6 tombent sous leur mutant · is_client_signed : 0 ligne de code (2 commentaires) · banc IDENTIQUES 498 faits · pytest 129 passed · pyright 6 avant, 6 après (sqlmodel absent de l'hôte)
- LOT4 : 5 tests nommés ; mutants CHECK v2 et DROP TRIGGER font tomber leur test (5/5 au total) · 17 mandats repris : 0 violation · banc IDENTIQUES 500 faits · pytest 134 passed · pyright 3 avant, 3 après (sqlmodel absent de l'hôte)
- LOT5 : Paiement : note figée, taux entre 20 et 60 %, choix des dates. Dépend de LOT2.
- LOT6 : Table des paramètres, grilles d'honoraires, journal des notes. Dépend de LOT5.
- LOT7 : Clients et personnel : adresses, téléphones, priorité 1 à 5. Dépend de LOT2.
- LOT8 : Pays, codes postaux, Eircode, secteurs et quartier. Dépend de LOT7.
- LOT9 : Biens : classe énergie, colonne d'auteur. Dépend de LOT8.
- LOT10 : Anciens mandats : échus, Nina Girard, statuts traduits. Dépend de LOT3.
- LOT11 : README, CLAUDE.md, base de dev recréée, message à l'équipe. Dépend de LOT3 à LOT10.
- LOT12 : Rôle en lecture seule, si Jeff a dit oui. Dépend de LOT11.
## Journal
- 2026-10-07 : 2026-10-07 — un seul statut 'lost' pour la vente perdue, hors agence (Q-REM-02) comme par un collègue (Q-REM-14) : tranché à LOT3
- 2026-10-07 : 2026-10-07 — trigger d'exclusivité : couple parent-enfant exclu dans les deux sens, mandat annulé ignoré (LOT4)
## Bilan

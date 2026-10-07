# Lot de migration (schéma v3) — notes et journal
## Résultat
Une base v2 migrée et une base v3 neuve ont le même schéma (banc IDENTIQUES), et pytest est vert.
## Notes
- LOT1 : diff -r : 1 ligne (en-tête README, 5 lignes de diff) · compose 1 insertion(+), 1 deletion(-) · montage lu : ligne v3 · pytest 123 passed avant et après · init-v2 restant : 5 fichiers justifiés
- LOT2 : banc IDENTIQUES, 499 faits, code 0, 17,8 à 27,4 s · mutant role.mutant : code 1, diff le nomme · contre-épreuve au milieu du CREATE TABLE : IDENTIQUES · script maison choisi · pytest 123 passed
- LOT3 : Statuts de fin du mandat, signature, offre signée. Dépend de LOT2.
- LOT4 : Mandat de 6 mois exacts, trigger d'exclusivité activé. Dépend de LOT3.
- LOT5 : Paiement : note figée, taux entre 20 et 60 %, choix des dates. Dépend de LOT2.
- LOT6 : Table des paramètres, grilles d'honoraires, journal des notes. Dépend de LOT5.
- LOT7 : Clients et personnel : adresses, téléphones, priorité 1 à 5. Dépend de LOT2.
- LOT8 : Pays, codes postaux, Eircode, secteurs et quartier. Dépend de LOT7.
- LOT9 : Biens : classe énergie, colonne d'auteur. Dépend de LOT8.
- LOT10 : Anciens mandats : échus, Nina Girard, statuts traduits. Dépend de LOT3.
- LOT11 : README, CLAUDE.md, base de dev recréée, message à l'équipe. Dépend de LOT3 à LOT10.
- LOT12 : Rôle en lecture seule, si Jeff a dit oui. Dépend de LOT11.
## Journal
## Bilan

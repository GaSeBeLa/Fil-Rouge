# Lot de migration (schéma v3) — notes et journal
## Résultat
Une base v2 migrée et une base v3 neuve ont le même schéma (banc IDENTIQUES), et pytest est vert.
## Notes
- LOT1 : Crée init-v3, copie de v2, et bascule le montage de docker-compose. Ne dépend de rien.
- LOT2 : Le banc qui compare base neuve et base migrée. Dépend de LOT1 ; toutes les fiches s'en servent.
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

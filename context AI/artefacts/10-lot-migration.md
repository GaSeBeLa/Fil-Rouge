# Lot de migration (schéma v3) — notes et journal
## Résultat
Une base v2 migrée et une base v3 neuve ont le même schéma (banc IDENTIQUES), et pytest est vert.
## Notes
- LOT1 : diff -r : 1 ligne (en-tête README, 5 lignes de diff) · compose 1 insertion(+), 1 deletion(-) · montage lu : ligne v3 · pytest 123 passed avant et après · init-v2 restant : 5 fichiers justifiés
- LOT2 : banc IDENTIQUES, 499 faits, code 0, 17,8 à 27,4 s · mutant role.mutant : code 1, diff le nomme · contre-épreuve au milieu du CREATE TABLE : IDENTIQUES · script maison choisi · pytest 123 passed
- LOT3 : 6 tests nommés, 6/6 tombent sous leur mutant · is_client_signed : 0 ligne de code (2 commentaires) · banc IDENTIQUES 498 faits · pytest 129 passed · pyright 6 avant, 6 après (sqlmodel absent de l'hôte)
- LOT4 : 5 tests nommés ; mutants CHECK v2 et DROP TRIGGER font tomber leur test (5/5 au total) · 17 mandats repris : 0 violation · banc IDENTIQUES 500 faits · pytest 134 passed · pyright 3 avant, 3 après (sqlmodel absent de l'hôte)
- LOT5 : 9 tests nommés (11 cas), 7/7 tombent sous leur mutant · grep invoice : 0 ligne · banc IDENTIQUES 507 faits · pytest 145 passed (55 rémunération compris) · pyright 3 avant, 3 après (sqlmodel absent de l'hôte)
- LOT6 : LOT6 : 4 tests nommés + 10 autres cas, 14/14 tombent sous leur mutant (10 refus, 4 accords) · \dt : 19 tables · banc IDENTIQUES 536 faits · pytest 160 passed (55 rémunération compris) · pyright 12 avant, 12 après ; nouveau modèle 3 (sqlmodel absent de l'hôte)
- LOT7 : Tests nommés : 0612345678 refusé, +33612345678 et +33000000000 acceptés (3 tables), priorité 0 et 6 refusées, 1 et 5 acceptées ; 6 mutants, chacun fait tomber ses tests (3, 3, 6, 2, 2, 1 failed). grep is_cartet : 0 ligne. Banc IDENTIQUES — 545 faits ; pytest 173 passed, 0 failed ; pyright 19 errors avant, 19 après (sqlmodel absent de la machine).
- LOT8 : Pays, codes postaux, Eircode, secteurs et quartier. Dépend de LOT7.
- LOT9 : Biens : classe énergie, colonne d'auteur. Dépend de LOT8.
- LOT10 : Anciens mandats : échus, Nina Girard, statuts traduits. Dépend de LOT3.
- LOT11 : README, CLAUDE.md, base de dev recréée, message à l'équipe. Dépend de LOT3 à LOT10.
- LOT12 : Rôle en lecture seule, si Jeff a dit oui. Dépend de LOT11.
## Journal
- 2026-10-07 : 2026-10-07 — un seul statut 'lost' pour la vente perdue, hors agence (Q-REM-02) comme par un collègue (Q-REM-14) : tranché à LOT3
- 2026-10-07 : 2026-10-07 — trigger d'exclusivité : couple parent-enfant exclu dans les deux sens, mandat annulé ignoré (LOT4)
- 2026-10-07 : 2026-10-07 — paiement : statuts 'invoice_submitted' et 'verified' retirés avec la facture ; dates announced_at et scheduled_for gardées (Q-REM-17, LOT5)
- 2026-10-07 : remuneration_parameters versionnée par effective_from + UNIQUE (comme Q-SCH-17) ; bornes relâchées au domaine d'un taux (0 à 1, -1 à 1, RCR:59, 199, 203) — tranché par Sébastien à LOT6
- 2026-10-07 : Téléphone : regex E.164 souple d'ADR-007 lue comme + exigé, 2 à 15 chiffres, un espace ou un tiret entre deux (choix de LOT7) ; client_priority sur estate_proposed (D6).
## Bilan

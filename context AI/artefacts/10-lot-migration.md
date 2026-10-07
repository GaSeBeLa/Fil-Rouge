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
- LOT8 : Recompte : 2 556 codes postaux de biens sur 2 556 à 5 chiffres. Biens 'FR' : 2 556 sur 2 556 sur les deux bases du banc (critères identiques, même md5). Tests nommés : FR 3100 refusé, 31000 accepté ; Eircode D02 X285 refusé, D02X285 accepté (estate, client, criteria) ; 3 mutants, chacun fait tomber ses tests (2, 2, 6 failed). Banc IDENTIQUES — 559 faits ; pytest 181 passed, 0 failed ; pyright 9 errors avant, 9 après (sqlmodel absent de la machine).
- LOT9 : count(energy_class) : 1 623 et energy_class NULL : 933 sur les deux bases du banc (même md5), égaux au recompte du CSV. grep energetic_score : 0 ligne. Test nommé : auteur inconnu refusé (409), auteur connu accepté ; le mutant DROP estate_id_author_fkey fait tomber 1 test, le bon. Banc IDENTIQUES — 561 faits ; pytest 183 passed, 0 failed ; pyright 3 errors avant, 3 après (sqlmodel absent de la machine).
- LOT10 : Sur les deux bases du banc (même md5) : les 6 mandats échus en 'expired' = 6 (8 'expired' au total, avec les 2 'expire' de la source) ; client du mandat 13 = Nina Girard ; demandes en 'launched' = 18, et non 17 : le mandat 13 ajoute la sienne (tranché au questionnaire). Mutant sans l'UPDATE des échus : cmp_v2_migree rend 0. Banc IDENTIQUES — 561 faits ; pytest 183 passed, 0 failed ; aucun Python touché.
- LOT11 : Banc IDENTIQUES — 561 faits ; pytest 183 passed, 0 failed (123 avant le chantier) ; pyright 48 errors sur 23 fichiers, toutes d'environnement (sqlmodel/argon2 absents de la machine) ; docker compose ps : db healthy ; \dt : 19 tables ; registre 31 lignes, 31 au README §0 (Q14 en attente, LOT12)
- LOT12 : Connecté en fil_rouge_reader : SELECT ok (5 rôles), INSERT « permission denied for table role » ; base de dev 19/19 tables lisibles, 0 modifiable ; test_reader_role_cannot_write[insert] tombe sous le mutant GRANT INSERT ; banc IDENTIQUES — 561 faits ; pytest 187 passed, 0 failed ; pyright 4 errors avant, 4 après (sqlmodel absent de la machine)
## Journal
- 2026-10-07 : 2026-10-07 — un seul statut 'lost' pour la vente perdue, hors agence (Q-REM-02) comme par un collègue (Q-REM-14) : tranché à LOT3
- 2026-10-07 : 2026-10-07 — trigger d'exclusivité : couple parent-enfant exclu dans les deux sens, mandat annulé ignoré (LOT4)
- 2026-10-07 : 2026-10-07 — paiement : statuts 'invoice_submitted' et 'verified' retirés avec la facture ; dates announced_at et scheduled_for gardées (Q-REM-17, LOT5)
- 2026-10-07 : remuneration_parameters versionnée par effective_from + UNIQUE (comme Q-SCH-17) ; bornes relâchées au domaine d'un taux (0 à 1, -1 à 1, RCR:59, 199, 203) — tranché par Sébastien à LOT6
- 2026-10-07 : Téléphone : regex E.164 souple d'ADR-007 lue comme + exigé, 2 à 15 chiffres, un espace ou un tiret entre deux (choix de LOT7) ; client_priority sur estate_proposed (D6).
- 2026-10-07 : Eircode avec espace : la migration 08 retire l'espace au lieu de s'arrêter ; sur estate, un code postal sans pays est refusé par le CASE (ELSE FALSE) ; Eircode sans espace aussi sur estate (choix de LOT8).
- 2026-10-07 : Auteur d'un bien : estate.id_author vers user, facultatif (vide = import), clé seule ; le rôle se vérifie dans l'API (questionnaire de LOT9, carte Q-ACC-09).
- 2026-10-07 : Reprise des mandats : demandes 'launched' sous mandat (18) ; échus à la date fixe de l'audit, 25/07/2026 (6) ; Nina Girard reprise avec demande, critère et mandat (questionnaire de LOT10).
## Bilan
- Livré : schéma PostgreSQL v3 (19 tables) dans docker/init-v3/, migrations v2→v3 03 à 12, banc base neuve = base migrée, 187 tests
- Surpris : les données réelles contredisaient souvent la fiche (demandes en confirmed, CRLF, Eircode) : compter avant d'écrire a évité trois erreurs
- Estimé : estimé non noté · cadré 12 · joué 12 fiches 48,04 $

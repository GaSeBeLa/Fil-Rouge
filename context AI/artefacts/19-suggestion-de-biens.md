# Moteur de suggestion de biens et cohérence des propositions — notes et journal
## Résultat
Le chasseur obtient par POST /search-requests/{id}/suggestions jusqu'à 10 biens qui collent aux critères, sans vendus ni déjà vus ; le client ne réécrit plus que sa note, fait son offre par une route dédiée, et un mandat ne se signe plus sans critères.
## Notes
- SUG1 : Rouge : client met accepted, 200 ; vert : 403, ligne intacte ; mutant retombe ; suite 1012 passed, 7 xfailed
- SUG2 : Rouge : signature sans critères 201 (POST), 200 (PUT) ; vert : 409 ; mutant retombe (2 tests) ; seeds passent sur base jetable ; suite 1016 passed, 7 xfailed
- SUG3 : Rouge : 7 failed ; vert : dépôt crée 1 criteria (budget, type, auteur), budget nul ou type inconnu 422 ; mutant retombe (2 tests) ; suite 1024 passed, 7 xfailed
- SUG4 : Rouge : 4 failed ; vert : statut hors liste 409, suggested/dismissed 409, kept 201 ; mutant retombe (2 tests) ; banc v2/v3 IDENTIQUE ; suite 1029 passed, 7 xfailed
- SUG5 : Rouge : 7 failed ; vert : 3 CHECK refusés puis acceptés, client décide par PUT ; mutant (CHECK de Gabriel) retombe ; banc v2/v3 IDENTIQUE ; seeds OK ; suite 1039 passed, 7 xfailed
- SUG6 : Rouge : 6 failed ; vert : offre 200 (4 champs), autre client 404, 2e offre 409, chasseur 403, montant nul 422 ; mutant retombe ; suite 1045 passed, 7 xfailed
- SUG7 : Rouge : module absent ; vert : 16 passed ; mutant lte→gte retombe (2 tests) ; pyright 0 erreur ; suite 1061 passed, 7 xfailed
- SUG8 : Rouge : 8 failed (route absente) ; vert : 9 passed, suggested au nom du chasseur, 10 au plus, vendu et écarté exclus, 404/403/409/503 ; mutant retombe ; route dans openapi ; suite 1070 passed, 7 xfailed
## Journal
- 2026-11-03 : SUG2 : les seeds refusent d'écrire dans `fil_rouge_test` (`seed_demo.py:498`), et cette base n'a pas les biens (`create_test_db.sh` ne charge pas `03_populate_estate.sql`) ; le critère « seeds sur fil_rouge_test » s'est vérifié sur une base jetable `fil_rouge_sug2` montée par `init-v3/01` à `06`, puis supprimée : `seed_demo` passe, `seed_volume --sales 100` passe, 119 mandats signés, 0 sans critères. Les seeds n'ont pas eu à changer : ils posent déjà des critères avant de signer. `MandateService` prend un 3ᵉ argument, `CriteriaRepository`.
## Bilan
- Livré : Moteur de suggestion POST /search-requests/{id}/suggestions (10 biens max, sans vendus ni déjà vus), état de la sélection, décision et offre du client, mandat refusé sans critères
- Surpris : Les seeds refusent fil_rouge_test, vérifiés sur une base jetable ; le compte des routes à part de la matrice était resté à 7 (10 en vrai)
- Estimé : estimé non noté · cadré 8 · joué 8 fiches 25,63 $

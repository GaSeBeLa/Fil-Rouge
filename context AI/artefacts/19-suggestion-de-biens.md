# Moteur de suggestion de biens et cohérence des propositions — notes et journal
## Résultat
Le chasseur obtient par POST /search-requests/{id}/suggestions jusqu'à 10 biens qui collent aux critères, sans vendus ni déjà vus ; le client ne réécrit plus que sa note, fait son offre par une route dédiée, et un mandat ne se signe plus sans critères.
## Notes
- SUG1 : Rouge : client met accepted, 200 ; vert : 403, ligne intacte ; mutant retombe ; suite 1012 passed, 7 xfailed
- SUG2 : Rouge : signature sans critères 201 (POST), 200 (PUT) ; vert : 409 ; mutant retombe (2 tests) ; seeds passent sur base jetable ; suite 1016 passed, 7 xfailed
- SUG3 : Budget et type de bien dans le dépôt de demande, qui crée la 1re version des critères. Dépend de rien.
- SUG4 : Colonne status dans la sélection (suggested, kept, dismissed) ; P19 renforcée. Dépend de rien.
- SUG5 : Décision du client sur un bien proposé, sa date, son motif et les CHECK de Gabriel. Dépend de rien, après SUG4.
- SUG6 : Route POST /estate-proposed/{id}/offer. Dépend de SUG1 et SUG5.
- SUG7 : Fonction pure : critères vers requête Elasticsearch, testée sans ES. Dépend de rien.
- SUG8 : Route POST /search-requests/{id}/suggestions. Dépend de SUG4 et SUG7.
## Journal
- 2026-11-03 : SUG2 : les seeds refusent d'écrire dans `fil_rouge_test` (`seed_demo.py:498`), et cette base n'a pas les biens (`create_test_db.sh` ne charge pas `03_populate_estate.sql`) ; le critère « seeds sur fil_rouge_test » s'est vérifié sur une base jetable `fil_rouge_sug2` montée par `init-v3/01` à `06`, puis supprimée : `seed_demo` passe, `seed_volume --sales 100` passe, 119 mandats signés, 0 sans critères. Les seeds n'ont pas eu à changer : ils posent déjà des critères avant de signer. `MandateService` prend un 3ᵉ argument, `CriteriaRepository`.
## Bilan

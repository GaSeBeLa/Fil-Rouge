# Seed de démo — notes et journal
## Résultat
Une commande remplit la base de dev avec un parcours complet (demande, mandat, biens proposés, visites, vente, paiement, note, avis) et 4 comptes de démo activés, un par rôle : le Swagger et la soutenance ont de quoi montrer.
## Notes
- DEM1 : test_seed_demo.py : 6 passed ; suite 933 passed, 8 skipped, 6 xfailed ; pyright 0 error ; mutant sans contrôle « déjà semé » : 1 failed (test_second_seed_writes_nothing)
- DEM2 : test_seed_demo.py : 10 passed (demande launched, 3 sélections, 3 propositions, 3 visites, le client ne voit que les siennes) ; suite 937 passed, 8 skipped, 6 xfailed ; pyright 0 error ; mutant sans visites : 2 failed
- DEM3 : test_seed_demo.py : 13 passed ; base de dev : estate_proposed 3, estate_searchrequest 3, visit 3, sale 1, payment 1 (paid, 3242.05), hunter_performance 1, review_media 1 ; suite 941 passed, 8 skipped, 6 xfailed ; pyright 0 error ; mutant montant constant : 1 failed
## Journal
- 2026-10-14 : DEM1 : les comptes de démo sont en @example.com (RFC 2606), pas en .invalid comme le disait la fiche : UserCreate (email-validator) refuse les noms à usage spécial (.invalid, .test, .local) ; DEM2 et DEM3 gardent example.com.
- 2026-10-14 : DEM3 : bug trouvé par le seed, corrigé à part sur choix A de Seb (Fil-Rouge-API 7e40e8d) : build_vente cherchait le chasseur par hunter.id au lieu de id_user, invisible sur les 6 chasseurs de 02 (id = id_user), 404 au paiement pour tout chasseur neuf. Et : review_media n'est ajouté que par le chasseur auteur de la note (ADR-051) ; l'avis de démo est donc sa note et son média, pas un avis du client.
## Bilan
- Livré : Seed de démo : seed_demo.py remplit la base de dev par les services (4 comptes, demande, mandat, propositions, visites, vente, paiement payé, note, avis), testé sur fil_rouge_test
- Surpris : le seed a révélé un bug de l'API (chasseur cherché par hunter.id au lieu de id_user, 404 au paiement d'un chasseur neuf), corrigé à part ; .invalid refusé par UserCreate ; avis réservé au chasseur (ADR-051)
- Estimé : estimé 6 fiches ≈29 $ · cadré 3 · joué 3 fiches 13,66 $

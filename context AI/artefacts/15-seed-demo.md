# Seed de démo — notes et journal
## Résultat
Une commande remplit la base de dev avec un parcours complet (demande, mandat, biens proposés, visites, vente, paiement, note, avis) et 4 comptes de démo activés, un par rôle : le Swagger et la soutenance ont de quoi montrer.
## Notes
- DEM1 : test_seed_demo.py : 6 passed ; suite 933 passed, 8 skipped, 6 xfailed ; pyright 0 error ; mutant sans contrôle « déjà semé » : 1 failed (test_second_seed_writes_nothing)
- DEM2 : Demande, mandat signé, biens proposés et visites ; dépend de DEM1
- DEM3 : Vente, paiement calculé, note du chasseur, avis, README et petit ADR ; dépend de DEM2
## Journal
- 2026-10-14 : DEM1 : les comptes de démo sont en @example.com (RFC 2606), pas en .invalid comme le disait la fiche : UserCreate (email-validator) refuse les noms à usage spécial (.invalid, .test, .local) ; DEM2 et DEM3 gardent example.com.
## Bilan

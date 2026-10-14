# Seed de démo — notes et journal
## Résultat
Une commande remplit la base de dev avec un parcours complet (demande, mandat, biens proposés, visites, vente, paiement, note, avis) et 4 comptes de démo activés, un par rôle : le Swagger et la soutenance ont de quoi montrer.
## Notes
- DEM1 : Le script seed_demo.py, faker, DEMO_PASSWORD, et les 4 comptes de démo ; ne dépend de rien
- DEM2 : Demande, mandat signé, biens proposés et visites ; dépend de DEM1
- DEM3 : Vente, paiement calculé, note du chasseur, avis, README et petit ADR ; dépend de DEM2
## Journal
## Bilan

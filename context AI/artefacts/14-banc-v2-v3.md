# Réparer le banc v2/v3 — notes et journal
## Résultat
Le banc base neuve = base migrée rend IDENTIQUES, et il tourne à chaque pytest : un écart casse les tests au lieu de passer inaperçu.
## Notes
- BAN1 : compare_v2_v3.sh : IDENTIQUES, exit 0, 617 faits. Mutant sans 44 : DIFFÉRENTES, exit 1, nomme commission_scale 0/5. Mutant sans liste de démo : exit 1, nomme estate_contact 0/2469. pytest 926 passed, 8 skipped, 6 xfailed
- BAN2 : psql 17.11 ; /api/sql/v2-vers-v3 : 41 .sql dans le conteneur, 41 sur l'hôte (40 avant BAN1) ; 0 .env sous /api/sql ; image 227 MB -> 286 MB ; pytest 926 passed, 8 skipped, 6 xfailed
- BAN3 : Le banc devient un test pytest, le script se réduit à le lancer. Attend BAN1 et BAN2.
## Journal
## Bilan

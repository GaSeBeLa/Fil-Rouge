# Réparer le banc v2/v3 — notes et journal
## Résultat
Le banc base neuve = base migrée rend IDENTIQUES, et il tourne à chaque pytest : un écart casse les tests au lieu de passer inaperçu.
## Notes
- BAN1 : Migration 44 pour les 7 lignes de paramètres ; le banc ne compte plus les contacts de démo. Ne dépend de rien.
- BAN2 : Le conteneur api reçoit psql et voit les fichiers SQL, en lecture seule. Ne dépend de rien.
- BAN3 : Le banc devient un test pytest, le script se réduit à le lancer. Attend BAN1 et BAN2.
## Journal
## Bilan

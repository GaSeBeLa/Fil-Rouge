# Réparer le banc v2/v3 — notes et journal
## Résultat
Le banc base neuve = base migrée rend IDENTIQUES, et il tourne à chaque pytest : un écart casse les tests au lieu de passer inaperçu.
## Notes
- BAN1 : compare_v2_v3.sh : IDENTIQUES, exit 0, 617 faits. Mutant sans 44 : DIFFÉRENTES, exit 1, nomme commission_scale 0/5. Mutant sans liste de démo : exit 1, nomme estate_contact 0/2469. pytest 926 passed, 8 skipped, 6 xfailed
- BAN2 : psql 17.11 ; /api/sql/v2-vers-v3 : 41 .sql dans le conteneur, 41 sur l'hôte (40 avant BAN1) ; 0 .env sous /api/sql ; image 227 MB -> 286 MB ; pytest 926 passed, 8 skipped, 6 xfailed
- BAN3 : test_banc_v2_v3.py : 1 passed en 9,15 s ; mutant (6e ligne de barème dans une copie de init-v3) : 1 failed, diff commission_scale 5/6 ; suite 926 -> 927 passed, 8 skipped, 6 xfailed, 62 s -> 72 s ; fil_rouge_reader noté puis remis (choix A)
## Journal
- 2026-10-14 : BAN3 : le test note l'état de fil_rouge_reader (login, empreinte du mot de passe) et le remet à la fin : init-v3/04 et migrations/12 le passent en NOLOGIN sans POSTGRES_READER_PASSWORD, absent du conteneur api (choix A de Sébastien, 14/10)
## Bilan
- Livré : banc v2/v3 IDENTIQUES (migration 44 des paramètres, contacts de démo non comptés) et devenu un test pytest lancé à chaque suite (psql et fichiers SQL dans le conteneur api)
- Surpris : le compte fil_rouge_reader est commun au serveur : rejouer init-v3/04 depuis api le passait en NOLOGIN ; le test note et remet son état
- Estimé : estimé non noté · cadré 3 · joué 3 fiches 8,03 $

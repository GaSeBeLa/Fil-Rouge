# Droits : moindre privilège — notes et journal
## Résultat
Tout fermé par défaut ; chaque rôle ne lit et n'écrit que ce que la cible d'ADR-027 lui donne, et seulement ses lignes (404 sur la ligne d'un autre).
## Notes
- DRO1 : test_droits_par_role.py 241 passed ; suite 690 passed, 8 skipped, 6 xfailed (avant 443 passed) ; mutant WRITER_ROLES en défaut : 4 failed ; mutant Manager lit /clients : 1 failed ; pyright 2 errors avant et après (crud_router.py, anciennes)
- DRO2 : test_droits_par_role.py 321 passed, dont Client 403 sur POST /commission-scales, GET /payments, POST /sales/{id}/payment et Hunter 403 sur POST /sales ; suite 770 passed, 8 skipped, 6 xfailed (avant 690) ; mutant Client lecteur de payment : 1 failed (/payments-lire-Client) ; pyright 0 errors
## Journal
- 2026-10-13 : DRO1 : POST /users reste à Admin seul (le client crée son compte par /search-requests/submit, Q-ACC-12) ; ouvert au Client, il lui laisserait choisir id_role.
- 2026-10-13 : DRO2 : POST /payments fermé à tous ; les tests écrivent les paiements par le service (write_payment), un refus y est un ConflictError.
## Bilan

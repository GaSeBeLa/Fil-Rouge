# Droits : moindre privilège — notes et journal
## Résultat
Tout fermé par défaut ; chaque rôle ne lit et n'écrit que ce que la cible d'ADR-027 lui donne, et seulement ses lignes (404 sur la ligne d'un autre).
## Notes
- DRO1 : test_droits_par_role.py 241 passed ; suite 690 passed, 8 skipped, 6 xfailed (avant 443 passed) ; mutant WRITER_ROLES en défaut : 4 failed ; mutant Manager lit /clients : 1 failed ; pyright 2 errors avant et après (crud_router.py, anciennes)
- DRO2 : test_droits_par_role.py 321 passed, dont Client 403 sur POST /commission-scales, GET /payments, POST /sales/{id}/payment et Hunter 403 sur POST /sales ; suite 770 passed, 8 skipped, 6 xfailed (avant 690) ; mutant Client lecteur de payment : 1 failed (/payments-lire-Client) ; pyright 0 errors
- DRO3 : test_droits_par_role.py : 7 routes à part nommées avec leur test, /auth/me rend le seul compte du jeton sans password ; suite 774 passed, 8 skipped, 7 xfailed (avant 770 ; +1 xfail strict : fuite du formulaire) ; mutant /auth/me lit l'id de l'URL : 1 failed ; pyright 0 errors
- DRO4 : test_le_sien.py 6 passed : le chasseur 1 liste ses paiements seulement, 404 sur celui du chasseur 2 en lecture, refus au service en modification (le PUT HTTP est à l'Admin, DRO2) ; suite 784 passed, 8 skipped, 7 xfailed (avant 774) ; mutant filtre de payment neutralisé : 3 failed ; pyright 2 errors anciennes ; relecteur indépendant : ACCEPTÉE
## Journal
- 2026-10-13 : DRO1 : POST /users reste à Admin seul (le client crée son compte par /search-requests/submit, Q-ACC-12) ; ouvert au Client, il lui laisserait choisir id_role.
- 2026-10-13 : DRO2 : POST /payments fermé à tous ; les tests écrivent les paiements par le service (write_payment), un refus y est un ConflictError.
- 2026-10-13 : DRO3 : la fuite du formulaire (409 pour un email neuf, 202 pour un connu, si un format est refusé) reste, gardée en xfail strict : la corriger demanderait de recopier en Python les CHECK de la base. À trancher.
- 2026-10-13 : DRO4 : le PUT passe par replace_visible (contrôle « visible », puis replace()). Le PUT de /payments étant à l'Admin (DRO2), son 404 se prouve au service. Relecteur indépendant : ACCEPTÉE.
## Bilan

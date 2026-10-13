# Droits : moindre privilège — notes et journal
## Résultat
Tout fermé par défaut ; chaque rôle ne lit et n'écrit que ce que la cible d'ADR-027 lui donne, et seulement ses lignes (404 sur la ligne d'un autre).
## Notes
- DRO1 : test_droits_par_role.py 241 passed ; suite 690 passed, 8 skipped, 6 xfailed (avant 443 passed) ; mutant WRITER_ROLES en défaut : 4 failed ; mutant Manager lit /clients : 1 failed ; pyright 2 errors avant et après (crud_router.py, anciennes)
## Journal
- 2026-10-13 : DRO1 : POST /users reste à Admin seul (le client crée son compte par /search-requests/submit, Q-ACC-12) ; ouvert au Client, il lui laisserait choisir id_role.
## Bilan

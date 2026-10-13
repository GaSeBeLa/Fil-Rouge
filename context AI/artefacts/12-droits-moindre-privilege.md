# Droits : moindre privilège — notes et journal
## Résultat
Tout fermé par défaut ; chaque rôle ne lit et n'écrit que ce que la cible d'ADR-027 lui donne, et seulement ses lignes (404 sur la ligne d'un autre).
## Notes
- DRO1 : test_droits_par_role.py 241 passed ; suite 690 passed, 8 skipped, 6 xfailed (avant 443 passed) ; mutant WRITER_ROLES en défaut : 4 failed ; mutant Manager lit /clients : 1 failed ; pyright 2 errors avant et après (crud_router.py, anciennes)
- DRO2 : test_droits_par_role.py 321 passed, dont Client 403 sur POST /commission-scales, GET /payments, POST /sales/{id}/payment et Hunter 403 sur POST /sales ; suite 770 passed, 8 skipped, 6 xfailed (avant 690) ; mutant Client lecteur de payment : 1 failed (/payments-lire-Client) ; pyright 0 errors
- DRO3 : test_droits_par_role.py : 7 routes à part nommées avec leur test, /auth/me rend le seul compte du jeton sans password ; suite 774 passed, 8 skipped, 7 xfailed (avant 770 ; +1 xfail strict : fuite du formulaire) ; mutant /auth/me lit l'id de l'URL : 1 failed ; pyright 0 errors
- DRO4 : test_le_sien.py 6 passed : le chasseur 1 liste ses paiements seulement, 404 sur celui du chasseur 2 en lecture, refus au service en modification (le PUT HTTP est à l'Admin, DRO2) ; suite 784 passed, 8 skipped, 7 xfailed (avant 774) ; mutant filtre de payment neutralisé : 3 failed ; pyright 2 errors anciennes ; relecteur indépendant : ACCEPTÉE
- DRO5 : test_le_sien.py 41 passed (35 du Client, 13 tables, deux clients) ; suite 826 passed, 8 skipped, 7 xfailed (avant 784) ; mutants : filtre de mandate retiré 3 failed, _check_owner neutralisé 4 failed, owns de search_request, criteria, estate_proposed 1 failed chacun ; pyright 4 errors avant et après (anciennes) ; relecteur indépendant : ACCEPTÉE
- DRO6 : test_le_sien.py 92 passed (51 du Hunter : chasseurs 1 et 2, 13 tables, 404 sur l'autre ; barème d'un autre 404, barème par défaut visible ; son seul manager) ; suite 876 passed, 8 skipped, 7 xfailed (avant 826) ; mutant filtre de client retiré : test /clients tombe ; 22 mutants + 2 des correctifs attrapés ; pyright 2 errors avant et après (anciennes) ; relecteur : REFUSÉE (champ omis effacé, mandat sur la demande d'un autre), corrigé, puis ACCEPTÉE
- DRO7 : 897 passed, 8 skipped, 7 xfailed (876 avant) ; 2 managers (1 au seed, 1 créé) : chacun son équipe sur 8 tables + paiements, 404 sur l'autre ; mutant payment → 1 failed ; pyright 4 → 4
- DRO8 : 905 passed, 8 skipped, 7 xfailed (897 avant) ; compte désactivé : Reader, Hunter, Manager reçoivent 404 sur son profil (4 tables, 7 cas), Admin le lit ; mutant is_activated retiré → 7 failed ; pyright 2 → 2
## Journal
- 2026-10-13 : DRO1 : POST /users reste à Admin seul (le client crée son compte par /search-requests/submit, Q-ACC-12) ; ouvert au Client, il lui laisserait choisir id_role.
- 2026-10-13 : DRO2 : POST /payments fermé à tous ; les tests écrivent les paiements par le service (write_payment), un refus y est un ConflictError.
- 2026-10-13 : DRO3 : la fuite du formulaire (409 pour un email neuf, 202 pour un connu, si un format est refusé) reste, gardée en xfail strict : la corriger demanderait de recopier en Python les CHECK de la base. À trancher.
- 2026-10-13 : DRO4 : le PUT passe par replace_visible (contrôle « visible », puis replace()). Le PUT de /payments étant à l'Admin (DRO2), son 404 se prouve au service. Relecteur indépendant : ACCEPTÉE.
- 2026-10-13 : Relecture de DRO1 à DRO3 : DRO1 et DRO2 acceptées ; DRO3 refusée pour la fuite du formulaire, question posée à Seb (accepter, resserrer en DRO11, ou reporter).
- 2026-10-13 : DRO5 : hunter filtré aussi (« son chasseur », colonne Client) ; écrire une ligne qui ne serait pas à soi rend 409 (crochet owns) ; rôle et activation : seul un vrai changement rend 403.
- 2026-10-13 : DRO6 : user ouvert au Hunter (son compte) ; mandat gardé à son nom et sur ses demandes (relecteur : sinon il s'ouvrait le client d'un autre ; Q-JEF-30) ; garde des coordonnées sur tout le modèle (un champ omis l'effaçait) ; POST /hunters refermé (create_roles suivait write_roles) ; PUT d'un média : ADR-051 (403) après le 404.
- 2026-10-13 : DRO3 : fuite du formulaire, Seb choisit B ; fiche DRO11 ajoutée avant DRO10 (la base juge les formats dans un SAVEPOINT annulé, même réponse pour tous).
- 2026-10-13 : DRO8 : les 25 comptes du seed sont désactivés (migrés sans mot de passe) ; Seb choisit A : règle telle quelle, seed inchangé, les tests activent ces comptes dans leur transaction. À mettre au rapport du 14/10.
## Bilan

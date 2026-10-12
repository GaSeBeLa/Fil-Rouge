# API : auth, RGPD et règles métier — notes et journal
## Résultat
Les règles des ADR acceptés le 12/10 sont codées et testées : connexion par jeton, rôles, clé d'API, contrôles entre tables, anonymisation sans DELETE, et un paiement calculé depuis la base.
## Notes
- API1 : test_auth : 7 tests verts (200 + jeton ; 401 mauvais mot de passe, inactif, expiré, forgé, désactivé après émission) ; mutant sans contrôle de relecture → 1 failed ; suite 258 passed, 7 skipped (avant 251)
- API2 : test_roles : sans jeton 401, Reader POST 403 / GET 200, POST /hunter-performances 403, Admin POST 201 ; mutant sans contrôle du rôle → 2 failed ; suite 265 passed, 7 skipped (avant 258)
- API3 : test_api_keys : sans clé 401, clé inconnue 401, bonne clé + jeton 200, bonne clé sans jeton 401 ; mutant toute clé acceptée → 2 failed ; suite 274 passed, 7 skipped (avant 265)
- API4 : test_entrees : 18 tests, 422 par règle (P2, P16, P29, P32) et un cas accepté chacune ; mutant sans contrôle des poids → 1 failed ; suite 292 passed, 7 skipped (avant 274)
- API5 : test_versions_paiement : 16 tests (citée 409, non citée 200 ; paid → announced 409 ; taux final faux 409) ; mutants : sans contrôle « déjà citée » → 3 failed, sans ordre du statut → 4 failed, sans P33 → 2 failed ; suite 308 passed, 7 skipped (avant 292)
- API6 : test_auteurs : 11 tests (Hunter et Manager créent, id_author = leur id, valeur envoyée ignorée ; Client, Admin, Reader 403 ; PUT garde l'auteur ; chasseur de la note 201, autre chasseur 403) ; mutants : id_author reçu → 3 failed, PUT sans garde → 1 failed, sans contrôle d'auteur du média → 1 failed ; suite 341 passed, 7 skipped (avant 332)
- API7 : Propositions et visites : P19, P20, P23, P25, visite avant signature
- API8 : Signature → 'launched' ; vente : P27, P28, grille en vigueur
- API9 : Demande enregistrée avant le compte (P5) ; dépend d'API1
- API10 : Anonymisation, 10 ans, plus de DELETE ; dépend d'API2
- API11 : Taux de réussite des mandats pour la note max (mandate_success_rate_for_max_score) = 100 % ; migration 39
- API12 : Paiement calculé depuis la base ; dépend d'API5, API8, API11
## Journal
- 2026-10-12 : API6 : l'auteur de la note (ADR-051) est estate_searchrequest.id_hunter, pas search_request.id_hunter ; seul le POST est restreint, les PUT restent aux rôles qui écrivent
## Bilan

# Refacto des profils — notes et journal
## Résultat
Les 11 FK visent la PK des fiches, le rôle vit sur la fiche ou sur user.system_role, une fiche au plus par compte ; tous les tests passent, banc v2/v3 compris
## Notes
- PRF1 : openapi.json : contenu identique (JSON égal), id affiché après les champs hérités (choix A de Seb) ; mutant gender tué ; 962 passed, 7 xfailed (avant 961) ; pyright 0 erreur sur les fichiers touchés
- PRF2 : 11 FK vers client.id, hunter.id, real_estate_manager.id (01, 02, migration 45) ; 5 FK composées retirées puis recréées ; test_fk_fiches 3 passed ; suite rouge seule, commitée avec PRF3 à PRF5 (choix A de Seb) : 967 passed, 7 xfailed au bout ; coût de PRF2 à PRF5 compté ensemble sur PRF2 (un seul passage)
- PRF3 : Principal.profile_id lu une fois dans get_principal ; branches Client sur client.id ; test_sien_client_fiche passed ; mutants mandates_of et requests_of en user.id tués ; relecture ACCEPTÉE
- PRF4 : hunter_rows, manager_rows, build_vente et seed_demo sur hunter.id ; test_sien_hunter_fiche passed ; mutants handles_mandate et search_request Hunter tués ; 2 oublis (actor.id) révélés par PRF5 et corrigés dans son commit ; relecture ACCEPTÉE
- PRF5 : base de test : id = id_user vaut 0 sur 18 clients, 6 chasseurs, 1 manager (ids à partir de 1001) ; 967 passed, 7 xfailed ; pyright tests 0, src 2 anciennes ; 6 mutants user.id tués ; base de dev effacée et resemée (seed_demo passé) ; relecture ACCEPTÉE
- PRF6 : test_une_fiche_par_compte : 3 passed (2e fiche 409, system_role sur compte à fiche 409, fiche sur compte Reader 409) ; mutant sans triggers : 3 failed ; pytest 970 passed, 7 xfailed (banc v2/v3 compris) ; pyright 2 errors avant / 2 après ; API b3c6d92
- PRF7 : get_principal lit le rôle sur la fiche ou system_role ; dépend de PRF5 et PRF6
- PRF8 : retrait de user.id_role, role à 3 lignes, migration 47 ; dépend de PRF7
- PRF9 : ADR-057, README, matrice des droits, Swagger ; dépend de PRF8
## Journal
- 2026-10-15 : - **2026-10-15** — PRF1 : `id` (propre à chaque fiche) s'affiche après les 7 champs hérités d'`AbstractPerson` dans le Swagger : Pydantic range les champs de la classe mère en tête. Contenu d'`openapi.json` identique, ordre accepté (choix A de Seb, 15/10).
- 2026-10-15 : - **2026-10-15** — PRF2 : il y a **5 FK composées** (pas 4) qui portent les colonnes converties ; la migration 45 les retire puis les recrée. trg_mandate_exclusivity levait U02 par intermittence pendant la conversion de mandate : coupé le temps des 2 UPDATE, puis une requête vérifie qu'aucun exclusif ne chevauche (conseil du Glaude). Commits PRF2 à PRF5 faits ensemble, une fois la suite verte (choix A de Seb).
- 2026-10-15 : - **2026-10-15** — PRF5 : les tests supposaient id = id_user (HUNTER_ID = 1 servait de compte et de fiche) : les comptes restent pour acting_as, les payloads reçoivent hunter_profile() / client_profile(). Le décalage à 1001 a révélé 2 oublis de PRF4 dans le code (estate_search_request_service.create et review_media_service._check_author comparaient user.id à id_hunter), corrigés. Base de dev refaite (down -v, volume minio compris) et seed_demo rejoué.
- 2026-10-15 : PRF6 : system_role s'écrit par l'API (UserCreate, UserUpdate), réservé à l'Admin au PUT (ADMIN_ONLY_FIELDS) ; le 409 du trigger nomme la contrainte one_profile_per_user ; test_constraints_db prend un compte neuf (le compte 1 est un hunter) ; migration 46 jouée sur la base de dev.
## Bilan

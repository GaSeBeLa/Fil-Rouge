# Refacto des profils — notes et journal
## Résultat
Les 11 FK visent la PK des fiches, le rôle vit sur la fiche ou sur user.system_role, une fiche au plus par compte ; tous les tests passent, banc v2/v3 compris
## Notes
- PRF1 : openapi.json : contenu identique (JSON égal), id affiché après les champs hérités (choix A de Seb) ; mutant gender tué ; 962 passed, 7 xfailed (avant 961) ; pyright 0 erreur sur les fichiers touchés
- PRF2 : les 11 FK vers client.id, hunter.id, real_estate_manager.id : 01, 02, migration 45, test d'introspection
- PRF3 : « le sien » du Client compare au numéro de fiche ; dépend de PRF2
- PRF4 : « le sien » du Hunter et du Manager, build_vente, seed ; dépend de PRF2
- PRF5 : base de test aux id ≠ id_user, le filet ; dépend de PRF3 et PRF4
- PRF6 : system_role, role_wording, trigger une fiche au plus, migration 46 ; dépend de PRF2
- PRF7 : get_principal lit le rôle sur la fiche ou system_role ; dépend de PRF5 et PRF6
- PRF8 : retrait de user.id_role, role à 3 lignes, migration 47 ; dépend de PRF7
- PRF9 : ADR-057, README, matrice des droits, Swagger ; dépend de PRF8
## Journal
- 2026-10-15 : - **2026-10-15** — PRF1 : `id` (propre à chaque fiche) s'affiche après les 7 champs hérités d'`AbstractPerson` dans le Swagger : Pydantic range les champs de la classe mère en tête. Contenu d'`openapi.json` identique, ordre accepté (choix A de Seb, 15/10).
## Bilan

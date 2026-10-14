# Finitions de l'API : erreurs et Swagger — notes et journal
## Résultat
Un 409 qui nomme la règle refusée sans recopier la valeur, un 500 neutre avec un numéro retrouvable dans les logs, et la phrase « numéro du compte (user.id) » sous les id du Swagger
## Notes
- FIN1 : test_erreurs_api.py 3 passed ; suite 924 passed, 8 skipped, 6 xfailed (avant 911) ; pyright 2 errors avant = 2 après (crud_router, anciennes) ; 2 mutants tombent ; API b4ab3ce
- FIN2 : test_openapi_ids.py 1 passed (20 champs, 16 schémas, tous user.id) ; suite 925 passed, 8 skipped, 6 xfailed ; pyright 0 errors (13 fichiers) ; mutant Mandate.id_client tombe ; API a5ed572
## Journal
## Bilan
- Livré : 409 qui nomme la contrainte sans la valeur refusée, 500 neutre avec référence dans le log, « numéro du compte (user.id) » sous les id du Swagger
- Surpris : Admin ne crée pas de demande de recherche (403) ; le Swagger porte 20 id de compte (16 schémas), pas 8 ; les 18 demandes de dev sont 'launched', pas 'confirmed'
- Estimé : estimé 4 fiches ≈20 $ · cadré 2 · joué 2 fiches 8,10 $

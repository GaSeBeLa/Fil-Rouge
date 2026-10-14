# Finitions de l'API : erreurs et Swagger — notes et journal
## Résultat
Un 409 qui nomme la règle refusée sans recopier la valeur, un 500 neutre avec un numéro retrouvable dans les logs, et la phrase « numéro du compte (user.id) » sous les id du Swagger
## Notes
- FIN1 : test_erreurs_api.py 3 passed ; suite 924 passed, 8 skipped, 6 xfailed (avant 911) ; pyright 2 errors avant = 2 après (crud_router, anciennes) ; 2 mutants tombent ; API b4ab3ce
- FIN2 : la phrase « numéro du compte (user.id) » sous id_client, id_hunter, id_realestatemanager, id_author, et le commentaire de status corrigé ; ne dépend de rien
## Journal
## Bilan

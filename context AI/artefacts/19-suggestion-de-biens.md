# Moteur de suggestion de biens et cohérence des propositions — notes et journal
## Résultat
Le chasseur obtient par POST /search-requests/{id}/suggestions jusqu'à 10 biens qui collent aux critères, sans vendus ni déjà vus ; le client ne réécrit plus que sa note, fait son offre par une route dédiée, et un mandat ne se signe plus sans critères.
## Notes
- SUG1 : PUT du client limité à client_priority et comment_client, sinon 403. Dépend de rien.
- SUG2 : 409 à la signature d'un mandat sans critères. Dépend de rien.
- SUG3 : Budget et type de bien dans le dépôt de demande, qui crée la 1re version des critères. Dépend de rien.
- SUG4 : Colonne status dans la sélection (suggested, kept, dismissed) ; P19 renforcée. Dépend de rien.
- SUG5 : Décision du client sur un bien proposé, sa date, son motif et les CHECK de Gabriel. Dépend de rien, après SUG4.
- SUG6 : Route POST /estate-proposed/{id}/offer. Dépend de SUG1 et SUG5.
- SUG7 : Fonction pure : critères vers requête Elasticsearch, testée sans ES. Dépend de rien.
- SUG8 : Route POST /search-requests/{id}/suggestions. Dépend de SUG4 et SUG7.
## Journal
## Bilan

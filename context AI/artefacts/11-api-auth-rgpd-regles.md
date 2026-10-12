# API : auth, RGPD et règles métier — notes et journal
## Résultat
Les règles des ADR acceptés le 12/10 sont codées et testées : connexion par jeton, rôles, clé d'API, contrôles entre tables, anonymisation sans DELETE, et un paiement calculé depuis la base.
## Notes
- API1 : Connexion et jeton JWT de 60 min ; arrêt pour le secret dans docker-compose
- API2 : Rôles sur toutes les routes, Reader en lecture seule ; dépend d'API1
- API3 : Une clé d'API par programme ; arrêt pour docker-compose ; dépend d'API1
- API4 : EmailStr, chambres ≤ pièces, réglages cohérents, trace du calcul typée
- API5 : Barème et grilles figés une fois cités ; ordre du paiement ; taux recalculé
- API6 : Auteur d'un bien et d'un média ; dépend d'API2
- API7 : Propositions et visites : P19, P20, P23, P25, visite avant signature
- API8 : Signature → 'launched' ; vente : P27, P28, grille en vigueur
- API9 : Demande enregistrée avant le compte (P5) ; dépend d'API1
- API10 : Anonymisation, 10 ans, plus de DELETE ; dépend d'API2
- API11 : Taux de réussite des mandats pour la note max (mandate_success_rate_for_max_score) = 100 % ; migration 39
- API12 : Paiement calculé depuis la base ; dépend d'API5, API8, API11
## Journal
## Bilan

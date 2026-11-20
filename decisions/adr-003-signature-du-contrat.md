# ADR-003 : Choix Signature du contrat

> Copié de Confluence (page 52135490, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 04/08/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte :** Dans le système d'informations actuel, la date de signature du contrat n'est pas stockée en base de données. Cf. registre des anomalies C8.

**Options envisagées :** Ajouter une attribut `Signature` a table mandat.

**Décision :** Nous choisissons de créer une nouvelle attribut `Signature`:

**Justification :** L'ajout de l'attribut`Signature` permet de garder un historique des signatures de mandat, notamment en cas de renouvellement de celui-ci. D'autre part, avec le système actuel, on ne peut pas savoir si un mandat a bien été signé ou non. On pourra ainsi relancer un client si le mandat n'a pas encore été signé dans un délai imparti choisi par l'agence, par exemple, 2 semaines. La loi n'impose pas de délai légal entre la création d'un mandat et sa signature.

**Conséquences :** Une attribut `Signature` est ajoutée aux schémas MCD fix, MLD fix et MPD fix.

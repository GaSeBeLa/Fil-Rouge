# Problèmes à régler

---

## P1. Une fiche `client` peut être créée pour un utilisateur de rôle Hunter

**Problème** : le schéma ne vérifie pas que `user.id_role` correspond à la fiche (`client`).

**Preuve** : testé sur PostgreSQL 16 (`init-v3/01_create_fil_rouge_immobilier.sql`) : l'insertion passe. Aucun contrôle côté API (code lu, non exécuté).

**Règle visée** : un chasseur qui veut être client crée un compte client distinct *(décision du groupe, aucun scénario)*.

**Pistes** : clé étrangère composite `(id_user, id_role)` (testée), ou trigger (non testé). L'API peut ajouter un message d'erreur clair.

**Non vérifié** : `hunter` et `real_estate_manager`.

**Solution recommandée (API)** : à la création d'une fiche `client`, `hunter` ou `real_estate_manager`, vérifier que le rôle du compte correspond (sinon 409) ; refuser de changer le rôle d'un compte qui a une fiche d'un autre type ; un test d'intégration par cas (exemple de `PLAN-DE-TESTS.md`, l. 47). Limite : un script en SQL direct contourne le contrôle (risque accepté par l'ADR-040).

**Alternative (SQL)** : clé étrangère composite `(id_user, id_role)` vers `user (id, id_role)`, colonne `id_role` figée par `CHECK` dans chaque fiche (testée). Écartée : colonne redondante dans trois tables, dépend des numéros de rôle.

**Statut** : ouvert ; connu du groupe (ADR-040 annexe, A13, « pas codé »). Le plan de tests du starter pack attend le refus (« insérer un client_id qui est un chasseur → refus »).

---

## P2. Email : doublons par la casse et aucun contrôle de format

**Problème** : `user.email` est `UNIQUE`, mais sensible à la casse et sans contrôle de format.

**Preuve** : testé sur PostgreSQL 16 : `Alice@Example.com` et `alice@example.com` acceptés comme deux comptes ; `pas-un-email` accepté.

**Impact** : doublons de comptes ; un chasseur pourrait créer son compte client avec le même email, majuscule changée.

**Non vérifié** : si l'API refuse déjà ces cas avant la base.

**Solution recommandée (SQL)** : `CREATE UNIQUE INDEX uq_user_email_lower ON "user" (lower(email));` et `CHECK (email ~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$')`. Testé : `alice@example.com` refusé après `Alice@Example.com`, `pas-un-email` refusé. Migration (25 emails) : aucun doublon par la casse, non exécutée avec ces contraintes.

**Alternative (API)** : `email: EmailStr` (Pydantic) et passage en minuscules avant l'écriture (aujourd'hui `email: str`, sans contrôle). En second : contournable en SQL direct. Les deux ensemble donnent un message clair et une garantie.

**Statut** : ouvert

---

## P3. Un client peut être enregistré sans aucune adresse

**Problème** : la base accepte un client sans adresse, sans code postal et sans ville (`ck_client_address_all_or_nothing` autorise « rien »).

**Preuve** : testé sur PostgreSQL 16 : fiche `client` créée sans aucune adresse.

**Règle visée** : l'adresse postale du client est obligatoire *(décision de Gabriel, 11/10 ; contredit l'ADR-022, tout-ou-rien, à remplacer par un nouvel ADR si le groupe la retient)*.

**Contexte** : pour les 18 clients repris, la migration a mis des valeurs de remplacement (`'non renseigné'`, `00000`) faute d'information. C'est un choix documenté de migration, pas le problème.

**Solution recommandée (SQL)** : `ALTER TABLE client ALTER COLUMN address SET NOT NULL, ALTER COLUMN postal_code SET NOT NULL, ALTER COLUMN town SET NOT NULL, ALTER COLUMN country_iso SET NOT NULL;` (le pays, car le code postal l'exige). Testé : client sans adresse refusé, avec adresse accepté. Les 18 clients repris ont déjà des valeurs (`02_migration.sql`, l. 155+) : non exécuté avec la contrainte. Conséquence sur P5 : le formulaire devra demander l'adresse.

**Alternative (API)** : champs obligatoires dans le modèle de création du client. En second : contournable en SQL direct.

**Statut** : ouvert

---

## P4. Deux managers possibles pour une même demande

**Problème** : `hunter.id_realestatemanager` (manager du chasseur) et `search_request.id_realestatemanager` (manager de la demande) peuvent désigner deux personnes différentes. Rien ne les relie.

**Preuve** : testé sur PostgreSQL 16 : demande attribuée à un chasseur dont le manager est Marie, avec Paul comme manager de la demande : acceptée.

**Impact** : l'exigence ENF-03 (rémunération lisible par « son manager ») ne dit pas lequel des deux.

**Non vérifié** : si une source dit que les deux doivent coïncider.

**Solution** : aucune modification. Choix assumé par le groupe (ADR-029, l. 90 et 103), déduction encore à confirmer (`md/adr/2026-10-09-deductions-a-confirmer.md`, l. 32). Reste à préciser pour ENF-03 quel manager voit la rémunération (l'ADR-027 donne au manager ses chasseurs et ses demandes).

**Alternative (API)** : à l'affectation du chasseur, vérifier manager de la demande = manager du chasseur. Irait contre l'ADR-029.

**Statut** : choix assumé (ADR-029), à confirmer

---

## P5. Demande enregistrée avant la création du compte

**Problème** : le scénario dit qu'un visiteur soumet le formulaire et que sa demande est enregistrée, le compte venant ensuite. Mais `search_request.id_client` exige déjà un `client` et un `user` (email et mot de passe obligatoires).

**Preuve** : `01_particulier_demande_et_compte.feature` (formulaire, l. 11 à 28), Readme P1-P2, `init-v3` (lu). Aucun ADR lu ne dit comment le compte existe avant.

**Pistes** : A compte inactif créé au formulaire ; B demande gardée dans la base du site ; C `id_client` facultatif. Non tranché.

**Non vérifié** : ADR-028 à 052 (sauf 027) ; si le formulaire envoie la demande à notre API.

**Solution recommandée (API, sans changer le schéma)** : à la soumission du formulaire, en une transaction, créer le `user` (`is_activated = FALSE`, mot de passe factice comme les 24 comptes repris, `security.py` l. 42-44), la fiche `client`, puis la `search_request`. À la finalisation, le client choisit son mot de passe (haché) et `is_activated` passe à `TRUE`. Le formulaire demande email et adresse (P3) ; un email déjà connu retrouve le compte (P2).

**Alternative (SQL)** : `password` facultatif avec `CHECK (is_activated = FALSE OR password IS NOT NULL)`. En second : change le schéma alors que la migration utilise déjà la valeur factice. Écartées : demande gardée dans la base du site (contredit EF-11), `id_client` facultatif.

**Statut** : codé côté API le 12/10/2026 (fiche API9), sans changer le schéma : `POST /search-requests/submit` (clé d'API, pas de jeton), mot de passe factice `PENDING_SIGNUP_PASSWORD` (`security.py`), activation par `PUT /users/{id}`. Un email connu garde sa fiche client telle quelle ; un email de chasseur ou de manager est ignoré et logué. Même réponse pour tous (`202`, sans id), pour ne pas dire si l'email existe (relecture du 12/10/2026) ; seul un formulaire mal formé, refusé par la base, le dit encore (`409` si l'email est neuf). Tests : `API/tests/integration/test_demande_avant_compte.py`.

---

## P6. Une demande « acceptée » peut n'avoir aucun chasseur

**Problème** : `search_request.status = 'accepted'` est la réponse du chasseur, mais `id_hunter` peut rester vide.

**Preuve** : testé sur PostgreSQL 16 : demande `accepted` sans chasseur acceptée. La liste « reste à coder » de l'ADR-041 ne contient pas cette règle.

**Solution recommandée (SQL)** : `CHECK (status = 'confirmed' OR id_hunter IS NOT NULL)`. Testé : `confirmed` sans chasseur accepté ; `accepted` et `launched` sans chasseur refusés. Les 18 demandes reprises sont `confirmed` (ADR-041) : non concernées, non exécuté avec la contrainte.

**Alternative (API)** : vérifier le chasseur au changement de statut. En second : contournable en SQL direct, plus de code.

**Statut** : ouvert

---

## P7. Le statut `confirmed` a deux sens

**Problème** : le scénario `01_` (l. 20) dit « l'affectation d'un chasseur est confirmée », donc un chasseur existe. L'ADR-041 utilise `confirmed` comme état de création, avec `id_hunter` vide.

**Preuve** : lu dans le scénario et l'ADR-041, non testé. Choix confirmé par le groupe le 09/10 (S5).

**Solution recommandée (documentation)** : `COMMENT ON COLUMN search_request.status IS 'confirmed : demande reçue, chasseur pas forcément désigné (id_hunter) ; accepted/rejected : réponse du chasseur ; launched : mandat signé (ADR-041).';`. La règle est décidée (ADR-041 l. 141, S5) ; seul le sens manque, aucun commentaire n'existe aujourd'hui.

**Alternative** : renommer la valeur (ex. `submitted`) : `CHECK`, 18 demandes reprises, API et documents à modifier ; va contre S5.

**Statut** : ouvert

---

## P8. Une version de critères peut pointer vers autre chose que la version d'avant

**Problème** : `criteria.id_previous_version` accepte une version d'une autre demande, une bifurcation, une deuxième version de départ et un lien vers soi-même.

**Preuve** : testé sur PostgreSQL 16 : les quatre cas acceptés. Une version datée avant sa précédente (`created_at` de 2000) est aussi acceptée.

**Règle visée** : une nouvelle version pointe vers celle d'avant, et rien d'autre *(Gabriel ; le Readme l. 234 demande d'historiser les versions)*.

**Piste testée** : clé composite `(id_previous_version, id_search_request)`, `UNIQUE(id_previous_version)`, index unique partiel sur la version de départ, `CHECK (id_previous_version <> id)`.

**Non vérifié** : via l'API (`created_at` y est un champ à valeur par défaut) ; les critères repris par la migration. La règle « date postérieure à la précédente » n'est écrite dans aucune source (hypothèse) ; elle demande un trigger ou l'API, pas un `CHECK`.

**Solution recommandée (SQL)** : `UNIQUE (id, id_search_request)` ; clé étrangère `(id_previous_version, id_search_request)` vers `criteria (id, id_search_request)` ; `UNIQUE (id_previous_version)` ; index unique partiel `(id_search_request) WHERE id_previous_version IS NULL` ; `CHECK (id_previous_version <> id)`. Testées. Aucune colonne ajoutée. 18 critères repris sans version précédente (probablement un par demande, non vérifié). Date : dans l'API, `created_at` fixé par le serveur, jamais reçu du client.

**Alternative (API)** : tout contrôler à la création d'une version. En second : plus de code, contournable en SQL direct.

**Statut** : ouvert

---

## P9. Une nouvelle version de critères peut n'avoir aucun motif

**Problème** : `criteria.change_reason` est facultatif, alors que le Readme (l. 234) demande « date, auteur, motif de chaque changement ».

**Preuve** : testé sur PostgreSQL 16 : versions créées sans motif, acceptées.

**Piste testée** : `CHECK (id_previous_version IS NULL OR change_reason IS NOT NULL)`. Version sans motif refusée, avec motif acceptée.

**Non vérifié** : le code de l'API (le modèle déclare `change_reason` facultatif).

**Solution recommandée (SQL)** : `CHECK (id_previous_version IS NULL OR change_reason IS NOT NULL)`. Testé : version sans motif refusée, avec motif acceptée. Aucune version reprise : pas d'impact.

**Alternative (API)** : motif obligatoire quand `id_previous_version` est fourni. À faire aussi pour un message clair ; seule, contournable en SQL direct.

**Statut** : ouvert

---

## P10. Type de bien et typologie peuvent se contredire

**Problème** : `criteria` accepte un `Terrain` avec la typologie `T3 / F3`, ou un `Studio` avec `T5 / F5`.

**Preuve** : testé sur PostgreSQL 16 : les deux cas acceptés.

**Règle visée** : aucune source ne l'établit (bon sens, hypothèse). Aucun scénario ni ADR lu ne lie `estate_type` à `typology`.

**Piste** : `CHECK` à plusieurs colonnes (non testé).

**Solution** : règle non établie (aucune source ne lie type et typologie). À trancher par le groupe. Si retenue : `CHECK` à plusieurs colonnes dans `criteria` et `estate` (ex. un `Terrain` n'a pas de typologie), non testé. Les 2 556 biens repris n'ont aucune typologie : pas d'impact.

**Alternative (API)** : contrôle à la saisie. En second : contournable en SQL direct.

**Statut** : ouvert

---

## P11. Le commentaire du SQL cite le mauvais ADR pour `ends_at`

**Problème** : le commentaire de `mandate.ends_at` attribue « figer la date » à l'ADR-018. C'est l'ADR-023 (l'ADR-018 porte sur la performance énergétique).

**Preuve** : `01_create_fil_rouge_immobilier.sql` l. 454-455 ; `md/adr/adr-039-regles-du-mandat.md` l. 31-32. Lu, non corrigé.

**Non vérifié** : la page Confluence de l'ADR-023.

**Solution (documentation)** : corriger le commentaire de `mandate.ends_at` : ADR-023 au lieu d'ADR-018.

**Alternative** : aucune.

**Statut** : ouvert

---

## P12. Un mandat peut avoir un autre client ou un autre chasseur que sa demande

**Problème** : `mandate.id_client` et `mandate.id_hunter` ne sont comparés ni au client ni au chasseur de `search_request`.

**Preuve** : testé sur PostgreSQL 16 : mandat du client 1 rattaché à la demande du client 2, et mandat d'un chasseur sur la demande d'un autre : acceptés. API : CRUD générique, service vide (code lu, non exécuté).

**Règle visée** : aucune source ne l'établit (bon sens, hypothèse). Pour le chasseur, la réaffectation est reportée (Q-MAN-08).

**Solution recommandée (SQL), pour le client** : `UNIQUE (id, id_client)` sur `search_request` et clé étrangère `(id_search_request, id_client)` vers `search_request (id, id_client)`. Testé : mandat du client 2 sur la demande du client 1 refusé. Aucune colonne ajoutée. **Pour le chasseur** : règle non établie (réaffectation reportée, Q-MAN-08) ; à trancher, puis API (le chasseur de la demande peut être vide ou changer).

**Alternative (API)** : comparer client et chasseur à la création du mandat. En second : contournable en SQL direct.

**Statut** : ouvert

---

## P13. Le lien de renouvellement contourne l'exclusivité

**Problème** : le trigger exempte le mandat parent et son enfant, sans regarder les dates. Un mandat exclusif d'un autre chasseur, signé en mars, est accepté en plein milieu d'un exclusif (janvier à juillet) s'il est déclaré « renouvellement ». Sans lien de parenté, il est refusé.

**Preuve** : testé sur PostgreSQL 16 (même recherche, même client). Même cas accepté : un mandat du client 2 successeur d'un mandat du client 1 ; un mandat son propre parent.

**Règle visée** : renouvellement « à l'échéance » (`00_`, l. 40) ; exclusivité (`00_`, `@exclusif`). Le contournement existe quelle que soit la réponse à Q3 (par client ou par recherche).

**Non vérifié** : l'API en exécution ; l'ADR-050 est un brouillon.

**Solution, à décider avec le groupe (trigger)** : A) garder le trigger et n'exempter le parent que si l'enfant est signé à son échéance (`NEW.signature_date >= ends_at` du parent), non testé ; B) déplacer la règle dans l'API. **Indépendamment de ce choix (SQL)** : `CHECK (id_mandate_parent <> id)` et clé étrangère `(id_mandate_parent, id_client)` vers `mandate (id, id_client)`. Testés : mandat son propre parent refusé ; parent d'un autre client refusé.

**Alternative** : tout dans l'API (parent, client, échéance). Contournable en SQL direct.

**Statut** : ouvert

---

## P14. Le statut d'un mandat peut contredire sa date de fin

**Problème** : `mandate.status` n'est relié à `ends_at` par aucune règle. L'expiration n'est pas codée (ADR-040 C-e, ADR-046 l. 189) : MAND-0013, 0014 et 0015, finis depuis août et septembre, restent `active`.

**Preuve** : testé sur PostgreSQL 16 : `expired` avec une fin en 2030 accepté ; `active` avec une fin en 2020 accepté. Aucun code d'expiration dans `API/src` (recherche).

**Règle visée** : `expired` seulement après la fin *(déduit de l'ADR-039, non écrit)*. Un `CHECK` ne convient pas (date du jour) : API ou tâche planifiée.

**Solution recommandée (API)** : une tâche planifiée passe à `expired` les mandats `active` dont `ends_at` est dépassée (règle C-e de l'ADR-040, pas codée). Un `CHECK` ne convient pas (date du jour).

**Alternative** : calculer le statut à la lecture (vue) au lieu de le stocker. Change la logique de toute la table.

**Statut** : ouvert

---

## P15. Deux mandats exclusifs qui se chevauchent passent s'ils sont créés en même temps

**Problème** : `trg_mandate_exclusivity` ne voit pas la ligne non validée d'une autre transaction. Deux exclusifs simultanés pour le même client sont tous deux enregistrés.

**Preuve** : testé sur PostgreSQL 16 avec deux sessions : `CC-A` (janv. à juil. 2031) et `CC-B` (mars à sept. 2031) enregistrés. Hors concurrence, le même cas est refusé (`U02`). L'ADR-039 ne parle pas de concurrence ; l'ADR-040 (l. 117) l'écrit « non mesuré » pour l'API seulement.

**Piste testée** : `PERFORM pg_advisory_xact_lock(NEW.id_client);` au début de la fonction. La seconde transaction attend, puis est refusée.

**Non vérifié** : l'impact sur les performances ; les autres triggers.

**Solution, à décider avec le groupe (trigger)** : A) garder le trigger et ajouter `PERFORM pg_advisory_xact_lock(NEW.id_client);` au début (testé : la seconde transaction attend, puis est refusée) ; B) déplacer la règle dans l'API, avec le même verrou dans la transaction (sinon même fenêtre, ADR-040 l. 117).

**Alternative** : aucune sans verrou : la concurrence existe dans les deux cas.

**Statut** : ouvert

---

## P16. 251 biens importés ont plus de chambres que de pièces

**Problème** : 251 des 2 556 biens ont `nb_bedrooms > nb_rooms` (ex. chalet : 1 pièce, 5 chambres ; écart de 1 à 4). Aucune contrainte ne l'empêche.

**Preuve** : `03_populate_estate.sql` chargé dans PostgreSQL 16, requête de contrôle.

**Règle visée** : une chambre est une pièce *(bon sens, aucune source ne définit `nb_rooms`)*.

**Non vérifié** : la définition de `nb_rooms` dans le CSV source. Un `CHECK (nb_bedrooms <= nb_rooms)` ferait échouer ces 251 lignes : nettoyer d'abord.

**Solution** : définition de `nb_rooms` non établie (CSV source) : à trancher. Puis (SQL) `CHECK (nb_bedrooms <= nb_rooms) NOT VALID` : protège les nouveaux biens sans échouer sur les 251 anciens. Testé : contrainte normale refusée par les données ; `NOT VALID` accepté ; nouveau bien 1 pièce / 5 chambres refusé.

**Alternative** : corriger les 251 lignes puis contrainte normale ; ou contrôle API à la saisie seulement.

**Statut** : ouvert

---

## P17. `estate` accepte des biens incohérents (hypothèses)

**Problème** : testé sur PostgreSQL 16, acceptés : latitude sans longitude ; prix absent ou à 0 ; `Terrain` avec typologie `T3 / F3` (même famille que P10) ; classe énergie A avec 900 kWh/m². `EstateService` est vide : le rôle de l'auteur du bien n'est contrôlé nulle part (code lu, non exécuté).

**Règle visée** : aucune source ne les établit (bon sens). Les 2 556 biens importés n'ont aucun prix absent ni coordonnée isolée.

**Solution recommandée (SQL)** : `CHECK ((latitude IS NULL) = (longitude IS NULL))`, testé (latitude seule refusée). Prix, typologie (voir P10) et classe énergie / kWh : règles non établies (seuils DPE hors des sources), à trancher. Rôle de l'auteur : API (A12).

**Alternative (API)** : tous les contrôles à la saisie d'un bien. En second : contournable en SQL direct.

**Statut** : ouvert ; le rôle de l'auteur est connu du groupe (ADR-040 annexe, A12, « pas codé »).

---

## P18. `floor` doit dire combien d'étages possède le bien, mais accepte `last floor`

**Problème** : `last floor` n'est pas un nombre d'étages. La valeur est autorisée dans `estate` et `criteria` (`CHECK`, l. 357 et 584) et présente sur 125 biens importés. Le nom `floor` et l'absence de définition laissent croire à « l'étage de l'appartement ».

**Preuve** : `03_populate_estate.sql` chargé dans PostgreSQL 16, comptage. Aucune définition de `floor` dans les scénarios, le Readme, le glossaire, le SQL ou les ADR (recherche « étage », « floor »).

**Règle visée** : `floor` = nombre d'étages du bien *(décision du groupe, écrite nulle part)*.

**Solution recommandée (SQL + documentation)** : `COMMENT ON COLUMN estate.floor` et `criteria.floor` (« nombre d'étages du bien ») ; retirer `last floor` de la liste du `CHECK` en `NOT VALID`, ou décider d'abord quoi faire des 125 biens repris (valeur inconnue). Non testé.

**Alternative** : renommer en `nb_floors` et passer en entier : plus clair, mais touche la migration, l'API et les documents.

**Statut** : ouvert

---

## P19. Un bien peut être proposé au client sans avoir été sélectionné

**Problème** : `estate_proposed` n'a aucun lien vers `estate_searchrequest`. Un bien jamais sélectionné pour la demande peut être proposé.

**Preuve** : testé sur PostgreSQL 16 : accepté.

**Règle visée** : le chasseur transmet **sa sélection** au client (`05_`, `@transmission-client`).

**Solution recommandée (API)** : à la création d'une proposition, vérifier que le bien est dans la sélection de la demande du mandat (règle entre trois tables).

**Alternative (SQL)** : ajouter `id_estate_searchrequest` dans `estate_proposed` avec clé étrangère. En second : colonne en plus.

**Statut** : ouvert

---

## P20. Un bien peut être proposé sur un mandat annulé

**Problème** : `estate_proposed` accepte un mandat de statut `canceled` (ou `expired`). Rien ne vérifie que le mandat est en cours.

**Preuve** : testé sur PostgreSQL 16 (mandat `canceled`) : accepté. `expired` : déduit, non testé.

**Règle visée** : contexte de `05_` : « un mandat de recherche est signé avec mon client ».

**Solution recommandée (API)** : refuser une proposition si le mandat n'est pas `active` (le statut change dans le temps : pas de contrainte possible).

**Alternative** : aucune simple (trigger écarté).

**Statut** : ouvert

---

## P21. Un mandat peut avoir deux offres signées, alors qu'il n'accepte qu'une vente

**Problème** : `estate_proposed` accepte deux propositions `signed` pour un même mandat, alors que `sale.id_mandate` est `UNIQUE` (une vente par mandat).

**Preuve** : testé sur PostgreSQL 16 : accepté. `UNIQUE` lu dans `sale`.

**Règle visée** : un client qui achète deux biens a deux mandats *(Gabriel ; cohérent avec `sale`, aucune source)*.

**Solution recommandée (SQL)** : `CREATE UNIQUE INDEX uq_proposed_one_signed ON estate_proposed (id_mandate) WHERE proposition_status = 'signed';`. Testé : seconde offre signée sur le même mandat refusée.

**Alternative (API)** : contrôle au passage à `signed`. En second : contournable en SQL direct.

**Statut** : ouvert

---

## P22. Un bien peut être proposé par un autre chasseur que celui du mandat

**Problème** : `estate_proposed.id_hunter` n'est pas comparé à `mandate.id_hunter`. Une proposition rattachée au mandat de Bruno peut indiquer Chloé comme chasseur.

**Preuve** : testé sur PostgreSQL 16 : accepté.

**Règle visée** : un chasseur agit avec **son** mandat, même en non-exclusif (`00_`, l. 30-34 ; Readme l. 76) *(déduit)*. Enjeu : la rémunération va au chasseur à l'origine de la vente (`00_`, l. 34).

**Solution recommandée (SQL)** : `UNIQUE (id, id_hunter)` sur `mandate` et clé étrangère `(id_mandate, id_hunter)` vers `mandate (id, id_hunter)`. Testé : proposition de Chloé sur le mandat de Bruno refusée. Aucune colonne ajoutée.

**Alternative (API)** : comparer à la création. En second : contournable en SQL direct.

**Statut** : ouvert

---

## P23. Un bien peut être visité sans avoir été proposé au client

**Problème** : `visit` n'a aucun lien vers `estate_proposed`. Un bien jamais proposé pour le mandat peut être visité.

**Preuve** : testé sur PostgreSQL 16 : accepté.

**Règle visée** : le client « reçoit des propositions… et choisit les biens à visiter » (Readme, P4, l. 99). Même famille que P19. Nuance : le chasseur peut visiter pour investiguer avant de proposer (`06_`) ; la règle viserait surtout `visitor_type = 'client'` (aucune source ne le précise).

**Solution recommandée (API)** : pour `visitor_type = 'client'`, vérifier que le bien a été proposé sur ce mandat (règle entre tables, ne vise pas les visites d'investigation du chasseur).

**Alternative (SQL)** : ajouter `id_estate_proposed` dans `visit`. En second : colonne en plus, et inadaptée aux visites du chasseur.

**Statut** : ouvert

---

## P24. Une visite prévue ne se distingue pas d'une visite faite

**Problème** : `visit` n'a pas de statut. Une visite datée de 2030 est acceptée, et rien ne dit si elle a eu lieu.

**Preuve** : testé sur PostgreSQL 16 : accepté.

**Enjeu** : le nombre de visites entre dans la rémunération (Readme, l. 88). Une visite prévue ou annulée serait comptée.

**Solution** : règle non établie (enregistre-t-on les visites prévues ?). À trancher. Si non : `CHECK (visit_date <= date du jour)` comme P34. Si oui : colonne de statut (prévue, faite, annulée) et ne compter que les visites faites. Non testé.

**Alternative (API)** : contrôle de la date à l'enregistrement.

**Statut** : ouvert *(hypothèse : aucune source ne dit si l'on enregistre les visites prévues)*

---

## P25. Une visite peut être rattachée à un mandat fini ou annulé

**Problème** : `visit` accepte une date après `mandate.ends_at`, et un mandat `canceled`. Le TODO du SQL ne couvre que la visite **avant** la signature.

**Preuve** : testé sur PostgreSQL 16 : visite de décembre sur un mandat fini en juillet, et visite sur un mandat annulé, toutes deux acceptées.

**Enjeu** : le nombre de visites entre dans la rémunération (Readme, l. 88). Même famille que P20.

**Solution recommandée (API)** : étendre le contrôle déjà prévu « visite avant signature » (Q-MAN-06) : visite pendant la validité du mandat, mandat non annulé.

**Alternative** : aucune simple (dates et statut d'une autre table).

**Statut** : ouvert

---

## P26. Une grille d'honoraires déjà utilisée peut être modifiée

**Problème** : les tarifs changeront. La base accepte un `UPDATE` sur une grille déjà référencée par une vente, au lieu d'imposer une nouvelle ligne datée. Les honoraires stockés ne correspondent alors plus à leur grille.

**Preuve** : testé sur PostgreSQL 16 : 10 500 € stockés contre 17 000 € selon la grille modifiée. Même effet par ajout : une grille antidatée (01/03/2026) insérée après une vente du 01/06/2026 est acceptée ; la règle « dernière grille ≤ date de l'acte » désigne alors une autre grille que celle référencée. Même effet sur `hunter_rate_parameters` : version du 01/03/2026 ajoutée après un paiement qui utilise celle du 01/01/2026, acceptée (testé).

**Règle visée** : « jamais modifier une ligne déjà utilisée par un paiement » (`05_parametres.sql`, commentaire du groupe).

**Pistes** : interdire la modification ; ou figer fixe et pourcentage dans `sale` (même logique qu'ADR-023).

**Solution recommandée** : modification : retirer le droit `UPDATE` et `DELETE` sur `parameters_fees` (et `commission_scale`, `hunter_rate_parameters`) au rôle de l'API, ou contrôle API (A5) ; non testé, suppose que l'API a un rôle dédié (non vérifié). Antidatée : l'API refuse une grille dont `effective_from` précède la dernière vente.

**Alternative (SQL)** : figer fixe et pourcentage dans `sale` (même logique qu'ADR-023) : la preuve ne dépend plus de la grille ; deux colonnes en plus.

**Statut** : ouvert ; connu du groupe pour la modification (ADR-040 annexe, A5, « pas codé »). La grille antidatée n'y figure pas.

---

## P27. Une vente peut porter sur un bien jamais proposé sur ce mandat

**Problème** : `sale` n'a aucun lien vers `estate_proposed`. Une vente est acceptée sur un bien sans proposition ni offre signée pour ce mandat.

**Preuve** : testé sur PostgreSQL 16 : accepté. Absent de l'annexe de l'ADR-040.

**Règle visée** : l'offre est signée avant l'acte (parcours du Readme : offre, acceptation, puis acte authentique) *(déduit)*. Même famille que P19 et P23. Nuance : ne vise que `sale_origin = 'hunter'` ; en `client_alone`, il n'y a pas de proposition.

**Solution recommandée (API)** : pour `sale_origin = 'hunter'`, exiger une offre `signed` sur ce bien et ce mandat.

**Alternative** : aucune simple en SQL : plusieurs offres par bien (ADR-041, l. 149) et l'exception `client_alone`.

**Statut** : ouvert

---

## P28. Le mandat ne passe pas à « terminé » après la vente

**Problème** : après une vente, le mandat garde le statut `active`. Rien ne le fait passer à `completed`.

**Preuve** : testé sur PostgreSQL 16 : mandat toujours `active` après la vente. L'annexe de l'ADR-040 ne prévoit que le passage du mandat **perdant** à `lost` (A11).

**Enjeu** : un mandat `active` bloque encore le client (exclusivité), alors que `completed` le libère (ADR-039, B2).

**Solution recommandée (API)** : à l'enregistrement de la vente, dans la même transaction, passer le mandat à `completed`.

**Alternative** : aucune simple (trigger écarté).

**Statut** : ouvert *(hypothèse : aucune règle écrite ne dit quand `completed` s'applique)*

---

## P29. Les réglages du taux acceptent des valeurs qui cassent le calcul

**Problème** : `hunter_rate_parameters` n'a aucun `CHECK`, même structurel. Acceptés : plancher > plafond, demi-amplitude à 0, poids négatif, fenêtre de 0 mois.

**Preuve** : testé sur PostgreSQL 16. Formule de `remuneration.py` reproduite : demi-amplitude 0 → `DivisionByZero` ; plancher > plafond → plancher ignoré. Somme des poids libre, alors que la fiche pose un score entre 0 et 100 (`REGLES-CALCUL-REMUNERATION.md` l. 75) : déduit. Paliers JSON non contrôlés : structure invalide → `TypeError` (lecture reproduite) ; paliers dans le désordre → mauvaise note sans erreur (`note_par_paliers`, lu). Aussi acceptés (formules lues) : amplitude de performance négative (une meilleure performance baisse la paie), plafond d'ancienneté négatif, notes au-dessus de 100.

**Règle visée** : des contrôles qui ne figent aucune valeur (plancher ≤ plafond, demi-amplitude > 0, poids ≥ 0 et de somme 1, paliers en liste triée), compatibles avec Q-REM-05 *(proposition)*.

**Solution recommandée (SQL)** : `CHECK` structurels : `rate_floor <= rate_ceiling` ; `score_half_range > 0` ; poids ≥ 0 et de somme 1 ; `window_months > 0` ; `jsonb_typeof(delay_tiers) = 'array'` (idem `visit_tiers`) ; amplitude et ancienneté ≥ 0. Testés un par un : chaque cas refusé, version de départ acceptée. Ordre des paliers : API.

**Alternative (API)** : valider la version à sa création (modèle Pydantic). En second : contournable en SQL direct.

**Statut** : ouvert

---

## P30. `payment` fige le plancher et le plafond que les réglages laissent libres

**Problème** : `payment.final_rate` a un `CHECK (final_rate BETWEEN 0.20 AND 0.60)`. `hunter_rate_parameters` refuse de graver ces bornes, pour que le client puisse les changer (Q-REM-05). Si le client les modifie, les paiements calculés avec les nouvelles bornes sont refusés.

**Preuve** : testé sur PostgreSQL 16 : version avec plancher 15 % et plafond 70 % acceptée ; paiement à 65 % refusé (`payment_final_rate_check`).

**Solution recommandée (SQL)** : remplacer le `CHECK` par `final_rate BETWEEN 0 AND 1`. Testé : paiement à 65 % accepté. Le respect des bornes de la version : API (comme A9).

**Alternative** : garder 20-60 % et interdire au client de changer les bornes. Va contre Q-REM-05.

**Statut** : ouvert

---

## P31. Le paramètre `window_months` n'est utilisé par aucun calcul

**Problème** : `window_months` (fenêtre de comptage des ventes et mandats) est lu par l'API, mais aucun calcul ne s'en sert. Le calcul reçoit des compteurs déjà faits, nommés `ventes_12_mois` et `mandats_12_mois`. Changer la fenêtre n'aurait aucun effet.

**Preuve** : lu dans `parametrage_service.py` (l. 109) et `remuneration.py` (l. 105, 139-140, 213-214).

**Règle visée** : « les paramètres sont des données, pas du code » (`REGLES-CALCUL-REMUNERATION.md`, l. 341).

**Non vérifié** : le code qui calculera ces compteurs n'existe pas encore ; il pourrait utiliser la fenêtre.

**Solution recommandée (API)** : le code qui calculera les compteurs de ventes et de mandats utilise `fenetre_mois`.

**Alternative (SQL)** : supprimer `window_months` si la fenêtre est fixée à 12 mois. Va contre « les paramètres sont des données ».

**Statut** : ouvert

---

## P32. Les détails du calcul d'un paiement peuvent être vides

**Problème** : l'ADR-033 (Décision 2) exige que `payment.calculation_details` porte au moins les 5 notes et les 4 entrées du calcul. La base n'exige qu'un JSON non nul : `{}` est accepté.

**Preuve** : testé sur PostgreSQL 16 : paiement avec `{}` accepté. Règle absente de l'annexe de l'ADR-040.

**Solution recommandée (API)** : un modèle Pydantic pour `calculation_details` (5 notes, 4 entrées, ADR-033) : lisible, facile à faire évoluer.

**Alternative (SQL)** : `CHECK (calculation_details ?& array[...])` avec les clés exactes de l'ADR-033. Non testé : les noms des clés restent à recopier.

**Statut** : ouvert

---

## P33. Les taux d'un paiement peuvent se contredire

**Problème** : `payment` accepte un taux final qui ne découle pas des taux stockés (taux de base, ancienneté, performance, bornes). L'ADR-033 ne prévoit de vérifier que le montant (Décision 6). La trace du calcul peut donc ne pas expliquer le taux final.

**Preuve** : testé sur PostgreSQL 16 : taux de base 30 %, ancienneté 0, performance 0, taux final 55 %, accepté. Ancienneté de 50 % acceptée alors que le plafond de la version des réglages est 10 % (testé).

**Règle visée** : taux final = taux de base × (1 + ancienneté + performance), borné (`remuneration.py`, l. 259-264) *(déduit)*.

**Solution recommandée (API)** : recalculer le taux final depuis les taux stockés et la version des réglages, et refuser s'il diffère (complète la Décision 6 de l'ADR-033).

**Alternative** : aucune simple en SQL (les bornes sont dans une autre table).

**Statut** : ouvert

---

## P34. Un paiement « payé » peut avoir une date de paiement dans le futur

**Problème** : `payment` accepte `status = 'paid'` avec `paid_at` en 2099. L'annexe de l'ADR-040 ne liste que l'ordre des dates (l. 81), pas qu'elles ne soient pas dans le futur.

**Preuve** : testé sur PostgreSQL 16 : paiement `paid` daté de 2099 accepté. Aussi accepté : une note de performance (`scored_at`) datée de 2099.

**Règle visée** : un paiement payé a eu lieu *(déduit)*. Même famille que P24.

**Solution recommandée (SQL)** : `CHECK (paid_at IS NULL OR paid_at <= (now() AT TIME ZONE 'utc'))`. Testé : paiement daté de 2099 refusé. Même `CHECK` pour `hunter_performance.scored_at`, non testé. Limite : un `CHECK` avec `now()` n'est vérifié qu'à l'écriture.

**Alternative (API)** : la date de paiement est fixée par le serveur au passage à `paid`.

**Statut** : ouvert

---

## P35. Une note de performance peut être attribuée à un autre chasseur que celui de sa source

**Problème** : `hunter_performance.id_hunter` n'est comparé ni à `payment.id_hunter` ni à `mandate.id_hunter`. Une note `mandate_expired` est aussi acceptée sur un mandat encore `active`.

**Preuve** : testé sur PostgreSQL 16 : note déclenchée par le paiement du chasseur A attribuée au chasseur B, et note `mandate_expired` sur un mandat `active` d'un autre chasseur, toutes deux acceptées. Absent de l'annexe de l'ADR-040 (A14, A17, B8 couvrent l'ordre des notes, pas le chasseur).

**Règle visée** : un paiement ou un mandat échu donne une note **à son chasseur** (ADR-042) *(déduit)*. Même famille que P12 et P22.

**Solution recommandée (SQL)** : `UNIQUE (id, id_hunter)` sur `payment` et `mandate`, clés étrangères `(id_payment, id_hunter)` et `(id_mandate, id_hunter)` depuis `hunter_performance`. Testé : note du paiement de Bruno attribuée à Chloé refusée ; note `mandate_expired` d'un autre chasseur refusée. Aucune colonne ajoutée. Mandat encore `active` : API.

**Alternative (API)** : comparer à l'écriture de la note. En second : contournable en SQL direct.

**Statut** : ouvert

---

## P36. Un chasseur peut avoir plusieurs notes `initial`

**Problème** : `hunter_performance` accepte deux notes `initial` pour le même chasseur. Rien ne dit qu'il n'y en a qu'une.

**Preuve** : testé sur PostgreSQL 16 : deux notes `initial` (50 puis 90) acceptées pour le même chasseur.

**Règle visée** : aucune source ne l'établit *(hypothèse)* : le nom « initial » suggère une seule note de départ.

**Solution** : règle non établie (une seule note `initial` ?). À trancher. Si oui (SQL) : `CREATE UNIQUE INDEX uq_perf_one_initial ON hunter_performance (id_hunter) WHERE trigger_type = 'initial';`, testé (seconde note refusée).

**Alternative (API)** : contrôle à l'écriture.

**Statut** : ouvert

---

## P37. Un bien peut être vendu deux fois

**Problème** : `sale.id_mandate` est `UNIQUE` (une vente par mandat), mais `sale.id_estate` n'a ni `UNIQUE` ni trigger. Le même bien peut donc être vendu deux fois, sur deux mandats différents.

**Preuve** : `docker/init-v3/01_create_fil_rouge_immobilier.sql`, table `sale` ; signalé par Gabriel le 12/10/2026. Testé : deux ventes du même bien sur les mandats 1 et 2, acceptées sans la contrainte.

**Règle visée** : un bien n'est vendu qu'une fois *(décision du groupe, Gabriel, Discord, 12/10/2026)*. Une revente plus tard serait une nouvelle annonce, donc un autre `estate`.

**Solution (SQL)** : `CONSTRAINT uq_sale_estate UNIQUE (id_estate)` dans `01` et la migration 38. 0 vente en base au 12/10/2026 : rien à reprendre. Test : `test_sale_second_sale_of_same_estate_returns_409`.

**Statut** : réglé le 12/10/2026 (ADR-053)

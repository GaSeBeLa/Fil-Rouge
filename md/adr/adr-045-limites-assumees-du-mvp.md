# ADR-045 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 045 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:68`,
> groupe 2). Il réunit la lettre T du pense-bête (`md/questions/questions-a-trancher.md:415`)
> et l'acte notarié hors périmètre, que la liste du chantier 4 range en « une
> ligne dans T » (`md/adr/2026-10-07-liste-adr-chantier-4.md:61-62`).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. L'arbitre a mis la Décision en tableau, et ajouté la limite 7 :
> l'import des annonces, question laissée par ADR-047. Aucune question ne reste
> ouverte.
>
> 🤝 **À faire à la séance de validation des ADR** : Jeff confirme le report
> de Q-SCH-08 et de Q-ACC-14. Ce sont des cartes du PO, et rien n'est noté le
> 07/10 (`md/questions/2026-10-07-questions-pour-jeff.html:379`). Jeff valide
> les ADR en une séance (Q-JEF-25, même fichier, l. 378).
>
> ℹ️ **Acte notarié : d'où vient « annoncé par Sébastien ».** Des notes de
> session de Claude du 02/10/2026, pas d'un fichier du dépôt. Le registre dit
> seulement « annoncé le 2026-10-02 (qui l'a décidé n'est pas noté) » (`:62`).
> Précisé par Sébastien le 2026-10-09 (Discord) : décidé par Jeff.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * `docker/init-v3/01_create_fil_rouge_immobilier.sql:712` dit « Visites
>   (décision D10 […]) ». D10, c'est la table des rendez-vous
>   (`livrables/2-modelisation/09-decisions-a-prendre.md:439-448`). L'erreur était
>   déjà relevée en v2 (registre `:1358`) ; elle est restée en v3.
> * `09-decisions-a-prendre.md:72-74` : D10, D11, D12 « ouverte ». Après cet
>   ADR : D10 fermée (pas de table), D11 et D12 reportées au parcours IA.
> * La fiche Q-ACC-14 (`md/questions/questions-a-trancher.html:1843-1867`) dit
>   « 4 rôles seulement » et « le contrôle d'accès est hors périmètre ». La v3 a
>   5 rôles (`01:163-164`), et l'authentification revient côté back (ADR-028).
>
> ℹ️ **Pas dans cet ADR** :
>
> * Les « Conséquences » d'ADR-039 et d'ADR-050 : du code à écrire, pas des
>   limites (voir « Questions tranchées »).
> * L'expiration d'un mandat fini : le sujet la demande
>   (`07_chasseur_remuneration_et_performance.feature:38-41`, parcours
>   `@actuel`). C'est du code à écrire (ADR-046), pas une limite.
> * Les notifications (Q-JEF-27 à 29) : elles attendent Jeff, rien n'est décidé.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-045 : Limites assumées du MVP — sept sujets écartés, ce qui se passe à leur place, ce qu'on en dit au jury

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions : 02/10/2026 pour l'acte notarié ; 05/10/2026 pour Q-SCH-07, Q-SCH-08, Q-SCH-14 ; 06/10/2026 pour Q-MAN-08 et Q-ACC-14)
* **Statut :** proposé
* **Décideurs :**
  * l'équipe projet, réponses du groupe : Q-SCH-07 « Ne pas créer, hors MVP », Q-SCH-14 « Accepter comme limite », Q-MAN-08 « Reporter » ;
  * cartes du PO, réponse du groupe « Reporter au parcours IA » : Q-SCH-08, Q-ACC-14. Le PO, c'est Jeff (Q-PRO-01) : il les confirme à la séance de validation des ADR (Q-JEF-25) ;
  * acte notarié : annoncé par Sébastien le 02/10/2026. Décidé par Jeff, précisé par Sébastien le 2026-10-09 (Discord) ; le registre ne le note pas encore (`:62`) ;
  * limite 7 : 💡 proposée par cet ADR, le 08/10/2026, puis réécrite le 2026-10-09 : Sébastien dit que le groupe compte importer les annonces par un flux Airflow. Acceptée par le groupe le 2026-10-09 (Sébastien, Discord) ; l'ADR-045 dans son ensemble reste « proposé ».
* **Remplace :** aucun ADR.
* **Complète :** ADR-029, Décision 5 (pas d'historique des managers) : la limite est décidée là-bas ; ici, on dit ce qu'on en dit au jury.
* **Voir aussi :** ADR-044 (seul le client signe le mandat : limite dite là-bas) ; ADR-038 (pas de facture : écart au sujet) ; ADR-047 (biens saisis à la main).

**Contexte**

Le sujet attend des limites dites en soutenance :

* « Reconnaître une limite est une force, pas un aveu. » La partie « Bilan & limites » dure 1 minute (`TRAME-SOUTENANCE.md:22`).
* La trame a une ligne « Limites assumées » (l. 48).
* Le conseil : « nous n'avons pas eu le temps de X, mais voici comment nous l'aurions abordé » (l. 57).

Le sujet dit aussi comment écrire une exclusion. Quatre éléments, « tous nécessaires » (`Gherkin.md:717-724`) :

* l'objet exclu, décidable ;
* le comportement de substitution : « Que fait le système si ça arrive quand même ? » ;
* la raison ;
* le renvoi ou l'échéance.

Le deuxième est « le plus important et le plus oublié » (`Gherkin.md:726`). Le hors-périmètre pur se réduit aux cas où le système « ne peut même pas être sollicité » (`:737`). À bannir : « etc. », « pour l'instant » sans date ni ticket, « on verra plus tard » (`:739-746`).

Entre le 02/10 et le 06/10/2026, six sujets ont été écartés du MVP. Le pense-bête en range cinq sous T : « décidé — à dire en soutenance » (`questions-a-trancher.md:415`). L'acte notarié s'y ajoute (`2026-10-07-liste-adr-chantier-4.md:61-62`). Le 08/10/2026, ADR-047 laisse une question : un import régulier des annonces. Cet ADR la range en septième limite.

**Options envisagées**

A. La forme

1. **Ne rien écrire** : les cartes du registre suffisent. Inconvénient : au jury, on improvise. Sans renvoi, « le besoin disparaît de tous les radars » (`Gherkin.md:724`). **Écartée.**
2. **Un ADR par limite.** Inconvénient : sept ADR pour dire « on ne le fait pas ». Le pense-bête les réunit déjà sous T. **Écartée.**
3. **Un seul ADR** : un tableau d'une ligne par limite, puis le détail, avec les quatre éléments du sujet et la phrase pour le jury. **Retenue** (pense-bête T ; forme de `Gherkin.md:717-724`).

B. Chaque limite (options des cartes)

| Limite | Option écartée, et pourquoi | Option retenue |
|---|---|---|
| 1. Acte notarié | 💡 « Modéliser l'acte » (notaire, pièces, encaissement) : aucun calcul ne le lit (`REGLES-CALCUL-REMUNERATION.md:130`). Option reconstituée à la rédaction : aucune n'est notée | hors périmètre (02/10/2026) |
| 2. Rendez-vous (Q-SCH-07) | « Créer la table » : une table de plus, qu'aucun calcul ne lit | « Ne pas créer, hors MVP » |
| 3. Pertinence, types d'offre (Q-SCH-08) | « Trancher maintenant » : des colonnes à ajouter pour un parcours futur | « Reporter au parcours IA » |
| 4. Historique des managers (Q-SCH-14) | « Historiser » : une table de plus | « Accepter comme limite » |
| 5. Refus d'une demande (Q-MAN-08) | une table `search_request_refusal` (demande, chasseur, date) : rien à brancher tant que l'affectation n'était pas décidée | « Reporter » |
| 6. Droits des chasseurs-IA (Q-ACC-14) | « Maintenant », dans la matrice : « une règle écrite sans savoir ce que fait un chasseur-IA » | « Reporter au parcours IA » |
| 7. Import des annonces | 💡 un seul chargement, sans dédoublonnage : écarté le 2026-10-09, le groupe prévoit un flux | 💡 un import par flux orchestré (Airflow), tri, mise en forme et dédoublonnage en map/reduce. Proposé par Sébastien et accepté par le groupe le 2026-10-09 |

Sources des options : fiches de `md/questions/questions-a-trancher.html`, l. 1204-1220 (Q-SCH-07), 1223-1238 (Q-SCH-08), 1336-1351 (Q-SCH-14), 1035-1058 (Q-MAN-08), 1843-1867 (Q-ACC-14) ; ADR-047 pour la ligne 7.

**Décision**

Sept limites. Le tableau les résume ; le détail sourcé suit.

| # | On ne fait pas | À la place | Renvoi |
|---|---|---|---|
| 1 | L'acte notarié | sa date et son prix entrent dans la vente (`sale`) | aucun : hors SI, chez le notaire |
| 2 | Une table des rendez-vous | on garde ce qu'un rendez-vous produit : mandat, vente, renouvellement | parcours IA |
| 3 | Le classement par pertinence ; les types d'offre | une liste sans score ; une priorité du client, de 1 à 5 ; une offre, un montant | parcours IA (Phase 4) |
| 4 | L'historique des managers | le manager courant seul | si la performance doit suivre le manager de l'époque |
| 5 | Garder qui a refusé une demande | une demande refusée reste `'rejected'` : « Non » mène à « Fin » | quand la réaffectation se code |
| 6 | Des droits propres aux chasseurs-IA | un chasseur-IA est un `hunter` | parcours IA (Phase 4) |
| 7 | 💡 Recharger les annonces ; les dédoublonner | 2 556 biens chargés une fois ; un nouveau bien se saisit à la main | parcours IA (dédoublonnage) |

**Détail et sources par limite**

Pour chacune : ce qu'on ne fait pas ; ce qui se passe à la place, y compris « si ça arrive quand même » ; pourquoi ; le renvoi ; la phrase pour le jury.

1. **L'acte notarié est hors du SI.**
   * ✅ On ne fait pas : le notaire, la collecte des honoraires, les pièces de l'acte (`questions-a-trancher.md:62-63`). Ni la date où l'entreprise reçoit les honoraires : elle « touche le circuit notarial » (`:722`).
   * ✅ À la place : l'acte entre par ses données, dans la vente (`:64-65`) : `sale.signature_date`, `sale.purchase_amount`, `sale.fees_amount` (`01:753-760`). Aucune colonne ne nomme le notaire. Le paiement du chasseur part du moment où on le prévient : `payment.announced_at` (`01:887-890`, ADR-038).
   * ✅ Pourquoi : le notaire « n'intervient pas dans le calcul » (`REGLES-CALCUL-REMUNERATION.md:130`). C'est un « officier public » (`GLOSSAIRE-METIER.md:10`), pas un utilisateur.
   * ✅ Renvoi : aucun. Hors SI, comme le « Versement bancaire. Hors SI » du modèle (`Gherkin.md:713-714`). Hors-périmètre pur : aucune table ni route ne peut le solliciter (`:737`).
   * 💡 Au jury : « Le notaire n'est pas dans notre SI. L'acte entre par sa date et son prix, dans la vente. C'est tout ce que le calcul lit. »
2. **Pas de table des rendez-vous** (Q-SCH-07, D10).
   * ✅ On ne fait pas : enregistrer un rendez-vous, sa date, son mode (présentiel ou en ligne). Le parcours en compte trois : le premier contact (`Readme.md:125-126`), l'acte chez le notaire (`:131`), le renouvellement (`:135`).
   * ✅ À la place : la base garde ce que produit le rendez-vous. Le premier produit un mandat signé, `mandate.signature_date` (« fait signer le mandat », `Readme.md:126`). Le deuxième, une vente, `sale.signature_date`. Le troisième, un nouveau mandat (ADR-050). Déduit du parcours et du schéma. `visit` porte les visites de biens (`01:712-726`), pas les rendez-vous.
   * ✅ Pourquoi : « Aucune règle de calcul ne s'en sert » (`questions-a-trancher.md:957`).
   * 💡 Renvoi : le parcours IA, qui veut automatiser « la prise de contact et de rendez-vous » (`09_futur_chasseur_assistance_ia.feature:23-26`). La table se décide avec lui.
   * 💡 Au jury : « Nous ne stockons pas les rendez-vous, seulement ce qu'ils produisent : un mandat, une vente, un renouvellement. Aucun calcul ne lit un rendez-vous. »
3. **Pertinence et types d'offre : reportés au parcours IA** (Q-SCH-08, D11 et D12).
   * ✅ On ne fait pas : ordonner une sélection « suivant leur pertinence » (`09_futur_chasseur_assistance_ia.feature:33-39`). Ni proposer « plusieurs offres d'achat (offre plus basse, offre au prix...) » (`:53-58`).
   * ✅ À la place : la sélection est une liste sans score. Un bien y figure une fois par demande (`uq_estate_search`, `01:659-668`). Le client donne sa priorité, de 1 à 5 (`estate_proposed.client_priority`, `01:706-709`). Une offre a un seul montant (`amount_proposition`, `01:690`). Après un refus du vendeur, le chasseur en refait une (`Readme.md:131`) : une nouvelle ligne (déduit, ADR-041). Aucun `UNIQUE` ne limite leur nombre (`01:684-710`).
   * ✅ Pourquoi : ce sont des règles du parcours futur. « Pas urgent : l'absence de ces règles n'est pas une erreur aujourd'hui. » (`09-decisions-a-prendre.md:454`). La liste des types d'offre est « ouverte » (`:467-468`).
   * ✅ Renvoi : le parcours IA, Phase 4 du sujet (`Readme.md:252`, `:257`).
   * 💡 Au jury : « Le classement par pertinence et les offres multiples sont des fonctions du parcours IA. Aujourd'hui, le chasseur choisit les biens, le client les note de 1 à 5, et une offre a un montant. »
4. **Pas d'historique des managers** (Q-SCH-14).
   * ✅ On ne fait pas : garder les anciens managers d'un chasseur.
   * ✅ À la place : `hunter.id_realestatemanager` (`01:294-297`) ne garde que le manager courant. Un changement écrase l'ancien (ADR-029, Décision 5). Le nouveau manager voit tout le passé du chasseur ; l'ancien n'en voit plus rien (ADR-029, Conséquences).
   * ✅ Pourquoi : « Suffisant pour les droits d'accès (ENF-03) » (`docker/init-v3/README.md:625-627`).
   * ✅ Renvoi : même source, « à revoir si la performance doit être rattachée au manager de l'époque ».
   * 💡 Au jury : « Un chasseur a un manager : le courant. En changer écrase l'ancien, c'est voulu. Pour suivre une équipe dans le temps, nous ajouterions une table d'historique. »
5. **On ne garde pas qui a refusé une demande** (Q-MAN-08).
   * ✅ On ne fait pas : réaffecter une demande refusée, ni se souvenir de qui l'a refusée.
   * ✅ À la place : une demande refusée reste `'rejected'`. Dans le schéma du sujet, « Non » mène à « Fin » (`Readme.md:140`). Rien ne la réaffecte dans le MVP : le service n'a aucune règle (`API/src/app/services/search_request_service.py:1-8`).
   * ✅ Si ça arrive quand même : l'API devra refuser de faire sortir une demande de `'rejected'`. C'est l'ordre des statuts d'ADR-041, à coder.
   * ✅ Pourquoi : le sujet dit « peut être réaffectée », pas « doit » (`04_chasseur_prise_en_charge_demande.feature:21`). Une demande ne garde qu'un chasseur, `search_request.id_hunter` (`01:315-316`).
   * 💡 Renvoi : quand la réaffectation se code. La table écartée, `search_request_refusal`, est la piste. La carte le prévoyait : « Si on réaffecte un jour, la demande peut revenir au chasseur qui l'a refusée : à dire comme limite en soutenance » (`questions-a-trancher.md:897`).
   * 💡 Au jury : « Le sujet dit qu'une demande refusée "peut être réaffectée". Notre MVP s'arrête au refus. Le jour où l'on réaffecte, une table des refus empêchera de la rendre à celui qui l'a refusée. »
6. **Les droits des chasseurs-IA : reportés au parcours IA** (Q-ACC-14).
   * ✅ On ne fait pas : des droits propres aux chasseurs-IA. La question 11 de la matrice reste ouverte (`md/securite/matrice-droits-crud-par-role.md:235`).
   * ✅ À la place : un chasseur-IA est un `hunter` avec `is_hunter_ai` (`01:293`). Il a un manager, comme tout chasseur (ADR-029). Aucun rôle ne lui est propre : 5 rôles, `'Admin'`, `'Client'`, `'Hunter'`, `'Manager'`, `'Reader'` (`01:163-164`). Déduit : il aurait les droits du rôle `'Hunter'`. 🟡 **À revoir (groupe, 09/10/2026, S10)** : droits reportés après les cours d'IA. Hypothèse de travail : l'IA cherche des biens et les soumet au chasseur humain, qui valide ; pas d'acte engageant (mandat, offre, vente) par l'IA seule. Point à garder : dans une zone sans chasseur humain, personne ne valide.
   * ✅ Pourquoi : le sujet dit peu de ce qu'il fera. Deux missions : « épauler les chasseurs humains », travailler dans les zones sans chasseur (`Readme.md:166-169`). Les chasseurs-IA doivent pouvoir « opérer seuls » (`09_futur_chasseur_assistance_ia.feature:6-7`) : la lecture seule, que le sujet veut pour une IA branchée sur la base (`Readme.md:282`), ne leur suffira pas.
   * ✅ Renvoi : la Phase 4, avec le « schéma du programme d'IA » (`Readme.md:257`).
   * 💡 Au jury, à la question « Comment évitez-vous qu'une IA branchée sur la base cause des dégâts ? » (`TRAME-SOUTENANCE.md:34`) : « Une IA qui lit la base passe par le rôle en lecture seule `fil_rouge_reader`. Un chasseur-IA doit agir : ses droits sont reportés au parcours IA. Nous ne les fixons pas sans savoir ce qu'il fera. » Répondre « reporté, et pourquoi », pas « défini » (fiche Q-ACC-14).
7. **💡 Les annonces : un import par flux orchestré, avec dédoublonnage** (ADR-047). Proposée par Sébastien, acceptée par le groupe le 2026-10-09 (Discord).
   * 💡 On fait : un flux de données orchestré par Airflow importe les annonces ; des étapes map/reduce font le tri, la mise en forme et le dédoublonnage. Le sujet ne l'exige pas (« Airflow » n'y apparaît pas) : c'est un choix du groupe, que `outils/Readme.md` rend plausible (flux volontairement hétérogène, de plusieurs sources).
   * 🟡 Reporté après les cours de machine learning et de data science (Sébastien, 2026-10-09) : où vit ce flux (dans le dépôt, quel dossier), et ce qu'il fait d'un bien saisi à la main qui arriverait aussi par l'import (`estate.reference` est `UNIQUE`, `01:561`).
   * ✅ État actuel du dépôt : les 2 556 biens sont chargés une fois, à la création de la base (`docker/init-v3/03_populate_estate.sql`). Un nouveau bien entre à la main, par un chasseur ou un manager (ADR-047). Recharger un autre CSV n'est pas outillé : `03` est une copie retouchée, et « le script de retouche n'est pas dans le dépôt » (`questions-a-trancher.md:180`). Le flux ci-dessus reste à écrire.
   * ✅ Pourquoi un flux : le sujet décrit une sélection envoyée « chaque jour » (`Readme.md:127`). Sans rechargement, elle puise toujours dans les mêmes biens, plus ceux saisis à la main.
   * ✅ Contexte : les annonces sont factices, produites par l'outil du sujet (`outils/Readme.md:3`, `:6`). Le sujet n'impose aucun outil : « Airflow » n'y apparaît pas (recherche du 08/10/2026).
   * ✅ Renvoi : le parcours IA, où le sujet place le dédoublonnage (`Readme.md:193`). Le groupe le ramène dans le flux d'import : écart au sujet, à dire au jury.
   * ✅ Ne couvre pas : l'expiration des mandats finis. Le sujet la demande (`07_chasseur_remuneration_et_performance.feature:38-41`) : c'est du code à écrire (ADR-046).
   * 💡 Au jury : « Nos annonces viennent de l'outil du sujet, qui simule plusieurs sources hétérogènes. Un flux Airflow les trie, les met en forme et les dédoublonne. Un bien hors marché se saisit à la main. Le sujet range le dédoublonnage dans le parcours IA : nous l'avons placé dans l'import, par choix. »

**Justification**

* Six limites viennent d'une décision datée : cinq cartes tranchées par le groupe, et l'annonce du 02/10/2026 pour l'acte notarié (voir Décideurs). La septième, proposée par cet ADR, a été réécrite et acceptée par le groupe le 2026-10-09.
* La forme suit le sujet : chaque exclusion dit ce qui se passe « si ça arrive quand même » (`Gherkin.md:722`).
* Aucune n'est un oubli : chacune a sa raison et son renvoi. Pour l'acte notarié, le renvoi est « hors SI ».
* Le notaire est le cas le plus net : le sujet lui-même le sort du calcul (`REGLES-CALCUL-REMUNERATION.md:130`).
* Le tableau en tête tient dans la minute que la trame donne au bilan (`TRAME-SOUTENANCE.md:22`).

**Conséquences**

* **Base :** rien ne change. Aucune table, aucune colonne (registre : `:162` « Rien en base », `:163`, `:169`, `:176`, `:186` « Rien maintenant »).
* **Code :** rien de propre à ces limites. Une seule appelle une garde, déjà à coder ailleurs : une demande ne sortira pas de `'rejected'` (limite 5 ; ordre des statuts, ADR-041). Les autres n'ont ni table ni colonne où écrire ce qui est écarté : le système ne peut pas être sollicité (`Gherkin.md:737`).
* **Soutenance :** les sept phrases vont dans « Limites assumées » (`TRAME-SOUTENANCE.md:48`). Ce sont des 💡 formulations : le groupe les ajuste.
* **Hors périmètre ou reporté :** l'acte notarié est exclu. Q-SCH-07 et Q-SCH-14 sont acceptées. Q-SCH-08, Q-MAN-08 et Q-ACC-14 sont reportées. L'import régulier est 💡 proposé comme limite.
* **Jeff :** il confirme les reports de Q-SCH-08 et de Q-ACC-14 à la séance de validation des ADR (Q-JEF-25).
* **Matrice des droits :** la question 11 reste ouverte, « bien visible » (fiche Q-ACC-14).
* **Livrable 2 :** D10 se ferme (pas de table) ; D11 et D12 restent reportées (`09-decisions-a-prendre.md:72-74`).

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Les « Conséquences » d'ADR-039 et d'ADR-050 ajoutent-elles des limites ? | Non. ADR-039 n'y liste que du code à écrire : le code de sa Décision 5, et le calcul de `ends_at`. ADR-050 range un `'renewed'` sans successeur en « Limite à connaître », mais sa Justification répond : « L'API devra le garantir ». Une règle à coder n'est pas une limite assumée. | déduit de `md/adr/adr-039-regles-du-mandat.md:136-141` ; `md/adr/adr-050-renouvellement-du-mandat.md:122` (Justification), `:149-150` (Conséquences) |
| L'expiration d'un mandat fini est-elle une limite ? | Non. Le sujet la demande, dans le parcours actuel : à l'échéance sans vente, invitation à renouveler et note à la baisse. C'est du code à écrire (ADR-046). | `07_chasseur_remuneration_et_performance.feature:38-41` (`@actuel`) ; `Readme.md:135` |
| La date et le prix de l'acte sortent-ils aussi du SI ? | Non. Ils restent des entrées du calcul, dans `sale`. | `questions-a-trancher.md:64-65` ; `01:756-758` |
| La date où l'entreprise reçoit les honoraires se stocke-t-elle ? | Non : elle touche le circuit notarial. | `questions-a-trancher.md:722` |
| Rendez-vous et visites, est-ce la même chose ? | Non. `visit` porte les visites de biens (`visitor_type` : chasseur ou client). D10 vise les rendez-vous. | `01:712-726` ; `09-decisions-a-prendre.md:439-448` |
| Un chasseur-IA a-t-il un manager ? | Oui : la colonne est obligatoire. | `01:294-297` ; ADR-029, Conséquences |
| Acte notarié : pourquoi, et quel renvoi ? | Raison : le notaire « n'intervient pas dans le calcul » ; c'est un « officier public ». Renvoi : aucun. Hors SI, comme le versement bancaire du modèle. | `REGLES-CALCUL-REMUNERATION.md:130` ; `GLOSSAIRE-METIER.md:10` ; `Gherkin.md:713-714`, `:737` (StarterPack) |
| Acte notarié : qui l'a décidé ? | Annoncé par Sébastien le 02/10/2026. Décidé par Jeff, précisé par Sébastien le 2026-10-09 (Discord). | `questions-a-trancher.md:62` ; notes de session de Claude du 02/10/2026 (hors dépôt) |
| Faut-il attendre Jeff pour Q-SCH-08 et Q-ACC-14 ? | Non. Jeff valide les ADR en une séance (Q-JEF-25) : il confirme ces reports à cette séance. C'est une tâche, pas une question. | `2026-10-07-questions-pour-jeff.html:378-379` ; `questions-a-trancher.md:197` |
| Q-MAN-08 : garder le report, maintenant que l'affectation est décidée ? | Oui. **Tranchée par déduction.** Q-ACC-10 dit qui affecte : le manager. Elle ne crée pas la réaffectation. Dans le schéma du sujet, « Non » mène à « Fin ». La carte le prévoyait : « Si on réaffecte un jour, […] à dire comme limite en soutenance ». Ni l'affectation ni la réaffectation ne sont codées. | `questions-a-trancher.md:247`, `:894`, `:896-897` ; `Readme.md:140` ; `search_request_service.py:1-8` |

**Questions ouvertes** 🟡

Aucune.

**Sources**

| Affirmation | Source |
|---|---|
| « Reconnaître une limite est une force » ; 1 minute de bilan ; « Limites assumées » ; « voici comment nous l'aurions abordé » | `documents utiles/TRAME-SOUTENANCE.md:22`, `:48`, `:57` (StarterPack) |
| Question du jury sur une IA branchée sur la base | même fichier, l. 34 |
| Les quatre éléments d'une exclusion ; le hors-périmètre pur ; formulations à bannir | `documents utiles/Gherkin.md:717-726`, `:737`, `:739-746` (StarterPack) |
| « Versement bancaire. Hors SI » | `Gherkin.md:713-714` (StarterPack) |
| T : cinq cartes, « décidé — à dire en soutenance » | `md/questions/questions-a-trancher.md:415` |
| Acte notarié hors périmètre, « qui l'a décidé n'est pas noté » ; date et prix restent des entrées | `questions-a-trancher.md:62-65` ; `md/adr/2026-10-07-liste-adr-chantier-4.md:61-62` |
| Date de réception des honoraires hors périmètre | `questions-a-trancher.md:722` |
| Le notaire « n'intervient pas dans le calcul » ; officier public | `documents utiles/REGLES-CALCUL-REMUNERATION.md:130` ; `documents utiles/GLOSSAIRE-METIER.md:10` (StarterPack) |
| `sale` : date, prix, honoraires ; `payment.announced_at` | `docker/init-v3/01_create_fil_rouge_immobilier.sql:753-760`, `:887-890` |
| Q-SCH-07 « Ne pas créer, hors MVP » ; « Aucune règle de calcul ne s'en sert » | `questions-a-trancher.md:162`, `:956-957` |
| Les rendez-vous du parcours ; la sélection « chaque jour » ; refaire une offre | `Readme.md:125-127`, `:131`, `:135` (StarterPack) |
| Rendez-vous automatisables ; pertinence, offres multiples ; « opérer seuls » | `user-stories/09_futur_chasseur_assistance_ia.feature:6-7`, `:23-26`, `:33-39`, `:53-58` (StarterPack) |
| `visit` | `01_create_fil_rouge_immobilier.sql:712-726` |
| D10, D11, D12 ; « Pas urgent » | `livrables/2-modelisation/09-decisions-a-prendre.md:72-74`, `:439-468` |
| Q-SCH-08 « Reporter au parcours IA » | `questions-a-trancher.md:163`, `:925` |
| Sélection, priorité du client, montant de l'offre | `01_create_fil_rouge_immobilier.sql:659-668`, `:684-710` |
| Nouvelle offre après un refus : une nouvelle ligne (déduit) | ADR-041 (proposé), Questions tranchées |
| Q-SCH-14 « Accepter comme limite » | `questions-a-trancher.md:169`, `:931`, `:966` |
| Pas d'historique ; « Suffisant pour les droits d'accès » | `docker/init-v3/README.md:625-627` ; ADR-029, Décision 5 et Conséquences |
| `hunter.id_realestatemanager NOT NULL` ; `is_hunter_ai` | `01_create_fil_rouge_immobilier.sql:293-297` |
| Q-MAN-08 « Reporter » ; constat, options, limite à dire en soutenance | `questions-a-trancher.md:176`, `:883-897` |
| « peut être réaffectée » ; un refus mène à « Fin » | `user-stories/04_chasseur_prise_en_charge_demande.feature:21` ; `Readme.md:140` (StarterPack) |
| `search_request.id_hunter` ; statuts de la demande | `01_create_fil_rouge_immobilier.sql:315-321` |
| Service sans règle | `API/src/app/services/search_request_service.py:1-8` |
| Q-ACC-10 : le manager affecte | `questions-a-trancher.md:247` |
| Q-ACC-14 « Reporter au parcours IA » ; cartes du PO | `questions-a-trancher.md:186`, `:197` ; fiche `questions-a-trancher.html:1843-1867` |
| Question 11 de la matrice | `md/securite/matrice-droits-crud-par-role.md:235` |
| Cinq rôles | `01_create_fil_rouge_immobilier.sql:158-165` |
| Missions et Phase 4 des chasseurs-IA ; « lecture seule » | `Readme.md:166-169`, `:252`, `:257`, `:282` (StarterPack) |
| Rôle `fil_rouge_reader` | `docker/init-v3/04_role-lecture-seule.sql:1-20` |
| Annonces factices de l'outil du sujet | `outils/Readme.md:3`, `:6` (StarterPack) |
| Dédoublonnage au parcours IA | `Readme.md:193` (StarterPack) |
| « Airflow » absent du sujet | recherche du 08/10/2026 dans le StarterPack : 0 fichier |
| 2 556 biens chargés une fois ; `03` copie retouchée, script absent | `docker/init-v3/03_populate_estate.sql` ; `questions-a-trancher.md:180` |
| Échéance sans vente : invitation, note à la baisse (parcours actuel) | `user-stories/07_chasseur_remuneration_et_performance.feature:38-41` ; `Readme.md:135` (StarterPack) |
| ADR-039 et ADR-050 : code à écrire ; « L'API devra le garantir » | `md/adr/adr-039-regles-du-mandat.md:136-141` ; `md/adr/adr-050-renouvellement-du-mandat.md:122`, `:149-150` |
| Jeff : pas de réponse sur Q-SCH-08 et Q-ACC-14 ; ADR validés en une séance | `md/questions/2026-10-07-questions-pour-jeff.html:378-379` |
| Modèle d'ADR | `documents utiles/JOURNAL-DE-DECISIONS.md:19-40`, `:72` (StarterPack) |

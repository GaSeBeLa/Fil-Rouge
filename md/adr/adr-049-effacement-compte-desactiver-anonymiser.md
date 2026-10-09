# ADR-049 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 049 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:80`).
> Il porte la lettre V du pense-bête (`md/questions/questions-a-trancher.md:417`).
>
> 💡 **Rédigé le 2026-10-08 par Claude**, d'après les fichiers du dépôt, le
> sujet, deux documents de la CNIL et trois textes de Légifrance. Relu le
> 08/10/2026 par deux relecteurs (sources ; oral et jury) et un arbitre. Aucune
> question ne reste ouverte. La durée X vaut 10 ans, d'après un décret. Son
> point de départ est une proposition de l'équipe, adoptée avec la fiche : le
> client laisse X au groupe (Q-JEF-15).
>
> 🌐 **Recherche web** (08/10/2026) :
>
> * rédacteur : 2 recherches (cnil.fr, legifrance.gouv.fr), 2 PDF de la CNIL
>   lus en entier ;
> * relecteur « sources » : article 2224 du Code civil ouvert sur Légifrance,
>   texte identique à l'extrait ;
> * relecteur « oral » : 1 recherche, décret n° 72-678 (article 72) et arrêt
>   de la Cour de cassation du 10/12/2014 lus sur Légifrance ;
> * arbitre : article 72 du décret rouvert, phrase identique.
> * ⚠️ **Non lu :** l'article 1 de la loi n° 70-9 du 2 janvier 1970, qui dit
>   quelles activités le décret couvre. Le lien entre ce décret et la recherche
>   de biens n'est vu que par l'arrêt de 2014.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * Le registre RGPD du projet n'existe pas encore (`livrables/` : aucun
>   fichier de registre). Les durées de cette fiche y entreront.
> * `md/securite/matrice-droits-crud-par-role.md:239`, question 15, « Au bout
>   de combien de temps anonymiser ? » : répondue ici, une fois adoptée.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-049 : Effacer un compte — le désactiver, rendre anonyme tout de suite ce que rien n'oblige à garder, le reste à la fin de son délai ; jamais de suppression

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (réponse du groupe : 06/10/2026 et 07/10/2026 ; client : 07/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * l'équipe projet : « lorsqu'il y a une demande de suppression de compte, admin va rendre anonyme les données du compte et passé [sic] le compte en inactif . tout ca pour la RGPD. » (Q-ACC-08, 06/10/2026) ; « 10 ans + X » (07/10/2026) ;
  * le client (Jeff, formateur jouant le commanditaire et le PO) : « ajouter une route, ou modifier la route DELETE, pour seulement anonymiser les données personnelles d'une personne. La durée X : le groupe la propose. » (Q-JEF-15, réponse notée par l'équipe le 07/10/2026).
* **Complète :** ADR-027 (un compte ne se supprime pas) et ADR-028 (un compte désactivé ne se connecte pas).

Abréviations : `01` = `docker/init-v3/01_create_fil_rouge_immobilier.sql` ; `reg` = `md/questions/questions-a-trancher.md` ; `jeff.html` = `md/questions/2026-10-07-questions-pour-jeff.html` ; « référentiel CNIL », « guide CNIL », « décret », « arrêt de 2014 » : voir Sources.

**Contexte**

Le sujet demande un registre RGPD avec, pour chaque traitement, une durée de conservation (`Readme.md:270`). Il pose la question : « comment un client peut-il consulter, corriger ou faire effacer ses données ? » (`REGISTRE-RGPD.md:38`). Ces exigences ne sont « **pas optionnelles** » (`Readme.md:266`).

Son modèle de registre, « à remplir » (`REGISTRE-RGPD.md:21`), donne trois traitements :

* gestion des mandats : « Durée du mandat + X ans (obligations légales) » (`:27`). X reste vide ;
* comptes acquéreurs : « Tant que le compte est actif » (`:28`) ;
* paiements et honoraires : « 10 ans (obligation comptable) » (`:29`).

Le métier a sa propre règle : « Les mandats et le registre des mandats sont conservés pendant dix ans. » (décret n° 72-678, article 72). La société signe des mandats de recherche, « document légal » (`Readme.md:73`).

La base ne peut pas supprimer une personne liée à autre chose. Ses 38 clés étrangères sont toutes en `ON DELETE RESTRICT`, aucune en `CASCADE` (`01`, compté le 08/10/2026). Un compte cité par un client renvoie 409 (`API/tests/integration/test_users_db.py:95-104`).

L'API a pourtant une route DELETE sur ses 20 ressources (`API/src/app/routes/crud_router.py:104-110`). Un compte libre se supprime (`test_users_db.py:89-92`). Aucune anonymisation n'est codée (recherche de `anonym` dans `API/src` le 08/10/2026 : 0 occurrence).

**Options envisagées**

1. **Supprimer la ligne.** Avantage : déjà codé. Inconvénients : impossible dès qu'une ligne la cite ; supprimerait aussi ce que la loi oblige à garder. Écartée par le groupe (Q-ACC-08).
2. **Désactiver seulement.** Avantage : rien ne se perd. Inconvénient : les données personnelles restent ; la demande d'effacement n'est pas servie. Écartée.
3. **Tout rendre anonyme tout de suite.** Avantage : simple. Inconvénient : l'identité liée aux paiements et aux mandats disparaît avant 10 ans. Écartée, déduit de « 10 ans + X ».
4. **Désactiver tout de suite, rendre anonyme tout de suite ce que rien n'oblige à garder, le reste à la fin de son délai.** **Retenue**, déduit de Q-ACC-08 et de « 10 ans + X ». Proposée telle quelle à Jeff (`jeff.html:1694`) ; sa réponse ne la conteste pas (`:1701`).

Sous-choix sur la durée X des mandats :

* **5 ans**, la prescription de droit commun (Code civil, article 2224 ; premier jet de cette fiche). Écartée : une prescription borne le temps d'agir en justice. Elle ne raccourcit pas une obligation de conserver.
* **10 ans**, l'obligation de conserver les mandats (décret, article 72). **Retenue.**

Sous-choix sur la route, laissé par le client (Q-JEF-15) :

* **Modifier la route DELETE.** Écartée, déduit : les tests définissent DELETE comme « supprimer, puis `GET` rend 404 » (`test_users_db.py:89-92`). Un DELETE qui rend anonyme laisserait `GET` à 200, et tromperait celui qui l'appelle.
* **Une route à part.** **Retenue.**

**Décision**

✅ veut dire « établi par une source », pas « codé ». Rien de cette fiche n'est codé.

1. ✅ **Sur une demande d'effacement, l'admin désactive le compte** : `is_activated = FALSE` (`01:173`). Le compte ne peut plus se connecter (ADR-028).
2. ✅ **Aucune personne ne se supprime.** L'effacement passe par l'anonymisation (Q-ACC-08). La CNIL l'admet : « en lieu et place de mesures d'effacement, les données peuvent faire l'objet d'un processus d'anonymisation afin de rendre impossible pour quiconque la « ré-identification » des personnes concernées » (guide CNIL). Limite : voir Conséquences.
3. ✅ **Une route à part rend anonyme** les données personnelles d'une personne (Q-JEF-15) : `POST /users/{id}/anonymize`, réservée à l'`Admin` (ADR-027). Elle désactive, et rend anonyme ce qui peut l'être. La forme est tranchée par déduction (Options). Demande du code, non fait.
4. ✅ **Ce que rien n'oblige à garder est rendu anonyme tout de suite** (déduit de Q-ACC-08 et de la minimisation, `REGISTRE-RGPD.md:9`). Garder « au cas où » n'est pas permis : « Il n'est pas possible d'archiver des données « au cas où… » » (guide CNIL).
5. **Les durées, rangées par traitement** (`REGISTRE-RGPD.md:27-29`) :

| Traitement du modèle | Durée écrite par le sujet | Ce que fait cette fiche | Statut |
|---|---|---|---|
| Comptes acquéreurs (`:28`) | « Tant que le compte est actif » | sur une demande d'effacement : désactivé et rendu anonyme tout de suite | ✅ Q-ACC-08 |
| Gestion des mandats (`:27`) | « Durée du mandat + X ans (obligations légales) » | **X = 10 ans** : « Les mandats et le registre des mandats sont conservés pendant dix ans » (décret, article 72) | ✅ tranchée par les sources, avec une déduction (Questions tranchées) |
| Paiements / honoraires (`:29`) | « 10 ans (obligation comptable) » | **10 ans** ; le référentiel CNIL cite une « obligation comptable de 10 ans » | ✅ |
| Le reste : téléphone, adresse, naissance, situation familiale, textes écrits par la personne | aucune | rendu anonyme tout de suite (point 4) | ✅ déduit |

   * 💡 **Point de départ, proposition de l'équipe, adoptée avec la fiche.** Pour un mandat : la fin du dernier mandat de la chaîne (`mandate.ends_at`, `01:457`). C'est la lecture de « Durée du mandat + X ans ». Pour un paiement : sa date (`payment.paid_at`, `01:892`) ; à défaut, celle de l'acte (`sale.signature_date`, `01:756`). L'identité attend la plus tardive de ces fins.
   * 💡 **Mandat jamais signé :** aucun contrat à garder. Rendu anonyme tout de suite.
6. ✅ **Rendre anonyme n'est pas vider.** Les colonnes obligatoires reçoivent une valeur neutre, au bon format ; les autres sont vidées (déduit des contraintes : `01:171`, `:197-200`, `:205-206`, `:221-222`, `:227-229`).
7. 💡 **Ce qui change, et quand** :

| Donnée | Où | Quand | Nouvelle valeur 💡 |
|---|---|---|---|
| Email | `"user".email`, `NOT NULL UNIQUE` (`01:171`) | tout de suite | `anonyme-<id>@exemple.invalid`, unique par construction |
| Mot de passe | `"user".password`, `NOT NULL` (`01:172`) | tout de suite | une valeur qui n'est pas une empreinte Argon2 : aucune connexion possible, comme les comptes repris (`API/src/app/utils/security.py:41-43`) |
| Téléphone | `phone_number`, `NOT NULL`, format imposé : `client` (`01:205-206`, `:221-222`), `hunter` (`01:276-277`, `:299-300`), `real_estate_manager` (`01:254-255`, `:263-264`) | tout de suite | `+33000000000`, la valeur factice déjà admise (`01:189-190`, Q-MIG-07) |
| Adresse, complément, code postal, ville, pays | `client` (`01:201`, `:207-215`) | tout de suite | vides, toutes ensemble (`01:227-229`) |
| Naissance, genre, situation familiale, enfants | `client` (`01:203`, `:216-219`) | tout de suite | vides |
| Textes écrits par la personne | `estate_proposed.comment_client` (`01:688`) ; `criteria.change_reason` quand elle en est l'auteur (`01:328`) | tout de suite | vides |
| Prénom, nom | `NOT NULL` : `client` (`01:197-200`), `hunter` (`01:272-275`), `real_estate_manager` (`01:250-253`) | à la fin du plus long délai qui la concerne (point 5) ; tout de suite si aucun | « Anonyme » |

8. ✅ **Même règle pour un chasseur ou un manager** (déduit de Q-ACC-08, qui ne distingue pas les rôles, `reg:183` ; et de `REGISTRE-RGPD.md:29`). Un chasseur a des paiements : son nom reste 10 ans (point 5). Sa date d'embauche, `NOT NULL`, sert au calcul de l'ancienneté (`01:284`) : elle suit le paiement.
9. 💡 **La seconde étape, à la fin d'un délai :** la même route, rappelée par l'`Admin`, à la demande. Plus tard, un traitement planifié. Proposition de l'équipe, adoptée avec la fiche. ✅ Le traitement planifié est **reporté à une éventuelle V2** (Sébastien, Discord, 09/10/2026) : dans le MVP, l'`Admin` relance la route à la main.
10. 💡 **Fermer DELETE sur toutes les ressources**, proposition de l'équipe, adoptée avec la fiche (ADR-027, point 4). Le registre ne le demandait que pour les comptes, « ou à justifier » (`reg:303`). Demande du code, non fait.

**Justification**

* Le groupe a choisi de désactiver puis de rendre anonyme (Q-ACC-08). Le client demande une route qui « seulement » anonymise (Q-JEF-15).
* La base l'impose pour une personne citée par une autre ligne (38 clés en `RESTRICT` sur 38). Un compte que rien ne cite se supprime encore (`test_users_db.py:89-92`) : c'est la règle du groupe qui l'interdit (Q-ACC-08).
* Deux temps, parce que deux règles se croisent : effacer sur demande, et garder ce que la loi impose. La CNIL décrit ce passage : au terme du contrat, les données « doivent être conservées en archivage intermédiaire […] si le responsable du traitement en a l'obligation légale […] ou s'il souhaite se constituer une preuve en cas de contentieux, et dans la limite du délai de prescription applicable » (référentiel CNIL, § 7).
* 10 ans pour les mandats : c'est une obligation légale de conserver, avec sa durée écrite (décret, article 72). Une prescription, comme les 5 ans de l'article 2224, borne le temps d'agir en justice : elle ne la raccourcit pas. Le référentiel CNIL dit aussi : « De manière générale, les durées de conservation ne devraient, en principe, pas dépasser les durées de prescriptions légales » (§ 7, 1er alinéa). « En principe » : ici, un texte fixe lui-même la durée.
* Une valeur neutre au bon format garde les contraintes de la base intactes. Vider une colonne `NOT NULL` serait refusé.
* Une route à part dit ce qu'elle fait. DELETE garde son sens : supprimer.

**Conséquences**

* **Code, à écrire :** la route d'anonymisation, réservée à l'`Admin` (ADR-027, ADR-028), et ses tests d'intégration. Un client rendu anonyme doit passer tous les `CHECK` de la base. Demande du code, non fait.
* **Routes DELETE :** la fabrique commune les donne à toutes les ressources (`crud_router.py:104-110`). Elles contredisent cette fiche et ADR-027. Les tests `test_users_db.py:89-104` décrivent une vraie suppression : à réécrire si DELETE se ferme (point 10).
* ⚠️ **Limite : plus proche d'une pseudonymisation que d'une anonymisation.** Le sujet dit l'anonymisation « irréversible » : « on supprime tout moyen de ré-identifier la personne » (`SOUVERAINETE-SECURITE-IA.md:19`). Or la vente garde l'adresse du bien, la date et le prix ; les critères gardent la ville et le quartier. En les croisant, on peut encore retrouver la personne. La pseudonymisation remplace les identifiants par des codes (`SOUVERAINETE-SECURITE-IA.md:20`) ; ici, aucune clé n'est gardée, mais le risque de ré-identification reste. À dire à l'oral, et dans le registre.
* **Données en attente :** pour la CNIL, elles « ne doivent plus être consultables par tous les opérationnels initialement prévus, mais seulement par des personnes spécialement habilitées » (guide CNIL). Le référentiel parle d'une « séparation logique dans la base de données active ». 💡 Ici : le compte désactivé, et ses données lisibles par l'`Admin` seul (ADR-027, point 7). Pas de base d'archive à part : le projet n'est pas déployé.
* **`fil_rouge_reader`** lit tout sauf `"user".password`, y compris les données pas encore anonymes (`docker/init-v3/04_role-lecture-seule.sql:51`). Limite dite dans ADR-027.
* **`is_activated` a deux sens.** Faux pour un compte pas encore finalisé (`F01:27-28`, `01:173`), faux aussi pour un compte désactivé. 💡 Ajouter une date : `deactivated_at`, et `anonymized_at` pour la seconde étape. Elles prouvent la réponse à la demande ; la CNIL permet de la garder « à des fins de preuve, dans la limite du délai de prescription applicable » (référentiel CNIL). Changement de schéma : demande du code, non fait.
* **Comptes inactifs :** le modèle du sujet garde les comptes « Tant que le compte est actif » (`REGISTRE-RGPD.md:28`). Pour un compte oublié, le référentiel CNIL juge qu'« un délai de deux ans apparait proportionné ». 💡 Piste pour le registre, pas décidée ici.
* **Textes du chasseur :** son avis et ses commentaires peuvent citer le client par son nom (`01:662`, `:687`). Un programme ne sait pas les trier. Limite connue, à dire.
* **Le budget et les critères restent.** Le budget d'un client identifié est une donnée personnelle (`REGISTRE-RGPD.md:13`). Une fois l'identité rendue anonyme, il ne désigne plus personne, sous la limite dite plus haut. Ils servent aux statistiques ; la CNIL : des données « dûment anonymisées » ne sont plus personnelles (référentiel CNIL).

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Supprimer ou désactiver ? | Désactiver, puis rendre anonyme | Q-ACC-08 (`reg:183`) |
| Qui le fait ? | L'admin | Q-ACC-08 (`reg:183`) |
| Par quoi ? | Une route à part, `POST /users/{id}/anonymize`. Tranchée par déduction : un DELETE qui anonymise contredirait ses tests. Jeff laissait le choix | Q-JEF-15 (`reg:253`, `:1170` ; `jeff.html:1701`) ; `test_users_db.py:89-92` |
| Combien de temps pour les paiements ? | 10 ans | `REGISTRE-RGPD.md:29` ; référentiel CNIL (« obligation comptable de 10 ans ») ; groupe, « 10 ans + X » (`reg:253`) |
| Combien vaut X, pour les mandats ? | 10 ans. Tranchée par les sources, avec une déduction : la société signe des mandats de recherche (`Readme.md:73`) ; l'arrêt de 2014 range les mandats de recherche dans le registre des mandats ; le schéma prévoit la carte professionnelle du chasseur (`01:287-290`). Limite : l'article 1 de la loi n° 70-9 n'a pas été lu. Jeff laisse X au groupe : c'est la proposition de l'équipe, adoptée avec la fiche ; confirmée par Sébastien le 2026-10-09 (Discord) | décret, article 72 ; arrêt de 2014 ; Q-JEF-15 (`jeff.html:1701`) |
| Pourquoi pas 5 ans (article 2224) ? | Une prescription borne le temps d'agir en justice ; elle ne raccourcit pas une obligation de conserver | Code civil, article 2224 ; décret, article 72 ; référentiel CNIL, § 7 |
| Et les données sans durée (demandes, visites) ? | Rien n'oblige à garder leur lien à une personne : l'identité part selon le point 5, les textes écrits tout de suite. Tranchée par déduction | point 4 ; guide CNIL (« au cas où… ») ; question posée à Jeff, sans réponse sur ce point (`jeff.html:1694`, `:1701`) |
| Rendre anonyme, est-ce effacer ? | Oui, si personne ne peut plus retrouver la personne. Ici, un risque reste : voir la limite des Conséquences | guide CNIL ; `SOUVERAINETE-SECURITE-IA.md:19-20` |
| Même règle pour un chasseur, un manager ? | Oui, tranchée par déduction : Q-ACC-08 ne distingue pas les rôles | `reg:183` ; `REGISTRE-RGPD.md:29` |
| Peut-on vider les colonnes ? | Pas les obligatoires : valeur neutre | `01:171`, `:197-200`, `:205-206`, `:221-222` |
| Un compte désactivé se connecte-t-il ? | Non | ADR-028, Questions tranchées ; `01:173` |
| Peut-on tout garder jusqu'au bout, par prudence ? | Non : seulement ce qu'une obligation impose | guide CNIL (« au cas où… ») |

**Questions ouvertes** 🟡

Aucune. Le point de départ des délais, la seconde étape et la fermeture de DELETE sont des propositions de l'équipe, adoptées avec la fiche (Décision, points 5, 9, 10). Ce qui reste est du code à écrire (Conséquences).

Où l'on a cherché X et son point de départ : le StarterPack (`REGISTRE-RGPD.md`, X laissé vide, l. 27 ; `Readme.md:268-270` ; `SOUVERAINETE-SECURITE-IA.md` ; les autres fiches de `documents utiles/`, recherche de `anonym`, `effac`, `conservation`, `supprim`) ; le dépôt (`reg:253`, `:1063-1065` ; la carte Q-JEF-15 ; la matrice du 02/10, question 15 ; `md/` et `context AI/`, recherche de `anonymis`, `durée de conservation`, `prescription`) ; le web (voir le bandeau). Le décret ne fixe pas de point de départ dans l'article lu.

**Sources**

| Affirmation | Source |
|---|---|
| Q-ACC-08 : désactiver et rendre anonyme (06/10/2026) | `md/questions/questions-a-trancher.md:183` |
| « 10 ans + X » ; route d'anonymisation (Q-JEF-15) ; route DELETE « à retirer pour les comptes, ou à justifier » | même fichier, l. 253, l. 1170, l. 303 |
| Question posée à Jeff ; sa réponse, « La durée X : le groupe la propose » | `md/questions/2026-10-07-questions-pour-jeff.html:1694`, `:1701` |
| Durées du modèle du sujet ; minimisation ; budget = donnée personnelle ; droits des personnes | `documents utiles/REGISTRE-RGPD.md:9`, `:13`, `:21`, `:27-29`, `:38` (StarterPack) |
| RGPD « pas optionnel » ; durée de conservation exigée | `Readme.md:266`, `:270` (StarterPack) |
| Le mandat de recherche, « document légal » | `Readme.md:73` (StarterPack) |
| Anonymisation « irréversible » ; pseudonymisation | `documents utiles/SOUVERAINETE-SECURITE-IA.md:19-20` (StarterPack) |
| Compte activé à la fin de sa création | `user-stories/01_particulier_demande_et_compte.feature:27-28` (StarterPack) |
| Colonnes, contraintes, téléphone factice, carte professionnelle | `docker/init-v3/01_create_fil_rouge_immobilier.sql:171-173`, `:189-229`, `:250-264`, `:272-277`, `:284`, `:287-290`, `:299-300`, `:328`, `:457`, `:662`, `:687-688`, `:756`, `:892` |
| 38 clés `RESTRICT`, 0 `CASCADE` | même fichier, compté le 08/10/2026 |
| Route DELETE commune ; tests de suppression | `API/src/app/routes/crud_router.py:104-110` ; `API/tests/integration/test_users_db.py:89-104` |
| Faux mot de passe : aucune connexion | `API/src/app/utils/security.py:41-43` |
| Aucune anonymisation codée | recherche de `anonym` dans `API/src`, 08/10/2026 : 0 occurrence |
| Décret : « Les mandats et le registre des mandats sont conservés pendant dix ans. » | décret n° 72-678 du 20 juillet 1972, article 72, doc officielle, [Légifrance](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000033202014), « Version en vigueur depuis le 01/10/2016 », lue le 08/10/2026 (relecteur, puis arbitre) |
| Mandats de recherche dans le registre : « tous les mandats visés par ce texte sont mentionnés sur un registre unique » ; un registre séparé pour les mandats de recherche n'est pas conforme | Cass. 1re civ., 10/12/2014, n° 13-24.352, jurisprudence officielle, [Légifrance](https://www.legifrance.gouv.fr/juri/id/JURITEXT000029899112/), lue le 08/10/2026 (relecteur) |
| Quelles activités le décret couvre | loi n° 70-9 du 2 janvier 1970, article 1 : **non lu** |
| Prescription de cinq ans : « Les actions personnelles ou mobilières se prescrivent par cinq ans à compter du jour où le titulaire d'un droit a connu ou aurait dû connaître les faits lui permettant de l'exercer. » | Code civil, article 2224, doc officielle, [Légifrance](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019017112), ouvert le 08/10/2026 (relecteur), texte identique ; en vigueur depuis le 19/06/2008 (loi n° 2008-561 du 17 juin 2008, art. 1) |
| Référentiel CNIL : § 7 « Durées de conservation » (1er alinéa, « en principe » ; archivage intermédiaire, prescription, séparation logique, preuve, deux ans pour un compte inactif, données anonymisées) ; tableau, « obligation comptable de 10 ans » | CNIL, « Référentiel relatif aux traitements de données à caractère personnel mis en œuvre aux fins de gestion des activités commerciales », doc officielle, [PDF](https://www.cnil.fr/sites/cnil/files/atoms/files/referentiel_traitements-donnees-caractere-personnel_gestion-activites-commerciales.pdf), lu le 08/10/2026 ; date d'adoption absente du texte lu |
| Guide CNIL : anonymiser au lieu d'effacer ; pas d'archive « au cas où » ; accès réservé aux personnes habilitées | CNIL, « Guide pratique — Les durées de conservation », « Version juillet 2020 », doc officielle, [PDF](https://www.cnil.fr/sites/default/files/atoms/files/guide_durees_de_conservation.pdf), lu le 08/10/2026 |

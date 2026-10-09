# ADR-027 — réécrit, brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller
> dans le journal de décisions de Confluence, à la place du texte d'ADR-027.
> Rien ne s'écrit sur Confluence depuis ce fichier.
>
> ⚠️ **Le numéro 027 existe déjà** sur Confluence, au statut « proposé » depuis
> le 22/09/2026 (copie du journal du 07/10, ADR-027 du 22/09/2026, en-tête). Cette fiche le
> réécrit. Elle réunit deux sujets du pense-bête : AA, les droits par rôle
> (réponses du groupe du 07/10), et AB, le rôle en lecture seule
> (`md/adr/2026-10-08-proposition-regroupement-adr.md:26`). 🟡 Ce regroupement
> est encore « à faire relire par le groupe » (`md/adr/2026-10-08-notes-seance-adr.md:28`).
>
> 💡 **Rédigé le 2026-10-08 par Claude**, d'après les fichiers du dépôt et le
> sujet. Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Les 9 questions ouvertes du texte du 22/09 sont tranchées. Aucune
> question ne reste ouverte : les cases que rien ne fixait sont des
> propositions de l'équipe, adoptées avec la fiche.
>
> 📎 **La matrice détaillée est en annexe** :
> `md/adr/adr-027-annexe-matrice-detaillee.md` (état au 08/10/2026). La fiche
> garde les principes et un tableau de cinq lignes. ➡️ **Sa place finale** est
> `md/securite/matrice-droits-crud-par-role.md`, à remplacer par l'annexe : une
> tâche pour l'équipe.
>
> 🗂️ **Points réglés hors de la fiche** (ils parlent de la page Confluence ou
> des sources, pas de la décision) :
>
> * **Réécrire un ADR proposé, est-ce permis ?** Le gabarit dit, mot pour mot :
>   « **Ne jamais effacer** un ADR : s'il est remplacé, marquer « remplacé par
>   ADR-XXX ». » (`documents utiles/JOURNAL-DE-DECISIONS.md:72`, StarterPack).
>   Le mot « accepté » n'y est pas. La règle « on ne réécrit jamais un ADR
>   accepté » vient du groupe (ADR-023, Conséquences). ADR-027
>   n'est que proposé : le pense-bête le dit « à réécrire (il n'est que
>   proposé) » (`md/adr/2026-10-07-liste-adr-chantier-4.md:52-54`). 💡 Le texte
>   du 22/09 reste dans l'historique des versions de la page.
> * **« ADR-026 » cité à tort.** La page cite ADR-026 pour « pas
>   d'authentification » (ADR-027 du 22/09/2026, Contexte et Options). Sur
>   Confluence, ADR-026 parle des mots de passe. L'authentification est
>   ADR-028. Cette fiche cite ADR-028.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * `md/securite/matrice-droits-crud-par-role.md` est périmée : « Cette matrice
>   ne sera donc **pas codée** » (l. 9) ; « 18 tables » (l. 129) et 4 rôles
>   (l. 17, l. 66) ; états de facture `invoice_submitted`, `verified`
>   (l. 209-213) ; « Aucun rôle humain ne crée un bien » (l. 237). À remplacer
>   par l'annexe de cette fiche.
> * `docker/init-v3/04_role-lecture-seule.sql:51` donnait à `fil_rouge_reader`
>   `SELECT` sur toutes les tables, mot de passe compris. Corrigé le 2026-10-09
>   (rapport « Rôle lecteur et mots de passe », L1 A, L2 A, L3 A) : le mot de
>   passe est fermé par un droit par colonne, voir Conséquences.
> * « 19 tables » dans `docker/init-v3/README.md:13`, `:133` et `CLAUDE.md:13`,
>   `:25`, `:36`. Le schéma en a 20 depuis `review_media` (compté le
>   08/10/2026 : 20 `CREATE TABLE`).
> * `API/README.md:251` : « Pas d'authentification : le client l'a mise hors
>   périmètre (ADR-026) ». Déjà signalé par ADR-028.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-027 : Qui a le droit de faire quoi — cinq rôles, le rôle puis la ligne, un compte ne se supprime pas

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 22/09/2026 ; réécrit le 08/10/2026 (réponses du groupe : 07/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * l'équipe projet : réponses du 07/10/2026 aux cartes Q-ACC-02 à 07, 10, 12, 13, 15, et aux questions Q7, Q8 et Q14 du plan d'action ; Q-ACC-08 et Q-ACC-09, le 06/10/2026 ;
  * le client (Jeff, formateur jouant le commanditaire et le PO) : « role, droit » dans les outils à fournir (Q-JEF-14), et oui au rôle en lecture seule (Discord, 07/10/2026).
  * **Q-ACC-06, 12 et 13 :** réponses du groupe, **à confirmer par Jeff à la validation de cet ADR (Q-JEF-25)**. Le registre les garde 🟡 (`reg:245`, `:248-249`). Jeff valide les ADR en une séance (`reg:263`).
* **Complète :** ADR-028 (les outils d'authentification). ADR-028 fournit l'outil ; cet ADR en fixe le contenu.
* **S'appuie sur :** ADR-029 (lien chasseur → manager), sans lequel « le manager voit ses chasseurs » ne se calcule pas.
* **Voir aussi :** ADR-049 (effacer un compte), ADR-047 (biens importés ou saisis à la main), ADR-038 (étapes du paiement).
* **Réécrit :** le texte du 22/09/2026 du même ADR, au statut proposé. Ce qui change : des droits **à coder**, et non plus seulement documentés ; **5 rôles** au lieu de 4 ; **20 tables** au lieu de 18.

Abréviations : `01` = `docker/init-v3/01_create_fil_rouge_immobilier.sql` ; `reg` = `md/questions/questions-a-trancher.md` ; `jeff.html` = `md/questions/2026-10-07-questions-pour-jeff.html` ; RCR = `documents utiles/REGLES-CALCUL-REMUNERATION.md` ; F01, F02, F10 = `user-stories/01_…`, `02_…`, `10_….feature` (StarterPack). P1 à P9 et H1 à H13 = les étapes des parcours du particulier et du chasseur (`Readme.md:96-104`, `:123-135`, StarterPack).

**Contexte**

Le 22/09/2026, ADR-027 décrivait un périmètre d'accès « par conception », non codé. Le client avait alors mis l'authentification hors périmètre.

Le 07/10/2026, le client l'a rouverte, côté back. Il demande les outils, dont « role, droit » (Q-JEF-14, ADR-028). Le « qui a le droit de faire quoi » redevient du code.

Le même jour :

* le groupe a répondu aux cartes de droits Q-ACC-02 à 15 (`reg:241-252`) ;
* le groupe a voulu un rôle en lecture seule, à deux niveaux (Q14). Jeff a dit oui sur Discord, « si vous l'expliquez et que ça sert à quelque chose et que c'est cohérent ». Il est posé en base depuis LOT12 (`reg:264`).

Le sujet, lui, n'a pas bougé :

* le RGPD et la note de souveraineté « ne sont **pas optionnelles** ; leur absence est pénalisante en jury » (`Readme.md:266`) ;
* la note doit préciser « le périmètre d'accès (idéalement **lecture seule**) » (`Readme.md:282`) ;
* le principe clé du registre est la minimisation (`REGISTRE-RGPD.md:9`).

Le schéma v3 compte 20 tables et 38 clés étrangères, toutes en `ON DELETE RESTRICT`, aucune en `CASCADE` (`01`, compté le 08/10/2026).

⚠️ L'exigence ENF-03 (« accès restreint au chasseur concerné et à son manager ») ne fonde pas cet ADR. Le sujet la range dans un exemple de cahier des charges, et la cite ailleurs comme une exigence : elle se lit de deux façons (ADR-029). Elle sert seulement pour l'argent (Décision, point 8).

**Options envisagées**

1. **Rester « par conception, non codé »**, comme le 22/09. Avantage : rien à coder. Écartée : le client demande « role, droit » le 07/10.
2. **Contrôler le rôle seul.** Avantage : simple, une règle par rôle. Écartée : deux chasseurs ont le même rôle ; le chasseur A lirait les paiements du chasseur B.
3. **Contrôler le rôle, puis l'appartenance de la ligne**, dans l'API. **Retenue.**

Sous-choix déjà tranché, le rôle en lecture seule (Q14) :

* un rôle PostgreSQL seul : il ne limite pas l'API, qui se connecte en `postgres` (`docker/init-v3/README.md:142`) ;
* un rôle applicatif seul : il ne protège pas les accès directs à la base ;
* **les deux** : retenu par le groupe, accepté par Jeff.

**Décision**

✅ veut dire « établi par une source », pas « codé ». Aucun contrôle de droit n'est codé aujourd'hui (voir Conséquences).

1. ✅ **Cinq rôles**, ceux de la table `role` : `Admin`, `Client`, `Hunter`, `Manager`, `Reader` (`01:164`).
2. ✅ **Deux contrôles**, dans cet ordre. Le rôle : ce type d'utilisateur a-t-il droit à ce type de donnée ? Puis l'appartenance : cette ligne est-elle la sienne ? Ils viennent après la clé d'API du programme appelant (ADR-028).
3. ✅ **La direction, c'est le rôle `Admin`** (déduit, voir Questions tranchées). Il tient aussi la comptabilité et le support de l'exemple du sujet (déduit de même, `REGISTRE-RGPD.md:28-29`).
4. **Supprimer : trois cas.**
   * ✅ **Un compte ne se supprime pas.** L'`Admin` le désactive et le rend anonyme (Q-ACC-08, `reg:183`). Le détail est dans ADR-049.
   * ✅ **Une ligne citée par une autre ne se supprime pas.** La base la refuse : 38 clés en `ON DELETE RESTRICT` sur 38 (`01`, recompté le 08/10/2026).
   * ⚠️ **Une ligne que rien ne cite se supprime encore.** Un compte libre se supprime : réponse 200 (`API/tests/integration/test_users_db.py:89-92`). Cinq tables ne sont citées par aucune clé : `picture`, `review_media`, `estate_proposed`, `visit`, `hunter_performance`.
   * 💡 **Proposition de l'équipe, adoptée avec la fiche : plus aucune route DELETE**, sur les 20 ressources. Le registre ne le demandait que pour les comptes, « ou à justifier » (`reg:303`). Lié à ADR-049. Déduit — demande du code, non fait.
5. ✅ **Trois écritures fermées à tous**, l'`Admin` compris, reprises du texte du 22/09 (ADR-027 du 22/09/2026, Décision, point 6) :
   * `criteria` ne se modifie pas : chaque changement crée une nouvelle version (`01:323-324`) ;
   * `hunter_performance` n'est jamais saisi à la main : le système l'écrit, sur trois déclencheurs (`01:1007-1008`) ;
   * `mandate`, `sale` et `payment` ne s'effacent pas : « documents légaux et traces comptables » (ADR-027 du 22/09/2026, Décision, point 6).
6. ✅ **`Reader` lit, et ne modifie rien.** Dans l'API : « consulter dans l'API sans modifier » (`docker/init-v3/README.md:134`). En base : `fil_rouge_reader`, `SELECT` seul, sur toutes les tables, présentes et futures (`docker/init-v3/04_role-lecture-seule.sql:49-52`).
7. 💡 **Un compte désactivé : ses données personnelles ne sont plus lues que par l'`Admin`.** La CNIL veut des données en attente lisibles par des personnes « spécialement habilitées » seulement (guide CNIL, cité et daté dans ADR-049). Le choix de l'`Admin` est la proposition d'ADR-049.
8. **Le montant de la rémunération** : deux exemples du sujet divergent (✅ sources ci-dessous). ENF-03 : « le montant et l'IBAN ne sont lisibles que par le chasseur concerné et son manager » (RCR:763 ; aussi RCR:296). Le modèle de registre donne les paiements à « comptabilité, direction » (`REGISTRE-RGPD.md:29`). On suit les deux : **le chasseur, son manager, et la direction (`Admin`), qui paie.** Personne d'autre, `Reader` compris. Tranchée par déduction (aucun des deux exemples ne nomme un auditeur). Confirmée par Sébastien le 2026-10-09 (Discord) ; un autre membre du groupe, Gabriel, avait proposé le contraire (Reader voit les paiements) avant ce choix.
9. **Qui lit et qui écrit quoi.** Chaque case, avec sa source et son statut, est dans l'annexe : `md/adr/adr-027-annexe-matrice-detaillee.md` (état au 08/10/2026). En bref :

| Rôle | Lit | Écrit |
|---|---|---|
| `Client` | son compte ; sa demande et ses critères ; son mandat ; les biens proposés pour lui, et leurs avis ; ses visites ; sa vente | crée son compte et sa demande ; signe son mandat ; commente, priorise, fait une offre |
| `Hunter` | ses clients, demandes, critères, mandats, visites, ventes, paiements ; sa note ; les biens ; son barème et les réglages du calcul | accepte ou refuse une demande ; crée un mandat, une version des critères, une sélection, un avis, une visite ; saisit un bien |
| `Manager` 💡 | le travail de son équipe : chasseurs, demandes, critères, mandats, visites, ventes, paiements, notes ; les biens | affecte une demande ; enregistre une vente ; saisit un bien |
| `Admin` | tout, sauf le mot de passe | les comptes (créer, désactiver, rendre anonyme) ; honoraires et barèmes ; réglages du taux 💡 ; étapes du paiement 💡 |
| `Reader` 💡 | tout, sauf le mot de passe, les paiements et les comptes désactivés | rien |

10. 💡 **Propositions de l'équipe, adoptées avec la fiche.** Ni le sujet ni le groupe ne fixaient ces cases. Jeff valide les ADR en une séance (Q-JEF-25, `reg:263`) : elles passent avec cette fiche.
    * **Manager :** il lit le travail de son équipe, pas l'identité des clients. Il lit `hunter`, `search_request`, `criteria`, `mandate`, `visit`, `sale`, `payment`, `hunter_performance`, et les biens (`estate`, `picture`). Il ne lit pas `client`, `estate_proposed`, `estate_searchrequest`, `review_media`. Cela suffit pour affecter une demande (Q-ACC-10), enregistrer une vente (Q-ACC-03), voir les paiements (Q-ACC-02) et lire les visites (Conséquences). L'équipe se calcule par `hunter.id_realestatemanager` (`01:296-297`) et `search_request.id_realestatemanager` (`01:317-318`).
    * **Paiement :** il est créé par le calcul, jamais saisi à la main. Le sujet place l'insertion dans une couche au-dessus du calcul : elle « insère le `Remuneration` dans `paiements` » (RCR:760). L'`Admin` lance ce calcul quand l'entreprise a reçu les honoraires (H10, `Readme.md:132`). Puis il fait avancer le paiement : programmé, payé (ADR-038).
    * **`Reader` :** il lit par l'API toutes les tables, sauf le mot de passe (jamais renvoyé, `API/src/app/models/user_model.py:35-46`), les paiements (point 8) et les comptes désactivés (point 7). Son usage écrit : « un auditeur ou le client qui suit l'avancement » (`docker/init-v3/README.md:139`). Une IA ne reçoit pas ce rôle : elle lit l'OLAP anonymisé (`SOUVERAINETE-SECURITE-IA.md:16`).

**Justification**

* Le client demande des outils de « role, droit » (Q-JEF-14). Une matrice non codée ne les fournit pas.
* Le second contrôle est celui qui manque le plus souvent. Sans lui, un rôle partagé ouvre les lignes de tous ses membres.
* La minimisation est un principe du règlement, cité par le sujet (`REGISTRE-RGPD.md:9`). Chaque rôle lit ce que son parcours demande. Exemple : le manager voit le travail de son équipe, pas la date de naissance d'un client. Le modèle du sujet donne les données du mandat au « chasseur affecté, direction » (`REGISTRE-RGPD.md:27`).
* Les parcours du sujet disent qui écrit. Ils ne disent jamais qui lit. Les réponses du groupe du 07/10 comblent l'essentiel ; le reste est proposé, et dit comme tel.
* Le rôle en lecture seule répond à « idéalement **lecture seule** » (`Readme.md:282`). C'est le moindre privilège (`docker/init-v3/README.md:138`).
* Un compte ne se supprime pas : c'est le choix du groupe (Q-ACC-08), pas une limite de la base. La base ne refuse que les lignes citées par une autre. Le texte du 22/09 le disait déjà : « Toute ligne reliée à une autre est déjà inaccessible à un `DELETE` » (ADR-027 du 22/09/2026, Décision, point 5).
* La matrice détaillée va en annexe : le modèle du sujet veut « une fiche courte par décision » (`JOURNAL-DE-DECISIONS.md:7`). Le texte du 22/09 l'annexait déjà (ADR-027 du 22/09/2026, Décision, point 8).

**Conséquences**

* **Code :** aucun contrôle de droit dans `API/` aujourd'hui. Recherche du 08/10/2026 sur `require_role`, `get_current_user`, `APIKeyHeader`, `anonym` dans `API/src` : 0 occurrence. Les contrôles se branchent sur la fabrique commune `build_crud_router` (`md/securite/tuto-2-authentification-jwt.md:387-409`). À coder.
* **Routes DELETE :** les 20 routeurs ont une route DELETE (`API/src/app/routes/crud_router.py:104-110`). Elles contredisent le point 4 pour les comptes. Les fermer est proposé (point 4) ; leurs tests (`test_users_db.py:89-104`) seront alors à réécrire (ADR-049). Demande du code, non fait.
* **`POST /hunter-performances` est ouvert** : il contredit le point 5 (ADR-035, Conséquences).
* **Conflit d'intérêts sur les visites :** le chasseur enregistre la visite (Q-ACC-13), et moins de visites donne une meilleure note (ADR-048). La carte le disait : « Il a intérêt à ne pas tout déclarer » (`jeff.html:1649`). 💡 Contre-pouvoir : le client lit ses visites, le manager celles de son équipe.
* **Limite du rôle PostgreSQL :** `fil_rouge_reader` lit toutes les tables (`04_role-lecture-seule.sql:51`). Depuis le 2026-10-09, il ne lit plus `"user".password` : la table est rouverte colonne par colonne, sans le mot de passe (`04_role-lecture-seule.sql`, fin du fichier ; migration `18_role-lecture-seule-sans-mot-de-passe.sql` pour une base déjà créée). Il lit encore les paiements et les comptes désactivés : plus que `Reader` dans l'API (points 8 et 10) ; question à part, non tranchée. `SELECT *` sur `"user"` lui est refusé. Correctif écrit mais pas encore exécuté (Docker arrêté le 2026-10-09).
* 💡 **Pour une IA ou une analyse :** lire une copie anonymisée (OLAP), pas la base de production, comme le dit le sujet (`documents utiles/SOUVERAINETE-SECURITE-IA.md:16`, StarterPack). Non décidé ici.
* **Comptes désactivés en attente d'anonymisation :** traités dans ADR-049.
* **Barème propre à un chasseur** (Q-PAR-09, décision D9 du sujet) : il va dans la RACI, pas ici (`reg:427` ; RCR:329).
* **Livrables :** la matrice nourrit la note « souveraineté & sécurité des données » et le registre RGPD.
* **À l'oral :** « Le RGPD est une exigence explicite du sujet. Nous appliquons la minimisation. Le qui-voit-quoi vient des réponses du groupe et du client ; le reste est proposé, et chaque case dit sa source. »

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Quels rôles ? | Les 5 de la base. `Reader` : « consulter dans l'API sans modifier » | `01:164` ; `docker/init-v3/README.md:134` |
| Qui est « la direction » ? | `Admin`, déduit. Les rôles sont fixés par un `CHECK`. La direction n'est pas le manager : Q-PAR-09 est passée « du manager » à « la direction ». Ni client, ni chasseur, ni lecteur. Et le groupe confie déjà à l'admin des tâches de direction (anonymiser, lancer l'import). Un 6e rôle demanderait de changer le `CHECK` : personne ne l'a demandé. Comptabilité et support, absents des rôles, vont à l'`Admin` de même (déduit) | `01:164` ; `reg:246`, `:251`, `:183-184` ; `REGISTRE-RGPD.md:28-29` |
| Que voit le manager ? | Ses chasseurs et leurs paiements. Il enregistre la vente, affecte la demande, peut saisir un bien. Le reste de sa colonne : proposition de l'équipe (Décision, point 10) | Q-ACC-02, 03, 10 (`reg:241-242`, `:247`) ; Q8 (`reg:252`) |
| Le client voit-il tout le catalogue ? | Non : les biens proposés pour lui | Q-ACC-05 (`reg:244`) ; P4 (`Readme.md:99`) |
| Le chasseur voit-il son barème ? | Oui, le barème par défaut et le sien. À confirmer par Jeff à la validation de cet ADR (Q-JEF-25). Appui du sujet : « Afin que chaque chasseur puisse vérifier son montant » | Q-ACC-06 (`reg:245`) ; `F10:11` ; `01:787-788` (`id_hunter` vide = barème par défaut) |
| Les réglages du taux et les honoraires, le chasseur les lit-il ? | Oui, tranchée par déduction : vérifier son montant demande toutes les entrées du calcul | `F10:11` |
| Qui crée le compte client ? | Le client. À confirmer par Jeff à la validation de cet ADR (Q-JEF-25). Appui du sujet : « Quand je finalise la création de mon compte […] Alors mon compte est activé » | Q-ACC-12 (`reg:248`) ; `F01:25-28` ; P2 (`Readme.md:97`) |
| Qui enregistre une visite ? | Le chasseur. À confirmer par Jeff à la validation de cet ADR (Q-JEF-25). Appui partiel du sujet : il visite les biens choisis | Q-ACC-13 (`reg:249`) ; H6 (`Readme.md:128`) ; P5 (`Readme.md:100`) ; `F02:17`, `:22` |
| Un chasseur peut-il créer une demande ? | Oui, seulement pour un client qui a déjà un compte | Q-ACC-15 et Q7 (`reg:250` ; `md/journal/2026-10-07-plan-action.html`, carte Q7) |
| Qui fixe barèmes et honoraires ? | La direction seule. Les réglages du taux (`hunter_rate_parameters`) : la même règle, par analogie, 💡 (comme ADR-034) | Q-ACC-07 (`reg:246`) ; ADR-034, bandeau |
| Qui fait avancer la facture ? | Sans objet : la facture est hors périmètre. Le paiement n'a plus d'état de facture | Q-ACC-04 (`reg:243`) ; `01:884-886` ; ADR-038 |
| L'import des biens tourne sous quel compte ? | Lancé par l'admin (ADR-047), joué sous le compte PostgreSQL du conteneur, pas par l'API. Le bien importé n'a pas d'auteur. Saisi à la main : le chasseur ou le manager, auteur noté | Q-ACC-09 (`reg:184`) ; ADR-047 ; `01:624-629` ; Q8 (`reg:252`) |
| La priorité du client (D6) ? | Une colonne de 1 à 5 sur le bien proposé, donnée par le client | `01:706-709` ; H6 (`Readme.md:128`, « commenté et priorisé ») |
| Désactiver plutôt que supprimer ? | Oui, pour un compte. Les autres lignes : Décision, point 4 | Q-ACC-08 (`reg:183`) ; ADR-049 |
| Son propre compte ? | Chacun lit et corrige le sien. Le rôle et l'activation, seul l'`Admin` les change. Tranchée par déduction — à confirmer par le groupe | `REGISTRE-RGPD.md:38` (« consulter, corriger ») ; Q-ACC-08 ; moindre privilège, `docker/init-v3/README.md:138` |
| Un rôle en lecture seule ? | Les deux niveaux, oui de Jeff, posé à LOT12 | `reg:264` ; `docker/init-v3/README.md:125-153` |
| Qui crée un barème propre à un chasseur ? | Pas ici : dans la RACI | `reg:251`, `:427` ; RCR:329 |

**Questions ouvertes** 🟡

Aucune. Ce qui reste est du code à écrire (Conséquences) et la confirmation de Q-ACC-06, 12 et 13 par Jeff à la validation (Décideurs).

Où l'on a cherché, pour les cases du point 10 : les parcours (`Readme.md:94-135`) ; les acteurs du glossaire (ni direction ni manager) ; `RACI.md` (un modèle de cours, sans ces rôles) ; `REGISTRE-RGPD.md:27-29` ; le registre (`reg:241-264`, `:1028-1065`) ; la carte Q-JEF-14 (`jeff.html:1440-1470`) ; la matrice du 02/10 (§ 6) ; ADR-038, qui renvoie ici « qui crée le paiement et le fait avancer » (`md/adr/adr-038-etapes-du-paiement-sans-facture.md:17-19`). Le sujet ne décrit ni le travail du manager ni celui de la direction.

**Sources**

| Affirmation | Source |
|---|---|
| Texte du 22/09/2026, « ADR-026 » cité à tort | journal de décisions Confluence, lu dans sa copie du 07/10/2026 : ADR-027 du 22/09/2026, Contexte et Options |
| Texte du 22/09 : « Toute ligne reliée à une autre » ; trois écritures fermées ; matrice annexée | ADR-027 du 22/09/2026, Décision, points 5, 6 et 8 |
| Réécrire : ADR-027 n'est que proposé | `md/adr/2026-10-07-liste-adr-chantier-4.md:52-54` |
| « Ne jamais effacer un ADR » ; « une fiche courte par décision » | `documents utiles/JOURNAL-DE-DECISIONS.md:72`, `:7` (StarterPack) |
| « on ne réécrit jamais un ADR accepté » (groupe) | journal de décisions Confluence, ADR-023, Conséquences |
| AA + AB réunis dans ADR-027 ; regroupement à faire relire | `md/adr/2026-10-08-proposition-regroupement-adr.md:26` ; `md/adr/2026-10-08-notes-seance-adr.md:28` |
| Réponses du groupe du 07/10 (Q-ACC-02 à 15, Q8) | `md/questions/questions-a-trancher.md:241-252` |
| Q-ACC-08 (comptes) ; Q-ACC-09 (l'admin lance l'import) | même fichier, l. 183, l. 184 |
| Route DELETE : « à retirer pour les comptes, ou à justifier » | même fichier, l. 303 |
| Rôle en lecture seule : Q14, oui de Jeff, LOT12 | `questions-a-trancher.md:264` ; `docker/init-v3/README.md:125-153` |
| Usage écrit de `Reader` ; moindre privilège ; l'API se connecte en `postgres` | `docker/init-v3/README.md:139`, `:138`, `:142` |
| Jeff : « role, droit » (Q-JEF-14) | `md/questions/2026-10-07-questions-pour-jeff.html`, carte Q-JEF-14 ; ADR-028 |
| Jeff valide les ADR en une séance | `questions-a-trancher.md:263` |
| 5 rôles | `docker/init-v3/01_create_fil_rouge_immobilier.sql:164` |
| 20 tables, 38 clés `RESTRICT`, 0 `CASCADE` ; 5 tables citées par aucune clé | même fichier, compté le 08/10/2026 |
| Un compte libre se supprime (200) ; un compte cité, 409 | `API/tests/integration/test_users_db.py:89-92`, `:95-104` |
| `fil_rouge_reader` : `SELECT` sur toutes les tables | `docker/init-v3/04_role-lecture-seule.sql:49-52` ; `"user"` sans `password` (fin du fichier) |
| L'API ne renvoie jamais le mot de passe | `API/src/app/models/user_model.py:35-46` |
| Comptes repris : mot de passe factice | `API/src/app/utils/security.py:41-43` ; `docker/init-v3/README.md:322-328` |
| Critères versionnés | `01:323-324` ; `GLOSSAIRE-METIER.md`, « Version de demande » (StarterPack) |
| Journal des notes, trois déclencheurs | `01:1002-1021` |
| Biens importés sans auteur | `01:624-629` |
| Barème par défaut ou propre au chasseur | `01:787-788` |
| Priorité du client | `01:706-709` |
| États du paiement | `01:884-886` |
| Lien chasseur → manager ; demande → manager | `01:296-297`, `:317-318` ; ADR-029 |
| Parcours du particulier et du chasseur | `Readme.md:96-104`, `:123-135` (StarterPack) |
| RGPD et souveraineté « pas optionnelles » ; « idéalement lecture seule » | `Readme.md:266`, `:282` (StarterPack) |
| Minimisation ; données du mandat, des comptes, des paiements : qui y accède ; droits des personnes | `documents utiles/REGISTRE-RGPD.md:9`, `:27-29`, `:38` (StarterPack) |
| ENF-03 : « le montant et l'IBAN ne sont lisibles que par le chasseur concerné et son manager » | RCR:763 ; RCR:296 (StarterPack) |
| Le calcul est inséré dans `paiements` par une couche au-dessus | RCR:760 (StarterPack) |
| « vérifier son montant » | `user-stories/10_calcul_remuneration_chasseur.feature:11` (StarterPack) |
| Le client finalise son compte | `user-stories/01_particulier_demande_et_compte.feature:25-28` (StarterPack) |
| L'IA lit un OLAP anonymisé | `documents utiles/SOUVERAINETE-SECURITE-IA.md:16` (StarterPack) |
| Conflit d'intérêts sur les visites | `jeff.html:1649` |
| Aucun contrôle de droit codé | recherche du 08/10/2026 dans `API/src` : 0 occurrence |
| Routes DELETE sur 20 routeurs | `API/src/app/routes/crud_router.py:104-110` ; 20 fichiers de `API/src/app/routes/` |
| Où brancher les contrôles | `md/securite/tuto-2-authentification-jwt.md:387-409` |
| Paiement : renvoyé à ADR-027 | `md/adr/adr-038-etapes-du-paiement-sans-facture.md:17-19` |
| Réglages du taux : analogie, 💡 | `md/adr/adr-034-parametres-remuneration-table-datee.md:33-37` |
| Barème nominatif : RACI | `questions-a-trancher.md:427` ; RCR:329 (StarterPack) |
| Compte désactivé : personnes « spécialement habilitées » | guide CNIL « Les durées de conservation », lien et date dans ADR-049, Sources |
| Matrice détaillée | `md/adr/adr-027-annexe-matrice-detaillee.md` (état au 08/10/2026) |

# ADR-046 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 046 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:69`,
> groupe 2). Il réunit la lettre U du pense-bête (`md/questions/questions-a-trancher.md:416`)
> et la ligne AC (`:423`), qui « peut rejoindre l'ADR U ». C'est le
> regroupement 3 de la même proposition (l. 25) : les deux parlent de données
> reprises.
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt et le
> sujet.** Chaque chiffre est recompté le 08/10/2026 dans le texte des scripts
> SQL, pas dans une base. Relu le 08/10/2026 par deux relecteurs (sources ; oral
> et jury) et un arbitre. Aucune question ne reste ouverte.
>
> ⚖️ **Tranché par l'arbitre** : ADR-018 (accepté, 07/09/2026) demande
> `energy_class_scheme = 'FR-DPE-2021'` à la migration. Aucun ADR ne l'a
> remplacé, et la carte Q-MIG-05 ne nomme pas cette colonne. ADR-018 s'applique :
> c'est du code à écrire, pas une question (voir Questions tranchées et
> Conséquences).
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * Les commentaires qui disent les quatre autres colonnes d'énergie toutes
>   vides : `docker/init-v3/01_create_fil_rouge_immobilier.sql:572-574`,
>   `03_populate_estate.sql:9-10`, `docker/init-v3/README.md:82`. À aligner
>   quand `energy_class_scheme` sera rempli.
> * « 17 » au lieu de 18 (critères, demandes, mandats, depuis LOT10) :
>   `docker/init-v3/02_migration.sql:16` et `:53` ; `docker/init-v3/README.md:74`,
>   `:76`, `:259` (§3.2), `:406-408` (table des comptes) ; registre `:182`.
>   `README.md:401` dit 4 rôles : 5 depuis LOT12.
> * `README.md:62` : valeurs factices « à remplacer quand Jeff fournit les
>   vraies (Q-JEF-26) ». Il ne les fournira pas : les manques sont voulus.
> * `README.md` §7, points 2 et 3 (l. 454-455), et §3.3, §3.4 : encore « à
>   trancher », « à confirmer ». Jeff a validé (Q-JEF-12, Q-JEF-10 ; registre
>   `:231`, `:235`).
> * `API/src/app/models/search_request_model.py:27-28` : « Les demandes migrees
>   valent 'confirmed', hypothese a confirmer ». C'est `'launched'` depuis LOT10.
> * `md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md:84` et
>   `:137` : « le projet passe par un faker de données plutôt que par la
>   migration du legacy ». Faux : l'ancienne base est migrée, et `hire_date`
>   est une hypothèse de reprise (Q-REM-16).
> * ADR-018 écrit `energy_kwh_m2 >= 0`, `ges_kg_co2_m2` et `>= 0`. Le schéma a
>   `energy_kwh_m2 > 0`, `energy_co2_m2` et `> 0`
>   (`docker/init-v3/01_create_fil_rouge_immobilier.sql:578-579`). Hors de cet
>   ADR.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-046 : Données reprises — vide si la colonne l'accepte, sinon une valeur factice documentée ; la source jamais touchée ; les anciens mandats repris à la date de l'audit

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions : 06/10/2026 pour Q-MIG-06 et Q-MIG-09 ; 07/10/2026 pour la Q4 du groupe, les réponses de Jeff et la mise en œuvre à LOT10)
* **Statut :** proposé
* **Décideurs :**
  * Jeff, client et PO (Q-PRO-01), entretien du 07/10/2026 : Q-JEF-26 (« les manques sont voulus ») et Q-JEF-13 (« oui à nos positions ») ;
  * l'équipe projet : réponse à la Q4 du plan d'action (07/10/2026) ; Q-MIG-06 et Q-MIG-09 (06/10/2026) ; Q-MIG-10, Q-MIG-12, Q-MIG-13, posées à Jeff ; ADR-018 (accepté, 07/09/2026) pour `energy_class_scheme` ;
  * Sébastien, pour la mise en œuvre à LOT10 (07/10/2026) : demandes en `'launched'`, échus comptés au 25/07/2026, mandat 13 repris avec sa demande et son critère (cartes F6, F7, F8).
* **Remplace :** aucun ADR.
* **Complète :** ADR-007 (accepté) : la reprise respecte son téléphone obligatoire, au format international.
* **S'appuie sur :** ADR-018 (accepté), pour `energy_class_scheme` : il reste en vigueur (voir Questions tranchées).

**Contexte**

Deux sources de données sont reprises :

* l'ancienne base du sujet, `fixtures/PgSQL.sql` : 24 utilisateurs (6 chasseurs, 18 clients), 18 mandats, 10 secteurs (`PgSQL.sql:167-170`) ;
* les annonces, `annonces_normalised.csv` : 2 556 biens (`docker/init-v3/03_populate_estate.sql:3`).

Elles ont des trous :

* 3 clients sans téléphone : « Certains clients n'ont pas de téléphone (NULL) » (`PgSQL.sql:88`, `:94`, `:100`, `:106`). La cible exige un téléphone (`phone_number NOT NULL`, ADR-007 ; `01:205`).
* Un seul budget par client, le maximum (`PgSQL.sql:71`).
* Une lettre DPE pour une partie des biens seulement ; aucune autre donnée d'énergie.
* Aucune adresse ni code postal de client (traité par ADR-043).

Les mandats posent trois problèmes :

* 4 statuts à la source : `'actif', 'suspendu', 'termine', 'expire'` (`PgSQL.sql:26`). La cible en a 7, sans « suspendu » (`01:446-449`).
* Le consultant demande : « combien de mandats "actif" ont en réalité dépassé leurs 6 mois de validité au 25/07/2026 ? » (`PgSQL.sql:172-175`). Le groupe en compte 6 : « le piège du consultant » (`md/journal/2026-09-21-point-etape.md:240-243`).
* Le mandat 13 a pour client l'utilisateur 3, « un CHASSEUR » (`PgSQL.sql:148-153`). La v2 l'avait écarté.

Le 07/10/2026, Jeff répond : « les manques sont voulus. Ne pas supprimer les anciennes données ; on peut fausser les autres (modifier le script fourni) » (`md/questions/2026-10-07-questions-pour-jeff.html:1428`).

**Options envisagées**

A. Les données qui manquent (Q4 du plan d'action, `md/journal/2026-10-07-plan-action.html:384-394`)

1. **Modifier le script du sujet.** Avantage : « La migration reste simple. » Inconvénient : « L'audit ne peut plus montrer les trous ; une mise à jour du sujet écrase nos changements. » **Écartée.**
2. **Une valeur inventée partout, dans notre migration.** Avantage : « Aucune case vide. » Inconvénient : « un faux budget se lit comme un vrai ». **Écartée.**
3. **Ne jamais toucher le script du sujet** ; vide si la colonne l'accepte, valeur factice documentée sinon. Avantage : « La source reste intacte pour l'audit ». Inconvénient : « Deux façons d'écrire « inconnu », à expliquer dans le README. » **Retenue** (registre `:240`).

B. Les mandats « actif » déjà finis (Q-MIG-10, `2026-10-07-questions-pour-jeff.html:1374-1375`)

1. **Les garder `'active'`, comme constat d'audit.** Inconvénient : « Statut faux en base. » **Écartée.**
2. **Les passer en `'expired'`.** Inconvénient : « On tranche à la place du client. » Levé : Jeff confirme. **Retenue.**

Pour la date de référence (carte F7, `md/journal/2026-10-07-rapport-final-chantier-lot.html:576-582`) : la date du jour est **écartée**, le 25/07/2026 **retenu**.

C. Le mandat 13 (Q-MIG-12, `2026-10-07-questions-pour-jeff.html:1394-1395`)

1. **Le laisser ignoré**, comme en v2. Inconvénient : « Un mandat perdu. » **Écartée.**
2. **Demander à Jeff si c'est Nina Girard**, puis le rattacher. Avantage : « Mandat peut-être récupéré. » Inconvénient : « Attente. » **Retenue** ; Jeff dit oui.
3. Un compte à part (note du groupe : « compte séparé ? »). **Écartée** : Nina Girard est déjà cliente (registre `:237`).

D. « suspendu » et le statut des demandes (Q-MIG-13, Q-MIG-03)

1. **Un nouvel état** (pause, suspendu). **Écartée** : « pas de pause, pas de nouvel état » (Jeff, Q-JEF-13).
2. **`suspendu` → `'canceled'`.** **Retenue.**
3. Pour les demandes (fiche Q-MIG-03, `md/questions/questions-a-trancher.html:1482-1484`) : garder `'confirmed'`, **écartée** (des demandes sous mandat signé resteraient « confirmées ») ; `'launched'` seulement au mandat signé, **écartée** ; `'launched'` pour toute demande qui a un mandat, **retenue** (F6).

**Décision**

Partie 1 — Les données qui manquent

1. ✅ Le script du sujet, `fixtures/PgSQL.sql`, ne se touche jamais. Tout se règle dans notre migration (`docker/init-v3/02_migration.sql`, `03_populate_estate.sql`).
2. ✅ Une donnée absente de la source reste vide (`NULL`) si la colonne l'accepte. Vide veut dire « inconnu ».
3. ✅ Si la colonne refuse le vide, elle reçoit une valeur factice. La valeur respecte le format de la colonne. Elle est documentée : un commentaire dans le script, une ligne dans `docker/init-v3/README.md` §0.
4. ✅ Aucune donnée ancienne n'est supprimée (Jeff, Q-JEF-26).
5. ✅ Pour tester les contraintes, un faker forké du script du sujet servira (registre `:240`). Il **devra** s'écrire : aucun faker n'existe dans le dépôt.

Ce que cela donne, colonne par colonne :

| Donnée | Colonne | Vide permis ? | Repris | Compté (08/10/2026) | Carte |
|---|---|---|---|---|---|
| Lettre DPE | `estate.energy_class` | oui (`01:575`) | la lettre du CSV, vide sinon | 1 623 lettres, 933 vides, sur 2 556 | Q-MIG-06 |
| Référentiel de la lettre | `energy_class_scheme` | oui (`01:576`) | `'FR-DPE-2021'` si le bien a une lettre ; vide sinon (déduit) | 0 rempli : absente des `INSERT` de `03`. ➡️ à coder : 1 623 | ADR-018 |
| Autres données d'énergie | `energy_class_date`, `energy_kwh_m2`, `energy_co2_m2` | oui (`01:577-579`) | vide | 0 rempli : absentes des `INSERT` de `03` | Q-MIG-05 ; ADR-018 |
| Ancien score d'énergie | `energetic_score` | — | colonne retirée ; elle était vide sur les 2 556 biens | — | Q-MIG-05 |
| Budget minimum | `criteria.budget_min` | oui (`01:353`) | vide | 18 sur 18 | Q-MIG-09 |
| Téléphone | `phone_number` de `client`, `hunter`, `real_estate_manager` | non (`01:205`, `:254`, `:276`) | `+33000000000` | 4 : 3 clients (Petit, Andre, Lambert) et le manager fictif | Q-MIG-07 |

Comptes : `03_populate_estate.sql` (2 556 `INSERT INTO estate`) ; `02_migration.sql:132`, `:158`, `:164`, `:170` (téléphones) ; `:208-228` (18 critères).

Partie 2 — Les anciens mandats

6. ✅ Les statuts se traduisent : `actif` → `'active'`, `termine` → `'completed'`, `expire` → `'expired'`, `suspendu` → `'canceled'`. Pas de pause, pas de nouvel état (Q-MIG-13, Q-MIG-03 ; Jeff, Q-JEF-13).
7. ✅ Un mandat `actif` déjà fini au 25/07/2026 passe en `'expired'` (Q-MIG-10 ; Jeff, Q-JEF-13). Fini veut dire : `date_debut + 6 mois` avant cette date (`PgSQL.sql:174`). Ils sont 6 : `MAND-0004`, `0007`, `0009`, `0010`, `0011`, `0012`. La date est fixe : le résultat ne dépend pas du jour de la migration (F7).
8. ✅ Le mandat 13 se rattache à Nina Girard (user 19), déjà cliente, avec sa demande et son critère. Pas de compte en plus (Q-MIG-12 ; Jeff, Q-JEF-13 ; F8).
9. ✅ Une demande qui a un mandat passe en `'launched'` : à la signature, « ma recherche est officiellement lancée » (`01_particulier_demande_et_compte.feature:37` ; Q-MIG-03 ; F6). Les quatre statuts de la demande sont l'objet d'ADR-041.

Ce que cela donne :

| | Source (`PgSQL.sql:169`) | Base (`02_migration.sql:238-255`, `:275-277`) |
|---|---|---|
| Mandats | 18 : 11 actif, 3 termine, 2 expire, 2 suspendu | 18 : 5 `'active'`, 3 `'completed'`, 8 `'expired'`, 2 `'canceled'` |
| Demandes | — | 18, insérées en `'confirmed'`, puis toutes `'launched'` |
| Critères | — | 18 |

Les 8 `'expired'` : les 6 mandats `actif` finis, plus les 2 déjà `expire` à la source (`MAND-0002`, `MAND-0006` ; `PgSQL.sql:137`, `:141`).

Partie 3 — Rangé ailleurs, pas redécidé ici

* L'adresse `'non renseigné'` et le code postal `'00000'` des 18 clients : ADR-043.
* Les 10 secteurs, devenus la localisation des critères : ADR-031.
* Le mot de passe fictif des 25 comptes : ADR-028.
* Le manager fictif (user 25) : ADR-029 ; le seed le remplacera (Q-MIG-04, registre `:179`).
* `hire_date` = date de création du compte : hypothèse validée par Jeff (Q-REM-16, Q-MIG-02, Q-JEF-10 ; registre `:231`).
* Le taux de commission de la source : « % des honoraires, non migré » (Q-MIG-01, Q-JEF-12 ; registre `:235`).

**Justification**

* **Un trou visible vaut mieux qu'une fausse valeur.** Une fausse lettre DPE sortirait dans une recherche « DPE C max » (registre `:285`). Un faux budget « se lit comme un vrai » (plan d'action, Q4).
* **Les colonnes chiffrées d'énergie refusent 0** (`CHECK > 0`, `01:578-579`). Un faux nombre positif « se lirait comme une vraie mesure » (registre `:280`).
* **La source intacte garde la preuve des trous**, pour l'audit (plan d'action, Q4). « Un seed ne doit pas les cacher » (`2026-09-21-point-etape.md:233`).
* **Le téléphone reste exigé des nouveaux comptes.** Rendre la colonne facultative l'aurait ôté à tous (registre `:294`).
* **Le 25/07/2026 donne la même base à tous** : « Le résultat ne dépend pas du jour où on lance la migration » (F7). C'est aussi la date de référence du projet (`MODELE-SWOT.md:26`).
* **Le mandat 13 :** « Aucune ligne de la source n'est perdue ; aucun compte inventé » (F8).
* **`'launched'` :** « L'état dit la vérité : la chasse a commencé » (F6).

**Conséquences**

* ✅ **Déjà fait dans le code**
  * Base neuve : `docker/init-v3/02_migration.sql` (en-tête l. 43-63) et `03_populate_estate.sql` (en-tête l. 8-11).
  * Base existante : `docker/migrations/v2-vers-v3/07_personnes.sql` (téléphones, l. 94-96), `09_biens.sql` (lettres DPE), `10_reprise-mandats.sql` (mandats, l. 89-97).
  * La migration s'arrête plutôt que d'inventer : « si un téléphone ou une adresse ne se complète pas sans inventer une donnée » (`README.md:68`) ; « si Nina n'est pas cliente, ou si l'id 13 est pris par un autre client » (`README.md:94`).
  * « Aucune ligne n'est supprimée » (`10_reprise-mandats.sql:39-40`).
  * Test : `+33000000000` passe le contrôle du téléphone (`API/tests/integration/test_constraints_db.py:183`).
  * Doc : `docker/init-v3/README.md` §0, LOT7 à LOT10 (l. 60-94).
* ⚠️ **Deux façons d'écrire « inconnu »** : `NULL`, ou une valeur factice (`'+33000000000'`, et pour l'adresse `'non renseigné'`, `'00000'`). Une statistique doit écarter les deux.
* ⚠️ **La base ne réserve pas `+33000000000` aux comptes repris.** Un nouveau compte peut l'écrire : le test l'accepte. Même limite que l'adresse (ADR-043, Conséquences).
* ⚠️ **Le statut « suspendu » ne vit plus qu'à la source**, intacte : `MAND-0008` et `MAND-0016` sont `'canceled'` en base.
* ⚠️ **Une recherche finie reste `'launched'`** : il n'y a pas d'état « terminée » (F6 ; ADR-041).
* ➡️ **Reste à coder dans l'API : faire expirer un mandat fini.** Déduit — demande du code, non fait.
  * `MAND-0013`, `0014` et `0015` sont finis depuis : le 10/08, le 01/09 et le 25/09/2026. Ils restent `'active'` : « les faire expirer revient à l'application » (`02_migration.sql:236-237`, `:250-252`).
  * Le quoi est fixé par le sujet. Quand « la date de fin de validité du mandat (signature + 6 mois) est atteinte » sans vente, le chasseur est invité à renouveler, et ses indicateurs sont « recalculés à la baisse » (`07_chasseur_remuneration_et_performance.feature:38-41`, parcours `@actuel` ; `Readme.md:135`). Le mandat passe en `'expired'`, ou il est renouvelé (`00_…feature:40` ; ADR-050).
  * Ce n'est donc pas une limite assumée : le sujet le demande (ADR-045 ne la range pas).
  * L'expiration écrit une note `'mandate_expired'`, une seule par mandat (`uq_perf_mandate`, `01:1020` ; ADR-042 ; C6, `09-contraintes-a-coder.md:190`, `:217-219`). La baisse elle-même relève d'ADR-048 (ADR-050, Conséquences).
  * Le comment se choisit en codant. 💡 Piste : une opération du service des mandats passe en `'expired'` tout mandat `'active'` dont `ends_at` est passée ; une route réservée au manager l'appelle ; rejouée, elle ne change rien de plus ; un test d'intégration la couvre. La règle se range avec les règles du mandat (ADR-039).
  * Aujourd'hui, `MandateService` n'a aucune règle (`API/src/app/services/mandate_service.py:1-8`).
* ➡️ **Reste à coder : `energy_class_scheme = 'FR-DPE-2021'`** sur les 1 623 biens qui ont une lettre (ADR-018). ✅ Confirmé par le groupe le 09/10/2026 (S11). Déduit — demande du code, non fait. Une ligne dans `03_populate_estate.sql` pour une base neuve ; une dans `docker/migrations/v2-vers-v3/09_biens.sql` pour une base v2 ; un test.
* ➡️ **Reste à écrire : le faker forké** du script du sujet, pour tester les contraintes.
* **Soutenance**
  * « Comment migrez-vous sans perdre de données ? » (`TRAME-SOUTENANCE.md:32`). 💡 Réponse : la source reste intacte. Ses 24 utilisateurs et ses 18 mandats sont repris, le mandat 13 compris. Chaque trou est compté et documenté.
  * « Comment garantissez-vous l'intégrité (ex. qu'un client ne soit pas un chasseur) ? » (`:29`). 💡 Réponse : le mandat 13. En v3, `mandate.id_client` pointe vers `client(id_user)` (`01:461-462`). Un chasseur sans fiche client ne peut plus être client d'un mandat.
  * Les 6 mandats échus sont un constat d'audit, pour le livrable 1 (`2026-09-21-point-etape.md:242-243`).

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Pourquoi le 25/07/2026, et pas la date du jour ? | C'est la date de référence du projet, et celle de la question du consultant. Jeff confirme « les 6 échus » : 6 est le compte à cette date. Au 08/10/2026, ce serait 9. | `MODELE-SWOT.md:26` ; `PgSQL.sql:167`, `:172-175` ; `2026-10-07-questions-pour-jeff.html:1349` ; déduit des fins `02_migration.sql:250-252` |
| Le total en `'expired'` est-il 6 ? | Non, 8 : les 6 échus, plus les 2 mandats déjà `expire` à la source. | compté dans `02_migration.sql:238-255` ; `PgSQL.sql:137`, `:141` |
| Faut-il demander les données manquantes à Jeff ? | Non : les manques sont voulus. | Q-JEF-26, `2026-10-07-questions-pour-jeff.html:1428` |
| « Modifier le script fourni » (Jeff) veut-il dire toucher `PgSQL.sql` ? | Non. Le groupe garde la source intacte et forke le script pour un faker. | registre `:240` ; plan d'action, Q4 (`2026-10-07-plan-action.html:384-394`) |
| Une valeur factice pour les colonnes chiffrées d'énergie ? | Impossible : `CHECK > 0` refuse 0, et un faux nombre se lirait comme une mesure. Elles restent vides. | `01:578-579` ; registre `:280` |
| `+330000000000` (note du 06/10) ? | Un zéro de trop. Un numéro français : `+33` puis 9 chiffres, soit `+33000000000`. | registre `:291` |
| Le contrôle du téléphone accepte-t-il cette valeur ? | Oui : un « + », puis 2 à 15 chiffres, le premier de 1 à 9. Testé. | `01:184-190`, `:221-222` ; `test_constraints_db.py:17`, `:183` |
| Mandat 13 : quel client ? | Nina Girard, déjà cliente : même ville, même budget (220 000), aucun mandat. | `PgSQL.sql:103`, `:153` ; Q-JEF-13 (`2026-10-07-questions-pour-jeff.html:1342`, `:1349`) |
| Quel statut pour une demande reprise ? | `'launched'`, pour les 18 : chacune a un mandat. | `02_migration.sql:269-277` ; F6 ; ADR-041 |
| `energy_class_scheme` : vide, ou `'FR-DPE-2021'` ? | `'FR-DPE-2021'` sur les 1 623 biens qui ont une lettre. **Tranchée par ADR-018**, accepté : « `energy_class_scheme` = `FR-DPE-2021` pour le jeu actuel, entièrement français ». Aucun ADR ne l'a remplacé. Le modèle dit : « Ne jamais effacer un ADR : s'il est remplacé, marquer « remplacé par ADR-XXX » ». Le groupe ajoute qu'on ne réécrit jamais un ADR accepté (ADR-023). La carte Q-MIG-05 ne dit pas l'inverse : elle porte sur `energetic_score` et les colonnes chiffrées, et ne nomme jamais `energy_class_scheme`. « Colonnes d'énergie vides » est le résumé du registre. Le code ne suit pas encore ADR-018 : tâche à coder (Conséquences). | copie du journal, ADR-018 : Statut (« accepté »), Conséquences ; ADR-023, l. 804 ; `JOURNAL-DE-DECISIONS.md:72` ; carte « Q-MIG-05 · energetic_score retiré », `questions-a-trancher.html:1517` ; `questions-a-trancher.md:240`, `:276-281` |
| Et les 933 biens sans lettre ? | Vide. **Tranchée par déduction** : le référentiel « lève […] les deux ambiguïtés de la lettre : pays et version ». Sans lettre, il n'a rien à décrire. C'est aussi la règle de la reprise : vide si la colonne l'accepte. | déduit d'ADR-018, Justification ; Q4, `questions-a-trancher.md:240` |
| « 2021 » est-il supposé ? | Non, c'est le choix d'ADR-018. Il tient pour un DPE valable aujourd'hui : ceux faits du 01/01/2018 au 30/06/2021 ne sont plus valables depuis le 1er janvier 2025 ; « Les DPE réalisés depuis le 1er juillet 2021 sont valables 10 ans ». Pour les DPE plus anciens, sources secondaires seulement. | [service-public.gouv.fr, fiche F16096](https://www.service-public.gouv.fr/particuliers/vosdroits/F16096), doc officielle, « vérifiée le 01/01/2026 », lue par le relecteur le 08/10/2026 |

**Questions ouvertes** 🟡

Aucune. Ce qui reste est du code à écrire, listé dans les Conséquences : l'expiration des mandats finis, et `energy_class_scheme`.

**Sources**

| Affirmation | Source |
|---|---|
| U : vide ou valeur factice ; AC : anciens mandats, « peut rejoindre l'ADR U » | `md/questions/questions-a-trancher.md:416`, `:423` |
| Q4 : vide si la colonne l'accepte, sinon valeur factice documentée ; faker forké ; `PgSQL.sql` jamais touché | `questions-a-trancher.md:240` |
| Q4 : les trois options | `md/journal/2026-10-07-plan-action.html:384-394` |
| Jeff : « les manques sont voulus » | `md/questions/2026-10-07-questions-pour-jeff.html:1428` |
| Jeff : « oui à nos positions » (Nina, statuts, 6 échus, pas de pause) | même fichier, l. 1349 ; registre `:236-239` |
| Q-MIG-06 « Oui, dans 03 » ; Q-MIG-09 « Laisser le minimum vide » | `questions-a-trancher.md:180`, `:182` |
| Avis sur Q-MIG-05, 06, 07 | `questions-a-trancher.md:276-294` |
| Options de Q-MIG-10, Q-MIG-12 | `2026-10-07-questions-pour-jeff.html:1374-1375`, `:1394-1395` |
| Options de Q-MIG-03 | `md/questions/questions-a-trancher.html:1482-1484` |
| Cartes F6, F7, F8 | `md/journal/2026-10-07-rapport-final-chantier-lot.html:566-592` |
| Source : statuts, téléphones, budget, Nina, mandat 13, répartition, question du consultant | `fixtures/PgSQL.sql:26`, `:71`, `:88-106`, `:136-158`, `:167-175` (StarterPack) |
| Date de référence : 25/07/2026 | `documents utiles/MODELE-SWOT.md:26` (StarterPack) |
| Quatre défauts, « Un seed ne doit pas les cacher », « piège du consultant » | `md/journal/2026-09-21-point-etape.md:231-245` |
| Reprise : clients, téléphones, critères, mandats, `'launched'` | `docker/init-v3/02_migration.sql:43-63`, `:126-132`, `:146-172`, `:198-228`, `:230-255`, `:269-277` |
| Biens et lettres DPE | `docker/init-v3/03_populate_estate.sql:1-11` |
| Colonnes : énergie, budget, téléphone, mandat, demande | `docker/init-v3/01_create_fil_rouge_immobilier.sql:184-190`, `:205`, `:221-222`, `:353-354`, `:446-449`, `:461-462`, `:575-579` |
| `energetic_score` vide sur les 2 556 biens | `docker/init-v3/README.md:219-226` |
| Résumé des lots, garde-fous | `docker/init-v3/README.md:60-94` |
| Migration d'une base v2 | `docker/migrations/v2-vers-v3/07_personnes.sql:94-96`, `10_reprise-mandats.sql:39-40`, `:89-97` |
| Test du téléphone factice | `API/tests/integration/test_constraints_db.py:17`, `:183` |
| « Ma recherche est officiellement lancée » | `user-stories/01_particulier_demande_et_compte.feature:37` |
| ADR-007 : téléphone `NOT NULL`, indicatif inclus | journal de Confluence, copie du 07/10/2026, ADR-007 |
| ADR-018, accepté : `FR-DPE-2021` à la migration ; le référentiel qualifie la lettre | même copie, ADR-018 : Statut, Justification, Conséquences |
| On ne réécrit jamais un ADR accepté (convention du groupe) | même copie, ADR-023, Conséquences |
| Q-MIG-05 porte sur `energetic_score` et les colonnes chiffrées | `questions-a-trancher.html:1517` ; `questions-a-trancher.md:276-281` |
| DPE : validité selon la date | [service-public.gouv.fr, fiche F16096](https://www.service-public.gouv.fr/particuliers/vosdroits/F16096), doc officielle, « vérifiée le 01/01/2026 », lue par le relecteur le 08/10/2026 |
| Échéance sans vente : invitation à renouveler, note à la baisse | `user-stories/07_chasseur_remuneration_et_performance.feature:38-41` ; `00_…feature:40` ; `Readme.md:135` (StarterPack) |
| Une note `'mandate_expired'` par mandat ; contrôle C6 | `01:1020` ; `livrables/2-modelisation/09-contraintes-a-coder.md:190`, `:217-219` |
| Questions du jury | `documents utiles/TRAME-SOUTENANCE.md:29`, `:32` (StarterPack) |
| `hire_date`, taux de commission, manager fictif | `questions-a-trancher.md:179`, `:231`, `:235` |
| Service des mandats sans règle | `API/src/app/services/mandate_service.py:1-8` |
| Modèle d'ADR, « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:19-40`, `:72` (StarterPack) |

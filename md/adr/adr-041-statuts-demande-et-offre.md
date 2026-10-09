# ADR-041 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 041 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:64`,
> lettre O). Il ne vaut rien tant que le groupe ne l'a pas pris sur Confluence.
>
> 💡 **Rédigé le 08/10/2026 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et
> un arbitre. Les passages marqués « déduit » sont une lecture des sources, pas
> une décision du groupe. Aucune question ne reste ouverte.
>
> 🗂️ **Deux points réglés hors de la fiche :**
>
> * **Aucun ADR de Confluence à marquer « remplacé ».** Aucun des 27 ADR (copie
>   du 07/10/2026) ne parle des statuts de la demande ou de l'offre.
> * **La reprise des 18 demandes** (Q-MIG-03) appartient à l'ADR-046 (lettres
>   U + AC, reprise des anciens mandats, `2026-10-08-proposition-regroupement-adr.md:69`).
>   Cette fiche n'en cite que l'effet sur le statut.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * `API/src/app/models/search_request_model.py:26-28` dit encore « Les demandes
>   migrees valent 'confirmed', hypothese a confirmer ». Faux depuis LOT10 : elles
>   valent `'launched'`.
> * `docker/init-v3/README.md:406` et `:408` comptent encore **17** demandes et
>   **17** mandats. Le même README en compte **18** depuis LOT10 (l. 91-93).
> * `md/questions/questions-a-trancher.md:239` : « Les 17 demandes en
>   `'launched'` (`02:241-246`) ». C'est **18**, et l'`UPDATE` est à `02:275-277`.
> * `livrables/2-modelisation/09-decisions-a-prendre.md` : D4 et D5 ont encore
>   « Décision retenue » vide (l. 354, l. 377), « ouverte » au tableau de bord
>   (l. 66-67), et deux noms à choisir vides (l. 483, l. 485).
> * **Trou repéré, hors de cette fiche.** L'offre est « déjà pré-remplie suivant
>   les conclusions du chasseur effectuées au point 7 (montant de l'offre) »
>   (`Readme.md:130`, StarterPack). Ce montant conseillé n'a pas de colonne : la
>   note d'avis est un texte libre (`review_hunter`, `01:662`). À voir avec le
>   parcours de l'offre.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-041 : La demande de recherche a quatre statuts ; l'offre d'achat gagne l'état « signée »

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions du groupe : 05/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * le groupe — réponses du 05/10/2026 aux cartes Q-SCH-03 (« Acter les 4 statuts ») et Q-SCH-04 (« Ajouter 'signed' ») ;
  * pour la reprise des demandes : Sébastien, au questionnaire de LOT10 (07/10/2026), d'après la réponse de Jeff à Q-JEF-13 (« pas de nouvel état »).
* **Remplace :** aucun ADR. Ferme les décisions D4 et D5 de `livrables/2-modelisation/09-decisions-a-prendre.md`.

**Contexte**

Le sujet décrit la vie d'une demande de recherche en quatre moments :

* l'affectation d'un chasseur « est confirmée » (`01_particulier_demande_et_compte.feature:20`) ;
* le chasseur accepte la demande (`04_chasseur_prise_en_charge_demande.feature:26`), ou décide « de ne pas l'accepter » (même fichier, l. 19) ;
* au mandat signé, « ma recherche est officiellement lancée » (`01_…feature:37`).

Il décrit aussi la vie d'une offre d'achat :

* le client peut « compléter et signer cette offre » (`06_chasseur_avis_et_offre_achat.feature:22`) ;
* le chasseur la transmet, et « le statut de l'offre passe en attente de réponse du vendeur » (même fichier, l. 34) ;
* le vendeur refuse (l. 39) ou accepte (l. 46).

Au 11/09/2026, le rapport d'écarts notait sur la demande « aucune colonne de statut » (`09-rapport-ecarts-contraintes.md:337-341`). Deux décisions restaient ouvertes : D4 (statuts d'une demande) et D5 (états d'une offre) (`09-decisions-a-prendre.md:66-67`).

Depuis, le schéma porte quatre statuts sur la demande. La carte Q-SCH-03 le constate : « Déjà en base […], jamais ratifiés » (`md/questions/questions-a-trancher.html:1147`).

Côté offre, un état manquait : « offre signée, pas encore envoyée ». `'proposed'` interdit le montant ; `'offer_pending'` veut dire « déjà envoyée » (`09-decisions-a-prendre.md:367-369`).

**Options envisagées**

Deux questions, tranchées le même jour.

A. Les statuts de la demande (Q-SCH-03)

1. **Acter les 4 statuts déjà en base.** Avantage : « Rien à recoder. » Inconvénient : « Aucun. » **Retenue.**
2. **Les revoir.** Avantage : « Débat ouvert. » Inconvénient : « Base à recréer. » **Écartée.**

B. L'état « signée, pas encore envoyée » de l'offre (Q-SCH-04)

1. **Ajouter `'signed'`.** Avantage : « Cas réel couvert. » Inconvénient : « Base à recréer. » **Retenue.**
2. **Reporter.** Avantage : « Rien à faire. » Inconvénient : « Cas non couvert. » **Écartée.**

(Avantages et inconvénients recopiés des cartes : `questions-a-trancher.html:1157-1158` et `:1175-1176`.)

**Décision**

1. `search_request.status` prend quatre valeurs, et seulement elles : `VARCHAR(20) NOT NULL CHECK (status IN ('confirmed', 'accepted', 'rejected', 'launched'))` (`docker/init-v3/01_create_fil_rouge_immobilier.sql:320-321`).

   | Statut | Sens | Story |
   |---|---|---|
   | `'confirmed'` | la demande est enregistrée ; elle attend la réponse d'un chasseur, affecté ou encore à affecter (`id_hunter` peut être vide) | `01_…feature:14`, `:20` (U18) |
   | `'accepted'` | le chasseur accepte la demande | U28 (`04_…feature:26`) |
   | `'rejected'` | le chasseur n'accepte pas la demande | U26 (`04_…feature:19`) |
   | `'launched'` | le mandat est signé : la recherche est lancée | U21 (`01_…feature:37`) |

2. `estate_proposed.proposition_status` prend cinq valeurs : `'proposed'`, `'offer_pending'`, `'accepted'`, `'signed'`, `'rejected'` (`01:692-694`). `'signed'` est la nouvelle.

   | Statut | Sens | Story |
   |---|---|---|
   | `'proposed'` | le bien est proposé au client ; pas de montant | `chk_offer` (`01:702-704`) |
   | `'signed'` | le client a complété et signé l'offre ; pas encore envoyée | U34 (`06_…feature:22`) |
   | `'offer_pending'` | le chasseur l'a transmise ; en attente du vendeur | U35 (`06_…feature:34`) |
   | `'accepted'` | le vendeur accepte | U37 (`06_…feature:46`) |
   | `'rejected'` | le vendeur refuse | U36 (`06_…feature:39`) |

3. `chk_offer` ne change pas. Hors de `'proposed'`, le montant est obligatoire (`01:702-704`). `'signed'` l'exige donc.
4. Pas de statut pour une recherche finie. La demande reste `'launched'`. La fin se lit sur le mandat (`mandate.status`, `01:446-449`).
5. Après un refus du vendeur, une nouvelle offre est une **nouvelle ligne**. L'offre refusée garde `'rejected'` et son montant. Tranchée par déduction (Questions tranchées).

**Justification**

* Une valeur par étape nommée par le sujet. La liste de D4 (`09-decisions-a-prendre.md:343-346`) correspond aux quatre valeurs en base.
* Acter plutôt que revoir : rien à recoder, et personne n'a proposé d'autre liste.
* `'signed'` couvre un vrai moment du parcours. Le client signe (`06_…feature:22`), puis le chasseur transmet (l. 33). Entre les deux, l'offre a un montant mais n'est pas envoyée. Ni `'proposed'` ni `'offer_pending'` ne le disent (`09-rapport-ecarts-contraintes.md:410`).
* Les valeurs sont en anglais, comme tout le schéma : ADR-002 choisit « la langue anglaise pour le code, les schémas de données » (journal Confluence, copie du 07/10/2026, ADR-002, Décision).
* Pas de nouvel état : Jeff a répondu « pas de pause, pas de nouvel état » sur les mandats repris (Q-JEF-13). Q-MIG-03 en est déduite pour les demandes (`questions-a-trancher.html:1479`). En ajouter un à la demande rouvrirait d'ailleurs Q-SCH-03 (`questions-a-trancher.md:273`).

**Conséquences**

* **Schéma :** les quatre statuts de la demande étaient déjà là ; seul leur type a grandi, de `VARCHAR(9)` à `VARCHAR(20)` (correction 7, `01:55-56`). `'signed'` est entré à LOT3 (commit `04b2bb3`) : `01:692-694`. Une base v2 y arrive par `docker/migrations/v2-vers-v3/03_mandat-statuts.sql` (l. 17, l. 55-59).
* **Tests :** `'signed'` accepté, et un statut inconnu (`'sent'`) refusé en 409 (`API/tests/integration/test_constraints_db.py:428`, `:434`). Aucun test sur `search_request.status`.
* **Reprise :** les 18 demandes sont insérées en `'confirmed'` (`docker/init-v3/02_migration.sql:179-196`). Les 18 ont un mandat (l. 238-255). L'`UPDATE` de la section 9 les passe en `'launched'` (l. 275-277). Compté dans le SQL, pas en base : Docker était arrêté le 08/10/2026.
* Parmi leurs 18 mandats : 5 `'active'`, 3 `'completed'`, 8 `'expired'`, 2 `'canceled'` (`MAND-0008`, `MAND-0016`). Les 18 demandes restent `'launched'`, même celles dont le mandat est fini : pas de nouvel état.
* **L'ordre des statuts n'est tenu nulle part.** Le `CHECK` ne liste que les valeurs permises. Les services `search_request_service.py` et `estate_proposed_service.py` n'ont aucune règle. `PUT /search-requests/{id}` accepte un saut de `'confirmed'` à `'launched'` (`API/src/app/routes/crud_router.py:95-102`).
* **Reste à coder dans l'API :** l'ordre des statuts (voir les questions tranchées), avec un test par passage. Une offre ne sort pas de `'rejected'` : la suivante s'écrit sur une nouvelle ligne.
* **Reste à coder dans l'API :** `'launched'` seulement si un mandat signé existe pour la demande. La règle croise deux tables : elle va dans l'API, testée (Q-MAN-06, ADR-040, proposé).
* **Deux `'accepted'` et deux `'rejected'`, de sens différents.** Sur la demande, c'est la réponse du chasseur. Sur l'offre, c'est celle du vendeur. À dire à l'oral, et à porter au glossaire FR/EN qu'ADR-002 demande (ADR-002, Conséquences).
* **Journal :** aucun ADR remplacé. D4 et D5 sont fermées.

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Quel statut à la création d'une demande ? | `'confirmed'`. ✅ Confirmé par le groupe le 09/10/2026 (S5). Déduit par élimination : la colonne est `NOT NULL` sans valeur par défaut ; `'accepted'` et `'rejected'` sont une réponse du chasseur ; `'launched'` suppose un mandat signé. Tant qu'aucun chasseur n'est désigné, `id_hunter` reste vide (colonne facultative). Le README v2 l'appelait déjà « l'état d'entrée neutre ». | déduit de `01:315-316`, `01:320-321`, `04_…feature:19-26`, `01_…feature:37` ; `docker/init-v2/README.md:164` |
| Qui passe la demande en `'accepted'` ou `'rejected'` ? | Le chasseur. | `04_…feature:19`, `:26` ; `md/securite/matrice-droits-crud-par-role.md:152` (« accepter / refuser ✅ ») |
| Que devient une demande `'rejected'` ? | Elle s'arrête là : dans le schéma du sujet, « Non » mène à « Fin ». La réaffectation (« peut être réaffectée », `04_…feature:21`) est reportée (Q-MAN-08). | `Readme.md:140` (StarterPack) ; `questions-a-trancher.md:176` ; ADR-045, limite 5 (proposé) |
| Dans quel ordre vont les statuts ? | Demande : `'confirmed'` → `'accepted'` ou `'rejected'` ; `'accepted'` → `'launched'`. Offre : `'proposed'` → `'signed'` → `'offer_pending'` → `'accepted'` ou `'rejected'`. Déduit de l'ordre du parcours. | déduit de `01_…feature:20`, `:37` ; `04_…feature:19-27`, `:36-41` ; `06_…feature:22`, `:33-34`, `:39`, `:46` |
| Qui fait respecter cet ordre ? | L'API, dans les services, avec un test par passage. Pas encore codé. Déduit : le `CHECK` ne voit que la valeur écrite ; `'launched'` dépend d'un mandat, donc d'une autre table, et le groupe range ces règles dans l'API (Q-MAN-06). | déduit de `01:320-321` ; `questions-a-trancher.md:155`, `:408` ; `API/src/app/main.py:14` (« c'est ici qu'irait une règle ») |
| Une recherche finie (vente, mandat échu, annulé) change-t-elle de statut ? | Non. Elle reste `'launched'` ; la fin se lit sur le mandat. | Jeff, Q-JEF-13 (« pas de nouvel état », `md/questions/2026-10-07-questions-pour-jeff.html:355`) ; `questions-a-trancher.html:1479` ; `02_migration.sql:270-273` |
| Une offre pré-remplie, pas encore signée, a-t-elle un état ? | Non : la ligne reste `'proposed'`, sans montant. Le montant s'écrit avec `'signed'`. Déduit de `chk_offer`, gardé tel quel. | déduit de `01:702-704` ; `09-rapport-ecarts-contraintes.md:410` (« `chk_offer` ne change pas ») |
| Faut-il les états « bien choisi » et « bien écarté » (F02) ? | Pas maintenant : F02 est du parcours futur, avec l'IA. Et `'rejected'` ne convient pas : il exige un montant, c'est une réponse du vendeur. | `09-decisions-a-prendre.md:360`, `:370-372` ; `08_futur_particulier_assistance_ia.feature:6` (`@futur-ia`), `:29` ; `questions-a-trancher.md:949` |
| Après un refus du vendeur, la nouvelle offre est-elle une nouvelle ligne, ou la même ligne qui repart ? | Une nouvelle ligne. **Tranchée par déduction.** ✅ Confirmé par le groupe le 09/10/2026 (S5). Le sujet parle d'une autre offre : « je peux proposer une nouvelle offre d'achat » ; « en refaire une autre ». `'rejected'` est un état final dans l'ordre ci-dessus. `chk_offer` garde le montant d'une offre refusée : réécrire la ligne effacerait la réponse du vendeur. Le schéma le permet déjà : pas de `UNIQUE` sur le bien et le mandat. Le bien apparaît alors deux fois : l'API montre la dernière offre (micro-décision). | déduit de `06_…feature:40` ; `Readme.md:131` (StarterPack) ; `01:684-710`, `:702-704` ; micro-décision : `JOURNAL-DE-DECISIONS.md:13` |

**Questions ouvertes** 🟡

Aucune. Ce qui reste est du code à écrire, listé dans les Conséquences.

**Sources**

| Affirmation | Source |
|---|---|
| Demande « enregistrée » ; affectation « confirmée » ; recherche « officiellement lancée » | `user-stories/01_particulier_demande_et_compte.feature:14`, `:20`, `:37` (StarterPack) |
| Le chasseur accepte, ou non ; réaffectation possible | `04_chasseur_prise_en_charge_demande.feature:19-21`, `:26` (StarterPack) |
| Offre signée, transmise, en attente, refusée, acceptée | `06_chasseur_avis_et_offre_achat.feature:22`, `:33-34`, `:39-40`, `:46` (StarterPack) |
| Refus du vendeur, côté client | `03_particulier_offre_et_signature.feature:21`, `:27` (StarterPack) |
| Refus du chasseur → Fin ; « en refaire une autre » ; offre pré-remplie | `Readme.md:140`, `:131`, `:130` (StarterPack) |
| F02, parcours futur | `08_futur_particulier_assistance_ia.feature:6`, `:29` (StarterPack) |
| « aucune colonne de statut » au 11/09 | `livrables/2-modelisation/09-rapport-ecarts-contraintes.md:337-341` |
| D4, D5 : questions, liste des stories, F02 « plus tard » | `livrables/2-modelisation/09-decisions-a-prendre.md:335-377` |
| U34 : `'proposed'` interdit le montant, `chk_offer` ne change pas | `09-rapport-ecarts-contraintes.md:410` |
| Q-SCH-03 : « Acter les 4 statuts » (05/10/2026) | `md/questions/questions-a-trancher.md:159` ; `questions-a-trancher.html:1143-1160` |
| Q-SCH-04 : « Ajouter 'signed' » (05/10/2026) | `questions-a-trancher.md:160` ; `questions-a-trancher.html:1161-1178` |
| Lettre O : statuts de la demande et de l'offre | `questions-a-trancher.md:410` |
| `search_request.status`, `id_hunter` facultatif | `docker/init-v3/01_create_fil_rouge_immobilier.sql:308-322` |
| Correction 7 : `VARCHAR(9)` → `VARCHAR(20)` | même fichier, l. 55-56 |
| `proposition_status` et `chk_offer` | même fichier, l. 692-694 et l. 702-704 |
| `mandate.status` | même fichier, l. 446-449 |
| `'signed'` en migration (LOT3, `04b2bb3`) | `docker/migrations/v2-vers-v3/03_mandat-statuts.sql:17`, `:55-59` |
| 18 demandes `'confirmed'`, 18 mandats, `UPDATE` en `'launched'` | `docker/init-v3/02_migration.sql:179-196`, `:238-255`, `:270-277` |
| LOT10 : les demandes étaient en `'confirmed'`, pas `'launched'` | `context AI/08-etat.md:263-268` |
| Même `UPDATE` pour une base v2 | `docker/migrations/v2-vers-v3/10_reprise-mandats.sql:95-97` |
| Jeff : « pas de pause, pas de nouvel état » | `md/questions/2026-10-07-questions-pour-jeff.html:355` |
| Q-MIG-03 tranchée par déduction de cette réponse | `questions-a-trancher.html:1479` ; `questions-a-trancher.md:239` |
| Un état de plus rouvrirait Q-SCH-03 | `questions-a-trancher.md:273` |
| Q-MAN-08 reportée | `questions-a-trancher.md:176`, `:883-897` |
| Q-MAN-06 : règles sur plusieurs tables dans l'API | `questions-a-trancher.md:155`, `:408` |
| Droits : le chasseur accepte ou refuse | `md/securite/matrice-droits-crud-par-role.md:152` |
| Modèles et services de l'API | `API/src/app/models/search_request_model.py:26-29` ; `estate_proposed_model.py:21-25` ; `services/search_request_service.py`, `services/estate_proposed_service.py` |
| `PUT` ouvert sur toutes les tables | `API/src/app/routes/crud_router.py:95-102` |
| Tests | `API/tests/integration/test_constraints_db.py:428`, `:434` |
| ADR-002 : anglais pour le schéma ; glossaire FR/EN | journal Confluence, copie du 07/10/2026, ADR-002 : Décision, Conséquences |
| Modèle d'ADR, micro-décisions, « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:13`, `:19-40`, `:72` (StarterPack) |

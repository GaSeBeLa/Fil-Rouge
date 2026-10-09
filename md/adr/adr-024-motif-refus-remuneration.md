# ADR-024 — version finie, à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence, **à la place** de la page actuelle
> « ADR-024 Annulé — les modifications à faire, en détail ». Rien ne s'écrit
> sur Confluence depuis ce fichier.
>
> ✏️ **Proposé le 21/09/2026, fini le 08/10/2026 par Claude**, d'après les
> fichiers du dépôt. Ajouts du 08/10 : la vente perdue (lettre B, statut
> `'lost'`), le schéma v3, la version des réglages du taux (G1). **Pas de
> numéro neuf** (`md/adr/2026-10-08-proposition-regroupement-adr.md:44`).
> Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un arbitre.
>
> 🗂️ **La page Confluence : quatre points réglés par les sources.**
>
> 1. **Le numéro 024 est le bon** (déduit). Le doute du 21/09 venait du cahier
>    des charges v2.0, décalé d'un rang sur le journal. Q-PRO-04 a tranché ce
>    décalage le 06/10/2026 : « Le journal Confluence fait foi »
>    (`md/questions/questions-a-trancher.md:200`). Le journal place ADR-024
>    juste après ADR-023 (copie du 07/10/2026 : la page d'ADR-024 suit ADR-023).
> 2. **Le statut n'est pas « Annulé » : il est « proposé ».** Aucune source
>    écrite n'annule cet ADR, aucune ne l'accepte. Le registre dit « en base
>    mais pas actée (ADR-024 « proposé ») » (`questions-a-trancher.md:1109`).
>    Le README du schéma dit « pas encore validé par le groupe »
>    (`docker/init-v3/README.md:471`). Le modèle du sujet ne connaît pas
>    « Annulé » (`JOURNAL-DE-DECISIONS.md:22`).
> 3. **La phrase « l'ADR-024 est validé par le groupe » est fausse.** C'est la
>    fin d'une phrase coupée au collage. La première version du compagnon
>    disait : « Ce fichier liste ce qu'il faudra changer **si** l'ADR-024 est
>    validé par le groupe » (commit `8684b7f`,
>    `md/adr-024-modifications-a-faire.md`, l. 3-4). Le compagnon actuel dit :
>    « Le groupe ne l'a pas validé » (`md/adr/adr-024-modifications-a-faire.md:8-9`).
> 4. **On peut le finir sans numéro neuf.** La page actuelle n'est pas l'ADR :
>    c'est le compagnon technique, collé par erreur
>    (`md/journal/2026-09-21-a-faire-a-la-main.md:197-204` ; copie du journal,
>    l. 810-814). Ce compagnon reste dans le dépôt : rien n'est effacé. Le sujet
>    dit, mot pour mot : « **Ne jamais effacer** un ADR : s'il est remplacé,
>    marquer « remplacé par ADR-XXX ». » (`JOURNAL-DE-DECISIONS.md:72`). Le mot
>    « accepté » n'y est pas. La convention « on ne réécrit jamais un ADR
>    accepté » vient du groupe (ADR-023, Conséquences). ADR-024 n'a
>    jamais été accepté (point 2) : il se finit sous son numéro.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * Confluence : remplacer la page actuelle par cette fiche. Le compagnon
>   (`md/adr/adr-024-modifications-a-faire.md`) reste dans le dépôt.
> * Registre : la question Q3 de Q-PRO-02, « pas actée (ADR-024) », se ferme
>   quand le groupe accepte cet ADR.
> * ⚠️ La proposition de regroupement se contredit : l. 44 « finit ADR-024, pas
>   de numéro neuf », l. 96 « 024 passe en « remplacé par » ». Cette fiche suit
>   la l. 44.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-024 : Le refus de rémunération se trace — le motif sur le paiement, la vente perdue sur le mandat

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 21/09/2026 (proposé) ; complété le 08/10/2026
* **Statut :** proposé
* **Décideurs :**
  * l'équipe projet, pour le motif sur le paiement (21/09/2026) ;
  * le groupe, pour la vente perdue (Q-REM-02 le 02/10/2026, Q-REM-14 le 05/10/2026) et pour la version des réglages du taux (G1, 08/10/2026) ;
  * le client, Jeff, pour « rien pour personne » (Q-JEF-03, 07/10/2026) ;
  * Sébastien, pour un seul statut `'lost'` (LOT3, 07/10/2026).

**Contexte**

Toutes les ventes n'ouvrent pas un droit à rémunération pour le chasseur. Le sujet impose d'en garder la raison : « Le refus retourne un **motif**, jamais un simple `False` » (`REGLES-CALCUL-REMUNERATION.md:497`). Il dit aussi où : « stocker le **motif** du droit refusé dans `paiements` » (`:100`). Sa décision D2 propose « Rien (R = 0), mais motif tracé » (`:322`).

Le code du sujet ferme le droit dans deux cas (`:500-508`) :

* `MANDAT_EXPIRE` : l'acte est signé après la fin du mandat. Un mandat renouvelé a une nouvelle fin : voir ADR-050 ;
* `HORS_DISPOSITIF` : le mandat est non exclusif, et la vente ne vient pas du chasseur (le client seul, ou une autre agence).

Un troisième cas n'a pas de motif dans ce code. Un client a deux mandats non exclusifs, avec Bruno et Chloé. La vente aboutit à l'initiative de Chloé : « "Bruno" ne perçoit aucune rémunération pour cette vente » (`10_calcul_remuneration_chasseur.feature:53-56`). Chloé « perçoit la totalité de la part chasseur » (`:55`) : elle est donc payée par l'entreprise, c'est une collègue de Bruno (déduit). Bruno n'a pas de vente : rien n'est calculé pour lui.

Le 21/09/2026, la table `payment` ne pouvait enregistrer aucun refus. Pas de colonne de motif. Aucun statut « refusé ». Un taux de base et une tranche de barème obligatoires, alors qu'un droit fermé n'en a pas.

Depuis, deux faits pèsent sur la vente perdue :

* Le client a tranché le 07/10/2026 : « rien pour personne : ni le chasseur, ni l'entreprise » (Q-JEF-03). Il n'y a donc pas d'honoraires.
* En base, un paiement exige une vente (`payment.id_sale NOT NULL`), et une vente exige des honoraires (`sale.fees_amount CHECK (> 0)`). Sans honoraires, pas de vente. Sans vente, pas de ligne de paiement.

**Options envisagées**

Sujet 1 — où garder un refus, quand la vente existe (21/09/2026) :

1. **Ne rien stocker** : une vente refusée n'a aucune ligne `payment`. Aucun changement, mais le motif est perdu. **Écartée.**
2. **Une ligne `payment` en état `refused`**, avec le motif, sans taux ni barème. **Retenue.**
3. **Une table `payment_refusal` à part.** Deux tables répondraient alors à « ce chasseur a-t-il été payé pour cette vente ? ». **Écartée.**
4. **Le motif sur `sale`.** Cela mélange la vente et le droit du chasseur. **Écartée.**

Sujet 2 — la vente perdue (Q-REM-02, Q-REM-14) :

1. **Une 3e origine `'other_agency'`, des honoraires à 0 permis, et un paiement refusé `'out_of_scope'`.** Avantage : tout refus est sur `payment`, comme le veut le sujet. Inconvénients : une vente sans honoraires, et un `CHECK` de `sale` à relâcher. Recommandée par Claude, **écartée** par le groupe. Raison : sans honoraires, il n'y a pas de vente à enregistrer (`sale.fees_amount CHECK (> 0)`, `01_…sql:760`) ; et le client ne veut rien pour personne (Q-JEF-03).
2. **Pas de vente : le mandat prend un statut de fin.** **Retenue.**
3. **Laisser le mandat expirer.** Inconvénient : on confond « perdu » et « expiré ». **Écartée.**

Sous-choix : **un seul statut** `'lost'`, ou deux (`'lost'` hors agence, `'superseded'` pour le collègue). **Un seul, retenu.**

**Décision**

1. **Quand une vente existe et que le droit est fermé**, le refus est une ligne de `payment` : statut `'refused'`, un motif, `amount = 0`. Elle ne porte ni taux, ni score, ni tranche de barème, ni version des réglages du taux, ni date d'étape.
2. Les deux motifs sont ceux du sujet, en anglais (ADR-002) : `mandate_expired` (« mandat échu à la date de l'acte ») et `out_of_scope` (« mandat non-exclusif et vente hors dispositif »).
3. **Quand la vente est perdue**, il n'y a ni vente ni paiement. **Le mandat prend le statut `'lost'`.** Un seul statut pour tous les cas : vendu par le client seul, par une autre agence, ou par un collègue sur l'autre mandat non exclusif.
4. **Pas d'indemnité.** D2 est fermée par le client : rien pour personne.

Le code, tel qu'il est aujourd'hui (`docker/init-v3/01_create_fil_rouge_immobilier.sql`) :

```sql
-- mandate (l. 446-449)
status IN ('active', 'completed', 'expired', 'renewed', 'canceled', 'pending_signature', 'lost')
-- payment (l. 884-886, 899-901)
status IN ('refused', 'announced', 'scheduled', 'paid')
refusal_reason VARCHAR(30) CHECK (refusal_reason IN ('mandate_expired', 'out_of_scope'))
```

`chk_refused` (l. 965-983) dit le reste. Un refus a un motif, un montant à 0, et aucun terme de calcul (taux, score, tranche, version des réglages). Un paiement a tous ses termes, et aucun motif.

**Justification**

* **Le sujet ne laisse pas le choix du principe** : le motif se garde. Ne rien stocker est la seule option qui perd la donnée demandée.
* **Un refus n'est pas un paiement à zéro.** C'est un événement de droit, daté et motivé, opposable au chasseur qui réclame. `chk_refused` empêche un refus de ressembler à un paiement en attente, et un vrai paiement d'exister sans taux ni barème.
* **`id_sale` est `UNIQUE`** : une vente porte un paiement ou un refus, jamais les deux.
* **La vente perdue n'a pas de vente.** Écrire son refus sur `payment` demanderait une vente sans honoraires (option 1), contre la réponse du client. Le statut du mandat est le seul endroit où ce cas existe en base.
* **`'lost'` porte la même information que le motif du sujet.** Le code du sujet range le client seul et l'autre agence sous un même motif, `HORS_DISPOSITIF` (`REGLES-CALCUL-REMUNERATION.md:506-508`). Le cas du collègue se lit sur l'autre mandat, celui qui porte la vente.
* **Un seul statut** reste simple. Inconvénient accepté : pour distinguer « hors agence » et « collègue », il faut croiser deux mandats.

**Conséquences**

* **Écart au sujet, assumé :** pour une vente perdue, le motif n'est pas dans `payment` (`REGLES-CALCUL-REMUNERATION.md:100`), mais dans `mandate.status`. À dire à l'oral.
* **Schéma : déjà fait.** `payment` depuis le 21/09/2026 (`docker/migrations/2026-09-21_adr-024_payment_refusal.sql` pour une base v2). `'lost'` depuis LOT3 (`docker/migrations/v2-vers-v3/03_mandat-statuts.sql`).
* **`chk_refused` a grandi depuis le 21/09.** Le taux final est exigé hors refus (Q-REM-10). Le score figé est vide sur un refus (Q-REM-03). La version des réglages du taux est vide sur un refus, exigée sinon (G1, commit `7fc63ed`, migration 15).
* **Un refus n'a pas de date d'étape** : ni `announced_at`, ni `scheduled_for` (`chk_announced`, `chk_scheduled`, l. 950-956).
* **Hors de cet ADR, et à ne pas lui attribuer :** les statuts de facture sont retirés (facture hors périmètre, Q-JEF-23) ; les bornes de `seniority_rate` et `performance_rate` sont devenues des bornes de domaine (Q-REM-05). La version du 21/09 disait ces bornes « inchangées » : ce n'est plus vrai.
* **Tests :** `'lost'` accepté (`API/tests/integration/test_constraints_db.py:275`) ; refus accepté, refus avec un taux, un score ou une version de réglages refusés, paiement sans version de réglages refusé (`:554-589`). Le refus sans motif et le refus avec un montant ont été mesurés en SQL le 21/09/2026, 10 cas sur 10 (`docker/init-v3/README.md:508-527`).
* **Cet ADR enregistre le refus, il ne le calcule pas.** Vérifier le droit (bon chasseur, barème en vigueur) reste à faire dans l'API (`01_…sql:985-993`, Q-MAN-06).
* **Qui pose `'lost'` :** rien n'est automatique. La route `/mandates` l'accepte. Passer le mandat du perdant en `'lost'` quand la vente du collègue est saisie : à écrire dans l'API.
* **Un mandat `'lost'` bloque-t-il encore l'exclusivité ?** La question est traitée dans ADR-039 (période du mandat, Questions tranchées n° 1) : il libère le client tout de suite, tranchée par déduction, confirmée par Sébastien le 2026-10-09 (Discord). C'est dans le code depuis le 2026-10-09 (migration 19).
* **La valeur `out_of_scope` reste** dans le `CHECK` (`01_…sql:897-901`) : elle recopie l'énumération du sujet (`REGLES-CALCUL-REMUNERATION.md:385-387`). Aujourd'hui, aucun chemin normal n'y mène (déduit : son cas mène à `'lost'`, sans vente, donc sans paiement). La garder ou la retirer est une micro-décision (`JOURNAL-DE-DECISIONS.md:13`) : rien ne change tant que le groupe ne demande pas de la retirer.
* **MPD v8 (08/10/2026) :** il porte `'lost'` et le nouveau `chk_refused`.

**Questions tranchées par les sources**

1. **Rien, ou une indemnité (D2) ?**
   Rien pour personne : le client, le 07/10/2026 (Q-JEF-03 ; `md/questions/2026-10-07-questions-pour-jeff.html:927` ; registre `:225`).
2. **Un statut de fin, ou deux ?**
   Un seul, `'lost'` : choisi par Sébastien à LOT3, gardé le 07/10/2026 (rapport LOT1 → LOT5, carte D2 ; registre `:135`).
3. **Un mandat exclusif peut-il finir `'lost'` ?**
   Non, déduit. En exclusif, le chasseur est payé même si le client trouve seul (`00_regles_metier_mandat_remuneration.feature:19` ; `REGLES-CALCUL-REMUNERATION.md:504-505`). Une autre agence y est un « cas impossible » (`:96`). Un mandat `'lost'` est donc toujours non exclusif.
   Rien en base ne l'impose aujourd'hui : aucun `CHECK` ne lie `status` et `is_exclusive`. 💡 Un `CHECK` sur `mandate` le dirait en une ligne (`status <> 'lost' OR NOT is_exclusive`) : à décider par le groupe.

**Questions ouvertes** 🟡

Aucune. La question de l'exclusivité d'un mandat `'lost'` est traitée dans ADR-039 ; celle de la valeur `out_of_scope` est une micro-décision, dite dans les Conséquences.

**Sources**

| Affirmation | Source |
|---|---|
| Le refus retourne un motif ; le garder dans `paiements` ; D2 | `REGLES-CALCUL-REMUNERATION.md:497`, `:100`, `:322` (StarterPack) |
| Les deux motifs du sujet | même fichier, l. 385-387 |
| Le droit : exclusif payé (l. 504-505) ; client seul et autre agence → `HORS_DISPOSITIF` (l. 506-508) | même fichier, l. 500-508 ; tableau l. 92-96 |
| Bruno et Chloé : Bruno ne perçoit rien ; Chloé perçoit la part chasseur | `10_calcul_remuneration_chasseur.feature:52-56` (StarterPack) |
| Exclusif : payé même si le client trouve seul | `00_regles_metier_mandat_remuneration.feature:19` (StarterPack) |
| Q-REM-02 : statut de fin, pas l'option recommandée ; écart à `RCR:100` | `md/questions/questions-a-trancher.md:122`, `:517-536` |
| Q-REM-14 : un seul statut `'lost'`, gardé le 07/10 | même registre, l. 135, l. 686-693 |
| B amende ADR-024, écart à `RCR:100` | même registre, l. 397 |
| Option « laisser expirer » : on confond perdu et expiré | `md/questions/questions-a-trancher.html:776` |
| Jeff : « rien pour personne : ni le chasseur, ni l'entreprise » | `md/questions/2026-10-07-questions-pour-jeff.html:927` (notée par l'équipe) |
| Carte D2 : un seul statut, choisi par Sébastien ; écarté : `'superseded'` | `md/journal/2026-10-07-rapport-lot1-a-lot5.html:445-457` |
| Statut `'lost'` | `docker/init-v3/01_create_fil_rouge_immobilier.sql:442-449` |
| Vente : honoraires `> 0`, deux origines, un mandat | même fichier, l. 760-763 |
| `payment` : statuts, motif, `chk_refused`, `id_sale UNIQUE` | même fichier, l. 884-886, 899-901, 932, 965-983 |
| G1 : version des réglages vide sur un refus | même fichier, l. 936-942 ; commit `7fc63ed` ; `docker/migrations/v2-vers-v3/15_paiement-reglages-taux.sql` |
| Le droit n'est pas calculé en base | même fichier, l. 985-993 |
| Tests | `API/tests/integration/test_constraints_db.py:275`, `:554-589` |
| Mesure SQL du 21/09, 10 cas sur 10 ; « pas encore validé par le groupe » | `docker/init-v3/README.md:471`, `:508-527` |
| Le compagnon n'est pas la décision | `md/journal/2026-09-21-a-faire-a-la-main.md:197-204` |
| À finir, avec B dedans | `md/adr/2026-10-07-liste-adr-chantier-4.md:55-56` |
| Exclusivité d'un mandat `'lost'` | ADR-039, Questions tranchées n° 1 |
| Modèle d'ADR ; micro-décisions ; « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:13`, `:22`, `:72` (StarterPack) |
| « on ne réécrit jamais un ADR accepté » : convention du groupe | ADR-023, Conséquences (journal Confluence, copie du 07/10/2026) |
| MPD v8 : `'lost'` et `chk_refused` avec la version des réglages | MPD v8 du 08/10/2026 (fichier `v8.drawio.xml` reçu sur Discord, hors dépôt), lu le 08/10/2026 |

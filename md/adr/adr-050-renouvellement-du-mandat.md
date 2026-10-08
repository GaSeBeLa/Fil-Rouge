# ADR-050 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 050 est une proposition.** Les numéros 028 à 049 sont déjà
> proposés (`md/adr/2026-10-08-proposition-regroupement-adr.md:37-80`) : 050
> est le premier libre.
>
> ✂️ **Coupé d'ADR-039 par l'arbitre le 08/10/2026.** Le premier jet « Règles
> du mandat » mêlait la période du mandat et son renouvellement. ADR-039 garde
> la période (6 mois, exclusivité, annulation, mandat clos). Cette fiche garde
> le renouvellement. Le modèle du sujet veut « une fiche courte par décision »
> (`JOURNAL-DE-DECISIONS.md:7`) et des numéros qui se suivent (`:70`) : pas de
> « 039a / 039b ».
>
> 💡 **Rédigé le 08/10/2026 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et
> un arbitre.
>
> 🧹 **À corriger ailleurs** (signalé ici, pas fait) :
>
> * Ces textes disent que la décision « remplace » ADR-010 et ADR-013. Elle
>   **complète** ADR-010 et **amende** ADR-013 (voir l'en-tête) :
>   * `docker/init-v3/01_create_fil_rouge_immobilier.sql:468` ;
>   * `docker/migrations/v2-vers-v3/16_mandat-renouvellement-sans-avenant.sql:9-10` ;
>   * `livrables/2-modelisation/09-decisions-a-prendre.md:101-102` ;
>   * `md/adr/2026-10-08-notes-seance-adr.md:26` et `:54`.
> * `01:774` dit que la vente doit tomber « DANS la validité du mandat ». Le
>   commentaire juste en dessous le nuance (`01:781-784`). À fusionner quand la
>   règle sera codée.
> * `livrables/2-modelisation/09-contraintes-a-coder.md:80-81` (« à
>   préciser ») est réglé par Q-MAN-04 : la vente pointe vers le nouveau mandat.
> * Page Confluence d'ADR-013 : 💡 ajouter une note « partie `Mandate` amendée
>   par ADR-050 : plus d'avenant », si le groupe garde le mot « amende » (le
>   modèle du sujet ne le connaît pas, `JOURNAL-DE-DECISIONS.md:22`).
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-050 : Renouvellement du mandat — une chaîne sans branche, `'renewed'` sur l'ancien, pas d'avenant ; l'acte signé après la fin

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions du 05/10, du 07/10 et du 08/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * le sujet du formateur, pour la règle de fond (renouvelable à l'échéance, sans vente ; acte signé après la fin) ;
  * le groupe, pour la mise en œuvre (registre, Q-MAN-03 et Q-MAN-04, 05/10/2026) ;
  * le client, Jeff (Q-JEF-07 et Q-JEF-11, entretien du 07/10/2026) ;
  * Gabriel, au nom du groupe, pour le sens de `'renewed'` et l'absence d'avenant (Discord, 08/10/2026).
* **Complète :** ADR-010 (qui reste « accepté »)
* **Amende :** ADR-013, pour la table `Mandate` seulement : plus d'avenant
* **Remplace :** l'ancienne décision D8 du livrable de modélisation (`09-decisions-a-prendre.md:105-125`). Ce n'est pas un ADR.
* **S'appuie sur :** ADR-023 (`ends_at` stocké) ; ADR-039 (période du mandat) ; ADR-024 (paiement refusé)

**Contexte**

Le sujet pose deux règles :

* Le mandat « peut être renouvelé à l'échéance si aucune vente n'a abouti » (`user-stories/00_regles_metier_mandat_remuneration.feature:40`).
* « Un acte signé après cette date n'ouvre aucun droit, sauf renouvellement du mandat » (`REGLES-CALCUL-REMUNERATION.md:98`).

Il ne dit pas comment relier deux mandats, ni combien de fois renouveler. Il ne parle pas d'avenant : 0 fichier du StarterPack contient le mot (recherche du 08/10/2026).

Trois textes du groupe existaient déjà :

* ADR-010 (19/08/2026) : une clé réflexive `id_mandate_parent` ; « Le nouveau mandat enregistre l'ID de l'ancien ».
* ADR-013 (22/08/2026) : le même type de lien sur `Criteria` et sur `Mandate`, pour les versions et les avenants.
* L'ancienne décision D8 du livrable : `'renewed'` est le statut du **nouveau** mandat. Un `CHECK`, `chk_renewed`, l'imposait (`09-decisions-a-prendre.md:115-117`).

Le 08/10/2026, le groupe a inversé le sens de `'renewed'` et refusé les avenants.

**Options envisagées**

Une sous-décision par bloc. L'option retenue est marquée **retenue** ; les autres sont écartées.

1. **Le lien entre deux mandats**
   * Une table d'historique à part. Écartée par ADR-010.
   * Une clé réflexive `id_mandate_parent`. **Gardée** (ADR-010, option 2).
2. **Le sens de `'renewed'`**
   * Le statut du nouveau mandat (ancienne décision D8). Écartée.
   * Le statut de l'ancien mandat. **Retenue** (Gabriel, 08/10/2026).
3. **Les avenants**
   * Sur le même lien que les renouvellements (ADR-013). Écartée.
   * Aucun avenant. **Retenue** (Gabriel, 08/10/2026).
4. **Le nombre de renouvellements**
   * Limité. Écartée : aucune source ne donne de limite.
   * Sans limite. **Retenue** (Q-MAN-03, Q-JEF-07).
5. **La vente, après un renouvellement**
   * Sur le premier mandat de la chaîne. Écartée : le code devrait chercher son successeur avant de comparer les dates (`09-decisions-a-prendre.md:173-174`).
   * Sur le dernier mandat. **Retenue** (Q-MAN-04).
6. **L'acte signé après la fin du mandat**
   * Payer quand même. Écartée : aucune source ne le dit (`09-decisions-a-prendre.md:161`).
   * Ne jamais payer. Écartée : le sujet prévoit « sauf renouvellement » (`REGLES-CALCUL-REMUNERATION.md:98`).
   * Pas de paiement, sauf si le mandat a été renouvelé. **Retenue** (tranchée par le sujet).

**Décision**

1. Le nouveau mandat porte dans `id_mandate_parent` l'identifiant du mandat qu'il renouvelle. Un premier mandat le laisse vide. (Repris d'ADR-010.)
2. `'renewed'` est le statut de **l'ancien** mandat.
3. **Pas d'avenant.** Un mandat a au plus un successeur : `id_mandate_parent` est `UNIQUE` (`01:470`). Les renouvellements forment une chaîne, sans branche.
4. Un mandat se renouvelle à l'échéance, **seulement sans vente** (`00_…feature:40`). Ce contrôle relève de l'API (Q-MAN-03) : **à coder**.
5. **Sans limite** de nombre (Q-MAN-03, Q-JEF-07).
6. La vente pointe vers le **dernier** mandat de la chaîne (Q-MAN-04). Un mandat a au plus une vente (`sale.id_mandate` est `UNIQUE`, `01:763`).
7. Le délai entre la signature du mandat et l'acte est l'un des cinq critères de la note du chasseur (`REGLES-CALCUL-REMUNERATION.md:55`). Il part de la **première** signature (Q-MAN-04). Le code **devra** remonter la chaîne `id_mandate_parent` pour la trouver : pas encore codé (`questions-a-trancher.md:841`). ADR-010 le prévoyait déjà (copie du journal, l. 254).
8. **Acte signé après la fin.**
   * La date de l'acte se compare à `ends_at` du mandat de la vente, donc du dernier de la chaîne.
   * Après cette date : pas de rémunération (`10_calcul_remuneration_chasseur.feature:45-50`). Le paiement est refusé, motif `'mandate_expired'` : voir ADR-024.
   * Un mandat renouvelé a une nouvelle fin. C'est ainsi que joue « sauf renouvellement ».

Pendant un renouvellement, l'exclusivité ne bloque pas : le trigger exclut le parent et l'enfant l'un pour l'autre (ADR-039, Décision 2).

**Justification**

* **Une clé réflexive** : la méthode la plus simple (ADR-010). Rien ne l'a remise en cause.
* **`'renewed'` sur l'ancien** : choix du groupe (« on veut », Gabriel, 08/10/2026).
  * 💡 Raison proposée : chaque information a une seule place. L'origine du nouveau mandat est dans `id_mandate_parent`. Le sort de l'ancien est dans son statut, comme `'expired'` ou `'canceled'`.
  * Avec l'ancienne décision, `'renewed'` répétait `id_mandate_parent`. Il fallait un `CHECK` pour garder les deux d'accord (`09-decisions-a-prendre.md:115-117`).
  * Inconvénient accepté : « `'renewed'` ⇒ un successeur existe » ne se vérifie plus par un `CHECK`, car un `CHECK` ne voit qu'une ligne. L'API devra le garantir (Questions tranchées, n° 2).
* **Pas d'avenant** : le sujet n'en parle pas, et le groupe n'en veut pas (« on veut pas des avenants », Gabriel, 08/10/2026).
  * Ce qui évolue au fil du mandat, c'est la demande du client. Le sujet demande d'en historiser les versions (`Readme.md:234`). `criteria.id_previous_version` le fait déjà (`01:399-400`). Déduit.
  * Avec un seul successeur par mandat, « le dernier de la chaîne » est unique. La vente et le délai se calculent sans ambiguïté.
* **Vente sur le nouveau mandat, délai depuis la première signature** :
  * Le nouveau mandat est le seul valide à la date de l'acte (`questions-a-trancher.md:839`).
  * La grille du délai va jusqu'à « > 48 sem. » (`REGLES-CALCUL-REMUNERATION.md:143`) : elle suppose plusieurs renouvellements (`questions-a-trancher.md:828`, `:840`).
  * L'exemple du sujet le montre. Le délai de Bruno, 258 jours, part du 14/11/2025 (`REGLES-CALCUL-REMUNERATION.md:237`, `:243`). La feature dit seulement « un mandat exclusif signé le "2025-11-14" » (`10_…feature:256`). Le renouvellement y est sous-entendu (`09-decisions-a-prendre.md:158`). Jeff l'a confirmé (Q-JEF-11).
* **Acte signé après la fin** : le sujet donne les deux cas, avec les mêmes dates.
  * Mandat non renouvelé : 0,00 € (`10_…feature:45-50`).
  * Mandat de Bruno, renouvelé : 6231,60 € (`10_…feature:255-264`).

**Conséquences**

* ✅ **Déjà fait dans le code**
  * Schéma : `id_mandate_parent` `UNIQUE`, `chk_renewed` retiré (`docker/init-v3/01_create_fil_rouge_immobilier.sql:465-470`, commit `6be4e56`).
  * Base existante : migration `docker/migrations/v2-vers-v3/16_mandat-renouvellement-sans-avenant.sql` (commit `4b16839`).
  * 2 tests d'intégration (`API/tests/integration/test_constraints_db.py`) :
    * un exclusif renouvelé est accepté, puis l'ancien passe à `'renewed'` (`:332-353`) ;
    * un second successeur est refusé (`:356-367`).
  * Données reprises : 18 mandats, aucun parent, aucun `'renewed'` (`docker/init-v3/02_migration.sql:238-255`). La migration 16 n'a rien à faire relire à la main.
  * MPD v8 (08/10/2026) : `UNIQUE` sur `id_mandate_parent`, plus de `chk_renewed` (`md/adr/2026-10-08-notes-seance-adr.md:110`).
* ➡️ **Reste à coder dans l'API.** `MandateService` n'a aucune règle : il hérite du CRUD générique (`API/src/app/services/mandate_service.py:1-8`). `id_mandate_parent` n'apparaît que dans le modèle (`API/src/app/models/mandate_model.py:35`).
  * L'opération de renouvellement : refuser s'il y a une vente ; créer le successeur et passer l'ancien à `'renewed'`, ensemble (`09-contraintes-a-coder.md:225-233`).
  * La remontée de la chaîne, pour le délai.
  * Le droit au paiement après la fin. Le calcul du sujet le fait déjà (`API/src/app/services/remuneration.py:168-169`), mais il n'est pas branché sur la base.
  * Le principe « dans l'API, chaque règle testée » est l'objet d'ADR-040 (Q-MAN-06).
* ⚠️ **Limite à connaître.** Aujourd'hui, rien n'empêche un `'renewed'` sans successeur. Aucune contrainte ne le vérifie (`01:465-470`), et `PUT /mandates/{id}` accepte ce statut. Le test l'utilise, mais seulement après avoir créé l'enfant (`test_constraints_db.py:348-353`).
  * 💡 Proposition : le service refuse `'renewed'` si aucun mandat ne pointe vers celui-ci, avec un test.
* **Anciens ADR**
  * ADR-010 reste « accepté ». Rien de son contenu n'est contredit : cette fiche le complète.
  * ADR-013 reste « accepté » pour `Criteria`. Sa partie `Mandate` est amendée : plus d'avenant (Questions tranchées, n° 1).
  * ADR-004 reste « remplacé par ADR-023 ». Sa colonne `renewal_count` reste inutile : la chaîne donne le nombre de renouvellements.
* **Performance** : la baisse des indicateurs quand un mandat arrive à échéance sans vente (`Readme.md:135`) relève de l'ADR des critères de performance (numéro proposé 048), pas de celui-ci.

**Questions tranchées par les sources**

1. **Cette fiche remplace-t-elle ADR-013 en entier ?**
   **Non : seulement sa partie `Mandate`.** Déduit, pas décidé.
   * ADR-013 couvre aussi `Criteria` : son titre dit « Tables Criteria et Mandate » (copie du journal, l. 310).
   * `criteria.id_previous_version` existe toujours (`01:399-400`).
   * Le sujet demande d'historiser les versions de la demande (`Readme.md:234`).
2. **« `'renewed'` ⇒ un successeur existe » : où le garantir ?**
   **Dans l'API, par l'opération de renouvellement elle-même.** Elle crée le successeur et passe l'ancien à `'renewed'`, dans la même transaction. Déduit, pas décidé. Rien n'est codé.
   * Q-MAN-03 met le contrôle du renouvellement dans `mandate_service` (`questions-a-trancher.md:830`).
   * Le bloc « Renouveler un mandat » du livrable des contraintes (`09-contraintes-a-coder.md:225-233`).
   * Le principe des règles sur plusieurs tables, dans l'API (Q-MAN-06, ADR-040).
3. **Après un renouvellement, vers quel mandat pointe la vente ?**
   **Le nouveau**, le dernier de la chaîne. La comparaison avec `ends_at` est directe.
   * Q-MAN-04 (`questions-a-trancher.md:833-841`).
   * Point d'étape du 21/09/2026, question 5 (`md/journal/2026-09-21-point-etape.md:116`).
4. **Acte signé après la fin d'un mandat non renouvelé : la vente est-elle refusée ?**
   **Non : elle s'enregistre, et c'est le paiement qui est refusé.** Le détail est dans ADR-024. Déduit, pas décidé.
   * Un paiement exige une vente (`payment.id_sale NOT NULL`, `01:932`). Le motif `'mandate_expired'` n'aurait sinon aucune ligne où vivre (`01:893-901`).
   * Le commentaire du schéma dit « non refuser sèchement » (`01:781-784`).
5. **Le mandat de Bruno, dans l'exemple du sujet, est-il un renouvellement ?**
   **Oui.** Jeff l'a confirmé (Q-JEF-11, `md/questions/2026-10-07-questions-pour-jeff.html:348`).
   * Le code d'exemple du sujet met sa fin au 14/08/2026, soit 9 mois (`REGLES-CALCUL-REMUNERATION.md:697`). Ce n'est ni 6 mois, ni un renouvellement : un défaut du sujet, à ne pas recopier (`09-decisions-a-prendre.md:180-183`).

**Questions ouvertes** 🟡

Aucune.

**Sources**

| Affirmation | Source |
|---|---|
| Renouvelable à l'échéance, si aucune vente n'a abouti | `00_regles_metier_mandat_remuneration.feature:40` ; `Readme.md:73` ; `GLOSSAIRE-METIER.md:14` |
| Acte après la fin : aucun droit, sauf renouvellement | `REGLES-CALCUL-REMUNERATION.md:98` ; `10_calcul_remuneration_chasseur.feature:45-50` ; ancienne décision D3, `09-decisions-a-prendre.md:129-185` |
| Pas d'avenant dans le sujet | recherche « avenant » dans le StarterPack, 08/10/2026 : 0 fichier |
| ADR-010 : clé réflexive, « remonter cette chaîne » | journal de décisions Confluence (page 15466509), copie du 07/10/2026, l. 234-254 |
| ADR-013 : `Criteria` et `Mandate`, versions et avenants | même copie, l. 310-338 |
| ADR-004, ADR-023 | même copie, l. 85-88 et l. 764-804 |
| Ancienne décision D8 et `chk_renewed` | `09-decisions-a-prendre.md:96-125` |
| `'renewed'` sur l'ancien ; pas d'avenant | Gabriel, Discord, 08/10/2026 (`md/adr/2026-10-08-notes-seance-adr.md:26-27`) ; `01:465-470` ; commits `6be4e56`, `4b16839` |
| Sans vente, sans limite ; vente sur le nouveau ; délai depuis la 1re signature | Q-MAN-03, Q-MAN-04 (`questions-a-trancher.md:822-841`) ; Jeff, Q-JEF-07 (`2026-10-07-questions-pour-jeff.html:347`) |
| Délai mandat → acte : un des cinq critères ; grille jusqu'à « > 48 sem. » (critère S₁) | `REGLES-CALCUL-REMUNERATION.md:55`, `:143` |
| Bruno : 258 jours depuis le 14/11/2025 ; payé 6231,60 € ; renouvellement sous-entendu | `REGLES-CALCUL-REMUNERATION.md:237`, `:243` ; `10_…feature:255-264` ; `09-decisions-a-prendre.md:158` ; Jeff, Q-JEF-11 (`2026-10-07-questions-pour-jeff.html:348`) |
| Fin à 9 mois dans le code du sujet | `REGLES-CALCUL-REMUNERATION.md:697` ; `09-decisions-a-prendre.md:180-183` |
| Un mandat, au plus une vente ; un paiement, une vente | `01:763` ; `01:932` |
| Motif `'mandate_expired'` | `01:893-901` ; ADR-024 |
| La demande s'historise | `Readme.md:234` ; `01:399-400` |
| Données reprises sans renouvellement | `docker/init-v3/02_migration.sql:238-255` |
| Tests | `API/tests/integration/test_constraints_db.py:332-367` |
| Aucune règle de mandat dans l'API | `API/src/app/services/mandate_service.py:1-8` ; `API/src/app/models/mandate_model.py:35` |
| Calcul du sujet : acte après la fin | `API/src/app/services/remuneration.py:168-169` |
| Opération de renouvellement à coder | `09-contraintes-a-coder.md:225-233` |
| Performance revue à la baisse sans vente | `Readme.md:135` |
| Modèle d'ADR : une fiche par décision, numérotation, statuts | `documents utiles/JOURNAL-DE-DECISIONS.md:7`, `:19-40`, `:22`, `:70` |

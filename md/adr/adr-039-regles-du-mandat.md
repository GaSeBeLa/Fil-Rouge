# ADR-039 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 039 est une proposition** : lettre L de
> `md/adr/2026-10-08-proposition-regroupement-adr.md:62`.
>
> ✂️ **Coupé en deux par l'arbitre le 08/10/2026.** Le premier jet « Règles du
> mandat » mêlait cinq sujets. Les notes du jour laissaient le choix ouvert
> (« un seul ADR, ou deux », `md/adr/2026-10-08-notes-seance-adr.md:59`). Le
> modèle du sujet veut « une fiche courte par décision »
> (`JOURNAL-DE-DECISIONS.md:7`) et des numéros qui se suivent (`:70`). D'où :
>
> * **ADR-039 (cette fiche) : la période du mandat** — 6 mois, exclusivité,
>   annulation, mandat clos ;
> * **ADR-050 : le renouvellement du mandat** — chaîne, `'renewed'`, pas
>   d'avenant, acte signé après la fin (`md/adr/adr-050-renouvellement-du-mandat.md`).
>   050 est le premier numéro libre après les propositions 028 à 049.
>
> 💡 **Rédigé le 08/10/2026 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et
> un arbitre.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * MPD v8 : la note du trigger est loin de la table `Mandate`, sans trait : à
>   rapprocher (`md/adr/2026-10-08-notes-seance-adr.md:112`).
> * Le commentaire `docker/init-v3/01_create_fil_rouge_immobilier.sql:454-455`
>   attribue « figer la date » à ADR-018. C'est ADR-023 : ADR-018 porte sur la
>   performance énergétique (journal Confluence : titres d'ADR-018 et d'ADR-023).
> * Si le groupe confirme la Décision 5 : le code à changer est listé dans les
>   Conséquences. Rien n'a été touché.
>
> ⚠️ **Pour l'oral** : ne pas dire « Merise n'a pas de symbole pour un
> trigger ». Les notes du jour le disent « de mémoire, non vérifié »
> (`2026-10-08-notes-seance-adr.md:120`). Ce qui est vérifié : le sujet ne
> donne aucune notation (Décision 3).
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-039 : Période du mandat — 6 mois exacts, exclusivité par un trigger, un mandat annulé ou clos libère le client

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions du 05/10 et du 07/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * le sujet du formateur, pour les règles de fond (6 mois, exclusivité) ;
  * le groupe, pour leur mise en œuvre (registre, Q-MAN-01, Q-MAN-02 et Q-MAN-07, 05/10/2026 ; cartes du lot 4 gardées le 07/10/2026) ;
  * le client, Jeff, pour l'annulation (Q-JEF-06, entretien du 07/10/2026) ;
  * Sébastien, pour la note du trigger sur le MPD (08/10/2026).
* **S'appuie sur :** ADR-023 (`ends_at` stocké, pas calculé)
* **Voir aussi :** ADR-050 (renouvellement du mandat)

**Contexte**

Le sujet pose ces règles sur la période du mandat de recherche :

* Il vaut 6 mois, renouvelable (`Readme.md:73`, `REGLES-CALCUL-REMUNERATION.md:57`).
* Une signature le 2026-02-25 donne une fin le 2026-08-25 (`user-stories/00_regles_metier_mandat_remuneration.feature:38-39`).
* Exclusif, il écarte tout autre chasseur : « aucun autre chasseur ne peut agir pour le compte d'Alice pendant la durée du mandat » (`00_…feature:20`).
* Deux mandats non exclusifs peuvent coexister (`00_…feature:30-34`).

Le sujet ne dit rien de l'annulation. Recherche dans tout le StarterPack : « annul » et « résili », aucune occurrence sur le mandat.

Avant le 05/10/2026, le schéma n'imposait presque rien (`md/questions/questions-a-trancher.md:801-802`, `:811-815`) :

* Le `CHECK` de `ends_at` n'imposait que l'ordre des dates. Un mandat « peut durer 10 ans ou 1 jour ».
* Le trigger d'exclusivité était écrit, mais pas activé. Tel quel, il aurait bloqué le renouvellement d'un mandat exclusif.

Le groupe a tranché le 05/10/2026. Le client a confirmé l'annulation le 07/10/2026. Le code a suivi au lot 4 du chantier de migration, le 07/10/2026.

**Options envisagées**

Une sous-décision par bloc. L'option retenue est marquée **retenue** ; les autres sont écartées.

1. **Durée du mandat**
   * Garder le `CHECK` de l'ordre des dates (schéma v2). Écartée : il laisse passer 10 ans ou 1 jour.
   * Calculer la fin à la lecture, avec une colonne `duration` (ADR-004). Écartée par ADR-023 : la fin est une donnée du contrat, elle se fige.
   * Stocker `ends_at` et imposer « exactement 6 mois » par un `CHECK`. **Retenue** (Q-MAN-01).
2. **Exclusivité**
   * `EXCLUDE … WHERE (is_exclusive)`. Écartée : elle ne compare que les exclusifs entre eux ; un non-exclusif posé pendant un exclusif passe (`docker/init-v3/01_create_fil_rouge_immobilier.sql:501-502`).
   * `EXCLUDE` sans filtre. Écartée : elle refuse aussi deux non-exclusifs, que le sujet autorise (`01:503-505`).
   * Contrôle dans l'API (envisagé : « un trigger (ou l'API) », `livrables/2-modelisation/09-contraintes-a-coder.md:269-272`). Écartée par le registre : Q-MAN-02 dit « corriger, activer » le trigger déjà écrit.
   * Un trigger, `trg_mandate_exclusivity`. **Retenue** (`01:506-507`, `:522-550`).
3. **Ne pas bloquer un renouvellement** (le renouvellement lui-même : ADR-050)
   * Exclure du contrôle le parent et l'enfant d'un renouvellement. **Retenue** (lot 4, carte gardée par le groupe le 07/10/2026).
   * Exclure du contrôle les mandats déjà finis (proposé par le registre, `questions-a-trancher.md:817`). Pas retenu pour le renouvellement : le groupe a gardé l'autre moyen. L'idée revient au bloc 5.
4. **Mandat annulé** (décision D7, `livrables/2-modelisation/09-decisions-a-prendre.md:404-409`)
   * A : il bloque le client jusqu'à `ends_at`. Écartée.
   * B : l'annulation libère le client tout de suite. **Retenue** (Jeff, Q-JEF-06).
   * Annuler un mandat jamais signé : interdit par `chk_status_signature` en v2, ou permis. **Permis** (Q-MAN-07).
5. **Mandat clos avant sa fin** (`'completed'` ou `'lost'`)
   * A : il bloque le client jusqu'à `ends_at`. C'est le code d'aujourd'hui, et la lecture littérale de « pendant la durée du mandat ». Écartée.
   * B : il libère le client tout de suite, comme l'annulation. **Retenue, par déduction — confirmée par Sébastien le 2026-10-09 (Discord)** (Questions tranchées, n° 1).

**Décision**

1. **Durée.**
   * `ends_at` vaut exactement `signature_date + 6 mois` : `CHECK chk_mandate_six_months` (`01:485-488`).
   * Sans signature, pas de fin : les deux colonnes sont vides ensemble.
   * Fin de mois : pour un 31/08, PostgreSQL rend le 28 ou le 29/02 (`01:483-484`). L'API devra calculer de la même façon (`01:484`) : pas encore codé.
2. **Exclusivité, par un trigger.**
   * `trg_mandate_exclusivity` (fonction `check_mandate_exclusivity`) s'exécute avant chaque `INSERT` et chaque `UPDATE` sur `mandate` (`01:548-550`).
   * Il refuse un mandat signé, non annulé, si un autre mandat du **même client**, signé et non annulé, chevauche sa période, et si **l'un des deux** est exclusif (`01:529-539`).
   * Les périodes se comparent bornes comprises (`'[]'`).
   * Le parent et l'enfant d'un renouvellement sont exclus l'un pour l'autre, dans les deux sens (`01:535-536`). Le renouvellement est l'objet d'ADR-050.
   * Le refus porte le code `23514` (`01:543`). L'API répond `409` (`API/tests/integration/test_constraints_db.py:311-316`).
3. **Le trigger sur le MPD.** Il est dit par une **note** sous la table `Mandate`. Le sujet ne donne aucune notation pour un trigger : le mot n'apparaît nulle part dans le StarterPack (recherche du 08/10/2026). L'équipe a choisi une note libre (Sébastien, 08/10/2026).
4. **Annulation.**
   * `'canceled'` est permis sans date de signature (`chk_status_signature`, `01:474-478`).
   * Un mandat `'canceled'` libère le client tout de suite : il ne bloque personne, et rien ne le bloque (`01:509-510`, `:525-527`, `:533`).
5. **Mandat clos.** Un mandat `'completed'` ou `'lost'` libère lui aussi le client tout de suite. Tranchée par déduction — confirmée par Sébastien le 2026-10-09 (Discord) (Questions tranchées, n° 1). ⚠️ **Pas encore dans le code** : aujourd'hui, le trigger n'ignore que `'canceled'` (`01:526`, `:533`).
   * `'expired'` et `'renewed'` ne posent pas la question : ils viennent à l'échéance (`00_…feature:40`), quand la période est finie (déduit). La liste des statuts : `01:446-449`.

**Justification**

* **6 mois exacts** : « 6 mois renouvelable » est une règle du sujet, pas un paramètre (`questions-a-trancher.md:804`). La base peut la vérifier seule : elle la vérifie.
* **Trigger plutôt qu'`EXCLUDE`** : mesuré, pas supposé (`01:500-507`). Un `EXCLUDE` ne sait pas dire « si l'un des deux est exclusif ». Le trigger s'applique à toute écriture, qu'elle vienne de l'API ou d'un script.
* **Annulation qui libère** : bloquer un client sur un mandat annulé n'a pas de sens métier évident (`questions-a-trancher.md:820`). Le client l'a confirmé (Q-JEF-06).
* **Parent et enfant exclus l'un pour l'autre** : un renouvellement signé à l'échéance touche la fin de son parent. Avec le seul parent exclu, passer le parent à un statut de fin après son renouvellement était refusé. Mesuré au lot 4 (`md/journal/2026-10-07-rapport-lot1-a-lot5.html:469`). Carte gardée par le groupe le 07/10/2026 (`questions-a-trancher.md:151`).
* **Mandat clos qui libère** : un mandat clos n'est plus en vigueur, comme un mandat annulé. Le raisonnement complet est dans les Questions tranchées, n° 1.

**Conséquences**

* ✅ **Déjà fait dans le code**
  * Schéma : `docker/init-v3/01_create_fil_rouge_immobilier.sql:437-550`.
  * Base existante : migration `docker/migrations/v2-vers-v3/04_mandat-duree-exclusivite.sql` (lot 4).
  * 6 tests d'intégration portent ces règles (`test_constraints_db.py:286-330`) : annuler sans signature, refuser un mandat actif sans signature, 6 mois acceptés, 7 mois refusés, un second mandat pendant un exclusif refusé, un mandat accepté après l'annulation d'un exclusif.
  * Données reprises : compté au lot 4 sur les 17 mandats d'alors, 0 hors des 6 mois, 0 paire en conflit (`md/journal/2026-10-07-rapport-lot1-a-lot5.html:382`).
  * MPD v8 (08/10/2026) : note du trigger posée.
* ➡️ **Reste à coder pour la Décision 5**, si le groupe la confirme :
  * le trigger : `01:526` et `01:533` ignorent aussi `'completed'` et `'lost'`, pas seulement `'canceled'` ;
  * une migration v2 → v3 pour une base existante ;
  * deux tests : un mandat accepté après un exclusif `'completed'` ; un exclusif accepté après un non-exclusif `'lost'`. Aucun test ne couvre ce cas aujourd'hui (`test_constraints_db.py:275-367`).
  * Le changement ne fait que relâcher la règle : aucune donnée qui passe aujourd'hui ne peut être refusée demain (déduit).
* ➡️ **Reste à coder dans l'API** : le calcul de `ends_at`. Aujourd'hui, l'API reçoit la date, et la base la vérifie. `MandateService` n'a aucune règle : il hérite du CRUD générique (`API/src/app/services/mandate_service.py:1-8`).
* **La règle se lit par client, pas par bien** (rapport LOT1→LOT5, carte « par client », gardée le 07/10/2026).
* **Anciens ADR :** ADR-004 reste « remplacé par ADR-023 ».

**Questions tranchées par les sources**

1. **Un mandat clos avant sa fin (`'completed'` ou `'lost'`) bloque-t-il encore le client jusqu'à `ends_at` ?**
   **Non : il le libère tout de suite, comme l'annulation. Tranchée par déduction — confirmée par Sébastien le 2026-10-09 (Discord).** Elle demande un changement de code (trigger, migration, tests : voir Conséquences).
   * Le client a déjà lu « pendant la durée du mandat » comme « tant que le mandat est en vigueur » : un mandat annulé libère tout de suite (Jeff, Q-JEF-06, `md/questions/2026-10-07-questions-pour-jeff.html:345`). Un mandat clos n'est plus en vigueur non plus.
   * L'exclusivité sert la rémunération du chasseur : « Un mandat exclusif garantit la rémunération même en cas de découverte autonome » (`00_…feature:15`). Un mandat clos n'a plus rien à protéger. Un mandat a au plus une vente (`sale.id_mandate UNIQUE`, `01:763`). Sur un mandat `'lost'`, personne n'est payé (Q-JEF-03).
   * L'achat clôt la relation (`03_particulier_offre_et_signature.feature:8`). Le sujet prévoit ensuite des « offres régulières de services » (`03_…feature:43` ; `Readme.md:104`). Bloquer le client jusqu'à `ends_at` irait contre.
   * Le registre avait proposé d'exclure « les mandats déjà finis » (`questions-a-trancher.md:817`). La réponse du groupe, « Corriger, activer, l'annulation libère tout de suite » (`:810`), ne l'a pas écarté.
   * Le rapport du lot 4 laissait le cas « point ouvert » pour `'lost'` (`md/journal/2026-10-07-rapport-lot1-a-lot5.html:388`).
   * Contre : la lettre de « pendant la durée du mandat » (`00_…feature:20`). Mais le trigger ne la suit déjà pas à la lettre. La phrase vise « aucun autre chasseur » ; le trigger compare par client, sans regarder le chasseur, donc il bloque aussi le même chasseur (`01:529-539`). Et il libère sur une annulation.
   * 💡 Pour la valider : le groupe l'adopte, puis informe Jeff, comme pour Q-JEF-19.

**Questions ouvertes** 🟡

1. **L'exclusivité vaut-elle par client ou par recherche ?** 🟡 À faire confirmer par Jeff.
   * Aujourd'hui le trigger compare les mandats du **même client** (`01:529-539`) : un exclusif bloque tout autre mandat du client sur la période.
   * 💡 Proposition (Gabriel puis Sébastien, 2026-10-09, Discord) : l'exclusivité vaut **par recherche**. Un client peut signer plusieurs exclusifs sur des **recherches différentes** ; sur une même recherche, un exclusif exclut tout autre mandat qui se chevauche. Le trigger ajouterait `m.id_search_request = NEW.id_search_request` (`mandate.id_search_request`, `01:463`).
   * Le sujet dit « aucun autre chasseur ne peut agir pour le compte d'Alice pendant la durée du mandat » (`00_…feature:20`), dans un contexte d'**une** demande de recherche (`:11`) : les deux lectures sont possibles.
   * ⚠️ Limite à écrire si adoptée : un client pourrait déposer une seconde recherche quasi identique pour contourner l'exclusivité.
   * Statut : 💡 proposée, pas acceptée. Rien n'est changé dans le trigger tant que Jeff n'a pas confirmé.

**Sources**

| Affirmation | Source |
|---|---|
| 6 mois, renouvelable | `Readme.md:73` ; `REGLES-CALCUL-REMUNERATION.md:57` ; `GLOSSAIRE-METIER.md:14` ; `00_…feature:37-40` |
| Exclusif : aucun autre chasseur pendant la durée du mandat ; il garantit la rémunération | `00_…feature:15-20` ; `Readme.md:75-76` |
| Deux non-exclusifs peuvent coexister | `00_…feature:30-34` |
| Ni annulation ni résiliation du mandat dans le sujet | recherche « annul », « résili » dans le StarterPack, 08/10/2026 |
| Le mot « trigger » absent du sujet | recherche « trigger » dans tout le StarterPack, 08/10/2026 : 0 fichier |
| `CHECK` des 6 mois, fin de mois, « l'API devra calculer pareil » | `01:480-488` ; Q-MAN-01 (`questions-a-trancher.md:798-806`) |
| Annuler sans signature | `01:472-478` ; Q-MAN-07 (`questions-a-trancher.md:874-881`) |
| Pourquoi pas `EXCLUDE` | `01:500-507` |
| Le trigger et ses exclusions ; seul `'canceled'` ignoré | `01:522-550` ; `04_mandat-duree-exclusivite.sql:48-79` ; `docker/init-v3/README.md:38-39` |
| Option « exclure les mandats déjà finis » | `questions-a-trancher.md:817` |
| L'annulation libère tout de suite | Jeff, Q-JEF-06 (`2026-10-07-questions-pour-jeff.html:345`, `:1240`) ; `questions-a-trancher.md:1167` ; ancienne décision D7, `09-decisions-a-prendre.md:397-414` |
| Parent et enfant exclus ; règle par client | rapport LOT1→LOT5, cartes D3 et D4 (`2026-10-07-rapport-lot1-a-lot5.html:461-489`) ; gardées le 07/10 (`questions-a-trancher.md:151`) |
| `'lost'` bloque encore l'exclusivité, « point ouvert » ; comptage du lot 4 ; parent seul exclu = parent bloqué | même rapport, l. 382, l. 388, l. 469 |
| Les 7 statuts du mandat | `01:446-449` |
| Un mandat, au plus une vente | `01:763` |
| L'achat clôt la relation ; offres de services ensuite | `03_particulier_offre_et_signature.feature:8`, `:43` ; `Readme.md:104` (StarterPack) |
| Rien pour personne sur une vente perdue | Jeff, Q-JEF-03 ; ADR-024 |
| Note du trigger sur le MPD | Sébastien, décision 7 (`2026-10-08-notes-seance-adr.md:32`, `:107-113`) |
| ADR-004, ADR-023 | journal de décisions Confluence (page 15466509), lu dans sa copie du 07/10/2026 |
| Tests | `API/tests/integration/test_constraints_db.py:286-330` ; aucun sur un mandat clos (`:275-367`) |
| Aucune règle de mandat dans l'API | `API/src/app/services/mandate_service.py:1-8` |
| Modèle d'ADR : une fiche par décision, numérotation | `documents utiles/JOURNAL-DE-DECISIONS.md:7`, `:19-40`, `:70` |

# Vérification de l'audit `problemes-a-regler.md` (P1 à P36)

> **Fait le 2026-10-12 par Claude**, à la demande de Sébastien (« go A »), d'après la
> consigne de Gabriel (Discord, 11/10/2026, `message.txt`). Dépôt au commit `43718ed`.
>
> ⚠️ **Limite d'indépendance.** L'audit a été écrit par Claude ; cette vérification aussi.
> Les tests sont rejoués et les citations relues, mais ce n'est pas un regard extérieur.
> Un second avis par une autre IA reste utile.
>
> **Méthode.** Trois bases neuves sur PostgreSQL 16.15 (`audit_a`, `audit_b`, `audit_c`),
> avec `01` seul pour les preuves, et `01 02 03 05` pour tester les solutions sur les
> données reprises. Chaque essai dans `BEGIN … ROLLBACK`. Un sous-agent par lot de 12 P,
> puis croisement des trois rapports. Les constats les plus lourds ont été relus une
> seconde fois à la source (ADR-041 l. 108, `docker-compose.yml:39`, `database.py:55`,
> ADR-034 l. 125-127, `normalised.py:88-93`, recherche de « EF-11 »).
>
> `notes-pour-jeff.md` (Q1 à Q3) n'était pas disponible : non vérifié.

## Bilan

* **36 P rejoués : 8 ✅ confirmés, 26 ⚠️ à corriger, 2 ❌ faux.**
* Les trous décrits **existent en base** pour les 36. Les ⚠️ portent surtout sur les
  sources, les statuts et les liens avec les ADR, pas sur le fond.
* Les solutions SQL marquées « testé » **marchent** et **ne cassent pas** les données
  reprises (P2, P3, P6, P8, P9, P12, P13, P29, P30, P32, P34, P35, P36).
* Aucun P ne repose sur l'ancienne unité K€.

### Les cinq constats qui comptent

1. **Des ADR déjà décidés ne sont pas cités.** P1 (ADR-040, micro-décision M), P4
   (ADR-029, M), P11 (ADR-039), P14 (ADR-046), P26 (ADR-030, ADR-034, S8), P29, P30
   et P31 (ADR-034). P30 et P31 recommandent même de défaire une décision.
2. **Le statut `'signed'` est mal lu (P21, P27).** `'signed'` = l'offre est signée par
   le client, **pas encore envoyée**. L'offre que le vendeur accepte est `'accepted'`
   (ADR-041 l. 108-110, ordre l. 144). P21 devient faux ; P27 doit viser `'accepted'`.
3. **Des sources mal classées.** Des règles notées « déduites » sont écrites dans un
   `.feature` (P14, P27, P33, P35, P23). À l'inverse, des règles sans source
   recommandent du SQL au lieu de « à trancher » (P2, P12, P25, P28).
4. **Quatre solutions ne marchent pas telles quelles.**
   * P13, option A : deux trous (comparaison à `NULL` sans `COALESCE` ; condition d'un
     seul côté).
   * P26 : l'API se connecte en **superutilisateur** (`POSTGRES_USER`) : un `REVOKE`
     ne fait rien.
   * P34 : `now()` = début de la transaction ; une heure prise en Python juste après est
     refusée.
   * P16 : `NOT VALID` bloque ensuite **toute** modification des 251 lignes, même du prix.
5. **P18 est plus large qu'écrit.** `floor` est défini (`normalised.py:88-93`) : « nombre
   d'étages de l'immeuble », alors que la source donne l'étage du logement. Ce sont les
   **1 026** valeurs reprises qui ont l'autre sens, pas seulement les 125 `last floor`.

## 1. Tableau, une ligne par P

| P | Verdict | Ce qui ne va pas | Preuve |
|---|---|---|---|
| P1 | ⚠️ | Déjà tranché : API (ADR-040 l. 55, l. 133 ; M oui le 09/10). Même trou pour `hunter` et `real_estate_manager`. Règle : ADR-005, `PLAN-DE-TESTS.md:47`, Readme l. 233. | 3 × `INSERT 0 1` |
| P2 | ⚠️ | Faits et SQL justes. Pas de ligne « Règle visée » : aucune source, donc « à trancher ». | index + `CHECK` testés sur les 25 emails repris |
| P3 | ⚠️ | Contredit aussi ADR-043 (décision 4) et ADR-049 l. 114 (l'anonymisation vide l'adresse) ; casse `client_payload` des tests. | `SET NOT NULL` passe sur les 18 clients |
| P4 | ⚠️ | Statut périmé : confirmé (ADR-029, M oui le 09/10). ENF-03 déjà répondu (ADR-029 l. 79-81). | `INSERT 0 1` |
| P5 | ⚠️ | « EF-11 » introuvable (dépôt et starter pack). 25 comptes repris, pas 24. ADR-049 l. 139 et ADR-027 l. 180 non cités. | `count(*)` → 25 |
| P6 | ⚠️ | Les 18 demandes reprises sont `launched` (`02:275-277`), pas `confirmed`. Sans impact sur le `CHECK`. | `CHECK` testé |
| P7 | ✅ | Le sens est déjà écrit (ADR-041 l. 98) ; seul le `COMMENT` manque. | `col_description` vide |
| P8 | ⚠️ | Un `UPDATE` crée encore un cycle de versions ; `PUT /criteria/{id}` est ouvert. | `UPDATE 1` avec les contraintes de P8 |
| P9 | ✅ | Rien à redire. | `CHECK` testé |
| P10 | ✅ | Recoupe P17 pour `estate` (doublon partiel). | `INSERT 0 2` |
| P11 | ⚠️ | Ligne fausse : `01:451-452`, pas 454-455. Déjà connu (ADR-039, bandeau). | `grep -n ADR-018` → 452 |
| P12 | ⚠️ | Classée « hypothèse » mais SQL recommandé. Source côté client : `01_…feature:32-37`. Contre-exemple côté chasseur : `00_…feature:30-34` (Chloé). | FK composite testée |
| P13 | ⚠️ | Option A : deux trous (voir § 2). La FK demande d'abord `UNIQUE (id, id_client)`. Option B suit ADR-050 décision 4. Cycle de deux mandats non signalé. | `INSERT 0 1` / `UPDATE 1` ; version corrigée → `ERROR: U02` |
| P14 | ⚠️ | Règle écrite : `07_…feature:36-41`, `Readme.md:135`. Déjà décidé : ADR-046 l. 189-196, annexe C-e. | `INSERT 0 2` |
| P15 | ✅ | Ajouter : le verrou ne tient qu'en `READ COMMITTED` (niveau de l'API, `database.py:68`). | 2 sessions ; `REPEATABLE READ` → `INSERT 0 1` |
| P16 | ⚠️ | `NOT VALID` bloque toute modification des 251 lignes. Source : `GLOSSAIRE-METIER.md:25`. L'écart vient du CSV brut. | `UPDATE … price = price` refusé |
| P17 | ✅ | Rien à redire. | 4 × `INSERT 0 1` |
| P18 | ⚠️ | `floor` est défini (`normalised.py:88-93`). Les 1 026 valeurs sont concernées. Trancher le sens d'abord. | comptage par valeur |
| P19 | ⚠️ | Règle à marquer « déduit » (`01:657`). | `INSERT 0 1` |
| P20 | ⚠️ | `expired` testé ; ajouter `pending_signature`, accepté aussi. | 3 × `INSERT 0 1` |
| P21 | ❌ | Prémisse fausse : `'signed'` ≠ vente. L'index est contourné par le parcours normal. ADR-045 l. 141 assume l'absence d'`UNIQUE`. À reclasser « à trancher ». | deux offres `accepted` : `UPDATE 2` |
| P22 | ✅ | Effet de bord : changer `mandate.id_hunter` devient impossible. | FK testée |
| P23 | ⚠️ | Source la plus haute : `02_…feature:14-17`, `:21-22` (visites **du chasseur**). La limite au client n'est pas soutenue. | `INSERT 0 1` |
| P24 | ⚠️ | Pas de ligne « Règle visée ». ADR-048 l. 94 : seules les visites client jusqu'à l'acte comptent. | `CHECK` testé |
| P25 | ⚠️ | Aucune source : « à trancher ». « Non annulé » refuserait une visite faite avant l'annulation (pas de date d'annulation). | 3 × `INSERT 0 1` |
| P26 | ⚠️ | `REVOKE` sans effet (superutilisateur). `DELETE` déjà bloqué par `RESTRICT`. Déjà tranché : API (ADR-030 l. 106, ADR-034 l. 182, S8). | `UPDATE` passe ; `DELETE` refusé |
| P27 | ⚠️ | Règle écrite (F03:24-28). Exiger `'accepted'`, pas `'signed'`. | `INSERT 0 1` |
| P28 | ⚠️ | Hypothèse : « à trancher ». 3 mandats repris `completed` sans vente (ADR-046 l. 142). | statut reste `active` |
| P29 | ⚠️ | Connu (ADR-034 l. 169, annexe C-f). Le SQL va contre ADR-034 Décision 3 : au groupe de trancher. `jsonb_typeof` laisse passer `[1,2]`. | 7 `CHECK` testés |
| P30 | ⚠️ | Choix assumé : ADR-034 Décision 5 (« une exception, voulue », Jeff Q-JEF-01). Ne pas l'enlever sans rouvrir Q-REM-19. | `payment_final_rate_check` |
| P31 | ❌ | Pas un défaut : voulu par le sujet (RCR:761, « reçus déjà calculés ») ; connu (ADR-034 l. 170). Reste une tâche à coder. | citations exactes |
| P32 | ✅ | Ajouter : ADR-033 prévoit 7 entrées ; noms de clés à fixer dans le code. Pas de conflit avec la migration 20, qui interdit `NULL`, pas `'{}'`. | `'{}'` → `INSERT 0 1` |
| P33 | ⚠️ | Règle écrite : F10:201, RCR:77, RCR:203. Pas « déduite ». | `INSERT 0 1` |
| P34 | ⚠️ | `now()` = début de transaction ; heure locale refusée aussi. Préférer `clock_timestamp()` avec marge, ou l'API. | `clock_timestamp()` après 1 s → refusé |
| P35 | ✅ | Source : F07:29-41. Même `UNIQUE (id, id_hunter)` que P22 : à créer une fois. | 2 FK testées |
| P36 | ⚠️ | « Aucune source » trop fort : ADR-042 l. 122, ADR-048 point 8 (une note de départ). L'unicité reste à trancher. | index testé |

## 2. Corrections à apporter au fichier, P par P

* **P1** — Statut : « solution tranchée : API (ADR-040 l. 55, l. 133 ; M, 09/10) ; connu (A13) ». Retirer « non vérifié : hunter, manager » (vérifié, même trou). Règle : ADR-005, `PLAN-DE-TESTS.md:47`, Readme l. 233.
* **P2** — Ajouter « Règle visée : aucune source (hypothèse) » ; solution « à trancher, puis SQL ». Testé sur les 25 emails repris : aucun refus.
* **P3** — Citer aussi ADR-043 (décision 4, question 2) et ADR-049 l. 114. Lister les conséquences : adresse neutre à l'anonymisation, `client_payload` à compléter (`test_constraints_db.py:64-72`), ADR-043 à amender.
* **P4** — Statut : « choix assumé et confirmé (ADR-029 ; M, 09/10) ». Retirer « reste à préciser pour ENF-03 » (ADR-029 l. 79-81).
* **P5** — Retirer « EF-11 » ou donner sa source. 24 → **25** comptes. Citer ADR-049 l. 139 (`is_activated` a deux sens) et ADR-027 l. 180 (Q-JEF-25).
* **P6** — Les 18 demandes reprises sont `launched`, toutes avec un chasseur. Règle : ADR-041, décision 1 (l. 96-101).
* **P7** — Rien. Nuance possible : le sens est déjà dans ADR-041 l. 98.
* **P8** — Ajouter : cycle possible par `UPDATE` (testé) ; une version ne se modifie pas, donc fermer `PUT /criteria/{id}` (Readme l. 234). « Probablement un par demande » : vérifié, 18 et 18.
* **P9** — Rien.
* **P10** — Signaler le doublon avec P17 pour `estate`.
* **P11** — Ligne : `01:451-452`. Statut : « connu (ADR-039, bandeau l. 30-32) ».
* **P12** — Côté client : citer `01_…feature:32-37`, ou passer « à trancher ». Côté chasseur : ajouter le contre-exemple `00_…feature:30-34` ; citer ADR-045 (pas de réaffectation dans le MVP).
* **P13** — Option A testée, à écrire ainsi (les deux trous fermés) :
  `AND NOT COALESCE(m.id = NEW.id_mandate_parent AND NEW.signature_date >= m.ends_at, FALSE)`
  `AND NOT COALESCE(m.id_mandate_parent = NEW.id AND m.signature_date >= NEW.ends_at, FALSE)`.
  Sans `COALESCE`, un exclusif sans parent signé le jour de fin d'un autre passe ; d'un seul côté, décaler le parent dans la période de l'enfant passe. Ajouter `UNIQUE (id, id_client)` avant la FK. Classer « successeur d'un autre client » en incohérence de données. Ajouter le cycle. Noter qu'un renouvellement avant l'échéance serait refusé, conforme à `00_…feature:40`. Option B : ADR-050 décision 4 (l. 105), A10.
* **P14** — Règle : `07_…feature:36-41`, `Readme.md:135`, ADR-046 l. 189-192. Statut : « connu (C-e) ; reste à coder ». Une seule fois la phrase sur le `CHECK`.
* **P15** — Ajouter la limite `READ COMMITTED`.
* **P16** — Effet de `NOT VALID` sur les mises à jour ; citer `GLOSSAIRE-METIER.md:25` ; l'écart vient de `normalised/annonces/annonces.csv` (251 lignes).
* **P17** — Rien.
* **P18** — Citer `normalised.py:88-93` ; ampleur : 1 026 valeurs ; trancher le sens (renommer, ou « étage du logement ») avant tout `CHECK`.
* **P19** — Règle « (déduit) », hypothèse `estate_searchrequest` = sélection (`01:657`).
* **P20** — `expired` testé ; ajouter `pending_signature`.
* **P21** — Réécrire : `'signed'` = offre signée, pas envoyée. Retirer `uq_proposed_one_signed`. Question « à trancher » : une seule offre `'accepted'` par mandat ? (ADR-045 l. 141.)
* **P22** — Ajouter l'effet de bord sur `mandate.id_hunter`.
* **P23** — Règle : `02_…feature:14-17`, `:21-22`. Retirer la nuance tirée de `06_`. « À trancher » : la règle vaut-elle pour `'hunter'` ?
* **P24** — Ajouter « Règle visée : aucune source ». Citer ADR-048 l. 94. `CHECK` : testé.
* **P25** — « Règle visée : aucune source (hypothèse) » ; solution « à trancher » ; dire le cas de la visite avant annulation.
* **P26** — Retirer `REVOKE`. Noter `RESTRICT` sur `DELETE`. Solution : API (A5 ; ADR-030 l. 106, ADR-034 l. 182, S8). Étendre la grille antidatée à `commission_scale` (non testé).
* **P27** — Règle : F03:24-28. `'signed'` → `'accepted'`.
* **P28** — « À trancher » d'abord ; citer les 3 `completed` repris sans vente et la vente sur mandat `expired` (A2).
* **P29** — Statut : « connu (ADR-034 l. 169 ; C-f) ». Conflit avec ADR-034 Décision 3 : au groupe. Limite de `jsonb_typeof`.
* **P30** — Statut : « connu et assumé (ADR-034 Décision 5 ; `01:911`) ». Rien à faire sauf si Q-REM-19 est rouvert.
* **P31** — Déclasser en tâche « à coder » (ADR-034 l. 170 ; RCR:761). Retirer « supprimer `window_months` ».
* **P32** — 7 entrées (ADR-033) ; alternative SQL : testée.
* **P33** — Règle : F10:201, RCR:77, RCR:203.
* **P34** — `scored_at` : testé. Ajouter le risque `now()` ; proposer `clock_timestamp()` avec marge, ou l'API.
* **P35** — Règle : F07:29-41. `UNIQUE` partagé avec P22.
* **P36** — Citer ADR-042 l. 122 et ADR-048 point 8.

## 3. Problèmes manquants

* **Cycles de versions** — `criteria` (testé, `UPDATE 1`) et `mandate` (testé : 35 → 36 → 35). Pas de `CHECK` possible ; dans l'API (opération de renouvellement, ADR-050), ou via l'option A de P13 pour les mandats signés.
* **`PUT /criteria/{id}` ouvert** — une version s'écrase, contre Readme l. 234 (`crud_router.py:95-102`).
* **`T_plein` sans colonne** — ADR-048 point 7 le veut dans `hunter_rate_parameters` ; la table ne l'a pas (`01:840-870`). Certitude moyenne.
* **Pied de `01` périmé** — `01:1100` « 19 tables » (il y en a 20) ; `01:1106` renvoie à `init-v2` ; `01:1110` parle de K€ (les données sont en euros). Style.
* **`security.py:42`** — « 24 comptes migrés » : 25. Style.

## 4. Non vérifié

* `notes-pour-jeff.md` (Q1 à Q3), donc la Q2 et ADR-041 l. 149. P13 n'en dépend pas.
* L'API en marche : constats d'API lus dans le code, sans appel HTTP (P1, P2, P8, P9, P12, P34).
* Les décisions sur Discord et Confluence non copiées dans le dépôt (décision de Gabriel du 11/10 sur P3, ADR-005, ADR-022).
* P13 option A : 5 cas ; `test_constraints_db.py` non rejoué avec le trigger modifié.
* P26 : `commission_scale` antidatée non testée. P29 : erreurs Python lues, pas exécutées.
* P15 : coût du verrou ; forme à deux entiers. P2 : adresses email limites (RFC).

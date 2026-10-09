# ADR-040, annexe — état des règles à coder dans l'API

> 📋 **Annexe d'ADR-040, pas un ADR.** ADR-040 fige le raisonnement : où va une
> règle qui croise plusieurs tables. Cette annexe dit où en est le code. Elle
> devient fausse dès qu'une règle est codée : à tenir à jour, ou à dater.
>
> 📅 **État au 08/10/2026.** Mesuré dans les fichiers ce jour-là :
>
> * les 19 services de table autres que `UserService` font 8 lignes chacun,
>   CRUD seul (`API/src/app/services/*_service.py`) ;
> * une recherche dans `services/`, `routes/`, `repositories/`, `utils/` et
>   `main.py`, hors code pur du calcul (`remuneration.py`) et
>   `parametrage_service.py`, ne trouve aucune des colonnes en jeu :
>   `signature_date`, `ends_at`, `id_mandate_parent`, `is_exclusive`,
>   `fees_amount`, `id_parameters_fees`, `id_commission_scale`, `id_author`,
>   `postal_code`, ni `'renewed'`, ni `'lost'` ;
> * une seule règle est codée : l'exclusivité du mandat, par un trigger (B1).
>
> ➡️ **Place finale : `livrables/2-modelisation/09-contraintes-a-coder.md`.**
> Le groupe y range ces règles (carte Q-MAN-06 : « Ces règles se rangent dans
> `09-contraintes-a-coder.md` », `md/questions/questions-a-trancher.md:871`).
> Ce fichier date du 11/09/2026 et est en partie périmé (bandeau d'ADR-040).
> Tâche pour l'équipe : y reporter ce tableau, puis retirer cette annexe.
> L'arbitre ne pouvait écrire que dans `md/adr/`.
>
> ✏️ **Tiré d'ADR-040 par l'arbitre le 08/10/2026**, et complété : règles
> d'ADR-041 et d'ADR-042 (A16, B7, B8), d'ADR-035 (A17), d'ADR-038 (B9) ;
> précisions d'ADR-033 et d'ADR-034 (A5, B5, B6) ; B2 confirmée par
> Sébastien le 2026-10-09.

## A. Règles qui croisent plusieurs tables (objet d'ADR-040)

| # | Règle | D'où elle vient | État au 08/10/2026 |
|---|---|---|---|
| A1 | Une visite ne précède pas la signature du mandat. | `docker/init-v3/01_create_fil_rouge_immobilier.sql:721-725` ; Q-MAN-06 | ❌ pas codé ; aucun test de visite |
| A2 | Une vente porte sur un mandat signé, et pas avant sa signature. Après la fin du mandat, la vente s'enregistre et le paiement est refusé. | `01:774-784` ; ADR-050 ; ADR-024 | ❌ pas codé |
| A3 | La vente pointe la grille d'honoraires en vigueur à la date de l'acte. | ADR-030 ; `01:767-768` | ❌ pas codé |
| A4 | Les honoraires se calculent depuis cette grille (C2). | `livrables/2-modelisation/09-contraintes-a-coder.md:88-107` | ❌ pas codé : le client de l'API envoie `fees_amount` (`API/tests/integration/test_constraints_db.py:496`). Le code pur sait choisir la grille (`API/src/app/services/remuneration.py:177-183`), pas branché. |
| A5 | Une grille d'honoraires déjà citée par une vente ne se modifie pas. De même pour une tranche du barème ou une version de réglages déjà citée par un paiement. | ADR-030 ; ADR-034 (Décision 6) | ❌ pas codé : `PUT /parameters-fees/{id}`, `/commission-scales/{id}`, `/hunter-rate-parameters/{id}` l'acceptent (`API/src/app/routes/crud_router.py:95-102`) |
| A6 | Le droit au paiement (C1) : le bon chasseur (U04) ; exclusif, ou vente due au chasseur (R01, R02) ; dans les délais (R04). Un droit fermé s'écrit `'refused'` avec son motif. | `01:985-993` ; `09-contraintes-a-coder.md:56-84` ; ADR-024 | ❌ pas codé. R01, R02 et R04 existent dans le code pur (`remuneration.py:166-174`), pas branché. U04 n'existe nulle part. |
| A7 | La tranche du barème est en vigueur à la date de l'acte, et c'est le barème par défaut ou celui de ce chasseur. | `01:985-989` ; carte Q-MAN-06 (`questions-a-trancher.md:863-864`) | ❌ pas codé. Le code pur fait ce choix (`remuneration.py:230-248`), pas branché. |
| A8 | La version des réglages du taux est en vigueur à la date de l'acte. | `01:936-941` (G1) | ❌ pas codé. `ParametrageService.reglages_applicables` la choisit (`API/src/app/services/parametrage_service.py:136`), sans route. |
| A9 | Montant = taux final × honoraires, arrondi (Q-REM-11). | `questions-a-trancher.md:131`, `:658-666` ; ADR-033 | ❌ pas codé ; la formule n'existe que dans le code pur |
| A10 | Un mandat ne se renouvelle que sans vente (C7). | Q-MAN-03 ; ADR-050 | ❌ pas codé |
| A11 | Le mandat du perdant passe à `'lost'` quand la vente du collègue est saisie. | ADR-024, Conséquences | ❌ pas codé : rien n'est automatique |
| A12 | L'auteur d'un bien saisi à la main est un chasseur ou un manager. | Q-ACC-09 ; `01:624-627` ; ADR-047 | ❌ pas codé : seule la clé est vérifiée (`test_constraints_db.py:120-128`) |
| A13 | Un compte n'a qu'un profil : client, chasseur ou manager. | ADR-005 ; `documents utiles/PLAN-DE-TESTS.md:47` (StarterPack : « insérer un client_id qui est un chasseur → refus ») | ❌ pas codé. Données reprises : 25 comptes, aucun en double (18 clients, id 7 à 24 ; 6 chasseurs, id 1 à 6 ; 1 manager, id 25 ; `docker/init-v3/02_migration.sql:132-172`) |
| A14 | La note de performance (C6) : après un paiement, la nouvelle note est ≥ à la précédente ; après un mandat échu, ≤. | `09-contraintes-a-coder.md:186-221` ; ADR-042 ; ADR-048 | ❌ pas codé |
| A15 | Réaffecter une demande refusée (C8) ; offres sous le prix affiché (C9). | `09-contraintes-a-coder.md:237-256` | reportés (Q-MAN-08 ; C9 « plus tard ») |
| A16 | Une demande ne passe `'launched'` que si un mandat signé existe pour elle. | ADR-041, Conséquences | ❌ pas codé |
| A17 | La note `'payment'` du journal ne s'écrit qu'une fois le paiement payé (`'paid'`). | ADR-035, Questions tranchées | ❌ pas codé : la base accepte une note `'payment'` sur un paiement seulement annoncé (`test_constraints_db.py:712-715`) |

## B. Règles sur plusieurs lignes d'une même table, ou sur l'ancienne valeur

| # | Règle | D'où elle vient | État au 08/10/2026 |
|---|---|---|---|
| B1 | Exclusivité : un mandat exclusif bloque tout autre mandat du client sur la période. | ADR-039 | ✅ codé, par trigger (`01:522-550`) ; testé (`test_constraints_db.py:311-353`) |
| B2 | Un mandat `'completed'` ou `'lost'` libère le client tout de suite. Tranchée par déduction — confirmée par Sébastien le 2026-10-09 (Discord). | ADR-039, Décision 5 | ❌ pas codé : le trigger n'ignore que `'canceled'` (`01:526`, `:533`). À changer dans le trigger, pas dans l'API, si le groupe confirme. |
| B3 | `'renewed'` ⇒ un successeur existe. | ADR-050 | ❌ pas codé : `PUT /mandates/{id}` accepte `'renewed'` sans successeur |
| B4 | Le délai se compte depuis la première signature : remonter `id_mandate_parent`. | ADR-050 ; Q-MAN-04 | ❌ pas codé |
| B5 | Les honoraires ne changent plus (C3). ADR-033 l'étend au prix, à la date de l'acte, à la grille et à l'origine de la vente. | Q-REM-12 ; `09-contraintes-a-coder.md:110-117` ; ADR-033, Décision 5 | ❌ pas codé : `API/src/app/services/sale_service.py` n'a que le CRUD |
| B6 | Le paiement ne change plus (C5) : seuls le statut et les dates d'étape avancent. | `09-contraintes-a-coder.md:169-182` ; « Le résultat est figé à l'acte » (`REGLES-CALCUL-REMUNERATION.md:764`, StarterPack) ; ADR-033, Décision 4 | ❌ pas codé |
| B7 | L'ordre des statuts. Demande : `'confirmed'` → `'accepted'` ou `'rejected'` ; `'accepted'` → `'launched'`. Offre : `'proposed'` → `'signed'` → `'offer_pending'` → `'accepted'` ou `'rejected'`. | ADR-041, Questions tranchées | ❌ pas codé : `PUT /search-requests/{id}` accepte un saut de `'confirmed'` à `'launched'` |
| B8 | Une note du journal, une fois écrite, ne se modifie plus. | ADR-042, Conséquences | ❌ pas codé : `PUT` et `DELETE` sur `/hunter-performances/{id}` sont ouverts (`crud_router.py:95-110`) |
| B9 | L'ordre des statuts du paiement : `'announced'` → `'scheduled'` → `'paid'`. | ADR-038, Décision 3 | ❌ pas codé : `PUT /payments/{id}` est ouvert |

## C. Règles sur une seule ligne, que d'autres ADR renvoient à l'API (hors du principe d'ADR-040 ; listées pour l'état)

| # | Règle | D'où elle vient | État au 08/10/2026 |
|---|---|---|---|
| C-a | Retirer l'espace d'un Eircode avant d'écrire. | ADR-031 | ❌ pas codé : `D02 X285` rend 409 (`test_constraints_db.py:224-229`) |
| C-b | Normaliser un code postal : majuscules, espaces en bord, préfixe `L-`. | ADR-021, Conséquences ; ADR-022, Conséquences | ❌ pas codé |
| C-c | Un mandat exclusif ne finit pas `'lost'`. | ADR-024, Questions tranchées n° 3 | ❌ pas codé. 💡 ADR-024 propose un `CHECK`, à décider par le groupe. |
| C-d | L'API calcule `ends_at` (signature + 6 mois). | ADR-039 ; `01:482-484` | ❌ pas calculé. Le `CHECK chk_mandate_six_months` refuse une mauvaise valeur ✅. |
| C-e | Faire expirer un mandat fini. | `docker/init-v3/02_migration.sql:236-237` (« les faire expirer revient à l'application ») | ❌ pas codé |
| C-f | La cohérence d'une version de réglages : poids, plancher et plafond, forme des paliers. | ADR-034, Conséquences (💡 proposé) | ❌ pas codé |

## Hors API, pour mémoire : deux `CHECK` attendus

* `chk_refused` : score et détail exigés hors refus, détail vide sur un refus. ADR-033, Décision 3 — **confirmée par Sébastien le 2026-10-09 (Discord)** (elle renverse le 3e point de la carte D8). Demande une migration.
* L'ordre des dates du paiement : `announced_at::date <= scheduled_for` et `announced_at <= paid_at` (💡 forme proposée). ADR-038, Conséquences — déduit. Demande une migration.

## Sources de l'annexe

| Affirmation | Source |
|---|---|
| Règles renvoyées à l'API par le lot 1 | `md/adr/adr-024-motif-refus-remuneration.md:140-141`, `:152-154` ; `adr-030-vente-reliee-grille-honoraires.md:91-92` ; `adr-031-localisation-criteria-eircode.md:113`, `:127-129` ; `adr-039-regles-du-mandat.md:106`, `:117`, `:141` ; `adr-050-renouvellement-du-mandat.md:105`, `:108`, `:144-150` |
| Règles des lots 2 et 3 | `md/adr/adr-033-tracabilite-du-calcul.md` (Décisions 3 à 5) ; `adr-034-parametres-remuneration-table-datee.md` (Décision 6, Conséquences) ; `adr-035-note-recalculee-a-chaque-vente.md` (Questions tranchées) ; `adr-038-etapes-du-paiement-sans-facture.md` (Décision 3, Conséquences) ; `adr-041-statuts-demande-et-offre.md` (Conséquences, Questions tranchées) ; `adr-042-journal-des-notes-du-chasseur.md` (Conséquences) |
| TODO du schéma renvoyés à l'API | `docker/init-v3/01_create_fil_rouge_immobilier.sql:624-627`, `:721-725`, `:767-768`, `:774-784`, `:936-941`, `:985-993` |
| Le seul trigger | `01:522-550` |
| Les blocs C1 à C9 | `livrables/2-modelisation/09-contraintes-a-coder.md` |
| Comptes repris | `docker/init-v3/02_migration.sql:132` (manager 25), `:139-144` (chasseurs 1 à 6), `:155-172` (clients 7 à 24) |
| `PUT` et `DELETE` ouverts | `API/src/app/routes/crud_router.py:95-110` |
| Tests | `API/tests/integration/test_constraints_db.py` (lignes citées dans les tableaux) |
| ADR-021, ADR-022, ADR-005 | journal Confluence, copie du 07/10/2026 |

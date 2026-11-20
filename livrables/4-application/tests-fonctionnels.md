# 🧭 Tests fonctionnels — les user stories, et les tests qui les prouvent

> **Plan de tests, partie fonctionnelle** (BC03). Complète `rapport-tests.md` (unitaires et intégration).
> Exigé par `GRILLE-EVALUATION.md` : « Plan de tests (unitaires + fonctionnels) | Scénarios + rapports d'exécution ».
> État : dépôt `Fil-Rouge-API`, commit `8ed2591` (2026-11-19) pour la matrice ; suite complète relancée le 2026-11-20 : **1 120 passed, 7 xfailed, 0 failed**.
> Matrice établie le 2026-11-19 : noms des tests lus, et corps lus pour les cas douteux ; 24 noms vérifiés par `grep`.

---

## 1. Le test de bout en bout

`API/tests/integration/test_parcours_particulier.py` enchaîne les user stories 01 et 02, **dans l'ordre où le particulier les vit** :

| # | Étape | Route | User story |
|---|---|---|---|
| 1 | Le visiteur dépose sa demande, sans compte | `POST /search-requests/submit` | 01, @formulaire |
| 2 | Un manager prend la demande « à prendre » et lui affecte un chasseur ; le chasseur l'accepte | `PUT /search-requests/{id}` | 01, @affectation ; 04, @acceptation |
| 3 | Le manager obtient le code ; le particulier pose son mot de passe et se connecte | `POST /users/{id}/activation-code`, `POST /auth/activate`, `POST /auth/login` | 01, @creation-compte |
| 4 | Le chasseur signe le mandat, garde un bien (photo décrite) et le propose | `POST /mandates`, `/estates`, `/pictures`, `/estate-search-requests`, `/estate-proposed` | 01, @signature-mandat ; 02, @propositions |
| 5 | Avec son jeton, le particulier voit **sa seule** proposition et se dit intéressé | `GET /estate-proposed`, `PUT /estate-proposed/{id}` | 02, @bien-retenu |

- **Outils** : pytest et le `TestClient` de FastAPI (de vraies requêtes HTTP, sur la vraie application), sur la base PostgreSQL de test `fil_rouge_test`, annulée après le test. Pas de navigateur : le projet n'a pas de front.
- **Le vrai contrôle d'accès** : pour les étapes du particulier, le test retire le compte simulé des autres tests. Il se connecte avec un vrai mot de passe et un **vrai jeton JWT**.
- 🔎 **Ce test a trouvé un trou** : une demande du formulaire n'avait ni chasseur ni manager, et **aucune route ne pouvait la confier**. Corrigé le même jour (choix B de Sébastien : les managers voient les demandes « à prendre » et en prennent une ; `test_demande_a_prendre.py`, 5 tests, `f8b821e`).

## 2. La matrice : chaque scénario, et sa preuve

Statuts : ✅ couvert par un test · ✅📝 couvert par un **choix écrit** (la règle diffère du scénario, exprès, et la raison est donnée) · 🟡 en partie, limite connue · ❌ non couvert, dans le périmètre · ➖ hors périmètre.
Hors périmètre, décidé par le groupe : le front, l'envoi d'emails (donc les notifications), la facture, l'acte notarié, l'IA générative.
Les tests unitaires sont dans `tests/`, ceux d'intégration dans `tests/integration/`.

### 00 — Règles du mandat et de la rémunération

| Ligne | Scénario | Statut | Test(s) |
|---|---|---|---|
| 15 | Exclusif : rémunéré même en découverte autonome | ✅ | `test_remuneration.py::test_droit_selon_exclusivite_et_origine` · `test_constraints_db.py::test_mandate_second_mandate_during_exclusive_returns_409` |
| 23 | Non exclusif : pas de rémunération automatique | ✅ | `test_remuneration.py::test_droit_selon_exclusivite_et_origine` · `test_calcul_paiement.py::test_sale_out_of_scope_gives_a_refused_payment` |
| 30 | Non exclusif : un autre chasseur peut agir | ✅ | `test_scenarios_restants.py::test_00_30_another_hunter_can_act_under_a_non_exclusive_mandate` |
| 37 | Durée 6 mois, renouvelable | ✅ | `test_constraints_db.py::test_mandate_seven_months_returns_409` · `test_trous_audit_db.py::test_p13_renewal_at_term_is_accepted` |
| 43 | Rémunération collectée par le notaire | ✅ (collecte ➖) | `test_remuneration.py::test_honoraires_sur_le_prix_acte` |
| 51 | Barème selon montant, ancienneté, performance | ✅ | `test_remuneration.py::test_bareme_du_chasseur_prevaut_sur_le_defaut` · `test_remuneration.py::test_bareme_en_vigueur_a_la_date_de_l_acte` |
| 58 | Performance recalculée sur critères | ✅ | `test_remuneration.py::test_score_global_agrege_les_cinq_criteres` · `test_calcul_paiement.py::test_journal_note_is_written_only_when_paid` |

### 01 — Le particulier : demande et compte

| Ligne | Scénario | Statut | Test(s) |
|---|---|---|---|
| 11 | Demande via le formulaire, affectation déclenchée | ✅ (l'affectation est faite par un manager, pas automatique) | `test_demande_avant_compte.py::test_new_form_creates_inactive_account_client_and_request` · `test_demande_a_prendre.py::test_every_manager_sees_a_request_nobody_follows` |
| 18 | Notification du chasseur affecté | ➖ pas d'email (le code d'activation la remplace) | `test_activation.py::test_manager_gets_code_only_for_own_request` |
| 25 | Finalise son compte | ✅ | `test_activation.py::test_visitor_finalises_own_account` · `test_parcours_particulier.py::test_particulier_from_form_to_interest` |
| 32 | Premier point et signature du mandat | ✅ | `test_signature_vente.py::test_signing_a_mandate_launches_its_request` · `test_constraints_db.py::test_mandate_six_months_is_accepted` |

### 02 — Le particulier : propositions et visites

| Ligne | Scénario | Statut | Test(s) |
|---|---|---|---|
| 14 | Reçoit des propositions, choisit quoi visiter | ✅ | `test_propositions_visites.py::test_selected_estate_can_be_proposed` · `test_parcours_particulier.py::test_particulier_from_form_to_interest` |
| 20 | Reçoit l'avis du chasseur après visite | ✅ | `test_le_sien.py::test_client_sees_his_rows_not_the_other_clients` · `test_auteurs.py::test_only_hunters_write_reviews` |
| 26 | Aucun bien ne convient, les propositions reprennent | ✅📝 le refus s'enregistre, le bien écarté n'est plus suggéré ; le chasseur **relance** les suggestions (route à la demande), voulu : il garde la main sur ce qu'il propose | `test_constraints_db.py::test_decline_reason_with_declined_is_accepted` · `test_suggestions.py::test_dismissed_estate_is_not_written_again` |
| 32 | Un bien convient : visiter ou faire une offre | ✅ | `test_propositions_visites.py::test_client_makes_an_offer` · `test_propositions_visites.py::test_client_visit_on_a_proposed_estate_is_accepted` |

### 03 — Le particulier : offre et signature

| Ligne | Scénario | Statut | Test(s) |
|---|---|---|---|
| 14 | Fait une offre d'achat | ✅ | `test_propositions_visites.py::test_client_makes_an_offer` · `test_propositions_visites.py::test_second_offer_returns_409` |
| 19 | Offre non acceptée | ✅ | `test_scenarios_restants.py::test_06_37_seller_refuses_the_offer` · `test_scenarios_restants.py::test_03_19_after_a_refusal_the_hunter_proposes_other_estates` |
| 25 | Offre acceptée, signature organisée | ✅ (le notaire ➖) | `test_scenarios_restants.py::test_06_44_seller_accepts_the_offer` · `test_signature_vente.py::test_hunter_sale_with_an_accepted_offer_is_accepted` |
| 31 | Acte signé, honoraires payés | ✅ (collecte ➖) | `test_remuneration.py::test_honoraires_sur_le_prix_acte` · `test_signature_vente.py::test_sale_completes_its_mandate` |
| 38 | Facture et retour d'expérience | ➖ facture exclue, pas d'email | — |

### 04 — Le chasseur : prise en charge de la demande

| Ligne | Scénario | Statut | Test(s) |
|---|---|---|---|
| 11 | Reçoit une demande | ➖ notification, pas d'email | (affectation : `test_le_sien.py::test_manager_assigns_a_request_to_one_of_his_hunters_only`) |
| 17 | N'accepte pas la demande | ✅ | `test_scenarios_restants.py::test_04_17_hunter_refuses_and_the_request_is_reassigned` |
| 24 | Accepte et consulte une recherche initiale | ✅ | `test_suggestions.py::test_suggestions_are_written_as_suggested` · `test_parcours_particulier.py::test_particulier_from_form_to_interest` |
| 30 | Prend contact, fixe un rendez-vous | ➖ un agenda est un outil externe (agenda partagé, prise de rendez-vous en ligne) : pas de table de rendez-vous, décidé le 2026-11-19 | — |
| 36 | Affine les critères, fait signer le mandat | ✅ | `test_trous_audit_db.py::test_p8_next_version_on_same_request_is_accepted` · `test_signature_vente.py::test_signing_a_request_with_one_criteria_is_accepted` |

### 05 — Le chasseur : sélection quotidienne

| Ligne | Scénario | Statut | Test(s) |
|---|---|---|---|
| 14 | Reçoit une sélection quotidienne | 🟡 **limite connue** : le moteur répond à la demande ; aucun déclenchement planifié chaque matin (il faudrait un DAG Airflow qui l'appelle) | `test_suggestions.py::test_suggestions_are_written_as_suggested` · `test_suggestions.py::test_never_more_than_ten` |
| 20 | Transmet une sélection au client | ✅ | `test_constraints_db.py::test_proposing_a_kept_estate_is_accepted` · `test_constraints_db.py::test_proposing_an_estate_not_kept_returns_409` |
| 26 | Alerte quand le client a commenté | ➖ alerte = notification | (priorité : `test_propositions_visites.py::test_client_can_set_his_priority`) |
| 32 | Engage les discussions ou organise une visite | ✅📝 une visite s'enregistre **une fois faite** ; une visite future est refusée, exprès (P24, ADR-053) : la table trace les visites, pas un agenda | `test_propositions_visites.py::test_client_visit_on_a_proposed_estate_is_accepted` · `test_trous_audit_db.py::test_p24_visit_in_the_future_is_refused` |
| 38 | Requalifie si rien ne convient | ✅ | `test_trous_audit_db.py::test_p9_next_version_without_reason_is_refused` · `test_suggestions.py::test_query_comes_from_the_latest_criteria` |

### 06 — Le chasseur : avis et offre d'achat

| Ligne | Scénario | Statut | Test(s) |
|---|---|---|---|
| 11 | Note d'avis avec audio et vidéo | ✅ | `test_constraints_db.py::test_review_accepts_several_media` |
| 18 | Offre pré-remplie selon l'avis | ➖ fonction nouvelle (un montant conseillé dans l'avis, et sa règle) : reportée en **v2**, décidé le 2026-11-19 | — |
| 25 | Le client ne veut pas acquérir | ✅📝 le refus s'enregistre ; la nouvelle sélection est relancée par le chasseur, comme 02:26 | `test_constraints_db.py::test_decline_reason_with_declined_is_accepted` |
| 31 | Transmet l'offre, statut en attente | ✅ | `test_propositions_visites.py::test_client_makes_an_offer` |
| 37 | Offre refusée par le vendeur | ✅ (trou réparé le 2026-11-19 : une nouvelle offre était refusée) | `test_scenarios_restants.py::test_06_37_seller_refuses_the_offer` · `test_scenarios_restants.py::test_06_37_a_new_offer_can_follow_a_refusal` |
| 44 | Offre acceptée par le vendeur | ✅ (le notaire ➖) | `test_scenarios_restants.py::test_06_44_seller_accepts_the_offer` |

### 07 — Le chasseur : rémunération et performance

| Ligne | Scénario | Statut | Test(s) |
|---|---|---|---|
| 11 | Prévenu du paiement proche | ➖ notification | (montant : `test_calcul_paiement.py::test_payment_amount_is_the_calculation_on_the_same_numbers`) |
| 18 | Envoie sa facture | ➖ facture exclue | — |
| 24 | Paiement programmé | ✅ (facture ➖) | `test_versions_paiement.py::test_payment_moves_forward_step_by_step` |
| 30 | Marqué payé, indicateurs recalculés | ✅ | `test_calcul_paiement.py::test_journal_note_is_written_only_when_paid` · `test_versions_paiement.py::test_paid_payment_is_frozen` |
| 37 | Mandat échu : renouveler, score à la baisse | 🟡 **limite connue** : renouvellement et baisse au calcul suivant ; aucune note `mandate_expired` n'est écrite à l'échéance (il faudrait une tâche planifiée) | `test_calcul_paiement.py::test_a_lost_mandate_is_an_issue_without_sale` · `test_trous_audit_db.py::test_p13_renewal_at_term_is_accepted` |

### 08 et 09 — Le futur, avec l'IA

- **08** (4 scénarios) : ➖ tous. Faisabilité, descriptions et articles rédigés par une IA générative, front.
- **09** (9 scénarios) : ➖ tous. Deux ont déjà une part faite, sans IA :
  - 09:35, sélection ordonnée par pertinence : l'ordre est prouvé (`test_suggestion_query.py::test_wanted_features_raise_the_score`) ; le dédoublonnage est de l'IA future.
  - 09:43, écarter les biens ressemblants : le bien écarté lui-même est exclu (`test_suggestions.py::test_dismissed_estate_is_not_written_again`) ; les biens « ressemblants » sont de l'IA future.

### 10 — Le calcul de la rémunération (26 scénarios)

- ✅ **22** : droit, échéance, assiette, cinq critères, score de 73,5, barème, ancienneté, performance, taux final de 46,16 %, plafond et plancher, arrondi, barème figé. Tous dans `test_remuneration.py`, et dans `test_calcul_paiement.py` pour la vente en base.
- ✅ **10:277** : le montant annoncé est figé jusqu'au paiement (`test_scenarios_restants.py::test_10_277_announced_amount_cannot_change_before_payment`). Trou réparé le 2026-11-19 : il pouvait changer.
- ✅📝 **3** :
  - 10:140 et 10:255 : la formule « mandats × 10 » du sujet est remplacée par le taux de transformation (ADR-048). Les cas du sujet restent, en `xfail(strict=True)`.
  - 10:289 : le calcul ne relit pas la note du journal ; il **recompte tout en base à chaque vente** (ADR-035, « note recalculée à chaque vente »). Le journal trace, le calcul recompte.

## 3. Le bilan

| | ✅ testé | ✅📝 choix écrit | 🟡 limite connue | ❌ | ➖ | Total |
|---|---|---|---|---|---|---|
| **Scénarios** | **51** | **6** | **2** | **0** | **21** | **80** |

- Dans le périmètre (➖ retirés), **59** scénarios : **57** couverts, par un test (51) ou par un choix écrit (6), soit **97 %**.
- **Plus aucun trou** (❌) : les 3 scénarios sans test l'ont eu le 2026-11-19, et deux ont été écartés par écrit (rendez-vous, offre pré-remplie).
- **Les tests ont trouvé 3 vrais trous**, réparés le même jour :
  1. une demande du formulaire ne pouvait être confiée à personne (`f8b821e`) ;
  2. après un refus du vendeur, le client ne pouvait pas refaire d'offre (`8ed2591`) ;
  3. le montant annoncé au chasseur pouvait changer avant le paiement (`8ed2591`).
- **Les 2 limites connues** (05:14, 07:37) demandent une tâche planifiée (Airflow) : écrites ici, codées s'il reste du temps.

## 4. Rejouer

Depuis `Fil-Rouge-API/docker/` :

```bash
docker compose exec -T api python -m pytest -v -p no:cacheprovider tests/integration/test_parcours_particulier.py tests/integration/test_demande_a_prendre.py tests/integration/test_scenarios_restants.py
```

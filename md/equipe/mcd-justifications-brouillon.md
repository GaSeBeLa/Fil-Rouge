# MCD : les justifications des choix débattus (brouillon)

> **Brouillon du Glaude, 2026-11-23**, demandé par Sébastien (« fait le 2 », Discord).
> Le Glaude ne touche ni aux schémas ni à `livrables/2-modelisation/mcd.md` (règle de Gabriel, 2026-11-20 : travail humain).
> ➡️ **Un humain relit ce texte, le corrige, puis le reporte sous le schéma.**
> Livrable visé (grille) : « MCD complet (cible) — 1 schéma + justifications des choix débattus ».
> Schémas : `livrables/2-modelisation/annexes/MCD v15.drawio.png`, `MLD v17.drawio.png`, `MPD v15.drawio.png`.
> Chaque source a été relue le 2026-11-23. `init-v3/01` = `Fil-Rouge-API/docker/init-v3/01_create_fil_rouge_immobilier.sql`.

---

## 1. Un compte, et une seule fiche par rôle

- **Choix** : `User` porte le compte (connexion). `Client`, `Hunter` et `RealEstateManager` sont des fiches à part, liées au compte (`User` 0,1 — fiche 1,1).
- **Pourquoi** : l'audit a trouvé un chasseur enregistré comme client sur un mandat (risque **R02**, `livrables/1-audit/1.2-registre-anomalies-risques.md`). La cause : client et chasseur visaient la même table, sans contrôle du rôle (R06).
- **Garde-fou** : un compte n'a qu'une seule fiche. Trois triggers l'imposent (`trg_client_one_profile`, `trg_hunter_one_profile`, `trg_real_estate_manager_one_profile`, `init-v3/01:376-383`).
- **Sources** : ADR-005, ADR-057.

## 2. Des critères versionnés

- **Choix** : `Criteria` pointe vers sa version précédente (association réflexive « Follows », colonne `id_previous_version`).
- **Pourquoi** : le chasseur requalifie la recherche avec le client. L'ancienne version reste, avec le motif du changement (`change_reason`). On sait ce qui a été demandé, et quand.
- **Garde-fou** : une version n'a qu'une suivante (`uq_criteria_one_successor`), et reste dans la même demande (`fk_criteria_previous_same_request`).
- **Source** : ADR-013 (relation réflexive sur `Criteria` et `Mandate`).

## 3. Un mandat qui en renouvelle un autre

- **Choix** : `Mandate` pointe vers le mandat qu'il renouvelle (association réflexive « Renews », colonne `id_mandate_parent`).
- **Pourquoi** : un mandat dure 6 mois, renouvelable. Le nombre de renouvellements se lit en remontant la chaîne, sans compteur à tenir à jour.
- **Garde-fou** : une chaîne sans branche (`id_mandate_parent` `UNIQUE`), pas son propre parent (`chk_mandate_not_own_parent`), et le même client (`fk_mandate_parent_same_client`).
- **Sources** : ADR-010, ADR-013, ADR-050.

## 4. La date de fin du mandat est stockée

- **Choix** : `mandate.ends_at` est une colonne, pas un calcul.
- **Pourquoi** : la fin se lit et se filtre directement. Un `CHECK` impose `ends_at = signature_date + 6 mois` (`init-v3/01:615-617`) : la colonne ne peut pas mentir.
- **Source** : ADR-023 (remplace ADR-004).

## 5. Deux liens entre bien et demande, deux rôles différents

- **Estate_SearchRequest** : le bien **trouvé** par le chasseur pour une demande, avec son avis (`review_hunter`) et son tri (`suggested`, `kept`, `dismissed`). Un bien n'y entre qu'une fois par demande (`uq_estate_search`).
- **EstateProposed** : le bien **proposé** au client sous mandat, avec la réponse du client et l'offre.
- **Pourquoi deux** : tous les biens trouvés ne sont pas proposés. Les mélanger aurait perdu le tri fait par le chasseur.
- **Source** : `init-v3/01:869` et `:901` (commentaires des deux tables) ; ADR-041 (statuts de la demande et de l'offre).

## 6. Une vente au plus par mandat, et par bien

- **Choix** : `Sale` 0,1 côté `Mandate` et côté `Estate`.
- **Pourquoi** : un bien ne se vend qu'une fois ; une revente serait une nouvelle annonce, donc un autre bien. Un mandat aboutit à une vente au plus.
- **Garde-fou** : `sale.id_mandate` `UNIQUE`, et `uq_sale_estate` (`init-v3/01:1017-1021`).
- **Source** : ADR-053, point P37 (Gabriel, Discord, 12/10/2026).

## 7. Le paiement garde les termes de son calcul

- **Choix** : `Payment` pointe vers la tranche du barème (`CommissionScale`) et la version des réglages (`HunterRateParameters`) qui ont servi. `Sale` pointe vers la grille d'honoraires (`ParametersFees`).
- **Pourquoi** : un barème qui change demain ne réécrit pas un paiement d'hier. Le calcul se rejoue à l'identique.
- **Source** : ADR-033 (« un paiement garde tous les termes de son calcul, figés à la date de l'acte »), décision G1 du 08/10/2026.

## 8. Un barème commun, ou propre à un chasseur

- **Choix** : `commission_scale.id_hunter` est facultatif.
- **Pourquoi** : vide, la tranche vaut pour tous les chasseurs ; remplie, elle ne vaut que pour lui (`init-v3/01:1045`).

## 9. Le contact du vendeur, à part du bien

- **Choix** : `EstateContact`, 0 ou 1 par bien, séparé de `Estate`.
- **Pourquoi** : ce sont des données personnelles d'un tiers, le vendeur. À part, le contact se cache, s'efface ou s'anonymise sans toucher au bien. Seuls Admin, Hunter et Manager le voient : ni le client, ni le rôle Reader, ni le compte d'analyse `fil_rouge_reader`.
- **Source** : ADR-054.

## 10. L'historique des prix

- **Choix** : `EstatePriceHistory`, une ligne par prix vu.
- **Pourquoi** : quand l'import voit un prix revu, l'ancien n'est pas écrasé : il se garde, avec sa date.
- **Source** : ADR-064.

## 11. Les montants en euros

- **Choix** : prix, budgets et barème en euros entiers (`INTEGER`) ; honoraires et paiements en `NUMERIC(12,2)`.
- **Pourquoi** : le groupe avait d'abord choisi les milliers d'euros (11/09), écartés le 21/09 : arrondis, ils faussent le barème (199 999 € devenait 200,0 K€ et passait à 35 % au lieu de 30 %). Le sujet arrondit le paiement au centime.
- **Source** : ADR-032.

---

## 🟡 Reste à trancher par l'équipe

- **Les auteurs** (`criteria`, `estate`, `estate_contact` vers `User`) : tous les montrer sur le MCD, ou aucun et l'écrire ici en une phrase.

# MCD — ce qu'il reste à mettre à jour (TODO)

> ✅ **§ 2 réglé le 2026-11-23** par Sébastien, à la main : **MCD v15, MLD v17, MPD v15** (dossier `vrac/`, hors dépôt). Les trois collent à la base en marche (22 tables, 43 clés étrangères), relus par script et à l'œil sur l'image. La liste détaillée de ces retouches est dans `vrac/retouches-v12.md`, hors dépôt.
> ✅ **§ 3 et § 4 réglés le 2026-11-23** : images copiées par Sébastien dans `livrables/2-modelisation/annexes/`, justifications écrites par le Glaude (accord de Sébastien) dans `livrables/2-modelisation/mcd.md`, à relire par l'équipe. Les numéros d'ADR et deux raisons de la liste du § 3 ci-dessous étaient faux : la version juste est dans `mcd.md`.

> Liste de travail du 2026-11-19, rédigée par le Glaude à la demande de Sébastien. **Le Glaude ne touche pas au schéma** : la mise en page se fait à la main, dans draw.io.
> MCD comparé : `MCD - 3 11 5.drawio.xml` (03/11/2026, dossier `vrac/` hors dépôt), lu par script : ses entités, ses associations, et les cardinalités posées sur chaque lien.
> Référence : le schéma v3 réellement monté (`Fil-Rouge-API/docker/init-v3/01_create_fil_rouge_immobilier.sql`), **43 clés étrangères**, lues dans la base le 2026-11-19 (une clé `NOT NULL` donne 1,1 du côté de la table qui la porte, une clé nullable 0,1 ; une clé `UNIQUE` donne 0,1 de l'autre côté, sinon 0,n).
> ⚠️ La lecture du draw.io par script est **approximative** : une cardinalité posée loin de son lien peut être mal rattachée. Chaque ligne se vérifie à l'œil avant d'être changée.
> Livrable visé (grille, l. 22) : « MCD complet (cible) — 1 schéma + justifications des choix débattus ».

---

## 1. Les entités

- ✅ Les **22 entités** du schéma v3 sont toutes dans le MCD : rien à ajouter, rien à retirer.

## 2. Ce qu'il faut changer (comparaison du 2026-11-19, 15 h 40)

> Refaite sur les **fichiers de Confluence** envoyés par Gabriel (`MCD - Cible`, `MLD CIBLE`, « Diagramme sans nom » = MPD), plus récents que celui de `vrac/`. Comparés au fichier `docker/init-v3/01_create_fil_rouge_immobilier.sql` (la base de dev n'a pas les migrations 50 et 51 : elle ne sert pas de référence).

### 2.1 MCD

Déjà corrigés depuis le 03/11 : ✅ SearchRequest — Hunter et — RealEstateManager en 0,1 · ✅ Payment — Hunter (« is for ») · ✅ le 1,1 en trop d'EstateContact · ✅ Hunter — Role nommé.

- ⬜ **Estate — Sale** (« is sold through ») : le lien a **disparu** ; à remettre (Sale **1,1**, Estate **0,1**).
- ⬜ **User — Client**, **— Hunter**, **— RealEstateManager** : nommer ; fiche **1,1**, User **0,1**.
- ⬜ **Estate_SearchRequest — Estate**, **— SearchRequest**, **— Hunter** : nommer ; Estate_SearchRequest **1,1**, les autres **0,n**.
- ⬜ **ReviewMedia — Estate_SearchRequest** : ReviewMedia **1,1**, Estate_SearchRequest **0,n**.
- ⬜ **EstatePriceHistory — Estate** : EstatePriceHistory **1,1**, Estate **0,n**.
- ⬜ **Payment — HunterRateParameters** : Payment **0,1**, HunterRateParameters **0,n**.
- ⬜ **Sale — ParametersFees** : le nom manque (« is based on ») ; Sale **1,1**, ParametersFees **0,n**.
- ⬜ **Client — Role** : vérifier que le lien existe (le script voit les « Has role » accrochés à RealEstateManager).
- ⬜ **EstateContact — User** : une seule cardinalité posée ; EstateContact **0,1**, User **0,n**.
- 🟡 **Les auteurs** (`criteria`, `estate`, `estate_contact` vers User) : tous les montrer, ou aucun et l'écrire dans les justifications.

### 2.2 MLD — 16 tables justes sur 22

- ⬜ `estate` : ajouter `energy_kwh_m2`, `energy_co2_m2`.
- ⬜ `picture` : ajouter `alt_text` (migration 53).
- ⬜ `payment` : ajouter `id_hunter_rate_parameters`.
- ⬜ `sale` : ajouter `id_parameters_fees`.
- ⬜ `review_media` : ajouter `id_estate_searchrequest`.

### 2.3 MPD — 17 tables justes sur 22

- ⬜ `estate` : ajouter `energy_kwh_m2`, `energy_co2_m2`.
- ⬜ `picture` : ajouter `alt_text`.
- ⬜ `hunter_performance` : ajouter `id_hunter`.
- ⬜ `estate_proposed` : ajouter `client_decided_at`, `decline_reason` (migration 51).

## 3. Les justifications à écrire sous le schéma

Une phrase par choix débattu, avec sa source. C'est la moitié du livrable (« justifications des choix débattus »).

- ⬜ **Un compte, et une fiche par rôle** (User + Client, Hunter, RealEstateManager) : l'audit a trouvé un chasseur enregistré comme client (R02) ; une fiche par rôle, et un trigger qui interdit deux fiches au même compte (ADR-005, chantier PRF).
- ⬜ **Des critères versionnés** (Criteria — Criteria, « Follows ») : le chasseur requalifie la recherche sans perdre l'historique (ADR-013, relation réflexive).
- ⬜ **Un mandat qui en renouvelle un autre** (Mandate — Mandate, « Renews ») : la durée de 6 mois est renouvelable ; le nombre de renouvellements se lit dans la chaîne (ADR-010, ADR-013, ADR-050).
- ⬜ **La date de fin stockée** (`mandate.ends_at`), contrôlée à signature + 6 mois (ADR-023).
- ⬜ **Deux liens bien ↔ demande, deux rôles** : Estate_SearchRequest = le bien trouvé pour la demande, avec l'avis du chasseur ; EstateProposed = le bien proposé au client sous mandat, avec son offre.
- ⬜ **Une vente au plus par mandat, et par bien** (Sale 0,1 des deux côtés) : un bien ne se vend qu'une fois (P37 de l'audit).
- ⬜ **Le paiement figé** (Payment — HunterRateParameters, CommissionScale) : le paiement garde les paramètres en vigueur le jour du calcul, pour qu'un changement de barème ne réécrive pas le passé.
- ⬜ **Un barème propre au chasseur, ou commun** (`commission_scale.id_hunter` nullable) : vide = le barème de tous.
- ⬜ **Le contact du vendeur à part** (EstateContact, ADR-054) : une donnée personnelle, séparée du bien, qui n'entre ni dans l'index ni dans l'OLAP.
- ⬜ **L'historique des prix** (EstatePriceHistory, chantier FLX) : une baisse de prix se garde, au lieu d'écraser l'ancien.
- ⬜ **Les montants en euros** (ADR-032) : entiers pour les prix, `NUMERIC(12,2)` pour les honoraires et les paiements.

---

## 4. Ensuite

1. ✅ Corriger le draw.io (§ 2), à la main (fait le 2026-11-23).
2. ✅ Exporter le PNG des trois schémas et les mettre dans le dépôt (Confluence n'est plus mis à jour depuis le 2026-11-20).
3. ✅ Écrire les justifications (§ 3) sous le schéma (`livrables/2-modelisation/mcd.md`, 2026-11-23).
4. ✅ Refaire la comparaison par script, pour vérifier qu'il ne reste rien (fait le 2026-11-23).

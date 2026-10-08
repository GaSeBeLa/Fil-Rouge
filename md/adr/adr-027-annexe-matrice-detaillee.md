# ADR-027 — annexe : la matrice détaillée, état au 08/10/2026

> 📋 **Annexe d'un brouillon, pas un document publié.** Elle détaille la
> Décision d'ADR-027 réécrit (`md/adr/adr-027-matrice-acces-par-role.md`),
> case par case. Rien ne s'écrit sur Confluence depuis ce fichier.
>
> ➡️ **Sa place finale** est `md/securite/matrice-droits-crud-par-role.md`,
> datée du 02/10 et périmée : la remplacer par ce contenu est une tâche pour
> l'équipe. Ce fichier vit dans `md/adr/` en attendant.
>
> 💡 **Rédigé le 2026-10-08 par Claude**, d'après les fichiers du dépôt et le
> sujet. Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre.

---

## Comment lire

✅ établi · 🟡 à décider · 💡 proposé

* **C** créer · **R** lire · **U** modifier. « Le sien » = sa propre ligne : le second contrôle (ADR-027, point 2).
* **Aucune case D** (supprimer) : ADR-027, point 4.
* ✅ = une réponse du groupe, une étape du sujet, ou une déduction dite « déduit ».
* 💡 = proposition de l'équipe, adoptée avec la fiche (ADR-027, point 10).
* « — » = aucun droit.
* ✅ veut dire « établi », pas « codé » : aucun contrôle de droit n'est codé (ADR-027, Conséquences).

Abréviations : `01` = `docker/init-v3/01_create_fil_rouge_immobilier.sql` ; `reg` = `md/questions/questions-a-trancher.md` ; P1 à P9 et H1 à H13 = les étapes des parcours du particulier et du chasseur (`Readme.md:96-104`, `:123-135`, StarterPack) ; F01, F10 = `user-stories/01_…`, `10_….feature` (StarterPack).

## Règles valables pour toutes les tables

* **`Reader`** 💡 : **R** sur toutes les tables par l'API, sauf trois choses. Le mot de passe, que l'API ne renvoie jamais (`API/src/app/models/user_model.py:35-46`). Les paiements (ADR-027, point 8). Les données personnelles d'un compte désactivé. Il n'écrit rien ✅ (`docker/init-v3/README.md:134`).
* **Compte désactivé** 💡 : ses données personnelles (`"user"`, `client`, `hunter`, `real_estate_manager`) ne sont plus lues que par l'`Admin` (ADR-049).
* **Écrits sans rôle humain** :
  * `hunter_performance` : le système, sur trois déclencheurs ✅ (`01:1007-1008`) ;
  * `estate` et `picture` importés : un script SQL lancé par l'admin, sans auteur ✅ (`01:624-629` ; ADR-047) ;
  * `payment` : créé par le calcul, jamais saisi à la main 💡 (RCR:760 ; ADR-027, point 10).
* **L'équipe d'un manager** : ses chasseurs (`hunter.id_realestatemanager`, `01:296-297`) et les demandes qui lui sont confiées (`search_request.id_realestatemanager`, `01:317-318`).

## 1. Les comptes

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `role` | — 💡 | — 💡 | — 💡 | **R** 💡 |
| `user` | **C** son compte ✅ Q-ACC-12 · **R U** le sien, sauf rôle et activation ✅ déduit | **R U** le sien, sauf rôle et activation ✅ déduit | **R U** le sien, sauf rôle et activation ✅ déduit | **C R U** 💡 · désactiver ✅ Q-ACC-08 |
| `client` | **C R U** le sien ✅ Q-ACC-12 | **R** ses clients ✅ H3 | — 💡 | **R U** 💡 · rendre anonyme ✅ Q-ACC-08 |
| `hunter` | **R** son chasseur ✅ P2 | **R** le sien · **U** ses coordonnées ✅ déduit | **R** ses chasseurs ✅ Q-ACC-02 | **C R U** 💡 · rendre anonyme ✅ déduit de Q-ACC-08 (ADR-049) |
| `real_estate_manager` | — 💡 | **R** son manager 💡 | **R** le sien · **U** ses coordonnées ✅ déduit | **C R U** 💡 · rendre anonyme ✅ déduit de Q-ACC-08 (ADR-049) |

« ✅ déduit » sur son propre compte : chacun consulte et corrige ses données (`REGISTRE-RGPD.md:38`) ; le rôle et l'activation, seul l'`Admin` les change (Q-ACC-08 ; moindre privilège, `docker/init-v3/README.md:138`). Tranchée par déduction — à confirmer par le groupe.

## 2. La demande et le mandat

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `search_request` | **C** ✅ P1 · **R** la sienne ✅ F01:29 | **C** pour un client qui a déjà un compte ✅ Q-ACC-15 · **R U** les siennes (accepter, refuser) ✅ H1, H2 | **R** celles de son équipe 💡 · **U** affecter un chasseur ✅ Q-ACC-10 | **R** 💡 |
| `criteria` | **C** ✅ P1 · **R** les siens ✅ déduit de F01:29 | **C** une nouvelle version ✅ H4 · **R** les siens ✅ H4 | **R** ceux de son équipe 💡 | **R** 💡 |
| `mandate` | **R** le sien ✅ déduit de P3 · **U** signer ✅ P3 | **C** ✅ H4 · **R U** les siens 💡 | **R** ceux de son équipe 💡 | **R U** 💡 |

F01:29 : « je peux accéder à l'espace acquéreur pour suivre ma recherche ».

## 3. Les biens, la sélection, les visites

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `estate`, `picture` | **R** les biens proposés pour lui ✅ Q-ACC-05 | **C** à la main ✅ Q8 · **R** ✅ H2, H5 | **C** à la main ✅ Q8 · **R** 💡 | **R U** 💡 |
| `estate_searchrequest`, `review_media` | **R** l'avis sur sa demande ✅ P5 | **C R U** les siens ✅ H7 | — 💡 | **R** 💡 |
| `estate_proposed` | **R** les siens · **U** commenter, prioriser, faire une offre ✅ H6, H8 | **C R U** les siens ✅ H5, H9 | — 💡 | **R** 💡 |
| `visit` | **R** les siennes 💡 | **C R** les siennes ✅ Q-ACC-13, à confirmer par Jeff (Q-JEF-25) | **R** celles de son équipe 💡 | **R U** 💡 |

Le manager ne lit ni la sélection ni les avis : minimisation (`REGISTRE-RGPD.md:9`). Il lit les visites : contre-pouvoir au conflit d'intérêts du chasseur (ADR-027, Conséquences).

## 4. L'argent et la note

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `sale` | **R** la sienne ✅ P8, P9 | **R** les siennes 💡 | **C** ✅ Q-ACC-03 · **R** celles de son équipe 💡 | **R** 💡 |
| `parameters_fees` | — 💡 | **R** ✅ déduit de F10:11 | **R** 💡 | **C R U** ✅ Q-ACC-07 |
| `commission_scale` | — 💡 | **R** le barème par défaut et le sien ✅ Q-ACC-06, à confirmer par Jeff (Q-JEF-25) | **R** ceux de ses chasseurs 💡 | **C R U** ✅ Q-ACC-07 |
| `hunter_rate_parameters` | — 💡 | **R** ✅ déduit de F10:11 | **R** 💡 | **C R U** 💡 par analogie avec Q-ACC-07 (comme ADR-034) |
| `payment` | — 💡 | **R** les siens ✅ H10 | **R** ceux de ses chasseurs ✅ Q-ACC-02 | **R** ✅ `REGISTRE-RGPD.md:29` · lancer le calcul, puis **U** programmé, payé 💡 |
| `hunter_performance` | — 💡 | **R** la sienne ✅ H12 | **R** celle de ses chasseurs 💡 | **R** 💡 |

Le paiement se lit par le chasseur, son manager et la direction : ENF-03 (RCR:763) et le modèle de registre (`REGISTRE-RGPD.md:29`), réunis (ADR-027, point 8). `Reader` ne le lit pas.

## Sources

| Affirmation | Source |
|---|---|
| Les principes de cette matrice | `md/adr/adr-027-matrice-acces-par-role.md`, Décision |
| Réponses du groupe (Q-ACC-02 à 15, Q8) | `md/questions/questions-a-trancher.md:241-252` |
| Q-ACC-08, Q-ACC-09 | même fichier, l. 183, l. 184 |
| Parcours du particulier et du chasseur | `Readme.md:96-104`, `:123-135` (StarterPack) |
| Suivre sa recherche | `user-stories/01_particulier_demande_et_compte.feature:29` (StarterPack) |
| « vérifier son montant » | `user-stories/10_calcul_remuneration_chasseur.feature:11` (StarterPack) |
| Minimisation ; qui accède aux paiements ; droits des personnes | `documents utiles/REGISTRE-RGPD.md:9`, `:29`, `:38` (StarterPack) |
| ENF-03 | `documents utiles/REGLES-CALCUL-REMUNERATION.md:763` (StarterPack) |
| Le calcul est inséré dans `paiements` par une couche au-dessus | même fichier, l. 760 |
| `Reader` ; moindre privilège | `docker/init-v3/README.md:134`, `:138` |
| Mot de passe jamais renvoyé | `API/src/app/models/user_model.py:35-46` |
| Équipe du manager | `docker/init-v3/01_create_fil_rouge_immobilier.sql:296-297`, `:317-318` |
| Biens importés sans auteur ; journal des notes | même fichier, l. 624-629, l. 1007-1008 |
| Réglages du taux : analogie | `md/adr/adr-034-parametres-remuneration-table-datee.md:33-37` |
| Import lancé par l'admin | `md/adr/adr-047-biens-import-et-saisie-a-la-main.md`, Décision |
| Comptes désactivés | `md/adr/adr-049-effacement-compte-desactiver-anonymiser.md` |

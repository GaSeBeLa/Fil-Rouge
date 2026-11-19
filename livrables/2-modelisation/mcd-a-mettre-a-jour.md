# MCD — ce qu'il reste à mettre à jour (TODO)

> Liste de travail du 2026-11-19, rédigée par le Glaude à la demande de Sébastien. **Le Glaude ne touche pas au schéma** : la mise en page se fait à la main, dans draw.io.
> MCD comparé : `MCD - 3 11 5.drawio.xml` (03/11/2026, dossier `vrac/` hors dépôt), lu par script : ses entités, ses associations, et les cardinalités posées sur chaque lien.
> Référence : le schéma v3 réellement monté (`Fil-Rouge-API/docker/init-v3/01_create_fil_rouge_immobilier.sql`), **43 clés étrangères**, lues dans la base le 2026-11-19 (une clé `NOT NULL` donne 1,1 du côté de la table qui la porte, une clé nullable 0,1 ; une clé `UNIQUE` donne 0,1 de l'autre côté, sinon 0,n).
> ⚠️ La lecture du draw.io par script est **approximative** : une cardinalité posée loin de son lien peut être mal rattachée. Chaque ligne se vérifie à l'œil avant d'être changée.
> Livrable visé (grille, l. 22) : « MCD complet (cible) — 1 schéma + justifications des choix débattus ».

---

## 1. Les entités

- ✅ Les **22 entités** du schéma v3 sont toutes dans le MCD : rien à ajouter, rien à retirer.

## 2. Les liens à corriger ou à compléter

Cases : ⬜ à faire · ✅ fait. Côté gauche = la table qui porte la clé.

### 2.1 Cardinalités à vérifier (le schéma dit « peut être vide »)

- ⬜ **SearchRequest — Hunter** (« Handled_by ») : du côté SearchRequest, **0,1** (pas 1,1). Une demande déposée par le formulaire n'a pas encore de chasseur (`search_request.id_hunter` nullable).
- ⬜ **SearchRequest — RealEstateManager** (« Manages ») : du côté SearchRequest, **0,1**. Une demande « à prendre » n'a pas encore de manager (`id_realestatemanager` nullable, choix B du 19/11).
- ⬜ **Estate — EstateContact** : une cardinalité **1,1 en trop** est accrochée au lien ; il doit rester EstateContact **1,1**, Estate **0,1**.
- ⬜ **Role — Client, Hunter, RealEstateManager** (« Has role ») : le script voit les trois « Has role » accrochés à RealEstateManager. Vérifier qu'il y a **un lien par fiche** : chaque fiche **1,1**, Role **0,n**. Le lien Client — Role semble manquer.

### 2.2 Associations sans nom ni cardinalités (le lien existe, il est nu)

- ⬜ **User — Client**, **User — Hunter**, **User — RealEstateManager** : nommer (ex. « est le compte de ») ; fiche **1,1**, User **0,1** (une seule fiche par compte, 3 triggers).
- ⬜ **Estate_SearchRequest — Estate**, **— SearchRequest**, **— Hunter** : nommer (les étiquettes « Targets », « Belongs to », « Select » semblent posées sans lien) ; Estate_SearchRequest **1,1** à chaque fois, les autres **0,n**.
- ⬜ **ReviewMedia — Estate_SearchRequest** (« Accompanies » ?) : ReviewMedia **1,1**, Estate_SearchRequest **0,n**.
- ⬜ **EstatePriceHistory — Estate** : nommer ; EstatePriceHistory **1,1**, Estate **0,n**.
- ⬜ **Payment — HunterRateParameters** : nommer (« is based on » ?) ; Payment **0,1**, HunterRateParameters **0,n**.
- ⬜ **Sale — ParametersFees** : cardinalités présentes, **nom absent** (« is based on » ?) ; Sale **1,1**, ParametersFees **0,n**.

### 2.3 Liens absents du MCD

- ⬜ **Payment — Hunter** (`payment.id_hunter`, obligatoire) : Payment **1,1**, Hunter **0,n**. C'est le chasseur payé.
- 🟡 **Les auteurs** : `criteria.id_author`, `estate.id_author`, `estate_contact.id_author` vers User. Le MCD n'en montre qu'un (SearchRequest — User, « Creates »), et EstateContact — User sans nom. **À trancher** : tous les montrer (Criteria **1,1**, Estate **0,1**, EstateContact **0,1** ; User **0,n**), ou n'en montrer aucun et l'écrire dans les justifications (« les auteurs sont de la traçabilité, pas du métier »).

### 2.4 Déjà justes (rien à faire)

Client — Mandate (« Signs ») · Hunter — Mandate (« Creates ») · SearchRequest — Mandate (« Formalises ») · SearchRequest — Client (« Owns ») · SearchRequest — User (« Creates ») · Criteria — SearchRequest (« Contains ») · Criteria — Criteria (« Follows ») · Mandate — Mandate (« Renews ») · EstateProposed — Estate, — Hunter, — Mandate · Visit — Estate, — Mandate · Sale — Estate, — Mandate · Payment — Sale · Picture — Estate · RealEstateManager — Hunter · Hunter — CommissionScale · CommissionScale — Payment · Hunter — HunterPerformance · HunterPerformance — Payment, — Mandate.

---

## 3. Les justifications à écrire sous le schéma

Une phrase par choix débattu, avec sa source. C'est la moitié du livrable (« justifications des choix débattus »).

- ⬜ **Un compte, et une fiche par rôle** (User + Client, Hunter, RealEstateManager) : l'audit a trouvé un chasseur enregistré comme client (R02) ; une fiche par rôle, et un trigger qui interdit deux fiches au même compte (ADR-005, chantier PRF).
- ⬜ **Des critères versionnés** (Criteria — Criteria, « Follows ») : le chasseur requalifie la recherche sans perdre l'historique (ADR-014).
- ⬜ **Un mandat qui en renouvelle un autre** (Mandate — Mandate, « Renews ») : la durée de 6 mois est renouvelable ; le nombre de renouvellements se lit dans la chaîne (ADR-011).
- ⬜ **La date de fin stockée** (`mandate.ends_at`), contrôlée à signature + 6 mois (ADR-018).
- ⬜ **Deux liens bien ↔ demande, deux rôles** : Estate_SearchRequest = le bien trouvé pour la demande, avec l'avis du chasseur ; EstateProposed = le bien proposé au client sous mandat, avec son offre.
- ⬜ **Une vente au plus par mandat, et par bien** (Sale 0,1 des deux côtés) : un bien ne se vend qu'une fois (P37 de l'audit).
- ⬜ **Le paiement figé** (Payment — HunterRateParameters, CommissionScale) : le paiement garde les paramètres en vigueur le jour du calcul, pour qu'un changement de barème ne réécrive pas le passé.
- ⬜ **Un barème propre au chasseur, ou commun** (`commission_scale.id_hunter` nullable) : vide = le barème de tous.
- ⬜ **Le contact du vendeur à part** (EstateContact, ADR-054) : une donnée personnelle, séparée du bien, qui n'entre ni dans l'index ni dans l'OLAP.
- ⬜ **L'historique des prix** (EstatePriceHistory, chantier FLX) : une baisse de prix se garde, au lieu d'écraser l'ancien.
- ⬜ **Les montants en euros** (ADR-032) : entiers pour les prix, `NUMERIC(12,2)` pour les honoraires et les paiements.

---

## 4. Ensuite

1. ⬜ Corriger le draw.io (§ 2), à la main.
2. ⬜ Exporter le PNG, et le remplacer sur la page Confluence « Schémas - MCD/MLD/MPD Cible ».
3. ⬜ Écrire les justifications (§ 3) sous le schéma, sur la même page.
4. ⬜ Refaire la comparaison par script, pour vérifier qu'il ne reste rien.

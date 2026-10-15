### ADR-058 : Le chasseur IA a moins de droits qu'un chasseur humain

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 15/10/2026
* **Statut :** 💡 proposé (Sébastien, Discord, 15/10/2026). **Rien n'est codé** tant qu'il n'est pas accepté. Accepté, il remplace le point 6 d'ADR-045 (« droits des chasseurs-IA : reportés au parcours IA »).
* **Décideurs :** Sébastien (« une IA n'aurait pas les mêmes droits, ça peut être dangereux », Discord, 15/10/2026).
* **Voir aussi :** ADR-045, point 6 ; ADR-057 (une fiche, un rôle) ; ADR-029 (un chasseur IA a un manager) ; ADR-054 (contact du vendeur) ; ADR-027 (droits par rôle)

**Contexte**

* Le sujet prévoit des chasseurs-IA qui devront « épauler les chasseurs humains » et « faire le travail dans les zones non couvertes physiquement par des chasseurs » (StarterPack - BASE, `Readme.md:166-169`).
* L'appli du chasseur-IA est **hors périmètre** : « l'appli chasseur-IA (Phase future, hors fil-rouge) » (`documents utiles/CAHIER-DES-CHARGES-TECHNIQUE.md:82`).
* En base, un chasseur IA est une fiche `hunter` avec `is_hunter_ai` (`docker/init-v3/01_create_fil_rouge_immobilier.sql:303`, dépôt Fil-Rouge-API). Il a le rôle `'Hunter'` (ADR-057), donc **aujourd'hui les mêmes droits qu'un chasseur humain**.
* ADR-045 (point 6) a reporté ses droits propres au parcours IA. Sébastien juge ce report dangereux : une IA qui agit avec tous les droits d'un humain peut faire des dégâts que personne ne voit.

**Options**

1. **Mêmes droits qu'un humain**, comme aujourd'hui. Écartée : c'est le risque soulevé par Sébastien.
2. **Lecture seule** : le chasseur IA passe par le Reader. Écartée : il doit pouvoir « faire le travail » là où il n'y a pas de chasseur (`Readme.md:169`), donc proposer des biens.
3. **Un sous-ensemble des droits du Hunter**, fixé par une liste blanche. **Proposée.**

**Décision proposée**

1. Le chasseur IA garde le rôle `'Hunter'` et sa fiche `hunter` (ADR-057). C'est **`is_hunter_ai = TRUE`** qui réduit ses droits, dans l'API.
2. **Ce qu'il peut faire** : lire les demandes et les mandats qui lui sont confiés ; proposer des biens pour ces demandes.
3. **Ce qu'il ne peut pas faire** :
   * rien qui engage de l'argent ou un contrat : offre d'achat, vente, paiement, barème ;
   * lire le contact du vendeur (`estate_contact`, données personnelles, ADR-054) ;
   * modifier ou effacer une ligne qu'un humain a écrite.
4. Un refus rend **403**, comme tout autre manque de droit.
5. Le manager du chasseur IA (ADR-029) voit ce qu'il a proposé, comme pour un chasseur humain.

**Conséquences**

* La liste blanche s'ajoute à la matrice des droits (`md/securite/matrice-droits-crud-par-role.md`) et se code dans « le sien » du Hunter (`API/src/app/services/hunter_rows.py`, dépôt Fil-Rouge-API).
* Un test par interdiction : un chasseur IA reçoit 403, un chasseur humain non.
* Au jury, une phrase : « le chasseur IA est un chasseur à droits réduits : il cherche et propose, un humain engage ».

**Ce que cet ADR ne tranche pas**

* 🟡 La liste exacte des opérations : à relire avec la matrice, opération par opération, avant d'accepter.
* 🟡 L'enregistrement d'une visite par un chasseur IA : il ne visite pas. Est-ce le chasseur humain qui l'enregistre, ou personne ?
* 🟡 La tension avec le parcours IA du sujet, où les chasseurs-IA doivent pouvoir « opérer seuls » (`user-stories/09_futur_chasseur_assistance_ia.feature:6-7`, StarterPack, cité par ADR-045). Cet ADR choisit la prudence ; le parcours IA pourra élargir la liste.
* 🟡 À montrer à Jeff (client) avant d'accepter.

**Sources**

| Affirmation | Source |
|---|---|
| « dangereux », droits réduits voulus | Sébastien, Discord, 15/10/2026 (question `adr15-4`) |
| Missions des chasseurs-IA | StarterPack - BASE, `Readme.md:166-169` |
| Appli chasseur-IA hors périmètre | StarterPack - BASE, `documents utiles/CAHIER-DES-CHARGES-TECHNIQUE.md:82` |
| `is_hunter_ai` au schéma | Fil-Rouge-API, `docker/init-v3/01_create_fil_rouge_immobilier.sql:303` ; `API/src/app/models/hunter_model.py:44` |
| Droits reportés au parcours IA | ADR-045, point 6 |
| « opérer seuls » | `user-stories/09_futur_chasseur_assistance_ia.feature:6-7` (StarterPack), via ADR-045 |

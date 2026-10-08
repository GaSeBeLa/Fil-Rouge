# ADR-029 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 029 est une proposition** (lettre Z du pense-bête,
> `md/adr/2026-10-08-proposition-regroupement-adr.md:40`).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt.** Relu le
> 08/10/2026 par deux relecteurs (sources ; oral et jury) et un arbitre. Aucune
> question ne reste ouverte : toutes sont tranchées par les sources (voir
> « Questions tranchées »).
>
> 🗂️ **Un point réglé hors de la fiche** (il parle des pages Confluence) :
> ADR-025 cite-t-il « ADR-026 » pour « pas d'authentification » ? Non. Vérifié
> dans la copie du journal du 07/10 : 0 occurrence dans ADR-025 (l. 1104-1142).
> Seul ADR-027 le fait (l. 1186, 1221, 1224). La note du jour
> (`md/adr/2026-10-08-notes-seance-adr.md:64`) est à corriger sur ce point.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) — commentaires à mettre
> à jour, documentation seule :
>
> * en-tête de `docker/init-v3/01_create_fil_rouge_immobilier.sql:13-37` : il
>   cite ENF-03 comme origine, nomme le lien « Manages » et dit « À acter en ADR » ;
> * `docker/init-v3/README.md:544-545` (« pas encore acté en ADR ») et `:577-581`
>   (« À assumer, ou renommer le second (« Supervises ») »).
> * `docker/init-v2/` est figé : on n'y touche pas.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-029 : Chaque chasseur est rattaché à un manager — la raison réécrite

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décision du groupe : 07/10/2026)
* **Statut :** proposé
* **Décideurs :** l'équipe projet (réponse « garder » à la Q9 de la page d'incohérences du 07/10, carte Q-ACC-20)
* **Remplace :** ADR-025 (« Chaque chasseur est rattaché à un manager », 22/09/2026). ADR-025 passe à « remplacé par ADR-029 ».

**Contexte**

ADR-025 relie chaque chasseur à un manager : la colonne `hunter.id_realestatemanager`, obligatoire. Il a été accepté sur Confluence le 22/09. La copie du journal du 07/10 le dit « Annulé », sans date ni raison écrite.

Sa raison écrite était un contrôle d'accès. Le lien était « nécessaire pour appliquer ce contrôle d'accès » : l'exigence ENF-03, « L'accès aux données de rémunération est restreint au chasseur concerné et à son manager ».

Cette raison a deux faiblesses :

* **ENF-03 se lit de deux façons dans le sujet.** Le modèle de cahier des charges la range dans un « Exemple rempli (extrait) ». Les règles de calcul l'appellent « exigence ENF-03 ». ADR-025 le disait lui-même : « un exemple rempli dans un modèle de document ».
* **Le contrôle ne devait pas être codé.** Le 22/09, le client a mis l'authentification hors périmètre. ADR-027 demandait donc de réécrire cet argument.

Le lien est pourtant resté en base, et plusieurs réponses du groupe s'appuient dessus : Q-ACC-02, Q-SCH-13, Q-MIG-04, Q-ACC-16.

Le 07/10, le groupe a tranché la Q9 : garder le lien, et écrire sa raison dans un nouvel ADR. La raison retenue : l'organisation de l'entreprise. Le même jour, le client a rouvert l'authentification, côté back (ADR-028).

**Options envisagées**

1. **Abandonner le lien.** Avantage : conforme au statut « Annulé ». Inconvénients : Q-ACC-02, Q-SCH-13 et Q-MIG-04 sont à revoir, et la base à changer. Écartée par la Q9.
2. **Déduire le manager des demandes** (`search_request.id_realestatemanager`). Avantage : pas de colonne en plus. Écartée dès ADR-025 : un chasseur sans demande n'a alors aucun manager, et deux demandes peuvent en donner deux. C'est toujours vrai : la colonne de la demande accepte le vide.
3. **Un lien facultatif (0,1).** Avantage : souple. Écartée dès ADR-025 : la base ne garantit plus la règle, tout repose sur l'API.
4. **Garder ADR-025 et corriger sa raison sur place.** Avantage : pas de nouveau numéro. Écartée : ADR-025 a été accepté, et le groupe ne réécrit jamais un ADR accepté (ADR-023, copie du journal, l. 804). Le sujet dit : « **Ne jamais effacer** un ADR : s'il est remplacé, marquer « remplacé par ADR-XXX ». » (`JOURNAL-DE-DECISIONS.md:72`).
5. **Garder le lien tel qu'il est en base, et écrire sa raison dans un nouvel ADR.** **Retenue** (Q9).

**Décision**

1. ✅ Le lien se garde, **sans rien changer en base** : `hunter.id_realestatemanager INTEGER NOT NULL`, clé vers `real_estate_manager(id_user)`, `ON DELETE RESTRICT`. Relation Hunter (1,1) — RealEstateManager (0,n).
2. ✅ Sa raison : **l'organisation de l'entreprise** (réponse du groupe, Q-ACC-20). Le sujet ne décrit cette organisation qu'à travers « son manager » : le chasseur a un manager (ENF-03, `REGLES-CALCUL-REMUNERATION.md:296`). L'équipe en tire un manager par chasseur, et donc des équipes, une par manager : c'est sa modélisation, pas une phrase du sujet.
3. ✅ ENF-03 **n'est plus la raison** du lien. Le lien reste compatible avec ENF-03, quelle qu'en soit la lecture.
4. ✅ Sur le MPD, ce lien s'appelle **« Supervises »**. Il se distingue ainsi du manager qui traite une demande.
5. ✅ **Pas d'historique** des changements de manager : seul le manager courant est connu. Inchangé depuis ADR-025.

**Justification**

* L'option retenue à la Q9 tient en une ligne : les réponses déjà données par le groupe tiennent, et la base ne change pas (`md/journal/2026-10-07-plan-action.html:461`).
* La nouvelle raison ne dépend ni d'un texte du sujet qui se lit de deux façons, ni d'un périmètre qui a déjà changé deux fois.
* Le lien sert des décisions du groupe déjà prises :
  * Q-ACC-02 : le manager voit **ses** chasseurs et leurs paiements. La page d'incohérences le relevait : cette réponse « a besoin de ce lien ».
  * Q-ACC-16 et Q-MIG-04 : le seed crée 2 managers, répartit les 6 chasseurs en 2 équipes, puis efface le manager fictif.
* Avec ADR-028, le filtre de Q-ACC-02 devient codable : la branche `Manager` du tuto 2 filtre les paiements par ce lien. C'est un usage du lien, pas sa raison.

**Conséquences**

* **Base :** rien ne change. Ni colonne, ni contrainte, ni migration.
* **ADR-025 :** passe à « remplacé par ADR-029 » sur Confluence. Son texte ne s'efface pas. Le mot « Annulé » disparaît : il n'existe pas dans le modèle du prof.
* **Seed :** pas encore fait. `docker/init-v3/02_migration.sql:126-144` rattache toujours les 6 chasseurs au manager fictif (user 25). Le remplacement attend le chantier « Seed de démo » (`context AI/08-etat.md:54`).
* **Droits :** la colonne `Manager` de la matrice (ADR-027 réécrit) s'appuie sur ce lien.
* **Inconvénient accepté, faute d'historique :** un chasseur qui change de manager emporte tout son passé. Le nouveau manager voit tous ses anciens paiements (Q-ACC-02) ; l'ancien n'en voit plus aucun (déduit de la Décision 5).
* **Deux managers par demande possibles :** le manager qui traite une demande et le manager du chasseur affecté peuvent différer. Rien ne l'interdit, et c'est assumé.
* **Chasseurs-IA :** la colonne est obligatoire, donc un chasseur-IA (`hunter.is_hunter_ai`) aura lui aussi un manager. Le parcours IA est reporté (Q-ACC-14).
* **Pour l'authentification, citer ADR-028.** L'ADR-026 de Confluence traite des mots de passe, pas du périmètre de l'authentification.

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Garder ou abandonner le lien ? | Garder | `md/questions/questions-a-trancher.md:259` (réponse du groupe à Q-ACC-20, Q9) ; texte de l'option : `md/journal/2026-10-07-plan-action.html:461` |
| Quelle raison ? | L'organisation de l'entreprise | `questions-a-trancher.md:259` |
| Remplacer ou amender ADR-025 ? | Remplacer, par un nouvel ADR | `questions-a-trancher.md:259`, `:420` ; `documents utiles/JOURNAL-DE-DECISIONS.md:72` ; ADR-023, copie du journal, l. 804 |
| ENF-03 est-elle une exigence ? | Le sujet dit les deux. Cet ADR ne s'appuie pas dessus, donc la question ne le bloque pas | `CAHIER-DES-CHARGES-TECHNIQUE.md:45`, `:74`, `:92`, `:97` ; `REGLES-CALCUL-REMUNERATION.md:296`, `:763` ; `questions-a-trancher.md:457` |
| Quel nom sur le MPD ? | « Supervises » (Q-SCH-13, 05/10) | `questions-a-trancher.md:168` |
| Le manager de la demande et celui du chasseur doivent-ils coïncider ? | Non, déduit : le groupe a choisi de renommer le lien (Q-SCH-13), pas d'ajouter une contrainte. ADR-025 laissait ce choix : « À assumer, ou renommer » | journal Confluence, ADR-025, « Conséquences » ; `questions-a-trancher.md:168` |
| Garder un historique des managers ? | Non, déduit : la Q9 garde la base telle quelle, et ADR-025 n'en gardait pas | `plan-action.html:461` ; journal Confluence, ADR-025, « Décision » |

**Questions ouvertes** 🟡

Aucune.

**Sources**

| Affirmation | Source |
|---|---|
| ADR-025 : décision, raison ENF-03, options 1 à 3, pas d'historique, deux liens « Manages » | copie du journal Confluence du 07/10, lignes 1104-1142 ; brouillon `md/adr/adr-025-lien-chasseur-manager.md:14-69` |
| ADR-025 « Annulé » sur Confluence, sans raison écrite | copie du journal Confluence du 07/10, ligne 1106 |
| ADR-025 accepté le 22/09 | `md/journal/2026-09-21-a-faire-a-la-main.md:189-190` |
| ADR-027 demande de réécrire l'argument d'ADR-025 | copie du journal Confluence du 07/10, ligne 1230 |
| ENF-03 : exemple dans le modèle de cahier des charges | `documents utiles/CAHIER-DES-CHARGES-TECHNIQUE.md:45`, `:74`, `:92`, `:97` (StarterPack) |
| ENF-03 : « exigence » dans les règles de calcul ; « son manager » | `documents utiles/REGLES-CALCUL-REMUNERATION.md:296`, `:763` (StarterPack) |
| Le sujet ne parle du manager du chasseur qu'à travers ENF-03 | grep « manager » dans le StarterPack, 08/10/2026 : `CAHIER-DES-CHARGES-TECHNIQUE.md:97` et `REGLES-CALCUL-REMUNERATION.md:296`, `:763` ; les autres occurrences (`Gherkin.md`) sont un exemple de note de frais, hors sujet |
| Q9 : garder le lien ; options « garder » et « abandonner » | `md/journal/2026-10-07-plan-action.html:454-462` |
| Réponse du groupe à Q-ACC-20, raison « organisation de l'entreprise » | `md/questions/questions-a-trancher.md:259`, `:420` |
| Q-ACC-02 : le manager voit ses chasseurs et leurs paiements | `questions-a-trancher.md:241` |
| Q-ACC-02 a besoin du lien | `md/journal/2026-10-07-plan-action.html:457` |
| Q-SCH-13 : « Supervises » | `questions-a-trancher.md:168` |
| Q-ACC-16, Q-MIG-04 : 2 managers, 2 équipes, manager fictif effacé | `questions-a-trancher.md:179`, `:187` |
| La colonne en base | `docker/init-v3/01_create_fil_rouge_immobilier.sql:294-297` ; commentaire `:1071-1072` |
| La colonne de la demande accepte le vide | `docker/init-v3/01_create_fil_rouge_immobilier.sql:317-318` |
| Le modèle de l'API | `API/src/app/models/hunter_model.py:51` |
| Le manager fictif et les 6 chasseurs rattachés | `docker/init-v3/02_migration.sql:126-144` |
| Filtre « ses chasseurs » codable avec l'authentification | `md/securite/tuto-2-authentification-jwt.md:493-500` ; ADR-028 |
| Parcours IA reporté | `questions-a-trancher.md:186` (Q-ACC-14) |
| Modèle d'ADR : statuts, « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:22`, `:72` (StarterPack) |
| « on ne réécrit jamais un ADR accepté » : convention du groupe | ADR-023, copie du journal Confluence du 07/10/2026, l. 804 |

# ADR-051 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 051 est une proposition.** 050 est déjà pris (renouvellement du
> mandat). Le sujet n'est pas dans la liste des 23 de
> `md/adr/2026-10-08-proposition-regroupement-adr.md` : il vient de la séance du
> 08/10/2026 (`md/adr/2026-10-08-notes-seance-adr.md:30`, `:57`).
>
> 💡 **Rédigé le 08/10/2026 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et
> un arbitre. Les passages marqués « déduit » sont une lecture des sources, pas
> une décision du groupe.
>
> 🗂️ **Un point réglé hors de la fiche : avec l'ADR-042, ou à part ?** À part.
> Les notes du jour laissaient le choix (`2026-10-08-notes-seance-adr.md:57`).
>
> * ADR-042 (lettre P) parle des **notes de performance** : un score de 0 à 100,
>   dans `hunter_performance` (`01:996-1025`).
> * Cette fiche parle de la **note d'avis** : le texte du chasseur sur un bien,
>   dans `estate_searchrequest` (`01:662` ; `09-rapport-ecarts-contraintes.md:284-285`).
> * Deux « notes » différentes, deux tables, deux sources (Q-SCH-06 d'un côté ;
>   Discord et la story U33 de l'autre).
> * Le sujet veut « une fiche courte par décision » (`JOURNAL-DE-DECISIONS.md:7`).
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * **Le schéma a 20 tables** (20 `CREATE TABLE` dans `01`). Disent encore
>   « 19 » : `docker/init-v3/01_create_fil_rouge_immobilier.sql:3` et `:1094` ;
>   `docker/init-v3/README.md:13` et `:133` ; `CLAUDE.md:13`, `:25`, `:36` ;
>   `API/src/app/main.py:24` ; `API/src/app/models/__init__.py:2`. Le compte de
>   258 colonnes (`01:1094`) n'a pas été remesuré.
> * `docker/init-v3/README.md` ne cite ni `review_media` ni la migration 17.
> * `md/securite/matrice-droits-crud-par-role.md` n'a pas de ligne
>   `review_media` : à ajouter avec la réécriture d'ADR-027.
> * `livrables/2-modelisation/09-decisions-a-prendre.md:486` : le nom de la
>   « table des médias d'un avis » est vide. Nom retenu : `review_media`.
> * `livrables/2-modelisation/09-rapport-ecarts-contraintes.md:137` : case
>   « une table de médias pour les avis (U33) » à cocher ; l. 284-285 citent
>   encore `media_url` et `media_type` sur `Estate_SearchRequest`.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-051 : Une note d'avis peut porter plusieurs médias (audio, vidéo) : table `review_media`, un média par ligne

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décision du groupe : 08/10/2026)
* **Statut :** proposé
* **Décideurs :** Sébastien (« option 2 »), sur une question de Gabriel — Discord, 08/10/2026 (`md/adr/2026-10-08-notes-seance-adr.md:30`). Seule trace écrite : ces notes, qui citent Discord (l. 36).
* **Remplace :** aucun ADR. Aucun ADR ne parlait des médias (même fichier, l. 57).

**Contexte**

Le sujet : « le chasseur rédige une note d'avis, peut y joindre des commentaires audio et des vidéos » (`Readme.md:129`, StarterPack). Le scénario 06 le redit : « Alors je peux y joindre des commentaires audio et des vidéos » (`06_chasseur_avis_et_offre_achat.feature:14`).

La note d'avis vit sur `estate_searchrequest`, la ligne d'un bien retenu pour une demande. Son texte est `review_hunter`, 2 000 caractères au plus (`docker/init-v3/01_create_fil_rouge_immobilier.sql:662`).

Jusqu'au 08/10/2026, cette même ligne portait **un seul** média (`docker/init-v2/01_create_fil_rouge_immobilier.sql:590-598`) :

* `media_url TEXT` ;
* `media_type VARCHAR(10) CHECK (media_type IN ('audio', 'video'))` ;
* `chk_media` : les deux remplis, ou aucun.

Le rapport d'écarts du 11/09/2026 l'avait vu : « « des » audios **et** des vidéos pour un même avis demandent plusieurs médias par avis, donc une table à part » (`livrables/2-modelisation/09-rapport-ecarts-contraintes.md:394`). La case était restée ouverte (même fichier, l. 137).

Le 08/10/2026, Gabriel a posé la question sur Discord. Sébastien a choisi « option 2 ».

**Options envisagées**

Le message de Gabriel n'est pas recopié dans le dépôt : ses options exactes ne sont pas connues. Les notes ne nomment que l'option retenue, « au lieu de 2 colonnes » (`2026-10-08-notes-seance-adr.md:57`).

1. **Garder les deux colonnes** sur `estate_searchrequest` (l'état d'avant). Avantage : rien à changer. Inconvénient : un seul média par note ; « des commentaires audio et des vidéos » ne passe pas. **Écartée.**
2. **Une table `review_media`**, une ligne par média, reliée à la note (1-N). Avantages : autant de médias qu'il faut ; chaque média garde son `CHECK` de type et sa clé vers la note. Inconvénients : une table de plus ; une base existante à migrer. **Retenue** (« option 2 »).
3. 💡 **Plusieurs adresses dans une seule colonne** (tableau ou JSON). Option ajoutée à la rédaction, pas discutée par le groupe. Avantage : pas de table. Inconvénient : plus de `CHECK` ni de type par média. **Écartée.**

**Décision**

1. Une table `review_media` (`01:670-681`) :
   * `id` et `created_at`, comme les autres tables ;
   * `media_url TEXT NOT NULL` ;
   * `media_type VARCHAR(10) NOT NULL CHECK (media_type IN ('audio', 'video'))` ;
   * `id_estate_searchrequest INTEGER NOT NULL REFERENCES estate_searchrequest(id) ON DELETE RESTRICT`.
2. Une ligne = un média. Une note d'avis a de 0 à n médias. Un média appartient à une seule note.
3. `media_url`, `media_type` et `chk_media` sortent de `estate_searchrequest` (`01:659-668`).
4. Pas de plafond : aucun `CHECK` ne limite le nombre de médias d'une note.
5. Au MPD (v8) : table `ReviewMedia`, lien « Accompanies », (0,n) côté `Estate_SearchRequest`, (1,1) côté `ReviewMedia` (`2026-10-08-notes-seance-adr.md:76`, `:108`).

**Justification**

* Le sujet dit « des » audios « et des » vidéos pour une même note (`06_…feature:14`) : il en faut plusieurs.
* La base reste gardienne. Le type est vérifié par `CHECK`, la note par clé étrangère. Les tests le montrent (voir Conséquences).
* `chk_media` n'a plus d'objet : une ligne de `review_media` est toujours un média, donc ses deux colonnes sont `NOT NULL`.
* Même forme que les photos d'un bien : `picture` porte une adresse (`url TEXT NOT NULL`) et une clé vers son bien (`01:644-649`).

**Conséquences**

* **Schéma :** commit `f27123d` (08/10/2026) : `01:670-681`.
* **Migration v2 :** `docker/migrations/v2-vers-v3/17_medias-de-la-note-d-avis.sql`. Elle copie les médias existants avant de retirer les colonnes (l. 46-57), puis retire `chk_media`, `media_url` et `media_type` (l. 59-62). « Compté le 2026-10-08 en base de dev : 0 note d'avis (donc 0 média). » (l. 17).
* **API :** modèle `ReviewMedia` (`API/src/app/models/review_media_model.py`), route `/review-media` (`routes/review_media_router.py`), service sans règle (`services/review_media_service.py`). Branchés dans `main.py:53` et `:94`.
* **Tests :** trois médias (audio, vidéo, audio) sur une même note, 201 ; un type `'image'`, 409 ; une note inconnue, 409 (`API/tests/integration/test_constraints_db.py:385`, `:399`, `:406`).
* **Le fichier n'est pas dans la base.** La table garde une adresse, comme `picture.url` (`01:647`). Les fichiers iraient dans le stockage objet d'ADR-015 (MinIO), prévu pour les « objets volumineux et non structurés » (journal Confluence, copie du 07/10/2026, ADR-015, Contexte).
* **Aucun envoi de fichier n'est codé.** « minio » : 0 résultat dans `API/src`. MinIO est gardé « a priori » (Q-INF-01, `md/questions/questions-a-trancher.md:190`).
* **Aucun contrôle de l'adresse** : `media_url` est un `TEXT NOT NULL`, sans format (`01:677`).
* **`ON DELETE RESTRICT`** : une note qui a des médias ne se supprime pas avant eux. C'est la règle de tout le schéma : aucune clé n'est en `CASCADE` (0 `ON DELETE CASCADE` dans `01`, compté le 08/10/2026). Le groupe désactive plutôt que de supprimer : « les clés en `RESTRICT` y poussent déjà » (Q-ACC-08, `md/questions/questions-a-trancher.md:1037`).
* **Rôle en lecture seule :** une base neuve lui donne la table (`docker/init-v3/04_role-lecture-seule.sql:51`, joué après `01`). Une base migrée compte sur les droits par défaut (`docker/migrations/v2-vers-v3/12_role-lecture-seule.sql:71`) : pas vérifié en base.
* **Journal :** aucun ADR remplacé.

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Au MPD, « Accompanies » ou « Illustrates » ? Les notes disent : « Le verbe « Accompanies » est un choix de Claude : le groupe peut préférer « Illustrates ». » | « Accompanies ». Déduit : c'est le verbe de la v8 du MPD, reçue sur Discord le 08/10/2026 (15 h 04). | déduit de `2026-10-08-notes-seance-adr.md:78`, `:107-108` |
| Le fichier audio ou vidéo va-t-il dans la base ? | Non : une adresse. Déduit : `media_url TEXT`, comme `picture.url` ; ADR-015 range ces objets dans un stockage objet. | déduit de `01:647`, `01:677` ; ADR-015, Contexte (journal Confluence) |
| Combien de médias par note ? | Pas de plafond. Le sujet dit « des », sans nombre ; aucun `CHECK` ne limite. | `06_…feature:14` ; `01:670-681` |
| Des images ? | Non : audio ou vidéo seulement. Les photos d'un bien vont dans `picture`. | `06_…feature:14` ; `01:678` ; `test_constraints_db.py:399` ; `01:644-649` |
| Qui écrit un média ? Qui le lit ? | Le chasseur l'écrit ; le client le lit. Déduit : les droits de la note s'étendent à ses médias. À écrire dans la matrice (ADR-027). | déduit de `06_…feature:14-15` (« je peux y joindre », « mise à disposition de mon client ») et de `md/securite/matrice-droits-crud-par-role.md:172`, `:185` |

**Questions ouvertes** 🟡

Aucune.

**Sources**

| Affirmation | Source |
|---|---|
| Note d'avis avec « des commentaires audio et des vidéos » | `Readme.md:129` ; `user-stories/06_chasseur_avis_et_offre_achat.feature:13-15` (StarterPack) |
| « une fiche courte par décision » | `documents utiles/JOURNAL-DE-DECISIONS.md:7` (StarterPack) |
| Décision 6 : Gabriel demande, Sébastien choisit « option 2 » | `md/adr/2026-10-08-notes-seance-adr.md:30` |
| Appliquée par `f27123d` ; sources Discord seulement | même fichier, l. 35-36 |
| « au lieu de 2 colonnes » ; aucun ADR sur les médias | même fichier, l. 57 |
| MPD v8 : `ReviewMedia`, « Accompanies », (0,n) / (1,1) | même fichier, l. 74-78, l. 107-108 |
| v2 : un seul couple `media_url` / `media_type`, `chk_media` | `docker/init-v2/01_create_fil_rouge_immobilier.sql:590-598` |
| U33 : il faut une table à part | `livrables/2-modelisation/09-rapport-ecarts-contraintes.md:137`, `:394` |
| Note d'avis sur `Estate_SearchRequest` | même fichier, l. 284-285 |
| Nom à choisir : « table des médias d'un avis » | `livrables/2-modelisation/09-decisions-a-prendre.md:486` |
| `review_media` ; `estate_searchrequest` sans médias | `docker/init-v3/01_create_fil_rouge_immobilier.sql:659-681` |
| `picture` : une adresse par photo | même fichier, l. 644-649 |
| Migration v2 | `docker/migrations/v2-vers-v3/17_medias-de-la-note-d-avis.sql:1-64` |
| API | `API/src/app/models/review_media_model.py` ; `routes/review_media_router.py` ; `services/review_media_service.py` ; `main.py:53`, `:94` |
| Tests | `API/tests/integration/test_constraints_db.py:370-409` |
| ADR-015 : MinIO, objets volumineux | journal Confluence, copie du 07/10/2026, ADR-015, Contexte |
| Q-INF-01 : MinIO gardé a priori | `md/questions/questions-a-trancher.md:190` |
| Droits sur la note d'avis | `md/securite/matrice-droits-crud-par-role.md:172`, `:185` |
| Rôle en lecture seule | `docker/init-v3/04_role-lecture-seule.sql:51-52` ; `docker/migrations/v2-vers-v3/12_role-lecture-seule.sql:70-71` |
| Aucune clé en `CASCADE` ; désactiver plutôt que supprimer (Q-ACC-08) | recherche « ON DELETE CASCADE » dans `docker/init-v3/01_create_fil_rouge_immobilier.sql`, 08/10/2026 : 0 ; `questions-a-trancher.md:1037` |
| Modèle d'ADR, « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:19-40`, `:72` (StarterPack) |

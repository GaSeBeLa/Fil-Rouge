# ADR-047 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 047 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:70`,
> lettre W). Il ne vaut rien tant que le groupe ne l'a pas pris sur Confluence.
>
> 💡 **Rédigé le 08/10/2026 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Les passages marqués « déduit » sont une lecture des sources, pas une
> décision du groupe. Aucune question ne reste ouverte : l'import régulier des
> annonces est devenu la limite 7 d'ADR-045 (réécrite et acceptée par le groupe le 2026-10-09 : un flux Airflow).
>
> 🗂️ **Sur la page d'ADR-027 (Confluence, « proposé », 22/09/2026)** : sa
> question n° 8, « L'import des biens tourne sous quel compte ? », avec la
> raison « Aucun rôle humain ne crée un bien » (journal Confluence, ADR-027 du 22/09/2026, questions, n° 8).
> Cette fiche y répond, et la raison ne tient plus. Le brouillon réécrit
> d'ADR-027 (lot 4) y répond aussi, en renvoyant à cette fiche.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * `md/securite/matrice-droits-crud-par-role.md` dit encore que les biens
>   viennent de l'import, « pas d'une saisie » (l. 119-121), qu'ils sont
>   « Écrit par le système » (l. 175), et « Aucun rôle humain ne crée un bien »
>   (l. 237). La ligne `estate` (l. 169) ne donne le droit C à aucun rôle.
>   À aligner : C pour le chasseur et le manager.
> * La décision F5 (forme de la colonne, choisie par Sébastien à LOT9) attend
>   encore « Je garde » ou « À revoir » du groupe
>   (`md/journal/2026-10-07-rapport-final-chantier-lot.html:550-562`). Accepter
>   cette fiche, qui la porte (Sujet 3), y répond.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-047 : Biens — importés par l'admin, ou saisis à la main par un chasseur ou un manager ; l'auteur est noté

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions : 06/10/2026, 07/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * Jeff, client, entretien du 07/10/2026 : un bien peut être saisi à la main (Q-JEF-24) ;
  * le groupe : qui lance l'import, l'admin (Q-ACC-09, 06/10/2026) ; qui saisit à la main, le chasseur et le manager (Q8, 07/10/2026) ;
  * Sébastien, à LOT9 (07/10/2026) : la forme de la colonne d'auteur (F5). Le groupe la prend en acceptant cet ADR.
* **Répond à :** la question n° 8 d'ADR-027 (proposé, 22/09/2026)

**Contexte**

Le sujet ne décrit qu'une arrivée des biens : le système envoie au chasseur une sélection de biens (`Readme.md:127` ; `05_chasseur_selection_quotidienne_biens.feature:14-17`). L'outil du sujet génère des annonces factices, « comme si les données provenaient de plusieurs sources différentes (agences, particuliers, plateformes) » (`outils/Readme.md:6`).

Dans le projet, les biens arrivent par une chaîne d'import :

1. `normalised/normalised.py` nettoie les annonces ;
2. il écrit `annonces_normalised.csv` ;
3. le script `docker/init-v3/03_populate_estate.sql` insère **2 556** biens.

L'étape 2 → 3 n'est pas un script du dépôt. `03` est une copie retouchée de `normalised/populate_estate.sql`, et « le script de retouche n'est pas dans le dépôt » (`md/questions/questions-a-trancher.md:180`). Aucun fichier `.py` ni `.sh` ne produit `populate_estate.sql` (recherche du 08/10/2026).

`03` tourne une seule fois, à la création de la base. Il passe par le compte PostgreSQL du conteneur, `POSTGRES_USER`, pas par un compte de l'application (`docker/docker-compose.yml:8`, `:17`).

La matrice des droits en tirait une règle : « Aucun rôle humain ne crée un bien ». Deux questions restaient ouvertes. Un bien peut-il être saisi à la main ? Et qui lance l'import ?

**Options envisagées**

Sujet 1 — d'où vient un bien :

1. **L'import seul.** C'était la matrice des droits. **Écartée** par Jeff : la saisie à la main est « courant dans l'immobilier » (Q-JEF-24).
2. **L'import, et la saisie à la main.** **Retenue.**

Sujet 2 — qui saisit un bien à la main (Q8) :

1. **Le chasseur et le manager, avec l'auteur noté sur le bien.** Avantage : le chasseur entre lui-même un bien trouvé hors marché ; on sait qui l'a saisi. Inconvénient : une colonne de plus. Option recommandée. **Retenue.**
2. **Le manager seul.** Avantage : un contrôle avant d'entrer au catalogue. Inconvénient : le chasseur dépend du manager. **Écartée.**
3. **Le demander à Jeff.** **Écartée** : le groupe a tranché lui-même.

Sujet 3 — comment noter l'auteur (F5, LOT9) :

1. **Une clé vers `"user"`, facultative.** Avantage : simple, et pareil que `criteria.id_author`. Inconvénient : le contrôle du rôle reste à écrire dans l'API. **Retenue.**
2. **Un trigger qui vérifie le rôle.** **Écartée.**
3. **Une clé vers `hunter` seul.** Inconvénient : le manager ne pourrait pas être auteur. **Écartée.**

Sujet 4 — quel compte lance l'import (Q-ACC-09) :

1. **Un compte technique dédié.** Avantage : sépare l'humain de la machine. Option recommandée. **Écartée** par le groupe.
2. **L'admin.** Avantage : rien à créer. **Retenue.**

**Décision**

1. Un bien entre en base de deux façons : **importé**, ou **saisi à la main**.
2. Seuls un **chasseur** ou un **manager** saisissent un bien à la main.
3. `estate.id_author` note l'auteur d'un bien saisi à la main. **Vide veut dire importé.**
4. La colonne est une clé vers `"user"(id)`, facultative, `ON DELETE RESTRICT`. La base refuse un auteur inconnu. Le rôle de l'auteur se vérifie dans l'API.
5. L'import est lancé par l'**admin** (Q-ACC-09). Aujourd'hui, cela veut dire créer la base, qui joue `03` sous le compte PostgreSQL du conteneur. L'import ne passe pas par l'API : aucun compte de l'application n'y prend part.

Le code, tel qu'il est aujourd'hui (`docker/init-v3/01_create_fil_rouge_immobilier.sql:624-629`) :

```sql
-- Auteur d'un bien saisi à la main, chasseur ou manager ; vide (NULL) :
-- bien importé (Q-ACC-09, Q-JEF-24 ; LOT9). Même forme que
-- criteria.id_author : un auteur inconnu est refusé, le rôle se vérifie
-- dans l'API.
id_author            INTEGER
                     REFERENCES "user"(id) ON DELETE RESTRICT,
```

**Justification**

* **Le métier le demande.** Jeff : « oui, un bien peut être saisi à la main (hors marché, courant dans l'immobilier) » (Q-JEF-24, 07/10/2026).
* **Savoir qui a saisi quoi.** Sans colonne, la ligne ne dit pas qui l'a créée (carte Q-ACC-09). Le même besoin a déjà sa réponse ailleurs : `search_request.id_author` et `criteria.id_author` (`01_…sql:311`, `:395`).
* **Facultative, au contraire de ces deux colonnes.** Elles sont `NOT NULL`. Ici, un bien importé n'a pas d'auteur humain : vide est la seule valeur honnête.
* **Le rôle dans l'API, pas en base.** C'est la même forme que `criteria.id_author`. Un trigger ajouterait une règle qui croise deux tables ; le groupe a mis ces règles dans l'API (Q-MAN-06, `questions-a-trancher.md:155`).

**Conséquences**

* **Code : déjà fait** à LOT9 (`cd05768`) :
  * la colonne (`01_…sql:624-629`) ;
  * la migration d'une base v2 (`docker/migrations/v2-vers-v3/09_biens.sql:40-41`) ;
  * le modèle de l'API (`API/src/app/models/estate_model.py:81-82`) ;
  * l'import laisse la colonne vide (`docker/init-v3/03_populate_estate.sql:10-11`).
* **Tests.** Un auteur inconnu est refusé (409). Un auteur connu est accepté (201) (`API/tests/integration/test_constraints_db.py:120-128`).
* **À coder dans l'API :** vérifier que l'auteur est un chasseur ou un manager (rapport final du chantier LOT, `2026-10-07-rapport-final-chantier-lot.html:668`). Aucun contrôle de rôle n'est codé aujourd'hui.
* **`POST /estates` devra exiger un auteur**, déduit, ✅ confirmé par le groupe le 09/10/2026 (S11) : la route existe (`API/src/app/routes/crud_router.py:88-93`), et l'import ne passe pas par elle. Un bien posté sans auteur se lirait comme importé. En base, `id_author` reste facultatif. 🟡 À revoir avec D8 : si le flux Airflow passe un jour par l'API, il faudra un compte technique ou une route d'import (remarque d'Améthyste, 09/10/2026).
* **Supprimer un auteur est refusé** (`ON DELETE RESTRICT`). Cela va avec la règle du groupe : désactiver un compte plutôt que le supprimer (Q-ACC-08, `questions-a-trancher.md:1037`).
* **L'import aujourd'hui.** Lancer l'import, c'est créer la base : le script `03` est joué à ce moment (`docker/docker-compose.yml:17`). Il n'écrit pas par l'API, donc aucun rôle de l'application n'a besoin du droit de créer un bien pour l'import.
* **Référence d'un bien saisi à la main.** La base exige une référence unique et non vide (`01_…sql:561-562`). Son format n'est pas fixé. Micro-décision, hors ADR (`JOURNAL-DE-DECISIONS.md:13`).
* **Import par flux orchestré, avec dédoublonnage** (ADR-045, limite 7, proposée puis acceptée par le groupe le 2026-10-09). Aujourd'hui le dépôt ne charge les annonces qu'une fois (`03`) ; le flux reste à écrire. Un bien saisi à la main pourrait aussi arriver par l'import : à régler, avec l'endroit où vit le flux, après les cours de machine learning et de data science (Sébastien, 2026-10-09). Le sujet range le dédoublonnage dans le futur parcours IA (`Readme.md:193`).

**Questions tranchées par les sources**

1. **Un bien importé a-t-il un auteur ?**
   Non : la colonne reste vide (`03_populate_estate.sql:10-11` ; `01_…sql:624-625`).
2. **L'admin peut-il saisir un bien à la main ?**
   Non, déduit de Q8 : le groupe nomme le chasseur et le manager (`questions-a-trancher.md:252`). L'admin lance l'import, ce qui ne laisse pas d'auteur.
3. **Où se vérifie le rôle de l'auteur ?**
   Dans l'API (`01_…sql:626-627` ; F5).
4. **L'admin doit-il avoir le droit de créer un bien dans l'API, pour l'import ?**
   Non, déduit : l'import est un script SQL joué sous `POSTGRES_USER` (`docker/docker-compose.yml:8`, `:17`), pas un appel à l'API.

5. **Un import régulier des nouvelles annonces entre-t-il dans le projet (Airflow) ?**
   Oui, accepté par le groupe le 2026-10-09 (proposé par Sébastien, Discord) : un flux Airflow, avec tri, mise en forme et dédoublonnage en map/reduce. C'est la limite 7 d'ADR-045, acceptée par le groupe le 2026-10-09 ; l'ADR-045 dans son ensemble reste « proposé ». La version du 08/10 disait non, en lisant la note du groupe comme conditionnelle : « si non les biens vont être importer via un script dans Airflow » (Q-ACC-09) ; Jeff avait dit oui à la saisie à la main. Le sujet n'impose aucun outil : « Airflow » n'y apparaît pas, c'est un choix du groupe.

**Questions ouvertes** 🟡

Aucune.

**Sources**

| Affirmation | Source |
|---|---|
| Le système envoie une sélection de biens, chaque jour | `Readme.md:127` ; `user-stories/05_chasseur_selection_quotidienne_biens.feature:14-17` (StarterPack) |
| Annonces factices, « plusieurs sources différentes » | `outils/Readme.md:6` ; `Readme.md:46` (StarterPack) |
| Dédoublonnage dans le futur parcours IA | `Readme.md:193` (StarterPack) |
| « Airflow » absent du sujet | recherche du 08/10/2026 dans le StarterPack : 0 fichier |
| Import par flux Airflow, dédoublonnage : limite 7 | ADR-045 (limite 7 acceptée le 2026-10-09) ; message de Sébastien, Discord, 2026-10-09 |
| `03` copie retouchée ; le script de retouche n'est pas dans le dépôt | `md/questions/questions-a-trancher.md:180` |
| Jeff, Q-JEF-24 : saisie à la main permise ; choix du groupe Q8 : chasseur et manager | `md/questions/2026-10-07-questions-pour-jeff.html:1682` ; `md/questions/questions-a-trancher.md:252`, `:1175` |
| Options de Q8 | `md/journal/2026-10-07-plan-action.html:447-449` |
| Q-ACC-09 : « L'admin » (06/10/2026), pas l'option recommandée ; note conditionnelle sur Airflow | `questions-a-trancher.md:184` ; carte : `questions-a-trancher.html:1772-1805` |
| Lettre W | `questions-a-trancher.md:418` |
| ADR-027, question n° 8 : « Aucun rôle humain ne crée un bien » ; statut proposé | journal Confluence (copie du 07/10/2026), ADR-027 du 22/09/2026 : en-tête, et questions, n° 8 |
| F5 : clé vers `"user"`, sans contrôle du rôle ; trigger et clé vers `hunter` écartés ; choisi par Sébastien | `md/journal/2026-10-07-rapport-final-chantier-lot.html:550-562`, `:668` |
| La colonne et son commentaire | `docker/init-v3/01_create_fil_rouge_immobilier.sql:624-629` |
| `search_request.id_author` et `criteria.id_author`, `NOT NULL` | même fichier, l. 311, l. 395 |
| Référence d'un bien : unique, non vide | même fichier, l. 561-562 |
| Import : 2 556 biens, `id_author` vide | `docker/init-v3/03_populate_estate.sql:1-11` |
| Import joué à la création de la base, sous `POSTGRES_USER` | `docker/docker-compose.yml:8`, `:17` (lu, non modifié) |
| Migration v2 vers v3 | `docker/migrations/v2-vers-v3/09_biens.sql:12-15`, `:40-41` |
| Modèle de l'API | `API/src/app/models/estate_model.py:17-18`, `:81-82` |
| `POST` du routeur commun | `API/src/app/routes/crud_router.py:88-93` |
| Tests de la clé | `API/tests/integration/test_constraints_db.py:120-128` |
| Règles croisées contrôlées par l'API (Q-MAN-06) | `questions-a-trancher.md:155` |
| Désactiver plutôt que supprimer (Q-ACC-08) | `questions-a-trancher.md:183`, `:1037` |
| Matrice des droits : import seul, aucun rôle ne crée un bien | `md/securite/matrice-droits-crud-par-role.md:119-121`, `:169`, `:175`, `:237` |
| Code fait à LOT9 | commit `cd05768` |
| Micro-décisions hors ADR ; modèle d'ADR | `documents utiles/JOURNAL-DE-DECISIONS.md:13`, `:19-40` (StarterPack) |

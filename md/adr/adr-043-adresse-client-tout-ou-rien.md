# ADR-043 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 043 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:66`,
> lettre R). Il ne vaut rien tant que le groupe ne l'a pas pris sur Confluence.
>
> 💡 **Rédigé le 08/10/2026 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Les passages marqués « déduit » sont une lecture des sources, pas une
> décision du groupe.
>
> 🗂️ **Sur la page d'ADR-022 (Confluence)** : rien à barrer. Cette fiche le
> complète, elle ne le remplace pas. Une ligne « complété par ADR-043 » suffit,
> si le groupe le veut. L'Eircode de `client` est déjà réglé par ADR-031.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * `docker/init-v3/README.md:62` dit « Valeurs factices, à remplacer quand
>   Jeff fournit les vraies (Q-JEF-26) ». Jeff a répondu que les manques sont
>   voulus (Q-JEF-26) : la phrase est périmée.
> * Même chose dans le registre : « Jeff peut fournir les vrais codes »
>   (`md/questions/questions-a-trancher.md:178`).
> * La réponse Q-SCH-18 demande « une ligne dans le README du schéma, et dans
>   l'audit » (`questions-a-trancher.md:178`). Le README l'a. L'audit
>   (`livrables/1-audit/`) est vide : la ligne reste à écrire.
> * Le commentaire du test `API/tests/integration/test_constraints_db.py:135-136`
>   dit « une adresse inconnue s'écrit 'non renseigné' ». Il peut se lire comme
>   une règle pour tout nouveau client. La décision ci-dessous la réserve aux
>   données reprises : à reformuler.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-043 : Adresse client — tout ou rien, et « non renseigné » / `00000` pour les 18 clients repris

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions du groupe : 05/10/2026 et 06/10/2026 ; réponse de Jeff : 07/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * le groupe : Q-SCH-01 le 05/10/2026, Q-SCH-18 le 06/10/2026 ;
  * Jeff, client, entretien du 07/10/2026 : les manques des anciennes données sont voulus (Q-JEF-26).
* **Complète :** ADR-022 (qui reste « accepté ») : sa règle tient, cette fiche dit comment la reprise des anciennes données la respecte.

**Contexte**

ADR-022 (accepté, 10/09/2026) pose une règle sur l'adresse d'un client. `address`, `postal_code` et `town` sont vides ensemble, ou remplis ensemble. Jamais un profil partiel.

L'ancienne base du client n'a pas d'adresse. Sa table `utilisateurs` a une `ville`, sans adresse, sans code postal, sans pays (`fixtures/PgSQL.sql:62-72`, StarterPack).

Compté avant la migration : **18 clients sur 18** n'ont que la ville (`docker/init-v3/README.md:68`).

La règle d'ADR-022 les refusait. Le schéma v2 l'avait donc assouplie, par un `ALTER` marqué « À VALIDER PAR LE GROUPE » (`docker/init-v2/02_migration.sql:40-60`). Le groupe devait trancher.

**Options envisagées**

1. **Assouplir la règle** : une adresse exige un code postal et une ville, mais une ville seule passe. C'était l'`ALTER` de v2. Avantage : les 18 villes sont gardées. Inconvénient : des adresses incomplètes entrent en base. Option recommandée sur la carte. **Écartée** par le groupe (Q-SCH-01).
2. **Garder la règle et vider la ville.** Avantage : rien d'inventé. Inconvénient : « 18 villes perdues » (carte Q-SCH-01). **Écartée** : le groupe ne veut pas perdre les anciennes données (son commentaire, plus bas).
3. **Garder la règle, avec un code postal vide.** Inconvénient : « La règle tout-ou-rien n'est plus entière » (carte Q-SCH-18). **Écartée.**
4. **Mettre la ville dans l'adresse.** Inconvénient : « ça ressemblerait à une donnée réelle qui ne l'est pas » (`docker/init-v3/02_migration.sql:153-154`). **Écartée.**
5. **Garder la règle, avec une adresse `'non renseigné'` et un code postal `'00000'`, documentés.** Avantage : la règle reste entière, et la ville est gardée. Inconvénient : un faux code postal, à écarter des statistiques. **Retenue.**

💡 Une sixième piste n'a pas été soumise au groupe : le vrai code postal de la ville. Elle ne tient pas, déduit de la source : Montpellier y a trois codes (`34000`, `34090`, `34070`, `fixtures/PgSQL.sql:42-45`). Il faudrait en choisir un, donc inventer. Et un code plausible se lit comme une vraie donnée, comme l'option 4.

**Décision**

1. La règle d'ADR-022 reste entière. `ck_client_address_all_or_nothing` : les trois colonnes vides ensemble, ou remplies ensemble.
2. Les **18 clients repris** reçoivent `address = 'non renseigné'` et `postal_code = '00000'`. Leur ville et leur pays `'FR'` viennent de la source et sont gardés.
3. Ces deux valeurs sont **factices** et documentées. Elles ne servent qu'aux données reprises.
4. Un nouveau client donne ses trois champs d'adresse, ou aucun (ADR-022).

Le code, tel qu'il est aujourd'hui (`docker/init-v3/01_create_fil_rouge_immobilier.sql:225-229`) :

```sql
-- Tout-ou-rien gardé (Q-SCH-01) : les 18 clients repris sans adresse
-- reçoivent « non renseigné » et le code postal 00000 (Q-SCH-18, 02).
CONSTRAINT ck_client_address_all_or_nothing
    CHECK ((address IS NULL     AND postal_code IS NULL     AND town IS NULL)
        OR (address IS NOT NULL AND postal_code IS NOT NULL AND town IS NOT NULL)),
```

**Justification**

* **L'intégrité d'abord.** Le groupe, mot pour mot : « ajoutez un champ "non renseigné" pour les champs vides. car l'on veux pas perdre l'intégrité malgré l'import des ancienne données, (obligatoire de les migré) » (Q-SCH-01, 05/10/2026).
* **Ne rien supprimer.** Jeff : les manques sont voulus ; ne pas supprimer les anciennes données (Q-JEF-26, 07/10/2026). Vider la ville irait contre.
* **Une valeur factice se voit.** `'non renseigné'` ne peut pas passer pour une vraie adresse. `00000` ne correspond à aucun des codes de la source.
* **Même logique ailleurs.** Les téléphones manquants reçoivent `'+33000000000'`, documenté (Q-MIG-07 ; `02_migration.sql:49-50`). La règle générale de la reprise est celle du groupe : « vide (NULL) si la colonne l'accepte, sinon une valeur factice documentée » (Q4, `questions-a-trancher.md:240`). Ici, le vide n'est pas permis : la ville est remplie.
* **`00000` passe le format.** Les 18 clients ont le pays `'FR'`. Le format français demande 5 chiffres : `'^[0-9]{5}$'` (`01_…sql:235`).

**Conséquences**

* **Code : déjà fait** à LOT7 (`0e7134d`) :
  * le schéma garde la règle (`01_…sql:225-229`) ;
  * la reprise écrit les 18 clients (`docker/init-v3/02_migration.sql:155-172`, en-tête l. 43-48) ;
  * une base v2 existante passe par `docker/migrations/v2-vers-v3/07_personnes.sql:112-117`. ⚠️ Cette migration écrit les valeurs factices sur **tout** client de la base v2 qui a une ville sans adresse, pas seulement sur les 18 repris (l. 113-114).
* **Garde de la migration.** Elle s'arrête si un client à compléter n'a pas un pays où `00000` est valide : FR, ES, DE ou IT (`07_personnes.sql:62-65`). Le code factice ne vaut pas pour les 10 pays.
* **Tests.** Une ville seule est refusée (409). Une adresse sans ville aussi (`API/tests/integration/test_constraints_db.py:132-143`).
* **Statistiques.** Écarter `'non renseigné'` et `'00000'` de toute analyse sur les adresses. À dire en soutenance (carte Q-SCH-18) : une valeur factice se voit et se filtre ; une fausse adresse plausible, non.
* **Limite : la base ne réserve pas ces valeurs aux 18 clients.** Rien n'empêche un nouveau client d'écrire `'non renseigné'`. C'est à l'API de ne pas le proposer (voir « Questions tranchées », n° 2).
* **Limite d'ADR-022, inchangée :** `address_complement` reste libre, hors de la règle (journal Confluence, ADR-022, Conséquences).
* **Pays des clients repris.** `'FR'` pour les 18, déjà en v2 (`docker/init-v2/02_migration.sql:148`). La source n'a pas de pays.

**Questions tranchées par les sources**

1. **Faut-il attendre que Jeff fournisse les vraies adresses ?**
   Non. Jeff : « les manques sont voulus. Ne pas supprimer les anciennes données » (`md/questions/2026-10-07-questions-pour-jeff.html:1428`, Q-JEF-26). Les valeurs factices restent.
2. **Un nouveau client peut-il recevoir `'non renseigné'` ?**
   Non, déduit de trois sources :
   * ADR-022 : un client « peut toujours n'avoir renseigné aucune adresse » (ADR-022, Justification), et le formulaire soumet les trois champs « ensemble ou aucun des trois » (ADR-022, Conséquences) ;
   * le titre de la lettre R : « « non renseigné » pour les données reprises » (`questions-a-trancher.md:413`) ;
   * le commentaire du groupe vise « l'import des ancienne données » (Q-SCH-01).
   Un nouveau client sans adresse a donc les trois colonnes vides.
3. **Le format irlandais (Eircode) de `client` change-t-il ici ?**
   Non : ADR-031 l'a déjà amendé.

**Questions ouvertes** 🟡

Aucune. Les deux réponses du groupe et celle de Jeff suffisent ; le code est fait.

**Sources**

| Affirmation | Source |
|---|---|
| ADR-022 : tout ou rien retenu, contre « aucune contrainte » et l'implication | journal Confluence (copie du 07/10/2026), ADR-022 : Statut, Options |
| ADR-022 : aucune adresse permise ; le formulaire envoie les trois ou aucun | même copie, ADR-022 : Justification, Conséquences |
| ADR-022 : `address_complement` hors de la règle | même copie, ADR-022, Conséquences |
| La source n'a qu'une ville, sans adresse ni code postal | `fixtures/PgSQL.sql:62-72` (StarterPack) |
| 18 clients sur 18 avec la ville seule | `docker/init-v3/README.md:68` |
| L'`ALTER` de v2, « À VALIDER PAR LE GROUPE » | `docker/init-v2/02_migration.sql:40-60` |
| Q-SCH-01 : « Garder le tout-ou-rien » (05/10/2026), pas l'option recommandée, et son commentaire | `md/questions/questions-a-trancher.md:157` ; options : `questions-a-trancher.html:1116-1117` |
| Q-SCH-18 : « Un code factice 00000, documenté » (06/10/2026) | `questions-a-trancher.md:178` ; options : `questions-a-trancher.html:1438-1439` |
| Jeff, Q-JEF-26 : manques voulus, ne pas supprimer | `md/questions/2026-10-07-questions-pour-jeff.html:1428` ; `questions-a-trancher.md:1176` |
| Q4 du groupe : vide si permis, sinon valeur factice documentée ; Q-SCH-01 et Q-SCH-18 inchangées | `questions-a-trancher.md:240` |
| Lettre R : « non renseigné » pour les données reprises | `questions-a-trancher.md:413` |
| Le CHECK et son commentaire | `docker/init-v3/01_create_fil_rouge_immobilier.sql:225-229` |
| Format français : 5 chiffres | même fichier, l. 233-235 |
| La ville dans l'adresse serait trompeuse | `docker/init-v3/02_migration.sql:151-154` |
| Les 18 `INSERT`, pays `'FR'` | même fichier, l. 155-172 ; en-tête l. 43-48 |
| Téléphones factices `'+33000000000'` | même fichier, l. 49-50 |
| Montpellier : trois codes postaux dans la source | `fixtures/PgSQL.sql:42-45` (StarterPack) |
| Migration v2 vers v3 : garde et mise à jour (tout client avec une ville sans adresse) | `docker/migrations/v2-vers-v3/07_personnes.sql:62-65`, `:112-117` |
| Tests de la règle | `API/tests/integration/test_constraints_db.py:132-143` |
| Code fait à LOT7 | commit `0e7134d` |
| Modèle d'ADR | `documents utiles/JOURNAL-DE-DECISIONS.md:19-40` (StarterPack) |

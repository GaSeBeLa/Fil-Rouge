# ADR-031 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 031 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:42`,
> lettre N, avec l'Eircode). Il ne vaut rien tant que le groupe ne l'a pas pris
> sur Confluence.
>
> 💡 **Rédigé le 08/10/2026 par Claude, d'après les fichiers du dépôt.** Relu le
> 08/10/2026 par deux relecteurs (sources ; oral et jury) et un arbitre. Les
> passages marqués « déduit » sont une lecture des sources, pas une décision du
> groupe.
>
> 🗂️ **Deux points réglés hors de la fiche** (ils parlent des pages Confluence
> et des notes) :
>
> * **Sur la page d'ADR-009 : « modifié le …, par l'ADR xx », ou « remplacé
>   par » ?** « Remplacé par ADR-031 ». Le modèle du sujet ne connaît que
>   « proposé / accepté / remplacé par ADR-YYY » (`JOURNAL-DE-DECISIONS.md:22`,
>   `:72`). La ligne demandée par le groupe (Q-SCH-02,
>   `questions-a-trancher.md:158`) s'écrit donc ainsi.
> * **ADR-022 (table `client`)** : cette fiche l'amende (Questions tranchées,
>   n° 1). Cela règle la question ouverte n° 3 des notes du jour
>   (`md/adr/2026-10-08-notes-seance-adr.md:65`) : pas besoin d'une phrase dans
>   un autre ADR, ni d'un ADR à part.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-031 : La localisation d'une recherche vit sur `criteria`, avec un quartier facultatif, et l'Eircode s'écrit sans espace

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions du groupe : 05/10/2026 et 06/10/2026 ; Eircode confirmé le 07/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * le groupe : Q-SCH-02 et Q-SCH-12 le 05/10/2026, Q-MIG-08 le 06/10/2026 ;
  * confirmation de l'Eircode le 07/10/2026 : **auteur non noté**. Le registre dit « Confirmée par Jeff » (`questions-a-trancher.md:167`) et le README du schéma aussi (`docker/init-v3/README.md:73`) ; le même registre la range côté groupe (`:255`). La carte ne nomme personne, et le rapport d'entretien de Jeff n'a aucune carte sur l'Eircode.
* **Remplace :** ADR-009 (caractère optionnel du secteur, `id_area` NULLABLE)
* **Amende :** ADR-021 (format de l'Eircode, colonne quartier) et ADR-022 (format de l'Eircode, par déduction : voir « Questions tranchées »)

**Contexte**

ADR-009 (accepté, 19/08/2026) range la localisation sur `SearchRequest`. Il passe par deux clés étrangères : `id_town` pour la ville, `id_area` pour le quartier. Il rend `id_area` facultatif, car certaines villes n'ont pas de quartier.

ADR-021 (accepté, 10/09/2026) met la ville, le code postal et le pays sur `Criteria`, en texte. Il écrit lui-même qu'il « ne tranche pas laquelle des deux approches remplace l'autre ». C'est la décision ouverte N2 (`livrables/2-modelisation/09-decisions-a-prendre.md:233-251`).

Le schéma réel a déjà choisi. `search_request` n'a aucune colonne de lieu. Il n'existe ni `id_town`, ni `id_area`, ni table des villes ou des quartiers. Le lieu est sur `criteria` seule : `country_iso`, `town`, `postal_code`, `district`.

L'ancienne base du client a 10 secteurs : ville, quartier, code postal. Deux n'ont pas de quartier : Castelnau-le-Lez et Lattes. Avant le lot de migration, ces secteurs n'étaient pas repris : `criteria.town` était vide 17 fois sur 17.

Enfin, l'Eircode (code postal irlandais) était décrit de deux façons. ADR-021, ADR-022 et le schéma v2 l'écrivent avec un espace (`D02 X285`). Le diagramme MPD, lui, l'exigeait avec un espace sur `client` et l'interdisait sur `criteria` (correction 8 de l'en-tête du schéma). Le même pays avait donc deux formats incompatibles.

**Options envisagées**

Sujet 1 — où ranger le lieu d'une recherche :

1. **Sur `search_request`, par clés vers des tables ville et quartier** (ADR-009). Avantage : une ville s'écrit une seule fois, comme le conseille la fiche OLTP du sujet. Inconvénients : ces tables n'existent pas, il faudrait un référentiel à remplir ; et le lieu ne suivrait pas les versions des critères. **Écartée.**
2. **Sur `criteria`, par une clé vers une table des secteurs** (ville, quartier, code postal), comme la table `secteurs` de l'ancienne base. Avantages : le lieu suit les versions ; une ville s'écrit une seule fois, comme le conseille la fiche OLTP du sujet (`OLTP.md:21`). Inconvénient : un référentiel de villes à construire et à tenir pour les 10 pays couverts (ADR-020), pour 10 secteurs repris. **Écartée.** C'est un écart à la fiche OLTP du sujet, assumé.
3. **Sur `criteria`, en texte, avec le pays** (ADR-021, MPD). Avantage : le lieu change avec la recherche, chaque version garde le sien. Inconvénient : une même ville peut s'écrire de deux façons. **Retenue.**
4. **Les deux** (sur `search_request` et sur `criteria`). Inconvénient : deux sources pour un même fait, qui peuvent se contredire. **Écartée.**

Sujet 2 — le quartier :

1. **Pas de quartier.** Inconvénient : 8 secteurs sur 10 en ont un ; il serait perdu à la migration. **Écartée.**
2. **Une colonne `district`, facultative, sur `criteria` et `estate`.** **Retenue.**
3. **Une colonne obligatoire.** Inconvénient : 2 secteurs sur 10 n'ont pas de quartier. Il faudrait des quartiers inventés, ce qu'ADR-009 refusait déjà. **Écartée.**

Sujet 3 — l'Eircode :

1. **Avec espace** (`D02 X285`), comme ADR-021 et ADR-022. Avantage : c'est le format affiché habituel. **Écartée** par le groupe.
2. **Sans espace** (`D02X285`). Avantage : une seule écriture, plus simple à comparer. Inconvénient : le Royaume-Uni et les Pays-Bas gardent leur espace, donc deux conventions dans la même colonne. **Retenue.**

**Décision**

1. Le lieu d'une recherche est **sur `criteria` seule** : `country_iso`, `town`, `postal_code`, `district`. Rien sur `search_request`. Aucune table de villes ni de quartiers.
2. **`district`** (le quartier) : `VARCHAR(100)`, **facultatif**, sur `criteria` et sur `estate`. Non vide et sans espace en bord. Sur `criteria`, un quartier exige une ville (`chk_criteria_district_needs_town`).
3. **L'Eircode s'écrit sans espace**, sur les trois tables `client`, `criteria` et `estate`. Le Royaume-Uni et les Pays-Bas ne changent pas.
4. Le reste d'ADR-021 tient : une ville ou un code postal exige un pays ; le format du code postal dépend du pays.

Le code, tel qu'il est aujourd'hui (`docker/init-v3/01_create_fil_rouge_immobilier.sql`) :

```sql
-- criteria (l. 339-340, 416-417, 428) ; estate (l. 621-622, 640) ; client (l. 240)
district  VARCHAR(100) CHECK (district = btrim(district) AND district <> ''),

CONSTRAINT chk_criteria_district_needs_town
    CHECK (district IS NULL OR town IS NOT NULL),

WHEN country_iso = 'IE' THEN postal_code ~ '^([AC-FHKNPRTV-Y][0-9]{2}|D6W)[0-9AC-FHKNPRTV-Y]{4}$'
```

**Justification**

* **Le lieu change avec la recherche.** Le sujet le dit : « cette demande évolue au fil du mandat », par exemple « le secteur s'élargit » (`MCD-MERISE.md:87`). Le glossaire range le secteur parmi les critères (`GLOSSAIRE-METIER.md:17`). Or `criteria` est versionnée : chaque version pointe vers la précédente. Sur `search_request`, un secteur élargi effacerait l'ancien.
* **Pas de table des secteurs** : pour 10 secteurs repris, un référentiel de villes sur 10 pays coûterait plus qu'il ne rapporte. Le prix : une ville peut s'écrire de deux façons (option 3, inconvénient accepté).
* **Le quartier est facultatif pour la même raison qu'ADR-009.** Certaines villes n'en ont pas. Dans la source, Castelnau-le-Lez et Lattes n'en ont pas. Cette idée d'ADR-009 est gardée ; seul son moyen (une clé vers une table `Area`) disparaît.
* **L'Eircode sans espace** donne une seule écriture, donc des comparaisons simples. Les deux formes sont officielles d'après le site Eircode (lu le 05/10/2026, carte Q-SCH-12). Aucune adresse irlandaise n'existe dans les données : le changement ne coûte rien.

**Conséquences**

* **ADR-009** passe en « remplacé par ADR-031 » sur Confluence (`JOURNAL-DE-DECISIONS.md:72`). Son texte ne change pas. C'est la ligne demandée par le groupe (Q-SCH-02).
* **ADR-021** reste accepté. Il change sur trois points : le format irlandais, la colonne `district` et sa contrainte, et sa « cohérence à vérifier » (N2), désormais close.
* **Noms des contraintes :** ADR-021 les nomme `ck_criteria_…`. Le code les nomme `chk_town_requires_country`, `chk_postal_code_needs_country`, `chk_postal_code_format`. Les noms du code font foi.
* **ADR-022** reste accepté. Seul le format irlandais change.
* **Code : déjà fait.** LOT8 (`578dfb6`, migration `docker/migrations/v2-vers-v3/08_localisation.sql`) ; la règle « un quartier exige une ville » (`8024210`, migration 13). La migration 08 retire l'espace d'un Eircode existant.
* **Tests :** un Eircode avec espace est refusé (409) sur `/estates`, `/clients` et `/criteria` ; sans espace, il est accepté (201). Un quartier sans ville est refusé (`API/tests/integration/test_constraints_db.py:210-255`).
* **Données :** les **18** critères repris reçoivent la ville, le code postal et le pays `'FR'` du secteur de leur mandat (`docker/init-v3/02_migration.sql:207`, `INSERT` l. 208-224 et 228). 3 n'ont pas de quartier (Castelnau-le-Lez deux fois, Lattes). Les 2 556 biens n'ont pas de quartier : le CSV n'en a pas (`docker/init-v3/README.md:75`).
* **MPD v8 (08/10/2026) :** il porte `district` sur `Criteria` et `Estate`, et les trois formats irlandais sans espace. L'ancienne colonne `area` de `Estate` y est devenue `district`.
* **API, écart à combler :** l'API ne retire pas l'espace aujourd'hui. `D02 X285` est refusé par la base. ADR-021 demande que l'API formate le code avant d'écrire (voir « Questions tranchées », n° 3).
* **Limite assumée :** deux conventions dans la même colonne. `D02X285` pour l'Irlande, `1234 AB` pour les Pays-Bas, `SW1A 1AA` pour le Royaume-Uni. La carte Q-SCH-12 ne visait que l'Irlande : le Royaume-Uni et les Pays-Bas n'ont pas été rouverts (`questions-a-trancher.html:1297`, `:1309` ; `docker/init-v3/README.md:73`).
* **Dette connue :** le même `CASE` de format est écrit trois fois (`client`, `criteria`, `estate`). Changer le format d'un pays touche trois tables et demande une migration. ADR-022 acceptait déjà cette redondance.
* **Rapprochement des biens** (pas encore codé) : un quartier vide ne filtre rien ; on cherche alors sur la ville. Déduit de la conséquence d'ADR-009 sur `id_area`.

**Questions tranchées par les sources**

1. **L'ADR-031 amende-t-il aussi ADR-022 (table `client`) ?**
   Oui, déduit de trois sources.
   * Le code l'a déjà fait : le format irlandais de `client` est sans espace (`01_…sql:232-240`), la migration 08 retire l'espace sur `client`, et un test le vérifie sur `/clients`.
   * La décision visait les deux tables dès le 05/10 : « Eircode sans espace, sur `client` et `criteria` » (`md/questions/questions-a-trancher.md:372`).
   * ADR-022 le demande lui-même : « toute évolution du barème par pays (nouveau pays, format Eircode révisé…) doit être répercutée sur les deux tables » (journal Confluence, ADR-022, Conséquences).
2. **Faut-il aussi « un quartier exige une ville » sur `estate` ?**
   Non, déduit : `estate.town` est `NOT NULL` (`01_…sql:611`). Un bien a toujours une ville.
3. **L'API doit-elle retirer l'espace d'un Eircode avant d'écrire ?**
   Oui, déduit. ADR-021 reste en vigueur sur ce point : l'API doit « formater NL/GB/IE selon leur regex » avant insertion. La regex irlandaise étant sans espace, formater veut dire retirer l'espace. La carte Q-SCH-12 le disait déjà : « l'API retire l'espace avant d'écrire » (`md/questions/questions-a-trancher.html:1308`).
   Ce n'est pas fait : aucune normalisation dans `API/src/`, et le test attend un refus. Le test changera avec le code.

**Questions ouvertes** 🟡

Aucune. Les trois sujets sont tranchés par le groupe et déjà dans le code.

**Sources**

| Affirmation | Source |
|---|---|
| ADR-009 : clés `id_town` / `id_area` sur `SearchRequest`, `id_area` NULLABLE, accepté | journal Confluence (copie du 07/10/2026), ADR-009 |
| ADR-020 : 10 pays couverts | même copie, ADR-020 ; `docker/init-v3/01_create_fil_rouge_immobilier.sql:202` |
| ADR-021 ne tranche pas entre les deux approches | même copie, ADR-021, Conséquences |
| ADR-021 et ADR-022 écrivent l'Eircode avec un espace | même copie, ADR-021 et ADR-022, Décision |
| ADR-022 : un format Eircode révisé se reporte sur les deux tables | même copie, ADR-022, Conséquences |
| ADR-021 : l'API formate NL/GB/IE avant insertion | même copie, ADR-021, Conséquences |
| Conflit N2, ses trois options | `livrables/2-modelisation/09-decisions-a-prendre.md:233-251` |
| Q-SCH-02 : garder `criteria`, un ADR remplace ADR-009 ; la ligne sur ADR-009 | `md/questions/questions-a-trancher.md:158` |
| Q-MIG-08 : « ajoute dans criteraia, sector nullable , idem dans estate » (06/10/2026) | même registre, l. 181 |
| Q-SCH-12 : sans espace (05/10/2026), pas l'option recommandée ; qui tranche : le groupe | même registre, l. 167 ; `questions-a-trancher.html:1297-1316` |
| Confirmation de l'Eircode le 07/10/2026 : « par Jeff » (registre l. 167, README l. 73), « 👥 » groupe (registre l. 255) ; la carte ne nomme personne | `questions-a-trancher.md:167`, `:255` ; `docker/init-v3/README.md:73` ; `questions-a-trancher.html:1312` |
| Le rapport d'entretien de Jeff n'a aucune carte sur l'Eircode | `md/questions/2026-10-07-questions-pour-jeff.html` : 0 occurrence de « eircode » et « irland » ; « postal » 3 fois, toutes sur le code postal français des clients repris (carte Q-JEF-26, l. 1421-1426) |
| « Au lot, sans réserve » : la confirmation s'applique au lot | `questions-a-trancher.md:255` |
| La carte ne vise que l'Irlande ; GB et NL gardent leur espace | `questions-a-trancher.html:1297`, `:1309` ; `docker/init-v3/README.md:73` |
| Les deux formes d'Eircode sont officielles ; aucune adresse irlandaise | `questions-a-trancher.html:1310` (carte, doc eircode.ie lue le 05/10/2026) |
| Pas de lieu sur `search_request` | `docker/init-v3/01_create_fil_rouge_immobilier.sql:308-322` |
| Lieu sur `criteria`, `district`, contraintes | même fichier, l. 331-340, l. 414-429 |
| `criteria` versionnée | même fichier, l. 324, l. 399-400 |
| `district` sur `estate` ; `estate.town` NOT NULL | même fichier, l. 611-612, l. 619-622 |
| Eircode avec espace dans le schéma v2, sur `client` et `criteria` | `docker/init-v2/01_create_fil_rouge_immobilier.sql:215`, `:391` |
| MPD : espace exigé sur `client`, interdit sur `criteria` (correction 8) | `docker/init-v3/01_create_fil_rouge_immobilier.sql:40-41`, `:57-61` |
| Eircode sans espace sur les trois tables, GB et NL inchangés | même fichier, l. 232-240, l. 420-428, l. 631-641 |
| Les 10 secteurs, 2 sans quartier | `fixtures/PgSQL.sql:34-51`, l. 46-47 (StarterPack) |
| Secteurs non repris avant LOT8 : `town` vide 17 fois sur 17 | `questions-a-trancher.md:988` |
| Le secteur fait partie des critères et évolue | `GLOSSAIRE-METIER.md:17`, `MCD-MERISE.md:87` (StarterPack) |
| Normaliser dans une table `secteurs` | `OLTP.md:21` (StarterPack, fiche de cours) |
| Données reprises : 18 critères, 3 sans quartier | `docker/init-v3/02_migration.sql:202-228` (le « 17 » de `README.md:74` date d'avant la reprise de la demande 13, LOT10) |
| 2 556 biens sans quartier | `docker/init-v3/README.md:75` |
| Code et migrations | commits `578dfb6` (LOT8), `8024210`, `6fc494f` (migration 13) ; `docker/migrations/v2-vers-v3/08_localisation.sql` |
| Tests Eircode et quartier | `API/tests/integration/test_constraints_db.py:210-255` |
| Aucune normalisation du code postal dans l'API | recherche du 08/10/2026 dans `API/src/` (`postal_code`, `replace`, `upper`) : seuls les champs des modèles |
| MPD v8 : `district` ×2, Eircode sans espace ×3, plus de `area` | MPD v8 du 08/10/2026 (fichier `v8.drawio.xml` reçu sur Discord, hors dépôt), lu le 08/10/2026 |
| Modèle d'ADR, « remplacé par » | `documents utiles/JOURNAL-DE-DECISIONS.md:22`, `:72` (StarterPack) |

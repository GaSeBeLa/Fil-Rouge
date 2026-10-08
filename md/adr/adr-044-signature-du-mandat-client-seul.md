# ADR-044 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 044 est une proposition** (`md/adr/2026-10-08-proposition-regroupement-adr.md:67`,
> lettre S). Il ne vaut rien tant que le groupe ne l'a pas pris sur Confluence.
>
> 💡 **Rédigé le 08/10/2026 par Claude, d'après les fichiers du dépôt et le
> sujet.** Relu le 08/10/2026 par deux relecteurs (sources ; oral et jury) et un
> arbitre. Les passages marqués « déduit » sont une lecture des sources, pas une
> décision du groupe.
>
> 🗂️ **Sur la page d'ADR-003 (Confluence)** : rien à barrer. Cette fiche le
> complète : l'attribut `Signature` d'ADR-003 existe, sous le nom
> `signature_date`. Une ligne « complété par ADR-044 » suffit, si le groupe le
> veut.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * `md/securite/matrice-droits-crud-par-role.md:162` cite encore la colonne
>   `mandate.is_client_signed`, retirée.
> * Le registre cite `02:218` et `02:225` pour `MAND-0008` et `MAND-0016`
>   (`md/questions/questions-a-trancher.md:175`). Ils sont aujourd'hui aux
>   lignes 245 et 253 de `docker/init-v3/02_migration.sql`.
> * `docker/init-v3/README.md:31` dit « les 17 mandats de `02` ». Le fichier en
>   compte 18 aujourd'hui (`02_migration.sql:238-255`).
> * Aucun test ne vérifie qu'un mandat `'pending_signature'` avec une date est
>   refusé. Les tests couvrent `'canceled'` et `'active'` sans date
>   (`API/tests/integration/test_constraints_db.py:286-297`).
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-044 : Signature du mandat — le client seul ; la date de signature est la seule trace

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décisions du groupe : 06/10/2026)
* **Statut :** proposé
* **Décideurs :** le groupe, Q-MAN-05 et Q-MAN-09, le 06/10/2026
* **Complète :** ADR-003 « Choix Signature du contrat » (qui reste « accepté »)
* **S'appuie sur :** ADR-039 (un mandat annulé peut n'avoir jamais été signé) et ADR-050 (un renouvellement est un nouveau mandat, donc une nouvelle signature)

**Contexte**

ADR-003 (accepté, 04/08/2026) constate que la date de signature du mandat n'est pas stockée (anomalie C8). Il crée un attribut `Signature`. But : savoir si un mandat est signé, garder un historique, relancer un client qui tarde.

Le schéma en a ensuite porté deux traces : une date `signature_date`, et une case `is_client_signed`, oui ou non. Rien ne les reliait. Deux mandats repris le montraient : `MAND-0008` et `MAND-0016` avaient une date de signature et la case à non (carte Q-MAN-05).

Le 05/10/2026, le groupe a d'abord voté un CHECK d'égalité entre les deux. Il a aussi demandé si le chasseur devait signer. Un mandat est un contrat à deux. Mais le sujet ne parle que de la signature du client (`Readme.md:98` ; `01_particulier_demande_et_compte.feature:35-37`). D'où la question Q-MAN-09.

**Options envisagées**

1. **Deux dates, une par partie** (`client_signed_on`, `hunter_signed_on`). Avantage : on sait qui a signé et quand. Inconvénient : deux colonnes de plus, et un ajout au sujet à justifier. Option recommandée sur la carte. **Écartée** par le groupe.
2. **Deux cases oui/non** (`is_client_signed`, `is_hunter_signed`). Inconvénient : une case ne dit pas quand. **Écartée.**
3. **Le client seul, en gardant la case**, reliée à la date par un CHECK d'égalité. C'était la réponse du 05/10/2026. Inconvénient : deux colonnes pour un seul fait. **Écartée** : le commentaire du 06/10/2026 la remplace.
4. **Le client seul, sans case** : la date et le statut `'pending_signature'` suffisent. **Retenue.**

**Décision**

1. Seule la signature du **client** est enregistrée, comme dans le sujet.
2. `mandate.signature_date` en est la **seule trace**. La colonne `is_client_signed` est retirée.
3. Le statut `'pending_signature'` va avec une date vide, et seulement avec elle. Un mandat `'canceled'` peut avoir une date ou non (`chk_status_signature`, `01:474-478` ; ADR-039). Tous les autres statuts exigent une date.
4. `signature_type` (`'electronic'` ou `'paper'`) dit comment le client a signé. Il ne prouve pas la signature.

Le code, tel qu'il est aujourd'hui (`docker/init-v3/01_create_fil_rouge_immobilier.sql:450-453`, `:474-478`) :

```sql
-- Seule trace de la signature du client : is_client_signed est retiré,
-- la date et le statut 'pending_signature' suffisent (Q-MAN-05, Q-MAN-09).
signature_date    DATE,
signature_type    VARCHAR(20) CHECK (signature_type IN ('electronic', 'paper')),

CONSTRAINT chk_status_signature
    CHECK ((status = 'pending_signature' AND signature_date IS NULL)
        OR  status = 'canceled'
        OR (status NOT IN ('pending_signature', 'canceled')
            AND signature_date IS NOT NULL)),
```

**Justification**

* **Le sujet ne garde qu'une date.** Son modèle n'a qu'une colonne `date date_signature` (`MCD-MERISE.md:61`, `OLTP.md:41`). La user story enregistre le mandat « avec sa date de signature » (`01_…feature:36`).
* **Une seule date sert partout.** Elle fixe la fin du mandat, `date_fin = date_signature + 6 mois` (`REGLES-CALCUL-REMUNERATION.md:98`). Elle ouvre le critère S₁, délai entre la signature et l'acte (`:143`, `:149`). Elle compte les « mandats signés » du critère S₄ (`:146`).
* **Deux traces d'un même fait finissent par se contredire.** `MAND-0008` et `MAND-0016` le montraient (carte Q-MAN-05).
* **Le groupe, mot pour mot :** « retirer is_client_signed, par juste la date de signature, on passe par le status pending signature » (Q-MAN-09, 06/10/2026).
* **L'accord du chasseur a déjà sa trace**, déduit du schéma : il peut ne pas accepter une demande (`Readme.md:124`), et la demande a les statuts `'accepted'` et `'rejected'` (`01_…sql:320-321`).
* **Aucun calcul du sujet ne lit une signature du chasseur.** Le calcul de la rémunération ne prend que `date_signature_mandat` (`REGLES-CALCUL-REMUNERATION.md:460-466`).

**Conséquences**

* **Code : déjà fait** à LOT3 (`04b2bb3`) :
  * le schéma (`01_…sql:450-453`, `:474-478`) ;
  * la migration d'une base v2 retire la colonne (`docker/migrations/v2-vers-v3/03_mandat-statuts.sql:45`, `:48-53`) ;
  * le modèle de l'API (`API/src/app/models/mandate_model.py:22-25`) ;
  * le README du schéma (`docker/init-v3/README.md:31`).
* **Données reprises.** Les 18 mandats repris ont tous une date de signature, aucun n'est `'pending_signature'` (`02_migration.sql:238-255`). `MAND-0008` et `MAND-0016` sont annulés et gardent leur date : elle vient de la source (`date_debut`, `fixtures/PgSQL.sql:130`).
* **`signature_type` reste facultatif.** Aucun CHECK ne le lie à la date. Les mandats repris n'en ont pas : la source n'a « NI mode de signature » (`fixtures/PgSQL.sql:113-114`).
* **ADR-003 tient.** Savoir si un mandat est signé : la date ou le statut. Relancer un client : un mandat `'pending_signature'` et sa date de création `created_at` (`01_…sql:439`). L'historique en cas de renouvellement : chaque renouvellement est un nouveau mandat, avec sa propre date (ADR-050).
* **À coder dans l'API :**
  * passer la demande à `'launched'` quand le client signe. Déduit de la user story : « ma recherche est officiellement lancée » (`01_…feature:37`), et de D4 : « lancée » (U21 — à la signature du mandat) (`livrables/2-modelisation/09-decisions-a-prendre.md:346`). Pas codé : `launched` n'apparaît dans `API/src/` qu'en commentaire ;
  * refuser une visite avant la signature, et une vente sur un mandat non signé. Ce sont deux TODO du schéma, à contrôler dans l'API (Q-MAN-06 ; `01_…sql:721-725`, `:774-780`).
* **Le trigger d'exclusivité** ignore un mandat sans date de signature (`01_…sql:525-527`). Un mandat en attente ne bloque donc pas le client.
* **Limite assumée.** Dans la réalité, un mandat est signé par les deux parties. Le sujet le dit aussi : le prospect « signe alors avec le chasseur un mandat de recherche » (`Readme.md:73`). Le schéma ne garde que la signature du client. À dire en soutenance (carte Q-MAN-05). 💡 Au jury : « Le chasseur est partie au mandat, mais aucun calcul du sujet ne lit sa signature. Nous gardons la seule date que le calcul utilise : celle du mandat, signée par le client. »

**Questions tranchées par les sources**

1. **ADR-003 est-il remplacé ?**
   Non, complété. Déduit : sa décision est un attribut de signature, et `signature_date` l'est. Ses trois buts sont tenus (voir Conséquences). Rien de ce qu'il décide n'est défait.
2. **Faut-il encore le CHECK d'égalité voté le 05/10/2026 ?**
   Non : sans case, il n'a plus d'objet. « Le commentaire fait foi : pas de CHECK d'égalité » (`questions-a-trancher.md:177`).
3. **Faut-il corriger la date de `MAND-0008` et `MAND-0016` ?**
   Non. Ils « gardent leur date, reprise de la source » (`questions-a-trancher.md:175`). Un mandat annulé peut garder sa date : `chk_status_signature` accepte `'canceled'` avec ou sans date (`01:474-478`).

**Questions ouvertes** 🟡

Aucune. Le groupe a tranché les deux questions ; le schéma est fait.

**Sources**

| Affirmation | Source |
|---|---|
| ADR-003 : date non stockée (C8), attribut `Signature`, relance, accepté le 04/08/2026 | journal Confluence (copie du 07/10/2026), ADR-003 |
| Q-MAN-05 : « Supprimer la colonne » (06/10/2026), remplace « Poser un CHECK d'égalité » (05/10/2026), et son commentaire | `md/questions/questions-a-trancher.md:175`, `:154` ; carte : `:843-854` |
| Q-MAN-09 : « Le client seul, comme le sujet » (06/10/2026), le commentaire fait foi | `questions-a-trancher.md:177` ; options : `:899-912` |
| Un mandat est un contrat à deux ; le sujet ne parle que du client | `questions-a-trancher.md:851-852` |
| Lettre S : le client seul, la date et `pending_signature` suffisent | `questions-a-trancher.md:414` |
| Le client signe le mandat ; il « signe alors avec le chasseur » | `Readme.md:73`, `:98`, `:126` ; `user-stories/01_particulier_demande_et_compte.feature:35-37` (StarterPack) |
| Une seule colonne `date_signature` dans le modèle du sujet | `documents utiles/MCD-MERISE.md:61`, `documents utiles/OLTP.md:41` (StarterPack) |
| Fin = signature + 6 mois ; critères S₁ et S₄ ; le calcul ne lit que `date_signature_mandat` | `documents utiles/REGLES-CALCUL-REMUNERATION.md:98`, `:143`, `:146`, `:149`, `:460-466` (StarterPack) |
| Le chasseur peut ne pas accepter une demande | `Readme.md:124` (StarterPack) |
| La source n'a ni date ni mode de signature ; `date_debut` | `fixtures/PgSQL.sql:113-114`, `:130` (StarterPack) |
| D4 : « lancée » à la signature du mandat | `livrables/2-modelisation/09-decisions-a-prendre.md:337-346` |
| Statuts du mandat, colonnes et `chk_status_signature` | `docker/init-v3/01_create_fil_rouge_immobilier.sql:446-453`, `:474-478` |
| Statuts de la demande | même fichier, l. 320-321 |
| `created_at` sur `mandate` | même fichier, l. 439 |
| Trigger d'exclusivité : un mandat sans date est ignoré | même fichier, l. 525-527 |
| TODO visite et vente, contrôlés par l'API (Q-MAN-06) | même fichier, l. 721-725, l. 774-780 ; `questions-a-trancher.md:155` |
| 18 mandats repris, tous datés ; `MAND-0008` et `MAND-0016` annulés | `docker/init-v3/02_migration.sql:238-255`, l. 245, l. 253 |
| Migration v2 vers v3 : colonne retirée, CHECK posé | `docker/migrations/v2-vers-v3/03_mandat-statuts.sql:45`, `:48-53` |
| Modèle de l'API | `API/src/app/models/mandate_model.py:22-25` |
| `launched` absent du code de l'API | recherche du 08/10/2026 dans `API/src/` : une seule occurrence, en commentaire (`search_request_model.py:27`) |
| Tests : annulé sans date accepté, actif sans date refusé | `API/tests/integration/test_constraints_db.py:286-297` |
| Code fait à LOT3 | commit `04b2bb3` |
| Modèle d'ADR | `documents utiles/JOURNAL-DE-DECISIONS.md:19-40` (StarterPack) |

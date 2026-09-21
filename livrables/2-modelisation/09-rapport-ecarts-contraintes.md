# Rapport — écarts entre le MPD et les règles métier

> **Pour qui ?** Toute l'équipe du fil rouge. Pas besoin d'avoir suivi
> l'analyse : lisez « L'essentiel », puis « Ce qu'il faut faire ». Les tableaux
> détaillés, plus bas, servent de référence quand vous traitez une table.
>
> **Date** : 2026-09-11.

## Sommaire

1. [L'essentiel](#lessentiel)
2. [Ce qu'il faut faire](#ce-quil-faut-faire) — quatre étapes, dans l'ordre
3. [Comment lire les tableaux](#comment-lire-les-tableaux)
4. [Petit lexique](#petit-lexique)
5. [Les codes des règles](#les-codes-des-règles)
6. [Détail — Personnes et biens](#détail--personnes-et-biens) (12 tables)
7. [Détail — Mandat et rémunération](#détail--mandat-et-rémunération) (6 tables)

---

## L'essentiel

On a comparé **deux choses** :

- **le MPD** (modèle physique de données) : le schéma de nos 18 tables, avec
  leurs colonnes, leurs types et leurs contraintes. C'est le fichier draw.io
  `MPD 4 MEURISE`, qui **n'est pas dans le dépôt git** ;
- **les règles métier** : ce que le service de chasse immobilière exige. Elles
  sont écrites dans les user stories (`user-stories/*.feature`) et dans les
  notes à la racine du dépôt.

Pour chaque règle, on s'est posé une question : **le MPD la fait-il
respecter ?**

| verdict | nombre | ce que ça veut dire |
|---|---|---|
| couverte | 84 | le MPD fait déjà respecter la règle |
| partielle | 49 | le MPD en fait une partie seulement |
| absente | 16 | rien dans le MPD |
| fausse | 1 | une contrainte existe, mais elle ne marche pas |
| **total** | **150** | une règle qui touche deux tables compte deux fois |

- Par partie : Personnes et biens 22 / 5 / 14 / 1 ; Mandat et rémunération
  62 / 44 / 2 / 0 (couverte / partielle / absente / fausse).
- 135 règles relevées en tout : 51 dans les user stories, 84 dans les notes.
  133 apparaissent dans les tableaux. Les 2 autres (`U29`, `F04`) parlent du
  **rendez-vous**, et aucune des 18 tables ne le porte.

**Les trois problèmes qui coûteraient le plus cher :**

1. **L'unité de H n'est pas fixée** (`X02`, `T14`, `R14` à `R18`). Une note dit
   « euros au centime », une autre « milliers d'euros à 0,1 près ». Chaque
   paiement de chasseur dépend d'une conversion que personne n'a écrite.
2. **Rien ne vérifie le droit d'un chasseur à être payé** (`U01`, `U04`,
   `R01`, `R02`, `R04`, `T17`). On peut payer un chasseur hors délai, sans
   droit, ou qui n'est même pas celui du mandat.
3. **L'exclusivité et la durée du mandat ne sont pas protégées** (`U02`,
   `U05`, `U42`). Deux chasseurs peuvent avoir le même client en exclusif, et
   un mandat peut durer ce qu'on veut au lieu de 6 mois.

**En plus, quatre erreurs empêchent de créer des tables** : c'est l'étape 1
ci-dessous.

> **Attention** : le fichier `docker/init/01_create_fil_rouge_immobilier.sql`
> est ancien (12 tables au lieu de 18). Il sera réécrit à partir du MPD
> corrigé. Ce rapport ne s'en sert pas.

---

## Ce qu'il faut faire

Quatre étapes, **dans cet ordre**. Chaque ligne renvoie à un code de règle :
cherchez-le dans les tableaux du détail pour avoir le SQL exact.

### Étape 1 — Débloquer la création des tables

Sans ces corrections, PostgreSQL **refuse de créer** certaines tables. Rien
d'autre ne pourra être testé avant.

- [ ] **`Client`** — dans `chk_marital_status`, écrire `is_married` au lieu de
  `is married` (en deux mots, c'est une faute de frappe qui casse la table).
  Voir `K02`.
- [ ] **`Criteria`** — supprimer les quatre contraintes posées là par erreur :
  `ck_client_nb_children_positive`, `ck_client_marital_status_exclusive`,
  `ck_client_birth_date_past`, `ck_client_address_all_or_nothing`. Elles
  parlent de colonnes que `Criteria` n'a pas. La dernière est à recréer sur
  `Client` (`K04`) ; les trois autres y existent déjà.
- [ ] **`HunterPerformance`** — vérifier que la colonne `id_payment` n'est
  écrite qu'**une** fois dans le MPD. On l'a relevée deux fois ; si c'est le
  cas, la table ne se crée pas.
- [ ] **Extension `btree_gist`** — vérifier que le script commence par
  `CREATE EXTENSION IF NOT EXISTS btree_gist;`. Sans elle, `CommissionScale`
  et `HunterPerformance` ne se créent pas (voir le [lexique](#petit-lexique)).

### Étape 2 — Décider en équipe

Ces questions n'ont **pas de bonne réponse technique** : les notes se
contredisent, ou ne disent rien. Il faut trancher avant d'écrire le reste.

| question | les options | ce qui en dépend |
|---|---|---|
| **Unité de H** (`X02`) | euros au centime (`NOTES-REMUNERATION-CHASSEUR.md`) **ou** milliers d'euros à 0,1 près (`schema-tracabilite-remuneration-chasseur_v4.md`, que le MPD suit) | `Sale.fees_amount`, `ParametersFees.fixed_amount`, les bornes de `CommissionScale`, le calcul de `Payment.amount`. Si on choisit l'euro, les types `NUMERIC(6,1)` sont trop petits (99 999,9 au maximum) |
| **Ancienneté et performance** (`X01`) | elles choisissent le barème (`BAREME-COMMISSION.md`) **ou** elles majorent le taux (`NOTES-REMUNERATION-CHASSEUR.md`) | le MPD suit déjà la seconde, qui se présente comme la version à jour : il suffit de l'acter |
| **L'exemple de Bruno** (`R04`) | la note dit « acte signé après les 6 mois : pas de paiement », mais son propre exemple (`NOTES-REMUNERATION-CHASSEUR.md:73`) paie Bruno au-delà | la règle de paiement à coder à l'étape 4 |
| **Statuts d'une demande** (`U18`, `U21`, `U26`, `U28`) | quelle liste ? Les stories disent « confirmée », « acceptée », « non acceptée », « lancée » | la nouvelle colonne de `SearchRequest` |
| **États d'une offre** (`U34`, `F02`) | quels noms pour « offre signée, pas encore envoyée », et plus tard « bien choisi » / « bien écarté » ? | la liste de `EstateProposed.proposition_status` |
| **Priorité du client** (`U32`) | quelle échelle (1 à 5, haute / basse…) ? | une nouvelle colonne de `EstateProposed` |
| **Mandat annulé** (`U02`) | un mandat exclusif `'canceled'` bloque-t-il encore le client jusqu'à sa date de fin ? | la contrainte d'exclusivité de `Mandate` |
| **Statut `'renewed'`** (`U07`) | désigne-t-il le **nouveau** mandat, ou l'**ancien** qu'il remplace ? | le sens de `chk_renewed` |
| **Deux scores le même jour** (`B14`) | aujourd'hui, deux scores d'un même chasseur doivent être à deux jours d'écart au moins. Le permettre ? | `chk_perf_period` de `HunterPerformance` |
| **Rendez-vous** (`U29`, `F04`) | faut-il une table ? Aucune ne le porte | une table de plus dans le MPD |
| *plus tard* — pertinence (`F05`), types d'offre (`F07`) | parcours futur, pas urgent | — |

### Étape 3 — Compléter le MPD

Le SQL est donné dans la dernière colonne des tableaux : il suffit de le
recopier dans le MPD.

**Contraintes à ajouter ou à corriger :**

- [ ] `Client` — `K04` (déplacée depuis `Criteria`), `K05`, `K06`.
- [ ] `Criteria` — `L03` ; renommer `ck_client_postal_code_needs_country` et
  `ck_client_postal_code_format`, justes mais mal nommées.
- [ ] `Mandate` — `U05` : la fin tombe **exactement** 6 mois après la
  signature (remplace `ends_at > signature_date`) ; `U02` : l'exclusivité.
- [ ] `Payment` — `R21` (taux final entre 20 % et 60 %), `R22` (ancienneté par
  pas de 2 %), `R24` (formule du taux final).
- [ ] *facultatif* — `Hunter.hire_date` pas dans le futur (`R22`, sous
  `Hunter`) ; « fin après début » sur `ParametersFees` ; `rate > 0` sur
  `CommissionScale`.

**Colonnes ou tables à créer** (noms à choisir) :

- [ ] `User` — compte activé (`U19`).
- [ ] `SearchRequest` — statut de la demande (`U18`).
- [ ] `EstateProposed` — priorité du client (`U32`) et nouveaux états (`U34`).
- [ ] une table de médias pour les avis (`U33`).
- [ ] *plus tard* — chasseur IA sur `Hunter` (`F03`), pertinence (`F05`).

### Étape 4 — Coder dans l'API

Une contrainte `CHECK` ne voit **qu'une ligne d'une table**. Les règles
ci-dessous croisent plusieurs tables, ou comparent avec l'ancienne valeur :
elles se programment dans l'API (couche `services/`) ou dans un trigger.

- [ ] **Avant de créer un paiement — le chasseur y a-t-il droit ?** (`U01`,
  `U04`, `R01`, `R02`, `R04`, `T17`)
  - mandat exclusif → payé, même si le client a trouvé seul ;
  - mandat non exclusif → payé seulement si `Sale.sale_origin = 'hunter'` ;
  - acte signé après `Mandate.ends_at` → pas de paiement ;
  - `Payment.id_hunter` doit être le chasseur du mandat.
- [ ] **À la création d'une vente — calculer H** (`B01`, `R05`, `T02`, `T04`) :
  montant fixe + pourcentage × prix d'achat, avec les paramètres en vigueur à
  la date de signature. Ensuite, H ne change plus jamais.
- [ ] **Calculer le paiement** (`B02`, `B04`, `R19`, `R20`, `U12`, `R06`,
  `T14`, `R27`) :
  - choisir la tranche en vigueur à la date de l'acte : le barème du chasseur
    d'abord, sinon le barème par défaut ;
  - copier son taux dans `base_rate`, calculer `final_rate`, puis
    `amount` = arrondi au centime de `final_rate` × H en euros ;
  - ensuite, ces valeurs ne changent plus jamais.
- [ ] **Score de performance** (`R07` à `R12`, `U43`, `B12`, `B13`) : le
  calculer à partir de `Mandate`, `Sale` et `Visit` ; il monte après un
  paiement `'paid'`, il baisse quand un mandat expire sans vente.
- [ ] **Renouveler un mandat** seulement s'il n'y a eu aucune vente (`U07`).
- [ ] **Réaffecter une demande** refusée à un **autre** chasseur que celui qui
  a refusé (`U27`).
- [ ] *plus tard* — offres calculées sous le prix affiché (`F06`).

---

## Comment lire les tableaux

Chaque sous-titre du détail est **une table du MPD**. Chaque ligne est **une
règle**. Les colonnes :

1. **règle (source)** — le code, la règle en une phrase, et où la lire
   (`fichier:ligne`).
2. **ce que le MPD contient** — la contrainte trouvée, recopiée telle quelle,
   fautes comprises ; ou « rien ».
3. **verdict** — voir le tableau de « L'essentiel ».
4. **à faire** — l'action, en un mot (liste ci-dessous).
5. **SQL proposé / détail** — la contrainte à écrire, ou l'explication. Un nom
   écrit `<entre chevrons>` n'est donné par **aucune** source : c'est à
   l'équipe de le choisir.

**Les actions de la colonne « à faire » :**

| action | ce qu'on fait |
|---|---|
| **Rien** | rien à changer dans le MPD |
| **Ajouter** | écrire dans le MPD la contrainte proposée |
| **Corriger** | remplacer une contrainte existante par celle proposée |
| **Déplacer** | la contrainte existe, mais sur la mauvaise table |
| **Retirer** | supprimer une contrainte en trop |
| **Renommer** | la contrainte est juste, mais son nom trompe |
| **Colonne** | il manque une colonne, ou une table, dans le MPD |
| **Coder** | impossible en contrainte : à programmer dans l'API ou dans un trigger |
| **Décider** | l'équipe doit trancher d'abord |

« *plus tard* » signale une règle du **parcours futur** (voir le lexique) :
son absence n'est pas une erreur aujourd'hui.

---

## Petit lexique

On suppose connus `CREATE TABLE`, les clés et le `CHECK` simple. Voici le
reste.

- **MPD** — modèle physique de données : le schéma exact des tables, tel que
  PostgreSQL le créera (types, clés, contraintes).
- **Contrainte** — une règle écrite dans la base. Si une ligne la viole,
  PostgreSQL refuse l'`INSERT` ou l'`UPDATE`.
- **Un `CHECK` accepte `NULL`** — une condition « inconnue » n'est pas
  « fausse ». C'est pour ça qu'on écrit souvent `postal_code IS NULL OR …`.
- **Un `CHECK` ne voit qu'une ligne** — il ne peut ni lire une autre table, ni
  compter des lignes, ni comparer avec l'ancienne valeur. Pour tout ça, il
  faut un trigger ou l'API.
- **Trigger** — une fonction que PostgreSQL lance tout seul avant ou après un
  `INSERT` / `UPDATE`. On y met ce qu'un `CHECK` ne sait pas faire. Dans ce
  projet, la même règle peut aussi se coder dans l'API, couche `services/`.
- **`EXCLUDE USING gist`** — interdit que deux lignes « se marchent dessus ».
  Exemple :
  `EXCLUDE USING gist (id_hunter WITH =, daterange(valid_from, valid_until, '[]') WITH &&)`
  veut dire : *pour un même chasseur, deux périodes ne peuvent pas se
  chevaucher*.
- **`daterange(début, fin, '[]')`** — une période de dates (`numrange` : un
  intervalle de nombres). `'[]'` : les deux bornes sont incluses ; `'[)'` :
  la fin est exclue. Une fin `NULL` veut dire « sans fin ». `&&` veut dire
  « se chevauchent ».
- **`btree_gist`** — une extension PostgreSQL, à activer une fois par base :
  `CREATE EXTENSION IF NOT EXISTS btree_gist;`. Sans elle, un `EXCLUDE` ne
  sait pas comparer un nombre entier avec `=` (comme `id_hunter WITH =`), et
  la table ne se crée pas.
- **`~`** — « correspond à l'expression régulière ».
  `postal_code ~ '^[0-9]{5}$'` veut dire : exactement cinq chiffres.
- **`NUMERIC(p, s)`** — un nombre de `p` chiffres en tout, dont `s` après la
  virgule. `NUMERIC(6,1)` va jusqu'à 99 999,9. `NUMERIC(5,4)` sert aux taux :
  0,3500 par exemple.
- **H** — les honoraires que l'entreprise encaisse sur une vente, via le
  notaire : un montant fixe + un pourcentage du prix d'achat. Rangés dans
  `Sale.fees_amount`. Le chasseur touche une **part de H**, jamais un
  pourcentage du prix.
- **K€** — milliers d'euros : 200,0 K€ = 200 000 €.
- **Mandat exclusif** — le client confie sa recherche à un seul chasseur,
  pendant 6 mois.
- **Barème, tranche** — la grille des taux du chasseur, par tranche de prix
  d'achat. Un barème **nominatif** est propre à un chasseur (`id_hunter`
  rempli) ; le barème **par défaut** vaut pour tous (`id_hunter` vide).
- **Parcours futur** — l'assistance par IA (user stories `08` et `09`), prévue
  plus tard.

---

## Les codes des règles

Chaque règle a un code : une lettre, qui dit d'où elle vient, et un numéro.

| lettre | d'où vient la règle | fichier |
|---|---|---|
| `U` | user stories du parcours actuel | `user-stories/00_…` à `07_…` |
| `F` | user stories du parcours futur (IA) | `user-stories/08_…` et `09_…` |
| `K` | notes sur le client | `notes_contraintes_client.md` |
| `L` | notes sur la localisation des critères | `notes_contraintes_localisation_criteria.md` |
| `R` | notes sur la rémunération du chasseur | `NOTES-REMUNERATION-CHASSEUR.md` |
| `B` | barème de commission | `BAREME-COMMISSION.md` |
| `T` | schéma de traçabilité de la rémunération | `schema-tracabilite-remuneration-chasseur_v4.md` |
| `X` | contradiction entre deux notes | les deux fichiers cités |

Les fichiers `.feature` sont dans `user-stories/` ; les notes sont à la racine
du dépôt.

---

## Détail — Personnes et biens

**Choix de rangement.** Certaines règles ne disent pas sur quelle table elles
portent. Voici où on les a rangées :

- l'**offre d'achat** (`U23`, `U24`, `U34`, `U35`, `U36`, `U37`, `F07`) va à
  `EstateProposed`, qui porte `amount_proposition` et un `proposition_status`
  contenant `'offer_pending'` ;
- la **note d'avis** (`U33`) va à `Estate_SearchRequest`, qui porte
  `review_hunter`, `media_url` et `media_type` ;
- le **rendez-vous** (`U29`, `F04`) n'a aucune table : il n'est pas jugé ici
  (voir l'étape 2) ;
- la **facture** (`U38`, `U39`, `F08`) est traitée dans la partie « Mandat et
  rémunération ».

### User

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| U19 — le compte est activé à la fin de sa création (`01_particulier_demande_et_compte.feature:28`) | aucune colonne ne dit si le compte est activé | absente | **Colonne** | pas de `CHECK` : un booléen `<compte activé>` suffit ; la colonne manque et son nom reste à choisir |

### Role

Aucune règle ne vise cette table. Sa seule contrainte figure dans la liste
« Contraintes du MPD qu'aucune règle ne demande », en fin de partie.

### Client

**Tant que `K02` reste fausse, la table `Client` ne se crée pas** : la
contrainte contient une faute de frappe. Trois autres contraintes écrites pour
`Client` ont été posées sur `Criteria` par erreur (voir `Criteria`).

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| K01 — nombre d'enfants positif ou nul (`notes_contraintes_client.md:49`) | `nb_children SMALLINT CHECK (nb_children >= 0)` ; un `NULL` passe un `CHECK`, c'est donc bien ce que dit la note | couverte | **Rien** ici — **Retirer** la copie sur `Criteria` | en place ; la copie `ck_client_nb_children_positive`, posée sur `Criteria`, est à supprimer |
| K02 — pas à la fois marié et pacsé (`notes_contraintes_client.md:51`) | `constraint chk_marital_status CHECK (NOT (is married AND is_civil_solidarity_pact))` — `is married` est écrit en deux mots ; `IS` est un mot réservé du SQL, la contrainte est invalide | fausse | **Corriger** | `CONSTRAINT chk_marital_status CHECK (NOT (is_married AND is_civil_solidarity_pact))` — la bonne écriture existe déjà, sur la mauvaise table (`ck_client_marital_status_exclusive`, sur `Criteria`) |
| K03 — date de naissance pas dans le futur (`notes_contraintes_client.md:53`) | `birth_date DATE CHECK (birth_date <= CURRENT_DATE)` | couverte | **Rien** ici — **Retirer** la copie sur `Criteria` | en place ; la copie `ck_client_birth_date_past`, posée sur `Criteria`, est à supprimer |
| K04 — adresse, code postal, ville : tous les trois ou aucun (`notes_contraintes_client.md:144`) | rien sur `Client` ; la contrainte `ck_client_address_all_or_nothing` est posée sur `Criteria`, qui n'a pas de colonne `address` | absente | **Déplacer** vers `Client` | `CONSTRAINT ck_client_address_all_or_nothing CHECK ((address IS NULL AND postal_code IS NULL AND town IS NULL) OR (address IS NOT NULL AND postal_code IS NOT NULL AND town IS NOT NULL))` |
| K05 — un code postal exige un pays (`notes_contraintes_client.md:60`) | `postal_code` n'a qu'un contrôle « non vide, sans espace en bord » ; la contrainte du même nom est sur `Criteria`, où elle sert à `L04` | absente | **Ajouter** sur `Client` | `CONSTRAINT ck_client_postal_code_needs_country CHECK (postal_code IS NULL OR country_iso IS NOT NULL)` ; celle de `Criteria` reste, mais son préfixe `ck_client_` est à renommer |
| K06 — format du code postal selon le pays, mêmes cas que L05 à L11 (`notes_contraintes_client.md:146`) | aucun contrôle de format sur `Client` ; la contrainte `ck_client_postal_code_format` est sur `Criteria` | absente | **Ajouter** sur `Client` | `CONSTRAINT ck_client_postal_code_format CHECK (postal_code IS NULL OR CASE WHEN country_iso IN ('FR','ES','DE','IT') THEN postal_code ~ '^[0-9]{5}$' WHEN country_iso IN ('BE','CH') THEN postal_code ~ '^[1-9][0-9]{3}$' WHEN country_iso = 'LU' THEN postal_code ~ '^[0-9]{4}$' WHEN country_iso = 'NL' THEN postal_code ~ '^[1-9][0-9]{3} [A-Z]{2}$' WHEN country_iso = 'GB' THEN postal_code ~ '^[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}$' WHEN country_iso = 'IE' THEN postal_code ~ '^([AC-FHKNPRTV-Y][0-9]{2}\|D6W) [0-9AC-FHKNPRTV-Y]{4}$' ELSE FALSE END)` |

### Hunter

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| F03 — un chasseur est humain ou chasseur-IA, parcours futur (`09_futur_chasseur_assistance_ia.feature:11`) | aucune colonne ne distingue les deux | absente | **Colonne** — *plus tard* | pas de `CHECK` : un booléen `<chasseur IA>` suffit ; la colonne manque et son nom reste à choisir |
| R22 — ancienneté : 2 % par année complète, 10 % au maximum (`NOTES-REMUNERATION-CHASSEUR.md:59`) | `hire_date DATE NOT NULL`, sans limite ; le plafond de 10 % se vérifie sur `Payment` | partielle | **Ajouter** (facultatif) | `CHECK (hire_date <= CURRENT_DATE)` — proposé sur le modèle de `K03`, aucune source ne l'écrit : une embauche dans le futur donnerait une ancienneté négative |

### RealEstateManager

Aucune règle ne vise cette table. Ses contrôles figurent dans la liste
« Contraintes du MPD qu'aucune règle ne demande ».

### SearchRequest

La table n'a **aucun `CHECK`** : les étapes de la vie d'une demande
(confirmée, acceptée, lancée…) n'existent pas dans la base. Cinq règles en
parlent ; il manque une colonne de statut.

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| U18 — l'affectation d'un chasseur est confirmée (`01_particulier_demande_et_compte.feature:20`) | aucune colonne de statut | absente | **Colonne** + **Décider** | `CHECK (<statut de la demande> IN (<…>))` — noms à décider ; les stories disent « confirmée », « acceptée », « non acceptée », « lancée » (U18, U28, U26, U21) |
| U21 — la signature du mandat lance officiellement la recherche (`01_particulier_demande_et_compte.feature:37`) | aucune colonne de statut | absente | **Colonne** (celle de U18) | même colonne que U18 |
| U26 — le chasseur peut ne pas accepter une demande (`04_chasseur_prise_en_charge_demande.feature:19`) | aucune colonne de statut | absente | **Colonne** (celle de U18) | même colonne que U18 |
| U27 — une demande non acceptée peut être réaffectée à un autre chasseur (`04_chasseur_prise_en_charge_demande.feature:21`) | `id_hunter` peut être vide et modifié : la réaffectation est possible ; mais rien ne se souvient du chasseur qui a refusé | partielle | **Coder** | pas de `CHECK` possible : « un autre chasseur » demande l'historique des refus |
| U28 — le chasseur peut accepter une demande (`04_chasseur_prise_en_charge_demande.feature:26`) | aucune colonne de statut | absente | **Colonne** (celle de U18) | même colonne que U18 |

### Criteria

**Quatre contraintes posées là par erreur.**
`ck_client_nb_children_positive`, `ck_client_marital_status_exclusive`,
`ck_client_birth_date_past` et `ck_client_address_all_or_nothing` portent sur
`nb_children`, `is_married`, `is_civil_solidarity_pact`, `birth_date` et
`address` : des colonnes que `Criteria` **n'a pas**.

- Tant qu'elles restent, **la table `Criteria` ne se crée pas**. Elles sont à
  supprimer (étape 1).
- Les verdicts *couverte* ci-dessous jugent chaque contrainte seule : ils ne
  valent qu'une fois ces quatre-là retirées.
- Leur place est `Client` (K01 à K04).

Deux autres contraintes au préfixe `ck_client_`
(`ck_client_postal_code_needs_country`, `ck_client_postal_code_format`)
portent, elles, sur des colonnes de `Criteria`. Elles sont **valides ici** et
couvrent L04 à L11 ; seul leur nom trompe.

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| F01 — critères budget, zone, type de bien, liste ouverte, parcours futur (`08_futur_particulier_assistance_ia.feature:15`) | `budget_min`, `budget_max`, `country_iso`, `town`, `postal_code`, `estate_type` | couverte | **Rien** | en place ; la liste étant ouverte, rien de plus à contraindre |
| L01 — pays dans une liste fermée de 10 codes (`notes_contraintes_localisation_criteria.md:44`) | `CHECK (country_iso IN ('FR', 'ES', 'DE','GB', 'IE', 'BE', 'NL', 'LU', 'IT','CH'))` — les mêmes dix codes | couverte | **Rien** | en place |
| L02 — ville non vide, sans espace en bord (`notes_contraintes_localisation_criteria.md:45`) | `CHECK (town = btrim(town) AND town <> '')` | couverte | **Rien** | en place |
| L03 — une ville exige un pays (`notes_contraintes_localisation_criteria.md:50`) | aucune contrainte sur `town` et `country_iso` ensemble | absente | **Ajouter** | `CHECK (town IS NULL OR country_iso IS NOT NULL)` |
| L04 — un code postal exige un pays (`notes_contraintes_localisation_criteria.md:52`) | `CONSTRAINT ck_client_postal_code_needs_country CHECK (postal_code IS NULL OR country_iso IS NOT NULL)` | couverte | **Renommer** | en place ; préfixe `ck_client_` à renommer |
| L05 — FR, ES, DE, IT : 5 chiffres (`notes_contraintes_localisation_criteria.md:55`) | le cas `WHEN country_iso IN ('FR','ES','DE','IT') THEN postal_code ~ '^[0-9]{5}$'` de `ck_client_postal_code_format` | couverte | **Rien** | en place (le nom de la contrainte est à renommer, comme L04) |
| L06 — BE, CH : 4 chiffres, le premier n'est pas 0 (`notes_contraintes_localisation_criteria.md:56`) | le cas `WHEN country_iso IN ('BE','CH') THEN postal_code ~ '^[1-9][0-9]{3}$'` | couverte | **Rien** | en place |
| L07 — LU : 4 chiffres (`notes_contraintes_localisation_criteria.md:57`) | le cas `WHEN country_iso = 'LU' THEN postal_code ~ '^[0-9]{4}$'` | couverte | **Rien** | en place |
| L08 — NL : 4 chiffres, une espace, 2 majuscules (`notes_contraintes_localisation_criteria.md:58`) | le cas `WHEN country_iso = 'NL' THEN postal_code ~ '^[1-9][0-9]{3} [A-Z]{2}$'` | couverte | **Rien** | en place |
| L09 — GB : format britannique en deux parties (`notes_contraintes_localisation_criteria.md:59`) | le cas `WHEN country_iso = 'GB' THEN postal_code ~ '^[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}$'` | couverte | **Rien** | en place |
| L10 — IE : format irlandais Eircode (`notes_contraintes_localisation_criteria.md:60`) | le cas `WHEN country_iso = 'IE' THEN postal_code ~ '^([AC-FHKNPRTV-Y][0-9]{2}\|D6W) [0-9AC-FHKNPRTV-Y]{4}$'` | couverte | **Rien** | en place |
| L11 — tout autre cas, pays vide compris, refuse le code postal (`notes_contraintes_localisation_criteria.md:61`) | `ELSE FALSE END` ; un pays `NULL` ne vérifie aucun `WHEN` et tombe dans le `ELSE` | couverte | **Rien** | en place |
| L12 — les trois colonnes de localisation peuvent être vides ensemble (`notes_contraintes_localisation_criteria.md:35`) | aucune contrainte « au moins une des trois » | couverte | **Rien** | en place — ici, c'est l'absence de contrainte qui respecte la règle |

### Estate

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| F06 — des offres sous le prix affiché sont calculées à l'avance, parcours futur (`09_futur_chasseur_assistance_ia.feature:40`) | `price NUMERIC (6, 1) CHECK (price >= 0)` porte le prix affiché ; l'offre est `EstateProposed.amount_proposition` | partielle | **Coder** — *plus tard* | pas de `CHECK` simple : `amount_proposition < price` compare deux tables, donc un trigger ou l'API |

### Picture

Aucune règle ne vise cette table, qui n'a d'ailleurs aucun `CHECK`.

### Estate_SearchRequest

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| U31 — sélection quotidienne, plusieurs envois par jour en zone tendue (`05_chasseur_selection_quotidienne_biens.feature:17`) | `created_at TIMESTAMP` garde l'heure : plusieurs envois par jour sont possibles | couverte | **Rien** | en place ; une fréquence d'envoi ne se vérifie pas sur une seule ligne |
| F05 — annonces classées par pertinence, échelle non précisée, parcours futur (`09_futur_chasseur_assistance_ia.feature:39`) | aucune colonne de pertinence | absente | **Colonne** + **Décider** — *plus tard* | `CHECK (<pertinence> …)` — l'échelle est à décider, la story ne la donne pas |
| U33 — une note d'avis porte des commentaires audio et des vidéos (`06_chasseur_avis_et_offre_achat.feature:14`) — rangée ici | `CHECK (media_type IN ('audio' ,'video') )` et `chk_media` ; mais un seul couple `media_url` / `media_type` par ligne | partielle | **Colonne** — une table de médias | les valeurs sont en place ; « des » audios **et** des vidéos pour un même avis demandent plusieurs médias par avis, donc une table à part, pas une contrainte |

### EstateProposed

La contrainte `chk_offer` impose un montant dès que `proposition_status` n'est
plus `'proposed'`. Donc `'accepted'` et `'rejected'` sont **des réponses du
vendeur à une offre**, pas des choix du client. C'est ce qui explique les
verdicts de `F02` et `U34`.

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| U22 — le client choisit un ou plusieurs biens à faire visiter (`02_particulier_recherche_et_visites.feature:17`) | le choix se traduit par une ligne dans `Visit`, pas par un état de la proposition | couverte | **Rien** | en place |
| U32 — le client classe la sélection par priorité, échelle non précisée (`05_chasseur_selection_quotidienne_biens.feature:28`) | `comment_client TEXT`, pas de colonne de priorité | absente | **Colonne** + **Décider** | `CHECK (<priorité> …)` — échelle à décider, la story ne la donne pas |
| F02 — le client choisit ou écarte un bien proposé, parcours futur (`08_futur_particulier_assistance_ia.feature:29`) | `proposition_status IN ('proposed', 'offer_pending', 'accepted', 'rejected')` ; un bien écarté sans offre ne peut pas être `'rejected'`, qui exige un montant | absente | **Corriger** + **Décider** — *plus tard* | `CHECK (proposition_status IN ('proposed', <choisi>, <écarté>, 'offer_pending', 'accepted', 'rejected'))`, et `chk_offer` réécrit avec `proposition_status IN ('proposed', <choisi>, <écarté>)` du côté « montant vide » |
| U23 — le vendeur peut ne pas accepter l'offre (`03_particulier_offre_et_signature.feature:21`) — rangée ici | la valeur `'rejected'` | couverte | **Rien** | en place |
| U24 — le vendeur peut accepter l'offre (`03_particulier_offre_et_signature.feature:27`) — rangée ici | la valeur `'accepted'` | couverte | **Rien** | en place |
| U34 — l'offre est complétée puis signée par le client (`06_chasseur_avis_et_offre_achat.feature:22`) — rangée ici | le montant est exigé dès qu'on quitte `'proposed'` ; mais aucun état ne dit « signée, pas encore envoyée » : `'proposed'` interdit le montant, `'offer_pending'` veut dire déjà envoyée (U35) | partielle | **Corriger** + **Décider** | `CHECK (proposition_status IN ('proposed', <offre signée>, 'offer_pending', 'accepted', 'rejected'))` ; `chk_offer` ne change pas, `<offre signée>` exigeant déjà un montant |
| U35 — une fois envoyée, l'offre passe « en attente de réponse du vendeur » (`06_chasseur_avis_et_offre_achat.feature:34`) — rangée ici | la valeur `'offer_pending'` | couverte | **Rien** | en place |
| U36 — le vendeur peut refuser l'offre (`06_chasseur_avis_et_offre_achat.feature:39`) — rangée ici | la valeur `'rejected'` | couverte | **Rien** | en place |
| U37 — le vendeur peut accepter l'offre (`06_chasseur_avis_et_offre_achat.feature:46`) — rangée ici | la valeur `'accepted'` | couverte | **Rien** | en place |
| F07 — plusieurs offres proposées, plus basse ou au prix, liste ouverte, parcours futur (`09_futur_chasseur_assistance_ia.feature:58`) — rangée ici | un seul `amount_proposition` par ligne, aucun type d'offre | absente | **Décider** — *plus tard* | pas de liste fermée possible : la story laisse la liste ouverte (« ... ») |

### Visit

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| U22 — le client choisit un ou plusieurs biens à faire visiter par son chasseur (`02_particulier_recherche_et_visites.feature:17`) | une ligne par bien visité ; `CHECK (visitor_type IN ('hunter', 'client'))` contient `'hunter'` | couverte | **Rien** | en place |

### Contraintes du MPD qu'aucune règle ne demande

Elles **ne sont pas fausses** : simplement, aucune user story ni note ne les
exige. **À garder.** Si l'une vous paraît inutile, en parler avant de la
retirer. Regroupées par type, pour ces douze tables :

- **Liste de rôles** — `Role.wording IN ('Admin', 'Client', 'Hunter', 'Manager')`.
- **Liste de pays** — `country_iso IN (…10 codes…)` sur `Client`, `Hunter`,
  `RealEstateManager` et `Estate` ; seule celle de `Criteria` a une règle
  (L01).
- **Liste de genres** — `gender IN ('male', 'female', 'other')` sur `Client`,
  `Hunter`, `RealEstateManager`.
- **« Non vide, sans espace en bord »** (`x = btrim(x) AND x <> ''`) :
  - `Client` : `first_name`, `last_name`, `phone_number`, `address`,
    `address_complement`, `postal_code`, `town` ;
  - `Hunter` : `first_name`, `last_name`, `phone_number`, `company_name`,
    `education_level` ;
  - `RealEstateManager` : `first_name`, `last_name`, `phone_number`,
    `company_name` ;
  - `Criteria.change_reason` ;
  - `Estate` : `reference`, `town`, `street`, `street_number`, `postal_code`.
  - Seul `Criteria.town` a une règle (L02).
- **Listes de biens** — les dix valeurs de `estate_type` (F01 demande le
  critère, pas ses valeurs), les douze de `typology`, les douze de `floor`,
  `energy_class_max` et `energy_class` de A à G.
- **Limites de `Criteria`** — `> 0` sur `budget_min`, `budget_max`, `rooms_*`,
  `surface_*` ; `>= 0` sur `renovation_budget_*`, `bedrooms_*`, `toilets_*`,
  `bathrooms_*`, `swimming_pool_*`, `nb_balcony_*`, `nb_terrace_*`,
  `land_surface_*`, `parking_spaces` ; et les dix contrôles « min ≤ max », de
  `chk_budget` à `chk_land_surface`.
- **Limites de `Estate`** — `price >= 0` (F06 cite le prix, pas sa limite),
  `energy_kwh_m2 > 0`, `energy_co2_m2 > 0`, `latitude BETWEEN -90 AND 90`,
  `longitude BETWEEN -180 AND 180`, `nb_rooms > 0`, `surface > 0`, et `>= 0`
  sur `nb_bedrooms`, `nb_bathrooms`, `nb_toilets`, `nb_swimming_pool`,
  `nb_balcony`, `nb_terrace`, `land_surface`, `parking_spaces`.
- **Longueurs de texte** — `char_length(…) <= 2000` sur `Estate.information`,
  `Estate_SearchRequest.review_hunter` et `EstateProposed.comment_hunter` ;
  `comment_client`, son équivalent côté client, n'en a pas.
- **Montant d'offre** — `EstateProposed.amount_proposition >= 0`.
- **Visiteur client** — la valeur `'client'` de `Visit.visitor_type` ;
  `'hunter'`, lui, s'appuie sur U22.

---

## Détail — Mandat et rémunération

**Choix de rangement.** Certaines règles ne disent pas sur quelle table elles
portent. Voici où on les a rangées :

- la **facture** (`U38`, `U39`, `F08`) va à `Payment`, dont le `status` porte
  `'invoice_submitted'` et `'verified'` ;
- le **montant collecté par le notaire** (`U09`) va à `Sale.fees_amount` :
  c'est H, « encaissé par l'entreprise via le notaire » selon `R06` ;
- les **indicateurs de performance** (`U13` à `U17`, `B06` à `B11`, `R08` à
  `R12`) n'ont pas de colonne : ils **se calculent** à partir de `Mandate`,
  `Sale` et `Visit`, et seul le score est enregistré. Ils sont jugés
  *couverts* dès que les données du calcul existent : un calcul ne se vérifie
  pas avec une contrainte, et paliers et poids sont des paramètres
  (`NOTES-REMUNERATION-CHASSEUR.md:17`). Le calcul lui-même est à coder
  (étape 4).

**Deux vérifications à faire d'abord** (elles font partie de l'étape 1) :

- **`btree_gist`.** `excl_scale_no_overlap` et `excl_perf_no_overlap`
  comparent `id_hunter WITH =` dans un `EXCLUDE`. Sans l'extension
  `btree_gist`, PostgreSQL ne sait pas le faire pour un entier, et la table ne
  se crée pas. On n'a pas pu vérifier si le MPD l'active.
- **`HunterPerformance.id_payment` apparaît deux fois.** Si le MPD contient
  vraiment ce doublon, la table ne se crée pas (colonne déclarée deux fois).
  Comme pour `Criteria`, les verdicts de cette table jugent chaque contrainte
  seule.

### Mandate

La table n'a **aucune contrainte `EXCLUDE`**, et une seule limite sur la durée
du mandat : `ends_at > signature_date` (la fin est après la signature). Or
cinq règles fixent cette durée à **6 mois**.

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| U01 — sous mandat exclusif, le chasseur est payé même si le client achète seul (`00_regles_metier_mandat_remuneration.feature:19`) | `is_exclusive` et `Sale.sale_origin IN ('hunter', 'client_alone')` existent ; rien ne relie l'exclusivité au droit d'être payé | partielle | **Coder** | pas de `CHECK` : la règle croise `Mandate`, `Sale` et `Payment` (T17) — trigger à la création du paiement, ou l'API |
| U02 — sous mandat exclusif, aucun autre chasseur n'agit pour ce client pendant la validité (`00_regles_metier_mandat_remuneration.feature:20`) | aucun `EXCLUDE` | absente | **Ajouter** + **Décider** | `EXCLUDE USING gist (id_client WITH =, id_hunter WITH <>, daterange(signature_date, ends_at, '[]') WITH &&) WHERE (is_exclusive AND signature_date IS NOT NULL)` — le `WHERE` écarte les mandats pas encore signés (sans dates, leur période vaudrait « toujours ») ; l'exclusion ne compare que deux mandats exclusifs entre eux, et empêcher un mandat non exclusif de se poser sur un exclusif demande un trigger ; `btree_gist` requis ; un mandat `'canceled'` bloquerait le client jusqu'à `ends_at` : à décider |
| U03 — deux mandats non exclusifs d'un même client, avec deux chasseurs, peuvent coexister (`00_regles_metier_mandat_remuneration.feature:33`) | aucune exclusion : rien n'empêche la coexistence | couverte | **Rien** | en place ; l'exclusion proposée pour U02, limitée aux mandats exclusifs, la laisse passer |
| U05 — la validité du mandat est de 6 mois (`00_regles_metier_mandat_remuneration.feature:37`) | `ends_at > signature_date` : l'ordre des dates, pas la durée | partielle | **Corriger** | `CHECK ((signature_date IS NULL AND ends_at IS NULL) OR (signature_date IS NOT NULL AND ends_at = (signature_date + INTERVAL '6 months')::date))`, à la place de la contrainte actuelle |
| U06 — signature le 2026-02-25, fin de validité le 2026-08-25 (`00_regles_metier_mandat_remuneration.feature:39`) | la contrainte actuelle accepte le 2026-08-25, mais aussi n'importe quelle date après | partielle | **Corriger** (celle de U05) | la contrainte de U05 n'accepte que le 2026-08-25 pour cet exemple |
| U07 — renouvelable à l'échéance si aucune vente n'a abouti (`00_regles_metier_mandat_remuneration.feature:40`) | le statut `'renewed'` et `chk_renewed` ; « aucune vente » se lit dans `Sale` | partielle | **Coder** + **Décider** | pas de `CHECK` pour « sans vente » : trigger à la création du renouvellement ; `chk_renewed` exige un mandat parent quand le statut est `'renewed'`, donc ce statut désigne le **nouveau** mandat et non celui qu'il remplace — sens à confirmer |
| U20 — mode exclusif ou non exclusif, date de signature, date de fin de validité (`01_particulier_demande_et_compte.feature:36`) | `is_exclusive BOOLEAN`, `signature_date`, `ends_at` | couverte | **Rien** | en place |
| U30 — la date de fin de validité est calculée, pas saisie à la main (`04_chasseur_prise_en_charge_demande.feature:41`) | toute date après la signature est acceptée | partielle | **Corriger** (celle de U05) | la contrainte de U05 refuse toute saisie qui n'est pas le bon calcul ; qui fait le calcul (API ou trigger) reste à coder |
| U42 — fin de validité = signature + 6 mois (`07_chasseur_remuneration_et_performance.feature:39`) | `ends_at > signature_date` | partielle | **Corriger** (celle de U05) | contrainte de U05 |
| R01 — sous mandat exclusif, toujours payé, même si le client trouve seul (`NOTES-REMUNERATION-CHASSEUR.md:22`) | comme U01 | partielle | **Coder** | comme U01 |
| R04 — un acte signé après signature + 6 mois ne donne aucun droit (`NOTES-REMUNERATION-CHASSEUR.md:22`) | `ends_at` et `Sale.signature_date` sont sur deux tables différentes | partielle | **Coder** + **Décider** | trigger à la création du paiement : `Sale.signature_date <= Mandate.ends_at` ; l'exemple de Bruno, dans la même note (ligne 73), dit le contraire |
| R29 — le mandat porte une date de fin (signature + 6 mois) et son exclusivité (`NOTES-REMUNERATION-CHASSEUR.md:89`) | `ends_at`, `is_exclusive` ; les 6 mois manquent | partielle | **Corriger** (celle de U05) | contrainte de U05 |
| B13 — à l'échéance (6 mois) sans vente, la performance baisse (`BAREME-COMMISSION.md:48`) — côté mandat | le statut `'expired'` marque l'échéance | couverte | **Rien** | en place ; la baisse se juge sous `HunterPerformance` |
| T17 — le droit à être payé croise mandat et vente, pas de `CHECK` simple (`schema-tracabilite-remuneration-chasseur_v4.md:117`) | les quatre colonnes citées existent : `is_exclusive`, `ends_at`, `sale_origin`, `signature_date` ; aucune vérification | partielle | **Coder** | trigger à la création du paiement, comme la note le dit |

**La période du mandat.** Le mandat a une période : de `signature_date` à
`ends_at`. Seule `U02` exige qu'elle ne chevauche pas une autre, et seulement
entre mandats exclusifs d'un même client. C'est la **seule exclusion qui
manque** dans ces six tables.

### Sale

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| U04 — la vente paie le chasseur à l'origine de la transaction (`00_regles_metier_mandat_remuneration.feature:34`) | `sale_origin` dit qui est à l'origine ; mais rien n'oblige `Payment.id_hunter` à être le chasseur du mandat vendu | partielle | **Coder** | trigger à la création du paiement : `Payment.id_hunter` égal au `Mandate.id_hunter` de la vente |
| U07 — renouvellement seulement sans vente (`00_regles_metier_mandat_remuneration.feature:40`) — côté vente | `id_mandate` | partielle | **Coder** | comme sous `Mandate` |
| U09 — le montant collecté par le notaire sert de base au calcul (`00_regles_metier_mandat_remuneration.feature:48`) — rangée ici | `fees_amount NUMERIC(6,1) CHECK (fees_amount > 0)` | couverte | **Rien** | en place |
| B01 — base = montant fixe + pourcentage × montant d'achat (`BAREME-COMMISSION.md:12`) | `purchase_amount`, `fees_amount` ; le fixe et le taux sont sur `ParametersFees` | partielle | **Coder** | pas de `CHECK` : le calcul croise deux tables — trigger à la création de la vente (T02) |
| R02 — sous mandat non exclusif, payé seulement si le chasseur est à l'origine (`NOTES-REMUNERATION-CHASSEUR.md:22`) | `sale_origin` ; `is_exclusive` est sur `Mandate` | partielle | **Coder** | trigger à la création du paiement : refus si le mandat est non exclusif et `sale_origin = 'client_alone'` |
| R03 — un seul chasseur payé par vente (`NOTES-REMUNERATION-CHASSEUR.md:22`) | c'est le rôle des clés, pas d'un `CHECK` | couverte | **Rien** | rien à ajouter en `CHECK` |
| R04 — acte après l'échéance : aucun droit (`NOTES-REMUNERATION-CHASSEUR.md:22`) — côté vente | `signature_date`, sans lien avec `Mandate.ends_at` | partielle | **Coder** | comme sous `Mandate` |
| R05 — H = montant fixe + pourcentage × prix d'achat (`NOTES-REMUNERATION-CHASSEUR.md:26`) | comme B01 | partielle | **Coder** | comme B01 |
| T01 — H strictement positif, en K€, `NUMERIC(6,1)`, figé à la signature (`schema-tracabilite-remuneration-chasseur_v4.md:16`) | `fees_amount NUMERIC(6,1) CHECK (fees_amount > 0)` — identique | couverte | **Rien** | en place |
| T02 — H calculé une seule fois avec les paramètres en vigueur, jamais recalculé (`schema-tracabilite-remuneration-chasseur_v4.md:19`) | `fees_amount` est enregistré ; rien ne le relie à `ParametersFees`, ni n'empêche de le modifier | partielle | **Coder** | trigger `BEFORE UPDATE` qui refuse de changer `fees_amount` ; un `CHECK` ne voit pas l'ancienne valeur |
| T04 — une date de signature retrouve toujours exactement une ligne de paramètres (`schema-tracabilite-remuneration-chasseur_v4.md:21`) — côté vente | `signature_date` ; l'exclusion de `ParametersFees` garantit **au plus** une ligne | partielle | **Coder** | « **au moins** une » suppose des périodes sans trou : trigger ou API |
| T17 — le droit à être payé croise mandat et vente (`schema-tracabilite-remuneration-chasseur_v4.md:117`) — côté vente | comme sous `Mandate` | partielle | **Coder** | comme sous `Mandate` |
| X02 — contradiction : H en euros au centime (NOTES) ou en K€ à une décimale (TRACABILITE) (`NOTES-REMUNERATION-CHASSEUR.md:74` ; `schema-tracabilite-remuneration-chasseur_v4.md:16`) | `fees_amount NUMERIC(6,1)` suit TRACABILITE, la note la plus récente | partielle | **Décider** | à trancher en équipe ; en K€, H est arrondi à 0,1 K€ près, soit jusqu'à 50 € d'écart, alors que `Payment.amount` est au centime : il faut une conversion que rien n'écrit (T14) |

### Payment

Tous les éléments du calcul sont enregistrés, chacun avec ses limites. Mais
**aucune contrainte ne les relie entre eux**, ni à `Sale.fees_amount`.

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| U01 — sous mandat exclusif, payé même si le client achète seul (`00_regles_metier_mandat_remuneration.feature:19`) — côté paiement | rien ne lie un paiement à l'exclusivité | partielle | **Coder** | comme sous `Mandate` |
| U38 — la facture du chasseur est envoyée pour vérification (`07_chasseur_remuneration_et_performance.feature:21`) — rangée ici | la valeur `'invoice_submitted'` | couverte | **Rien** | en place |
| U39 — la facture est affichée vérifiée et conforme (`07_chasseur_remuneration_et_performance.feature:26`) — rangée ici | la valeur `'verified'` | couverte | **Rien** | en place |
| U40 — le paiement est affiché programmé (`07_chasseur_remuneration_et_performance.feature:27`) | la valeur `'scheduled'` | couverte | **Rien** | en place |
| U41 — le paiement effectué est marqué payé (`07_chasseur_remuneration_et_performance.feature:33`) | la valeur `'paid'` et `chk_paid`, qui lie cet état à `paid_at` | couverte | **Rien** | en place |
| F08 — facture vérifiée et conforme, sans anomalie, parcours futur (`09_futur_chasseur_assistance_ia.feature:65`) — rangée ici | la valeur `'verified'` | couverte | **Rien** | en place ; détecter une anomalie n'est pas une contrainte |
| B02 — rémunération = base × taux(chasseur, montant, date) (`BAREME-COMMISSION.md:20`) | `amount`, `final_rate`, `id_commission_scale` ; rien ne lie `amount` à `final_rate` × H | partielle | **Coder** | trigger, voir T14 |
| B12 — la performance monte quand un paiement est effectué (`BAREME-COMMISSION.md:47`) — côté paiement | la valeur `'paid'` marque l'événement | couverte | **Rien** | en place ; la hausse se juge sous `HunterPerformance` |
| R01 — sous mandat exclusif, toujours payé (`NOTES-REMUNERATION-CHASSEUR.md:22`) — côté paiement | comme U01 | partielle | **Coder** | comme sous `Mandate` |
| R02 — sous mandat non exclusif, payé seulement si à l'origine (`NOTES-REMUNERATION-CHASSEUR.md:22`) — côté paiement | aucune vérification | partielle | **Coder** | comme sous `Sale` |
| R03 — un seul chasseur payé par vente (`NOTES-REMUNERATION-CHASSEUR.md:22`) — côté paiement | c'est le rôle des clés, pas d'un `CHECK` | couverte | **Rien** | rien à ajouter en `CHECK` |
| R06 — le chasseur touche une part de H, jamais un pourcentage du prix (`NOTES-REMUNERATION-CHASSEUR.md:28`) | `amount` n'est lié ni à H ni au prix | partielle | **Coder** | trigger de T14 : `amount` calculé sur `Sale.fees_amount`, jamais sur `purchase_amount` |
| R21 — taux final entre 20 % et 60 % (`NOTES-REMUNERATION-CHASSEUR.md:58`) | `final_rate CHECK (final_rate > 0 AND final_rate <= 1)` : des limites trop larges | partielle | **Corriger** | `CHECK (final_rate BETWEEN 0.20 AND 0.60)` |
| R22 — ancienneté : 2 % par année complète, 10 % au maximum (`NOTES-REMUNERATION-CHASSEUR.md:59`) — côté paiement | `seniority_rate BETWEEN 0 AND 0.10` : les limites, pas le pas de 2 % | partielle | **Corriger** | `CHECK (seniority_rate IN (0, 0.02, 0.04, 0.06, 0.08, 0.10))` |
| R23 — performance = (score − 50) / 50 × 20 %, entre −20 % et +20 % (`NOTES-REMUNERATION-CHASSEUR.md:60`) | `performance_rate BETWEEN -0.20 AND 0.20` | couverte | **Rien** | en place |
| R24 — les majorations s'additionnent, puis s'appliquent au taux de base (`NOTES-REMUNERATION-CHASSEUR.md:62`) | rien ne lie `final_rate` aux trois autres taux | absente | **Ajouter** | `CHECK (final_rate = LEAST(0.60, GREATEST(0.20, round(base_rate * (1 + seniority_rate + performance_rate), 4))))` — l'arrondi à 4 décimales vient du type `NUMERIC(5,4)`, aucune source ne le fixe |
| R25 — rémunération arrondie au centime (`NOTES-REMUNERATION-CHASSEUR.md:66`) | `amount NUMERIC(12,2)` | couverte | **Rien** | en place, si `amount` est en euros — voir T14 |
| R26 — marge = H − rémunération, jamais arrondie à part (`NOTES-REMUNERATION-CHASSEUR.md:67`) | aucune colonne de marge | couverte | **Rien** | en place : la marge se calcule, elle ne s'enregistre pas |
| R27 — les éléments du calcul sont figés à la date de l'acte, jamais recalculés (`NOTES-REMUNERATION-CHASSEUR.md:70`) | les quatre taux et le montant sont enregistrés ; rien n'empêche de les modifier | partielle | **Coder** | trigger `BEFORE UPDATE` sur ces cinq colonnes ; un `CHECK` ne voit pas l'ancienne valeur |
| R32 — le paiement fige honoraires, score, taux de base, majorations, taux final, montant (`NOTES-REMUNERATION-CHASSEUR.md:92`) | taux et montant sur `Payment`, H sur `Sale` ; pas de score, mais on le retrouve exactement : score = 50 + `performance_rate` × 250 | couverte | **Rien** | en place |
| T10 — taux de tranche entre 0 (exclu) et 1, `NUMERIC(5,4)` (`schema-tracabilite-remuneration-chasseur_v4.md:90`) | `base_rate NUMERIC(5,4) CHECK (base_rate > 0 AND base_rate <= 1)` — identique | couverte | **Rien** | en place |
| T11 — majoration d'ancienneté entre 0 et 0,10 (`schema-tracabilite-remuneration-chasseur_v4.md:91`) | `seniority_rate BETWEEN 0 AND 0.10` — identique | couverte | **Rien** | en place |
| T12 — majoration de performance entre −0,20 et 0,20 (`schema-tracabilite-remuneration-chasseur_v4.md:92`) | `performance_rate BETWEEN -0.20 AND 0.20` — identique | couverte | **Rien** | en place |
| T13 — taux final = base × (1 + ancienneté + performance), ramené entre 0,20 et 0,60 (`schema-tracabilite-remuneration-chasseur_v4.md:96`) | `final_rate > 0 AND final_rate <= 1` : ni la formule ni les bonnes limites | partielle | **Ajouter** (celle de R24) | la contrainte de R24, qui contient aussi les limites |
| T14 — montant = arrondi au centime de final_rate × H, H lu dans la vente (`schema-tracabilite-remuneration-chasseur_v4.md:96`) | `amount >= 0` ; H est sur `Sale` | partielle | **Coder** + **Décider** | trigger : `amount = round(final_rate * <H en euros>, 2)` ; H étant en K€ (T01), `<H en euros>` vaut `fees_amount * 1000` si l'unité est confirmée (X02) |
| X01 — contradiction : ancienneté et performance, clé du barème (BAREME) ou majorations du taux (NOTES) (`BAREME-COMMISSION.md:31` ; `NOTES-REMUNERATION-CHASSEUR.md:58`) | `seniority_rate`, `performance_rate` sur `Payment`, aucun niveau sur `CommissionScale` : le MPD suit NOTES | couverte | **Décider** (acter) | en place côté NOTES, qui se présente comme la version qui remplace ; reste à l'acter en équipe |

### CommissionScale

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| U10 — barème défini par tranches de montant (`00_regles_metier_mandat_remuneration.feature:52`) | `amount_min >= 0`, `amount_max > amount_min`, `chk_scale_amounts` | couverte | **Rien** | en place ; le contrôle sur `amount_max` fait doublon avec `chk_scale_amounts` |
| U11 — le barème change dans le temps et selon le chasseur (`00_regles_metier_mandat_remuneration.feature:53`) | `valid_from`, `valid_until`, `id_hunter`, `chk_scale_period` | couverte | **Rien** | en place |
| U12 — la part est celle de *la* tranche en vigueur pour ce montant, cette date, ce chasseur (`00_regles_metier_mandat_remuneration.feature:55`) | `excl_scale_no_overlap` et `excl_scale_global` : **au plus** une tranche par montant, date et chasseur | partielle | **Coder** | « **au moins** une » suppose des tranches et des périodes sans trou : trigger ou API, comme T04 |
| B02 — taux(chasseur, montant, date) (`BAREME-COMMISSION.md:20`) — côté barème | `rate`, par chasseur, tranche et période | couverte | **Rien** | en place |
| B03 — chaque tranche a son propre taux (`BAREME-COMMISSION.md:27`) | un `rate` par ligne | couverte | **Rien** | en place |
| B04 — le barème appliqué est celui en vigueur à la date de l'acte (`BAREME-COMMISSION.md:28`) | les dates existent ; rien ne vérifie que la ligne choisie par `Payment.id_commission_scale` couvre `Sale.signature_date`, ni que `Payment.base_rate` égale son `rate` | partielle | **Coder** | trigger à la création du paiement : `valid_from <= Sale.signature_date AND (valid_until IS NULL OR Sale.signature_date <= valid_until)`, même chasseur ou barème par défaut, et `base_rate = rate` |
| B05 — deux chasseurs, deux taux pour une même tranche et une même date (`BAREME-COMMISSION.md:29`) | `id_hunter WITH =` dans `excl_scale_no_overlap` : deux chasseurs différents ne se gênent pas | couverte | **Rien** | en place |
| B15 — tranche × date × chasseur → taux ; montant fixe « éventuellement » (`BAREME-COMMISSION.md:57`) | les trois axes et `rate` ; pas de montant fixe, qui est facultatif | couverte | **Rien** | en place |
| R13 — un seul taux pour la totalité des honoraires (`NOTES-REMUNERATION-CHASSEUR.md:44`) | une ligne de barème par paiement, un `rate` par ligne | couverte | **Rien** | en place |
| R14 — prix < 200 000 € → 30 % (`NOTES-REMUNERATION-CHASSEUR.md:48`) | `rate` accepte 0,30 ; `amount_max NUMERIC(6,1)` s'arrête à 99 999,9 : la limite 200 000 ne tient qu'en K€ (200,0) | partielle | **Décider** (unité, X02) | pas de contrainte : c'est une ligne de données à insérer ; l'unité des bornes est à décider — `Sale.purchase_amount`, en K€, garde ce type |
| R15 — 200 000 – 349 999 € → 35 % (`NOTES-REMUNERATION-CHASSEUR.md:49`) | comme R14 | partielle | **Décider** (unité, X02) | comme R14 ; en K€, la tranche s'écrit `[200,0 ; 350,0)` grâce au `'[)'` de l'exclusion |
| R16 — 350 000 – 499 999 € → 40 % (`NOTES-REMUNERATION-CHASSEUR.md:50`) | comme R14 | partielle | **Décider** (unité, X02) | comme R14 |
| R17 — 500 000 – 749 999 € → 45 % (`NOTES-REMUNERATION-CHASSEUR.md:51`) | comme R14 | partielle | **Décider** (unité, X02) | comme R14 |
| R18 — prix ≥ 750 000 € → 50 % (`NOTES-REMUNERATION-CHASSEUR.md:52`) | comme R14 ; un `amount_max` vide ouvre la tranche vers le haut | partielle | **Décider** (unité, X02) | comme R14 |
| R19 — barème daté, en vigueur à la date de l'acte (`NOTES-REMUNERATION-CHASSEUR.md:54`) | comme B04 | partielle | **Coder** | comme B04 |
| R20 — un barème nominatif passe avant le barème par défaut (`NOTES-REMUNERATION-CHASSEUR.md:54`) | les deux exclusions ne comparent jamais un nominatif à un défaut : les deux coexistent | couverte | **Rien** dans le MPD | en place ; choisir le nominatif d'abord se code dans l'API (étape 4) |
| R31 — clé (chasseur, période, tranche), chasseur vide = barème par défaut (`NOTES-REMUNERATION-CHASSEUR.md:91`) | `excl_scale_no_overlap` pour les nominatifs, `excl_scale_global … WHERE (id_hunter IS NULL)` pour le défaut | couverte | **Rien** | en place |
| T15 — tranche × date × chasseur nominatif facultatif (`schema-tracabilite-remuneration-chasseur_v4.md:38`) | comme R31 | couverte | **Rien** | en place |
| T16 — le chevauchement de barèmes est « déjà tranché » par contrainte, sans SQL (`schema-tracabilite-remuneration-chasseur_v4.md:70`) | les deux `EXCLUDE` donnent le SQL que les notes n'ont pas | couverte | **Rien** | en place ; `btree_gist` requis |
| X01 — contradiction : clé du barème ou majorations (`BAREME-COMMISSION.md:31` ; `NOTES-REMUNERATION-CHASSEUR.md:58`) — côté barème | aucune colonne de niveau | couverte | **Décider** (acter) | comme sous `Payment` |

**La période des barèmes.** Deux `EXCLUDE`, bien pensés :

- `excl_scale_no_overlap` sépare les chasseurs (`id_hunter WITH =`). Mais en
  SQL, `NULL = NULL` n'est pas « vrai » : deux barèmes par défaut
  (`id_hunter` vide) lui échapperaient.
- `excl_scale_global`, limitée à `id_hunter IS NULL`, bouche ce trou.
- Les montants sont en `'[)'` (fin exclue), ce qui colle aux tranches « moins
  de 200 000 » puis « 200 000 – 349 999 » ; les dates sont en `'[]'` (bornes
  incluses), comme T03 et T09.
- **Rien ne manque.**

### HunterPerformance

Seul le score est enregistré ; les indicateurs se jugent sur les données qui
servent à les calculer (voir le « Choix de rangement » en tête de partie).

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| U13 — délai signature → achat en semaines, arrondi à la semaine inférieure (`00_regles_metier_mandat_remuneration.feature:65`) | `Mandate.signature_date`, `Sale.signature_date` | couverte | **Rien** | en place ; c'est un calcul |
| U14 — mandat exclusif ou non (`00_regles_metier_mandat_remuneration.feature:66`) | `Mandate.is_exclusive` | couverte | **Rien** | en place |
| U15 — nombre de ventes réussies (`00_regles_metier_mandat_remuneration.feature:67`) | les lignes de `Sale` | couverte | **Rien** | en place |
| U16 — nombre de mandats signés (`00_regles_metier_mandat_remuneration.feature:68`) | `Mandate.signature_date` | couverte | **Rien** | en place |
| U17 — nombre de visites avant achat, moins il y en a, mieux c'est (`00_regles_metier_mandat_remuneration.feature:69`) | les lignes de `Visit` | couverte | **Rien** | en place |
| U43 — un mandat échu sans vente fait baisser les indicateurs (`07_chasseur_remuneration_et_performance.feature:41`) | la cause `'mandate_expired'` et `chk_perf_source`, qui exige le mandat ; rien ne compare au score précédent | partielle | **Coder** | trigger : le nouveau score du chasseur est inférieur ou égal au précédent — une comparaison entre deux lignes, impossible en `CHECK` |
| B06 — la performance se calcule sur 5 indicateurs (`BAREME-COMMISSION.md:35`) | les données des cinq existent (voir U13 à U17) | couverte | **Rien** | en place |
| B07 — délai signature → acte, arrondi à la semaine inférieure, plus court = mieux (`BAREME-COMMISSION.md:39`) | comme U13 | couverte | **Rien** | en place |
| B08 — l'exclusivité améliore la performance (`BAREME-COMMISSION.md:40`) | comme U14 | couverte | **Rien** | en place |
| B09 — plus de ventes réussies = mieux (`BAREME-COMMISSION.md:41`) | comme U15 | couverte | **Rien** | en place |
| B10 — plus de mandats signés = mieux (`BAREME-COMMISSION.md:42`) | comme U16 | couverte | **Rien** | en place |
| B11 — moins de visites avant achat = mieux (`BAREME-COMMISSION.md:43`) | comme U17 | couverte | **Rien** | en place |
| B12 — recalcul à la hausse quand un paiement est effectué (`BAREME-COMMISSION.md:47`) | la cause `'payment'` et `chk_perf_source` ; rien n'exige un paiement `'paid'`, ni ne compare au score précédent | partielle | **Coder** | trigger : paiement `'paid'` et score supérieur ou égal au précédent |
| B13 — recalcul à la baisse à l'échéance sans vente (`BAREME-COMMISSION.md:48`) — côté performance | comme U43 | partielle | **Coder** | comme U43 |
| B14 — score recalculé et enregistré à chaque événement (`BAREME-COMMISSION.md:56`) | trois causes, une période par ligne, `excl_perf_no_overlap` ; mais `'[]'` et `valid_until > valid_from` imposent au moins deux jours d'écart entre deux scores d'un même chasseur | partielle | **Décider** | `valid_until >= valid_from` ramène l'écart à un jour ; deux événements le même jour demandent une période avec l'heure (`tsrange`) — T07 et T09 sont écrites ainsi par la note la plus récente |
| R07 — score de 0 à 100, moyenne pondérée de 5 critères (`NOTES-REMUNERATION-CHASSEUR.md:30`) | `score BETWEEN 0 AND 100` ; la pondération se calcule | couverte | **Rien** | en place |
| R08 — délai, poids 25 %, paliers de ≤ 12 semaines : 100 à > 48 : 0 (`NOTES-REMUNERATION-CHASSEUR.md:35`) | comme U13 | couverte | **Rien** | en place ; paliers et poids sont des paramètres |
| R09 — exclusivité, poids 10 %, 100 ou 60 (`NOTES-REMUNERATION-CHASSEUR.md:36`) | comme U14 | couverte | **Rien** | en place |
| R10 — ventes sur les 12 derniers mois, poids 25 %, min(100 ; ventes × 20) (`NOTES-REMUNERATION-CHASSEUR.md:37`) | comme U15 ; la date est `Sale.signature_date` | couverte | **Rien** | en place |
| R11 — mandats sur les 12 derniers mois, poids 15 %, min(100 ; mandats × 10) (`NOTES-REMUNERATION-CHASSEUR.md:38`) | comme U16 | couverte | **Rien** | en place |
| R12 — visites, poids 25 %, paliers de ≤ 3 : 100 à > 15 : 0 (`NOTES-REMUNERATION-CHASSEUR.md:39`) | comme U17 | couverte | **Rien** | en place |
| T05 — score de 0 à 100 à une décimale, `NUMERIC(4,1)` (`schema-tracabilite-remuneration-chasseur_v4.md:48`) | `score NUMERIC(4,1) CHECK (score BETWEEN 0 AND 100)` — identique | couverte | **Rien** | en place |
| T06 — trois causes : `initial`, `payment`, `mandate_expired` (`schema-tracabilite-remuneration-chasseur_v4.md:52`) | `trigger_type IN ('initial', 'payment', 'mandate_expired')` — identique | couverte | **Rien** | en place |
| T07 — fin de validité vide ou après le début (`schema-tracabilite-remuneration-chasseur_v4.md:55`) | `chk_perf_period` — identique | couverte | **Rien** | en place ; voir B14 |
| T08 — la cause fixe la source (`schema-tracabilite-remuneration-chasseur_v4.md:56-59`) | `chk_perf_source` — identique | couverte | **Rien** | en place |
| T09 — pour un chasseur, pas de périodes qui se chevauchent, bornes incluses (`schema-tracabilite-remuneration-chasseur_v4.md:61-64, :70`) | `excl_perf_no_overlap` — identique | couverte | **Rien** | en place ; `btree_gist` requis ; voir B14 |

**La période des scores.** `excl_perf_no_overlap` fonctionne : `id_hunter`
n'est jamais vide ici, donc le problème du `NULL` de `CommissionScale` ne se
pose pas. Le souci vient de sa combinaison avec `chk_perf_period` : voir B14.

### ParametersFees

| règle (source) | ce que le MPD contient | verdict | à faire | SQL proposé / détail |
|---|---|---|---|---|
| U08 — honoraires = montant fixe + pourcentage du montant de l'achat (`00_regles_metier_mandat_remuneration.feature:47`) | `fixed_amount CHECK (fixed_amount > 0)`, `rate CHECK (rate >= 0 and rate <= 1)` | couverte | **Rien** | en place |
| U25 — le client paie ces honoraires en plus de l'achat (`03_particulier_offre_et_signature.feature:34`) | comme U08 | couverte | **Rien** | en place |
| B01 — base = montant fixe + pourcentage × montant d'achat (`BAREME-COMMISSION.md:12`) — côté paramètres | comme U08 | couverte | **Rien** | en place ; le calcul se juge sous `Sale` |
| R05 — H = montant fixe + pourcentage × prix d'achat (`NOTES-REMUNERATION-CHASSEUR.md:26`) — côté paramètres | comme U08 | couverte | **Rien** | comme B01 |
| R28 — exemple : fixe 3 000 €, pourcentage 2,5 % (`NOTES-REMUNERATION-CHASSEUR.md:74`) | 3 000 tient dans `NUMERIC(6,1)` en euros comme en K€ (3,0) ; 0,025 tient dans `NUMERIC(5,4)` | couverte | **Rien** | en place ; l'unité de `fixed_amount` doit suivre celle de `Sale.fees_amount` (X02) |
| R30 — fixe et pourcentage datés (`NOTES-REMUNERATION-CHASSEUR.md:90`) | `valid_from`, `valid_until` | couverte | **Rien** | en place |
| T02 — H calculé avec les paramètres en vigueur à la signature (`schema-tracabilite-remuneration-chasseur_v4.md:19`) — côté paramètres | `excl_fees_no_overlap` ; aucun lien avec `Sale` | partielle | **Coder** | comme sous `Sale` |
| T03 — pas de périodes qui se chevauchent, bornes incluses (`schema-tracabilite-remuneration-chasseur_v4.md:28-31`) | `excl_fees_no_overlap EXCLUDE USING gist (daterange(valid_from, valid_until, '[]') WITH &&)` — identique | couverte | **Rien** | en place ; pas besoin de `btree_gist` ici |
| T04 — toujours exactement une ligne de paramètres (`schema-tracabilite-remuneration-chasseur_v4.md:21`) — côté paramètres | **au plus** une | partielle | **Coder** | comme sous `Sale` |

**La période des paramètres.** L'exclusion porte sur la période seule : c'est
juste, les paramètres valent pour tout le monde. Mais il manque la contrainte
« fin après début » que `CommissionScale` et `HunterPerformance` ont :

- une période à l'envers est bien refusée, mais seulement parce que
  `daterange` plante, avec un message peu clair ;
- `CHECK (valid_until IS NULL OR valid_until >= valid_from)` donnerait une
  erreur claire et nommée. Proposé sur le modèle de T07 : aucune source ne
  l'écrit. → **Ajouter** (facultatif).

### Contraintes du MPD qu'aucune règle ne demande — six tables

Comme pour la première partie : **pas fausses, à garder**. Deux d'entre elles
méritent une retouche, signalée.

- **`Mandate`** — `reference` non vide, sans espace en bord ;
  `signature_type IN ('electronic', 'paper')` ; les statuts `'active'`,
  `'completed'`, `'canceled'` (`'expired'` et `'renewed'`, eux, s'appuient sur
  U42 et U07).
- **`Sale`** — `purchase_amount > 0` ; `chk_fees_lower_than_price`.
- **`Payment`** — le statut `'announced'` ; `amount >= 0`, qui accepte un
  paiement à zéro alors que T01 (H > 0) et R21 (taux ≥ 20 %) l'excluent.
- **`CommissionScale`** — `amount_min >= 0` ; `rate >= 0`, qui accepte un taux
  nul que `Payment.base_rate > 0` (T10) refuse ensuite : `rate > 0`
  mettrait les deux d'accord.
- **`ParametersFees`** — `fixed_amount > 0` et les limites de `rate` : U08
  demande le fixe et le pourcentage, pas leurs limites.

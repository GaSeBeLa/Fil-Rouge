# À faire après le chantier SUG — 2026-11-03

Le chantier SUG (moteur de suggestion de biens) est **clos et poussé**.
Ce fichier liste ce qui reste à faire **par le groupe**, dans l'ordre.

- Dépôt API : `GaSeBeLa/Fil-Rouge-API`, jusqu'à `f3fd402`
- Dépôt docs : `GaSeBeLa/Fil-Rouge`, jusqu'à `f2733b4` (le chantier RGP, après, n'a pas touché au schéma)
- Suite de tests : **1070 passed, 7 xfailed**

---

## 1. Chacun, après le pull

La base gagne deux migrations (50 et 51). Il faut recréer sa base locale.

⚠️ Cela **efface la base de dev locale**.

Depuis `../Fil-Rouge-API/docker/` :

```bash
docker compose down -v && docker compose up -d
```

Puis depuis `../Fil-Rouge-API/` :

```bash
bash docker/create_test_db.sh
```

---

## 2. Sur Confluence : les changements du schéma (MPD), dans l'ordre

Deux tables changent.
Aucune table créée, aucune supprimée.
Référence : `docker/init-v3/01_create_fil_rouge_immobilier.sql` (dépôt API).

### Le texte à recopier dans le MPD — vérifié le 2026-11-03

Comparé par script à l'export `vrac/mpd 03 11.drawio.xml` (Seb, 03/11/2026) :
**22 tables** de chaque côté, et **il ne manque que ces 7 lignes**. Tout le
reste (PRF, `estate_price_history`, `estate_contact`…) y est déjà.

Chaque ligne : à gauche, le nom de la colonne ; à droite, son texte, comme
les autres lignes du MPD.

**Table `Estate_SearchRequest`** — 1 ligne à ajouter, après `id_hunter`,
avant la ligne `CONSTRAINT` :

| Nom | Texte |
|---|---|
| `status` | `VARCHAR(20) NOT NULL DEFAULT 'suggested' CHECK (status IN ('suggested', 'kept', 'dismissed'))` |

**Table `EstateProposed`** — 3 lignes à ajouter, juste après `client_priority` :

| Nom | Texte |
|---|---|
| `client_decision` | `VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (client_decision IN ('pending', 'interested', 'declined'))` |
| `client_decided_at` | `TIMESTAMP` |
| `decline_reason` | `VARCHAR(20) CHECK (decline_reason IN ('too_expensive', 'too_far', 'too_small', 'wrong_type', 'other'))` |

**Table `EstateProposed`** — la ligne `CONSTRAINT` : ajouter à la fin, après
`chk_offer …`, ces 3 contraintes :

```text
, CONSTRAINT chk_decline_reason_if_declined CHECK (decline_reason IS NULL OR client_decision = 'declined'), CONSTRAINT chk_decided_at_once_decided CHECK (client_decision = 'pending' OR client_decided_at IS NOT NULL), CONSTRAINT chk_offer_needs_interest CHECK (proposition_status = 'proposed' OR client_decision = 'interested')
```

- Aucune relation ne change : pas de flèche à ajouter ni à retirer.
- Pour revérifier après la mise à jour : déposer le nouvel export dans `vrac/`
  et demander la comparaison ; elle doit dire « 22 tables, 22 swimlanes », sans
  aucun écart.

✅ Fait par Seb le 2026-11-03 : l'export `vrac/mpd 33 11 2.drawio.xml`,
recomparé, donne 22 tables et **0 écart**.

### Le texte à recopier dans le MLD — vérifié le 2026-11-03

Comparé par script à l'export `vrac/mld 03 11.drawio.xml` : **22 tables**
de chaque côté. Il manque **4 lignes**, toutes de SUG. Le MLD ne porte ni
`CHECK` ni contrainte : les 3 contraintes du MPD n'y vont pas.

**Table `Estate_SearchRequest`** — 1 ligne, après `id_hunter` :

| Nom | Type |
|---|---|
| `status :` | `String` |

**Table `EstateProposed`** — 3 lignes, juste après `client_priority` :

| Nom | Type |
|---|---|
| `client_decision :` | `String` |
| `client_decided_at :` | `DateTime` |
| `decline_reason :` | `String` |

- Aucune relation ne change.
- 💡 Facultatif : dans `Hunter` et `SearchRequest`, le MLD écrit
  `id_realEstateManager` ; le SQL dit `id_realestatemanager` (tout en
  minuscules, comme PostgreSQL le range).

Le détail, point par point :

### 1️⃣ `estate_searchrequest` : ajouter `status`

- **Type** : `VARCHAR(20) NOT NULL DEFAULT 'suggested'`
- **Valeurs** : `'suggested'`, `'kept'`, `'dismissed'`
- **Raison** : le moteur propose un bien avant que le chasseur l'ait choisi.
- **En clair** : la sélection devient un panier à trois cases.
  - « suggéré » : la machine le propose ;
  - « gardé » : le chasseur le valide ;
  - « écarté » : non merci.
  - Seul un bien **gardé** se montre au client.
- **Migration** : `50_etat-de-la-selection.sql` (les lignes déjà là passent à `'kept'`)

### 2️⃣ `estate_proposed` : ajouter `client_decision`

- **Type** : `VARCHAR(20) NOT NULL DEFAULT 'pending'`
- **Valeurs** : `'pending'`, `'interested'`, `'declined'`
- **Raison** : on ne savait pas ce que le client pensait d'un bien proposé.
- **En clair** : « pas encore répondu », « ça m'intéresse », « non merci ».

### 3️⃣ `estate_proposed` : ajouter `client_decided_at`

- **Type** : `TIMESTAMP`, vide tant que le client n'a rien dit
- **Raison** : savoir **quand** il a répondu.
- **En clair** : la date de sa dernière réponse (pas l'historique).

### 4️⃣ `estate_proposed` : ajouter `decline_reason`

- **Type** : `VARCHAR(20)`, vide sauf en cas de refus
- **Valeurs** : `'too_expensive'`, `'too_far'`, `'too_small'`, `'wrong_type'`, `'other'`
- **Raison** : savoir **pourquoi** il refuse, pour mieux chercher ensuite.
- **En clair** : trop cher, trop loin, trop petit, pas le bon type, autre.

### 5️⃣ `estate_proposed` : contrainte `chk_decline_reason_if_declined`

- **Règle** : `decline_reason IS NULL OR client_decision = 'declined'`
- **En clair** : une raison de refus, seulement si on a refusé.

### 6️⃣ `estate_proposed` : contrainte `chk_decided_at_once_decided`

- **Règle** : `client_decision = 'pending' OR client_decided_at IS NOT NULL`
- **En clair** : dès que le client répond, la date est obligatoire.

### 7️⃣ `estate_proposed` : contrainte `chk_offer_needs_interest`

- **Règle** : `proposition_status = 'proposed' OR client_decision = 'interested'`
- **Raison** : pas d'offre d'achat sans client intéressé.
- **En clair** : pour aller plus loin que « proposé », le client doit avoir dit « ça m'intéresse ».

Les points 2 à 7 viennent de la migration `51_decision-du-client.sql`.
Les offres déjà en base y passent à `'interested'`, datées de leur création.

---

## 3. À trancher : faut-il un ADR pour ces règles ?

Elles sont codées dans l'API, **sans changer le schéma**.
Le groupe décide si elles méritent un ADR sur Confluence.

- **M1** : un mandat ne se signe pas sans critères → `409`.
- **Dépôt de demande** : il crée tout de suite ses critères (budget max et type de bien).
- **P19** : on ne propose au client qu'un bien **gardé**.
- **PUT du client** : il ne change que sa note, son commentaire et sa décision.
- **L'offre** : `POST /estate-proposed/{id}/offer`, par le client du mandat.
- **Les suggestions** : `POST /search-requests/{id}/suggestions`, par le chasseur de la demande.
  - 10 biens au plus ;
  - jamais un bien vendu, jamais un bien déjà vu ;
  - Elasticsearch en panne → `503`, rien n'est écrit.

---

## 4. À trancher : les idées de chantiers suivants

Aucune n'est encore dans la TODO (`context AI/08-etat.md`).
Une idée y entre avec deux oui.

- **A. Indexer les critères oubliés** — 🟡 environ 3 fiches
  - balcon, terrasse, étage, piscine, vue… sont ignorés par la recherche ;
  - les ajouter à l'index `estates`, puis à la requête.
- **B. Tester avec un vrai Elasticsearch** — 🟢 1 à 2 fiches
  - les tests de SUG8 tournent sur un faux ;
  - un test contre le vrai conteneur protège la démo.
- **C. Le refus du client nourrit la recherche** — 🟡 2 à 3 fiches
  - après plusieurs refus du même motif, proposer de nouveaux critères ;
  - touche au futur parcours IA.
- **D. Démo du parcours de suggestion** — 🟢 1 à 2 fiches
  - étendre `seed_demo.py` : demande → suggérés → gardé → proposé → intéressé → offre.
- **E. Merise en petits schémas** — déjà dans la TODO (n° 6, Livrable 2).

**Avis** : B d'abord, puis D pour l'oral, puis A. C attend la discussion sur le parcours IA.

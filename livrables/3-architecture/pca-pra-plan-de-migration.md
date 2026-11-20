# PCA, PRA et plan de migration

> **Brouillon de Gabriel du 2026-11-19, relu et complété par le Glaude le même jour** (chiffres recomptés, test de restauration joué, `restart:` posé). À relire par l'équipe. Phase 3 du sujet
> (`SP/Readme.md:248`), bloc BC02. Modèle suivi :
> `SP/documents utiles/PCA-PRA-MIGRATION.md`.
>
> Statuts : ✅ établi (lu dans le code ou mesuré) · 🟡 à décider ou à valider
> par le Product Owner · 💡 proposé · ⚠️ trou connu.
>
> Sources : `Fil-Rouge-API` (`docker/docker-compose.yml`, `docker/init-v3/`,
> `docker/migrations/v2-vers-v3/`, `API/README.md`) ; `Fil-Rouge`
> (`livrables/3-architecture/`, ADR-046, ADR-061) ; Confluence (notes
> « Éco-conception », « 3V », « RGPD »).

## 0. Ce que le projet a vraiment aujourd'hui

À lire avant le reste : ce document décrit un plan, pas une exploitation en
place.

| Fait | Statut |
|---|---|
| Sauvegarde quotidienne codée le 2026-11-20 : DAG `db_backup` (dépôt `Fil-Rouge-API`, commit `83b7c0d`, 2026-11-20), chaque nuit à 1 h, base + rôles sans mot de passe dans MinIO (bucket `backup`), 7 jours gardés. Restauration éprouvée dans une base à part : mêmes comptes (3 219 biens, 539 comptes, 501 ventes, 22 tables). ⚠️ MinIO est sur la même machine : pas de copie hors site, ni de journaux WAL | ✅ / ⚠️ |
| Un test de restauration a été joué **une fois, à la main**, le 2026-11-19 : 0 écart sur 28 tables (§ 2.4). Rien ne l'automatise | ✅ / ⚠️ |
| `db` et `api` redémarrent seuls après un plantage (`restart: unless-stopped`, posé le 2026-11-19, `Fil-Rouge-API` `557964d` ; crash simulé : relancé seul, `GET /` en `200`) | ✅ |
| Une seule instance de chaque service ; Elasticsearch en 1 shard, 0 réplique (`mapping.py`) | ✅ |
| `docker/.env` (mots de passe, `JWT_SECRET`, clés d'API) n'est pas dans git : un poste perdu perd les secrets | ⚠️ |
| Le code, les migrations, les schémas et le tableau de bord Kibana sont dans git | ✅ |
| Les politiques de fréquence et de rétention des sauvegardes sont écrites (note d'éco-conception) | ✅ |
| Reconstruire une base vide et semée prend quelques secondes (`healthy` après 6 s, mesuré le 2026-10-07) | ✅ |

## 1. PCA — continuer pendant un incident

### 1.1 Activités critiques

| Activité | Si elle s'arrête | Secours | Statut |
|---|---|---|---|
| Se connecter, appeler l'API (`api` + `db`) | Plus personne ne travaille : chasseurs, clients, managers | Redémarrage automatique (`restart: unless-stopped`) ; vérifier `/` et `pg_isready` | ✅ posé le 2026-11-19 |
| Mandats, propositions, ventes, paiements (`db`) | Perte d'engagements juridiques et financiers | Sauvegarde horaire (§ 2.2) | 💡 à mettre en place |
| Calcul du paiement (`POST /sales/{id}/payment`) | Rémunérations retardées, rien de perdu | Rejouable : une vente, un paiement, `409` au second appel | ✅ |
| Recherche de biens (`elasticsearch`) | `GET /estates/search` répond `503` ; le reste de l'API marche | Index refait par le DAG de 4 h (ADR-061) | ✅ |
| Import des annonces (Airflow, 2 h) | Catalogue pas à jour le lendemain | Rejouer le DAG (`airflow dags test …`) ; un rejet va en `quarantine` | ✅ |
| OLAP et Kibana (3 h, `elk`) | Tableaux de bord vides | Reconstructible : l'OLAP se recalcule, le tableau de bord est dans git | ✅ |

### 1.2 Ce qui se refait, ce qui ne se refait pas

| Donnée | Refaisable ? | Conséquence |
|---|---|---|
| PostgreSQL (`db_data`) | ❌ source de vérité | Seule à sauvegarder avec soin |
| Index `estates`, schéma `olap`, bucket `gold` | ✅ en une nuit | Pas de sauvegarde (ADR-061) |
| MinIO `bronze` | ✅ regénérable depuis le générateur | Pas de sauvegarde (éco-conception) |
| Logs (`logs-api-*`) | ❌ mais sans valeur métier | Gardés 6 mois (RGPD-11) |
| Secrets (`docker/.env`) | ❌ | 💡 coffre de mots de passe de l'équipe, hors git |

### 1.3 RTO et RPO

🟡 **Valeurs proposées par l'équipe**, à faire valider par le Product Owner :
le sujet n'en donne aucune.

| Donnée | RPO (perte tolérée) | RTO (reprise) | Lien |
|---|---|---|---|
| Contractuel et financier : `mandate`, `estate_proposed`, `sale`, `payment`, `visit` | **1 h** | **4 h** | Éco-conception : tranche horaire. ⚠️ Cette note (11 tables) ne cite pas `sale`, `payment` ni `visit` : à y ajouter |
| Demandes et critères : `search_request`, `criteria` | **12 h** | 4 h | Tranche 12 h |
| Référentiels : comptes, fiches, `estate` | **24 h** | 8 h | Tranche 24 h |
| Index, OLAP, MinIO `gold` | sans objet | **24 h** (une nuit) | Refait par les DAG |

Deux limites à dire :
- 🟡 Le RTO suppose une base petite. La note 3V prévoit de 22 à 133 Go après
  2 ans : restaurer 133 Go prend des heures, pas des minutes. À ce volume,
  une restauration complète ne tient plus 4 h ; il faudra une réplique
  de secours (§ 4).
- 💡 Sur PostgreSQL, la fréquence « par table » de l'éco-conception se règle
  mal avec `pg_dump`. Proposition : **une sauvegarde complète par jour**
  (tranche 24 h) **plus l'archivage continu des journaux de transactions
  (WAL)**, qui donne un RPO de quelques minutes pour toutes les tables. Les
  durées de l'éco-conception (7, 30, 90 jours) deviennent la rétention.

## 2. PRA — repartir après un sinistre

### 2.1 Scénarios

| Scénario | Exemple | Procédure |
|---|---|---|
| A. Un service tombe | `api` plante | Redémarrer le conteneur ; lire les logs (`docker compose logs api`) |
| B. Volume de base perdu ou corrompu | `docker compose down -v` par erreur (⚠️ efface la base de dev, `API/README.md`) | Procédure § 2.2 |
| C. Machine détruite | Poste ou serveur perdu | Cloner les deux dépôts, retrouver `.env`, restaurer § 2.2 |
| D. Mauvaise écriture | Un `PUT` ou un script écrase des lignes | Restauration à un instant donné (WAL), sur une base temporaire, puis recopie des lignes |
| E. Compromission | Clé d'API ou jeton volé | Changer `JWT_SECRET` (tous les jetons **et tous les codes d'activation** deviennent invalides) et les `API_KEY_*` ; relire les logs Kibana |

### 2.2 Procédure de reprise (scénarios B et C)

1. **Détecter et qualifier** : `pg_isready`, `docker compose ps`, logs. Noter
   l'heure du dernier état sain.
2. **Isoler** : arrêter `api` (`docker compose stop api`) pour qu'aucune
   écriture n'arrive pendant la restauration. Arrêter aussi les DAG.
3. **Retrouver les secrets** : `docker/.env` depuis le coffre (💡).
4. **Recréer la base** : `docker compose up -d db`. Sur un volume neuf,
   `init-v3/` recrée le schéma, les rôles et le semis de départ.
5. **Restaurer** la dernière sauvegarde saine (complète), puis rejouer les WAL
   jusqu'à l'instant voulu. ⚠️ `pg_dump` ne sauvegarde **pas les rôles**
   PostgreSQL (`fil_rouge_reader`) : ce sont des objets du serveur, pas de la
   base. Les garder à part (`pg_dumpall --globals-only`), ou les recréer par
   `init-v3/04` sur un volume neuf.
6. **Vérifier l'intégrité** :
   - comptage des lignes par table, comparé à la sauvegarde ;
   - `pytest` : la suite (1 116 tests réussis au 2026-11-19, commit `31094a8`) contrôle les règles et les
     contraintes. ⚠️ Ses tests d'intégration tournent sur `fil_rouge_test`,
     pas sur la base restaurée : pour juger la copie, il faut les y pointer ;
   - `POST /auth/login` et `GET /auth/me` répondent.
7. **Rejouer les effacements RGPD** (voir § 2.3) avant de rouvrir.
8. **Remettre en ligne** : `docker compose up -d api`, puis les DAG ; l'index
   et l'OLAP se refont à la nuit suivante, ou à la main.
9. **Communiquer** : prévenir le Product Owner et les chasseurs ; écrire
   l'incident au journal (ADR si une règle change).

### 2.3 Le piège RGPD de la restauration

⚠️ Une sauvegarde plus ancienne contient des personnes déjà **anonymisées**
depuis (`POST /users/{id}/anonymize`, ADR-049). La restaurer les ressuscite.
Or la page RGPD note que **la date d'effacement n'est pas gardée** (RGPD-14,
v2). Donc :

- 💡 tenir hors de la base une liste des comptes effacés (id et date), à
  rejouer après toute restauration ;
- une sauvegarde restaurée garde aussi les **codes d'activation** encore valides
  (7 jours) : changer `JWT_SECRET` après une restauration les annule tous ;
- les sauvegardes sont elles-mêmes des données personnelles : leur rétention
  maximale (90 jours, éco-conception) est le délai pendant lequel un effacement
  reste présent dans une copie. À écrire au registre RGPD.

### 2.4 Test de la reprise

> Une sauvegarde jamais restaurée n'est pas une sauvegarde (`SP/PCA-PRA-MIGRATION.md`).

✅ **Joué le 2026-11-19**, à la main, sur une base jetable (`fil_rouge_restauration`), supprimée à la fin. La base de dev n'a été que **lue**.

| Étape | Mesure | Résultat |
|---|---|---|
| Sauvegarde complète de la base de dev (`pg_dump -Fc`, 57 Mo sur disque) | **0,96 s** ; fichier de **573 Ko** (compressé) | ✅ |
| Sauvegarde des rôles (`pg_dumpall --globals-only`) | 1 Ko, **3** `CREATE ROLE` | ✅ |
| Restauration dans `fil_rouge_restauration` (`pg_restore`) | **2,82 s** : c'est le **RTO mesuré** de la base seule | ✅ |
| Comptage par table, source contre copie (`public` et `olap`) | **28 tables, 18 246 lignes, 0 écart** | ✅ |
| Index, droits du lecteur, politiques par ligne | 67 index des deux côtés ; `fil_rouge_reader` lit `estate`, pas `payment` ; 4 politiques des deux côtés | ✅ |
| `pytest` d'intégration sur la copie | ⏭️ **non joué** : les tests fabriquent leurs propres lignes sur `fil_rouge_test` et ne jugent pas une copie ; le comptage et les droits ci-dessus font la preuve | — |

- Les durées comprennent le lancement de `docker compose exec` : la restauration seule est plus courte.
- La copie fait **15 Mo**, contre **57 Mo** pour la base de dev : la base de dev garde des pages mortes (des essais annulés) ; une restauration les compacte.
- ⚠️ Au volume de la note 3V (22 à 133 Go), ces secondes deviennent des heures (§ 1.3).

Les commandes, depuis `Fil-Rouge-API/docker/` (sous Git Bash, préfixer par `MSYS_NO_PATHCONV=1`, sinon `/tmp` devient un chemin Windows) :

```bash
docker compose exec -T db pg_dump -U postgres -Fc -d fil_rouge_immobilier -f /tmp/sauvegarde.dump
docker compose exec -T db pg_dumpall -U postgres --globals-only -f /tmp/roles.sql
docker compose exec -T db createdb -U postgres fil_rouge_restauration
docker compose exec -T db pg_restore -U postgres -d fil_rouge_restauration /tmp/sauvegarde.dump
docker compose exec -T db dropdb -U postgres fil_rouge_restauration
```

## 3. Plan de migration — de l'ancien au nouveau SI

### 3.1 Point de départ et d'arrivée

| | Avant | Après |
|---|---|---|
| Base | `Fil_Rouge_Depart` : 3 tables, `secteurs` (10), `utilisateurs` (24 : 6 chasseurs, 18 clients), `mandats` (18), critères en texte libre dans `description_recherche` | PostgreSQL v3 : 22 tables, 5 rôles |
| Backend | code perdu, développeur absent | `Fil-Rouge-API` (FastAPI) |
| Données reprises | les 3 tables ci-dessus, plus 2 556 annonces (CSV du sujet) | 25 comptes (dont 1 manager placeholder), 18 demandes, 18 critères, 18 mandats, 2 556 biens, 1 976 photos |

Le mandat 13 (son client était un chasseur) est écarté par v2, puis rattaché
à une vraie cliente par la migration 10 (LOT10) : 17 mandats en v2, 18 en v3.

### 3.2 Stratégie : big bang sur les données ✅

| Option | Verdict |
|---|---|
| **Big bang** : on migre tout d'un coup | **Retenue**. Le volume est minuscule (quelques dizaines de lignes métier) ; l'ancien backend n'est plus exploitable, donc **aucun fonctionnement en parallèle n'est possible** |
| Progressive, par lots | Écartée aujourd'hui. À reprendre **pour l'expansion** : un pays à la fois, quand les rachats arriveront |

Le site web et l'application métier restent (`SP/Readme.md:210`) : leurs
développeurs doivent pointer vers la nouvelle API (route, clé d'API, jeton)
**le jour de la bascule**. 🟡 La date reste à fixer avec eux.

### 3.3 Étapes

| # | Étape | Action | Vigilance | Retour arrière |
|---|---|---|---|---|
| 1 | **Préparation** | Figer l'ancien schéma ; sauvegarder la source ; arrêter les DAG | La source n'est **jamais modifiée** (ADR-046) | Rien n'a changé |
| 2 | **Extraction** | Lire `Fil_Rouge_Depart` (fixtures du sujet) | Anomalies de l'audit : un chasseur enregistré client (mandat 13), 6 mandats « actifs » échus au 25/07/2026 | Sans effet |
| 3 | **Création** | `init-v2/01` (schéma) | Ordre des clés étrangères : `real_estate_manager` avant `hunter` | Supprimer la base neuve |
| 4 | **Transformation et chargement v2** | `init-v2/02` (données), `03` (biens) | Euros et non K€ ; manager placeholder (user 25) pour les 6 chasseurs ; `hire_date` = date de création du compte | Idem |
| 5 | **Passage v2 → v3** | Les **50 migrations** `docker/migrations/v2-vers-v3/` par ordre de nom (de `03` à `53`, compté le 2026-11-19) | Chacune a son `COMMIT` (50 sur 50) ; plusieurs **s'arrêtent d'elles-mêmes** si le comptage ne correspond pas | Une migration échouée annule sa transaction ; reprendre à son numéro |
| 6 | **Vérification** | `test_banc_v2_v3.py` : base migrée comparée à une base neuve de `init-v3/` (colonnes, contraintes, index, triggers, fonctions, nombre de lignes) | `1 passed` (mesuré à 9,2 s le 2026-10-14) ; sinon le diff | Ne pas basculer |
| 7 | **Comptages** | Lignes avant/après, table par table (§ 3.1) | Aucune donnée perdue | Ne pas basculer |
| 8 | **Bascule** | Rouvrir l'API ; créer l'Admin (`create_admin`) ; relancer les DAG | Fenêtre hors 2 h à 4 h (imports de nuit) | Voir ci-dessous |

**Retour arrière** : avant l'étape 8, il suffit d'abandonner la base neuve ;
l'ancienne n'a pas bougé. Après la bascule, deux filets : (1) la sauvegarde
complète prise juste avant, (2) l'ancienne base gardée en lecture seule
pendant une période à fixer (🟡).

### 3.4 Ce que la migration ne fait pas et qu'il faut dire

- ✅ **Les 25 comptes repris** (24 personnes et le manager placeholder) ont un
  mot de passe factice (`MIGRATED_PLACEHOLDER_MUST_RESET`), pas une empreinte
  argon2 : ils ne peuvent pas se connecter tels quels. Depuis le 2026-11-19
  (`Fil-Rouge-API` `6755600`), chacun choisit **son** mot de passe :
  l'Admin demande un code (`POST /users/{id}/activation-code`, 7 jours), la
  personne l'envoie avec son mot de passe (`POST /auth/activate`). Personne
  d'autre ne connaît ce mot de passe. Un compte effacé reste refusé.
  ⚠️ Sans serveur d'email, le code se transmet à la main.
- Valeurs **factices documentées** (ADR-046) : adresse « non renseigné » et
  code postal `00000` pour 18 clients, téléphone `+33000000000`, manager
  placeholder. Elles sont à remplacer par les vraies quand l'entreprise
  les fournit.
- `docker compose down -v` détruit la base et ses comptes : ne jamais le
  lancer sur autre chose qu'une base de dev.

## 4. Pour l'expansion (hors périmètre aujourd'hui)

| Besoin | Piste | Lien |
|---|---|---|
| RTO tenu à 22 – 133 Go | Réplique PostgreSQL en lecture, promue en cas de panne | Note 3V § 6 |
| Plusieurs pays | Migration progressive, un pays à la fois | § 3.2 |
| Disponibilité | Plus d'une instance de `api`, derrière un répartiteur | Dossier d'architecture |

## 5. À décider

1. 🟡 RTO et RPO du § 1.3, par le Product Owner.
2. 💡 Sauvegarde complète quotidienne + WAL, ou rester sur les tranches par
   table de l'éco-conception ?
3. 💡 Où garder `docker/.env` et la liste des comptes effacés.
4. 🟡 Date de bascule du site et de l'application métier.
5. 🟡 Durée de garde de l'ancienne base en lecture seule.
6. ✅ `restart: unless-stopped` posé sur `db` et `api` (2026-11-19). ✅ Sauvegarde
   quotidienne planifiée le 2026-11-20 (DAG `db_backup`). 💡 Reste : une
   copie hors site et l'archivage des journaux WAL.

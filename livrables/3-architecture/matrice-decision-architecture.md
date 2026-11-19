# Matrice de décision d'architecture

> Phase 3, BC01 : « Comprendre avantages et inconvénients de chaque
> architecture (performance, scalabilité, sécurité, éco-conception) pour
> recommander la solution adaptée » → « Matrice de décision d'architecture
> (critères pondérés) » (`SP/documents utiles/TRACABILITE-COMPETENCES.md:37`).
> Modèle suivi : `SP/documents utiles/MATRICE-DECISION.md`.
>
> Brouillon du 2026-11-19, à relire par l'équipe. Elle s'appuie sur la note 3V
> (`note-dimensionnement-3v.md`), le schéma OLAP (`../2-modelisation/olap.md`)
> et les ADR 059 à 064. Le dossier qui la commente :
> [`dossier-architecture.md`](dossier-architecture.md).
>
> Statuts : ✅ établi (lu ou mesuré) · 🟡 à décider · 💡 proposé.

## 1. Les options comparées

| Option | Ce que c'est |
|---|---|
| **A. Une base, tout dedans** | Le métier et l'analyse lisent les mêmes tables ; pas de schéma d'analyse |
| **B. OLTP + OLAP dans la même instance PostgreSQL** | Les 22 tables du métier, plus un schéma `olap` en étoile (6 tables) recalculé chaque nuit ; Elasticsearch en copie pour la recherche |
| **C. OLTP + entrepôt séparé** | Le même découpage, mais l'analyse dans un autre moteur, sur une autre machine (un entrepôt en colonnes) |
| **D. Microservices** | Un service et une base par domaine (comptes, mandats, biens, paiements) |

✅ **B est ce que le projet a construit** (chantier FLX, ADR-059 à 064). La
matrice vérifie après coup que ce choix tient face aux autres.

## 2. Les critères et leur poids

Poids de 1 (accessoire) à 5 (crucial), pour **ce** projet.

| Critère | Poids | Pourquoi ce poids |
|---|---|---|
| Sécurité et RGPD | **5** | La base est « saturée de données personnelles » (`SP/Readme.md:270`) ; une IA doit y lire sans tout voir |
| Performance sous charge | **4** | Les lectures d'analyse ne doivent pas ralentir le métier |
| Scalabilité (volume, 10 pays) | **4** | 22 à 133 Go après 2 ans (note 3V § 3) : gros, mais une seule instance suffit encore |
| Éco-conception et coût | **4** | Exigence transverse du titre ; tout tourne en local, outils gratuits |
| Simplicité et maintenance | **4** | Une équipe de 4, sans exploitation ; chacun doit pouvoir tout expliquer seul au jury |
| Cohérence des données | **3** | Une seule source de vérité ; un décalage d'une nuit est acceptable pour l'analyse |

## 3. La matrice

Note de 1 à 5 ; case = note × poids.

| Critère | Poids | A. Une base | **B. OLTP + OLAP, même instance** | C. Entrepôt séparé | D. Microservices |
|---|---|---|---|---|---|
| Sécurité et RGPD | 5 | 2 → 10 | **4 → 20** | 4 → 20 | 3 → 15 |
| Performance sous charge | 4 | 2 → 8 | **4 → 16** | 5 → 20 | 4 → 16 |
| Scalabilité | 4 | 2 → 8 | **3 → 12** | 4 → 16 | 5 → 20 |
| Éco-conception et coût | 4 | 4 → 16 | **4 → 16** | 2 → 8 | 1 → 4 |
| Simplicité et maintenance | 4 | 5 → 20 | **4 → 16** | 2 → 8 | 1 → 4 |
| Cohérence des données | 3 | 5 → 15 | **4 → 12** | 3 → 9 | 2 → 6 |
| **TOTAL** (sur 120) | | **77** | **92** | **81** | **65** |

### Pourquoi ces notes

| Critère | A | B | C | D |
|---|---|---|---|---|
| Sécurité | l'analyse lit les tables nominatives | ✅ `olap` sans nom, email, téléphone ni adresse (`08_olap.sql`) | même étoile pseudonymisée, mais une copie de plus à protéger, hors de la base | autant de bases, de comptes et de flux réseau que de services |
| Performance | les agrégats refont des jointures sur `sale`, `payment`, `visit` à chaque lecture | ✅ agrégats précalculés la nuit (3 h) ; mais même processeur que le métier | moteur en colonnes, machine à part : aucune concurrence | chaque service a sa base ; les requêtes qui traversent les domaines coûtent cher |
| Scalabilité | rien à séparer quand ça grossit | une instance tient 133 Go (note 3V § 6) ; ensuite, réplique et partitions (dossier § 4) | l'analyse grossit sans toucher au métier | chaque domaine grossit seul |
| Éco-conception | un seul service | ✅ un seul moteur ; un recalcul par nuit, pas en continu | un second moteur allumé en permanence | un conteneur et une base par domaine |
| Simplicité | une base, rien d'autre | ✅ `docker compose up -d` lance `db` et `api` (≈ 234 Mio, ADR-062) ; le reste à la demande | deux moteurs, deux langages SQL, une synchronisation | réseau, découverte de services, déploiements séparés : prématuré pour 4 personnes |
| Cohérence | une seule copie | ✅ l'étoile se réécrit dans **une** transaction : jamais à moitié vide (`airflow/src/olap/load.py`) ; elle a au plus une nuit de retard | une synchronisation entre deux systèmes | des transactions qui traversent des services |

## 4. Le résultat tient-il si on change les poids ?

| Scénario | A | B | C | D | En tête |
|---|---|---|---|---|---|
| Poids du § 2 | 77 | **92** | 81 | 65 | B |
| Croissance d'abord : performance 5, scalabilité 5 | 81 | **99** | 90 | 74 | B |
| Tous les poids à 3 | 60 | **69** | 60 | 48 | B |
| Seulement performance et scalabilité | 16 | 28 | 36 | **36** | C, D |

B reste en tête tant que la sécurité, le coût et la simplicité comptent. Il
ne perd que si l'on regarde **seulement** la performance et la scalabilité :
c'est le jour où le volume l'imposera (§ 6).

## 5. Décision

✅ **Option B : OLTP et OLAP séparés, dans la même instance PostgreSQL**, avec
Elasticsearch en copie pour la recherche (ADR-061).

Elle sépare ce que le sujet demande de séparer, le transactionnel et
l'analytique (`SP/Readme.md:247`), sans payer un second moteur ni une
exploitation que l'équipe ne peut pas tenir. Elle met l'analyse dans un schéma
pseudonymisé, ce qui sert aussi l'ouverture des données à l'IA.

## 6. Options écartées, et quand les reprendre

| Option | Écartée parce que | À reprendre quand |
|---|---|---|
| A. Une base | l'analyse lirait les données nominatives et chargerait les tables du métier | jamais : elle ne sépare pas ce que le sujet demande de séparer |
| C. Entrepôt séparé | un second moteur, plus cher et plus lourd, pour un volume que PostgreSQL tient | 🟡 quand les requêtes d'analyse ralentissent le métier, mesuré, ou quand l'étoile ne se recalcule plus dans sa nuit |
| D. Microservices | complexité prématurée pour une équipe de 4 et une seule application | 🟡 quand plusieurs équipes devront livrer des domaines séparément (après les rachats) |

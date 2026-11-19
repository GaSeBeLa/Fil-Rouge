> **Copie de Confluence** — page « Notes de Eco-conception » (id 33783821, version 2), espace GaSeBeLa1, copiée le 2026-11-19.
> La source qui fait foi reste Confluence : https://laurenceamethyste.atlassian.net/wiki/spaces/GaSeBeLa1/pages/33783821/Notes+de+Eco-conception. Les images, schémas draw.io et encadrés ne passent pas dans l'export : ils sont signalés par une ligne « 🖼️ Image ou schéma non copié : <nom ou légende si connue> ».

> **Mise à jour du 03/11/2026** — brouillon à relire par l'équipe. Le texte de Gabriel, en dessous, n'est pas modifié : son arbitrage « coût de perte × coût de sauvegarde » reste juste. Cet encadré liste seulement ce qui a changé dans le projet depuis septembre. Source : dépôt Fil-Rouge, `md/journal/2026-11-03-eco-conception-corrections.md`, commit `e96b2ae`.
>
> **1. Corrections — la note dit autre chose que le code**
>
> * « 11 tables » (Méthode suivie, point 1) → aujourd'hui **22 tables** dans `docker/init-v3/01_create_fil_rouge_immobilier.sql`.
> * `estate_searchrequest.media_url` → les médias audio et vidéo vivent dans la table `review_media`.
> * Couche Gold dans MinIO → le décisionnel est un **schéma OLAP dans PostgreSQL** (`docker/init-v3/08_olap.sql`), rafraîchi par le DAG `olap_refresh`.
> * Bronze purgé après « ex. 7 jours » → Bronze, Silver et un bucket **quarantine** existent dans MinIO, mais **aucune purge n'est codée** : le brut est gardé.
>
> **2. Ajouts — ce qui est né depuis septembre**
>
> * Index Elasticsearch `estates` : reconstruit chaque nuit depuis `estate` → aucune sauvegarde proposée, il se régénère.
> * Logs de l'API dans Logstash → Elasticsearch → Kibana : volume qui grossit chaque jour → durée de rétention votée (voir point 4), pas encore réglée dans Elasticsearch.
> * `estate_price_history` : copie 24 h proposée, comme `estate` ; purgée avec le bien archivé.
> * `estate_contact` (contact du vendeur) : donnée personnelle → durée fixée par la note RGPD.
> * `hunter_performance` : copie 24 h proposée, gardée comme le paiement (10 ans, page RGPD).
>
> **3. Fréquences réelles — trois DAG enchaînés la nuit**
>
> * 2 h : `annonces_import` (bronze → silver → `estate`).
> * 3 h : `olap_refresh` (rafraîchit le schéma OLAP).
> * 4 h : `estates_index` (reconstruit l'index `estates`).
>
> **4. Tranché le 03/11/2026** (Discord, Seb et amethyste ; Gabriel absent)
>
> * Logs Kibana : **gardés 6 mois**, puis supprimés (bas de la fourchette de six mois à un an de la CNIL, délibération n° 2021-122).
> * Purge de Bronze : **reste sur le papier** — proposée, non codée ; le brut est gardé.

## Contexte du projet

Le schéma cible (`01_create_fil_rouge_immobilier.sql`) distingue nettement des données de nature très différente :

| Catégorie | Tables concernées | Nature |
| --- | --- | --- |
| Référentiel peu volatil | `user`, `client`, `hunter`, `real_estate_manager` | change rarement, faible volume |
| Métier évolutif (versionné) | `search_request`, `criteria` (`id_previous_version`) | historisation déjà gérée côté applicatif |
| Contractuel / engageant | `mandate`, `estate_proposed` | statut juridique, faible tolérance à la perte |
| Annonces | `estate` | régénérable depuis les sources (`migrate.py`, `generer_annonces.py`) |
| Médias lourds | `picture.url`, `estate_searchrequest.media_url` (audio/vidéo) | gros volume binaire, faible fréquence de mise à jour |
| Pipeline data (BC05) | Bronze / Silver / Gold (MinIO/Airflow) | Bronze = brut re-dérivable, Gold = coûteux à recalculer |

C'est cette hétérogénéité qui justifie de **ne pas appliquer une politique unique** (sauvegarde, fréquence de traitement ou rétention) à toute la base. Ce document couvre les 4 leviers du numérique responsable : sobriété du stockage, fréquence des traitements, optimisation des requêtes, cycle de vie de la donnée — avec le cas des sauvegardes multi-fréquences (imposé par le brief) comme fil conducteur.

---

## Choix éco-conçus du projet

| Décision | Alternative plus lourde écartée | Gain environnemental | Comment mesurer |
| --- | --- | --- | --- |
| Sauvegarde différentielle/incrémentale pour `estate`, `picture` | Sauvegarde complète à chaque cycle | Réduction forte du volume stocké (les annonces et photos changent peu une fois créées) | Comparer la taille du dump complet vs la taille cumulée des diffs sur une semaine (`pg_dump` + `du -sh`) |
| Pas de sauvegarde dédiée de la couche **Bronze** (BC05) | Sauvegarder Bronze comme le reste | Bronze est ré-ingérable depuis les fichiers sources (`migrate.py`, `generer_annonces.py`) → inutile de dupliquer une donnée reproductible | Comparer le volume MinIO du bucket `bronze` à ce qu'aurait coûté une copie de sauvegarde équivalente |
| Historisation applicative de `criteria` via `id_previous_version` plutôt que multiplier les snapshots de sauvegarde | Sauvegarde fréquente de toute la table `criteria` pour tracer l'évolution | L'historique existe déjà en base ; la sauvegarde n'a plus qu'un rôle de reprise sur incident, pas de traçabilité fonctionnelle | Compter le nombre de lignes `criteria` par `id_search_request` (chaîne de versions) vs le nombre de sauvegardes qu'il aurait fallu sans historisation |
| Index sur les FK fréquemment jointes (`id_search_request`, `id_estate`, `id_hunter`...) | Requêtes sans index sur les tables volumineuses (`estate`, `criteria`) | Moins de CPU/E-S par requête → moindre consommation énergétique du serveur | `EXPLAIN ANALYZE` avant/après création de l'index : comparer `execution time` et le passage de `Seq Scan` à `Index Scan` |
| `floor` en `VARCHAR(10)` contraint plutôt qu'une table de référence séparée | Table `floor_reference` + jointure systématique | Évite une jointure supplémentaire sur une donnée à faible cardinalité | `EXPLAIN ANALYZE` sur une requête filtrant par `floor` : compter le nombre de jointures dans le plan |

---

## Optimisation des requêtes

Levier souvent traité comme un détail technique alors qu'il a un impact direct : une requête mal écrite sur `estate` ou `criteria` (les tables les plus larges du schéma, \~50 colonnes chacune) consomme plus de CPU à chaque appel — multiplié par le nombre d'appels quotidiens (recherche client, push chasseur), l'écart devient réel.

| Bonne pratique | Anti-pattern écarté | Pourquoi ça compte ici |
| --- | --- | --- |
| `SELECT` des colonnes nécessaires uniquement (ex. liste d'annonces : `id, reference, price, surface, town`) | `SELECT *` sur `estate` (\~40 colonnes, dont `information TEXT` jusqu'à 2000 caractères) | Éviter de transférer et charger des colonnes lourdes (texte long) non affichées dans une liste |
| Pagination systématique (`LIMIT`/`OFFSET` ou keyset) sur les endpoints listant `estate`, `criteria`, `mandate` | Retourner toutes les lignes puis filtrer côté client | Le README projette des "plusieurs centaines, voire milliers de biens répertoriés par recherche" — sans pagination, chaque appel API charge tout |
| Index sur les colonnes de filtre fréquent du matching (`estate.town`, `estate.price`, `estate.estate_type`) | Filtrer `estate` par ces colonnes sans index (scan complet à chaque recherche client) | Le matching bien/demande (Phase 4) va filtrer sur exactement ces colonnes à chaque requête client |
| `EXPLAIN ANALYZE` systématique sur les requêtes de matching avant mise en prod | Déployer sans avoir vérifié le plan d'exécution | Détecte un `Seq Scan` sur une table volumineuse avant que ça devienne un problème en prod, pas après |
| Agréger les indicateurs de performance chasseur en amont (table/vue matérialisée Gold) plutôt que recalculer par jointures à chaque affichage | Recalculer `nb_ventes`, `nb_mandats`, `délai moyen` par jointures sur `mandate`/`estate_proposed` à chaque consultation du profil chasseur | Le calcul (défini au README : délai, exclusivité, nb ventes, nb mandats, nb visites) est coûteux en jointures ; un chasseur consulte son profil bien plus souvent que ses indicateurs ne changent |

**Réflexe** : une requête qui tourne une fois par jour en batch peut se permettre d'être lourde ; une requête appelée à chaque clic utilisateur (liste de biens, profil chasseur) doit être optimisée en priorité — c'est la fréquence d'appel qui doit guider l'effort d'optimisation, pas la complexité perçue de la requête.

---

**Important : ce tableau ne parle PAS des données vivantes en base.** Les tables (`mandate`, `estate`, etc.) restent en base tant qu'elles ont une utilité métier/légale — rien n'est effacé de la base de production ici. Il s'agit uniquement de la durée pendant laquelle on **garde les copies de secours** (les snapshots pris à chaque sauvegarde), avant de les supprimer _elles_, une fois qu'une copie plus récente ou moins fréquente prend le relais.

| Fréquence de sauvegarde | Tables concernées | Durée de conservation **de la copie** | Justification |
| --- | --- | --- | --- |
| Horaire | `mandate`, `estate_proposed` | Copies gardées 7 jours glissants, puis supprimées (la donnée source, elle, reste en base) | Au-delà de 7 jours, une restauration se base sur la copie 24h suivante — pas besoin de garder les copies horaires plus longtemps |
| 12 h | `search_request`, `criteria` | Copies gardées 30 jours | Couvre un cycle de recherche client complet sans accumuler indéfiniment de copies |
| 24 h | Référentiels `user`, `client`, `hunter`, `real_estate_manager`, `estate` | Copies gardées 90 jours, puis archivage froid | Perte d'un jour acceptable pour ces données peu volatiles ; l'archivage suffit au-delà de 90 jours |
| — | Médias (`picture`, `estate_searchrequest.media_url`) | Pas de copie de sauvegarde classique ; réplication MinIO en continu | Le volume binaire rend une sauvegarde SQL classique disproportionnée ; la réplication objet remplit déjà ce rôle |
| — | Couche Bronze (BC05) | Aucune copie de sauvegarde dédiée | La couche existe bien en MinIO ; elle est simplement re-générable à la demande depuis les sources brutes (`generer_annonces.py`), donc pas besoin de la dupliquer en plus dans un système de backup |
| 24 h | Couche Gold (BC05, agrégats/matching) | Copies gardées 30 jours | Recalcul coûteux en CPU si perdu ; sauvegarder la copie est plus économe que tout recalculer |

---

## Arbitrage des sauvegardes par type de donnée

| Fréquence | Tables / données | Justification métier |
| --- | --- | --- |
| **Horaire** | `mandate`, `estate_proposed` | Données contractuelles/engageantes (signature de mandat, proposition acceptée) : une perte d'une journée peut correspondre à un engagement juridique disparu. Volume faible → coût de sauvegarde négligeable malgré la fréquence. |
| **12 h** | `search_request`, `criteria` | Données métier importantes mais déjà versionnées applicativement (`id_previous_version`) ; la sauvegarde sert la reprise sur incident, pas la traçabilité fonctionnelle. |
| **24 h** | `user`, `client`, `hunter`, `real_estate_manager`, `estate`, couche Gold | Référentiels peu volatils, ou données ré-générables/recalculables à un coût raisonnable. |
| **Aucune (hors réplication objet)** | Médias (`picture`, `estate_searchrequest.media_url`), couche Bronze | Volume binaire disproportionné pour une sauvegarde SQL classique (médias) ou donnée strictement reproductible depuis la source (Bronze). |

**Le réflexe appliqué ici** : `mandate` est peu volumineux mais critique → sauvegarde fréquente peu coûteuse. `estate` est volumineux mais reconstructible → sauvegarde peu fréquente, réplication suffit. Ce n'est pas la taille de la table qui fixe la fréquence, c'est le couple **coût de perte × coût de sauvegarde**.

---

## Fréquence des traitements (au-delà des sauvegardes)

Le brief décrit un besoin métier réel qui pousse à sur-calculer : le chasseur reçoit une sélection de biens _"chaque jour, voire plusieurs fois par jour dans les zones tendues"_ (parcours utilisateur, point 5). Une fréquence unique et globale serait un gaspillage — le réflexe éco-conception s'applique aussi ici.

| Traitement | Fréquence proposée | Alternative écartée | Justification |
| --- | --- | --- | --- |
| Recherche de biens correspondants (push chasseur) | Quotidienne par défaut, plusieurs fois/jour **uniquement** sur les zones à forte tension (Paris, Lyon...) | Plusieurs fois/jour partout | Recalculer un matching sur un marché calme (ex. petites villes) plusieurs fois par jour ne change rien au résultat mais consomme du CPU pour rien |
| Ingestion Bronze (BC05) | À chaque nouvelle livraison de source (batch `generer_annonces.py` ou flux réel) | Ingestion en continu (streaming) | Le volume actuel (fictif, batché) ne justifie pas une infra streaming plus coûteuse à faire tourner |
| Transformation Silver (nettoyage) | Déclenchée après chaque ingestion Bronze réussie | Nettoyage recalculé à intervalle fixe qu'il y ait ou non de la nouvelle donnée | Événementiel = pas de job qui tourne "au cas où" sur des données déjà nettoyées |
| Agrégats Gold / features de matching | Quotidien | Recalcul à chaque écriture Silver | Le matching bien/demande n'a pas besoin d'une fraîcheur à la minute ; un recalcul quotidien suffit et évite un job qui tourne en continu |
| Recalcul des indicateurs de performance chasseur | Événementiel, déclenché par le paiement effectif (parcours chasseur, point 12) | Recalcul périodique (ex. toutes les nuits) de tous les chasseurs | L'indicateur ne change qu'à des événements précis (vente payée, mandat renouvelé) ; un job périodique recalculerait inutilement des chasseurs sans activité |

🧠 **Principe** : une fréquence se justifie par la vitesse à laquelle la réalité change, pas par une préférence technique. Un marché tendu bouge vite → fréquence haute justifiée localement ; un indicateur qui ne change qu'à un événement précis → traitement événementiel, pas de polling périodique.

---

## Cycle de vie de la donnée (archivage / purge)

Le schéma actuel ne prévoit aucune purge : tout s'accumule indéfiniment (`estate`, `picture`, `search_request`...). C'est le levier le plus négligé du projet à ce stade — à documenter même si l'implémentation n'est pas exigée en Phase 2/3.

| Donnée | Signal de fin de vie utile | Action proposée | Gain |
| --- | --- | --- | --- |
| `mandate` | Statut `expired` ou `canceled`, au-delà de la durée légale de conservation des documents contractuels | Archivage froid (hors base active) après la période légale ; jamais de suppression pure (valeur probante) | Réduit le volume de la table active la plus consultée en usage courant, sans perdre la traçabilité légale |
| `search_request` / `criteria` | Mandat associé clôturé (vendu ou expiré sans renouvellement) | Archivage froid après quelques mois d'inactivité ; l'historique `id_previous_version` part avec | Allège les tables les plus jointes (impact direct sur les perfs de recherche courante) |
| `estate` | Bien vendu ou mandat vendeur expiré (retiré du marché) | Marquer obsolète puis archiver/purger après un délai court | Évite que des annonces mortes polluent les résultats de matching et gonflent indéfiniment la table la plus volumineuse |
| `picture`, `estate_searchrequest.media_url` | Rattachés à un `estate` archivé | Purgés avec le bien (le plus gros gain : ce sont les objets binaires les plus lourds) | Le stockage objet (MinIO) est le poste le plus coûteux en volume — c'est là que la purge a le plus d'impact |
| Bronze (BC05) | Une fois transformé avec succès en Silver | Purge après une fenêtre courte de rejouabilité (ex. 7 jours, pour pouvoir corriger un bug de transformation sans tout ré-ingérer) | Le brut n'a de valeur que le temps de vérifier que la transformation a réussi |
| Silver / Gold (BC05) | Nouvelle version d'agrégat disponible | Conserver seulement les N dernières versions (pas d'accumulation infinie) | Les anciens agrégats n'ont pas de valeur d'usage une fois remplacés |

**Lien avec la note RGPD** : la durée de conservation des données personnelles (`user`, `client`) doit rester cohérente entre les deux notes — c'est la note RGPD qui fixe la durée légale, celle-ci en hérite plutôt que d'en fixer une différente.

---

## Méthode suivie

1. **Inventorier** : 11 tables classées par volume (léger vs lourd) et par volatilité (référentiel vs transactionnel vs médias).
2. **Questionner** : pour chaque table, le besoin métier justifie-t-il une sauvegarde fréquente ? (`mandate` → oui, `estate` → non, il est reconstructible).
3. **Arbitrer** : fréquence alignée sur la criticité réelle, pas sur une politique uniforme.
4. **Documenter** : tableaux ci-dessus, réutilisables en soutenance.

**Réponse type à la question piège orale** : _« Pourquoi sauvegarder_ `mandate` _toutes les heures mais pas_ `estate` _? »_ → `mandate` est une donnée contractuelle à faible volume dont la perte a un impact juridique direct ; `estate` est volumineux mais entièrement régénérable depuis `migrate.py`/`generer_annonces.py`, donc la réplication objet et une sauvegarde quotidienne suffisent.

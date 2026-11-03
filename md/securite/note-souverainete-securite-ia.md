# Note souveraineté et sécurité des données face à l'IA

> ⚠️ **Remplacée** le 2026-11-03 (fiche RGP4) par
> [`livrables/5-transverse/note-souverainete-securite-ia.md`](../../livrables/5-transverse/note-souverainete-securite-ia.md),
> mise d'accord avec le registre. Ce brouillon reste pour l'historique ; il
> ne se met plus à jour.

> Brouillon du 2026-11-03 (vote « suite » A), à reprendre par Laurence (R
> proposé au RACI). Format : 1 page (`SP/documents utiles/GRILLE-EVALUATION.md:38`).
> Modèle suivi : `SP/documents utiles/SOUVERAINETE-SECURITE-IA.md`.
> Statuts : ✅ codé ou établi · 🟡 à décider · 💡 proposé.

## Le principe

L'IA voit **le strict nécessaire**, en **lecture seule** quand elle lit, et
**jamais une donnée personnelle en clair** qui ne sert pas sa tâche. Quand elle
agit, elle a **moins de droits qu'un humain**, et un humain engage.

## 1. Périmètre d'accès — qui voit quoi

Deux usages, deux portes :

| Usage | Porte | Droits |
|---|---|---|
| Analyse, assistant branché sur la base (MCP…) | rôle PostgreSQL `fil_rouge_reader` | ✅ `SELECT` seulement : ni `INSERT`, ni `UPDATE`, ni `DELETE` (`docker/init-v3/04_role-lecture-seule.sql`) |
| Chasseur IA qui suggère et propose des biens | l'API, avec un compte `hunter` où `is_hunter_ai = TRUE` | 💡 un sous-ensemble des droits du chasseur humain (ADR-058, **proposé**, pas codé) |

| Ressource | Accès accordé à l'IA | Justification |
|---|---|---|
| `estate`, `estate_price_history`, index `estates` | lecture | nécessaire au matching |
| `criteria` de la demande confiée | lecture | nécessaire au matching |
| `estate_searchrequest`, `estate_proposed` | lecture ; écriture en `suggested` seulement (SUG8) | le chasseur humain trie, l'IA ne propose rien seule au client |
| `"user".password` | ✅ **fermé** au lecteur, colonne par colonne | aucun usage |
| `estate_contact` (contact du vendeur) | ✅ **fermé** au lecteur ; 💡 fermé au chasseur IA (ADR-058) | donnée personnelle d'un tiers (ADR-054) |
| `payment` (montant, IBAN) | ✅ **fermé** au lecteur | données financières (ADR-027) |
| comptes désactivés | ✅ **invisibles** au lecteur (politique par ligne) | ADR-027, point 7 |
| offre, vente, paiement, barème | 💡 **interdits** au chasseur IA (ADR-058) | ce qui engage de l'argent ou un contrat reste humain |

- ⚠️ **Le trou qui reste** : `fil_rouge_reader` lit encore `client` et
  `hunter` **en clair** (nom, téléphone, date de naissance…). C'est voulu pour un
  analyste humain, pas pour une IA.
  - 💡 Parade : l'IA lit le **schéma OLAP**, pas la base de production (voir § 2).

## 2. Anonymisation et pseudonymisation

- ✅ **L'OLAP est déjà pseudonymisé** (`docker/init-v3/08_olap.sql`) :
  - `dim_client` ne garde que l'id, l'année d'inscription, la ville et le pays ;
  - `dim_chasseur` ne garde que l'id, l'année d'embauche, IA ou non, carte T, et le pays ;
  - aucun nom, email ni téléphone.
  - C'est une **pseudonymisation**, pas une anonymisation : l'id renvoie à la
    base de production, pour qui y a accès.
- ✅ **Les features du matching** n'utilisent **aucune donnée personnelle**
  ([`livrables/4-application/conception-matching-features.md`](../../livrables/4-application/conception-matching-features.md), § 3) : le modèle juge un couple
  (demande, bien), pas une personne.
- ✅ **Le droit à l'effacement** : la route `POST /users/{id}/anonymize`
  anonymise un compte sans `DELETE` (chantier API).
- 💡 Avant tout envoi à un LLM (par exemple pour expliquer une suggestion au
  chasseur) : n'envoyer que les colonnes du bien et des critères, **jamais**
  `comment_client`, qui est du texte libre et peut contenir n'importe quoi.

## 3. Souveraineté et localisation

- ✅ **Aujourd'hui, tout tourne en local** : PostgreSQL, Elasticsearch,
  MinIO, Airflow et Kibana sont des conteneurs `docker compose` sur la machine
  du développeur. **Aucune donnée ne sort.**
- ✅ **Le moteur de suggestion v1 n'appelle aucun service externe** : c'est
  une requête Elasticsearch locale (SUG7, SUG8).
- 🟡 **Un LLM hébergé hors UE** poserait la question du transfert de données
  hors de l'UE au regard du RGPD. Choix à faire si la v2 en utilise un :
  modèle hébergé dans l'UE, ou modèle local.
- 🟡 **Le déploiement sur le VPS** (chantier 9 de la TODO) : le pays de
  l'hébergeur est à documenter ici le jour où il est choisi.

## 4. Risques et parades

| Risque | Parade | État |
|---|---|---|
| L'IA exécute une requête destructrice | compte en lecture seule `fil_rouge_reader` | ✅ codé |
| L'IA lit des données personnelles inutiles | elle lit l'OLAP pseudonymisé ; contact du vendeur et paiement fermés | ✅ en partie (le trou du § 1) |
| Le chasseur IA engage un contrat seul | liste blanche : il cherche et propose, un humain engage | 💡 ADR-058, proposé |
| Une suggestion part chez le client sans contrôle | l'IA écrit en `suggested` ; seul un bien `kept` se propose | ✅ voté, codé en SUG4 et SUG8 |
| Fuite par un LLM externe | rien n'est envoyé aujourd'hui ; plus tard, colonnes minimales, modèle UE ou local | 🟡 v2 |
| On ne sait pas qui a fait quoi | logs de l'API dans Kibana, gardés **6 mois** (vote du 2026-11-03, fourchette CNIL de 6 mois à 1 an) | ✅ logs codés ; ⚠️ durée pas encore réglée |

## Au jury, en une phrase

« L'IA lit en lecture seule des données pseudonymisées, elle suggère sans
jamais engager, un humain trie et signe, et rien ne quitte nos serveurs. »

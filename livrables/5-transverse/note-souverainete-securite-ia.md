# Note souveraineté et sécurité des données face à l'IA

> Écrite le 2026-11-03 (fiche RGP4), d'après le brouillon Confluence
> 63438854 et `md/securite/note-souverainete-securite-ia.md`. R : Laurence,
> A : Gabriel (RACI proposé, RGPD-1). Format : 1 page
> (`SP/documents utiles/GRILLE-EVALUATION.md:38`). Modèle :
> `SP/documents utiles/SOUVERAINETE-SECURITE-IA.md`. D'accord avec le
> registre : `registre-rgpd.md`. Statuts : ✅ établi · 🟡 ouvert · 💡 proposé.
> ✅ Écart avec Confluence (N1 à N7) **validé par le groupe** le 2026-11-03
> (Seb ; Laurence et Gabriel, rapporté par Seb) ; report sur Confluence à faire.

**Le principe.** L'IA voit le strict nécessaire, en lecture seule quand elle
lit, et jamais une donnée personnelle en clair qui ne sert pas sa tâche.
Quand elle agit, elle a moins de droits qu'un humain, et un humain engage.

## 1. Périmètre d'accès — qui voit quoi

| Ressource | Accès accordé à l'IA | Justification |
|---|---|---|
| `estate`, `estate_price_history`, index `estates` | lecture | nécessaire au matching |
| `criteria` de la demande confiée | lecture | nécessaire au matching |
| `estate_searchrequest`, `estate_proposed` | lecture ; écriture en `suggested` seulement (SUG8) | un chasseur humain garde (`kept`) avant toute proposition |
| `"user".password` | ✅ fermé au lecteur, colonne par colonne | aucun usage |
| `estate_contact` (vendeur) | ✅ fermé au lecteur ; 💡 fermé au chasseur IA (ADR-058) | donnée d'un tiers (ADR-054) |
| `payment` (montants, taux, score) | ✅ fermé au lecteur | données financières (ADR-027) |
| comptes désactivés | ✅ invisibles au lecteur (politique par ligne) | ADR-027, point 7 |
| offre, vente, paiement, barème | 💡 interdits au chasseur IA | engager reste humain |

- Le chasseur IA passe par l'API, avec un compte `hunter` à
  `is_hunter_ai` vrai : droits réduits selon **ADR-058, proposé** (pas
  accepté, pas codé ; RGPD-18).
- ⚠️ **Le trou** : `fil_rouge_reader` (`SELECT` seul, `04_role-lecture-seule.sql`)
  lit `client` et `hunter` en clair. Voulu pour un analyste humain, pas pour
  une IA. 🟡 Parade : une IA lirait l'OLAP (ADR-027, l. 165) — mais
  `fil_rouge_reader` n'a aucun droit sur `olap` (`init-v3/README.md:180`) :
  il faudrait un rôle à part, cible v2.

## 2. Masquage — anonymisation et pseudonymisation

- ✅ **L'OLAP est pseudonymisé** (RGPD-13) : ni nom, ni email, ni téléphone,
  ni adresse, ni rue, ni GPS (`08_olap.sql:54-57` ; inventaire RGP1 § 5).
  Il garde `id_client` et `id_hunter` (`08_olap.sql:91`, `:100`) : une clé
  de retour vers la base, donc pas une anonymisation. Gardé **10 ans**,
  comme les ventes (RGPD-12).
- ✅ **Le matching** n'utilise aucune donnée personnelle : il juge un
  couple (demande, bien), pas une personne
  (`livrables/4-application/conception-matching-features.md`, § 3).
- ✅ **L'effacement** : `POST /users/{id}/anonymize`, sans `DELETE`
  (ADR-049) ; la date de l'effacement n'est pas gardée (v2, RGPD-14).
- 💡 Si un LLM arrive en v2 : il ne reçoit que les colonnes du bien et des
  critères, **jamais** un texte libre (`comment_client`…, RGPD-8).

## 3. Souveraineté et localisation

- ✅ **v1 : aucun LLM, tout en local** (RGPD-17). PostgreSQL,
  Elasticsearch, MinIO, Airflow et Kibana sont des conteneurs
  `docker compose` sur la machine du développeur : aucune donnée ne sort.
- ✅ Le moteur de suggestion v1 est une requête Elasticsearch locale (SUG7,
  SUG8) : aucun service externe.
- 🟡 **v2 ouverte** : un LLM hébergé hors UE poserait la question du
  transfert hors UE. Choix à faire alors : modèle hébergé dans l'UE, ou local.
- 🟡 Le pays de l'hébergeur, le jour d'un déploiement (VPS), s'écrira ici.

## 4. Journalisation et risques

- ✅ **Qui a fait quoi** : chaque appel à l'API est journalisé (FLX10),
  sans mot de passe ni email, lu dans Kibana. Gardé **6 mois** (RGPD-11,
  vote du 2026-11-03, CNIL). 🟡 Le compte Kibana reste à définir.

| Risque | Parade | État |
|---|---|---|
| requête destructrice | compte en lecture seule | ✅ codé |
| données personnelles inutiles | OLAP pseudonymisé ; contact et paiement fermés | ✅ en partie (le trou du § 1) |
| le chasseur IA engage seul | il cherche et suggère, un humain engage | 💡 ADR-058, proposé |
| une suggestion part sans contrôle | `suggested`, puis `kept` par un humain | ✅ SUG4, SUG8 |
| fuite par un LLM externe | aucun LLM en v1 ; v2 : colonnes minimales, UE ou local | 🟡 v2 |

**Au jury, en une phrase.** « L'IA lit en lecture seule des données
pseudonymisées, elle suggère sans jamais engager, un humain trie et signe,
et rien ne quitte nos machines. »

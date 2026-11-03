# Livrable 4 — Le schéma du programme d'IA

> Brouillon du 2026-11-03, à relire par l'équipe. Format attendu : « 1 schéma
> + description entrées/sorties » (`SP/documents utiles/GRILLE-EVALUATION.md:32`).
> Statuts : ✅ établi (codé ou voté) · 🟡 à décider · 💡 proposé.

## En une phrase

La machine **suggère**, le chasseur **trie**, le client **décide**. Chaque
décision deviendra, plus tard, la donnée qui apprend au système les goûts réels.

## Le schéma

Le schéma est une page HTML : [`schema-programme-ia.html`](schema-programme-ia.html),
dessinée par Gabriel le 2026-11-03. Sur Confluence, elle se colle dans un bloc
« HTML Macro Pro Block » (`/html`).

Il se lit de gauche à droite, en quatre cases, puis la v2 en dessous :

1. **Ce qui entre** → 2. **Le moteur (v1)** → 3. **Ce qui sort** → 4. **Les décisions**
5. En pointillés : **la v2**, qui apprend des décisions et renvoie un ordre au moteur.

## Les quatre cases, expliquées

### 1. Ce qui entre

- **La demande du client** : son budget et le type de bien. Ses critères
  (`criteria`) sont gardés version par version. Route : `POST /search-requests/submit` (✅ SUG3).
- **Les annonces**, indexées dans Elasticsearch (index `estates`).
- Chaque nuit, Airflow importe les annonces à 2 h (`annonces_import`) et
  refait l'index à 4 h (`estates_index`) (✅ chantier FLX).

### 2. Le moteur, v1

- Des **filtres durs** écartent les biens qui ne conviennent pas, puis un
  **score bonus** classe les autres.
- Route : `POST /search-requests/{id}/suggestions`, appelée par le chasseur (✅ SUG7, SUG8).
- ➡️ **Il n'apprend rien** : ce sont des règles écrites à la main.
  L'énoncé demande de concevoir l'IA, pas d'entraîner un modèle (`SP/Readme.md:257`).

### 3. Ce qui sort

- **10 suggestions au plus**, ni vendues, ni déjà vues.
- Elles sont enregistrées dans `estate_searchrequest` au statut `suggested` (✅ SUG8).
- La machine n'écrit **jamais** directement chez le client.

### 4. Les décisions

- **Le chasseur trie** : il garde (`kept`) ou il écarte (`dismissed`) (✅ SUG4).
  Seul un bien gardé peut être proposé au client.
- **Le client décide** : `interested`, ou `declined` avec un motif : trop
  cher, trop loin, trop petit, mauvais type, autre (✅ SUG5).
- **S'il est intéressé** : offre (`POST /estate-proposed/{id}/offer`), puis vente (✅ SUG6).

### La v2, sur le papier

- Un **modèle de reclassement** apprend des décisions du chasseur et du
  client, des offres et des ventes. Une vente signée est le signal le plus fort.
- Il renvoie au moteur **un ordre de pertinence**.
- 💡 Conçu, pas codé. Le détail des features : `conception-matching-features.md`.

## Ce qui entre, ce qui sort

| Étape | Entrée | Sortie | Statut |
|---|---|---|---|
| Import et index | annonces CSV | lignes `estate`, documents de l'index `estates` | ✅ codé (chantier FLX) |
| Dépôt de la demande | formulaire JSON du client | `search_request` + 1ʳᵉ version de `criteria` | ✅ codé en SUG3 |
| Suggestion | dernière version de `criteria`, index `estates` | ≤ 10 lignes `estate_searchrequest` en `suggested` | ✅ codé en SUG7 et SUG8 |
| Tri du chasseur | les `suggested` | `kept` ou `dismissed` | ✅ codé en SUG4 |
| Décision du client | un bien proposé | `interested` ou `declined` + motif | ✅ codé en SUG5 |
| Reclassement v2 | décisions, offres et ventes passées | un ordre de pertinence | 💡 sur le papier |

## Les briques de l'énoncé, et où elles en sont

L'énoncé liste les assistances voulues (`SP/user-stories/09_futur_chasseur_assistance_ia.feature`).

| Scénario (ligne) | Ce que nous faisons |
|---|---|
| Sélection dédoublonnée et ordonnée par pertinence (l.34-40) | ✅ v1 : filtres + score ; la pertinence apprise viendra en v2 |
| Écarter les biens qui ressemblent aux biens rejetés (l.42-46) | 💡 v2 : vecteur par bien, recherche des plus proches (`dense_vector` + kNN d'Elasticsearch) |
| Offre sous le prix affiché pré-calculée (l.40, l.54-58) | 💡 feature « baisse de prix » tirée de `estate_price_history` |
| Rapport de faisabilité, prise de contact, avis pré-rédigés, facture, renouvellement (l.15-32, 48-71) | 🟡 hors périmètre de ce livrable |

## Les garde-fous

- **Le chasseur reste dans la boucle** : seul un bien `kept` peut être proposé
  au client (règle P19 renforcée, SUG4).
- **Lecture seule pour l'IA** : tout outil d'IA branché sur la base passe par
  le rôle `fil_rouge_reader` (chantier LOT, LOT12).
- **Aucune donnée personnelle** dans les features : ni nom, ni âge, ni
  situation familiale. Le modèle juge un couple (demande, bien), pas une personne.
- **Le chasseur IA a moins de droits qu'un humain** : il cherche et suggère ;
  l'offre, la vente et le paiement restent humains (ADR-058, 🟡 proposé, pas codé).
- Le détail : [`../5-transverse/note-souverainete-securite-ia.md`](../5-transverse/note-souverainete-securite-ia.md).

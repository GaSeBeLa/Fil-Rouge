# Livrable 4 — Le schéma du programme d'IA

> Version du 2026-11-20 (brouillon du 2026-11-03 complété par le Glaude, à la demande de Gabriel) :
> le sujet veut un schéma « (chasseurs-IA, faisabilité, matching) » (`SP/Readme.md:256`) ; la faisabilité
> et le chasseur-IA y sont ajoutés. Format attendu : « 1 schéma + description entrées/sorties »
> (`SP/documents utiles/GRILLE-EVALUATION.md:32`).
> Statuts : ✅ établi (codé ou voté) · 🟡 à décider · 💡 proposé.

## En une phrase

Trois pièces : la **faisabilité** juge la demande, le **matching** cherche les
biens, le **chasseur-IA** fait tourner le tout. La machine **suggère**, le
chasseur **trie**, le client **décide** ; chaque décision deviendra, plus tard,
la donnée qui apprend au système les goûts réels.

## Le schéma

Le schéma est une page HTML : [`schema-programme-ia.html`](schema-programme-ia.html),
dessinée par Gabriel le 2026-11-03. Sur Confluence, elle se colle dans un bloc
« HTML Macro Pro Block » (`/html`).

Il se lit de gauche à droite, en quatre cases, puis la v2 en dessous :

1. **Ce qui entre** → 2. **Le moteur (v1)** → 3. **Ce qui sort** → 4. **Les décisions**
5. En pointillés : **la v2**, qui apprend des décisions et renvoie un ordre au moteur.
6. En pointillés, dessous : **le rapport de faisabilité** et **le chasseur-IA**, conçus, pas codés.

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

### Le rapport de faisabilité, sur le papier

Le sujet le demande à l'acceptation d'une demande (`SP/user-stories/09_futur_chasseur_assistance_ia.feature`,
scénario `@rapport-faisabilite`, l.15-19) : un rapport « complet », et comment reformuler la demande.

- **Il reçoit** la demande acceptée (budget, type, surface, zone), les biens et les
  ventes de la zone (`estate`, `sale`, et le schéma `olap`), l'historique des prix
  (`estate_price_history`).
- **Il calcule** : combien de biens collent aujourd'hui, avec la même recherche que
  le moteur v1 ; le budget face au prix médian de la zone ; le critère qui bloque le plus.
- **Il rend au chasseur** : faisable, difficile ou irréaliste, et une piste de
  reformulation (élargir la zone, revoir la surface ou le budget).
- 💡 Conçu, pas codé. Toutes ses données existent déjà en base : c'est un calcul,
  pas un modèle à entraîner.

### Le chasseur-IA, sur le papier

- Le sujet le veut capable d'**épauler** les chasseurs humains, et d'**opérer seul**
  dans les zones non couvertes physiquement (rappel en tête du même fichier `.feature`).
- ✅ En base : une fiche `hunter` avec `is_hunter_ai`, rattachée à un manager humain (ADR-029).
- **Il peut** : lire les demandes et les mandats qui lui sont confiés, lancer le moteur, proposer des biens.
- **Il ne peut pas** : faire une offre, conclure une vente, toucher au paiement (ADR-058,
  💡 proposé). Aujourd'hui il a les droits d'un `Hunter` : la restriction n'est pas codée.

## Ce qui entre, ce qui sort

| Étape | Entrée | Sortie | Statut |
|---|---|---|---|
| Import et index | annonces CSV | lignes `estate`, documents de l'index `estates` | ✅ codé (chantier FLX) |
| Dépôt de la demande | formulaire JSON du client | `search_request` + 1ʳᵉ version de `criteria` | ✅ codé en SUG3 |
| Suggestion | dernière version de `criteria`, index `estates` | ≤ 10 lignes `estate_searchrequest` en `suggested` | ✅ codé en SUG7 et SUG8 |
| Tri du chasseur | les `suggested` | `kept` ou `dismissed` | ✅ codé en SUG4 |
| Décision du client | un bien proposé | `interested` ou `declined` + motif | ✅ codé en SUG5 |
| Reclassement v2 | décisions, offres et ventes passées | un ordre de pertinence | 💡 sur le papier |
| Rapport de faisabilité | demande acceptée, biens, ventes et prix de la zone | faisable / difficile / irréaliste + piste de reformulation | 💡 sur le papier |
| Chasseur-IA | demandes qui lui sont confiées | suggestions, comme un chasseur humain ; jamais d'offre ni de vente | 💡 droits réduits proposés (ADR-058), fiche `is_hunter_ai` ✅ en base |

## Les briques de l'énoncé, et où elles en sont

L'énoncé liste les assistances voulues (`SP/user-stories/09_futur_chasseur_assistance_ia.feature`).

| Scénario (ligne) | Ce que nous faisons |
|---|---|
| Sélection dédoublonnée et ordonnée par pertinence (l.34-40) | 🟢 en partie : la v1 ordonne par score et écarte les biens déjà vus ; le dédoublonnage des annonces en double et la pertinence apprise viendront en v2 |
| Écarter les biens qui ressemblent aux biens rejetés (l.42-46) | 💡 v2 : vecteur par bien, recherche des plus proches (`dense_vector` + kNN d'Elasticsearch) |
| Offre sous le prix affiché pré-calculée (l.40, l.54-58) | 💡 feature « baisse de prix » tirée de `estate_price_history` |
| Rapport de faisabilité et reformulation (l.15-19) | 💡 conçu ci-dessus, pas codé |
| Prise de contact, affinage assisté, avis pré-rédigés, facture, renouvellement (l.21-32, 48-71) | 🟡 hors périmètre de ce livrable |

## Les garde-fous

- **Le chasseur reste dans la boucle** : seul un bien `kept` peut être proposé
  au client (règle P19 renforcée, SUG4).
- **Lecture seule pour l'IA** : tout outil d'IA branché sur la base passe par
  le rôle `fil_rouge_reader` (chantier LOT, LOT12).
- **Aucune donnée personnelle** dans les features : ni nom, ni âge, ni
  situation familiale. Le modèle juge un couple (demande, bien), pas une personne.
- **Le chasseur IA a moins de droits qu'un humain** : il cherche et suggère ;
  l'offre, la vente et le paiement restent humains (ADR-058, 💡 proposé, pas codé).
- Le détail : [`../5-transverse/note-souverainete-securite-ia.md`](../5-transverse/note-souverainete-securite-ia.md).

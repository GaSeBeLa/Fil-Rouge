# Livrable 4 — La conception du modèle de matching et ses features

> Brouillon du 2026-11-03, à relire par l'équipe. Format attendu : « 2 pages
> (conception, pas entraînement) » (`SP/documents utiles/GRILLE-EVALUATION.md:31`).
> L'énoncé : « on conçoit la base qui nourrit le modèle, l'entraînement n'est
> pas exigé » (`SP/Readme.md:257`).
> Statuts : ✅ établi · 🟡 à décider · 💡 proposé.

## 1. Le problème posé

- **L'unité jugée** : un couple (demande, bien) — une ligne `criteria` (sa
  dernière version) face à une ligne `estate`.
- **La question** : ce bien plaira-t-il à ce client ? On ne classe pas, on
  **ordonne** : les 10 premiers vont au chasseur.
- **Deux étages** :
  1. ✅ **Filtrer** : les critères durs écartent ce qui ne convient pas du tout.
  2. 💡 **Ordonner** : les features notent ce qui reste.

## 2. Étage 1 — les filtres durs (v1, chantier SUG)

| Critère (`criteria`) | Champ du bien (`estate`) | Règle |
|---|---|---|
| `town`, `postal_code` | `town`, `postal_code` | égalité |
| `estate_type` | `estate_type` | égalité |
| `budget_min`, `budget_max` | `price` | dans la fourchette |
| `surface_min` | `surface` | ≥ |
| `rooms_min`, `bedrooms_min` | `nb_rooms`, `nb_bedrooms` | ≥ |
| `energy_class_max` | `energy_class` | lettre ≤ |
| — | `sale.id_estate` | exclu s'il est vendu |
| — | `estate_searchrequest` | exclu s'il est déjà dans la sélection |

- ⚠️ Des critères n'ont **pas leur champ dans l'index** `estates` : balcon,
  terrasse, vue, piscine, calme, lumineux (`airflow/src/search/mapping.py`).
  Ils restent en base ; la v1 ne les utilise pas.

## 3. Étage 2 — le tableau des features

Toutes se calculent depuis la base, sans donnée personnelle.

| # | Feature | Source | Calcul | Pourquoi elle compte |
|---|---|---|---|---|
| 1 | Écart prix / budget | `estate.price`, `criteria.budget_max` | `price / budget_max` | un bien à 98 % du budget n'est pas jugé comme un bien à 70 % |
| 2 | Marge de surface | `estate.surface`, `criteria.surface_min` | `surface / surface_min` | « plus grand que demandé » plaît souvent |
| 3 | Pièces en plus | `estate.nb_rooms`, `criteria.rooms_min` | `nb_rooms − rooms_min` | idem, pour les pièces |
| 4 | Marge énergétique | `estate.energy_class`, `criteria.energy_class_max` | rang(max) − rang(bien), A = 1 … G = 7 | un DPE meilleur qu'exigé est un plus |
| 5 | Options cochées satisfaites | les booléens `has_garden`, `has_elevator`, `has_cellar`, `has_garage`, `is_climatised`… des deux tables | options du bien ∩ options voulues ÷ options voulues | mesure « ce qu'il a, parmi ce qu'il veut » |
| 6 | Même quartier | `estate.district`, `criteria.district` | 1 si égaux | la ville est filtrée, le quartier départage |
| 7 | Conflit travaux | `estate.needs_renovation`, `criteria.needs_renovation` | 1 si le bien en demande et pas le client | un refus fréquent et prévisible |
| 8 | Ancienneté de l'annonce | `estate.created_at` | jours depuis la mise en ligne | une annonce ancienne se négocie mieux |
| 9 | Baisse de prix | `estate_price_history` | nombre de baisses, et % total | prépare l'offre sous le prix (feature 09, l.40) |
| 10 | Score texte | `estate.information`, `criteria` | score Elasticsearch (BM25, analyseur `french`) | capte « lumineux », « calme » absents des colonnes |
| 11 | Ressemblance aux rejetés | les biens `dismissed` ou `declined` de la même demande | similarité maximale entre vecteurs de biens | « écarter ce qui ressemble aux rejetés » (feature 09, l.42-46) — v2 |

- 🟡 **Distance au lieu voulu** : utile, mais `criteria` n'a qu'une ville, pas
  de point GPS. Il faudrait un référentiel des communes (centre de chaque
  ville). Non décidé.
- 💡 **Où elles vivent** : une vue SQL `matching_features`, recalculée chaque
  nuit après `estates_index` (cohérent avec la note d'éco-conception : un
  recalcul par jour suffit).

## 4. Le label — comment on sait qu'un bien plaît

On lit les décisions déjà enregistrées. Plus la décision engage, plus le signal est fort.

| Signal | Source | Sens | Force 💡 |
|---|---|---|---|
| Offre acceptée ou signée | `estate_proposed.proposition_status` ∈ `accepted`, `signed` | plaît | très forte |
| Offre faite | `proposition_status = 'offer_pending'` | plaît | forte |
| Client intéressé | `client_decision = 'interested'` (SUG5) | plaît | moyenne |
| Bonne note du client | `client_priority` 4 ou 5 (échelle 1 à 5) | plaît | moyenne |
| Visite du client | `visit.visitor_type = 'client'` | plaît un peu | faible |
| Client refuse | `client_decision = 'declined'` + `decline_reason` (SUG5) | ne plaît pas | forte |
| Chasseur écarte | `estate_searchrequest.status = 'dismissed'` (SUG4) | ne plaît pas, selon le chasseur | faible : c'est son avis, pas celui du client |
| Bien proposé sans réponse | `client_decision = 'pending'` | inconnu | exclu de l'apprentissage |

- ✅ Le **motif de refus** (`too_expensive`, `too_far`, `too_small`,
  `wrong_type`, `other`) dit **quelle feature** a joué : `too_expensive` pointe
  la feature 1. C'est pourquoi Gabriel l'a demandé en liste fermée.

## 5. Le modèle proposé

- ✅ **v1 — des règles explicables** : les filtres, puis un score de bonus
  (jardin, ascenseur, cave, garage, parking). Codée en SUG7 et SUG8.
- 💡 **v2 — apprendre à ordonner** (« learning to rank ») : un modèle de type
  gradient boosting prend les features 1 à 11 et apprend, du label, l'ordre qui
  plaît. Il remplace le score de bonus, pas les filtres.
- 💡 **Comment on le jugerait** :
  - la part de `kept` parmi les 10 suggestions (le chasseur garde-t-il ce qu'on propose ?) ;
  - la part d'`interested` parmi les biens proposés ;
  - dès la v1, `recherches.csv` sert de **jeu de test** : pour une recherche
    `REC-…`, le moteur retrouve-t-il les annonces faites pour elle ?

## 6. La page franche — ce que nous ne pouvons pas promettre

- ✅ **La v1 n'est pas de l'IA** : c'est une requête et des règles. Nous
  l'appelons « moteur de suggestion » (relevé par Gabriel, journal du 2026-11-02, § 4.2).
- ✅ **Nos données sont générées** : un modèle entraîné dessus n'apprendrait
  que le hasard du générateur, pas les goûts des clients.
- ✅ **`recherches.csv` n'apprend rien** : il ne contient que des exemples
  positifs, fabriqués par les règles mêmes du générateur. Il sert à tester, pas à entraîner.
- ✅ **Ce qui manque, c'est le label réel** : les colonnes de décision (SUG4,
  SUG5) se posent maintenant, pour que les vraies décisions s'accumulent dès la mise en service.
- 🟡 **Combien de décisions faut-il avant la v2 ?** Nous ne le savons pas : cela
  se mesure sur les premières données réelles, aucun chiffre n'est avancé ici.
- 🟡 **Démarrage à froid** : une demande neuve n'a aucune décision ; la v1 reste
  son seul moteur, jusqu'aux premiers retours.

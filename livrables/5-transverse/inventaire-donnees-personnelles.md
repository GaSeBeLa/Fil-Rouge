# Inventaire des données personnelles

Recompté le 2026-11-03 (fiche RGP1, chantier RGP) sur le schéma du jour,
dans le dépôt `Fil-Rouge-API` :

- `docker/init-v3/01_create_fil_rouge_immobilier.sql` (le schéma, noté `01`) ;
- `docker/init-v3/08_olap.sql` (l'entrepôt OLAP, noté `08`).

Il remplace l'inventaire du 15/10
(`md/securite/2026-10-15-preparation-chantier-rgpd.md`, § 3).

Une **donnée personnelle** désigne une personne, directement (un nom) ou
parce qu'elle s'y rattache (le budget d'un client identifié, `REG:13`).
L'adresse d'un bien en est une (RGPD-7).

---

## 1. Les comptes

| Ce qu'on compte | Commande | Compte brut | Verdict |
|---|---|---|---|
| tables de `01` | `grep -c "CREATE TABLE" 01_create_fil_rouge_immobilier.sql` | **22** | ✅ 22 attendu |
| tables de ce fichier (§ 2) | lignes numérotées du tableau | **22** | ✅ concorde |
| colonnes de `01` | extraction `awk` ci-dessous | **280** | — |
| colonnes de `01` au 15/10 | même extraction, commit `0b7e256` | **276** | ➡️ 4 de plus (§ 4) |
| tables de `08` | `grep -c "CREATE TABLE" 08_olap.sql` | **6** | — |

Extraction des colonnes, à relancer depuis `docker/init-v3/` :

```bash
awk '/^CREATE TABLE/{t=$3; inb=1; next} inb && /^\);/{inb=0}
     inb && /^    [a-z_"]+ +[A-Z]/{gsub(/"/,"",$1); if($1!="CONSTRAINT") print t"."$1}' \
    01_create_fil_rouge_immobilier.sql | wc -l
```

---

## 2. Les 22 tables, une par ligne

Trois paniers, comme au 15/10 :

- 👤 **personne** : la table décrit une personne ;
- 🔗 **liée** : ses colonnes se rattachent à une personne identifiée ;
- ⚪ **aucune** : rien de personnel (paramètres, libellés).

| # | Table | Panier | Colonnes personnelles ou rattachées |
|---|---|---|---|
| 1 | `role` | ⚪ aucune | `wording` : trois libellés (`Client`, `Hunter`, `Manager`) |
| 2 | `"user"` | 👤 personne | `email`, `password` (haché), `is_activated`, `system_role` |
| 3 | `client` | 👤 personne | `first_name`, `last_name`, `phone_number`, `address`, `address_complement`, `postal_code`, `town`, `country_iso`, `gender`, `birth_date`, `is_married`, `is_civil_solidarity_pact`, `nb_children` ; lien `id_user` |
| 4 | `real_estate_manager` | 👤 personne | `first_name`, `last_name`, `phone_number`, `country_iso`, `gender`, `company_name` ; lien `id_user` |
| 5 | `hunter` | 👤 personne | `first_name`, `last_name`, `phone_number`, `country_iso`, `gender`, `company_name`, `hire_date`, `education_level`, `is_carte_t`, `certification_date`, `is_hunter_ai` ; liens `id_user`, `id_realestatemanager` |
| 6 | `search_request` | 🔗 liée | `status` ; liens `id_author`, `id_client`, `id_hunter`, `id_realestatemanager` |
| 7 | `criteria` | 🔗 liée | `budget_min`, `budget_max`, `town`, `postal_code`, `district`, `country_iso`, `change_reason` (texte libre) et les souhaits du bien ; lien `id_author` — le projet d'achat d'un client |
| 8 | `mandate` | 🔗 liée | `signature_date`, `signature_type`, `ends_at`, `is_exclusive`, `status` ; liens `id_client`, `id_hunter` |
| 9 | `estate` | 🔗 liée | `street`, `street_number`, `postal_code`, `town`, `district`, `latitude`, `longitude`, `information` (texte libre) ; lien `id_author` — l'adresse désigne le vendeur (RGPD-7) |
| 10 | `picture` | 🔗 liée | `url` — une photo peut montrer une personne (RGPD-9) |
| 11 | `estate_contact` | 👤 personne (un tiers : le vendeur) | `contact_name`, `phone_number`, `email`, `agency_name`, `is_private` |
| 12 | `estate_price_history` | 🔗 liée, de loin | `price`, `seen_at` d'un bien (`id_estate`) — 💡 rattaché au vendeur par le bien seulement |
| 13 | `estate_searchrequest` | 🔗 liée | `review_hunter` (texte libre), `status` ; lien `id_hunter` |
| 14 | `review_media` | 🔗 liée | `media_url` — un audio ou une vidéo du chasseur, sa voix ou son image |
| 15 | `estate_proposed` | 🔗 liée | `comment_client`, `comment_hunter` (textes libres), `amount_proposition`, `client_priority`, `client_decision`, `client_decided_at`, `decline_reason` ; lien `id_hunter` |
| 16 | `visit` | 🔗 liée | `visit_date`, `visitor_type` ; lien `id_mandate` |
| 17 | `parameters_fees` | ⚪ aucune | barème des honoraires de l'agence |
| 18 | `sale` | 🔗 liée | `signature_date`, `purchase_amount`, `fees_amount`, `sale_origin` ; lien `id_mandate` |
| 19 | `commission_scale` | 🔗 liée | `amount_min`, `amount_max`, `rate`, `valid_from`, `valid_until` ; lien `id_hunter` — le barème d'un chasseur |
| 20 | `hunter_rate_parameters` | ⚪ aucune | paramètres communs du calcul de rémunération |
| 21 | `payment` | 🔗 liée | `amount`, `status`, `announced_at`, `scheduled_for`, `paid_at`, `refusal_reason`, `base_rate`, `final_rate`, `seniority_rate`, `performance_rate`, `performance_score`, `calculation_details` ; lien `id_hunter` — la paie d'un chasseur |
| 22 | `hunter_performance` | 🔗 liée | `score`, `scored_at`, `trigger_type` ; lien `id_hunter` — la note d'un chasseur |

Bilan : **5** tables 👤, **14** tables 🔗, **3** tables ⚪ (5 + 14 + 3 = 22).

---

## 3. Données sensibles

- ✅ Le sujet les définit : « santé, opinions, origine… » (`REG:14`).
- ✅ **Aucune colonne de ces catégories** dans `01` : les 22 tables du § 2,
  relues une par une, n'en ont pas. Les 4 colonnes neuves (§ 4) non plus.
- ✅ `gender`, `birth_date`, `is_married`, `is_civil_solidarity_pact`,
  `nb_children` sont **gardés**, et leur usage s'écrit au registre (RGPD-6).
- 💡 `hunter_performance.score` et `payment.performance_score` notent une
  personne. Le calcul est tracé (`payment.calculation_details`).

---

## 4. Changé depuis le 15/10

Base de comparaison : le commit `0b7e256` du dépôt `Fil-Rouge-API`
(2026-10-15 14:24, FLX4), dernier à toucher `01` avant l'écriture de la
matière (2026-10-15 14:48, commit `d9cd097` de ce dépôt).

```bash
git log --format="%h %ad %s" --date=short 0b7e256..HEAD -- docker/init-v3/01_create_fil_rouge_immobilier.sql
# 64d3195 2026-11-03 SUG5 : Enregistrer la décision du client sur un bien proposé
# 039c684 2026-11-03 SUG4 : Donner un état à chaque bien de la sélection
```

`diff` des colonnes (276 → 280) : **4 colonnes neuves**, aucune retirée,
aucune table neuve (22 → 22).

| Table | Colonne neuve | Fiche | Personnelle ? |
|---|---|---|---|
| `estate_searchrequest` | `status` (`suggested`, `kept`, `dismissed`) | SUG4 | 🔗 le tri d'un chasseur sur la demande d'un client |
| `estate_proposed` | `client_decision` (`pending`, `interested`, `declined`) | SUG5 | 🔗 l'avis d'un client identifié |
| `estate_proposed` | `client_decided_at` | SUG5 | 🔗 la date de cet avis |
| `estate_proposed` | `decline_reason` (`too_expensive`, `too_far`, `too_small`, `wrong_type`, `other`) | SUG5 | 🔗 le motif d'un refus ; liste fermée, pas un texte libre |

Ce que l'inventaire du 15/10 n'avait pas, sans que le schéma ait bougé :

- ⚠️ `estate_price_history` (FLX4, avant la matière) n'y figurait pas :
  ajoutée ici, ligne 12.
- ⚠️ `estate_proposed.client_priority` (LOT7) n'y figurait pas : ajoutée ici,
  ligne 15.
- ⚠️ `search_request`, `mandate`, `visit`, `sale` ont maintenant leur ligne
  propre, avec leurs colonnes.

Côté FLX : aucune colonne ajoutée dans `estate_searchrequest` ni dans
`estate_proposed` après le 15/10 (le `git log` ci-dessus n'a que SUG4 et SUG5).

---

## 5. L'entrepôt OLAP (`08_olap.sql`)

### Ni rue, ni numéro, ni latitude, ni longitude (RGPD-7)

| Mot cherché | `grep -ci` sur `08` | Où | Verdict |
|---|---|---|---|
| `street` | **0** | — | ✅ |
| `latitude` | **0** | — | ✅ |
| `longitude` | **0** | — | ✅ |
| `numero` | **0** | — | ✅ |
| `rue` | **1** | `08:57`, un commentaire | ✅ pas une colonne |
| `adresse` | **2** | `08:55-56`, un commentaire | ✅ pas une colonne |

Les colonnes de lieu gardées : `dim_client.ville`, `dim_client.pays`,
`dim_secteur.code_postal`, `dim_secteur.ville`, `dim_secteur.pays`,
`dim_chasseur.pays`. Aucune ne situe une maison.

### Les numéros de personne gardés (RGPD-13)

| Ligne | Colonne | Renvoie à |
|---|---|---|
| `08_olap.sql:91` | `dim_chasseur.id_hunter` | `hunter.id` |
| `08_olap.sql:100` | `dim_client.id_client` | `client.id` |

➡️ Ces deux numéros relient l'OLAP aux fiches : c'est une
**pseudonymisation**, pas une anonymisation (RGPD-13). Le reste des
dimensions de personnes est sans nom, sans contact, sans date de naissance :
`dim_chasseur` (`annee_embauche`, `est_ia`, `a_carte_t`, `pays`) et
`dim_client` (`annee_inscription`, `ville`, `pays`).

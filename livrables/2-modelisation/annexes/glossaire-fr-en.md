# Glossaire de correspondance français ↔ anglais

> Généré le 2026-11-23 par `annexes/glossaire/generer_glossaire.py`, depuis
> `docker/init-v3/01_create_fil_rouge_immobilier.sql` (dépôt Fil-Rouge-API) : **22 tables, 283 colonnes**.
> Ne pas éditer à la main : corriger le script, puis le relancer. Il refuse d'écrire si
> une table, une colonne ou un statut de la base n'a pas de terme français.

Le code et les schémas (MCD, MLD, MPD) sont en anglais ; le métier se discute en
français avec le client (ADR-002). Ce glossaire fait le lien. Les définitions des
termes métier sont dans le glossaire du sujet (`GLOSSAIRE-METIER.md`, StarterPack).

## Les tables

| Table | En français | Ce qu'elle porte |
|---|---|---|
| `user` | compte (utilisateur) | l'identifiant de connexion : email, mot de passe haché, activation |
| `role` | rôle à fiche | Client, Hunter ou Manager ; Admin et Reader sont sur le compte (system_role) |
| `client` | fiche client (acquéreur) | le particulier qui cherche à acheter |
| `hunter` | fiche chasseur | le chasseur immobilier, rattaché à un manager |
| `real_estate_manager` | fiche manager (gestionnaire immobilier) | le responsable d'une équipe de chasseurs |
| `search_request` | demande de recherche | la demande d'un client, suivie par un chasseur |
| `criteria` | critères de recherche (une version) | ce que cherche le client ; chaque changement crée une version |
| `mandate` | mandat de recherche | le contrat client ↔ chasseur, 6 mois, exclusif ou non |
| `estate` | bien immobilier | le logement, importé des annonces ou saisi à la main |
| `picture` | photo du bien | une photo d'un bien, avec son texte alternatif |
| `estate_contact` | contact du vendeur | l'agence ou le particulier qui vend le bien |
| `estate_price_history` | historique des prix | le prix d'un bien vu à chaque import |
| `estate_searchrequest` | sélection de biens | un bien retenu pour une demande (sélection quotidienne) |
| `review_media` | média d'avis | un audio ou une vidéo joint à l'avis du chasseur sur un bien |
| `estate_proposed` | proposition de bien (présentation) | un bien présenté au client sous un mandat, et l'offre |
| `visit` | visite | une visite d'un bien, par le chasseur ou le client |
| `sale` | vente (acte authentique) | l'acte signé chez le notaire, qui déclenche la rémunération |
| `parameters_fees` | grille d'honoraires | honoraires = montant fixe + taux × prix, versionnés par date |
| `commission_scale` | barème de commission | les tranches de prix et leur taux de base |
| `hunter_rate_parameters` | réglages du taux du chasseur | poids, paliers et bornes du calcul de performance |
| `payment` | paiement du chasseur (versement) | la commission annoncée, programmée, payée ou refusée |
| `hunter_performance` | journal des notes de performance | chaque note du chasseur, datée, avec sa cause |

## Les colonnes, table par table

Une colonne `id_xxx` est une clé étrangère : elle pointe vers la ligne nommée.

### `user` — compte (utilisateur)

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `email` | adresse email |
| `password` | mot de passe (empreinte Argon2, jamais en clair) |
| `is_activated` | compte activé |
| `system_role` | rôle sans fiche (Admin ou Reader) |

### `role` — rôle à fiche

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `wording` | libellé du rôle |

### `client` — fiche client (acquéreur)

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `id_user` | compte de la fiche |
| `role_wording` | rôle de la fiche (Client, Hunter ou Manager) |
| `first_name` | prénom |
| `last_name` | nom |
| `country_iso` | pays (code ISO 3166, 2 lettres) |
| `gender` | genre |
| `phone_number` | téléphone |
| `address` | adresse |
| `address_complement` | complément d'adresse |
| `postal_code` | code postal |
| `town` | ville |
| `is_married` | marié |
| `is_civil_solidarity_pact` | pacsé |
| `nb_children` | nombre d'enfants |
| `birth_date` | date de naissance |

### `hunter` — fiche chasseur

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `id_user` | compte de la fiche |
| `role_wording` | rôle de la fiche (Client, Hunter ou Manager) |
| `first_name` | prénom |
| `last_name` | nom |
| `phone_number` | téléphone |
| `country_iso` | pays (code ISO 3166, 2 lettres) |
| `gender` | genre |
| `company_name` | raison sociale |
| `hire_date` | date d'embauche (base de l'ancienneté) |
| `education_level` | niveau d'études |
| `is_carte_t` | carte professionnelle T (transaction) |
| `certification_date` | date de certification |
| `is_hunter_ai` | chasseur-IA |
| `id_realestatemanager` | manager |

### `real_estate_manager` — fiche manager (gestionnaire immobilier)

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `id_user` | compte de la fiche |
| `role_wording` | rôle de la fiche (Client, Hunter ou Manager) |
| `first_name` | prénom |
| `last_name` | nom |
| `phone_number` | téléphone |
| `country_iso` | pays (code ISO 3166, 2 lettres) |
| `gender` | genre |
| `company_name` | raison sociale |

### `search_request` — demande de recherche

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `id_author` | auteur (compte qui a saisi la ligne) |
| `id_client` | client |
| `id_hunter` | chasseur |
| `id_realestatemanager` | manager |
| `status` | statut (voir les valeurs plus bas) |

### `criteria` — critères de recherche (une version)

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `change_reason` | motif du changement |
| `country_iso` | pays (code ISO 3166, 2 lettres) |
| `town` | ville |
| `postal_code` | code postal |
| `district` | quartier |
| `estate_type` | type de bien |
| `typology` | typologie (T1, T2…) |
| `budget_min` | budget minimum (euros) |
| `budget_max` | budget maximum (euros) |
| `floor` | étage |
| `is_new_build` | neuf |
| `needs_renovation` | travaux à prévoir |
| `energy_class_max` | DPE maximum accepté |
| `rooms_min` | pièces (minimum) |
| `rooms_max` | pièces (maximum) |
| `bedrooms_min` | chambres (minimum) |
| `bedrooms_max` | chambres (maximum) |
| `toilets_min` | WC (minimum) |
| `toilets_max` | WC (maximum) |
| `bathrooms_min` | salles de bain (minimum) |
| `bathrooms_max` | salles de bain (maximum) |
| `swimming_pool_min` | piscines (minimum) |
| `swimming_pool_max` | piscines (maximum) |
| `has_garden` | jardin |
| `nb_balcony_min` | balcons (minimum) |
| `nb_balcony_max` | balcons (maximum) |
| `nb_terrace_min` | terrasses (minimum) |
| `nb_terrace_max` | terrasses (maximum) |
| `is_climatised` | climatisé |
| `surface_min` | surface habitable minimum (m²) |
| `surface_max` | surface habitable maximum (m²) |
| `land_surface_min` | surface du terrain minimum (m²) |
| `land_surface_max` | surface du terrain maximum (m²) |
| `has_separate_kitchen` | cuisine séparée |
| `has_cellar` | cave |
| `has_view` | vue |
| `is_quiet` | calme |
| `is_bright` | lumineux |
| `has_garage` | garage |
| `has_elevator` | ascenseur |
| `has_chimney` | cheminée |
| `parking_spaces` | places de parking |
| `id_author` | auteur (compte qui a saisi la ligne) |
| `id_search_request` | demande de recherche |
| `id_previous_version` | version précédente des critères |

### `mandate` — mandat de recherche

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `reference` | référence |
| `status` | statut (voir les valeurs plus bas) |
| `signature_date` | date de signature |
| `signature_type` | mode de signature |
| `ends_at` | date de fin (validité) |
| `is_exclusive` | mandat exclusif |
| `id_hunter` | chasseur |
| `id_client` | client |
| `id_search_request` | demande de recherche |
| `id_mandate_parent` | mandat renouvelé (le précédent de la chaîne) |

### `estate` — bien immobilier

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `reference` | référence |
| `country_iso` | pays (code ISO 3166, 2 lettres) |
| `estate_type` | type de bien |
| `price` | prix (euros) |
| `construction_date` | date de construction |
| `energy_class` | classe énergie (lettre du DPE) |
| `energy_class_scheme` | référentiel du DPE |
| `energy_class_date` | date du DPE |
| `energy_kwh_m2` | consommation d'énergie (kWh/m²/an) |
| `energy_co2_m2` | émissions de CO2 (kg/m²/an) |
| `latitude` | latitude |
| `longitude` | longitude |
| `floor` | étage |
| `typology` | typologie (T1, T2…) |
| `nb_rooms` | nombre de pièces |
| `nb_bedrooms` | nombre de chambres |
| `nb_bathrooms` | nombre de salles de bain |
| `nb_toilets` | nombre de WC |
| `nb_swimming_pool` | nombre de piscines |
| `has_garden` | jardin |
| `nb_balcony` | nombre de balcons |
| `nb_terrace` | nombre de terrasses |
| `is_climatised` | climatisé |
| `surface` | surface habitable (m²) |
| `land_surface` | surface du terrain (m²) |
| `has_cellar` | cave |
| `has_view` | vue |
| `is_quiet` | calme |
| `is_bright` | lumineux |
| `has_garage` | garage |
| `has_elevator` | ascenseur |
| `has_chimney` | cheminée |
| `parking_spaces` | places de parking |
| `has_separate_kitchen` | cuisine séparée |
| `needs_renovation` | travaux à prévoir |
| `town` | ville |
| `street` | rue |
| `street_number` | numéro de rue |
| `postal_code` | code postal |
| `district` | quartier |
| `information` | description libre |
| `id_author` | auteur (compte qui a saisi la ligne) |

### `picture` — photo du bien

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `url` | adresse de la photo |
| `id_estate` | bien |
| `alt_text` | texte alternatif (accessibilité) |

### `estate_contact` — contact du vendeur

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `is_private` | vendeur particulier |
| `agency_name` | nom de l'agence |
| `contact_name` | nom du contact |
| `phone_number` | téléphone |
| `email` | adresse email |
| `id_estate` | bien |
| `id_author` | auteur (compte qui a saisi la ligne) |

### `estate_price_history` — historique des prix

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `id_estate` | bien |
| `price` | prix (euros) |
| `seen_at` | date de l'import où le prix a été vu |

### `estate_searchrequest` — sélection de biens

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `review_hunter` | avis du chasseur |
| `id_estate` | bien |
| `id_search_request` | demande de recherche |
| `id_hunter` | chasseur |
| `status` | statut (voir les valeurs plus bas) |

### `review_media` — média d'avis

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `media_url` | adresse du média |
| `media_type` | type de média |
| `id_estate_searchrequest` | bien de la sélection |

### `estate_proposed` — proposition de bien (présentation)

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `comment_hunter` | commentaire du chasseur |
| `comment_client` | commentaire du client |
| `amount_proposition` | montant de l'offre (euros) |
| `proposition_status` | statut de la proposition |
| `id_hunter` | chasseur |
| `id_estate` | bien |
| `id_mandate` | mandat |
| `client_priority` | priorité donnée par le client (1 à 5) |
| `client_decision` | décision du client |
| `client_decided_at` | date de la décision du client |
| `decline_reason` | motif du refus du client |

### `visit` — visite

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `visit_date` | date de la visite |
| `visitor_type` | qui visite |
| `id_estate` | bien |
| `id_mandate` | mandat |

### `sale` — vente (acte authentique)

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `signature_date` | date de signature |
| `purchase_amount` | prix d'achat à l'acte (euros) |
| `fees_amount` | honoraires de l'acte (euros, au centime) |
| `sale_origin` | origine de la vente |
| `id_mandate` | mandat |
| `id_estate` | bien |
| `id_parameters_fees` | grille d'honoraires appliquée |

### `parameters_fees` — grille d'honoraires

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `effective_from` | en vigueur à partir du |
| `fixed_amount` | part fixe des honoraires (euros) |
| `rate` | taux |

### `commission_scale` — barème de commission

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `amount_min` | borne basse de la tranche (euros) |
| `amount_max` | borne haute de la tranche (euros) |
| `rate` | taux |
| `valid_from` | valable à partir du |
| `valid_until` | valable jusqu'au |
| `id_hunter` | chasseur |

### `hunter_rate_parameters` — réglages du taux du chasseur

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `effective_from` | en vigueur à partir du |
| `weight_delay` | poids du délai (poids_delai) |
| `weight_exclusivity` | poids de l'exclusivité (poids_exclusivite) |
| `weight_sales` | poids des ventes (poids_ventes) |
| `weight_mandates` | poids des mandats (poids_mandats) |
| `weight_visits` | poids des visites (poids_visites) |
| `delay_tiers` | paliers du délai, en semaines (paliers_delai) |
| `visit_tiers` | paliers des visites (paliers_visites) |
| `score_exclusive` | note d'un mandat exclusif (note_exclusif) |
| `score_non_exclusive` | note d'un mandat non exclusif (note_non_exclusif) |
| `points_per_sale` | points par vente (points_par_vente) |
| `points_per_mandate` | points par mandat (plus lu depuis ADR-048) |
| `mandate_success_rate_for_max_score` | taux ventes ÷ mandats qui vaut la note maximale (ADR-048) |
| `window_months` | fenêtre de calcul, en mois (fenetre_mois) |
| `seniority_rate_per_year` | majoration par année d'ancienneté (taux_par_annee) |
| `seniority_cap` | plafond de l'ancienneté (plafond_anciennete) |
| `score_pivot` | note pivot (score_pivot) |
| `score_half_range` | demi-amplitude de la note (demi_amplitude_score) |
| `performance_amplitude` | amplitude de la performance (amplitude_performance) |
| `rate_floor` | taux plancher (taux_plancher) |
| `rate_ceiling` | taux plafond (taux_plafond) |

### `payment` — paiement du chasseur (versement)

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `amount` | montant (euros, au centime) |
| `status` | statut (voir les valeurs plus bas) |
| `announced_at` | date d'annonce |
| `scheduled_for` | date de versement prévue |
| `paid_at` | date de versement |
| `refusal_reason` | motif du refus de rémunération |
| `base_rate` | taux de base (barème) |
| `final_rate` | taux final |
| `seniority_rate` | majoration d'ancienneté |
| `performance_rate` | modulation de performance |
| `performance_score` | note de performance |
| `calculation_details` | détail du calcul (JSON) |
| `id_sale` | vente |
| `id_hunter` | chasseur |
| `id_commission_scale` | tranche de barème appliquée |
| `id_hunter_rate_parameters` | version des réglages appliquée |

### `hunter_performance` — journal des notes de performance

| Colonne | En français |
|---|---|
| `id` | identifiant (clé technique) |
| `created_at` | date de création de la ligne |
| `score` | note |
| `scored_at` | date de la note |
| `trigger_type` | cause de la note |
| `id_hunter` | chasseur |
| `id_payment` | paiement |
| `id_mandate` | mandat |

## Les valeurs des statuts et catégories

| Table.colonne | Valeur | En français |
|---|---|---|
| `role.wording` | `Client` | client |
| `role.wording` | `Hunter` | chasseur |
| `role.wording` | `Manager` | manager |
| `user.system_role` | `Admin` | administrateur |
| `user.system_role` | `Reader` | lecteur (lecture seule) |
| `search_request.status` | `confirmed` | enregistrée, en attente d'un chasseur |
| `search_request.status` | `accepted` | acceptée par le chasseur |
| `search_request.status` | `rejected` | refusée par le chasseur |
| `search_request.status` | `launched` | lancée (mandat signé) |
| `mandate.status` | `active` | actif |
| `mandate.status` | `completed` | terminé par une vente |
| `mandate.status` | `expired` | expiré |
| `mandate.status` | `renewed` | renouvelé |
| `mandate.status` | `canceled` | annulé |
| `mandate.status` | `pending_signature` | en attente de signature |
| `mandate.status` | `lost` | perdu (vente perdue, personne n'est payé) |
| `mandate.signature_type` | `electronic` | électronique |
| `mandate.signature_type` | `paper` | papier |
| `estate_searchrequest.status` | `suggested` | suggéré (par la machine) |
| `estate_searchrequest.status` | `kept` | gardé par le chasseur |
| `estate_searchrequest.status` | `dismissed` | écarté |
| `review_media.media_type` | `audio` | audio |
| `review_media.media_type` | `video` | vidéo |
| `estate_proposed.proposition_status` | `proposed` | proposé au client |
| `estate_proposed.proposition_status` | `offer_pending` | offre transmise, en attente du vendeur |
| `estate_proposed.proposition_status` | `accepted` | acceptée par le vendeur |
| `estate_proposed.proposition_status` | `signed` | offre signée par le client, pas encore envoyée |
| `estate_proposed.proposition_status` | `rejected` | refusée par le vendeur |
| `estate_proposed.client_decision` | `pending` | en attente |
| `estate_proposed.client_decision` | `interested` | intéressé |
| `estate_proposed.client_decision` | `declined` | pas intéressé |
| `estate_proposed.decline_reason` | `too_expensive` | trop cher |
| `estate_proposed.decline_reason` | `too_far` | trop loin |
| `estate_proposed.decline_reason` | `too_small` | trop petit |
| `estate_proposed.decline_reason` | `wrong_type` | pas le bon type |
| `estate_proposed.decline_reason` | `other` | autre |
| `visit.visitor_type` | `hunter` | chasseur |
| `visit.visitor_type` | `client` | client |
| `sale.sale_origin` | `hunter` | trouvé par le chasseur |
| `sale.sale_origin` | `client_alone` | trouvé seul par le client |
| `payment.status` | `refused` | refusé |
| `payment.status` | `announced` | annoncé |
| `payment.status` | `scheduled` | programmé |
| `payment.status` | `paid` | payé |
| `payment.refusal_reason` | `mandate_expired` | mandat expiré à la date de l'acte |
| `payment.refusal_reason` | `out_of_scope` | hors dispositif (non exclusif, client seul) |
| `hunter_performance.trigger_type` | `initial` | note de départ |
| `hunter_performance.trigger_type` | `payment` | après un paiement |
| `hunter_performance.trigger_type` | `mandate_expired` | mandat éteint sans vente |

Les types de bien (`Appartement`, `Maison`…), les typologies (`T3 / F3`…) et les
étages sont déjà en français dans la base : ils ne se traduisent pas.

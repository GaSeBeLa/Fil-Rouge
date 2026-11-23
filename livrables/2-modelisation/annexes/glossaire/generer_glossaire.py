"""Génère le glossaire de correspondance français ↔ anglais (ADR-002).

Usage, depuis la racine du dépôt Fil-Rouge :
    python livrables/2-modelisation/annexes/glossaire/generer_glossaire.py \
        ../Fil-Rouge-API/docker/init-v3/01_create_fil_rouge_immobilier.sql

Lit le schéma de référence, et écrit `annexes/glossaire-fr-en.md`.
Refuse d'écrire (code 1) si une table, une colonne ou une valeur de statut
du schéma n'a pas de terme français, ou si ce fichier en traduit une qui
n'existe plus : le glossaire suit toujours la base.
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

SQL_TYPES = (r"(SERIAL|BIGSERIAL|INTEGER|INT|SMALLINT|BIGINT|VARCHAR|CHAR|TEXT|BOOLEAN|DATE|"
             r"TIMESTAMPTZ|TIMESTAMP|NUMERIC|DECIMAL|JSONB|JSON|REAL|DOUBLE|UUID)\b")

# Table -> (terme français, ce qu'elle porte). Ordre = ordre du glossaire.
TABLES: dict[str, tuple[str, str]] = {
    "user": ("compte (utilisateur)", "l'identifiant de connexion : email, mot de passe haché, activation"),
    "role": ("rôle à fiche", "Client, Hunter ou Manager ; Admin et Reader sont sur le compte (system_role)"),
    "client": ("fiche client (acquéreur)", "le particulier qui cherche à acheter"),
    "hunter": ("fiche chasseur", "le chasseur immobilier, rattaché à un manager"),
    "real_estate_manager": ("fiche manager (gestionnaire immobilier)", "le responsable d'une équipe de chasseurs"),
    "search_request": ("demande de recherche", "la demande d'un client, suivie par un chasseur"),
    "criteria": ("critères de recherche (une version)", "ce que cherche le client ; chaque changement crée une version"),
    "mandate": ("mandat de recherche", "le contrat client ↔ chasseur, 6 mois, exclusif ou non"),
    "estate": ("bien immobilier", "le logement, importé des annonces ou saisi à la main"),
    "picture": ("photo du bien", "une photo d'un bien, avec son texte alternatif"),
    "estate_contact": ("contact du vendeur", "l'agence ou le particulier qui vend le bien"),
    "estate_price_history": ("historique des prix", "le prix d'un bien vu à chaque import"),
    "estate_searchrequest": ("sélection de biens", "un bien retenu pour une demande (sélection quotidienne)"),
    "review_media": ("média d'avis", "un audio ou une vidéo joint à l'avis du chasseur sur un bien"),
    "estate_proposed": ("proposition de bien (présentation)", "un bien présenté au client sous un mandat, et l'offre"),
    "visit": ("visite", "une visite d'un bien, par le chasseur ou le client"),
    "sale": ("vente (acte authentique)", "l'acte signé chez le notaire, qui déclenche la rémunération"),
    "parameters_fees": ("grille d'honoraires", "honoraires = montant fixe + taux × prix, versionnés par date"),
    "commission_scale": ("barème de commission", "les tranches de prix et leur taux de base"),
    "hunter_rate_parameters": ("réglages du taux du chasseur", "poids, paliers et bornes du calcul de performance"),
    "payment": ("paiement du chasseur (versement)", "la commission annoncée, programmée, payée ou refusée"),
    "hunter_performance": ("journal des notes de performance", "chaque note du chasseur, datée, avec sa cause"),
}

# Nom de colonne -> terme français. Un même nom a le même sens dans toutes les tables.
COLUMNS: dict[str, str] = {
    # Commun
    "id": "identifiant (clé technique)",
    "created_at": "date de création de la ligne",
    "id_author": "auteur (compte qui a saisi la ligne)",
    "reference": "référence",
    "status": "statut (voir les valeurs plus bas)",
    "wording": "libellé du rôle",
    "role_wording": "rôle de la fiche (Client, Hunter ou Manager)",
    # Compte et fiches
    "email": "adresse email",
    "password": "mot de passe (empreinte Argon2, jamais en clair)",
    "is_activated": "compte activé",
    "system_role": "rôle sans fiche (Admin ou Reader)",
    "id_user": "compte de la fiche",
    "first_name": "prénom",
    "last_name": "nom",
    "gender": "genre",
    "birth_date": "date de naissance",
    "phone_number": "téléphone",
    "country_iso": "pays (code ISO 3166, 2 lettres)",
    "town": "ville",
    "address": "adresse",
    "address_complement": "complément d'adresse",
    "postal_code": "code postal",
    "district": "quartier",
    "street": "rue",
    "street_number": "numéro de rue",
    "is_married": "marié",
    "is_civil_solidarity_pact": "pacsé",
    "nb_children": "nombre d'enfants",
    "company_name": "raison sociale",
    "hire_date": "date d'embauche (base de l'ancienneté)",
    "education_level": "niveau d'études",
    "is_carte_t": "carte professionnelle T (transaction)",
    "certification_date": "date de certification",
    "is_hunter_ai": "chasseur-IA",
    "id_realestatemanager": "manager",
    # Demande, critères, mandat
    "id_client": "client",
    "id_hunter": "chasseur",
    "id_search_request": "demande de recherche",
    "id_previous_version": "version précédente des critères",
    "change_reason": "motif du changement",
    "estate_type": "type de bien",
    "typology": "typologie (T1, T2…)",
    "budget_min": "budget minimum (euros)",
    "budget_max": "budget maximum (euros)",
    "floor": "étage",
    "is_new_build": "neuf",
    "needs_renovation": "travaux à prévoir",
    "energy_class_max": "DPE maximum accepté",
    "rooms_min": "pièces (minimum)",
    "rooms_max": "pièces (maximum)",
    "bedrooms_min": "chambres (minimum)",
    "bedrooms_max": "chambres (maximum)",
    "toilets_min": "WC (minimum)",
    "toilets_max": "WC (maximum)",
    "bathrooms_min": "salles de bain (minimum)",
    "bathrooms_max": "salles de bain (maximum)",
    "swimming_pool_min": "piscines (minimum)",
    "swimming_pool_max": "piscines (maximum)",
    "has_garden": "jardin",
    "nb_balcony_min": "balcons (minimum)",
    "nb_balcony_max": "balcons (maximum)",
    "nb_terrace_min": "terrasses (minimum)",
    "nb_terrace_max": "terrasses (maximum)",
    "is_climatised": "climatisé",
    "surface_min": "surface habitable minimum (m²)",
    "surface_max": "surface habitable maximum (m²)",
    "land_surface_min": "surface du terrain minimum (m²)",
    "land_surface_max": "surface du terrain maximum (m²)",
    "has_separate_kitchen": "cuisine séparée",
    "has_cellar": "cave",
    "has_view": "vue",
    "is_quiet": "calme",
    "is_bright": "lumineux",
    "has_garage": "garage",
    "has_elevator": "ascenseur",
    "has_chimney": "cheminée",
    "parking_spaces": "places de parking",
    "signature_date": "date de signature",
    "signature_type": "mode de signature",
    "ends_at": "date de fin (validité)",
    "is_exclusive": "mandat exclusif",
    "id_mandate": "mandat",
    "id_mandate_parent": "mandat renouvelé (le précédent de la chaîne)",
    # Bien
    "price": "prix (euros)",
    "construction_date": "date de construction",
    "energy_class": "classe énergie (lettre du DPE)",
    "energy_class_scheme": "référentiel du DPE",
    "energy_class_date": "date du DPE",
    "energy_kwh_m2": "consommation d'énergie (kWh/m²/an)",
    "energy_co2_m2": "émissions de CO2 (kg/m²/an)",
    "latitude": "latitude",
    "longitude": "longitude",
    "nb_rooms": "nombre de pièces",
    "nb_bedrooms": "nombre de chambres",
    "nb_bathrooms": "nombre de salles de bain",
    "nb_toilets": "nombre de WC",
    "nb_swimming_pool": "nombre de piscines",
    "nb_balcony": "nombre de balcons",
    "nb_terrace": "nombre de terrasses",
    "surface": "surface habitable (m²)",
    "land_surface": "surface du terrain (m²)",
    "information": "description libre",
    "id_estate": "bien",
    "url": "adresse de la photo",
    "alt_text": "texte alternatif (accessibilité)",
    "is_private": "vendeur particulier",
    "agency_name": "nom de l'agence",
    "contact_name": "nom du contact",
    "seen_at": "date de l'import où le prix a été vu",
    # Sélection, proposition, visite
    "review_hunter": "avis du chasseur",
    "media_url": "adresse du média",
    "media_type": "type de média",
    "id_estate_searchrequest": "bien de la sélection",
    "comment_hunter": "commentaire du chasseur",
    "comment_client": "commentaire du client",
    "amount_proposition": "montant de l'offre (euros)",
    "proposition_status": "statut de la proposition",
    "client_priority": "priorité donnée par le client (1 à 5)",
    "client_decision": "décision du client",
    "client_decided_at": "date de la décision du client",
    "decline_reason": "motif du refus du client",
    "visit_date": "date de la visite",
    "visitor_type": "qui visite",
    # Vente et argent
    "purchase_amount": "prix d'achat à l'acte (euros)",
    "fees_amount": "honoraires de l'acte (euros, au centime)",
    "sale_origin": "origine de la vente",
    "id_parameters_fees": "grille d'honoraires appliquée",
    "effective_from": "en vigueur à partir du",
    "fixed_amount": "part fixe des honoraires (euros)",
    "rate": "taux",
    "amount_min": "borne basse de la tranche (euros)",
    "amount_max": "borne haute de la tranche (euros)",
    "valid_from": "valable à partir du",
    "valid_until": "valable jusqu'au",
    "amount": "montant (euros, au centime)",
    "announced_at": "date d'annonce",
    "scheduled_for": "date de versement prévue",
    "paid_at": "date de versement",
    "refusal_reason": "motif du refus de rémunération",
    "base_rate": "taux de base (barème)",
    "seniority_rate": "majoration d'ancienneté",
    "performance_rate": "modulation de performance",
    "final_rate": "taux final",
    "performance_score": "note de performance",
    "calculation_details": "détail du calcul (JSON)",
    "id_sale": "vente",
    "id_commission_scale": "tranche de barème appliquée",
    "id_hunter_rate_parameters": "version des réglages appliquée",
    "id_payment": "paiement",
    # Réglages du taux (noms français de remuneration.py, code du sujet)
    "weight_delay": "poids du délai (poids_delai)",
    "weight_exclusivity": "poids de l'exclusivité (poids_exclusivite)",
    "weight_sales": "poids des ventes (poids_ventes)",
    "weight_mandates": "poids des mandats (poids_mandats)",
    "weight_visits": "poids des visites (poids_visites)",
    "delay_tiers": "paliers du délai, en semaines (paliers_delai)",
    "visit_tiers": "paliers des visites (paliers_visites)",
    "score_exclusive": "note d'un mandat exclusif (note_exclusif)",
    "score_non_exclusive": "note d'un mandat non exclusif (note_non_exclusif)",
    "points_per_sale": "points par vente (points_par_vente)",
    "points_per_mandate": "points par mandat (plus lu depuis ADR-048)",
    "mandate_success_rate_for_max_score": "taux ventes ÷ mandats qui vaut la note maximale (ADR-048)",
    "window_months": "fenêtre de calcul, en mois (fenetre_mois)",
    "seniority_rate_per_year": "majoration par année d'ancienneté (taux_par_annee)",
    "seniority_cap": "plafond de l'ancienneté (plafond_anciennete)",
    "score_pivot": "note pivot (score_pivot)",
    "score_half_range": "demi-amplitude de la note (demi_amplitude_score)",
    "performance_amplitude": "amplitude de la performance (amplitude_performance)",
    "rate_floor": "taux plancher (taux_plancher)",
    "rate_ceiling": "taux plafond (taux_plafond)",
    # Journal des notes
    "score": "note",
    "scored_at": "date de la note",
    "trigger_type": "cause de la note",
}

# (table, colonne) -> {valeur: terme français}. Seulement les colonnes de statut ou de catégorie.
VALUES: dict[tuple[str, str], dict[str, str]] = {
    ("role", "wording"): {"Client": "client", "Hunter": "chasseur", "Manager": "manager"},
    ("user", "system_role"): {"Admin": "administrateur", "Reader": "lecteur (lecture seule)"},
    ("search_request", "status"): {"confirmed": "enregistrée, en attente d'un chasseur",
                                   "accepted": "acceptée par le chasseur", "rejected": "refusée par le chasseur",
                                   "launched": "lancée (mandat signé)"},
    ("mandate", "status"): {"pending_signature": "en attente de signature", "active": "actif",
                            "completed": "terminé par une vente", "expired": "expiré", "renewed": "renouvelé",
                            "canceled": "annulé", "lost": "perdu (vente perdue, personne n'est payé)"},
    ("mandate", "signature_type"): {"electronic": "électronique", "paper": "papier"},
    ("estate_searchrequest", "status"): {"suggested": "suggéré (par la machine)", "kept": "gardé par le chasseur",
                                         "dismissed": "écarté"},
    ("review_media", "media_type"): {"audio": "audio", "video": "vidéo"},
    ("estate_proposed", "proposition_status"): {"proposed": "proposé au client", "signed": "offre signée par le client, pas encore envoyée",
                                                "offer_pending": "offre transmise, en attente du vendeur",
                                                "accepted": "acceptée par le vendeur", "rejected": "refusée par le vendeur"},
    ("estate_proposed", "client_decision"): {"pending": "en attente", "interested": "intéressé",
                                             "declined": "pas intéressé"},
    ("estate_proposed", "decline_reason"): {"too_expensive": "trop cher", "too_far": "trop loin",
                                            "too_small": "trop petit", "wrong_type": "pas le bon type",
                                            "other": "autre"},
    ("visit", "visitor_type"): {"hunter": "chasseur", "client": "client"},
    ("sale", "sale_origin"): {"hunter": "trouvé par le chasseur", "client_alone": "trouvé seul par le client"},
    ("payment", "status"): {"announced": "annoncé", "scheduled": "programmé", "paid": "payé", "refused": "refusé"},
    ("payment", "refusal_reason"): {"mandate_expired": "mandat expiré à la date de l'acte",
                                    "out_of_scope": "hors dispositif (non exclusif, client seul)"},
    ("hunter_performance", "trigger_type"): {"initial": "note de départ", "payment": "après un paiement",
                                             "mandate_expired": "mandat éteint sans vente"},
}


def read_schema(sql: str) -> dict[str, dict[str, list[str]]]:
    """Rend {table: {"columns": [...], colonne: [valeurs du CHECK IN]}}.

    Les commentaires `--` sont retirés d'abord. Une colonne est une ligne
    « nom_en_minuscules TYPE » dans le CREATE TABLE ; les valeurs viennent
    du premier `colonne IN ('a', 'b')` trouvé pour cette colonne.
    """
    sql = re.sub(r"--[^\n]*", "", sql)
    schema: dict[str, dict[str, list[str]]] = {}
    for match in re.finditer(r'CREATE TABLE\s+"?(\w+)"?\s*\((.*?)\n\);', sql, re.S):
        table, body = match.group(1), match.group(2)
        columns = [m.group(1) for line in body.split("\n")
                   if (m := re.match(r'\s*"?([a-z_0-9]+)"?\s+' + SQL_TYPES, line))]
        entry: dict[str, list[str]] = {"columns": columns}
        for column in columns:
            found = re.search(rf"\b{column}\s+IN\s*\(([^)]*)\)", body)
            if found:
                entry[column] = re.findall(r"'([^']*)'", found.group(1))
        schema[table] = entry
    return schema


def check(schema: dict[str, dict[str, list[str]]]) -> list[str]:
    """Les écarts entre le schéma et ce fichier ; liste vide si tout colle."""
    problems = [f"table sans terme français : {t}" for t in schema if t not in TABLES]
    problems += [f"table traduite mais absente du schéma : {t}" for t in TABLES if t not in schema]
    used = {c for entry in schema.values() for c in entry["columns"]}
    problems += [f"colonne sans terme français : {c}" for c in sorted(used - COLUMNS.keys())]
    problems += [f"colonne traduite mais absente du schéma : {c}" for c in sorted(COLUMNS.keys() - used)]
    for (table, column), terms in VALUES.items():
        actual = schema.get(table, {}).get(column)
        if actual is None:
            problems.append(f"valeurs sans CHECK IN dans le schéma : {table}.{column}")
        elif set(actual) != set(terms):
            problems.append(f"valeurs différentes pour {table}.{column} : schéma {sorted(actual)}, "
                            f"glossaire {sorted(terms)}")
    return problems


def render(schema: dict[str, dict[str, list[str]]], source: str) -> str:
    """Le glossaire en Markdown : tables, colonnes par table, valeurs."""
    n_cols = sum(len(e["columns"]) for e in schema.values())
    out = [
        "# Glossaire de correspondance français ↔ anglais",
        "",
        f"> Généré le {date.today():%Y-%m-%d} par `annexes/glossaire/generer_glossaire.py`, depuis",
        f"> `{source}` (dépôt Fil-Rouge-API) : **{len(schema)} tables, {n_cols} colonnes**.",
        "> Ne pas éditer à la main : corriger le script, puis le relancer. Il refuse d'écrire si",
        "> une table, une colonne ou un statut de la base n'a pas de terme français.",
        "",
        "Le code et les schémas (MCD, MLD, MPD) sont en anglais ; le métier se discute en",
        "français avec le client (ADR-002). Ce glossaire fait le lien. Les définitions des",
        "termes métier sont dans le glossaire du sujet (`GLOSSAIRE-METIER.md`, StarterPack).",
        "",
        "## Les tables",
        "",
        "| Table | En français | Ce qu'elle porte |",
        "|---|---|---|",
    ]
    out += [f"| `{t}` | {fr} | {what} |" for t, (fr, what) in TABLES.items()]
    out += ["", "## Les colonnes, table par table", "",
            "Une colonne `id_xxx` est une clé étrangère : elle pointe vers la ligne nommée.", ""]
    for table, (fr, _) in TABLES.items():
        cols = schema[table]["columns"]
        out += [f"### `{table}` — {fr}", "", "| Colonne | En français |", "|---|---|"]
        out += [f"| `{c}` | {COLUMNS[c]} |" for c in cols]
        out.append("")
    out += ["## Les valeurs des statuts et catégories", "",
            "| Table.colonne | Valeur | En français |", "|---|---|---|"]
    for (table, column), terms in VALUES.items():
        out += [f"| `{table}.{column}` | `{v}` | {terms[v]} |" for v in schema[table][column]]
    out += ["", "Les types de bien (`Appartement`, `Maison`…), les typologies (`T3 / F3`…) et les",
            "étages sont déjà en français dans la base : ils ne se traduisent pas.", ""]
    return "\n".join(out)


def main() -> int:
    """Écrit le glossaire à côté du dossier du script ; 1 si le schéma et le glossaire divergent."""
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    sql_path = Path(sys.argv[1])
    schema = read_schema(sql_path.read_text(encoding="utf-8"))
    problems = check(schema)
    for p in problems:
        print(f"ÉCART : {p}")
    if problems:
        print(f"Glossaire NON écrit : {len(problems)} écart(s).")
        return 1
    target = Path(__file__).resolve().parent.parent / "glossaire-fr-en.md"
    target.write_text(render(schema, "docker/init-v3/" + sql_path.name), encoding="utf-8", newline="\n")
    n_cols = sum(len(e["columns"]) for e in schema.values())
    print(f"Écrit : {target.name} — {len(schema)} tables, {n_cols} colonnes, {len(VALUES)} listes de valeurs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

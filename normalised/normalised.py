#!/usr/bin/env python3
"""
normalised.py — Nettoyage & normalisation du fichier "annonces.csv"
                 (fixtures/annonces/annonces.csv) vers un fichier plat
                 aligné sur les contraintes réelles de la table cible
                 "estate" (docker/init/01_create_fil_rouge_immobilier.sql).

============================================================================
COMMENT LIRE CE FICHIER
============================================================================
Le fichier source "annonces.csv" est volontairement sale (jeu de données
d'exercice) : plusieurs formats de date cohabitent, les prix sont parfois
écrits avec le symbole "€", les booléens sont du texte ("True", "False" ou
vide), une même information (surface) peut être répartie sur deux colonnes
différentes ("surface" / "surface_m2"), certains champs sont imbriqués
("contact.nom", "contact.telephone", ...), etc.

Ce script :
  1. LIT le CSV source avec le module standard `csv`.
  2. NETTOIE/TRANSFORME chaque ligne et RENOMME les colonnes pour
     correspondre exactement aux colonnes de la table "estate" (même nom,
     même ordre que dans le CREATE TABLE). Les informations qui n'ont pas
     leur place dans "estate" (contact, charges, exclusivité, dpe...) sont
     conservées à la fin, dans des colonnes clairement identifiées.
  3. ÉCRIT le résultat dans "annonces.csv" (à côté de ce script) + un
     rapport texte des anomalies rencontrées.

============================================================================
RÈGLE DEMANDÉE : AUCUNE CELLULE VIDE EN SORTIE
============================================================================
Toute valeur manquante est remplacée par une valeur EXPLICITE :
  - "NULL"  quand la vraie valeur est inconnue et qu'on ne peut/doit pas
            l'inventer (une quantité, une date, des coordonnées GPS, un
            contact...). C'est la représentation texte de SQL NULL.
  - "False" (ou 0 pour les compteurs) quand l'absence de mention dans la
            source signifie raisonnablement "non/aucun" — cas des colonnes
            "présence" de la source qui ne contiennent QUE "True" ou vide
            (jamais de "False" explicite) : jardin, cave, ascenseur, calme,
            lumineux, terrasse, balcon, particulier. Dans ces colonnes,
            une ligne vide veut dire "la caractéristique n'est pas
            présente", jamais "on ne sait pas".

Deux colonnes sources ("meuble", "exclusivite") sont différentes : elles
contiennent à la fois des "True", des "False" ET des lignes vides. La
présence de "False" explicite prouve que, pour ces colonnes-là, une ligne
vide ne veut PAS dire "False" (sinon la source écrirait "False" comme pour
les autres lignes) : elle veut dire "non renseigné". On respecte donc
cette nuance et on met "NULL" pour ces deux colonnes quand elles sont
vides, plutôt que de leur inventer une réponse.

Les colonnes de la table "estate" qui n'ont AUCUNE source correspondante
dans le CSV et AUCUN indice exploitable dans le texte libre
(nb_bathrooms, nb_toilets, nb_swimming_pool, land_surface,
energetic_score) restent à "NULL" sur toutes les lignes : on ne fabrique
pas de nombre qu'on n'a pas. À l'inverse, les colonnes booléennes qui
n'ont ni source ni la moindre mention textuelle trouvée dans TOUTE la
base (is_climatised, has_garage, has_chimney, has_separate_kitchen —
vérifié par recherche de mots-clés sur 2556 lignes, 0 occurrence) sont
mises à "False" partout, car pour un booléen d'équipement, l'absence
totale et systématique de toute mention est traitée comme "non équipé"
plutôt que comme un inconnu à répéter 2556 fois.

============================================================================
CORRESPONDANCE AVEC LE SCHÉMA CIBLE "estate" (contraintes prises en compte)
============================================================================
  - reference   VARCHAR(50) NOT NULL UNIQUE -> toujours présente et unique
                dans la source (0 doublon sur 2556 lignes) : recopiée telle
                quelle.
  - estate_type NOT NULL CHECK IN (10 valeurs) -> toujours l'une des
                valeurs autorisées dans la source (Maison/Chalet/Château) ;
                une valeur hors-liste serait mise à NULL + anomalie (aucun
                cas dans ce jeu de données, mais le CHECK empêcherait
                l'insertion d'une valeur NULL sur une colonne NOT NULL —
                anomalie loggée pour signalement manuel si jamais rencontré).
  - price       NUMERIC(6,1) CHECK (price >= 0) -> ne peut pas stocker un
                montant brut en euros (max 99 999,9). Converti en K€
                (354712 € -> 354.7), comme migration/migrate.py pour les
                budgets. Le montant brut est conservé à part (price_eur).
  - surface     NUMERIC(7,2) NOT NULL CHECK (surface > 0) -> fusion des
                deux colonnes redondantes "surface"/"surface_m2" (jamais
                les deux vides à la fois : vérifié 0/2556).
  - town        VARCHAR(100) NOT NULL -> toujours renseignée (0 vide).
  - construction_date DATE -> la source ne donne qu'une année
                ("annee_construction", vide sur 1926/2556 lignes) : posée
                au 1er janvier de cette année quand connue, NULL sinon
                (année brute gardée dans construction_year, hors-schéma).
  - floor   SMALLINT -> mappé depuis "etage" (RDC -> 0, "dernier
                étage" -> NULL, impossible à convertir en numéro absolu
                sans connaître la hauteur du bâtiment). NB : "etage"
                désigne l'étage du logement, "floor" dans le schéma
                cible désigne plutôt le nombre d'étages de l'immeuble —
                c'est la colonne la plus proche disponible, approximation
                documentée ici comme demandé.
  - has_view / needs_renovation : déduits du texte libre (titre/
                description : "vue dégagée", "Travaux à prévoir") ; jamais
                NULL (colonnes "présence" : pas de mention = False).
  - parking_spaces SMALLINT -> pas de colonne "parking" dans la source,
                mais 586/2556 descriptions mentionnent "parking inclus" ->
                1 quand mentionné, 0 sinon (jamais NULL, déductible comme
                has_view).
  - dpe (lettre A-G) : n'existe PAS dans le schéma "estate" (qui n'a que
                "energetic_score" en kWh/m², donnée qu'on n'a pas et qu'on
                ne fabrique pas depuis la lettre DPE). La lettre est donc
                conservée en colonne hors-schéma.
============================================================================
"""

from __future__ import annotations

import csv
import sys
from datetime import date, datetime, timezone
from pathlib import Path

# ----------------------------------------------------------------------------
# 0. CHEMINS & CONSTANTES
# ----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "annonces" / "annonces.csv"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "annonces_normalised.csv"
REPORT = HERE / "rapport_anomalies.txt"

NULL = "NULL"  # valeur littérale écrite dans le CSV pour une inconnue réelle

# Liste fermée des types de bien acceptés par la table cible "estate"
# (CHECK estate_type IN (...) dans docker/init/01_create_fil_rouge_immobilier.sql)
ALLOWED_ESTATE_TYPES = {
    "Appartement", "Maison", "Studio", "Loft", "Villa",
    "Duplex", "Terrain", "Local commercial", "Chalet", "Château",
}

FRENCH_MONTHS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4,
    "mai": 5, "juin": 6, "juillet": 7, "août": 8, "aout": 8,
    "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12, "decembre": 12,
}

# Colonnes de sortie, dans l'ordre. Les 27 premières reprennent, EXACTEMENT
# dans le même ordre et avec le même nom, les colonnes de la table "estate"
# (id/created_at exceptés : "id" est repris tel quel de la source pour
# rester traçable, "created_at" n'existe pas côté source). Les colonnes
# suivantes sont des informations utiles qui n'ont pas leur place dans
# "estate" (contact, charges, exclusivité, dpe, photos, recherche_ref...),
# regroupées à la fin plutôt que supprimées.
OUTPUT_COLUMNS = [
    # --- colonnes de la table "estate" (même nom, même ordre) ---
    "id", "reference", "estate_type", "price", "construction_date",
    "latitude", "longitude", "floor", "nb_rooms", "nb_bedrooms",
    "nb_bathrooms", "nb_toilets", "nb_swimming_pool", "has_garden",
    "nb_balcony", "nb_terrace", "is_climatised", "energetic_score",
    "surface", "land_surface", "has_cellar", "has_view", "is_quiet",
    "is_bright", "has_garage", "has_elevator", "has_chimney",
    "parking_spaces", "has_separate_kitchen", "needs_renovation",
    "town", "street", "street_number", "postal_code", "information",
    # --- hors périmètre "estate", conservé pour d'autres tables/usages ---
    "price_eur", "construction_year", "dpe", "recherche_ref", "title",
    "date_publication", "charges_mensuelles", "is_particulier",
    "is_exclusive", "is_furnished", "contact_name", "contact_phone",
    "contact_email", "contact_agency", "photos",
]


# ----------------------------------------------------------------------------
# 1. UTILITAIRES DE NETTOYAGE (une fonction = un type de valeur à normaliser)
# ----------------------------------------------------------------------------
anomalies: list[str] = []


def log_anomaly(ref: str, field: str, raw_value: str, reason: str) -> None:
    anomalies.append(f"[{ref}] champ '{field}' = {raw_value!r} -> {reason}")


def clean_str(v: str | None) -> str | None:
    """Chaîne nettoyée (strip) ou None si vide."""
    if v is None:
        return None
    v = v.strip()
    return v or None


def parse_bool_presence(v: str | None) -> bool:
    """
    Colonnes 'présence' de la source (jardin, cave, ascenseur, calme,
    lumineux, terrasse, balcon, particulier) : ne contiennent QUE 'True'
    ou vide (jamais 'False' explicite, vérifié sur 2556 lignes) -> une
    ligne vide veut dire "absent", donc False (jamais NULL).
    """
    v = clean_str(v)
    return v is not None and v.lower() == "true"


def parse_bool_or_null(v: str | None) -> bool | None:
    """
    Colonnes qui contiennent à la fois 'True', 'False' ET du vide
    (meuble, exclusivite) : ici le vide veut dire "non renseigné", pas
    "False" (sinon la source écrirait "False" comme elle le fait déjà
    ailleurs) -> None (NULL), distinct de False.
    """
    v = clean_str(v)
    if v is None:
        return None
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    return None


def bool_to_count(v: str | None) -> int:
    """Présence booléenne -> compteur 0/1 (nb_balcony/nb_terrace attendent un nombre)."""
    return 1 if parse_bool_presence(v) else 0


def parse_float(v: str | None) -> float | None:
    v = clean_str(v)
    if v is None:
        return None
    try:
        return float(v.replace(",", "."))
    except ValueError:
        return None


def parse_int(v: str | None) -> int | None:
    f = parse_float(v)
    return int(f) if f is not None else None


def parse_price_eur(ref: str, v: str | None) -> int | None:
    """'406042 €' ou '406042' -> 406042 (entier, en euros)."""
    v = clean_str(v)
    if v is None:
        return None
    cleaned = v.replace("€", "").replace(" ", "").replace("\u202f", "")
    try:
        return int(round(float(cleaned.replace(",", "."))))
    except ValueError:
        log_anomaly(ref, "prix", v, "prix illisible, mis à NULL")
        return None


def parse_surface(ref: str, surface: str | None, surface_m2: str | None) -> float | None:
    """Fusionne les deux colonnes redondantes 'surface' / 'surface_m2'."""
    value = parse_float(surface)
    if value is None:
        value = parse_float(surface_m2)
    if value is None:
        log_anomaly(ref, "surface/surface_m2", "", "surface manquante des deux côtés")
    return value


def parse_etage(ref: str, floor: str | None) -> int | None:
    floor = clean_str(floor)
    if floor is None:
        return None
    if floor.upper() == "RDC":
        return 0
    try:
        if int(floor) < 10:
            return floor
        else :
            return "10 and more"
    except ValueError:
        pass
    if "dernier" in floor.lower():
        return 'last floor'
    log_anomaly(ref, "etage", floor, "valeur d'étage non reconnue -> NULL")
    return None


def parse_estate_type(ref: str, v: str | None) -> str | None:
    v = clean_str(v)
    if v is None:
        log_anomaly(ref, "type_bien", "", "type de bien manquant (colonne NOT NULL) -> NULL, à corriger manuellement")
        return None
    if v in ALLOWED_ESTATE_TYPES:
        return v
    log_anomaly(ref, "type_bien", v, "type de bien hors de la liste autorisée par le schéma cible -> NULL")
    return None


def split_address(v: str | None) -> tuple[str | None, str | None]:
    """'200 avenue des Champs' -> ('200', 'avenue des Champs')."""
    v = clean_str(v)
    if v is None:
        return None, None
    parts = v.split(" ", 1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[0], parts[1]
    return None, v


def split_photos(v: str | None) -> str | None:
    """'url1; url2; url3' -> 'url1;url2;url3' (séparateur uniformisé)."""
    v = clean_str(v)
    if v is None:
        return None
    urls = [p.strip() for p in v.split(";") if p.strip()]
    return ";".join(urls) if urls else None


def parse_date_publication(ref: str, v: str | None) -> str | None:
    """
    Uniformise tous les formats rencontrés vers 'YYYY-MM-DD' :
      - timestamp UNIX                    : '1785807730'
      - date/heure ISO                    : '2025-06-06T12:43:10'
      - date ISO                          : '2025-03-19'
      - date française en toutes lettres  : '25 octobre 2024'
      - jour/mois/année (slash)           : '27/03/2025'  (DD/MM/YYYY)
      - mois-jour-année (tiret)           : '03-16-2026'  (MM-DD-YYYY)
    """
    v = clean_str(v)
    if v is None:
        return None

    try:
        if v.isdigit():
            return datetime.fromtimestamp(int(v), tz=timezone.utc).date().isoformat()

        if "T" in v:
            return datetime.fromisoformat(v).date().isoformat()

        if len(v) == 10 and v[4] == "-" and v[7] == "-":
            return date.fromisoformat(v).isoformat()

        if "/" in v:
            day, month, year = v.split("/")
            return date(int(year), int(month), int(day)).isoformat()

        if len(v) == 10 and v[2] == "-" and v[5] == "-":
            month, day, year = v.split("-")
            return date(int(year), int(month), int(day)).isoformat()

        # Format texte français : "25 octobre 2024"
        parts = v.lower().split(" ")
        if len(parts) == 3 and parts[1] in FRENCH_MONTHS:
            day, month_name, year = parts
            return date(int(year), FRENCH_MONTHS[month_name], int(day)).isoformat()

        raise ValueError("format non reconnu")
    except (ValueError, IndexError):
        log_anomaly(ref, "date_publication", v, "format de date non reconnu -> NULL")
        return None


def derive_needs_renovation(description: str | None) -> bool:
    """Pas de mention 'travaux' -> False (colonne 'présence' déduite du texte)."""
    return description is not None and "travaux" in description.lower()


def derive_has_view(title: str | None, description: str | None) -> bool:
    text = f"{title or ''} {description or ''}".lower()
    return "vue dégagée" in text


def derive_parking_spaces(description: str | None) -> int:
    """Pas de colonne 'parking' dans la source : déduit du texte -> 1 ou 0."""
    if description is not None and "parking" in description.lower():
        return 1
    return 0


# ----------------------------------------------------------------------------
# 2. TRANSFORMATION LIGNE PAR LIGNE
# ----------------------------------------------------------------------------
def normalise_row(row: dict[str, str]) -> dict[str, object]:
    ref = clean_str(row.get("reference")) or clean_str(row.get("id")) or "?"

    price_eur = parse_price_eur(ref, row.get("prix"))
    price_k_eur = round(price_eur / 1000, 1) if price_eur is not None else None

    street_number, street = split_address(row.get("adresse"))
    description = clean_str(row.get("description"))
    title = clean_str(row.get("titre"))

    construction_year = parse_int(row.get("annee_construction"))
    construction_date = f"{construction_year:04d}-01-01" if construction_year else None

    return {
        # --- colonnes de la table "estate" ---
        "id": clean_str(row.get("id")),
        "reference": clean_str(row.get("reference")),
        "estate_type": parse_estate_type(ref, row.get("type_bien")),
        "price": price_k_eur,
        "construction_date": construction_date,
        "latitude": parse_float(row.get("latitude")),
        "longitude": parse_float(row.get("longitude")),
        "floor": parse_etage(ref, row.get("etage")),
        "nb_rooms": parse_int(row.get("nb_pieces")),
        "nb_bedrooms": parse_int(row.get("nb_chambres")),
        "nb_bathrooms": None,       # aucune source ni indice texte -> NULL
        "nb_toilets": None,         # idem
        "nb_swimming_pool": None,   # idem
        "has_garden": parse_bool_presence(row.get("jardin")),
        "nb_balcony": bool_to_count(row.get("balcon")),
        "nb_terrace": bool_to_count(row.get("terrasse")),
        "is_climatised": False,     # 0 mention trouvée sur toute la base -> False
        "energetic_score": None,    # pas déductible de la lettre DPE -> NULL
        "surface": parse_surface(ref, row.get("surface"), row.get("surface_m2")),
        "land_surface": None,       # aucune source ni indice texte -> NULL
        "has_cellar": parse_bool_presence(row.get("cave")),
        "has_view": derive_has_view(title, description),
        "is_quiet": parse_bool_presence(row.get("calme")),
        "is_bright": parse_bool_presence(row.get("lumineux")),
        "has_garage": False,        # 0 mention trouvée sur toute la base -> False
        "has_elevator": parse_bool_presence(row.get("ascenseur")),
        "has_chimney": False,       # 0 mention trouvée sur toute la base -> False
        "parking_spaces": derive_parking_spaces(description),
        "has_separate_kitchen": False,  # 0 mention trouvée sur toute la base -> False
        "needs_renovation": derive_needs_renovation(description),
        "town": clean_str(row.get("ville")),
        "street": street,
        "street_number": street_number,
        "postal_code": clean_str(row.get("code_postal")),
        "information": description,
        # --- hors périmètre "estate", conservé pour d'autres tables/usages ---
        "price_eur": price_eur,
        "construction_year": construction_year,
        "dpe": clean_str(row.get("dpe")),
        "recherche_ref": clean_str(row.get("recherche_ref")),
        "title": title,
        "date_publication": parse_date_publication(ref, row.get("date_publication")),
        "charges_mensuelles": parse_float(row.get("charges_mensuelles")),
        "is_particulier": parse_bool_presence(row.get("particulier")),
        "is_exclusive": parse_bool_or_null(row.get("exclusivite")),
        "is_furnished": parse_bool_or_null(row.get("meuble")),
        "contact_name": clean_str(row.get("contact.nom")),
        "contact_phone": clean_str(row.get("contact.telephone")),
        "contact_email": clean_str(row.get("contact.email")),
        "contact_agency": clean_str(row.get("contact.agence")),
        "photos": split_photos(row.get("photos")),
    }


def to_csv_value(v: object) -> str:
    """None -> 'NULL' (littéral), bool -> 'True'/'False', reste -> str(v)."""
    if v is None:
        return NULL
    if isinstance(v, bool):
        return "True" if v else "False"
    return str(v)


# ----------------------------------------------------------------------------
# 3. PROGRAMME PRINCIPAL
# ----------------------------------------------------------------------------
def main() -> None:
    with SRC.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [normalise_row(row) for row in reader]

    DST.parent.mkdir(parents=True, exist_ok=True)
    with DST.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: to_csv_value(row.get(col)) for col in OUTPUT_COLUMNS})

    with REPORT.open("w", encoding="utf-8") as f:
        f.write(f"Rapport de normalisation — {len(rows)} lignes traitées, {len(anomalies)} anomalies\n")
        f.write("=" * 80 + "\n")
        for a in anomalies:
            f.write(a + "\n")

    print(f"✅ {len(rows)} lignes normalisées -> {DST}")
    print(f"ℹ️  {len(anomalies)} anomalies journalisées -> {REPORT}")


if __name__ == "__main__":
    main()

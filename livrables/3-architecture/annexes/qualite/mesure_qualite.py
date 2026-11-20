"""Mesure la qualité des annonces : source brute, puis sortie normalisée.

Usage, depuis la racine du dépôt Fil-Rouge :
    python livrables/3-architecture/annexes/qualite/mesure_qualite.py

Lit `normalised/annonces/annonces.csv` (copie de la fixture du sujet) et
`normalised/annonces_normalised.csv` (sortie de `normalised/normalised.py`).
Imprime des comptes bruts ; ne modifie aucun fichier.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "normalised" / "annonces" / "annonces.csv"
OUT = ROOT / "normalised" / "annonces_normalised.csv"
REQ = ROOT / "normalised" / "annonces" / "recherches.csv"


def read(path):
    """Rend (en-têtes, lignes) d'un CSV UTF-8 ; un BOM éventuel est ignoré."""
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return (list(rows[0].keys()) if rows else []), rows


def filled(v):
    """Vrai si la cellule porte une valeur (ni vide, ni « NULL »)."""
    return v is not None and v.strip() not in ("", "NULL")


def date_kind(v):
    """Classe un format de date de publication ; rend « vide » pour une cellule vide."""
    v = (v or "").strip()
    if not v:
        return "vide"
    if re.fullmatch(r"\d{9,11}", v):
        return "horodatage Unix"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        return "AAAA-MM-JJ"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", v):
        return "AAAA-MM-JJThh:mm:ss"
    if re.fullmatch(r"\d{2}-\d{2}-\d{4}", v):
        return "JJ-MM-AAAA"
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", v):
        return "JJ/MM/AAAA"
    if re.fullmatch(r"\d{1,2} [a-zéû]+ \d{4}", v):
        return "en toutes lettres"
    return "autre"


def main():
    """Imprime les mesures ; rend 1 si un fichier manque."""
    for p in (SRC, OUT, REQ):
        if not p.exists():
            print(f"fichier absent : {p}", file=sys.stderr)
            return 1

    cols, rows = read(SRC)
    n = len(rows)
    print(f"== Source brute : {n} annonces, {len(cols)} colonnes")
    rates = {c: sum(filled(r[c]) for r in rows) / n for c in cols}
    print(f"remplissage moyen des colonnes : {100 * sum(rates.values()) / len(cols):.1f} %")
    for c, r in sorted(rates.items(), key=lambda x: x[1]):
        print(f"  {100 * r:5.1f} %  {c}")

    print("formats de date de publication :", dict(Counter(date_kind(r["date_publication"]) for r in rows)))
    euro = sum("€" in (r["prix"] or "") for r in rows)
    print(f"prix écrits avec « € » : {euro}")
    both = sum(filled(r["surface"]) and filled(r["surface_m2"]) for r in rows)
    one = sum(filled(r["surface"]) != filled(r["surface_m2"]) for r in rows)
    none = sum(not filled(r["surface"]) and not filled(r["surface_m2"]) for r in rows)
    print(f"surface : dans 1 seule des 2 colonnes {one}, dans les 2 {both}, aucune {none}")
    print(f"identifiants en double : {n - len({r['id'] for r in rows})} ; références en double : {n - len({r['reference'] for r in rows})}")
    _, reqs = read(REQ)
    known = {r.get("reference") or r.get("ref") or next(iter(r.values())) for r in reqs}
    orphan = sum(r["recherche_ref"] not in known for r in rows)
    print(f"recherches : {len(reqs)} ; annonces dont la recherche est inconnue : {orphan}")

    ocols, orows = read(OUT)
    m = len(orows)
    print(f"== Sortie normalisée : {m} annonces, {len(ocols)} colonnes")
    orates = {c: sum(filled(r[c]) for r in orows) / m for c in ocols}
    print(f"remplissage moyen (hors « NULL ») : {100 * sum(orates.values()) / len(ocols):.1f} %")
    empty = [c for c, r in orates.items() if r == 0]
    print(f"colonnes vides partout ({len(empty)}) : {', '.join(empty)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

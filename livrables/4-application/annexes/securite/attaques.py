"""Rejoue les 4 attaques de la note de sécurité (§ 3) contre l'API locale.

Se lance DANS le conteneur `api`, depuis `Fil-Rouge-API/docker/` :

    docker compose exec -T api python - < ../../Fil-Rouge/livrables/4-application/securite/attaques.py

Ce qu'il fait : envoie de vraies requêtes à http://localhost:8000 et affiche,
pour chaque essai, la requête, le code HTTP reçu et le verdict (TIENT / FAILLE).
Il n'écrit rien en base : aucune route d'écriture n'est appelée. Les essais de
connexion visent un email qui n'existe pas ; le frein qu'ils déclenchent vit en
mémoire et s'efface au redémarrage du conteneur `api`.

Cas limite : une réponse inattendue (ni le code attendu, ni une faille connue)
est affichée « FAILLE ? » avec son code, jamais rangée en silence.
"""

import os
import sys

import httpx
from sqlalchemy import text  # pyright: ignore[reportMissingImports]  (installé dans le conteneur api seulement)

sys.path.insert(0, "/api")
from src.app.conf.database import engine  # noqa: E402  # pyright: ignore[reportMissingImports]  (idem)
from src.app.utils.security import create_access_token  # noqa: E402  # pyright: ignore[reportMissingImports]  (code de l'API, lu dans le conteneur)

BASE = "http://localhost:8000"
KEY = next(v for k, v in sorted(os.environ.items()) if k.startswith("API_KEY_") and v)


def manager_user_id() -> int:
    """Rend l'id du premier compte Manager actif ; lève une erreur s'il n'y en a pas."""
    with engine.connect() as conn:
        row = conn.execute(text(
            'SELECT u.id FROM "user" u JOIN real_estate_manager m ON m.id_user = u.id '
            "WHERE u.is_activated ORDER BY u.id LIMIT 1")).first()
    if row is None:
        raise SystemExit("Aucun compte Manager actif : essais impossibles.")
    return row[0]


def verdict(name: str, request: str, response: httpx.Response, ok: bool) -> bool:
    """Affiche une ligne de résultat ; rend `ok` (True si l'attaque a échoué)."""
    print(f"{'TIENT ' if ok else 'FAILLE?'} | {name:28} | {request:60} | {response.status_code} "
          f"{response.headers.get('content-type', '-')}")
    return ok


def main() -> None:
    """Joue les essais des 4 familles d'attaque et affiche le bilan."""
    results = []
    with httpx.Client(base_url=BASE, headers={"X-API-Key": KEY}, timeout=30) as c:
        # 1. Injection SQL : dans l'email de connexion, et dans un id de chemin.
        r = c.post("/auth/login", json={"email": "' OR '1'='1' --", "password": "x' OR '1'='1"})
        results.append(verdict("SQL : email de connexion", "POST /auth/login email=' OR '1'='1' --", r, r.status_code in (401, 429)))
        bearer = {"Authorization": f"Bearer {create_access_token(manager_user_id())}"}
        r = c.get("/estates/1 OR 1=1", headers=bearer)
        results.append(verdict("SQL : id dans le chemin", "GET /estates/1 OR 1=1", r, r.status_code == 422))
        r = c.get("/estates/1;DROP TABLE estate", headers=bearer)
        results.append(verdict("SQL : requête empilée", "GET /estates/1;DROP TABLE estate", r, r.status_code in (404, 422)))

        # 2. XSS : un script dans un champ revient-il comme page HTML ?
        r = c.post("/auth/login", json={"email": "<script>alert(1)</script>", "password": "x"})
        html = "text/html" in r.headers.get("content-type", "")
        results.append(verdict("XSS : script dans un champ", "POST /auth/login email=<script>…", r, not html))

        # 3. CSRF : un navigateur n'envoie que des cookies. Sans en-tête, refus ?
        r = c.get("/estates/1", headers={"Origin": "https://site-pirate.example"}, cookies={"access_token": "x"})
        results.append(verdict("CSRF : cookie seul", "GET /estates/1 avec cookie, sans Authorization", r, r.status_code == 401))
        cors = r.headers.get("access-control-allow-origin")
        print(f"        CORS : Access-Control-Allow-Origin = {cors!r} (None : aucun site tiers autorisé)")
        r = c.post("/auth/login", json={"email": "personne@example.org", "password": "mauvais-mot-de-passe"})
        print(f"        Set-Cookie à la connexion : {r.headers.get('set-cookie')!r} (None : le jeton n'est jamais un cookie)")

        # 4. Authentification : 15 mauvais mots de passe d'affilée.
        codes = []
        for i in range(15):
            r = c.post("/auth/login", json={"email": "attaque-test@example.org", "password": f"faux-{i}"})
            codes.append(r.status_code)
        first_429 = codes.index(429) + 1 if 429 in codes else None
        print(f"        codes reçus : {codes}")
        ok = first_429 is not None and first_429 <= 6
        results.append(verdict("Force brute : 15 essais", f"15 x POST /auth/login ; 1er 429 à l'essai {first_429}", r, ok))
        print(f"        Retry-After : {r.headers.get('retry-after')!r} secondes")

    print(f"\nBilan : {sum(results)} essais tiennent sur {len(results)}")


if __name__ == "__main__":
    main()

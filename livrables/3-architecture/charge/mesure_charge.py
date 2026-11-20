"""Mesure de charge de l'API : temps de réponse sous requêtes parallèles.

Se lance DANS le conteneur `api` (il y trouve httpx, la clé d'API et le secret
JWT), depuis `Fil-Rouge-API/docker/` :

    docker compose exec -T api python - < ../../Fil-Rouge/livrables/3-architecture/charge/mesure_charge.py

Ce qu'il fait : fabrique un jeton pour un compte Manager existant (aucun mot de
passe lu ni affiché), puis envoie N requêtes par route, P à la fois, sur
http://localhost:8000. Il affiche, par route : réponses en 200, médiane,
95e centile, maximum (en millisecondes) et débit (requêtes par seconde).

Cas limites : une réponse autre que 200 est comptée à part et signalée, jamais
mêlée aux temps ; une route qui ne rend aucun 200 est marquée « ÉCHEC ».
"""

import os
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import httpx
from sqlalchemy import text

sys.path.insert(0, "/api")
from src.app.conf.database import engine  # noqa: E402  (l'engine de l'API, même base)
from src.app.utils.security import create_access_token  # noqa: E402

BASE = "http://localhost:8000"
N = 1000      # requêtes par route
PARALLEL = 10  # requêtes en même temps


def manager_user_id() -> int:
    """Rend l'id du premier compte Manager actif ; lève une erreur s'il n'y en a pas."""
    with engine.connect() as conn:
        row = conn.execute(text(
            'SELECT u.id FROM "user" u JOIN real_estate_manager m ON m.id_user = u.id '
            "WHERE u.is_activated ORDER BY u.id LIMIT 1")).first()
    if row is None:
        raise SystemExit("Aucun compte Manager actif : mesure impossible.")
    return row[0]


def api_key() -> str:
    """Rend la première clé d'API non vide ; lève une erreur si aucune n'est définie."""
    for name, value in sorted(os.environ.items()):
        if name.startswith("API_KEY_") and value:
            return value
    raise SystemExit("Aucune clé API_KEY_* dans l'environnement du conteneur.")


def measure(client: httpx.Client, path: str) -> dict:
    """Envoie N requêtes GET sur `path`, PARALLEL à la fois ; rend les temps des 200 et les autres codes."""
    def one(_: int) -> tuple[int, float]:
        start = time.perf_counter()
        status = client.get(path).status_code
        return status, (time.perf_counter() - start) * 1000

    begin = time.perf_counter()
    with ThreadPoolExecutor(max_workers=PARALLEL) as pool:
        results = list(pool.map(one, range(N)))
    elapsed = time.perf_counter() - begin
    ok = sorted(ms for status, ms in results if status == 200)
    others: dict[int, int] = {}
    for status, _ in results:
        if status != 200:
            others[status] = others.get(status, 0) + 1
    return {"ok": ok, "others": others, "elapsed": elapsed}


def main() -> None:
    """Mesure chaque route et affiche une ligne de résultat par route."""
    headers = {"X-API-Key": api_key(),
               "Authorization": f"Bearer {create_access_token(manager_user_id())}"}
    routes = ["/estates", "/estates/1", "/search-requests"]
    print(f"{N} requêtes par route, {PARALLEL} en parallèle, sur {BASE}")
    with httpx.Client(base_url=BASE, headers=headers, timeout=60) as client:
        client.get("/estates/1")  # une requête d'échauffement, non comptée
        for path in routes:
            r = measure(client, path)
            ok = r["ok"]
            if not ok:
                print(f"{path:20} ÉCHEC : aucun 200, codes {r['others']}")
                continue
            p95 = ok[max(0, int(len(ok) * 0.95) - 1)]
            print(f"{path:20} 200: {len(ok):4}  médiane {statistics.median(ok):7.1f} ms  "
                  f"p95 {p95:7.1f} ms  max {ok[-1]:7.1f} ms  débit {N / r['elapsed']:6.1f} req/s"
                  + (f"  autres codes {r['others']}" if r["others"] else ""))


if __name__ == "__main__":
    main()

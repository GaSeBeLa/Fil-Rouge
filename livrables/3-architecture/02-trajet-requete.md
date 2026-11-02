# Schéma 2 — le trajet d'une requête dans l'API

> Tiré de la présentation du 2026-10-16 (schéma 2), complété le 2026-11-02 :
> la clé d'API et le refus `401` manquaient. Vérifié dans **Fil-Rouge-API**
> (`API/src/app/`).

## À quoi il sert

Dire où une requête peut être arrêtée, et quel code de réponse le montre.

## Le schéma

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#faf1e2","primaryColor":"#faf1e2","primaryBorderColor":"#6e6151","primaryTextColor":"#50433b","lineColor":"#6e6151","textColor":"#50433b","edgeLabelBackground":"#efe2c9","clusterBkg":"#f3e8d4","clusterBorder":"#c1b295","fontFamily":"Atkinson Hyperlegible, sans-serif","fontSize":"18px"}}}%%
flowchart LR
    U["Utilisateur<br/>Swagger, script"]
    subgraph API["L'API FastAPI"]
        K["Clé d'API<br/>en-tête X-API-Key"]
        J["Jeton JWT<br/>60 min, ADR-052"]
        R["routes/<br/>revalide l'entrée"]
        S["services/<br/>règles et droits"]
        D["repositories/<br/>SQL"]
    end
    P[("PostgreSQL<br/>22 tables")]

    U --> K --> J --> R --> S --> D --> P

    K -. "clé absente ou fausse" .-> E401a["401"]
    J -. "jeton absent, expiré,<br/>ou compte désactivé" .-> E401b["401"]
    R -. "entrée invalide" .-> E422["422"]
    S -. "le rôle n'a pas le droit" .-> E403["403"]
    S -. "la ligne est à un autre" .-> E404["404"]
    P -. "tout va bien" .-> OK["200"]

    classDef couche fill:#e1e9f2,stroke:#2f5d8c,color:#50433b
    classDef refus fill:#f6e3d6,stroke:#a63d40,color:#50433b
    classDef bon fill:#e2efe4,stroke:#2d7551,color:#50433b
    class K,J,R,S,D couche
    class E401a,E401b,E422,E403,E404 refus
    class OK bon
```

## Comment le lire

- La requête va de gauche à droite. Chaque couche peut l'**arrêter**.
- 🟥 Les cases rouges sont les refus. Le **code** dit où elle s'est arrêtée.
- **401** : le même message dans tous les cas, exprès, pour ne rien
  révéler (ADR-052).
- **403** : les droits se vérifient d'abord **par rôle**, table par table
  (ADR-027). Les 5 rôles : Admin, Client, Hunter, Manager, Reader.
- **404** : le rôle a le droit, mais la ligne appartient à un autre. On
  répond comme si elle n'existait pas : un 403 dirait qu'elle existe.
- Chaque couche a un seul métier : les routes parlent HTTP, les services
  portent les règles, les repositories parlent SQL.

## Sources

- Clé d'API : `utils/api_keys.py` (`require_api_key`, en-tête `X-API-Key`).
- Jeton : `utils/current_user.py` (`get_current_user`) ; il relit le compte
  en base à chaque appel et refuse un compte non activé.
- Revalidation à la route : ADR-036.

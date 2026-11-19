# Schéma 8 — se connecter et utiliser son jeton

> Nouveau le 2026-11-02 : il manquait. Lu dans le code de
> **Fil-Rouge-API** : `routes/auth_router.py`, `services/user_service.py`,
> `utils/security.py`, `utils/current_user.py`.

## À quoi il sert

Montrer, dans l'ordre, ce qui se passe quand on se connecte, puis quand on
appelle une route avec son jeton.

## Le schéma

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#faf1e2","primaryColor":"#faf1e2","primaryBorderColor":"#6e6151","primaryTextColor":"#50433b","lineColor":"#6e6151","textColor":"#50433b","edgeLabelBackground":"#efe2c9","clusterBkg":"#f3e8d4","clusterBorder":"#c1b295","actorBkg":"#e1e9f2","actorBorder":"#2f5d8c","noteBkgColor":"#efe2c9","noteBorderColor":"#c1b295","fontFamily":"Atkinson Hyperlegible, sans-serif","fontSize":"18px"}}}%%
sequenceDiagram
    actor U as Utilisateur
    participant A as API
    participant B as PostgreSQL

    Note over U,A: 1. Se connecter
    U->>A: POST /login (X-API-Key, email, mot de passe)
    A->>B: chercher le compte par email
    B-->>A: le compte, ou rien
    A->>A: vérifier le mot de passe (Argon2)
    A->>A: compte activé ?
    alt un des trois échoue
        A-->>U: 401, toujours le même message
    else tout est bon
        A-->>U: 200, jeton JWT valable 60 min
    end

    Note over U,A: 2. Appeler une route
    U->>A: GET /… (X-API-Key, Bearer jeton)
    A->>A: lire l'id dans le jeton (HS256)
    A->>B: relire le compte
    B-->>A: le compte
    alt jeton faux, expiré, ou compte désactivé
        A-->>U: 401
    else jeton valable
        A-->>U: la suite du trajet (schéma 2)
    end
```

## Comment le lire

- Deux clés, deux rôles :
  - la **clé d'API** (`X-API-Key`) dit **quel programme** appelle ;
  - le **jeton** (JWT) dit **quelle personne** appelle.
- Le jeton ne porte **que l'id du compte** : ni e-mail, ni rôle.
- Le compte est **relu en base à chaque appel** : un compte désactivé est
  refusé tout de suite, même avec un jeton encore valable.
- Un email inconnu prend **le même temps** qu'un mauvais mot de passe : on
  ne peut pas deviner quels emails existent.
- Pas de jeton de rafraîchissement : après 60 minutes, on se reconnecte.

## Sources

- `routes/auth_router.py` : `login`, `me`.
- `services/user_service.py` : `authenticate`.
- `utils/security.py` : Argon2, `JWT_ALGORITHM = "HS256"`,
  `ACCESS_TOKEN_TTL = timedelta(minutes=60)`.
- `utils/current_user.py` : `get_current_user`.
- Décisions : ADR-028 (clé d'API), ADR-052 (jeton), ADR-016 (Argon2).

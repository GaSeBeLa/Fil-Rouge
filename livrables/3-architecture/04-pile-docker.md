# Schéma 4 — la pile Docker, et ce qu'elle coûte

> Tiré de la présentation du 2026-10-16 (schéma 4), complété le 2026-11-02
> avec les ports et l'ordre de démarrage, lus dans
> `Fil-Rouge-API/docker/docker-compose.yml`.

## À quoi il sert

Savoir quels conteneurs existent, lesquels lancer, et dans quel ordre ils
démarrent.

## Le schéma

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#faf1e2","primaryColor":"#faf1e2","primaryBorderColor":"#6e6151","primaryTextColor":"#50433b","lineColor":"#6e6151","textColor":"#50433b","edgeLabelBackground":"#efe2c9","clusterBkg":"#f3e8d4","clusterBorder":"#c1b295","fontFamily":"Atkinson Hyperlegible, sans-serif","fontSize":"18px"}}}%%
flowchart TB
    subgraph BASE["Sans profil · toujours lancés · ≈ 234 Mio"]
        DB[("db<br/>PostgreSQL · 5432")]
        API["api<br/>FastAPI · 8000"]
    end
    subgraph AIR["Profil airflow · ≈ 1,5 Gio"]
        MIN[("minio<br/>9000 · console 9001")]
        MSET["minio-setup<br/>tâche unique"]
        AINIT["airflow-init<br/>tâche unique"]
        AWEB["airflow-webserver<br/>8080"]
        ASCH["airflow-scheduler"]
    end
    subgraph ELK["Profil elk · ≈ 3,2 Gio"]
        ES[("elasticsearch")]
        ESSET["es-setup<br/>tâche unique"]
        KIB["kibana<br/>5601"]
        LS["logstash"]
    end

    DB -->|"santé OK"| API
    MIN --> MSET
    AINIT -->|"fini sans erreur"| AWEB
    AINIT -->|"fini sans erreur"| ASCH
    ES -->|"santé OK"| ESSET
    ESSET -->|"fini sans erreur"| KIB
    ESSET -->|"fini sans erreur"| LS
    ES -->|"santé OK"| LS

    classDef db fill:#e1e9f2,stroke:#2f5d8c,color:#50433b
    classDef airflow fill:#e2efe4,stroke:#2d7551,color:#50433b
    classDef elk fill:#f3e4cc,stroke:#8f5a0f,color:#50433b
    class DB,API db
    class MIN,MSET,AINIT,AWEB,ASCH airflow
    class ES,ESSET,KIB,LS elk
```

## Comment le lire

- **11 conteneurs**, rangés en **3 groupes** : on ne lance que ce dont on a
  besoin.
- Une flèche = « attend que l'autre soit prêt » (`depends_on`).
- « Tâche unique » : le conteneur prépare quelque chose, puis s'arrête.
- Le port affiché est celui ouvert sur la machine (`localhost:<port>`).

## Ce qu'elle coûte en mémoire

| Ce qu'on lance | Mémoire au repos |
|---|---|
| base + API seules | ≈ **234 Mio** |
| + profil `airflow` | ≈ **1,7 Gio** |
| + profil `elk` (tout) | ≈ **5,0 Gio** |

- Mesuré le 2026-10-15 vers 16 h 30 avec `docker stats --no-stream` :
  234,3 Mio (base), 1 552,2 Mio (airflow), 3 309,3 Mio (elk).
- Conseil : donner **6 Go** à Docker quand tout tourne.

## Sources

- `docker/docker-compose.yml` : services, `profiles`, `ports`, `depends_on`.
- Comment lancer chaque profil : [`md/equipe/tuto-lancer-la-pile.md`](../../md/equipe/tuto-lancer-la-pile.md).

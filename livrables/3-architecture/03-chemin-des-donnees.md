# Schéma 3 — le chemin des données

> Tiré de la présentation du 2026-10-16 (schéma 3). C'est la **vue
> d'ensemble**. Le détail, avec les noms exacts des fichiers MinIO et des
> tâches, est dans [`md/flux/schema-du-flux.md`](../../md/flux/schema-du-flux.md) :
> en cas d'écart, c'est lui qui fait foi.

## À quoi il sert

Suivre les données : de l'import de nuit jusqu'à la recherche, et des
requêtes de l'API jusqu'aux tableaux de bord.

## Le schéma

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#faf1e2","primaryColor":"#faf1e2","primaryBorderColor":"#6e6151","primaryTextColor":"#50433b","lineColor":"#6e6151","textColor":"#50433b","edgeLabelBackground":"#efe2c9","clusterBkg":"#f3e8d4","clusterBorder":"#c1b295","fontFamily":"Atkinson Hyperlegible, sans-serif","fontSize":"18px"}}}%%
flowchart LR
    subgraph AIR["Profil airflow"]
        GEN["Générateur<br/>airflow/tools/"]
        BR[("MinIO bronze<br/>CSV brut")]
        SI[("MinIO silver<br/>annonces valides")]
        QU[("MinIO quarantine<br/>rejets + raison")]
        GO[("MinIO gold<br/>bilan olap")]
    end
    subgraph PG["PostgreSQL"]
        EST[("estate")]
        OLTP[("sale, payment…")]
        OLAP[("schéma olap<br/>fait_ventes + 5 dim")]
    end
    subgraph ELK["Profil elk"]
        IDX[("Elasticsearch<br/>index estates")]
        LS["Logstash<br/>pipeline api"]
        LOGS[("Elasticsearch<br/>logs-api-default")]
        KB["Kibana<br/>port 5601"]
    end
    USR["Utilisateur<br/>avec un jeton"]
    API["api<br/>FastAPI, port 8000"]

    GEN -->|"2 h · generate"| BR
    BR -->|"clean_validate"| SI
    BR -->|"clean_validate : rejets"| QU
    SI -->|"load : un bien par reference"| EST
    OLTP -->|"3 h · refresh"| OLAP
    OLAP -->|"report"| GO
    EST -->|"4 h · index puis prune<br/>sans contact ni adresse"| IDX
    USR -->|"GET /estates/search"| API
    API -->|"compte api_search,<br/>lecture seule"| IDX
    API -->|"une ligne JSON par requête"| LS
    LS -->|"compte logstash_internal"| LOGS
    LOGS --> KB
    IDX --> KB

    classDef airflow fill:#e2efe4,stroke:#2d7551,color:#50433b
    classDef db fill:#e1e9f2,stroke:#2f5d8c,color:#50433b
    classDef elk fill:#f3e4cc,stroke:#8f5a0f,color:#50433b
    class GEN,BR,SI,QU,GO airflow
    class EST,OLTP,OLAP db
    class IDX,LS,LOGS,KB elk
```

## Comment le lire

- 🟩 Vert : le profil `airflow`. 🟦 Bleu : la base. 🟧 Ocre : le profil `elk`.
- Trois traitements de nuit, chacun à son heure :
  - **2 h** · `annonces_import` : le CSV brut → bronze → silver ou
    quarantine → la table `estate` ;
  - **3 h** · `olap_refresh` : les tables du métier → le schéma `olap` ;
  - **4 h** · `estates_index` : `estate` → l'index de recherche.
- Rien ne se perd en silence : un rejet part en **quarantine**, avec sa raison.
- Les logs ne gardent **ni e-mail ni mot de passe**.

## Sources

- La présentation du 2026-10-16 (`md/equipe/2026-10-16-presentation.md`).
- Les ADR 059 à 064 (`md/adr/`).

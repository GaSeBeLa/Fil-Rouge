# Schéma 1 — d'où on part, où on arrive

> Tiré de la présentation du 2026-10-16 (schéma 1). Comptes de tables
> revérifiés le 2026-11-02 dans le dépôt **Fil-Rouge-API** (`docker/`).

## À quoi il sert

Montrer en un coup d'œil comment la base a grandi : des fixtures reçues
avec le sujet jusqu'au schéma v3 monté aujourd'hui.

## Le schéma

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#faf1e2","primaryColor":"#faf1e2","primaryBorderColor":"#6e6151","primaryTextColor":"#50433b","lineColor":"#6e6151","textColor":"#50433b","edgeLabelBackground":"#efe2c9","clusterBkg":"#f3e8d4","clusterBorder":"#c1b295","fontFamily":"Atkinson Hyperlegible, sans-serif","fontSize":"18px"}}}%%
flowchart LR
    F["Fixtures du sujet<br/>3 tables<br/>secteurs, utilisateurs, mandats"]
    V1["Première cible<br/>12 tables<br/>montants en milliers d'euros<br/>docker/init/"]
    V2["Schéma v2 · 21/09<br/>18 tables<br/>docker/init-v2/ (figé)"]
    V3["Schéma v3 · 07/10 → 15/10<br/>22 tables<br/>montants en euros<br/>docker/init-v3/ + migrations"]

    F -->|"audit : 37 montants sur 47<br/>débordaient en milliers d'euros"| V1
    V1 -->|"abandonnée, plus montée"| V2
    V2 -->|"docker/migrations/v2-vers-v3/<br/>vérifié par le banc v2/v3"| V3

    classDef vieux fill:#efe2c9,stroke:#6e6151,color:#50433b
    classDef actuel fill:#e1e9f2,stroke:#2f5d8c,stroke-width:3px,color:#50433b
    class F,V1,V2 vieux
    class V3 actuel
```

## Comment le lire

- De gauche à droite : le temps.
- 🔵 La boîte bleue est la **seule version montée** aujourd'hui : le schéma v3.
- Le schéma v2 est **figé** : il ne sert plus qu'au banc de migration.
- Le banc `API/tests/integration/test_banc_v2_v3.py` migre une base v2 et la
  compare au schéma v3, à chaque lancement des tests.

## Sources

- Comptes de `CREATE TABLE` : `docker/init/` (12), `docker/init-v2/` (18),
  `docker/init-v3/01_create_fil_rouge_immobilier.sql` (22).
- « 37 montants sur 47 » : repris de la présentation, pas recompté ici.
- Montants en euros : ADR-032.

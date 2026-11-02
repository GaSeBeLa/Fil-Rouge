# Schéma 7 — les données : vente et rémunération

> Nouveau le 2026-11-02 : il manquait. Troisième des trois schémas du
> modèle (5, 6, 7). Lu dans
> `Fil-Rouge-API/docker/init-v3/01_create_fil_rouge_immobilier.sql`, qui fait
> foi.

## À quoi il sert

Montrer ce qui se passe quand un bien est acheté : la **vente**, puis le
**paiement** du chasseur, calculé avec des paramètres datés.

## Le schéma

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#faf1e2","primaryColor":"#faf1e2","primaryBorderColor":"#6e6151","primaryTextColor":"#50433b","lineColor":"#6e6151","textColor":"#50433b","edgeLabelBackground":"#efe2c9","clusterBkg":"#f3e8d4","clusterBorder":"#c1b295","fontFamily":"Atkinson Hyperlegible, sans-serif","fontSize":"18px"}}}%%
erDiagram
    sale {
        int id PK
        date signature_date
        int purchase_amount "euros, entier"
        numeric fees_amount "euros, au centime"
        varchar sale_origin "hunter ou client_alone"
        int id_mandate FK "unique"
        int id_estate FK
        int id_parameters_fees FK
    }
    payment {
        int id PK
        numeric amount "euros, au centime"
        varchar status
        int id_sale FK "unique"
        int id_hunter FK
        int id_commission_scale FK "facultatif"
        int id_hunter_rate_parameters FK "facultatif"
    }

    mandate ||--o| sale : "se conclut par"
    estate ||--o{ sale : "est vendu"
    parameters_fees ||--o{ sale : "fixe les honoraires"
    sale ||--o| payment : "rémunère"
    hunter ||--o{ payment : "reçoit"
    commission_scale |o--o{ payment : "barème utilisé"
    hunter_rate_parameters |o--o{ payment : "réglages utilisés"
    hunter |o--o{ commission_scale : "barème propre"
    hunter ||--o{ hunter_performance : "a un historique"
    payment |o--o{ hunter_performance : "déclenche"
    mandate |o--o{ hunter_performance : "déclenche à l'échéance"
```

## Comment le lire

- Une **vente** par mandat au plus (`id_mandate` unique).
- Un **paiement** par vente au plus (`id_sale` unique).
- Le paiement garde **les paramètres utilisés** pour le calculer : on peut
  toujours refaire le calcul, même si les paramètres changent ensuite.
- `hunter_performance` garde l'historique du taux de réussite du chasseur.
  Une ligne naît d'un paiement, d'un mandat échu, ou au départ
  (`trigger_type` : `payment`, `mandate_expired`, `initial`).
- Montants : prix en **euros entiers**, honoraires et paiements **au
  centime** (règle 4 du `CLAUDE.md`).
- Le calcul lui-même : `services/remuneration.py`, branché par
  `POST /sales/{id}/payment`.

## Sources

- `01_create_fil_rouge_immobilier.sql` : `parameters_fees` (l. 962), `sale`
  (l. 975), `commission_scale` (l. 1014), `hunter_rate_parameters`
  (l. 1065), `payment` (l. 1103), `hunter_performance` (l. 1246).
- La traçabilité du calcul : [`md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md`](../../md/regles-metier/schema-tracabilite-remuneration-chasseur_v4.md).

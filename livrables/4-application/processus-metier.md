# Processus métier — de l'existant au système cible

> Compétence : « Schématiser les processus métier en tenant compte des contraintes, de l'existant et des vulnérabilités » — schémas de processus, du parcours utilisateur au processus système (`documents utiles/TRACABILITE-COMPETENCES.md:49` et `:62`, StarterPack). Phases 2 à 4.
> Version 2 du 2026-11-19, rédigé avec l'assistant IA du projet après la relecture de Gabriel (v1 : l'existant n'était pas dessiné, les failles et les contraintes n'étaient pas sur le schéma, des chemins manquaient).
> Sources : le `Readme.md` du sujet (les parcours), l'audit de la phase 1 (`livrables/1-audit/`, failles `R01` à `R16`), les user stories (`user-stories/01` à `07`), le schéma v3 (valeurs des statuts, `docker/init-v3/01_create_fil_rouge_immobilier.sql`) et les routes réelles de l'API (`GET /openapi.json`, `Fil-Rouge-API`, 2026-11-19).
> Images : [`images/processus-existant.png`](images/processus-existant.png), [`images/processus-particulier.png`](images/processus-particulier.png), [`images/processus-chasseur.png`](images/processus-chasseur.png).

**Comment lire.**
- Un couloir par acteur. Un ovale marque le **début** ou la **fin** ; un losange, une **décision** (le couloir dit qui décide).
- Sur chaque étape, la ligne **« Contrôle »** dit la contrainte qui s'y applique, et la ligne **« Règle »** la faille de l'audit qu'elle corrige.
- Toute requête passe d'abord par les contrôles de l'API : clé et jeton (`401`), entrée valide (`422`), rôle autorisé (`403`), « le sien » (`404`). Ils ne sont pas répétés sur chaque étape.

---

## 1. L'existant, au 25/07/2026

```mermaid
flowchart TB
    D0(["Début : un prospect cherche un bien"])
    subgraph E_PROS["Prospect"]
        E1["Remplit le formulaire du site web<br/>(hors périmètre)"]
    end
    subgraph E_SI["SI hérité"]
        E2["Backend : code perdu, développeur absent<br/>Faille R09"]
        E3["Table utilisateurs : clients et chasseurs mêlés,<br/>données en clair<br/>Failles R02, R05, R06, R16"]
        E4["Table mandats : critères en texte libre,<br/>ni date de signature ni date de fin,<br/>statut « actif » jamais mis à jour<br/>Failles R01, R04, R07"]
        E5["Taux de commission fixe par chasseur<br/>Faille R08"]
    end
    subgraph E_PAP["Hors numérique"]
        E6["Mandat signé rangé dans l'armoire,<br/>sans lien avec la base<br/>Faille R10"]
        E7["Le notaire encaisse les honoraires :<br/>aucune trace dans le SI<br/>Faille R03"]
    end
    F0(["Fin : la vente existe, le SI ne la connaît pas"])

    D0 --> E1 --> E2 --> E3 --> E4 --> E6 --> E7 --> F0
    E4 -.-> E5

    classDef faille fill:#f6dcd5,stroke:#b3261e,color:#50433b
    classDef hors fill:#efe6d6,stroke:#97a0af,color:#50433b
    classDef bord fill:#faf1e2,stroke:#6e6151,color:#50433b
    class E2,E3,E4,E5,E6,E7 faille
    class E1 hors
    class D0,F0 bord
```

Ce que montre l'existant : rien ne relie la demande, le mandat signé, la vente et les honoraires. Chaque flèche passe par une faille ; la cible les ferme une à une.

---

## 2. Le parcours cible du particulier

```mermaid
flowchart TB
    D1(["Début : le particulier a un projet d'achat"])
    subgraph PART["Particulier"]
        P1["1 · Dépose sa demande, sans compte<br/>POST /search-requests/submit<br/>Contrôle : statut « confirmed », ni chasseur ni manager<br/>Règle R07 : critères typés"]
        P4["4 · Active son compte avec le code<br/>POST /auth/activate · POST /auth/login<br/>Contrôle : code 7 jours, mot de passe 12 caractères,<br/>5 échecs → 429<br/>Règle R16"]
        P7{"7 · Le particulier :<br/>le bien l'intéresse ?"}
        P8["8 · Visite le bien lui-même<br/>POST /visits (visitor_type client)"]
        P9["9 · Fait une offre d'achat<br/>POST /estate-proposed/{id}/offer<br/>Contrôle : réservée au client"]
        P7N["Écarte le bien, avec une raison<br/>PUT /estate-proposed/{id} (declined)<br/>Contrôle : il ne sera plus proposé"]
    end
    subgraph MAN["Manager"]
        M2["2 · Prend la demande « à prendre »,<br/>affecte un chasseur<br/>PUT /search-requests/{id}<br/>Contrôle : son équipe et les demandes à prendre"]
        M3["3 · Donne le code d'activation<br/>POST /users/{id}/activation-code"]
    end
    subgraph CHA["Chasseur"]
        C5["5 · Rendez-vous : critères, mandat signé<br/>POST /criteria · POST /mandates<br/>Contrôle : fin = signature + 6 mois ;<br/>un seul mandat exclusif à la fois<br/>Règles R01, R04 ; R10 en partie"]
        C6["6 · Propose un bien<br/>POST /estate-proposed<br/>Contrôle : avec son propre mandat"]
        C10{"10 · Le vendeur<br/>accepte l'offre ?"}
    end
    subgraph SYS["Système (API et base)"]
        S11["11 · Acte signé : vente et honoraires<br/>POST /sales<br/>Contrôle : une vente par mandat et par bien ;<br/>honoraires au centime<br/>Règle R03"]
    end
    F1(["Fin : bien acheté, honoraires tracés"])

    D1 --> P1 --> M2 --> M3 --> P4 --> C5 --> C6 --> P7
    P7 -->|"non"| P7N --> C6
    P7 -->|"oui"| P8 --> P9 --> C10
    C10 -->|"non : nouvelle offre"| P9
    C10 -->|"oui"| S11 --> F1

    classDef part fill:#e1e9f2,stroke:#2f5d8c,color:#50433b
    classDef man fill:#f3e4cc,stroke:#8f5a0f,color:#50433b
    classDef cha fill:#e2efe4,stroke:#2d7551,color:#50433b
    classDef sys fill:#f3e8d4,stroke:#6e6151,color:#50433b
    classDef bord fill:#faf1e2,stroke:#6e6151,color:#50433b
    class P1,P4,P7,P7N,P8,P9 part
    class M2,M3 man
    class C5,C6,C10 cha
    class S11 sys
    class D1,F1 bord
```

---

## 3. Le parcours cible du chasseur

```mermaid
flowchart TB
    D2(["Début : une demande est affectée"])
    subgraph MAN2["Manager"]
        A1["1 · Affecte la demande<br/>PUT /search-requests/{id}"]
    end
    subgraph CHA2["Chasseur"]
        A2{"2 · Le chasseur :<br/>accepte la demande ?"}
        A3["3 · Rendez-vous : critères versionnés, mandat<br/>POST /criteria · POST /mandates<br/>Contrôle : fiches séparées, une fiche par compte<br/>Règles R02, R05, R06"]
        A4["4 · Demande une sélection de biens<br/>POST /search-requests/{id}/suggestions<br/>Contrôle : 10 biens au plus, un bien écarté exclu<br/>Règle R07"]
        A5["5 · Garde des biens, donne son avis,<br/>joint photo, audio ou vidéo<br/>POST /estate-search-requests · POST /review-media"]
        A6["6 · Propose au client, puis visite<br/>POST /estate-proposed · POST /visits (hunter)"]
        A7{"7 · Le mandat est-il<br/>arrivé à échéance ?"}
        A8["Renouvelle le mandat<br/>POST /mandates (id_mandate_parent)<br/>Contrôle : la note baisse au calcul suivant"]
    end
    subgraph SYS2["Système (API et base)"]
        B1["8 · Vente enregistrée, avec son origine<br/>POST /sales (hunter ou client_alone)"]
        B2{"9 · Le système :<br/>le chasseur a-t-il droit<br/>à une rémunération ?"}
        B3["10 · Paiement annoncé, montant figé<br/>POST /sales/{id}/payment (Admin)<br/>Contrôle : une seule fois, sinon 409<br/>Règle R08 : barème par tranches"]
        B4["11 · Programmé, puis payé ;<br/>note de performance recalculée<br/>PUT /payments/{id}<br/>Règle R03"]
        B5["Paiement refusé, montant 0<br/>(non exclusif, le client a trouvé seul)"]
    end
    F2(["Fin : le chasseur est payé, ou le refus est tracé"])

    D2 --> A1 --> A2
    A2 -->|"non : redevient à prendre"| A1
    A2 -->|"oui"| A3 --> A4 --> A5 --> A6 --> A7
    A7 -->|"oui, sans vente"| A8 --> A4
    A7 -->|"non, une offre aboutit"| B1 --> B2
    B2 -->|"oui"| B3 --> B4 --> F2
    B2 -->|"non"| B5 --> F2

    classDef man fill:#f3e4cc,stroke:#8f5a0f,color:#50433b
    classDef cha fill:#e2efe4,stroke:#2d7551,color:#50433b
    classDef sys fill:#f3e8d4,stroke:#6e6151,color:#50433b
    classDef bord fill:#faf1e2,stroke:#6e6151,color:#50433b
    class A1 man
    class A2,A3,A4,A5,A6,A7,A8 cha
    class B1,B2,B3,B4,B5 sys
    class D2,F2 bord
```

---

## 4. De l'existant à la cible : chaque faille, et l'étape qui la ferme

| Faille de l'audit | Dans l'existant | Étape cible qui la ferme |
|---|---|---|
| R01 statut « actif » faux | jamais mis à jour | particulier 5, chasseur 7 : la fin est calculée et contrôlée ; le renouvellement crée un nouveau mandat lié à l'ancien |
| R02, R05, R06 rôles mêlés | une seule table | chasseur 3 : une fiche par rôle, un compte n'en a qu'une |
| R03 honoraires sans trace | chez le notaire seulement | particulier 11, chasseur 8 à 11 : vente, honoraires, paiement |
| R04 pas de date de fin | absente | particulier 5 : fin = signature + 6 mois |
| R07 critères en texte libre | « T3 Ecusson, budget… » | particulier 1, chasseur 3-4 : critères typés et versionnés, lus par le moteur |
| R08 taux fixe | un taux par chasseur | chasseur 10 : barème par tranches, ancienneté, performance |
| R09 code perdu | backend sans source | toutes : une API sur GitHub, couverte par 1 120 tests |
| R10 armoire papier | aucun lien | **en partie**, particulier 5 : le mandat est en base, avec sa date et son mode de signature (`paper` ou `electronic`) ; le document papier reste dans l'armoire, sa numérisation est prévue plus tard (ADR-065) |
| R16 données en clair | sans droits | particulier 4 : comptes et droits par rôle ; « le sien » sur chaque lecture |

---

## 5. Limites connues

- **La sélection n'est pas quotidienne** : le chasseur la demande (étape 4) ; aucune tâche planifiée ne la lance chaque jour (backlog, Should).
- **L'échéance du mandat n'est pas détectée seule** : le renouvellement se fait à la main, et la note baisse au calcul suivant (backlog, Should).
- **Hors périmètre** : les notifications (le code d'activation remplace l'email), la facture (Product Owner, 07/10), le notaire (sa date et son prix sont des entrées du calcul), l'IA générative (user stories 08 et 09, conçues dans `schema-programme-ia.md` et `conception-matching-features.md`).

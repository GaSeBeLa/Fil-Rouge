# 📋 Backlog priorisé (MoSCoW)

> **Backlog priorisé** (phase 2, pilotage). Exigé par `GRILLE-EVALUATION.md` l. 72 : « backlog priorisé, MoSCoW ou équivalent ».
> Rédigé le 2026-11-19 par le Glaude ; priorités retenues par l'équipe (Sébastien, 2026-11-19), le Product Owner n'ayant pas pu être joint.
> Une ligne par scénario des user stories (`user-stories/00` à `10`). L'état vient de la matrice des tests (`livrables/4-application/tests-fonctionnels.md`, dépôt `Fil-Rouge-API` au commit `8ed2591`).

---

## 1. Les quatre priorités

| Priorité | Ce qu'elle veut dire ici | Règle de tri |
|---|---|---|
| **Must** — doit | sans elle, le métier ne marche pas, ou le sujet l'exige nommément | règle du mandat et de la rémunération ; parcours actuel du particulier et du chasseur |
| **Should** — devrait | utile et attendu, mais le parcours tient sans | automatismes, tâches planifiées |
| **Could** — pourrait | confort, à faire s'il reste du temps | aide au chasseur, fonctions nouvelles |
| **Won't** — pas cette fois | hors périmètre, décidé avec le Product Owner ou par le sujet | facture, emails, notaire, IA générative, front |

État : ✅ codé et testé · ✅📝 codé, la règle diffère du scénario par un choix écrit · 🟡 en partie · ➖ pas fait, hors périmètre.

---

## 2. Le backlog

### 00 — Règles du mandat et de la rémunération

| # | Élément | Priorité | État |
|---|---|---|---|
| 00:15 | Exclusif : le chasseur est rémunéré même si le client trouve seul | Must | ✅ |
| 00:23 | Non exclusif : pas de rémunération automatique | Must | ✅ |
| 00:30 | Non exclusif : un autre chasseur peut agir | Must | ✅ |
| 00:37 | Mandat de 6 mois, renouvelable | Must | ✅ |
| 00:43 | Honoraires collectés par le notaire | Must (calcul) · Won't (collecte) | ✅ calcul · ➖ collecte |

### 01 — Le particulier : demande et compte

| # | Élément | Priorité | État |
|---|---|---|---|
| 01:11 | Demande déposée par le formulaire, puis confiée | Must | ✅ (confiée par un manager) |
| 01:18 | Notification du chasseur affecté | Won't | ➖ pas d'email ; le code d'activation la remplace |
| 01:25 | Le particulier finalise son compte | Must | ✅ |
| 01:32 | Premier point et signature du mandat | Must | ✅ |

### 02 — Le particulier : propositions et visites

| # | Élément | Priorité | État |
|---|---|---|---|
| 02:14 | Reçoit des propositions, choisit quoi visiter | Must | ✅ |
| 02:20 | Reçoit l'avis du chasseur après visite | Must | ✅ |
| 02:26 | Aucun bien ne convient : les propositions reprennent | Must | ✅📝 |
| 02:32 | Un bien convient : visiter ou faire une offre | Must | ✅ |

### 03 — Le particulier : offre et signature

| # | Élément | Priorité | État |
|---|---|---|---|
| 03:14 | Fait une offre d'achat | Must | ✅ |
| 03:19 | Offre non acceptée | Must | ✅ |
| 03:25 | Offre acceptée, signature organisée | Must | ✅ (notaire ➖) |
| 03:31 | Acte signé, honoraires payés | Must | ✅ (collecte ➖) |
| 03:38 | Facture et retour d'expérience | Won't | ➖ facture exclue (Product Owner, 07/10), pas d'email |

### 04 — Le chasseur : prise en charge de la demande

| # | Élément | Priorité | État |
|---|---|---|---|
| 04:11 | Reçoit une demande (notification) | Won't | ➖ pas d'email |
| 04:17 | Refuse la demande, qui redevient « à prendre » | Must | ✅ |
| 04:24 | Accepte et consulte une recherche initiale | Must | ✅ |
| 04:30 | Prend contact, fixe un rendez-vous | Could | ➖ agenda externe, écarté par écrit |
| 04:36 | Affine les critères, fait signer le mandat | Must | ✅ |

### 05 — Le chasseur : sélection quotidienne

| # | Élément | Priorité | État |
|---|---|---|---|
| 05:14 | Reçoit une sélection **chaque jour** | Should | 🟡 le moteur répond à la demande ; pas de tâche planifiée |
| 05:20 | Transmet une sélection au client | Must | ✅ |
| 05:26 | Alerté quand le client a commenté | Won't | ➖ notification |
| 05:32 | Engage les discussions ou organise une visite | Must | ✅📝 |
| 05:38 | Requalifie la recherche si rien ne convient | Must | ✅ |

### 06 — Le chasseur : avis et offre d'achat

| # | Élément | Priorité | État |
|---|---|---|---|
| 06:11 | Note d'avis, avec audio et vidéo | Must | ✅ (adresse du média ; l'envoi dans MinIO n'est pas codé) |
| 06:18 | Offre pré-remplie selon l'avis | Could | ➖ reportée en v2, écartée par écrit |
| 06:25 | Le client ne veut pas acquérir | Must | ✅📝 |
| 06:31 | Transmet l'offre, statut « en attente » | Must | ✅ |
| 06:37 | Offre refusée par le vendeur, nouvelle offre possible | Must | ✅ |
| 06:44 | Offre acceptée par le vendeur | Must | ✅ (notaire ➖) |

### 07 — Le chasseur : rémunération et performance

| # | Élément | Priorité | État |
|---|---|---|---|
| 07:11 | Prévenu du paiement proche | Won't | ➖ notification |
| 07:18 | Envoie sa facture | Won't | ➖ facture exclue |
| 07:24 | Paiement programmé | Must | ✅ |
| 07:30 | Marqué payé, indicateurs recalculés | Must | ✅ |
| 07:37 | Mandat échu : renouveler, score à la baisse | Should | 🟡 baisse au calcul suivant ; pas de tâche planifiée |

### 08 et 09 — Le futur, avec l'IA

| # | Élément | Priorité | État |
|---|---|---|---|
| 08, 09 | **Concevoir** la base et le programme d'IA (schéma, features du matching) | Must (livrable de phase 4) | ✅ `schema-programme-ia`, `conception-matching-features` |
| 09:35 | Sélection ordonnée par pertinence, sans IA | Should | ✅ moteur de suggestion à règles (v1) |
| 09:43 | Écarter un bien refusé des sélections suivantes | Should | ✅ le bien écarté ; ➖ les biens « ressemblants » |
| 08, 09 | Les 11 autres scénarios : textes, faisabilité, offres rédigés par une IA générative | Won't | ➖ pas d'entraînement ni d'IA générative (sujet, phase 4) |

### 10 — Le calcul de la rémunération (26 scénarios)

| # | Élément | Priorité | État |
|---|---|---|---|
| 10 | Les 26 scénarios du calcul (droit, assiette, critères, barème, plafond, arrondi…) | Must | ✅ 23 · ✅📝 3 (ADR-048, ADR-035) |

---

## 3. Le bilan

Comptes faits sur les lignes du § 2 (une ligne = un élément ; la ligne 10 compte pour 1, la ligne 00:43 pour Must).

| Priorité | Lignes | ✅ ou ✅📝 | 🟡 | ➖ |
|---|---|---|---|---|
| **Must** | 31 | 31 | 0 | 0 |
| **Should** | 4 | 2 | 2 | 0 |
| **Could** | 2 | 0 | 0 | 2 |
| **Won't** | 7 | — | — | 7 |
| **Total** | **44** | | | |

- ✅ **Tous les Must sont codés et testés.**
- 🟡 Les 2 Should en partie (05:14, 07:37) demandent une tâche planifiée (Airflow) : écrites, codées s'il reste du temps.
- ➖ Les 2 Could sont écartés par écrit : agenda externe (04:30), offre pré-remplie en v2 (06:18).

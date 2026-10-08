# Proposition : regrouper la liste des ADR du chantier 4 — 2026-10-08

- 💡 **Statut : proposition.** Rien n'est tranché, rien n'est rédigé.
- 📍 Point de départ : `md/adr/2026-10-07-liste-adr-chantier-4.md` (28 lignes, A à AC).
- ✅ Accord de principe de Sébastien sur Discord le 2026-10-08 : « regroupe si tu penses que c'est ok ».
- ⚠️ Les regroupements ci-dessous sont **mon jugement**, argumenté. À relire par le groupe.

## 1. En un coup d'œil

| Avant | Après |
|---|---|
| 28 lignes (A à AC) | **23 sujets** |
| | dont **B** s'écrit en finissant ADR-024 (pas de nouveau numéro) |
| | donc **22 numéros neufs : ADR-028 à ADR-049** |

- ✅ Prochain numéro libre : **028** (`2026-10-07-liste-adr-chantier-4.md:68`).
- 🟡 Les numéros 028 à 049 sont **ma proposition d'ordre**, pas un fait.

## 2. Les 5 regroupements, et pourquoi

| # | Regroupement | Pourquoi |
|---|---|---|
| 1 | **I + Q** → un seul ADR | I relie la vente à sa grille d'honoraires et remplace ADR-019. Mais ADR-019 s'appuie sur la contrainte `EXCLUDE USING gist` (périodes qui ne se chevauchent pas). Q (Q-SCH-17) remplace justement cette contrainte par `UNIQUE (effective_from)` (`questions-a-trancher.md:172`). Écrire I sans Q laisserait ADR-019 remplacé à moitié. |
| 2 | **K** → dans **D** | K dit « les paramètres proposés sont validés par Jeff ». C'est une **validation**, pas une décision de conception. D (paramètres en table datée) est le bon endroit pour l'écrire. |
| 3 | **AC** → dans **U** | La liste le propose elle-même : « peut rejoindre l'ADR U » (`2026-10-07-liste-adr-chantier-4.md`, ligne AC). Les deux parlent de données reprises incomplètes. |
| 4 | **AA + AB** → on **réécrit ADR-027** | AA (droits par rôle) est dit « pas d'ADR propre : la matrice ADR-027 se met à jour » (`questions-a-trancher.md:421`). AB (rôle lecture seule) est une affaire de droits aussi. ADR-027 n'est que « proposé » : on peut le réécrire sans casser la règle « ne jamais effacer un ADR accepté ». |
| 5 | **Eircode sans espace** → dans **N** | N remplace ADR-009 sur la localisation. L'Eircode (Q-SCH-12) amende ADR-021 (`criteria`). Même sujet : où et comment on écrit une adresse. |

- ⚠️ **Point faible du regroupement 5** : ADR-022 (table `client`) écrit aussi l'Eircode avec un espace. N parle de `criteria`, pas de `client`. 🟡 À trancher : une phrase dans R (adresse client) pour ADR-022, ou un petit ADR à part.

## 3. Les 23 sujets, dans l'ordre que je propose

### Groupe 1 — ils remplacent d'anciens ADR (à écrire en premier)

Raison : le modèle du prof impose de marquer « remplacé par ADR-XXX » (`documents utiles/JOURNAL-DE-DECISIONS.md:72`). Tant que le remplaçant n'existe pas, l'ancien reste sans statut propre.

| N° proposé | Lettres | Sujet | Remplace ou amende | Sources |
|---|---|---|---|---|
| **028** | Y | Authentification : outils côté back, mot de passe gardé en Argon2, une clé par programme | **complète** ADR-016 et ADR-026 (remis en vigueur, voir ci-dessous) | Q-JEF-14, Q-JEF-22 ; `questions-a-trancher.md:419` |
| **029** | Z | Lien chasseur → manager, raison réécrite | ADR-025 | Q-ACC-20 ; `:420` |
| **030** | I + Q | Vente reliée à sa grille d'honoraires, grilles « en vigueur à partir du » | ADR-019 | Q-REM-13, Q-SCH-17 ; `:404`, `:412` |
| **031** | N (+ Eircode) | Localisation sur `criteria`, colonne quartier, Eircode sans espace | ADR-009 ; amende ADR-021 | Q-SCH-02, Q-MIG-08, Q-SCH-12 ; `:409` |
| **032** | A | Types monétaires : prix en `INTEGER`, euro | ADR-012 | Q-REM-01 ; `:396` ; `2026-10-07-liste-adr-chantier-4.md:45-49` |
| **024** | B | Vente perdue : statut `'lost'` sur le mandat | **finit ADR-024**, pas de numéro neuf | Q-REM-02, Q-REM-14 ; `:397` |

- ✏️ **Corrigé le 2026-10-08, après la réponse de Laurence sur Discord** : ADR-016 et ADR-026 **sont remis en vigueur**, donc Y **ne les remplace pas**.
  - Les fichiers vont dans ce sens : l'authentification est rouverte par Jeff le 2026-10-07 (`questions-a-trancher.md:87`, `:257`) ; mot de passe gardé en Argon2 = contenu d'ADR-016 ; 12 caractères gardés (Q-ACC-17) = contenu d'ADR-026 ; le groupe répond « dé-annuler » (`:260`).
  - 🟡 La décision du groupe est dite par Laurence sur Discord. Je ne l'ai pas vue écrite ailleurs ; « il me semble » (`:260`) reste la seule trace dans les fichiers.
  - ➡️ ADR-016 et ADR-026 repassent en **« accepté »**, avec une note : « annulé le 22/09, remis en vigueur le 08/10 (Jeff, 07/10) ». Rien n'est effacé (`JOURNAL-DE-DECISIONS.md:72`).
  - ➡️ Y (ADR-028) traite seulement le **nouveau** : outils d'authentification côté back, clé par programme. Il **complète** 016 et 026.

### Groupe 2 — déjà décidés, à mettre par écrit

| N° proposé | Lettres | Sujet | Sources |
|---|---|---|---|
| **033** | C | Traçabilité du calcul : figer la note et les entrées | Q-REM-03, 04, 11 ; Jeff Q-JEF-20 |
| **034** | D (+ K) | Paramètres de rémunération dans une table datée, validés par Jeff | Q-REM-05, Q-REM-19 ; K : Q-PAR-01 à 04, 06 à 08, 10, 11, 13 ; Jeff Q-JEF-01 (`questions-a-trancher.md:399`, `:406`) |
| **035** | E | Note recalculée à chaque vente | Q-REM-06 ; Jeff Q-JEF-17 |
| **036** | G | Validation de l'entrée dans le routeur commun | Q-INF-06 |
| **037** | H | X01 : ancienneté et performance majorent le taux | Q-REM-18 |
| **038** | J | Étapes du paiement, sans facture | Q-REM-17, Q-ACC-11 ; Jeff |
| **039** | L (+ D3) | Règles du mandat : 6 mois, exclusivité, renouvellement, annulation ; acte signé après la fin du mandat | Q-MAN-01 à 04, 07 ; `09-decisions-a-prendre.md:178` |
| **040** | M | Règles sur plusieurs tables : dans l'API, testées | Q-MAN-06 |
| **041** | O | Statuts de la demande et de l'offre | Q-SCH-03, 04 |
| **042** | P | Journal des notes du chasseur | Q-SCH-06 |
| **043** | R | Adresse client : tout ou rien, « non renseigné » | Q-SCH-01, Q-SCH-18 |
| **044** | S | Signature du mandat : le client seul | Q-MAN-05, Q-MAN-09 |
| **045** | T (+ acte notarié) | Limites assumées du MVP | Q-SCH-07, 08, 14, Q-MAN-08, Q-ACC-14 |
| **046** | U (+ AC) | Données reprises incomplètes ; reprise des anciens mandats | Q-MIG-05, 06, 07, 09 ; Q-MIG-03, 10, 12, 13 |
| **047** | W | Biens : import, et saisie à la main | Q-ACC-09 ; Jeff Q-JEF-24 |

- 💡 **L'ordre dans ce groupe est libre.** Je l'ai suivi par thème (calcul, mandat, schéma, reprise).
- 💡 **Dans D**, la liste donne aussi « D3 » à ranger dans L : « puis un ADR », oublié (`2026-10-07-liste-adr-chantier-4.md:57-60`).

### Groupe 3 — ils attendent quelque chose (à écrire en dernier)

| N° proposé | Lettres | Sujet | Ce qui manque |
|---|---|---|---|
| **048** | F | Critères de performance | 🟡 « la grille du groupe reste à écrire » ; sens du critère « visites » à vérifier dans le code du sujet (`questions-a-trancher.md:401`, `:228`) |
| **049** | V | Effacement d'un compte : désactiver et rendre anonyme | 🟡 la durée X est à proposer par le groupe, avec sa source |

## 4. Les ADR existants à toucher (sans numéro neuf)

| ADR | Ce qu'on fait | Pourquoi |
|---|---|---|
| **024** | Le finir, avec B dedans ; changer le titre « Annulé » et la phrase « validé par le groupe » | `2026-10-07-liste-adr-chantier-4.md:55-56` |
| **027** | Le réécrire (il est « proposé ») : l'authentification revient (Q-JEF-14), la matrice se met à jour (AA), le rôle lecture seule entre (AB) | `:52-54` ; `questions-a-trancher.md:421-422` |
| **004** | Reste « remplacé par ADR-023 » | Déjà bon : c'est le seul « remplacé » qui suit le modèle du prof |
| **009, 012, 019, 025** | Passent en « remplacé par ADR-0xx » **quand** leur remplaçant est écrit | Règle du prof (`JOURNAL-DE-DECISIONS.md:72`) |
| **016, 026** | Repassent en « accepté », avec une note « annulé le 22/09, remis en vigueur le 08/10 » | Remis en vigueur (Laurence, Discord, 2026-10-08) ; ADR-028 les complète sans les remplacer |

## 5. Le mot « Annulé »

- ⚠️ Le modèle du prof ne connaît que **proposé / accepté / remplacé par ADR-YYY** (`documents utiles/JOURNAL-DE-DECISIONS.md:22`).
- ⚠️ « Annulé » n'y existe pas. La liste le note déjà (`2026-10-07-liste-adr-chantier-4.md:73-75`).
- 💡 **Proposition** : quand Z et B sont écrits, 025 et 024 passent en « remplacé par ». 016 et 026 repassent en « accepté » (remis en vigueur). Sur Confluence, le dossier « Annulé / Remplacé » devient « Remplacé », et les pages 016 et 026 en sortent pour retourner dans « Accepté ».
- 🟡 **À trancher** : si le groupe garde « Refusé » pour les options écartées, il faut dire à quoi il sert (aujourd'hui aucun ADR n'est refusé).

## 6. Ce que je n'ai pas vérifié

- ❌ Je n'ai **pas relu** les 1 437 lignes de `questions-a-trancher.md`, seulement les lignes 1 à 315 et 380 à 439.
- ❌ Je n'ai **pas relu le code** ni le schéma `docker/init-v3/`. Des commits récents renomment des tables (`G2 : remuneration_parameters devient hunter_rate_parameters`) : les noms de tables cités dans les ADR D et I sont peut-être déjà périmés.
- ⚠️ Les numéros **028 à 049** sont **proposés**. Ils ne valent rien tant que le groupe ne les a pas pris sur Confluence.
- ⚠️ Rien n'a été modifié sur Confluence pour cette proposition.

# Qui peut faire quoi — la matrice d'accès par rôle

> 📅 **2 octobre 2026.** Remplace la version du 22/09 (toujours lisible
> dans l'historique git).
>
> 📌 **Statut : livrable de conception, pas du code.** Le client a mis
> l'authentification hors périmètre le 22/09 : « vous ne gérez pas l'auth,
> c'est géré au dessus » (`md/adr/adr-026-perimetre-authentification.md`).
> Cette matrice ne sera donc **pas codée** dans l'API. Elle sert à
> **argumenter** nos choix RGPD et sécurité devant le jury.
> Brouillon d'ADR associé : `md/adr/adr-027-matrice-acces-par-role.md`.

---

## 1. L'essentiel en 5 points

- **4 rôles** : Client, Hunter (chasseur), Manager, Admin.
- **Le parcours du sujet** dit parfois qui **reçoit** une information. Il
  ne dit **jamais** qui n'a **pas** le droit de voir, ni la limite
  « seulement les siens » : ça, ce sont **nos propositions**.
- 💡 **Personne ne supprime rien.** On désactive un compte, et on
  anonymise si le client le demande (RGPD).
- **« Les siens » compte double.** Vérifier le rôle ne suffit pas : un
  chasseur ne doit voir que **ses** clients, pas ceux d'un collègue.
- **Le Manager est le grand inconnu** : le sujet ne décrit pas son
  travail. Toute sa colonne est **à trancher en groupe**.

---

## 2. Comment lire les tableaux

**Les lettres** — ce qu'on a le droit de faire :

| Lettre | Sens |
|---|---|
| **C** | créer |
| **R** | lire |
| **U** | modifier |
| **—** | aucun accès |
| **les siens** | seulement ses propres lignes |

**Les signes** — d'où vient la case :

| Signe | Sens |
|---|---|
| ✅ | **établi** : une source du sujet le dit (tableau « Pourquoi » sous chaque matrice) |
| 💡 | **proposé** par nous : à défendre, pas imposé |
| 🟡 | **à trancher** en groupe : voir la liste au §6 |

⚠️ **Règle de lecture.** Dans « **R** les siens ✅ », le ✅ porte sur
l'accès. La limite « les siens » est **toujours** 💡 : aucune source ne
la donne.

**Les sources** — abréviations utilisées :

| Code | Où le lire |
|---|---|
| **P1** à **P9** | sujet, `Readme.md`, « Le parcours utilisateur actuel » → « Le particulier », étape 1 à 9 |
| **H1** à **H13** | même section → « Le chasseur », étape 1 à 13 |
| **GLO** | sujet, `documents utiles/GLOSSAIRE-METIER.md` |
| **SQL** | `docker/init-v2/01_create_fil_rouge_immobilier.sql` |
| **US** | sujet, `user-stories/*.feature` — « déduites des parcours » (`Readme.md` l.50) : un **appui**, pas une preuve |

---

## 3. Les 4 rôles

| Rôle | Qui c'est | Comptes en base (mesuré le 02/10) |
|---|---|---|
| **Client** | le particulier qui cherche un bien | 18 |
| **Hunter** | le chasseur immobilier | 6 |
| **Manager** | 💡 le manager du chasseur — notre choix du 22/09 (SQL, commentaire l.869) | 1 (compte de migration, pas une vraie personne) |
| **Admin** | 💡 nous, l'équipe technique | 0 |

- ✅ Seules ces **4 valeurs** sont permises pour un rôle (SQL, ligne 148).
- ➡️ Le **notaire** et le **vendeur** apparaissent dans le parcours (H9),
  mais n'ont **aucun rôle** : ils n'utilisent pas le système (hors périmètre).
- ➡️ Les futurs **chasseurs-IA** (`Readme.md`, « Le futur des besoins »)
  sont prévus comme des **Hunters** : colonne `hunter.is_hunter_ai`
  (SQL, ligne 259). 🟡 Ont-ils les mêmes droits qu'un chasseur humain ?

---

## 4. Quatre règles valables partout

### 4.1 On ne supprime jamais 💡

- ✅ Les **34** clés étrangères du schéma sont en `ON DELETE RESTRICT` :
  la base refuse d'effacer une ligne **que d'autres lignes utilisent
  encore**.
- ⚠️ Une ligne que rien n'utilise (une visite, une photo) peut, elle,
  être effacée. C'est donc **notre règle** qui interdit de supprimer,
  pas la base.
- 💡 **Notre proposition** : aucun rôle n'a le droit de supprimer.
  - un compte qu'on arrête → `user.is_activated = false` (la colonne existe)
  - un client qui demande l'effacement → on **anonymise** (« Client 42 »)
- ➡️ C'est pourquoi **aucune case D** (supprimer) n'apparaît dans les
  tableaux.

### 4.2 Les critères ne se modifient jamais ✅

- Chaque changement crée une **nouvelle version**, reliée à la précédente
  (`criteria.id_previous_version`).
- Source : GLO, « Version de demande » — « On ne supprime jamais les
  précédentes ».

### 4.3 « Les siens » = deux contrôles 💡

- Contrôle 1 : **le rôle** (« un chasseur peut lire des clients »).
- Contrôle 2 : **l'appartenance** (« …mais seulement **les siens** »).
- ⚠️ Oublier le contrôle 2, c'est la faille **IDOR** : le chasseur A lit
  les clients du chasseur B.

### 4.4 Le système écrit certaines tables seul

- ✅ **`hunter_performance`** : les indicateurs sont « recalculés et
  affichés » (H12), ou « recalculés à la baisse et affichés » (H13).
  3 moments : `initial`, `payment`, `mandate_expired` (SQL, ligne 802).
- **`estate`** (les biens) : ✅ « le système lui envoie une sélection de
  biens » (H5). 💡 Ces biens viennent de l'**import** des annonces, pas
  d'une saisie.
- ➡️ Dans les tableaux, ces écritures automatiques sont notées **sous** la
  matrice, pas dans une colonne de rôle.

---

## 5. La matrice, table par table

> 18 tables, en 4 familles. Rappel : aucune case **D** (§4.1).

### 5.1 Les comptes

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `role` | — 💡 | — 💡 | — 💡 | **R** 💡 |
| `user` | **R U** le sien 💡 | **R U** le sien 💡 | **R U** le sien 💡 | **C R U** 💡 |
| `client` | **R U** le sien 💡 | **R** ses clients ✅ | 🟡 | **C R U** 💡 |
| `hunter` | **R** son chasseur ✅ | **R U** le sien 💡 | 🟡 | **C R U** 💡 |
| `real_estate_manager` | — 💡 | 🟡 | **R U** le sien 💡 | **C R U** 💡 |

| Pourquoi | Source |
|---|---|
| Client **R** son chasseur | ✅ P2 : la notification lui présente « quel chasseur va s'occuper de son besoin » |
| Hunter **R** ses clients | ✅ H3 : « il prend contact avec le prospect » — il lui faut ses coordonnées |
| Client **U** son compte | 💡 P2 parle de « finaliser la création de son compte », mais sur le site web, « hors de votre scope » (`Readme.md`, « Le SI ») |
| `role` : seul l'Admin le lit | 💡 les autres rôles n'en ont pas besoin |

### 5.2 La demande, les critères, le mandat

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `search_request` | **C** ✅ · **R** la sienne 💡 | **R** les siennes ✅ · **U** accepter / refuser ✅ | 🟡 | **R U** 💡 |
| `criteria` | **C** ✅ · **R** les siens 💡 | **C** ✅ · **R** les siens ✅ | 🟡 | **R** 💡 |
| `mandate` | **R** le sien 💡 · **U** signer ✅ | **C** ✅ · **R** les siens 💡 · **U** 💡 | 🟡 | **R U** 💡 |

| Pourquoi | Source |
|---|---|
| Client **C** la demande et ses premiers critères | ✅ P1 : il « formule une demande » en ligne |
| Hunter **R** et **U** la demande | ✅ H1 : il la reçoit ; H2 : il « peut ne pas l'accepter » |
| Hunter **C** critères | ✅ H4 : « il affine les critères » → une nouvelle version (§4.2) |
| Hunter **C** le mandat | ✅ H4 : il « fait signer le mandat » |
| Client **U** signer | ✅ P3 : « signer le mandat de recherche » ; colonne `mandate.is_client_signed` |
| Renouveler un mandat | ✅ H13 : c'est un **nouveau** mandat, relié à l'ancien (`mandate.id_mandate_parent`) |

### 5.3 Les biens, la sélection, les visites

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `estate` | **R** 🟡 | **R** ✅ | 🟡 | **R U** 💡 |
| `picture` | comme `estate` | comme `estate` | comme `estate` | comme `estate` |
| `estate_proposed` | **R** les siens ✅ · **U** commenter, choisir, faire une offre ✅ | **C R U** ✅ | 🟡 | **R** 💡 |
| `estate_searchrequest` | **R** l'avis ✅ | **C R U** ✅ | 🟡 | **R** 💡 |
| `visit` | **R** les siennes 💡 · **C** 🟡 | **C R** ✅ | 🟡 | **R U** 💡 |

Écrit par le système : `estate` et `picture` (import des annonces, §4.4).

| Pourquoi | Source |
|---|---|
| Hunter **R** les biens | ✅ H2 et H5 : le système lui affiche les biens |
| `estate_proposed` = la sélection proposée au client | ✅ H5 : il « en fait une sélection à proposer » ; P4 : le client la reçoit |
| Client **U** : commenter | ✅ H6 : le client a « commenté et priorisé » ; colonne `comment_client` |
| Client **U** : choisir les biens à visiter | ✅ P4 : il « choisit les biens à visiter ». ⚠️ Aucune colonne ne stocke ce choix |
| Client **U** : faire une offre | ✅ H8 : « le système lui présente une offre d'achat à compléter et signer » ; colonnes `amount_proposition`, `proposition_status` |
| Hunter **U** : transmettre l'offre | ✅ H9 : « le chasseur transmet l'offre d'achat au vendeur » |
| `estate_searchrequest` = l'avis du chasseur | ✅ H7 : « note d'avis », audio, vidéo ; P5 : le client la reçoit |
| Hunter **C** une visite | ✅ P5 : « après que ce dernier ait effectué des visites » |
| Client **C** une visite | 🟡 P6 : il « est invité à visiter », et `visit.visitor_type` accepte `client`. Mais qui l'enregistre ? |

### 5.4 L'argent et la performance

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `sale` | **R** la sienne ✅ | **R** les siennes 💡 | 🟡 | **R** 💡 · **C** 🟡 |
| `parameters_fees` | 🟡 | 🟡 | 🟡 | **C R U** 💡 |
| `commission_scale` | — 💡 | **R** le sien 🟡 | 🟡 | **C R U** 💡 |
| `payment` | — 💡 | **R** les siens ✅ · **U** envoyer sa facture ✅ | 🟡 | **R U** 💡 · **C** 🟡 |
| `hunter_performance` | — 💡 | **R** la sienne ✅ | 🟡 | **R** 💡 |

Écrit par le système : `hunter_performance` (§4.4).

| Pourquoi | Source |
|---|---|
| Client **R** sa vente | ✅ P8 : « paiement des honoraires » ; P9 : « il reçoit sa facture ». Le montant est `sale.fees_amount` |
| Hunter **R** son paiement | ✅ H10 : il est « prévenu du paiement proche de sa rémunération et de son montant » |
| Hunter **U** : envoyer sa facture | ✅ H11 : il « a envoyé sa facture dans le système ». ⚠️ Aucune colonne ne stocke la facture : seul l'état passe à `invoice_submitted` |
| Hunter **R** sa performance | ✅ H12 : les indicateurs sont « recalculés et affichés » |
| Client sans accès à l'argent du chasseur | 💡 minimisation RGPD : il n'en a pas besoin |

**Les 6 états d'un paiement** (SQL, ligne 727) :
`announced` → `invoice_submitted` → `verified` → `scheduled` → `paid`,
ou `refused` — avec un motif obligatoire (ADR-024, la décision sur le
motif de refus).
- ✅ Le chasseur fait passer à `invoice_submitted` (H11).
- 🟡 Qui fait passer aux autres états ? H11 dit seulement « le système
  l'affiche comme vérifiée ».

---

## 6. Ce qu'il faut trancher en groupe

Du plus bloquant au moins bloquant.

| # | Question | Pourquoi c'est ouvert |
|---|---|---|
| 1 | **Que voit et que fait le Manager ?** | Le sujet ne décrit pas son travail. Notre schéma le relie aux chasseurs et aux demandes (« le manager qui traite la demande », commentaire SQL de `search_request.id_realestatemanager`) |
| 2 | **Qui affecte une demande à un chasseur ?** | « un chasseur est affecté au prospect » (`Readme.md` l.73) ; US 01 : « un processus d'affectation d'un chasseur est déclenché ». Aucun des deux ne dit **qui** |
| 3 | **Qui enregistre la vente ?** | L'acte est signé chez le notaire (H9), et le notaire n'a pas de rôle |
| 4 | **Qui crée le paiement, et le fait avancer après la facture ?** | H10 : « une fois que l'entreprise reçoit les honoraires » ; H11 : « le système » — sans dire qui |
| 5 | **Où stocker la facture du chasseur ?** | Aucune colonne ne la porte (§5.4) |
| 6 | **Le client voit-il tout le catalogue, ou seulement ses propositions ?** | P4 dit qu'il **reçoit** des propositions, pas qu'il cherche lui-même |
| 7 | **Le chasseur voit-il son barème de commission ?** | Question de confidentialité salariale |
| 8 | **Qui fixe les honoraires et les barèmes ?** | Personne ne les touche dans le parcours |
| 9 | **Qui crée le compte du client ?** | Il naît sur le site web (P1-P2), « hors de votre scope » (`Readme.md`, « Le SI ») |
| 10 | **Qui enregistre une visite faite par le client ?** | P6 l'invite à visiter ; `visit.visitor_type` accepte `client` |
| 11 | **Les chasseurs-IA ont-ils les droits d'un chasseur ?** | Prévus comme Hunters (`hunter.is_hunter_ai`). Par analogie : le sujet veut, pour une IA ouverte sur la base, un accès « idéalement lecture seule » |
| 12 | **Le chasseur peut-il créer une demande pour un client ?** | Le schéma le permet (`search_request.id_author`), le parcours ne le dit pas |
| 13 | **Sous quel compte tourne l'import des biens ?** | Aucun rôle humain ne crée un bien |
| 14 | **La priorité et le choix du client** : où les stocker ? | H6 : le client a « commenté et priorisé » ; P4 : il « choisit les biens à visiter ». Aucune colonne pour l'un ni pour l'autre |
| 15 | **Au bout de combien de temps anonymiser ?** | Le sujet demande une durée de conservation, sans chiffre |

⚠️ **Une question à reposer au client.** Le 22/09, la question posée
mélangeait « l'authentification » et « ce qu'ils peuvent faire sur
l'application ». Sa réponse ne justifie que l'authentification.

---

## 7. Ce qu'on dit au jury

- ❌ **Ne pas dire** : « le cahier des charges impose ces droits ». C'est
  faux : le sujet ne parle jamais de droits d'accès par rôle.
- ✅ **Dire plutôt** : « Le RGPD est exigé par le sujet, avec la protection
  des données dès la conception. Nous avons appliqué la **minimisation** :
  chacun n'accède qu'à ce dont il a besoin. Le détail est notre arbitrage,
  tracé dans un ADR. »
- Sources : `Readme.md`, « Exigences transverses » (« Elles ne sont pas
  optionnelles ») et « RGPD » (*privacy by design*).
- 💡 Le sujet demande aussi un **périmètre d'accès** pour l'**IA** branchée
  sur la base, « idéalement lecture seule » (`Readme.md`, « Souveraineté &
  sécurité »). Cette matrice applique la même idée aux **humains**.

---

## 8. Rejouer les mesures

Depuis `Fil-Rouge/` :

```bash
grep -c 'ON DELETE RESTRICT' docker/init-v2/01_create_fil_rouge_immobilier.sql
```

Attendu : **34**.

Comptes par rôle, base lancée, depuis `docker/` :

```bash
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "select r.wording, count(u.id) from role r left join public.user u on u.id_role = r.id group by r.wording"'
```

Attendu : Admin 0, Client 18, Hunter 6, Manager 1.

---

## Lexique

| Mot | Sens |
|---|---|
| **CRUD** | créer, lire, modifier, supprimer (en anglais) |
| **Appartenance** | une ligne « appartient » à un utilisateur : son compte, ses clients |
| **IDOR** | la faille quand on oublie l'appartenance : A lit les données de B |
| **`ON DELETE RESTRICT`** | la base refuse d'effacer une ligne encore utilisée ailleurs |
| **Minimisation** | principe RGPD : n'accéder qu'au strictement nécessaire |
| **Anonymiser** | remplacer les données qui identifient quelqu'un, sans effacer la ligne |
| **ADR** | une décision d'architecture écrite, avec ses raisons |

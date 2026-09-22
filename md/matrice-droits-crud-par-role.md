# Qui a le droit de faire quoi — les 4 rôles, table par table

> 📖 **Pour tout le groupe.** Aucune notion de sécurité supposée.
> Support de la réunion : les cases 🟡 sont à trancher **ensemble**.
>
> 📅 22 septembre 2026. Prolonge le §4.3 de
> `md/securite-mots-de-passe-et-droits.md`, qui ouvrait le tableau.
>
> ⚠️ **Cette note ne fait pas foi.** Chaque affirmation ✅ porte sa source
> au §7. Ce qui n'a pas de source est marqué 🟡, même si ça paraît évident.

---

## 1. Le constat, en trois phrases

**1.** L'énoncé ne dit **rien** sur les droits d'accès. Pas une ligne.

**2.** La seule phrase qui en parle — *« l'accès aux données de rémunération
est restreint au chasseur concerné et à son manager »* — est un **exemple de
rédaction** dans un modèle de document, pas une exigence du client. C'est
déjà acté (`securite-mots-de-passe-et-droits.md` §7.1).

**3.** Donc : les sources nous disent **qui fait quoi dans le parcours**.
Elles ne nous disent **pas qui a le droit de regarder quoi**.

➡️ **Conséquence directe** : les colonnes « créer » et « modifier » sont
largement tranchées par le parcours client/chasseur. Les colonnes « lire »
et « supprimer » sont presque entièrement à décider par nous.

### 1.1 Un chiffre qui simplifie tout

| Vérification, le 22/09 | Résultat |
|---|---|
| Clés étrangères dans le schéma v2 | **34** |
| En `ON DELETE RESTRICT` | **34** |
| En `ON DELETE CASCADE` | **0** |

➡️ **Le « supprimer » est déjà fermé par la base.** Dès qu'une ligne est
reliée à une autre, PostgreSQL refuse le `DELETE`. Supprimer un client
qui a une demande : impossible. Supprimer un mandat qui a une vente :
impossible.

💡 Ce n'est pas un accident, c'est une bonne nouvelle : ça nous évite
d'avoir à écrire la règle. On la **constate**, on la documente.

⚠️ Ce que ça n'empêche pas : supprimer une ligne **isolée** (un compte
tout neuf, une photo). D'où la question 🟡 « on supprime ou on désactive ? »

### 1.2 Comment lire les tableaux

| Signe | Sens |
|---|---|
| **C** | créer une ligne |
| **R** | lire (de l'anglais *read*) |
| **U** | modifier (*update*) |
| **D** | supprimer (*delete*) |
| ✅ | tranché, avec une source citable |
| 🟡 | **à discuter en réunion** |
| ❌ | non, et c'est proposé comme tel |
| ⚙️ | c'est le **système** qui écrit, pas une personne |
| *siens* | seulement ses propres lignes |

---

## 2. Les 4 rôles, une phrase chacun

Les quatre rôles existent en base depuis le 22/09 ✅ :

| Rôle | Qui c'est | Comptes aujourd'hui |
|---|---|---|
| **Client** | le particulier qui cherche un bien | 18 |
| **Hunter** | le chasseur immobilier | 6 |
| **Manager** | l'encadrant des chasseurs | 1 *(placeholder, bloqué)* |
| **Admin** | nous, l'équipe technique | **0** |

⚠️ Le Manager en base **n'est pas une personne** : c'est un bouche-trou de
migration. Et il n'y a **aucun** compte Admin.

✅ Le hachage Argon2id est en place depuis le 22/09 (commit `d8ba03d`) :
plus rien ne bloque la **création des vrais comptes** Manager et Admin.
Proposition déjà sur la table : **1 admin, 2 managers** — deux, pour
pouvoir démontrer qu'un manager ne voit pas les chasseurs de l'autre.

---

## 3. Ce que chaque rôle peut, et ne peut pas

> Version vulgarisée. Le détail table par table est au §5.

### 👤 Le **Client** — il gère son projet d'achat, et rien d'autre

**Il peut :**

- ✅ déposer sa demande de recherche
- ✅ créer et modifier **son** compte
- ✅ faire évoluer ses critères (ça crée une **nouvelle version**)
- ✅ signer son mandat
- ✅ lire les biens qu'on lui propose, les commenter
- ✅ lire l'avis du chasseur après visite
- ✅ lire sa vente et sa facture

**Il ne peut pas :**

- ❌ voir un autre client, ni un autre chasseur que le sien
- ❌ voir **combien gagne son chasseur** — ni le barème, ni le paiement
- ❌ voir les indicateurs de performance de son chasseur
- ❌ effacer une version de ses critères (l'historique est obligatoire)

**🟡 À trancher :** voit-il **tout** le catalogue de biens, ou seulement
ceux qu'on lui a proposés ? C'est la question la plus ouverte de sa liste.

---

### 🕵️ Le **Hunter** (chasseur) — il travaille pour **ses** clients

**Il peut :**

- ✅ accepter ou refuser une demande qu'on lui affecte
- ✅ lire la fiche de **ses** clients (il doit les appeler)
- ✅ affiner les critères (nouvelle version, là aussi)
- ✅ faire signer le mandat, le renouveler
- ✅ construire sa sélection de biens, la proposer, écrire son avis
- ✅ enregistrer les visites
- ✅ envoyer sa facture
- ✅ lire **sa** rémunération et **ses** indicateurs de performance

**Il ne peut pas :**

- ❌ voir un client qui n'est pas le sien
- ❌ voir la rémunération d'un autre chasseur
- ❌ se fixer son propre barème de commission
- ❌ écrire lui-même ses indicateurs de performance (c'est le système)

**🟡 À trancher :** voit-il **son propre barème** de commission ? Et
peut-il créer une demande à la place d'un client (le schéma le permet :
`search_request.id_author`) ?

⚠️ **Le piège n° 1 du projet.** Deux chasseurs ont le **même rôle**. Si on
ne vérifie que le rôle, le chasseur A lit les paiements du chasseur B. Il
faut **deux** contrôles : le rôle **et** l'appartenance de la ligne.

---

### 👔 Le **Manager** — le seul rôle presque entièrement à définir

**Ce qui est acquis :**

- ✅ le lien « ce chasseur est encadré par ce manager » **existe en base**
  depuis le 22/09 (`hunter.id_realestatemanager`, obligatoire)
- ✅ donc la phrase « ses chasseurs » a enfin un sens technique

**Ce qui n'est décidé nulle part :**

- 🟡 lit-il les paiements de ses chasseurs ?
- 🟡 fixe-t-il les barèmes de commission ?
- 🟡 lit-il les mandats et les ventes de son équipe ?
- 🟡 voit-il les clients de ses chasseurs ?
- 🟡 valide-t-il les factures des chasseurs ?

➡️ **C'est le gros morceau de la réunion.** Aucune source ne parle de lui :
tout ce qu'on écrira sera **notre arbitrage**, à tracer en ADR.

---

### 🔧 L'**Admin** — nous, et personne d'autre

**Il peut :** tout lire, tout créer, tout corriger.

**Il ne peut pas (proposition) :**

- ❌ supprimer un mandat, une vente, un paiement → **documents légaux et
  traces comptables**, on ne les efface pas
- ❌ supprimer une version de critères → l'historique est **exigé par le
  sujet**
- ❌ supprimer un compte lié à quoi que ce soit → **la base le refuse déjà**

💡 Un admin qui ne peut rien effacer, ce n'est pas une limite : c'est
l'argument qu'on présente au jury sur la traçabilité.

---

## 4. Le cas « supprimer » — à lire avant la réunion

Trois façons de faire disparaître quelqu'un, et elles ne se valent pas :

| Façon | Ce que ça fait | Notre avis |
|---|---|---|
| `DELETE` | la ligne disparaît | ❌ casse l'historique, et la base le refuse déjà 34 fois sur 34 |
| `is_activated = false` | le compte ne peut plus se connecter | ✅ la colonne **existe déjà** dans `user` |
| Anonymisation | le nom devient « Client 42 » | ✅ c'est la réponse RGPD au droit à l'effacement |

➡️ **Proposition** : on ne supprime jamais, on **désactive**, et on
**anonymise** si le client le demande. Ça se défend en soutenance au titre
du RGPD, et ça ne coûte presque rien à coder.

🟡 Reste à décider : au bout de combien de temps on anonymise ? Le sujet
dit « durée du mandat + durée légale », sans chiffre.

---

## 5. La matrice détaillée, table par table

> 18 tables, regroupées par domaine. Une ligne = une table.
> Rappel : **C** créer · **R** lire · **U** modifier · **D** supprimer.

### 5.1 Comptes et identités

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `role` | ❌ | ❌ | ❌ | **R** seul ✅ |
| `user` | **R U** sien ✅ | **R U** sien ✅ | **R U** sien ✅ | **C R U** ✅ |
| `client` | **R U** sien ✅ | **R** *ses clients* ✅ | 🟡 *ceux de son équipe ?* | **C R U** ✅ |
| `hunter` | ❌ | **R U** sien ✅ | 🟡 *ses chasseurs ?* | **C R U** ✅ |
| `real_estate_manager` | ❌ | 🟡 *son manager ?* | **R U** sien 🟡 | **C R U** ✅ |

- `role` ne contient que 4 lignes verrouillées par une contrainte.
  Ajouter un rôle = une migration, pas un appel d'API. ➡️ **lecture seule
  pour tout le monde**, proposition.
- 🟡 **Qui crée le compte d'un client ?** Le parcours dit que le
  particulier « finalise » son compte — donc quelqu'un l'a commencé.
  Inscription publique ou création par le chasseur ? Non tranché.

### 5.2 Demande, critères, mandat

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `search_request` | **C** ✅ · **R** sienne ✅ | **R** siennes ✅ · **U** accepter/refuser ✅ · **C** 🟡 | 🟡 | **C R U** ✅ |
| `criteria` | **C** version ✅ · **R** ✅ | **C** version ✅ · **R** ✅ | 🟡 | **C R** ✅ |
| `mandate` | **R** sien ✅ · **U** signer ✅ | **C** ✅ · **R** siens ✅ · **U** statut ✅ | 🟡 | **C R U** ✅ |

- ✅ **`criteria` ne se modifie jamais et ne s'efface jamais.** Chaque
  changement crée une **nouvelle version** qui pointe vers la précédente.
  C'est une exigence explicite du sujet, pas un choix.
- ✅ Le chasseur **et** le client peuvent tous deux créer une version : la
  colonne `id_author` est là pour ça.
- 🟡 Un chasseur peut-il **créer** une demande pour un client ? Le schéma
  le permet. Le parcours ne le prévoit pas.

### 5.3 Biens, sélection, visites

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `estate` | **R** 🟡 *tout ou ses propositions ?* | **R** ✅ | **R** 🟡 | **R U** ✅ · **C** ⚙️ |
| `picture` | idem `estate` | idem `estate` | idem | idem |
| `estate_searchrequest` | **R** l'avis ✅ | **C R U** ✅ | 🟡 | **R** ✅ |
| `estate_proposed` | **R** siennes ✅ · **U** son commentaire ✅ | **C R U** ✅ | 🟡 | **R** ✅ |
| `visit` | **R** siennes ✅ · **C** 🟡 | **C R** ✅ | 🟡 | **C R U** ✅ |

⚠️ **Personne ne crée un bien à la main.** Les biens viennent des annonces
importées (`normalised/`). Le **C** est donc un **import automatique**, pas
un rôle humain. 🟡 Sous quel compte tourne cet import ?

🟡 **Le client voit-il tout le catalogue ?** Le §4.3 de la note du 22/09
proposait « ✅ pour les 4 rôles ». Ça se discute : le parcours dit qu'il
**reçoit des propositions**, il ne dit pas qu'il fouille la base.

🟡 **La colonne « priorité » manque.** Le parcours dit que le client
« commente **et priorise** » la sélection. La colonne n'existe pas :
l'échelle n'a pas été choisie (1 à 5 ? haute / moyenne / basse ?).

### 5.4 Argent et performance

| Table | Client | Hunter | Manager | Admin |
|---|---|---|---|---|
| `sale` | **R** sienne ✅ | **R** siennes ✅ | 🟡 | **C R** 🟡 *qui saisit ?* |
| `parameters_fees` | **R** 🟡 | **R** 🟡 | 🟡 | **C R U** 🟡 |
| `commission_scale` | ❌ ✅ | **R** le sien 🟡 | 🟡 *fixe-t-il ?* | **C R U** 🟡 |
| `payment` | ❌ ✅ | **R** siens ✅ · **U** envoi facture ✅ | 🟡 *ceux de son équipe ?* | **R U** ✅ · **C** ⚙️ |
| `hunter_performance` | ❌ | **R** sien ✅ | 🟡 | **R** ✅ · **C** ⚙️ |

- ✅ **`hunter_performance` n'est jamais saisi à la main.** Le système le
  recalcule à trois moments : au départ, à chaque paiement, à chaque mandat
  expiré. Aucun rôle humain ne l'écrit — pas même l'admin.
- 🟡 **Qui enregistre la vente ?** L'acte est signé chez le **notaire**, et
  le notaire n'est **pas** un utilisateur du système. Donc quelqu'un saisit
  la vente après coup : le chasseur ? le manager ? un back-office ? **Rien
  ne le dit.**
- 🟡 **Le circuit de la facture.** Le parcours dit « le système affiche ma
  facture comme vérifiée ». Le mot « système » ne dit pas **qui**. Le
  paiement passe par 5 états : annoncé → facture envoyée → vérifiée →
  programmée → payée. Qui pousse chaque bouton ?
- 🟡 **Les honoraires et les barèmes** sont des paramètres d'entreprise.
  Personne ne les touche dans le parcours. Manager ou Admin ?

---

## 6. Ce qu'il faut trancher en réunion

Par ordre d'importance, le plus bloquant d'abord.

| # | La question | Pourquoi ça bloque |
|---|---|---|
| **1** | **Le Manager voit quoi ?** Les 5 lignes 🟡 du §3 | Un rôle entier sans aucune règle |
| **2** | **Qui saisit la vente ?** | Le notaire n'est pas dans le SI, et sans vente il n'y a pas de rémunération |
| **3** | **Qui fait avancer la facture** dans ses 5 états ? | Bloque la fin du parcours chasseur |
| **4** | **Le client voit-il tout le catalogue** de biens ? | Change la taille de ce qu'on expose |
| **5** | **Le chasseur voit-il son barème** de commission ? | Question de confidentialité salariale |
| **6** | **Qui fixe les barèmes et les honoraires** ? | Manager ou Admin |
| **7** | **On supprime ou on désactive ?** | Proposition au §4, à valider |
| **8** | **L'import des biens** tourne sous quel compte ? | Aucun rôle humain ne crée un bien |
| **9** | **L'échelle de priorité** du client (D6) | Colonne absente du schéma |

➡️ Une fois validé, ce tableau devient un **ADR**. C'est explicitement
prévu : *« la matrice d'accès mérite son propre ADR »*.

### 6.1 L'argument à sortir en soutenance

Ne **jamais** dire « le cahier des charges impose que… » — c'est faux, et
un jury le vérifie en trente secondes.

✅ **Dire plutôt** : *« Le RGPD est une exigence explicite du sujet. Nous
avons appliqué le principe de **minimisation** : chacun n'accède qu'au
strictement nécessaire. Le détail du qui-voit-quoi est notre arbitrage,
tracé dans l'ADR. »*

C'est exact, et beaucoup plus difficile à contester.

---

## 7. Sources

| Affirmation | Source |
|---|---|
| Le parcours client (demande, compte, mandat, propositions, avis, facture) | `BASE/Readme.md`, « Le parcours utilisateur actuel » ; `user-stories/01` à `03` |
| Le parcours chasseur (accepter, affiner, sélectionner, avis, offre, facture) | `BASE/Readme.md`, même section ; `user-stories/04` à `07` |
| Les critères sont **versionnés**, jamais écrasés, avec date/auteur/motif | `BASE/Readme.md` Phase 2 ; `BASE/documents utiles/GLOSSAIRE-METIER.md`, « Version de demande » |
| Le notaire est **hors périmètre** du SI | `BASE/documents utiles/GLOSSAIRE-METIER.md`, « Acteurs » |
| ENF-03 (chasseur + manager) est un **exemple**, pas une exigence | `BASE/documents utiles/CAHIER-DES-CHARGES-TECHNIQUE.md`, « Exigences non fonctionnelles **(extrait)** » |
| Le RGPD n'est pas optionnel | `BASE/Readme.md`, section RGPD |
| Les 4 rôles Client / Hunter / Manager / Admin | `docker/init-v2/01_create_fil_rouge_immobilier.sql`, table `role` ; `docker/migrations/2026-09-22_role_admin.sql` |
| 34 clés étrangères, 34 en `ON DELETE RESTRICT`, 0 en `CASCADE` | mesuré le 22/09 sur `01_create_fil_rouge_immobilier.sql` — commande au §7.1 |
| `user.is_activated` existe déjà | même fichier, table `user` |
| `search_request.id_author` et `criteria.id_author` | même fichier |
| Les 5 états du paiement | même fichier, table `payment`, contrainte `status` |
| `hunter_performance` écrit sur 3 déclencheurs | même fichier, colonne `trigger_type` |
| La colonne « priorité client » manque (décision D6) | même fichier, `estate_proposed`, bloc TODO |
| Le lien chasseur → manager, obligatoire depuis le 22/09 | même fichier, `hunter.id_realestatemanager` ; `md/adr-025-lien-chasseur-manager.md` |
| Le tableau de départ, et ses cases 🟡 | `md/securite-mots-de-passe-et-droits.md` §4.3 |
| Rôle ≠ appartenance : le piège IDOR | `md/securite-mots-de-passe-et-droits.md` §4.1 |

### 7.1 Rejouer la mesure des `ON DELETE`

Depuis `Fil-Rouge/` :

```bash
grep -c 'ON DELETE RESTRICT' docker/init-v2/01_create_fil_rouge_immobilier.sql
```

Attendu : **34**. Et `ON DELETE CASCADE` doit donner **0**.

---

## Lexique

| Terme | Définition |
|---|---|
| **CRUD** | les 4 opérations sur une donnée : créer, lire, modifier, supprimer |
| **RBAC** | contrôle d'accès **par rôle** — « un chasseur peut voir les paiements » |
| **Ownership** | contrôle d'**appartenance** — « …mais seulement **les siens** » |
| **IDOR** | la faille quand on oublie l'ownership : A lit les données de B |
| **`ON DELETE RESTRICT`** | la base refuse d'effacer une ligne encore utilisée ailleurs |
| **Minimisation** | principe RGPD : n'accéder qu'au strictement nécessaire |
| **ADR** | décision d'architecture tracée, sur Confluence |

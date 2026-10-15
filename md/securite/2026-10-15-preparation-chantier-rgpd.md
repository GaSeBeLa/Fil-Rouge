# Préparation du chantier RGPD — le terrain dégrossi

> 📋 **Ce n'est pas un chantier ouvert.** C'est la matière pour le cadrer plus
> tard avec `/vlp:chantier` : ce que le sujet demande, ce qui existe déjà, ce
> qui manque, et les questions à trancher. Rien n'est décidé ici.
>
> Écrit le 2026-10-15, à la demande de Sébastien (« dégrossir le futur
> travail »). TODO n° 5 de `context AI/08-etat.md` (« Doc d'équipe »).
>
> ✅ établi par une source · 🟡 à trancher · 💡 proposé par Claude

**Abréviations**

- `01` = `docker/init-v3/01_create_fil_rouge_immobilier.sql` (dépôt Fil-Rouge-API).
- `SP` = `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/` (sujet, lecture seule).
- `REG` = `SP/documents utiles/REGISTRE-RGPD.md`.
- `SOU` = `SP/documents utiles/SOUVERAINETE-SECURITE-IA.md`.

⚠️ **État lu** : le `01` de `main` dans Fil-Rouge-API, avec les fiches FLX déjà
commitées (`5548e55`, FLX5, **non poussé**). Le schéma `olap` et les logs
peuvent encore bouger tant que le chantier FLX n'est pas clos.

---

## 0. La RGPD pour débutants — les mots à connaître

Pour que tout le groupe suive, même sans avoir jamais fait de RGPD. Chaque
définition vient du sujet.

| Le mot | Ce qu'il veut dire | Un exemple chez nous |
|---|---|---|
| **RGPD** | la loi européenne qui protège les informations sur les personnes | — |
| **Donnée personnelle** | toute information qui désigne une personne (`REG:13`) | l'e-mail d'un client, son téléphone, et même son budget |
| **Donnée sensible** | santé, opinions, origine… (`REG:14`) | aucune chez nous (§ 3) |
| **Traitement** | ce qu'on fait des données, pour un but précis (`REG:23`) | « gérer les mandats » |
| **Finalité** | le but du traitement (`REG:15`) | « trouver un bien pour le client » |
| **Base légale** | la raison qui nous autorise à garder la donnée : contrat, consentement, loi, intérêt légitime (`REG:16`) | le mandat signé = un contrat |
| **Durée de conservation** | combien de temps on garde, avant d'effacer ou d'anonymiser (`REG:17`) | 10 ans pour un mandat |
| **Minimisation** | ne garder que le nécessaire (`REG:9`) | pas d'IBAN dans notre base |
| **Anonymiser** | retirer tout moyen de retrouver la personne, pour toujours (`SOU`, § 2) | remplacer le nom par « Anonyme » |
| **Pseudonymiser** | remplacer le nom par un numéro ; on peut revenir en arrière avec une clé (`SOU`, § 2) | l'OLAP garde `id_client` |
| **Registre** | le tableau qui liste tous les traitements | le livrable à écrire |

---

## 1. Ce que le sujet demande

- ✅ Un **registre de traitement minimal** : pour chaque traitement, la
  finalité, la base légale, la durée de conservation, et les données
  sensibles (`SP/Readme.md:270`).
- ✅ C'est **« pas optionnel »**, et pénalisant en jury (`SP/Readme.md:266`).
- ✅ Une ligne **par traitement**, pas par table (`REG:23`).
- ✅ En plus du registre : minimisation, sécurité, **droits des personnes**,
  anonymisation, privacy by design (`REG:34-40`).
- ✅ Une **note souveraineté & sécurité des données** face à l'IA : périmètre
  d'accès, anonymisation, localisation (`SP/Readme.md:282`, modèle dans `SOU`).
- ✅ La grille a une case « RGPD : Registre de traitement »
  (`SP/documents utiles/GRILLE-EVALUATION.md:96`).
- ✅ À l'oral : 2 minutes sur les arbitrages transverses
  (`SP/documents utiles/TRAME-SOUTENANCE.md:21`).

➡️ **Deux livrables à écrire** : le registre (avec les droits des personnes),
et la note souveraineté IA.

---

## 2. Ce qui existe déjà

| Sujet | Ce qui est fait | Où |
|---|---|---|
| Effacer un compte | désactiver, rendre anonyme tout de suite ce que rien n'oblige à garder ; le nom attend **10 ans** s'il y a un mandat ou un paiement | ADR-049, accepté ; codé fiche API10 : `POST /users/{id}/anonymize`, Admin |
| Supprimer une ligne | **plus aucune route `DELETE`** (`405`) | ADR-049, point 10 ; API10 |
| Contact du vendeur | gardé **3 ans** après la dernière activité du bien, puis anonymisé | ADR-054 ; `POST /estate-contacts/anonymize-expired`, Admin |
| Qui lit le contact du vendeur | Admin, Hunter, Manager ; ni Client ni Reader | `API/src/app/routes/estate_contact_router.py:17`, `:26` ; migration 41 |
| Droits par rôle | rôle, puis « le sien » table par table | chantier DRO ; `md/securite/matrice-droits-crud-par-role.md` § 3 |
| Mots de passe | Argon2id, jamais renvoyés par l'API | ADR-016 ; `md/securite/` |
| OLAP | aucune identité directe dans les dimensions | `docker/init-v3/08_olap.sql:54-57` (FLX5, non poussé) |
| Recherche de biens | `estate_contact` jamais dans l'index | question flux-14, tranchée A le 15/10 |
| Logs de l'API | jamais le jeton, le mot de passe ni un e-mail | fiche FLX10, **pas encore jouée** |
| Chasseur IA | droits réduits, pas de contact du vendeur | ADR-058, **💡 proposé** |
| IBAN | **absent** du schéma : grep `iban` dans `01` = 0 | minimisation, à dire |

✅ **Le gros des décisions est pris.** Le registre range surtout ce qui
existe : ce chantier est **surtout de l'écriture**.

---

## 3. Inventaire des données personnelles

Lu dans `01` le 2026-10-15. Une donnée personnelle désigne une personne,
même un budget lié à un client identifié (`REG:13`).

### Les personnes

| Table | Colonnes personnelles | Nombre |
|---|---|---|
| `"user"` | `email`, `password` (haché), `is_activated`, `system_role` | 4 |
| `client` | `first_name`, `last_name`, `phone_number`, `address`, `address_complement`, `postal_code`, `town`, `country_iso`, `gender`, `birth_date`, `is_married`, `is_civil_solidarity_pact`, `nb_children` | 13 |
| `real_estate_manager` | `first_name`, `last_name`, `phone_number`, `country_iso`, `gender`, `company_name` | 6 |
| `hunter` | `first_name`, `last_name`, `phone_number`, `country_iso`, `gender`, `company_name`, `hire_date`, `education_level`, `is_carte_t`, `certification_date`, `is_hunter_ai` | 11 |
| `estate_contact` (un tiers : le vendeur) | `contact_name`, `phone_number`, `email`, `agency_name`, `is_private` | 5 |

### Liées à une personne

| Table | Colonnes | Pourquoi c'est personnel |
|---|---|---|
| `criteria` | `budget_min`, `budget_max`, `town`, `district`, `change_reason`… | le projet d'achat d'un client identifié |
| `estate_proposed` | `comment_client`, `comment_hunter`, `amount_proposition` | textes libres, offre d'un client |
| `estate_searchrequest` | `review_hunter` | texte libre, peut citer le client (ADR-049, Conséquences) |
| `estate` | `street`, `street_number`, `latitude`, `longitude`, `information` | 💡 l'adresse d'un bien désigne son vendeur ; `information` est un texte libre |
| `visit`, `sale`, `mandate` | dates, montants, statut | la vie d'un contrat avec une personne |
| `payment`, `commission_scale`, `hunter_performance` | montants, taux, `score`, `calculation_details` | la paie et la note d'un chasseur |
| `picture`, `review_media` | `url`, `media_url` | 💡 une photo peut montrer une personne |

### Données sensibles

- ✅ Le sujet les définit : « santé, opinions, origine… », « normalement
  absente ici, mais à vérifier » (`REG:14`).
- ✅ **Aucune colonne de ces catégories** dans `01` (relu table par table, ci-dessus).
- 💡 À **challenger quand même** (minimisation, `REG:36`) : `gender`,
  `birth_date`, `is_married`, `is_civil_solidarity_pact`, `nb_children`.
  À quoi servent-elles dans une chasse immobilière ? Question 🟡 RGPD-6.
- 💡 La **note de performance** du chasseur (`hunter_performance.score`) est
  une évaluation chiffrée d'une personne. Le calcul est tracé
  (`calculation_details`, ADR-033) : c'est la réponse à préparer pour l'oral.

---

## 4. Le registre, en brouillon

Une ligne par traitement (`REG:23`). Les **bases légales** sont des
propositions 💡 : le modèle du sujet en donne trois exemples (`REG:27-29`),
le reste est à valider (🟡 RGPD-16).

| # | Traitement | Finalité | Base légale | Durée | Qui y accède |
|---|---|---|---|---|---|
| T1 | Comptes et connexion | se connecter à son espace | 💡 contrat (`REG:28`) | ✅ tant que le compte est actif (`REG:28`) ; sur demande, anonymisé (ADR-049) ; 🟡 compte oublié (RGPD-10) | la personne, Admin ; Reader sans le mot de passe |
| T2 | Fiche client et demande de recherche | trouver un bien pour le client | 💡 contrat, et avant lui la demande du client | ✅ identité : 10 ans après la fin du dernier mandat ; le reste anonymisé sur demande ; mandat jamais signé : tout de suite (ADR-049, point 5) | le client (le sien), ses chasseurs, le manager de l'équipe, Admin, Reader |
| T3 | Mandats, propositions, visites, ventes | exécuter le mandat de recherche | ✅ contrat + obligation légale (décret n° 72-678, article 72, cité par ADR-049) | ✅ **10 ans** après la fin du mandat (ADR-049) | client, chasseur, manager de l'équipe, Admin, Reader |
| T4 | Contact du vendeur | joindre le vendeur d'un bien repéré | 💡 intérêt légitime : le vendeur n'a pas de contrat avec nous | ✅ **3 ans** après la dernière activité du bien (ADR-054) | Admin, Hunter, Manager (`estate_contact_router.py:17`) |
| T5 | Chasseurs et managers | gérer l'équipe et ses contrats | 💡 contrat | 🟡 non tranchée ; le nom suit les paiements (ADR-049, point 8) | la personne, son manager, Admin |
| T6 | Rémunération des chasseurs | calculer et payer la commission | ✅ obligation comptable (`REG:29`) | ✅ **10 ans** (`REG:29`, ADR-049) | le chasseur et son manager (`REGLES-CALCUL-REMUNERATION.md:296`), Admin ; ni Client ni Reader (`payment_router.py:43`) |
| T7 | Statistiques (OLAP) | piloter l'activité | 💡 intérêt légitime | 🟡 RGPD-12 | 🟡 qui lit le schéma `olap` ? |
| T8 | Recherche de biens (Elasticsearch) | chercher un bien vite | 💡 contrat | ✅ suit la base (index rempli chaque nuit, flux-15) | mêmes rôles que la lecture de `estate` (flux-14) |
| T9 | Logs de l'API | sécurité, diagnostic | 💡 intérêt légitime | 🟡 RGPD-11 | 🟡 compte Kibana à définir |
| T10 | Chasseur IA | proposer des biens sans chasseur humain | 💡 contrat | — | droits réduits (ADR-058, 💡 proposé) |

**Hors registre, à dire en une ligne**

- ✅ Le **seed de démo** et le faker sont des données inventées (ADR-055,
  ADR-046) : pas de personne réelle, pas de traitement RGPD.
- 💡 Les données reprises du sujet (CSV, `PgSQL.sql`) sont aussi des données
  d'exercice. Le registre décrit ce que ferait la **vraie** agence.

---

## 5. Les droits des personnes

`REG:38` : « comment un client peut-il consulter, corriger ou faire effacer
ses données ? »

| Droit | Ce qui existe | Le trou |
|---|---|---|
| Consulter | `GET` sur « le sien » (matrice § 3) | 🟡 pas d'export de tout en une fois |
| Corriger | `PUT` sur sa fiche ; les champs gardés rendent `403` (matrice § 3) | — |
| Effacer | `POST /users/{id}/anonymize`, Admin, sur demande (ADR-049) | 🟡 la date de la demande n'est pas gardée (`deactivated_at`, `anonymized_at` : ADR-049, Conséquences, non codé) |
| Être informé | rien : pas de front | 💡 le vendeur (T4) ne nous a rien donné lui-même : 🟡 RGPD-15 |

💡 La liste complète des droits (opposition, limitation, portabilité…) est à
**relire sur cnil.fr** pendant le chantier : non vérifiée ici.

---

## 6. La note souveraineté & IA, en plan

Le modèle du sujet pose trois questions (`SOU`, § « Les trois questions »).

1. **Périmètre** — qui voit quoi ?
   - ✅ Une IA ne reçoit pas le rôle Reader : elle lit l'OLAP anonymisé
     (ADR-027, l. 146 et 165).
   - 💡 Le chasseur IA : droits réduits, jamais `estate_contact` (ADR-058, proposé).
2. **Masquage** — quoi retirer avant l'IA ?
   - ✅ L'OLAP n'a ni nom, ni e-mail, ni téléphone, ni adresse
     (`08_olap.sql:54-57`).
   - ⚠️ Il garde `id_client` et `id_hunter` (`08_olap.sql:91`, `:100`) : une
     clé de retour vers la base. C'est une **pseudonymisation**, pas une
     anonymisation (`SOU`, § 2). À dire, ou à changer (🟡 RGPD-13).
3. **Localisation** — où tourne l'IA ?
   - 🟡 Rien n'est écrit. Quel modèle, quel serveur, quel pays ? (RGPD-17)
   - Le sujet cite une démo « Tabularis + Claude » du cours (`SOU`, ligne 3).
4. **Journalisation** (`SOU`, méthode, point 5) : les logs de FLX10.

---

## 7. Les limites, à dire à l'oral

Toutes viennent d'ADR-049, § Conséquences.

- ⚠️ **Plus proche d'une pseudonymisation** : la vente garde l'adresse du
  bien, la date et le prix. En les croisant, on peut retrouver la personne.
- ⚠️ **Textes libres** : un chasseur peut citer le client par son nom ; un
  programme ne sait pas les trier.
- ⚠️ **`is_activated` a deux sens** : compte pas encore fini, ou compte
  désactivé.
- ✅ **`fil_rouge_reader` : la limite d'ADR-049 est réglée depuis.** Il ne
  lit plus ni les comptes désactivés, ni les paiements, ni le mot de passe,
  ni le contact du vendeur (fiches DRO8, DRO9 ;
  `md/securite/matrice-droits-crud-par-role.md:140-147`).

---

## 8. Questions pour l'équipe 🟡

**Comment les poser** (demandé par Sébastien le 2026-10-15 : « plein de
questions », « très compréhensible pour tout le monde, il y a des
débutants ») :

- Au cadrage, sur Discord : **une question par message**, « Question n sur N ».
- Chaque question garde son **« 💬 En clair »** : le lexique du § 0 suffit
  pour la comprendre.
- Les options disent **ce qu'elles changent**, pas seulement leur nom.
- 💡 = le conseil de Claude ; il vaut ce qu'il vaut. Le groupe tranche.
- Les questions sont rangées **de la plus simple à la plus technique**.

### Pour s'organiser

**RGPD-1 — Qui s'occupe de la RGPD dans le groupe ?**

- 💬 En clair : quelqu'un doit relire le registre et le présenter à l'oral.
- A — une personne pilote, les autres relisent.
- B — à deux : un qui écrit, un qui présente.
- C — tout le groupe, chacun une partie.
- 💡 B : à l'oral, le jury peut interroger n'importe qui (`TRAME-SOUTENANCE.md:21`).

**RGPD-2 — Où ranger le registre et la note IA ?**

- 💬 En clair : ce sont deux documents à rendre. Il faut un endroit fixe.
- A — un nouveau dossier `livrables/5-transverse/`.
- B — dans `livrables/2-modelisation/`, à côté du modèle de données.
- C — dans `md/securite/`, avec la matrice des droits.
- 💡 A : le sujet range la RGPD dans les exigences « transverses »
  (`SP/Readme.md:264`), à côté de l'accessibilité et de l'éco-conception.

**RGPD-3 — En quel format ?**

- 💬 En clair : un fichier dans le dépôt, une page sur Confluence, ou les deux.
- A — un fichier `.md` dans le dépôt, copié sur Confluence à la fin.
- B — Confluence seul.
- 💡 A : comme les ADR, le dépôt garde l'historique.

### Pour comprendre notre histoire

**RGPD-4 — Au nom de qui écrit-on le registre ?**

- 💬 En clair : le registre est tenu par l'entreprise qui garde les données.
  Chez nous, c'est l'agence de chasse immobilière du sujet, pas l'école.
- A — au nom de l'agence du sujet, comme si elle existait.
- B — au nom du groupe, comme un exercice.
- 💡 A : le jury attend un registre « comme en vrai ».

**RGPD-5 — Nos données sont inventées : on le dit ?**

- 💬 En clair : le seed de démo et le faker inventent des personnes
  (ADR-055). La loi ne s'applique qu'à de vraies personnes.
- A — oui, en une ligne : « le registre décrit ce que ferait la vraie agence ».
- B — non, on fait comme si tout était vrai.
- 💡 A : c'est honnête, et ça montre qu'on sait faire la différence.

### Pour les données qu'on garde

**RGPD-6 — Genre, date de naissance, mariage, PACS, enfants : on les garde ?**

- 💬 En clair : la règle est de ne garder que le nécessaire (§ 0,
  minimisation). Ces 5 colonnes de `client` viennent du sujet. Servent-elles
  à trouver un bien ?
- A — on les garde, et on écrit à quoi elles servent (exemple : le nombre
  d'enfants aide à choisir le nombre de chambres).
- B — on les retire du schéma.
- C — on les garde, mais facultatives et jamais dans l'OLAP.
- 💡 A ou C : B change le schéma, l'API et les tests.

**RGPD-7 — L'adresse précise d'un bien : donnée personnelle ou pas ?**

- 💬 En clair : un bien a une rue, un numéro, et sa position GPS
  (`estate.street`, `street_number`, `latitude`, `longitude`). Avec
  l'adresse, on peut retrouver le vendeur.
- A — oui : on l'écrit dans le registre, et on la garde hors de l'OLAP
  (déjà le cas : `dim_secteur` n'a que pays, code postal, ville).
- B — non : un bien n'est pas une personne.
- 💡 A, par prudence.

**RGPD-8 — Les textes libres : que fait-on ?**

- 💬 En clair : un chasseur peut écrire « M. Dupont est pressé » dans un
  commentaire. Un programme ne sait pas trouver ce nom pour l'effacer.
- A — on garde la limite, et on la dit à l'oral (ADR-049).
- B — on ajoute une consigne aux chasseurs : jamais de nom dans un commentaire.
- C — A et B.
- 💡 C.

**RGPD-9 — Les photos des biens : une règle ?**

- 💬 En clair : une photo peut montrer une personne, ou une plaque de rue.
- A — une consigne : jamais de personne sur une photo.
- B — rien, hors périmètre : l'API n'envoie aucun fichier vers MinIO.
- 💡 A, en une ligne du registre.

### Pour les durées

**RGPD-10 — Un compte jamais utilisé : on le garde combien de temps ?**

- 💬 En clair : un client crée son compte, puis ne revient jamais. Le sujet
  dit « tant que le compte est actif » (`REG:28`), sans dire quand un compte
  « dort ».
- A — 2 ans sans connexion, puis anonymisé (piste de la CNIL, citée par
  ADR-049).
- B — pas de limite : seulement sur demande.
- 💡 A. ⚠️ Il faudrait alors la date de dernière connexion, qui n'existe
  pas en base : du code en plus.

**RGPD-11 — Les logs de l'API : combien de temps ?**

- 💬 En clair : les logs notent chaque appel à l'API (FLX10). Ils servent à
  trouver une panne ou une attaque. Ils ne contiennent ni mot de passe ni
  e-mail.
- A — une durée fixe, à chercher sur cnil.fr pendant le chantier.
- B — on ne fixe rien : le projet n'est pas en production.
- 💡 A : une seule recherche, et la réponse est prête pour l'oral.

**RGPD-12 — L'OLAP : combien de temps ?**

- 💬 En clair : l'OLAP sert aux statistiques. Il n'a pas de nom, mais il
  garde des numéros de client et de chasseur.
- A — aussi longtemps que la vente (10 ans).
- B — sans limite, s'il devient vraiment anonyme (voir RGPD-13).
- 💡 A tant que les numéros restent.

### Pour la technique

**RGPD-13 — Dans l'OLAP, on garde `id_client` et `id_hunter` ?**

- 💬 En clair : avec ces numéros, on peut revenir à la fiche du client
  dans la base. C'est donc de la **pseudonymisation**, pas de
  l'anonymisation (§ 0).
- A — on les garde, et on le dit (les statistiques par chasseur en ont besoin).
- B — on les remplace par un code sans retour possible.
- 💡 A : B casse les statistiques par chasseur, et FLX5 est déjà écrit.

**RGPD-14 — Garder la date de la demande d'effacement ?**

- 💬 En clair : quand un client demande l'effacement, rien ne note **quand**
  on l'a fait. Une date le prouverait (`deactivated_at`, `anonymized_at`,
  ADR-049).
- A — oui : une fiche de code à part (`RGP5`).
- B — plus tard, en V2.
- 💡 A si le temps le permet : c'est une preuve facile à montrer.

**RGPD-15 — Le vendeur doit-il savoir qu'on garde son contact ?**

- 💬 En clair : le client nous donne ses données lui-même. Le vendeur, non :
  on les prend dans une annonce. La loi demande sans doute de le prévenir.
- A — on le vérifie sur cnil.fr, puis on l'écrit dans le registre.
- B — hors périmètre : pas de mail dans le projet.
- 💡 A, au moins pour le dire à l'oral. ⚠️ Non vérifié : à chercher.

**RGPD-16 — Les bases légales du § 4 : on les valide comment ?**

- 💬 En clair : pour chaque traitement, il faut dire quelle raison nous
  autorise à garder la donnée (§ 0). Claude en a proposé une par ligne.
- A — le groupe les relit une à une.
- B — on les montre à Jeff (client), en plus.
- 💡 B pour celles qui ne viennent pas du modèle du sujet (T4, T7, T9).

### Pour l'IA

**RGPD-17 — Quelle IA, et où tourne-t-elle ?**

- 💬 En clair : si on envoie des données à une IA, elles partent sur un
  serveur. Dans quel pays ? Le sujet demande de le dire (`SOU`, § 3).
- A — on choisit un outil, et on écrit où il tourne.
- B — aucun choix fait : on écrit les critères (Europe, lecture seule, OLAP).
- 💡 B : l'appli du chasseur IA est hors périmètre (ADR-058, Contexte).

**RGPD-18 — Le chasseur IA : on attend ADR-058 ?**

- 💬 En clair : ADR-058 dit ce que le chasseur IA a le droit de faire. Il
  est seulement proposé. La note IA en dépend.
- A — on accepte ADR-058 d'abord, puis on écrit la note.
- B — on écrit la note avec « proposé », et on la met à jour ensuite.
- 💡 A : une note qui cite un ADR non accepté devra être réécrite.

---

## 9. Découpage proposé 💡

Code de fiche proposé : `RGP` (libre au 2026-10-15).

| Fiche | Titre | Dépend de |
|---|---|---|
| `RGP1` | Recompter l'inventaire des données personnelles | FLX clos |
| `RGP2` | Écrire le registre des traitements | `RGP1` |
| `RGP3` | Écrire les droits des personnes et les limites | `RGP2` |
| `RGP4` | Écrire la note souveraineté & IA | `RGP2`, ADR-058 accepté |
| `RGP5` | (option) Dater la désactivation et l'anonymisation | RGPD-14 = oui |

- **Avant `RGP1` : les 18 questions du § 8**, posées à l'équipe. Une fiche
  ne devine pas une réponse : elle s'arrête et demande.
- **Attendre la fin de FLX** : le registre décrit l'OLAP, l'index et les
  logs, qui sont encore en cours.
- **Coût** : 4 fiches, 5 avec l'option. Repère : **5,15 $/fiche** au chantier
  API (61,74 $ pour 12 fiches, `context AI/11-api-auth-rgpd-regles.md:17`).
  Des fiches d'écriture coûtent sans doute moins : à mesurer.
- `RGP1` recompte par grep, avec le compte brut : l'inventaire du § 3 date du
  15/10 et le schéma aura bougé.

---

## Sources

| Affirmation | Source |
|---|---|
| Registre exigé, « pas optionnel » | `SP/Readme.md:266`, `:270` |
| Modèle du registre, vocabulaire, minimisation, droits | `REG:9`, `:13-14`, `:23`, `:27-29`, `:34-40` |
| Note souveraineté IA | `SP/Readme.md:282` ; `SOU` |
| Case de la grille ; temps à l'oral | `GRILLE-EVALUATION.md:96` ; `TRAME-SOUTENANCE.md:21` |
| Accès à la paie du chasseur | `SP/documents utiles/REGLES-CALCUL-REMUNERATION.md:296` |
| Effacement, durées, limites | `md/adr/adr-049-effacement-compte-desactiver-anonymiser.md` |
| Contact du vendeur | `md/adr/adr-054-contact-du-vendeur.md` |
| Chasseur IA | `md/adr/adr-058-droits-du-chasseur-ia.md` (proposé) |
| Une IA lit l'OLAP | `md/adr/adr-027-matrice-acces-par-role.md:146`, `:165` |
| Droits « le sien » | `md/securite/matrice-droits-crud-par-role.md` § 3 |
| Colonnes | `01` (Fil-Rouge-API, `main`, lu le 15/10/2026) |
| OLAP | `docker/init-v3/08_olap.sql:54-57`, `:91`, `:100` (FLX5, non poussé) |
| Logs | `../Fil-Rouge-flux/context AI/17-flux-donnees.md`, fiche FLX10 |
| Recherche, horaires | questions flux-14 et flux-15, tranchées le 15/10/2026 |

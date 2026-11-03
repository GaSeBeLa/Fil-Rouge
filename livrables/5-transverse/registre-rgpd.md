# Registre des traitements

Tenu au nom de **la société de chasse immobilière du sujet**, responsable
des traitements (RGPD-4). Le sujet ne lui donne pas de nom : « une société
de chasse immobilière » (`SP/Readme.md:71`).

> ⚠️ **Données inventées.** L'entreprise, ses données et ses personnages
> sont fictifs (`SP/Readme.md:13`) : le registre décrit ce que ferait la
> vraie agence (RGPD-5).

Écrit le 2026-11-03 (fiche RGP2, chantier RGP). Il part du registre de
Gabriel sur Confluence (page 44826725 « RGPD », modifiée le 22/09/2026) et
garde sa structure (RGPD-3). Il le complète par le brouillon du 15/10
(`md/securite/2026-10-15-preparation-chantier-rgpd.md`, § 4, T1 à T10) et
par l'inventaire recompté (`inventaire-donnees-personnelles.md`, RGP1).

Abréviations des sources :

- `REG` = `SP/documents utiles/REGISTRE-RGPD.md`, le modèle du sujet ;
- `SP` = le StarterPack du sujet, en lecture seule ;
- `RGPD-n` = une question tranchée le 2026-11-03 (Discord, Seb ; socle du
  chantier, `context AI/20-rgpd.md`) ;
- `01`, `08` = `docker/init-v3/01_…sql` et `08_olap.sql`, dans `Fil-Rouge-API`.

---

## 1. Le registre — 11 traitements

Une ligne par traitement, pas par table (`REG:23`). Les six premières sont
celles de Gabriel, dans son ordre ; les cinq suivantes sont neuves.

| # | Traitement | Finalité | Données personnelles concernées | Base légale | Durée de conservation | Qui y accède |
|---|---|---|---|---|---|---|
| 1 | Comptes utilisateurs | Authentifier les personnes sur la plateforme | `email`, `password` (haché), `is_activated`, `system_role` (`"user"`) | Exécution du contrat (`REG:28`) | Tant que le compte est actif (`REG:28`). Sur demande : désactivé, puis anonymisé (ADR-049). Compte dormant : effacé **sur demande seulement** (RGPD-10) ; 2 ans sans connexion = cible v2 | la personne, `Admin` ; `Reader` sans le mot de passe |
| 2 | Gestion du mandat de recherche | Exécuter le mandat entre le client et le chasseur | fiche `client` (nom, prénom, téléphone, adresse, pays, genre, date de naissance, mariage, PACS, enfants) ; demande et critères (`search_request`, `criteria` : budget, ville, quartier, souhaits) ; `mandate` ; biens proposés et avis du client (`estate_proposed`) | Exécution du contrat ; avant lui, la demande du client | **10 ans** après la fin du dernier mandat (décret n° 72-678, art. 72 ; ADR-049). Mandat jamais signé : anonymisé tout de suite (ADR-049, point 5) | le client (le sien), ses chasseurs, le manager de l'équipe, `Admin`, `Reader` |
| 3 | Gestion du personnel (chasseur / manager) | Gérer les collaborateurs et leurs habilitations | `hunter`, `real_estate_manager` : nom, prénom, téléphone, pays, genre, société, date d'embauche, niveau d'études, carte T, certification | Exécution du contrat de travail | Durée du contrat ; l'identité et la date d'embauche suivent les paiements : **10 ans** après le dernier (ADR-049, point 8) | le collaborateur lui-même, son manager, `Admin` |
| 4 | Rémunération et performance des chasseurs | Calculer et verser la rémunération, suivre la performance | `payment` (montants, taux, `performance_score`, `calculation_details`), `commission_scale`, `hunter_performance` (`score`), ventes (`sale`) | Exécution du contrat + obligation légale comptable (`REG:29`) | **10 ans** (obligation comptable, `REG:29` ; ADR-049) | le chasseur et son manager (`SP/…/REGLES-CALCUL-REMUNERATION.md:296`), `Admin` ; ni `Client` ni `Reader` (`payment_router.py:43`) |
| 5 | Suivi des visites et avis | Tracer le parcours de recherche (visites, avis rédigés) | `visit` (date, type de visiteur) ; avis du chasseur (`estate_searchrequest.review_hunter`, `review_media`) ; commentaires (`estate_proposed.comment_client`, `comment_hunter`) | Exécution du contrat | **10 ans** après la fin du mandat, comme le mandat (ADR-049). ⚠️ Textes libres : un nom écrit dedans ne s'efface pas par programme (RGPD-8, ADR-049) | le chasseur affecté, le client concerné, le manager, `Admin` |
| 6 | Prospection commerciale post-mandat | Envoyer des offres de services après la vente (`SP/Readme.md`, parcours particulier, étape 9) | nom, email | **Consentement** : le mandat est fini à ce stade | Jusqu'au retrait du consentement (registre de Gabriel, page 44826725). ⚠️ Aucun code ni table pour ce traitement dans `01` | service marketing / commercial |
| 7 | Contact du vendeur et adresse des biens | Joindre le vendeur d'un bien repéré | `estate_contact` (nom, téléphone, email, agence, particulier ou non) ; adresse du bien (`estate.street`, `street_number`, `latitude`, `longitude`, code postal, ville), donnée personnelle (RGPD-7) ; `estate.information` (texte libre) ; photos (`picture.url`) | Intérêt légitime : le vendeur n'a pas de contrat avec la société | Contact : **3 ans** après la dernière activité du bien, puis anonymisé (ADR-054, décision 4). Adresse : gardée avec le bien, sans durée votée (RGPD-7). Le vendeur est informé au **1er appel** du chasseur (RGPD-15, CNIL : au plus tard sous 1 mois) | contact : `Admin`, `Hunter`, `Manager` (`estate_contact_router.py:17`) ; pas `fil_rouge_reader` (ADR-054, décision 5) |
| 8 | Statistiques (OLAP) | Piloter l'activité | `olap.dim_client` (`id_client`, année d'inscription, ville, pays), `olap.dim_chasseur` (`id_hunter`, année d'embauche, IA ou non, carte T, pays), `fait_ventes` (montants, commission) — **pseudonymisées** : les numéros ramènent aux fiches (RGPD-13) | Intérêt légitime | **10 ans** (RGPD-12, vote du 03/11), comme les ventes | le DAG `olap_refresh` (écrit chaque nuit) ; pas `fil_rouge_reader` (`docker/init-v3/README.md:180`) |
| 9 | Recherche de biens (Elasticsearch) | Chercher un bien vite | copie des biens (`estate`), dont la ville et le quartier | Exécution du contrat | Suit la base : l'index se remplit chaque nuit (question flux-15, 15/10) | les mêmes rôles que la lecture de `estate` (question flux-14, 15/10) |
| 10 | Logs de l'API | Sécurité, diagnostic | chaque appel à l'API (FLX10) ; ni mot de passe ni email | Intérêt légitime | **6 mois** (RGPD-11, vote du 03/11, recommandation CNIL) | 🟡 le compte Kibana reste à définir |
| 11 | Chasseur IA | Proposer des biens sans chasseur humain | les données des traitements 2 et 5, lues par un compte `hunter` à `is_hunter_ai` vrai | Exécution du contrat | Suit les traitements 2 et 5. v1 : **aucun LLM**, tout en local (RGPD-17) | droits réduits, ADR-058 **proposé**, pas accepté (RGPD-18) |

Compte : **11** traitements, pour **6** lignes sur la page de Gabriel.

---

## 2. À quoi servent les 5 colonnes de `client` (RGPD-6)

Les cinq sont **gardées**. La minimisation demande d'écrire pourquoi
(`REG:36`). ✅ Usages validés par le groupe le 2026-11-03 (E13) :

| Colonne | Usage dans la chasse |
|---|---|
| `gender` | la civilité pour s'adresser au client |
| `birth_date` | vérifier que le client est majeur avant de signer un mandat |
| `is_married` | un couple marié achète souvent à deux : le mandat et l'offre en tiennent compte |
| `is_civil_solidarity_pact` | même raison pour un couple pacsé |
| `nb_children` | aider à choisir le nombre de chambres |

- ✅ Aucune n'entre dans l'OLAP : `dim_client` n'a que `id_client`,
  `annee_inscription`, `ville`, `pays` (`08_olap.sql:98-103`, RGP1 § 5).
- ✅ Aucune donnée sensible au sens du sujet (`REG:14`) : RGP1 § 3.

---

## 3. Hors registre

- ✅ Le **seed de démo** et le faker sont des données inventées (ADR-055,
  ADR-046) : pas de personne réelle.
- ✅ Les dates d'effacement (`deactivated_at`, `anonymized_at`) sont une
  cible **v2**, pas de code (RGPD-14).

---

## 4. Écart avec Confluence

Ce qu'il faudrait changer sur la page 44826725 de Gabriel. Rien n'est écrit
sur Confluence : le groupe décide (règle du projet, `CLAUDE.md`).

| # | Ligne de la page | Ce qu'elle dit | Proposition |
|---|---|---|---|
| E1 | (en tête) | — | Ajouter : « tenu au nom de la société du sujet » (RGPD-4) et « données inventées » (RGPD-5) |
| E2 | Comptes utilisateurs | « Tant que le compte est actif » ; accès « La personne elle-même, `Admin` » | Ajouter : compte dormant effacé sur demande seulement (RGPD-10), anonymisation ADR-049 ; accès : `Reader` sans le mot de passe |
| E3 | Gestion du mandat de recherche | « Durée du mandat + [à valider] » ; accès « Chasseur affecté, manager » | Durée : **10 ans** après la fin du dernier mandat (décret 72-678, art. 72 ; ADR-049). Données : ajouter email, pays, genre, PACS, enfants, critères. Accès : ajouter le client, `Admin`, `Reader` |
| E4 | Gestion du personnel | « Durée du contrat + [à valider] » ; accès « RH / direction » | Durée : identité **10 ans** après le dernier paiement (ADR-049, point 8). Accès : son manager, `Admin` (les rôles du code) |
| E5 | Rémunération et performance | accès « comptabilité » | Accès : le chasseur, son manager, `Admin` ; ni `Client` ni `Reader` (`payment_router.py:43`) |
| E6 | Suivi des visites et avis | « Durée du mandat » | Durée : **10 ans** après la fin du mandat (ADR-049). Ajouter : la limite des textes libres (RGPD-8) |
| E7 | Prospection commerciale | consentement, « jusqu'au retrait » | Garder ; ajouter : aucun code ni table pour ce traitement |
| E8 | — | — | Ajouter la ligne 7 : contact du vendeur et adresse des biens (ADR-054, RGPD-7, RGPD-15) |
| E9 | — | — | Ajouter la ligne 8 : statistiques OLAP, 10 ans, pseudonymisées (RGPD-12, RGPD-13) |
| E10 | — | — | Ajouter la ligne 9 : recherche Elasticsearch |
| E11 | — | — | Ajouter la ligne 10 : logs de l'API, 6 mois (RGPD-11) |
| E12 | — | — | Ajouter la ligne 11 : chasseur IA, aucun LLM en v1 (RGPD-17, ADR-058 proposé) |
| E13 | — | — | Ajouter la section « À quoi servent les 5 colonnes de `client` » (RGPD-6) |

🟡 **Bases légales à relire par le groupe** (RGPD-16, sans Jeff) : surtout
les lignes 7, 8 et 10 (intérêt légitime), qui ne viennent pas du modèle du
sujet. Demande envoyée sur Discord (fiche RGP2) ; « relues » cliqué par
Seb le 2026-11-03.

✅ **Validé par le groupe le 2026-11-03** : E1 à E13 et les bases légales
(Seb par ses clics ; Gabriel et Laurence, rapporté par Seb sur Discord).
Reporté sur Confluence le 2026-11-03 (page 44826725, version 2).

---

## 5. Droits des personnes

La liste vient de la CNIL : [« Les droits pour maîtriser vos données
personnelles »](https://www.cnil.fr/fr/mes-demarches/les-droits-pour-maitriser-vos-donnees-personnelles)
(doc officielle, lue le 2026-11-03 ; la page n'affiche pas de date). Elle
compte **9 droits**, dans cet ordre. La question du sujet : « comment un
client peut-il consulter, corriger ou faire effacer ses données ? »
(`REG:38`).

Les routes et les rôles viennent de `md/securite/matrice-droits-crud-par-role.md`
§ 3 et du code (`Fil-Rouge-API`, `API/src/app/routes/`).

| # | Droit (titre CNIL) | Ce que l'API offre | Le trou |
|---|---|---|---|
| 1 | Rester informé | rien dans l'API : pas de front. Vendeur : consigne 3 ci-dessous (RGPD-15) | 🟡 aucune mention d'information affichée au client |
| 2 | Vous opposer | prospection (registre, ligne 6) : sous consentement, donc retirable | 🟡 aucune route pour noter une opposition ; l'`Admin` la traite à la main |
| 3 | Vérifier vos données (accès) | `GET /auth/me` (`auth_router.py:83`) ; `GET` sur « le sien », table par table, pour `Client`, `Hunter`, `Manager` (matrice § 3) | 🟡 pas d'export de tout en une fois |
| 4 | Rectifier vos données | `PUT` sur sa fiche et `PUT /users` sur son compte, avec « le sien » ; rôle et activation gardés → `403` (matrice § 3) | — |
| 5 | Déréférencer un contenu | sans objet : l'API n'est indexée par aucun moteur de recherche public | — |
| 6 | Effacer vos données | `POST /users/{id}/anonymize`, `Admin`, sur demande (`user_router.py:46`, ADR-049) ; contact du vendeur : `POST /estate-contacts/anonymize-expired`, `Admin` (ADR-054). Aucune route `DELETE` (matrice § 3) | 🟡 la date de la demande n'est pas gardée (RGPD-14) ; ce qu'une loi impose reste 10 ans (registre, lignes 2 à 4) |
| 7 | Emporter vos données (portabilité) | les `GET` du droit 3, en JSON | 🟡 pas d'export d'un seul tenant |
| 8 | Demander une intervention humaine | la rémunération est calculée par la machine, mais lancée par l'`Admin` (matrice § 3, point 10) ; les biens suggérés (`suggested`) ne vont au client qu'une fois gardés par un chasseur (`kept`, SUG4) | 💡 la note du chasseur (`hunter_performance.score`) est automatique : le recours passe par son manager, à la main |
| 9 | Geler l'utilisation de vos données (limitation) | désactiver le compte (`is_activated`) : son profil n'est plus lu que par l'`Admin` (matrice § 3, fiche DRO8) | ⚠️ désactivé ne dit pas pourquoi (voir les limites) |

Compte : **9** lignes, pour **9** droits sur la page CNIL.

### Les trois consignes

1. **Jamais de nom dans un texte libre** (RGPD-8). Un commentaire, un avis
   ou une note (`comment_client`, `comment_hunter`, `review_hunter`,
   `estate.information`, `criteria.change_reason`) ne cite personne par son
   nom.
2. **Jamais de personne sur une photo** (RGPD-9). Une photo de bien
   (`picture`) ne montre ni un occupant ni un visage.
3. **Au premier appel, le chasseur informe le vendeur** (RGPD-15,
   ADR-054). Il lui dit d'où vient son contact (l'annonce qu'il a publiée)
   et qu'on le garde **3 ans** après la dernière activité du bien. La CNIL
   demande d'informer « au plus tard, dans le délai d'1 mois »
   ([cnil.fr](https://cnil.fr/fr/cnil-direct/question/reglement-europeen-quand-informer-les-personnes-concernees-par-un-fichier),
   lu le 2026-11-03, socle du chantier).

---

## 6. Limites

À dire à l'oral. Elles viennent d'ADR-049, § Conséquences, sauf mention.

- ⚠️ **Une pseudonymisation, pas une anonymisation.** Un compte effacé
  laisse sa vente : l'adresse du bien, la date et le prix. En les croisant,
  on peut retrouver la personne. L'OLAP garde aussi `id_client` et
  `id_hunter` (`08_olap.sql:91`, `:100`) : les numéros ramènent aux fiches
  (RGPD-13).
- ⚠️ **Les textes libres.** Un programme ne sait pas trouver un nom écrit
  dans un commentaire pour l'effacer : la consigne 1 est la seule garde
  (RGPD-8).
- ⚠️ **`is_activated` a deux sens.** Faux veut dire « compte pas encore
  fini » ou « compte désactivé, peut-être effacé » ; rien ne les distingue
  (matrice § 3, « Écarts qui restent »).
- ⚠️ **Les comptes dormants** (RGPD-10). Un compte jamais utilisé n'est
  effacé que **sur demande**. La cible v2 : 2 ans sans connexion, puis
  anonymisé ; il faudrait d'abord la date de dernière connexion, absente de
  la base.
- ⚠️ **La date d'effacement** (RGPD-14). Rien ne note quand un compte a été
  désactivé ou anonymisé (`deactivated_at`, `anonymized_at`) : remis en
  **v2**, sans code.
- ✅ **`fil_rouge_reader`** ne lit plus ni les comptes désactivés, ni les
  paiements, ni le mot de passe, ni le contact du vendeur (fiches DRO8,
  DRO9 ; matrice § 3) : la limite d'ADR-049 est réglée.

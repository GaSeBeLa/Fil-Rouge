> **QUAND LIRE** : on joue une fiche `RGP*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache RGP<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier RGP — RGPD : registre, droits et note souveraineté IA

**Ouvert.** le 2026-11-03.

**À quoi il sert.** Le sujet exige un registre de traitement et une note
souveraineté & IA (« pas optionnel », `SP/Readme.md:266`) : ce chantier les écrit.

**Fait.** Rien. Ouvert le 2026-11-03, cadré en 4 fiches d'écriture, `RGP1` à jouer.

**Session** : 812d8351-8578-4762-9a91-978550768445

## Le socle commun

**Matière** : `md/securite/2026-10-15-preparation-chantier-rgpd.md` (§ 3
inventaire, § 4 registre en brouillon, § 5 droits, § 6 note IA, § 7 limites).
Elle date du 15/10 : tout chiffre s'y recompte, rien ne s'y recopie sans grep.

**Les 18 questions sont tranchées** (Discord, 2026-11-03, Seb ; votes de
Gabriel et d'amethyste2004 notés sur les messages). Le numéro renvoie au § 8.

| Q | Réponse |
|---|---|
| RGPD-1 | RACI proposé (`md/equipe/raci-propositions.md`) : registre R Gabriel, A Laurence ; note IA R Laurence, A Gabriel |
| RGPD-2 | copie dépôt dans **`livrables/5-transverse/`** |
| RGPD-3 | on part du **registre de Gabriel** sur Confluence, on le complète |
| RGPD-4 | écrit **au nom de l'agence** du sujet |
| RGPD-5 | une ligne : « le registre décrit ce que ferait la vraie agence » (données inventées) |
| RGPD-6 | genre, naissance, mariage, PACS, enfants **gardés**, et leur usage écrit |
| RGPD-7 | l'adresse d'un bien **est** une donnée personnelle, hors OLAP |
| RGPD-8 | textes libres : limite dite à l'oral **et** consigne « jamais de nom » |
| RGPD-9 | photos : consigne « jamais de personne » |
| RGPD-10 | compte dormant : effacé **sur demande seulement**, limite dite ; 2 ans = cible v2 |
| RGPD-11 | logs gardés **6 mois** (vote du 03/11, CNIL) |
| RGPD-12 | OLAP gardé **10 ans** |
| RGPD-13 | `id_client`, `id_hunter` gardés dans l'OLAP : **pseudonymisation** dite |
| RGPD-14 | date d'effacement (`deactivated_at`, `anonymized_at`) : **v2**, pas de code |
| RGPD-15 | vendeur informé au **1er appel** du chasseur (CNIL : « au plus tard, dans le délai d'1 mois », [cnil.fr](https://cnil.fr/fr/cnil-direct/question/reglement-europeen-quand-informer-les-personnes-concernees-par-un-fichier), lu le 03/11) |
| RGPD-16 | bases légales relues **par le groupe**, sans Jeff |
| RGPD-17 | v1 : aucun LLM, tout en local ; v2 ouverte (`md/securite/note-souverainete-securite-ia.md`) |
| RGPD-18 | ADR-058 reste **proposé** : la note le cite comme tel |

**Confluence** (espace `GaSeBeLa1`, site `laurenceamethyste.atlassian.net`) :
registre de Gabriel = page **44826725** « RGPD » ; note IA en brouillon = page
**63438854**. Lecture libre ; **aucune écriture sans un clic de Seb sur Discord**
(salon 1559859075947175976) : la fiche propose le texte, elle n'écrit pas.

**Schéma** : `../Fil-Rouge-API/docker/init-v3/01_create_fil_rouge_immobilier.sql`
(22 tables) et `08_olap.sql` ; on lit par grep, on ne modifie rien.

**Dehors** : aucun code, aucune migration, aucun test (RGPD-6, 10, 13, 14) ;
les deux StarterPack en lecture seule ; aucun ADR créé ni réécrit.

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `RGP1` | Recompter l'inventaire des données personnelles | rien |
| `RGP2` | Écrire le registre des traitements | `RGP1` |
| `RGP3` | Écrire les droits, les consignes et les limites | `RGP2` |
| `RGP4` | Écrire la note souveraineté & IA | `RGP2` |

`RGP3` et `RGP4` se jouent dans n'importe quel ordre une fois `RGP2` faite.

---

<!-- FICHE:RGP1 -->
## RGP1 [x] — Recompter l'inventaire des données personnelles

**Session** : 5e8e0bd7-7c11-4e35-8104-73f5c1d4c279
**Dépend de** : rien.
**Fichiers** : `../Fil-Rouge-API/docker/init-v3/01_create_fil_rouge_immobilier.sql`,
`../Fil-Rouge-API/docker/init-v3/08_olap.sql`, la matière § 3 ; écrit
`livrables/5-transverse/inventaire-donnees-personnelles.md` — et rien d'autre.

**Prompt**
Refais l'inventaire du § 3 sur le schéma du jour. Compte les tables par grep
(`CREATE TABLE`) et affiche le compte brut (22 attendu). Pour chaque table,
liste les colonnes qui désignent une personne ou s'y rattachent, au format du
§ 3 (les personnes / liées à une personne / sensibles). Note à part ce qui a
changé depuis le 15/10, en particulier les colonnes ajoutées par FLX et SUG
dans `estate_searchrequest` et `estate_proposed`. Vérifie par grep que
l'OLAP n'a ni rue, ni numéro, ni latitude, ni longitude (RGPD-7), et relève
les lignes `id_client`, `id_hunter` (RGPD-13). Chaque ligne cite sa table ;
chaque compte s'affiche brut à côté de son verdict.

**Critère de fin**
Le fichier existe ; `grep -c "CREATE TABLE"` sur `01` et le nombre de tables
du fichier concordent (comptes affichés) ; une section « Changé depuis le
15/10 » liste au moins les colonnes neuves des deux tables nommées, ou dit
« aucune » avec le grep qui le prouve.
<!-- /FICHE -->

---

<!-- FICHE:RGP2 -->
## RGP2 [x] — Écrire le registre des traitements

**Session** : 5e8e0bd7-7c11-4e35-8104-73f5c1d4c279
**Dépend de** : `RGP1`.
**Fichiers** : Confluence page 44826725 (lecture), la matière § 4,
`livrables/5-transverse/inventaire-donnees-personnelles.md` ; écrit
`livrables/5-transverse/registre-rgpd.md` — et rien d'autre.

**Prompt**
Lis le registre de Gabriel (page 44826725) et garde sa structure. Compare-le
ligne à ligne au brouillon du § 4 (T1 à T10) et à l'inventaire de `RGP1`.
Écris le registre complet au nom de l'agence (RGPD-4), avec la ligne
« données inventées » (RGPD-5) : finalité, données, base légale, durée, qui
accède. Applique les réponses du socle : logs 6 mois, OLAP 10 ans,
pseudonymisation de l'OLAP, comptes dormants sur demande, usage des 5
colonnes de `client`, adresse du bien. Chaque durée cite sa source (ADR,
`REG:`, vote). Termine par une section « Écart avec Confluence » : ce qu'il
faut ajouter ou changer sur la page de Gabriel, ligne par ligne. Envoie cet
écart sur Discord, avec un bouton par proposition, et demande au groupe de
relire les bases légales (RGPD-16). N'écris rien sur Confluence.

**Critère de fin**
Le fichier existe et compte une ligne par traitement (nombre affiché, ≥ les
lignes de la page 44826725) ; chaque durée a sa source ; la section « Écart
avec Confluence » existe ; le message Discord de relecture est envoyé (son id
recopié dans le compte rendu).
<!-- /FICHE -->

---

<!-- FICHE:RGP3 -->
## RGP3 [x] — Écrire les droits, les consignes et les limites

**Session** : 5e8e0bd7-7c11-4e35-8104-73f5c1d4c279
**Dépend de** : `RGP2`.
**Fichiers** : la matière § 5 et § 7, `md/securite/matrice-droits-crud-par-role.md`
§ 3, `livrables/5-transverse/registre-rgpd.md` ; écrit une section « Droits
des personnes » et une section « Limites » dans ce registre — et rien d'autre.

**Prompt**
Relis sur cnil.fr la liste complète des droits (accès, rectification,
effacement, opposition, limitation, portabilité, information) : une
recherche, lien et date recopiés. Pour chaque droit, dis ce que l'API offre
(route et rôle, depuis la matrice) et le trou s'il y en a. Écris les trois
consignes : jamais de nom dans un texte libre (RGPD-8), jamais de personne
sur une photo (RGPD-9), au 1er appel le chasseur dit au vendeur d'où vient
son contact et qu'on le garde 3 ans (RGPD-15, ADR-054). Écris les limites à
dire à l'oral : pseudonymisation (vente, OLAP), textes libres, `is_activated`
à deux sens, comptes dormants et date d'effacement remis en v2 (RGPD-10, 14).

**Critère de fin**
Les deux sections existent ; chaque droit de la liste CNIL a sa ligne (compte
affiché, égal au nombre de droits de la page lue) ; les 3 consignes et les
limites RGPD-10 et RGPD-14 y figurent (grep de « RGPD-10 », « RGPD-14 »).
<!-- /FICHE -->

---

<!-- FICHE:RGP4 -->
## RGP4 [x] — Écrire la note souveraineté & IA

**Session** : 5e8e0bd7-7c11-4e35-8104-73f5c1d4c279
**Dépend de** : `RGP2`.
**Fichiers** : Confluence page 63438854 (lecture),
`md/securite/note-souverainete-securite-ia.md`, la matière § 6 ; écrit
`livrables/5-transverse/note-souverainete-securite-ia.md` — et rien d'autre.

**Prompt**
Pars du brouillon Confluence 63438854 et de sa source dans `md/securite/`.
Garde les trois questions du modèle (`SOU`) : périmètre, masquage,
localisation, et la journalisation. Mets-le d'accord avec le registre de
`RGP2` : OLAP pseudonymisé (RGPD-13), logs 6 mois (RGPD-11), v1 sans LLM et
tout en local, v2 ouverte (RGPD-17), ADR-058 cité « proposé » (RGPD-18).
Garde le format d'une page (`GRILLE-EVALUATION.md:38`). Dis dans
`md/securite/note-souverainete-securite-ia.md` qu'elle est remplacée par la
copie de `livrables/5-transverse/`. Envoie sur Discord l'écart avec la page
63438854, un bouton par proposition, pour Laurence (R) et Gabriel (A).
N'écris rien sur Confluence.

**Critère de fin**
Le fichier existe ; il répond aux trois questions (trois titres, grep) ;
aucune durée ne contredit le registre (grep de « 6 mois » et « 10 ans » dans
les deux fichiers, comptes affichés) ; le message Discord est envoyé (id
recopié).
<!-- /FICHE -->

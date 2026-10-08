# Notes pour la séance de rédaction des ADR — 2026-10-08 (soir)

- 📋 **But de la séance** : rédiger tous les ADR qui manquent, avec relecteurs et arbitre (demandé par Sébastien sur Discord, 2026-10-08 14:28).
- ✏️ **Notes prises par Claude** pendant la journée du 2026-10-08, d'après les échanges Discord et les fichiers du dépôt.
- ⚠️ Ce sont des **notes**, pas des ADR. Les numéros 028 à 049 sont une **proposition**.
- 🟡 = pas tranché · ✅ = source montrée · 💡 = avis de Claude

## 1. Où on en est

| Sujet | État | Où |
|---|---|---|
| 27 ADR existants rangés en pages Confluence | ✅ fait : 21 dans « Accepté », 1 dans « Proposé » (ADR-027) | espace GaSeBeLa |
| ADR-004, 024, 025 | ✅ dans le dossier « Annulé / Remplacé » | Confluence |
| ADR-016 et ADR-026 | ✅ **remis en vigueur** le 08/10 (Laurence, pour le groupe) ; statut complété, texte d'origine gardé ; sortis de « Annulé / Remplacé » | Confluence |
| Liste des ADR à écrire | ✅ regroupée de 28 à 23 sujets (accord de principe de Sébastien) | `md/adr/2026-10-08-proposition-regroupement-adr.md` |
| ADR-028 (authentification côté back) | ✅ brouillon écrit, **6 questions ouvertes** | `md/adr/adr-028-authentification-outils-cote-back.md` |
| Rien d'autre n'est rédigé | ❌ | |

⚠️ Je n'ai relancé aucun comptage sur Confluence après les créations (la recherche avait du retard d'indexation).

## 2. Décisions prises aujourd'hui

| # | Décision | Qui | Conséquence pour les ADR |
|---|---|---|---|
| 1 | ADR-016 et ADR-026 **remis en vigueur** | Laurence, au nom du groupe | ADR-028 les **complète**, il ne les remplace pas |
| 2 | `'renewed'` = statut de l'**ancien** mandat ; le nouveau pointe vers le précédent | Gabriel, au nom du groupe (« on veut ») | **Remplace ADR-010 et ADR-013** et la décision D8 (« renewed = le nouveau ») |
| 3 | **Pas d'avenants** | Gabriel (« on veut pas des avenants ») | `id_mandate_parent` reste `UNIQUE`. ADR-013 prévoyait les avenants : à dire noir sur blanc |
| 4 | Les 5 regroupements de la liste (I+Q, K→D, AC→U, AA+AB→ADR-027, Eircode→N) | accord de principe de Sébastien | 🟡 **à faire relire par le groupe** |
| 5 | Seed des 3 tables de paramètres, et service qui les lit | Sébastien (« oui pour le seed », « fais le service ») | Matière pour l'ADR D (paramètres en table datée) |

- ✅ Décisions 2 et 3 appliquées dans le code : commit `6be4e56` (SQL v3, test, docs).
- ⚠️ Sources de 2 et 3 : des messages Discord. Aucune trace écrite ailleurs.

## 3. Ce que le code dit déjà (à citer dans les ADR)

- ✅ **Exclusivité du mandat** : un trigger, `trg_mandate_exclusivity` (`docker/init-v3/01_create_fil_rouge_immobilier.sql:522-550`).
  - Un `EXCLUDE` ne sait pas dire « si l'un des deux est exclusif » (commentaire l. 500-507).
  - Un mandat `canceled` libère le client tout de suite (Q-MAN-02, Q-JEF-06).
  - 🟡 Le **diagramme MPD (V6 et V7) ne le montre pas**. À ajouter en note sur `Mandate`.
- ✅ **Paramètres de rémunération** : 3 tables, 3 étapes (`parameters_fees` → `commission_scale` → `hunter_rate_parameters`).
  - Valeurs du sujet : `documents utiles/REGLES-CALCUL-REMUNERATION.md:644-685`.
  - Seed : `docker/init-v3/05_parametres.sql`. Service : `API/src/app/services/parametrage_service.py`.
  - Le sujet dit « table de paramètres, jamais en dur » (`REGLES-CALCUL-REMUNERATION.md:47`) mais **ne dit pas qui construit le `Parametrage`** depuis la table : c'est un choix de conception de l'équipe (🟡 à écrire dans l'ADR D).
- ✅ **Table `hunter_rate_parameters`** : aucun CHECK sur les valeurs, voulu (`01_create…sql:827`). Valeurs « à valider avec le client ».

## 4. Nouveaux sujets d'ADR nés aujourd'hui

| Sujet | Où le ranger | Remplace |
|---|---|---|
| Renouvellement : `renewed` sur l'ancien, pas d'avenant | **ADR L** (règles du mandat, numéro proposé 039) | **ADR-010 et ADR-013** → passent en « remplacé par » |
| Exclusivité par trigger, pas par `EXCLUDE` | **ADR L** (039) | rien |
| Qui lit les paramètres : un service qui construit le `Parametrage` | **ADR D** (034) | rien |

💡 L'ADR L grossit : 6 mois, exclusivité, renouvellement, annulation, plus ces deux points. 🟡 À décider : un seul ADR, ou deux (mandat : durée et exclusivité / renouvellement).

## 5. Questions ouvertes à trancher en séance

1. 🟡 **ADR-028** : 6 questions dans le brouillon (type de token et de session, génération et remise de la clé d'API…). La citation de Jeff est **notée par l'équipe**, non vue en direct.
2. ❌ **ADR-027 et ADR-025 citent « ADR-026 » pour « pas d'authentification »**, mais l'ADR-026 de Confluence parle des mots de passe. À corriger quand on réécrit ADR-027.
3. 🟡 **Eircode** : le regroupement dans N ne couvre pas ADR-022 (table `client`). Une phrase dans R, ou un petit ADR à part ?
4. 🟡 **Y dépendait d'une vérif** : faite pour 016 et 026 (remis en vigueur). Reste à relire ADR-025 / Z (lien chasseur → manager).
5. 🟡 **Vocabulaire des statuts** : le modèle du prof n'a que « proposé / accepté / remplacé par ADR-xxx » (`JOURNAL-DE-DECISIONS.md:22`, `:72`).
   - « Annulé » n'y existe pas.
   - Proposition : quand le remplaçant est écrit, 024 et 025 passent en « remplacé par » ; le dossier « Annulé / Remplacé » devient « Remplacé » ; « Refusé » : à quoi sert-il (aucun ADR refusé aujourd'hui) ?
6. 🟡 **« renewed ⇒ un successeur existe »** : aucune contrainte simple ne le dit. L'API, un trigger, ou on assume ?
7. ⚠️ **Noms de tables périmés** possibles dans les ADR D et I (`remuneration_parameters` est devenu `hunter_rate_parameters`).
8. 🟡 **F et V attendent** : la grille de performance (F, sens du critère « visites » à vérifier), la durée d'effacement d'un compte (V, à proposer avec sa source).

## 6. Ordre de travail proposé

1. **Ceux qui remplacent d'anciens ADR** (pour pouvoir écrire « remplacé par ») : 028 (auth), 029 (Z, remplace 025), 030 (I+Q, remplace 019), 031 (N, remplace 009), 032 (A, remplace 012), puis finir **024** avec B, puis **L** (remplace 010 et 013).
2. **Ceux déjà décidés** : 033 à 047 (liste dans `2026-10-08-proposition-regroupement-adr.md`, § 3, groupe 2).
3. **Ceux qui attendent** : 048 (F), 049 (V).
4. **Réécrire ADR-027** (proposé, donc modifiable) : authentification, matrice des droits, rôle lecture seule.

## 7. Règles à rappeler à la table

- ✅ **Ne jamais effacer un ADR accepté** : on écrit un nouvel ADR, et l'ancien passe en « remplacé par » (`JOURNAL-DE-DECISIONS.md:72`).
- ✅ Chaque ADR : contexte, options envisagées, décision, conséquences, sources. Un chiffre se recopie avec sa source.
- ⚠️ Les numéros sont des propositions tant que le groupe ne les a pas pris sur Confluence.
- ⚠️ **Rien sur Confluence sans accord** du groupe. Claude crée des **pages**, pas des **dossiers** (l'outil ne sait pas), et ne voit pas les dossiers.

## 8. Ce que Claude n'a pas vérifié

- ❌ ADR-010 et ADR-013 relus **sur Confluence** : lus seulement à travers les notes du dépôt.
- ❌ Image du diagramme V7 : non relue ; le PDF et le XML V6 ont été lus.
- ❌ `questions-a-trancher.md` : lu en partie (1 437 lignes).
- ⚠️ Les tests tournent en local (202 passés) et dans le conteneur `api` (7 tests sautés, normal : il ne voit pas `docker/`).
- ⚠️ `requirements.txt` ne fixe aucune version : SQLAlchemy 2.1 casse la connexion, il faut `sqlalchemy<2.1`. Non corrigé.

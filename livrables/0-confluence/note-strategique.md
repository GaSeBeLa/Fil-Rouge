> **Copie de Confluence** — page « Note stratégique (axes d’évolution) » (id 18022434, version 7), espace GaSeBeLa1, copiée le 2026-11-19.
> La source qui fait foi reste Confluence : https://laurenceamethyste.atlassian.net/wiki/spaces/GaSeBeLa1/pages/18022434/Note+strat+gique+axes+d+volution. Les images, schémas draw.io et encadrés ne passent pas dans l'export : ils sont signalés par une ligne « 🖼️ Image ou schéma non copié : <nom ou légende si connue> ».

### 1. Synthèse de l'existant et diagnostic technique

Le système d'information actuel de la société de chasse immobilière repose sur une architecture artisanale limitant son périmètre à seulement 3 tables (`secteurs`, `utilisateurs`, `mandats`), ce qui constitue aujourd'hui un frein structurel majeur. L'audit a formellement qualifié 16 risques, dont trois classés en priorité absolue (cote 9 sur 9) : des mandats marqués « actifs » alors qu'ils ont expiré (R01), un chasseur enregistré comme client (R02), et l'absence de toute trace des honoraires (R03). S'y ajoutent la perte du code source du backend (R09, cote 6) et une architecture qui ne pourra pas absorber la charge future.

L'analyse directe des données illustre la criticité de la situation :

* Un tiers des mandats (6 sur 18) sont faussement marqués comme « actifs » alors qu'ils ont dépassé leur validité légale de 6 mois, allant jusqu'à 247 jours de dépassement.
* L'intégrité référentielle est défaillante, ayant déjà conduit à enregistrer un chasseur comme client sur un mandat existant.
* Les critères de recherche sont noyés dans des champs textes inexploitables (83 % des surfaces ambiguës), bloquant toute démarche d'automatisation.

---

### 2. Vision cible et enjeux stratégiques

Le SI doit impérativement se transformer pour soutenir le modèle économique rentable et le plan de développement de l'entreprise.

* **Hyper-croissance et Internationalisation :** Le système doit absorber un passage à l'échelle massif prévoyant le rachat d'agences, un déploiement dans 9 autres pays européens (Espagne, Allemagne, Royaume-Uni, Irlande, les 3 pays du BeNeLux, Italie, Suisse) ainsi que les DROM, générant plusieurs milliers de mandats par semaine.
* **Intégration de l'Intelligence Artificielle :** La structuration absolue des données est le prérequis technique non négociable pour déployer les modèles de _matching_ entre biens et demandes, ainsi que les futurs « chasseurs-IA » d'assistance.
* **Sécurisation juridique et financière :** Le SI doit refléter fidèlement l'exhaustivité du métier (statuts réels des mandats, paiements notariés, barèmes de commission variables) tout en garantissant la stricte conformité réglementaire.

---

### 3. Axes d'évolution prioritaires

Pour combler l'écart entre le SI hérité et la vision cible, la stratégie s'articule autour de trois axes de refonte :

**Axe 1 : Refonte structurelle du modèle de données (Data)**

* **Ségrégation des rôles :** Démembrement de la table unique `utilisateurs` en entités distinctes (`Client` et `Hunter`) pour éradiquer les failles d'intégrité et les valeurs nulles par conception.
* **Modélisation du parcours métier complet :** Création des entités manquantes fondamentales permettant le calcul de performance et la comptabilité : `biens`, `visites`, `offres`, `baremes_commission` et `paiements`.
* **Maîtrise temporelle et historique :** Implémentation d'une table de suivi des signatures, historisation des demandes de recherche en versions successives, et matérialisation informatique du cycle de vie légal des mandats.
* **Structuration pour l'IA :** Typage strict des critères de recherche et normalisation des entités géographiques (`secteurs`) pour rendre les données exploitables par les algorithmes.

**Axe 2 : Modernisation de l'architecture technique (Build)**

* **Changement de paradigme SGBD :** Migration vers PostgreSQL pour bénéficier de son partitionnement déclaratif natif (indispensable pour gérer le volume international) et de la richesse de ses types complexes (JSONB).
* **Standardisation linguistique :** Adoption de l'anglais pour l'ensemble du code, des schémas de base de données cibles et de la documentation technique afin de faciliter l'intégration de développeurs lors des futurs rachats d'agences étrangères.
* **Séparation OLTP/OLAP :** Isolation de la base de production (transactionnelle) et du système décisionnel (analytique) pour garantir la vélocité du SI sous très forte charge.

**Axe 3 : Conformité et Gouvernance (Security & Compliance)**

* **Privacy by Design (RGPD) :** Anonymisation ou pseudonymisation des données personnelles en clair, et élaboration d'un registre des traitements strict avant toute exposition des données aux outils d'Intelligence Artificielle.
* **Numérique responsable :** Intégration de pratiques d'éco-conception pour limiter l'empreinte environnementale du SI, notamment par l'optimisation des politiques de rétention et de sauvegarde des données (arbitrage multi-fréquences).

---

### 4. Trajectoire de mise en œuvre

La transformation sera exécutée de manière incrémentale selon les phases du projet :

1. **Phase 2 (Réponse au besoin actuel) :** Élaboration du Modèle Conceptuel et Logique de Données cible (MCD/MLD) couvrant l'intégralité du métier, mise en place des contraintes d'intégrité, et rédaction du script de migration sécurisé des données historiques (`migration.sql`).
2. **Phase 3 (Absorber la croissance) :** Conception de l'architecture Big Data, dimensionnement chiffré des composantes (Volume, Vélocité, Variété), et conception du schéma d'alimentation des données vers le modèle analytique (OLAP).
3. **Phase 4 (Parcours IA) :** Développement applicatif d'un nouveau Backend API robuste, accompagné de ses maquettes, de sa couverture de tests, et de la conception logicielle du programme de _matching_ IA.

---

# Note de cadrage — compléments proposés (brouillon)

> Brouillon du 2026-11-03, préparé pour Békanty (R de la note de cadrage) : elle
> corrige, puis colle sur la page Confluence « Note de cadrage » (page 17498130,
> version du 21 août). Les sections 1, 2 et 4 de la page ne changent pas.
>
> Sources : modèle `SP/documents utiles/NOTE-DE-CADRAGE.md` ; compétence notée
> `SP/documents utiles/TRACABILITE-COMPETENCES.md:50` (« démarche, objectifs,
> délais, budget, ressources, qualité ») ; formats `GRILLE-EVALUATION.md`.
> ✅ établi par une source · 🟡 à compléter par l'équipe · 💡 proposé.

---

## 3. Périmètre — à remplacer

**Dans le périmètre**

- Refonte complète du modèle de données : MCD/MLD cible, puis schéma
  PostgreSQL **v3** de **22 tables** (comptes, fiches clients et chasseurs,
  demandes et critères versionnés, mandats, biens, propositions, visites,
  offres, ventes, paiements).
- Une **API backend** en Python (FastAPI + SQLModel) sur PostgreSQL : un
  CRUD complet, des droits par rôle, et le calcul de rémunération du sujet.
- La **migration** des données existantes vers le nouveau schéma
  (`migration.sql`, rejouable), avec le nettoyage des anomalies de l'audit.
- Le **flux de données** : import des annonces chaque nuit (Airflow),
  stockage brut (MinIO), recherche (Elasticsearch), logs (Kibana), et un
  schéma analytique (OLAP).
- Un **moteur de suggestion de biens** simple, à base de règles (v1),
  pour préparer l'IA.

**Hors périmètre**

- ✅ Aucun site web ni écran (pas de « front ») ; aucune mise en production.
- ✅ Pas de page de connexion : on fournit seulement les outils côté serveur
  (connexion, jeton, rôles, droits) — Jeff, entretien rapporté le 07/10.
- ✅ Pas de facture en base — Jeff, entretien rapporté le 07/10.
- ✅ L'acte chez le notaire n'est pas géré ; sa date et son prix restent des
  entrées du calcul — dit le 02/10.
- ✅ Pas d'entraînement de modèle d'IA : le sujet demande de **concevoir**
  la base qui le nourrit (`SP/Readme.md:257`).

---

## 3 bis. Contraintes et hypothèses — à ajouter (💡 pratique courante)

**Contraintes** (ce qui nous est imposé)

- La base est **PostgreSQL** (ADR-001) ; les noms du code sont en anglais (ADR-002).
- Tous les montants sont en **euros**.
- Les fichiers d'origine du sujet (le StarterPack) ne se modifient jamais.
- Tout tourne en local, avec Docker, et sans budget.
- Les données sont **fictives** : celles du sujet, et des données générées.

**Hypothèses** (ce qu'on suppose vrai)

- La croissance prévue : plusieurs milliers de mandats par semaine, et des
  centaines à des milliers de biens par recherche (`SP/Readme.md:160`).
- Les chiffres de la rémunération sont ceux proposés par le sujet ; ils
  restent des paramètres, que l'entreprise pourra changer.

---

## 3 ter. Gouvernance — à ajouter (💡 pratique courante)

- **Le Product Owner** (les formateurs) valide le périmètre et les livrables.
- **L'équipe décide ensemble** : une question ouverte se vote sur Discord ;
  la décision est écrite dans un ADR (journal de décisions, Confluence).
- **Chaque livrable a un responsable (R) et un valideur (A)** : voir le RACI.

---

## 5. Parties prenantes — lignes « à définir » à remplacer

D'après le RACI (proposition du 03/11, à valider) :

| Membre | Ce qu'il porte surtout |
|---|---|
| Sébastien | l'API backend, le modèle cible, la migration, l'architecture, l'OLAP, les tests |
| Laurence | le registre des anomalies, le journal de décisions, la conception de l'appli, la matrice de décision, la note souveraineté IA |
| Békanty | la note stratégique, la note de cadrage, le cahier des charges, le SWOT, le MoSCoW, l'accessibilité |
| Gabriel | l'organisation du dépôt, la cartographie, l'étude d'opportunité, le RGPD, la note 3V, l'éco-conception, le PCA/PRA, la note d'indexation |

---

## 6. Planning et jalons — à remplacer

| Jalon | Date cible | Livrables associés |
|---|---|---|
| Phase 1 — Audit de l'existant | du 25 au 31 juillet | registre des anomalies, cartographie, rapport d'audit |
| Phase 2 — Besoin actuel | à partir du 17 août · 🟡 fin | note de cadrage, MoSCoW, CDC technique, MCD/MLD cible, `migration.sql`, note d'indexation |
| Phase 3 — Croissance | 🟡 | dossier d'architecture, matrice de décision, note 3V, schéma OLAP, éco-conception, PCA/PRA |
| Phase 4 — Parcours futur avec l'IA | 🟡 | API, plan de tests, schéma du programme d'IA, conception du matching, note souveraineté |
| Présentation intermédiaire | ✅ 16 octobre | diaporama |
| Soutenance | 🟡 | dossier professionnel, oral individuel |

🟡 Les dates à compléter : demander à Seb ou au formateur.

---

## 7. Ressources — à écrire

- **Humaines** : 4 étudiants (Sébastien, Laurence, Békanty, Gabriel) ; les
  formateurs jouent le Product Owner.
- **Techniques** : nos ordinateurs, et une pile Docker locale : PostgreSQL,
  l'API, MinIO, Airflow, Elasticsearch, Logstash, Kibana.
- **Outils de travail** : GitHub (code, et un kanban GitHub Projects),
  Confluence (documentation), Discord (échanges), un assistant IA (Claude)
  pour aider à coder et à relire.
- **Budget** : 0 €. Tous les outils sont gratuits ou en offre étudiante.

---

## 7 bis. Démarche et qualité — à ajouter (demandé par le jury)

- **Démarche** : un projet découpé en **chantiers**, eux-mêmes découpés en
  petites tâches d'une séance ; chaque tâche suivie sur le kanban ; les
  décisions votées sur Discord et notées dans le journal (ADR, Confluence).
- **Qualité** :
  - des **tests automatiques** à chaque changement du code (plus de 1 000
    tests, tous verts au 03/11) ;
  - chaque tâche de code est relue avant d'être enregistrée (commit) ;
  - chaque décision importante a sa trace écrite (ADR).

---

## 8. Risques identifiés — à écrire

| Risque | Impact | Parade envisagée |
|---|---|---|
| Un membre absent ou surchargé | des livrables en retard | le RACI répartit le travail ; chacun a un remplaçant qui valide (A) |
| Le travail repose trop sur une personne | un oral fragile, une charge inégale | répartir les livrables manquants (RACI du 03/11) ; chacun relit les parties des autres |
| Perdre des données ou du travail | des jours de travail perdus | tout est sur GitHub et Confluence ; sauvegardes et plan de reprise (PCA/PRA) |
| Données personnelles mal protégées | non-conformité RGPD | registre RGPD, droits par rôle, compte en lecture seule, données pseudonymisées |
| L'assistant IA se trompe | un livrable faux | relire chaque sortie, tout vérifier contre le sujet et le code (`SP/Readme.md:342-346`) |
| Le périmètre déborde | du temps perdu sur l'inutile | le hors-périmètre ci-dessus, validé avec le Product Owner |

---

## 9. Critères de réussite — à écrire

- Chaque livrable de la grille d'évaluation existe, au bon format
  (`GRILLE-EVALUATION.md`).
- La base v3 tourne, la migration se rejoue, et les tests passent.
- Les règles métier du sujet sont respectées (rémunération, mandats, droits).
- **Chaque membre sait expliquer tout le projet**, y compris les parties des
  autres : le jury interroge chacun seul (`SP/Readme.md:322`).

**Indicateurs** (💡 un chiffre par objectif ; les cibles sont à valider)

| Objectif (section 2) | Indicateur | Cible |
|---|---|---|
| Fiabiliser l'intégrité des données | anomalies du registre d'audit traitées par la migration | toutes |
| Sécuriser la conformité juridique | mandats expirés encore actifs | 0 |
| Structurer la recherche de biens | critères de recherche en texte libre | 0 |
| Pérenniser l'architecture | tests automatiques verts | 100 % |
| Livrer le projet | livrables de la grille présents (`GRILLE-EVALUATION.md`, 21 lignes) | 21 sur 21 |

---

## 10. Validation — à ajouter (💡 pratique courante)

| Version | Date | Rédigée par | Validée par |
|---|---|---|---|
| 1 | 21 août 2026 | Békanty | 🟡 |
| 2 | 🟡 | Békanty | 🟡 (A du RACI : Sébastien) |

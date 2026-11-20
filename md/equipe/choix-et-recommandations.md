# Choix et recommandations en attente

> Demandé par Sébastien le 2026-11-20 : « pour chaque choix comme ça (ou recommandation), note-le quelque part pour ne pas l'oublier ».
> Une ligne par choix proposé ou recommandation. Elle reste ici tant qu'elle n'est pas tranchée **et** faite (ou écartée, avec la raison).
> Statuts : 🟡 à trancher · ➡️ tranché, à faire · ✅ fait · ❌ écarté.

| # | Date | Choix ou recommandation | D'où il vient | Proposition du Glaude | Statut |
|---|---|---|---|---|---|
| ENV-A | 2026-11-20 | Épingler PostgreSQL : `postgres:16` → `postgres:16.15` dans `docker-compose.yml` | note d'environnement, § 2 (écart à ADR-015) | oui, 5 min ; il faut le oui de Sébastien (fichier réservé) | ✅ oui (Sébastien, 20/11) ; fait, API `68ce316`, tests verts |
| ENV-B | 2026-11-20 | Coder la sauvegarde quotidienne : `pg_dump` + rôles chaque nuit, 7 jours gardés | note d'environnement § 5, PCA/PRA, éco-conception, SWOT phase 3 | oui, ~45 min, avec un test | ➡️ A, un DAG Airflow (Sébastien, 20/11) |
| ENV-C | 2026-11-20 | Mesure de charge : 1 000 requêtes sur la recherche et la liste des biens, médiane et 95e centile | note d'environnement § 4-5, dossier d'architecture § 6 | si le temps le permet, ~30 min | ➡️ A, maintenant (Sébastien, 20/11) |
| ENV-D | 2026-11-20 | Garder comme limites écrites : mesure d'énergie, Airflow 2 en fin de vie, choix de l'hébergeur | note d'environnement § 4-5 | oui, rien à faire | ✅ on les assume (Sébastien, 20/11) |
| GANTT | 2026-11-19 | Confirmer 3 dates proposées : fin de la phase 4 (27/11), rendu des livrables (18/12), début de la préparation de l'oral (04/01/2027) | `livrables/6-pilotage/gantt.md` | à confirmer par le groupe | 🟡 |
| MCD-AUT | 2026-11-19 | Les liens « auteur » (Criteria, Estate, EstateContact → User) dans le MCD : tous, ou aucun ? | `livrables/2-modelisation/mcd-a-mettre-a-jour.md` | aucun, et l'écrire dans les justifications (traçabilité, pas métier) | 🟡 |
| PREUVES | 2026-11-19 | Les 2 preuves qui manquent encore à la grille : comptes rendus d'ateliers ; pipeline CI | grille d'auto-évaluation | comptes rendus d'abord (~30 min), CI ensuite (~45 min) | 🟡 |

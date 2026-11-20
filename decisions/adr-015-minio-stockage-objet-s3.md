# ADR-015 : Choix de MinIO comme solution de stockage objet S3-compatible

> Copié de Confluence (page 52363404, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 02/09/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte**

Dans le cadre du Fil Rouge immobilier, le projet doit stocker des objets volumineux et non structurés : photos de biens, diagnostics, pièces jointes des mandats, exports. Le projet met aussi en place une architecture de type Data Lake avec 3 zones de traitement. Il faut une solution de stockage objet compatible avec l'écosystème S3, utilisable en local sans coût et déployable en production sans dépendance cloud.

**Options envisagées**

**Option 1 :** Stockage local sur filesystem / volume Docker simple - Simple mais pas d'API standard, pas de gestion de buckets, pas portable vers un S3 cloud.

**Option 2 :** Service cloud managé type AWS S3, Scaleway Object Storage, GCP Storage - Solution robuste mais payante, nécessite des accès internet et des credentials cloud dès le développement, vendor lock-in.

**Option 3 :** Solution S3-compatible auto-hébergée - MinIO - Implémente l'API S3, 100% auto-hébergeable dans notre `docker-compose.yml`, gratuite, légère.

**Décision**

Option 3 retenue. Utilisation de MinIO avec deux services : `minio` pour le serveur et `minio-setup` avec `minio/mc` pour l'initialisation automatique.

**Justification**

MinIO a été choisi pour sa cohérence avec notre architecture :

1. **Compatibilité S3 standard :** Toute librairie S3 fonctionne, passage futur vers AWS S3 ou Scaleway sans changer le code applicatif.
2. **Architecture Medallion prête :** Permet de créer nativement les 3 buckets `bronze / silver / gold` pour notre pipeline de données.
3. **Intégration Docker simple :** S'intègre directement dans le `docker-compose.yml` du projet avec persistance via le volume `minio_data` et console web sur le port 9001.
4. **Autonomie :** Fonctionne offline, gratuit pour le développement, aucun coût d'infrastructure cloud pour le Fil Rouge.

**Conséquences**

**Base de données / Infra :** Ajout de 2 services dans `docker-compose.yml` : `minio` sur les ports 9000 (API S3) et 9001 (console) et `minio-setup` qui crée automatiquement les buckets `bronze`, `silver`, `gold` au démarrage.

**Développement :** Le code applicatif doit utiliser un client S3. Les credentials sont gérés via `MINIO_ROOT_USER` et `MINIO_ROOT_PASSWORD`. Les buckets n'ont plus besoin d'être créés manuellement.

**Gestion métier :** Permet de stocker les documents liés aux critères et aux mandats et de poser les bases d'une future couche data pour la prospection immobilière.

# ADR-014 : Pinning strict des versions d'images Docker - Interdiction du tag latest en production

> Copié de Confluence (page 52690992, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 02/09/2026
**Statut :** accepté
**Décideurs :** L'équipe projet

**Contexte**

En production, l'utilisation du tag `latest` pour les images Docker rend les déploiements non déterministes. `latest` est un tag mutable qui pointe vers une version différente au fil du temps. Si un membre de l'équipe exécute un `docker pull` dans 3 mois, il obtiendra un binaire différent de celui validé aujourd'hui, ce qui peut introduire des régressions, des breaking changes ou des failles de sécurité non maîtrisées. Pour garantir la stabilité, l'auditabilité et la conformité aux exigences de cybersécurité, il est indispensable de figer les versions utilisées.

**Options envisagées**

**Option 1 :** Utiliser le tag `latest` pour toutes les images (ex: `node:latest`, `postgres:latest`). Simplicité apparente mais perte totale de reproductibilité.

**Option 2 :** Pinner chaque image sur une version complète et fixe - ex: `postgres:16.10-alpine` et `minio/minio:RELEASE.2025-02-07T23-21-09Z`. Tout le monde a exactement la même version.

**Décision**

Option 2 retenue. Interdiction du tag `latest` et des tags sans version patch en production. Toutes les images du `docker-compose.yml` doivent être pinnées sur une version fixe.

**Justification**

En production on ne met jamais `latest` car on perd la reproductibilité. Pinner garantit que tout le monde a le même binaire, c'est une exigence DevOps et cybersécurité. Une version figée évite les mises à jour silencieuses et les breaking changes non maîtrisés.

**Conséquences**

Base de données / Docker : Le `docker-compose.yml` est mis à jour

**Documentation :** Chaque montée de version doit faire l'objet d'un test et d'une validation avant déploiement en production, garantissant un historique clair des binaires utilisés.

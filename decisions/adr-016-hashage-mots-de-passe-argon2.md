# ADR-016 : Hashage des mots de passe avec Argon2

> Copié de Confluence (page 52592771, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 04/09/2026
**Statut :** accepté, ANNULE le 22/09/2026 après contact avec PO (Jeff) car authentification hors scope — **REMIS EN VIGUEUR le 08/10/2026** (authentification rouverte par Jeff le 07/10/2026 ; confirmé par Laurence pour le groupe). Complété par l'ADR-028 (à venir).
**Décideurs :** L'équipe projet

**Contexte**

L'API doit stocker les mots de passe utilisateurs de manière sécurisée. On ne stocke jamais un mot de passe en clair : on stocke le résultat d'une fonction de hashage à sens unique, spécialement conçue pour être lente et coûteuse à attaquer (contrairement à SHA-256 ou MD5, trop rapides et donc cassables par force brute/GPU). Deux candidats sérieux existent aujourd'hui : Bcrypt (standard historique depuis 1999) et Argon2 (vainqueur du Password Hashing Competition en 2015, recommandé par l'OWASP).

**Options envisagées**

- Option 1 : Bcrypt — facteur de coût CPU réglable, mais pas memory-hard (coût mémoire fixe et faible, ~4 Ko) et limite silencieuse à 72 octets.
- Option 2 : Argon2id — vainqueur du Password Hashing Competition (2015), memory-hard (`time_cost`, `memory_cost`, `parallelism` réglables), choix n°1 recommandé par l'OWASP.
- Option 3 : PBKDF2 — configurable en itérations uniquement, pas memory-hard du tout, donc encore plus vulnérable au GPU cracking que Bcrypt.
- Option 4 : Scrypt — également memory-hard et un bon candidat, mais moins recommandé qu'Argon2 par l'OWASP en 2026.

**Décision**

Option 2 retenue. Utilisation d'Argon2id comme algorithme de hashage des mots de passe, via la librairie Python `argon2-cffi`. Deux règles non négociables en découlent : un mot de passe en clair n'est jamais stocké, sous aucune forme et à aucune étape (ni en base, ni en logs, ni en cache) ; la colonne `password` passe en `VARCHAR(255)` pour contenir la chaîne encodée produite par Argon2id (algorithme, version, paramètres, sel et hash concaténés).

**Justification**

| Critère | Bcrypt | Argon2id |
| --- | --- | --- |
| Résistance mémoire (memory-hard) | Non — coût mémoire fixe et faible (~4 Ko) | Oui — paramétrable, jusqu'à plusieurs dizaines/centaines de Mo |
| Résistance aux attaques GPU/ASIC | Limitée : les GPU/ASIC modernes cassent Bcrypt bien plus vite qu'un CPU classique | Forte : un GPU a beaucoup de cœurs mais peu de RAM par cœur, ce qui casse l'avantage de la parallélisation massive |
| Limite de longueur du mot de passe | Oui, tronqué à 72 octets (bug historique connu, silencieux) | Non, pas de limite pratique gênante |
| Recommandation actuelle OWASP | Alternative acceptable si Argon2 indisponible | Choix n°1 recommandé |

La faiblesse structurelle de Bcrypt est qu'il n'est pas « memory-hard » : un attaquant disposant de matériel spécialisé (GPU, voire ASIC/FPGA dédiés) peut casser des hashs Bcrypt à une vitesse largement supérieure à celle d'un attaquant limité au CPU, car Bcrypt ne nécessite quasiment aucune RAM par tentative. Argon2, en forçant l'utilisation de RAM par tentative de hash, rend ce type de parallélisation matérielle beaucoup plus coûteuse en argent et en infrastructure — c'est la raison principale de sa supériorité en 2026, dans un monde où le cassage par cluster GPU est devenu accessible.

**Conséquences**

- **Base de données :** migration de la colonne `password` vers `VARCHAR(255)` requise sur les environnements existants, avant tout déploiement. Les mots de passe déjà hashés avec un autre algorithme (ex. Bcrypt) restent valides tels quels.
- **Développement :** toujours utiliser la fonction de vérification fournie par `argon2-cffi` (comparaison en temps constant), jamais une comparaison manuelle de chaînes ; prévoir un mécanisme `check_needs_rehash` pour re-hasher progressivement les anciens mots de passe (migration depuis Bcrypt) au moment de la reconnexion.
- **Infrastructure :** surveiller la consommation mémoire côté serveur si beaucoup de hashs sont calculés en parallèle (pic de connexions) → prévoir du rate-limiting sur les endpoints d'authentification ; vérifier la compatibilité des bindings C d'`argon2-cffi` avec l'environnement de déploiement (Docker, etc.).
- **Migration :** possible progressivement, sans forcer un reset de mot de passe pour l'ensemble des utilisateurs. Les paramètres (`time_cost`, `memory_cost`, `parallelism`) devront être calibrés sur l'infrastructure de production réelle, avec un objectif de ~250-500 ms par hashage.

# ADR-026 : Politique de robustesse des mots de passe utilisateurs

> Copié de Confluence (page 51578382, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 22/09/2026
**Statut :** ANNULE le 22/09/2026 après contact avec PO (Jeff) — **REMIS EN VIGUEUR le 08/10/2026** (authentification rouverte par Jeff le 07/10/2026 ; confirmé par Laurence pour le groupe). Complété par l'ADR-028 (à venir).
**Décideurs :** L'équipe projet (proposition Gabriel, à confirmer)

**Contexte**

`UserCreate`/`UserUpdate` imposent `min_length=12`, marqué dans le code comme "une proposition, pas une décision" (tuto 1, §4.2). Il faut trancher une politique actée.

**Options envisagées**

| Option | Description | Source |
| --- | --- | --- |
| 1 | Longueur seule, `min_length=12`, aucune règle de composition | OWASP ASVS / NIST SP 800-63B-4 (2025) |
| 2 | Longueur `min_length=12` + composition obligatoire (majuscule, minuscule, chiffre, caractère spécial) | Écartée — voir Justification |
| 3 | Longueur ≥15, sans composition | NIST SP 800-63B-4 (recommandé, plus strict) |

**Décision**

Option 1 retenue. `min_length=12`, aucune règle de composition obligatoire.

**Justification**

NIST SP 800-63B-4 (2025), référence citée par l'OWASP Authentication Cheat Sheet, interdit désormais explicitement aux vérificateurs d'imposer des règles de composition ("SHALL NOT"), au profit de la seule longueur. La complexité forcée pousse les utilisateurs vers des motifs prévisibles (`Password1!`) sans gain réel contre le vol par phishing/malware : une étude sur 1,08 milliard de mots de passe compromis montre qu'environ 21 % respectaient toutes les règles de complexité et ont quand même été volés. 12 caractères correspond au minimum recommandé par l'OWASP ASVS.

**Conséquences**

- `UserCreate.password` / `UserUpdate.password` : `min_length=12` seul, déjà en place — aucun changement de code nécessaire.
- Pas de validator Pydantic supplémentaire à écrire pour la composition.
- Documentation à jour dans `user_model.py` si un commentaire mentionnait la composition (à vérifier — je n'en ai pas ajouté dans le code final, seulement dans la proposition d'ADR initiale, non appliquée).

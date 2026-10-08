# ADR-028 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 028 est une proposition.** Il vient de Laurence (Discord,
> 2026-10-08) et du pense-bête (`md/adr/2026-10-07-liste-adr-chantier-4.md:68`,
> « prochain numéro libre : 028 »).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt.** Les
> passages marqués 🟡 ne sont pas tranchés. Ce sont des questions, pas des
> décisions.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-028 : L'authentification revient côté back — outils d'authentification, mot de passe gardé, une clé d'API par programme

* **Date :** 08/10/2026 (décision du client : 07/10/2026)
* **Statut :** proposé
* **Décideurs :** le client (Jeff, formateur jouant le commanditaire) pour le périmètre ; l'équipe projet pour la mise en œuvre
* **Complète :** ADR-016 et ADR-026, remis en vigueur le 08/10/2026 (confirmé par Laurence pour le groupe)

**Contexte**

Le 22/09/2026, le client a répondu « non » à l'authentification : « vous ne gérez pas l'auth, c'est géré au dessus » (`md/adr/adr-026-perimetre-authentification.md:42-43`). Il a ajouté : « si vous voulez mettre quelque chose : prévoyez une simple vérification de provenance ou clé d'api générée de votre côté » (`:51-52`). ADR-016 (hachage Argon2) et ADR-026 (robustesse des mots de passe) avaient alors été marqués « ANNULE » sur Confluence.

Le 07/10/2026, à l'entretien, le client a changé de position (`md/questions/2026-10-07-questions-pour-jeff.html`, carte Q-JEF-14) :

> « on doit fournir les outils pour une bonne gestion de l'authentification (route de connextion, token, session, role, droit, etc.) , mais l'on ne doit pas crée la page de login en elle même. »

Dans le même entretien : une clé d'API **par programme** (Q-JEF-22), et le mot de passe **se garde**, haché en Argon2 (Q-JEF-21, « réglée par sa réponse à Q-JEF-14 »).

**Options envisagées**

1. **Rester hors périmètre**, comme le disait le brouillon d'ADR-026 du 22/09. Rejetée : le client a lui-même rouvert le sujet le 07/10.
2. **Authentification complète, page de login comprise.** Rejetée : le client précise « l'on ne doit pas créer la page de login en elle-même ».
3. **Fournir les outils côté back, sans page de login** (route de connexion, token, session, rôles, droits). **Retenue** : c'est ce que demande le client.

Sous-choix déjà tranchés par le client :

* **Mot de passe :** retirer la colonne, ou la garder. Gardée, hachée en Argon2 (Q-JEF-21).
* **Clé d'API :** une seule, ou une par programme. Une par programme (Q-JEF-22 : « il valide notre position, sans changement »).

**Décision**

1. L'équipe fournit, **côté back**, les outils d'authentification demandés par le client : route de connexion, token, session, rôles, droits. La liste du client se termine par « etc. » : elle est ouverte.
2. **Aucune page de login** n'est créée.
3. Le mot de passe est **gardé** et **haché en Argon2** : ADR-016 s'applique. Longueur minimale de 12 caractères, sans règle de composition : ADR-026 s'applique.
4. **Une clé d'API par programme** appelant l'API.
5. Le « qui a le droit de faire quoi » reste porté par la matrice d'ADR-027 (à réécrire, voir Conséquences).

**Justification**

Le client est le décideur du périmètre : ce qu'il a retiré le 22/09, il peut le rendre le 07/10. L'équipe n'a donc pas à défendre l'ancien périmètre. Le mot de passe se garde parce que les outils d'authentification sont maintenant à la charge de l'équipe : la colonne `user.password` a un usage. Sa protection par Argon2 était déjà décidée (ADR-016) et déjà codée (`API/src/app/utils/security.py:20-23`).

**Conséquences**

* **Code :** il n'y a aujourd'hui, dans `API/`, **aucune** route de connexion, aucun token, aucune clé d'API. Recherche faite le 08/10/2026 sur `APIKeyHeader`, `auth/login`, `create_access_token`, `get_current_user`, `require_role`, `OAuth2PasswordBearer`, `jwt` : **0 occurrence**. Ce qui existe : le hachage Argon2 (`security.py`, tests dans `API/tests/test_security.py`) et le minimum de 12 caractères (`API/tests/test_user_models.py:10`).
* **Plan de sécurité :** les étapes que le brouillon du 22/09 déclarait caduques (étapes 4 à 8 de `md/securite/securite-mots-de-passe-et-droits.md`, et `md/securite/tuto-2-authentification-jwt.md`) redeviennent d'actualité.
* **ADR-027 :** son contexte dit « l'authentification et le contrôle d'accès ne sont pas implémentés ». C'est faux depuis le 07/10. ADR-027 n'est que « proposé » : il se réécrit (`md/adr/2026-10-07-liste-adr-chantier-4.md:52-54`).
* **Brouillon local `md/adr/adr-026-perimetre-authentification.md` :** il décrit le périmètre « hors authentification ». Cet ADR-028 le remplace. Il ne doit pas être publié sous le numéro 026, qui est déjà pris sur Confluence.
* **Q-JEF-21 est close** ; Q-ACC-17, Q-ACC-18 et Q-MIG-11 n'ont plus d'objet, leur réponse étant « garder » (`md/questions/questions-a-trancher.md:257`).

**Questions ouvertes** 🟡

1. **Quel token, quelle session ?** Le client dit « token, session » sans choisir. Un tuto JWT existe déjà (`md/securite/tuto-2-authentification-jwt.md`). 💡 Proposition : le prendre comme point de départ, et dire pourquoi un autre choix serait préférable s'il y en a un.
2. **La clé d'API :** comment la génère-t-on, où la range-t-on, comment la remet-on au programme ? Le client a validé « une par programme » (Q-JEF-22) mais la carte demandait aussi « comment vous les remettre » : la réponse notée ne tranche que le nombre. 💡 Proposition à discuter : la clé dans `docker/.env`, jamais dans git (`md/questions/questions-a-trancher.md:188`).
3. **Quels rôles et quels droits ?** La liste du client finit par « etc. ». Les rôles actuels sont `Client`, `Hunter`, `Manager`, `Admin` (ADR-027), plus un rôle `Reader` en lecture seule fait au lot 12 (`questions-a-trancher.md:264`). À écrire dans ADR-027 réécrit.
4. **Parole du client :** la citation de Jeff du 07/10 est **notée par l'équipe** dans le rapport Jeff. Je ne l'ai pas vue en première main. À confirmer si elle doit servir de preuve en soutenance.
5. **ADR-026 « à confirmer » :** sa page Confluence garde « (proposition Gabriel, à confirmer) » dans les décideurs. Remis en vigueur, mais jamais « confirmé » par écrit dans ce qu'on a lu. 🟡 À dire en une ligne.
6. **Numéros qui se croisent :** ADR-027 et ADR-025 sur Confluence citent « l'ADR-026 » pour la décision « hors authentification ». Or l'ADR-026 de Confluence traite des **mots de passe**. À corriger dans ADR-027 (réécriture) en citant ADR-028.

**Sources**

| Affirmation | Source |
|---|---|
| Réponse du client du 22/09 | `md/adr/adr-026-perimetre-authentification.md:36-53` |
| Authentification rouverte, mot de passe gardé, Argon2 | `md/questions/questions-a-trancher.md:87`, `:257` |
| Citation de Jeff du 07/10 | `md/questions/2026-10-07-questions-pour-jeff.html`, carte Q-JEF-14 |
| Une clé par programme | même fichier, carte Q-JEF-22 ; `questions-a-trancher.md:258` |
| 016 et 026 remis en vigueur | Laurence, Discord, 2026-10-08 ; Confluence, pages 52592771 et 51578382, version 2 |
| Pas de code d'authentification dans l'API | recherche du 2026-10-08 : 0 occurrence dans `API/` |
| Argon2 déjà codé | `API/src/app/utils/security.py:20-23` |
| Modèle d'ADR et règle « ne jamais effacer » | `documents utiles/JOURNAL-DE-DECISIONS.md:19-40`, `:72` |

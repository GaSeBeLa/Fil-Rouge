### ADR-052 : La connexion repose sur un jeton JWT de 60 minutes, l'utilisateur relu en base à chaque appel

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 09/10/2026
* **Statut :** proposé
* **Décideurs :** Sébastien a choisi l'option 1 le 09/10/2026 (Discord, réponse à la question 1 d'ADR-028) ; le groupe l'accepte avec cet ADR.
* **Complète :** ADR-028 (authentification côté back, question ouverte 1) ; ADR-016 (Argon2) ; ADR-026 (robustesse des mots de passe)
* **Voir aussi :** ADR-027 (qui a le droit de faire quoi) ; ADR-049 (désactiver un compte)

**Contexte**

* Le client demande des outils d'authentification côté back : « route de connexion, token, session, rôle, droit » (cité dans ADR-028).
* Le sujet ne dit rien de JWT, de token ni de session (recherche du 08/10/2026 dans le StarterPack, citée dans ADR-028).
* Le tuto 2 du dépôt (`md/securite/tuto-2-authentification-jwt.md`) propose un JWT sans trancher, et dit que le choix « mérite un ADR, avec sa durée d'expiration ».
* Aujourd'hui, `API/` n'a aucune route de connexion ni aucun token (ADR-028, section Conséquences).

**Options envisagées**

1. **Un JWT signé, 60 minutes, l'utilisateur relu en base à chaque appel.** Avantage : le tuto 2 l'explique déjà ; un compte désactivé ou rétrogradé perd ses droits tout de suite. Inconvénients : une lecture en base à chaque appel ; une bibliothèque de plus. **Retenue.**
2. **Une session rangée en base.** Avantage : se coupe d'un geste, côté serveur. Inconvénients : une table de plus ; rien n'est préparé dans le dépôt. Écartée.
3. **Décider plus tard, en codant.** Avantage : rien à faire ce soir. Inconvénient : ADR-028 garde une question ouverte devant le jury. Écartée.

**Décision**

1. ✅ Un **JWT** signé, que le client présente à chaque appel.
2. ✅ Durée de vie : **60 minutes**, sans jeton de rafraîchissement.
3. ✅ À chaque appel, l'utilisateur est **relu en base** : son rôle et son activation du moment font foi, pas ceux écrits dans le jeton.
4. 💡 Signature `HS256` avec `pyjwt`, la bibliothèque de la doc FastAPI (proposition d'ADR-028, à confirmer au codage).
5. 💡 Le secret se génère avec `openssl rand -hex 32` et ne s'écrit jamais dans le dépôt.
6. La « session » du client est donc la durée de vie du jeton.

**Conséquences**

* **Code :** à écrire. `API/requirements.txt` n'a aucune bibliothèque de jeton : il faut ajouter `pyjwt`. Rien n'est codé.
* **Où brancher :** une dépendance posée sur `build_crud_router` vaut pour toutes les routes CRUD (ADR-028).
* **Compte désactivé :** il perd ses droits au prochain appel (ADR-049).
* **Prix :** une lecture en base de plus à chaque appel.
* **Limite :** pas de jeton de rafraîchissement, donc une reconnexion toutes les 60 minutes.

**Questions ouvertes** 🟡

Aucune sur le choix. À décider au codage : la durée exacte si 60 minutes gêne, et où ranger le secret.

**Sources**

| Affirmation | Source |
|---|---|
| Choix de l'option 1 | Sébastien, Discord, 09/10/2026 |
| Le client demande « route de connexion, token, session » | ADR-028, Contexte |
| JWT proposé, 60 minutes, utilisateur relu en base | ADR-028, question ouverte 1, proposition |
| Le tuto propose JWT sans trancher ; « mérite un ADR » | `md/securite/tuto-2-authentification-jwt.md` (citée par ADR-028) |
| Aucune bibliothèque de jeton dans le dépôt | `API/requirements.txt` (cité par ADR-028) |

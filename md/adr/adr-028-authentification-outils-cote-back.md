# ADR-028 — brouillon à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À relire par le groupe, puis à coller dans
> le journal de décisions de Confluence. Rien ne s'écrit sur Confluence depuis
> ce fichier.
>
> ⚠️ **Le numéro 028 est une proposition.** Il vient du pense-bête :
> « prochain numéro libre : **028** » (`md/adr/2026-10-07-liste-adr-chantier-4.md:68`).
>
> 💡 **Rédigé le 2026-10-08 par Claude, d'après les fichiers du dépôt ; fini le
> même jour.** Le premier jet avait 6 questions ouvertes. Relu le 08/10/2026 par
> deux relecteurs (sources ; oral et jury) et un arbitre. Il en reste **une**,
> marquée 🟡 : le type de token. C'est une question, pas une décision.
>
> 🗂️ **Trois points réglés hors de la fiche** (ils parlent des sources ou des
> pages Confluence, pas de la décision) :
>
> * **La citation de Jeff sert de preuve**, comme « réponse notée par
>   l'équipe ». C'est la règle convenue : Jeff ne remplit pas le rapport,
>   l'équipe note ses réponses en entretien (`questions-a-trancher.md:111-112`,
>   `:214`, `:1183-1185`).
> * **ADR-026 garde « à confirmer » dans ses décideurs.** Il est confirmé sur le
>   fond : le groupe garde 12 caractères (Q-ACC-17, 07/10), puis remet ADR-026
>   en vigueur (Laurence, Discord, 08/10/2026). Reste à retirer « à confirmer »
>   sur la page : une retouche, pas une décision.
> * **Qui cite « ADR-026 » pour « pas d'authentification » ?** Sur Confluence,
>   ADR-027 seul (ADR-027 du 22/09 : Contexte et Options). ADR-025 ne le
>   cite pas (ADR-025 : 0 occurrence). Dans le dépôt : `API/README.md:251`.
>   L'erreur vient du brouillon local numéroté 026, jamais publié sous ce numéro.
>
> 🧹 **À faire ailleurs** (des tâches, pas la décision) :
>
> * Docs qui disent encore « hors périmètre » :
>   * `API/README.md:251` : « Pas d'authentification : le client l'a mise hors
>     périmètre (ADR-026) ». Le numéro est faux aussi : à remplacer par ADR-028.
>   * `md/securite/matrice-droits-crud-par-role.md:6-11` : « Cette matrice ne
>     sera donc pas codée ».
>   * `livrables/4-application/rapport-tests.md:255` : ENF-03 « dépend des
>     droits d'accès ; l'authentification est hors périmètre ».
>   * Q-INF-08 (`questions-a-trancher.md:196`) : « ENF-03 tombe avec l'auth ».
>     Le test d'accès croisé redevient possible.
>   * `API/src/app/models/user_model.py:61-62` : « min_length=12 : proposition du
>     tuto, pas une décision actée par le groupe […] À confirmer en réunion ».
>     Périmé depuis Q-ACC-17 et ADR-026 remis en vigueur.
>   * L'en-tête « la moitié de cette note est caduque »
>     (`md/securite/securite-mots-de-passe-et-droits.md:19-33`).
> * Le brouillon local `md/adr/adr-026-perimetre-authentification.md` décrit le
>   périmètre « hors authentification ». Cet ADR-028 le remplace. Il ne doit pas
>   être publié sous le numéro 026, déjà pris sur Confluence par les mots de passe.
> * ⚠️ `docker/docker-compose.yml` : « Jamais modifiés : […]
>   `docker/docker-compose.yml`, hormis la ligne du montage en LOT1 (accord du
>   2026-10-07, cette ligne seule) » (`context AI/10-lot-migration.md:63`).
>   Y ajouter les lignes des clés : à demander avant.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

### ADR-028 : L'authentification revient côté back — outils d'authentification, mot de passe gardé, une clé d'API par programme

✅ établi · 🟡 à décider · 💡 proposé

* **Date :** 08/10/2026 (décision du client : 07/10/2026)
* **Statut :** proposé
* **Décideurs :**
  * le client (Jeff, formateur jouant le commanditaire et le PO), pour le périmètre ;
  * l'équipe projet, pour la mise en œuvre (réponse « outils » à la Q2 de la page d'incohérences du 07/10).
* **Complète :** ADR-016 (hachage Argon2) et ADR-026 (robustesse des mots de passe), remis en vigueur le 08/10/2026 (Laurence, pour le groupe). Cet ADR ne les remplace pas.

**Contexte**

Le 22/09/2026, le client a répondu « non » à l'authentification : « vous ne gérez pas l'auth, c'est géré au dessus ». Il a ajouté : « si vous voulez mettre quelque chose : prévoyez une simple vérification de provenance ou clé d'api générée de votre côté ». ADR-016 et ADR-026 avaient alors été marqués « ANNULE » sur Confluence.

Le 07/10/2026, à l'entretien, le client a changé de position (carte Q-JEF-14) :

> « on doit fournir les outils pour une bonne gestion de l'authentification (route de connextion [sic], token, session, role, droit, etc.) , mais l'on ne doit pas crée [sic] la page de login en elle même. »

Dans le même entretien :

* le mot de passe **se garde**, haché en Argon2 (Q-JEF-21, « réglée par sa réponse à Q-JEF-14 ») ;
* une clé d'API **par programme** : il valide la position de l'équipe, « sans changement » (Q-JEF-22).

Ces réponses sont notées par l'équipe. C'est la règle convenue : Jeff ne remplit pas le rapport, le groupe lui pose les questions en entretien et note ses réponses.

**Options envisagées**

1. **Rester hors périmètre**, comme le disait le brouillon local d'ADR-026 du 22/09. Avantage : rien à coder. Écartée : le client a lui-même rouvert le sujet le 07/10.
2. **Authentification complète, page de login comprise.** Avantage : parcours complet à montrer. Écartée : le client précise « l'on ne doit pas crée la page de login en elle même ».
3. **Une clé d'API seule**, l'idée du client du 22/09. Avantage : très peu de code. Écartée : une clé dit quel programme appelle, pas quelle personne agit ; elle ne porte ni utilisateur ni expiration (`md/securite/tuto-2-authentification-jwt.md:99`). Elle ne suffit donc pas pour « role, droit ».
4. **Outils côté back, sans page de login, plus une clé par programme.** **Retenue** : c'est ce que le client demande le 07/10, sur les deux cartes.

Sous-choix déjà tranchés par le client :

* **Mot de passe :** le retirer, ou le garder. Gardé, haché en Argon2 (Q-JEF-21).
* **Clé d'API :** une seule, ou une par programme. Une par programme (Q-JEF-22).

**Décision**

✅ veut dire « établi par une source », pas « codé ». Les outils (points 1, 4, 5, 6) ne sont pas encore codés ; le hachage, les 12 caractères et les 5 rôles le sont (voir Conséquences).

1. ✅ L'équipe fournit, **côté back**, les outils d'authentification demandés : route de connexion, token, session, rôles, droits. La liste du client finit par « etc. » : elle est ouverte.
2. ✅ **Aucune page de login** n'est créée.
3. ✅ Le mot de passe est **gardé** et **haché en Argon2id** : ADR-016 s'applique. Longueur minimale de 12 caractères, sans règle de composition : ADR-026 s'applique.
4. ✅ **Une clé d'API par programme** qui appelle l'API. Chaque programme montre sa clé à chaque appel. Sans elle, il est refusé.
5. ✅ Les clés sont **générées par l'équipe** et rangées dans `docker/.env`. Jamais dans git, jamais dans le code.
6. ✅ Déduit des points 1 et 4 : **deux contrôles**, qui ne se remplacent pas. La clé dit quel programme appelle. Le token dit quelle personne agit.
7. ✅ Les rôles sont les **5 valeurs** de la table `role` : `Admin`, `Client`, `Hunter`, `Manager`, `Reader`. `Reader` consulte sans modifier.
8. ✅ Le « qui a le droit de faire quoi » est la matrice d'ADR-027, à réécrire. Cet ADR fournit l'outil ; ADR-027 en fixe le contenu.
9. 🟡 Le type de token et de session reste à choisir (question ouverte 1). 💡 Ce choix mérite son propre ADR, avec sa durée d'expiration (le tuto 2 le disait déjà, `tuto-2-authentification-jwt.md:105-106`).

**Justification**

* Le client est le décideur du périmètre, et il est notre PO. Ce qu'il a retiré le 22/09, il peut le rendre le 07/10. L'équipe n'a pas à défendre l'ancien périmètre.
* Le mot de passe se garde parce qu'il a de nouveau un usage : la route de connexion le vérifie. Le modèle de registre RGPD du sujet prévoit un « mot de passe (haché) » pour les comptes. Le hachage Argon2 était déjà décidé (ADR-016) et déjà codé.
* Une clé par programme : on peut en couper une sans couper l'autre. C'est l'argument de la position validée par le client.
* Clé et token ensemble : le client a demandé les deux le même jour. La clé seule ne sait pas qui agit ; le token seul ne sait pas quel programme appelle.

**Conséquences**

* **Code :** il n'y a aujourd'hui, dans `API/`, aucune route de connexion, aucun token, aucune clé d'API. Recherche refaite le 08/10/2026 sur `APIKeyHeader`, `api_key`, `auth/login`, `create_access_token`, `get_current_user`, `require_role`, `OAuth2PasswordBearer`, `jwt`, `token`, `Bearer` : 0 occurrence. Ce qui existe : le hachage Argon2 (`API/src/app/utils/security.py:20-32`), sa vérification à temps constant (`:35-49`), `needs_rehash` (`:52-60`), et le minimum de 12 caractères (`API/src/app/models/user_model.py:63`, testé dans `API/tests/test_user_models.py`).
* **Où brancher les contrôles :** les routes CRUD sortent d'une seule fabrique, `build_crud_router`. Une dépendance posée sur elle vaut pour toutes ses routes (`md/securite/tuto-2-authentification-jwt.md:387-409`).
* **Dépendance :** `API/requirements.txt` n'a aucune bibliothèque de token. Si le groupe retient JWT, il faut ajouter `pyjwt` (tuto 2, §2.1).
* **Les clés, comme les autres secrets du dépôt** (déduit de la pratique) : la valeur dans `docker/.env`, le nom seul dans `docker/.env.exemple`, comme `POSTGRES_PASSWORD` et `POSTGRES_READER_PASSWORD` (`docker/.env.exemple:14`, `:20`).
* **Générer la clé et la remettre au programme :** une micro-décision (« Pas pour les micro-décisions », `JOURNAL-DE-DECISIONS.md:13`), à écrire dans le README quand on codera. 💡 `openssl rand -hex 32`, comme pour le secret du JWT (tuto 2, `:139`) ; la valeur remise au responsable du programme, hors dépôt.
* **`docker/docker-compose.yml` :** le service `api` liste ses variables une à une (`docker-compose.yml:32-40`). Les clés et le secret du token y demandent donc une ligne chacun.
* **Limiter les essais de connexion :** déjà demandé par ADR-016, remis en vigueur (« prévoir du rate-limiting sur les endpoints d'authentification »).
* **Re-hacher après une connexion réussie :** déjà demandé par ADR-016 (`check_needs_rehash`). La fonction existe : `needs_rehash` (`security.py:52-60`).
* **Comptes repris de l'ancienne base :** leur faux mot de passe au préfixe `$2b$` n'est pas une empreinte Argon2. Ils ne peuvent pas se connecter, et c'est voulu (`security.py:42-44`). Le faux hash reste, documenté (`md/questions/questions-a-trancher.md:257`).
* **Plan de sécurité :** les étapes 4 à 8 de `md/securite/securite-mots-de-passe-et-droits.md` (`:390-394`) et le tuto 2 redeviennent d'actualité.
* **ADR-027 :** son contexte dit « l'authentification et le contrôle d'accès ne sont pas implémentés ». C'est faux depuis le 07/10. Il n'est que « proposé » : il se réécrit (`md/adr/2026-10-07-liste-adr-chantier-4.md:52-54`). Il doit citer ADR-028, et non ADR-026, pour l'authentification. Il passe de 4 à 5 rôles (`Reader`).
* **ADR-029 (lien chasseur → manager) :** le filtre « le manager voit ses chasseurs » devient codable avec ces outils.
* **Questions closes :** Q-JEF-21, Q-ACC-17 (12 caractères gardés), Q-ACC-18 (mot de passe gardé), Q-MIG-11 (faux hash gardé, documenté) (`questions-a-trancher.md:257`) ; Q-ACC-19 et Q-JEF-22 (`:258`).

**Questions tranchées par les sources**

| Question | Réponse | Source |
|---|---|---|
| Quels rôles ? | Les 5 de la base : `Admin`, `Client`, `Hunter`, `Manager`, `Reader`. `Reader` : « consulter dans l'API sans modifier » | `docker/init-v3/01_create_fil_rouge_immobilier.sql:164` ; `docker/init-v3/README.md:134` |
| Quels droits ? | Ceux que le groupe a répondus le 07/10 (Q-ACC-02 à 15). Ils vont dans ADR-027 réécrit, pas ici | `questions-a-trancher.md:241-252` ; `md/adr/2026-10-08-proposition-regroupement-adr.md:26` |
| Où ranger la clé ? | Dans `docker/.env`, ignoré par git, jamais dans le code. C'était dans la position que Jeff a validée « sans changement ». Le nom seul va dans `docker/.env.exemple`, comme les autres secrets (déduit) | `md/questions/2026-10-07-questions-pour-jeff.html`, carte Q-JEF-22 (position, réponse) ; `.gitignore:6` ; `CLAUDE.md`, règle 5 ; `docker/.env.exemple:14`, `:20` |
| Qui génère la clé ? | L'équipe : « clé d'api générée de votre côté » | `md/adr/adr-026-perimetre-authentification.md:51-52` |
| Combien de clés au départ ? | Deux, déduit : le client nomme deux programmes appelants, « l'api interne » et « le back de l'app » | `md/adr/adr-026-perimetre-authentification.md:48-49` ; carte Q-JEF-22 (« l'API interne, le back de l'app ») |
| La clé à chaque appel ? | Oui : « chaque programme qui appelle notre API montre sa clé, sinon il est refusé », validé par Jeff | carte Q-JEF-22 (« À lui dire », réponse du 07/10) |
| Un compte désactivé peut-il se connecter ? | Non, déduit : on désactive au lieu de supprimer, et un compte non dit activé ne l'est pas | Q-ACC-08 (`questions-a-trancher.md:183`) ; `01_create_fil_rouge_immobilier.sql:173` (`is_activated NOT NULL DEFAULT FALSE`) |

**Questions ouvertes** 🟡

1. **Quel token, quelle session ?** Un JWT signé, sans état côté serveur ; ou une session rangée en base ; et pour combien de temps ?
   * Où on a cherché (rédacteur, puis arbitre le 08/10/2026) :
     * le StarterPack : `jwt`, `token`, `oauth`, `bearer`, `session`, `authentif`, `login`, `connexion`, `jeton`, `expir`, `cookie`. Rien sur le sujet (deux mots « session » et « authentifie », hors sujet : `fixtures/Readme.md:56`, `GLOSSAIRE-METIER.md:10`) ;
     * le dépôt (`md/`, `livrables/`, `context AI/`, `API/README.md`, registre) : aucune décision du groupe. Le tuto 2 laisse le choix ouvert : « Ce tuto **propose** JWT ; il ne tranche pas » (`tuto-2-authentification-jwt.md:10-12`, `:91-107`, `:657`). Le plan du 22/09 partait sur JWT (`securite-mots-de-passe-et-droits.md:241-260`, étape 4 `:390` ; brouillon local d'ADR-026, `:29`), mais c'est une note « rédigée avec l'IA », qui « ne fait pas foi » (`securite-mots-de-passe-et-droits.md:7`) ; la même note propose 1 h sans le décider (`:370-371`) ; `context AI/08-etat.md:53` dit « token » sans choisir ;
     * le client dit « token, session » sans choisir.
   * Pourquoi ça ne suffit pas : aucune décision du groupe n'est écrite. Discord n'a pas été relu au-delà des notes du jour.
   * 💡 Proposition : un **JWT** signé en `HS256` avec `pyjwt`, la bibliothèque de la doc FastAPI (tuto 2, §2, source consultée le 22/09/2026) ; durée **60 minutes**, sans jeton de rafraîchissement (`securite-mots-de-passe-et-droits.md:370-371`) ; l'utilisateur **relu en base à chaque appel** (tuto 2, §5, `:370-383`). Ce dernier point corrige le défaut du JWT : un compte désactivé ou rétrogradé perd ses droits tout de suite, sans attendre l'expiration. La « session » de Jeff serait alors la durée de vie du token.
   * 💡 Ce choix mérite **son propre ADR** (tuto 2, `:105-106` : « ce choix mérite un ADR, avec sa durée d'expiration »). ADR-028 garde le périmètre ; le futur ADR fixera le mécanisme.

**Sources**

| Affirmation | Source |
|---|---|
| Réponse du client du 22/09 (« géré au dessus », clé d'API « générée de votre côté ») | `md/adr/adr-026-perimetre-authentification.md:42-43`, `:48-53` |
| Authentification rouverte, mot de passe gardé, Argon2 | `md/questions/questions-a-trancher.md:87`, `:257` |
| Citation de Jeff du 07/10 | `md/questions/2026-10-07-questions-pour-jeff.html`, carte Q-JEF-14 ; `questions-a-trancher.md:1169` |
| Mot de passe gardé (Q-JEF-21) | même fichier, carte Q-JEF-21 ; `questions-a-trancher.md:1173` |
| Une clé par programme, rangée dans `docker/.env` | même fichier, carte Q-JEF-22 ; `questions-a-trancher.md:188`, `:258` |
| Réponse du groupe « outils » (Q2) | `md/journal/2026-10-07-plan-action.html`, carte Q2 ; `questions-a-trancher.md:257` |
| Jeff est le PO | `questions-a-trancher.md:197` |
| 016 et 026 remis en vigueur | Laurence, Discord, 08/10/2026 (`md/adr/2026-10-08-notes-seance-adr.md:14`, `:25`) ; Confluence, pages 52592771 et 51578382, version 2 (cité par le premier jet, non revérifié) |
| ADR-016 : Argon2id, rate-limiting, `check_needs_rehash` | copie du journal Confluence du 07/10, ADR-016, « Décision » et « Conséquences » |
| ADR-026 : 12 caractères, sans composition | copie du journal Confluence du 07/10, ADR-026, « Décision » |
| 5 rôles, dont `Reader` | `docker/init-v3/01_create_fil_rouge_immobilier.sql:164` ; `docker/init-v3/README.md:125-143` |
| `is_activated NOT NULL DEFAULT FALSE` | `docker/init-v3/01_create_fil_rouge_immobilier.sql:173` |
| Pas de code d'authentification dans l'API | recherche du 08/10/2026 : 0 occurrence dans `API/` |
| Argon2 déjà codé ; comptes repris sans connexion | `API/src/app/utils/security.py:20-32`, `:42-44` |
| Une clé seule : « pas d'utilisateur, pas d'expiration » | `md/securite/tuto-2-authentification-jwt.md:99` |
| JWT ou session : non tranché ; « mérite un ADR » ; proposition 1 h | `tuto-2-authentification-jwt.md:10-12`, `:91-107`, `:657-658` ; `securite-mots-de-passe-et-droits.md:7`, `:370-371` |
| Secrets : valeur dans `.env`, nom dans `.env.exemple` | `docker/.env.exemple:14`, `:20` |
| Variables du service `api` listées une à une | `docker/docker-compose.yml:32-40` |
| « mot de passe (haché) » dans le registre RGPD du sujet | `documents utiles/REGISTRE-RGPD.md:28`, `:37` (StarterPack) |
| Le sujet ne parle ni de JWT, ni de token, ni de session | grep du StarterPack, 08/10/2026 (rédacteur, puis arbitre) : 0 occurrence utile |
| Modèle d'ADR, micro-décisions | `documents utiles/JOURNAL-DE-DECISIONS.md:13`, `:19-40` (StarterPack) |

> **Version complète, gardée en annexe.** Le livrable est la version courte : `livrables/4-application/note-securite-applicative.md` (2026-11-20).

# 🔐 Note de sécurité applicative — API Fil Rouge Immobilier

> **Note sécurité** (BC03).
> Exigée par `GRILLE-EVALUATION.md` (StarterPack - BASE) : « Sécurité applicative | Code + note sécurité ».
> `TRACABILITE-COMPETENCES.md:65` précise : « Extraits de code commentés + note sécurité ».
> Le bloc **BC04 cybersécurité** n'est pas au programme du projet (`Readme.md` l. 7, option BC05). Cette note décrit donc les **pratiques de sécurité du code**, pas un audit d'intrusion complet.
> État du code : dépôt `Fil-Rouge-API`, commit **`aa149c0`** (2026-11-20). Les extraits du § 2 ont été relevés sur `141d068` ; depuis, `utils/security.py` a seulement gagné la constante `MIGRATED_PASSWORD` (comptes repris, activation), sans toucher aux extraits. Rédigée par le Glaude ; § 3 rejoué le 2026-11-20. **À relire par l'équipe.**

---

## 1. Les protections en place

Chaque appel à l'API passe **deux contrôles**, qui ne se remplacent pas (ADR-028, point 6) :

- **la clé d'API** dit **quel programme** appelle ;
- **le jeton** dit **quelle personne** agit.

| Protection | Ce qu'elle empêche | Où dans le code | Décision |
| --- | --- | --- | --- |
| Mots de passe hachés avec **Argon2id** (environ 300 ms et 512 Mo par essai) | Lire les mots de passe en cas de vol de la base | `utils/security.py`, `hash_password` | ADR-016 |
| **Clé d'API** par programme (en-tête `X-API-Key`) | Un programme inconnu qui appelle l'API | `utils/api_keys.py`, `require_api_key` | ADR-028 |
| **Jeton JWT** signé, valable **60 min** | Agir sans s'être connecté | `utils/security.py`, `create_access_token` | ADR-052 |
| Compte et rôle **relus en base à chaque appel** | Garder ses droits après une désactivation | `utils/current_user.py`, `get_current_user` | ADR-052, décision 3 |
| **Droits par rôle**, et « le sien seulement » | Un client qui lit la fiche d'un autre client | `utils/roles.py`, `require_roles` | ADR-027 |
| **Même message** pour un email inconnu ou un mot de passe faux | Deviner quels emails ont un compte | `routes/auth_router.py`, `_BAD_CREDENTIALS` | ADR-052 |
| **Frein** aux essais en série : 5 échecs par email, 20 par IP, en 15 min | Essayer des mots de passe sans fin (force brute) | `utils/login_throttle.py` | 2026-11-19 |
| **Code d'activation** à usage unique, valable 7 jours | Un compte que seul un admin pouvait activer | `services/activation_service.py` | user story 01 |
| Requêtes SQL **paramétrées** (SQLModel) | L'injection SQL | `repositories/` | — |
| Effacement = **désactiver et anonymiser** | Garder des données personnelles en clair | `services/anonymization_service.py` | ADR-049 |
| **En-têtes de sécurité** sur chaque réponse ; nom du serveur caché | Qu'un navigateur devine le type d'un contenu, affiche l'API dans le cadre d'un autre site, ou garde une réponse en cache | `main.py`, `security_headers_middleware` | SEC-HEAD, 2026-11-20 |

Tous les chemins de ce tableau partent de `API/src/app/`.

---

## 2. Extraits de code commentés

### 2.1 Le mot de passe ne se compare jamais avec `==`

```python
# utils/security.py
def verify_password(stored: str, plain: str) -> bool:
    try:
        return _hasher.verify(stored, plain)   # comparaison à temps constant (argon2)
    except VerifyMismatchError:
        return False
    except InvalidHashError:
        spend_password_check(plain)            # même durée pour un compte sans mot de passe
        return False
```

- Un `==` répondrait plus vite quand les premiers caractères sont faux. Le chronomètre trahirait alors le mot de passe.
- `spend_password_check` : un email inconnu répond **aussi lentement** qu'un email connu. Le temps de réponse ne dit donc pas si un compte existe.

### 2.2 Le rôle se relit en base, jamais dans le jeton

```python
# utils/current_user.py
user = _users.get_by_id(session, decode_access_token(credentials.credentials))
if not user.is_activated:
    raise unauthorized(BAD_TOKEN)              # compte désactivé : refusé tout de suite
```

- Le jeton ne porte **que** l'identifiant du compte (`sub`).
- Un compte désactivé perd donc ses droits **au prochain appel**, sans attendre la fin de son jeton.

### 2.3 Le frein aux essais en série

```python
# routes/auth_router.py, POST /auth/login
for throttle, key in ((login_throttle.by_email, email_key), (login_throttle.by_ip, ip_key)):
    wait = throttle.retry_after(key)
    if wait is not None:
        raise _too_many(wait)                  # 429 + Retry-After, même avec le bon mot de passe
```

- Pendant le blocage, **même le bon mot de passe** est refusé. Sinon, l'attaquant saurait qu'il a trouvé.

### 2.4 Le code d'activation ne peut pas servir de jeton de connexion

```python
# utils/security.py
payload = {"sub": str(user_id), "aud": "activate", "iat": now, "exp": now + expires_delta}
```

- La bibliothèque `pyjwt` **refuse** un jeton qui porte un `aud` inattendu.
- Le code d'activation n'ouvre donc **pas** l'API. Dans l'autre sens, un jeton de connexion n'est pas non plus un code d'activation.

---

## 3. Les tests d'attaque

Gabriel a essayé **4 attaques** sur l'API (résultats rapportés le 2026-11-09) :

| Attaque | Résultat | Pourquoi ça tient |
| --- | --- | --- |
| Injection SQL | ✅ Tient | SQLModel envoie les valeurs **à part** de la requête. La seule requête écrite à la main (`estate_contact_repository.py:40`) passe aussi sa valeur en paramètre (`:cutoff`). |
| XSS (script glissé dans un champ) | ✅ Tient | L'API ne rend que du **JSON**, jamais de page HTML. |
| CSRF (requête forgée depuis un autre site) | ✅ Tient | Le jeton voyage dans l'en-tête `Authorization`, **pas dans un cookie** : le navigateur ne l'envoie pas tout seul. |
| Authentification | ❌ **Faille** | **15 mauvais mots de passe** d'affilée, aucun blocage. Seul Argon2 ralentissait (environ 430 ms par essai). |

➡️ **Faille corrigée le 2026-11-19** : c'est le frein du §2.3 (commit `e6f4b87`).

### 3.1 Rejoués le 2026-11-20 : méthode, requêtes, réponses

Les 4 attaques ont été **rejouées après la correction**, par un script qu'on peut relancer : `securite/attaques.py` (sortie brute : `securite/sortie-2026-11-20.txt`). Il envoie de vraies requêtes HTTP à l'API locale, dans le conteneur `api`, et n'écrit rien en base.

**Outil** : `httpx` (client HTTP Python), la clé d'API du conteneur, et un jeton de Manager fabriqué sur place (aucun mot de passe lu ni affiché).

| Attaque | Requête envoyée | Réponse | Verdict |
| --- | --- | --- | --- |
| Injection SQL, champ texte | `POST /auth/login`, email `' OR '1'='1' --`, mot de passe `x' OR '1'='1` | `401` | ✅ la chaîne est comparée comme un texte, pas lue comme du SQL |
| Injection SQL, chemin | `GET /estates/1 OR 1=1` | `422` | ✅ l'id doit être un entier : refusé **avant** la base |
| Injection SQL, requête empilée | `GET /estates/1;DROP TABLE estate` | `422` | ✅ idem ; la table est toujours là |
| XSS | `POST /auth/login`, email `<script>alert(1)</script>` | `401`, `application/json` | ✅ aucune réponse en HTML : rien à exécuter pour un navigateur |
| CSRF | `GET /estates/1` avec un cookie et une origine `https://site-pirate.example`, sans en-tête `Authorization` | `401` | ✅ le jeton n'est jamais un cookie (aucun `Set-Cookie` à la connexion), et aucun site tiers n'est autorisé (pas d'en-tête CORS) |
| Force brute | 15 × `POST /auth/login`, même email, mots de passe faux | `401` ×5, puis `429` ×10, `Retry-After: 300` | ✅ bloqué **au 6e essai**, pour 5 minutes |

**Bilan : 6 essais sur 6 tiennent.** La faille du 2026-11-09 (15 essais sans blocage) est fermée.

⚠️ Ce que ces essais ne couvrent pas : un outil d'audit automatique (OWASP ZAP, sqlmap), le Swagger `/docs` (seule page HTML, page de développement), et une attaque répartie sur plusieurs adresses IP (le frein par IP s'arrête à 20 échecs en 15 minutes).

---

## 4. Les preuves par les tests automatiques

- Toute la suite : **1 120 tests réussis**, 7 échecs attendus (`xfail`), **0 échec** (2026-11-20, conteneur `api`, après les en-têtes de sécurité).
- Les tests qui prouvent la sécurité :
  - `tests/test_login_throttle.py` : le frein (10 tests) ;
  - `tests/test_activation_token.py` et `tests/integration/test_activation.py` : le code d'activation (15 tests) ;
  - `tests/integration/test_droits_par_role.py` : **chaque route** a un test qui juge ses droits. Une route ajoutée sans ce test fait échouer la suite.
  - `tests/test_access_log.py` : aucun mot de passe, jeton ni email n'apparaît dans le journal d'accès.
  - `tests/test_security_headers.py` : les 4 en-têtes de sécurité sont sur les réponses 200, 401 et 404 (4 tests).

---

## 5. Limites connues

- ⚠️ Les compteurs du frein vivent **en mémoire** : un redémarrage les efface. C'est suffisant pour un seul conteneur `api`. Avec plusieurs, il faudrait un stockage partagé (Redis, par exemple).
- ⚠️ **Pas de serveur d'email** : le code d'activation est rendu au manager par l'API, pas envoyé par mail au client.
- ⚠️ **Pas de HTTPS** dans la pile Docker locale. En production, il faudrait un proxy TLS devant l'API.
- ⚠️ **Pas de jeton de rafraîchissement** : on se reconnecte toutes les 60 minutes. C'est un choix assumé (ADR-052), plus simple et plus sûr.

---

## 6. Ce que le cours aborde, point par point

> Ajouté le 2026-11-20 (choix SEC-COURS, accepté par Gabriel). Grille : les sommaires des 4 supports du cours (authentification, cryptographie, sécurité des applications par l'attaque, vulnérabilités), comparés au code de `Fil-Rouge-API` (`83b7c0d`). Chaque ligne « en place » se vérifie dans le fichier cité, depuis `API/src/app/`.

### 6.1 En place, sans être écrit plus haut

| Thème du cours | Ce que fait l'API | Où |
| --- | --- | --- |
| Contrôler un jeton reçu | L'algorithme est **figé** au décodage (`algorithms=["HS256"]`) : un jeton signé autrement, ou « sans signature », est refusé. Le jeton expiré est refusé | `utils/security.py`, `decode_access_token` |
| Clé secrète robuste | `JWT_SECRET` de **32 caractères au moins**, sinon l'API refuse de démarrer | `utils/security.py`, `_load_jwt_secret` |
| Politique de mot de passe (NIST 800-63B) | **12 caractères au moins**, aucune règle de complexité, aucun changement forcé : ce que recommande le NIST. ⚠️ Le seuil de 12 reste « à confirmer en réunion » (commentaire du code) | `models/user_model.py` |
| Ne rien exposer | Une erreur 500 rend un **message neutre et un numéro** ; la pile reste dans le journal | `main.py`, `internal_error_with_reference` |
| Fail-closed | Sans clé d'API valable, **tout est refusé**, avant même de lire le jeton | `utils/api_keys.py`, `require_api_key` |
| Défense en profondeur | Trois barrières qui ne se remplacent pas : la clé (le programme), le jeton (la personne), le rôle **relu en base** à chaque appel | § 1 |
| Broken Access Control (OWASP) | Le rôle est vérifié **côté serveur** sur chaque route ; la ligne d'un autre rend `404`, pas `403`, pour ne pas dire qu'elle existe | `utils/roles.py` (le rôle), les services (« le sien ») |
| Validation en entrée | Chaque corps et chaque paramètre est validé par un schéma : une valeur hors type rend `422` **avant** la base (§ 3.1) | modèles SQLModel |
| Minimisation et pseudonymisation | Effacer un compte = le désactiver et l'**anonymiser** | `services/anonymization_service.py`, ADR-049 |
| En-têtes de sécurité | **Posés le 2026-11-20** (SEC-HEAD, `aa149c0`) : `X-Content-Type-Options`, `X-Frame-Options`, `Cache-Control: no-store`, `Referrer-Policy` ; `server: uvicorn` retiré. ⚠️ Pas de `Content-Security-Policy` (elle casserait le Swagger), et une erreur 500 n'a pas ces en-têtes | `main.py`, `security_headers_middleware` ; `Dockerfile` |

### 6.2 Absent : les limites qu'on assume

| Thème du cours | Ce qui manque | Pourquoi, et ce qu'il faudrait |
| --- | --- | --- |
| MFA, passkeys | Pas de second facteur | Hors du sujet ; à prévoir pour les comptes Manager et Admin avant une mise en production |
| Révocation d'un jeton | Un jeton vit 60 min, sans liste noire | **En partie couvert** : un compte désactivé est refusé à l'appel suivant, car il est relu en base |
| Mots de passe fuités (NIST) | Aucune comparaison avec une liste de mots de passe connus | Possible sans envoyer le mot de passe (service à préfixe de hachage) ; non fait |
| Chiffrement au repos | La base et les sauvegardes MinIO ne sont pas chiffrées | Seuls les mots de passe sont protégés (Argon2) ; en production, chiffrer le disque et le bucket `backup` |
| Rotation des secrets | `JWT_SECRET` et les clés d'API ne changent jamais | Changer `JWT_SECRET` déconnecte tout le monde : à faire seulement sur soupçon de fuite, avec une procédure écrite |
| Composants vulnérables | Analyse **faite une fois** (2026-11-20, `pip-audit`, conteneur `api`) : **0 faille** dans les dépendances de `requirements.txt` ; **6 failles connues** dans `pip` 25.0.1, l'outil d'installation fourni par l'image `python:3.12-slim` (corrigées en 26.2), qui ne sert pas quand l'API tourne | Relancer `pip-audit` à chaque changement de dépendance, idéalement dans la CI ; mettre `pip` à jour dans le `Dockerfile` (choix SEC-PIP) |
| Limiter les ressources (OWASP API n° 4) | Seule la connexion a un frein ; les listes ne sont pas paginées (`GET /estates` rend 3 219 biens en 1,25 s) | Choix PAGIN, en attente |
| Réponse à incident | Les journaux d'accès vont dans Elasticsearch (on peut **détecter**) ; aucune marche à suivre pour **répondre** | À écrire avec le PCA/PRA |

### 6.3 Non concernés, et pourquoi

- **SSRF** : l'API ne va chercher **aucune** URL donnée par un utilisateur ; les photos sont des liens, jamais téléchargés par le serveur.
- **XXE** : l'API ne lit pas de XML, seulement du JSON.
- **Désérialisation dangereuse** : aucun `pickle` ni format qui exécute du code ; le JSON est validé par des schémas.
- **Prototype pollution** : propre au JavaScript ; l'API est en Python.
- **Sessions et cookies** (fixation, détournement, flags) : l'API n'a **pas de session** ni de cookie ; le jeton passe dans l'en-tête `Authorization`.


# 🔐 Note de sécurité applicative — API Fil Rouge Immobilier

> **Note sécurité** (BC03).
> Exigée par `GRILLE-EVALUATION.md` (StarterPack - BASE) : « Sécurité applicative | Code + note sécurité ».
> `TRACABILITE-COMPETENCES.md:65` précise : « Extraits de code commentés + note sécurité ».
> Le bloc **BC04 cybersécurité** n'est pas au programme du projet (`Readme.md` l. 7, option BC05). Cette note décrit donc les **pratiques de sécurité du code**, pas un audit d'intrusion complet.
> État du code : dépôt `Fil-Rouge-API`, commit **`83b7c0d`** (2026-11-20). Les extraits du § 2 ont été relevés sur `141d068` ; depuis, `utils/security.py` a seulement gagné la constante `MIGRATED_PASSWORD` (comptes repris, activation), sans toucher aux extraits. Rédigée par le Glaude ; § 3 rejoué le 2026-11-20. **À relire par l'équipe.**

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

- Toute la suite : **1 116 tests réussis**, 7 échecs attendus (`xfail`), **0 échec** (2026-11-19, conteneur `api`).
- Les tests qui prouvent la sécurité :
  - `tests/test_login_throttle.py` : le frein (10 tests) ;
  - `tests/test_activation_token.py` et `tests/integration/test_activation.py` : le code d'activation (15 tests) ;
  - `tests/integration/test_droits_par_role.py` : **chaque route** a un test qui juge ses droits. Une route ajoutée sans ce test fait échouer la suite.
  - `tests/test_access_log.py` : aucun mot de passe, jeton ni email n'apparaît dans le journal d'accès.

---

## 5. Limites connues

- ⚠️ Les compteurs du frein vivent **en mémoire** : un redémarrage les efface. C'est suffisant pour un seul conteneur `api`. Avec plusieurs, il faudrait un stockage partagé (Redis, par exemple).
- ⚠️ **Pas de serveur d'email** : le code d'activation est rendu au manager par l'API, pas envoyé par mail au client.
- ⚠️ **Pas de HTTPS** dans la pile Docker locale. En production, il faudrait un proxy TLS devant l'API.
- ⚠️ **Pas de jeton de rafraîchissement** : on se reconnecte toutes les 60 minutes. C'est un choix assumé (ADR-052), plus simple et plus sûr.

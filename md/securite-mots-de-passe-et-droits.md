# Mots de passe et droits d'accès — ce qu'il faut faire

> 📖 **Écrit pour tout le groupe, techniciens ou non.** Chaque notion est
> expliquée avant d'être utilisée. Aucune connaissance préalable demandée.
>
> ⚠️ **Note rédigée avec l'IA.** Elle ne fait pas foi : les sources sont au §9.
>
> 📅 22 septembre 2026. Correspond aux étapes `B1`, `B2` et `B3` du plan.

---

## 1. Le problème, en une image

Notre application a **24 comptes**. Aujourd'hui, deux choses clochent :

🔓 **Les mots de passe s'écrivent en clair.** C'est comme si, à l'hôtel, la
réception notait le code de ton coffre-fort sur un carnet posé sur le
comptoir. N'importe qui passant derrière le comptoir peut le lire.

🚪 **Toutes les portes sont ouvertes.** Il n'y a ni serrure, ni badge. Qui que
tu sois, tu peux consulter la paie de n'importe quel chasseur, les budgets de
n'importe quel client, les coordonnées de tout le monde.

**Ce document explique comment fermer ces deux trous.** Ce sont deux chantiers
différents, à faire dans l'ordre.

---

## 2. Où on en est exactement — mesuré le 22/09

### 2.1 Les chiffres

| Ce qu'on a vérifié | Résultat |
|---|---|
| Comptes dans la base | **24** — 18 clients, 6 chasseurs |
| Comptes « manager » | **0** ⚠️ |
| Comptes « admin » | **0** ⚠️ |
| Mots de passe protégés | ❌ **aucun** |
| Routes protégées dans l'API | ❌ **aucune** |
| Outil de protection installé | ❌ aucun |

### 2.2 Ce qui va mieux qu'on ne le croyait

✅ **Les 24 comptes existants ne sont pas en danger.**

Quand les données de l'ancien système ont été reprises, personne n'a inventé de
faux mots de passe. À la place, l'équipe a écrit dans chaque compte une valeur
volontairement inutilisable :

```
$2b$12$MIGRATED_PLACEHOLDER_MUST_RESET
```

🔒 **C'est une serrure bouchée à la colle.** Aucun mot de passe au monde ne
correspond à cette valeur. Personne ne peut entrer sur ces 24 comptes. C'était
le bon réflexe, et il est resté en place.

✅ **Deuxième bonne nouvelle** : l'API ne renvoie plus jamais le mot de passe
quand on lui demande la liste des comptes. C'était un bug, corrigé le 21/09.

### 2.3 Ce qui est pire qu'on ne le croyait

❌ **Tout compte créé aujourd'hui stocke son mot de passe en clair.**

Ce n'est pas une supposition. Le test a été fait le 22/09 :

| Étape | Résultat |
|---|---|
| 1. Créer un compte via l'API, mot de passe `MotDePasseEnClair123` | accepté |
| 2. Regarder ce que la base a gardé | **`MotDePasseEnClair123`** ❌ |
| 3. Supprimer le compte de test | fait, retour à 24 comptes |

➡️ **Le mot de passe est recopié tel quel, lisible par quiconque ouvre la
base.** Le placeholder protège le passé ; il ne protège rien de ce qu'on
écrira demain.

💡 C'est exactement ce qu'il faut montrer au groupe : le trou n'est pas
théorique, il est déjà ouvert.

---

## 3. Premier chantier — protéger les mots de passe

### 3.1 « Hacher », c'est quoi ?

🍓 **Imagine un smoothie.** Tu mets une fraise dans un mixeur. Tu obtiens un
liquide rose. Personne, même avec le meilleur matériel du monde, ne peut
reconstituer la fraise d'origine à partir du smoothie.

**Hacher un mot de passe, c'est ça.** On passe le mot de passe au mixeur, et on
ne garde **que le smoothie**. Le mot de passe d'origine, on ne le garde nulle
part.

### 3.2 Mais alors, comment vérifie-t-on ?

Question logique. La réponse est simple :

1. Tu tapes ton mot de passe pour te connecter.
2. L'application le passe **au même mixeur**.
3. Elle compare **les deux smoothies**.
4. S'ils sont identiques, c'est que c'était le bon mot de passe. ✅

➡️ À aucun moment l'application n'a eu besoin de connaître ton mot de passe.
Elle sait juste reconnaître son empreinte.

### 3.3 Pourquoi c'est important

Si quelqu'un vole notre base de données :

| Aujourd'hui | Après |
|---|---|
| Il lit tous les mots de passe | Il ne trouve que des smoothies |
| Il peut se connecter à la place de chacun | Il ne peut rien en faire |

💡 **Et ça dépasse notre appli.** Beaucoup de gens réutilisent le même mot de
passe partout. Un mot de passe volé chez nous ouvrirait aussi leur boîte mail.
C'est pour ça que ce n'est pas négociable.

### 3.4 Le petit truc en plus : le « sel »

Si deux personnes choisissent le même mot de passe, elles auraient le même
smoothie — et un voleur verrait qu'elles ont le même.

🧂 **Le sel**, c'est un ingrédient aléatoire ajouté à chaque mixage. Résultat :
même mot de passe, smoothies différents. Chacun est unique.

✅ **Bonne nouvelle** : l'outil qu'on a choisi fait ça tout seul. On n'a rien à
gérer.

### 3.5 L'outil est déjà choisi

⚠️ **Le point d'étape du 21/09 disait que ce choix restait à faire. C'est
faux** : la décision existe depuis le **4 septembre**.

`ADR-016` a retenu **Argon2id** — un mixeur reconnu comme le meilleur
aujourd'hui, recommandé par l'OWASP, l'organisme de référence en sécurité web.

Deux raisons de l'avoir préféré à son concurrent historique :

- 🐢 **Il est lent exprès.** Un mixeur trop rapide permet à un voleur d'essayer
  des milliards de mots de passe par seconde. Celui-ci est calibré pour prendre
  environ **un quart de seconde**. Invisible pour toi, ruineux pour un attaquant.
- 🧠 **Il consomme de la mémoire exprès.** Les cartes graphiques, qu'utilisent
  les pirates pour casser des mots de passe en masse, ont beaucoup de
  puissance mais peu de mémoire. Cet outil les prend à contre-pied.

✅ **Et la base est déjà prête** : la colonne qui stocke le mot de passe a déjà
la bonne taille pour accueillir un smoothie Argon2id.

✅ **Confirmé le 22/09** : on part bien sur **Argon2**. Le choix n'est plus en
discussion, il reste à l'appliquer — et à faire passer `ADR-016` de
« proposé » à « validé ».

⚠️ **Un petit détail à ne pas rater.** Le placeholder des 24 comptes commence
par `$2b$`, qui est la signature d'un **autre** mixeur, plus ancien, appelé
bcrypt. Ce n'est pas grave — la valeur est inutilisable de toute façon — mais
elle envoie un mauvais signal : on croit lire du bcrypt alors qu'on a décidé
Argon2. À remplacer par un placeholder cohérent quand on écrira les données de
démo.

### 3.6 Ce qu'il reste concrètement à faire

| # | Quoi | Pour les techniciens |
|---|---|---|
| 1 | Installer l'outil | ajouter `argon2-cffi` aux dépendances |
| 2 | Mixer à la création d'un compte | dans le service, jamais dans la route |
| 3 | Séparer ce qu'on reçoit de ce qu'on stocke | un modèle `UserCreate` d'entrée |
| 4 | Ne jamais écrire le mot de passe ailleurs | ni journal, ni cache, ni message d'erreur |

🟡 **À moitié fait** : le point 3 est déjà en place **dans un sens**. L'API ne
renvoie plus jamais le mot de passe. Il manque l'autre sens : ce qu'on accepte
en entrée.

---

## 4. Deuxième chantier — savoir qui est qui

⚠️ **Avant de décider ce que quelqu'un a le droit de voir, il faut savoir qui
il est.** C'est une étape à part entière, qu'on oublie souvent.

### 4.1 Le bracelet de festival

🎪 À l'entrée d'un festival, tu montres ta carte d'identité **une seule fois**.
On te donne un **bracelet**. Ensuite, à chaque scène, tu montres le bracelet —
pas ta carte.

C'est exactement ce qu'il nous faut :

1. Tu envoies ton email et ton mot de passe **une fois**.
2. L'application vérifie, et te renvoie un **bracelet électronique**.
3. À chaque demande suivante, ton navigateur montre le bracelet.

💡 **Pourquoi ne pas renvoyer le mot de passe à chaque fois ?** Parce qu'il
circulerait en permanence sur le réseau. Le bracelet, lui, **expire tout seul**
au bout d'un moment — et un bracelet volé ne donne pas le mot de passe.

### 4.2 Ce qu'il reste à faire

| # | Quoi |
|---|---|
| 1 | Une page de connexion : email + mot de passe → un bracelet |
| 2 | Chaque demande à l'API présente son bracelet |
| 3 | Une demande **sans** bracelet valide est refusée |

---

## 5. Troisième chantier — qui a le droit de voir quoi

Le bracelet dit **qui tu es**. Les droits disent **où tu peux aller**.

### 5.1 Nos quatre rôles

| Rôle | Qui c'est | Comptes aujourd'hui |
|---|---|---|
| `Client` | le particulier qui cherche un bien | **18** |
| `Hunter` | le chasseur immobilier | **6** |
| `Manager` | le responsable qui encadre des chasseurs | **0** ⚠️ |
| `Admin` | l'administrateur du système | **0** ⚠️ |

### 🆕 Le rôle `Admin` a été créé le 22/09

Il manquait, et c'est une drôle d'histoire.

Le schéma **autorisait** le mot « Admin » depuis le début. Mais la ligne
n'avait jamais été **écrite**. Autrement dit : le rôle était prévu au
règlement, mais n'existait nulle part. Impossible de nommer qui que ce soit
administrateur.

➡️ C'est corrigé : la base compte maintenant **quatre rôles**, et l'API les
affiche bien tous les quatre.

💡 **Pourquoi l'admin n'a pas de fiche d'identité, contrairement aux autres ?**
Un client, un chasseur et un manager ont chacun une fiche en base avec leur
nom, leur téléphone, leur société. L'admin, non — **et c'est voulu**. Un
administrateur n'a pas de métier immobilier : il ne cherche pas de bien, n'en
vend pas, n'encadre personne. Il n'a que des **droits**. Rien d'autre à
stocker sur lui.

⚠️ **Aucun compte admin n'a été créé**, volontairement. Créer un compte veut
dire écrire un mot de passe — qui serait aujourd'hui stocké en clair (§2.3).
**Le premier compte admin se crée après le hachage, pas avant.**

⚠️ **Et le manager reste à zéro.** C'est pourtant lui qui devrait consulter la
paie de ses chasseurs. Tant qu'aucun compte n'existe, cette règle ne peut être
**ni montrée, ni testée**.

### 5.2 Le piège à éviter absolument

C'est le point le plus important de tout ce document.

❌ **Le rôle ne suffit pas.**

Bruno et Sophie sont tous les deux chasseurs. Ils ont le **même rôle**. Si on
s'arrête au rôle, Bruno peut consulter la paie de Sophie.

✅ **Il faut donc deux vérifications, pas une :**

| Niveau | La question posée | Exemple |
|---|---|---|
| 1 | *Ton rôle a-t-il accès à ce type d'information ?* | un client n'a rien à faire dans les paies |
| 2 | *Est-ce que c'est **à toi** ?* | Bruno voit **sa** paie, pas celle de Sophie |

💡 Dans une soutenance, c'est exactement là que le jury appuie. « Un chasseur
peut-il voir la rémunération d'un collègue ? » Il faut pouvoir répondre non, et
le **montrer**.

### 5.3 Ce qu'il reste à faire

| # | Quoi |
|---|---|
| 1 | Remplir le tableau « qui voit quoi » (§6) |
| 2 | Vérifier le rôle sur chaque route |
| 3 | Vérifier l'appartenance sur les données personnelles |
| 4 | Prouver par des tests qu'un accès interdit est **refusé** |

---

## 6. Ce qu'il faut décider ensemble

Rien de technique ici. Ce sont des choix métier.

### 6.1 Le tableau à remplir

Une croix = « a le droit de voir ». Les cases 🟡 sont à trancher.

| Donnée | Client | Chasseur | Manager | Admin |
|---|---|---|---|---|
| Ses propres coordonnées | ✅ | ✅ | ✅ | ✅ |
| Les coordonnées d'un autre | ❌ | 🟡 ses clients ? | 🟡 | ✅ |
| Sa propre rémunération | — | ✅ | — | ✅ |
| La rémunération d'un autre chasseur | ❌ | ❌ | 🟡 les siens ? | ✅ |
| Le barème de commission | ❌ | 🟡 le sien ? | 🟡 | ✅ |
| Les biens et annonces | ✅ | ✅ | ✅ | ✅ |
| Son mandat | ✅ | ✅ | 🟡 | ✅ |

### 6.2 Les cinq questions

1. 👔 **Combien de comptes manager et admin crée-t-on ?** Aujourd'hui zéro des
   deux. Proposition : **un admin** et **deux managers**, pour pouvoir montrer
   qu'un manager voit ses chasseurs et pas ceux du voisin.
2. 🔗 **Comment sait-on qu'un chasseur dépend d'un manager ?** Le lien
   n'existe pas en base aujourd'hui. Il faut décider comment le créer — c'est
   la condition pour que la règle « son manager » veuille dire quelque chose.
3. ⏱️ **Combien de temps dure un bracelet ?** Une heure, une journée ? Court =
   plus sûr, mais il faut se reconnecter souvent.
4. 🔑 **Que fait-on des 24 comptes existants ?** Leur serrure est bouchée
   (§2.2), donc rien ne presse. Proposition : leur donner un vrai mot de passe
   mixé dans les données de démo, pour pouvoir se connecter en soutenance.
5. 📋 **Jusqu'où va-t-on ?** Inscription, changement de mot de passe, « mot de
   passe oublié » : chacun est un chantier en plus. Le sujet ne les demande
   pas explicitement.

---

## 7. Le plan, dans l'ordre

Chaque étape s'appuie sur la précédente. On ne peut pas sauter.

| # | Étape | Attend | Poids |
|---|---|---|---|
| 0 | ~~Créer le rôle `Admin`~~ | — | ✅ **fait le 22/09** |
| 1 | Installer Argon2id et mixer à la création | rien | 🟢 petit |
| 2 | Séparer l'entrée de la sortie | 1 | 🟢 petit |
| 3 | Créer la page de connexion et le bracelet | 2 | 🟠 moyen |
| 4 | Refuser toute demande sans bracelet | 3 | 🟠 moyen |
| 5 | Vérifier le rôle sur chaque route | 4 + le §6 rempli | 🟠 moyen |
| 6 | Vérifier l'appartenance des données | 5 | 🔴 le plus délicat |
| 7 | Les tests qui prouvent que ça bloque | base de test (`A2`) | 🟠 moyen |

⚠️ **Le vrai verrou est ailleurs.** L'étape 7 attend la **base de test isolée**
(étape `A2` du plan). Sans elle, chaque test abîmerait la vraie base. Tant
qu'elle n'existe pas, on peut écrire la sécurité, mais pas **prouver** qu'elle
tient — et en soutenance, seule la preuve compte.

💡 **Les étapes 1 et 2 sont indépendantes de tout.** Elles peuvent démarrer
aujourd'hui.

💡 **Les comptes manager et admin se créent entre l'étape 2 et l'étape 3** —
une fois le mixeur en place, jamais avant.

---

## 8. Ce que ça vaut en soutenance

### 8.1 Une correction importante à faire

⚠️ Le point d'étape du 21/09 affirme : *« Le cahier des charges demande que la
paie d'un chasseur ne soit visible que par lui et son manager. »*

**C'est imprécis, et c'est risqué de le dire tel quel.** En remontant à la
source, cette phrase vient d'un **exemple de rédaction** placé dans un modèle
de document à remplir — la section s'intitule d'ailleurs « Exigences non
fonctionnelles **(extrait)** ». Ce n'est pas une commande du client.

Si un jury vérifie, on se retrouve à avoir présenté un exemple pédagogique
comme une exigence contractuelle.

### 8.2 Le vrai argument, bien plus solide

Le **RGPD**, lui, est explicitement exigé, et le sujet écrit noir sur blanc que
ces exigences « ne sont **pas optionnelles** ; leur absence est pénalisante en
jury ». Il demande la protection des données **dès la conception**.

➡️ **Notre justification devient donc :** on restreint les accès parce que le
RGPD impose la minimisation, pas parce qu'une ligne d'exemple le suggérait. Et
c'est le groupe qui a arbitré le détail du « qui voit quoi » — d'où le tableau
du §6, à porter en ADR.

💡 C'est plus honnête, et bien plus difficile à attaquer.

### 8.3 Deux décisions à ouvrir

- `ADR-016` (Argon2id) est encore au statut **« proposé »** depuis le 4/09. À
  valider.
- Le tableau « qui voit quoi » mérite **son propre ADR**, une fois rempli.

---

## 9. Où vérifier

| Ce qui est affirmé | Source |
|---|---|
| Argon2id est choisi, via `argon2-cffi` | Confluence, *Journal de décisions*, `ADR-016` |
| La colonne mot de passe est déjà dimensionnée | `docker/init-v2/01_create_fil_rouge_immobilier.sql`, table `user` |
| Le placeholder des 24 comptes | `docker/init-v2/02_migration.sql`, bloc `1. USERS` |
| L'API ne renvoie plus le mot de passe | `API/src/app/models/user_model.py`, classe `UserPublic` |
| Rien ne mixe le mot de passe | `API/src/app/services/user_service.py` — 7 lignes, aucun traitement |
| Aucune authentification dans l'API | aucun fichier d'authentification dans `API/src/app/` |
| L'outil n'est pas installé | `API/requirements.txt` |
| Le rôle `Admin` manquait | `docker/migrations/2026-09-22_role_admin.sql` |
| Le RGPD n'est pas optionnel | `BASE/Readme.md`, section 🔐 RGPD |
| L'exigence sur les droits est un **exemple** | `BASE/documents utiles/CAHIER-DES-CHARGES-TECHNIQUE.md`, section « Exigences non fonctionnelles (extrait) » |

### 9.1 Revoir les quatre rôles

Depuis `docker/` :

```bash
docker exec fil_rouge_immobilier_db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT r.id, r.wording, count(u.id) FROM role r LEFT JOIN \"user\" u ON u.id_role = r.id GROUP BY r.id, r.wording ORDER BY r.id;"'
```

Attendu : **4 lignes** — Client 18, Hunter 6, Manager 0, Admin 0.

### 9.2 Refaire la preuve du mot de passe en clair

⚠️ Ces trois commandes **écrivent dans la base**, puis nettoient derrière
elles. La troisième n'est pas optionnelle.

**1.** Créer un compte de test :

```bash
curl -s -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"email":"test-preuve-hash@exemple.fr","password":"MotDePasseEnClair123","is_activated":true,"id_role":1}'
```

**2.** Lire ce que la base a gardé :

```bash
docker exec fil_rouge_immobilier_db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT id, email, password FROM \"user\" WHERE email = '"'"'test-preuve-hash@exemple.fr'"'"';"'
```

Attendu : **`MotDePasseEnClair123`**, en toutes lettres. C'est le problème.

**3.** Supprimer le compte de test — remplacer `NN` par l'`id` renvoyé
à l'étape 1 :

```bash
curl -s -X DELETE http://localhost:8000/users/NN
```

Attendu ensuite : **24 comptes**, comme avant.

---

## Mini-lexique

| Mot | En clair |
|---|---|
| **Hacher** | passer un mot de passe au mixeur, sans garder le fruit |
| **Sel** | un ingrédient aléatoire, pour que deux mots de passe identiques ne se ressemblent pas |
| **Argon2id** | le mixeur qu'on a choisi |
| **OWASP** | l'organisme de référence en sécurité des applications web |
| **Jeton (token)** | le bracelet de festival : une preuve qu'on s'est déjà identifié |
| **Authentification** | prouver **qui** on est |
| **Autorisation** | savoir **ce qu'on a le droit** de faire |
| **RGPD** | la loi européenne sur les données personnelles |
| **Minimisation** | n'accéder qu'aux données strictement nécessaires |
| **ADR** | une décision d'équipe écrite, sur Confluence |

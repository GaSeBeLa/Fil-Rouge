# ADR-026 — proposition à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À coller dans le *Journal de décisions
> (ADR)* de Confluence une fois relu par le groupe. Rien ne s'écrit sur
> Confluence depuis le dépôt.
>
> ⚠️ **Numéro à vérifier.** Il suit `ADR-025` (22/09/2026), lui-même encore au
> statut « proposé ».
>
> 💡 **Particularité de cet ADR :** la décision ne vient **pas** de l'équipe.
> Elle vient du **client**. L'équipe ne fait que l'acter et en tirer les
> conséquences.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

**ADR-026 : L'authentification est hors périmètre du projet**

**Date :** 22/09/2026
**Statut :** proposé
**Décideur :** le client (Jeff, formateur jouant le commanditaire)
**Acté par :** l'équipe projet

**Contexte**

Le MPD porte une table `role`, une colonne `user.email` et une colonne
`user.password`. L'équipe avait donc ouvert un chantier sécurité :
hachage Argon2id (`ADR-016`), puis authentification JWT et contrôle d'accès
par rôle. Le plan est décrit dans `md/securite-mots-de-passe-et-droits.md`
(étapes `B1` à `B3b`).

Aucune user story ne couvre l'authentification ni les droits d'accès.
L'équipe a demandé au client s'il fallait en ajouter.

**La réponse du client, le 22/09/2026 (Discord)**

À « rien n'est prévu dans les user-stories concernant leur authentification
et ce qu'ils peuvent faire sur l'application. Peut-on rajouter des
user-stories sur ces sujets ? » :

> « non »
> « vous ne gérez pas l'auth, c'est géré au dessus »

À « dans notre MPD on a email, mot de passe, une table rôle… comment on gère
ça du coup ? » :

> « on peut considérer que ça va être consommé par l'api interne et par le
> back de l'app directement »
> « on peut considérer que ça passe en local »
> « si vous voulez mettre quelque chose : prévoyez une simple vérification
> de provenance ou clé d'api générée de votre côté »
> « mais en soi, ça n'est pas directement demandé à ce stade »

**Cohérence avec l'énoncé**

La réponse ne contredit pas le sujet, elle le précise. Le `Readme.md` place
déjà le site web et le logiciel métier « **hors de votre scope** », et ne
confie à l'équipe que le backend exposant l'API. La couche qui authentifie
un utilisateur est donc, littéralement, au-dessus de nous.

**Décision**

1. **L'authentification n'est pas réalisée.** Pas de `POST /auth/login`,
   pas de JWT, pas de `get_current_user`.
2. **Le contrôle d'accès n'est pas implémenté.** Pas de `require_role`,
   pas de filtrage par appartenance, pas de tests `401` / `403`.
3. **L'API est considérée comme consommée en local**, par le back de
   l'application et l'API interne.
4. **Le modèle de données ne bouge pas.** `role`, `user.email` et
   `user.password` restent : le client dit qu'ils seront « consommés »,
   pas qu'ils sont inutiles.
5. **Le hachage des mots de passe est conservé** (`ADR-016`, déjà
   implémenté). Son motif change : ce n'est plus « pour se connecter »,
   c'est le *privacy by design* exigé par le sujet. Stocker un mot de passe
   en clair resterait indéfendable, authentification ou non.
6. **Le « qui accède à quoi » reste un livrable de conception.** Le sujet
   exige une note « souveraineté & sécurité des données » (BC05) qui
   réclame le périmètre d'accès et l'anonymisation, et pose le RGPD comme
   non optionnel. Le client a retiré l'implémentation, pas l'énoncé.

**Options envisagées**

- Option 1 : implémenter quand même l'authentification complète. Rejetée —
  le client dit explicitement que ce n'est pas demandé, et l'étape la plus
  lourde (filtrage par appartenance) est bloquée par l'absence de base de
  test isolée.
- Option 2 : retirer `password` et `role` du MPD. Rejetée — le client ne l'a
  pas demandé, et ces colonnes existent dans les fixtures d'origine.
- Option 3 : ne rien implémenter, conserver le modèle, et traiter les droits
  d'accès comme un livrable documentaire. **Retenue.**
- Option 4 : ajouter la clé d'API que le client propose. **Non tranchée** —
  il la présente comme facultative (« si vous voulez »). Voir questions
  ouvertes.

**Conséquences**

- Les étapes `4` à `8` du plan de `md/securite-mots-de-passe-et-droits.md`
  sont caduques, ainsi que `md/tuto-2-authentification-jwt.md`. Les deux
  documents sont conservés : leurs mesures et leur vocabulaire restent
  justes, et ils tracent une réflexion que le jury peut interroger.
- `md/matrice-droits-crud-par-role.md` change de statut : livrable de
  **conception**, plus backlog d'implémentation. Ses cases 🟡 restent à
  trancher, mais pour la documentation, pas pour du code.
- La motivation de l'`ADR-025` (lien chasseur → manager) s'affaiblit :
  elle s'appuyait sur le contrôle d'accès ENF-03, déjà identifié comme un
  simple exemple de rédaction. **La décision tient quand même** — c'est de
  la modélisation de données, et le MPD 03 4 la porte. Son argumentaire est
  à réécrire sans invoquer le contrôle d'accès.
- Les comptes `Manager` et `Admin` restent à créer, mais pour le **seed de
  démonstration**, plus pour se connecter.
- Charge de travail retirée : l'étape la plus lourde du chantier sécurité.

**Questions ouvertes**

1. ⚠️ **La question posée au client mélangeait deux sujets** :
   « l'authentification » **et** « ce qu'ils peuvent faire sur
   l'application ». Son « non » portait sur l'ensemble, mais sa
   justification ne parle que de l'authentification. **À lui faire
   préciser** avant de considérer les droits d'accès comme clos.
2. Garde-t-on `user.password` alors que personne dans notre périmètre ne
   l'utilise ? Le conserver oblige à le protéger ; le retirer s'écarte des
   fixtures.
3. Implémente-t-on la vérification de provenance / clé d'API proposée par
   le client ? Elle est petite, démontrable en soutenance, et explicitement
   sanctionnée — mais « pas directement demandée à ce stade ».

**Source**

Échange Discord du 22/09/2026, 15:21 à 15:36, entre l'équipe et le client.
Capture conservée par l'équipe.

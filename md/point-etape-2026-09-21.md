# Point d'étape et plan — 21 septembre 2026

> ⚠️ **Note rédigée avec l'IA.** Elle ne fait pas foi : en cas de doute, on
> remonte à la source. Chaque affirmation a son fichier et sa ligne au §10.
> Rien de ce qui est « à faire » ici n'est déjà codé.

---

## 1. En 30 secondes

- ✅ La base tourne : **18 tables**, tous les montants en **euros**.
- ✅ L'API tourne, avec une page pour la tester : http://localhost:8000/docs
- ✅ Deux bugs corrigés aujourd'hui (voir §3).
- ⚠️ **9 tables sur 18 sont vides** : tout ce qui touche à l'argent.
- ➡️ Prochaine étape : les remplir avec des données de démo.
- ➡️ Avant ça : **5 questions à trancher ensemble** (§5).

---

## 2. Où on en est

| Brique | État | En clair |
|---|---|---|
| Base PostgreSQL | ✅ | 18 tables, créées et remplies par `docker compose` |
| Données reprises de l'ancien système | ✅ | 24 comptes, 6 chasseurs, 18 clients, 17 mandats |
| Annonces | ✅ | 2 556 biens, 1 976 photos |
| API (lire, créer, modifier, supprimer) | ✅ | sur les 18 tables, 91 opérations vérifiées |
| Tests automatiques | ⚠️ | **un seul** : « l'API démarre » |
| Règles métier | ❌ | rien n'est codé : ni le calcul de la paie, ni les 6 mois, ni l'exclusivité |
| Connexion et droits d'accès | ❌ | n'importe qui peut tout lire |

**Les 9 tables vides** (mesuré aujourd'hui) :

- `visit` — les visites ;
- `estate_proposed` — les biens proposés et les offres ;
- `estate_searchrequest` — le lien bien ↔ recherche ;
- `sale` — les ventes ;
- `payment` — les paiements aux chasseurs ;
- `hunter_performance` — les scores des chasseurs ;
- `commission_scale` — le barème ;
- `parameters_fees` — les honoraires ;
- `real_estate_manager` — les managers.

**Les livrables** :

| Dossier | Contenu |
|---|---|
| `livrables/1-audit` | vide |
| `livrables/2-modelisation` | 3 rapports (chantier `C`, clos le 11/09) |
| `livrables/3-architecture` | vide |
| `livrables/4-application` | vide |

---

## 3. Ce qui a changé aujourd'hui

| Commit | Quoi |
|---|---|
| `d960992` | l'API couvre les 18 tables du nouveau schéma |
| `4ed58b3` | l'API se lance avec `docker compose`, Swagger inclus |
| `3b8f2a7` | 🐛 l'API en Docker répondait `500` si on avait un fichier `API/.env` |
| `8c0b93b` | 🔒 `/users` ne renvoie plus les mots de passe |

➡️ **À faire chez chacun**, depuis le dossier `docker/` :

```bash
git pull
docker compose up -d api
```

Le bug du `.env`, en une phrase : Docker embarquait le fichier `API/.env`,
qui dit « la base est sur `localhost` ». Vrai sur ton PC, **faux dans le
conteneur**. Maintenant le conteneur ne voit plus ce fichier. Merci Gabriel.

---

## 4. Le « seed », expliqué simplement

**Un seed**, ce sont des données de démo qu'on écrit nous-mêmes, pour que la
base ne soit pas vide.

🎭 **C'est un décor de théâtre.** Il rend la scène crédible. Il ne prouve pas
que la pièce est bonne.

| | Le décor | La preuve |
|---|---|---|
| C'est quoi | le seed | les tests |
| Ça sert à | montrer l'appli, faire la démo en soutenance | prouver que le calcul est juste |
| Fichier | `docker/init-v2/04_seed_demo.sql` (à écrire) | les tests automatiques (à écrire) |

Deux choses à retenir :

- 🧮 **Le sujet fournit déjà la calculette.** Une fonction Python qui calcule
  la paie du chasseur, avec **55 cas de test**. On n'a pas à l'inventer.
- ✋ **Aucun montant calculé à la main dans le seed.** Les paiements du seed
  sortent de la calculette. Sinon on risque une démo avec des chiffres faux.

Rappel : les chiffres du sujet (3 000 €, 2,5 %, barème de 30 à 50 %…) sont des
**propositions**, pas des règles imposées. Ce qui est imposé, c'est la forme du
calcul. En soutenance, on dit « valeur proposée, validée par le groupe ».

---

## 5. Les 5 questions à trancher ensemble

> 🗳️ **Position de Sébastien, arrêtée le 21/09 — à valider par le groupe.**
> Ce n'est pas encore une décision collective : l'étape **A1** du plan reste
> ouverte. Le détail de chaque question est conservé ci-dessous, inchangé.

| # | La question | Réponse retenue |
|---|---|---|
| 1 | Date de début du barème | **Reculer à 2025** — le barème démarre au 01/01/2025 |
| 2 | Quel score entre dans un paiement | **Le score de cette vente**, comme le sujet |
| 3 | Chasseur sans droit à sa paie | **Ajouter la colonne « motif »** à `payment` — option **B** |
| 4 | Biens de la démo | **Créer 3 à 5 biens fictifs** à Montpellier |
| 5 | Mandat renouvelé | **La vente pointe vers le nouveau mandat** |

⚠️ **La réponse 3 change le plan.** Elle ne se contente pas du seed : elle
impose un **changement de schéma** sur `payment` (colonne de motif, et
contrainte `base_rate > 0` à assouplir). Donc un **ADR** et une modification de
`docker/init-v2/01_create_fil_rouge_immobilier.sql` **avant** l'étape A4.
Nouvelle étape **A3 bis** au §6.


### Question 1 — 📅 À quelle date commence le barème ?

- **Le problème.** Dans le code d'exemple du sujet, le barème commence le
  **1er janvier 2026**. Nos 3 mandats terminés datent de **2025**. Une vente
  de 2025 ne trouverait **aucun barème** → le calcul plante.
- **Option A.** Faire commencer le barème plus tôt (par exemple 2025-01-01).
  C'est un paramètre : on a le droit.
- **Option B.** Garder 2026, et placer les ventes de démo en 2026, sur
  d'autres mandats.
- 💡 **Suggestion : A.** Plus simple, et ça garde les 3 mandats terminés.

### Question 2 — 🧮 Quel score entre dans un paiement ?

- **Le problème.** Le chasseur a un score de 0 à 100, qui fait monter ou
  baisser sa paie. Deux lectures existent.
- **Option A — le score de cette vente.** C'est ce que fait le sujet. Pour
  Bruno : le délai de **cette** vente, les visites de **cette** vente, plus
  son activité des 12 derniers mois **sans compter** la vente en cours.
  Résultat : 73,5 sur 100.
- **Option B — le score courant du chasseur.** C'est ce que dit notre note
  `schema-tracabilite…_v4.md`.
- 💡 **Suggestion : A, suivre le sujet.** Bonus : plus besoin d'inventer un
  « score de départ », que le sujet ne définit nulle part.

### Question 3 — 🧾 Que fait-on quand le chasseur n'a pas droit à sa paie ?

- **Le problème.** Le sujet veut qu'on garde **la raison** du refus (mandat
  expiré, client qui a trouvé seul…). Notre table `payment` n'a **aucune
  colonne** pour ça, et elle interdit un taux à zéro.
- **Option A.** Dans le seed : une vente refusée = une vente **sans** ligne
  de paiement. Ça marche dès aujourd'hui.
- **Option B.** Ajouter une colonne « raison du refus » à `payment`. C'est un
  changement de schéma, donc une décision d'équipe (ADR).
- 💡 **Suggestion : A pour le seed, et ouvrir B comme décision à part.**

### Question 4 — 🏠 Quels biens vend-on dans la démo ?

- **Le problème.** Nos 3 clients aux mandats terminés cherchaient à
  **Montpellier** (Écusson, Beaux-Arts, Port Marianne), pour 320 000, 280 000
  et 550 000 €. Or nos 2 556 biens sont à Toulouse, Annecy, Nantes et
  Limoges. Et le plus cher vaut **406 042 €**.
- **Option A.** Écrire à la main 3 à 5 biens fictifs à Montpellier.
- **Option B.** Vendre des biens existants, sans se soucier de la ville.
  Incohérent : un jury le verra.
- 💡 **Suggestion : A.**

### Question 5 — 🔁 Mandat renouvelé : la vente se rattache à quel mandat ?

- **Le problème.** Un mandat dure 6 mois. S'il est renouvelé, il y a **deux**
  mandats : l'ancien et le nouveau. Une vente ne peut pointer que vers **un**.
  C'est le cas de Bruno dans le sujet. Notre rapport du 11/09 avait déjà noté
  la question, sans la fermer.
- **Option A.** La vente pointe vers le **nouveau** mandat, celui qui est
  valable le jour de la vente. Le délai se compte quand même depuis la
  **première** signature, en remontant au mandat d'origine.
- **Option B.** La vente pointe vers l'**ancien** mandat.
- 💡 **Suggestion : A.** Elle respecte la règle « la vente est signée pendant
  la validité du mandat ».

---

## 6. Le plan

### Partie A — le seed

| # | Étape | Qui | Attend |
|---|---|---|---|
| A0 | Corriger 4 citations dans nos fichiers | Sébastien | rien |
| A1 | Trancher les 5 questions du §5 | **tout le groupe** | rien |
| A2 | Monter une base **de test**, séparée de la vraie | Sébastien | rien |
| A3 | Reprendre la calculette du sujet et ses 55 tests | Sébastien | A2 |
| A3 bis | Motif de refus sur `payment` : ADR + schéma (suite Q3) | le groupe | A1 |
| A4 | Écrire le seed `04_seed_demo.sql` | Sébastien | A1 et A3 |
| A5 | Décider quoi faire des 4 défauts du §7 | le groupe | rien |
| A6 | Un générateur de **gros volume** | plus tard, Phase 3 | A3 |

Détails utiles :

- **A0.** Nos fichiers citent `user-stories/10_calcul_remuneration_chasseur.feature`
  comme s'il était dans le dépôt. Il n'y est **pas** : il vit dans le
  StarterPack BASE. Et on y appelle le barème « officiel », alors qu'il est
  « proposé ».
- **A2.** Tant qu'il n'y a pas de base de test, chaque test abîmerait la vraie
  base. C'est le premier verrou du projet.
- **A6.** Le sujet demande une note d'indexation (avant / après) et une note
  de dimensionnement. Il faudra donc beaucoup de lignes — mais **plus tard**,
  et pas dans le seed de démo.

### Partie B — la sécurité de l'API

| # | Étape | Attend |
|---|---|---|
| B1 | **Hacher** les mots de passe à l'enregistrement (les brouiller, sans retour possible) | le choix de l'outil, par le groupe |
| B2 | Séparer « ce qu'on envoie » de « ce qui est stocké » pour un compte | B1 |
| B3 | Connexion + droits par rôle | A2 |

- ⚠️ Aujourd'hui, un mot de passe envoyé à l'API est stocké **en clair**.
- ⚠️ Aujourd'hui, **aucune route n'est protégée**. Le cahier des charges
  demande que la paie d'un chasseur ne soit visible que par lui et son manager.
- 🔎 Les 24 mots de passe repris de l'ancien système sont des faux. Rien à
  convertir.

**Ordre conseillé :** A0 et A5 tout de suite → A1 en réunion → A2 → A3 → A4.

---

## 7. Quatre défauts trouvés dans la reprise des données

Ils sont **mesurés**, pas corrigés. Un seed ne doit pas les cacher.

| # | Le défaut | Le chiffre | En clair |
|---|---|---|---|
| 1 | Le secteur de recherche a disparu | ville vide sur **17 critères sur 17** | on ne sait plus où les clients cherchent |
| 2 | Budget mini = budget maxi | **17 sur 17** | chercher « entre mini et maxi » ne trouve rien |
| 3 | Téléphones inventés `0000000000` | **3 clients** | Petit, Andre, Lambert |
| 4 | Mandats « actifs » mais déjà finis | **6 mandats** au 25/07/2026 | `MAND-0004`, `0007`, `0009`, `0010`, `0011`, `0012` |

- Le n° 4 est **le piège du consultant**, présent dans les données d'origine.
  À garder tel quel : c'est un **constat d'audit**, à mettre dans le livrable 1.
- Le n° 1 vient de notre script : l'ancienne table `secteurs` (10 lignes) n'a
  pas été reprise.

---

## 8. Les règles du décor

- 📅 Des dates **fixes**, pensées au **25 juillet 2026** (la date de référence
  du sujet). Jamais « la date du jour ».
- 👤 Que des personnes **fictives**.
- 🔢 Le barème s'écrit avec une borne haute **exclue** : de `0` à `200000`,
  pas de `0` à `199999`. Sinon un bien à 199 999,50 € n'a aucune tranche.
- 🧮 Les paiements sortent de la calculette (§4).
- 🧱 Le seed respecte **déjà** les règles pas encore codées : mandat de 6 mois
  pile, taux final entre 20 % et 60 %, ancienneté par pas de 2 %, vente signée
  avant la fin du mandat, paiement au chasseur du mandat, 2 jours entre deux
  scores d'un même chasseur. Sinon il cassera le jour où on les code.
- 🪜 Ordre d'écriture : honoraires et barème → visites → offres → ventes →
  paiements → scores.

---

## 9. Ce qui n'a PAS été vérifié

- ❌ **Confluence n'a pas pu être lu** aujourd'hui (le connecteur ne répondait
  pas). Ce qui est dit ici des décisions d'équipe vient du rapport du 11/09,
  pas des pages ADR.
- ❌ Le seed n'est pas commencé.
- ❌ Rien de la partie B n'est commencé.

---

## 10. Où vérifier

`BASE/` = `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/`
`REGLES` = `BASE/documents utiles/REGLES-CALCUL-REMUNERATION.md`
`feature 10` = `BASE/user-stories/10_calcul_remuneration_chasseur.feature`

| Ce qui est affirmé | Fichier | Ligne |
|---|---|---|
| Les chiffres sont des propositions | feature 10 | 3-5 |
| idem | REGLES | 59 |
| Date de référence : 25 juillet 2026 | `BASE/Readme.md` | 308 |
| Barème proposé (bornes à 199999…) | feature 10 | 23-27 |
| Chez nous, la borne haute est exclue | `docker/init-v2/01_create_fil_rouge_immobilier.sql` | 672, 775-777 |
| Le barème d'exemple commence le 2026-01-01 | REGLES | 646 |
| Pas de barème → erreur | REGLES | 493, 520 |
| Exemple de Bruno (73,5 · 46,16 % · 6 231,60 €) | REGLES | 237-254 |
| Deux critères portent sur la vente en cours | REGLES | 139 |
| Ventes des 12 mois « hors vente en cours » | REGLES | 470 |
| Notre note dit « score courant » | `md/schema-tracabilite-remuneration-chasseur_v4.md` | 74 |
| L'équipe avait déjà posé la question du score | `livrables/2-modelisation/09-contraintes-a-coder.md` | 163 |
| Garder la raison du refus | REGLES | 100, 322, 497 |
| Secteurs d'origine (Montpellier…) | `BASE/fixtures/PgSQL.sql` | 41-51 |
| Les 3 mandats terminés | `BASE/fixtures/PgSQL.sql` | 136, 138, 140 |
| Secteurs non repris | `docker/init-v2/02_migration.sql` | 62 |
| Téléphones inventés | `docker/init-v2/02_migration.sql` | 121 |
| Bruno = mandat renouvelé (décision D3) | `livrables/2-modelisation/09-decisions-a-prendre.md` | 122 |
| « Vers quel mandat pointe la vente ? » | idem | 164 |
| Le jumeau de Bruno, sans renouvellement | feature 10 | 45-50 |
| 55 cas de test fournis | REGLES | 724 |
| Un test repart toujours d'un état propre | `BASE/documents utiles/Gherkin.md` | 996 |
| Deux niveaux de test demandés | `BASE/documents utiles/PLAN-DE-TESTS.md` | 15-16 |
| Notes d'indexation et de dimensionnement | `BASE/documents utiles/GRILLE-EVALUATION.md` | 28, 30 |
| Pas de données personnelles réelles | `BASE/documents utiles/ORGANISATION-DEPOT.md` | 55 |
| La paie : visible du chasseur et de son manager | `BASE/documents utiles/CAHIER-DES-CHARGES-TECHNIQUE.md` | 97 |
| Règles pas encore codées | `livrables/2-modelisation/09-rapport-ecarts-contraintes.md` | 505, 512, 526, 560, 562, 631 |

**Refaire les mesures du §7.** Ouvrir `psql` dans le conteneur de la base :

```bash
docker exec -it fil_rouge_immobilier_db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

Puis coller, une requête à la fois :

```sql
-- défauts 1 et 2 : attendu 17 | 0 | 17
SELECT count(*) AS total,
       count(town) AS avec_ville,
       count(*) FILTER (WHERE budget_min = budget_max) AS mini_egal_maxi
FROM criteria;

-- défaut 3 : attendu 3
SELECT count(*) FROM client WHERE phone_number = '0000000000';

-- défaut 4 : attendu 6 lignes
SELECT reference, ends_at
FROM mandate
WHERE status = 'active' AND ends_at < DATE '2026-07-25'
ORDER BY reference;

-- question 4 : 4 villes, prix maxi 406042.00
SELECT town, count(*), max(price) FROM estate GROUP BY town ORDER BY 2 DESC;
```

`\q` pour sortir.

---

## Mini-lexique

| Mot | En clair |
|---|---|
| **Seed** | des données de démo, écrites par nous |
| **Mandat** | le contrat entre le client et le chasseur, valable 6 mois |
| **Honoraires** | ce que le client paie à l'entreprise : un fixe + un pourcentage du prix |
| **Barème** | la part des honoraires qui revient au chasseur, selon le prix du bien |
| **Tranche** | une ligne du barème : « de tant à tant, c'est tel taux » |
| **Borne exclue** | « jusqu'à 200 000 **non compris** » |
| **Score** | la note du chasseur, de 0 à 100 |
| **Hacher** | brouiller un mot de passe de façon irréversible : même nous, on ne peut plus le lire |
| **ADR** | une décision d'équipe écrite, sur Confluence |
| **Swagger** | la page web qui permet de tester l'API à la souris |

# Rapport des changements — séance du 21 septembre 2026

> ⚠️ **Note rédigée avec l'IA.** Elle ne fait pas foi : en cas de doute, on
> remonte à la source. Chaque affirmation a son fichier au §8.
>
> 📅 Séance de 16:16 à 17:02. Fait suite au point d'étape du même jour.

---

## 1. En 30 secondes

- ✅ La base sait désormais enregistrer **pourquoi** un chasseur n'a pas été payé.
- ✅ **7 commits**, 12 fichiers, 867 lignes ajoutées.
- ✅ Testé sur une vraie base PostgreSQL : **10 cas sur 10**.
- ✅ Confluence a enfin pu être lu — le point d'étape disait le contraire.
- ⚠️ La décision qui justifie tout ça n'est **pas encore validée** par le groupe.
- ➡️ Il reste les 3 diagrammes, et la validation en réunion.

---

## 2. Le changement principal — `payment` sait dire non

### 2.1 Le problème

Toutes les ventes n'ouvrent pas un droit à rémunération. Le sujet impose de
garder **la raison** du refus, et désigne même l'endroit : « stocker le motif
du droit refusé dans `paiements` ».

Notre table ne pouvait rien enregistrer de tel. **Quatre verrous**, et non un
seul — c'est ce qui a fait passer ce point du simple « seed » à un vrai
changement de schéma :

| # | Le verrou | Ce qu'il empêchait |
|---|---|---|
| 1 | Aucune colonne de motif | le motif n'avait nulle part où aller |
| 2 | `base_rate` obligatoire et `> 0` | un refus n'a pas de taux → ligne rejetée |
| 3 | Aucun statut « refusé » | rien ne disait qu'un droit était fermé |
| 4 | Barème obligatoire | un refus aurait dû désigner une tranche, ce qui n'a pas de sens |

### 2.2 Ce qui a été fait

| # | Changement |
|---|---|
| 1 | État `refused` ajouté aux statuts |
| 2 | Colonne `refusal_reason`, limitée à `mandate_expired` et `out_of_scope` |
| 3 | Taux et barème deviennent **facultatifs** (4 colonnes) |
| 4 | Contrainte `chk_refused` ajoutée |

Les deux motifs ne sont **pas inventés** : ils viennent de l'énumération
`MotifRefus` fournie par le sujet, traduits en anglais comme le veut `ADR-002`.

### 2.3 Le vrai gain

`chk_refused` interdit les demi-mesures :

- ❌ Un refus qui porterait un taux → **rejeté**
- ❌ Un refus sans motif → **rejeté**
- ❌ Un paiement réel sans barème → **rejeté**

💡 Résultat : la base rend **impossible** de confondre « refusé » et « pas
encore payé ». C'est l'erreur qui aurait coûté le plus cher, et elle est
maintenant hors d'atteinte.

💡 Et comme une vente n'accepte qu'une ligne de paiement, une vente porte
**soit** un paiement, **soit** un refus. Jamais les deux.

### 2.4 Une bonne surprise

Les bornes des règles (`base_rate > 0`, ancienneté entre 0 et 10 %…) **n'ont
pas eu à bouger**. En PostgreSQL, une règle de validation ignore les cases
vides : il suffisait de rendre la colonne facultative. La règle métier reste
intacte, mot pour mot.

---

## 3. Les mesures

Rien n'a été pris pour acquis. Une base PostgreSQL 16 jetable a été montée
pour tout vérifier.

| # | Cas testé | Attendu | Obtenu |
|---|---|---|---|
| 1 | refus « mandat échu », montant 0 | accepté | ✅ |
| 2 | refus « hors dispositif » | accepté | ✅ |
| 3 | refus **sans** motif | rejeté | ✅ |
| 4 | refus **avec** un taux | rejeté | ✅ |
| 5 | refus **avec** un montant | rejeté | ✅ |
| 6 | refus, motif inventé | rejeté | ✅ |
| 7 | paiement **sans** barème | rejeté | ✅ |
| 8 | paiement **avec** un motif de refus | rejeté | ✅ |
| 9 | paiement complet | accepté | ✅ |
| 10 | deux lignes sur la même vente | rejeté | ✅ |

**10 sur 10**, et deux fois plutôt qu'une :

- sur une base **créée à neuf** avec le script modifié ;
- sur une base **existante**, mise à jour par le script de migration.

➡️ **Les deux voies donnent exactement le même comportement.** C'est ce qui
garantit qu'un équipier qui migre et un équipier qui recrée auront la même base.

Le script de migration a aussi été passé **deux fois de suite** sans erreur :
le relancer par erreur ne casse rien.

Côté API : elle démarre, `/payments` répond `200`, et la documentation Swagger
expose bien la nouvelle colonne.

---

## 4. Ce qui a changé ailleurs

### 4.1 Le fichier `.env` a déménagé

- ❌ Avant : `API/.env exemple` — décrivait un fichier à poser dans `API/`.
- ✅ Après : `docker/.env.exemple` — au bon endroit, celui que lit `docker compose`.

➡️ **Action pour chacun**, une seule fois, depuis `docker/` :

```bash
git pull
cp .env.exemple .env
```

Puis mettre ses propres mots de passe dans `docker/.env`. Sans ce fichier, la
base refuse de démarrer.

### 4.2 Un dossier de migrations est né

`docker/migrations/` contient le script pour les bases **déjà créées**.

- ⚠️ Ce dossier **n'est pas monté** par `docker compose` : le script ne part
  jamais tout seul, il se lance à la main.
- 💡 Si tu peux refaire ta base à zéro, tu n'en as pas besoin : le script de
  création contient déjà tout.

---

## 5. Ce que Confluence a appris

Le point d'étape du matin disait « Confluence n'a pas pu être lu ». C'était un
faux diagnostic : un seul appel échouait, pas le connecteur. **Le wiki est
lisible.**

Trois choses en sont sorties :

### 5.1 Une étape du plan était déjà faite

`B1` attendait « le choix de l'outil de hachage, par le groupe ». Or `ADR-016`
l'avait déjà tranché le **4 septembre** : Argon2id, via `argon2-cffi`. Et la
colonne `password` est déjà au bon format.

➡️ `B1` n'attend plus rien. Il reste à écrire le code.

### 5.2 Huit décisions dorment

`ADR-016` à `ADR-023` sont toutes au statut **« proposé »**. La plus ancienne
date du 4 septembre. Aucune n'a bougé depuis le 11.

⚠️ Huit décisions structurantes non validées, c'est le reproche le plus facile
à formuler en soutenance.

### 5.3 Le cahier des charges audite le mauvais schéma

Le *Cahier des Charges Technique* v2.0, mis à jour le 21/09 à 08:56, analyse
`docker/init/` — l'**ancien** schéma, 12 tables, montants en K€. Le projet
tourne sur `docker/init-v2/` : **18 tables, tout en euros**.

Conséquences :

| Le CDC déclare | La réalité |
|---|---|
| 🔴 6 tables « critiques » absentes | elles **existent** dans le schéma v2 |
| 🔴 « bloquant » : pas de ville sur la demande | `criteria.town` existe |
| 🔴 « bloquant » : pas de typologie sur le bien | `estate.typology` existe |
| §5 : prix en K€ | la règle du projet dit **euros** |

⚠️ Ses renvois aux ADR sont aussi décalés d'un rang.

💡 Rien n'est perdu : le §12 reste juste **sur l'ancien schéma**. C'est la
cible de l'audit qu'il faut corriger.

---

## 6. Les décisions prises — et leur statut réel

| # | La question | Réponse | Statut |
|---|---|---|---|
| 1 | Date de début du barème | reculer à 2025 | ⚠️ position perso |
| 2 | Quel score dans un paiement | celui de cette vente | ⚠️ position perso |
| 3 | Paie refusée | colonne « motif » ajoutée | ⚠️ position perso |
| 4 | Biens de la démo | biens fictifs à Montpellier | ⚠️ position perso |
| 5 | Mandat renouvelé | la vente vise le nouveau | ⚠️ position perso |
| — | `ADR-024` | rédigé | ⚠️ « proposé » |

⚠️ **Rien de tout cela n'est validé par le groupe.** C'est écrit noir sur blanc
dans chaque fichier concerné. Le schéma applique déjà la décision 3 : si le
groupe tranche autrement, c'est le commit `4a66906` qu'il faut défaire.

---

## 7. Ce qui reste ouvert

| Quoi | Qui | Bloqué par |
|---|---|---|
| Valider les 5 réponses et `ADR-024` | le groupe | réunion |
| Dépiler les 8 ADR « proposé » | le groupe | réunion |
| Publier `ADR-024` sur Confluence | Sébastien | rien |
| Reprendre les 3 diagrammes MCD/MLD/MPD | Sébastien | rien |
| Prévenir Békanty du décalage du CDC | Sébastien | rien |
| Monter la base de test (`A2`) | Sébastien | **rien** |
| Écrire les tests automatiques | — | `A2` |
| Écrire le seed (`A4`) | — | `A1`, `A3` |

💡 **`A2` reste le premier verrou.** Elle ne dépend d'aucune validation, et
débloque tout le reste.

⚠️ Un TODO ancien **n'est pas fermé** par ce travail : rien ne vérifie encore
qu'un paiement va au bon chasseur, ni que le barème était en vigueur à la date
de l'acte. `ADR-024` *enregistre* un refus, il ne le *calcule* pas.

---

## 8. Où vérifier

| Ce qui est affirmé | Fichier |
|---|---|
| Le schéma modifié | `docker/init-v2/01_create_fil_rouge_immobilier.sql`, table `payment` |
| Le script pour base existante | `docker/migrations/2026-09-21_adr-024_payment_refusal.sql` |
| Le modèle de l'API | `API/src/app/models/payment_model.py` |
| Les 10 mesures, en détail | `docker/init-v2/README.md` §8 |
| La décision et ses options | `md/adr-024-motif-refus-remuneration.md` |
| Le détail des modifications | `md/adr-024-modifications-a-faire.md` |
| Les 5 réponses | `md/point-etape-2026-09-21.md` §5 |
| Ce qui reste à faire à la main | `md/a-faire-a-la-main-2026-09-21.md` |

**Les 7 commits de la séance :**

| Heure | Commit | Quoi |
|---|---|---|
| 16:16 | `a45e003` | les 5 réponses, et l'étape `A3 bis` |
| 16:21 | `9ed95c0` | l'`ADR-024` proposé |
| 16:27 | `8684b7f` | le détail des modifications |
| 16:30 | `133d7d6` | la liste des étapes manuelles |
| 16:32 | `175d399` | le `.env` déplacé vers `docker/` |
| 16:36 | `3fb7bea` | l'`ADR-024` raccourci |
| 17:02 | `4a66906` | l'application en base |

**Refaire les mesures soi-même** — base jetable, sans toucher à la sienne :

```bash
docker run --rm -d --name verif -e POSTGRES_PASSWORD=test -e POSTGRES_DB=verif postgres:16
docker cp docker/init-v2/01_create_fil_rouge_immobilier.sql verif:/tmp/01.sql
docker exec verif psql -U postgres -d verif -v ON_ERROR_STOP=1 -f /tmp/01.sql
docker rm -f verif
```

Attendu : **0 erreur, 18 tables**.

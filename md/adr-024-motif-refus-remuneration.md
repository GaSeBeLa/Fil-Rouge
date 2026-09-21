# ADR-024 — proposition à relire avant publication

> 📋 **Ce fichier est un brouillon, pas un ADR publié.** Il est écrit pour être
> **collé tel quel** dans le *Journal de décisions (ADR)* de Confluence, une
> fois relu par le groupe. Rien ne s'écrit sur Confluence depuis le dépôt.
>
> ⚠️ **Le numéro est à vérifier.** Le journal s'arrête à `ADR-023` (11/09/2026),
> donc le suivant est `ADR-024`. Mais le *Cahier des Charges Technique* v2.0
> renvoie à une numérotation décalée d'un rang — il appelle `ADR-017` le
> hachage Argon2, que le journal numérote `ADR-016`. À trancher avant de poser
> le numéro.

---

**ADR-024 : Traçabilité du refus de rémunération du chasseur (table `payment`)**

**Date :** 21/09/2026
**Statut :** proposé
**Décideurs :** L'équipe projet

**Contexte**

Toutes les ventes n'ouvrent pas un droit à rémunération pour le chasseur. Le
document `REGLES-CALCUL-REMUNERATION.md` du Starter Pack ferme le droit dans
deux cas, et **impose d'en conserver la raison** :

> « Le refus retourne un **motif**, jamais un simple `False` : le §4 impose de
> tracer *pourquoi* le droit est fermé, pour pouvoir répondre au chasseur et
> pour rouvrir le débat de la décision D2 sans perdre l'historique. »
> — `REGLES-CALCUL-REMUNERATION.md`, ligne 497

Le même document désigne nommément l'emplacement attendu : « d'où l'intérêt de
stocker le **motif** du droit refusé dans `paiements` » (ligne 100). Sa
décision `D2` retient « Rien (R = 0), mais motif tracé » (ligne 322).

Les deux motifs sont fournis par le sujet, et ne sont donc pas à inventer
(ligne 385) :

```python
class MotifRefus(Enum):
    MANDAT_EXPIRE   = "mandat échu à la date de l'acte"
    HORS_DISPOSITIF = "mandat non-exclusif et vente hors dispositif"
```

En cas de refus, la calculette du sujet renvoie `Remuneration(droit_ouvert=False,
motif_refus=motif)` — **sans honoraires, sans taux, sans barème** (ligne 611).

Or la table `payment` livrée ne peut rien enregistrer de tel. Quatre verrous, et
non un seul :

| # | Le verrou, dans `01_create_fil_rouge_immobilier.sql` | Ce qu'il empêche |
|---|---|---|
| 1 | Aucune colonne de motif | Le motif n'a nulle part où aller |
| 2 | `base_rate NOT NULL CHECK (base_rate > 0 …)` | Un refus n'a pas de taux : la ligne est rejetée |
| 3 | `status IN ('announced','invoice_submitted','verified','scheduled','paid')` | Aucun état ne dit « refusé » |
| 4 | `id_commission_scale INTEGER NOT NULL` | Un refus devrait désigner une tranche de barème, ce qui n'a pas de sens |

**Options envisagées**

| # | Option | Ce qu'elle coûte, ce qu'elle perd |
|---|---|---|
| 1 | **Ne rien stocker** : une vente refusée n'a aucune ligne `payment`. | Aucun changement de schéma. Mais le motif est perdu : on ne peut ni répondre au chasseur, ni rouvrir `D2`. Contredit deux fois le sujet. |
| 2 | **Une ligne `payment` en état « refusé »**, portant le motif, sans taux ni barème. | Modifie `payment` : une colonne, un statut, trois contraintes assouplies, une contrainte de cohérence. |
| 3 | **Une table séparée** `payment_refusal`, liée à `sale`. | `payment` reste intacte, mais deux tables répondent alors à « ce chasseur a-t-il été payé pour cette vente ? ». Le sujet dit `paiements`, pas une table à côté. |
| 4 | **Porter le motif sur `sale`.** | Mélange la vente et la rémunération : `sale.sale_origin` décrit la vente, le refus décrit le droit du chasseur. Deux sujets distincts. |

**Décision**

Option 2 retenue. Le refus devient une **ligne de `payment` à part entière**, en
état `refused`, portant son motif et aucun montant.

```sql
-- 1. Un état de plus
status VARCHAR(20) NOT NULL
       CHECK (status IN ('refused', 'announced', 'invoice_submitted',
                         'verified', 'scheduled', 'paid')),

-- 2. Le motif, repris des deux valeurs du sujet
refusal_reason VARCHAR(30)
       CHECK (refusal_reason IN ('mandate_expired', 'out_of_scope')),

-- 3. Le barème devient facultatif
id_commission_scale INTEGER REFERENCES commission_scale(id) ON DELETE RESTRICT,

-- 4. Les taux deviennent facultatifs (bornes inchangées)
base_rate        NUMERIC(5,4) CHECK (base_rate > 0 AND base_rate <= 1),
seniority_rate   NUMERIC(5,4) CHECK (seniority_rate BETWEEN 0 AND 0.10),
performance_rate NUMERIC(5,4) CHECK (performance_rate BETWEEN -0.20 AND 0.20),

-- 5. Un refus et un paiement ne se ressemblent jamais à moitié
CONSTRAINT chk_refused
    CHECK ((status =  'refused'
            AND refusal_reason      IS NOT NULL
            AND amount              = 0
            AND base_rate           IS NULL
            AND seniority_rate      IS NULL
            AND performance_rate    IS NULL
            AND final_rate          IS NULL
            AND id_commission_scale IS NULL)
        OR (status <> 'refused'
            AND refusal_reason      IS NULL
            AND base_rate           IS NOT NULL
            AND seniority_rate      IS NOT NULL
            AND performance_rate    IS NOT NULL
            AND id_commission_scale IS NOT NULL))
```

Correspondance avec le sujet, en anglais conformément à `ADR-002` :

| Motif du sujet | Valeur en base |
|---|---|
| `MANDAT_EXPIRE` — mandat échu à la date de l'acte | `mandate_expired` |
| `HORS_DISPOSITIF` — mandat non-exclusif et vente hors dispositif | `out_of_scope` |

**Justification**

Le sujet ne laisse pas le choix de l'emplacement : il écrit « dans `paiements` ».
L'option 3 rangerait la même information ailleurs, et ferait coexister deux
tables pour une seule question. L'option 1, la plus économe, est la seule qui
perde précisément la donnée que le sujet demande de garder.

Une ligne de refus n'est pas un paiement à zéro : c'est un **événement de
droit**, daté, motivé, opposable au chasseur qui réclame. La contrainte
`chk_refused` lui interdit d'emprunter les attributs d'un vrai paiement — pas de
taux, pas de barème, pas de date de versement. Elle rend donc impossible la
confusion entre « refusé » et « pas encore payé », la seule erreur vraiment
coûteuse ici.

`id_sale` est déjà `UNIQUE` : une vente porte **soit** un paiement, **soit** un
refus, jamais les deux. La contradiction est interdite par le schéma, pas
seulement par la discipline.

Enfin, cette forme garde `D2` ouverte. Si le groupe décide plus tard une
indemnité forfaitaire plutôt que zéro, il suffira d'assouplir `amount = 0` dans
`chk_refused` : l'historique des refus sera déjà là, motif compris.

**Conséquences**

- **Base de données :** `payment` modifiée dans
  `docker/init-v2/01_create_fil_rouge_immobilier.sql`. Trois colonnes passent de
  `NOT NULL` à facultatif ; aucune donnée existante n'est concernée, la table
  est **vide** à ce jour. Un `COMMENT ON COLUMN` doit documenter
  `refusal_reason` et renvoyer à cet ADR.
- **Développement :** le modèle SQLModel `Payment` de l'API suit. Les trois taux
  et le barème deviennent `Optional`. Toute écriture passe par `chk_refused` :
  un refus se crée en une fois, jamais par modifications successives.
- **Seed de démo :** une vente sans droit s'écrit désormais comme une ligne
  `payment` en `refused`, et non comme une vente sans paiement. Cela change
  l'étape `A4` du plan du 21/09.
- **Tests :** deux cas au minimum, un par motif, plus un cas négatif vérifiant
  qu'un `refused` porteur d'un taux est bien rejeté par la base.
- **Limite assumée :** les deux motifs sont figés dans un `CHECK`. En ajouter un
  demandera une migration. Une table de référence serait plus souple, mais le
  sujet n'en définit que deux — inutile d'outiller une variabilité qui n'existe
  pas (voir la page *YAGNI / KISS* de l'espace).

**Sources**

| Affirmation | Fichier | Ligne |
|---|---|---|
| Le refus retourne un motif, jamais `False` | `REGLES-CALCUL-REMUNERATION.md` | 497 |
| Stocker le motif dans `paiements` | idem | 100 |
| `D2` : rien (R = 0), mais motif tracé | idem | 322 |
| Les deux valeurs de `MotifRefus` | idem | 385 |
| Un refus ne porte ni honoraires ni taux | idem | 611 |
| Les quatre verrous de `payment` | `docker/init-v2/01_create_fil_rouge_immobilier.sql` | table `payment` |
| Code et schéma en anglais | Journal de décisions | `ADR-002` |

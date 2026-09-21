# ADR-024 — les modifications à faire, en détail

> ✅ **APPLIQUÉ le 21/09/2026.** Ce fichier décrivait ce qu'il fallait changer ;
> tout a été fait et **vérifié sur PostgreSQL 16** — 10 cas de test sur 10,
> sur base neuve et sur base migrée. Il reste utile comme trace de ce qui a
> bougé et pourquoi.
>
> ⚠️ **Mais `ADR-024` est toujours au statut « proposé ».** Le groupe ne l'a
> pas validé. Si la décision change, c'est le §2 qu'il faut défaire.
>
> 📍 Où c'est fait :
> - schéma : `docker/init-v2/01_create_fil_rouge_immobilier.sql`, table `payment`
> - base existante : `docker/migrations/2026-09-21_adr-024_payment_refusal.sql`
> - API : `API/src/app/models/payment_model.py`
> - mesures : `docker/init-v2/README.md` §8
>
> ❌ **Pas encore fait** : les trois diagrammes MCD/MLD/MPD (§6) et les tests
> automatiques (§7), qui attendent la base de test isolée (étape `A2`).
>
> Compagnon de [`adr-024-motif-refus-remuneration.md`](./adr-024-motif-refus-remuneration.md).

---

## 1. En un coup d'œil

| Où | Quoi | Effort |
|---|---|---|
| `01_create_fil_rouge_immobilier.sql` | 1 colonne, 1 statut, 3 contraintes assouplies, 1 contrainte ajoutée | ~20 lignes |
| Le même fichier, section `COMMENT ON` | 1 commentaire de colonne | 2 lignes |
| `API/src/app/models/payment_model.py` | 4 champs passent en `Optional`, 1 champ ajouté | ~6 lignes |
| Schémas MCD / MLD / MPD (draw.io, Confluence) | 1 attribut sur l'entité paiement | 3 diagrammes |
| Base déjà créée chez un équipier | `ALTER TABLE` ou recréation | voir §5 |

✅ **Aucune donnée n'est en jeu** : la table `payment` est vide à ce jour.

---

## 2. Le SQL — table `payment`

Fichier `docker/init-v2/01_create_fil_rouge_immobilier.sql`, **lignes 684 à 720**.

### 2.1 Les cinq changements

| # | Ligne | Aujourd'hui | Demain |
|---|---|---|---|
| 1 | 689-691 | `status` sans état de refus | `'refused'` ajouté en tête de liste |
| 2 | — | *(colonne absente)* | `refusal_reason` ajoutée après `paid_at` |
| 3 | 694 | `base_rate … NOT NULL CHECK (…)` | `NOT NULL` retiré |
| 4 | 705-706 | `seniority_rate` et `performance_rate` `NOT NULL` | `NOT NULL` retiré sur les deux |
| 5 | 709 | `id_commission_scale INTEGER NOT NULL` | `NOT NULL` retiré |
| 6 | 711-713 | `chk_paid` seule | `chk_refused` ajoutée à côté |

⚠️ **Les bornes des `CHECK` ne bougent pas.** `base_rate > 0`, `seniority_rate
BETWEEN 0 AND 0.10`, `performance_rate BETWEEN -0.20 AND 0.20` restent
identiques. En PostgreSQL, un `CHECK` ne s'applique pas à une valeur `NULL` :
retirer le `NOT NULL` suffit, sans toucher à la règle.

### 2.2 Le bloc à écrire

```sql
CREATE TABLE payment (
    id                  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at          TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    -- Euros, arrondi au centime au demi supérieur (règle officielle).
    -- Vaut 0.00 sur une ligne de refus (ADR-024, décision D2 « R = 0 »).
    amount              NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    -- 'refused' : le droit à rémunération est fermé, le motif est en
    --   refusal_reason et la ligne ne porte ni taux ni barème (ADR-024).
    status              VARCHAR(20) NOT NULL
                        CHECK (status IN ('refused', 'announced',
                                          'invoice_submitted',
                                          'verified', 'scheduled', 'paid')),
    paid_at             TIMESTAMP,
    -- Motif du droit refusé. Les deux valeurs viennent de l'énumération
    --   MotifRefus du sujet (REGLES-CALCUL-REMUNERATION.md l. 385), en
    --   anglais conformément à ADR-002 :
    --     mandate_expired  <- MANDAT_EXPIRE   « mandat échu à la date de l'acte »
    --     out_of_scope     <- HORS_DISPOSITIF « mandat non-exclusif et vente
    --                                            hors dispositif »
    refusal_reason      VARCHAR(30)
                        CHECK (refusal_reason IN ('mandate_expired',
                                                  'out_of_scope')),
    -- Taux de tranche issu du barème. NULL sur une ligne de refus.
    base_rate           NUMERIC(5,4) CHECK (base_rate > 0 AND base_rate <= 1),
    -- TODO (R21) — le taux final est borné entre 20 % et 60 % par la règle
    --   officielle (10_calcul_remuneration_chasseur.feature:201 ; exemples
    --   l. 236-250 : 65 % ramené à 60 %, 17,60 % remonté à 20 %).
    --   Le CHECK ci-dessous accepte tout entre 0 et 1. À remplacer par :
    --       CHECK (final_rate BETWEEN 0.20 AND 0.60)
    --   L'en-tête du Gherkin précise que ces bornes sont des paramètres
    --   « proposés, non imposés » : d'où la prudence, mais la règle de bornage,
    --   elle, est bien métier.
    final_rate          NUMERIC(5,4) CHECK (final_rate > 0 AND final_rate <= 1),
    -- Majoration d'ancienneté, modulation de performance (décision D2).
    -- NULL sur une ligne de refus.
    seniority_rate      NUMERIC(5,4) CHECK (seniority_rate BETWEEN 0 AND 0.10),
    performance_rate    NUMERIC(5,4) CHECK (performance_rate BETWEEN -0.20 AND 0.20),
    id_sale             INTEGER NOT NULL UNIQUE REFERENCES sale(id) ON DELETE RESTRICT,
    id_hunter           INTEGER NOT NULL REFERENCES hunter(id_user) ON DELETE RESTRICT,
    -- NULL sur une ligne de refus : un droit fermé ne désigne aucune tranche.
    id_commission_scale INTEGER REFERENCES commission_scale(id) ON DELETE RESTRICT,

    CONSTRAINT chk_paid
        CHECK ((status =  'paid' AND paid_at IS NOT NULL)
            OR (status <> 'paid' AND paid_at IS NULL)),

    -- ADR-024 — un refus et un paiement ne se ressemblent jamais à moitié.
    --   Empêche les deux erreurs qui coûteraient cher : un « refusé » qui
    --   porterait des taux (donc lisible comme un paiement en attente), et
    --   un paiement réel sans barème ni taux (donc inexplicable après coup).
    CONSTRAINT chk_refused
        CHECK ((status =  'refused'
                AND refusal_reason      IS NOT NULL
                AND amount              =  0
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

    -- TODO (U01/U04, R01-R04, T17) — le droit à être payé n'est pas vérifié :
    --   testé, on peut aujourd'hui payer un chasseur qui n'est PAS celui du
    --   mandat de la vente, et rattacher le paiement à un barème qui n'était
    --   pas en vigueur à la date de l'acte. Croise payment, sale, mandate et
    --   commission_scale -> trigger à la création du paiement, ou API.
    --   ADR-024 ne ferme PAS ce TODO : il enregistre le refus, il ne le
    --   calcule pas. Le calcul du droit reste à faire (trigger ou API).
);
```

### 2.3 Le commentaire de colonne

À ajouter dans la section `COMMENT ON`, **après la ligne 781** (juste après
`COMMENT ON COLUMN payment.amount`) :

```sql
COMMENT ON COLUMN payment.refusal_reason IS
  'Motif du droit refuse (ADR-024) ; NULL si le droit est ouvert.';
```

---

## 3. Ce que la contrainte `chk_refused` garantit

| Tentative d'écriture | Résultat |
|---|---|
| `refused` + motif + `amount = 0`, tout le reste `NULL` | ✅ acceptée |
| `refused` **sans** motif | ❌ rejetée |
| `refused` avec un `base_rate` renseigné | ❌ rejetée |
| `refused` avec `amount = 1500.00` | ❌ rejetée |
| `scheduled` avec un `refusal_reason` | ❌ rejetée |
| `paid` sans barème | ❌ rejetée |
| `paid` + taux + barème + `paid_at` | ✅ acceptée |

💡 Deux garde-fous déjà en place et **inchangés** :

- `chk_paid` — seul un `paid` porte une date de versement. Un refus a donc
  forcément `paid_at` à `NULL`, sans rien ajouter.
- `id_sale` est `UNIQUE` — une vente porte **soit** un paiement, **soit** un
  refus. Jamais les deux, jamais deux fois.

---

## 4. L'API — `payment_model.py`

Fichier `API/src/app/models/payment_model.py`, **lignes 33 à 42**.

```python
    # status : NOT NULL + CHECK cote base — 'refused', 'announced',
    # 'invoice_submitted', 'verified', 'scheduled', 'paid'.
    status: str = Field(max_length=20)
    paid_at: Optional[datetime] = None
    # Motif du droit refuse (ADR-024) : 'mandate_expired' ou 'out_of_scope'.
    # Renseigne si et seulement si status vaut 'refused'.
    refusal_reason: Optional[str] = Field(default=None, max_length=30)
    # Les taux sont des NUMERIC(5,4) : 0.3000 vaut 30 %.
    # Tous NULL sur une ligne de refus (contrainte chk_refused).
    base_rate: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=4)
    final_rate: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=4)
    seniority_rate: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=4)
    performance_rate: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=4)
    id_sale: int = Field(foreign_key="sale.id")
    id_hunter: int = Field(foreign_key="hunter.id_user")
    id_commission_scale: Optional[int] = Field(default=None, foreign_key="commission_scale.id")
```

➡️ Et compléter l'en-tête du module : les quatre taux sont désormais
facultatifs, et une ligne de refus n'en porte aucun.

⚠️ **Effet de bord à connaître.** Rendre ces champs `Optional` fait que l'API
accepte un paiement **sans** taux ni barème. C'est la base qui refusera, via
`chk_refused` — donc une erreur `500` plutôt qu'un `422` propre. Une
validation applicative reste à écrire dans `payment_service.py` : c'est le
même chantier que le TODO `U01/U04` déjà posé dans le schéma.

---

## 5. Appliquer le changement

### Cas 1 — base recréée (le cas normal)

Les scripts de `docker/init-v2/` ne s'exécutent qu'à la **création** du volume.
Il faut donc repartir de zéro :

```bash
docker compose down -v
docker compose up -d
```

⚠️ `-v` **supprime le volume**, donc toutes les données. C'est sans
conséquence aujourd'hui — les données viennent entièrement des scripts —
mais ce ne sera plus vrai une fois le seed enrichi à la main.

### Cas 2 — base existante à modifier sur place

```sql
BEGIN;

ALTER TABLE payment ADD COLUMN refusal_reason VARCHAR(30);

ALTER TABLE payment ADD CONSTRAINT chk_refusal_reason
    CHECK (refusal_reason IN ('mandate_expired', 'out_of_scope'));

ALTER TABLE payment DROP CONSTRAINT payment_status_check;
ALTER TABLE payment ADD CONSTRAINT payment_status_check
    CHECK (status IN ('refused', 'announced', 'invoice_submitted',
                      'verified', 'scheduled', 'paid'));

ALTER TABLE payment ALTER COLUMN base_rate           DROP NOT NULL;
ALTER TABLE payment ALTER COLUMN seniority_rate      DROP NOT NULL;
ALTER TABLE payment ALTER COLUMN performance_rate    DROP NOT NULL;
ALTER TABLE payment ALTER COLUMN id_commission_scale DROP NOT NULL;

ALTER TABLE payment ADD CONSTRAINT chk_refused
    CHECK ((status =  'refused'
            AND refusal_reason      IS NOT NULL
            AND amount              =  0
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
            AND id_commission_scale IS NOT NULL));

COMMENT ON COLUMN payment.refusal_reason IS
  'Motif du droit refuse (ADR-024) ; NULL si le droit est ouvert.';

COMMIT;
```

⚠️ **Le nom `payment_status_check` est à vérifier** avant de lancer : c'est le
nom que PostgreSQL génère automatiquement, mais il n'est pas garanti. Pour le
lire :

```sql
SELECT conname, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'payment'::regclass AND contype = 'c';
```

---

## 6. Les schémas MCD / MLD / MPD

Les trois diagrammes vivent sur Confluence, page *Schémas - MCD/MLD/MPD Cible*,
en draw.io. Ils sont à reprendre **à la main**.

| Schéma | Ce qui change |
|---|---|
| **MCD** | Entité `PAIEMENT` : ajouter l'attribut *motif de refus*. Le statut existe déjà, seule sa liste de valeurs s'allonge. |
| **MLD** | `PAIEMENT` : ajouter `refusal_reason`. Marquer `base_rate`, `seniority_rate`, `performance_rate` et `id_commission_scale` comme **facultatifs** — c'est le vrai changement de lecture, la cardinalité vers `BAREME` passe de 1,1 à 0,1. |
| **MPD** | `refusal_reason VARCHAR(30)`, les quatre colonnes en *nullable*, et la contrainte `chk_refused` en note. |

💡 Le point à ne pas rater : sur le MLD, le lien `PAIEMENT → BAREME` **cesse
d'être obligatoire**. C'est ce qu'un jury regardera, plus que la colonne.

---

## 7. Les tests à écrire

Ils supposent la base de test isolée — étape `A2` du plan, toujours ouverte.

| # | Le cas | Attendu |
|---|---|---|
| 1 | Refus `mandate_expired`, `amount = 0`, reste `NULL` | ✅ inséré |
| 2 | Refus `out_of_scope`, idem | ✅ inséré |
| 3 | Refus **sans** motif | ❌ rejeté par `chk_refused` |
| 4 | Refus portant un `base_rate` | ❌ rejeté |
| 5 | Refus avec `amount > 0` | ❌ rejeté |
| 6 | Paiement normal sans `id_commission_scale` | ❌ rejeté |
| 7 | Deux lignes sur la même vente | ❌ rejeté par `id_sale UNIQUE` |

Les cas 3 à 7 sont des **tests négatifs** : ils prouvent que la base refuse.
Sans eux, la contrainte n'est pas testée, seulement écrite.

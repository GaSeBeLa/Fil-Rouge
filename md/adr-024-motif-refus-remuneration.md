# ADR-024 — proposition à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À coller dans le *Journal de décisions
> (ADR)* de Confluence une fois relu par le groupe. Rien ne s'écrit sur
> Confluence depuis le dépôt.
>
> ⚠️ **Numéro à vérifier.** Le journal s'arrête à `ADR-023` (11/09/2026), donc
> le suivant est `ADR-024`. Mais le *Cahier des Charges Technique* v2.0 renvoie
> à une numérotation décalée d'un rang — il appelle `ADR-017` le hachage
> Argon2, que le journal numérote `ADR-016`.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

**ADR-024 : Traçabilité du refus de rémunération du chasseur**

**Date :** 21/09/2026
**Statut :** proposé
**Décideurs :** L'équipe projet

**Contexte**

Toutes les ventes n'ouvrent pas un droit à rémunération pour le chasseur. Le
document `REGLES-CALCUL-REMUNERATION.md` impose de conserver la raison du
refus — « Le refus retourne un **motif**, jamais un simple `False` » (l. 497) —
et désigne l'emplacement attendu : « stocker le motif du droit refusé dans
`paiements` » (l. 100). Sa décision `D2` retient « Rien (R = 0), mais motif
tracé » (l. 322). Les deux motifs sont fournis et n'ont pas à être inventés
(l. 385) : `MANDAT_EXPIRE` et `HORS_DISPOSITIF`. En cas de refus, la calculette
du sujet ne renvoie ni honoraires, ni taux, ni barème (l. 611).

La table `payment` livrée ne peut rien enregistrer de tel. Quatre verrous, et
non un seul : aucune colonne de motif ; `base_rate NOT NULL CHECK (base_rate >
0)` ; aucun statut ne dit « refusé » ; `id_commission_scale NOT NULL`, alors
qu'un droit fermé ne désigne aucune tranche de barème.

**Options envisagées**

- Option 1 : ne rien stocker — une vente refusée n'a aucune ligne `payment`.
  Aucun changement de schéma, mais le motif est perdu et `D2` ne peut plus être
  rouverte.
- Option 2 : une ligne `payment` en état `refused`, portant le motif, sans taux
  ni barème.
- Option 3 : une table `payment_refusal` séparée — deux tables répondraient
  alors à « ce chasseur a-t-il été payé pour cette vente ? ».
- Option 4 : porter le motif sur `sale` — mélange la vente et le droit du
  chasseur, deux sujets distincts.

**Décision**

Option 2 retenue. Le refus devient une ligne de `payment` à part entière, en
état `refused`, motivée et à zéro euro.

```sql
status IN ('refused', 'announced', 'invoice_submitted',
           'verified', 'scheduled', 'paid')

refusal_reason VARCHAR(30)
    CHECK (refusal_reason IN ('mandate_expired', 'out_of_scope'))

-- NOT NULL retiré sur : base_rate, seniority_rate, performance_rate,
--   id_commission_scale. Les bornes des CHECK sont inchangées : en
--   PostgreSQL, un CHECK ne s'applique pas à une valeur NULL.

CONSTRAINT chk_refused
    CHECK ((status =  'refused'
            AND refusal_reason IS NOT NULL AND amount = 0
            AND base_rate IS NULL AND seniority_rate IS NULL
            AND performance_rate IS NULL AND final_rate IS NULL
            AND id_commission_scale IS NULL)
        OR (status <> 'refused'
            AND refusal_reason IS NULL
            AND base_rate IS NOT NULL AND seniority_rate IS NOT NULL
            AND performance_rate IS NOT NULL
            AND id_commission_scale IS NOT NULL))
```

Les deux motifs du sujet, en anglais conformément à `ADR-002` :
`mandate_expired` (mandat échu à la date de l'acte) et `out_of_scope` (mandat
non-exclusif et vente hors dispositif).

**Justification**

Le sujet ne laisse pas le choix de l'emplacement : il écrit « dans
`paiements` ». L'option 1, la plus économe, est précisément la seule qui perde
la donnée qu'il demande de garder.

Une ligne de refus n'est pas un paiement à zéro : c'est un **événement de
droit**, daté, motivé, opposable au chasseur qui réclame. `chk_refused` lui
interdit d'emprunter les attributs d'un vrai paiement, ce qui rend impossible
la confusion entre « refusé » et « pas encore payé » — la seule erreur vraiment
coûteuse ici.

`id_sale` étant déjà `UNIQUE`, une vente porte soit un paiement, soit un refus,
jamais les deux : la contradiction est interdite par le schéma, pas seulement
par la discipline.

Enfin, `D2` reste ouverte. Si le groupe préfère plus tard une indemnité
forfaitaire, il suffira d'assouplir `amount = 0` : l'historique des refus sera
déjà là, motif compris.

**Conséquences**

- **Base de données :** `payment` modifiée dans
  `docker/init-v2/01_create_fil_rouge_immobilier.sql`. La table est **vide** à
  ce jour : aucune donnée en jeu. Ajouter un `COMMENT ON COLUMN` sur
  `refusal_reason`.
- **Développement :** les quatre champs concernés passent en `Optional` dans le
  modèle SQLModel. L'API acceptera dès lors un paiement sans taux, que seule la
  base refusera : une validation applicative reste à écrire.
- **Seed de démo :** une vente sans droit s'écrit en ligne `refused`, et non
  comme une vente sans paiement.
- **Tests :** deux cas positifs, un par motif, et cinq cas négatifs vérifiant
  que la base refuse bien.
- **Limite assumée :** les deux motifs sont figés dans un `CHECK` ; en ajouter
  un demandera une migration. Le sujet n'en définit que deux.
- **Ne ferme pas** le TODO déjà posé sur le calcul du droit : cet ADR
  *enregistre* le refus, il ne le *calcule* pas.

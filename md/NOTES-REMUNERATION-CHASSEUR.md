# Notes d'équipe — Règles de calcul de la rémunération du chasseur

> Résumé de travail à partir du document officiel poussé par le prof :
> [`REGLES-CALCUL-REMUNERATION.md`](<../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/documents utiles/REGLES-CALCUL-REMUNERATION.md>)
> et de sa spécification Gherkin associée [`10_calcul_remuneration_chasseur.feature`](<../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack - BASE/user-stories/10_calcul_remuneration_chasseur.feature>).
>
> ⚠️ Ce document **remplace/complète** [`BAREME-COMMISSION.md`](./BAREME-COMMISSION.md) : celui-ci avait été écrit avant que le prof ne publie les formules et paramètres exacts (poids, tranches, bornes). Certains points qu'on y notait comme « zone à trancher » sont maintenant donnés noir sur blanc.

## 1. Règle métier vs paramètre — la distinction à retenir

| | Règle métier | Paramètre |
|---|---|---|
| Origine | Le Readme, le glossaire, le client | Une décision de conception |
| Exemple | « honoraires = fixe + % du prix » | « le fixe vaut 3000 € » |
| Si on la change | Le métier n'est plus respecté | Le calcul reste juste, le résultat change |

**Ne jamais présenter en soutenance un paramètre comme une exigence imposée par le client.** Les valeurs numériques du document (3000€, 2,5%, tranches, poids des critères, bornes...) sont *proposées* par le prof, pas imposées — à confirmer/tracer dans notre propre journal de décisions.

## 2. Le calcul en 5 étapes (ordre obligatoire)

**Étape 0 — Droit à rémunération**
Dépend de l'exclusivité du mandat et de l'origine de la vente. Mandat exclusif → toujours payé, même si le client trouve seul. Mandat non-exclusif → payé seulement si c'est le chasseur qui est à l'origine de la vente. Un seul chasseur est payé par vente (jamais de partage). Un acte signé après l'échéance du mandat (signature + 6 mois) n'ouvre aucun droit.

**Étape 1 — L'assiette (honoraires)**
```
H = montant_fixe + pourcentage × prix_achat
```
Le chasseur touche une part de **H** (les honoraires encaissés par l'entreprise via le notaire), **jamais** un pourcentage direct du prix du bien. Erreur classique à éviter : appliquer le taux au prix du bien multiplie le résultat par ~30.

**Étape 2 — Score de performance (0 à 100)**
Moyenne pondérée de 5 critères, **imposés par le Readme**, notation/poids proposés par le prof :

| Critère | Poids | Notation |
|---|---:|---|
| Délai mandat → acte (arrondi à la semaine inférieure) | 25% | ≤12 sem:100 · 13-20:80 · 21-28:60 · 29-36:40 · 37-48:20 · >48:0 |
| Exclusivité du mandat | 10% | exclusif:100 · non-exclusif:60 |
| Nb ventes réussies (12 mois glissants) | 25% | min(100 ; ventes × 20) |
| Nb mandats signés (12 mois glissants) | 15% | min(100 ; mandats × 10) |
| Nb visites avant achat | 25% | ≤3:100 · 4-6:80 · 7-9:60 · 10-12:40 · 13-15:20 · >15:0 |

⚠️ Sens inversé pour délai et visites : **moins il y en a, meilleure est la note** (le Readme le dit explicitement).

**Étape 3 — Taux de base (barème par tranche)**
Grille par tranche de prix, **un seul taux pour la totalité** des honoraires (pas de découpage progressif façon impôt) :

| Tranche sur le prix | Taux |
|---|---:|
| < 200 000 € | 30% |
| 200 000 – 349 999 € | 35% |
| 350 000 – 499 999 € | 40% |
| 500 000 – 749 999 € | 45% |
| ≥ 750 000 € | 50% |

Le barème est **daté** (on prend celui en vigueur à la date de l'acte) et peut être **propre à un chasseur** (un barème nominatif prime sur le barème par défaut).

**Étape 4 — Ajustement ancienneté + performance**
```
taux_final = borne(taux_base × (1 + ancienneté + performance), 20%, 60%)
ancienneté = min(2% × années révolues, 10%)          # plafonné à 5 ans
performance = (score - 50) / 50 × 20%                 # pivot à 50, ±20%
```
Variations **relatives** et **additionnées** avant application (pas de composition explosive). Taux final toujours borné entre 20% et 60%.

**Étape 5 — Le montant**
```
Rémunération = arrondi_centime(taux_final × H)
Marge entreprise = H - Rémunération   (jamais arrondie séparément)
```

**Traçabilité** : tous les éléments du calcul sont **figés à la date de l'acte** dans `paiements` et ne sont jamais recalculés a posteriori — même si le barème change ensuite.

### Exemple de bout en bout (Bruno)
Mandat exclusif signé 14/11/2025, 3 ans d'ancienneté, 4 ventes + 9 mandats/12 mois, 5 visites, acte signé 30/07/2026 pour 420 000 € :
- Honoraires : 3000 + 2,5% × 420000 = **13 500,00 €**
- Score : 0,25×40 + 0,10×100 + 0,25×80 + 0,15×90 + 0,25×80 = **73,5/100**
- Taux de tranche (420k ∈ [350k;500k[) : **40%**
- Ancienneté : +6% · Performance : +9,4%
- Taux final : 40% × 1,154 = **46,16%**
- **Rémunération : 6 231,60 €** · Marge entreprise : 7 268,40 €

## 3. Tables à modéliser (Phase 2)

Le Readme officiel (section Phase 2) exige **nommément** `baremes_commission` + `paiements` — ce n'est pas hors scope, c'est un livrable explicite. Le reste (`ventes`, `visites`) en découle logiquement : sans elles, aucun des 5 critères de performance n'est calculable.

| Table | Statut | Rôle |
|---|---|---|
| `ventes` | à créer (n'existe pas) | prix acté, date acte, origine de la vente, lien mandat/chasseur |
| `visites` | à créer (n'existe pas) | compte le nb de visites avant achat (critère S₅) |
| `mandats` | existe, à compléter | ajouter `date_fin` (signature + 6 mois) et `exclusivite` |
| `parametres_honoraires` | à créer | `montant_fixe` + `taux_pourcentage`, **datés** |
| `baremes_commission` | à créer | clé = **triplet (chasseur, période, tranche)** → `taux`. `chasseur_id NULL` = barème par défaut, sinon barème nominatif qui prime |
| `paiements` | à créer | **fige** tous les termes du calcul (honoraires, score, taux_base, majorations, taux_final, montant) pour ne jamais les recalculer après coup |

**À ne pas faire** : une seule colonne `taux_commission` (c'est justement l'anomalie de l'existant — ni tranche, ni date, ni distinction par chasseur, cf. anomalie A1 du document officiel).

## 4. Sur le "hors scope" — clarification

`baremes_commission` et `paiements` sont **explicitement cités par leur nom** dans la mission Phase 2 du Readme du projet :
> « Concevez le modèle de données cible (...) : `baremes_commission` (par tranches de montant, variables dans le temps et par chasseur) + `paiements` »

Ce qui va potentiellement **au-delà** de ce qu'on doit produire : le code Python complet du document du prof (§14, `remuneration.py`). Le Readme demande un MCD/MLD/CDC technique, pas une implémentation. Ce code est probablement fourni comme référence/inspiration, pas comme livrable attendu de notre part — à confirmer si besoin avec le prof.

## 5. Prochaine étape suggérée

Esquisser le MCD (schéma Mermaid façon `MCD-MERISE.md`) avec ces entités et leurs cardinalités, notamment :
- `CHASSEUR (1,n) — (1,1) MANDAT`
- `MANDAT (1,1) — (0,n) VENTE`
- `VENTE (1,1) — (0,n) VISITE`
- `CHASSEUR (0,n) — (0,n) BAREME_COMMISSION` via la clé (chasseur nullable, période, tranche)
- `VENTE (1,1) — (0,1) PAIEMENT`

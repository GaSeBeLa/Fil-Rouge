# Calcul du barème de commission du chasseur

> Synthèse déduite du [`Readme.md`](../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack%20-%20BASE/Readme.md) (section « Le contexte ») et des user stories [`00_regles_metier_mandat_remuneration.feature`](./user-stories/00_regles_metier_mandat_remuneration.feature) et [`07_chasseur_remuneration_et_performance.feature`](./user-stories/07_chasseur_remuneration_et_performance.feature).
>
> ⚠️ C'est une **synthèse fonctionnelle de travail**, pas un livrable officiel : elle sert de point de départ à la modélisation (`baremes_commission`) et documente ce qui est explicitement donné par le sujet vs. ce qui reste un choix de conception à tracer (journal de décisions).

## 1. La base de calcul (montant à répartir)

Devant notaire, l'entreprise collecte, en plus du prix d'achat :

```
Base = montant_fixe + (pourcentage × montant_achat)
```

Cette `Base` sert **à la fois** de rémunération à l'entreprise et au chasseur : le chasseur ne touche pas un pourcentage du prix du bien, mais un pourcentage de cette `Base`, elle-même déjà calculée à partir du prix du bien.

## 2. La part du chasseur = un taux appliqué à cette base

```
Rémunération_chasseur = Base × taux(chasseur, montant_achat, date_acte)
```

Le `taux` est donné par un **barème par tranches de montant**, qui n'est pas unique : il dépend de trois axes croisés (cf. scénario `@bareme`) :

| Axe | Effet |
|---|---|
| **Montant du projet** | on regarde la tranche dans laquelle tombe `montant_achat` → chaque tranche a son propre taux |
| **Date** | le barème « varie dans le temps » → il faut prendre le barème **en vigueur à la date de l'acte**, pas le barème actuel |
| **Chasseur** | le barème est « différent pour chaque chasseur » → deux chasseurs peuvent avoir des taux différents pour la même tranche/date |

La variation par chasseur est elle-même pilotée par deux sous-facteurs : **ancienneté** et **performance**. Ni le Readme ni les user stories ne donnent la formule exacte de pondération (ex. +X % par année d'ancienneté, ou table de correspondance score → taux) — **c'est une zone à trancher et à documenter**, pas déductible du texte tel qu'il est. Ce qui *est* déductible, c'est la structure : ancienneté + performance → un **niveau/score chasseur**, qui sert de clé (avec la tranche de montant et la date) pour aller chercher le taux dans le barème.

## 3. Le calcul de la performance (les 5 critères)

La performance est recalculée à partir de 5 indicateurs bruts, chacun avec un sens de variation donné par le texte :

| Critère | Sens |
|---|---|
| Délai signature mandat → acte authentique, **arrondi à la semaine inférieure** | plus court = mieux (vente rapide) |
| Mandat exclusif ou non | l'exclusivité valorise la performance (le chasseur « sécurise » la vente) |
| Nombre de ventes réussies | plus = mieux |
| Nombre de mandats signés | plus = mieux (mesure l'activité/productivité) |
| Nombre de visites avant achat | **moins il y en a, plus la rémunération monte** (efficacité du matching) |

Ce recalcul est déclenché à deux moments identifiés dans le parcours chasseur :

- **à la hausse** quand un paiement est effectué (vente aboutie, étape 12) ;
- **à la baisse** quand un mandat arrive à échéance (6 mois) sans vente (étape 13).

Le texte ne donne pas de formule de pondération entre ces 5 critères (ex. `score = f(délai, exclusivité, ventes, mandats, visites)`) — c'est aussi un choix de conception à faire et à documenter (matrice de décision / journal de décisions), pas une donnée du sujet.

## 4. Modèle de données qui en découle

Deux objets distincts, historisés dans le temps :

1. **`performance_chasseur`** — un score/niveau recalculé à chaque événement (vente payée, mandat expiré), alimenté par les 5 compteurs/indicateurs ci-dessus.
2. **`baremes_commission`** — table par **tranche de montant × date de validité × chasseur (ou niveau ancienneté/performance)** → `taux` (et éventuellement `montant_fixe` si lui aussi variable).

C'est exactement ce que pointe la mission Phase 2 du Readme (« `baremes_commission` par tranches de montant, variables dans le temps et par chasseur ») — et c'est aussi ce que l'actuel `taux_commission` (colonne unique, plate, sur la table `utilisateurs`) ne peut pas représenter : ni tranches, ni historique temporel, ni lien à la performance. C'est vraisemblablement une partie du « besoin métier non géré » évoqué dans le constat de l'entreprise.

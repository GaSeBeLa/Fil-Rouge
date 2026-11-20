# ADR-018 : Modélisation de la performance énergétique des biens

> Copié de Confluence (page 52297855, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

**Date :** 07/09/2026

**Statut :** accepté

**Décideurs :** L'équipe projet

**Contexte**

La source ne fournit aucune valeur numérique. Dans `outils/generer_annonces.py`, la constante `DPE_LETTRES` (l. 86) est la seule origine d'une valeur DPE : la demande reçoit une lettre (l. 175), le bien reçoit une lettre (l. 284-287).

Trois contraintes encadrent la décision :

- le DPE français porte depuis 2021 **deux étiquettes** (kWh/m²/an et kg CO₂/m²/an), la classe retenue étant la plus défavorable — la lettre arbitre donc déjà entre deux dimensions ;
- les référentiels **diffèrent selon les pays** (`DPE`, `Energieausweis`, `EPC`) : mêmes lettres, seuils différents, alors que le `README` annonce dix pays ;
- les **seuils évoluent** (réforme française de 2021) et un diagnostic vaut dix ans.

**Options envisagées**

| Option | Description | Motif |
| --- | --- | --- |
| 1 | Tout en lettres | Fidèle à la donnée, mais ferme toute comparaison entre référentiels nationaux |
| 2 | Lettre convertie en valeur unique | Fabrique une précision inexistante : une lettre couvre un intervalle, pas une valeur |
| 3 | Lettre convertie en intervalle min/max | Conversion **réversible** : `A → [0,70]` et `[0,70] → A` portent la même information. Comparer deux intervalles revient à comparer deux lettres, au prix de quatre colonnes. Entre référentiels, produit des recouvrements partiels au résultat inexplicable |
| 4 | Lettre **et** valeurs numériques prévues, laissées nulles | **Retenue** |

**Décision**

`estate` :

```
energy_class          CHAR(1) CHECK (energy_class IN ('A','B','C','D','E','F','G'))
energy_class_scheme   VARCHAR(20)
energy_class_date     DATE
energy_kwh_m2         INTEGER CHECK (energy_kwh_m2 >= 0)
ges_kg_co2_m2         INTEGER CHECK (ges_kg_co2_m2 >= 0)
```

`criteria`, en remplacement de `energy_kwh_m2_min/max` :

```
energy_class_max      CHAR(1) CHECK (energy_class_max IN ('A','B','C','D','E','F','G'))
```

**Justification**

*La lettre porte le matching* parce que c'est la seule donnée détenue. Une conversion sans source n'est pas une mesure : une colonne vide dit « nous ne savons pas », une colonne déduite dit « nous savons », et c'est faux. Les lettres étant ordonnées, le matching s'écrit `estate.energy_class <= criteria.energy_class_max`.

`energy_class_scheme` au format `PAYS-DISPOSITIF-ANNÉE` (`FR-DPE-2021`, `DE-EnEV-2014`) lève d'un même mouvement les deux ambiguïtés de la lettre : pays et version. Une réforme française deviendra `FR-DPE-2030` sans modifier aucune ligne existante.

`energy_class_date` : une classe est constatée par un certificat daté et opposable, jamais recalculée a posteriori. La date situe le référentiel appliqué et contrôle la validité de dix ans. Même principe que `mandate.ends_at` : figer la valeur constatée, ne jamais appliquer rétroactivement une règle future.

*Les deux colonnes numériques nulles* sont une réserve assumée, pas un travail inachevé. La comparaison entre pays — objectif de Phase 3 — suppose des grandeurs mesurées : 62 kWh/m² se compare à 68, là où deux intervalles `[0,70]` sont égaux. La structure les accueillera sans refonte. Elles ne doivent jamais être dérivées de la lettre, ce qui reviendrait à l'option 3 déguisée.

*Un seul attribut côté demande* : le générateur ne produit qu'un `dpe_max`, et l'acquéreur exprime un plancher de qualité (« au moins un D »), pas une fourchette.

**Conséquences**

- **Schéma :** suppression de `estate.energetic_score` et de `criteria.energy_kwh_m2_min/max` ; ajout des six attributs.
- **Migration :** alimenter `estate.energy_class` depuis la lettre source — clôt l'écart #21 du cahier des charges. `energy_class_scheme` = `FR-DPE-2021` pour le jeu actuel, entièrement français. `energy_class_date` reste nulle, la source n'en fournit pas.
- **Documentation :** `COMMENT ON COLUMN` sur les six attributs, en signalant que `energy_kwh_m2` et `ges_kg_co2_m2` sont volontairement vides et ne doivent pas être dérivés de la classe.
- **MPD :** mettre à jour `Estate` et `Criteria` dans `MPD_CIBLE_drawio.xml`.
- **Limite assumée :** le `scheme` distingue les référentiels sans permettre de les comparer. Une recherche transfrontalière restera impossible tant que les valeurs numériques ne seront pas alimentées, ou qu'aucune table de correspondance n'aura été établie. Relève de la Phase 3.

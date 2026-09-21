# Annexe C2 — Domaines de valeurs exigés par les user stories

> Écrite par la fiche `C2` du chantier `09-contraintes-mpd`, le 2026-09-11.
> Source : les dix `user-stories/*.feature`, et rien d'autre.
> Relue par `C4` et `C5` : c'est la **citation** qui fait autorité, pas la
> reformulation de la colonne « Règle ».

## Conventions

- **Une règle par ligne.** Est relevé ce qui contraint une valeur : une liste
  fermée d'états ou de types, une borne, un pourcentage, une cohérence entre
  deux dates, un format, une unité.
- **Citation** : le texte de la ligne source, recopié tel quel ; `…` marque
  une coupe en début de ligne, jamais une retouche.
- **Cible** : la table, choisie parmi les 18 du MPD, quand elle se devine.
  « à rattacher (objet) » quand aucune des 18 ne porte l'objet évidemment —
  l'objet est nommé entre parenthèses, en français.
- **La colonne est toujours « à rattacher »** : cette fiche n'ouvre pas le
  MPD ; le rattachement à une colonne est le travail de `C4` et `C5`.
- Aucune règle par déduction : « exclusif ou non » est un booléen, une liste
  suivie de « ... » reste une liste ouverte.

## Règles du parcours actuel (fichiers 00 à 07)

| # | Règle | Citation | Source | Cible |
|---|---|---|---|---|
| U01 | Sous mandat exclusif, le chasseur est rémunéré même si le client achète un bien trouvé seul. | «Alors Bruno est rémunéré pour cette vente» | `00_regles_metier_mandat_remuneration.feature:19` | `Mandate`, `Payment` · à rattacher |
| U02 | Sous mandat exclusif, aucun autre chasseur ne peut agir pour ce client pendant la durée de validité du mandat. | «Et aucun autre chasseur ne peut agir pour le compte d'Alice pendant la durée du mandat» | `00_regles_metier_mandat_remuneration.feature:20` | `Mandate` · à rattacher |
| U03 | Deux mandats non exclusifs d'un même client, avec deux chasseurs, peuvent coexister. | «Alors Bruno et Chloé peuvent tous deux agir pour le compte d'Alice» | `00_regles_metier_mandat_remuneration.feature:33` | `Mandate` · à rattacher |
| U04 | La vente rémunère le chasseur à l'origine de la transaction aboutie. | «Et la vente finale rémunère le chasseur à l'origine de la transaction aboutie» | `00_regles_metier_mandat_remuneration.feature:34` | `Sale` · à rattacher |
| U05 | La durée de validité d'un mandat est de 6 mois. | «Scénario: La durée de validité du mandat est de 6 mois, renouvelable» | `00_regles_metier_mandat_remuneration.feature:37` | `Mandate` · à rattacher |
| U06 | Exemple chiffré de la règle précédente : signature le 2026-02-25 (ligne 38), fin de validité le 2026-08-25. | «Alors la date de fin de validité du mandat est le "2026-08-25"» | `00_regles_metier_mandat_remuneration.feature:39` | `Mandate` · à rattacher |
| U07 | Un mandat peut être renouvelé à l'échéance, à condition qu'aucune vente n'ait abouti. | «Et le mandat peut être renouvelé à l'échéance si aucune vente n'a abouti» | `00_regles_metier_mandat_remuneration.feature:40` | `Mandate`, `Sale` · à rattacher |
| U08 | Les honoraires de l'entreprise valent un montant fixe plus un pourcentage du montant de l'achat. | «…un montant fixe et un pourcentage du montant de l'achat pour le compte de l'entreprise» | `00_regles_metier_mandat_remuneration.feature:47` | `ParametersFees` · à rattacher |
| U09 | Le montant collecté par le notaire est la base de calcul des rémunérations de l'entreprise et du chasseur. | «Et ce montant sert de base de calcul à la rémunération de l'entreprise et du chasseur» | `00_regles_metier_mandat_remuneration.feature:48` | à rattacher (base de calcul) |
| U10 | Le barème de commission est défini par tranches de montant. | «Étant donné un barème de commission défini par tranches de montant» | `00_regles_metier_mandat_remuneration.feature:52` | `CommissionScale` · à rattacher |
| U11 | Le barème varie dans le temps et selon le chasseur. | «Et que ce barème varie dans le temps et selon le chasseur» | `00_regles_metier_mandat_remuneration.feature:53` | `CommissionScale` · à rattacher |
| U12 | La part du chasseur est celle de *la* tranche en vigueur pour ce montant, cette date et ce chasseur — l'article défini suppose une seule tranche applicable. | «…la part reversée à Bruno correspond à la tranche du barème en vigueur applicable à ce montant, à cette date, pour ce chasseur» | `00_regles_metier_mandat_remuneration.feature:55` | `CommissionScale` · à rattacher |
| U13 | Critère de performance : délai signature → achat, compté en semaines, arrondi à la semaine inférieure. | «délai entre la signature du mandat et l'achat effectif (arrondi à la semaine inférieure)» | `00_regles_metier_mandat_remuneration.feature:65` | `HunterPerformance` · à rattacher |
| U14 | Critère de performance : mandat exclusif ou non (booléen). | «caractère exclusif ou non du mandat» | `00_regles_metier_mandat_remuneration.feature:66` | `HunterPerformance` · à rattacher |
| U15 | Critère de performance : nombre de ventes réussies. | «nombre de ventes réussies» | `00_regles_metier_mandat_remuneration.feature:67` | `HunterPerformance` · à rattacher |
| U16 | Critère de performance : nombre de mandats signés. | «nombre de mandats signés» | `00_regles_metier_mandat_remuneration.feature:68` | `HunterPerformance` · à rattacher |
| U17 | Critère de performance : nombre de visites avant achat ; moins il y en a, plus la rémunération monte. | «nombre de visites effectuées avant achat (moins il y en a, plus la rémunération monte)» | `00_regles_metier_mandat_remuneration.feature:69` | `HunterPerformance` · à rattacher |
| U18 | L'affectation d'un chasseur à une demande est confirmée. | «Quand l'affectation est confirmée» | `01_particulier_demande_et_compte.feature:20` | `SearchRequest` · à rattacher |
| U19 | Le compte utilisateur est activé à la fin de sa création. | «Alors mon compte est activé» | `01_particulier_demande_et_compte.feature:28` | `User` · à rattacher |
| U20 | Le mode du mandat a deux valeurs : exclusif ou non exclusif ; le mandat porte aussi sa date de signature et sa date de fin de validité. | «…le mandat de recherche est enregistré avec sa date de signature, son mode (exclusif ou non-exclusif) et sa date de fin de validité» | `01_particulier_demande_et_compte.feature:36` | `Mandate` · à rattacher |
| U21 | La signature du mandat lance officiellement la recherche. | «Et ma recherche est officiellement lancée» | `01_particulier_demande_et_compte.feature:37` | `SearchRequest` · à rattacher |
| U22 | Le client choisit un ou plusieurs biens à faire visiter. | «Et je peux choisir un ou plusieurs biens à faire visiter par mon chasseur» | `02_particulier_recherche_et_visites.feature:17` | `EstateProposed`, `Visit` · à rattacher |
| U23 | Le vendeur peut ne pas accepter l'offre. | «Quand le vendeur n'accepte pas mon offre» | `03_particulier_offre_et_signature.feature:21` | à rattacher (offre d'achat) |
| U24 | Le vendeur peut accepter l'offre. | «Quand le vendeur accepte mon offre» | `03_particulier_offre_et_signature.feature:27` | à rattacher (offre d'achat) |
| U25 | Le client règle, en plus de l'achat, des honoraires valant un montant fixe plus un pourcentage du montant de l'achat. | «Alors je règle, en plus du montant de l'achat, les honoraires de l'entreprise (montant fixe + pourcentage du montant de l'achat)» | `03_particulier_offre_et_signature.feature:34` | `ParametersFees` · à rattacher |
| U26 | Le chasseur peut ne pas accepter une demande reçue. | «Quand je décide de ne pas l'accepter» | `04_chasseur_prise_en_charge_demande.feature:19` | `SearchRequest` · à rattacher |
| U27 | Une demande non acceptée peut être réaffectée à un autre chasseur. | «Et elle peut être réaffectée à un autre chasseur» | `04_chasseur_prise_en_charge_demande.feature:21` | `SearchRequest` · à rattacher |
| U28 | Le chasseur peut accepter une demande reçue. | «Quand j'accepte la demande» | `04_chasseur_prise_en_charge_demande.feature:26` | `SearchRequest` · à rattacher |
| U29 | Un rendez-vous a deux modalités : en présentiel ou en ligne. | «Alors un rendez-vous est fixé, en présentiel ou en ligne» | `04_chasseur_prise_en_charge_demande.feature:33` | à rattacher (rendez-vous) |
| U30 | La date de fin de validité du mandat est calculée, et non saisie. | «Et le mandat de recherche est signé et sa date de fin de validité est calculée» | `04_chasseur_prise_en_charge_demande.feature:41` | `Mandate` · à rattacher |
| U31 | La sélection est quotidienne, et peut être envoyée plusieurs fois par jour dans les zones tendues. | «Et cette sélection peut m'être envoyée plusieurs fois par jour dans les zones tendues» | `05_chasseur_selection_quotidienne_biens.feature:17` | `Estate_SearchRequest` · à rattacher |
| U32 | Le client priorise la sélection transmise ; l'échelle de priorité n'est pas précisée. | «Quand mon client commente et priorise cette sélection» | `05_chasseur_selection_quotidienne_biens.feature:28` | `EstateProposed` · à rattacher |
| U33 | Une note d'avis peut porter des commentaires audio et des vidéos. | «Alors je peux y joindre des commentaires audio et des vidéos» | `06_chasseur_avis_et_offre_achat.feature:14` | à rattacher (note d'avis) |
| U34 | L'offre d'achat est complétée puis signée par le client. | «Et mon client peut compléter et signer cette offre» | `06_chasseur_avis_et_offre_achat.feature:22` | à rattacher (offre d'achat) |
| U35 | Transmise au vendeur, l'offre prend le statut « en attente de réponse du vendeur ». | «Alors le statut de l'offre passe en attente de réponse du vendeur» | `06_chasseur_avis_et_offre_achat.feature:34` | à rattacher (offre d'achat) |
| U36 | Le vendeur peut refuser l'offre. | «Quand le vendeur refuse l'offre» | `06_chasseur_avis_et_offre_achat.feature:39` | à rattacher (offre d'achat) |
| U37 | Le vendeur peut accepter l'offre. | «Quand le vendeur accepte l'offre» | `06_chasseur_avis_et_offre_achat.feature:46` | à rattacher (offre d'achat) |
| U38 | La facture du chasseur est soumise à vérification. | «Alors ma facture est soumise à vérification» | `07_chasseur_remuneration_et_performance.feature:21` | à rattacher (facture) |
| U39 | La facture peut être affichée comme vérifiée et conforme. | «Quand le système affiche ma facture comme vérifiée et conforme» | `07_chasseur_remuneration_et_performance.feature:26` | à rattacher (facture) |
| U40 | Le paiement de la rémunération peut être « programmé ». | «Alors le paiement de ma rémunération est affiché comme programmé» | `07_chasseur_remuneration_et_performance.feature:27` | `Payment` · à rattacher |
| U41 | Une fois effectué, le paiement est marqué comme payé. | «Alors la somme est marquée comme payée» | `07_chasseur_remuneration_et_performance.feature:33` | `Payment` · à rattacher |
| U42 | La date de fin de validité du mandat vaut la date de signature plus 6 mois. | «Quand la date de fin de validité du mandat (signature + 6 mois) est atteinte» | `07_chasseur_remuneration_et_performance.feature:39` | `Mandate` · à rattacher |
| U43 | Un mandat échu sans vente fait baisser les indicateurs de performance du chasseur. | «Et mes indicateurs de performance sont recalculés à la baisse et affichés» | `07_chasseur_remuneration_et_performance.feature:41` | `HunterPerformance` · à rattacher |

## Règles du parcours futur (fichiers 08 et 09)

Ces règles décrivent un parcours **qui n'existe pas encore**. Elles ne se
jugent pas comme les précédentes : leur absence du MPD n'est pas un défaut
en soi.

| # | Règle | Citation | Source | Cible |
|---|---|---|---|---|
| F01 | Les critères saisis comprennent budget, zone et type de bien ; la liste est ouverte. | «Quand je saisis mes critères (budget, zone, type de bien...)» | `08_futur_particulier_assistance_ia.feature:15` | `Criteria` · à rattacher |
| F02 | Le client choisit ou écarte un bien proposé. | «Quand je choisis un bien ou que j'en écarte un» | `08_futur_particulier_assistance_ia.feature:29` | `EstateProposed` · à rattacher |
| F03 | Un chasseur est humain ou chasseur-IA. | «En tant que chasseur immobilier (humain ou chasseur-IA)» | `09_futur_chasseur_assistance_ia.feature:11` | `Hunter` · à rattacher |
| F04 | Le rendez-vous proposé par le système est en présentiel ou en ligne. | «Alors le système prend contact avec le prospect et propose un rendez-vous en présentiel ou en ligne» | `09_futur_chasseur_assistance_ia.feature:26` | à rattacher (rendez-vous) |
| F05 | Les annonces de la sélection sont ordonnées par pertinence ; le domaine de la pertinence n'est pas précisé. | «Et les annonces sont comparées, pré-filtrées et ordonnées suivant leur pertinence» | `09_futur_chasseur_assistance_ia.feature:39` | `Estate_SearchRequest` · à rattacher |
| F06 | Des offres en dessous du prix affiché sont pré-calculées. | «Et les possibilités de faire une offre en dessous du prix affiché sont pré-calculées» | `09_futur_chasseur_assistance_ia.feature:40` | à rattacher (offre d'achat), `Estate` · à rattacher |
| F07 | Plusieurs offres sont proposées : offre plus basse, offre au prix ; la liste est ouverte. | «Alors il propose plusieurs offres d'achat (offre plus basse, offre au prix...)» | `09_futur_chasseur_assistance_ia.feature:58` | à rattacher (offre d'achat) |
| F08 | La facture est affichée vérifiée et conforme si aucune anomalie n'est détectée. | «Et il l'affiche comme vérifiée et conforme si aucune anomalie n'est détectée» | `09_futur_chasseur_assistance_ia.feature:65` | à rattacher (facture) |

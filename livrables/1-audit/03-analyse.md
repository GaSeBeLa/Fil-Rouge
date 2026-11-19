# Livrable 1 — analyse de l'existant

> Phase 1, BC01. Format cible : 1 à 2 pages
> (`SP/documents utiles/GRILLE-EVALUATION.md`).
>
> Reprend la page Confluence « Audit du système d'information » (Gabriel,
> 05/08/2026), en garde la structure et les conclusions, corrige sa langue et
> renvoie chaque constat au registre ([`02-registre-anomalies-risques.md`](02-registre-anomalies-risques.md)).
> Chiffres recomptés le 2026-11-19 sur `fixtures/PgSQL.sql`.

## En résumé

L'entreprise est rentable, et ses honoraires sont sécurisés par le notaire.
Mais son système d'information ne reflète plus fidèlement son activité, et il
ne pourra pas suivre l'expansion qui se prépare.

Trois constats, mesurés sur les données réelles :

- **Un tiers des mandats affiche un statut faux.** 6 mandats sur 18 (6 des
  11 marqués « actifs ») ont dépassé leurs 6 mois de validité, l'un depuis
  247 jours. Les chasseurs ne sont donc pas alertés qu'il faut les renouveler
  (R01).
- **Un chasseur figure comme client d'un mandat** (mandat 13). Ce n'est pas une
  faute isolée : le système ne distingue pas les deux rôles, donc rien
  n'empêche que cela se reproduise (R02, R06).
- **Les honoraires n'existent nulle part.** Aucune trace du montant perçu, ni
  de sa date : impossible de retrouver le chiffre d'affaires dans le système
  (R03).

## Ce que cela coûte aujourd'hui

- **Suivi commercial.** Un mandat échu non détecté, c'est une relance qui n'a
  pas lieu. À 18 mandats, on corrige à la main ; à plusieurs milliers de
  mandats par semaine (`SP/Readme.md:160`), le même taux d'erreur devient
  ingérable.
- **Risque juridique.** Facturer sur un mandat que le système croit valide,
  mais qui a expiré, expose l'entreprise en cas de contestation. Ce risque
  existe déjà ; il ne dépend pas de la croissance.
- **Pilotage.** Les critères des clients sont écrits en texte libre : lisibles
  par un humain, **inexploitables par une machine** (R07). Impossible de
  filtrer, de recouper, ou d'alimenter les assistants IA envisagés.
- **Rémunération.** Un taux fixe par chasseur (de 2 à 3,25 %) ne peut pas
  exprimer le barème du sujet, par tranches, variable dans le temps et selon
  la performance (R08).
- **Continuité.** Le code du backend est perdu et son développeur absent :
  plus personne ne peut faire évoluer le système (R09).

## Comment nous avons procédé

1. Lu le schéma et les **24 + 18 + 10 lignes** des trois tables.
2. Vérifié chacune des **13 remarques** du consultant : 11 retenues, 2
   fusionnées avec une autre, aucune écartée sans motif (registre, § 3).
3. Ajouté ce que le consultant n'avait pas vu, en confrontant le schéma aux
   règles du sujet (barème, honoraires, armoire papier, données personnelles).
4. Coté chaque problème : probabilité × impact, de 1 à 9.

**Résultat : 16 problèmes.** **3** en priorité absolue, **9** à corriger
impérativement, **4** mineurs. Le poids est en haut de l'échelle : ce n'est pas
un système sain avec quelques défauts, mais une structure dont la plupart des
faiblesses demandent une action.

## Ce que nous recommandons

Une **refonte du modèle de données**, plutôt que des corrections ponctuelles.

Une correction partielle traiterait les symptômes visibles (statuts faux,
erreur de rôle) sans lever les deux blocages qui conditionnent la suite : des
critères inexploitables par une machine, et l'absence de toute trace
financière. Ce sont précisément les prérequis des chasseurs-IA prévus pour les
zones non couvertes.

| Option | Verdict | Pourquoi |
|---|---|---|
| Ne rien faire en attendant les rachats | ❌ écartée | La croissance rend le défaut ingérable, et l'application n'est déjà plus maintenable |
| Corriger seulement l'urgent | ❌ écartée | Plus rapide, mais laisse les deux fondations manquantes |
| **Refondre le modèle** | ✅ retenue | Règle la cause (rôles, durée, critères), pas seulement les symptômes |

## Mesures à engager en phase 2

| Priorité | Mesure | Ce que cela débloque | Risques traités |
|---|---|---|---|
| 1 | Séparer clients et chasseurs ; dater et borner les mandats | erreurs de rôle impossibles, échéances calculables | R01, R02, R04, R05, R06 |
| 2 | Structurer et historiser les critères | filtrage, matching, IA | R07 |
| 3 | Créer biens, visites, offres, ventes | performance des chasseurs calculable | R03 |
| 4 | Créer honoraires, barème, paiements | chiffre d'affaires et rémunération traçables | R03, R08 |
| 5 | Reprendre le backend | fin de la dépendance au code perdu | R09 |
| 6 | Contrôles de format, droits par rôle | qualité et protection des données | R11 à R16 |

## Conclusion

Le système actuel ne représente que la moitié du métier : il sait qui sont les
clients et les chasseurs, mais **il ignore ce qui est vendu et ce qui est
encaissé**. Cette moitié manquante (biens, visites, offres, honoraires)
explique à la fois les difficultés de pilotage et l'impossibilité
d'automatiser. Il faut compléter le modèle sur ces entités **avant** toute
mise en œuvre, plutôt que de déployer une structure qui reproduirait la même
lacune.

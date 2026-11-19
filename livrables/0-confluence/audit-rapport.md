> **Copie de Confluence** — page « Audit du système d'information » (id 19038211, version 1), espace GaSeBeLa1, copiée le 2026-11-19.
> La source qui fait foi reste Confluence : https://laurenceamethyste.atlassian.net/wiki/spaces/GaSeBeLa1/pages/19038211/Audit+du+syst+me+d+information. Les images, schémas draw.io et encadrés ne passent pas dans l'export : ils sont signalés par une ligne « 🖼️ Image ou schéma non copié : <nom ou légende si connue> ».

## Objet : État des lieux du système actuel et recommandations 

---

## En résumé

L'entreprise est rentable et les honoraires sont juridiquement sécurisés par le notaire. Mais le système informatique qui la fait tourner **ne reflète plus fidèlement l'activité réelle** — et il ne pourra pas accompagner l'expansion que se préparé.

Trois constats mesurés sur les données réelles :

* **Un tiers des mandats affiche un statut faux.** 6 mandats sur 18 sont enregistrés comme « actifs » alors qu'ils ont dépassé leur validité légale de 6 mois — l'un depuis 247 jours. Les chasseurs ne sont donc pas alertés qu'il faut les renouveler.
* **Un chasseur figure comme client dans un des mandats.** Ce n'est pas une faute de frappe isolée : le système ne fait aucune différence entre les deux rôles, donc rien ne l'empêche de se reproduire.
* **Les honoraires n'existent nulle part.** Aucune trace informatique du montant perçu, ni de sa date. N'est pas possible de produire l'historique des chiffres d'affaires depuis le système.

## Ce que cela coûte aujourd'hui

**Sur le suivi commercial.** Un mandat expiré non détecté, c'est une relance qui n'a pas lieu et un client qu'on ne rappelle pas. À l'échelle actuelle (18 mandats), la correction reste faisable manuellement. À l'échelle que visé — plusieurs milliers de mandats par semaine — le même taux d'erreur devient ingérable.

**Sur le plan juridique.** Facturer des honoraires sur un mandat que le système croit valide alors qu'il est légalement expiré, expose en cas de contestation. Le risque existe déjà, il ne dépend pas de la croissance.

**Sur la capacité à piloter.** Les critères de recherche des clients sont saisis en texte libre. Résultat : ils sont lisibles par un humain, mais **inexploitables automatiquement**. Impossible aujourd'hui de filtrer, de recouper, et surtout d'alimenter les outils d'assistance intelligente envisagés.

**Sur la continuité.** Le développeur qui maintenait l'application est indisponible, et son code n'est pas récupérable. Concrètement : plus personne ne peut faire évoluer le système en l'état.

## Comment nous avons procédé

Nous avons examiné l'intégralité de la base de données, vérifié chaque observation du consultant intervenu avant nous, et coté chaque problème identifié selon une méthode standard (probabilité de survenue × gravité de l'impact, sur une échelle de 1 à 9).

**Résultat : 16 problèmes identifiés.** Trois sont classés en priorité absolue, neuf demandent une correction impérative, quatre sont mineurs. La concentration en haut de l'échelle est le point important : il ne s'agit pas d'un système globalement sain avec quelques défauts, mais d'une structure dont la majorité des faiblesses appellent une action.

## Ce que nous recommandons

Nous recommandons une **refonte de la structure de données**, plutôt que des corrections ponctuelles.

Ce n'est pas un choix de confort. Une correction partielle traiterait les symptômes visibles (les mandats expirés, l'erreur de rôle) sans lever les deux blocages qui conditionnent les projets : l'impossibilité d'exploiter automatiquement les critères clients, et l'absence totale de traçabilité financière. Or ce sont précisément les prérequis des chasseurs-IA qu'est souhaité déployer sur les zones non couvertes.

Deux alternatives ont été examinées et écartées :

* **Ne rien faire en attendant les rachats** — c'est la croissance elle-même qui rend le défaut ingérable, et votre application n'est déjà plus maintenable indépendamment de tout rachat.
* **Corriger uniquement l'urgent** — plus rapide, mais laisse intactes les deux fondations manquantes ci-dessus.

## Ce qui a déjà été conçu

Une première version du nouveau modèle de données est établie. Elle règle :

* **la confusion client/chasseur** — la nouvelle structure rend cette erreur techniquement impossible, plus seulement improbable ;
* **le suivi des échéances** — date de début, durée et nombre de renouvellements permettent de calculer la validité réelle à tout moment ;
* **les modalités de signature** — date et mode de signature sont désormais enregistrés ;
* **les critères de recherche** — ils deviennent des données structurées et filtrables, tout en conservant le texte d'origine pour ce qui relève de l'appréciation (« charme ancien », « standing »).

## Mesures à engager en phase suivante

| Priorité | Mesure | Ce que cela débloque |
| --- | --- | --- |
| **1** | Créer le suivi des biens, des visites et des offres | Rend enfin calculable la performance de vos chasseurs (délai, nombre de visites, ventes conclues) |
| **2** | Créer le suivi des honoraires et des paiements | Vous donne l'historique de votre chiffre d'affaires et la traçabilité comptable |
| **3** | Remplacer le taux de commission fixe par un barème | Reflète enfin votre règle réelle : variable selon le montant, l'ancienneté et la performance |
| **4** | Reprendre l'application métier | Lève la dépendance au code perdu et redonne la capacité d'évoluer |
| **5** | Dimensionner l'architecture pour la croissance | Prépare l'international et les milliers de mandats hebdomadaires annoncés |

Les trois premières mesures relèvent de la conception du modèle de données et peuvent être engagées immédiatement. Les deux dernières supposent des arbitrages techniques et budgétaires à valider avec vous.

## Conclusion

Le système actuel ne représente qu'une partie du métier : il sait qui sont les clients et les chasseurs, mais **il ignore ce qu'est vendu et ce qu'est encaissé**. C'est cette moitié manquante — les biens, les visites, les offres, les honoraires — qui explique à la fois les difficultés de pilotage actuelles et l'impossibilité d'automatiser quoi que ce soit.

La partie déjà reconçue est solide et peut avancer. Notre recommandation est de compléter le modèle sur ces entités manquantes avant toute mise en œuvre, plutôt que de déployer une structure qui reproduirait la même lacune.

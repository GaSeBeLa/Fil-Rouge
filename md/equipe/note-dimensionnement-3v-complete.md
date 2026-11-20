> **Version complète, gardée en annexe** (hypothèses A à M, 14 calculs, 14 sources). Le livrable est la version courte : `livrables/3-architecture/3.1-note-dimensionnement-3v.md` (2026-11-20).

> **Copie de Confluence** — page « Note de dimensionnement 3V — deux scénarios » (id 45252610, version 13), espace GaSeBeLa1, copiée le 2026-11-19.
> La source qui fait foi reste Confluence : https://laurenceamethyste.atlassian.net/wiki/spaces/GaSeBeLa1/pages/45252610/Note+de+dimensionnement+3V+deux+sc+narios. Les images, schémas draw.io et encadrés ne passent pas dans l'export : ils sont signalés par une ligne « 🖼️ Image ou schéma non copié : <nom ou légende si connue> ».

# Note de dimensionnement 3V

15 oct. 2026 (mise à jour de la note du 7 oct. 2026) — Gabriel Capelli

## 1. Objet

Estimer le volume, la vélocité et la variété des données après l'expansion (France + 9 pays), avec un catalogue alimenté par le **scraping des agences immobilières**, en France et à l'étranger. Les photos des annonces ne sont **pas copiées** : on enregistre un lien vers la photo sur le site de l'agence.

Deux axes de scénarios :

* **Activité** : **Bas** et **Haut** (nombre de mandats, nombre de biens par recherche) ;
* **Couverture du catalogue** : **Moyen** (une part `c` du marché) et **Complet** (tout le marché des 10 pays).

**Comment lire cette note :** les hypothèses sont notées **A à M** (§ 2). Les calculs sont numérotés **1 à 14** (§ 3 et § 4). Les sources sont citées entre crochets **\[1\], \[2\]…** et détaillées au § 9, avec leur statut de vérification. Les chiffres de stockage sont un **majorant** : un bien est stocké une seule fois (catalogue commun) et le nombre de biens est plafonné par le marché.

## 2. Hypothèses (données de départ)

|  | Hypothèse | Bas | Haut | D'où ça vient |
| --- | --- | --- | --- | --- |
| A | Mandats par semaine | 2 000 | 5 000 | « Plusieurs milliers de mandats par semaine » \[1\]. Les bornes 2 000 et 5 000 : choix de l'équipe |
| B | Biens répertoriés par recherche | 300 | 1 000 | « Plusieurs centaines, voire milliers de biens répertoriés par recherche » \[1\]. Les bornes 300 et 1 000 : choix de l'équipe |
| C | Ventes du marché par an (10 pays) | 5,2 M | 5,2 M | France : 958 000 ventes de logements anciens \[2\]. Étendu aux 10 pays au prorata de la population \[3\]\[4\] : non vérifié. Le neuf n'est pas compté à part \[5\]. Les 10 pays : France, Espagne, Allemagne, Royaume-Uni, Irlande, Benelux (3 pays), Italie, Suisse \[1\] |
| D | Biens mis en vente pour 1 vente | 1,4 | 1,8 | Flux publiés par Yanport : de 1,4 à 3,5 \[6\], recoupés avec les stocks des portails \[7\]. Haut = valeur centrale de la note d'origine |
| E | Liens de photos par bien | 20 | 20 | Choix de l'équipe. Repère : 30 photos pour 51 % des agents américains \[8\] |
| F | Poids d'une photo | 0,5 Mo | 0,5 Mo | Choix de l'équipe. Repère : de 100 Ko à 6 Mo par photo selon les plateformes \[8\]. **Non utilisé dans les calculs** depuis la décision L (photos non copiées) ; gardé pour mesurer ce qu'on évite (§ 7) |
| G | Durée en production | 2 ans | 2 ans | Choix de l'équipe |
| H | Taille d'une ligne en base | 113 octets (liens bien-recherche), 151 octets (liens de photos) | idem | Mesures du groupe sur 1 M de lignes : 113 et 149 octets \[11\] ; le calcul garde 151 (valeur de la note d'origine \[12\]). Coût fixe d'une ligne : 23 octets d'en-tête + 4 de pointeur \[10\] |

**Hypothèses ajoutées pour le scraping :**

|  | Hypothèse | Valeur | D'où ça vient |
| --- | --- | --- | --- |
| I | Part du marché couverte par le catalogue (`c`) | Moyen : 20 % · Complet : 100 % | Choix de l'équipe, **20 % à confirmer**. Le scénario Complet met dans le catalogue tous les biens du marché des 10 pays |
| J | Stock de biens à vendre en même temps | Bas : 4,0 M · Haut : 4,8 M | Stock France de 742 000 à 890 000 annonces \[7\], multiplié par 5,4 (rapport des 10 pays à la France, même méthode que l'hypothèse C). **Non vérifié** |
| K | Fréquence de passage du scraping | 1 passage par bien et par jour | Choix de l'équipe, **à confirmer** |
| L | Photos | **Liées, pas copiées** : on garde l'URL de la photo sur le site de l'agence | Décision du groupe (15 oct. 2026). Aucune loi connue n'oblige à les stocker ; les copier en masse expose à un litige (droit d'auteur, droit des bases de données). **À faire valider** |
| M | Même bien publié par plusieurs agences | facteur `k` ≥ 1, **non chiffré** | Aucune source. Le facteur D (1,4 à 1,8) compte les biens mis en vente pour une vente, pas ces doublons |

## 3. Volume (2 ans en production)

Le scénario **Complet** correspond à `c` = 100 % ; le scénario **Moyen** multiplie par `c` les calculs qui dépendent du nombre de biens du catalogue (n°2, 4, 6 et la table des biens du n°7).

| N° | Ce qu'on calcule | Calcul | Bas | Haut |
| --- | --- | --- | --- | --- |
| 1 | Mandats par an | A × 52 semaines | 104 000 | 260 000 |
| 2 | Biens distincts du marché par an (**plafond**, scénario Complet) | C × D | 5,2 M × 1,4 = 7,3 M | 5,2 M × 1,8 = 9,4 M |
| 3 | Lignes « liens bien-recherche » par an | n° 1 × B | 104 000 × 300 = 31 M | 260 000 × 1 000 = 260 M |
| 4 | Lignes « liens de photos » par an | n° 2 × E | 7,3 M × 20 = 146 M | 9,4 M × 20 = 188 M |
| 5 | Taille des liens bien-recherche, sur 2 ans | n° 3 × 113 octets × G | 31 M × 113 o × 2 = **7 Go** | 260 M × 113 o × 2 = **59 Go** |
| 6 | Taille des liens de photos, sur 2 ans | n° 4 × 151 octets × G | 146 M × 151 o × 2 = **44 Go** | 188 M × 151 o × 2 = **57 Go** |
| 7 | Autres tables (propositions, biens, divers) | valeurs de la note d'origine \[12\], non revérifiées | 4 + 5 + 0,7 = **9,7 Go** | 9 + 6 + 1,7 = **16,7 Go** |
| 8 | **Total base PostgreSQL** | n° 5 + 6 + 7 | **≈ 61 Go** | **≈ 133 Go** |
| 9 | **Photos en stockage objet** | Aucune photo copiée (hypothèse L) | **0 To** | **0 To** |

**Tableau récapitulatif des quatre scénarios** (Moyen : `c` = 20 %) :

| Ce qu'on calcule | Moyen, Bas | Moyen, Haut | Complet, Bas | Complet, Haut |
| --- | --- | --- | --- | --- |
| Biens distincts par an (n°2 × c) | 1,5 M | 1,9 M | 7,3 M | 9,4 M |
| Lignes « liens de photos » par an (n°4 × c) | 29 M | 38 M | 146 M | 188 M |
| Liens de photos, sur 2 ans (n°6 × c) | 8,8 Go | 11,4 Go | 44 Go | 57 Go |
| Table des biens, sur 2 ans | 1 Go | 1,2 Go | 5 Go | 6 Go |
| Liens bien-recherche, sur 2 ans (n°5, ne dépend pas de c) | 7 Go | 59 Go | 7 Go | 59 Go |
| Autres tables (propositions, divers) | 4,7 Go | 10,7 Go | 4,7 Go | 10,7 Go |
| **Total base PostgreSQL** | **≈ 22 Go** | **≈ 82 Go** | **≈ 61 Go** | **≈ 133 Go** |
| **Photos en stockage objet** | **0 To** | **0 To** | **0 To** | **0 To** |

_Figure 1 : base PostgreSQL par scénario (graphique « 2-base-postgresql »)._

Ces valeurs sont le **cumul à la fin des 2 ans**. La base grandit à un rythme régulier : à la fin de l'année 1, elle pèse environ la moitié de ces chiffres.

## 4. Vélocité (moyennes)

| N° | Ce qu'on calcule | Calcul | Bas | Haut |
| --- | --- | --- | --- | --- |
| 10 | Nouveaux mandats par jour | n° 1 ÷ 365 | 285 | 712 |
| 11 | Liens de photos enregistrés par seconde (scénario Complet) | n° 4 ÷ 31,5 M (secondes dans une année) | 4,6 | 6 |

**Vélocité du scraping :**

| N° | Ce qu'on calcule | Calcul | Moyen | Complet |
| --- | --- | --- | --- | --- |
| 12 | Nouveaux biens par jour | n° 2 × c ÷ 365 | 4 000 à 5 200 | 20 000 à 25 800 |
| 13 | Pages à relire par jour (rafraîchissement) | J × c × K | 0,8 à 1,0 M | 4,0 à 4,8 M |
| 14 | Pages relues par seconde | n° 13 ÷ 86 400 | 9 à 11 | 46 à 56 |

Le rafraîchissement (n°13 et n°14) est le flux le plus rapide : il dépasse largement les 4,6 à 6 liens de photos par seconde du n°11, qui ne demandent qu'une écriture en base, sans téléchargement de fichier. Il décide du nombre de machines de scraping et du débit sortant.

_Figure 2 : débit à tenir, par seconde (à régénérer sans la barre « photos copiées »)._

## 5. Variété

* **Formes** : structuré (mandats, ventes, paiements), semi-structuré (annonces de sources hétérogènes \[14\]), non structuré (photos des agences, lues sur leurs sites ; avis audio et vidéo du projet).
* **Sources** : des milliers de sites d'agences dans 10 pays, avec des pages différentes, des langues différentes et des devises différentes. Le flux du script du sujet \[14\] n'en donne qu'une version simulée.
* **Doublons** : un même bien arrive de plusieurs agences. Il faut dédoublonner **avant** d'enregistrer ses liens de photos, sinon on garde `k` fois les mêmes lignes. Le flux brut vaut `k` fois les n°12 et n°13.
* **Qualité** : sur 2 556 annonces mesurées, 75 % de remplissage moyen \[11\].
* **10 pays** : formats de code postal (ADR-021) et classes énergétiques (ADR-018) différents ; tous les montants sont en euros.
* **Droit et données personnelles** : les noms et téléphones d'agents scrapés vont au registre RGPD. Le droit de réutiliser les annonces et d'extraire le catalogue d'une agence est à vérifier site par site.

## 6. Conséquences pour l'architecture

* Base de 22 à 133 Go (n° 8 et tableau récapitulatif) : une instance PostgreSQL suffit (appréciation, non mesurée).
* **Pas de photo copiée** (hypothèse L) : le stockage objet ne sert plus aux photos des annonces. Il reste pour les médias propres au projet (avis audio et vidéo, ADR-051), non chiffrés ici. Les photos sont lues sur le site de l'agence, donc le catalogue dépend de sa disponibilité.
* Le scraping demande de 9 à 56 pages par seconde : un orchestrateur et plusieurs workers (flux Airflow de l'ADR-045).
* Les liens bien-recherche (n° 5) et les liens de photos (n° 6) pèsent de 84 à 87 % du volume de la base dans le scénario Complet : candidats au partitionnement. Leur `id` passe en BIGINT : un INTEGER plafonne à 2,1 milliards \[10\], atteint en ≈ 8 ans (liens bien-recherche) et ≈ 11 ans (liens de photos) dans le Haut.

## 7. Limites

* **Majorant** : le vrai volume dépend du recoupement entre recherches. Aucune source ne le donne.
* **Couverture** : la valeur `c` = 20 % du scénario Moyen est un choix de l'équipe, à confirmer. Le volume est proportionnel à `c`.
* **Stock J** : étendu de la France aux 10 pays par la population, comme l'hypothèse C. Non vérifié.
* **Catalogue commun** : le script du sujet génère de 100 à 1 000 annonces par recherche, sans partage \[14\]. Avec ce modèle, la table des biens passerait à 31–260 M de lignes par an, soit de 16 à 167 Go de plus.
* **Hors calcul** : journal de transactions, sauvegardes, fragmentation. Règle courante ×2 à ×3 \[13\], soit 270 à 400 Go pour le Complet Haut.
* **Taille d'une ligne de photo** : le calcul garde 151 octets (hypothèse H). Une URL complète peut demander davantage : à 250 octets, la base du Complet Haut passerait de 133 à environ 170 Go.
* **Liens cassés** : une agence qui retire ou déplace une photo casse le lien. Il faut un contrôle régulier des liens, non chiffré ici.
* **Charge sur les sites des agences** : chaque affichage de photo sollicite leur serveur, et certains bloquent l'affichage depuis un autre site.
* **Ce qu'on évite** : copier les photos aurait demandé de 29 à 188 To (à 0,5 Mo la photo, hypothèse F), et de 75 à 1 130 To pour le Complet Haut si la photo pèse entre 0,2 et 3 Mo.
* **Doublons entre agences** (hypothèse M) : non chiffrés, donc le flux brut de scraping est sous-estimé d'un facteur `k`.

## 8. Décisions prises

* Les photos des agences sont **liées**, pas copiées (15 oct. 2026). Raison : aucune obligation de stockage connue, risque juridique et coût du stockage objet.
* Deux axes de scénarios : activité (Bas, Haut) et couverture du catalogue (Moyen, Complet).

## 9. Sources

Statut : **vérifié** = relu dans les fichiers du projet pour cette note ; **repris** = chiffre repris de la note d'origine ou des notes du groupe, non relu.

**Sujet et mesures du groupe**

* \[1\] Readme du sujet (StarterPack), l. 160 : projections de mandats et de biens par recherche, liste des pays. _Vérifié._
* \[14\] Script du sujet `outils/generer_annonces.py` : valeurs par défaut de 100 à 1 000 annonces par recherche, flux hétérogène. _Vérifié_ (`outils/Readme.md` non relu).
* \[11\] Mesures du groupe : 1 M de lignes insérées dans PostgreSQL (113 et 149 octets) ; `annonces_normalised.csv` (2 556 annonces, 5 recherches, 75 % de remplissage). _Repris._
* \[12\] Note de dimensionnement d'origine, mesures du groupe du 22/09/2026 : taille de ligne retenue (151 octets), « autres tables ». _Repris, non revérifié._

**Sources publiques**

* \[2\] Insee, Informations rapides n° 216, 8 sept. 2026 : 958 000 ventes de logements anciens sur 12 mois à fin juin 2026. _Repris._
* \[3\] IGEDD, déc. 2025 : 929 000 ventes, base du taux de 13,5 pour 1 000 habitants de la note d'origine. _Repris._
* \[4\] Eurostat, population au 1er janvier 2025 : extension aux 10 pays. _Cité par la note d'origine, non relu._
* \[5\] SDES, logements neufs, T2 2026 : 17 499 logements neufs mis en vente sur le trimestre ; le neuf reste marginal selon la note d'origine. _Repris._
* \[10\] Documentation PostgreSQL : coût fixe d'une ligne (23 octets d'en-tête, 4 de pointeur) ; plafond de 2,1 milliards pour un INTEGER. _Repris, non relu._

**Sources privées ou commerciales (fiabilité moindre)**

* \[6\] Yanport, T3 2026 : nouvelles annonces par mois et stock par portail, d'où l'écart de 1,4 à 3,5. _Repris._
* \[7\] Recoupements du stock : Leboncoin (890 291 annonces de ventes, début oct. 2026) ; eXp France d'après SeLoger, via Batinfo (864 167 logements à vendre, juin 2026) ; Maison & Vous (742 000 annonces Leboncoin, mars 2026). _Repris._
* \[8\] Photos : HomeJab (30 photos pour 51 % des agents américains) ; Fast.io (plateformes limitées de 100 Ko à 6 Mo par photo). _Repris._
* \[13\] Dimensionnement : STACKIT ; liste pgsql-general (gonflement des tables). _Repris._

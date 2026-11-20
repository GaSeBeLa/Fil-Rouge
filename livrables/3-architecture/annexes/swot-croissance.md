> D'après la page de travail « SWOT - Phase 3 (croissance) » de l'équipe, copiée le 2026-11-19. **Le dépôt fait foi** depuis le 2026-11-20.
> 

# 🧭 SWOT — le nouveau SI, face à la croissance

> Matrice SWOT (Forces, Faiblesses, Opportunités, Menaces), selon le modèle du sujet (`documents utiles/MODELE-SWOT.md`, StarterPack), qui la prévoit en phase 1 et en **phase 3**. Bloc BC01.
> La SWOT de **départ** (le SI hérité, phase 1) est la page « Matrice SWOT » de Békanty (19/08/2026). Celle-ci est la SWOT d'**arrivée** : le SI que nous avons construit, face à la croissance.
> Rédigée le 2026-11-19 avec l'assistant IA du projet, à partir du dépôt (`Fil-Rouge`, `Fil-Rouge-API`) et du `Readme.md` du sujet.

## Contexte analysé

- **Objet de l'analyse :** le SI cible (schéma v3, API, flux de données), face aux rachats, à l'expansion dans 9 autres pays et à l'arrivée de l'IA. La SWOT prépare les décisions de la phase 3 : que faut-il ajouter pour tenir la charge ?
- **Date :** 19/11/2026 (date de référence des données : 25/07/2026).
- **Auteurs (groupe) :** Sébastien, Laurence, Békanty, Gabriel.

---

## La matrice

### 💪 Forces *(interne, positif)*

- **Un modèle qui couvre tout le métier** : 22 tables, des comptes aux paiements ; montants en euros ; les rôles séparés, l'erreur du mandat 13 devient impossible (3 triggers d'exclusivité).
- **Des règles prouvées** : 1 120 tests passent (2026-11-20) ; les 33 éléments « Must » du backlog sont codés et testés (backlog MoSCoW).
- **Des mandats datés** : fin = signature + 6 mois, contrôlée par la base ; plus de statut « actif » faux.
- **Des critères structurés et versionnés**, avec la localisation de la demande : la base qui nourrira le matching existe.
- **Une pile prête pour le volume** : import des annonces chaque nuit (Airflow), stockage brut (MinIO), recherche (Elasticsearch), logs (Kibana), schéma analytique séparé (OLAP).
- **Des mesures, pas des promesses** : 3 index posés, de 15 à 100 fois plus rapides à 500 000 sélections (note d'indexation) ; une restauration complète en 2,82 s, sans écart (PCA/PRA).

### ⚠️ Faiblesses *(interne, négatif)*

- **Un seul serveur** : ni réplication, ni partitionnement posés ; tout tourne en local sous Docker.
- **Sauvegarde sur la même machine** : la copie quotidienne est codée depuis le 2026-11-20 (7 jours gardés), mais sans copie hors site ni journaux WAL : on peut perdre jusqu'à 24 h de données (PCA/PRA).
- **Deux tâches planifiées manquent** : la sélection de biens chaque jour, et la note du mandat échu (backlog, Should en partie).
- **La typologie des biens est vide** : la colonne existe, 0 bien sur 3 219 l'a remplie (cahier des charges, écart 13 quater).
- **Pas de notification** : ni email, ni alerte (backlog, Won't).

### 🚀 Opportunités *(externe, positif)*

- **Des rachats prévus** d'entreprises du même type (`Readme.md:160`) : leurs données peuvent entrer par la même migration rejouable.
- **9 autres pays et les DROM**, des milliers de mandats par semaine (`Readme.md:160`) : le modèle porte déjà un code pays (`country_iso`) sur les biens, les critères des demandes et les fiches client.
- **Des chasseurs-IA** pour les zones sans chasseur (`Readme.md:166-169`) : le moteur de suggestion à règles (v1) et le jeu de features préparent leur arrivée.
- **Des outils libres et gratuits** : toute la pile l'est ; l'entreprise ne paie pas de licence en grandissant.

### 🌩️ Menaces *(externe, négatif)*

- **Le volume** : jusqu'à **133 Go** de base à 2 ans dans le scénario haut (note 3V). Une instance PostgreSQL les tient (note 3V, matrice) ; ce qui manque, c'est un second serveur pour la reprise et les lectures.
- **Le RGPD, avec l'IA** : ouvrir les données à un assistant touche à « qui accède à quoi » (`Readme.md:282`) ; une fuite coûterait cher.
- **Des règles différentes par pays** : formats de téléphone et d'adresse, fiscalité et mandat qui ne sont peut-être pas les mêmes qu'en France (non vérifié pays par pays).
- **Des données rachetées de qualité inconnue** : comme l'existant au 25/07, elles peuvent arriver avec des statuts faux ou des rôles mélangés.

---

## Stratégies croisées *(le vrai livrable)*

| Croisement | Question directrice | Actions retenues |
| --- | --- | --- |
| **Forces × Opportunités** (offensif) | Comment utiliser mes forces pour saisir les opportunités ? | Faire entrer chaque agence rachetée par la migration rejouable et ses contrôles ; ouvrir un pays en renseignant `country_iso`, sans changer le schéma. |
| **Forces × Menaces** (défensif) | Comment utiliser mes forces pour parer les menaces ? | Ouvrir les données à l'IA par le rôle en lecture seule déjà posé (`fil_rouge_reader`), sur les seules données pseudonymisées ; garder les tests comme filet à chaque ajout de pays. |
| **Faiblesses × Opportunités** (ajustement) | Quelles faiblesses corriger pour saisir les opportunités ? | Coder les deux tâches planifiées (sélection quotidienne, mandat échu) ; remplir la typologie des biens, condition du matching ; ajouter les notifications. |
| **Faiblesses × Menaces** (survie) | Quelles faiblesses me rendent vulnérable aux menaces ? | Ajouter à la sauvegarde quotidienne une copie hors site et les journaux WAL ; prévoir réplication et partitionnement avant d'approcher les 133 Go (matrice de décision d'architecture). |

---

## Décision / conclusion

Le nouveau SI règle les défauts de structure relevés en phase 1 : le métier entier est en base, les règles sont testées, les données sont prêtes pour l'IA. Ce qui manque pour la croissance n'est plus le modèle, mais **l'exploitation** : un seul serveur, une sauvegarde sans copie hors site, deux tâches automatiques à coder. **Décision : garder le modèle v3, et investir la phase suivante dans l'exploitation** (sauvegarde, réplication, partitionnement), choisie par la matrice de décision d'architecture.

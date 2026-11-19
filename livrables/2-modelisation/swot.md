> **Copie de Confluence** — page « SWOT- Phase 2 » (id 27033601, version 2), espace GaSeBeLa1, copiée le 2026-11-19.
> La source qui fait foi reste Confluence : https://laurenceamethyste.atlassian.net/wiki/spaces/GaSeBeLa1/pages/27033601/SWOT-+Phase+2.

# 🧭 SWOT — le SI hérité, avant la refonte

> Matrice SWOT (Forces, Faiblesses, Opportunités, Menaces), selon le modèle du sujet (`documents utiles/MODELE-SWOT.md`, StarterPack). Bloc BC01.
> Rédigée le 2026-11-19 par le Glaude, à partir de l'audit de la phase 1 (`livrables/1-audit/`) et du `Readme.md` du sujet.

## Contexte analysé

- **Objet de l'analyse :** le SI hérité de l'entreprise, face à l'expansion et à l'ajout de l'IA. La SWOT prépare la décision de la phase 2 : corriger l'existant, ou refondre le modèle.
- **Date :** 25/07/2026, la date de référence du projet.
- **Auteurs (groupe) :** Sébastien, Laurence, Békanty, Gabriel.

Chaque ligne renvoie à sa preuve : un risque du registre coté (`R01` à `R16`, `livrables/1-audit/02-registre-anomalies-risques.md`), ou une ligne du `Readme.md` du sujet.

---

## La matrice

### 💪 Forces *(interne, positif)*

- **L'entreprise est rentable** malgré son SI : « l'entreprise tourne bien et gagne de l'argent » (`Readme.md:160`). Il y a donc une marge pour investir.
- **Ses honoraires sont sûrs** : le notaire les collecte à l'acte (`Readme.md:78`). Le SI ne porte pas le risque d'impayé.
- **Des données réelles existent** : 10 secteurs, 24 utilisateurs (6 chasseurs, 18 clients), 18 mandats. La migration a une base concrète, et des cas réels pour se tester.
- **La base tourne déjà sous PostgreSQL** (`fixtures/PgSQL.sql`) : la refonte garde le même moteur (ADR-001).
- **Un audit déjà commencé** : les 13 remarques du consultant précédent, toutes vérifiées et tracées (registre, § 3).

### ⚠️ Faiblesses *(interne, négatif)*

- **Des statuts faux** : 6 mandats « actifs » sur 11 ont dépassé leurs 6 mois, jusqu'à 247 jours (R01, cote 9).
- **Des rôles mélangés** : clients et chasseurs dans une seule table ; un chasseur est enregistré comme client du mandat 13 (R02, R05, R06).
- **Aucune trace financière** : ni honoraires, ni barème, ni paiement en base (R03, cote 9 ; R08).
- **Des critères en texte libre**, que la machine ne sait pas lire : « T3 Ecusson, budget 320000… » (R07).
- **Le code du backend est perdu**, et son seul développeur est absent (R09 ; `Readme.md:208`).
- **Des documents papier** sans lien avec la base (R10 ; `Readme.md:207`).

### 🚀 Opportunités *(externe, positif)*

- **Des rachats prévus** d'entreprises du même type (`Readme.md:160`) : le volume à venir justifie une vraie architecture.
- **Une expansion dans 9 autres pays** et les DROM, avec des milliers de mandats par semaine (`Readme.md:160`) : un marché bien plus grand.
- **Des outils d'IA mûrs** : des chasseurs-IA pour épauler les humains et couvrir les zones sans chasseur (`Readme.md:166-169`).
- **Des outils libres et gratuits** pour bâtir la pile : PostgreSQL, Airflow, MinIO, Elasticsearch, Kibana.

### 🌩️ Menaces *(externe, négatif)*

- **Le RGPD** : 24 personnes, avec nom, email et téléphone en clair, sans droits par rôle (R16). L'ouverture à une IA aggrave ce risque (`Readme.md:282`).
- **La montée en charge** : à des milliers de mandats par semaine, une erreur corrigée à la main sur 18 mandats devient ingérable.
- **Le risque juridique** : facturer sur un mandat expiré expose l'entreprise en cas de contestation (R01). Ce risque existe déjà.
- **Des pays aux formats différents** : téléphone sans indicatif, code postal sans contrôle (R12, R13). Ils bloquent l'international.

---

## Stratégies croisées *(le vrai livrable)*

| Croisement | Question directrice | Actions retenues |
| --- | --- | --- |
| **Forces × Opportunités** (offensif) | Comment utiliser mes forces pour saisir les opportunités ? | Investir la marge dans une **refonte du modèle**, sur PostgreSQL déjà en place ; migrer les données réelles pour partir d'un historique, pas d'une base vide. |
| **Forces × Menaces** (défensif) | Comment utiliser mes forces pour parer les menaces ? | Appuyer le calcul de la rémunération sur l'acte du notaire, déjà sûr ; dater chaque mandat à sa signature pour couper le risque juridique (fin = signature + 6 mois). |
| **Faiblesses × Opportunités** (ajustement) | Quelles faiblesses corriger pour saisir les opportunités ? | Structurer et historiser les critères : c'est la condition du matching et des chasseurs-IA. Créer biens, visites, offres, ventes, barème et paiements. Reprendre le backend en API testée. |
| **Faiblesses × Menaces** (survie) | Quelles faiblesses me rendent vulnérable aux menaces ? | Séparer les rôles et poser les droits par rôle (RGPD) ; contrôler les formats par pays ; ouvrir les données à l'IA en lecture seule, sur un périmètre restreint. |

---

## Décision / conclusion

Le SI hérité ne sait que la moitié du métier : il connaît les clients et les chasseurs, mais pas ce qui est vendu ni ce qui est encaissé. Ses faiblesses touchent la structure, pas seulement les données : corriger l'urgent laisserait les deux blocages de la croissance, des critères illisibles et aucune trace financière. **Décision : refondre le modèle de données**, sur PostgreSQL, puis bâtir dessus l'API, le flux de données et la conception de l'IA. C'est ce que fait le schéma v3 (22 tables, montants en euros).

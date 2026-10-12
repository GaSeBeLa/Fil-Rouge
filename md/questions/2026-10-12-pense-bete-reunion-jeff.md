# Réunion avec Jeff — pense-bête

Préparé le 12/10/2026. Le numéro entre parenthèses renvoie à l'ADR, pour qui veut le détail.

## Déroulé

1. On présente ce qu'on a décidé (la liste ci-dessous).
2. Jeff réagit : ce qui lui va, ce qu'il veut changer.
3. On pose les questions de la fin.
4. On note ses retours, et on les donne à Claude, qui met les ADR à jour.

## Ce qu'on a décidé

### La rémunération du chasseur

- Les montants sont en euros : prix et barème en entiers ; honoraires et paiement au centime. (032)
- Les réglages (taux, tranches, notes) vivent dans des tables datées, avec les valeurs du sujet que vous avez validées. (034)
- Une vente garde la grille d'honoraires qui a servi ; une grille vaut jusqu'à la suivante. (030)
- Un paiement garde tous les éléments de son calcul, figés à la date de l'acte : on peut toujours expliquer un montant. (033)
- L'ancienneté et la performance augmentent le taux de la tranche ; elles ne changent pas de barème. (037)
- La note du chasseur se recalcule à chaque vente. (035)
- La note a cinq critères ; moins de visites vaut mieux ; « mandats signés » est noté par le taux de transformation. (048)
- Les notes du chasseur forment un journal : une ligne par note, la dernière est la note actuelle. (042)
- Un paiement passe par trois étapes datées : annoncé, programmé, payé. Pas de facture du chasseur. (038)

### Le mandat

- Le client seul signe le mandat ; la date de signature fait foi. (044)
- Un mandat dure 6 mois exacts. Un mandat exclusif bloque les autres mandats du client sur la période. (039)
- Le renouvellement se fait à l'échéance, par un nouveau mandat lié à l'ancien. Pas d'avenant. (050, 053)
- Un mandat porte forcément sur une demande de son propre client. (053)

### La recherche, les biens et les visites

- Une demande de recherche a quatre statuts ; une offre d'achat peut être « signée ». (041)
- Une recherche se localise par ville et code postal, avec un quartier facultatif. (031)
- Les biens sont importés par l'admin, ou saisis à la main par un chasseur ou un manager ; on note qui l'a saisi. (047)
- Le chasseur visite d'abord les biens choisis par le client ; puis le client visite avec lui le bien qui lui plaît. Seule cette visite du client compte pour la rémunération. (053)
- On n'enregistre que les visites faites, pas les visites prévues. (053)
- La note d'avis du chasseur peut porter plusieurs médias : audio, vidéo. (051)

### Les comptes et la sécurité

- Cinq rôles : Admin, Client, Hunter, Manager, Reader (lecture seule). (027)
- Chaque chasseur est rattaché à un manager. (029)
- Connexion par un jeton valable 60 minutes ; chaque programme qui appelle l'API montre sa clé. (028, 052)
- Un compte ne se supprime jamais : il est désactivé et rendu anonyme (RGPD). (049)
- L'adresse du client est obligatoire ; un email ne sert qu'à un seul compte. (053)

### Les données et la base

- Les données reprises qui manquent restent vides si possible, sinon une valeur factice documentée. (046)
- L'API vérifie ce qu'on lui envoie ; la base garde le dernier mot sur les règles. (036, 040)
- Gabriel a audité la base : 36 trous. 14 sont réparés en base le 12/10 ; les autres se feront dans l'API. (053)

### Ce qu'on ne fait pas dans le MVP (045)

- L'acte notarié reste chez le notaire : on garde seulement sa date et son prix.
- Pas d'agenda des rendez-vous.
- Le classement des biens par pertinence et les droits des chasseurs-IA : plus tard, au parcours IA.
- On garde le manager actuel d'un chasseur, pas l'historique.
- Les annonces sont chargées une fois ; un nouveau bien se saisit à la main.

## Les questions à lui poser

1. **L'exclusivité vaut-elle par client, ou par recherche ?** Aujourd'hui : par client. Un client peut-il signer deux mandats exclusifs pour deux recherches différentes ? (039)
2. **Un acte est signé après la fin d'un mandat non renouvelé.** On refuse la vente, ou on l'enregistre et on refuse seulement le paiement du chasseur ? (050, 024)
3. **Trois droits à confirmer** (027) :
   - le chasseur voit-il son barème ? Nous : oui.
   - le client crée-t-il lui-même son compte ? Nous : oui.
   - est-ce le chasseur qui enregistre la visite ? Nous : oui.
4. **Les notifications** (chasseur affecté, nouvelle demande, avis du client, paiement proche) : notre API doit-elle les porter ? (Q-JEF-27 à 29)
5. **Si le temps le permet — la réaffectation.** Un chasseur ne peut plus suivre un mandat (maladie ou autre) : est-ce dans le MVP, ou pour une V2 ? Nous penchons pour la V2. (Q-JEF-30)

## Où en sont les ADR

- 20 acceptés par le groupe le 12/10/2026.
- 3 à accepter après une petite retouche : 028, 043, 048.
- 1 attend la question des étages, que le groupe tranche : 053.
- 4 attendent les réponses de Jeff : 024, 027, 039, 050.
- 2 vieux brouillons remplacés : 025 (par 029), 026 (par 028).

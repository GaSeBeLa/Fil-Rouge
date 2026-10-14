# Chantier courant — Fil Rouge Immobilier

> Fichier lu **en entier** par `/vlp:chantier` et `/vlp:tache`, depuis la racine du
> projet. C'est la seule table à tenir : rien à mettre à jour ailleurs quand un
> chantier s'ouvre ou se clôt. Garde-le sous le seuil de `scripts/vlp.py` : `renvois` avertit.
> Les libellés en gras se recopient **à l'identique** : ils sont lus tels quels.

- **alias** : fil-rouge
- **kit** : le plugin `vlp`, installé à part par chaque développeur — pour un
  humain ; les commandes voyagent avec lui
- **contexte** : context AI/
- **méthode** : methode-chantier.md, à la racine du kit — il voyage avec le plugin
- **chantiers possibles** : context AI/08-etat.md
- **fichier d'état** : context AI/08-etat.md
- **index** : context AI/00-INDEX.md
- **artefact feuille de route** : https://claude.ai/artifact/Wu5xkSJUtfbjuhFdbvUq3C
- **artefact du chantier** : aucun
- **livraison** : aucune — le code vit dans `../Fil-Rouge-API/` depuis le
  2026-10-13, et tourne en local (`docker compose up -d` depuis
  `../Fil-Rouge-API/docker/`)
- **vérification** : depuis `../Fil-Rouge-API/docker/`, `docker compose exec -T api python -m pytest -q`
  — la session la lance et lit son verdict ; base de test `fil_rouge_test` recréée
  par `bash docker/create_test_db.sh` depuis `../Fil-Rouge-API/` (`API/README.md` § Tests)

## Contraintes d'écriture

Les règles que toute fiche respecte, quel que soit son sujet. Trois ou quatre,
pas quinze — celles qu'on regrette de ne pas avoir écrites.

- **Les deux dossiers `../Fil-Rouge-EISI-Data-IA-26-D04-StarterPack*/` ne se
  modifient jamais**, ni **`docker/docker-compose.yml`** (dans
  `../Fil-Rouge-API/`) sans le oui de l'utilisateur.
- Le schéma de référence est `docker/init-v3/01_create_fil_rouge_immobilier.sql`,
  dans `../Fil-Rouge-API/` :
  tout modèle SQLModel s'y confronte par grep. **Tout montant est en euros**
  (`CLAUDE.md`, règle 4).
- Prose et commentaires de code en français ; noms de code en anglais. Le code
  cite la carte qui le justifie (`Q-xx`, registre
  `md/questions/questions-a-trancher.md`).
- Aucun secret ni `.env` dans git, aucun chemin absolu dans le code ; du Python
  touché passe `pyright` avant son commit.

## Chantiers clos — dans l'index, pas ici

Chacun a sa ligne dans l'**index** ; sa page reste sur la feuille de route.

Lettres de fiche déjà prises : C, LOT, API (API : auth, RGPD et règles métier), DRO (droits : moindre privilège), FIN (Finitions de l'API : erreurs et Swagger), BAN (Réparer le banc v2/v3), DEM (Seed de démo). Un nouveau chantier en choisit un autre —
trois majuscules, jamais réemployées, même après clôture. `/vlp:chantier` le
propose, l'utilisateur tranche ; c'est cette ligne qui rend le refus possible.

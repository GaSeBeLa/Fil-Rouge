# ADR-066 : Les commentaires de code s'écrivent en français, les noms restent en anglais

✅ établi · 🟡 à décider · 💡 proposé

- **Date :** 23/11/2026
- **Statut :** ✅ accepté (Sébastien, Discord, 23/11/2026, question `lang23`). Choix noté en LANG-23 dans `md/equipe/choix-et-recommandations.md`.
- **Décideurs :** Sébastien.
- **Remplace :** ADR-002, **sur le seul point des commentaires de code**. Le reste d'ADR-002 tient : noms du code et schémas de données en anglais, glossaire FR/EN.

**Contexte**

- ADR-002 (03/08/2026) choisit l'anglais « pour le code, les schémas de données et les commentaires de code ».
- Dans les faits, l'équipe commente en français depuis le début. Le `CLAUDE.md` du projet le demande : « Prose et commentaires de code en français ; noms de code en anglais » (`CLAUDE.md:73`).
- Compté le 23/11/2026 dans le dépôt Fil-Rouge-API :
  - **80 des 146** fichiers Python de `API/src`, `airflow/src` et `airflow/dags` ont des commentaires `#` en français ;
  - **304** lignes de commentaire `--` en français dans `docker/init-v3/01_create_fil_rouge_immobilier.sql` ;
  - les docstrings sont en français elles aussi.
- Le cahier des charges complet recopiait ADR-002. La règle écrite et le code se contredisaient : un lecteur qui lit l'ADR puis le code voit l'écart.

**Options**

1. **Écrire ce que l'équipe fait : commentaires et docstrings en français, noms en anglais.** **Retenue.**
2. Garder ADR-002 et traduire tous les commentaires en anglais. Écartée : des centaines de lignes à retoucher, un risque d'erreur dans le code, et le métier se pense en français avec le client.
3. Ne rien écrire et l'expliquer à l'oral. Écartée : la contradiction resterait écrite.

**Décision**

1. **En anglais** : les noms du code (tables, colonnes, valeurs de statut, classes, fonctions, variables, routes), comme le veut ADR-002.
2. **En français** : les commentaires, les docstrings et la documentation du code (README).
3. Le glossaire `livrables/2-modelisation/annexes/glossaire-fr-en.md` fait le lien entre les deux langues.

**Justification**

- Les commentaires expliquent le métier, qui se discute en français avec le client. Les écrire dans la même langue évite une traduction de plus, et les erreurs qu'elle apporte.
- L'équipe est francophone. Un commentaire n'est utile que s'il est lu, et juste.
- La raison d'ADR-002 tient pour les noms : ce sont eux que l'outillage, l'ORM et un futur développeur étranger manipulent. Un commentaire se traduit plus tard, fichier par fichier, sans rien casser.

**Conséquences**

- ADR-002 garde son statut « accepté ». Une mention dit que le point « commentaires de code » est remplacé par cet ADR.
- Le cahier des charges complet (`md/equipe/cahier-des-charges-technique-complete.md`, ligne « Langue ») et le livrable 2.5 (`livrables/2-modelisation/2.5-cahier-des-charges-technique.md`, ligne « Langue ») citent les deux ADR.
- Aucune ligne de code ne change.
- 🟡 Le jour où un développeur non francophone rejoint le projet, la traduction des commentaires se rediscute.

**Pour refaire la mesure**, depuis le dossier Fil-Rouge-API :

```sh
grep -l -E '^\s*#.*\b(le|la|les|des|une|est|pour|qui)\b' $(find API/src airflow/src airflow/dags -name "*.py") | wc -l
grep -c -E '^\s*--.*\b(le|la|les|des|une|est)\b' docker/init-v3/01_create_fil_rouge_immobilier.sql
```

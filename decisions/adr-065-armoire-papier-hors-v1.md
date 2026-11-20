# ADR-065 : L'armoire à dossiers papier reste hors de la v1, sa reprise est prévue plus tard

> Copié de Confluence (page 67928067, espace GaSeBeLa1) le 2026-11-20. Depuis cette date, ce fichier du dépôt fait foi.

> Publié sur Confluence le 2026-11-19, dans « Accepté ». Source : `md/adr/adr-065-armoire-papier-hors-v1.md` du dépôt Fil-Rouge.

✅ établi · 🟡 à décider · 💡 proposé

- **Date :** 19/11/2026
- **Statut :** ✅ accepté (Laurence et Sébastien, Discord, 19/11/2026). Discuté entre nous sans être tracé ; écrit pour garder la trace.
- **Décideurs :** Laurence, Sébastien.
- **Voir aussi :** registre de l'audit, faille R10 (`livrables/1-audit/02-registre-anomalies-risques.md`) ; cahier des charges, § 2.2 ; ADR-015 et ADR-051 (médias dans MinIO).

**Contexte**

- Le sujet compte dans le SI « une armoire à dossiers papier » (`Readme.md:207`). Il ne dit pas ce qu'elle contient ; l'audit suppose des mandats signés (« mandats signés ? »).
- L'audit en fait la faille **R10**, cotée 6 : les documents papier n'ont aucun lien avec la base.
- Le cahier des charges (§ 2.2) la place « hors de tout périmètre numérique ». Aucun livrable ne disait ce qu'on en ferait ensuite.
- Le sujet ne parle pas de versions. L'équipe a convenu entre elle qu'un problème qu'on ne peut pas traiter en v1, faute de temps, se traite dans une version suivante, à condition d'être écrit.

**Options**

1. **v1 : l'armoire reste hors périmètre ; la base garde la date et le mode de signature du mandat. Version suivante : numériser les mandats signés.** **Retenue.**
2. Numériser l'armoire dès la v1. Écartée : pas le temps, et le contenu de l'armoire n'est pas connu.
3. Ne rien écrire. Écartée : la faille R10 resterait ouverte sans que personne ne le sache.

**Décision**

1. **En v1**, la base trace chaque mandat : `mandate.signature_date` et `mandate.signature_type` (`paper` ou `electronic`). On sait qu'un mandat papier existe ; on ne sait pas où il est rangé.
2. **Dans une version suivante**, chaque mandat signé sur papier est scanné en PDF, rangé dans MinIO comme les médias du chasseur (ADR-051), et relié à son mandat par une adresse.
3. La faille **R10 est donc réglée en partie** : le lien entre le mandat et la base existe ; le lien vers le document papier, non.
4. Le backlog MoSCoW gagne une ligne **Could** : « numériser les mandats de l'armoire ».

**Conséquences**

- À l'oral : « l'armoire est connue, tracée par le mode de signature, et sa numérisation est prévue ». Ce n'est pas un oubli.
- Les processus métier (`livrables/4-application/processus-metier.md`) disent « R10 en partie » à l'étape du mandat.
- 🟡 Le contenu réel de l'armoire est à vérifier le jour de la reprise : le sujet ne le dit pas.

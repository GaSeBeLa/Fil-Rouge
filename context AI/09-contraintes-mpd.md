> **QUAND LIRE** : on joue une fiche `C*` de ce chantier, ou on se demande où
> il en est. `/vlp:tache C<n>` n'en lit que le socle commun et sa fiche — jamais
> ce fichier en entier.

# Chantier C — Contraintes manquantes du MPD

**CLOS** le 2026-09-11. Ne se rejoue pas — ne sert plus qu'à relire son socle.

**À quoi il sert.** Le MPD dessiné dans draw.io porte déjà beaucoup de `CHECK`,
mais personne n'a vérifié qu'il couvre les règles écrites dans les user stories
et les notes métier. Ce chantier produit un **rapport d'écarts écrit** : règle
métier par règle métier, la contrainte est présente, absente, ou fausse.

**Fait.** Rien. Ouvert le 2026-09-11, cadré en 5 fiches, `C1` à jouer.

## Le socle commun

**L'autorité, dans cet ordre.** Les `user-stories/*.feature` priment ; le MPD
vient ensuite. `docker/init/01_create_fil_rouge_immobilier.sql` est **périmé et
hors jeu** : il ne s'ouvre pas, il ne se cite pas, il ne sert pas d'arbitre.
C'est une dérogation explicite et datée à la règle 3 de `CLAUDE.md`, décidée
par l'utilisateur qui refera ce fichier lui-même.

**La frontière.** Dedans : les clauses `CHECK`, les énumérations, les bornes
chiffrées, la cohérence de dates, les formats, et les `EXCLUDE USING gist`
contre le chevauchement de périodes de validité. Dehors, et on n'en parle
même pas dans le rapport : les clés primaires et étrangères, les actions
`ON DELETE` / `ON UPDATE`, `NOT NULL`, `UNIQUE`, les index et les `DEFAULT`.

**Ce que le chantier ne fait pas.** Aucun fichier de schéma n'est modifié,
aucune migration n'est écrite, aucun modèle SQLModel n'est touché. Le chantier
n'absorbe pas l'entrée #3 de `context AI/08-etat.md` (livrable 2, modélisation)
qui reste ouverte à part.

**Les fichiers du chantier** — aucune fiche n'en ouvre d'autre :

| Chemin | Ce qu'il rend |
|---|---|
| `../vrac/MPD 4 MEURISE.xml` | le MPD, format draw.io, hors dépôt, **lecture seule** |
| `context AI/09-annexe-inventaire-mpd.md` | écrit par `C1` — les tables et leurs contraintes, lisible |
| `context AI/09-annexe-domaines-user-stories.md` | écrit par `C2` |
| `context AI/09-annexe-domaines-notes.md` | écrit par `C3` |
| `livrables/2-modelisation/09-rapport-ecarts-contraintes.md` | écrit par `C4`, complété par `C5` — le livrable ; sorti de `context AI/` après la clôture, les fiches le citent à son ancien chemin |

**Les 18 tables du MPD**, relevées sur l'export PNG du diagramme — ce sont les
seuls noms de tables qu'une fiche a le droit d'employer : `User`, `Role`,
`Client`, `Hunter`, `RealEstateManager`, `SearchRequest`, `Criteria`, `Estate`,
`Picture`, `Estate_SearchRequest`, `EstateProposed`, `Visit`, `Mandate`,
`Sale`, `Payment`, `CommissionScale`, `HunterPerformance`, `ParametersFees`.

**Le piège du format.** Tout le contenu du MPD vit dans les attributs
`value="…"` des `<mxCell>`, en **HTML échappé** : `&lt;span style=…&gt;`,
`&#x9;`, `&amp;nbsp;`. Un `sed` de nettoyage a déjà été tenté et laisse des
balises dans sa sortie — d'où `C1`. Un nom de table peut être noyé dans une
balise : c'est ainsi que cinq des dix-huit avaient été manquées.

**La forme du rapport.** Une ligne par règle métier relevée, jamais par
colonne : *règle → table.colonne visée → contrainte présente dans le MPD →
verdict (couverte / absente / partielle / fausse) → formulation proposée*. La
formulation proposée est du SQL cité en prose, pas un fichier exécutable.

**Écriture.** Prose en français, noms de code en anglais. Aucun chiffre ni
libellé inventé : ce qui n'est pas lu dans un fichier ne s'écrit pas.

## L'ordre des fiches

| Fiche | Titre | Dépend de |
|---|---|---|
| `C1` | Extraire du MPD un inventaire lisible des contraintes | rien |
| `C2` | Relever les domaines de valeurs exigés par les user stories | rien |
| `C3` | Relever les domaines de valeurs exigés par les notes métier | rien |
| `C4` | Rapporter les écarts sur les personnes et les biens | `C1`, `C2`, `C3` |
| `C5` | Rapporter les écarts sur le mandat et la rémunération | `C4` |

`C1`, `C2` et `C3` sont trois relevés indépendants : elles se jouent dans
n'importe quel ordre. `C4` les confronte et crée le rapport ; `C5` ne dépend de
`C4` que parce qu'elle écrit dans le même fichier, après lui.

---

<!-- FICHE:C1 -->
## C1 [x] — Extraire du MPD un inventaire lisible des contraintes

**Session** : C:/Users/znorr/.claude/projects/C--Users-znorr-Documents-COURS-ENG--IA-ProjetFileRouge-Fil-Rouge/41697e62-7fcd-40fd-bae4-fec6e4970c36.jsonl

**Dépend de** : rien.
**Fichiers** : `../vrac/MPD 4 MEURISE.xml` en lecture, `context AI/09-annexe-inventaire-mpd.md` en écriture — et rien d'autre.

**Prompt**
Écris un script Python **dans le scratchpad de la session**, pas dans le dépôt :
il ne sert qu'une fois. Il lit le XML, parcourt les `<mxCell>`, prend leur
attribut `value`, le passe dans `html.unescape`, retire les balises HTML avec un
vrai parseur (`html.parser` de la bibliothèque standard, pas une expression
régulière), et normalise les espaces.

Le MPD est un diagramme : chaque table est une cellule conteneur, chaque
colonne une cellule enfant dont le parent porte le nom de la table. Sers-toi de
l'attribut `parent` pour rattacher les colonnes à leur table plutôt que de
deviner par la position. Les cellules d'association (`Signs`, `Creates`,
`Renews`, `Concerns`…) et les cardinalités (`0,n`, `1,1`) se reconnaissent à
leur absence d'enfants : écarte-les.

Écris ensuite l'annexe en Markdown : un titre de niveau 2 par table, puis un
tableau `colonne | type | contraintes`. Recopie les contraintes **verbatim**,
sans les reformuler ni les corriger — une contrainte fautive doit rester
fautive dans l'inventaire, c'est `C4` et `C5` qui la jugeront. Termine par les
contraintes de niveau table, celles nommées `CONSTRAINT …`.

**Critère de fin**
`grep -c '^## ' "context AI/09-annexe-inventaire-mpd.md"` affiche **18**, et
`grep -cE '<(span|font|div|br)' "context AI/09-annexe-inventaire-mpd.md"`
affiche **0**. Affiche aussi le nombre de `CHECK` par table, table par table.
<!-- /FICHE -->

---

<!-- FICHE:C2 -->
## C2 [x] — Relever les domaines de valeurs exigés par les user stories

**Session** : C:/Users/znorr/.claude/projects/C--Users-znorr-Documents-COURS-ENG--IA-ProjetFileRouge-Fil-Rouge/439826c5-9c98-4453-b92b-e8cad4b3cc91.jsonl

**Dépend de** : rien.
**Fichiers** : les dix `user-stories/*.feature` en lecture, `context AI/09-annexe-domaines-user-stories.md` en écriture — et rien d'autre. Pas le `README.md` du dossier.

**Prompt**
Lis les dix fichiers Gherkin et relève **tout ce qui contraint une valeur** :
une liste fermée d'états ou de types, une borne chiffrée, un pourcentage, une
règle de cohérence entre deux dates, un format imposé, une unité. Les fichiers
`08_` et `09_` décrivent un parcours futur : relève-les aussi, mais range-les
dans une section à part intitulée « Règles du parcours futur », parce qu'elles
ne se jugent pas comme les autres.

Une règle par ligne de tableau : `règle en une phrase | fichier:ligne | table et
colonne visées si elles sont devinables, sinon « à rattacher »`. Cite la ligne
du fichier, ne la paraphrase pas — c'est elle qui fera autorité en `C4` et `C5`.

N'invente aucune règle par déduction : si une story dit qu'un mandat est
« exclusif ou non », c'est un booléen, pas une énumération de trois valeurs.
Ce qui n'est pas écrit n'est pas une règle.

**Critère de fin**
Le fichier existe et
`grep -c '^|' "context AI/09-annexe-domaines-user-stories.md"` affiche son
nombre de lignes de tableau. Affiche le compte de règles **par fichier
source**, les dix nommés : un fichier à zéro règle est un résultat, mais il
doit être visible.
<!-- /FICHE -->

---

<!-- FICHE:C3 -->
## C3 [x] — Relever les domaines de valeurs exigés par les notes métier

**Session** : C:/Users/znorr/.claude/projects/C--Users-znorr-Documents-COURS-ENG--IA-ProjetFileRouge-Fil-Rouge/2826c5df-fd10-4a8b-93fd-e663077e2a1e.jsonl

**Dépend de** : rien.
**Fichiers** : `BAREME-COMMISSION.md`, `NOTES-REMUNERATION-CHASSEUR.md`, `notes_contraintes_client.md`, `notes_contraintes_localisation_criteria.md`, `schema-tracabilite-remuneration-chasseur_v4.md` en lecture, `context AI/09-annexe-domaines-notes.md` en écriture — et rien d'autre.

**Prompt**
Même relevé que `C2`, même format de tableau, sur les cinq notes métier. Ces
notes sont plus précises que les user stories sur les chiffres : taux, paliers
de barème, seuils d'ancienneté, coefficients de performance, bornes de codes
postaux et de pays. Recopie les valeurs exactes.

Trois notes ne sont pas encore commitées (`notes_contraintes_client.md`,
`notes_contraintes_localisation_criteria.md`,
`schema-tracabilite-remuneration-chasseur_v4.md`) : elles sont donc récentes et
priment sur les deux autres en cas de contradiction. Quand deux notes se
contredisent, ne tranche pas — écris les deux valeurs sur la même ligne et
marque la ligne « **contradiction** ». C'est un résultat du chantier.

Signale en fin de fichier les règles qui portent sur une période de validité
(un barème valable du … au …) : ce sont elles que les `EXCLUDE USING gist` du
MPD sont censés protéger.

**Critère de fin**
Le fichier existe, et la sortie affiche le compte de règles **par note**, les
cinq nommées, plus le nombre de lignes marquées « contradiction ».
<!-- /FICHE -->

---

<!-- FICHE:C4 -->
## C4 [x] — Rapporter les écarts sur les personnes et les biens

**Session** : C:/Users/znorr/.claude/projects/C--Users-znorr-Documents-COURS-ENG--IA-ProjetFileRouge-Fil-Rouge/d631b047-b31c-45d6-935a-fe7b3565b193.jsonl

**Dépend de** : `C1`, `C2`, `C3`.
**Fichiers** : `context AI/09-annexe-inventaire-mpd.md`, `context AI/09-annexe-domaines-user-stories.md`, `context AI/09-annexe-domaines-notes.md` en lecture, `context AI/09-rapport-ecarts-contraintes.md` en écriture — et rien d'autre. Ni le XML, ni les user stories : les annexes les remplacent.

**Prompt**
Crée le rapport avec ses deux sections de niveau 2, « Personnes et biens » et
« Mandat et rémunération » — la seconde reste vide, `C5` la remplit.

Remplis la première pour les douze tables `User`, `Role`, `Client`, `Hunter`,
`RealEstateManager`, `SearchRequest`, `Criteria`, `Estate`, `Picture`,
`Estate_SearchRequest`, `EstateProposed`, `Visit`. Un sous-titre par table, et
un tableau : `règle (avec sa source fichier:ligne) | contrainte trouvée dans le
MPD | verdict | formulation proposée`.

Quatre verdicts et pas d'autres : **couverte**, **absente**, **partielle**,
**fausse**. « Fausse » vise une contrainte qui existe mais ne dit pas ce
qu'elle croit dire — une clause syntaxiquement invalide, ou une énumération qui
contredit la story. La formulation proposée est un `CHECK` écrit en toutes
lettres dans le tableau ; elle ne part dans aucun fichier `.sql`.

Termine la section par une liste des contraintes du MPD qu'**aucune** règle
relevée ne justifie : elles ne sont pas fautives, mais elles sont sans source.

**Critère de fin**
`grep -cE '\| (couverte|absente|partielle|fausse) \|' "context AI/09-rapport-ecarts-contraintes.md"` est **au moins égal** au nombre de règles des annexes `C2` et `C3` qui visent ces douze tables. Affiche les deux nombres côte à côte, et le décompte par verdict.
<!-- /FICHE -->

---

<!-- FICHE:C5 -->
## C5 [x] — Rapporter les écarts sur le mandat et la rémunération

**Session** : C:/Users/znorr/.claude/projects/C--Users-znorr-Documents-COURS-ENG--IA-ProjetFileRouge-Fil-Rouge/5da119c6-dbdc-4cf0-b3dd-f8b72aa7722f.jsonl
**Dépend de** : `C4`.
**Fichiers** : les trois annexes `context AI/09-annexe-*.md` en lecture, `context AI/09-rapport-ecarts-contraintes.md` en écriture — et rien d'autre.

**Prompt**
Remplis la section « Mandat et rémunération » laissée vide par `C4`, même
format, mêmes quatre verdicts, pour les six tables `Mandate`, `Sale`,
`Payment`, `CommissionScale`, `HunterPerformance`, `ParametersFees`.

C'est ici que se joue le cœur du métier : les paliers de barème, les taux, les
coefficients de performance, la chaîne mandat → vente → paiement. Confronte
particulièrement `00_regles_metier_mandat_remuneration.feature` et
`07_chasseur_remuneration_et_performance.feature`, via les lignes qu'en a tirées
`C2`, aux contraintes de `Payment`, `CommissionScale` et `HunterPerformance`.

Traite explicitement les périodes de validité : pour chaque table qui porte un
couple `valid_from` / `valid_until`, dis si un `EXCLUDE USING gist` protège du
chevauchement, s'il porte sur la bonne clé de partition, et s'il manque là où
une note de `C3` exige une période unique.

Ajoute pour finir une section « Synthèse » de dix lignes maximum : les écarts
par verdict, et les trois qui coûteraient le plus cher à laisser passer.

**Critère de fin**
La section n'est plus vide, les six tables y ont leur sous-titre, et la sortie
affiche le décompte par verdict pour l'ensemble du rapport — les dix-huit
tables — à côté du nombre total de règles relevées en `C2` et `C3`.
<!-- /FICHE -->

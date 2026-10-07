# ADR-027 — proposition à relire avant publication

> 📋 **Brouillon, pas un ADR publié.** À coller dans le *Journal de décisions
> (ADR)* de Confluence une fois relu par le groupe. Rien ne s'écrit sur
> Confluence depuis le dépôt.
>
> ⚠️ **Numéro à vérifier, et plus que d'habitude.** Il suit `ADR-026`
> (22/09/2026), lui-même encore au statut « proposé ». Le connecteur
> Confluence n'a pas répondu le 22/09 : **le dernier numéro réellement
> publié n'a pas pu être lu.** À confirmer avant de coller.
>
> 💡 **Ce que cet ADR acte :** un périmètre d'accès **conçu et documenté**,
> pas implémenté. L'implémentation est hors périmètre depuis l'`ADR-026`.
>
> ✂️ **Ne pas copier ce bandeau.** Le texte à coller commence sous le trait.

---

**ADR-027 : Le périmètre d'accès par rôle est défini par conception, au titre
de la minimisation RGPD**

**Date :** 22/09/2026
**Statut :** proposé
**Décideurs :** l'équipe projet

**Contexte**

L'`ADR-026` acte que l'authentification et le contrôle d'accès ne sont pas
implémentés : le client a tranché que « c'est géré au dessus ».

Le sujet, lui, n'a pas bougé. Il exige :

- une note **« souveraineté & sécurité des données »** (BC05) précisant
  « le **périmètre d'accès** (idéalement lecture seule) » et
  l'anonymisation des données personnelles avant exposition à une IA ;
- un **registre RGPD** avec protection des données dès la conception, et
  précise que ces exigences « ne sont **pas optionnelles** ; leur absence
  est **pénalisante en jury** ».

➡️ Le « qui accède à quoi » reste donc un **livrable**. Il change seulement
de nature : document, et non code.

Un premier tableau avait été esquissé (7 lignes, majoritairement des cases
ouvertes) dans `md/securite/securite-mots-de-passe-et-droits.md` §4.3. Il était
incomplet : 7 ressources sur 18, et aucune source citée.

⚠️ **Ce qui ne fonde PAS cet ADR.** L'exigence `ENF-03` — « l'accès aux
données de rémunération est restreint au chasseur concerné et à son
manager » — est un **exemple de rédaction** dans un modèle de document
(section intitulée « Exigences non fonctionnelles **(extrait)** »), pas une
exigence du client. L'invoquer comme contrainte contractuelle serait
attaquable, et vérifiable par un jury en trente secondes.

**Décision**

1. **Le périmètre d'accès par rôle est défini par conception**, documenté
   table par table, et **non implémenté**.

2. **Le fondement est la minimisation** (RGPD) : chaque rôle n'accède qu'au
   strictement nécessaire à son parcours. C'est un principe du règlement,
   pas une lecture d'un exemple pédagogique.

3. **Quatre rôles** : `Client`, `Hunter`, `Manager`, `Admin` — les quatre
   déjà portés par la table `role`.

4. **Deux niveaux de contrôle sont décrits**, et non un seul :
   - le **rôle** : ce type d'utilisateur accède-t-il à ce type de donnée ?
   - l'**appartenance** : cette ligne précise est-elle la sienne ?

   ⚠️ Le second est ce qui manque le plus souvent. Deux chasseurs portent le
   même rôle ; un contrôle limité au rôle laisse le chasseur A lire les
   paiements du chasseur B.

5. **Le « supprimer » n'est pas une décision, c'est un constat** : les 34
   clés étrangères du schéma sont **toutes** en `ON DELETE RESTRICT`, aucune
   en `CASCADE`. Toute ligne reliée à une autre est déjà inaccessible à un
   `DELETE`.

   ➡️ La réponse au droit à l'effacement est donc la **désactivation**
   (`user.is_activated`, colonne existante) puis l'**anonymisation**, jamais
   la suppression.

6. **Trois écritures sont fermées à tous les rôles, y compris l'Admin :**
   - `criteria` ne se modifie ni ne s'efface — chaque changement crée une
     **nouvelle version** ; l'historique versionné est une exigence
     explicite du sujet ;
   - `hunter_performance` n'est jamais saisi à la main — le système le
     recalcule sur trois déclencheurs (`initial`, `payment`,
     `mandate_expired`) ;
   - `mandate`, `sale` et `payment` ne s'effacent pas — documents légaux et
     traces comptables.

7. **Ce que les sources fixent, et ce qu'elles ne fixent pas.** Le parcours
   client et le parcours chasseur du sujet disent **qui fait quoi**. Ils
   fixent donc les créations et les modifications. Ils ne disent **jamais**
   qui a le droit de **lire**. Toute règle de lecture écrite ici est un
   arbitrage de l'équipe, signalé comme tel.

8. **La matrice complète est annexée** :
   `md/securite/matrice-droits-crud-par-role.md` — 18 tables, 4 rôles, chaque case
   soit sourcée, soit marquée comme restant à trancher.

**Options envisagées**

- Option 1 : ne rien documenter, puisque rien n'est implémenté. **Rejetée** —
  le sujet exige la note souveraineté et le registre RGPD ; les supprimer
  coûterait plus cher en jury que l'`ADR-026` n'a fait gagner.
- Option 2 : documenter les rôles en prose, sans détail par table.
  **Rejetée** — trop vague pour être vérifiable, et le jury demande
  explicitement le périmètre d'accès.
- Option 3 : matrice complète sur les 18 tables, chaque case sourcée ou
  marquée ouverte. **Retenue.**
- Option 4 : ajouter la vérification de provenance / clé d'API proposée par
  le client. **Non tranchée**, reportée — voir `ADR-026`, questions ouvertes.

**Conséquences**

- Alimente directement deux livrables exigés : la note « souveraineté &
  sécurité des données » (BC05) et le registre RGPD.
- **Aucune conséquence sur le code.** Rien n'est à implémenter.
- L'argumentaire de l'`ADR-025` (lien chasseur → manager) est à réécrire :
  il s'appuyait sur `ENF-03` et sur un contrôle d'accès qui n'existera pas.
  La décision elle-même tient — c'est de la modélisation de données, portée
  par le MPD 03 4.
- Les comptes `Manager` et `Admin` restent à créer, pour le **seed de
  démonstration**.
- La formulation à tenir en soutenance : *« Le RGPD est une exigence
  explicite du sujet. Nous avons appliqué le principe de minimisation. Le
  détail du qui-voit-quoi est notre arbitrage, tracé dans cet ADR. »* — et
  non « le cahier des charges impose que… », qui serait faux.

**Questions ouvertes — à trancher avant de passer l'ADR en « accepté »**

| # | La question | Pourquoi elle bloque |
|---|---|---|
| 1 | Le `Manager` voit quoi ? | Un rôle entier sans aucune règle écrite |
| 2 | Qui enregistre la vente ? | Le notaire n'est pas un utilisateur du SI |
| 3 | Qui fait avancer la facture dans ses 5 états ? | Fin du parcours chasseur |
| 4 | Le client voit-il tout le catalogue de biens ? | Change la surface exposée |
| 5 | Le chasseur voit-il son propre barème ? | Confidentialité salariale |
| 6 | Qui fixe barèmes et honoraires ? | `Manager` ou `Admin` |
| 7 | Désactivation plutôt que suppression : validé ? | Proposition du point 5 |
| 8 | L'import des biens tourne sous quel compte ? | Aucun rôle humain ne crée un bien |
| 9 | L'échelle de priorité du client (décision `D6`) | Colonne absente du schéma |

⚠️ **Une réserve de méthode.** La question posée au client le 22/09
mélangeait deux sujets : « l'authentification » **et** « ce qu'ils peuvent
faire sur l'application ». Son « non » portait sur l'ensemble, mais sa
justification ne parle que de l'authentification. **À lui faire préciser**
avant de considérer cet ADR comme clos.

**Vérification (22/09/2026)**

Le constat du point 5, rejouable depuis `Fil-Rouge/` :

```bash
grep -c 'ON DELETE RESTRICT' docker/init-v2/01_create_fil_rouge_immobilier.sql
grep -c 'ON DELETE CASCADE'  docker/init-v2/01_create_fil_rouge_immobilier.sql
```

Attendu : **34** et **0**. Mesuré le 22/09/2026 : 34 références au total,
34 en `RESTRICT`, 0 en `CASCADE`, 0 sans clause `ON DELETE`.

**Sources**

| Affirmation | Source |
|---|---|
| Le périmètre d'accès et l'anonymisation sont exigés | `BASE/Readme.md`, « Souveraineté & sécurité des données » |
| Le RGPD n'est pas optionnel | `BASE/Readme.md`, section RGPD |
| `ENF-03` est un **extrait** de modèle, pas une exigence | `BASE/documents utiles/CAHIER-DES-CHARGES-TECHNIQUE.md` |
| L'historique versionné des critères est exigé | `BASE/Readme.md` Phase 2 ; `GLOSSAIRE-METIER.md`, « Version de demande » |
| Le notaire est hors périmètre du SI | `GLOSSAIRE-METIER.md`, « Acteurs » |
| Les 4 rôles, `is_activated`, les 3 déclencheurs de performance | `docker/init-v2/01_create_fil_rouge_immobilier.sql` |
| Le tableau de départ, incomplet | `md/securite/securite-mots-de-passe-et-droits.md` §4.3 |
| La matrice complète | `md/securite/matrice-droits-crud-par-role.md` |

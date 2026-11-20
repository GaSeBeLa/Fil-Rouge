# Note d'accessibilité (PSH) — l'espace acquéreur

> Équipe du projet — version courte du 2026-11-20. [Version complète](../../md/equipe/note-accessibilite-psh-complete.md).
> Exigée par le sujet : « Visez au minimum les critères de contraste, navigation clavier, tailles de cibles, alternatives textuelles ». Cahier des charges, exigence **ENF-13** : des préconisations pour l'espace acquéreur sur le contraste, le clavier, la taille des cibles et les textes alternatifs.

## 1. Périmètre

- Le projet livre la base et l'API, **pas de site web**. La note dit ce que le futur site devra respecter, et ce que l'API lui fournit.
- **Écrans visés** (parcours du particulier) : demande de recherche, finalisation du compte avec le code d'activation, liste et fiche des biens avec photos, décision du client (intéressé, ou refus motivé).
- **Normes** : **WCAG 2.2** niveau **AA**, norme du W3C ([Recommandation du 12 décembre 2024](https://www.w3.org/TR/WCAG22/)) ; **RGAA**, sa déclinaison française — version 4.1.2 d'après des sources secondaires, ⚠️ à revérifier sur accessibilite.numerique.gouv.fr.

## 2. Préconisations

| Thème | Ce que le site doit faire | Critère WCAG 2.2 | Niveau |
| --- | --- | --- | --- |
| **Contraste** du texte | « at least 4.5:1 » entre texte et fond | 1.4.3 | AA |
| Contraste des **boutons, champs, icônes** | « at least 3:1 against adjacent color(s) » | 1.4.11 | AA |
| **Clavier** | tout le parcours **sans souris** | 2.1.1 | A |
| **Focus visible** | on voit toujours où est le curseur du clavier | 2.4.7 | AA |
| Focus **pas caché** | un bandeau ne recouvre pas l'élément actif | 2.4.11 | AA |
| **Taille des cibles** | « at least 24 by 24 CSS pixels » | 2.5.8 | AA |
| **Alternatives textuelles** | chaque photo de bien a un texte qui la décrit | 1.1.1 | A |
| **Étiquettes** | chaque champ a une étiquette visible (« Budget maximum, en euros ») | 3.3.2 | A |
| **Erreurs** | dites **en texte**, près du champ, pas seulement en rouge | 3.3.1 | A |
| **Zoom** | texte agrandi à « 200 percent without loss of content or functionality » | 1.4.4 | AA |

**Lecteurs dyslexiques** (bonnes pratiques, hors WCAG, éprouvées par une personne de l'équipe) : police très lisible (Atkinson Hyperlegible, gratuite) ; fond crème et texte brun foncé ; phrases courtes, une idée par ligne ; ni capitales, ni italique.

## 3. Ce que l'API fournit au site

| Besoin du site | État dans l'API |
| --- | --- |
| **Texte alternatif** des photos | ✅ colonne `picture.alt_text`, facultative, 300 caractères au plus ; le chasseur la remplit à l'ajout |
| **Messages d'erreur clairs** | ✅ une erreur `422` nomme le champ fautif ; les contraintes de la base ont un message lisible |
| **Motifs de refus** en mots | ✅ liste fermée (`too_expensive`, `too_far`…), que le site traduit en phrases |
| Pas de **délai trop court** | ✅ connexion valable 60 min, code d'activation 7 jours |

## 4. Vérifier

- **Outils gratuits** : axe DevTools, WAVE, Lighthouse (Chrome). Ils ne trouvent qu'une partie des problèmes.
- **À la main** : tout le parcours au clavier seul, puis avec un lecteur d'écran (NVDA, gratuit).
- **Avec des personnes concernées** : le seul test qui compte vraiment.

## 5. Limites

- ⚠️ Pas de site, donc **aucun audit réel** : la note fixe des exigences, elle ne prouve rien.
- ⚠️ Les **photos importées** des annonces n'ont pas de texte alternatif. Nos données sont fictives : les remplir n'aurait pas de sens. La colonne est prête ; son remplissage, par le chasseur ou par une IA relue, est prévu en **v2**.

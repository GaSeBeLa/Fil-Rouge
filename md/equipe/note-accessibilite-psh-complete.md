> **Version complète, gardée en annexe.** Le livrable est la version courte : `livrables/5-transverse/note-accessibilite-psh.md` (2026-11-20).

# ♿ Note d'accessibilité (PSH) — l'espace acquéreur

> **Note de préconisations d'accessibilité** (BC02, BC03).
> Exigée par le `Readme.md` du sujet (StarterPack - BASE, § « Accessibilité (PSH) ») : « Visez au minimum les critères de contraste, navigation clavier, tailles de cibles, alternatives textuelles ».
> Exigence du cahier des charges, dans le modèle du sujet : **ENF-05**, « L'espace acquéreur respecte le RGAA niveau AA » (`CAHIER-DES-CHARGES-TECHNIQUE.md:99`).
> Brouillon du Glaude, 2026-11-19, **à relire par le groupe**.

---

## 1. Le périmètre

- Le projet ne livre **pas** de site web : il livre la base et l'API. Cette note dit donc **ce que le futur site devra respecter**, et **ce que l'API doit lui fournir** pour y arriver.
- **Les écrans visés** : le parcours du particulier (`user-stories/01` à `03`).
  - Le formulaire de demande de recherche.
  - La finalisation du compte, avec le code d'activation.
  - La liste des biens proposés, et la fiche d'un bien avec ses photos.
  - La décision du client : intéressé, ou refus avec un motif.
- **Les normes de référence** :
  - **WCAG 2.2**, niveau **AA** : la norme internationale du W3C ([Recommandation du 12 décembre 2024](https://www.w3.org/TR/WCAG22/), lue le 2026-11-19).
  - **RGAA 4.1.2** : sa déclinaison française. Version citée par plusieurs audits de 2025 ; une version 5 est annoncée. ⚠️ C'est un faisceau de sources secondaires, pas la page officielle : à revérifier sur accessibilite.numerique.gouv.fr avant le rendu.

## 2. Les préconisations, critère par critère

| Thème | Ce que le site doit faire | Critère WCAG 2.2 | Niveau |
| --- | --- | --- | --- |
| 🎨 **Contraste** du texte | « a contrast ratio of at least 4.5:1 » entre le texte et son fond | 1.4.3 | AA |
| 🎨 Contraste des **boutons, champs, icônes** | « at least 3:1 against adjacent color(s) » | 1.4.11 | AA |
| ⌨️ **Clavier** | tout le parcours se fait **sans souris** : remplir le formulaire, ouvrir un bien, dire « intéressé » | 2.1.1 | A |
| ⌨️ **Focus visible** | on voit toujours où est le curseur du clavier | 2.4.7 | AA |
| ⌨️ Focus **pas caché** | un bandeau (cookies, menu collant) ne recouvre pas l'élément actif | 2.4.11 | AA |
| 👆 **Taille des cibles** | « at least 24 by 24 CSS pixels » pour chaque bouton ou lien | 2.5.8 | AA |
| 🖼️ **Alternatives textuelles** | chaque photo d'un bien a un texte qui la décrit ; une photo décorative est ignorée | 1.1.1 | A |
| 📝 **Étiquettes** | chaque champ du formulaire a une étiquette visible (« Budget maximum, en euros ») | 3.3.2 | A |
| ⚠️ **Erreurs** | une erreur est dite **en texte**, près du champ, pas seulement en rouge | 3.3.1 | A |
| 🔍 **Zoom** | le texte s'agrandit jusqu'à « 200 percent without loss of content or functionality » | 1.4.4 | AA |

## 3. Pour les lecteurs dyslexiques

Ce ne sont pas des critères WCAG, mais des **bonnes pratiques**. Une personne de l'équipe est concernée, et les a éprouvées sur nos propres documents :

- une police très lisible, par exemple **Atkinson Hyperlegible** (gratuite) ;
- un fond **crème**, pas blanc pur, et un texte brun foncé, pas noir pur : un contraste fort fatigue ;
- des phrases courtes, **une idée par ligne**, des listes plutôt que des blocs ;
- **aucun texte en capitales**, ni en italique.

## 4. Ce que l'API doit fournir au site

| Besoin du site | État dans l'API | À faire |
| --- | --- | --- |
| Un **texte alternatif** pour chaque photo | ✅ colonne `picture.alt_text`, facultative, 300 caractères au plus, ajoutée le 2026-11-19 (`Fil-Rouge-API` `981c1c7`, migration 53, testée) | le chasseur la remplit quand il ajoute une photo ; les photos importées n'en ont pas |
| Des **messages d'erreur clairs**, en français | ✅ le routeur commun rend un `422` qui nomme le champ fautif ; les contraintes de la base ont un message lisible (fiche FIN1) | — |
| Les **motifs de refus** dits en mots | ✅ liste fermée (`too_expensive`, `too_far`…) : le site les traduit en phrases | — |
| Pas de **délai trop court** | ✅ le jeton dure 60 min, le code d'activation 7 jours | — |

## 5. Comment le vérifier

- **Outils automatiques**, gratuits : l'extension de navigateur **axe DevTools** ou **WAVE**, et le contrôle « Accessibility » de **Lighthouse** dans Chrome. Ils ne trouvent qu'une partie des problèmes : le contrôle à la main reste nécessaire.
- **À la main** : faire tout le parcours **au clavier seul**, puis avec un **lecteur d'écran** (NVDA, gratuit sous Windows).
- **Avec des personnes concernées** : le seul test qui compte vraiment.

## 6. Limites

- ⚠️ Pas de site, donc **aucun audit réel** : cette note fixe des exigences, elle ne prouve rien.
- ⚠️ Les **photos importées** des annonces n'ont pas de texte alternatif : seules les photos ajoutées à la main en auront un. Nos données sont fictives : les remplir n'aurait pas de sens. La colonne est **prête** ; son remplissage, par le chasseur ou par une IA relue, est prévu en **v2** (remarque de Laurence, 2026-11-19).

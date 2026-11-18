# Bobinou — Design system (v1)

Direction **« Atelier »** : écru, terracotta, indigo de teinture. Chaleureux et un peu
artisanal, pour parler aux métiers d'art plutôt qu'aux outils de bureau — mais sourd :
l'interface ne porte jamais de couleur saturée, pour ne pas concurrencer les couleurs
du modèle, qui sont la matière du travail.

Maquettes (canvas d'artboards, 14 écrans) :
https://claude.ai/artifact/HquaXAVVUR66cjeBs368AA

Jetons : [`tokens.json`](./tokens.json) · Écrans : [`screens.md`](./screens.md)

## Charte graphique

| | Valeur | Usage |
| --- | --- | --- |
| Écru | `#F7F2E9` | Fond d'application |
| Lin | `#FDFBF7` | Cartes, surfaces |
| Encre | `#221F1C` | Texte principal (14,8:1) |
| Encre douce | `#5A544C` | Texte secondaire (6,4:1) |
| Bordure | `#E3DAC9` | Traits, séparateurs |
| Trait de calque | `#141414` | Contours générés |
| Terracotta | `#B4532F` | Action principale (blanc dessus 5,3:1) |
| Terracotta clair | `#F0DED4` | Sélection, fond d'action |
| Indigo | `#2C3C5A` | Cotes, repères, totaux |
| Sauge | `#3C5A41` | Validé, en stock |
| Ambre | `#8A5A00` | À vérifier, estimation |
| Brique | `#A33327` | Erreur, manque |

**Typographie.** *Fraunces* (serif humaniste, empattements un peu « tissés ») pour les
titres ; *Inter* pour toute l'interface. Chiffres en `tabular-nums` partout où une valeur
se compare d'une ligne à l'autre (cm, g, m², %).

**Formes.** Rayons 8 (vignettes) / 16 (cartes) / 999 (boutons, puces). Boutons en pilule,
hauteur 54 px pour l'action principale, 44 px minimum partout ailleurs. Ombres rares :
`raised` pour l'onglet actif d'un segment, `float` pour une feuille qui flotte.

**Iconographie.** Trait 1,6 px, bouts arrondis, jamais remplie. Jamais d'emoji.

**Mascotte.** La bobine de Bobinou, avec deux yeux et un sourire, apparaît dans les
cartes d'aide et les confirmations — pas dans les barres d'outils.

## Ton de voix

- On tutoie l'étudiant ; l'app dit « je » (« je redresse la perspective »).
- On encourage sans en faire trop : « Bon tissage ! », jamais trois points d'exclamation.
- Pas de jargon logiciel. Le vocabulaire est celui du métier : calque, contexture, trame,
  chaîne, écheveau, bain de teinture, lisière.
- Un chiffre estimé le dit : « estimation à partir d'une consommation moyenne ».

## Trois principes

1. **L'app propose, le lissier tranche.** Contours, regroupement des tons, quantités :
   tout résultat automatique est une proposition modifiable, jamais un verdict. Un
   « Ajuster » accompagne chaque calcul.
2. **La mesure est visible.** Dimensions, surfaces et quantités s'affichent avec leur
   unité et leur source (saisie / calculée / estimée).
3. **Une main sur l'écran.** L'étudiant travaille debout devant son métier : cibles
   ≥ 44 px, action principale en bas, aucun geste à deux doigts indispensable.

## Composants

Boutons (primaire pilule, secondaire contour, fantôme, désactivé, icône) · champs avec
label + aide + état d'erreur · curseur (niveau de détail, nombre de tons, contexture,
marge) · segment (domestique / ornemental, numéros / couleurs) · puces de ton (pastille +
numéro + surface) · carte projet · ligne de liste de matière · fil de progression
« Étape n sur 6 » · bandeau de confirmation sombre · carte d'aide à la mascotte · état vide.

## Points encore ouverts

Les valeurs chiffrées des maquettes (consommations g/m², contextures, conditionnement des
écheveaux, nombre de tons d'un ouvrage type) sont des **placeholders**, en attente des
réponses de Justine. Le calcul affiché suit la formule de la vision fonctionnelle :
`Quantité = Surface × Consommation(fibre, contexture) × (1 + marge)`.

# Écrans (MVP étudiants)

Parcours en 6 étapes, 12 écrans + 2 planches de fondations. Chaque artboard du canvas
porte le nom de fichier indiqué.

Trois séries coexistent sur le canvas :

| Série | Ce qu'elle est | Typo |
| --- | --- | --- |
| v1 — `Accueil`, `Capture`… | premier jet | Fraunces + Inter |
| V2 — `AccueilV2`… | direction « Bobinou te guide » : titres en phrases, ombres, rayons unifiés | Young Serif + Space Grotesk |
| V3 — `CaptureV3`… | V2 + le fil de progression à la place de la barre, sur les 6 écrans qui portent une étape | Young Serif + Space Grotesk |

La série v1 est conservée comme archive ; elle n'a pas été reprise.

## Fondations

| Artboard | Contenu |
| --- | --- |
| `Main` | Charte graphique : palette, contrastes, typographie, principes, ton de voix |
| `Systeme` | Composants : espacement, rayons, icônes, actions, saisie, blocs, progression |

## F1 — Du modèle au calque

| # | Artboard | Rôle | À noter |
| --- | --- | --- | --- |
| 1 | `Accueil` | Liste des projets, nouveau projet, import galerie | Statut par projet : Calque / Palette / Chiffré |
| 2 | `Capture` | Prise de vue, 4 poignées de perspective | Fond sombre ; mire de calibration optionnelle |
| 3 | `Calque` | Contours générés, curseur de détail | Interactif : le curseur change le nombre de traits |
| 4 | `Retouche` | Crayon, gomme, main, lisser ; épaisseur | Annuler / rétablir dans la barre du haut |
| 5 | `Dimensions` | Largeur × hauteur en cm, contexte d'usage | Fixe l'échelle du PDF **et** toutes les surfaces |
| 6 | `ExportCalque` | Pavage A4 / A3 / traceur, repères, recouvrement | 120 × 90 cm → 24 pages A4 (6 × 4) |

## F2 — Distinction des couleurs

| # | Artboard | Rôle | À noter |
| --- | --- | --- | --- |
| 7 | `Palette` | Réduction de palette, 4 → 16 tons | Interactif : fusionne les tons voisins les plus légers et recolore l'aperçu |
| 8 | `Tons` | Fusionner / séparer / renommer, réf. nuancier | Conseil mascotte : deux tons proches = un bain en moins |
| 9 | `Zones` | Calque numéroté façon peinture par numéros | Bascule Numéros / Couleurs / Les deux + légende |

## F3 — Chiffrage matière

| # | Artboard | Rôle | À noter |
| --- | --- | --- | --- |
| 10 | `Chiffrage` | Fibre, contexture, marge de perte | Interactif : total recalculé en direct ; chaîne comptée à part |
| 11 | `Matiere` | Poids et écheveaux par ton, statut | À teindre / en stock / à demander |
| 12 | `Fiche` | Fiche de préparation PDF, sections à inclure | 2 pages A4 + les 24 pages de calque |

## Hors MVP (déjà prévus dans la navigation)

- Nuanciers fournisseurs ou de l'école (la pastille « Réf. à associer » devient un choix).
- Partage à l'enseignant (le bouton existe dans `Fiche`).
- Devis client et mesure d'objet par caméra : version pro, aucun écran dessiné.

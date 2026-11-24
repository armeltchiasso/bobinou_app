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
| 3 | `Calque` | Contours générés, curseur de détail | Interactif : le curseur change le nombre de traits **et le pas des bandes** (détaillé → 20 cm, large → 40 cm) |
| 4 | `Retouche` | Crayon, gomme, main, lisser ; épaisseur | Annuler / rétablir dans la barre du haut |
| 5 | `Dimensions` | Largeur × hauteur en cm, **technique**, contexte d'usage | Fixe l'échelle du PDF **et** toutes les surfaces ; la technique commande le miroir et le pas |
| 6 | `ExportCalque` | **Miroir**, découpe en bandes, cordeau, recouvrement | **À refaire** : le pavage A4 libre n'est pas la bonne découpe — voir ci-dessous |

### À refaire sur F1 — révision du 2026-11-23

Les réponses métier ([`../docs/reponses-metier.md`](../docs/reponses-metier.md))
invalident l'export tel qu'il est maquetté. Deux corrections, toutes deux sur
`ExportCalque` :

- **Miroir obligatoire.** En haute lice le licier est derrière le métier et voit le
  calque à contre-jour, donc inversé ; en basse lice il est « repris à l'envers » sur
  papier toilé. Un calque en lecture directe ne sert à rien. Ce n'est pas une option de
  confort : c'est le sens d'emploi par défaut.
- **Bandes horizontales, pas un pavage.** Le calque se fragmente en bandes de **20 cm**
  (motifs détaillés) ou **40 cm** (motifs larges) : au-delà, les fils travaillent et un
  trait horizontal devient une dent de scie. Chaque bande porte en pleine largeur la
  **ligne de cordeau** qui sert de repère maître au remontage, et chevauche la partie
  déjà tissée. L'exemple « 120 × 90 cm → 24 pages A4 (6 × 4) » est à remplacer par un
  découpage en hauteur : 90 cm au pas de 20 → 5 bandes (4 × 20 + recouvrement), chacune
  imprimée en lés sur la largeur selon le traceur disponible.

## F2 — Distinction des couleurs

| # | Artboard | Rôle | À noter |
| --- | --- | --- | --- |
| 7 | `Palette` | **Choix de technique** puis réduction de palette | **À refaire** : le curseur 4 → 16 tons ne peut pas être l'entrée — voir ci-dessous |
| 8 | `Tons` | Fusionner / séparer / renommer, réf. nuancier | Conseil mascotte : deux tons proches = un bain en moins |
| 9 | `Zones` | Calque numéroté façon peinture par numéros | Bascule Numéros / Couleurs / Les deux + légende |

### À refaire sur F2 — révision du 2026-11-23

Le métier ne raisonne pas en nombre de tons mais en **technique d'interprétation**, et le
nombre de tons en découle (Galice, p. 61) : « à partir de ce choix, pourront être
sélectionnés la couleur, le nombre de tons ainsi que la quantité ».

- L'entrée de `Palette` devient le choix **aplats / hachure / chiné / demi-duite**, d'après
  le modèle. Le curseur de tons reste, mais en dessous.
- **Une hachure classique fabrique trois zones intermédiaires entre deux tons.** La
  réduction de palette doit les compter comme produites au métier, pas comme des bains à
  teindre — sinon la liste de matière surestime le nombre de couleurs à acheter.
- Le **chiné** obtient des transparences en mélangeant des brins sur une même broche : il
  réduit les couleurs achetées sans réduire les couleurs vues. Déconseillé sur de très
  petites surfaces, où le brin minoritaire peut ne jamais apparaître — la **demi-duite**
  prend le relais.
- En **Savonnerie**, le ton se juge sur un pompon tondu, pas sur un écheveau, et il faut
  forcer un peu la valeur : au sol le tapis reçoit la lumière à jour frisant, ce qui
  rabat les couleurs. Si l'app propose un rendu, il doit le dire.

Le nuancier de l'école est indexé **clarté × chroma × teinte** (références du type
`50 80 180/6`). La pastille « Réf. à associer » de `Tons` peut viser ces coordonnées
plutôt qu'un RGB libre.

`Zones` est en revanche **confirmé tel quel** : la codification du calque fait main
consiste bien à donner à chaque zone un numéro renvoyant à une teinte ou à un mélange de
fils. Mais l'ordre compte — ce code se fixe **après** l'échantillonnage, pas avant. Les
numéros de `Zones` ne valent donc qu'une fois les tons arrêtés en 7 et 8.

## F3 — Kilotage (ex « chiffrage matière »)

**Renommé le 2026-11-24.** Le métier nomme déjà cette opération : « à partir du carton,
le lissier évalue la quantité de matériaux (laine, soie, fils d'or et d'argent) dont il
a besoin. On appelle cette opération le **kilotage** » — et elle lui sert à chiffrer le
coût de son travail, ce qui est la rubrique du dossier de BMA. Détail et sources dans
[`../docs/reponses-metier.md`](../docs/reponses-metier.md) § 9.

« Chiffrage matière » était une invention d'interface ; le mot juste existe, il est
libre, et il est dans le vocabulaire que l'étudiant apprend. À reprendre sur les
artboards.


| # | Artboard | Rôle | À noter |
| --- | --- | --- | --- |
| 10 | `Chiffrage` | Fibre, contexture, marge de perte, **essai pesé** | Interactif : total recalculé en direct ; chaîne comptée à part |
| 11 | `Matiere` | Poids et écheveaux par ton, statut | À teindre / en stock / à demander |
| 12 | `Fiche` | Fiche de préparation PDF, sections à inclure | 2 pages A4 + les bandes de calque |

### À ajouter sur F3 — révision du 2026-11-23

Les placeholders ont leurs valeurs : consommation **1 à 2 kg/m²**, contextures de **2 à 8
fils de chaîne au centimètre** (table complète dans
[`../docs/reponses-metier.md`](../docs/reponses-metier.md)). Mais un facteur 2 sur la
consommation écrase le reste du calcul.

D'où un champ qui n'est pas maquetté : **« j'ai pesé mon essai »** — essai tissé de
10 × 10 ou 20 × 20 cm, poids en grammes. C'est la méthode du métier, et elle fait passer
la consommation de *estimée* à *mesurée*, donc toute la ligne de `Matiere` avec elle.
Deux raisons de ne pas la court-circuiter : la consommation « peut être différente selon
la main de chacun », et le référentiel BMA évalue **l'échantillonnage comme une
compétence à part entière**. L'app doit l'outiller, pas la remplacer.

## Hors MVP (déjà prévus dans la navigation)

- Nuanciers fournisseurs ou de l'école (la pastille « Réf. à associer » devient un choix).
- Partage à l'enseignant (le bouton existe dans `Fiche`).
- Devis client et mesure d'objet par caméra : version pro, aucun écran dessiné.

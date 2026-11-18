# Bobinou v2 — direction « Bobinou te guide »

Note de conception, 18 novembre 2026. Cible : le canvas
[Bobinou — Design system & écrans](https://claude.ai/artifact/HquaXAVVUR66cjeBs368AA).

## Intention

La v1 est juste mais froide : elle se lit comme une notice technique alors qu'elle
s'adresse à des étudiants lissiers. On garde la palette « Atelier » telle quelle
(Armel l'aime) et on va chercher la chaleur ailleurs : formes, typographie, voix.
La v2 vit à côté de la v1 sur le même canvas ; la v1 n'est pas touchée.

Ce qui rend la v1 froide, relevé dans les fichiers :

- Fraunces 600 sur les titres et micro-labels 12 px en capitales espacées.
- Cartes plates à filet 1 px partout, aucune élévation, états vides en pointillés.
- Rayons incohérents : 8, 10, 12, 16 et pilule se croisent (CTA Accueil à 12 px,
  CTA Calque en pilule).
- La mascotte perd son visage dès qu'elle entre dans l'app : dans l'en-tête de
  l'Accueil elle est réduite à trois rectangles, sans yeux ni sourire.

## Objectifs

- Une v2 visiblement plus accueillante que la v1, à palette identique.
- Un langage de formes unique, appliqué partout.
- La mascotte devient la voix de l'app, pas seulement un logo.
- Les écrans restent utilisables debout devant un métier, mains occupées.

## Non-objectifs

- Pas de changement de palette : les hex de la v1 sont repris à l'identique.
- Pas de nouvelle fonctionnalité, pas de nouvel écran, pas de nouveau parcours.
- Pas de code applicatif : on reste sur le canvas de maquettes.
- Pas de retouche de la v1, note parasite comprise (décision séparée).

## Anti-objectifs

Ce qui ferait rater la v2 même si elle « marche » :

- Une app devenue enfantine : la mascotte amuse mais ne doit jamais gêner le travail.
- Un contraste dégradé au nom de la douceur — les seuils v1 restent des planchers.
- Une densité d'information en baisse : les chiffres (cm, g, m², %) doivent rester
  comparables d'une ligne à l'autre.
- Une direction qui concurrencerait les couleurs du modèle à l'écran.

## Contraintes reprises de la v1

- Palette figée : écru `#F7F2E9`, lin `#FDFBF7`, encre `#221F1C`, encre douce
  `#5A544C`, bordure `#E3DAC9`, trait de calque `#141414`, terracotta `#B4532F`,
  terracotta clair `#F0DED4`, indigo `#2C3C5A`, sauge `#4A6B4F`, ambre `#8A5A00`,
  brique `#A33327`.
- L'interface reste sourde : l'image et la palette de l'ouvrage sont les seules
  zones saturées de l'écran.
- Cibles tactiles ≥ 44 px, action principale en bas de l'écran.
- Les tons du modèle portent toujours un libellé texte ; jamais la couleur seule.
- Contrôles réels (`button`, `a href`, `input` + `label`), `aria-label` sur les
  icônes seules, contrastes texte ≥ 4,5:1.
- Chaque résultat calculé reste une proposition modifiable, jamais un verdict.

## Approches envisagées

Inspiration : `~/projects/perso/awesome-design-md` (84 DESIGN.md). Airbnb pour la
géométrie douce à accent unique et aux titres modestes, Notion pour les surfaces
chaudes, Pinterest pour l'arrondi généreux.

| | Approche | Ce qu'elle troque |
|---|---|---|
| A | **Atelier adouci** — échelle de rayons unique, un étage d'ombre à la place des filets, fin des capitales, plus d'air | Peu risqué mais reste une v1 peignée : pro, pas vraiment accueillant |
| B | **Bobinou te guide** *(retenue)* — A, plus la mascotte comme voix de l'app, titres en phrases, axes SOFT/WONK de Fraunces | Plus de travail d'illustration ; la mascotte peut encombrer si elle n'est pas cadrée |
| C | **Grosses touches** — le tactile plutôt que le mignon : corps 18-20 px, action pleine largeur 64 px, pastilles grosses comme des écheveaux | Moins d'éléments par écran, plus de défilement |

Armel a retenu **B**. C'est la seule qui exploite un atout déjà là — la bobine qui
sourit — et la palette étant figée, la chaleur doit venir de la forme, de la typo
et de la voix.

## Le système v2

### Formes

Une seule échelle, appliquée sans exception :

| Rôle | Rayon |
|---|---|
| Pastilles, badges, boutons, segments | 999 px (pilule) |
| Vignettes de projet | 14 px |
| Champs de saisie | 16 px |
| Cartes | 20 px |
| Panneaux et feuilles (zone image, modale) | 28 px |

Un seul étage d'élévation, qui remplace le filet 1 px sur les surfaces posées :
`0 2px 4px rgba(34,31,28,0.04), 0 8px 24px -8px rgba(34,31,28,0.10)`. La bordure
`#E3DAC9` ne sert plus qu'aux séparateurs et aux contours de champs. Les états
vides passent du pointillé à une carte en lin avec illustration.

### Typographie

Fraunces reste, mais sur ses axes variables doux : `SOFT 100`, `WONK 1` —
empattements arrondis et italiques légèrement de guingois, même famille.

```
https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,400..700,100,1&family=Inter:wght@400;500;600;700&display=swap
```

avec `font-variation-settings: 'SOFT' 100, 'WONK' 1` sur les titres. Inter garde
le corps : ses chiffres tabulaires sont indispensables aux cm, g et m².

| Rôle | Taille / interligne | Police |
|---|---|---|
| Display | 34/40, 600, -0.01em | Fraunces soft |
| Titre d'écran | 22/28, 500 | Fraunces soft |
| Sous-titre | 18/26, 500 | Fraunces soft |
| Corps | 16/26, 400 | Inter |
| Bouton | 17/20, 600 | Inter |
| Secondaire | 15/22, 400 | Inter |
| Label | 14/20, 500, casse normale | Inter |
| Chiffres | `tabular-nums` | Inter |

Les capitales espacées disparaissent : un label se lit « Largeur de l'ouvrage »,
pas « LARGEUR DE L'OUVRAGE ». Le secondaire passe de 13 à 15 px.

### La mascotte

Trois emplois, pas un de plus :

1. **Le guide** — bobine 32 px au visage, suivie d'une phrase de conduite, en tête
   des écrans d'étape.
2. **Les états vides et les confirmations** — illustration 96 à 120 px.
3. **Le logo** — il retrouve ses yeux et son sourire partout, y compris en 26 px.

Règles : une seule apparition par écran ; jamais au-dessus de la zone image ou du
calque ; jamais sur une erreur bloquante, qui reste du texte sobre en brique.

### La voix

Les titres d'écran deviennent des phrases courtes — « On passe aux contours »
plutôt que « Calque », « Je t'ai trouvé 32 zones » plutôt que « 32 zones
détectées ». Tutoiement, l'app dit « je », pas d'emoji, pas de points
d'exclamation en rafale. Les calculs restent annoncés comme des propositions.

## Périmètre de cette passe

Quatorze nouveaux artboards, en trois rangées sous la v1. Première passe : les
fondations et quatre écrans témoins. Seconde passe, après validation de la
direction : les huit écrans restants, et les liens de navigation des écrans v2
redirigés vers leurs suites v2 pour que le parcours soit cliquable de bout en
bout sans retomber dans la v1.

| Fichier | Format | Contenu |
|---|---|---|
| `project/MainV2.dc.html` | 1280 × 1700 | Charte v2 |
| `project/SystemeV2.dc.html` | 1280 × 1700 | Composants v2 |
| `project/AccueilV2.dc.html` | 390 × 844 | Mes projets |
| `project/CalqueV2.dc.html` | 390 × 844 | Générer le calque |
| `project/PaletteV2.dc.html` | 390 × 844 | Réduire la palette |
| `project/FicheV2.dc.html` | 390 × 844 | Fiche de préparation |

| `project/CaptureV2.dc.html` | 390 × 844 | Cadrer le modèle |
| `project/RetoucheV2.dc.html` | 390 × 844 | Retoucher |
| `project/DimensionsV2.dc.html` | 390 × 844 | Dimensions & contexte |
| `project/ExportCalqueV2.dc.html` | 390 × 844 | Export PDF 1:1 |
| `project/TonsV2.dc.html` | 390 × 844 | Ajuster les tons |
| `project/ZonesV2.dc.html` | 390 × 844 | Zones numérotées |
| `project/ChiffrageV2.dc.html` | 390 × 844 | Paramètres matière |
| `project/MatiereV2.dc.html` | 390 × 844 | Liste de matière |

La numérotation des étapes est remise d'équerre sur les six temps du parcours
(1 photo, 2 contours, 3 échelle, 4 palette, 5 chiffrage, 6 fiche) : la v1 était
incohérente, le Calque y annonçant tantôt l'étape 2, tantôt l'étape 3.

Aucun fichier v1 n'est modifié ni supprimé.

## Laissé au constructeur

- Le dessin exact des illustrations d'état vide et de confirmation.
- La formulation de la phrase de guidage de chaque écran.
- Le micro-placement dans chaque écran, à partir du contenu de l'écran v1 jumeau.
- Les placeholders de chiffrage restent ceux de la v1, en attente des réponses de
  Justine.

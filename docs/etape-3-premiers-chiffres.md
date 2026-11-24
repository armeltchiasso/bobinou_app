# Étape 3 — premiers chiffres du prototype

2026-11-24. Premier passage de [`prototype/`](../prototype/) sur le cas de référence.

**Ce n'est pas le verdict de l'étape 3.** Le verdict demande le test papier avec Ju,
les 3 ouvrages réels et l'analyse de sensibilité. Ce document dit seulement ce que le
script mesure aujourd'hui, et ce qu'on a appris en le confrontant au calque fait main.

## Le cas

`oeuvres/IMG_1217` — deux tapisseries de basse lice tissées **du même calque**, dans
deux gammes opposées. Et `calques/IMG_1215` est la photo de ce calque. C'est la seule
vérité terrain directe du corpus : on peut confronter le tracé généré à celui qu'une
lissière a réellement produit.

**Cote retenue : 60 × 100 cm (0,60 m²).** Déduite du rapport largeur/hauteur mesuré
sur la photo redressée (0,60), **pas relevée au mètre**. À confirmer avec Ju — toutes
les surfaces et le chiffrage en dépendent proportionnellement.

Facteur d'agrandissement de la photo à l'ouvrage : **×12,2**. Galice décrit ce procédé
et son mode de ruine au-delà d'une dizaine de fois (p. 177). On est pile dans la zone
où « le moindre petit moucheté devient un groupe de taches ». C'est visible plus bas.

## Les trois niveaux

| Niveau | Tons | Zones | Zones < 1 cm² | Tracé (cm) | Aire médiane | Pas | Bandes | Pages A4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `fin` | 16 | **391** | **182** | 17 572 | 1,11 cm² | 20 | 5 | 20 |
| `moyen` | 12 | 66 | 0 | 7 274 | 7,94 cm² | 20 | 5 | 20 |
| `large` | 6 | **24** | 0 | 3 030 | 145,55 cm² | 40 | 3 | 20 |

Lecture : `fin` est inexploitable. 182 de ses 391 zones font moins d'un centimètre
carré — à 5 fils/cm, une zone d'un cm² fait 5 fils sur 5 duites. Ce ne sont pas des
zones, c'est du bruit de photo promu au rang de motif. C'est exactement l'effet que
Galice attribue à l'agrandissement.

`large` donne 24 zones de 145 cm² médians. C'est un calque.

Le nombre de pages est le même partout (20) : les bandes de `large` sont deux fois
plus hautes mais deux fois moins nombreuses. Le pas ne change pas le volume de papier,
il change **le rythme de travail** — 3 remontages de calque au lieu de 5.

## Confrontation au calque fait main

| | Fait main (`IMG_1215`) | Généré (`large`) |
| --- | --- | --- |
| Zones fermées | **25** | **27** |
| Encre | 126 kpx | 71 kpx |

Deux zones d'écart sur vingt-cinq. Et l'orientation est la bonne : le calque généré
sort dans le même sens que celui de la lissière — la colombe à gauche, alors qu'elle
est à droite sur la tapisserie. Le miroir est juste.

**Ce que la comparaison ne prouve pas.** Elle n'aligne pas les tracés au millimètre :
la feuille est tenue à la main, gondolée, photographiée de biais, et une homographie
ne corrige pas une ondulation de papier. On juge la présence et la forme des traits,
pas leur position. Le chiffre de 25 contre 27 ne doit pas être lu comme une précision
de 92 % — il dit que la structure est la même.

### Où ça tient, où ça casse

Côte à côte (`sorties/comparaison_cote_a_cote.png`), la séparation est nette et elle
suit exactement la typologie de cas prévue au plan :

**Ça tient** — les six panneaux d'aplats géométriques : colombe, trèfle, étoile,
poisson, et les deux panneaux de formes. Mêmes contours, mêmes découpes internes, à
l'angulosité près. Sur ceux-là, le tracé généré est de qualité comparable au fait main.

**Ça casse** — les deux panneaux du haut, les seuls figuratifs. Le rinceau végétal perd
ses courbes, qui deviennent des polygones à angles vifs. Le caniche perd son visage :
la lissière a tracé l'œil, le museau, les mèches ; le script rend une masse avec deux
accidents. Il perd aussi les petits détails isolés que le fait main garde — l'œil de la
colombe, l'œil du poisson.

C'est la case « zones fines (visage, main) — là où le calque auto casse » du tableau du
§ 1, confirmée sur pièce. Avec une nuance utile : ça ne casse pas partout, ça casse
**là où c'est figuratif**, et le reste de la planche est bon.

## Palette, niveau `large`

| Ton | Surface | Part |
| --- | --- | --- |
| `#070E2D` | 2 141 cm² | 35,7 % |
| `#A26C83` | 1 186 cm² | 19,8 % |
| `#9F3B67` | 731 cm² | 12,2 % |
| `#6A81AD` | 729 cm² | 12,2 % |
| `#48508F` | 639 cm² | 10,6 % |
| `#171E5A` | 575 cm² | 9,6 % |

Deux bleus nuit très proches (`#070E2D` et `#171E5A`) sortent séparés alors qu'ils sont
probablement un seul bain plus une ombre de photo. C'est le conseil de la mascotte de
l'écran `Tons` — « deux tons proches = un bain en moins » — qui se trouve justifié par
la mesure, pas par le design.

À 1–2 kg/m² sur 0,60 m², l'ouvrage pèse **0,6 à 1,2 kg** de laine. La fourchette reste
du simple au double tant qu'on n'a pas pesé un essai.

## Ce que ça change pour la suite

1. **Trois niveaux, c'est un de trop.** `fin` ne produit jamais rien d'utilisable à ce
   facteur d'agrandissement. Soit le curseur démarre à `moyen`, soit `fin` n'est
   proposé que sous un seuil d'agrandissement.
2. **Le facteur d'agrandissement mérite un avertissement dans l'app**, pas seulement
   une mesure. Au-delà de ×10, prévenir : « ta photo est petite pour un ouvrage de
   cette taille, le tracé va se fragmenter ».
3. **La retouche de F1 doit viser le figuratif.** Les aplats sortent bons tout seuls.
   C'est sur les visages et les courbes que l'étudiant passera son temps — donc les
   outils à soigner sont la courbe et le détail isolé, pas le polygone.
4. **Le pas change le rythme, pas le papier.** Bon argument pour laisser le choix au
   lissier plutôt que de l'optimiser automatiquement.

## Reste à faire

- Le **test papier** avec Ju : imprimer deux bandes consécutives, les poser à l'envers
  sur le métier, et poser les quatre questions du § 3 du plan.
- Les **cotes réelles**, qui remplaceront le 60 × 100 déduit.
- Les **3 ouvrages** avec leur matière, pour l'écart au poids prédit.
- L'**analyse de sensibilité**.

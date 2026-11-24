# Prototype — étape 3

Un script, pas une app. Il répond à une seule question : **un calque généré
automatiquement est-il tissable ?**

Le plan complet est dans [`../docs/etape-3-prouver-le-calque.md`](../docs/etape-3-prouver-le-calque.md),
les contraintes métier et leurs sources dans [`../docs/reponses-metier.md`](../docs/reponses-metier.md).

## Installation

```
python -m venv .venv
.venv/Scripts/python.exe -m pip install numpy opencv-python-headless scikit-image reportlab
```

Testé sur Python 3.12 / Windows. Rien n'est propre à la plateforme.

## Les trois scripts

| Script | Rôle |
| --- | --- |
| `trouver_coins.py` | Repère les pièces sur une photo d'atelier et sort leurs coins |
| `calque.py` | La chaîne complète : photo → calque imprimable en bandes |
| `comparer.py` | Confronte un calque généré au calque fait main correspondant |
| `sensibilite.py` | Ce qui pèse sur le chiffrage, et quelle marge met à l'abri |

### Cadrer

Une photo d'atelier est pleine de quadrilatères — murs, rails, cadres, métiers. La
détection automatique de `calque.py` s'y trompe, donc on cadre d'abord :

```
python trouver_coins.py PHOTO.jpg --apercu
python trouver_coins.py CALQUE.jpg --clair --apercu   # feuille claire sur fond sombre
```

L'aperçu est à vérifier à l'œil : c'est deux secondes, et ça évite de mesurer un mur.

### Générer

```
python calque.py PHOTO.jpg --largeur 60 --hauteur 100 \
    --coins "217,540 732,552 693,1589 115,1565"
```

La chaîne :

```
photo → redressement → réduction de palette → zones fermées → vectorisation
      → MIROIR → PDF 1:1 découpé en BANDES avec cordeau
```

Deux étapes ne sont pas négociables, et viennent du métier :

- **le miroir** — le calque est le carton inversé, en haute lice comme en basse lice ;
- **les bandes** — 20 cm pour un motif détaillé, 40 cm pour un motif large (Galice,
  p. 69). Au-delà, les fils travaillent et un trait horizontal devient une dent de
  scie. Chaque bande porte sa ligne de cordeau et chevauche la partie déjà tissée.

### Les trois niveaux de détail

Un seul réglage, trois conséquences — c'est le curseur de l'écran `Calque`.

| Niveau | Tons | Aire mini | Tolérance | Pas |
| --- | --- | --- | --- | --- |
| `fin` | 16 | 0,5 cm² | 0,6 mm | 20 cm |
| `moyen` | 12 | 2 cm² | 1,5 mm | 20 cm |
| `large` | 6 | 8 cm² | 3 mm | 40 cm |

### Ce que sort le PDF

Une page A4 porte : le tracé détouré à sa zone utile, la **ligne de cordeau** en
pointillé orange, la zone de recouvrement hachurée, le bord de l'ouvrage en tireté,
des repères de coupe aux quatre coins, un cartouche (`bande n/N · page c/C · MIROIR`)
et un **témoin d'échelle de 100 mm**. Si ce témoin ne mesure pas 100 mm sur le papier,
l'impression n'est pas à 100 % et tout le reste est faux.

## Comparer au calque fait main

`IMG_1217` est un cas rare : deux tapisseries tissées du même calque, et la photo de
ce calque (`IMG_1215`). C'est la seule vérité terrain directe dont on dispose.

```
python comparer.py --main IMG_1215.jpeg \
    --coins-main "437,468 1076,458 1100,1778 471,1788" \
    --genere sorties/IMG_1217_calque_large.png
```

**Ce que la comparaison ne dit pas.** Elle n'aligne pas les deux tracés au
millimètre. La feuille est tenue à la main, gondolée, photographiée de biais : une
homographie ne corrige pas une ondulation de papier. L'écart visible sur la
superposition est donc en bonne partie celui de la prise de vue. On juge la
**présence** et la **forme** des traits, pas leur position.

## Chiffrer et mesurer le risque

```
python sensibilite.py --largeur 60 --hauteur 100
```

Sort trois choses : ce qui pèse sur le poids annoncé (une variable à la fois, puis la
part de variance sur 200 000 tirages), et surtout **la marge nécessaire pour ne pas
manquer de laine** selon ce que l'étudiant a mesuré. Lecture dans
[`../docs/etape-3-sensibilite.md`](../docs/etape-3-sensibilite.md).

Point de méthode à ne pas perdre : la contexture se tire **par rang entier** de la
table de Galice p. 22. Le métrage au kilo et les fils/cm y montent ensemble ; les
faire varier séparément fabrique des contextures qui n'existent pas, et un faux
résultat à 30 % d'amplitude.

## Ce qui reste à faire

- Les **3 ouvrages réels** avec leur liste de matière : l'emplacement est prévu dans
  les mesures, il calculera l'écart entre poids prédit et poids réel.
- Le **test papier** avec Ju, qui seul tranche.
- Les **cotes réelles** des pièces photographiées. Celles utilisées ici (60 × 100 cm)
  sont déduites du rapport largeur/hauteur mesuré, pas relevées au mètre.

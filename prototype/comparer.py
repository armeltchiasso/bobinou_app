#!/usr/bin/env python
"""
Compare un calque généré au calque fait main correspondant.

Le cas d'IMG_1217 est rare et précieux : deux tapisseries tissées à partir du même
calque, et la photo de ce calque (IMG_1215). C'est la seule vérité terrain directe
dont on dispose pour juger le tracé automatique.

Ce que ce script fait :
  * redresse la photo du calque fait main à partir des coins du cadre dessiné ;
  * en extrait l'encre (le tracé du lissier) ;
  * superpose le tracé généré, en rouge ;
  * compte les zones fermées de chaque côté.

Ce qu'il NE fait PAS, et qu'il ne faut pas lui faire dire : il n'aligne pas les deux
tracés au millimètre. La feuille est tenue à la main, gondolée, photographiée de
biais ; une homographie ne corrige pas une ondulation de papier. L'écart résiduel
que l'on voit sur la superposition est donc en grande partie celui de la prise de
vue, pas celui du tracé. On juge ici la PRÉSENCE et la FORME des traits, pas leur
position exacte — c'est déjà la question qui décide de l'étape 3.

Usage :
    python comparer.py --main IMG_1215.jpeg --coins-main "..." \
                       --genere sorties/IMG_1217_calque_large.png
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

PX_PAR_CM = 20.0


def ordonner(pts):
    pts = np.asarray(pts, dtype=np.float32).reshape(4, 2)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).ravel()
    return np.array([pts[np.argmin(s)], pts[np.argmin(d)],
                     pts[np.argmax(s)], pts[np.argmax(d)]], dtype=np.float32)


def redresser(img, coins, largeur_cm, hauteur_cm):
    L = int(round(largeur_cm * PX_PAR_CM))
    H = int(round(hauteur_cm * PX_PAR_CM))
    cible = np.array([[0, 0], [L - 1, 0], [L - 1, H - 1], [0, H - 1]], np.float32)
    M = cv2.getPerspectiveTransform(ordonner(coins), cible)
    return cv2.warpPerspective(img, M, (L, H), flags=cv2.INTER_AREA)


def extraire_encre(rect):
    """Isole le trait sur un papier beige, éclairé de biais : seuil adaptatif."""
    gris = cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (3, 3), 0)
    encre = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 31, 12)
    # les trous de la perforation du calque font du poivre : on l'enlève
    encre = cv2.morphologyEx(encre, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    n, comp, stats, _ = cv2.connectedComponentsWithStats(encre, 8)
    propre = np.zeros_like(encre)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= 60:        # un trait, pas un grain
            propre[comp == i] = 255
    return propre


def zones_fermees(binaire, aire_min_cm2=8.0):
    """Compte les plages que le tracé referme — l'unité de travail du lissier."""
    plein = cv2.dilate(binaire, np.ones((3, 3), np.uint8), iterations=1)
    inverse = cv2.bitwise_not(plein)
    n, _, stats, _ = cv2.connectedComponentsWithStats(inverse, 4)
    seuil = aire_min_cm2 * PX_PAR_CM ** 2
    return sum(1 for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] >= seuil)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main", type=Path, required=True, help="photo du calque fait main")
    ap.add_argument("--coins-main", type=str, required=True)
    ap.add_argument("--genere", type=Path, required=True, help="PNG du calque généré")
    ap.add_argument("--largeur", type=float, default=60.0)
    ap.add_argument("--hauteur", type=float, default=100.0)
    ap.add_argument("--miroir-main", action="store_true",
                    help="si la photo du calque fait main est dans le sens de lecture")
    ap.add_argument("--sorties", type=Path, default=Path(__file__).parent / "sorties")
    args = ap.parse_args()

    photo = cv2.imread(str(args.main))
    genere = cv2.imread(str(args.genere), cv2.IMREAD_GRAYSCALE)
    if photo is None or genere is None:
        raise SystemExit("image illisible")

    coins = np.array([[float(v) for v in p.split(",")]
                      for p in args.coins_main.split()], np.float32)
    rect = redresser(photo, coins, args.largeur, args.hauteur)
    if args.miroir_main:
        rect = cv2.flip(rect, 1)
    encre = extraire_encre(rect)

    genere = cv2.resize(genere, (encre.shape[1], encre.shape[0]),
                        interpolation=cv2.INTER_AREA)
    gen_bin = (genere < 160).astype(np.uint8) * 255

    args.sorties.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.sorties / "comparaison_main_redresse.png"), rect)
    cv2.imwrite(str(args.sorties / "comparaison_main_encre.png"),
                cv2.bitwise_not(encre))

    # superposition : le fait main en noir, le généré en rouge
    sup = np.full((*encre.shape, 3), 255, np.uint8)
    sup[encre > 0] = (30, 30, 30)
    rouge = gen_bin > 0
    sup[rouge] = (0, 0, 220)
    chevauche = (encre > 0) & rouge
    sup[chevauche] = (40, 150, 40)
    cv2.imwrite(str(args.sorties / "comparaison_superposition.png"), sup)

    # côte à côte
    gauche = cv2.cvtColor(cv2.bitwise_not(encre), cv2.COLOR_GRAY2BGR)
    droite = cv2.cvtColor(cv2.bitwise_not(gen_bin), cv2.COLOR_GRAY2BGR)
    sep = np.full((encre.shape[0], 12, 3), 200, np.uint8)
    cv2.imwrite(str(args.sorties / "comparaison_cote_a_cote.png"),
                np.hstack([gauche, sep, droite]))

    zm, zg = zones_fermees(encre), zones_fermees(gen_bin)
    encre_px = int((encre > 0).sum())
    gen_px = int(rouge.sum())

    print(f"\ncalque fait main ({args.main.name}) vs généré ({args.genere.name})")
    print(f"  surface de travail      {args.largeur:g} × {args.hauteur:g} cm")
    print(f"  zones fermées, main     {zm}")
    print(f"  zones fermées, généré   {zg}")
    print(f"  encre, main             {encre_px / 1000:.0f} kpx")
    print(f"  encre, généré           {gen_px / 1000:.0f} kpx")
    print(f"  rapport de densité      ×{gen_px / max(encre_px, 1):.2f}")
    print(f"\n  sorties dans {args.sorties}")
    print("  superposition : noir = fait main, rouge = généré, vert = les deux\n")
    print("  Rappel : pas de recalage au millimètre, la feuille est gondolée.")
    print("  On juge la présence et la forme des traits, pas leur position.\n")


if __name__ == "__main__":
    main()

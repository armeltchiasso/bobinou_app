#!/usr/bin/env python
"""Aide au cadrage : repère les pièces sur une photo d'atelier et sort leurs coins.

Une photo d'atelier contient des murs, des rails, des cadres et des métiers qui sont
tous des quadrilatères. La détection automatique du script principal s'y trompe. Ce
petit utilitaire isole ce qui est saturé ou sombre sur un mur clair, ce qui suffit
pour une tapisserie accrochée, et imprime les coins à passer à `calque.py --coins`.

Usage :
    python trouver_coins.py PHOTO.jpg [--apercu]
"""

import argparse
from pathlib import Path

import cv2
import numpy as np


def ordonner(pts):
    pts = np.asarray(pts, dtype=np.float32).reshape(4, 2)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).ravel()
    return np.array([pts[np.argmin(s)], pts[np.argmin(d)],
                     pts[np.argmax(s)], pts[np.argmax(d)]], dtype=np.float32)


def candidats(img, aire_min_frac=0.02, clair=False):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if clair:
        # une feuille de calque : claire et désaturée sur un fond plus sombre
        masque = ((gris > 150) & (hsv[:, :, 1] < 70)).astype(np.uint8) * 255
    else:
        masque = ((hsv[:, :, 1] > 55) | (gris < 110)).astype(np.uint8) * 255
    masque = cv2.morphologyEx(masque, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    masque = cv2.morphologyEx(masque, cv2.MORPH_OPEN, np.ones((15, 15), np.uint8))
    cnts, _ = cv2.findContours(masque, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    aire_mini = aire_min_frac * img.shape[0] * img.shape[1]
    out = []
    for c in sorted(cnts, key=cv2.contourArea, reverse=True):
        if cv2.contourArea(c) < aire_mini:
            break
        # le quadrilatère minimal qui enferme la pièce : robuste aux franges et aux fils
        boite = cv2.boxPoints(cv2.minAreaRect(c))
        approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
        quad = approx.reshape(-1, 2) if len(approx) == 4 else boite
        out.append((cv2.contourArea(c), ordonner(quad), cv2.boundingRect(c)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo", type=Path)
    ap.add_argument("--apercu", action="store_true",
                    help="écrit un PNG avec les coins trouvés, à vérifier à l'œil")
    ap.add_argument("--clair", action="store_true",
                    help="la pièce est claire sur fond sombre (feuille de calque)")
    args = ap.parse_args()

    img = cv2.imread(str(args.photo))
    if img is None:
        raise SystemExit(f"illisible : {args.photo}")
    print(f"{args.photo.name} — {img.shape[1]}×{img.shape[0]} px\n")

    trouves = candidats(img, clair=args.clair)
    if not trouves:
        print("rien trouvé — la pièce est peut-être claire sur fond clair")
        return

    apercu = img.copy()
    for i, (aire, quad, (x, y, w, h)) in enumerate(trouves, 1):
        rapport = w / h if h else 0
        print(f"pièce {i} : aire {aire:>9.0f} px²  bbox {w}×{h}  "
              f"rapport l/h {rapport:.2f}")
        print(f'  --coins "' +
              " ".join(f"{int(px)},{int(py)}" for px, py in quad) + '"\n')
        if args.apercu:
            cv2.polylines(apercu, [quad.astype(np.int32)], True, (0, 0, 255), 6)
            for px, py in quad:
                cv2.circle(apercu, (int(px), int(py)), 14, (0, 200, 255), -1)
            cv2.putText(apercu, str(i), (x + 20, y + 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 6)

    if args.apercu:
        sortie = args.photo.parent / f"{args.photo.stem}_coins.png"
        sortie = Path(__file__).parent / "sorties" / sortie.name
        sortie.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(sortie), apercu)
        print(f"aperçu : {sortie}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
Bobinou — prototype de l'étape 3 : du modèle photographié au calque imprimable.

Un script, pas une app. Il sert à répondre à une seule question : un calque généré
automatiquement est-il tissable ?

La chaîne suit le plan révisé (docs/etape-3-prouver-le-calque.md) :

    photo → redressement de perspective → réduction de palette → zones fermées
         → vectorisation → MIROIR → PDF 1:1 découpé en BANDES avec cordeau

Les deux contraintes qui ne sont pas négociables viennent du métier, pas du confort
d'impression (voir docs/reponses-metier.md) :

  * le calque s'emploie à l'envers, en haute lice comme en basse lice ;
  * il se fragmente en bandes de 20 cm (motifs détaillés) ou 40 cm (motifs larges),
    repérées par un cordeau, chaque bande chevauchant la partie déjà tissée.

Usage :
    python calque.py MODELE.jpg --largeur 60 --hauteur 110
    python calque.py MODELE.jpg --largeur 60 --hauteur 110 \
        --coins "130,530 730,545 725,1610 135,1600"
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field, asdict
from pathlib import Path

import cv2
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rl_canvas

cv2.setRNGSeed(20261124)

# --------------------------------------------------------------------------- #
# Niveaux de détail
# --------------------------------------------------------------------------- #
# Le pas des bandes découle du niveau : « vingt centimètres de haut pour une
# composition à motifs détaillés et quarante centimètres pour une composition à
# motifs larges » (Galice, p. 69). C'est le même réglage que le curseur de
# l'écran Calque — un seul curseur, deux conséquences.

@dataclass(frozen=True)
class Niveau:
    nom: str
    tons: int           # taille de la palette réduite
    aire_min_cm2: float  # une zone plus petite est absorbée par sa voisine
    tolerance_mm: float  # simplification du polygone
    pas_cm: int         # hauteur d'une bande

NIVEAUX = [
    Niveau("fin",   16, 0.5, 0.6, 20),
    Niveau("moyen", 12, 2.0, 1.5, 20),
    Niveau("large",  6, 8.0, 3.0, 40),
]

PX_PAR_CM = 20.0   # résolution de travail du redressement (≈ 50 dpi suffit pour des zones)
RECOUVREMENT_CM = 5.0


# --------------------------------------------------------------------------- #
# 1. Redressement de perspective
# --------------------------------------------------------------------------- #

def ordonner_coins(pts: np.ndarray) -> np.ndarray:
    """Range 4 points en haut-gauche, haut-droit, bas-droit, bas-gauche."""
    pts = np.asarray(pts, dtype=np.float32).reshape(4, 2)
    somme = pts.sum(axis=1)
    diff = np.diff(pts, axis=1).ravel()
    return np.array([
        pts[np.argmin(somme)],   # HG : x+y minimal
        pts[np.argmin(diff)],    # HD : x-y maximal
        pts[np.argmax(somme)],   # BD
        pts[np.argmax(diff)],    # BG
    ], dtype=np.float32)


def detecter_coins(img: np.ndarray) -> np.ndarray | None:
    """Cherche le plus grand quadrilatère de l'image. Faillible : une photo
    d'atelier contient des murs, des cadres et des métiers qui en sont aussi."""
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (5, 5), 0)
    bords = cv2.Canny(gris, 50, 150)
    bords = cv2.dilate(bords, np.ones((3, 3), np.uint8), iterations=2)
    contours, _ = cv2.findContours(bords, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    aire_image = img.shape[0] * img.shape[1]
    for c in sorted(contours, key=cv2.contourArea, reverse=True)[:12]:
        aire = cv2.contourArea(c)
        if aire < 0.05 * aire_image:
            break
        approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            return ordonner_coins(approx)
    return None


def redresser(img: np.ndarray, coins: np.ndarray,
              largeur_cm: float, hauteur_cm: float) -> np.ndarray:
    """Remet le modèle d'aplomb et à l'échelle réelle de l'ouvrage."""
    L = int(round(largeur_cm * PX_PAR_CM))
    H = int(round(hauteur_cm * PX_PAR_CM))
    cible = np.array([[0, 0], [L - 1, 0], [L - 1, H - 1], [0, H - 1]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(ordonner_coins(coins), cible)
    return cv2.warpPerspective(img, M, (L, H), flags=cv2.INTER_AREA)


def facteur_agrandissement(coins: np.ndarray, largeur_cm: float, hauteur_cm: float) -> float:
    """Combien de fois le modèle photographié est agrandi pour atteindre l'ouvrage.

    Galice (p. 177) décrit exactement ce procédé et son mode de ruine : « sur une
    maquette de 15 cm × 15 cm agrandie ne serait-ce que dix fois, le moindre petit
    moucheté devient un groupe de taches ». C'est la variable de risque du tracé.
    """
    c = ordonner_coins(coins)
    larg_px = (np.linalg.norm(c[1] - c[0]) + np.linalg.norm(c[2] - c[3])) / 2
    haut_px = (np.linalg.norm(c[3] - c[0]) + np.linalg.norm(c[2] - c[1])) / 2
    # 1 px de photo couvre combien de cm d'ouvrage, rapporté à une impression 300 dpi
    cm_par_px = ((largeur_cm / larg_px) + (hauteur_cm / haut_px)) / 2
    return cm_par_px * 300 / 2.54


# --------------------------------------------------------------------------- #
# 2. Réduction de palette
# --------------------------------------------------------------------------- #

def quantifier(img: np.ndarray, n_tons: int) -> tuple[np.ndarray, np.ndarray]:
    """k-moyennes dans l'espace Lab, où les distances approchent la perception.

    Rappel métier : le nombre de tons n'est pas le bon point d'entrée — on choisit
    d'abord la technique (aplats / hachure / chiné / demi-duite) et le nombre de tons
    en découle (Galice, p. 61). Ici on le fixe pour mesurer, pas pour décider.
    """
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    donnees = lab.reshape(-1, 3).astype(np.float32)
    critere = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
    _, labels, centres = cv2.kmeans(donnees, n_tons, None, critere, 5,
                                    cv2.KMEANS_PP_CENTERS)
    labels = labels.reshape(img.shape[:2])
    centres_bgr = cv2.cvtColor(centres.astype(np.uint8).reshape(-1, 1, 3),
                               cv2.COLOR_LAB2BGR).reshape(-1, 3)
    return labels, centres_bgr


def nettoyer(labels: np.ndarray, aire_min_px: float) -> np.ndarray:
    """Absorbe les îlots plus petits que l'aire minimale dans le ton majoritaire
    autour d'eux. C'est le « moucheté devenu groupe de taches » qu'on supprime."""
    sortie = labels.copy()
    for ton in np.unique(labels):
        masque = (sortie == ton).astype(np.uint8)
        n, composants, stats, _ = cv2.connectedComponentsWithStats(masque, 8)
        for i in range(1, n):
            if stats[i, cv2.CC_STAT_AREA] >= aire_min_px:
                continue
            ilot = composants == i
            dilate = cv2.dilate(ilot.astype(np.uint8), np.ones((3, 3), np.uint8))
            bord = (dilate > 0) & ~ilot
            voisins = sortie[bord]
            if voisins.size:
                sortie[ilot] = np.bincount(voisins).argmax()
    return sortie


# --------------------------------------------------------------------------- #
# 3. Vectorisation
# --------------------------------------------------------------------------- #

@dataclass
class Zone:
    ton: int
    aire_cm2: float
    perimetre_cm: float
    sommets: int
    contour_cm: list[tuple[float, float]]
    trous_cm: list[list[tuple[float, float]]] = field(default_factory=list)


def vectoriser(labels: np.ndarray, niveau: Niveau) -> list[Zone]:
    eps_px = niveau.tolerance_mm / 10.0 * PX_PAR_CM
    aire_min_px = niveau.aire_min_cm2 * PX_PAR_CM ** 2
    zones: list[Zone] = []
    for ton in np.unique(labels):
        masque = (labels == ton).astype(np.uint8)
        contours, hierarchie = cv2.findContours(masque, cv2.RETR_CCOMP,
                                                cv2.CHAIN_APPROX_SIMPLE)
        if hierarchie is None:
            continue
        hierarchie = hierarchie[0]
        for i, c in enumerate(contours):
            if hierarchie[i][3] != -1:      # c'est un trou, traité avec son parent
                continue
            if cv2.contourArea(c) < aire_min_px:
                continue
            ext = cv2.approxPolyDP(c, eps_px, True).reshape(-1, 2)
            trous = []
            j = hierarchie[i][2]
            while j != -1:
                if cv2.contourArea(contours[j]) >= aire_min_px:
                    trous.append(cv2.approxPolyDP(contours[j], eps_px, True).reshape(-1, 2))
                j = hierarchie[j][0]
            aire = cv2.contourArea(ext) - sum(cv2.contourArea(t) for t in trous)
            perim = cv2.arcLength(ext, True) + sum(cv2.arcLength(t, True) for t in trous)
            zones.append(Zone(
                ton=int(ton),
                aire_cm2=aire / PX_PAR_CM ** 2,
                perimetre_cm=perim / PX_PAR_CM,
                sommets=len(ext) + sum(len(t) for t in trous),
                contour_cm=[(x / PX_PAR_CM, y / PX_PAR_CM) for x, y in ext],
                trous_cm=[[(x / PX_PAR_CM, y / PX_PAR_CM) for x, y in t] for t in trous],
            ))
    return zones


def miroir(zones: list[Zone], largeur_cm: float) -> list[Zone]:
    """Le calque est le carton inversé. Sans ça, rien n'est tissable."""
    def flip(pts):
        return [(largeur_cm - x, y) for x, y in pts]
    return [Zone(z.ton, z.aire_cm2, z.perimetre_cm, z.sommets,
                 flip(z.contour_cm), [flip(t) for t in z.trous_cm]) for z in zones]


# --------------------------------------------------------------------------- #
# 4. Découpe en bandes
# --------------------------------------------------------------------------- #

@dataclass
class Bande:
    numero: int
    y_bas_cm: float      # dans le repère du tissage : 0 = départ, en bas
    y_haut_cm: float
    cordeau_cm: float    # la ligne de repère, en bas de la bande

def decouper(hauteur_cm: float, pas_cm: int, recouvrement_cm: float) -> list[Bande]:
    """Bandes numérotées du bas vers le haut : on tisse et on trace de bas en haut
    (Galice, p. 67). Chaque bande déborde vers le bas sur la partie déjà tissée."""
    n = math.ceil(hauteur_cm / pas_cm)
    bandes = []
    for i in range(n):
        base = i * pas_cm
        bandes.append(Bande(
            numero=i + 1,
            y_bas_cm=max(0.0, base - (recouvrement_cm if i else 0.0)),
            y_haut_cm=min(hauteur_cm, base + pas_cm),
            cordeau_cm=base,
        ))
    return bandes


# --------------------------------------------------------------------------- #
# 5. PDF 1:1
# --------------------------------------------------------------------------- #

MARGE_MM = 10.0

def ecrire_pdf(chemin: Path, zones: list[Zone], bandes: list[Bande],
               largeur_cm: float, niveau: Niveau, nom_modele: str) -> dict:
    page_l, page_h = A4
    utile_l = page_l - 2 * MARGE_MM * mm
    utile_h = page_h - 2 * MARGE_MM * mm - 12 * mm      # 12 mm de cartouche

    c = rl_canvas.Canvas(str(chemin), pagesize=A4)
    c.setTitle(f"Calque {nom_modele} — niveau {niveau.nom}")
    total_pages = 0
    pages_par_bande = []

    for bande in bandes:
        h_bande_mm = (bande.y_haut_cm - bande.y_bas_cm) * 10
        l_bande_mm = largeur_cm * 10
        n_col = math.ceil(l_bande_mm * mm / utile_l)
        n_lig = math.ceil(h_bande_mm * mm / utile_h)
        pages_par_bande.append(n_col * n_lig)

        for lig in range(n_lig):
            for col in range(n_col):
                total_pages += 1
                ox = MARGE_MM * mm - col * utile_l
                # le PDF a son origine en bas à gauche, comme le tissage
                oy = MARGE_MM * mm + 12 * mm - lig * utile_h

                c.saveState()
                # on détoure à la zone utile : ce qui déborde appartient à la page voisine
                decoupe = c.beginPath()
                decoupe.rect(MARGE_MM * mm, MARGE_MM * mm + 12 * mm, utile_l, utile_h)
                c.clipPath(decoupe, stroke=0, fill=0)
                c.translate(ox, oy)

                bas_mm, haut_mm = 0.0, h_bande_mm * mm
                larg_mm = largeur_cm * 10 * mm

                # --- zone de recouvrement : elle déborde sur la partie déjà tissée ---
                y_cord = (bande.cordeau_cm - bande.y_bas_cm) * 10 * mm
                if y_cord > 0:
                    c.saveState()
                    c.setStrokeColorRGB(0.87, 0.83, 0.77)
                    c.setLineWidth(0.3)
                    pas = 4 * mm
                    x = -y_cord
                    while x < larg_mm:
                        c.line(max(x, 0), max(-x, 0) if x < 0 else 0,
                               min(x + y_cord, larg_mm),
                               min(y_cord, larg_mm - x) if x + y_cord > larg_mm else y_cord)
                        x += pas
                    c.restoreState()

                # --- le tracé ---
                c.setLineWidth(0.35)
                c.setStrokeColorRGB(0.08, 0.08, 0.08)
                for z in zones:
                    for anneau in [z.contour_cm] + z.trous_cm:
                        ys = [y for _, y in anneau]
                        if max(ys) < bande.y_bas_cm or min(ys) > bande.y_haut_cm:
                            continue        # l'anneau est entièrement hors de la bande
                        p = c.beginPath()
                        x0, y0 = anneau[0]
                        p.moveTo(x0 * 10 * mm, (y0 - bande.y_bas_cm) * 10 * mm)
                        for x, y in anneau[1:]:
                            p.lineTo(x * 10 * mm, (y - bande.y_bas_cm) * 10 * mm)
                        p.close()
                        c.drawPath(p, stroke=1, fill=0)

                # --- la ligne de cordeau, repère maître du remontage ---
                c.setStrokeColorRGB(0.70, 0.33, 0.18)
                c.setLineWidth(0.8)
                c.setDash(6, 3)
                c.line(0, y_cord, larg_mm, y_cord)
                c.setDash()

                # --- bord de l'ouvrage, pour poser la lisière ---
                c.setStrokeColorRGB(0.55, 0.55, 0.55)
                c.setLineWidth(0.4)
                c.setDash(1, 2)
                c.line(0, bas_mm, 0, haut_mm)
                c.line(larg_mm, bas_mm, larg_mm, haut_mm)
                c.setDash()

                c.restoreState()

                # --- repères de coupe et cartouche ---
                c.setStrokeColorRGB(0.4, 0.4, 0.4)
                c.setLineWidth(0.25)
                for cx, cy in [(MARGE_MM * mm, MARGE_MM * mm + 12 * mm),
                               (page_l - MARGE_MM * mm, MARGE_MM * mm + 12 * mm),
                               (MARGE_MM * mm, page_h - MARGE_MM * mm),
                               (page_l - MARGE_MM * mm, page_h - MARGE_MM * mm)]:
                    c.line(cx - 3 * mm, cy, cx + 3 * mm, cy)
                    c.line(cx, cy - 3 * mm, cx, cy + 3 * mm)

                c.setFont("Helvetica", 7)
                c.setFillColorRGB(0.3, 0.3, 0.3)
                c.drawString(MARGE_MM * mm, 6 * mm,
                             f"{nom_modele} · niveau {niveau.nom} · bande "
                             f"{bande.numero}/{len(bandes)} "
                             f"({bande.y_bas_cm:.0f}–{bande.y_haut_cm:.0f} cm) · "
                             f"page {lig * n_col + col + 1}/{n_col * n_lig} · MIROIR")

                # --- témoin d'échelle : si ce segment ne fait pas 100 mm, l'impression ment ---
                c.setStrokeColorRGB(0.1, 0.1, 0.1)
                c.setLineWidth(0.5)
                bx = page_l - MARGE_MM * mm - 100 * mm
                c.line(bx, 6.5 * mm, bx + 100 * mm, 6.5 * mm)
                for t in range(11):
                    c.line(bx + t * 10 * mm, 6.5 * mm, bx + t * 10 * mm,
                           (6.5 + (2 if t % 5 == 0 else 1)) * mm)
                c.setFont("Helvetica", 6)
                c.drawRightString(page_l - MARGE_MM * mm, 3 * mm, "témoin 100 mm")

                c.showPage()

    c.save()
    return {"pages_total": total_pages, "pages_par_bande": pages_par_bande}


# --------------------------------------------------------------------------- #
# 6. Mesures
# --------------------------------------------------------------------------- #

def mesurer(zones: list[Zone], labels: np.ndarray, centres: np.ndarray,
            niveau: Niveau, bandes: list[Bande], info_pdf: dict,
            largeur_cm: float, hauteur_cm: float) -> dict:
    aires = sorted(z.aire_cm2 for z in zones)
    perim = sum(z.perimetre_cm for z in zones)
    total_px = labels.size
    surface_par_ton = []
    for t in range(len(centres)):
        part = float((labels == t).sum()) / total_px
        b, g, r = centres[t]
        surface_par_ton.append({
            "ton": t,
            "rvb": f"#{r:02X}{g:02X}{b:02X}",
            "surface_cm2": round(part * largeur_cm * hauteur_cm, 1),
            "part_pct": round(part * 100, 1),
        })
    surface_par_ton.sort(key=lambda d: -d["surface_cm2"])

    def pct(p):
        return round(aires[int(p * (len(aires) - 1))], 2) if aires else 0.0

    return {
        "niveau": niveau.nom,
        "tons": niveau.tons,
        "aire_min_cm2": niveau.aire_min_cm2,
        "tolerance_mm": niveau.tolerance_mm,
        "zones_fermees": len(zones),
        "sommets_total": sum(z.sommets for z in zones),
        "longueur_tracee_cm": round(perim, 1),
        "traits_distincts_estimes_cm": round(perim / 2, 1),
        "aire_zone_cm2": {
            "min": round(aires[0], 2) if aires else 0.0,
            "q1": pct(0.25), "mediane": pct(0.5), "q3": pct(0.75),
            "max": round(aires[-1], 2) if aires else 0.0,
        },
        "zones_sous_1cm2": sum(1 for a in aires if a < 1.0),
        "pas_cm": niveau.pas_cm,
        "bandes": len(bandes),
        "recouvrement_cm": RECOUVREMENT_CM,
        "cordeaux_cm": [b.cordeau_cm for b in bandes],
        "pages_a4": info_pdf["pages_total"],
        "pages_par_bande": info_pdf["pages_par_bande"],
        "surface_par_ton": surface_par_ton,
    }


def apercu(chemin: Path, zones: list[Zone], largeur_cm: float, hauteur_cm: float):
    """PNG du calque tel qu'il sera imprimé — à l'envers."""
    L = int(largeur_cm * PX_PAR_CM)
    H = int(hauteur_cm * PX_PAR_CM)
    img = np.full((H, L, 3), 255, np.uint8)
    for z in zones:
        for anneau in [z.contour_cm] + z.trous_cm:
            pts = np.array([[int(x * PX_PAR_CM), int(H - y * PX_PAR_CM)]
                            for x, y in anneau], np.int32)
            cv2.polylines(img, [pts], True, (20, 20, 20), 1, cv2.LINE_AA)
    cv2.imwrite(str(chemin), img)


# --------------------------------------------------------------------------- #

def main():
    # la console Windows est en cp1252 : sans ça, les accents sortent en charabia
    try:
        import sys
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser(description="Bobinou — prototype de calque")
    ap.add_argument("modele", type=Path)
    ap.add_argument("--largeur", type=float, required=True, help="largeur de l'ouvrage en cm")
    ap.add_argument("--hauteur", type=float, required=True, help="hauteur de l'ouvrage en cm")
    ap.add_argument("--coins", type=str, default=None,
                    help='"x1,y1 x2,y2 x3,y3 x4,y4" en pixels de la photo')
    ap.add_argument("--sorties", type=Path, default=Path(__file__).parent / "sorties")
    args = ap.parse_args()

    img = cv2.imread(str(args.modele))
    if img is None:
        raise SystemExit(f"Image illisible : {args.modele}")
    args.sorties.mkdir(parents=True, exist_ok=True)
    nom = args.modele.stem

    if args.coins:
        coins = np.array([[float(v) for v in p.split(",")]
                          for p in args.coins.split()], dtype=np.float32)
        origine = "fournis"
    else:
        coins = detecter_coins(img)
        origine = "détectés"
        if coins is None:
            raise SystemExit("Aucun quadrilatère trouvé. Passe --coins.")

    rect = redresser(img, coins, args.largeur, args.hauteur)
    cv2.imwrite(str(args.sorties / f"{nom}_redresse.png"), rect)
    agrandissement = facteur_agrandissement(coins, args.largeur, args.hauteur)

    print(f"\n{nom} — {args.largeur:g} × {args.hauteur:g} cm "
          f"({args.largeur * args.hauteur / 1e4:.2f} m²)")
    print(f"coins {origine} · photo {img.shape[1]}×{img.shape[0]} px")
    print(f"facteur d'agrandissement ≈ ×{agrandissement:.1f} "
          f"(au-delà de ×6, le moucheté devient tache — Galice p. 177)\n")

    resultats = {
        "modele": nom,
        "largeur_cm": args.largeur,
        "hauteur_cm": args.hauteur,
        "surface_m2": round(args.largeur * args.hauteur / 1e4, 3),
        "coins": origine,
        "facteur_agrandissement": round(agrandissement, 1),
        "niveaux": [],
    }

    entete = (f"{'niveau':<7}{'tons':>5}{'zones':>7}{'<1cm²':>7}"
              f"{'tracé cm':>10}{'médiane':>9}{'pas':>5}{'bandes':>8}{'pages':>7}")
    print(entete)
    print("-" * len(entete))

    for niveau in NIVEAUX:
        labels, centres = quantifier(rect, niveau.tons)
        labels = nettoyer(labels, niveau.aire_min_cm2 * PX_PAR_CM ** 2)
        zones = vectoriser(labels, niveau)

        # le repère du tissage : y = 0 en bas, comme le PDF
        zones = [Zone(z.ton, z.aire_cm2, z.perimetre_cm, z.sommets,
                      [(x, args.hauteur - y) for x, y in z.contour_cm],
                      [[(x, args.hauteur - y) for x, y in t] for t in z.trous_cm])
                 for z in zones]
        zones = miroir(zones, args.largeur)

        bandes = decouper(args.hauteur, niveau.pas_cm, RECOUVREMENT_CM)
        pdf = args.sorties / f"{nom}_calque_{niveau.nom}.pdf"
        info = ecrire_pdf(pdf, zones, bandes, args.largeur, niveau, nom)
        apercu(args.sorties / f"{nom}_calque_{niveau.nom}.png",
               zones, args.largeur, args.hauteur)

        m = mesurer(zones, labels, centres, niveau, bandes, info,
                    args.largeur, args.hauteur)
        resultats["niveaux"].append(m)
        print(f"{niveau.nom:<7}{niveau.tons:>5}{m['zones_fermees']:>7}"
              f"{m['zones_sous_1cm2']:>7}{m['longueur_tracee_cm']:>10.0f}"
              f"{m['aire_zone_cm2']['mediane']:>9.2f}{niveau.pas_cm:>5}"
              f"{m['bandes']:>8}{m['pages_a4']:>7}")

    def brut(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return round(float(o), 3)
        raise TypeError(type(o))

    chemin_json = args.sorties / f"{nom}_mesures.json"
    chemin_json.write_text(
        json.dumps(resultats, indent=2, ensure_ascii=False, default=brut),
        encoding="utf-8")
    print(f"\nMesures : {chemin_json}")
    print(f"PDF et aperçus : {args.sorties}\n")


if __name__ == "__main__":
    main()

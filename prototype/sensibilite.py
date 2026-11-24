#!/usr/bin/env python
"""
Bobinou — analyse de sensibilité du chiffrage matière.

Deux questions, pas une :

  1. Sur le poids annoncé, qu'est-ce qui pèse ? → dans quel ordre interroger Ju.
  2. La marge de perte couvre-t-elle l'erreur ? → c'est la question de l'étudiant,
     qui ne veut pas racheter de la laine d'un bain différent en cours d'ouvrage
     (Galice, p. 61 : « prévoir toujours davantage plutôt que de courir le risque
     d'en manquer »).

La seconde est la bonne. Un chiffrage qui se trompe de 20 % par excès coûte un peu
de laine ; de 20 % par défaut, il coûte un bain de teinture et une rupture de ton au
milieu de la pièce.

Le calcul, chaîne comptée à part :

    trame  = surface_m2 × consommation_kg_m2 × (1 + marge)
    chaîne = fils_par_cm × largeur_cm × longueur_m / métrage_au_kilo

Les plages viennent de Galice 1985, vérifiées page par page (../docs/reponses-metier.md) :
consommation 1 à 2 kg/m² (p. 61), contextures p. 22, marge non publiée.

Point de méthode : la contexture n'est pas un curseur libre. Dans la table, le
métrage au kilo et le nombre de fils au centimètre montent ensemble — une chaîne plus
fine, c'est plus de fils mais un fil plus léger. On tire donc un RANG de la table, pas
deux valeurs indépendantes, sans quoi on fabrique des contextures qui n'existent pas.

Usage :
    python sensibilite.py --largeur 60 --hauteur 100
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

RNG = np.random.default_rng(20261124)
N = 200_000

# (métrage au kilo, fils/pienne min, max, étiquette) — Galice p. 22, chaîne laine.
# La pienne fait 10 cm : fils/pienne ÷ 10 = fils/cm.
CONTEXTURES = [
    (750,   20, 24, "750 · 6 brins"),
    (750,   26, 28, "750 · 4-5 brins + coton 20/36"),
    (750,   28, 30, "750 · 1 brin de Smyrne"),
    (750,   30, 34, "750 · 4-5 brins + coton 20/27"),
    (1250,  36, 40, "1250 · 3-4 brins"),
    (1250,  40, 44, "1250 · 2-3 brins"),
    (1650,  50, 62, "1650 · 1 brin"),
]

CONSO_MIN, CONSO_MAX = 1.0, 2.0
MONTAGE_MIN, MONTAGE_MAX = 0.30, 0.60
COTE_INCERT = 0.08          # cotes déduites d'une photo
COTE_RELEVEE = 0.01         # cotes prises au mètre
ESSAI_INCERT = 0.05         # essai de 10 × 10 pesé, puis extrapolé


def chaine_kg(fils_par_cm, largeur_cm, hauteur_cm, metrage, montage_m):
    longueur_m = hauteur_cm / 100.0 + montage_m
    return fils_par_cm * largeur_cm * longueur_m / metrage


def tirer_contexture(n):
    rangs = RNG.integers(0, len(CONTEXTURES), n)
    metrage = np.array([CONTEXTURES[r][0] for r in rangs], float)
    fmin = np.array([CONTEXTURES[r][1] for r in rangs], float)
    fmax = np.array([CONTEXTURES[r][2] for r in rangs], float)
    return RNG.uniform(fmin, fmax) / 10.0, metrage


# --------------------------------------------------------------------------- #
# 1. Une variable à la fois
# --------------------------------------------------------------------------- #

def oat(largeur_cm, hauteur_cm, marge=0.15):
    base = dict(conso=1.5, largeur=largeur_cm, hauteur=hauteur_cm,
                marge=marge, montage=0.45, rang=4)

    def calc(**maj):
        p = {**base, **maj}
        metrage, fmin, fmax, _ = CONTEXTURES[p["rang"]]
        fils = (fmin + fmax) / 2 / 10
        trame = p["largeur"] * p["hauteur"] / 1e4 * p["conso"] * (1 + p["marge"])
        return trame + chaine_kg(fils, p["largeur"], p["hauteur"], metrage, p["montage"])

    nominal = calc()
    essais = [
        ("consommation", "1 – 2 kg/m²",
         [calc(conso=v) for v in (CONSO_MIN, CONSO_MAX)]),
        ("cote largeur", f"{largeur_cm * 0.92:.0f} – {largeur_cm * 1.08:.0f} cm",
         [calc(largeur=largeur_cm * f) for f in (0.92, 1.08)]),
        ("cote hauteur", f"{hauteur_cm * 0.92:.0f} – {hauteur_cm * 1.08:.0f} cm",
         [calc(hauteur=hauteur_cm * f) for f in (0.92, 1.08)]),
        ("marge de perte", "5 – 25 %",
         [calc(marge=v) for v in (0.05, 0.25)]),
        ("contexture (rang entier)", "2,2 – 5,6 fils/cm",
         [calc(rang=r) for r in range(len(CONTEXTURES))]),
        ("longueur de montage", "0,30 – 0,60 m",
         [calc(montage=v) for v in (MONTAGE_MIN, MONTAGE_MAX)]),
    ]
    lignes = []
    for titre, plage, valeurs in essais:
        lignes.append({"variable": titre, "plage": plage,
                       "poids_bas_kg": round(min(valeurs), 3),
                       "poids_haut_kg": round(max(valeurs), 3),
                       "amplitude_pct": round((max(valeurs) - min(valeurs)) / nominal * 100, 1)})
    lignes.sort(key=lambda d: -d["amplitude_pct"])
    return nominal, lignes


# --------------------------------------------------------------------------- #
# 2. Part de variance
# --------------------------------------------------------------------------- #

def variance(largeur_cm, hauteur_cm):
    largeur = largeur_cm * (1 + RNG.uniform(-COTE_INCERT, COTE_INCERT, N))
    hauteur = hauteur_cm * (1 + RNG.uniform(-COTE_INCERT, COTE_INCERT, N))
    conso = RNG.uniform(CONSO_MIN, CONSO_MAX, N)
    marge = RNG.uniform(0.05, 0.25, N)
    montage = RNG.uniform(MONTAGE_MIN, MONTAGE_MAX, N)
    fils, metrage = tirer_contexture(N)

    trame = largeur * hauteur / 1e4 * conso * (1 + marge)
    chaine = chaine_kg(fils, largeur, hauteur, metrage, montage)
    total = trame + chaine

    noms = {"consommation": conso, "cote largeur": largeur, "cote hauteur": hauteur,
            "marge de perte": marge, "contexture": fils, "longueur de montage": montage}
    X = np.column_stack(list(noms.values()))
    Xc = (X - X.mean(0)) / X.std(0)
    yc = (total - total.mean()) / total.std()
    beta, *_ = np.linalg.lstsq(Xc, yc, rcond=None)
    r2 = 1 - ((yc - Xc @ beta) ** 2).sum() / (yc ** 2).sum()
    parts = dict(zip(noms, beta ** 2 / (beta ** 2).sum()))
    p5, p50, p95 = np.percentile(total, [5, 50, 95])
    return {
        "p5_kg": round(float(p5), 3), "mediane_kg": round(float(p50), 3),
        "p95_kg": round(float(p95), 3), "fourchette": round(float(p95 / p5), 3),
        "part_chaine_pct": round(float(chaine.mean() / total.mean() * 100), 1),
        "chaine_kg_moyenne": round(float(chaine.mean()), 3),
        "chaine_min_kg": round(float(chaine.min()), 3),
        "chaine_max_kg": round(float(chaine.max()), 3),
        "r2": round(float(r2), 4),
        "part_variance_pct": {k: round(float(v) * 100, 1)
                              for k, v in sorted(parts.items(), key=lambda kv: -kv[1])},
    }


# --------------------------------------------------------------------------- #
# 3. Risque de manquer de laine
# --------------------------------------------------------------------------- #

def risque(largeur_cm, hauteur_cm, cotes_relevees: bool, essai_pese: bool,
           marges=np.arange(0.0, 0.55, 0.05)):
    """La vraie question : avec quelle marge l'étudiant est-il à l'abri ?

    On sépare ce que l'app CROIT de ce qui EST. L'app prédit à partir de cotes et
    d'une consommation supposées ; le métier consomme ce qu'il consomme. On compte
    la proportion de cas où la prédiction passe sous le besoin réel.
    """
    incert = COTE_RELEVEE if cotes_relevees else COTE_INCERT
    conso_reelle = RNG.uniform(CONSO_MIN, CONSO_MAX, N)
    largeur_reelle = largeur_cm * (1 + RNG.uniform(-incert, incert, N))
    hauteur_reelle = hauteur_cm * (1 + RNG.uniform(-incert, incert, N))

    # ce que l'app suppose
    if essai_pese:
        conso_supposee = conso_reelle * (1 + RNG.uniform(-ESSAI_INCERT, ESSAI_INCERT, N))
    else:
        conso_supposee = np.full(N, (CONSO_MIN + CONSO_MAX) / 2)   # 1,5 par défaut
    surface_supposee = largeur_cm * hauteur_cm / 1e4
    besoin_reel = largeur_reelle * hauteur_reelle / 1e4 * conso_reelle

    out = []
    for m in marges:
        predit = surface_supposee * conso_supposee * (1 + m)
        manque = predit < besoin_reel
        out.append({
            "marge_pct": round(float(m) * 100),
            "risque_manquer_pct": round(float(manque.mean()) * 100, 1),
            "exces_median_pct": round(float(np.median(predit / besoin_reel - 1)) * 100, 1),
        })
    return out


def marge_pour(lignes, seuil_pct=5.0):
    for l in lignes:
        if l["risque_manquer_pct"] <= seuil_pct:
            return l["marge_pct"]
    return None


# --------------------------------------------------------------------------- #

def main():
    try:
        import sys
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--largeur", type=float, default=60.0)
    ap.add_argument("--hauteur", type=float, default=100.0)
    ap.add_argument("--sorties", type=Path, default=Path(__file__).parent / "sorties")
    args = ap.parse_args()

    surface = args.largeur * args.hauteur / 1e4
    print(f"\nOuvrage {args.largeur:g} × {args.hauteur:g} cm — {surface:.2f} m²")
    print(f"{N:,} tirages".replace(",", " "))

    nominal, lignes = oat(args.largeur, args.hauteur)
    print(f"\nPoids nominal (consommation 1,5 · marge 15 %) : {nominal:.2f} kg\n")
    print("UNE VARIABLE À LA FOIS")
    print(f"{'variable':<26}{'plage':<22}{'poids kg':<16}{'amplitude':>10}")
    print("-" * 74)
    for l in lignes:
        print(f"{l['variable']:<26}{l['plage']:<22}"
              f"{l['poids_bas_kg']:.2f} – {l['poids_haut_kg']:<9.2f}"
              f"{l['amplitude_pct']:>9.1f} %")

    v = variance(args.largeur, args.hauteur)
    print(f"\n\nTOUT À LA FOIS — poids total")
    print(f"  P5 {v['p5_kg']:.2f} · médiane {v['mediane_kg']:.2f} · "
          f"P95 {v['p95_kg']:.2f} kg   (fourchette ×{v['fourchette']:.2f})")
    print(f"  chaîne : {v['chaine_kg_moyenne']:.2f} kg en moyenne, "
          f"{v['part_chaine_pct']:.0f} % du total "
          f"(elle ne bouge qu'entre {v['chaine_min_kg']:.2f} et {v['chaine_max_kg']:.2f} kg)")
    print(f"\n  part de variance (R² du modèle linéaire : {v['r2']:.3f})")
    for k, p in v["part_variance_pct"].items():
        print(f"    {k:<24}{p:>5.1f} %  {'█' * int(round(p / 2.5))}")

    print(f"\n\nRISQUE DE MANQUER DE LAINE")
    print("  « prévoir toujours davantage plutôt que de courir le risque d'en manquer »")
    print(f"\n{'marge':>7}", end="")
    scenarios = [
        ("cotes déduites, pas d'essai", False, False),
        ("cotes relevées, pas d'essai", True, False),
        ("cotes déduites, essai pesé", False, True),
        ("cotes relevées, essai pesé", True, True),
    ]
    resultats_risque = {}
    for titre, cr, ep in scenarios:
        resultats_risque[titre] = risque(args.largeur, args.hauteur, cr, ep)
        print(f"{titre:>30}", end="")
    print()
    for i, l in enumerate(resultats_risque[scenarios[0][0]]):
        print(f"{l['marge_pct']:>6} %", end="")
        for titre, _, _ in scenarios:
            r = resultats_risque[titre][i]["risque_manquer_pct"]
            print(f"{r:>29.1f} %", end="")
        print()

    print(f"\n  marge nécessaire pour descendre sous 5 % de risque :")
    for titre, _, _ in scenarios:
        m = marge_pour(resultats_risque[titre])
        print(f"    {titre:<30}{(str(m) + ' %') if m is not None else '> 50 %':>8}")

    resultats = {
        "largeur_cm": args.largeur, "hauteur_cm": args.hauteur,
        "surface_m2": round(surface, 3), "tirages": N,
        "poids_nominal_kg": round(nominal, 3),
        "une_variable_a_la_fois": lignes,
        "tout_a_la_fois": v,
        "risque_de_manquer": resultats_risque,
        "marge_pour_5pct": {t: marge_pour(resultats_risque[t]) for t, _, _ in scenarios},
    }
    args.sorties.mkdir(parents=True, exist_ok=True)
    chemin = args.sorties / "sensibilite.json"
    chemin.write_text(json.dumps(resultats, indent=2, ensure_ascii=False),
                      encoding="utf-8")
    print(f"\nMesures : {chemin}\n")


if __name__ == "__main__":
    main()

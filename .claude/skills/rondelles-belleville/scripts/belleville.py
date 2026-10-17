#!/usr/bin/env python3
"""Calculateur de rondelles Belleville (ressorts à disque) selon EN 16984 (ex-DIN 2092).

Unités : mm, N, MPa. Aucune dépendance hors bibliothèque standard.
Formules : manuel Schnorr « Disc Springs handy for use » (formules 1 à 25), cf. references/sources.md.
Convention de signe : contrainte > 0 = traction, < 0 = compression.

Exemples :
  python3 belleville.py rondelle --De 40 --Di 20.4 --t 2.25 --l0 3.15 --s 0.675
  python3 belleville.py rondelle --De 200 --Di 82 --t 12 --tp 11.5 --l0 16.6 --s 3.45
  python3 belleville.py empilage --De 40 --Di 20.4 --t 2.25 --l0 3.15 --serie 4 --parallele 2 \\
      --L1 22 --L2 20.5 --serie-din A
  python3 belleville.py selection --F1 3000 --L1 20 --F2 4500 --L2 18.5 --De-max 60 --guide 25
  python3 belleville.py catalogue
Ajouter --json (avant la sous-commande) pour une sortie machine.
"""
import argparse
import json
import math
import sys

E_ACIER = 206000.0
UN_MOINS_MU2 = 0.91   # Schnorr §1.5 : garder 1 − µ² = 0,91 même pour un autre matériau
RM_ACIER = 1600.0     # Schnorr §2.1 : Rm ≈ 1600 MPa pour l'acier à ressort (DIN 17221/17222)

# Rondelles EN 16983 (ex-DIN 2093) séries A/B/C, groupes 1-2 (t ≤ 6 mm) :
# (série, De, Di, t, l0, h0) relevées dans le catalogue SPIROL (cf. sources.md).
CATALOGUE = [
    ("A", 18, 9.2, 1.00, 1.40, 0.40), ("A", 20, 10.2, 1.25, 1.75, 0.50),
    ("C", 35.5, 18.3, 0.90, 2.05, 1.15), ("B", 35.5, 18.3, 1.25, 2.25, 1.00), ("A", 35.5, 18.3, 2.00, 2.80, 0.80),
    ("C", 40, 20.4, 1.00, 2.30, 1.30), ("B", 40, 20.4, 1.50, 2.65, 1.15), ("A", 40, 20.4, 2.25, 3.15, 0.90),
    ("C", 45, 22.4, 1.25, 2.85, 1.60), ("B", 45, 22.4, 1.75, 3.05, 1.30), ("A", 45, 22.4, 2.50, 3.50, 1.00),
    ("C", 50, 25.4, 1.25, 2.85, 1.60), ("B", 50, 25.4, 2.00, 3.40, 1.40), ("A", 50, 25.4, 3.00, 4.10, 1.10),
    ("C", 56, 28.5, 1.50, 3.45, 1.95), ("B", 56, 28.5, 2.00, 3.60, 1.60), ("A", 56, 28.5, 3.00, 4.30, 1.30),
    ("C", 63, 31, 1.80, 4.15, 2.35), ("B", 63, 31, 2.50, 4.25, 1.75), ("A", 63, 31, 3.50, 4.90, 1.40),
    ("C", 71, 36, 2.00, 4.60, 2.60), ("B", 71, 36, 2.50, 4.50, 2.00), ("A", 71, 36, 4.00, 5.60, 1.60),
    ("C", 80, 41, 2.25, 5.20, 2.95), ("B", 80, 41, 3.00, 5.30, 2.30), ("A", 80, 41, 5.00, 6.70, 1.70),
    ("C", 90, 46, 2.50, 5.70, 3.20), ("B", 90, 46, 3.50, 6.00, 2.50), ("A", 90, 46, 5.00, 7.00, 2.00),
    ("C", 100, 51, 2.70, 6.20, 3.50), ("B", 100, 51, 3.50, 6.30, 2.80), ("A", 100, 51, 6.00, 8.20, 2.20),
    ("C", 112, 57, 3.00, 6.90, 3.90), ("B", 112, 57, 4.00, 7.20, 3.20), ("A", 112, 57, 6.00, 8.50, 2.50),
    ("C", 125, 64, 3.50, 8.00, 4.50), ("B", 125, 64, 5.00, 8.50, 3.50),
    ("C", 140, 72, 3.80, 8.70, 4.90), ("B", 140, 72, 5.00, 9.00, 4.00),
    ("C", 160, 82, 4.30, 9.90, 5.60), ("B", 160, 82, 6.00, 10.50, 4.50),
    ("C", 180, 92, 4.80, 11.00, 6.20), ("B", 180, 92, 6.00, 11.10, 5.10),
    ("C", 200, 102, 5.50, 12.50, 7.00),
]

# Coefficients de frottement DIN 2092 (Schnorr §6.5) : (wM min, wM max, wR min, wR max)
FROTTEMENT = {"A": (0.005, 0.030, 0.03, 0.05), "B": (0.003, 0.020, 0.02, 0.04), "C": (0.002, 0.015, 0.01, 0.03)}

# Jeu de guidage recommandé par DIN 2093 (Schnorr §6.3) : (Di ou De jusqu'à, jeu)
JEU_GUIDAGE = [(16, 0.2), (20, 0.3), (26, 0.4), (31.5, 0.5), (50, 0.6), (80, 0.8), (140, 1.0), (250, 1.6)]


def groupe(t):
    """Schnorr §2.2 / DIN 2093 : groupe 1 t < 1,25 ; 2 : 1,25–6 ; 3 : > 6–14 mm."""
    return 1 if t < 1.25 else (2 if t <= 6 else 3)


def constantes(De, Di):
    """Schnorr formules 2 à 5 (EN 16984)."""
    d = De / Di
    ln = math.log(d)
    K1 = (1 / math.pi) * ((d - 1) / d) ** 2 / ((d + 1) / (d - 1) - 2 / ln)
    K2 = (6 / math.pi) * ((d - 1) / ln - 1) / ln
    K3 = (3 / math.pi) * (d - 1) / ln
    return d, K1, K2, K3


def k4(t, tp, l0):
    """Schnorr formule 6 : rondelles du groupe 3 à surfaces d'appui et épaisseur réduite t'."""
    if tp is None or tp == t:
        return 1.0
    r = tp / t
    C1 = r ** 2 / ((0.25 * l0 / t - r + 0.75) * (0.625 * l0 / t - r + 0.375))
    C2 = C1 / r ** 3 * (5 / 32 * (l0 / t - 1) ** 2 + 1)
    return math.sqrt(-C1 / 2 + math.sqrt((C1 / 2) ** 2 + C2))


class Rondelle:
    def __init__(self, De, Di, t, l0, tp=None, E=E_ACIER):
        self.De, self.Di, self.t, self.l0, self.E = De, Di, t, l0, E
        self.tp = tp if tp else t            # épaisseur de calcul (t' si groupe 3 réduit)
        self.h0 = l0 - t                      # hauteur de cône de la rondelle nominale
        self.h0c = l0 - self.tp               # hauteur de cône de calcul (h0' = l0 − t')
        self.delta, self.K1, self.K2, self.K3 = constantes(De, Di)
        self.K4 = k4(t, tp, l0)
        self.c = 4 * E / UN_MOINS_MU2

    def effort(self, s):
        """Schnorr formules 7 / 8a / 8b (t et h0 remplacés par t' et h0' si réduit)."""
        t, h, K4 = self.tp, self.h0c, self.K4
        return (self.c * t ** 4 / (self.K1 * self.De ** 2) * K4 ** 2 * (s / t)
                * (K4 ** 2 * (h / t - s / t) * (h / t - s / (2 * t)) + 1))

    def raideur(self, s):
        """Schnorr formule 14."""
        t, h, K4 = self.tp, self.h0c, self.K4
        return (self.c * t ** 3 / (self.K1 * self.De ** 2) * K4 ** 2
                * (K4 ** 2 * ((h / t) ** 2 - 3 * (h / t) * (s / t) + 1.5 * (s / t) ** 2) + 1))

    def travail(self, s):
        """Schnorr formule 16."""
        t, h, K4 = self.tp, self.h0c, self.K4
        return (self.c / 2 * t ** 5 / (self.K1 * self.De ** 2) * K4 ** 2 * (s / t) ** 2
                * (K4 ** 2 * (h / t - s / (2 * t)) ** 2 + 1))

    def contraintes(self, s):
        """Schnorr formules 9 à 13. σOM : contrôle statique sur t et h0 nominaux (Schnorr ex. 3)."""
        t, h, K4, d = self.tp, self.h0c, self.K4, self.delta
        a = -self.c * t ** 2 / (self.K1 * self.De ** 2) * K4 * (s / t)
        u = h / t - s / (2 * t)
        return dict(
            OM=-self.c * self.t ** 2 / (self.K1 * self.De ** 2) * (s / self.t) * 3 / math.pi,
            I=a * (K4 * self.K2 * u + self.K3),
            II=a * (K4 * self.K2 * u - self.K3),
            III=a / d * (K4 * (self.K2 - 2 * self.K3) * u - self.K3),
            IV=a / d * (K4 * (self.K2 - 2 * self.K3) * u + self.K3),
        )

    def fleche(self, F):
        """Inversion de F(s) par dichotomie sur [0 ; h0] (F croissante si h0/t ≤ √2)."""
        lo, hi = 0.0, self.h0c
        if F > self.effort(hi):
            return None
        for _ in range(80):
            m = (lo + hi) / 2
            if self.effort(m) < F:
                lo = m
            else:
                hi = m
        return (lo + hi) / 2


def alertes_geometrie(r, alertes):
    if not 1.75 <= r.delta <= 2.5:
        alertes.append(f"δ = De/Di = {r.delta:.2f} hors plage conseillée 1,75–2,5 (Schnorr §1.6).")
    if r.delta < 1.75:
        alertes.append("δ < 1,75 : le calcul sous-estime l'effort (bras de levier raccourcis), consulter le fabricant.")
    if r.De / r.t > 50:
        alertes.append(f"De/t = {r.De / r.t:.0f} > 50 : le calcul surestime l'effort (Schnorr §1.6).")
    if r.h0c / r.tp > math.sqrt(2):
        alertes.append("h0/t > √2 : courbe effort-flèche à zone décroissante, l'inversion F→s est ambiguë.")
    g = groupe(r.t)
    if g == 3 and r.tp == r.t:
        alertes.append("Groupe 3 (t > 6 mm) : rondelle à surfaces d'appui et épaisseur réduite t'. "
                       "Fournir --tp (valeur du tableau EN 16983 ou du fabricant), sinon le calcul est faux.")
    return g


def calc_rondelle(De, Di, t, l0, s_liste, tp=None, E=E_ACIER, Rm=RM_ACIER):
    r = Rondelle(De, Di, t, l0, tp, E)
    alertes = []
    g = alertes_geometrie(r, alertes)
    res = dict(De=De, Di=Di, t=t, t_calcul=r.tp, l0=l0, h0=r.h0, h0_calcul=r.h0c, groupe=g,
               delta=r.delta, h0_sur_t=r.h0c / r.tp, De_sur_t=De / t, K1=r.K1, K2=r.K2, K3=r.K3, K4=r.K4,
               F_a_0_75h0=r.effort(0.75 * r.h0), F_a_plat=r.effort(r.h0c))
    sOM_plat = r.contraintes(r.h0)["OM"]
    res["sigma_OM_a_plat"] = sOM_plat
    if r.tp != t:
        # Schnorr ex. 3 : contrôle de σOM pour l'épaisseur réduite, σ'OM = σOM·K4·t'/t
        res["sigma_OM_reduit_a_plat"] = sOM_plat * r.K4 * r.tp / t
        sOM_plat = res["sigma_OM_reduit_a_plat"]
    if abs(sOM_plat) > Rm:
        alertes.append(f"|σOM| à plat = {abs(sOM_plat):.0f} MPa > Rm = {Rm:.0f} MPa : tassement possible "
                       "si la rondelle est mise à plat (Schnorr §2.1).")
    points = []
    for s in s_liste:
        st = r.contraintes(s)
        points.append(dict(s=s, s_sur_h0=s / r.h0, L=l0 - s, F=r.effort(s), R=r.raideur(s),
                           W=r.travail(s), **{f"sigma_{k}": v for k, v in st.items()}))
        if s > 0.75 * r.h0 + 1e-9:
            alertes.append(f"s = {s} mm > 0,75·h0 : effort réel supérieur au calcul (Schnorr §1.7, "
                           "utiliser 75–80 % de la flèche).")
        if s > r.h0c + 1e-9:
            alertes.append(f"s = {s} mm > h0 : au-delà de la position à plat.")
    res["points"] = points
    res["alertes"] = alertes
    return r, res


def jeu_guidage(D):
    for dmax, j in JEU_GUIDAGE:
        if D <= dmax:
            return j
    return None


def calc_empilage(De, Di, t, l0, i, n, tp=None, L1=None, L2=None, F1=None, F2=None, serie_din=None,
                  E=E_ACIER, Rm=RM_ACIER, guide=None):
    """Schnorr formules 17 à 25 : i ensembles en série, n rondelles en parallèle par ensemble.
    L0 = i·(l0 + (n−1)·t'), déduit des formules 19 et 22 (formule 25 illisible dans la source)."""
    r, res = calc_rondelle(De, Di, t, l0, [], tp, E, Rm)
    alertes = res["alertes"]
    H = l0 + (n - 1) * r.tp
    L0 = i * H
    res.update(serie_i=i, parallele_n=n, L0_empilage=L0, L_a_plat=i * (H - r.h0c),
               F_empilage_a_0_75h0=n * r.effort(0.75 * r.h0))
    if L0 > 3 * De:
        alertes.append(f"L0 = {L0:.1f} mm > 3·De = {3 * De:.0f} mm : diviser l'empilage avec des rondelles "
                       "de guidage (Schnorr §6.1).")
    if n > 3:
        alertes.append("Plus de 3 rondelles en parallèle : frottement et échauffement importants (Schnorr §6.1).")
    if guide is not None:
        res["jeu_guidage_recommande"] = jeu_guidage(guide)
    pts = []
    for k, L, F in ((1, L1, F1), (2, L2, F2)):
        if L is not None:
            s = (L0 - L) / i
        elif F is not None:
            s = r.fleche(F / n)
            if s is None:
                alertes.append(f"F{k} = {F} N dépasse l'effort à plat de l'empilage.")
                continue
        else:
            continue
        if s > r.h0c + 1e-9:
            alertes.append(f"Point {k} : L = {L0 - i * s:.2f} mm < longueur à plat {i * (H - r.h0c):.2f} mm : "
                           "impossible, les rondelles sont à plat.")
            continue
        F_th = n * r.effort(s)
        p = dict(point=k, s_rondelle=s, s_sur_h0=s / r.h0, s_empilage=i * s, L=L0 - i * s, F=F_th,
                 **{f"sigma_{kk}": v for kk, v in r.contraintes(s).items()})
        if serie_din in FROTTEMENT and n >= 1:
            wMmin, wMmax, wRmin, wRmax = FROTTEMENT[serie_din]
            # Formule DIN 2092 (Schnorr formule 26) : F_R = n·F / (1 ∓ wM(n−1) ∓ wR), − en charge, + en décharge.
            F1r = r.effort(s)
            p["F_charge"] = (n * F1r / (1 - wMmin * (n - 1) - wRmin), n * F1r / (1 - wMmax * (n - 1) - wRmax))
            p["F_decharge"] = (n * F1r / (1 + wMmax * (n - 1) + wRmax), n * F1r / (1 + wMmin * (n - 1) + wRmin))
        if s > 0.75 * r.h0 + 1e-9:
            alertes.append(f"Point {k} : s/h0 = {s / r.h0:.2f} > 0,75 (Schnorr §1.7).")
        if s < 0:
            alertes.append(f"Point {k} : longueur supérieure à L0, empilage non chargé.")
        pts.append(p)
    res["points"] = pts
    if len(pts) == 2:
        p1, p2 = sorted(pts, key=lambda p: p["s_rondelle"])
        fat = {}
        for pt in ("II", "III"):
            su, so = p1[f"sigma_{pt}"], p2[f"sigma_{pt}"]
            fat[pt] = dict(sigma_u=su, sigma_o=so, sigma_h=so - su)
        decisif = max(fat, key=lambda k: fat[k]["sigma_h"])
        res["fatigue"] = dict(points=fat, point_decisif=decisif, groupe=res["groupe"],
                              note="Comparer σu/σo du point décisif au diagramme de fatigue du groupe "
                                   "(EN 16984, Schnorr fig. 18-20, Mubea) : non intégré au calculateur.")
        if p1["s_rondelle"] < 0.15 * r.h0:
            alertes.append(f"Précharge s1 = {p1['s_rondelle']:.3f} mm < 0,15·h0 = {0.15 * r.h0:.3f} mm : risque de "
                           "fissures au point I en dynamique (précharge 0,15–0,20·h0, Schnorr §2.2).")
    return res


def selection(F1, L1, F2=None, L2=None, De_max=None, guide=None, ext_guide=None, n_max=3, tol=0.10):
    """Parcourt le catalogue EN 16983 (séries A/B/C) et les montages n = 1..n_max en parallèle."""
    sols = []
    for serie, De, Di, t, l0, h0 in CATALOGUE:
        if De_max and De > De_max:
            continue
        if guide is not None:
            j = jeu_guidage(Di)
            if j is None or Di < guide + j:
                continue
        if ext_guide is not None:
            j = jeu_guidage(De)
            if j is None or De > ext_guide - j:
                continue
        r = Rondelle(De, Di, t, l0)
        for n in range(1, n_max + 1):
            s1 = r.fleche(F1 / n)
            if s1 is None or s1 > 0.75 * h0:
                continue
            H = l0 + (n - 1) * t
            if H - s1 <= 0:
                continue
            i = max(1, round(L1 / (H - s1)))
            L0 = i * H
            sA = (L0 - L1) / i
            if sA < 0 or sA > 0.75 * h0:
                continue
            FA = n * r.effort(sA)
            if abs(FA - F1) / F1 > tol:
                continue
            sol = dict(serie=serie, rondelle=f"{De}x{Di}x{t}", l0=l0, n_parallele=n, i_serie=i,
                       nb_rondelles=n * i, L0=round(L0, 2), F1=round(FA), s1_sur_h0=round(sA / h0, 2))
            ok = True
            if L2 is not None:
                sB = (L0 - L2) / i
                sol.update(F2=round(n * r.effort(sB)), s2_sur_h0=round(sB / h0, 2))
                if sB > 0.75 * h0:
                    ok = False
                if F2 and abs(n * r.effort(sB) - F2) / F2 > tol:
                    ok = False
            sol["L0_sur_3De"] = round(L0 / (3 * De), 2)
            if ok and L0 <= 3 * De:
                sols.append(sol)
    sols.sort(key=lambda s: (s["nb_rondelles"], abs(s["F1"] - F1)))
    return dict(nb_solutions=len(sols), solutions=sols[:10],
                note="Catalogue limité aux séries A/B/C EN 16983 t ≤ 6 mm relevées chez SPIROL ; tolérance "
                     f"±{tol:.0%} sur les efforts ; utilisation ≤ 0,75·h0 ; L0 ≤ 3·De.")


def _arrondir(o):
    if isinstance(o, float):
        return float(f"{o:.4g}")
    if isinstance(o, dict):
        return {k: _arrondir(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_arrondir(v) for v in o]
    return o


def afficher(res, as_json):
    res = _arrondir(res)
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    for k, v in res.items():
        if k == "alertes":
            continue
        if isinstance(v, list) and v and isinstance(v[0], dict):
            print(f"{k:>22} :")
            for x in v:
                print("    " + json.dumps(x, ensure_ascii=False))
        else:
            print(f"{k:>22} : {json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v}")
    al = res.get("alertes", [])
    print("\nALERTES :" if al else "\nAucune alerte.")
    for a in al:
        print("  - " + a)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("catalogue")

    def geo(sp):
        sp.add_argument("--De", type=float, required=True)
        sp.add_argument("--Di", type=float, required=True)
        sp.add_argument("--t", type=float, required=True, help="épaisseur nominale")
        sp.add_argument("--l0", type=float, required=True, help="hauteur libre")
        sp.add_argument("--tp", type=float, help="épaisseur réduite t' (groupe 3)")
        sp.add_argument("--E", type=float, default=E_ACIER)
        sp.add_argument("--Rm", type=float, default=RM_ACIER, help="limite pour |σOM| (défaut 1600 MPa)")

    r = sub.add_parser("rondelle")
    geo(r)
    r.add_argument("--s", type=float, nargs="*", help="flèches (mm) ; défaut 0,25/0,5/0,75/1·h0")

    e = sub.add_parser("empilage")
    geo(e)
    e.add_argument("--serie", type=int, default=1, help="i : ensembles en série")
    e.add_argument("--parallele", type=int, default=1, help="n : rondelles en parallèle par ensemble")
    for a in ("L1", "L2", "F1", "F2"):
        e.add_argument(f"--{a}", type=float)
    e.add_argument("--serie-din", choices=["A", "B", "C"], help="active le calcul du frottement DIN 2092")
    e.add_argument("--guide", type=float, help="diamètre de guidage (Di ou De) pour le jeu recommandé")

    s = sub.add_parser("selection")
    for a in ("F1", "L1"):
        s.add_argument(f"--{a}", type=float, required=True)
    s.add_argument("--F2", type=float)
    s.add_argument("--L2", type=float)
    s.add_argument("--De-max", type=float, help="diamètre extérieur disponible")
    s.add_argument("--guide", type=float, help="diamètre de la tige de guidage intérieure")
    s.add_argument("--alesage", type=float, help="diamètre d'un guidage extérieur")
    s.add_argument("--n-max", type=int, default=3)
    s.add_argument("--tol", type=float, default=0.10)

    a = p.parse_args(argv)
    if a.cmd == "catalogue":
        print(json.dumps([dict(serie=c[0], De=c[1], Di=c[2], t=c[3], l0=c[4], h0=c[5]) for c in CATALOGUE],
                         ensure_ascii=False, indent=1))
        return
    if a.cmd == "rondelle":
        s_l = a.s if a.s else [round(k * (a.l0 - a.t), 4) for k in (0.25, 0.5, 0.75, 1.0)]
        _, res = calc_rondelle(a.De, a.Di, a.t, a.l0, s_l, a.tp, a.E, a.Rm)
    elif a.cmd == "empilage":
        res = calc_empilage(a.De, a.Di, a.t, a.l0, a.serie, a.parallele, a.tp, a.L1, a.L2, a.F1, a.F2,
                            a.serie_din, a.E, a.Rm, a.guide)
    else:
        res = selection(a.F1, a.L1, a.F2, a.L2, a.De_max, a.guide, a.alesage, a.n_max, a.tol)
    afficher(res, a.json)


if __name__ == "__main__":
    sys.exit(main())

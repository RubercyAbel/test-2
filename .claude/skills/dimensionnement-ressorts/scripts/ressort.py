#!/usr/bin/env python3
"""Calculateur de ressorts hélicoïdaux (compression, traction, torsion).

Unités : mm, N, N·mm, MPa, degrés. Aucune dépendance hors bibliothèque standard.
Méthodes : EN 13906-1/2/3 et Shigley (Mechanical Engineering Design, ch. 10).
Les valeurs matière sont indicatives : vérifier avec la fiche fournisseur.

Exemples :
  python3 ressort.py materiaux
  python3 ressort.py compression --d 2 --D 16 --n 8 --L0 50 --extremites rapprochees_meulees \
      --F1 20 --F2 60 --materiau DH --appuis encastre --fatigue
  python3 ressort.py concevoir-compression --F1 20 --L1 40 --F2 60 --L2 30 \
      --De-max 20 --materiau DH
  python3 ressort.py traction --d 1.5 --D 12 --n 20 --F0 5 --F 40 --materiau DH
  python3 ressort.py torsion --d 2 --D 16 --n 6 --M 800 --l1 20 --l2 20 --materiau DH
Ajouter --json pour une sortie machine.
"""
import argparse
import json
import math
import sys

# Rm(d) = A / d**m  (MPa, d en mm) — Shigley tableau 10-4, plages de validité indicatives.
# G, E en MPa ; rho en kg/m3 ; t_max température d'emploi indicative (°C).
MATERIAUX = {
    "DH": dict(nom="Fil acier patenté tréfilé EN 10270-1 DH (~corde à piano)",
               A=2211, m=0.145, G=81500, E=206000, rho=7850, t_max=80, d_rng=(0.1, 6.5)),
    "SH": dict(nom="Fil acier patenté tréfilé EN 10270-1 SH",
               A=1783, m=0.190, G=81500, E=206000, rho=7850, t_max=80, d_rng=(0.7, 12.7)),
    "VDSiCr": dict(nom="Fil trempé à l'huile EN 10270-2 VDSiCr (soupapes)",
                   A=1974, m=0.108, G=79500, E=206000, rho=7850, t_max=250, d_rng=(1.6, 9.5)),
    "FDCrV": dict(nom="Fil trempé à l'huile EN 10270-2 FDCrV",
                  A=2005, m=0.168, G=79500, E=206000, rho=7850, t_max=220, d_rng=(0.8, 11.1)),
    "FDC": dict(nom="Fil trempé à l'huile EN 10270-2 FDC (non allié)",
                A=1855, m=0.187, G=79500, E=206000, rho=7850, t_max=150, d_rng=(0.5, 12.7)),
    "1.4310": dict(nom="Inox EN 10270-3 1.4310 (X10CrNi18-8, ~AISI 302)",
                   A=1867, m=0.146, G=70000, E=185000, rho=7900, t_max=250, d_rng=(0.3, 2.5)),
    "CuSn6": dict(nom="Bronze phosphoreux CuSn6 (amagnétique, conducteur)",
                  A=1000, m=0.0, G=42000, E=115000, rho=8800, t_max=80, d_rng=(0.1, 6.0)),
}

EXTREMITES = {
    # n_t = n + nm ; L_c (longueur à bloc) ≈ facteur × d  (EN 13906-1, valeurs max)
    "rapprochees_meulees": dict(nm=2.0, Lc=lambda nt, d: nt * d),
    "rapprochees": dict(nm=2.0, Lc=lambda nt, d: (nt + 1.5) * d),
    "libres_meulees": dict(nm=1.0, Lc=lambda nt, d: nt * d),
    "libres": dict(nm=0.0, Lc=lambda nt, d: (nt + 1.0) * d),
}

# Coefficient d'appui ν pour le flambage (EN 13906-1 fig. / Shigley α)
APPUIS = {
    "encastre": 0.5,          # deux appuis plans parallèles guidés
    "encastre_rotule": 0.7,
    "rotule": 1.0,            # deux extrémités articulées
    "encastre_libre": 2.0,    # une extrémité libre
}


def rm(mat, d):
    return mat["A"] / d ** mat["m"]


def k_bergstrasser(C):
    """Facteur de correction de contrainte EN 13906-1 : k = (w+0.5)/(w-0.75)."""
    return (C + 0.5) / (C - 0.75)


def k_wahl(C):
    return (4 * C - 1) / (4 * C - 4) + 0.615 / C


def tau_nom(F, D, d):
    return 8 * F * D / (math.pi * d ** 3)


def avertissements_C(C, alertes):
    if C < 4:
        alertes.append(f"Indice C = {C:.2f} < 4 : enroulement difficile, contraintes internes élevées.")
    elif C > 16:
        alertes.append(f"Indice C = {C:.2f} > 16 : ressort instable, s'emmêle, tolérances larges.")
    elif not 5 <= C <= 12:
        alertes.append(f"Indice C = {C:.2f} hors plage conseillée 5–12.")


def verifier_diametre(mat, d, alertes):
    lo, hi = mat["d_rng"]
    if not lo <= d <= hi:
        alertes.append(f"d = {d} mm hors plage de validité de la loi Rm(d) ({lo}–{hi} mm) : Rm à confirmer.")


def zimmerli(grenaille):
    # Shigley : Ssa, Ssm (MPa) — ressorts d < 10 mm, 10^7 cycles
    return (398.0, 534.0) if grenaille else (241.0, 379.0)


def goodman_torsion(tau_a, tau_m, Sut, grenaille):
    Ssa, Ssm = zimmerli(grenaille)
    Ssu = 0.67 * Sut
    Sse = Ssa / (1 - Ssm / Ssu)
    nf = 1.0 / (tau_a / Sse + tau_m / Ssu) if (tau_a or tau_m) else float("inf")
    return dict(Ssu=Ssu, Sse=Sse, n_fatigue=nf, ref="Goodman + Zimmerli (Shigley)")


# ---------------------------------------------------------------- compression
def calc_compression(d, D, n, L0, extremites, materiau, F1=None, F2=None,
                     appuis="encastre", fatigue=False, grenaille=False,
                     tau_adm_ratio=0.5):
    mat = MATERIAUX[materiau]
    ext = EXTREMITES[extremites]
    alertes = []
    C = D / d
    avertissements_C(C, alertes)
    verifier_diametre(mat, d, alertes)
    G, E = mat["G"], mat["E"]
    R = G * d ** 4 / (8 * D ** 3 * n)                 # raideur N/mm
    nt = n + ext["nm"]
    Lc = ext["Lc"](nt, d)
    Sa = (0.0015 * D ** 2 / d + 0.1 * d) * n           # somme mini des jeux entre spires (EN 13906-1)
    Rm = rm(mat, d)
    tau_adm = tau_adm_ratio * Rm
    kB = k_bergstrasser(C)
    Fc = R * (L0 - Lc)
    tau_c = tau_nom(Fc, D, d)
    res = dict(type="compression", materiau=mat["nom"], d=d, D=D, De=D + d, Di=D - d, C=C,
               n=n, nt=nt, L0=L0, R=R, Lc=Lc, Sa_min=Sa, Ln_min=Lc + Sa, Rm=Rm, tau_adm=tau_adm,
               k_B=kB, k_Wahl=k_wahl(C), Fc=Fc, tau_c=tau_c,
               pas=(L0 - (nt - n) * d) / n if n else None,
               masse_g=mat["rho"] * math.pi ** 2 * d ** 2 * D * nt / 4 * 1e-6)
    if L0 <= Lc:
        alertes.append("L0 ≤ Lc : géométrie impossible.")
    if tau_c > tau_adm:
        alertes.append(f"τ à bloc {tau_c:.0f} MPa > τadm {tau_adm:.0f} MPa : ressort non 'à bloc sûr' "
                       "(risque de tassement si mis à bloc). Prévoir une butée ou un pré-tassement.")
    # Fréquence propre (deux extrémités sur plateaux, spires actives)
    m_act = mat["rho"] * math.pi ** 2 * (d * 1e-3) ** 2 * (D * 1e-3) * n / 4
    res["f_propre_Hz"] = 0.5 * math.sqrt(R * 1e3 / m_act)
    # Flambage EN 13906-1
    nu = APPUIS[appuis]
    ratio = 1 - G / E
    arg = 1 - ratio / (0.5 + G / E) * (math.pi * D / (nu * L0)) ** 2
    if arg <= 0:
        res["s_flambage"] = None
        res["flambage"] = "stable (aucune flèche critique)"
    else:
        sk = L0 * 0.5 / ratio * (1 - math.sqrt(arg))
        res["s_flambage"] = sk
        res["flambage"] = f"flèche critique sk = {sk:.2f} mm (L = {L0 - sk:.2f} mm)"
    res["elancement_L0_sur_D"] = L0 / D
    for i, F in ((1, F1), (2, F2)):
        if F is None:
            continue
        s = F / R
        L = L0 - s
        tau = tau_nom(F, D, d)
        res[f"s{i}"] = s
        res[f"L{i}"] = L
        res[f"tau{i}"] = tau
        res[f"tau{i}_corr"] = kB * tau
        if L < Lc + Sa:
            alertes.append(f"L{i} = {L:.2f} mm < Ln mini {Lc + Sa:.2f} mm : jeu entre spires insuffisant.")
        if tau > tau_adm:
            alertes.append(f"τ{i} = {tau:.0f} MPa > τadm {tau_adm:.0f} MPa.")
        if res["s_flambage"] is not None and s >= res["s_flambage"]:
            alertes.append(f"F{i} : flèche {s:.2f} ≥ flèche critique {res['s_flambage']:.2f} : FLAMBAGE "
                           "(guider sur tige/alésage ou réduire L0/D).")
    if F1 is not None and F2 is not None:
        # Augmentation du diamètre extérieur à bloc (EN 13906-1)
        p = res["pas"]
        res["delta_De_bloc"] = 0.1 * (p ** 2 - 0.8 * p * d - 0.2 * d ** 2) / D
        if fatigue:
            Fa, Fm = (F2 - F1) / 2, (F2 + F1) / 2
            ta, tm = kB * tau_nom(Fa, D, d), kB * tau_nom(Fm, D, d)
            fg = goodman_torsion(ta, tm, Rm, grenaille)
            fg.update(tau_a=ta, tau_m=tm, tau_k_course=2 * ta, grenaille=grenaille)
            res["fatigue"] = fg
            if fg["n_fatigue"] < 1.2:
                alertes.append(f"Coefficient de sécurité fatigue {fg['n_fatigue']:.2f} < 1.2 (10^7 cycles).")
            if res["f_propre_Hz"]:
                res["note_frequence"] = "La fréquence d'excitation doit rester < f_propre/13 (règle usuelle)."
    res["alertes"] = alertes
    return res


def concevoir_compression(F1, L1, F2, L2, materiau, De_max=None, Di_min=None,
                          extremites="rapprochees_meulees", C_cible=None,
                          tau_adm_ratio=0.45, appuis="encastre"):
    """Recherche de solutions sur les diamètres de fil normalisés (série R20)."""
    mat = MATERIAUX[materiau]
    R = (F2 - F1) / (L1 - L2)
    if R <= 0:
        raise SystemExit("Il faut F2 > F1 et L2 < L1.")
    s1 = F1 / R
    L0 = L1 + s1
    fils = [0.5, 0.56, 0.63, 0.7, 0.8, 0.9, 1.0, 1.1, 1.25, 1.4, 1.6, 1.8, 2.0, 2.25, 2.5,
            2.8, 3.0, 3.2, 3.5, 3.8, 4.0, 4.5, 5.0, 5.5, 6.0, 6.3, 7.0, 8.0, 9.0, 10.0]
    sols = []
    for d in fils:
        Rm_d = rm(mat, d)
        tau_a = tau_adm_ratio * Rm_d
        Cs = [C_cible] if C_cible else [x / 2 for x in range(8, 25)]  # 4 .. 12
        for C in Cs:
            D = C * d
            if De_max and D + d > De_max:
                continue
            if Di_min and D - d < Di_min:
                continue
            if k_bergstrasser(C) * tau_nom(F2, D, d) > tau_a:
                continue
            n = mat["G"] * d ** 4 / (8 * D ** 3 * R)
            n = max(2.0, round(n * 2) / 2)
            r = calc_compression(d, D, n, L0, extremites, materiau, F1, F2, appuis,
                                 tau_adm_ratio=tau_adm_ratio)
            if r["L2"] < r["Ln_min"]:
                continue
            sols.append(dict(d=d, D=round(D, 2), De=round(D + d, 2), C=C, n=n, L0=round(L0, 2),
                             R=round(r["R"], 3), Lc=round(r["Lc"], 2),
                             tau2_corr=round(r["tau2_corr"]), tau_adm=round(tau_a),
                             masse_g=round(r["masse_g"], 2),
                             flambage=r["flambage"], alertes=r["alertes"]))
    # Tri : sans alerte d'abord, puis masse croissante
    sols.sort(key=lambda s: (len(s["alertes"]), s["masse_g"]))
    return dict(R_requise=R, L0=L0, nb_solutions=len(sols), solutions=sols[:8])


# ---------------------------------------------------------------- traction
def calc_traction(d, D, n, materiau, F0=None, F=None, r1=None, r2=None, L0=None):
    mat = MATERIAUX[materiau]
    alertes = []
    C = D / d
    avertissements_C(C, alertes)
    verifier_diametre(mat, d, alertes)
    G, E = mat["G"], mat["E"]
    na = n + G / E                        # Shigley : spires actives = spires du corps + G/E (crochets)
    R = G * d ** 4 / (8 * D ** 3 * na)
    Rm = rm(mat, d)
    # Plage de tension initiale réalisable (Shigley, τi en MPa)
    base = 231 / math.exp(0.105 * C)
    ecart = 6.9 * (4 - (C - 3) / 6.5)
    ti_min, ti_max = base - ecart, base + ecart
    Fi = lambda t: t * math.pi * d ** 3 / (8 * D)
    res = dict(type="traction", materiau=mat["nom"], d=d, D=D, De=D + d, C=C, n_corps=n, na=na,
               R=R, Rm=Rm, tau_i_min=ti_min, tau_i_max=ti_max,
               F0_min=Fi(ti_min), F0_max=Fi(ti_max), L_corps=(n + 1) * d,
               adm=dict(corps_torsion=0.45 * Rm, crochet_flexion=0.75 * Rm, crochet_torsion=0.40 * Rm))
    if F0 is not None:
        if not Fi(ti_min) <= F0 <= Fi(ti_max):
            alertes.append(f"F0 = {F0} N hors plage réalisable [{Fi(ti_min):.1f} ; {Fi(ti_max):.1f}] N.")
    if F is not None:
        F0v = F0 or 0.0
        s = (F - F0v) / R if F > F0v else 0.0
        res.update(s=s, tau_corps=k_bergstrasser(C) * tau_nom(F, D, d))
        if L0:
            res["L"] = L0 + s
        if res["tau_corps"] > res["adm"]["corps_torsion"]:
            alertes.append("Contrainte du corps > 0.45 Rm.")
        # Crochet standard : r1 = D/2, r2 = rayon de pliage (défaut 2d)
        r1 = r1 or D / 2
        r2 = r2 or 2 * d
        C1, C2 = 2 * r1 / d, 2 * r2 / d
        KA = (4 * C1 ** 2 - C1 - 1) / (4 * C1 * (C1 - 1))
        KB = (4 * C2 - 1) / (4 * C2 - 4)
        sA = F * (KA * 16 * D / (math.pi * d ** 3) + 4 / (math.pi * d ** 2))
        tB = KB * 8 * F * D / (math.pi * d ** 3)
        res.update(sigma_crochet_A=sA, tau_crochet_B=tB)
        if sA > res["adm"]["crochet_flexion"]:
            alertes.append(f"Flexion au crochet {sA:.0f} MPa > 0.75 Rm.")
        if tB > res["adm"]["crochet_torsion"]:
            alertes.append(f"Torsion au rayon de pliage {tB:.0f} MPa > 0.40 Rm (augmenter r2).")
    res["alertes"] = alertes
    return res


# ---------------------------------------------------------------- torsion
def calc_torsion(d, D, n, materiau, M=None, l1=0.0, l2=0.0, Dm_axe=None):
    mat = MATERIAUX[materiau]
    alertes = []
    C = D / d
    avertissements_C(C, alertes)
    verifier_diametre(mat, d, alertes)
    E = mat["E"]
    na = n + (l1 + l2) / (3 * math.pi * D)           # contribution des branches
    R_rad = E * d ** 4 / (64 * D * na)                # N·mm/rad
    R_deg = R_rad * math.pi / 180
    Rm = rm(mat, d)
    Ki = (4 * C ** 2 - C - 1) / (4 * C * (C - 1))     # côté intérieur (fermeture)
    res = dict(type="torsion", materiau=mat["nom"], d=d, D=D, Di=D - d, De=D + d, C=C, n=n, na=na,
               R_Nmm_par_rad=R_rad, R_Nmm_par_deg=R_deg, Rm=Rm, K_i=Ki, sigma_adm=0.70 * Rm,
               L_corps=(n + 1) * d)
    if M is not None:
        alpha = M / R_deg
        sigma = Ki * 32 * M / (math.pi * d ** 3)
        Di_charge = n * D / (n + alpha / 360) - d
        res.update(angle_deg=alpha, sigma=sigma, Di_sous_charge=Di_charge,
                   L_corps_charge=(n + 1 + alpha / 360) * d)
        if sigma > res["sigma_adm"]:
            alertes.append(f"σ = {sigma:.0f} MPa > 0.70 Rm ({0.7 * Rm:.0f} MPa).")
        if Dm_axe:
            jeu = Di_charge - Dm_axe
            res["jeu_axe"] = jeu
            if jeu < 0.1 * Dm_axe:
                alertes.append(f"Jeu sur l'axe sous charge {jeu:.2f} mm < 10 % du diamètre d'axe : risque de serrage.")
    alertes.append("Toujours charger un ressort de torsion dans le sens de l'enroulement (fermeture).")
    res["alertes"] = alertes
    return res


# ---------------------------------------------------------------- CLI
def afficher(res, as_json):
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        return
    for k, v in res.items():
        if k == "alertes":
            continue
        if isinstance(v, float):
            v = f"{v:.4g}"
        if isinstance(v, (list, dict)):
            v = json.dumps(v, ensure_ascii=False, default=lambda x: f"{x:.4g}")
        print(f"{k:>22} : {v}")
    al = res.get("alertes", [])
    print("\nALERTES :" if al else "\nAucune alerte.")
    for a in al:
        print("  - " + a)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("materiaux")

    c = sub.add_parser("compression")
    c.add_argument("--d", type=float, required=True, help="diamètre du fil (mm)")
    c.add_argument("--D", type=float, required=True, help="diamètre moyen (mm)")
    c.add_argument("--n", type=float, required=True, help="spires actives")
    c.add_argument("--L0", type=float, required=True, help="longueur libre (mm)")
    c.add_argument("--extremites", choices=EXTREMITES, default="rapprochees_meulees")
    c.add_argument("--materiau", choices=MATERIAUX, default="DH")
    c.add_argument("--F1", type=float)
    c.add_argument("--F2", type=float)
    c.add_argument("--appuis", choices=APPUIS, default="encastre")
    c.add_argument("--fatigue", action="store_true")
    c.add_argument("--grenaille", action="store_true", help="grenaillage de précontrainte")
    c.add_argument("--tau-adm", type=float, default=0.5, help="τadm / Rm (défaut 0.5, EN 13906-1)")

    cc = sub.add_parser("concevoir-compression")
    for a in ("F1", "L1", "F2", "L2"):
        cc.add_argument(f"--{a}", type=float, required=True)
    cc.add_argument("--De-max", type=float, help="alésage disponible moins le jeu (mm)")
    cc.add_argument("--Di-min", type=float, help="tige de guidage plus le jeu (mm)")
    cc.add_argument("--C", type=float, help="indice d'enroulement imposé")
    cc.add_argument("--materiau", choices=MATERIAUX, default="DH")
    cc.add_argument("--extremites", choices=EXTREMITES, default="rapprochees_meulees")
    cc.add_argument("--appuis", choices=APPUIS, default="encastre")
    cc.add_argument("--tau-adm", type=float, default=0.45)

    t = sub.add_parser("traction")
    t.add_argument("--d", type=float, required=True)
    t.add_argument("--D", type=float, required=True)
    t.add_argument("--n", type=float, required=True, help="spires du corps")
    t.add_argument("--materiau", choices=MATERIAUX, default="DH")
    t.add_argument("--F0", type=float, help="tension initiale (N)")
    t.add_argument("--F", type=float, help="effort de service (N)")
    t.add_argument("--L0", type=float, help="longueur libre entre crochets (mm)")
    t.add_argument("--r1", type=float, help="rayon moyen du crochet (défaut D/2)")
    t.add_argument("--r2", type=float, help="rayon de pliage du crochet (défaut 2d)")

    q = sub.add_parser("torsion")
    q.add_argument("--d", type=float, required=True)
    q.add_argument("--D", type=float, required=True)
    q.add_argument("--n", type=float, required=True, help="spires du corps")
    q.add_argument("--materiau", choices=MATERIAUX, default="DH")
    q.add_argument("--M", type=float, help="couple (N·mm)")
    q.add_argument("--l1", type=float, default=0.0, help="longueur branche 1 (mm)")
    q.add_argument("--l2", type=float, default=0.0, help="longueur branche 2 (mm)")
    q.add_argument("--axe", type=float, help="diamètre de l'axe de guidage (mm)")

    a = p.parse_args(argv)
    if a.cmd == "materiaux":
        res = {k: dict(v, d_rng=list(v["d_rng"])) for k, v in MATERIAUX.items()}
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    if a.cmd == "compression":
        res = calc_compression(a.d, a.D, a.n, a.L0, a.extremites, a.materiau, a.F1, a.F2,
                               a.appuis, a.fatigue, a.grenaille, a.tau_adm)
    elif a.cmd == "concevoir-compression":
        res = concevoir_compression(a.F1, a.L1, a.F2, a.L2, a.materiau, a.De_max, a.Di_min,
                                    a.extremites, a.C, a.tau_adm, a.appuis)
    elif a.cmd == "traction":
        res = calc_traction(a.d, a.D, a.n, a.materiau, a.F0, a.F, a.r1, a.r2, a.L0)
    else:
        res = calc_torsion(a.d, a.D, a.n, a.materiau, a.M, a.l1, a.l2, a.axe)
    afficher(res, a.json)


if __name__ == "__main__":
    sys.exit(main())

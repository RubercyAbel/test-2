#!/usr/bin/env python3
"""Calculateur de ressorts hélicoïdaux à fil rond enroulés à froid (compression, traction, torsion).

Unités : mm, N, N·mm, MPa, degrés. Aucune dépendance hors bibliothèque standard.
Méthodes : EN 13906-1/2/3 (formulaires publics Gutekunst, cf. references/sources.md) et
Shigley, Mechanical Engineering Design, ch. 10. Rm = valeur MINIMALE des tableaux EN 10270
(lecture par classe de diamètre, côté sûr). Les valeurs matière restent à confirmer avec
le certificat du fil ; l'option --Rm permet d'imposer la valeur réelle.

Exemples :
  python3 ressort.py materiaux
  python3 ressort.py compression --d 2 --D 16 --n 8 --L0 50 --F1 20 --F2 60 --fatigue
  python3 ressort.py concevoir-compression --F1 20 --L1 40 --F2 60 --L2 30 --De-max 20
  python3 ressort.py traction --d 1.5 --D 12 --n 20 --F0 10 --F 40 --L0 60
  python3 ressort.py torsion --d 2 --D 16 --n 6 --M 800 --M1 200 --l1 20 --l2 20 --axe 12
Ajouter --json (avant la sous-commande) pour une sortie machine.
"""
import argparse
import json
import math
import sys

# Rm minimale (MPa) par diamètre nominal (mm). Lecture : plus petite entrée >= d.
# EN 10270-1 SH/DH (même Rm ; S = statique, D = dynamique) — tableau Mollificio Modenese,
# recoupé avec Metalle Schmidt.
_EN10270_1 = [
    (0.30, 2660), (0.40, 2560), (0.50, 2480), (0.60, 2410), (0.70, 2360), (0.80, 2310),
    (0.90, 2250), (1.00, 2230), (1.10, 2200), (1.20, 2170), (1.25, 2150), (1.30, 2140),
    (1.40, 2110), (1.50, 2090), (1.60, 2060), (1.70, 2040), (1.80, 2020), (1.90, 2000),
    (2.00, 1980), (2.10, 1970), (2.25, 1940), (2.40, 1920), (2.50, 1900), (2.60, 1890),
    (2.80, 1860), (3.00, 1840), (3.20, 1820), (3.40, 1790), (3.60, 1770), (3.80, 1750),
    (4.00, 1740), (4.25, 1710), (4.50, 1690), (4.75, 1680), (5.00, 1660), (5.30, 1640),
    (5.60, 1620), (6.00, 1590), (6.30, 1570), (6.50, 1560), (7.00, 1540), (7.50, 1510),
    (8.00, 1490), (8.50, 1470), (9.00, 1450), (9.50, 1430), (10.0, 1410), (10.5, 1390),
    (11.0, 1380), (12.0, 1350), (12.5, 1330), (13.0, 1320), (14.0, 1290), (15.0, 1270),
    (16.0, 1240), (17.0, 1220), (18.0, 1200), (19.0, 1180), (20.0, 1160)]
# EN 10270-2 (fils trempés à l'huile) — tableau Lemetal.
_FDC = [
    (0.80, 1900), (1.00, 1860), (1.30, 1810), (1.40, 1790), (1.60, 1760), (2.00, 1730),
    (2.50, 1670), (2.70, 1640), (3.00, 1620), (3.20, 1600), (3.50, 1580), (4.00, 1550),
    (4.20, 1540), (4.50, 1520), (4.70, 1510), (5.00, 1500), (5.60, 1470), (6.00, 1460),
    (6.50, 1440), (7.00, 1430), (8.00, 1400), (8.50, 1380), (10.0, 1360), (12.0, 1320),
    (14.0, 1280), (15.0, 1270), (17.0, 1250)]
_FDSICR = [
    (1.00, 2100), (1.30, 2070), (1.40, 2060), (1.60, 2040), (2.00, 2000), (2.50, 1970),
    (2.70, 1950), (3.00, 1930), (3.20, 1910), (3.50, 1900), (4.00, 1870), (4.20, 1860),
    (4.50, 1850), (4.70, 1840), (5.00, 1830), (5.60, 1800), (6.00, 1780), (6.50, 1760),
    (7.00, 1740), (8.00, 1710), (8.50, 1700), (10.0, 1660), (12.0, 1620), (14.0, 1580),
    (15.0, 1570), (17.0, 1550)]
_VDSICR = [
    (1.30, 2080), (1.60, 2060), (2.00, 2010), (2.50, 1960), (3.50, 1910), (4.50, 1860),
    (5.60, 1810), (6.50, 1760), (8.00, 1710), (10.0, 1670)]
# EN 10270-3 1.4310 NS — extrait public iTeh de la norme (classes "a < d <= b").
_X10CRNI = [
    (0.20, 2200), (0.30, 2150), (0.40, 2100), (0.50, 2050), (0.65, 2000), (0.80, 1950),
    (1.00, 1900), (1.25, 1850), (1.50, 1800), (1.75, 1750), (2.00, 1700), (2.50, 1650),
    (3.00, 1600), (3.50, 1550), (4.25, 1500)]

# E, G (MPa), rho (kg/m3) : EN 13906-1 tab. 3 / fiches Gutekunst. t_max indicative (Gutekunst).
# shigley_tors : colonne du tableau 10-10 de Shigley (fatigue des ressorts de torsion).
MATERIAUX = {
    "DH": dict(nom="EN 10270-1 DH (patenté tréfilé, dynamique)", table=_EN10270_1, d_min=0.30,
               G=81500, E=206000, rho=7850, t_max=80, shigley_tors="A228"),
    "SH": dict(nom="EN 10270-1 SH (patenté tréfilé, statique ; même Rm que DH)", table=_EN10270_1,
               d_min=0.30, G=81500, E=206000, rho=7850, t_max=80, shigley_tors="A228"),
    "FDC": dict(nom="EN 10270-2 FDC (trempé huile, statique)", table=_FDC, d_min=0.50,
                G=79500, E=206000, rho=7850, t_max=None, shigley_tors="A230"),
    "FDSiCr": dict(nom="EN 10270-2 FDSiCr (trempé huile allié, statique)", table=_FDSICR,
                   d_min=0.50, G=79500, E=206000, rho=7850, t_max=None, shigley_tors="A230"),
    "VDSiCr": dict(nom="EN 10270-2 VDSiCr (soupape, haute fatigue)", table=_VDSICR, d_min=0.50,
                   G=79500, E=206000, rho=7850, t_max=120, shigley_tors="A230"),
    "1.4310": dict(nom="EN 10270-3 1.4310 NS (X10CrNi18-8)", table=_X10CRNI, d_min=0.0,
                   G=70000, E=185000, rho=7900, t_max=160, shigley_tors="A228"),
    "CuSn6": dict(nom="CuSn6 (EN 12166) — Rm Shigley ASTM B159, indicatif", table=None, d_min=0.1,
                  G=42000, E=115000, rho=8730, t_max=80, shigley_tors=None),
}

EXTREMITES = {
    # n_t = n + nm ; L_c max. Rapprochées : EN 13906-1 ; libres : Shigley tab. 10-1.
    "rapprochees_meulees": dict(nm=2.0, Lc=lambda nt, d: nt * d, pas=lambda L0, d, n: (L0 - d) / n),
    "rapprochees": dict(nm=2.0, Lc=lambda nt, d: (nt + 1.5) * d, pas=lambda L0, d, n: (L0 - 2.5 * d) / n),
    "libres_meulees": dict(nm=1.0, Lc=lambda nt, d: nt * d, pas=lambda L0, d, n: L0 / (n + 1)),
    "libres": dict(nm=0.0, Lc=lambda nt, d: (nt + 1.0) * d, pas=lambda L0, d, n: (L0 - d) / n),
}

# Coefficient d'appui ν pour le flambage (EN 13906-1)
APPUIS = {
    "encastre": 0.5,          # deux plateaux parallèles guidés
    "encastre_rotule": 0.7,
    "rotule": 1.0,
    "encastre_libre": 2.0,
}

# Shigley tab. 10-10 : Sr (pulsé 0 -> max) en fraction de Sut, ressorts de torsion.
SHIGLEY_TORSION_SR = {
    ("A228", 1e5): (0.53, 0.62), ("A228", 1e6): (0.50, 0.60),
    ("A230", 1e5): (0.55, 0.64), ("A230", 1e6): (0.53, 0.62),
}


def rm(materiau, d, alertes, Rm_impose=None):
    if Rm_impose:
        return Rm_impose
    mat = MATERIAUX[materiau]
    if mat["table"] is None:  # CuSn6 : Shigley tab. 10-4 (bronze phosphoreux)
        if d <= 0.6:
            v = 1000.0
        elif d <= 2.0:
            v = 913 / d ** 0.028
        else:
            v = 932 / d ** 0.064
        if d > 7.5:
            alertes.append("CuSn6 : d > 7,5 mm hors plage Shigley, Rm à fournir (--Rm).")
        return v
    if d < mat["d_min"]:
        alertes.append(f"d = {d} mm sous la plage du tableau {materiau}, Rm à fournir (--Rm).")
    for dn, v in mat["table"]:
        if d <= dn + 1e-9:
            return float(v)
    alertes.append(f"d = {d} mm au-delà du tableau {materiau} : dernière valeur utilisée (optimiste), "
                   "fournir Rm (--Rm).")
    return float(mat["table"][-1][1])


def k_bergstrasser(C):
    """EN 13906-1 : k = (w+0.5)/(w-0.75) (= K_B de Shigley)."""
    return (C + 0.5) / (C - 0.75)


def k_wahl(C):
    return (4 * C - 1) / (4 * C - 4) + 0.615 / C


def tau_nom(F, D, d):
    return 8 * F * D / (math.pi * d ** 3)


def verifier_C(C, alertes):
    if C < 4:
        alertes.append(f"Indice C = {C:.2f} < 4 : hors domaine EN 13906 (4 ≤ w ≤ 20), enroulement difficile.")
    elif C > 20:
        alertes.append(f"Indice C = {C:.2f} > 20 : hors domaine EN 13906.")
    elif not 5 <= C <= 12:
        alertes.append(f"Indice C = {C:.2f} hors plage conseillée 5–12 (Shigley : 4–12).")


def goodman_zimmerli(tau_a, tau_m, Sut, grenaille):
    """Shigley : Zimmerli (d < 10 mm, 10^7 cycles), Ssu = 0.67 Sut, Goodman le long de la droite de charge."""
    Ssa, Ssm = (398.0, 534.0) if grenaille else (241.0, 379.0)
    Ssu = 0.67 * Sut
    Sse = Ssa / (1 - Ssm / Ssu)
    nf = 1.0 / (tau_a / Sse + tau_m / Ssu) if (tau_a or tau_m) else float("inf")
    return dict(Ssu=Ssu, Sse=Sse, n_fatigue=nf, ref="Goodman + Zimmerli (Shigley §10-9)")


# ---------------------------------------------------------------- compression
def calc_compression(d, D, n, L0, extremites="rapprochees_meulees", materiau="DH", F1=None, F2=None,
                     appuis="encastre", fatigue=False, grenaille=False, tau_adm_ratio=0.5, Rm_impose=None):
    mat = MATERIAUX[materiau]
    ext = EXTREMITES[extremites]
    alertes = []
    C = D / d
    verifier_C(C, alertes)
    if n < 2:
        alertes.append("n < 2 : hors domaine EN 13906-1.")
    G, E = mat["G"], mat["E"]
    R = G * d ** 4 / (8 * D ** 3 * n)
    nt = n + ext["nm"]
    Lc = ext["Lc"](nt, d)
    # EN 13906-1 : Sa statique ; x1,5 en dynamique (formulaire Gutekunst)
    Sa = (0.0015 * D ** 2 / d + 0.1 * d) * n * (1.5 if fatigue else 1.0)
    Rm = rm(materiau, d, alertes, Rm_impose)
    tau_adm = tau_adm_ratio * Rm
    tau_c_adm = 0.56 * Rm
    kB = k_bergstrasser(C)
    Fc = R * (L0 - Lc)
    tau_c = tau_nom(Fc, D, d)
    pas = ext["pas"](L0, d, n)
    res = dict(type="compression", materiau=mat["nom"], d=d, D=D, De=D + d, Di=D - d, C=C,
               n=n, nt=nt, L0=L0, R=R, Lc=Lc, Sa_min=Sa, Ln_min=Lc + Sa, Rm_min=Rm,
               tau_adm=tau_adm, tau_c_adm=tau_c_adm, k=kB, k_Wahl=k_wahl(C), Fc=Fc, tau_c=tau_c,
               pas=pas, delta_De_bloc=0.1 * (pas ** 2 - 0.8 * pas * d - 0.2 * d ** 2) / D,
               masse_g=mat["rho"] * math.pi ** 2 * d ** 2 * D * nt / 4 * 1e-6)
    if L0 <= Lc:
        alertes.append("L0 ≤ Lc : géométrie impossible.")
    if pas > 0.7 * (D - d):
        alertes.append("Pas > 0,7·Di : pas maximal conseillé dépassé (formulaire Gutekunst).")
    res["a_bloc_sur"] = tau_c <= tau_c_adm
    if not res["a_bloc_sur"]:
        alertes.append(f"τc à bloc {tau_c:.0f} MPa > 0,56·Rm = {tau_c_adm:.0f} MPa : ressort non à bloc sûr "
                       "(tassement s'il est mis à bloc). Prévoir une butée.")
    # Fréquence propre (EN 13906-1 / Gutekunst) : fe = 3560·d/(n·D²)·√(G/ρ), ρ en kg/dm³
    res["f_propre_Hz"] = 3560 * d / (n * D ** 2) * math.sqrt(G / (mat["rho"] / 1000))
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
        res.update({f"s{i}": s, f"L{i}": L, f"tau{i}": tau, f"tau{i}_corr": kB * tau})
        if L < Lc + Sa:
            alertes.append(f"L{i} = {L:.2f} mm < Ln mini {Lc + Sa:.2f} mm : jeu entre spires insuffisant.")
        if tau > tau_adm:
            alertes.append(f"τ{i} = {tau:.0f} MPa > τadm = {tau_adm_ratio}·Rm = {tau_adm:.0f} MPa.")
        if res["s_flambage"] is not None and s >= res["s_flambage"]:
            alertes.append(f"F{i} : flèche {s:.2f} ≥ flèche critique {res['s_flambage']:.2f} : FLAMBAGE "
                           "(guider sur tige/alésage ou réduire L0/D).")
    if fatigue and F1 is not None and F2 is not None:
        Fa, Fm = (F2 - F1) / 2, (F2 + F1) / 2
        ta, tm = kB * tau_nom(Fa, D, d), kB * tau_nom(Fm, D, d)
        fg = goodman_zimmerli(ta, tm, Rm, grenaille)
        fg.update(tau_a=ta, tau_m=tm, tau_kh=2 * ta, tau_k2=kB * tau_nom(F2, D, d), grenaille=grenaille)
        res["fatigue"] = fg
        if fg["n_fatigue"] < 1.2:
            alertes.append(f"Coefficient de sécurité fatigue {fg['n_fatigue']:.2f} < 1,2 (10^7 cycles).")
        if d > 10:
            alertes.append("Données de Zimmerli valables pour d < 10 mm.")
        res["note_frequence"] = ("Shigley : f_propre ≥ 15 à 20 × la fréquence d'excitation "
                                 f"(ici f_exc ≤ {res['f_propre_Hz'] / 20:.0f} Hz).")
    res["alertes"] = alertes
    return res


def concevoir_compression(F1, L1, F2, L2, materiau="DH", De_max=None, Di_min=None,
                          extremites="rapprochees_meulees", C_cible=None, tau_adm_ratio=0.5,
                          appuis="encastre", fatigue=False):
    """Balaye les diamètres de fil courants (série R20) et C = 4..12."""
    R = (F2 - F1) / (L1 - L2)
    if R <= 0:
        raise SystemExit("Il faut F2 > F1 et L2 < L1.")
    L0 = L1 + F1 / R
    fils = [0.5, 0.56, 0.63, 0.7, 0.8, 0.9, 1.0, 1.1, 1.25, 1.4, 1.6, 1.8, 2.0, 2.25, 2.5,
            2.8, 3.0, 3.2, 3.5, 3.8, 4.0, 4.5, 5.0, 5.5, 6.0, 6.3, 7.0, 8.0, 9.0, 10.0]
    sols = []
    for d in fils:
        Cs = [C_cible] if C_cible else [x / 2 for x in range(8, 25)]
        for C in Cs:
            D = C * d
            if De_max and D + d > De_max:
                continue
            if Di_min and D - d < Di_min:
                continue
            n = MATERIAUX[materiau]["G"] * d ** 4 / (8 * D ** 3 * R)
            n = max(2.0, round(n * 2) / 2)
            r = calc_compression(d, D, n, L0, extremites, materiau, F1, F2, appuis, fatigue,
                                 tau_adm_ratio=tau_adm_ratio)
            if r["tau2"] > r["tau_adm"] or r["L2"] < r["Ln_min"]:
                continue
            sols.append(dict(d=d, D=round(D, 2), De=round(D + d, 2), C=C, n=n, L0=round(L0, 2),
                             R=round(r["R"], 3), Lc=round(r["Lc"], 2), tau2=round(r["tau2"]),
                             tau_adm=round(r["tau_adm"]), a_bloc_sur=r["a_bloc_sur"],
                             n_fatigue=round(r["fatigue"]["n_fatigue"], 2) if fatigue else None,
                             masse_g=round(r["masse_g"], 2), flambage=r["flambage"],
                             alertes=r["alertes"]))
    sols.sort(key=lambda s: (len(s["alertes"]), s["masse_g"]))
    return dict(R_requise=R, L0=L0, nb_solutions=len(sols), solutions=sols[:8])


# ---------------------------------------------------------------- traction
def calc_traction(d, D, n, materiau="DH", F0=None, F=None, r1=None, r2=None, L0=None, Rm_impose=None):
    mat = MATERIAUX[materiau]
    alertes = []
    C = D / d
    verifier_C(C, alertes)
    G, E = mat["G"], mat["E"]
    na = n + G / E                        # Shigley éq. 10-39 : spires actives = corps + G/E
    R = G * d ** 4 / (8 * D ** 3 * na)
    Rm = rm(materiau, d, alertes, Rm_impose)
    # Shigley éq. 10-41 (en MPa) : plage préférée de contrainte initiale non corrigée
    base = 231 / math.exp(0.105 * C)
    ecart = 6.9 * (4 - (C - 3) / 6.5)
    ti_min, ti_max = base - ecart, base + ecart
    Fi = lambda t: t * math.pi * d ** 3 / (8 * D)
    Di = D - d
    res = dict(type="traction", materiau=mat["nom"], d=d, D=D, De=D + d, Di=Di, C=C, n_corps=n, na=na,
               R=R, Rm_min=Rm, tau_i_min=ti_min, tau_i_max=ti_max, F0_min=Fi(ti_min), F0_max=Fi(ti_max),
               L_corps=(n + 1) * d,
               hauteur_anneau=dict(demi_allemand=(0.55 * Di, 0.80 * Di), allemand=(0.80 * Di, 1.10 * Di),
                                   anglais=1.10 * Di),
               adm=dict(corps_EN=0.45 * Rm, crochet_flexion_Shigley=0.75 * Rm,
                        crochet_torsion_Shigley=0.40 * Rm))
    if F0 is not None and not Fi(ti_min) <= F0 <= Fi(ti_max):
        alertes.append(f"F0 = {F0} N hors plage préférée [{Fi(ti_min):.1f} ; {Fi(ti_max):.1f}] N (Shigley).")
    if F is not None:
        F0v = F0 or 0.0
        s = (F - F0v) / R if F > F0v else 0.0
        tau = tau_nom(F, D, d)
        res.update(s=s, tau_corps=tau, tau_corps_corr=k_bergstrasser(C) * tau)
        if L0:
            res["L"] = L0 + s
        if tau > res["adm"]["corps_EN"]:
            alertes.append("Contrainte du corps > 0,45·Rm (EN 13906-2).")
        sn = (0.45 * Rm * math.pi * d ** 3 / (8 * D) - F0v) / R
        res["s_max_conseille"] = 0.8 * sn
        if s > 0.8 * sn:
            alertes.append(f"Flèche {s:.1f} mm > 0,8·sn = {0.8 * sn:.1f} mm (risque de relaxation, Gutekunst).")
        # Crochet usuel : r1 ≈ D/2, r2 = rayon de pliage (défaut 2d)
        r1 = r1 or D / 2
        r2 = r2 or 2 * d
        C1, C2 = 2 * r1 / d, 2 * r2 / d
        KA = (4 * C1 ** 2 - C1 - 1) / (4 * C1 * (C1 - 1))
        KB = (4 * C2 - 1) / (4 * C2 - 4)
        sA = F * (KA * 16 * D / (math.pi * d ** 3) + 4 / (math.pi * d ** 2))
        tB = KB * 8 * F * D / (math.pi * d ** 3)
        res.update(sigma_crochet_A=sA, tau_crochet_B=tB)
        if sA > res["adm"]["crochet_flexion_Shigley"]:
            alertes.append(f"Flexion au crochet {sA:.0f} MPa > 0,75·Rm.")
        if tB > res["adm"]["crochet_torsion_Shigley"]:
            alertes.append(f"Torsion au rayon de pliage {tB:.0f} MPa > 0,40·Rm (augmenter r2).")
    alertes.append("Traction en dynamique : pas de méthode générale fiable (crochets), essai d'endurance recommandé.")
    res["alertes"] = alertes
    return res


# ---------------------------------------------------------------- torsion
def calc_torsion(d, D, n, materiau="DH", M=None, M1=None, l1=0.0, l2=0.0, Dm_axe=None,
                 cycles=1e6, grenaille=False, Rm_impose=None):
    mat = MATERIAUX[materiau]
    alertes = []
    C = D / d
    verifier_C(C, alertes)
    E = mat["E"]
    na = n + (l1 + l2) / (3 * math.pi * D)           # Shigley éq. 10-48
    R_rad = E * d ** 4 / (64 * D * na)
    R_deg = R_rad * math.pi / 180                     # = E·d⁴/(3667·D·n) (EN 13906-3)
    Rm = rm(materiau, d, alertes, Rm_impose)
    q = (C + 0.07) / (C - 0.75)                       # EN 13906-3
    Ki = (4 * C ** 2 - C - 1) / (4 * C * (C - 1))     # Shigley, fibre intérieure
    res = dict(type="torsion", materiau=mat["nom"], d=d, D=D, Di=D - d, De=D + d, C=C, n=n, na=na,
               R_Nmm_par_rad=R_rad, R_Nmm_par_deg=R_deg, Rm_min=Rm, q=q, K_i=Ki,
               sigma_adm=0.70 * Rm, L_corps=(n + 1.5) * d)
    if M is not None:
        alpha = M / R_deg
        sigma = 32 * M / (math.pi * d ** 3)
        Di_charge = n * D / (n + alpha / 360) - d
        res.update(angle_deg=alpha, sigma=sigma, sigma_q=q * sigma, Di_sous_charge=Di_charge,
                   L_corps_charge=(n + 1.5 + alpha / 360) * d)
        if q * sigma > res["sigma_adm"]:
            alertes.append(f"σq = {q * sigma:.0f} MPa > 0,70·Rm ({0.7 * Rm:.0f} MPa).")
        if Dm_axe:
            jeu = Di_charge - Dm_axe
            res["jeu_axe"] = jeu
            if jeu < 0.1 * Dm_axe:
                alertes.append(f"Jeu sur l'axe sous charge {jeu:.2f} mm < 10 % du diamètre d'axe : risque de serrage.")
        if M1 is not None:
            col = mat["shigley_tors"]
            cle = (col, 1e5 if cycles <= 1e5 else 1e6)
            if col is None:
                alertes.append("Fatigue en torsion non disponible pour ce matériau (Shigley tab. 10-10).")
            else:
                Sr = SHIGLEY_TORSION_SR[cle][1 if grenaille else 0] * Rm
                Se = (Sr / 2) / (1 - ((Sr / 2) / Rm) ** 2)        # Gerber, Shigley éq. 10-58
                Ma, Mm = (M - M1) / 2, (M + M1) / 2
                sa, sm = Ki * 32 * Ma / (math.pi * d ** 3), Ki * 32 * Mm / (math.pi * d ** 3)
                if sm > 0 and sa > 0:
                    nf = 0.5 * (sa / Se) * (Rm / sm) ** 2 * (-1 + math.sqrt(1 + (2 * sm * Se / (Rm * sa)) ** 2))
                else:
                    nf = float("inf")
                res["fatigue"] = dict(Sr=Sr, Se=Se, sigma_a=sa, sigma_m=sm, n_fatigue=nf, cycles=cle[1],
                                      ref="Gerber + Shigley tab. 10-10 (sans surge, détensionné)")
                if nf < 1.2:
                    alertes.append(f"Coefficient de sécurité fatigue {nf:.2f} < 1,2 ({cle[1]:.0e} cycles).")
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
        if isinstance(v, (list, dict, tuple)):
            v = json.dumps(v, ensure_ascii=False)
        print(f"{k:>22} : {v}")
    al = res.get("alertes", [])
    print("\nALERTES :" if al else "\nAucune alerte.")
    for a in al:
        print("  - " + a)


def _arrondir(o):
    if isinstance(o, float):
        return float(f"{o:.4g}")
    if isinstance(o, dict):
        return {k: _arrondir(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_arrondir(v) for v in o]
    return o


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("materiaux")

    def commun(sp):
        sp.add_argument("--materiau", choices=MATERIAUX, default="DH")
        sp.add_argument("--Rm", type=float, help="Rm réelle du fil (certificat), remplace le tableau")

    c = sub.add_parser("compression")
    c.add_argument("--d", type=float, required=True, help="diamètre du fil (mm)")
    c.add_argument("--D", type=float, required=True, help="diamètre moyen (mm)")
    c.add_argument("--n", type=float, required=True, help="spires actives")
    c.add_argument("--L0", type=float, required=True, help="longueur libre (mm)")
    c.add_argument("--extremites", choices=EXTREMITES, default="rapprochees_meulees")
    c.add_argument("--F1", type=float)
    c.add_argument("--F2", type=float)
    c.add_argument("--appuis", choices=APPUIS, default="encastre")
    c.add_argument("--fatigue", action="store_true", help="sollicitation dynamique (> 10^4 cycles)")
    c.add_argument("--grenaille", action="store_true", help="grenaillage de précontrainte")
    c.add_argument("--tau-adm", type=float, default=0.5, help="τadm / Rm (défaut 0.5, EN 13906-1)")
    commun(c)

    cc = sub.add_parser("concevoir-compression")
    for a in ("F1", "L1", "F2", "L2"):
        cc.add_argument(f"--{a}", type=float, required=True)
    cc.add_argument("--De-max", type=float, help="alésage disponible moins le jeu (mm)")
    cc.add_argument("--Di-min", type=float, help="tige de guidage plus le jeu (mm)")
    cc.add_argument("--C", type=float, help="indice d'enroulement imposé")
    cc.add_argument("--extremites", choices=EXTREMITES, default="rapprochees_meulees")
    cc.add_argument("--appuis", choices=APPUIS, default="encastre")
    cc.add_argument("--fatigue", action="store_true")
    cc.add_argument("--tau-adm", type=float, default=0.5)
    cc.add_argument("--materiau", choices=MATERIAUX, default="DH")

    t = sub.add_parser("traction")
    t.add_argument("--d", type=float, required=True)
    t.add_argument("--D", type=float, required=True)
    t.add_argument("--n", type=float, required=True, help="spires du corps")
    t.add_argument("--F0", type=float, help="tension initiale (N)")
    t.add_argument("--F", type=float, help="effort de service (N)")
    t.add_argument("--L0", type=float, help="longueur libre entre crochets (mm)")
    t.add_argument("--r1", type=float, help="rayon moyen du crochet (défaut D/2)")
    t.add_argument("--r2", type=float, help="rayon de pliage du crochet (défaut 2d)")
    commun(t)

    q = sub.add_parser("torsion")
    q.add_argument("--d", type=float, required=True)
    q.add_argument("--D", type=float, required=True)
    q.add_argument("--n", type=float, required=True, help="spires du corps")
    q.add_argument("--M", type=float, help="couple maxi (N·mm)")
    q.add_argument("--M1", type=float, help="couple mini en cyclique (active la fatigue)")
    q.add_argument("--cycles", type=float, default=1e6, help="1e5 ou 1e6 (Shigley tab. 10-10)")
    q.add_argument("--grenaille", action="store_true")
    q.add_argument("--l1", type=float, default=0.0, help="longueur branche 1 (mm)")
    q.add_argument("--l2", type=float, default=0.0, help="longueur branche 2 (mm)")
    q.add_argument("--axe", type=float, help="diamètre de l'axe de guidage (mm)")
    commun(q)

    a = p.parse_args(argv)
    if a.cmd == "materiaux":
        res = {k: {kk: vv for kk, vv in v.items() if kk != "table"} | (
            {"Rm_min_tableau": {str(dn): r for dn, r in v["table"]}} if v["table"] else {})
            for k, v in MATERIAUX.items()}
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    if a.cmd == "compression":
        res = calc_compression(a.d, a.D, a.n, a.L0, a.extremites, a.materiau, a.F1, a.F2,
                               a.appuis, a.fatigue, a.grenaille, a.tau_adm, a.Rm)
    elif a.cmd == "concevoir-compression":
        res = concevoir_compression(a.F1, a.L1, a.F2, a.L2, a.materiau, a.De_max, a.Di_min,
                                    a.extremites, a.C, a.tau_adm, a.appuis, a.fatigue)
    elif a.cmd == "traction":
        res = calc_traction(a.d, a.D, a.n, a.materiau, a.F0, a.F, a.r1, a.r2, a.L0, a.Rm)
    else:
        res = calc_torsion(a.d, a.D, a.n, a.materiau, a.M, a.M1, a.l1, a.l2, a.axe,
                           a.cycles, a.grenaille, a.Rm)
    afficher(_arrondir(res), a.json)


if __name__ == "__main__":
    sys.exit(main())

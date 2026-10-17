# Matériaux pour ressorts

Les repères [S#] renvoient à `sources.md`. Le calculateur utilise **Rm minimale** par classe de diamètre (côté sûr).
Il faut toujours confirmer avec le certificat matière (EN 10204 3.1). L'option `--Rm` permet d'imposer la valeur réelle.

## Propriétés
| Nuance | Norme | E (MPa) | G (MPa) | ρ (kg/dm³) | T max indicative | Usage | Source |
|---|---|---|---|---|---|---|---|
| SH | EN 10270-1 | 206 000 | 81 500 | 7,85 | 80 °C | Statique (S = statique) | [S4][S5] |
| DH | EN 10270-1 | 206 000 | 81 500 | 7,85 | 80 °C | Dynamique (D = dynamique), même Rm que SH | [S4][S5] |
| FDC, FDSiCr | EN 10270-2 | 206 000 | 79 500 | 7,85 | non vérifiée | Statique, gros fils | [S6], G selon EN 13906-1 |
| VDSiCr | EN 10270-2 | 206 000 | 79 500 | 7,85 | 120 °C | Soupapes, haute fatigue | [S4][S6] |
| 1.4310 (X10CrNi18-8) | EN 10270-3 | 185 000 | 70 000 | 7,9 | 160 °C | Corrosion, légèrement magnétique | [S4][S7] |
| 1.4568 (17-7PH) | EN 10270-3 | 195 000 | 73 000 | 7,9 | 200 °C | Inox haute résistance | [S4] |
| 1.4401 | EN 10270-3 | 180 000 | 68 000 | 7,95 | 300 °C | Meilleure corrosion, Rm plus faible | [S4] |
| CuSn6 | EN 12166 | 115 000 | 42 000 | 8,73 | 80 °C | Amagnétique, conducteur, Rm ≤ 900 MPa | [S4] |
| CuBe2 | EN 12166 | 120 000 | 47 000 | 8,8 | 80 °C | Conducteur, plus résistant | [S4] |
| Inconel X-750 | – | 214 000 | 75 000 | – | 550 °C | Haute température | [S4] |
| Nimonic 90 | – | 230 000 | 82 500 | – | 500 °C | Haute température, dynamique | [S4] |

Correction de température (aciers EN 10270-1/-2) : G(T) = G(20 °C)·(3620 − T)/3600, idem pour E [S3].

## Rm minimale — extraits (MPa)
| d (mm) | SH = DH (EN 10270-1) [S5] | FDC [S6] | FDSiCr [S6] | VDSiCr [S6] | 1.4310 NS [S7] |
|---|---|---|---|---|---|
| 0,5 | 2480 | 1900 | 2100 | 2080 | 2050 |
| 1,0 | 2230 | 1860 | 2100 | 2080 | 1900 |
| 1,6 | 2060 | 1760 | 2040 | 2060 | 1750 (1,5–1,75) |
| 2,0 | 1980 | 1730 | 2000 | 2010 | 1700 |
| 3,0 | 1840 | 1620 | 1930 | 1910 | 1600 |
| 4,0 | 1740 | 1550 | 1870 | 1860 | 1500 (3,5–4,25) |
| 5,0 | 1660 | 1500 | 1830 | 1810 | – |
| 8,0 | 1490 | 1400 | 1710 | 1710 | – |
| 10 | 1410 | 1360 | 1660 | 1670 | – |

Les tableaux complets sont dans `scripts/ressort.py` (`python3 ressort.py materiaux`). Rm maxi ≈ Rm mini + 150 à 330 MPa selon la nuance.

Approximation Shigley (fils ASTM, tab. 10-4) [S8] : Sut = A/d^m (MPa, mm).
Corde à piano A228 : A = 2211, m = 0,145 (0,10–6,5 mm) ; elle donne des valeurs proches de Rm min EN DH.
Trempé à l'huile A229 : A = 1855, m = 0,187 ; inox 302 : A = 1867, m = 0,146 (0,3–2,5 mm) ;
bronze phosphoreux : 1000 (0,1–0,6 mm), 913/d^0,028 (0,6–2 mm), 932/d^0,064 (2–7,5 mm).
Le fil « hard-drawn » A227 (A = 1783, m = 0,190) est **moins résistant** que SH/DH : ne pas les confondre.

## Traitements
- Revenu de détensionnement après enroulement (systématique) [S2].
- **Grenaillage** : améliore la fatigue (Zimmerli : Ssa passe de 241 à 398 MPa [S8]). Conseillé pour tout ressort dynamique de fil > 1 mm. Impossible sur un ressort de traction à spires jointives [S2].
- Pré-tassement : le ressort est enroulé plus long puis mis à bloc, ce qui augmente la charge admissible [S2].
- Revêtements (zinc lamellaire, phosphatation, peinture). Le zingage électrolytique des fils durs expose à la fragilisation par l'hydrogène : c'est un point de vigilance général, non sourcé ici, à valider avec le traiteur de surface.

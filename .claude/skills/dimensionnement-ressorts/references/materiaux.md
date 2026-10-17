# Matériaux pour ressorts (valeurs indicatives)

Résistance à la traction approchée : **Rm(d) = A / d^m** (MPa, d en mm, Shigley tab. 10-4).
Toujours confirmer avec la norme produit ou le certificat matière : les plages EN donnent Rm min et max par diamètre.

| Code | Norme | A | m | G (MPa) | E (MPa) | T max (°C) | Usage |
|---|---|---|---|---|---|---|---|
| DH | EN 10270-1 (patenté tréfilé) | 2211 | 0,145 | 81 500 | 206 000 | 80 | Standard, statique et dynamique |
| SH | EN 10270-1 | 1783 | 0,190 | 81 500 | 206 000 | 80 | Statique, économique |
| FDC | EN 10270-2 (trempé huile) | 1855 | 0,187 | 79 500 | 206 000 | 150 | Usage général, gros fils |
| FDCrV / VDCrV | EN 10270-2 | 2005 | 0,168 | 79 500 | 206 000 | 220 | Chocs, températures modérées |
| VDSiCr | EN 10270-2 | 1974 | 0,108 | 79 500 | 206 000 | 250 | Soupapes, haute fatigue |
| 1.4310 | EN 10270-3 (inox) | 1867 | 0,146 | 70 000 | 185 000 | 250 | Corrosion (légèrement magnétique) |
| 1.4568 (17-7PH) | EN 10270-3 | – | – | 73 000 | 195 000 | 300 | Inox haute résistance |
| CuSn6 | EN 12166 | ≈ 1000 (cst) | 0 | 42 000 | 115 000 | 80 | Amagnétique, conducteur |
| Inconel X-750 | – | – | – | 76 000 | 214 000 | 550 | Très haute température |

Remarques :
- Préfixe EN 10270-2 : F = statique, T = dynamique moyen, V = soupape (fatigue sévère).
- Les ressorts en inox subissent une relaxation en température : appliquer un abattement sur τadm au-delà de 100 °C.
- Pour d > 10–17 mm, les ressorts sont enroulés à chaud (EN 10089) puis trempés et revenus ; τadm ≈ 0,5·Rm de l'acier traité.
- Traitements : revenu de détensionnement après enroulement (systématique), **grenaillage de précontrainte** (+30 à 60 % en fatigue), pré-tassement (élimine la relaxation initiale), revêtements (zinc lamellaire, phosphatation, peinture époxy). Attention à la fragilisation par l'hydrogène avec les zingages électrolytiques des fils à Rm > 1000 MPa.

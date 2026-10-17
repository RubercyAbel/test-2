# Sources vérifiées (consultées le 17/10/2026)

Les normes EN complètes sont payantes. Les formules ont été recoupées à partir d'extraits officiels,
de formulaires de fabricants qui calculent selon EN 13906, et du cours de Shigley.
Les copies non autorisées de normes (Scribd, etc.) ont été écartées.

| # | Source | Ce qui a été vérifié |
|---|---|---|
| S1 | Extrait officiel EN 13906-1:2013 — iTeh : https://cdn.standards.iteh.ai/samples/38074/dc919140f4c049d693d94831cb248018/SIST-EN-13906-1-2014.pdf | Domaine (froid : d ≤ 20 mm, n ≥ 2, 4 ≤ w ≤ 20), symboles, définition statique / quasi-statique (< 10⁴ cycles) / dynamique, durée de vie infinie (10⁷ cycles à froid) |
| S2 | Gutekunst Federn, « Design of metal springs – Part 2 » : https://blog.federnshop.com/en/design-of-metal-springs-part-2-calculation/ | R, τ, k de Bergsträsser, τzul = 0,5·Rm, τczul = 0,56·Rm, Lc, Sa, ΔDe, pas ; traction : τzul = 0,45·Rm, s2 ≤ 0,8·sn, longueurs de corps et d'anneaux ; torsion : R = E·d⁴/(3667·D·n), q = (w + 0,07)/(w − 0,75), σzul = 0,7·Rm, Di sous charge, Lk = (n + 1,5)·d |
| S3 | Gutekunst, formulaire compression : https://blog.federnshop.com/wp-content/uploads/Gutekunst_Druckfedern_Formeln_2015.pdf | Flèche critique de flambage sK, fe = 3560·d·√(G/ρ)/(n·D²), Sa × 1,5 en dynamique, Sa des ressorts enroulés à chaud, G(T) et E(T), pas maxi 0,7·Di |
| S4 | Gutekunst, propriétés des fils : https://blog.federnshop.com/en/spring-steel-wires-and-their-properties/ | E, G, ρ, températures maximales (SH/DH, VDSiCr, 1.4310, 1.4568, 1.4401, CuSn6, CuBe2, Inconel X-750, Nimonic 90) |
| S5 | Mollificio Modenese, EN 10270-1 : https://www.mollificiomodenese.it/en/insights/materials-used/music-wire-uni-en-10270-1-sh-dh/ — recoupé avec Metalle Schmidt : https://www.metalleschmidt.de/en/wire/hard-drawn-steel/ | Rm min/max SH et DH par diamètre (SH = DH en Rm), E = 206 GPa, G = 81,5 GPa |
| S6 | Lemetal, EN 10270-2 : https://lemetal.ro/oil-tempered-steel-wire-according-to-en-10270-2/ | Rm FDC, FDSiCr, TDSiCr, VDSiCr par diamètre |
| S7 | Extrait officiel EN 10270-3 — iTeh : https://cdn.standards.iteh.ai/samples/30610/fa0cca4f41ba4e95956d0de6c0b9a63f/SIST-EN-10270-3-2012.pdf | Rm 1.4310 NS/HS, 1.4401, 1.4568… jusqu'à d = 4,25 mm |
| S8 | Shigley, *Mechanical Engineering Design* ch. 10 (support de cours, 9e éd.) : https://www.philadelphia.edu.jo/academics/mgogazeh/uploads/DESIGN%202%20CH10.pdf | Tab. 10-4 (A, m), K_W, K_B, extrémités, stabilité L0 < 2,63·D/α, Zimmerli, Goodman, Ssu = 0,67·Sut, f_n ≥ 15–20 × f_exc, crochets σA/τB, τi préférée, Na = Nb + G/E, torsion Ki, Na = Nb + (l1 + l2)/(3πD), Sy = 0,78/0,87/0,61·Sut, tab. 10-10 et Gerber (fatigue en torsion), exemples chiffrés |
| S9 | Axomek, calcul EN 13906 : https://axomek.com/calculations/spring-calculation-en-13906/ | Exemple chiffré complet (DH 2,5 × 20, n = 8,5), utilisé comme test du calculateur |
| S10 | Catalogue iTeh EN 15800:2008 : https://standards.iteh.ai/catalog/standards/cen/ccd4840e-89d8-45ae-bb0d-f8c650b2fa64/en-15800-2008 | Domaine : tolérances des ressorts de **compression** enroulés à froid uniquement |

## Tests de non-régression du calculateur
| Cas | Référence | Résultat publié | `ressort.py` |
|---|---|---|---|
| Compression DH 2,5 × 20, n = 8,5, L0 = 60 | S9 | R 5,852 ; τ2 419,7 ; τc 643,8 ; Ln 32,5 (dyn.) ; fe 266,6 Hz | 5,852 ; 419,6 ; 643,8 ; 32,5 ; 266,7 |
| Fatigue compression (Goodman/Zimmerli) | S8 (exemple fatigue, fil 0,092 in) | nf = 1,23 | 1,231 |
| Fatigue torsion (Gerber, tab. 10-10) | S8 (exemple ressort de torsion catalogue) | nf = 1,13 | 1,132 |
| Crochets de traction | S8 ex. 10-6 | σA 156,9 kpsi (1082 MPa) ; τB 78,4 kpsi (541 MPa) | 1082 ; 542 |

## Points restant non vérifiés (à confirmer dans la norme achetée ou auprès du fournisseur)
- Diagrammes de Goodman EN 13906 (abaques non publics) : le calculateur utilise Zimmerli/Shigley à la place.
- Rm du CuSn6 : loi Shigley (ASTM B159) ; EN 12166 désigne CuSn6 R950.
- Températures maximales de FDC et FDSiCr ; Rm du 1.4310 au-delà de d = 4,25 mm.
- Correspondance des nuances EN ↔ ASTM pour la fatigue en torsion (DH ≈ A228, fils trempés à l'huile ≈ A230/A232).
- Traction avec embouts vissés : na = n_total − spires vissées (raisonnement mécanique ; seul l'usage en dynamique est sourcé chez Gutekunst, https://blog.federnshop.com/en/eyelet-shapes-extension-springs/).
- Compression non meulée : conseil de calculer le flambage avec ν = 0,7 (jugement d'ingénieur).
- Tolérances : DIN 2097 (traction) et DIN 2194 (torsion) sont citées par Gutekunst, mais leur statut actuel n'a pas été vérifié.

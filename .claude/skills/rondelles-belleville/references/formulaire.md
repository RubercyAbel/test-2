# Rondelles Belleville — formulaire (EN 16984, ex-DIN 2092)

Les repères [B#] renvoient à `sources.md`. Unités : mm, N, MPa.
Contraintes : > 0 = traction, < 0 = compression [B1].

## Normes
- **EN 16984** (ex-DIN 2092) : calcul. **EN 16983** (ex-DIN 2093) : qualité et dimensions, séries A/B/C, groupes 1/2/3. Remplacement au 01/02/2017 [B5][B2].
- Groupes d'épaisseur [B1] : **1** t < 1,25 mm ; **2** 1,25 ≤ t ≤ 6 mm ; **3** 6 < t ≤ 14 mm.
  Le groupe 3 a des surfaces d'appui et une épaisseur réduite t'.

## Notations
De, Di diamètres ; t épaisseur (t' réduite) ; l0 hauteur libre ; h0 = l0 − t hauteur de cône (h0' = l0 − t') ;
s flèche ; δ = De/Di ; E = 206 000 MPa et µ = 0,3 pour l'acier, soit 4E/(1 − µ²) = 905 495 MPa [B1].

## Constantes [B1 formules 2–6]
- K1 = (1/π)·((δ − 1)/δ)² / ((δ + 1)/(δ − 1) − 2/ln δ)
- K2 = (6/π)·((δ − 1)/ln δ − 1)/ln δ
- K3 = (3/π)·(δ − 1)/ln δ
- K4 = 1 pour les groupes 1 et 2. Pour le groupe 3 :
  C1 = (t'/t)² / [(¼·l0/t − t'/t + ¾)·(⅝·l0/t − t'/t + ⅜)] ;
  C2 = C1/(t'/t)³ · [5/32·(l0/t − 1)² + 1] ;
  K4 = √(−C1/2 + √((C1/2)² + C2)).
  Validé : 200 × 82 × 12, t' = 11,5 donne K4 = 1,05374, valeur publiée [B1 ex. 3].

## Rondelle seule
- **Effort** [B1 f. 7/8a/8b] :
  F = 4E/(1 − µ²) · t⁴/(K1·De²) · K4² · (s/t) · [K4²·(h0/t − s/t)·(h0/t − s/(2t)) + 1].
  Pour le groupe 3, remplacer t par t' et h0 par h0'.
- **Raideur** [f. 14] : R = 4E/(1 − µ²) · t³/(K1·De²) · K4² · [K4²·((h0/t)² − 3·(h0/t)·(s/t) + 1,5·(s/t)²) + 1].
- **Travail** [f. 16] : W = 2E/(1 − µ²) · t⁵/(K1·De²) · K4² · (s/t)² · [K4²·(h0/t − s/(2t))² + 1].
- **Contraintes** [f. 9–13], avec a = −4E/(1 − µ²) · t²/(K1·De²) · K4 · s/t et u = h0/t − s/(2t) :
  - σOM = −4E/(1 − µ²) · t²/(K1·De²) · s/t · 3/π (point au diamètre D0 = (De − Di)/ln δ) ;
  - σI = a·[K4·K2·u + K3] ; σII = a·[K4·K2·u − K3] ;
  - σIII = (a/δ)·[K4·(K2 − 2K3)·u − K3] ; σIV = (a/δ)·[K4·(K2 − 2K3)·u + K3].
- **Forme de la courbe** : elle dépend uniquement de h0/t ; l'effort est toujours dégressif [B1]. Pour h0/t > √2, la courbe présente une zone décroissante [B1 §1.7].

## Domaine de validité [B1 §1.6, B3]
- Conseillé : δ = 1,75 à 2,5.
- De/t > 50 (B3 : De/t ≫ 40) : effort calculé **trop élevé**.
- δ < 1,75 (B3 : < 1,8) : effort calculé **trop faible**, consulter le fabricant.
- Matériau autre que l'acier : prendre son E, mais garder 1 − µ² = 0,91 [B1 §1.5].
- Au-delà de s ≈ 0,75·h0, l'effort réel dépasse le calcul. N'utiliser que **75 à 80 % de h0** ; c'est pourquoi DIN 2093 donne l'effort à 0,75·h0 [B1 §1.7].

## Résistance
- **Statique** (< 10⁴ cycles) : |σOM| ≤ Rm, avec Rm ≈ 1600 MPa pour l'acier à ressort. Contrôle à plat (s = h0) [B1 §2.1].
  Groupe 3 : contrôler aussi σ'OM = σOM·K4·t'/t [B1 ex. 3].
  Certaines rondelles normalisées dépassent légèrement cette limite (dimensionnées autrefois sur σI) : léger tassement possible [B1].
- **Dynamique** [B1 §2.2] :
  - durée de vie longue ≥ 2·10⁶ cycles ; durée limitée entre 10⁴ et 2·10⁶ cycles ;
  - les fissures partent de la face inférieure. Calculer σII **et** σIII entre s1 et s2, et retenir le point le plus sollicité ;
  - comparer σu et σo au diagramme de fatigue du groupe (EN 16984, Schnorr fig. 18–20, Mubea). **Ces diagrammes ne sont pas intégrés** ;
  - précharger à **s1 ≥ 0,15 à 0,20·h0**, sinon des fissures apparaissent au point I ;
  - les diagrammes valent pour ≤ 10 rondelles en série, un guidage trempé et une charge sinusoïdale. Au-delà, prévoir une marge et consulter le fabricant.

## Empilages [B1 f. 17–25]
| Montage | Effort | Flèche | Longueur libre |
|---|---|---|---|
| i rondelles en série (opposées) | F | i·s | i·l0 |
| n rondelles en parallèle (emboîtées) | n·F | s | l0 + (n − 1)·t |
| i ensembles de n en parallèle | n·F | i·s | i·(l0 + (n − 1)·t)  (*) |

(*) Combinaison des deux lignes précédentes ; la formule 25 est illisible dans la source. Utiliser t' pour le groupe 3.

- Longueur d'empilage **L0 ≤ 3·De**. Au-delà, diviser l'empilage par des rondelles de guidage [B1 §6.1].
- **≤ 2 à 3 rondelles en parallèle**, sauf si l'on cherche de l'amortissement [B1 §6.1].
- **Frottement** (DIN 2092, n rondelles en parallèle) : F_R = n·F/(1 ∓ wM·(n − 1) ∓ wR), signe − en charge et + en décharge [B1 §6.5].

  | Série | wM | wR |
  |---|---|---|
  | A | 0,005 à 0,030 | 0,03 à 0,05 |
  | B | 0,003 à 0,020 | 0,02 à 0,04 |
  | C | 0,002 à 0,015 | 0,01 à 0,03 |

## Guidage [B1 §6.3–6.4, d'après DIN 2093]
- Guidage intérieur (tige) préféré au guidage extérieur. Surface du guide plus dure que la rondelle : ≥ 55 HRC conseillé en dynamique.
- Jeu recommandé selon Di ou De :

| Diamètre | Jeu |
|---|---|
| ≤ 16 mm | 0,2 mm |
| ≤ 20 mm | 0,3 mm |
| ≤ 26 mm | 0,4 mm |
| ≤ 31,5 mm | 0,5 mm |
| ≤ 50 mm | 0,6 mm |
| ≤ 80 mm | 0,8 mm |
| ≤ 140 mm | 1,0 mm |
| ≤ 250 mm | 1,6 mm |

# Ressort hélicoïdal de traction — formulaire (EN 13906-2 / Shigley)

Les repères [S#] renvoient à `sources.md`.

## Raideur et effort
- **R = G·d⁴ / (8·D³·n) = (F − F0)/s** ; **F = F0 + R·s** [S2].
- Shigley compte les crochets dans les spires actives : na = n_corps + G/E [S8]. EN et Gutekunst utilisent n [S2]. L'écart est d'environ 0,4 spire.
- Longueur du corps : LK = (nt + 1)·d ; L0 = LK + 2·LH [S2].
- Hauteur d'anneau LH [S2] : demi-anneau allemand 0,55–0,80·Di ; anneau allemand entier 0,80–1,10·Di ; crochet > 1,10·Di ; anneau anglais 1,10·Di.

## Tension initiale réalisable [S8]
Plage préférée de contrainte initiale non corrigée (Shigley éq. 10-41, convertie en MPa) :
**τi = 231/e^(0,105·C) ± 6,9·(4 − (C − 3)/6,5)**, puis F0 = τi·π·d³/(8·D).
F0 dépend de l'indice et ne peut pas être augmentée à volonté [S2]. Il vaut mieux spécifier deux points (F1, L1) et (F2, L2) que F0.

## Contraintes
- Corps : τ = 8·F·D/(π·d³) ≤ **τzul = 0,45·Rm** [S2]. Shigley compare K_B·τ à 0,45·Sut [S8].
- Pour limiter la relaxation, n'utiliser que **80 %** de la flèche admissible : s2 ≤ 0,8·sn [S2].
- **Crochets** (Shigley, statique [S8]) :
  - Flexion au point A (rayon r1, C1 = 2·r1/d) :
    σA = F·[KA·16·D/(π·d³) + 4/(π·d²)] avec KA = (4C1² − C1 − 1)/(4C1·(C1 − 1)) ; limite **0,75·Sut**.
  - Torsion au point B (rayon de pliage r2, C2 = 2·r2/d) :
    τB = KB·8·F·D/(π·d³) avec KB = (4C2 − 1)/(4C2 − 4) ; limite **0,40·Sut**.
  - Axomek, qui calcule selon EN, retient 0,7·Rm en flexion et 0,45·Rm en torsion [S9].

## Fatigue
Il n'existe pas de valeurs d'endurance générales, à cause des surcontraintes aux pliages des anneaux.
Les ressorts de traction ne peuvent pas être grenaillés (spires jointives).
En dynamique, préférer des embouts roulés ou vissés et faire un essai d'endurance [S2].
Shigley propose une méthode (Gerber au corps et aux crochets) [S8], mais elle n'est pas implémentée dans le calculateur.

## Bonnes pratiques
- Ne flambe pas, mais la rupture interrompt complètement la transmission d'effort [S2]. Prévoir une butée.
- Pour une fonction de sécurité, un ressort de compression monté en tirant reste porteur même cassé.
- Tolérances : EN 15800 ne s'applique pas à la traction [S10] ; Gutekunst cite DIN 2097 [S2].

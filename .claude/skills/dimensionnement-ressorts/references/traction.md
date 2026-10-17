# Ressort hélicoïdal de traction — formulaire (EN 13906-2 / Shigley)

## Raideur et effort
- Spires actives : na = n_corps + G/E (contribution des crochets, Shigley). Dans la norme EN, on prend na ≈ n_corps.
- Raideur : **R = G·d⁴ / (8·D³·na)**.
- Effort : **F = F0 + R·s**, où F0 est la tension initiale (effort à vaincre avant que les spires ne s'écartent).
- Longueur du corps à vide : Lk = (n_corps + 1)·d (spires jointives).
- L0 = Lk + 2 × longueur de crochet (souvent ≈ 0,8–1,1·Di par crochet standard).

## Tension initiale réalisable
Contrainte initiale (Shigley, MPa) : τi = 231/e^(0,105·C) ± 6,9·(4 − (C − 3)/6,5).
F0 = τi·π·d³/(8·D). Au-delà de cette plage, le ressort n'est pas fabricable ; en deçà, il faut un recuit.
Tolérance usuelle sur F0 : ±10 à 15 %. Mieux vaut spécifier deux points (F1, L1) et (F2, L2) plutôt que F0.

## Contraintes
- Corps : τ = k·8·F·D/(π·d³) ≤ ≈ 0,45·Rm (statique).
- **Crochets (zones critiques)** :
  - Flexion au point A (sortie du crochet, rayon r1 ≈ D/2, C1 = 2·r1/d) :
    σA = F·[KA·16·D/(π·d³) + 4/(π·d²)] avec KA = (4C1² − C1 − 1)/(4C1·(C1 − 1)) ; limite ≈ 0,75·Rm.
  - Torsion au point B (pliage, rayon r2, C2 = 2·r2/d) :
    τB = KB·8·F·D/(π·d³) avec KB = (4C2 − 1)/(4C2 − 4) ; limite ≈ 0,40·Rm. Viser r2 ≥ 2·d.
- En fatigue, les crochets cassent avant le corps. Pour améliorer la tenue : crochets réduits avec spire de transition, embouts vissés, ou une conception en compression si c'est possible.

## Bonnes pratiques
- Prévoir une butée de fin de course : sans arrêt, une rupture libère la pièce.
- Pour la sécurité, préférer un ressort de compression monté en tirant (« drawbar ») : il reste porteur même cassé.
- Préciser l'orientation relative des crochets (0°, 90°, 180°) et leur type (anglais, allemand, crochet latéral, boucle double).

# Ressort hélicoïdal de torsion — formulaire (EN 13906-3 / Shigley)

## Raideur
- Spires actives : na = n + (l1 + l2)/(3·π·D), où l1 et l2 sont les longueurs de branches.
- Raideur angulaire : **R = E·d⁴ / (64·D·na)** en N·mm/rad, soit R° = R·π/180 en N·mm/°.
  (Shigley donne aussi d⁴·E/(10,8·D·na) en N·mm/tour, avec la friction sur l'axe incluse.)
- Couple : M = F·r = R°·α.

## Contrainte (flexion)
- σ = q·32·M/(π·d³), avec q = Ki = (4C² − C − 1)/(4C·(C − 1)) (fibre intérieure, Shigley).
  EN 13906-3 approxime q ≈ (C + 0,07)/(C − 0,75).
- Statique : σ ≤ ≈ 0,70·Rm (0,78·Rm pour la corde à piano, 0,87·Rm pour les fils trempés à l'huile, 0,61·Rm pour l'inox, selon Shigley). Retenir 0,70·Rm par défaut.
- Charger **dans le sens de l'enroulement** (fermeture du ressort) : les contraintes résiduelles d'enroulement sont alors favorables.

## Géométrie sous charge
- Le diamètre intérieur diminue : Di' = n·D/(n + α/360) − d, avec α en degrés.
  Prévoir un jeu d'environ 10 % sur l'axe sous charge maximale.
- Le corps s'allonge : Lk' = (n + 1 + α/360)·d. Prévoir la place, ou un pas initial entre les spires pour réduire la friction.
- Spécifier la position angulaire libre des branches et sa tolérance (± quelques degrés selon n).

## Fatigue
Pas de diagramme universel. Utiliser le diagramme de Goodman en flexion du fournisseur ou d'EN 13906-3, et limiter la course de contrainte.
Les plis de branche à petit rayon sont des amorces de rupture : prendre un rayon ≥ d.

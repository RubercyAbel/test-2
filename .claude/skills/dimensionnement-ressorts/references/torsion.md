# Ressort hélicoïdal de torsion — formulaire (EN 13906-3 / Shigley)

Les repères [S#] renvoient à `sources.md`.

## Raideur
- EN 13906-3 : **RM = M/α = E·d⁴/(3667·D·n)** en N·mm/° [S2]. C'est la même chose que E·d⁴/(64·D·n) en N·mm/rad.
- Shigley ajoute la flexion des branches : **na = Nb + (l1 + l2)/(3·π·D)** [S8].
  Il donne aussi k' = d⁴·E/(10,8·D·na) en N·mm/tour, qui inclut empiriquement le frottement.

## Contrainte (flexion)
- σ = 32·M/(π·d³) ; corrigée **σq = q·σ, avec q = (w + 0,07)/(w − 0,75)** (EN 13906-3) [S2].
  Shigley utilise Ki = (4C² − C − 1)/(4C·(C − 1)) (fibre intérieure) [S8], de valeur très voisine.
- Statique : **σzul = 0,7·Rm** (EN [S2]). Le calculateur compare σq, ce qui est prudent.
  Shigley donne la limite d'élasticité selon le matériau : Sy = 0,78·Sut (corde à piano, acier tréfilé), 0,87·Sut (aciers trempés à l'huile), 0,61·Sut (inox austénitique, non ferreux) [S8].
- Monter le ressort sur un mandrin et ne le charger que **dans le sens de l'enroulement** [S2].

## Géométrie sous charge [S2]
- Diamètre intérieur sous charge : **Di' = D·n/(n + α/360) − d**. Prévoir un jeu d'environ 10 % sur l'axe.
- Longueur du corps : **Lk = (n + 1,5)·d** à vide, et (n + 1,5 + α/360)·d sous charge.
- Course de l'extrémité d'une branche de bras RH : s = α·RH/57,3.
- Prévoir un pas entre les spires si le frottement est gênant. En dynamique, éviter les pliages à arête vive [S2].

## Fatigue
- EN 13906-3 : diagrammes de Goodman de la norme (non publics).
- Shigley [S8] : résistance en cycle pulsé Sr (tab. 10-10, en % de Sut, sans surge, ressort détensionné) :

| Durée de vie | A228 et inox 302, non grenaillé | A228 et inox 302, grenaillé | A230 / A232, non grenaillé | A230 / A232, grenaillé |
|---|---|---|---|---|
| 10⁵ cycles | 53 % | 62 % | 55 % | 64 % |
| 10⁶ cycles | 50 % | 60 % | 53 % | 62 % |

  Se = (Sr/2)/(1 − (Sr/(2·Sut))²) ; puis Gerber :
  nf = ½·(σa/Se)·(Sut/σm)²·[−1 + √(1 + (2·σm·Se/(Sut·σa))²)], avec σ = Ki·32·M/(π·d³).
  Le calculateur assimile DH, SH et 1.4310 à A228/302, et les fils EN 10270-2 à A230/A232 : c'est une approximation.

Tolérances : EN 15800 ne s'applique pas à la torsion [S10] ; Gutekunst cite DIN 2194 [S2].

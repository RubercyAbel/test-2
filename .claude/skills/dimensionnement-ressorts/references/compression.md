# Ressort hélicoïdal de compression — formulaire (EN 13906-1)

Notations : d fil, D diamètre moyen, De = D + d, Di = D − d, n spires actives, nt spires totales,
L0 longueur libre, Lc longueur à bloc, s flèche, R raideur, G module de cisaillement. Unités mm, N, MPa.

## Géométrie et raideur
- Indice d'enroulement : C = D/d (plage conseillée 5–12, possible 4–16).
- Raideur : **R = G·d⁴ / (8·D³·n)**  → n = G·d⁴ / (8·D³·R).
- Effort : F = R·s.
- Extrémités (nt = n + nm) :

| Extrémités | nm | Lc max |
|---|---|---|
| Rapprochées meulées (standard) | 2 | nt·d |
| Rapprochées non meulées | 2 | (nt + 1,5)·d |
| Libres meulées | 1 | nt·d |
| Libres | 0 | (nt + 1)·d |

  Pour des extrémités rapprochées meulées, prendre n se terminant par ,5 afin que les extrémités soient opposées.
- Somme minimale des jeux entre spires à Ln (statique) : **Sa = (0,0015·D²/d + 0,1·d)·n** ; en dynamique, doubler Sa.
  Condition : L2 (plus petite longueur de service) ≥ Lc + Sa.
- Augmentation de De à bloc : ΔDe = 0,1·(m² − 0,8·m·d − 0,2·d²)/D, avec m le pas. Elle détermine le jeu dans l'alésage.

## Contraintes
- Contrainte nominale : **τ = 8·F·D / (π·d³)**.
- Facteur de correction (courbure) : k = (C + 0,5)/(C − 0,75) (Bergsträsser, EN) ≈ Wahl (4C−1)/(4C−4) + 0,615/C.
- **Statique** : comparer τ non corrigé à τadm ≈ 0,5·Rm (EN 13906-1, fil écroui à froid).
  Viser une marge : 0,45·Rm en avant-projet.
- **À bloc sûr** : τc = 8·Fc·D/(π·d³) ≤ τadm, sinon le ressort se tasse s'il est mis à bloc.
  Si ce n'est pas le cas, prévoir une butée mécanique ou un pré-tassement par le fabricant.
- **Dynamique** : on utilise τk = k·τ. Course de contrainte : τkh = τk2 − τk1.
  - EN 13906-1 : comparer τkh et τk2 au diagramme de Goodman du matériau (abaques de la norme, pour 10⁷ cycles).
  - Shigley (Goodman + Zimmerli, d < 10 mm) : Ssu = 0,67·Rm ;
    Ssa/Ssm = 241/379 MPa (non grenaillé) ou 398/534 MPa (grenaillé) ;
    Sse = Ssa/(1 − Ssm/Ssu) ; **nf = 1 / (τa/Sse + τm/Ssu)** ≥ 1,2 à 1,5.

## Flambage (EN 13906-1)
Flèche critique :
sk = L0 · 0,5/(1 − G/E) · [1 − √(1 − (1 − G/E)/(0,5 + G/E) · (π·D/(ν·L0))²)]

| Appuis | ν |
|---|---|
| Deux plateaux parallèles guidés (encastré–encastré) | 0,5 |
| Encastré – articulé | 0,7 |
| Articulé – articulé | 1 |
| Encastré – libre | 2 |

Si la racine est imaginaire, le ressort est stable. Règle rapide en acier avec ν = 0,5 : stable si L0/D < 5,2.
Sinon, guider le ressort sur une tige ou dans un alésage (jeu ≈ 0,1·D), ou réduire L0/D.

## Dynamique
- Fréquence propre (deux extrémités sur plateaux) : f = ½·√(R/m), m = ρ·π²·d²·D·n/4.
  Pour l'acier : f ≈ 3,56·10⁵ · d/(n·D²) Hz, avec d et D en mm.
- Garder la fréquence d'excitation < f/13 pour éviter le « surge » (onde dans les spires).

## Démarche de conception (charge F1 à L1, F2 à L2)
1. R = (F2 − F1)/(L1 − L2) ; L0 = L1 + F1/R.
2. Choisir le matériau (voir `materiaux.md`) et C (≈ 6–9).
3. Estimer d par **d ≈ ∛(8·k·F2·C / (π·τadm))**, puis itérer, car Rm dépend de d. Retenir un diamètre normalisé.
4. D = C·d ; contrôler De + ΔDe ≤ alésage − jeu et Di ≥ tige + jeu.
5. n = G·d⁴/(8·D³·R), arrondi à 0,5 ; nt, Lc, Sa.
6. Vérifier : L2 ≥ Lc + Sa, τ statique, à bloc sûr, flambage, fatigue et fréquence.
7. Spécifier le ressort (voir la section Plan dans SKILL.md).

# Ressort hélicoïdal de compression — formulaire (EN 13906-1)

Notations : d fil, D diamètre moyen, De = D + d, Di = D − d, n spires actives, nt spires totales,
L0 longueur libre, Lc longueur à bloc, s flèche, R raideur, G module de cisaillement. Unités mm, N, MPa.
Les repères [S#] renvoient à `sources.md`.

Domaine EN 13906-1 (enroulé à froid) : d ≤ 20 mm, n ≥ 2, 4 ≤ w = D/d ≤ 20 [S1]. Plage conseillée : 4–12 (Shigley [S8]), idéalement 5–10.

## Géométrie et raideur [S2]
- Raideur : **R = G·d⁴ / (8·D³·n)**  → n = G·d⁴ / (8·D³·R) ; F = R·s.
- Extrémités (nt = n + nm) :

| Extrémités | nm | Lc max | Pas m | Source |
|---|---|---|---|---|
| Rapprochées meulées (standard) | 2 | nt·dmax | (L0 − d)/n | [S2][S3] |
| Rapprochées non meulées | 2 | (nt + 1,5)·dmax | (L0 − 2,5·d)/n | [S2][S3] |
| Libres meulées | 1 | nt·d | L0/(n + 1) | Shigley [S8] |
| Libres | 0 | (nt + 1)·d | (L0 − d)/n | Shigley [S8] |

- Pas maximal conseillé ≈ 0,7·Di [S3].
- Somme minimale des jeux entre spires actives à Ln [S2][S3] :
  **Sa = (0,0015·D²/d + 0,1·d)·n** en statique, **× 1,5 en dynamique**.
  Pour un ressort enroulé à chaud : 0,02·(D + d)·n en statique, 0,04·(D + d)·n en dynamique.
  Condition : Ln = Lc + Sa ≤ L2.
- Augmentation de De sous charge : **ΔDe = 0,1·(m² − 0,8·m·d − 0,2·d²)/D**, avec m le pas [S2][S3].

## Contraintes
- Nominale (non corrigée) : **τ = 8·F·D / (π·d³)** = G·d·s/(π·n·D²) [S2].
- Correction de courbure (Bergsträsser) : **k = (w + 0,5)/(w − 0,75)**, identique au K_B = (4C + 2)/(4C − 3) de Shigley [S2][S8].
  Wahl, pour comparaison : (4C − 1)/(4C − 4) + 0,615/C.
- **Statique / quasi-statique** (< 10⁴ cycles [S1]) : τ non corrigé ≤ **τzul = 0,5·Rm** [S2].
  Rm est la valeur **minimale** du tableau EN 10270 pour le diamètre considéré.
  Shigley procède autrement : il compare la contrainte corrigée K_B·τ à Ssy = 0,45·Sut (fil à corde à piano) [S8].
- **À bloc** : τc ≤ **0,56·Rm** [S2][S3]. Sinon, le ressort se tasse s'il est mis à bloc : prévoir une butée ou un pré-tassement.
- **Dynamique** (> 10⁴ cycles) : utiliser τk = k·τ. On vérifie la contrainte maximale τk2 et la course τkh = τk2 − τk1.
  - EN 13906-1 : comparer aux diagrammes de Goodman de la norme (10⁷ cycles à froid [S1]). Ces abaques ne sont **pas publics** : demander au fournisseur.
  - Shigley [S8] (Goodman + Zimmerli, d < 10 mm) : Ssu = 0,67·Sut ;
    Ssa/Ssm = 241/379 MPa (non grenaillé) ou 398/534 MPa (grenaillé) ;
    Sse = Ssa/(1 − Ssm/Ssu) ; **nf = 1/(τa/Sse + τm/Ssu)**, avec τa et τm corrigés par K_B.
  - Gutekunst recommande de grenailler tout ressort dynamique dont le fil dépasse 1 mm [S2].

## Flambage (EN 13906-1) [S3]
sK = L0 · 0,5/(1 − G/E) · [1 − √(1 − (1 − G/E)/(0,5 + G/E) · (π·D/(ν·L0))²)]

| Appuis | ν |
|---|---|
| Deux plateaux parallèles guidés | 0,5 |
| Encastré – articulé | 0,7 |
| Articulé – articulé | 1 |
| Encastré – libre | 2 |

ν décrit la tenue des plateaux, pas le meulage. Mais des extrémités non meulées (appui sur le fil rond) encastrent mal.
Avec `rapprochees` ou `libres` et ν = 0,5, le calculateur conseille donc de refaire le calcul avec ν = 0,7.
C'est un jugement d'ingénieur, non sourcé.

Si la racine est imaginaire, le ressort est stable.
Shigley : stabilité absolue si L0 < 2,63·D/α, soit L0/D < 5,26 pour α = 0,5 [S8].
Sinon, guider le ressort sur une tige ou dans un alésage, ou réduire L0/D.

## Dynamique
- Fréquence propre (deux extrémités sur plateaux) : **fe = 3560·d·√(G/ρ) / (n·D²)** en Hz, avec d et D en mm, G en MPa, ρ en kg/dm³ [S3].
  Pour l'acier, G = 81 500 et ρ = 7,85 donnent fe ≈ 3,63·10⁵·d/(n·D²). Shigley donne la même chose sous la forme f = ½·√(k/m).
- Shigley : la fréquence propre doit valoir **15 à 20 fois** la fréquence d'excitation [S8].

## Démarche de conception (charge F1 à L1, F2 à L2)
1. R = (F2 − F1)/(L1 − L2) ; L0 = L1 + F1/R.
2. Choisir le matériau (voir `materiaux.md`) et w ≈ 6–9.
3. Estimer d [S3] : **d ≈ ∛(8·F2·D/(π·τzul))** ou, à C fixé, d ≈ √(8·F2·C/(π·τzul)). Itérer, car Rm dépend de d. Retenir un diamètre normalisé.
4. D = w·d ; contrôler De + ΔDe ≤ alésage − jeu et Di ≥ tige + jeu.
5. n = G·d⁴/(8·D³·R), arrondi à 0,5 ; nt, Lc, Sa.
6. Vérifier : L2 ≥ Ln, τ2 ≤ 0,5·Rm, τc ≤ 0,56·Rm, flambage, fatigue et fréquence.
7. Spécifier le ressort : tolérances **EN 15800**, classes 1/2/3 [S10].

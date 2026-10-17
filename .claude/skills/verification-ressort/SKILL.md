---
name: verification-ressort
description: Vérifie un ressort existant (plan, référence catalogue, échantillon mesuré ou définition proposée par un fournisseur) et rend un verdict conforme / à risque / non conforme sur contraintes, à bloc, flambage, fatigue, fréquence, jeux de montage et complétude de la cotation (EN 15800, DIN 2097, DIN 2194). À utiliser pour « vérifie ce ressort », « mon ressort casse / se tasse / flambe », « ce ressort catalogue convient-il ? », revue de plan ressort, ou analyse de défaillance d'un ressort.
---

# Vérification et diagnostic d'un ressort

S'appuie sur le calculateur et les formulaires du skill `dimensionnement-ressorts` :
`.claude/skills/dimensionnement-ressorts/scripts/ressort.py` et `.claude/skills/dimensionnement-ressorts/references/`.

## 1. Relever la définition
Extraire du plan, du catalogue ou de la mesure : type, matériau, d, De/Di/D, n et nt, L0, extrémités, sens d'enroulement, traitements, points de charge spécifiés, tolérances.
Pour un échantillon mesuré : n actives ≈ nt − 2 (extrémités rapprochées). Contrôler la raideur mesurée par rapport à la raideur calculée : un écart supérieur à 10 % indique une erreur sur d, n ou le matériau.

Relever aussi **les conditions réelles d'utilisation** : longueurs ou angles mini et maxi en service, cycles, fréquence, guidage, température, milieu.

## 2. Recalculer
```bash
S=.claude/skills/dimensionnement-ressorts/scripts/ressort.py
python3 $S compression --d … --D … --n … --L0 … --F1 … --F2 … --appuis encastre --fatigue
python3 $S traction --d … --D … --n … --F0 … --F … --L0 …
python3 $S torsion --d … --D … --n … --M … --l1 … --l2 … --axe …
```
Si l'utilisateur fournit des longueurs plutôt que des efforts : F = R·(L0 − L).

## 3. Grille de vérification
| # | Critère | Conforme si |
|---|---|---|
| 1 | Indice C | 4 ≤ C ≤ 16 (idéal 5–12) |
| 2 | Contrainte statique max | τ ≤ 0,5·Rm (compression) ; corps ≤ 0,45·Rm (traction, EN) et crochets ≤ 0,75·Rm en flexion / 0,40·Rm en torsion (Shigley) ; σq ≤ 0,7·Rm (torsion) |
| 3 | À bloc sûr (compression) | τc ≤ 0,56·Rm, ou butée qui empêche la mise à bloc |
| 4 | Jeu mini entre spires | L2 ≥ Lc + Sa (Sa × 1,5 en dynamique) |
| 5 | Flambage | flèche max < sK, ou ressort guidé |
| 6 | Fatigue (si > 10⁴ cycles) | nf ≥ 1,2 (≥ 1,5 si sécurité) ; grenaillage spécifié si fil > 1 mm |
| 7 | Fréquence | f propre ≥ 15 à 20 × f excitation (Shigley) |
| 8 | Jeux de montage | De + ΔDe < alésage ; Di > tige ; Di' sous couple > axe × 1,1 (torsion) |
| 9 | Température / milieu | matériau compatible (cf. `materiaux.md`) |
| 10 | Cotation | ≤ 2 efforts fonctionnels tolérancés ; norme de tolérance adaptée (EN 15800 compression, DIN 2097 traction, DIN 2194 torsion) ; matériau normalisé ; sens d'enroulement ; extrémités ; traitements ; L0 ou n libre pour l'ajustement |

Les valeurs et leurs sources sont détaillées dans `.claude/skills/dimensionnement-ressorts/references/` (repères [S#] vers `sources.md`).
Si le fournisseur donne la Rm réelle du lot, la passer avec `--Rm`.

## 4. Diagnostic de défaillance (si incident)
- **Rupture en fatigue** (faciès plat, lignes d'arrêt, amorce en fibre intérieure) : course de contrainte trop forte, absence de grenaillage, défaut de surface, corrosion, résonance (surge).
- **Rupture au crochet** (traction) : rayon de pliage trop faible (r2 < 2d), crochet mal orienté.
- **Tassement / perte d'effort** : τ trop proche de τadm, ressort mis à bloc, température excessive (relaxation), absence de pré-tassement.
- **Flambage ou frottement** : L0/D élevé sans guidage, appuis non parallèles, jeu insuffisant (ΔDe).
- **Rupture fragile différée** après revêtement : fragilisation par l'hydrogène (zingage électrolytique sans dégazage).
- **Usure / rupture de branche** (torsion) : ressort chargé dans le sens du déroulement, serrage sur l'axe.

## 5. Rendu
1. **Verdict global** : ✅ conforme / ⚠️ à risque / ❌ non conforme.
2. Tableau de la grille, avec valeurs calculées et marges.
3. Causes probables (en cas d'incident), classées par vraisemblance.
4. Corrections proposées, chiffrées (nouveau d, n, L0, matériau ou traitement), revérifiées avec le calculateur. Pour une refonte complète, basculer sur `dimensionnement-ressorts`.
5. Limites : valeurs matière indicatives, essais recommandés pour une pièce de sécurité.

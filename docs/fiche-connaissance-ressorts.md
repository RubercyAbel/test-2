# Fiche de connaissance — Conception et dimensionnement des ressorts

> Synthèse pratique pour concevoir, dimensionner et spécifier des ressorts hélicoïdaux en fil rond.
> Unités : mm, N, MPa. Références : EN 13906-1/2/3, EN 10270-1/2/3, EN 15800, EN ISO 2162, Shigley *Mechanical Engineering Design* (ch. 10), SMI *Handbook of Spring Design*.

---

## 1. Familles de ressorts et choix

| Type | Fonction | Atouts | Limites | Norme de calcul |
|---|---|---|---|---|
| Hélicoïdal de **compression** | Pousser, amortir, stocker de l'énergie | Simple, robuste, reste porteur même cassé | Flambage si élancé ; place à bloc | EN 13906-1 |
| Hélicoïdal de **traction** | Tirer, rappeler | Compact à vide, tension initiale | Crochets fragiles en fatigue ; libère la pièce s'il rompt | EN 13906-2 |
| Hélicoïdal de **torsion** | Couple autour d'un axe (charnières, rappels) | Couple sur un axe | Frottement sur l'axe, réduction de Di | EN 13906-3 |
| Rondelle **Belleville** | Efforts très élevés, courses faibles | Très compact, courbe réglable par empilage | Course faible, frottement | EN 16983 / DIN 2092 |
| **Lame** / ressort plat | Contacts, clips, suspension | Formes libres | Calcul de poutre au cas par cas | – |
| **Spiral** / à force constante | Couple sur grand angle, enrouleurs | Grande rotation | Fabrication spécifique | – |
| Ressort **à gaz** / élastomère | Amortissement, effort quasi constant | Effort quasi constant, amortissement | Température, durée de vie des joints | Fournisseur |

**Règle de choix** : privilégier la compression. Passer en traction si l'encombrement l'impose, en torsion pour un couple.

---

## 2. Vocabulaire et notations (hélicoïdal)

| Symbole | Signification |
|---|---|
| d | diamètre du fil |
| D, De, Di | diamètre moyen, extérieur (D + d), intérieur (D − d) |
| C = D/d | indice d'enroulement (idéal 5–12) |
| n, nt | spires actives, spires totales |
| L0, Ln, Lc | longueur libre, longueur minimale de service, longueur à bloc |
| s, R | flèche, raideur (N/mm ou N·mm/°) |
| F0 | tension initiale (traction) |
| τ, σ | contrainte de torsion (compression/traction), de flexion (torsion) |
| Rm | résistance à la traction du fil, qui **dépend de d** |

---

## 3. Formules essentielles

### 3.1 Compression
- Raideur : **R = G·d⁴ / (8·D³·n)**
- Contrainte : **τ = 8·F·D / (π·d³)**, corrigée par k = (C + 0,5)/(C − 0,75) en dynamique.
- Longueur à bloc : Lc = nt·d (extrémités meulées) ; nt = n + 2 (extrémités rapprochées).
- Jeu minimal entre spires : Sa = (0,0015·D²/d + 0,1·d)·n, et Ln ≥ Lc + Sa.
- Statique : τ ≤ 0,5·Rm. **À bloc sûr** si τ à Lc ≤ 0,5·Rm.
- Flambage : stable si L0/D < ≈ 5,2 (appuis plans guidés). Sinon, appliquer la formule EN de la flèche critique ou guider le ressort.
- Fréquence propre (acier) : f ≈ 3,56·10⁵·d/(n·D²) Hz. Rester sous f/13.

### 3.2 Traction
- R = G·d⁴/(8·D³·na), avec na = n + G/E ; **F = F0 + R·s**.
- Tension initiale réalisable : τi ≈ 231·e^(−0,105·C) ± 6,9·(4 − (C − 3)/6,5) MPa.
- Crochets : flexion σA ≤ 0,75·Rm et torsion τB ≤ 0,40·Rm. Rayon de pliage ≥ 2·d.

### 3.3 Torsion
- R = E·d⁴/(64·D·na) [N·mm/rad], avec na = n + (l1 + l2)/(3·π·D).
- σ = Ki·32·M/(π·d³), avec Ki = (4C² − C − 1)/(4C·(C − 1)) ; σ ≤ ≈ 0,7·Rm.
- Di sous charge : n·D/(n + α/360) − d. Prévoir un jeu d'environ 10 % sur l'axe. Charger dans le sens de l'enroulement.

### 3.4 Fatigue (compression et traction)
- Charges alternées : τa = k·τ(Fa), τm = k·τ(Fm), avec Fa = (F2 − F1)/2 et Fm = (F2 + F1)/2.
- Goodman + Zimmerli (Shigley, d < 10 mm, 10⁷ cycles) :
  Ssu = 0,67·Rm ; Ssa/Ssm = 241/379 MPa (brut) ou 398/534 MPa (grenaillé) ;
  Sse = Ssa/(1 − Ssm/Ssu) ; **nf = 1/(τa/Sse + τm/Ssu)**, à viser ≥ 1,2–1,5.
- EN 13906-1 : diagrammes de Goodman par matériau (course τkh et τk2).

---

## 4. Matériaux (aperçu)

| Fil | Rm (d = 2 mm) | G (GPa) | T max | Usage |
|---|---|---|---|---|
| EN 10270-1 **DH** | ≈ 2000 MPa | 81,5 | 80 °C | Standard, statique et dynamique |
| EN 10270-1 SH | ≈ 1560 MPa | 81,5 | 80 °C | Statique économique |
| EN 10270-2 **VDSiCr** | ≈ 1830 MPa | 79,5 | 250 °C | Haute fatigue (soupapes) |
| EN 10270-2 FDCrV | ≈ 1780 MPa | 79,5 | 220 °C | Chocs, température |
| EN 10270-3 **1.4310** | ≈ 1700 MPa | 70 | 250 °C | Corrosion |
| CuSn6 | ≈ 1000 MPa | 42 | 80 °C | Amagnétique, conducteur |

Rm ≈ A/d^m : plus le fil est fin, plus il est résistant. Ces valeurs sont indicatives ; se reporter à la norme ou au certificat matière.

**Traitements** : détensionnement (systématique), **grenaillage** (+30 à 60 % en fatigue), pré-tassement (supprime le tassement initial), revêtements. Attention à la fragilisation par l'hydrogène avec le zingage électrolytique.

---

## 5. Démarche de conception (compression)

1. **Besoin** : points (F1, L1) et (F2, L2), encombrement (alésage, tige), sollicitation, environnement.
2. **Raideur et L0** : R = (F2 − F1)/(L1 − L2) ; L0 = L1 + F1/R.
3. **Matériau et indice** : choisir le fil, puis C ≈ 6–9.
4. **Fil** : d ≈ ∛(8·k·F2·C/(π·τadm)), à itérer car Rm dépend de d. Retenir un diamètre normalisé.
5. **Géométrie** : D = C·d ; contrôler De + ΔDe ≤ alésage − jeu et Di ≥ tige + jeu.
6. **Spires** : n = G·d⁴/(8·D³·R), arrondi à 0,5 ; nt, Lc, Sa.
7. **Vérifications** : Ln ≥ Lc + Sa ; τ statique ; à bloc sûr ; flambage ; fatigue ; fréquence.
8. **Spécification** : plan EN ISO 2162, tolérances EN 15800.

### Exemple chiffré
Besoin : 20 N à 40 mm, 60 N à 30 mm, alésage de 20 mm, fil DH, usage cyclique.
- R = 40/10 = **4 N/mm** ; L0 = 40 + 20/4 = **45 mm**.
- Solution retenue : **d = 1,6 mm, D = 12,8 mm (De = 14,4 mm), C = 8, n = 8, nt = 10**, extrémités rapprochées meulées.
- R = 3,98 N/mm ; Lc = 16 mm ; Ln mini = 18,5 mm < L2 = 29,9 mm ✅
- τ2 = 478 MPa < τadm = 0,5 × 2065 = 1033 MPa ✅ ; à bloc τc = 918 MPa < 1033 MPa → **à bloc sûr** ✅
- L0/D = 3,5 → **pas de flambage** ✅ ; f propre ≈ 443 Hz.
- Fatigue (non grenaillé) : nf = 1,20, à la limite → **grenailler** ou passer au VDSiCr pour gagner de la marge.

(Résultats obtenus avec `python3 .claude/skills/dimensionnement-ressorts/scripts/ressort.py compression --d 1.6 --D 12.8 --n 8 --L0 45 --F1 20 --F2 60 --fatigue`.)

---

## 6. Spécifier un ressort sur plan

- Au plus **2 points de charge fonctionnels** tolérancés (F @ L), plus L0 ou n laissé « à ajuster par le fabricant ».
- Matériau normalisé (ex. « EN 10270-1 DH »), d, De **ou** Di (un seul tolérancé), extrémités, **sens d'enroulement**, nt.
- Classe de tolérance **EN 15800** (1 = précise, 2 = standard, 3 = large).
- Traitements : détensionné, grenaillé, pré-tassé, revêtement.
- Torsion : position angulaire libre des branches et sa tolérance, sens de chargement.
- Traction : type et orientation des crochets, F0 avec sa tolérance (ou 2 points).

---

## 7. Erreurs fréquentes

| Erreur | Conséquence | Parade |
|---|---|---|
| Confondre D, De et Di | Raideur fausse de 30 % ou plus | Toujours préciser lequel |
| Oublier la variation de Rm avec d | Surdimensionnement ou rupture | Rm(d) issu de la norme |
| Ressort pas « à bloc sûr » sans butée | Tassement définitif | Vérifier τc, ou ajouter une butée |
| L0/D > 5 sans guidage | Flambage, frottement | Guider ou raccourcir |
| Ressort de torsion chargé en ouverture | Rupture prématurée | Charger dans le sens de l'enroulement |
| Crochet à petit rayon de pliage | Rupture en fatigue au crochet | r2 ≥ 2d, crochet réduit |
| Excitation proche de f propre | Surge, rupture rapide | f exc < f propre/13 |
| Trop de cotes tolérancées | Ressort infabricable | Au plus 2 cotes fonctionnelles |
| Zingage électrolytique d'un fil dur | Rupture fragile différée | Zinc lamellaire, ou dégazage |

---

## 8. Skills Claude associés

| Skill | Rôle | Déclencheurs |
|---|---|---|
| `dimensionnement-ressorts` | Concevoir un ressort à partir d'un cahier des charges, avec le calculateur `scripts/ressort.py` | « dimensionne un ressort », « il me faut X N à Y mm », « quelle raideur » |
| `verification-ressort` | Auditer un ressort existant ou un plan, diagnostiquer une défaillance | « vérifie ce ressort », « mon ressort casse / se tasse », « ce ressort catalogue convient-il » |

Emplacement : `.claude/skills/`. Claude Code charge automatiquement les skills de ce dépôt.
Pour une utilisation sur claude.ai, zipper le dossier d'un skill et l'importer depuis la section Skills des paramètres de claude.ai.

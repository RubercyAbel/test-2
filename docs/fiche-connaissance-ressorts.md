# Fiche de connaissance — Conception et dimensionnement des ressorts

> Synthèse pratique pour concevoir, dimensionner et spécifier des ressorts hélicoïdaux en fil rond enroulés à froid.
> Unités : mm, N, MPa. Les repères **[S#]** renvoient à la section 9 (sources consultées le 17/10/2026).
> Les normes EN complètes sont payantes : les formules ont été recoupées à partir d'extraits officiels, de formulaires de fabricants qui calculent selon EN 13906, et du cours de Shigley.

---

## 1. Familles de ressorts et choix

| Type | Fonction | Atouts | Limites | Norme de calcul |
|---|---|---|---|---|
| Hélicoïdal de **compression** | Pousser, amortir, stocker de l'énergie | Simple, robuste, reste porteur même cassé | Flambage si élancé ; place à bloc | EN 13906-1 |
| Hélicoïdal de **traction** | Tirer, rappeler | Ne flambe pas, tension initiale | Crochets fragiles en fatigue ; la rupture coupe la transmission d'effort [S2] | EN 13906-2 |
| Hélicoïdal de **torsion** | Couple autour d'un axe (charnières, rappels) | Couple sur un axe | Frottement sur l'axe, réduction de Di | EN 13906-3 |
| Rondelle **Belleville** | Efforts très élevés, courses faibles | Très compact, courbe réglable par empilage | Course faible, frottement | EN 16983 / DIN 2092 |
| **Lame** / ressort plat | Contacts, clips, suspension | Formes libres | Calcul de poutre au cas par cas | – |
| **Spiral** / à force constante | Couple sur grand angle, enrouleurs | Grande rotation | Fabrication spécifique | – |
| Ressort **à gaz** / élastomère | Amortissement, effort quasi constant | Effort quasi constant, amortissement | Température, durée de vie des joints | Fournisseur |

**Règle de choix** : privilégier la compression. Passer en traction si l'encombrement l'impose, en torsion pour un couple.
(Belleville, lames, spiraux et ressorts à gaz sont cités pour mémoire : non couverts par les skills.)

Domaine EN 13906-1 pour l'enroulement à froid : d ≤ 20 mm, n ≥ 2, 4 ≤ w = D/d ≤ 20 [S1].

---

## 2. Vocabulaire et notations (hélicoïdal)

| Symbole | Signification |
|---|---|
| d | diamètre du fil |
| D, De, Di | diamètre moyen, extérieur (D + d), intérieur (D − d) |
| w = C = D/d | indice d'enroulement (conseillé 5–12 ; Shigley : 4–12) |
| n, nt | spires actives, spires totales |
| L0, Ln, Lc | longueur libre, longueur minimale de service, longueur à bloc |
| s, R | flèche, raideur (N/mm ou N·mm/°) |
| F0 | tension initiale (traction) |
| τ, σ | contrainte de torsion (compression/traction), de flexion (torsion) |
| Rm | résistance **minimale** à la traction du fil (EN 10270), qui **dépend de d** |

---

## 3. Formules essentielles

### 3.1 Compression (EN 13906-1)
- Raideur : **R = G·d⁴ / (8·D³·n)** [S2]
- Contrainte : **τ = 8·F·D / (π·d³)** ; corrigée **τk = k·τ** avec k = (w + 0,5)/(w − 0,75) (Bergsträsser), **uniquement en dynamique** [S2].
- Longueur à bloc : nt = n + 2 ; Lc = nt·dmax pour des extrémités meulées, (nt + 1,5)·dmax sinon [S2].
- Jeu minimal entre spires : **Sa = (0,0015·D²/d + 0,1·d)·n**, **× 1,5 en dynamique** ; Ln = Lc + Sa ≤ L2 [S2][S3].
- Statique : **τ ≤ 0,5·Rm** ; à bloc : **τc ≤ 0,56·Rm** (« à bloc sûr ») [S2].
- Augmentation de De : ΔDe = 0,1·(m² − 0,8·m·d − 0,2·d²)/D, avec m = (L0 − d)/n pour des extrémités meulées [S2].
- Flambage : sK = L0·0,5/(1 − G/E)·[1 − √(1 − (1 − G/E)/(0,5 + G/E)·(π·D/(ν·L0))²)], avec ν = 0,5 / 0,7 / 1 / 2 selon les appuis [S3].
  Règle rapide : stable si L0/D < 5,26 avec des appuis plans guidés [S8].
- Fréquence propre : **fe = 3560·d·√(G/ρ)/(n·D²)** Hz, avec G en MPa et ρ en kg/dm³ [S3]. Pour l'acier, fe ≈ 3,63·10⁵·d/(n·D²).
  La fréquence propre doit valoir **15 à 20 fois** la fréquence d'excitation [S8].

### 3.2 Traction (EN 13906-2)
- **F = F0 + R·s**, avec R = G·d⁴/(8·D³·n) [S2]. Shigley prend na = n + G/E pour compter les crochets [S8].
- Corps : τ ≤ **0,45·Rm** ; n'utiliser que 80 % de la flèche admissible [S2].
- Tension initiale réalisable (Shigley) : τi = 231·e^(−0,105·C) ± 6,9·(4 − (C − 3)/6,5) MPa [S8].
- Crochets (Shigley) : flexion σA ≤ 0,75·Sut, torsion au pliage τB ≤ 0,40·Sut [S8].
- Pas de grenaillage possible (spires jointives). En dynamique, préférer des embouts roulés ou vissés et faire un essai [S2].
- **Embout vissé** : les spires en prise ne travaillent plus, donc na = n_total − spires vissées des deux côtés, et la raideur augmente. Il n'y a plus de contrainte de crochet ; le point critique est la dernière spire en prise. Ce décompte est un raisonnement mécanique, non sourcé : à valider par une mesure de raideur.
- Compression avec extrémités non meulées (appui sur le fil rond) : Lc plus long de 1,5·d, et flambage à calculer prudemment avec ν = 0,7 plutôt que 0,5 (jugement d'ingénieur).

### 3.3 Torsion (EN 13906-3)
- **RM = E·d⁴/(3667·D·n)** en N·mm/° [S2]. Shigley ajoute les branches : na = n + (l1 + l2)/(3·π·D) [S8].
- **σq = q·32·M/(π·d³)**, avec q = (w + 0,07)/(w − 0,75) ; σ ≤ **0,7·Rm** [S2].
- Di sous charge : D·n/(n + α/360) − d ; longueur du corps : (n + 1,5)·d [S2]. Prévoir un jeu d'environ 10 % sur l'axe. Charger dans le sens de l'enroulement.

### 3.4 Fatigue
- Statique ou quasi-statique : < 10⁴ cycles. Durée de vie infinie : 10⁷ cycles pour un ressort enroulé à froid [S1].
- EN 13906 : diagrammes de Goodman par matériau, non publics, à obtenir avec la norme ou auprès du fournisseur.
- **Compression** — Goodman + Zimmerli (Shigley, d < 10 mm) [S8] :
  τa = k·τ(Fa), τm = k·τ(Fm) ; Ssu = 0,67·Rm ; Ssa/Ssm = 241/379 MPa (brut) ou 398/534 MPa (grenaillé) ;
  Sse = Ssa/(1 − Ssm/Ssu) ; **nf = 1/(τa/Sse + τm/Ssu)**, à viser ≥ 1,2–1,5.
- **Torsion** — Gerber, avec Sr = 50 à 64 % de Sut selon le matériau, le grenaillage et le nombre de cycles (Shigley tab. 10-10) [S8].
- Grenailler les ressorts dynamiques de fil > 1 mm [S2].

---

## 4. Matériaux (aperçu)

| Fil | Rm min à d = 2 mm | E / G (GPa) | T max indicative | Usage |
|---|---|---|---|---|
| EN 10270-1 **SH / DH** | 1980 MPa (identique) [S5] | 206 / 81,5 | 80 °C | SH : statique ; DH : dynamique |
| EN 10270-2 FDC | 1730 MPa [S6] | 206 / 79,5 | non vérifiée | Statique, gros fils |
| EN 10270-2 **VDSiCr** | 2010 MPa [S6] | 206 / 79,5 | 120 °C [S4] | Haute fatigue (soupapes) |
| EN 10270-3 **1.4310** NS | 1700 MPa [S7] | 185 / 70 | 160 °C [S4] | Corrosion |
| CuSn6 | ≤ 900 MPa [S4] | 115 / 42 | 80 °C | Amagnétique, conducteur |

- Rm baisse quand d augmente : DH vaut 2230 MPa à 1 mm et 1660 MPa à 5 mm [S5]. Toujours prendre la valeur du tableau au bon diamètre, ou celle du certificat matière.
- Correction de température (aciers) : G(T) = G(20 °C)·(3620 − T)/3600 [S3].
- **Traitements** : détensionnement (systématique), **grenaillage** (Zimmerli : Ssa passe de 241 à 398 MPa), pré-tassement, revêtements.

---

## 5. Démarche de conception (compression)

1. **Besoin** : points (F1, L1) et (F2, L2), encombrement (alésage, tige), sollicitation, environnement.
2. **Raideur et L0** : R = (F2 − F1)/(L1 − L2) ; L0 = L1 + F1/R.
3. **Matériau et indice** : choisir le fil, puis w ≈ 6–9.
4. **Fil** : d ≈ ∛(8·F2·D/(π·τzul)) [S3], à itérer car Rm dépend de d. Retenir un diamètre normalisé.
5. **Géométrie** : D = w·d ; contrôler De + ΔDe ≤ alésage − jeu et Di ≥ tige + jeu.
6. **Spires** : n = G·d⁴/(8·D³·R), arrondi à 0,5 ; nt, Lc, Sa.
7. **Vérifications** : Ln ≤ L2 ; τ2 ≤ 0,5·Rm ; τc ≤ 0,56·Rm ; flambage ; fatigue ; fréquence.
8. **Spécification** : plan EN ISO 2162-1, tolérances EN 15800 [S10].

### Exemple chiffré
Besoin : 20 N à 40 mm, 60 N à 30 mm, alésage de 20 mm, fil DH, usage cyclique.
- R = 40/10 = **4 N/mm** ; L0 = 40 + 20/4 = **45 mm**.
- Solution retenue : **d = 1,6 mm, D = 12,8 mm (De = 14,4 mm), w = 8, n = 8, nt = 10**, extrémités rapprochées meulées.
- R = 3,98 N/mm ; Lc = 16 mm ; Ln = 19,8 mm (dynamique) < L2 = 29,9 mm ✅
- Rm min = 2060 MPa (DH, d = 1,6 mm).
  τ2 = 478 MPa < 0,5·Rm = 1030 MPa ✅ ; τc = 918 MPa < 0,56·Rm = 1154 MPa → **à bloc sûr** ✅
- L0/D = 3,5 → **pas de flambage** ✅ ; fe ≈ 443 Hz, donc excitation admissible jusqu'à environ 22 Hz.
- Fatigue (non grenaillé, Goodman/Zimmerli) : nf = 1,20, à la limite → **grenailler** ou passer au VDSiCr pour gagner de la marge.

Obtenu avec `python3 .claude/skills/dimensionnement-ressorts/scripts/ressort.py compression --d 1.6 --D 12.8 --n 8 --L0 45 --F1 20 --F2 60 --fatigue`.
Le calculateur redonne les résultats des exemples publiés d'Axomek et de Shigley : voir `.claude/skills/dimensionnement-ressorts/references/sources.md`.

---

## 6. Spécifier un ressort sur plan

- Au plus **2 points de charge fonctionnels** tolérancés (F @ L), plus L0 ou n laissé « à ajuster par le fabricant ».
- Matériau normalisé (ex. « EN 10270-1 DH »), d, De **ou** Di (un seul tolérancé), extrémités, **sens d'enroulement**, nt.
- Tolérances : **EN 15800** (classes 1, 2, 3) pour la **compression** seulement [S10]. Gutekunst cite DIN 2097 pour la traction et DIN 2194 pour la torsion [S2].
- Traitements : détensionné, grenaillé, pré-tassé, revêtement.
- Torsion : position angulaire libre des branches et sa tolérance, sens de chargement.
- Traction : type d'anneau (allemand, anglais, crochet…) et orientation, F0 avec sa tolérance (ou 2 points).

---

## 7. Erreurs fréquentes

| Erreur | Conséquence | Parade |
|---|---|---|
| Confondre D, De et Di | Raideur fausse de 30 % ou plus | Toujours préciser lequel |
| Prendre une Rm constante | Surdimensionnement ou rupture | Rm min du tableau EN au bon diamètre |
| Confondre SH/DH (EN) avec le fil « hard-drawn » ASTM A227 | Rm de SH sous-estimée d'environ 20 % | SH = DH en Rm ; A227 ≈ SL/SM |
| Ressort non « à bloc sûr » sans butée | Tassement définitif | τc ≤ 0,56·Rm, ou butée |
| L0/D > 5 sans guidage | Flambage, frottement | Guider ou raccourcir |
| Oublier la majoration de Sa en dynamique | Spires qui se touchent, usure | Sa × 1,5 |
| Ressort de torsion chargé en ouverture | Rupture prématurée | Charger dans le sens de l'enroulement [S2] |
| Crochet à petit rayon de pliage | Rupture en fatigue au crochet | r2 ≥ 2d, embouts roulés ou vissés |
| Excitation proche de fe | Surge, rupture rapide | fe ≥ 15–20 × f exc [S8] |
| Trop de cotes tolérancées | Ressort infabricable | Au plus 2 cotes fonctionnelles |

---

## 8. Skills Claude associés

| Skill | Rôle | Déclencheurs |
|---|---|---|
| `dimensionnement-ressorts` | Concevoir un ressort à partir d'un cahier des charges, avec le calculateur `scripts/ressort.py` | « dimensionne un ressort », « il me faut X N à Y mm », « quelle raideur » |
| `verification-ressort` | Auditer un ressort existant ou un plan, diagnostiquer une défaillance | « vérifie ce ressort », « mon ressort casse / se tasse », « ce ressort catalogue convient-il » |

Emplacement : `.claude/skills/`. Claude Code charge automatiquement les skills de ce dépôt.
Pour une utilisation sur claude.ai, zipper le dossier d'un skill et l'importer depuis la section Skills des paramètres de claude.ai.

---

## 9. Sources

| # | Source | Apport |
|---|---|---|
| S1 | Extrait officiel EN 13906-1:2013 (iTeh) — https://cdn.standards.iteh.ai/samples/38074/dc919140f4c049d693d94831cb248018/SIST-EN-13906-1-2014.pdf | Domaine, symboles, types de sollicitation |
| S2 | Gutekunst Federn, *Design of metal springs – Part 2* — https://blog.federnshop.com/en/design-of-metal-springs-part-2-calculation/ | Formules EN 13906-1/2/3 et contraintes admissibles |
| S3 | Gutekunst, formulaire compression — https://blog.federnshop.com/wp-content/uploads/Gutekunst_Druckfedern_Formeln_2015.pdf | Flambage, fréquence, Sa dynamique, G(T) |
| S4 | Gutekunst, propriétés des fils — https://blog.federnshop.com/en/spring-steel-wires-and-their-properties/ | E, G, ρ, températures |
| S5 | Mollificio Modenese, EN 10270-1 — https://www.mollificiomodenese.it/en/insights/materials-used/music-wire-uni-en-10270-1-sh-dh/ (recoupé avec https://www.metalleschmidt.de/en/wire/hard-drawn-steel/) | Rm SH/DH |
| S6 | Lemetal, EN 10270-2 — https://lemetal.ro/oil-tempered-steel-wire-according-to-en-10270-2/ | Rm FDC, FDSiCr, VDSiCr |
| S7 | Extrait officiel EN 10270-3 (iTeh) — https://cdn.standards.iteh.ai/samples/30610/fa0cca4f41ba4e95956d0de6c0b9a63f/SIST-EN-10270-3-2012.pdf | Rm des inox |
| S8 | Shigley, *Mechanical Engineering Design*, ch. 10 (support de cours) — https://www.philadelphia.edu.jo/academics/mgogazeh/uploads/DESIGN%202%20CH10.pdf | Fatigue, crochets, tension initiale, torsion, exemples |
| S9 | Axomek, calcul EN 13906 — https://axomek.com/calculations/spring-calculation-en-13906/ | Exemple de validation |
| S10 | Catalogue iTeh EN 15800:2008 — https://standards.iteh.ai/catalog/standards/cen/ccd4840e-89d8-45ae-bb0d-f8c650b2fa64/en-15800-2008 | Domaine de la norme de tolérances |

**Non vérifié** (à confirmer dans la norme achetée ou auprès du fournisseur) :
- diagrammes de Goodman EN ;
- Rm du CuSn6 (EN 12166) ;
- températures maximales FDC/FDSiCr ;
- Rm du 1.4310 au-delà de 4,25 mm ;
- statut actuel de DIN 2097 et DIN 2194 ;
- fragilisation par l'hydrogène des fils zingués (bonne pratique générale, non sourcée ici).

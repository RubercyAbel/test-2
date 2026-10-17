---
name: dimensionnement-ressorts
description: Conçoit et dimensionne des ressorts hélicoïdaux de compression, traction et torsion (fil rond) selon EN 13906 et Shigley — choix du type et du matériau, calcul de d, D, n, L0, raideur, contraintes, flambage, fatigue, fréquence propre, puis spécification de fabrication. À utiliser dès qu'on demande de concevoir, dimensionner, calculer, choisir ou remplacer un ressort, de trouver une raideur, ou de partir d'un cahier des charges effort/longueur/encombrement (« il me faut un ressort qui fait 50 N à 30 mm », « spring design », « calcul de ressort »).
---

# Dimensionnement de ressorts hélicoïdaux

Ce skill guide la conception d'un ressort à partir d'un besoin fonctionnel, jusqu'à une définition fabricable.
Unités : **mm, N, N·mm, MPa**. Les calculs se font avec `scripts/ressort.py` (Python 3, sans dépendance) plutôt qu'à la main.

## 1. Recueillir le cahier des charges
Poser les questions manquantes, mais ne pas bloquer : proposer des hypothèses par défaut et les annoncer.
- **Fonction** : pousser (compression), tirer (traction) ou appliquer un couple (torsion).
- **Points de fonctionnement** : (F1, L1) et (F2, L2), ou un couple et un angle. Sinon, une raideur et une course.
- **Encombrement** : alésage maxi, tige ou axe de guidage, longueur disponible à vide et en position comprimée.
- **Sollicitation** : statique (< 10⁴ cycles) ou dynamique (nombre de cycles, fréquence).
- **Environnement** : température, corrosion, magnétisme, conductivité, choc.
- **Contraintes industrielles** : quantité, coût, tolérances visées, ressort catalogue acceptable ou non.
  Normes de tolérance : EN 15800 classes 1/2/3 pour la compression ; DIN 2097 pour la traction et DIN 2194 pour la torsion (citées par Gutekunst).

Hypothèses par défaut : fil DH EN 10270-1 avec **Rm minimale du tableau EN**, extrémités rapprochées meulées, appuis plans parallèles (ν = 0,5), tolérances EN 15800 classe 2.
Limites admissibles EN 13906 : τ ≤ 0,5·Rm (compression), τc ≤ 0,56·Rm à bloc, τ ≤ 0,45·Rm (traction), σq ≤ 0,7·Rm (torsion).

Domaine couvert : ressorts **enroulés à froid** en fil rond (EN 13906-1 : d ≤ 20 mm, n ≥ 2, 4 ≤ D/d ≤ 20). Les ressorts enroulés à chaud ne sont pas traités par le calculateur.
Chaque formule des références porte un repère [S#] vers `references/sources.md`. Citer ces sources quand l'utilisateur demande d'où vient un résultat.

## 2. Choisir le type et le matériau
- Compression : le plus robuste, il reste porteur même cassé. Le préférer par défaut.
- Traction : les crochets sont des points faibles en fatigue. Prévoir une butée.
- Torsion : pour des couples sur un axe. Le charger dans le sens de l'enroulement.
- Hors périmètre du skill : rondelles Belleville (EN 16983), lames, ressorts spiraux, ressorts à gaz, fil de section rectangulaire. Les signaler et renvoyer à la norme ou au fournisseur.

Matériaux, Rm(d), G, E et températures limites : lire `references/materiaux.md`.

## 3. Dimensionner
Lire la référence du type concerné avant de calculer :
- `references/compression.md`
- `references/traction.md`
- `references/torsion.md`

Outil :
```bash
S=.claude/skills/dimensionnement-ressorts/scripts/ressort.py
python3 $S concevoir-compression --F1 20 --L1 40 --F2 60 --L2 30 --De-max 20 --materiau DH
python3 $S compression --d 1.6 --D 12.8 --n 8 --L0 45 --F1 20 --F2 60 --fatigue [--grenaille] [--Rm 2150]
python3 $S traction --d 1.5 --D 12 --n 20 --F0 10 --F 40 --L0 60
python3 $S torsion --d 2 --D 16 --n 6 --M 800 --M1 200 --l1 20 --l2 20 --axe 12   # --M1 : fatigue
python3 $S materiaux          # ajouter --json avant la sous-commande pour une sortie machine
```
`--Rm` remplace la Rm du tableau par la valeur du certificat matière.
`--fatigue` passe le calcul en dynamique : Sa est majoré de 50 %, et la fatigue est calculée par Goodman avec les données de Zimmerli.
Le calculateur est validé sur des exemples publiés (Axomek, Shigley) : voir `references/sources.md`.
`concevoir-compression` balaie les diamètres de fil normalisés et les indices C de 4 à 12, puis classe les solutions (sans alerte d'abord, masse croissante).
Repasser ensuite la solution retenue dans `compression` pour avoir tous les résultats, y compris la fatigue.

Itérer jusqu'à ce que **toutes les alertes** soient levées ou explicitement acceptées par l'utilisateur.
Leviers usuels :
- contrainte trop élevée → augmenter d ou réduire C, choisir un fil plus résistant, grenailler ;
- flambage → guider le ressort, réduire L0/D, augmenter D ;
- manque de place à bloc → réduire d·nt, utiliser un fil plus résistant, réduire la course ;
- fatigue → grenaillage, VDSiCr, réduire la course de contrainte.

## 4. Présenter le résultat
Fournir systématiquement :
1. **Hypothèses** (matériau, extrémités, appuis, τadm) et données d'entrée.
2. **Tableau de définition** : d, De (ou Di), n, nt, L0, Lc, sens d'enroulement, extrémités, matériau et traitements.
3. **Points de contrôle** : F1 @ L1 et F2 @ L2 avec tolérances. Ce sont les cotes fonctionnelles du plan : fixer au plus deux efforts et laisser L0 ou n « à ajuster par le fabricant ».
4. **Vérifications** : τ/τadm, à bloc sûr (oui/non), flambage, nf en fatigue, f propre, jeux de montage (ΔDe à bloc, Di' sous couple).
5. **Recommandations** : guidage, traitements, alternatives (ressort catalogue proche, autre matériau).

Le plan suit EN ISO 2162-1 (représentation des ressorts). Indiquer la norme de tolérance et la mention « ressort détensionné », plus « grenaillé » ou « pré-tassé » si applicable.

## Garde-fous
- Les Rm sont les **minimums des tableaux EN** relevés chez des fournisseurs, et la fatigue suit Zimmerli/Shigley, pas les diagrammes EN (non publics). Le dire, et recommander la validation par le fournisseur ou par des essais pour toute pièce de sécurité.
- Ne pas présenter comme vérifié un point listé dans « Points restant non vérifiés » de `references/sources.md`.
- Ne pas confondre D moyen, De et Di : demander lequel l'utilisateur donne.
- Un ressort de sécurité (frein, soupape, arrêt d'urgence) se conçoit en compression, avec un coefficient de sécurité accru, et se valide par essai.
- Pour un audit d'un ressort existant ou d'un plan, utiliser le skill `verification-ressort`.

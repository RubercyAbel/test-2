---
name: rondelles-belleville
description: Calcule, sélectionne et vérifie des rondelles Belleville (ressorts à disque, disc springs) et leurs empilages en série et en parallèle selon EN 16984 (ex-DIN 2092) et EN 16983 (ex-DIN 2093) — effort non linéaire, raideur, contraintes aux points OM/I/II/III/IV, contrôle statique, contraintes de fatigue, frottement, longueur d'empilage, jeu de guidage, choix dans les séries A/B/C. À utiliser pour « rondelle Belleville », « ressort à disque », « empilage de rondelles », « disc spring », « Tellerfeder », précontrainte de boulon par rondelles, ou vérification d'un empilage existant.
---

# Rondelles Belleville

Unités : **mm, N, MPa**. Tous les calculs se font avec `scripts/belleville.py` (Python 3, sans dépendance).
Chaque formule et chaque règle vient d'une source listée dans `references/sources.md` (repères [B#]).
Le formulaire complet est dans `references/formulaire.md` : le lire avant de calculer.

**Règle absolue : ne pas présenter comme vérifié ce qui figure dans « Ce qui n'est PAS vérifié » de `sources.md`, et ne jamais inventer de valeur admissible en fatigue.**

## 1. Recueillir le besoin
Demander ce qui manque, sans bloquer :
- **Points de fonctionnement** : (F1, L1) et (F2, L2), ou un effort et une course.
- **Encombrement** : De maxi, diamètre de la tige ou de l'alésage de guidage, longueur disponible.
- **Sollicitation** : statique (< 10⁴ cycles) ou dynamique (nombre de cycles visé).
- **Matériau** : acier à ressort par défaut (E = 206 000 MPa, Rm ≈ 1600 MPa). Un autre matériau impose son E et sa limite.

## 2. Calculer
```bash
S=.claude/skills/rondelles-belleville/scripts/belleville.py
python3 $S selection --F1 3000 --L1 20 --F2 4500 --L2 18.5 --De-max 60 --guide 20   # choix dans les séries A/B/C
python3 $S rondelle --De 40 --Di 20.4 --t 2.25 --l0 3.15 [--s 0.3 0.6]              # rondelle seule
python3 $S rondelle --De 200 --Di 82 --t 12 --tp 11.5 --l0 16.6                     # groupe 3 : t' obligatoire
python3 $S empilage --De 40 --Di 20.4 --t 2.25 --l0 3.15 --serie 4 --parallele 2 \
    --L1 21.2 --L2 19.8 --serie-din A --guide 20.4                                  # empilage + frottement
python3 $S catalogue
python3 .claude/skills/rondelles-belleville/scripts/test_belleville.py              # 61 tests sur valeurs publiées
```
- `selection` parcourt les rondelles A/B/C du catalogue intégré (t ≤ 6 mm, liste partielle d'EN 16983 relevée chez SPIROL) avec 1 à 3 rondelles en parallèle. Elle garde les solutions qui tiennent les efforts à ±10 % avec s ≤ 0,75·h0 et L0 ≤ 3·De.
  Si aucune solution ne convient, le dire et proposer un calcul `rondelle` ou `empilage` sur une rondelle du fabricant.
- Pour le **groupe 3** (t > 6 mm), il faut t' (tableau EN 16983 ou fabricant). Sans t', le calcul est faux et le script le signale.

## 3. Vérifier
| Critère | Règle | Source |
|---|---|---|
| Domaine de validité | 1,75 ≤ δ ≤ 2,5 conseillé ; De/t > 50 → effort surestimé ; δ < 1,75 → effort sous-estimé | [B1 §1.6][B3] |
| Utilisation | s ≤ 0,75 à 0,80·h0 ; jamais au-delà de la position à plat | [B1 §1.7] |
| Statique | \|σOM\| à plat ≤ Rm (≈ 1600 MPa pour l'acier) ; groupe 3 : σ'OM | [B1 §2.1] |
| Dynamique | précharge s1 ≥ 0,15–0,20·h0 ; σu/σo du point décisif (II ou III) à comparer au diagramme de fatigue du groupe | [B1 §2.2] |
| Empilage | L0 ≤ 3·De ; ≤ 2–3 en parallèle ; frottement calculé si la série DIN est connue | [B1 §6.1, §6.5] |
| Guidage | jeu selon le tableau DIN 2093 ; guide ≥ 55 HRC en dynamique | [B1 §6.3–6.4] |

**Fatigue** : le calculateur donne σu, σo et σh, mais **pas de verdict**.
Dire à l'utilisateur de lire le diagramme de son groupe (EN 16984, manuels Schnorr ou Mubea) ou de demander la durée de vie au fabricant.
Ne jamais conclure « tient en fatigue » sans ce diagramme.

## 4. Présenter le résultat
1. Hypothèses (matériau, E, Rm, série et groupe) et données d'entrée.
2. Définition : rondelle De × Di × t (t'), l0, montage (i en série × n en parallèle), L0 de l'empilage, nombre de rondelles, guidage et jeu.
3. Tableau effort-longueur aux points de fonctionnement, avec la plage de frottement en charge et en décharge si disponible.
4. Vérifications du §3, avec les marges.
5. Limites : fatigue non conclue sans diagramme, catalogue partiel, validation par essai pour une pièce de sécurité.

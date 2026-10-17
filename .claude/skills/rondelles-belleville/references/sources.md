# Sources vérifiées — rondelles Belleville (consultées le 17/10/2026)

Les normes EN 16983 et EN 16984 sont payantes. Le calcul est repris du manuel Schnorr, qui reproduit les formules de DIN 2092 (devenue EN 16984).
Il a été validé sur des valeurs publiées indépendantes (SPIROL). Les copies non autorisées de normes ont été écartées.

| # | Source | Ce qui a été vérifié |
|---|---|---|
| B1 | Schnorr, *Disc Springs handy for use* (manuel, 151 p.) — http://www2.schnorr-group.com/uploads/media/handbuch_en.pdf | Formules 1 à 25 : D0, K1–K4, effort, contraintes OM/I/II/III/IV, raideur, travail ; groupes 1/2/3 ; rondelles à épaisseur réduite t' ; matériaux spéciaux (1 − µ² = 0,91) ; domaine de validité ; utilisation ≈ 75–80 % de h0 ; limite statique |σOM| ≤ Rm ≈ 1600 MPa ; durée de vie (≥ 2·10⁶ cycles / 10⁴–2·10⁶) ; point II ou III décisif ; précharge 0,15–0,20·h0 ; empilages série/parallèle ; L0 ≤ 3·De ; ≤ 2–3 en parallèle ; jeu de guidage (DIN 2093) ; guide ≥ 55 HRC ; coefficients wM/wR (DIN 2092) et tableau d'écarts d'effort ; exemples 2 et 3 |
| B2 | SPIROL, *Disc Spring Design Guide* — https://www.spirol.com/assets/files/dsc-disc-spring-design-guide-us.pdf | Tableaux des rondelles DIN EN 16983 séries A/B/C (De, Di, t, l0, h0), efforts et contraintes « calculés selon DIN EN 16984 (ex-DIN 2092) » avec E = 206 kMPa et µ = 0,3. Utilisé comme catalogue et comme jeu de test |
| B3 | Mubea, *Disc Springs Manual* — https://mubea-discsprings.com/wp-content/uploads/2019/08/mubea-disc-springs-manual.pdf | Recoupement : surfaces d'appui (même effort à 0,75·h0), surestimation de l'effort si De/t ≫ 40, sous-estimation si De/Di < 1,8, efforts mini au déchargement (tab. 4.3) |
| B4 | Catalogue iTeh EN 16983:2016 — https://standards.iteh.ai/catalog/standards/cen/b7855c03-8bcf-4690-a9d6-02037519f1c9/en-16983-2016 | EN 16983 : qualité et dimensions, 3 groupes et 3 séries |
| B5 | Schnorr, page « Disc springs » — https://www.schnorr-group.com/en/expertise-technologies/disc-springs | DIN 2092/2093 remplacées au 01/02/2017 par DIN EN 16984 (calcul) et DIN EN 16983 (qualité, dimensions) |

## Tests de non-régression (`scripts/test_belleville.py`) : 61/61
| Cas | Référence | Résultats publiés retrouvés |
|---|---|---|
| 60 × 30,5 × 1,5, l0 = 3,5 | B1 ex. 2 | K1/K2/K3 = 0,688/1,212/1,365 ; σOM = −1048 MPa ; F = 1338/2058/2367/2469 N |
| 200 × 82 × 12, t' = 11,5, l0 = 16,6 (groupe 3) | B1 ex. 3 | K4 = 1,05374 ; σOM = −1579 MPa, σ'OM = −1595 MPa ; F = 66 924…235 503 N ; σII = 416…2011 MPa |
| 40 × 20,4 × 2,25 (A), 40 × 20,4 × 1 (C), 100 × 51 × 3,5 (B), 63 × 31 × 3,5 (A) | B2 | F, σII, σIII, σOM à 1 % près |
| Frottement série A, n = 1 à 3 | B1 §6.5 | Écarts +3,09…+12,36 % et −2,91…−9,91 % retrouvés avec F_R = n·F/(1 ∓ wM(n − 1) ∓ wR) |

## Ce qui n'est PAS vérifié ou PAS intégré
- **Diagrammes de fatigue** (EN 16984, Schnorr fig. 18–20) : non exploitables sous forme numérique dans les sources consultées (graphiques). Le calculateur donne σu, σo et σh aux points II et III, mais **pas de verdict de fatigue**.
- **Formule 26 (frottement)** : illisible dans la conversion du PDF. La forme F_R = n·F/(1 ∓ wM(n − 1) ∓ wR) est retenue parce qu'elle reproduit exactement le tableau chiffré de B1. Ce n'est pas une lecture directe de la formule.
- **Formule 25 (longueur d'un empilage mixte)** : illisible. Le calculateur utilise L0 = i·(l0 + (n − 1)·t'), combinaison directe des formules 19 (série) et 22 (parallèle) de B1.
- **Définition chiffrée des séries A/B/C** : non trouvée en texte. Les rapports typiques (A : h0/t ≈ 0,34–0,43, De/t ≈ 16–18,7 ; B : h0/t ≈ 0,70–0,85, De/t ≈ 25–30 ; C : h0/t ≈ 1,27–1,31, De/t ≈ 35–40) sont **observés** dans le tableau B2, ce ne sont pas des définitions normatives.
- **Catalogue intégré** : seulement les rondelles A/B/C de t ≤ 6 mm repérées par leur série dans B2 (liste partielle d'EN 16983). Le tableau B2 contient quelques coquilles (lignes en double incohérentes) : seules les dimensions ont été reprises.
- **t'/t des rondelles du groupe 3** : B1 donne des facteurs moyens 0,94 (A, B) et 0,96 (C) ; B3 donne 0,938 (A, B), et un chiffre illisible pour C. Le calculateur exige t' en entrée (tableau EN 16983 ou fabricant).
- Matériaux autres que l'acier à ressort, température, corrosion, tolérances EN 16983 : non intégrés au calcul.

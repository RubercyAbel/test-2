# 02 — Base de certification préliminaire (porte PAX, CS-25)

> **Avertissement.** Ce document est une liste de travail, pas la base de certification. Celle-ci est fixée par le responsable navigabilité et l'autorité : amendement applicable (règle du produit modifié, 21.A.101), CRI, conditions spéciales, niveaux de sécurité équivalents. Les titres et le contenu des paragraphes sont à vérifier sur l'amendement applicable. En cas de validation FAA, les paragraphes 14 CFR Part 25 de même numéro s'appliquent.

## 1. Moyens de conformité (codes EASA)

| Code | Moyen |
|---|---|
| MC0 | Déclaration de conformité, référence aux documents de définition |
| MC1 | Revue de conception |
| MC2 | Calcul, analyse |
| MC3 | Analyse de sécurité |
| MC4 | Essais en laboratoire |
| MC5 | Essais au sol sur avion |
| MC6 | Essais en vol |
| MC7 | Inspection de conception, audit |
| MC8 | Simulation |
| MC9 | Qualification d'équipement |

## 2. Paragraphes applicables

Colonne « Agents » : agents qui **contribuent aux preuves** (numérotation de l'architecture cible). La constatation de conformité reste humaine.

| Paragraphe | Objet | Implication pour la porte | MoC envisagés | Agents | Responsable humain |
|---|---|---|---|---|---|
| 25.301, 25.303, 25.305, 25.307 | Charges limites et extrêmes, facteur de sécurité 1,5, résistance et déformation, preuve de la structure | Toutes les pièces structurales | MC2, MC4 si méthode non validée | A6, A7, A8, A10 | Ingénieur calcul, CVE |
| 25.365 | Compartiments pressurisés | Charge dimensionnante. (d) : différentiel maximal de la soupape × 1,33 jusqu'à 45 000 ft, × 1,67 au-delà, sans autres charges. Combinaison avec les charges de vol. (e) : décompression brutale | MC2, MC4 | A6, A7, A8 | Ingénieur calcul |
| 25.561 | Atterrissage d'urgence | Tenue des mécanismes, de l'escalier et des équipements sous facteurs d'inertie | MC2 | A6, A7 | Ingénieur calcul |
| 25.571 | Fatigue et tolérance aux dommages | Cycles de pressurisation ; identification des éléments structuraux principaux (charnières, verrous, encadrement) | MC2, MC4 | A9 (phase 4) | Ingénieur fatigue |
| 25.603, 25.605, 25.609 | Matériaux, procédés de fabrication, protection | Choix des matériaux et procédés, protection contre la corrosion | MC0, MC1 | A5 | Ingénieur matériaux |
| 25.613 | Propriétés et valeurs de calcul des matériaux | Valeurs base A ou B selon la redondance du chemin d'efforts | MC2 | A5, A7, A10 | Ingénieur calcul |
| 25.619, 25.621, 25.623, 25.625 | Facteurs spéciaux : fonderie, matage, ferrures | Facteur de ferrure 1,15 sur les ferrures ; facteurs de matage sur les articulations | MC2 | A7, A10 | Ingénieur calcul |
| 25.783 | Portes de fuselage | Cœur du sujet. (a) dispositions générales, (b) ouverture par des personnes, (c) moyen de prévention de pressurisation, (d) verrouillage et blocage, (e) alerte et indication, (f) inspection visuelle, (g) portes de maintenance et issues amovibles, (h) portes ne présentant pas de danger | MC1, MC2, MC3, MC4, MC5, MC6 | A2, A3, A11 (traçabilité, revue de conception) | Resp. navigabilité, ingénieur systèmes |
| 25.807 à 25.813 | Issues de secours : types, agencement, moyens d'évacuation, marquage, éclairage, accès | Si la porte compte comme issue (H4) : manœuvre simple et évidente, ouverture de l'intérieur et de l'extérieur, risque de coincement après déformation du fuselage, efforts de manœuvre | MC1, MC4, MC5 | A2, A11 (hors pilote) | Resp. navigabilité |
| 25.1309 | Systèmes et équipements | Indication de porte, motorisation éventuelle | MC3 | Hors pilote | Ingénieur systèmes |
| 25.581, 25.899 | Foudre, métallisation | Continuité électrique porte, charnières, fuselage | MC1, MC2 | Interface | Ingénieur électrique |

Documents d'accompagnement à exploiter : AMC 25.783 et les AMC des paragraphes ci-dessus.

## 3. Points ouverts

| ID | Question | Responsable |
|---|---|---|
| B1 | Amendement CS-25 applicable et conditions spéciales éventuelles | Resp. navigabilité |
| B2 | Altitude maximale d'exploitation (facteur 1,33 ou 1,67) | Resp. de projet |
| B3 | La porte compte-t-elle comme issue de secours, et de quel type ? | Resp. navigabilité |
| B4 | Architecture plug ou non-plug | Resp. de projet, ingénieur calcul |
| B5 | Méthodes de calcul déjà validées dans le DOA (et donc utilisables en MC2 sans essai) | Ingénieur calcul |

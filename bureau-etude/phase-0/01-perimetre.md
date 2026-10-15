# 01 — Note de cadrage : périmètre

## 1. Objet

Concevoir, dessiner et justifier la porte passagers principale d'un jet d'affaires pressurisé, avec un bureau d'étude agentique opérant sous les procédures de l'organisme de conception (DOA).

## 2. Décomposition produit

| Sous-ensemble | Contenu type | Remarques |
|---|---|---|
| Structure de porte | Revêtement, cadres, poutres de bord, intercostales, raidisseurs | Chargée en pression ; architecture plug ou non-plug (H2) |
| Ferrures | Charnières (ferrures et bras), butées (porte plug) ou reprises de verrous (porte non-plug), ferrures de verrou | Pièces critiques ; facteur de ferrure 1,15 (CS 25.625) |
| Mécanismes | Poignées intérieure et extérieure, timonerie, verrous et crochets, ressorts ou vérins d'assistance, amortisseur, arrêt d'ouverture | Cœur des exigences 25.783 (verrouillage, prévention d'ouverture en vol) |
| Escalier intégré | Marches, bras ou câbles de soutien, main courante | Seulement si porte-escalier |
| Étanchéité et garnitures | Joints, habillage intérieur | |
| Indication et commande | Capteurs de position, câblage, éventuelle assistance motorisée | Relève de 25.1309 (systèmes) |
| Encadrement fuselage | Cadre d'entourage, doublures, seuil | Interface ; souvent un lot séparé |

## 3. Périmètre du pilote

Le pilote doit être assez riche pour être représentatif, mais limité aux activités où l'on sait mesurer la justesse du résultat.

**Inclus**

- Structure de porte et ferrures : géométrie 3D, plans de définition, justification statique.
- Pièces de timonerie mécanique : géométrie et résistance (pas la fonction de verrouillage).
- Cas de charge : pression (25.365), manœuvre et abus sur poignée, inertie en atterrissage d'urgence (25.561), vent au sol porte ouverte.
- Justification statique analytique et par éléments finis, puis pré-vérification par l'agent vérificateur.
- Matrice de traçabilité exigences vers preuves, pour la partie structure.

**Exclus du pilote** (traités de façon classique ; seules les interfaces sont gérées)

| Exclu | Raison | Phase prévue |
|---|---|---|
| Fatigue et tolérance aux dommages (25.571) | Méthodes et données plus lourdes ; à ajouter une fois la statique fiabilisée | Phase 4 |
| Analyse de sécurité de la fonction verrouillage et indication (25.783, 25.1309) | Jugement d'ingénierie système ; l'IA peut assister la rédaction mais pas mener l'analyse | Hors système, assistance documentaire en phase 4 |
| Système d'indication, câblage, électronique | Autre discipline et autres normes | Hors périmètre |
| Escalier, joints, garnitures | Réduire le pilote | Phase 4 ou au-delà |
| Encadrement fuselage | Lot séparé ; on reçoit les efforts d'interface | Interface seulement |
| Essais (MC4, MC5, MC6) | Planifiés et menés par des humains ; l'IA peut préparer les plans d'essai | Hors système |

## 4. Livrables attendus du système en pilote

1. Modèles CATIA V5 : pièces et assemblage de la porte, conformes à la norme de modélisation.
2. Plans de définition des pièces du périmètre.
3. Dossier de cas de charge, avec sources et hypothèses.
4. Notes de calcul statique (analytique et éléments finis), sur le gabarit du DOA.
5. Rapport de pré-vérification de l'agent vérificateur.
6. Matrice de traçabilité exigences vers preuves (structure).
7. Registre des hypothèses, avec le statut de validation humaine de chacune.

## 5. Mode ombre

Pendant le pilote, le processus classique reste la référence. Le système agentique produit les mêmes livrables **en parallèle**, et on compare. Aucun livrable agentique n'entre dans un dossier de conformité avant la clôture de la phase 5.

## 6. Critères de succès du pilote

Valeurs proposées, à ajuster :

| Critère | Cible proposée | Mesure |
|---|---|---|
| Traçabilité | 100 % des valeurs numériques reliées à une source avec révision | Contrôle automatique |
| Justesse | Écart de marge ≤ 5 % (ou de même signe et même mode de rupture) avec le dossier de référence | Comparaison sur jeu de référence |
| Détection d'erreurs | ≥ 95 % des erreurs injectées de criticité haute détectées par l'agent vérificateur | Protocole d'injection, voir [07](07-independance-verification.md) |
| Conformité des modèles | 0 écart bloquant à la norme de modélisation CATIA | Contrôle de l'agent qualité + revue humaine |
| Effort humain | Temps de vérification humaine par pièce comparé au processus classique | Relevé de temps |
| Coût | Tokens et coût par pièce justifiée | Panneau de consommation |

## 7. Jeu de référence

À constituer en phase 1 : au moins trois pièces déjà justifiées et validées, de complexité croissante (par exemple une ferrure de charnière, une butée ou une reprise de verrou, un cadre de porte), avec leurs notes de calcul approuvées.

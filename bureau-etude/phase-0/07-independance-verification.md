# 07 — Indépendance de la vérification

## 1. Le problème

Le Part 21 (AMC 21.A.239(a)) exige une fonction de vérification indépendante : le vérificateur de conformité (CVE) ne doit pas être l'auteur des données qu'il vérifie. Or le producteur et le vérificateur partagent les mêmes méthodes validées et souvent les mêmes hypothèses. Avec des agents, s'ajoute un mode commun supplémentaire : même modèle d'IA, mêmes données, mêmes scripts.

## 2. Ce que l'indépendance veut dire

Partager des **méthodes approuvées** est normal : c'est même ce que le DOA exige. L'indépendance ne consiste pas à tout refaire autrement. Elle consiste à ce que le vérificateur :

1. **vérifie les hypothèses au lieu de les recevoir** ;
2. n'hérite pas du raisonnement du producteur ;
3. dispose d'au moins un contrôle par un chemin différent sur les résultats critiques ;
4. soit **mesuré** : son taux de détection est connu.

## 3. Six niveaux d'indépendance

| Niveau | Partagé (autorisé) | Non partagé | Mécanisme |
|---|---|---|---|
| Organisationnel | — | Auteur et vérificateur | Agent A10 distinct ; CVE humain non auteur |
| Informationnel | Livrables, documents sources | Raisonnement, brouillons et contexte du producteur | A10 démarre avec un contexte vierge et ne lit que le livrable et les sources |
| Hypothèses | Le registre des hypothèses **comme objet à vérifier** | Les hypothèses comme données d'entrée acquises | Ré-extraction en aveugle des entrées depuis les sources, puis comparaison automatique |
| Méthode | Méthodes validées du DOA | — | Pour les marges critiques, un contrôle par un autre chemin : analytique contre éléments finis, équilibre global, ordre de grandeur |
| Implémentation | Scripts validés | — | Scripts validés une fois sur cas de référence ; pour les méthodes les plus critiques, une seconde implémentation indépendante, testée sur les mêmes cas |
| Modèle d'IA | — | Même modèle et même consigne | Vérificateur sur un modèle différent du producteur, avec une consigne de recherche d'erreurs et une checklist |

## 4. Ré-extraction en aveugle des entrées

C'est la parade la plus efficace contre les hypothèses partagées.

1. A10 reçoit la géométrie, la spécification, les documents de charges et la base de certification, **mais pas** le registre des hypothèses du producteur.
2. A10 reconstitue lui-même la liste des entrées : charges, facteurs, matériaux, valeurs admissibles, conditions aux limites.
3. Un script compare les deux listes ; chaque divergence devient un point à trancher par l'IC.

Ce qui reste commun après cette étape, ce sont les sources elles-mêmes. Elles sont protégées par la double saisie et la révision tracée (risque R9).

## 5. Ce que vérifie A10 sur chaque note de calcul

- Application de la méthode dans son domaine de validité.
- Unités et cohérence dimensionnelle.
- Équilibre global du modèle éléments finis (somme des réactions égale aux charges appliquées).
- Convergence du maillage sur les zones critiques.
- Facteurs appliqués : 1,5, facteur de ferrure 1,15, facteur de pression 1,33 ou 1,67, base A ou B.
- Mode de rupture identifié et cohérent avec la géométrie.
- Recalcul des marges critiques par un autre chemin.

## 6. Mesurer l'indépendance : injection d'erreurs

Sans mesure, l'indépendance reste déclarative.

1. Constituer un catalogue d'erreurs réalistes : mauvais facteur, unité, valeur admissible de mauvaise base, condition aux limites trop rigide, cas de charge oublié, épaisseur mal reportée.
2. Injecter régulièrement ces erreurs dans des dossiers du jeu de référence, à l'insu du vérificateur.
3. Mesurer le taux de détection par catégorie. Cible proposée : ≥ 95 % pour la criticité haute.
4. Toute catégorie mal détectée entraîne une action : contrôle automatique, ajout à la checklist, ou changement de méthode.

## 7. Rôle du CVE humain

- A10 est une **pré-vérification**. Le CVE humain reste la fonction indépendante au sens du Part 21 et signe.
- Le CVE fait ses contrôles en aveugle **avant** de lire le rapport de A10, sur les marges critiques et sur un échantillon tiré au hasard.
- Le CVE relit ensuite le rapport A10 et l'utilise comme liste de points complémentaires.
- Le taux de détection de A10 et celui du CVE sont suivis séparément, pour détecter une dérive vers la confiance aveugle.

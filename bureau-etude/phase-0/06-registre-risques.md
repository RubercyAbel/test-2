# 06 — Registre des risques du bureau d'étude agentique

Gravité (G) et probabilité (P) de 1 (faible) à 4 (forte), avant parade.

| ID | Risque | Effet | G | P | Parade | Resp. |
|---|---|---|---|---|---|---|
| R1 | Valeur inventée par un agent (valeur admissible, facteur, propriété) | Marge fausse, non conservative | 4 | 3 | Valeurs lues uniquement dans des fichiers de référence ; contrôle automatique rejetant toute valeur sans source ; vérification indépendante | IC |
| R2 | Erreur de mode commun entre producteur et vérificateur | Erreur non détectée | 4 | 3 | Indépendance informationnelle, méthodologique et d'implémentation ; injection d'erreurs ([07](07-independance-verification.md)) | CVE |
| R3 | Limites du module éléments finis de CATIA V5 : contacts (verrous, butées), non-linéarités, précharges | Résultats non représentatifs du chemin d'efforts réel | 4 | 3 | Choix du solveur tranché en phase 1 ; en pilote, éléments finis linéaires avec conditions aux limites validées par l'IC et corrélées à l'analytique | IC |
| R4 | Erreur silencieuse du MCP CATIA (opération partielle, mise à jour non faite, géométrie corrompue) | Modèle faux transmis aux plans et au calcul | 3 | 3 | Macro-outils idempotents ; contrôles automatiques après chaque opération (mise à jour, masse, interférences, paramètres) | CC |
| R5 | Fuite de données (client, contrôle des exportations) | Juridique, commercial | 4 | 2 | Charte § 6 ; validation juridique et informatique préalable | RP |
| R6 | Biais d'automatisation des ingénieurs | Vérification humaine de façade | 4 | 3 | Contrôles en aveugle obligatoires ; formation ; mesure du taux de détection | CVE |
| R7 | Dérive non maîtrisée des skills, prompts ou scripts | Comportement modifié sans revue | 3 | 3 | Gestion de configuration, revue avant fusion, tests de non-régression | RQ |
| R8 | Changement de version du modèle d'IA | Comportement différent sur les mêmes entrées | 3 | 3 | Version figée ; jeu de référence rejoué avant tout changement | IC |
| R9 | Erreur de saisie dans les données de référence (base matériaux, fixations) | Erreur reproduite partout, y compris chez le vérificateur | 4 | 2 | Double saisie indépendante à la création ; vérification humaine ; révision tracée | IC |
| R10 | Mauvaise hypothèse d'architecture (plug ou non-plug, redondance des verrous) | Refonte tardive | 3 | 2 | Gate G1 | RP |
| R11 | Non-acceptation par l'autorité | Pas de crédit de certification | 3 | 2 | Mode ombre ; intégration dans les procédures DOA ; dialogue anticipé | OoA |
| R12 | Coût en tokens et délais incompatibles avec l'activité | Rentabilité | 2 | 2 | Skills, scripts, choix du modèle par tâche ; mesure par pièce | RP |

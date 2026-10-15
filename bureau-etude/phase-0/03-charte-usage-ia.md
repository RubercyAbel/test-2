# 03 — Charte d'usage de l'IA au bureau d'étude

## 1. Statut des agents

Les agents sont des **outils** au sens des procédures du DOA, au même titre qu'un logiciel de calcul. La responsabilité technique et réglementaire reste entièrement aux personnes désignées dans le [RACI](04-raci.md).

## 2. Ce que les agents font

- Produire des **projets** : modèles 3D, plans, cas de charge, calculs, notes, matrices de traçabilité.
- Pré-vérifier les livrables d'autres agents et signaler les écarts.
- Tenir à jour les fichiers du dossier projet et la traçabilité.

## 3. Ce que les agents ne font jamais

1. Signer, approuver, libérer un document, ou déclarer une conformité.
2. Utiliser une valeur numérique (valeur admissible, facteur, propriété, charge) **sans source référencée** dans un document maîtrisé. Aucune valeur ne vient de la mémoire du modèle.
3. Modifier une donnée de référence (base matériaux, facteurs, méthodes) hors d'une demande de modification approuvée.
4. Trancher une **hypothèse de jugement** (chemin d'efforts, conditions aux limites, engagement des verrous, redondance) sans validation humaine enregistrée.
5. Franchir un gate ([05](05-gates.md)) sans approbation humaine enregistrée.
6. Communiquer avec l'extérieur (client, autorité, fournisseur).
7. Appliquer une méthode hors de son domaine de validité : l'agent s'arrête et escalade.

## 4. Traçabilité

- Chaque valeur porte : identifiant de la source, révision, page ou tableau.
- Chaque hypothèse est inscrite au registre des hypothèses : identifiant, énoncé, justification, auteur, statut de validation humaine.
- Chaque livrable indique la version du système qui l'a produit (version du dépôt, des skills et des scripts, modèle utilisé).
- Les journaux de session sont conservés selon les exigences d'archivage applicables au DOA (Part 21).

## 5. Mode ombre

Jusqu'à la clôture de la phase 5 (vérification et validation du système), les livrables agentiques sont produits en parallèle du processus classique et **ne constituent pas des preuves de conformité**.

## 6. Données et confidentialité

À valider par le juridique et l'informatique **avant tout envoi de données projet** :

- Classification des données : propriété du client, accords de confidentialité, contrôle des exportations (règlement UE 2021/821 sur les biens à double usage ; réglementations américaines si des données d'origine américaine sont concernées).
- Conditions contractuelles du fournisseur d'IA : conservation des données, localisation, usage pour l'entraînement.
- Liste des environnements autorisés par niveau de classification.
- Aucune donnée classée dans un environnement non approuvé.

## 7. Maîtrise de configuration du système agentique

Les agents, skills, scripts et données de référence sont des **éléments maîtrisés** :

- Versionnés dans Git ; toute modification passe par une revue avant fusion.
- Un script de calcul n'est utilisable qu'après validation sur des cas de référence (tests automatiques).
- Tout changement de version du modèle d'IA impose de rejouer le jeu de référence avant utilisation.

## 8. Anomalies

- Tout écart, erreur ou comportement inattendu est inscrit au registre des anomalies.
- Chaque anomalie de criticité haute fait l'objet d'une analyse des causes et d'une action corrective (script, skill, donnée ou règle).

## 9. Biais d'automatisation

- Les ingénieurs sont formés aux modes de défaillance des agents.
- Le vérificateur humain (CVE) fait des contrôles « en aveugle » sur un échantillon, sans regarder d'abord la conclusion de l'agent vérificateur (voir [07](07-independance-verification.md)).

## 10. Revue de la charte

Revue à chaque fin de phase et après toute anomalie de criticité haute.

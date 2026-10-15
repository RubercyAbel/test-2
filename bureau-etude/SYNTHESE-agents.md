# Synthèse de l'architecture agentique — bureau d'étude porte PAX

**Statut :** révision A, 2026-10-16. Document de travail, à valider par le responsable de projet.
**Périmètre :** porte passagers de jet d'affaires (phase 0 : `phase-0/`).
**Principe directeur :** aucun agent ne décide ni ne signe. Chaque valeur porte sa source. La vérification est indépendante et mesurée.

---

## 1. Vue d'ensemble : 19 agents en 5 familles

| Famille | Agents |
|---|---|
| **Pilotage** | A1 Orchestrateur · A2 Exigences et certification |
| **Conception** | A3 Concepteur structure · A4 Concepteur mécanisme · A5 Analyste tolérancement |
| **Production numérique** | A6 CAO 3D et 2D · A18 Outillage 3D (bâti d'assemblage) · A19 Conception d'essai (bâti d'essai) |
| **Ingénierie** | A7 Matériaux et procédés · A8 Charges · A9 Calcul analytique · A10 Éléments finis · A11 Fatigue et dommages · A15 AMDEC et fabricabilité · A17 Méthodes (gamme et montabilité) |
| **Assurance et documentation** | A12 Vérificateur calcul · A13 Conformité réglementaire · A14 Qualité et configuration · A16 Rédaction |

### Modèle par agent

| Modèle | Agents | Raison |
|---|---|---|
| Opus | A1, A2, A4, A9, A11, A12, A13 | Raisonnement, arbitrage, vérification |
| Sonnet | A3, A5, A6, A7, A8, A10, A15, A17, A18, A19 | Exécution encadrée par des scripts et des données |
| Haiku | A14, A16 | Mise en forme, contrôles mécaniques |

### Trois règles de structure

1. **Un agent décide, un autre exécute.** Les concepteurs (A3, A4) décident de la forme et du fonctionnement. A6 traduit en CAO. A5 et A17 contrôlent la cohérence du point de vue fonctionnel et de la fabrication.
2. **L'indépendance se démontre.** A12 ne reçoit ni le raisonnement du producteur ni ses hypothèses. Il ré-extrait les entrées depuis les sources. Le CVE humain signe (voir `phase-0/07-independance-verification.md`).
3. **Les calculs sont des scripts, pas du raisonnement.** Les agents appellent des fonctions testées et lisent des fichiers de référence sourcés.

### Communication entre agents

Pas de conversation libre. Les échanges passent par des fichiers versionnés :
- **Document d'interface** entre concepteurs : enveloppes réservées, points d'attache, efforts.
- **Demande de modification d'interface chiffrée** : « +8 mm ici ; impact masse +40 g ; marge nervure 0,35 → 0,22 ».
- **Registre des décisions**, arbitré par A1 selon l'ordre sécurité et conformité, puis fonction, puis masse, puis coût. Au bout de trois tours sans accord, la décision remonte à un humain.

---

## 2. Documents par agent

Pour chaque agent : **entrées** (ce qu'il lit), **sorties** (ce qu'il produit), et **lacunes** relevées dans le bilan du projet local.

### A1 — Orchestrateur

- **Entrées :** `phase-0/` (README, gates, RACI), registre des hypothèses, registre des décisions, état du projet.
- **Sorties :** `etat_projet.yaml`, plan de tâches, demandes de gate (`gates/Gx.yaml`, à signer par un humain), registre des décisions.
- **Ne fait pas :** signer, franchir un gate, trancher une hypothèse de jugement.

### A2 — Exigences et certification

- **Entrées :** fiches CS-25 (amendement confirmé), AC et AMC associés, base de certification ou CRI, fiches de certification des portes (`AC_25.783-1A`), spécification client.
- **Sorties :** `exigences.yaml` (identifiant, texte source, paragraphe, moyen de conformité), matrice des moyens de conformité, base de certification préliminaire (`phase-0/02`).
- **Lacunes :** amendement CS-25 à confirmer (la proposition d'août 2026 n'est pas vérifiée), ASSIST non consulté.

### A3 — Concepteur structure

- **Entrées :** exigences (A2), charges (A8), fiches structure (nervures, cadres, poutres de bord, ferrures), manuel de conception du DOA, document d'interface.
- **Sorties :** squelette structure (points, axes, enveloppes, paramètres nommés), chemin d'efforts, demandes d'interface.
- **Lacunes :** le manuel de conception interne n'est pas référencé dans les fiches.

### A4 — Concepteur mécanisme

- **Entrées :** exigences fonctionnelles, CS 25.783 (verrouillage, prévention d'ouverture), fiches mécanisme (bielles réglables et non réglables, bielle à ressort, came et galet, point mort, crochet de verrou), document d'interface.
- **Sorties :** schéma cinématique, squelette cinématique (points, axes, courses), loi entrée-sortie, efforts de manœuvre, demandes d'interface.

### A5 — Analyste tolérancement

- **Entrées :** spécification GPS ou plan de tolérancement, normes ISO 1101, ISO 8015, ISO 5459 (ou ASME Y14.5 si applicable), ISO 286 pour les ajustements, séquence d'assemblage (depuis A17), squelettes (A3, A4), fiches chaînes de cotes.
- **Sorties :** spécification GPS (cadres de tolérance, référentiels), chaînes de cotes (résultats de script : pire cas, quadratique, Monte-Carlo), analyse de réglage, demandes de tolérance.
- **Lacunes :** GPS non exposé par le MCP ; licence GPS non vérifiée.

### A6 — CAO 3D et 2D

- **Entrées :** squelettes, paramètres, norme de modélisation CATIA interne, gabarits paramétriques, spécification GPS, norme de dessin (ISO 128, ISO 129-1, ISO 5455), catalogue de pièces standard (NAS, EN, ASNA).
- **Sorties :** modèles CATPart et CATProduct, plans (CATDrawing), nomenclature, journal de publication, rapports de contrôle du MCP (`controles`, `avertissements`).
- **Lacunes :** pas d'outil de mise en plan dans le MCP ; licence Drawing non vérifiée ; export STEP non vérifié.

### A7 — Matériaux et procédés

- **Entrées :** MMPDS (en vigueur), CMH-17 (composites), spécifications de procédés (AMS et équivalents), fiches matériaux et admissibles (20 fiches), fiches protections (10 fiches).
- **Sorties :** fiche matériau et procédé par pièce, valeurs admissibles sourcées (base A ou B), spécification de protection.
- **Lacunes :** MIL-HDBK-5J annulé et remplacé par MMPDS ; MIL-DTL-5541F téléchargée mais la synthèse dit qu'elle est absente (contradiction à corriger).

### A8 — Charges

- **Entrées :** CS 25.301 à 25.305, 25.365 (pression, facteurs 1,33 ou 1,67 selon l'altitude), 25.561 (atterrissage d'urgence), 25.571 (cycles), enveloppe de vol, documents de charges client.
- **Sorties :** `cas_charge.yaml` (cas, valeurs, source de chaque valeur), facteurs appliqués, enveloppe de charges.
- **Lacunes :** altitude maximale d'exploitation (H3) à confirmer ; 1,33 ou 1,67 dépend de cette valeur.

### A9 — Calcul analytique

- **Entrées :** méthodes internes validées (MC-xxx), charges (A8), matériaux (A7), géométrie (A3, A6), `config/facteurs.yaml`, fiches méthodes, scripts testés.
- **Sorties :** résultats JSON (marges), projets de notes de calcul, rapports de test des scripts.
- **Lacunes :** 437 tests annoncés le 08/10, dernier passage non refait ; méthodes internes à valider dans le DOA.

### A10 — Éléments finis

- **Entrées :** géométrie (STEP ou CATPart), guide de modélisation EF interne (types d'éléments, convergence, critères d'acceptation), charges (A8), matériaux (A7), scripts existants (`20_sortie/elements_finis/`).
- **Sorties :** modèle EF, rapport de convergence, contraintes et marges, comparaison avec le calcul analytique (A9).
- **Lacunes :** pas d'outil EF dans le MCP ; solveur à choisir (GSA, Nastran ou Abaqus selon les calculs justificatifs) ; contacts des verrous et butées non traités par le linéaire.

### A11 — Fatigue et dommages (phase 4)

- **Entrées :** CS 25.571, AC 25.571-1, spectres de charge, données de propagation (MMPDS), fiches TCCA (2 fiches), intervalles d'inspection.
- **Sorties :** analyse de fatigue, intervalles d'inspection, données d'entrée pour le programme d'entretien.

### A12 — Vérificateur calcul (CVE calcul)

- **Entrées :** livrables de A9 et A10 (résultats, notes) et **sources uniquement**. Il ne reçoit ni le registre d'hypothèses du producteur ni son raisonnement. Il ré-extrait charges, facteurs et matériaux depuis les sources.
- **Sorties :** rapport de pré-vérification, liste d'écarts, résultats des injections d'erreurs.
- **Règle :** il tourne sur un modèle différent du producteur, et ses contrôles sont mesurés (taux de détection).

### A13 — Conformité réglementaire

- **Entrées :** exigences (A2), dossiers de preuve, matrice de traçabilité, paragraphes CS-25 et AMC, rapports de A12.
- **Sorties :** matrice de conformité, liste des lacunes, projet de déclaration de conformité.
- **Ne fait pas :** constater la conformité. Il prépare les pièces pour le signataire humain.

### A14 — Qualité et configuration

- **Entrées :** procédures du DOA, exigences EN 9100 (§ 8.3), historique Git, registre des anomalies.
- **Sorties :** registre des anomalies, registre des décisions, revue de configuration, contrôle de la numérotation et des indices.

### A15 — AMDEC et fabricabilité

- **Entrées :** fiches AMDEC, FHA, FTA et méthodes de sécurité (5 fiches), taux de défaillance (21 fiches), règles de fabricabilité (usinage, tôlerie, composites), plans (A6).
- **Sorties :** AMDEC de conception, contrôle de fabricabilité par pièce, causes et effets.
- **Lacunes :** FHA sur ARP4761A non possédée ; taux de défaillance sur des éditions anciennes à remettre à jour.

### A16 — Rédaction

- **Entrées :** gabarits (note de calcul, fiche de conformité, rapport de vérification), sorties des autres agents, glossaire, modèle de document du DOA.
- **Sorties :** notes de calcul et documents de conformité en projet, mis en forme. **Ils ne sont pas signés par l'agent.**

### A17 — Méthodes (gamme d'assemblage et montabilité)

- **Entrées :** modèles CAO (A6), catalogue d'outillage et accès, catalogue de fixations (couples de serrage sourcés), procédés d'étanchéité, séquence et référentiels (chaînes de référentiels, avec A5), spécification de montage.
- **Sorties :** gamme d'assemblage (opérations, outils, couples, contrôles), graphe de précédence, rapport de montabilité (collisions, accès aux fixations, passage des outils), documents de gamme, demandes de bâti lorsque le critère est atteint.
- **Lacunes :** collisions et accès ne sont pas exposés par le MCP ; licence Assembly non vérifiée.

### A18 — Outillage 3D (bâti d'assemblage)

- **Entrées :** décision de besoin de bâti (prise par A17 et validée par un humain), principe de localisation (3-2-1), tolérance du bâti, pièce à positionner, catalogue d'outillage standard.
- **Sorties :** modèle 3D du bâti, plan du bâti, analyse de précision du bâti.
- **Ne doit pas partager :** l'agent du bâti d'essai (A19). Un même agent validerait son propre montage de test.

### A19 — Conception d'essai (bâti d'essai)

- **Entrées :** exigences d'essai (MC4 et MC5), normes et paragraphes d'essai (ex. essai de pression), plan d'essai, liste d'instrumentation, fiches essais.
- **Sorties :** plan d'essai, bâti d'essai 3D, procédure d'essai en projet, points de mesure.
- **Lacunes :** aucune fiche d'essai dans la base.

---

## 3. Documents transversaux (tous les agents)

| Document | Rôle | Responsable |
|---|---|---|
| `CLAUDE.md` | Règles absolues, carte du dépôt, commande de test. Court, car il est chargé à chaque session. | A14 |
| Registre des sources | Chaque valeur : identifiant, document, révision, page, statut de validation | A14 |
| Registre des hypothèses | Chaque hypothèse de jugement : énoncé, justification, auteur, validation humaine | A1 |
| Registre des décisions | Arbitrages entre agents, décisions humaines, dates | A1 |
| Registre des anomalies | Erreurs, comportements inattendus, actions correctives | A14 |
| Gates signés | `gates/Gx.yaml` : approbateur, date, décision, réserves | Humains |
| Versions des skills, scripts et modèle | Quel système a produit quel livrable | A14 |

---

## 4. Points bloquants avant tout usage en production

Ces points viennent du bilan du projet local. Ils conditionnent tout ce qui suit.

| # | Blocage | Impact | Action |
|---|---|---|---|
| B1 | **0 fiche sur 86 validée par un humain** | Des valeurs servent déjà à des calculs | Validation nominative des fiches utilisées, avant tout calcul |
| B2 | Contradictions entre fiches et journaux (Notice 2 du 217F, MIL-DTL-5541F, statuts issus d'everyspec et non d'ASSIST) | Erreurs reproduites dans les calculs | Mise à jour et traçage des révisions |
| B3 | Amendement CS-25 non confirmé (Amdt 28 et proposition d'août 2026) | Base de certification fausse possible | Interrogation d'ASSIST, confirmation par l'OoA |
| B4 | Export STEP non vérifié | Échange de géométrie non fiable | Test de l'export sur une pièce du jeu de référence |
| B5 | Licences Drawing, Assembly, GPS, FEA non vérifiées | Agents A5, A6, A10, A17 peuvent être bloqués | Test COM, comme pour les licences déjà vérifiées |
| B6 | 437 tests non relancés | Régression possible du moteur | Passage complet avant la prochaine phase |
| B7 | Fermeture CATIA silencieuse (un `Close` répond OK sans effet) | Blocage de CATIA | Plafond de tentatives à éprouver |
| B8 | Pas de jeu de référence validé | Impossible de mesurer la justesse | Constituer 3 dossiers validés (phase 3 du plan) |

---

## 5. Séquence de déploiement

| Phase | Agents actifs | Sortie attendue |
|---|---|---|
| **Phase 0** (en cours) | Aucun agent. Cadrage et gouvernance. | Documents `phase-0/` signés |
| **Phase 1** : connaissance | Aucun agent. Validation des fiches et des données. | Fiches utilisées validées, B1 à B3 levés |
| **Phase 2** : outils | Aucun agent. Export STEP, licences, tests, macros CATIA. | B4 à B7 levés |
| **Phase 3** : pilote minimal | A1 Orchestrateur, A6 CAO, A9 Calcul, A12 Vérificateur. Gates humains. | Une ferrure de porte traitée de bout en bout, en mode ombre |
| **Phase 4** : élargissement | + A2, A3, A4, A8, A10, A13, A14, A16 | Porte complète, structure et mécanisme |
| **Phase 5** : validation du système | + A5, A7, A15, A17, A18, A19. Mesure du taux de détection. | Clôture du mode ombre si les critères sont tenus |
| **Phase 6** : fatigue et pack automobile | + A11. Puis remplacement des fiches aéro par le pack auto. | Noyau réutilisé |

**Pourquoi le pilote ne contient que quatre agents :** chaque agent ajouté augmente la coordination. Le pilote doit d'abord être fiable sur le calcul, avant d'ajouter des concepteurs et des méthodes.

---

## 6. Décisions attendues

1. **Valider le découpage en 19 agents**, ou décider de fusions (par exemple A18 et A19 en un seul agent outillage, en renonçant à l'indépendance entre bâti de production et bâti d'essai).
2. **Confirmer la base** : CS-25 ou CS-23 (H1), architecture de porte (H2), altitude maximale (H3).
3. **Nommer les titulaires humains** du RACI (`phase-0/04-raci.md`), notamment le CVE.
4. **Lancer la validation des fiches** (B1), qui conditionne tout le reste.

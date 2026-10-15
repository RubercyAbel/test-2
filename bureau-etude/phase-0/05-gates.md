# 05 — Gates humains

Aucun agent ne poursuit au-delà d'un gate sans approbation humaine enregistrée. L'enregistrement prend la forme d'un fichier `gates/Gx.yaml` versionné (nom, rôle, date, décision, réserves). En phase 2, un hook bloquera techniquement le passage si ce fichier est absent.

| Gate | Objet | Entrées produites par les agents | Critères de passage | Approbateur |
|---|---|---|---|---|
| **G0** Lancement | Cadre réglementaire et exigences | Base de certification préliminaire, exigences dérivées, périmètre | Points B1 à B5 tranchés ou assumés ([02](02-base-certification-preliminaire.md)) | OoA + RP |
| **G1** Hypothèses et charges | Architecture et chemin d'efforts | Architecture de porte (plug ou non-plug, nombre et position des verrous et charnières), registre des hypothèses, cas de charge | Chaque hypothèse de jugement validée nominativement ; cas de charge complets et sourcés | IC, revue par CVE |
| **G2** Définition préliminaire | Pré-dimensionnement | 3D préliminaire, pré-dimensionnement analytique, choix matériaux | Marges préliminaires positives ou plan d'action ; faisabilité confirmée | RP + IC + CC |
| **G3** Définition détaillée | Définition figée | 3D détaillée, plans, modèles éléments finis et résultats | Convergence du maillage démontrée ; corrélation analytique et éléments finis ; conformité à la norme de modélisation | IC + CC |
| **G4** Justification vérifiée | Dossier de calcul | Notes de calcul, rapport de pré-vérification A10 | Tous les écarts A10 traités ; contrôles en aveugle du CVE concluants ([07](07-independance-verification.md)) | **CVE** |
| **G5** Libération | Mise en configuration | Plans, dossier de conformité, matrice de traçabilité | Traçabilité complète ; configuration cohérente | RQ + OoA |

En **mode ombre** (pilote), les gates sont tenus sur le dossier classique ; le dossier agentique est comparé à chaque gate et les écarts sont inscrits au registre des anomalies.

# Phase 0 — Cadrage et gouvernance

**Objet :** porte passagers (PAX) de jet d'affaires, conçue et justifiée avec l'assistance d'un bureau d'étude agentique.
**Statut :** brouillon, révision A, 2026-10-15. Aucun de ces documents n'est approuvé tant que les signatures de la section « Approbation » ne sont pas renseignées.

La phase 0 fixe le cadre **avant toute technique** : ce que le système agentique fait, ce qu'il ne fait jamais, qui décide, et comment on prouvera qu'il est fiable.

## Documents

| N° | Document | Contenu | Approbateur |
|---|---|---|---|
| 01 | [Périmètre](01-perimetre.md) | Décomposition de la porte, périmètre du pilote, livrables, critères de succès | Resp. de projet |
| 02 | [Base de certification préliminaire](02-base-certification-preliminaire.md) | Paragraphes CS-25 applicables, moyens de conformité, contribution des agents | Resp. navigabilité |
| 03 | [Charte d'usage de l'IA](03-charte-usage-ia.md) | Règles, interdits, traçabilité, données, mode ombre | Direction technique + Qualité |
| 04 | [RACI](04-raci.md) | Qui réalise, approuve, est consulté, informé | Resp. de projet |
| 05 | [Gates humains](05-gates.md) | Points de décision G0 à G5, entrées, critères, signataires | Resp. de projet + Resp. navigabilité |
| 06 | [Registre des risques](06-registre-risques.md) | Risques propres au bureau d'étude agentique et parades | Resp. de projet |
| 07 | [Indépendance de la vérification](07-independance-verification.md) | Comment garantir que la vérification (agent puis CVE humain) est réellement indépendante | Resp. navigabilité |

## Hypothèses de travail (à confirmer)

| ID | Hypothèse | Pourquoi c'est structurant |
|---|---|---|
| H1 | Base **CS-25**. Si l'avion est dans le champ de CS-23 (≤ 19 passagers et ≤ 8 618 kg), la base change entièrement (CS-23 amendement 5, exigences de performance et normes ASTM). | Toute la checklist de conformité en dépend. |
| H2 | Architecture de porte **non arrêtée** : porte « plug » (efforts de pression repris par des butées) ou porte-escalier ouvrant vers l'extérieur (efforts repris par les verrous), cas fréquent sur jet d'affaires. | Change le chemin d'efforts, les pièces critiques, la modélisation FEA et les exigences 25.783. |
| H3 | Altitude maximale d'exploitation **> 45 000 ft** probable (jet d'affaires). | Facteur de pression 1,67 au lieu de 1,33 (CS 25.365(d)). |
| H4 | La porte est **comptée comme issue de secours**. | Ajoute les exigences 25.807 à 25.813. |
| H5 | Nature du projet **à préciser** : nouvelle définition, modification majeure / STC, ou lot sous-traité sous le DOA d'un avionneur. | Fixe l'amendement applicable (règle du produit modifié, 21.A.101) et qui signe. |
| H6 | Le pilote fonctionne en **mode ombre** : les livrables agentiques ne servent pas de preuve de conformité tant que la phase 5 (V&V du système) n'est pas close. | Permet d'apprendre sans risque réglementaire. |

## Décisions attendues de votre part

1. Confirmer H1 (CS-25 ou CS-23) et H5 (nature du projet, statut DOA).
2. Choisir l'architecture de porte (H2) ou décider qu'elle fait partie de l'étude.
3. Nommer les titulaires des rôles humains du [RACI](04-raci.md).
4. Valider le périmètre du pilote ([01](01-perimetre.md) § 3).
5. Faire valider par le juridique et l'informatique le cadre d'usage des données ([03](03-charte-usage-ia.md) § 6), **avant** d'envoyer des données projet à un service d'IA.

## Entrées à fournir pour la phase 1

- Vos documents de calcul (méthodes internes) avec leurs exemples résolus.
- Un ou plusieurs dossiers de porte ou de ferrures déjà validés (jeu de référence).
- Le manuel DOA et les procédures de conception / vérification.
- La spécification de la porte (ou d'une porte comparable) et les documents de charges.
- La liste des outils exposés par le MCP CATIA V5.
- La norme de modélisation CATIA et la norme de dessin internes.

## Approbation

| Rôle | Nom | Date | Visa |
|---|---|---|---|
| Responsable de projet | [À COMPLÉTER] | | |
| Responsable navigabilité (OoA) | [À COMPLÉTER] | | |
| Responsable qualité | [À COMPLÉTER] | | |

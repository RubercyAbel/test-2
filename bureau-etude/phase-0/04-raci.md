# 04 — Matrice RACI

**R** réalise · **A** approuve (une seule personne, toujours humaine) · **C** consulté · **I** informé.
Règle : un agent peut être **R**, jamais **A**.

## Rôles humains

| Code | Rôle | Titulaire |
|---|---|---|
| RP | Responsable de projet | [À COMPLÉTER] |
| IC | Ingénieur calcul responsable | [À COMPLÉTER] |
| CC | Concepteur CAO référent | [À COMPLÉTER] |
| CVE | Vérificateur de conformité structure, indépendant | [À COMPLÉTER] |
| OoA | Responsable navigabilité (Office of Airworthiness) | [À COMPLÉTER] |
| RQ | Responsable qualité et configuration | [À COMPLÉTER] |

## Agents

A1 orchestrateur · A2 exigences et certification · A3 CAO · A4 mise en plan · A5 matériaux · A6 charges · A7 calcul analytique · A8 éléments finis · A9 fatigue · A10 vérificateur calcul · A11 conformité · A12 qualité et configuration · A13 AMDEC et fabricabilité · A14 rédaction.

Actifs dès le pilote (phase 3) : **A1, A3, A6–A8 (regroupés en un agent calcul), A10**. Les autres arrivent en phase 4.

## Matrice

| Activité | RP | IC | CC | CVE | OoA | RQ | Agents (R) |
|---|---|---|---|---|---|---|---|
| Base de certification et checklist | C | C | I | C | **A** | I | A2 |
| Exigences dérivées de la porte | **A** | C | C | I | C | I | A2 |
| Hypothèses de jugement (chemin d'efforts, conditions aux limites, verrous) | I | **A** | C | C | I | I | A6, A8 proposent |
| Cas de charge | I | **A** | I | C | C | I | A6 |
| Modélisation 3D | I | C | **A** | I | I | C | A3 |
| Plans de définition | I | C | **A** | I | I | C | A4 |
| Matériaux et procédés | I | **A** | C | I | I | I | A5 |
| Calculs analytiques | I | **A** | I | I | I | I | A7 |
| Calculs éléments finis | I | **A** | I | I | I | I | A8 |
| Pré-vérification des calculs | I | I | I | **A** | I | I | A10 |
| Vérification de conformité et visa | I | C | I | **A** (R) | C | I | — |
| Matrice de traçabilité | I | C | I | C | **A** | I | A11 |
| Gestion de configuration, libération | **A** | I | C | I | I | R | A12 |
| Validation des skills, scripts et données de référence | I | **A** | C | C | I | R | — |
| Revue de la charte IA | **A** | C | C | C | C | R | — |

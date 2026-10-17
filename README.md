# test-2

## Ressorts — conception et dimensionnement

- [Fiche de connaissance](docs/fiche-connaissance-ressorts.md) : types, formules (EN 13906), matériaux, démarche, exemple chiffré, erreurs fréquentes.
- Skills Claude (`.claude/skills/`) :
  - `dimensionnement-ressorts` : conception de ressorts de compression, traction et torsion à partir d'un cahier des charges, avec le calculateur `scripts/ressort.py`.
  - `verification-ressort` : audit d'un ressort ou d'un plan existant, et diagnostic de défaillance.
  - `rondelles-belleville` : calcul, sélection et vérification de rondelles Belleville et de leurs empilages (EN 16984), avec le calculateur `scripts/belleville.py` validé sur 61 valeurs publiées.

```bash
python3 .claude/skills/dimensionnement-ressorts/scripts/ressort.py concevoir-compression \
  --F1 20 --L1 40 --F2 60 --L2 30 --De-max 20 --materiau DH
```

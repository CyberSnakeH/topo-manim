# Legacy

Scripts uniques antérieurs conservés pour référence historique.

Les scènes canoniques utilisées par le `Makefile` se trouvent sous `scenes/<chapitre>/` et s'appuient sur les modules réutilisables de `src/`. Les fichiers présents ici sont des prototypes d'une seule pièce, antérieurs à cette architecture deux-couches.

Ces fichiers :

- ne sont **ni testés ni lintés** (exclus de `ruff` et de `pytest`),
- ne sont **pas importés** par le code de production,
- utilisent un style plus simple (`from manim import *`, pas de `from __future__ import annotations`),
- peuvent être rendus à la main avec Manim si besoin (`uv run manim -ql legacy/sin1x.py`).

| Fichier | Sujet |
|---|---|
| `sin1x.py` | Démo simple de la fonction sin(1/x) |
| `sin1x_legacy.py` | Variante très proche, conservée pour comparaison |
| `contre_exemple_sin1x.py` | Esquisse du contre-exemple ; version aboutie : `scenes/01_connexite/contre_exemple_sin1x.py` |
| `definition.py` | Démo sur la connexité par arcs et cercles |
| `homeo.py` | Démo d'homéomorphisme cercle ↔ carré |
| `theo_fonction_continue.py` | Démo sur les espaces connexes et la continuité |

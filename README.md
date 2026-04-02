# topo-manim

Animations Manim pour illustrer le cours de topologie de L3.

Encadrant : Frédéric Le Roux  
Référence principale : *Mémo de topologie*, F. Le Roux / F. Klopp, 2021  
Outil : Manim Community Edition

## Objectif

Le projet construit des scènes courtes et réutilisables pour visualiser des notions abstraites de topologie métrique :

- connexité et connexité par arcs ;
- compacité et recouvrements ouverts ;
- complétude et théorème de Baire.

Le code est organisé en deux couches :

- `src/` contient les briques réutilisables ;
- `scenes/` contient les scènes finales prêtes au rendu.

## Structure

```text
topo-manim/
├── src/
│   ├── animations/
│   ├── objects/
│   └── utils/
├── scenes/
│   ├── 01_connexite/
│   ├── 02_compacite/
│   └── 03_completude/
├── tests/
├── Makefile
├── pyproject.toml
└── README.md
```

## Installation

Le projet utilise `uv` pour gérer l'environnement Python.

```powershell
python -m uv sync
```

## Rendus

Rendre une scène en basse qualité :

```powershell
python -m uv run manim render -ql scenes/01_connexite/connexe_vs_arcs.py ConnexeVsArcs
```

Rendre toutes les scènes via le `Makefile` :

```powershell
make all
```

Scènes actuellement disponibles :

- `ConnexeVsArcs`
- `InvarianceTopologique`
- `ContreExempleSin1x`
- `BorelLebesgue`
- `Baire`

## Vérification

Vérification syntaxique :

```powershell
python -m compileall src scenes tests
```

Tests d'import :

```powershell
python -m uv run pytest
```

## Choix pédagogiques

- Les scènes privilégient les idées structurantes du cours plutôt que des démonstrations intégrales.
- Les énoncés affichés à l'écran sont volontairement courts, mais ils restent mathématiquement corrects.
- Les couleurs sont centralisées dans `src/utils/colors.py` et la configuration Manim dans `src/config.py`.

## Remarques

- Le dossier `media/` contient uniquement des sorties générées ; il ne doit pas être versionné.
- Les scènes sont pensées pour un usage de cours, de TD, ou de support vidéo court.

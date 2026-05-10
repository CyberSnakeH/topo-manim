# Changelog

Tous les changements notables de ce projet sont documentés dans ce fichier.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et le
projet adhère au [versionnage sémantique](https://semver.org/lang/fr/).

---

## `v0.3` — Outillage cross-platform et nettoyage du repo (mai 2026)

### Ajouté
- **`Justfile`** : lanceur de tâches unique pour Linux, macOS et Windows.
  Remplace l'ancien `Makefile` (Linux-only) et `render.ps1` (Windows-only)
  qui se désynchronisaient. La directive `set windows-shell` fait tourner
  les recettes nativement sous PowerShell sans Git Bash ni WSL.
- **Configuration Ruff** dans `pyproject.toml` : `line-length = 100`,
  jeu de règles `E/W/F/I/UP/B/SIM/RUF`, `target-version = "py311"`,
  exclusions sur `legacy/`, `media/`, `videos/`, `references/`.
- **`.editorconfig`** : UTF-8, LF, indentation cohérente (4 espaces Python,
  2 espaces YAML/TOML/JSON, tabs pour le Makefile historique).
- **`legacy/`** : dossier dédié aux 6 scripts mono-fichiers antérieurs à
  l'architecture deux-couches `src/` + `scenes/` (cf.
  [`legacy/README.md`](legacy/README.md)).
- **`CONTRIBUTING.md`** : guide de contribution en français (workflow,
  conventions de nommage, règles de style).
- **`CHANGELOG.md`** : ce fichier, séparé du README pour respecter la
  convention OSS.
- `srt` ajouté en dépendance explicite — Manim 0.20.x l'importe au
  chargement, mais le résolveur peut rater l'install transitive
  (notamment sur Windows / OneDrive).

### Modifié
- **`pyproject.toml`** : `[tool.setuptools.packages.find]` restreint à
  `src*` et `scenes*` (évite que `legacy/` ou `tests/` soient considérés
  comme des paquets installables).
- Application uniforme de `ruff format` + `ruff check --fix` sur `src/` et
  `scenes/` (≈ 884 ins / 441 del, principalement tri des imports et
  reformatage des longues chaînes Manim).
- Cookie `# -*- coding: utf-8 -*-` retiré des 6 fichiers où il subsistait
  (UTF-8 est la valeur par défaut en Python 3, cf. PEP 3120).
- `README.md` réécrit : section Installation en trois étapes claires
  (prérequis système, `uv` + `just`, clone), section Vidéos en tableau
  compact, badge Python aligné sur `>=3.11`, mention des collaborateurs
  (`@QJ1009`, `@solveiggir`, `@walidcr`) en tête de fichier.

### Supprimé
- `Makefile` et `render.ps1` (remplacés par le `Justfile`).
- 6 scripts mono-fichiers de la racine (déplacés vers `legacy/`),
  dont `Theo de fonction continue.py` renommé en
  `theo_fonction_continue.py` (élimination des espaces).
- `Latex/Rapports/` (rapport de stage hors scope du repo d'animations).
- `videos/thumbnails/` (le preview natif de GitHub remplace les
  miniatures).
- Deux placeholders MP4 de 2 octets traînant à la racine et dans
  `videos/`.
- Section *Roadmap* du README (pas activement maintenue).
- Patterns LaTeX du `.gitignore` devenus inutiles.

### Corrigé
- 2 erreurs `F841` (variables locales non utilisées) dans
  `connexe_vs_arcs.py` et `contre_exemple_sin1x.py` (renommées avec un
  préfixe `_` pour indiquer l'usage en effet de bord).
- 6 erreurs `B905` (`zip()` sans `strict=`) en ajoutant `strict=False`
  pour préserver le comportement existant.

---

## `v0.2` — Alignement formel sur le cours (avril 2025)

- **`connexe_vs_arcs.py`** entièrement refondue (220 → 1637 lignes) :
  - Notation alignée sur le cours : $x_0, x_1$ et $O, O'$ partout.
  - Réordonnement des sections selon l'ordre exact du cours
    (caractérisation $\{0,1\}$ avant le théorème, qui en utilise le
    corollaire $[0,1]$ connexe).
  - Définition primaire de la connexité par les **ouverts-fermés** (et non
    par la partition, qui devient une *proposition équivalente*).
  - Ajout de cinq sub-frames visuels pour la **Proposition IV.1** :
    image continue, réunion à point commun, produit fini, concaténation
    $\gamma \star \gamma'$, invariance topologique.
  - Ajout du **corollaire $[0,1]$ est connexe** explicitement encadré à
    la fin de la section 5.
  - Démonstration de `c.p.a. ⟹ connexe` sous forme de **schéma central
    persistant** ($X = O \sqcup O'$ en haut, $[0,1]$ en bas reliés par
    une flèche $\gamma^{-1}$) avec **une seule ligne d'étape** qui se
    transforme.
  - Visualisation explicite de $f^{-1}(\{0\})$ et $f^{-1}(\{1\})$ comme
    sous-régions distinctes de $X$, animées (l'une rétrécit à
    $\varnothing$ quand $X$ est connexe).
  - Théorème de relais § IV.2.(a) corrigé : *complet, connexe,
    localement connexe* (au lieu de *localement connexe par arcs*, qui
    était faux).
  - Référence textuelle au contre-exemple `sin(1/x)` formulée selon le
    cours.
- **`Makefile`** : remplacé `python -m uv run` par `uv run` (compatible
  avec l'install standalone d'`uv`).
- **`.gitignore`** : ajout des artefacts LaTeX (`.aux`, `.log`, `.out`,
  etc.).
- **Bug Manim contourné** : `\begin{cases}` est inutilisable dans
  `MathTex` car Manim wrappe le contenu dans `\begin{align*}`, qui
  intercepte les séparateurs `&`. Toutes les définitions par cas sont
  reformulées en deux `MathTex` empilés.
- **Organisation du repo** :
  - création de `videos/` (1080p, suivi par git) pour les rendus finaux,
  - création de `references/` pour le PDF du cours,
  - les rendus de travail restent dans `media/` (ignoré).

---

## `v0.1` — Version initiale (déposée)

- Squelette du projet (`pyproject.toml`, `Makefile`, structure
  `src/scenes/tests`).
- Cinq scènes brouillon : `ConnexeVsArcs`, `ContreExempleSin1x`,
  `InvarianceTopologique`, `BorelLebesgue`, `Baire`.
- Briques réutilisables (`metric_space`, `paths`, `topological_set`,
  `coverings`, `presentation`).
- Animations partielles (continuité, convergence, déformations).
- Tests d'import basiques.

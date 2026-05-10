# topo-manim

> Animations Manim pour illustrer le cours de topologie de L3 — Sorbonne Université.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Manim](https://img.shields.io/badge/manim_community-0.20.1-orange.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Référence principale :** *Mémo de topologie*, Frédéric Le Roux & Frédéric Klopp,
[SU 3M260, 2021](references/3M260-memoTOP-2021.pdf)
**Encadrant :** Frédéric Le Roux
**Collaborateurs :** [@QJ1009](https://github.com/QJ1009) · [@solveiggir](https://github.com/solveiggir) · [@walidcr](https://github.com/walidcr)
**Outil :** [Manim Community Edition](https://www.manim.community/)

---

## Sommaire

- [Présentation](#présentation)
- [Vidéos](#vidéos)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Développement](#développement)
- [Contenu mathématique](#contenu-mathématique)
- [Documentation et références](#documentation-et-références)
- [Contribuer](#contribuer)
- [Changelog](#changelog)
- [Licence](#licence)

---

## Présentation

Ce projet construit des **scènes Manim courtes et réutilisables** pour visualiser
les notions abstraites du cours de topologie métrique de L3 :

- **Connexité** et connexité par arcs
- **Compacité** et recouvrements ouverts
- **Complétude** et théorème de Baire

Le code suit fidèlement le formalisme du *Mémo de topologie* de F. Le Roux et
F. Klopp : énoncés, notations, ordre des sections et recettes de preuves sont
alignés sur le PDF du cours fourni dans [`references/`](references/).

L'organisation est en deux couches :

| Dossier      | Rôle                                                            |
|--------------|-----------------------------------------------------------------|
| `src/`       | Briques réutilisables : objets topologiques, animations, utils. |
| `scenes/`    | Scènes finales prêtes au rendu, organisées par chapitre.        |

---

## Vidéos

Trois scènes ont été rendues en **1920×1080**.

| # | Scène | Sujet | Durée | Résolution | Taille | Fichier |
|---|---|---|---|---|---|---|
| 1 | **ConnexeVsArcs** | Connexité par arcs vs connexité topologique | 3:56 | 1920×1080@30fps | 9.7 MB | [`videos/ConnexeVsArcs.mp4`](videos/ConnexeVsArcs.mp4) |
| 2 | **ContreExempleSin1x** | Contre-exemple `sin(1/x)` | 1:47 | 1920×1080@60fps | 7.5 MB | [`videos/ContreExempleSin1x.mp4`](videos/ContreExempleSin1x.mp4) |
| 3 | **BorelLebesgue** | Compacité et théorème de Borel-Lebesgue | 1:01 | 1920×1080@30fps | 2.4 MB | [`videos/BorelLebesgue.mp4`](videos/BorelLebesgue.mp4) |

**Détails :**

- **ConnexeVsArcs** définit la connexité par arcs et la connexité, prouve
  rigoureusement `c.p.a. ⟹ connexe` par contraposition selon la *recette du
  cours*, et introduit le contre-exemple `sin(1/x)` pour la réciproque.
- **ContreExempleSin1x** construit progressivement le graphe
  `{(x, sin(1/x)) : x > 0} ∪ {0}×[-1,1]`, zoom infini sur l'origine,
  démontre que `E` est connexe (adhérence d'un connexe par arcs) mais n'est
  pas connexe par arcs (argument du *coureur topologique*).
- **BorelLebesgue** présente la compacité séquentielle, le théorème de
  Borel-Lebesgue (*tout recouvrement ouvert admet un sous-recouvrement
  fini*), Heine-Borel dans `ℝⁿ`, le contre-exemple `]0,1]` et le lemme de
  Lebesgue.

> [!NOTE]
> Les scènes `InvarianceTopologique` et `Baire` n'ont pas encore été rendues
> en 1080p. Pour les rendre vous-même : `just invariance quality=qh` ou
> `just baire quality=qh`.

---

## Structure du projet

```text
topo-manim/
├── src/                          # Briques réutilisables
│   ├── animations/
│   │   ├── continuity.py         # ε-δ, image réciproque d'ouverts
│   │   ├── convergence.py        # suites convergentes
│   │   └── deformations.py       # déformations continues, homéomorphismes
│   ├── objects/
│   │   ├── coverings.py          # recouvrements ouverts
│   │   ├── metric_space.py       # espaces métriques génériques
│   │   ├── paths.py              # chemins, arcs, concaténation
│   │   ├── presentation.py       # primitives visuelles (glow, panneaux)
│   │   └── topological_set.py    # ouverts, fermés, intérieur, adhérence
│   ├── utils/
│   │   ├── colors.py             # palette sémantique partagée
│   │   ├── layout.py             # positionnement et annotations
│   │   └── tex_labels.py         # labels LaTeX standardisés
│   └── config.py                 # config Manim (1920×1080, fond sombre)
│
├── scenes/                       # Scènes finales par chapitre
│   ├── 01_connexite/
│   │   ├── connexe_vs_arcs.py            (1637 lignes)
│   │   ├── contre_exemple_sin1x.py       (834 lignes)
│   │   └── invariance_topologique.py     (242 lignes)
│   ├── 02_compacite/
│   │   └── borel_lebesgue.py             (278 lignes)
│   └── 03_completude/
│       └── baire.py                      (232 lignes)
│
├── tests/                        # Tests d'import des scènes
│   └── test_scene_imports.py
│
├── videos/                       # Vidéos finales (1080p) ← suivies par git
│   ├── ConnexeVsArcs.mp4
│   ├── ContreExempleSin1x.mp4
│   └── BorelLebesgue.mp4
│
├── references/                   # Documents de cours
│   └── 3M260-memoTOP-2021.pdf    # Mémo de topologie (Le Roux/Klopp)
│
├── legacy/                       # Prototypes uniques antérieurs (référence)
│   └── README.md
│
├── media/                        # Rendus de travail Manim (gitignored)
│
├── .editorconfig                 # Conventions d'édition partagées
├── Justfile                      # Tâches cross-platform (rendu, test, lint, format)
├── pyproject.toml                # Dépendances + config ruff
├── CHANGELOG.md                  # Historique des versions
├── CONTRIBUTING.md               # Guide de contribution (FR)
└── README.md
```

> Le dossier `legacy/` contient les premiers scripts mono-fichiers, antérieurs à
> l'architecture deux-couches actuelle. Ils ne sont ni testés ni lintés ; voir
> [`legacy/README.md`](legacy/README.md).

---

## Installation

Le projet utilise deux outils en ligne de commande, à installer **une seule fois** :

| Outil | Rôle | Installation |
|---|---|---|
| [`uv`](https://docs.astral.sh/uv/) | Gestionnaire Python (interpréteur + venv + dépendances) | voir ci-dessous |
| [`just`](https://github.com/casey/just) | Lanceur de tâches cross-platform (remplace `make`) | voir ci-dessous |

### 1. Prérequis système

Manim nécessite **FFmpeg, Cairo, Pango et LaTeX**. Selon votre OS :

```bash
# Linux (Fedora / RHEL)
sudo dnf install -y cairo-devel pango-devel pkgconf-pkg-config python3-devel \
                    ffmpeg-free-devel texlive-scheme-medium

# Linux (Debian / Ubuntu)
sudo apt install -y libcairo2-dev libpango1.0-dev pkg-config python3-dev \
                    ffmpeg texlive-latex-extra

# macOS
brew install cairo pango ffmpeg
brew install --cask mactex

# Windows
winget install MiKTeX.MiKTeX
winget install Gyan.FFmpeg
# Cairo et Pango sont fournis par les wheels manimpango
```

### 2. Installer `uv` et `just`

```bash
# uv
curl -LsSf https://astral.sh/uv/install.sh | sh   # Linux / macOS
winget install astral-sh.uv                       # Windows

# just
sudo dnf install just                              # Linux (Fedora)
brew install just                                  # macOS
winget install Casey.Just                          # Windows
```

### 3. Cloner et installer le projet

```bash
git clone https://github.com/CyberSnakeH/topo-manim.git
cd topo-manim
just install        # équivalent à : uv sync
just test           # vérifie que tout est en place — doit afficher "2 passed"
```

C'est tout. Tu peux maintenant lancer n'importe quelle recette `just`.

---

## Utilisation

Toutes les commandes ci-dessous fonctionnent **sur les trois OS** sans
modification. La liste complète des recettes disponibles s'affiche avec :

```bash
just                    # ou : just --list
```

### Rendre une scène individuelle

```bash
just connexe_vs_arcs                    # qualité basse (-ql, ~480p, rapide)
just connexe_vs_arcs quality=qh         # qualité haute (-qh, 1080p)
just borel_lebesgue
just baire
just sin1x
just invariance
```

ou directement, sans `just` :

```bash
uv run manim render -qh scenes/01_connexite/connexe_vs_arcs.py ConnexeVsArcs
```

### Rendre toutes les scènes

```bash
just all                # toutes les scènes en qualité basse
just hq                 # toutes les scènes en qualité haute (1080p)
just connexite          # tout le chapitre IV
```

### Tests

```bash
just test               # vérifie que toutes les scènes s'importent
just check              # vérification syntaxique (compileall)
```

### Nettoyage

```bash
just clean              # supprime media/
```

---

## Développement

Le style Python est unifié via [Ruff](https://docs.astral.sh/ruff/) (configuré
dans [`pyproject.toml`](pyproject.toml)) et un fichier [`.editorconfig`](.editorconfig)
fixe l'encodage, les fins de ligne et l'indentation pour tous les fichiers du
repo.

```bash
just lint               # vérifie le style (ruff check)
just format             # reformate + autofix (ruff format puis ruff check --fix)
just format-check       # CI : échoue si quelque chose n'est pas conforme
```

Toute contribution doit passer `just lint`, `just test` et `just check` avant push.

---

## Contenu mathématique

L'organisation des scènes suit l'ordre du *Mémo de topologie* (Le Roux/Klopp 3M260) :

### Chapitre IV — Connexité

| Scène                     | Sections du cours couvertes                                                          | Durée  |
|---------------------------|--------------------------------------------------------------------------------------|--------|
| `ConnexeVsArcs`           | § IV.1.(a) connexité par arcs, § IV.1.(c) connexité, corollaire c.p.a. ⟹ connexe    | 3:56   |
| `ContreExempleSin1x`      | § IV.2.(a) contre-exemple à la réciproque                                             | 1:47   |
| `InvarianceTopologique`   | Corollaire IV.2 — invariance topologique                                              | —      |

**Détail de `ConnexeVsArcs` (suit fidèlement le cours) :**

1. **Ouverture** — la question intuitive
2. **§ IV.1.(a) Connexité par arcs** — chemin γ : [0,1] → X, exemple ℝᴺ via
   γ(t) = (1-t)x₀ + tx₁, **Proposition IV.1** (image continue, réunion à
   point commun, produit fini), **Corollaire IV.2**, concaténation γ ⋆ γ'
3. **§ IV.1.(c) Connexité** — définition primaire par les ouverts-fermés,
   proposition équivalente : X non connexe ⟺ ∃ X = O ⊔ O' partition en
   ouverts non vides
4. **Caractérisation par les applications vers {0,1}** — exercice 88 du
   cours sur les applications localement constantes, équivalence
   X connexe ⟺ toute f : X → {0,1} continue est constante, **corollaire
   [0,1] est connexe**
5. **Corollaire c.p.a. ⟹ connexe** — démonstration par contraposition
   selon la *recette du cours* : on suppose X = O ⊔ O', x₀ ∈ O, x₁ ∈ O',
   on fabrique la partition de [0,1] = γ⁻¹(O) ⊔ γ⁻¹(O') et on conclut
   par contradiction avec la connexité de [0,1]
6. **Et la réciproque ?** — théorème de relais § IV.2.(a) : *tout espace
   métrique complet, connexe, localement connexe, est connexe par arcs*

### Chapitre III — Compacité

| Scène           | Sections couvertes                                                                 | Durée  |
|-----------------|------------------------------------------------------------------------------------|--------|
| `BorelLebesgue` | § III.1 compacité séquentielle, théorème de Borel-Lebesgue, Heine-Borel, lemme    | 1:01   |

### Chapitre II — Complétude

| Scène     | Sections couvertes                                                                       | Durée  |
|-----------|------------------------------------------------------------------------------------------|--------|
| `Baire`   | § II.1 complétude, théorème de Baire, application : ℝ non dénombrable                    | —      |

---

## Documentation et références

- **[Mémo de topologie](references/3M260-memoTOP-2021.pdf)** — F. Le Roux,
  F. Klopp, SU 3M260, 2021. Référence principale du cours, dont les énoncés,
  notations et recettes de preuves sont reprises *verbatim* dans les scènes.
- **[Manim Community Documentation](https://docs.manim.community/)** — 0.20.1.

### Choix pédagogiques

- Les scènes privilégient les **idées structurantes du cours** plutôt que
  des démonstrations intégrales.
- Les énoncés affichés à l'écran sont **mathématiquement corrects et
  formellement alignés** sur le cours.
- Les couleurs sont centralisées dans `src/utils/colors.py` et la
  configuration Manim dans `src/config.py`.
- Style visuel inspiré de **3Blue1Brown** : schémas centraux grands et
  persistants, runners lumineux, animations ciblées par étape.

---

## Contribuer

Les contributions sont les bienvenues — corrections, nouvelles scènes,
clarifications du contenu mathématique, améliorations de la documentation.

Avant d'ouvrir une Pull Request, lisez le guide complet :
[**`CONTRIBUTING.md`**](CONTRIBUTING.md). Il décrit le workflow attendu, les
conventions de nommage de branche et de commit, les règles de style et la
procédure pour ajouter une nouvelle scène.

En résumé :

```bash
# Sur votre fork
git checkout -b feature/ma-modif
just format && just lint && just test && just check     # tout doit passer
git commit -m "feat: courte description"
git push origin feature/ma-modif
# Puis ouvrir une PR vers main
```

Pour signaler un bug ou proposer une amélioration, ouvrez une
[issue GitHub](https://github.com/CyberSnakeH/topo-manim/issues).

---

## Changelog

L'historique des versions est consigné dans
[**`CHANGELOG.md`**](CHANGELOG.md). Les entrées suivent le format
[Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et le projet
adhère au [versionnage sémantique](https://semver.org/lang/fr/).

Versions publiées :

- **`v0.3`** — Outillage cross-platform et nettoyage du repo (mai 2026)
- **`v0.2`** — Alignement formel sur le cours (avril 2025)
- **`v0.1`** — Version initiale

---

## Licence

Projet à usage pédagogique pour le cours 3M260 (Sorbonne Université).
Code source sous licence MIT — le PDF du *Mémo de topologie* est la
propriété de ses auteurs (F. Le Roux et F. Klopp) et est inclus dans
[`references/`](references/) avec leur autorisation pédagogique.

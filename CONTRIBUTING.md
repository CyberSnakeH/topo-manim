# Contribuer à topo-manim

Les contributions sont les bienvenues — corrections, nouvelles scènes,
clarifications du contenu mathématique, améliorations de la documentation
ou de l'outillage.

Ce document décrit le workflow attendu, les conventions de code et les
points d'attention spécifiques au projet.

---

## Mise en place

```bash
# 1. Forker le dépôt depuis GitHub puis cloner votre fork
git clone https://github.com/<votre-pseudo>/topo-manim.git
cd topo-manim

# 2. Installer l'environnement et vérifier que tout fonctionne
just install                  # équivalent à : uv sync
just test                     # doit afficher : 2 passed
```

Si vous n'avez pas encore `uv` ou `just`, voir la section
[Installation](README.md#installation) du README.

---

## Workflow de contribution

### 1. Créer une branche depuis `main`

Utilisez un préfixe parlant pour clarifier l'intention du changement :

```bash
git checkout -b feature/nouvelle-scene-banach    # nouvelle fonctionnalité
git checkout -b fix/contraposition-iv1c          # correction de bug
git checkout -b docs/clarifier-borel-lebesgue    # documentation
git checkout -b refactor/extraire-helper-tex     # refactor sans changement fonctionnel
git checkout -b chore/mise-a-jour-deps           # tâche de maintenance
```

### 2. Coder, formater, tester localement

Avant l'ouverture de toute Pull Request, ces quatre commandes doivent
passer sans erreur :

```bash
just format         # reformate automatiquement (ruff)
just lint           # vérifie le style sans modifier
just test           # tests d'import des scènes
just check          # tous les fichiers compilent (compileall)
```

`just format-check` (combine `lint` + `format --check`) est exécuté en
intégration continue ; faites-le tourner localement avant de pousser.

### 3. Écrire des messages de commit clairs

Format `type: description courte` (style *Conventional Commits*) :

| Type | Usage | Exemple |
|---|---|---|
| `feat` | Nouvelle fonctionnalité visible | `feat: scène Heine-Borel pour la compacité dans Rⁿ` |
| `fix` | Correction de bug ou d'erreur mathématique | `fix: corriger l'orientation du chemin γ⋆γ' dans connexe_vs_arcs` |
| `docs` | Documentation seulement | `docs: ajouter référence à la prop. III.2 du cours` |
| `refactor` | Restructuration sans changement de comportement | `refactor: extraire make_caption_box dans src/utils/layout.py` |
| `style` | Reformatage, espaces, imports (sans logique) | `style: appliquer ruff format` |
| `test` | Ajout ou modification de tests | `test: vérifier la construction de BorelLebesgue` |
| `chore` | Maintenance (deps, config, build) | `chore: bump manim 0.20.0 → 0.21.0` |
| `build` | Système de build / outillage | `build: ajouter recette just heine_borel` |

### 4. Ouvrir une Pull Request

Poussez votre branche et ouvrez une PR vers `main` en décrivant la
motivation **mathématique ou technique** du changement.

Pour les nouvelles scènes ou les modifications de scènes existantes,
joignez si possible un GIF court ou une capture d'une frame
caractéristique pour faciliter la revue.

---

## Règles de style

- **Python ≥ 3.11**, type hints encouragés dans `src/` (les scènes
  peuvent rester plus libres).
- **Imports explicites** : pas de `from manim import *` (sauf dans
  `legacy/`, qui n'est plus modifié).
- **Indentation 4 espaces, encodage UTF-8, fins de ligne LF** — tout est
  garanti automatiquement par [`.editorconfig`](.editorconfig) et
  `ruff format`. Ne pas mélanger tabs et espaces.
- **Cohérence avec le cours** : les énoncés et notations affichés à
  l'écran doivent rester *verbatim* alignés sur le *Mémo de topologie*
  (Le Roux/Klopp 3M260). Si vous modifiez une formulation
  mathématique, citez la section précise du cours dans le message de
  commit.
- **Couleurs et configuration** : utilisez les constantes de
  `src/utils/colors.py` et `src/config.py` plutôt que des valeurs en
  dur, pour garder la cohérence visuelle entre scènes.

---

## Ajouter une nouvelle scène

Si vous ajoutez une scène, voici la checklist :

1. La placer dans `scenes/<chapitre>/` (créer le dossier si le chapitre
   n'existe pas, par ex. `scenes/04_evn/`).
2. Référencer la nouvelle classe `Scene` dans
   [`tests/test_scene_imports.py`](tests/test_scene_imports.py) pour
   s'assurer qu'elle s'importe sans erreur.
3. Ajouter une recette dans le [`Justfile`](Justfile) pour la rendre
   facilement, sur le modèle des recettes existantes :

   ```just
   heine_borel quality=quality:
       uv run manim render -{{quality}} scenes/03_compacite/heine_borel.py HeineBorel
   ```

4. Documenter brièvement le contenu mathématique dans la section
   *Contenu mathématique* du [README](README.md#contenu-mathématique),
   en référençant les paragraphes correspondants du cours.

---

## Reporter un bug ou proposer une amélioration

Pour signaler un bug ou proposer une amélioration, ouvrez une
[issue GitHub](https://github.com/CyberSnakeH/topo-manim/issues) en
décrivant précisément :

- le **comportement observé** (capture d'écran ou trace d'erreur si
  pertinent),
- le **comportement attendu**,
- les **étapes pour le reproduire** (commande exacte, version d'OS et
  d'`uv`, etc.).

Pour les bugs Manim sous-jacents, mentionnez la version
(`uv pip show manim`) — le projet est verrouillé sur `manim>=0.18` mais
testé en pratique sur `0.20.x`.

---

## Questions

Pour toute question sur le contenu mathématique ou pédagogique,
contactez l'encadrant Frédéric Le Roux (Sorbonne Université) ou ouvrez
une [discussion GitHub](https://github.com/CyberSnakeH/topo-manim/discussions).

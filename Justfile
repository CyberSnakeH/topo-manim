# topo-manim — Cross-platform task runner
# Usage:  just <recipe> [quality=ql|qm|qh|qk]
# List all recipes: just --list  (or simply: just)

# Default recipe shows the list of available recipes
default:
    @just --list

# Quality flag for manim render. Override per-call:
#   just sin1x quality=qh
quality := "ql"

# ── Scene rendering ────────────────────────────────────────────────────────

# Render ConnexeVsArcs
connexe_vs_arcs quality=quality:
    uv run manim render -{{quality}} scenes/01_connexite/connexe_vs_arcs.py ConnexeVsArcs

# Render InvarianceTopologique
invariance quality=quality:
    uv run manim render -{{quality}} scenes/01_connexite/invariance_topologique.py InvarianceTopologique

# Render ContreExempleSin1x
sin1x quality=quality:
    uv run manim render -{{quality}} scenes/01_connexite/contre_exemple_sin1x.py ContreExempleSin1x

# Render BorelLebesgue
borel_lebesgue quality=quality:
    uv run manim render -{{quality}} scenes/02_compacite/borel_lebesgue.py BorelLebesgue

# Render Baire
baire quality=quality:
    uv run manim render -{{quality}} scenes/03_completude/baire.py Baire

# ── Group targets ──────────────────────────────────────────────────────────

# Render every Chapter IV (Connexité) scene
connexite quality=quality: (connexe_vs_arcs quality) (invariance quality) (sin1x quality)

# Render every Chapter III (Compacité) scene
compacite quality=quality: (borel_lebesgue quality)

# Render every Chapter II (Complétude) scene
completude quality=quality: (baire quality)

# Render every scene in the selected quality (default ql)
all quality=quality: (connexite quality) (compacite quality) (completude quality)

# Render every scene in high quality (1080p)
hq: (all "qh")

# ── Dev workflow ──────────────────────────────────────────────────────────

# Sync the virtual environment from pyproject.toml + uv.lock
install:
    uv sync

# Run pytest
test:
    uv run pytest

# Verify all .py files compile (compileall)
check:
    uv run python -m compileall src scenes tests

# Lint with ruff (no modifications)
lint:
    uv run ruff check .

# Reformat + autofix lint issues
format:
    uv run ruff format .
    uv run ruff check --fix .

# CI-friendly: fail if anything would be reformatted or has lint issues
format-check:
    uv run ruff format --check .
    uv run ruff check .

# Remove media/ (Manim work renders, not tracked)
clean:
    python -c "import shutil; shutil.rmtree('media', ignore_errors=True)"

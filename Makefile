PYTHON = python
UV = uv run
export PYTHONPATH := $(CURDIR)
MANIM = $(UV) manim render
QUALITY ?= -ql

.DEFAULT_GOAL := all

connexe_vs_arcs:
	$(MANIM) $(QUALITY) scenes/01_connexite/connexe_vs_arcs.py ConnexeVsArcs

invariance:
	$(MANIM) $(QUALITY) scenes/01_connexite/invariance_topologique.py InvarianceTopologique

sin1x:
	$(MANIM) $(QUALITY) scenes/01_connexite/contre_exemple_sin1x.py ContreExempleSin1x

borel_lebesgue:
	$(MANIM) $(QUALITY) scenes/02_compacite/borel_lebesgue.py BorelLebesgue

baire:
	$(MANIM) $(QUALITY) scenes/03_completude/baire.py Baire

connexite: connexe_vs_arcs invariance sin1x

compacite: borel_lebesgue

completude: baire

all: connexite compacite completude

hq:
	$(MAKE) all QUALITY=-qh

check:
	$(UV) python -m compileall src scenes tests

test:
	$(UV) pytest

install:
	uv sync

clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('media', ignore_errors=True)"

.PHONY: connexe_vs_arcs invariance sin1x borel_lebesgue baire \
	connexite compacite completude all hq check test install clean

"""Tests minimaux d'import pour les scenes et les modules reutilisables."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


SCENES = {
    "scenes/01_connexite/connexe_vs_arcs.py": "ConnexeVsArcs",
    "scenes/01_connexite/invariance_topologique.py": "InvarianceTopologique",
    "scenes/01_connexite/contre_exemple_sin1x.py": "ContreExempleSin1x",
    "scenes/02_compacite/borel_lebesgue.py": "BorelLebesgue",
    "scenes/03_completude/baire.py": "Baire",
}


def load_module(relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_scene_modules_define_expected_classes():
    for relative_path, class_name in SCENES.items():
        module = load_module(relative_path)
        assert hasattr(module, class_name)


def test_reusable_modules_are_importable():
    modules = [
        "src.animations.continuity",
        "src.animations.convergence",
        "src.animations.deformations",
        "src.objects.coverings",
        "src.objects.metric_space",
        "src.objects.paths",
        "src.objects.topological_set",
        "src.utils.colors",
        "src.utils.layout",
        "src.utils.tex_labels",
    ]
    for module_name in modules:
        __import__(module_name)

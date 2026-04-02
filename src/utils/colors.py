"""Palette de couleurs cohérente pour le projet topo-manim."""

from manim import ManimColor

# --- Espaces et ensembles ---
SPACE_COLOR = ManimColor("#2B2D42")       # fond d'espace métrique
OPEN_SET_COLOR = ManimColor("#06D6A0")    # ouverts
CLOSED_SET_COLOR = ManimColor("#EF476F")  # fermés
INTERIOR_COLOR = ManimColor("#118AB2")    # intérieur
BOUNDARY_COLOR = ManimColor("#FFD166")    # frontière
CLOSURE_COLOR = ManimColor("#073B4C")     # adhérence

# --- Chemins et arcs ---
PATH_COLOR = ManimColor("#F72585")
ARC_COLOR = ManimColor("#7209B7")

# --- Recouvrements ---
COVER_COLORS = [
    ManimColor("#4361EE"),
    ManimColor("#4CC9F0"),
    ManimColor("#F72585"),
    ManimColor("#7209B7"),
    ManimColor("#3A0CA3"),
]

# --- Epsilon-delta -> Continuité ---
EPSILON_COLOR = ManimColor("#06D6A0")
DELTA_COLOR = ManimColor("#FFD166")

# --- Général ---
HIGHLIGHT_COLOR = ManimColor("#F77F00")
DIM_COLOR = ManimColor("#8D99AE")
TEXT_COLOR = ManimColor("#EDF2F4")

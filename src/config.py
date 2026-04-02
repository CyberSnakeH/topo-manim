"""Configuration globale du projet topo-manim."""

from manim import config as manim_config

# Résolution Full HD
manim_config.pixel_width = 1920
manim_config.pixel_height = 1080
manim_config.frame_rate = 30

# Fond sombre
manim_config.background_color = "#1A1A2E"

# Dossier de sortie
manim_config.media_dir = "./media"

# Durée par défaut des animations (secondes)
DEFAULT_ANIM_DURATION = 2.0
DEFAULT_WAIT = 1.0
SHORT_WAIT = 0.5

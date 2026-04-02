"""Labels LaTeX fréquents pour la topologie."""

from manim import MathTex


# --- Quantificateurs et symboles ---
def forall_eps(font_size: int = 30) -> MathTex:
    return MathTex(r"\forall \varepsilon > 0", font_size=font_size)


def exists_delta(font_size: int = 30) -> MathTex:
    return MathTex(r"\exists \delta > 0", font_size=font_size)


def eps_delta_condition(font_size: int = 28) -> MathTex:
    return MathTex(
        r"d(x,y) < \delta \Rightarrow d(f(x), f(y)) < \varepsilon",
        font_size=font_size,
    )


# --- Topologie ---
def open_ball(center: str = "x", radius: str = "r", font_size: int = 30) -> MathTex:
    return MathTex(rf"B({center}, {radius})", font_size=font_size)


def closure_tex(subset: str = "A", font_size: int = 30) -> MathTex:
    return MathTex(rf"\overline{{{subset}}}", font_size=font_size)


def interior_tex(subset: str = "A", font_size: int = 30) -> MathTex:
    return MathTex(rf"\mathring{{{subset}}}", font_size=font_size)


def boundary_tex(subset: str = "A", font_size: int = 30) -> MathTex:
    return MathTex(rf"\partial {subset}", font_size=font_size)


# --- Connexité ---
def connexe_def(font_size: int = 26) -> MathTex:
    return MathTex(
        r"X \text{ connexe} \iff \nexists\, U,V \text{ ouverts disjoints t.q. } X = U \sqcup V",
        font_size=font_size,
    )


def arc_connexe_def(font_size: int = 26) -> MathTex:
    return MathTex(
        r"\forall x,y \in X,\; \exists \gamma : [0,1] \to X "
        r"\text{ continue, } \gamma(0)=x,\, \gamma(1)=y",
        font_size=font_size,
    )


# --- Compacité ---
def borel_lebesgue_tex(font_size: int = 26) -> MathTex:
    return MathTex(
        r"X \text{ compact} \iff "
        r"\text{tout recouvrement ouvert admet un sous-recouvrement fini}",
        font_size=font_size,
    )

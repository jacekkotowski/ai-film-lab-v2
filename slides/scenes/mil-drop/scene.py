"""mil-drop -- gravity acts the whole flight: drop = 1/2 g t^2.

Content: spec.md. Slide 6 of the mil-measure film. Side view: the bore
line straight, the path curving under it; the drop at 0.5 s and 1 s.
The curve's shape is exact (y ~ t^2 with x ~ t); its depth is drawn large.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/mil-drop/out scenes/mil-drop/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Arrow, DashedLine, FadeIn, ParametricFunction, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Drop"
G = 9.81
TIMES = [0.5, 1.0]                   # s


def drop(t: float) -> float:
    return 0.5 * G * t * t           # 1.23 m, 4.91 m


# ---- layout --------------------------------------------------------------
# Safe area: x in [-SIDE, SIDE] = [-4, 4]; y in [BOTTOM, TOP] = [-4, 7].
BORE_Y, X0, PER_S = 5.0, -3.8, 7.0   # muzzle at (X0, BORE_Y); x = X0 + PER_S * t
PER_M = 3.4 / drop(1.0)              # units down per metre of drop: 1 s -> 3.4
FORMULA_Y, FORMULA_FONT = -0.35, 72
CHAIN_TOP, CHAIN_STEP = -1.45, 1.15  # "faster bullet" / "less time" / "less drop"

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["Gravity", "Below", "second", "faster"]
BEAT_LINES = [0, 1, 2, 4]
RUN_TIMES = [1.5, 1.0, 1.5, 1.5]


def x_of(t):
    return X0 + PER_S * t


def y_of(t):
    return BORE_Y - drop(t) * PER_M


def flight():
    bore = DashedLine((X0, BORE_Y, 0), (frame.SIDE, BORE_Y, 0), dash_length=0.15,
                      stroke_width=3, color=frame.DIM)
    path = ParametricFunction(lambda t: (x_of(t), y_of(t), 0), t_range=(0, TIMES[-1]))
    return VGroup(bore, path.set_stroke(frame.INK, width=5))


def marks():
    g = []
    for t in TIMES:
        x = x_of(t)
        g.append(Arrow((x, BORE_Y, 0), (x, y_of(t), 0), buff=0, stroke_width=5,
                       color=frame.ACCENT, max_tip_length_to_length_ratio=0.3,
                       tip_length=0.2))
        g.append(kit.text(f"{t:g} s", x, BORE_Y + 0.25, frame.SECOND))
    # the drops: under the curve, clear of it (right of the 1 s arrow is past SIDE)
    g.append(kit.text(f"{drop(TIMES[0]):.1f} m", x_of(TIMES[0]) - 0.15,
                      y_of(TIMES[0]) - 0.65, frame.ACCENT, align="right"))
    g.append(kit.text(f"{drop(TIMES[1]):.1f} m", x_of(TIMES[1]) + 0.6,
                      y_of(TIMES[1]) - 0.75, frame.ACCENT, align="right"))
    return VGroup(*g)


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE)]
        steps = [self.step_flight, self.step_formula, self.step_marks, self.step_faster]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_flight(self):
        return [FadeIn(flight())]

    def step_formula(self):
        return [FadeIn(kit.text("drop ≈ ½ g t²", 0, FORMULA_Y, frame.INK, FORMULA_FONT))]

    def step_marks(self):
        return [FadeIn(marks())]

    def step_faster(self):
        return [FadeIn(kit.chain(["faster bullet", "less time", "less drop"], CHAIN_TOP, step=CHAIN_STEP,
                                 colors=(frame.INK, frame.SECOND, frame.ACCENT)))]

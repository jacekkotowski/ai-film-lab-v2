"""mil-angle -- a mil is an angle: the further, the more cm it covers.

Content: spec.md. Slide 4 of the mil-measure film. One mil seen from the
side, opening from the eye; the angle drawn far wider than 1 mil.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/mil-angle/out scenes/mil-angle/scene.py Slide
"""

import math
import sys
from pathlib import Path

from manim import Arc, FadeIn, Line, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "MIL is an angle"
METRES = [100, 200, 300]


def cm(metres: float) -> int:
    return round(metres / 10)        # 1 mil = 1/1000: 100 m -> 10 cm


# ---- layout --------------------------------------------------------------
# Safe area: x in [-SIDE, SIDE] = [-4, 4]; y in [BOTTOM, TOP] = [-4, 7].
EYE = (0.0, -3.0, 0.0)
PER_100M = 2.7                       # units up per 100 m
HALF_300 = 1.25                      # half the width at 300 m: labels need 2.4 beside it
LABEL_GAP, CAP = 0.3, 0.15
ARC_R = 1.8

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["angle", "hundred|100", "two|200"]
BEAT_LINES = [1, 2, 3]
RUN_TIMES = [1.0, 1.0, 1.5]


def y_of(m):
    return EYE[1] + m / 100 * PER_100M


def half(m):
    return HALF_300 * m / METRES[-1]


def cone():
    top = y_of(METRES[-1])
    edges = VGroup(Line(EYE, (-half(METRES[-1]), top, 0)),
                   Line(EYE, (half(METRES[-1]), top, 0))).set_stroke(frame.INK, width=3)
    a = math.atan2(half(METRES[-1]), top - EYE[1])
    arc = Arc(radius=ARC_R, start_angle=math.pi / 2 - a, angle=2 * a,
              arc_center=EYE)
    arc.set_stroke(frame.SECOND, width=5)
    label = kit.text("1 MIL", EYE[0] + 0.45, EYE[1] - 0.2, frame.SECOND, align="left")
    return VGroup(edges, arc, label)


def row(m):
    y, w = y_of(m), half(m)
    bar = VGroup(Line((-w, y, 0), (w, y, 0)), Line((-w, y - CAP, 0), (-w, y + CAP, 0)),
                 Line((w, y - CAP, 0), (w, y + CAP, 0))).set_stroke(frame.ACCENT, width=6)
    return VGroup(bar,
                  kit.text(f"{m} m", -w - LABEL_GAP, y - 0.22, frame.INK, align="right"),
                  kit.text(f"{cm(m)} cm", w + LABEL_GAP, y - 0.22, frame.ACCENT, align="left"))


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE)]
        steps = [self.step_angle, self.step_first, self.step_rest]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_angle(self):
        return [FadeIn(cone())]

    def step_first(self):
        return [FadeIn(row(METRES[0]))]

    def step_rest(self):
        return [FadeIn(row(m)) for m in METRES[1:]]

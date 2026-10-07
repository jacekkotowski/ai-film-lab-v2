"""back-azimuth -- the way back is half a circle away.

Content: spec.md. Never rendered yet (PLAN step 1).

    uv run --extra render manim -s -r 540,960 --media_dir scenes/back-azimuth/out scenes/back-azimuth/scene.py Slide
"""

import math
import sys
from pathlib import Path

from manim import (Arrow, Circle, Create, Dot, FadeIn, GrowArrow, Line,
                   Scene, Text, VGroup, Write, LEFT, UP)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
MILS = 6400
FORWARD_MIL = 1200
BACK_MIL = (FORWARD_MIL + MILS // 2) % MILS

# ---- layout --------------------------------------------------------------
# Tick labels are 1.9 wide at MIN_FONT (measured), so a label beside the
# circle at 1600/4800 fits inside frame.SIDE only if RADIUS <= 2.0.
RADIUS = 2.0
CENTRE = (0.0, 2.0, 0.0)
WALK = 3.6                       # A to B, in frame units; B stays inside SIDE
TICKS = (0, 1600, 3200, 4800)
TICK_BUFF = 0.1                  # label to circle
BACK_SHIFT = 0.3                 # the way back, drawn beside the way there

# ---- timing --------------------------------------------------------------
# Step i belongs to sentence BEAT_LINES[i] of the narration over this
# picture (0-based). Change these after narrating, not the waits.
BEAT_LINES = [0, 1, 2, 3]
RUN_TIMES = [1.5, 1.2, 1.5, 1.0]


def towards(mil: float) -> tuple[float, float, float]:
    """A bearing in mils -> a unit vector. 0 is north (up), clockwise."""
    a = 2 * math.pi * mil / MILS
    # Rounded: sin(pi) is 1.2e-16, which next_to reads as "to the right".
    return (round(math.sin(a), 9), round(math.cos(a), 9), 0.0)


def plus(p, v, k=1.0):
    return (p[0] + k * v[0], p[1] + k * v[1], 0.0)


class Slide(Scene):
    def construct(self):
        background = []
        steps = [self.step_circle, self.step_forward, self.step_back, self.step_sum]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background)

    # ---- one method per step; each returns its animations ----------------
    def step_circle(self):
        ring = Circle(radius=RADIUS, color=frame.DIM).move_to(CENTRE)
        labels = VGroup(*[
            Text(str(m), font_size=frame.MIN_FONT, color=frame.DIM)
            .next_to(plus(CENTRE, towards(m), RADIUS), towards(m),
                     buff=TICK_BUFF)
            for m in TICKS])
        title = Text(f"{MILS} mil", font_size=frame.TITLE_FONT,
                     color=frame.INK).move_to((0, frame.TOP - 0.3, 0))
        return [Create(ring), FadeIn(labels), Write(title)]

    def step_forward(self):
        self.a = CENTRE
        self.b = plus(CENTRE, towards(FORWARD_MIL), WALK)
        arrow = Arrow(self.a, self.b, buff=0, color=frame.ACCENT)
        label = Text(f"{FORWARD_MIL}", font_size=frame.MIN_FONT,
                     color=frame.ACCENT).next_to(arrow.get_center(), UP)
        return [FadeIn(Dot(self.a, color=frame.INK)), GrowArrow(arrow),
                FadeIn(label)]

    def step_back(self):
        # Shifted to the right of the way there (clockwise of the forward
        # bearing), so the two arrows do not lie on one line.
        side = towards(FORWARD_MIL + MILS // 4)
        b, a = plus(self.b, side, BACK_SHIFT), plus(self.a, side, BACK_SHIFT)
        north = Line(b, plus(b, (0, 1, 0), 1.2), color=frame.DIM)
        arrow = Arrow(b, a, buff=0, color=frame.SECOND)
        label = Text(f"{BACK_MIL}", font_size=frame.MIN_FONT,
                     color=frame.SECOND).next_to(north.get_end(), LEFT)
        return [Create(north), GrowArrow(arrow), FadeIn(label)]

    def step_sum(self):
        line = Text(f"{FORWARD_MIL} + {MILS // 2} = {BACK_MIL}",
                    font_size=frame.MIN_FONT, color=frame.INK
                    ).move_to((0, frame.BOTTOM + 1.0, 0))
        return [Write(line)]

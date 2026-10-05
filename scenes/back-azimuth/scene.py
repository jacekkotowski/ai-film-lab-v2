"""back-azimuth -- the way back is half a circle away.

Content: spec.md. Never rendered yet (PLAN step 1).

    uv run --extra render manim -s -r 540,960 --media_dir scenes/back-azimuth/out scenes/back-azimuth/scene.py Slide
"""

import math
import sys
from pathlib import Path

from manim import (Arrow, Circle, Create, Dot, FadeIn, GrowArrow, Line,
                   Scene, Text, VGroup, Write, UP)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import beats, frame  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
MILS = 6400
FORWARD_MIL = 1200
BACK_MIL = (FORWARD_MIL + MILS // 2) % MILS

# ---- layout --------------------------------------------------------------
RADIUS = 3.0
CENTRE = (0.0, 2.0, 0.0)
WALK = 3.6                       # A to B, in frame units
TICKS = (0, 1600, 3200, 4800)

# ---- timing --------------------------------------------------------------
# Step i belongs to sentence BEAT_LINES[i] of the narration over this
# picture (0-based). Change these after narrating, not the waits.
BEAT_LINES = [0, 1, 2, 3]
RUN_TIMES = [1.5, 1.2, 1.5, 1.0]


def towards(mil: float) -> tuple[float, float, float]:
    """A bearing in mils -> a unit vector. 0 is north (up), clockwise."""
    a = 2 * math.pi * mil / MILS
    return (math.sin(a), math.cos(a), 0.0)


def plus(p, v, k=1.0):
    return (p[0] + k * v[0], p[1] + k * v[1], 0.0)


class Slide(Scene):
    def construct(self):
        steps = [self.step_circle, self.step_forward, self.step_back, self.step_sum]
        p = beats.for_scene(HERE, BEAT_LINES, RUN_TIMES)
        for wait, step, rt in zip(p.waits, steps, RUN_TIMES):
            if wait >= beats.MIN_WAIT:
                self.wait(wait)
            self.play(*step(), run_time=rt)
        if p.tail >= beats.MIN_WAIT:
            self.wait(p.tail)

    # ---- one method per step; each returns its animations ----------------
    def step_circle(self):
        ring = Circle(radius=RADIUS, color=frame.DIM).move_to(CENTRE)
        labels = VGroup(*[
            Text(str(m), font_size=frame.MIN_FONT * 0.6, color=frame.DIM)
            .move_to(plus(CENTRE, towards(m), RADIUS + 0.6))
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
        north = Line(self.b, plus(self.b, (0, 1, 0), 1.2), color=frame.DIM)
        arrow = Arrow(self.b, self.a, buff=0.15, color=frame.SECOND)
        label = Text(f"{BACK_MIL}", font_size=frame.MIN_FONT,
                     color=frame.SECOND).next_to(self.b, UP * 2.2)
        return [Create(north), GrowArrow(arrow), FadeIn(label)]

    def step_sum(self):
        line = Text(f"{FORWARD_MIL} + {MILS // 2} = {BACK_MIL}",
                    font_size=frame.MIN_FONT, color=frame.INK
                    ).move_to((0, frame.BOTTOM + 1.0, 0))
        return [Write(line)]

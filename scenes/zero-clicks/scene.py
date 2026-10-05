"""zero-clicks -- clicks = distance / what one click moves.

Content: spec.md. Slide 2 of 4 of the zeroing film.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/zero-clicks/out scenes/zero-clicks/scene.py Slide
"""

import math
import sys
from pathlib import Path

from manim import FadeIn, Line, Scene, Text, VGroup, Write

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
DISTANCE_M = 100
MOA_CM = DISTANCE_M * math.tan(math.radians(1 / 60)) * 100   # 2.909 cm
UP_CM, RIGHT_CM = 5.0, 4.5       # the group from slide 1, to correct
OPTICS = [                       # name, click label, click in MOA
    ("Triumph", "½ MOA", 0.5),
    ("SLx", "¼ MOA", 0.25),
]
FORMULA = "clicks = cm ÷ click"

# ---- layout --------------------------------------------------------------
COLUMN_X = (-2.2, 2.2)
S = 1.0                          # frame units per cm, for the bar
BAR_TOP = 3.2
TICK = 0.3                       # half-width of a click tick
# Rows are placed by their TOP edge: centring would set "Triumph" (with
# its descender) higher than "SLx".
ROW = {"name": 5.9, "moa": 5.0, "cm": 4.15, "up": -2.3, "right": -3.1}

# ---- timing --------------------------------------------------------------
# Step i belongs to sentence BEAT_LINES[i] of the narration over this
# picture (0-based). Change these after narrating, not the waits.
BEAT_LINES = [0, 1, 2]
RUN_TIMES = [1.0, 1.5, 1.0]


def text(s, top, x, color=frame.INK):
    t = Text(s, font_size=frame.MIN_FONT, color=color)
    return t.move_to((x, top - t.height / 2, 0))


class Slide(Scene):
    def construct(self):
        background = []
        steps = [self.step_formula, self.step_optics, self.step_counts]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background)

    # ---- one method per step; each returns its animations ----------------
    def step_formula(self):
        return [Write(text(FORMULA, frame.TOP, 0))]

    def step_optics(self):
        columns = []
        for x, (name, moa_label, moa) in zip(COLUMN_X, OPTICS):
            click = moa * MOA_CM
            n = round(UP_CM / click)
            bar = Line((x, BAR_TOP, 0), (x, BAR_TOP - UP_CM * S, 0)
                       ).set_stroke(frame.DIM, width=6)
            ticks = VGroup(*[
                Line((x - TICK, BAR_TOP - k * click * S, 0),
                     (x + TICK, BAR_TOP - k * click * S, 0))
                for k in range(n + 1)]).set_stroke(frame.ACCENT, width=5)
            columns.append(VGroup(
                text(name, ROW["name"], x),
                text(moa_label, ROW["moa"], x, frame.DIM),
                text(f"{click:.2f} cm", ROW["cm"], x, frame.ACCENT),
                bar, ticks))
        span = text(f"{UP_CM:g} cm", BAR_TOP - UP_CM * S / 2 + 0.3, 0, frame.DIM)
        return [FadeIn(columns[0]), FadeIn(columns[1]), FadeIn(span)]

    def step_counts(self):
        counts = [VGroup(
            text(f"up {round(UP_CM / (moa * MOA_CM))}", ROW["up"], x, frame.ACCENT),
            text(f"right {round(RIGHT_CM / (moa * MOA_CM))}", ROW["right"], x,
                 frame.ACCENT))
            for x, (_, _, moa) in zip(COLUMN_X, OPTICS)]
        return [FadeIn(c) for c in counts]

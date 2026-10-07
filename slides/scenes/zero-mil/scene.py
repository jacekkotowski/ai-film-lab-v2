"""zero-mil -- one mil on the reticle is about 14 turret clicks.

Content: spec.md. Slide 3a of 4 of the zeroing film.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/zero-mil/out scenes/zero-mil/scene.py Slide
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
MIL_CM = DISTANCE_M * math.tan(0.001) * 100                  # 10.000 cm
CLICK_MOA = 0.25
CLICK_CM = CLICK_MOA * MOA_CM                                # 0.727 cm
CLICKS_PER_MIL = MIL_CM / CLICK_CM                           # 13.75

# ---- layout --------------------------------------------------------------
S = 0.6                          # frame units per cm, for the bar
BAR_TOP = 4.0
COLUMN_X = (-2.2, 2.2)           # turret left, reticle right
TICK = 0.45                      # click ticks reach this far left of the bar
BRACKET_X = 0.45                 # the mil bracket, right of the bar
# Rows are placed by their BASELINE (the bottom of letters without
# descenders), so "turret" and "reticle" sit on one line.
ROW = {"head": 6.3, "unit": 5.45, "cm": 4.6, "result": -2.95}

# ---- timing --------------------------------------------------------------
# Step i belongs to sentence BEAT_LINES[i] of the narration over this
# picture (0-based). Change these after narrating, not the waits.
# Each step starts on its word (beats.starts_by_words): the word as he
# says it in films/zeroing.script.txt. "a|b" accepts either. Not heard ->
# the step starts with the one before, and [beats] says so.
BEAT_WORDS = ["turrets", "reticle", "fourteen|14"]
BEAT_LINES = [0, 1, 2]
RUN_TIMES = [1.5, 1.0, 1.0]


def text(s, baseline, x, color=frame.INK):
    """Text centred on x with its baseline on y. An "H" is set after it
    to find the baseline (its bottom), then taken away."""
    t = Text(s + "H", font_size=frame.MIN_FONT, color=color)
    h = t[-1]
    t.shift((0, baseline - h.get_bottom()[1], 0))
    t.remove(h)
    return t.shift((x - t.get_center()[0], 0, 0))


def y_at(cm: float) -> float:
    return BAR_TOP - cm * S


class Slide(Scene):
    def construct(self):
        background = []
        steps = [self.step_turret, self.step_reticle, self.step_result]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    # ---- one method per step; each returns its animations ----------------
    def step_turret(self):
        x = COLUMN_X[0]
        n = math.ceil(CLICKS_PER_MIL)                         # 14
        bar = Line((0, y_at(0), 0), (0, y_at(MIL_CM), 0)
                   ).set_stroke(frame.DIM, width=6)
        ticks = VGroup(*[Line((-TICK, y_at(k * CLICK_CM), 0),
                              (0, y_at(k * CLICK_CM), 0))
                         for k in range(n + 1)]).set_stroke(frame.ACCENT, width=5)
        labels = VGroup(text("turret", ROW["head"], x),
                        text(f"{'¼' if CLICK_MOA == 0.25 else CLICK_MOA} MOA",
                             ROW["unit"], x, frame.DIM),
                        text(f"{CLICK_CM:.2f} cm", ROW["cm"], x, frame.ACCENT))
        return [FadeIn(VGroup(bar, ticks, labels))]

    def step_reticle(self):
        x = COLUMN_X[1]
        top, bottom = y_at(0), y_at(MIL_CM)
        bracket = VGroup(
            Line((BRACKET_X, top, 0), (BRACKET_X, bottom, 0)),
            Line((0.1, top, 0), (BRACKET_X, top, 0)),
            Line((0.1, bottom, 0), (BRACKET_X, bottom, 0)),
        ).set_stroke(frame.SECOND, width=5)
        labels = VGroup(text("reticle", ROW["head"], x),
                        text("1 mil", ROW["unit"], x, frame.DIM),
                        text(f"{MIL_CM:.0f} cm", ROW["cm"], x, frame.SECOND))
        return [FadeIn(VGroup(bracket, labels))]

    def step_result(self):
        return [Write(text(f"{CLICKS_PER_MIL:.2f} ≈ {round(CLICKS_PER_MIL)} clicks",
                           ROW["result"], 0))]

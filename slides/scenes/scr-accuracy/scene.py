"""scr-accuracy -- "95 % accurate" loses to a test that calls everyone healthy.

Content: spec.md. Slide 1 of the screening film.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/scr-accuracy/out scenes/scr-accuracy/scene.py Slide
"""

import math
import sys
from pathlib import Path

from manim import Arc, FadeIn, Line, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402
from aimanim import screening as ex  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "95% accurate?"
T = ex.EXAMPLE
TEST_ACC = T.accuracy * 100              # 94.99
LAZY_ACC = T.always_negative * 100       # 99.8
LABELS = (("screening", "test"), ("always", "healthy"))
SCALE = (90, 100)                        # the gauges read 90 % .. 100 %

# ---- layout --------------------------------------------------------------
GAUGE_X, GAUGE_Y, GAUGE_R = 2.05, 2.6, 1.2   # "screening" 3.81 wide: x <= 2.09
LABEL_ROWS = (5.25, 4.45)                # baselines; 0.7 apart, "g" touched "test"
TICK_ROW, VALUE_ROW, VALUE_FONT = 1.9, 0.95, 64

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["doctor", "every", "score"]
BEAT_LINES = [0, 1, 1]
RUN_TIMES = [1.0, 1.5, 1.0]


def gauge(x, value, color, words):
    """A half dial from SCALE[0] (left) to SCALE[1] (right), its needle on
    `value`, the value under it and two words above it."""
    lo, hi = SCALE
    a = math.pi * (hi - value) / (hi - lo)
    arc = Arc(radius=GAUGE_R, start_angle=0, angle=math.pi,
              arc_center=(x, GAUGE_Y, 0)).set_stroke(frame.DIM, 8)
    needle = Line((x, GAUGE_Y, 0), (x + 0.9 * GAUGE_R * math.cos(a),
                                    GAUGE_Y + 0.9 * GAUGE_R * math.sin(a), 0)
                  ).set_stroke(color, 8)
    ticks = VGroup(kit.text(str(lo), x - GAUGE_R, TICK_ROW, frame.DIM),
                   kit.text(str(hi), x + GAUGE_R, TICK_ROW, frame.DIM))
    label = VGroup(*[kit.text(w, x, b) for w, b in zip(words, LABEL_ROWS)])
    val = kit.text(f"{value:.1f}%", x, VALUE_ROW, color, VALUE_FONT)
    return VGroup(label, arc, ticks, needle, val)


def population():
    healthy, cases = ex.grid_places()
    pts = kit.grid_points(ex.N, ex.GRID_COLS, ex.GRID_PITCH, ex.GRID_LEFT, ex.GRID_TOP)
    return (kit.dots([pts[i] for i in healthy], ex.GRID_DOT, frame.HEALTHY),
            kit.dots([pts[i] for i in cases], ex.CASE_DOT, frame.SICK))


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE)]
        steps = [self.step_test, self.step_population, self.step_lazy]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_test(self):
        return [FadeIn(gauge(-GAUGE_X, TEST_ACC, frame.ACCENT, LABELS[0]))]

    def step_population(self):
        healthy, cases = population()
        return [FadeIn(healthy), FadeIn(cases)]

    def step_lazy(self):
        return [FadeIn(gauge(GAUGE_X, LAZY_ACC, frame.SECOND, LABELS[1]))]

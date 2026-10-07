"""mil-wind -- drift = crosswind x lag, and 30 cm at 300 m is 1 mil.

Content: spec.md. Slide 7 of the mil-measure film. Seen from above: the
aim line straight, the bullet's path bending downwind; the drift drawn large.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/mil-wind/out scenes/mil-wind/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Arrow, DashedLine, FadeIn, Line, ParametricFunction, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Wind"
DRIFT_CM, DIST_M = 30, 300


def drift_mil() -> float:
    return DRIFT_CM * 10 / DIST_M    # 1.0


# ---- layout --------------------------------------------------------------
# Safe area: x in [-SIDE, SIDE] = [-4, 4]; y in [BOTTOM, TOP] = [-4, 7].
MUZZLE, TARGET_Y = (0.0, 2.0), 5.0   # the aim line runs straight up
DRIFT_W = 1.3                        # the drift at the target, drawn
WIND_YS = (2.7, 3.5, 4.3)            # wind arrows from the left
FORMULA_ROWS = (1.0, 0.05)           # baselines
CHAIN_TOP, CHAIN_STEP = -1.3, 1.2    # 3 rows to -3.7

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["Wind", "speed", "Thirty|30"]
BEAT_LINES = [0, 1, 2]
RUN_TIMES = [1.5, 1.5, 1.5]


def flight():
    h = TARGET_Y - MUZZLE[1]
    aim = DashedLine((0, MUZZLE[1], 0), (0, TARGET_Y, 0), dash_length=0.15,
                     stroke_width=3, color=frame.DIM)
    # drift grows faster than the distance; drawn as distance squared
    path = ParametricFunction(lambda s: (DRIFT_W * s * s, MUZZLE[1] + h * s, 0),
                              t_range=(0, 1)).set_stroke(frame.INK, width=5)
    wind = [Arrow((-3.8, y, 0), (-1.6, y, 0), buff=0, stroke_width=5, color=frame.SECOND,
                  max_tip_length_to_length_ratio=0.2, tip_length=0.25) for y in WIND_YS]
    return VGroup(aim, path, *wind)


def drift():
    y = TARGET_Y + 0.3
    bar = VGroup(Line((0, y, 0), (DRIFT_W, y, 0)), Line((0, y - 0.15, 0), (0, y + 0.15, 0)),
                 Line((DRIFT_W, y - 0.15, 0), (DRIFT_W, y + 0.15, 0))).set_stroke(frame.ACCENT, width=5)
    return VGroup(bar, kit.text(f"{DRIFT_CM} cm", DRIFT_W + 0.3, y - 0.22, frame.ACCENT, align="left"))


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE)]
        steps = [self.step_flight, self.step_lag, self.step_mil]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_flight(self):
        return [FadeIn(flight())]

    def step_lag(self):
        return [FadeIn(VGroup(kit.text("drift = wind × lag", 0, FORMULA_ROWS[0]),
                              kit.text("lag = t − D ÷ v₀", 0, FORMULA_ROWS[1], frame.DIM)))]

    def step_mil(self):
        return [FadeIn(drift()),
                FadeIn(kit.chain([f"{DRIFT_CM} cm at {DIST_M} m", f"{DRIFT_CM} × 10 ÷ {DIST_M}",
                                  f"{drift_mil():g} MIL"], CHAIN_TOP, step=CHAIN_STEP,
                                 colors=(frame.ACCENT, frame.INK, frame.SECOND)))]

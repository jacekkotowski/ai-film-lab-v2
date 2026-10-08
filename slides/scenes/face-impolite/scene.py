"""face-impolite -- politeness climbs away from the bare threat;
impoliteness goes the other way, past "bald, on record".

Content: spec.md. Slide 6 of love-as-a-face-threatening-act. Brown and
Levinson's strategies as one ladder (bald at the bottom, "don't do it" at
the top); Culpeper's impoliteness below its bottom rung.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/face-impolite/out scenes/face-impolite/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Arrow, Create, FadeIn, GrowArrow, Line, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Soften or attack"
BALD = "bald, on record"
SOFTER = ("with redress", "off record", "don't do it")   # upwards
ATTACK = "impoliteness"

# ---- layout --------------------------------------------------------------
AXIS_X = -3.4                    # the ladder's line
LABEL_X = -2.6                   # labels start here (widest 5.98: ends 3.38)
TICK = 0.4                       # a rung's tick, right of the line
BALD_Y = 0.7                     # baselines; rungs 1.3 apart (>= 0.80)
SOFTER_Y = (2.0, 3.3, 4.6)
ATTACK_Y = -2.6
MID = 0.2                        # tick height above a baseline: lower-case middle
UP_TOP, DOWN_END = 5.4, ATTACK_Y + MID

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["impoliteness", "Bald", "soften", "opposite"]
BEAT_LINES = [3, 4, 5, 6]
RUN_TIMES = [1.0, 1.0, 1.5, 1.0]


def rung(label, y, color=frame.INK):
    tick = Line((AXIS_X, y + MID, 0), (AXIS_X + TICK, y + MID, 0)).set_stroke(color, 6)
    return VGroup(tick, kit.text(label, LABEL_X, y, color, align="left"))


class Slide(Scene):
    def construct(self):
        steps = [self.step_attack, self.step_bald, self.step_soften, self.step_opposite]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.title(TITLE)],
                beat_words=BEAT_WORDS)

    def step_attack(self):
        return [FadeIn(kit.text(ATTACK, LABEL_X, ATTACK_Y, frame.SICK, align="left"))]

    def step_bald(self):
        return [FadeIn(rung(BALD, BALD_Y))]

    def step_soften(self):
        up = Arrow((AXIS_X, BALD_Y + MID, 0), (AXIS_X, UP_TOP, 0), buff=0,
                   stroke_width=6, color=frame.DIM)
        rungs = VGroup(*[rung(s, y, frame.DIM) for s, y in zip(SOFTER, SOFTER_Y)])
        return [GrowArrow(up), FadeIn(rungs)]

    def step_opposite(self):
        down = Arrow((AXIS_X, BALD_Y + MID, 0), (AXIS_X, DOWN_END, 0), buff=0,
                     stroke_width=6, color=frame.SICK)
        return [Create(down)]

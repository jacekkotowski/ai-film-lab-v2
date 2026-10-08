"""face-fail -- the insults break Grice's maxims, and their stones hit
mianzi but stop at lian.

Content: spec.md. Slide 7 of love-as-a-face-threatening-act. The rings
are face-two's (aimanim/faces.py, I14).

    uv run --extra render manim -s -r 540,960 --media_dir scenes/face-fail/out scenes/face-fail/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Circle, Create, FadeIn, Scene, Transform, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402
from aimanim.faces import (CENTRE, INNER_R, LIAN_Y, MIANZI_Y, OUTER_R,  # noqa: E402
                           RING_W, on_circle)

# ---- content (from spec.md) ---------------------------------------------
TITLE = "They fail"
MIANZI, LIAN = "mianzi", "lian"
MAXIMS = (("quality", "false"), ("relation", "not now"))   # broken, why

# ---- layout --------------------------------------------------------------
MAXIM_Y = (-2.4, -3.4)           # baselines, 1.0 apart
NAME_X, WHY_X = -3.5, 0.4        # left edges ("relation" 3.03 ends -0.47)
STONE_R = 0.13
STONE_AT = (20, 160, 200, 245, 295, 340)   # degrees; none under "mianzi"
HIT_R = OUTER_R + STONE_R + 0.06           # just outside mianzi's ring
STOP_R = INNER_R + STONE_R + 0.06          # just outside lian's ring

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["quality", "relation", "aim", "cannot", "chooses"]
BEAT_LINES = [1, 2, 3, 4, 5]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0]


def ring(r, color):
    return Circle(radius=r).move_to((*CENTRE, 0)).set_stroke(color, RING_W)


def stones(r):
    # one VMobject per stone: one for all would box "lian" in (a false [layout] note)
    return VGroup(*[kit.dots([on_circle(r, a)], STONE_R, frame.SICK) for a in STONE_AT])


class Slide(Scene):
    def construct(self):
        self.inner = ring(INNER_R, frame.INK)
        self.lian = kit.text(LIAN, CENTRE[0], LIAN_Y)
        background = [kit.title(TITLE), ring(OUTER_R, frame.SECOND),
                      kit.text(MIANZI, CENTRE[0], MIANZI_Y, frame.SECOND),
                      self.inner, self.lian]
        steps = [lambda: self.maxim(0), lambda: self.maxim(1),
                 self.step_aim, self.step_stop, self.step_chooses]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def maxim(self, k):
        name, why = MAXIMS[k]
        t = kit.text(name, NAME_X, MAXIM_Y[k], align="left")
        return [FadeIn(t), Create(kit.strike(t, frame.SICK)),
                FadeIn(kit.text(why, WHY_X, MAXIM_Y[k], frame.SICK, align="left"))]

    def step_aim(self):
        self.stones = stones(HIT_R)
        return [FadeIn(self.stones, scale=1.4)]

    def step_stop(self):
        return [Transform(self.stones, stones(STOP_R))]

    def step_chooses(self):
        return [VGroup(self.inner, self.lian).animate.set_color(frame.ACCENT)]

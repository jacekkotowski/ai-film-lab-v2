"""mil-finale -- a MIL reticle is a measuring instrument.

Content: spec.md. Slide 8 of the mil-measure film. The whole Aurora MIL
(kit.reticle, as on mil-unit), and what the film measured with it.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/mil-finale/out scenes/mil-finale/scene.py Slide
"""

import sys
from pathlib import Path

from manim import FadeIn, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
WORDS = ["SIZE", "DISTANCE", "ANGLE", "MOVEMENT", "TRAJECTORY"]
LAST = ["A MIL reticle", "is a measuring", "instrument."]

# ---- layout --------------------------------------------------------------
# Safe area: x in [-SIDE, SIDE] = [-4, 4]; y in [BOTTOM, TOP] = [-4, 7].
S, AIM = 0.27, (0.0, 4.9)            # no title: the "2"s reach 6.93
WORD_TOP, WORD_STEP = 1.4, 0.7       # capitals, no descenders
LAST_TOP, LAST_STEP = -2.3, 0.75     # "instrument." ends on -3.8

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["size", "distance", "angle", "movement", "trajectory", "MIL|mil"]
BEAT_LINES = [0, 0, 0, 0, 0, 1]
RUN_TIMES = [0.5, 0.5, 0.5, 0.5, 0.5, 1.5]


class Slide(Scene):
    def construct(self):
        background = [kit.reticle(kit.mil_to(S, AIM))]
        steps = [self.word(i) for i in range(len(WORDS))] + [self.step_last]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def word(self, i):
        return lambda: [FadeIn(kit.text(WORDS[i], 0, WORD_TOP - i * WORD_STEP, frame.SECOND))]

    def step_last(self):
        return [FadeIn(VGroup(*[kit.text(s, 0, LAST_TOP - i * LAST_STEP, frame.ACCENT)
                                for i, s in enumerate(LAST)]))]

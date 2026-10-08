"""face-implied -- the threat is not in what is said but in what she
searches for under it: the implied request, the "?" weight of face-ledger.

Content: spec.md. Slide 4 of love-as-a-face-threatening-act. Speaker,
hearer and "I love you" stand where they stood on face-ledger; a line
splits "said" from "meant" (Grice).

    uv run --extra render manim -s -r 540,960 --media_dir scenes/face-implied/out scenes/face-implied/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Arrow, Create, FadeIn, Line, Rectangle, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402
# speaker, hearer and "I love you" where face-ledger has them (I14)
from aimanim.ledger import FEET, FIG_H, PERSON_X, SAID_Y  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Said and meant"
SAID = "I love you"
LAYERS = ("said", "meant")
ASKED = "?"
REQUEST = "implied request"

# ---- layout --------------------------------------------------------------
SPLIT_Y = 1.4                    # the line between said and meant
LAYER_Y = {"said": 1.6, "meant": 0.6}          # baselines, left on SIDE
WEIGHT_W, WEIGHT_H = 1.6, 1.4
WEIGHT_C = (0.0, -0.8)
ASK_SIZE = 120
REQUEST_Y = -2.4                 # baseline; 0.3 under the weight's bottom
SEARCH_FROM = (PERSON_X, FEET - 0.25)          # under the hearer's feet
SEARCH_TO = (WEIGHT_W / 2 + 0.15, WEIGHT_C[1] + WEIGHT_H / 2 + 0.1)
COLORS = (frame.ACCENT, frame.SECOND)

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["Grice", "search", "want", "implied"]
BEAT_LINES = [1, 4, 5, 7]
RUN_TIMES = [1.0, 1.0, 0.5, 1.0]


class Slide(Scene):
    def construct(self):
        people = VGroup(*[kit.man(FIG_H, (s * PERSON_X, FEET), COLORS[i])
                          for i, s in enumerate((-1, 1))])
        said = kit.text(SAID, 0, SAID_Y, frame.ACCENT)
        background = [kit.title(TITLE), people, said]
        steps = [self.step_split, self.step_search, self.step_ask, self.step_request]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_split(self):
        line = Line((-frame.SIDE, SPLIT_Y, 0), (frame.SIDE, SPLIT_Y, 0)).set_stroke(frame.DIM, 4)
        names = VGroup(*[kit.text(n, -frame.SIDE, LAYER_Y[n], frame.DIM, align="left")
                         for n in LAYERS])
        return [Create(line), FadeIn(names)]

    def step_search(self):
        arrow = Arrow((*SEARCH_FROM, 0), (*SEARCH_TO, 0), buff=0,
                      stroke_width=6, color=frame.SECOND)
        return [Create(arrow)]

    def step_ask(self):
        self.ask = kit.text(ASKED, WEIGHT_C[0], 0, frame.SICK, ASK_SIZE)
        self.ask.shift((0, WEIGHT_C[1] - self.ask.get_center()[1], 0)).set_z_index(1)
        return [FadeIn(self.ask)]

    def step_request(self):
        weight = (Rectangle(width=WEIGHT_W, height=WEIGHT_H).move_to((*WEIGHT_C, 0))
                  .set_fill(frame.SICK, 1).set_stroke(width=0))
        weight.strikes = self.ask        # meant to lie under this one text (I11)
        label = kit.text(REQUEST, 0, REQUEST_Y, frame.SICK)
        return [FadeIn(weight), self.ask.animate.set_color(frame.BACKGROUND),
                FadeIn(label)]

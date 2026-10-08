"""face-weight -- two faces to threaten, and the threat's weight is
distance + power + the size of the imposition.

Content: spec.md. Slide 2 of love-as-a-face-threatening-act. The bars and
the red weight are the ledger's (aimanim/ledger.py), so slide 03 reads
as this one put between two people.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/face-weight/out scenes/face-weight/scene.py Slide
"""

import sys
from pathlib import Path

from manim import DOWN, FadeIn, Rectangle, Scene, Transform, VGroup, Write

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402
from aimanim.ledger import ASK_SIZE, BAR_H, WEIGHT_H, WEIGHT_SHARE  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "The weight"
FACES = ("accepted", "free")         # positive, negative face
W = "W"
FORMULA = "W = D + P + R"
TERMS = (("D", "distance"), ("P", "power"), ("R", "imposition"))

# ---- layout --------------------------------------------------------------
BAR_L = 6.0                          # one person's bars, -3 to 3
HEAD_Y = {"accepted": 4.5, "free": 2.5}   # names (baselines)
BAR_Y = {"accepted": 3.8, "free": 1.8}    # bar centres
FORMULA_Y = -0.1
TERM_Y = (-1.3, -2.3, -3.3)          # baselines, 1.0 apart
LETTER_X, WORD_X = -3.6, -2.6        # left edges

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["accepted", "free", "touches", "distance", "power", "size"]
BEAT_LINES = [1, 2, 3, 4, 4, 4]
RUN_TIMES = [1.0, 1.0, 1.0, 0.5, 0.5, 0.5]


def bar(left, right, y, color=frame.SECOND):
    return (Rectangle(width=right - left, height=BAR_H)
            .move_to(((left + right) / 2, y, 0))
            .set_fill(color, 1).set_stroke(width=0))


class Slide(Scene):
    def construct(self):
        steps = [self.step_accepted, self.step_free, self.step_weight,
                 *[lambda k=k: self.step_term(k) for k in range(3)]]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.title(TITLE)],
                beat_words=BEAT_WORDS)

    def face(self, f):
        self.bars = getattr(self, "bars", {})
        self.bars[f] = bar(-BAR_L / 2, BAR_L / 2, BAR_Y[f])
        return [FadeIn(VGroup(kit.text(f, 0, HEAD_Y[f]), self.bars[f]))]

    def step_accepted(self):
        return self.face("accepted")

    def step_free(self):
        return self.face("free")

    def step_weight(self):
        y = BAR_Y["free"]
        cut = BAR_L / 2 - BAR_L * WEIGHT_SHARE        # 0.6
        w = (Rectangle(width=BAR_L * WEIGHT_SHARE, height=WEIGHT_H)
             .move_to(((cut + BAR_L / 2) / 2, y, 0))
             .set_fill(frame.SICK, 1).set_stroke(width=0))
        letter = kit.text(W, w.get_center()[0], 0, frame.BACKGROUND, ASK_SIZE)
        letter.shift((0, y - letter.get_center()[1], 0))
        w.strikes = letter           # meant to lie under this one text (I11)
        return [FadeIn(VGroup(w, letter), shift=0.8 * DOWN),
                Transform(self.bars["free"], bar(-BAR_L / 2, cut, y)),
                Write(kit.text(FORMULA, 0, FORMULA_Y, frame.SICK))]

    def step_term(self, k):
        letter, word = TERMS[k]
        return [FadeIn(VGroup(
            kit.text(letter, LETTER_X, TERM_Y[k], frame.SICK, align="left"),
            kit.text(word, WORD_X, TERM_Y[k], align="left")))]

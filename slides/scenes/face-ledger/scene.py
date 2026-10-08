"""face-ledger -- declaring love costs both people face: the speaker's
"accepted" goes on the table, the hearer's "free" takes a weight.

Content: spec.md. Slide 3 of love-as-a-face-threatening-act (the number is
a placeholder). Face drawn as a ledger: one bar per face per person
(Brown and Levinson's positive face = "accepted", negative = "free").
The lengths are a picture, not a measurement: face has no unit.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/face-ledger/out scenes/face-ledger/scene.py Slide
"""

import sys
from pathlib import Path

from manim import DOWN, FadeIn, Line, Rectangle, Scene, Transform, VGroup, Write

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402
# the people, table and bars are shared with slides 04 and 05 (I14)
from aimanim.ledger import (ASK_SIZE, BAR_H, BAR_IN, BAR_L, BAR_Y, FACES,  # noqa: E402
                            FEET, FIG_H, HEAD_Y, LEG_X, NAME_Y, PERSON_X,
                            SAID_Y, TABLE_HALF, TABLE_TOP, WEIGHT_H,
                            WEIGHT_SHARE, WHO, side)

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Declaring love"
SAID = "I love you"
ASKED = "?"
COLORS = (frame.ACCENT, frame.SECOND)

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["Declaring", "puts", "receives", "question"]
BEAT_LINES = [0, 2, 3, 4]
RUN_TIMES = [1.0, 1.5, 1.0, 0.5]


def bar(left, right, y, color):
    return (Rectangle(width=right - left, height=BAR_H)
            .move_to(((left + right) / 2, y, 0))
            .set_fill(color, 1).set_stroke(width=0))


class Slide(Scene):
    def construct(self):
        people = VGroup(*[kit.man(FIG_H, (side(i) * PERSON_X, FEET), COLORS[i])
                          for i in range(2)])
        names = VGroup(*[kit.text(WHO[i], side(i) * PERSON_X, NAME_Y, COLORS[i])
                         for i in range(2)])
        table = VGroup(Line((-TABLE_HALF, TABLE_TOP, 0), (TABLE_HALF, TABLE_TOP, 0)),
                       *[Line((x, TABLE_TOP, 0), (x, FEET, 0)) for x in (-LEG_X, LEG_X)]
                       ).set_stroke(frame.DIM, 6)
        rows = VGroup(*[kit.text(f, 0, HEAD_Y[f]) for f in FACES])
        self.bars = {(i, f): bar(*sorted((side(i) * BAR_IN, side(i) * (BAR_IN + BAR_L))),
                                 BAR_Y[f], COLORS[i])
                     for i in range(2) for f in FACES}
        background = [kit.title(TITLE), people, names, table, rows, *self.bars.values()]
        steps = [self.step_said, self.step_stake, self.step_weight, self.step_question]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_said(self):
        return [Write(kit.text(SAID, 0, SAID_Y, frame.ACCENT))]

    def step_stake(self):
        b = self.bars[(0, "accepted")]
        y = BAR_Y["accepted"]
        left, right = -(BAR_IN + BAR_L), -BAR_IN
        slot = kit.box(left, y - BAR_H / 2, right, y + BAR_H / 2, frame.ACCENT, 3)
        return [b.animate.move_to((0, TABLE_TOP + BAR_H / 2 + 0.03, 0)), FadeIn(slot)]

    def step_weight(self):
        y = BAR_Y["free"]
        cut = BAR_IN + BAR_L * (1 - WEIGHT_SHARE)          # 2.7
        self.weight = (Rectangle(width=BAR_L * WEIGHT_SHARE, height=WEIGHT_H)
                       .move_to(((cut + BAR_IN + BAR_L) / 2, y, 0))
                       .set_fill(frame.SICK, 1).set_stroke(width=0))
        return [FadeIn(self.weight, shift=0.8 * DOWN),
                Transform(self.bars[(1, "free")], bar(BAR_IN, cut, y, COLORS[1]))]

    def step_question(self):
        w = self.weight
        ask = kit.text(ASKED, w.get_center()[0], 0, frame.BACKGROUND, ASK_SIZE)
        ask.shift((0, w.get_center()[1] - ask.get_center()[1], 0))
        w.strikes = ask          # meant to lie under this one text (I11)
        return [FadeIn(ask)]

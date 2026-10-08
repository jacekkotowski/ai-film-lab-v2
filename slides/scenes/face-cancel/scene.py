"""face-cancel -- the implied request can be cancelled: the "?" is struck,
the weight lifts off the hearer's "free" and lands on the speaker's.

Content: spec.md. Slide 5 of love-as-a-face-threatening-act. It opens on
face-ledger's last picture (same people, table, bars, weight), so the two
slides read as one ledger.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/face-cancel/out scenes/face-cancel/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Create, Line, Rectangle, Scene, Transform, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402
# the people, table, bars and weight of slides 03 and 04 (I14)
from aimanim.ledger import (ASK_SIZE, BAR_H, BAR_IN, BAR_L, BAR_Y, FACES,  # noqa: E402
                            FEET, FIG_H, HEAD_Y, LEG_X, NAME_Y, PERSON_X,
                            SAID_Y, TABLE_HALF, TABLE_TOP, WEIGHT_H,
                            WEIGHT_SHARE, WHO, bar_span, side, weight_span)

# ---- content (from spec.md) ---------------------------------------------
TITLE = "The way out"
SAID = "I love you"
ASKED = "?"
COLORS = (frame.ACCENT, frame.SECOND)

# ---- layout --------------------------------------------------------------
KEPT = BAR_L * (1 - WEIGHT_SHARE)    # 1.8 of 3.0: a "free" bar under the weight
GONE_C = (0.0, -2.8)                 # the weight between the two "free" bars,
                                     # its top 0.29 under the word "free"

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["cancelled", "gone", "pays"]
BEAT_LINES = [1, 7, 8]
RUN_TIMES = [0.5, 1.0, 1.0]


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
        said = kit.text(SAID, 0, SAID_Y, frame.ACCENT)
        rows = VGroup(*[kit.text(f, 0, HEAD_Y[f]) for f in FACES])
        # face-ledger's end: his "accepted" on the table, its empty slot,
        # her "free" cut where the weight sits
        y = BAR_Y["accepted"]
        staked = bar(-BAR_L / 2, BAR_L / 2, TABLE_TOP + BAR_H / 2 + 0.03, COLORS[0])
        left, right = bar_span(0)
        slot = kit.box(left, y - BAR_H / 2, right, y + BAR_H / 2, frame.ACCENT, 3)
        self.bars = {(1, "accepted"): bar(*bar_span(1), y, COLORS[1]),
                     (0, "free"): bar(*bar_span(0), BAR_Y["free"], COLORS[0]),
                     (1, "free"): bar(*bar_span(1, KEPT), BAR_Y["free"], COLORS[1])}
        left, right = weight_span(1)
        w = (Rectangle(width=right - left, height=WEIGHT_H)
             .move_to(((left + right) / 2, BAR_Y["free"], 0))
             .set_fill(frame.SICK, 1).set_stroke(width=0))
        self.ask = kit.text(ASKED, w.get_center()[0], 0, frame.BACKGROUND, ASK_SIZE)
        self.ask.shift((0, w.get_center()[1] - self.ask.get_center()[1], 0))
        w.strikes = self.ask         # meant to lie under this one text (I11)
        self.weight = VGroup(w, self.ask)
        background = [kit.title(TITLE), people, names, table, said, rows,
                      staked, slot, *self.bars.values(), self.weight]
        steps = [self.step_cancel, self.step_gone, self.step_pays]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_cancel(self):
        line = kit.strike(self.ask, frame.INK)
        self.weight.add(line)        # the struck "?" travels with its weight
        return [Create(line)]

    def step_gone(self):
        y = BAR_Y["free"]
        return [self.weight.animate.move_to((*GONE_C, 0)),
                Transform(self.bars[(1, "free")], bar(*bar_span(1), y, COLORS[1]))]

    def step_pays(self):
        y = BAR_Y["free"]
        left, right = weight_span(0)
        return [self.weight.animate.move_to(((left + right) / 2, y, 0)),
                Transform(self.bars[(0, "free")], bar(*bar_span(0, KEPT), y, COLORS[0]))]

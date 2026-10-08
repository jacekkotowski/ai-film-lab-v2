"""face-cost -- the insult takes a piece of her face and costs the speaker
nothing; the declaration gives a piece of his away.

Content: spec.md. Slide 10 of love-as-a-face-threatening-act. Two small
ledgers, one above the other, with the bars of aimanim/ledger.py (speaker
left, hearer right, growing outwards from BAR_IN), shorter so a moved
piece fits inside the frame.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/face-cost/out scenes/face-cost/scene.py Slide
"""

import sys
from pathlib import Path

from manim import FadeIn, Rectangle, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402
from aimanim.ledger import BAR_H, BAR_IN, WHO, side  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Who pays"
COLORS = (frame.ACCENT, frame.SECOND)
ACTS = (("insult", "cheap", frame.SICK), ("declaration", "expensive", frame.ACCENT))

# ---- layout --------------------------------------------------------------
BAR_L, PIECE = 2.0, 0.9          # a face (0.9 to 2.9 out), the piece that moves
KEEP = BAR_L - PIECE             # 1.1 stays
GAP = 0.05                       # between a moved piece and the bar it joins
NAME_X = 1.9                     # speaker at -1.9, hearer at +1.9
# per act: (its name, the people's names, bars' centre, its price), baselines
ROWS = ((4.6, 3.6, 2.9, 1.8), (0.2, -0.8, -1.5, -2.6))

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["insult", "takes", "declaration", "everything"]
BEAT_LINES = [0, 1, 2, 3]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0]


def out(i, d):
    """x at distance d out from where person i's bar starts (BAR_IN)."""
    return side(i) * (BAR_IN + d)


def bar(i, d0, d1, y, color):
    """Person i's bar from d0 to d1 out, centred on y."""
    left, right = sorted((out(i, d0), out(i, d1)))
    return (Rectangle(width=right - left, height=BAR_H)
            .move_to(((left + right) / 2, y, 0))
            .set_fill(color, 1).set_stroke(width=0))


class Slide(Scene):
    def construct(self):
        self.pieces = {}
        steps = [lambda: self.act(0), lambda: self.move(0, 1),
                 lambda: self.act(1), lambda: self.move(1, 0)]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.title(TITLE)],
                beat_words=BEAT_WORDS)

    def act(self, a):
        """Act a's ledger: its name, the two people, their bars, its price.
        Each bar is the part that stays and its outer PIECE."""
        name, price, color = ACTS[a]
        top, names_y, y, price_y = ROWS[a]
        parts = [kit.text(name, 0, top, color), kit.text(price, 0, price_y, color)]
        for i in range(2):
            self.pieces[(a, i)] = bar(i, KEEP, BAR_L, y, COLORS[i])
            parts += [kit.text(WHO[i], side(i) * NAME_X, names_y, COLORS[i]),
                      bar(i, 0, KEEP, y, COLORS[i]), self.pieces[(a, i)]]
        return [FadeIn(VGroup(*parts))]

    def move(self, a, giver):
        """The giver's piece goes to the outer end of the other's bar; an
        empty slot is left where it was."""
        y = ROWS[a][2]
        lo, hi = sorted((out(giver, KEEP + GAP), out(giver, BAR_L)))
        slot = kit.box(lo, y - BAR_H / 2, hi, y + BAR_H / 2, COLORS[giver], 3)
        end = out(1 - giver, BAR_L + GAP + PIECE / 2)
        return [self.pieces[(a, giver)].animate.move_to((end, y, 0)), FadeIn(slot)]

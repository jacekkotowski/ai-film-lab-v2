"""mil-plate -- a 50 cm plate filling 2 mil is 250 m away.

Content: spec.md. Slide 3 of the mil-measure film. The centre of the
Aurora MIL's horizontal line (kit.reticle, a window of it), enlarged.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/mil-plate/out scenes/mil-plate/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Circle, FadeIn, Line, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Range by size"
PLATE_M = 0.50
READING = 2                          # mil, dot -1 to dot +1


def metres() -> int:
    return round(PLATE_M * 1000 / READING)   # 250


# ---- layout --------------------------------------------------------------
# Safe area: x in [-SIDE, SIDE] = [-4, 4]; y in [BOTTOM, TOP] = [-4, 7].
S, AIM = 1.1, (0.0, 3.9)             # dots to ±3 mil = ±3.3 units
WINDOW = (-3.4, 3.4, -0.85, 0.4)     # the line and chevron; no ladder
BRACKET_GAP = 0.5                    # the 2 mil bracket, this far under the plate
CAP = 0.15
CHAIN_FONT, CHAIN_TOP = 64, 0.6      # "0.50 × 1000 ÷ 2" 7.28 wide at 64
CHAIN_STEP = 1.4                     # 4 rows from 0.6 to -3.6

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["plate", "fills", "Half"]
BEAT_LINES = [0, 1, 2]
RUN_TIMES = [1.0, 1.0, 1.5]

at = kit.mil_to(S, AIM)


def chain():
    return kit.chain([f"{round(PLATE_M * 100)} cm", f"{READING} MIL",
                      f"{PLATE_M:.2f} × 1000 ÷ {READING}", f"{metres()} m"],
                     CHAIN_TOP, step=CHAIN_STEP, size=CHAIN_FONT)


def plate():
    c = Circle(radius=READING / 2 * S).move_to(at(0, 0))
    return c.set_fill(frame.ACCENT, opacity=0.35).set_stroke(frame.ACCENT, width=4).set_z_index(-1)


def bracket():
    l, r = at(-READING / 2, 0)[0], at(READING / 2, 0)[0]
    y = at(0, -READING / 2)[1] - BRACKET_GAP
    return VGroup(Line((l, y, 0), (r, y, 0)), Line((l, y, 0), (l, y + CAP * 2, 0)),
                  Line((r, y, 0), (r, y + CAP * 2, 0))).set_stroke(frame.SECOND, width=5)


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE),
                      kit.reticle(at, WINDOW, stroke=6, dot_r=0.09, numbers=False)]
        steps = [self.step_plate, self.step_reading, self.step_range]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_plate(self):
        return [FadeIn(plate()), FadeIn(chain()[0])]

    def step_reading(self):
        return [FadeIn(bracket()), FadeIn(chain()[1])]

    def step_range(self):
        return [FadeIn(VGroup(*chain()[2:]))]

"""obs-rec -- slide 03 Target coordinates: position, distance, azimuth -> Rec -> the target's E and N.

Film: Map and Calculator 01 - Observer. Content: his plan,
film/docs/plans/2026-10-11/PLAN-map-calculator.md (slide 03), numbers
computed here. x of Rec is the step north, y the step east (the angle is an
azimuth). Pieces come one after another on his words; the still is the end of B.

The map is the background from "2400" to the end (his choice, 2026-10-11:
the viewer must see the map the numbers come from). Keys, screens and cards
stand on the bottom edge over it, one at a time; ME, the line and TARGET sit
in the band between the headline and the tallest of them (the B card).
Grid numbers and labels a panel would cover fade with it.

    uv run --directory slides python -m aimanim.look still obs-rec full
"""

import math
import sys
from pathlib import Path

from manim import UP, FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (his plan, slide 03) -------------------------------------------
SERIES = "MAP AND CALCULATOR · 01 · OBSERVER"
ME = (34500, 21800)                               # E, N in metres
D, AZ = 2400, 65                                  # rangefinder (m), map azimuth (deg)
A_TAG, A_HEAD = "SLIDE 3 · A", "I see the target"
A_SUB = "Your position, the rangefinder distance, the map azimuth."
A_FOOT = "Comma: SHIFT + )"
B_TAG, B_HEAD = "SLIDE 3 · B", "Add the shifts"
B_SUB = "x is the step north, y the step east."
B_FOOT = "✓ North-east: x and y positive"

X = D * math.cos(math.radians(AZ))                # 1014.283828, north
Y = D * math.sin(math.radians(AZ))                # 2175.138689, east
TARGET = (ME[0] + round(Y), ME[1] + round(X))     # E 36675, N 22814

# ---- layout ----------------------------------------------------------------
SCALE = 0.00095                                   # frame units per metre: TARGET's label
ME_X, ME_Y = -1.1, 3.47                           # under the headline, ME's over the B card
GRID = dict(e0=33000, e1=39000, n0=15000, n1=23000, left=ME_X - 1500 * SCALE,
            bottom=ME_Y - (ME[1] - 15000) * SCALE, scale=SCALE)
KEEP_N = (21, 22)                                 # N numbers left in view over the panels
E_EVERY = 2                                       # km between E numbers: 0.95 apart they touch
GAP = 0.3                                         # between stacked panels
FLOOR = frame.BOTTOM + 0.05                       # the panels stand here

# ---- timing ----------------------------------------------------------------
# Each step on its word in [03] of slides.script.txt (his narration, approved 2026-10-11).
BEAT_WORDS = ["I", "position", "2400|two", "Press", "is", "Add", "step", "Equals",
              "legs", "them", "North"]
BEAT_LINES = [0, 1, 1, 2, 3, 4, 4, 5, 5, 6, 7]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def stack_up(*mobs, floor: float = FLOOR) -> None:
    """Stand the mobjects one on another, the first on `floor`."""
    y = floor
    for m in mobs:
        m.shift(UP * (y - m.get_bottom()[1]))
        y = m.get_top()[1] + GAP


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        e, n = TARGET
        # the map: the grid, its numbers, and what is drawn on it
        g, at = kit.map_grid(**GRID)
        lines, nums = g[0], g[1]
        cols = list(range(GRID["e0"] // 1000, GRID["e1"] // 1000 + 1))
        n_rows = list(range(GRID["n0"] // 1000, GRID["n1"] // 1000 + 1))
        row = dict(zip(n_rows, nums[len(cols):len(cols) + len(n_rows)]))
        e_nums = [m for k, m in zip(cols, nums) if k % E_EVERY == 0] + [nums[-2]]  # and "E"
        self.grid = VGroup(lines, *e_nums,
                           *[row[k] for k in n_rows[:-1]])            # top row under the headline
        self.covered = VGroup(*e_nums, *[row[k] for k in n_rows[:-1] if k not in KEEP_N])
        self.low_n = VGroup(*[row[k] for k in KEEP_N if k != max(KEEP_N)])
        corner = (ME[0], TARGET[1])
        self.line = kit.map_line(at, ME, TARGET)
        self.d_label = kit.map_line(at, ME, TARGET, f"{D} m", side=-1, where=0.95)[1]
        self.arc = kit.azimuth_arc(at, ME, AZ, 0.6, f"{AZ}°", label_at=130)
        self.az_label = self.arc[-1]
        self.me = kit.map_point(at, *ME, "ME", kit.PAPER, "left")
        self.legs = VGroup(kit.map_line(at, ME, corner, None, kit.MUTED, dashed=True),
                           kit.map_line(at, corner, TARGET, None, kit.MUTED, dashed=True))
        self.target = kit.map_point(at, *TARGET, "TARGET", kit.GREEN, "right")

        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.a_sub = kit.note(A_SUB, kit.below(self.a_top[1]))
        self.a_card = kit.card([f"ME\nE {ME[0]} · N {ME[1]}", f"D {D} m", f"Az {AZ}°"],
                               self.a_sub.get_bottom()[1] - GAP)
        self.keys = kit.keys(["SHIFT", "−"], 0, sep="+", then="Rec(")
        self.a_screen = kit.screen(f"Rec({D},{AZ})", rows=2)
        self.a_foot = kit.note(A_FOOT, 0)
        stack_up(self.a_foot, self.a_screen, self.keys)
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.b_screen = kit.screen(f"Rec({D},{AZ})", [f"x={X:.10g}", f"y={Y:.10g}"])
        self.b_screen.shift(UP * (self.a_screen.get_top()[1] - self.b_screen.get_top()[1]))
        self.b_sub = kit.note(B_SUB, 0)
        stack_up(self.b_sub, floor=self.a_screen.get_top()[1] + GAP)
        self.b_card = kit.card([f"E {ME[0]} + {round(Y)}\n= {e}",
                                f"N {ME[1]} + {round(X)}\n= {n}",
                                f"TARGET\nE {e} · N {n}"], 0, hl=2)
        self.b_foot = kit.note(B_FOOT, 0, kit.GREEN)
        stack_up(self.b_foot, self.b_card)
        steps = [self.a_head, self.a_says, self.a_map_in, self.a_keys,
                 self.a_comma, self.b_head, self.b_says, self.b_results, self.b_legs,
                 self.b_card_in, self.b_ok]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    # ---- A: I see the target ----------------------------------------------
    def a_head(self):
        return [FadeIn(self.a_top)]

    def a_says(self):                              # his three inputs and their values
        return [FadeIn(self.a_sub), FadeIn(self.a_card)]

    def a_map_in(self):                            # the same three, on the map
        return [FadeOut(VGroup(self.a_sub, self.a_card)),
                FadeIn(VGroup(self.grid, self.line, self.d_label, self.arc, self.me))]

    def a_keys(self):
        return [FadeOut(self.covered), FadeIn(self.keys), FadeIn(self.a_screen)]

    def a_comma(self):
        return [FadeIn(self.a_foot)]

    # ---- B: add the shifts -------------------------------------------------
    def b_head(self):
        return [FadeOut(VGroup(self.a_top, self.keys, self.a_foot)), FadeIn(self.b_top)]

    def b_says(self):                              # the subline covers the map's lower band
        return [FadeOut(VGroup(self.az_label, self.low_n)), FadeIn(self.b_sub)]

    def b_results(self):
        return [FadeOut(self.a_screen), FadeIn(self.b_screen)]

    def b_legs(self):                              # "the two legs on the map"
        return [FadeOut(self.d_label), FadeIn(VGroup(self.legs, self.target))]

    def b_card_in(self):
        return [FadeOut(VGroup(self.b_sub, self.b_screen)), FadeIn(self.b_card)]

    def b_ok(self):
        return [FadeIn(self.b_foot)]

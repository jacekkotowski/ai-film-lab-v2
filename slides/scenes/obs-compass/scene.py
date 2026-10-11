"""obs-compass -- slide 02 Compass and map: a compass gives a magnetic azimuth; add the correction.

Film: Map and Calculator 01 - Observer. Content: his plan,
film/docs/plans/2026-10-11/PLAN-map-calculator.md (slide 02). The two norths
are the map's margin; no number for the correction (it depends on the
sheet). Pieces come one after another on his words; the still is the end of B.

B shows a map sheet from "margin" to the end (his ask, 2026-10-11): its
kilometre grid at the top, the border round it, and the two norths in the
margin under the grid, where his words say the correction is printed.

    uv run --directory slides python -m aimanim.look still obs-compass full
"""

import sys
from pathlib import Path

from manim import UP, FadeIn, FadeOut, Rectangle, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (his plan, slide 02) -------------------------------------------
SERIES = "MAP AND CALCULATOR · 01 · OBSERVER"
A_TAG, A_HEAD = "SLIDE 2 · A", "The compass isn't the map"
A_SUB = "A compass gives a magnetic azimuth."
A_FOOT = "✗ Don't type it in as it is"
NEEDLE = 61                                       # degrees, the compass reading
B_TAG, B_HEAD = "SLIDE 2 · B", "Add the correction"
B_SUB = "Its value and sign are in the map margin."
FORMULA = ["Map azimuth =\ncompass azimuth\n+ correction"]
B_FOOT = "✓ From here on, only the map azimuth"

# ---- layout ----------------------------------------------------------------
DIAL, DIAL_R = (0, 1.0), 2.3          # top 3.3, under a two-line headline (3.61)
A_FOOT_B = -2.3
GRID = dict(e0=32000, e1=38000, n0=21000, n1=23000, left=-2.6, bottom=1.6,
            scale=0.00095)            # the sheet's top: 6 x 2 km under the headline
SHEET_TOP = 3.62                      # the border, just over the grid's top line
NORTH_X, NORTH_TIP, NORTH_DEG = -0.4, 1.3, 12     # tips under the grid; no number
NORTH_ARC = 0.28                      # "correction" clears "Magnetic north" (0.45: touched)
GAP = 0.3
FLOOR = frame.BOTTOM + 0.05

# ---- timing ----------------------------------------------------------------
# Each step on its word in [02] of slides.script.txt (his narration, approved 2026-10-11).
BEAT_WORDS = ["The", "gives", "61|sixty", "type", "Add", "value", "margin", "equals", "From"]
BEAT_LINES = [0, 1, 1, 2, 3, 3, 3, 4, 5]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.a_sub = kit.note(A_SUB, kit.below(self.a_top[1]))
        self.dial = kit.compass(DIAL, DIAL_R, NEEDLE)
        self.a_foot = kit.note(A_FOOT, A_FOOT_B, kit.ORANGE)
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.b_sub = kit.note(B_SUB, kit.below(self.b_top[1]))
        # the formula stands on the floor; at the end it rises for the ✓ line
        self.card = kit.card(FORMULA, 0)
        self.card.shift(UP * (FLOOR - self.card.get_bottom()[1]))
        self.b_foot = kit.note(B_FOOT, 0, kit.GREEN)
        self.b_foot.shift(UP * (FLOOR - self.b_foot.get_bottom()[1]))
        self.lift = self.b_foot.get_top()[1] + GAP - self.card.get_bottom()[1]
        # the sheet: grid and N numbers (an E row would cost the norths 0.85),
        # the border, the norths in its margin
        g, at = kit.map_grid(**GRID)
        lines, nums = g[0], g[1]
        cols = list(range(GRID["e0"] // 1000, GRID["e1"] // 1000 + 1))
        n_rows = list(range(GRID["n0"] // 1000, GRID["n1"] // 1000 + 1))
        n_nums = nums[len(cols):len(cols) + len(n_rows) - 1]          # top row: the headline's
        origin_y = self.card.get_top()[1] + GAP
        border = Rectangle(width=2 * frame.SIDE - 0.1, height=SHEET_TOP - origin_y + GAP)
        border.move_to((0, (SHEET_TOP + origin_y - GAP) / 2, 0)).set_stroke(kit.RULE, 4)
        self.sheet = VGroup(kit.under(border), lines, *n_nums)
        self.norths = kit.norths((NORTH_X, origin_y), NORTH_TIP - origin_y, NORTH_DEG,
                                 arc_r=NORTH_ARC)
        steps = [self.a_head, self.a_says, self.a_shows, self.a_warns,
                 self.b_head, self.b_says, self.b_shows, self.b_formula, self.b_ok]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    # ---- A: the compass isn't the map -------------------------------------
    def a_head(self):
        return [FadeIn(self.a_top)]

    def a_says(self):
        return [FadeIn(self.a_sub)]

    def a_shows(self):
        return [FadeOut(self.a_sub), FadeIn(self.dial)]

    def a_warns(self):
        return [FadeIn(self.a_foot)]

    # ---- B: add the correction --------------------------------------------
    def b_head(self):
        return [FadeOut(VGroup(self.a_top, self.dial, self.a_foot)), FadeIn(self.b_top)]

    def b_says(self):
        return [FadeIn(self.b_sub)]

    def b_shows(self):                             # "in the map margin"
        return [FadeOut(self.b_sub), FadeIn(self.sheet), FadeIn(self.norths)]

    def b_formula(self):
        return [FadeIn(self.card)]

    def b_ok(self):
        return [FadeOut(self.norths), self.card.animate.shift(UP * self.lift),
                FadeIn(self.b_foot)]

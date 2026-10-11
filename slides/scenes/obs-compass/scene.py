"""obs-compass -- slide 02 Compass and map: a compass gives a magnetic azimuth; add the correction.

Film: Map and Calculator 01 - Observer. Content: his plan,
film/docs/plans/2026-10-11/PLAN-map-calculator.md (slide 02). The two norths
are the map's margin; no number for the correction (it depends on the
sheet). Pieces come one after another on his words; the still is the end of B.

    uv run --directory slides python -m aimanim.look still obs-compass full
"""

import sys
from pathlib import Path

from manim import UP, FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import kit  # noqa: E402

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
NORTH_O, NORTH_L, NORTH_DEG = (-1.2, -0.7), 4.0, 12   # drawn angle only: no number
CARD_TOP = -1.0                       # under the norths' origin

# ---- timing ----------------------------------------------------------------
# Each step on its word in [02] of slides.script.txt (Claude's draft, 2026-10-11).
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
        self.norths = kit.norths(NORTH_O, NORTH_L, NORTH_DEG)
        self.card = kit.card(FORMULA, CARD_TOP)
        # at the end the formula moves up under the headline, the footer under it
        self.lift = self.b_top[1].get_bottom()[1] - 0.3 - CARD_TOP
        lifted_bottom = self.card.get_bottom()[1] + self.lift
        self.b_foot = kit.note(B_FOOT, lifted_bottom - 0.3 - kit.cap(56, kit.SANS), kit.GREEN)
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

    def b_shows(self):
        return [FadeOut(self.b_sub), FadeIn(self.norths)]

    def b_formula(self):
        return [FadeIn(self.card)]

    def b_ok(self):
        return [FadeOut(self.norths), self.card.animate.shift(UP * self.lift),
                FadeIn(self.b_foot)]

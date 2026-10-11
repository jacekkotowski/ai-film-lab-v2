"""obs-correction -- slide 05 Fire correction: the burst 20 mils left at 3 km -> RIGHT 60.

Film: Map and Calculator 01 - Observer. Content: his plan,
film/docs/plans/2026-10-11/PLAN-map-calculator.md (slide 05), numbers
computed here. W (m) = D (km) × mils: 1 mil ≈ 1 m at 1 km (exact 58.9 m).
Pieces come one after another on his words; the still is the end of B.

    uv run --directory slides python -m aimanim.look still obs-correction full
"""

import sys
from pathlib import Path

from manim import FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import kit  # noqa: E402

# ---- content (his plan, slide 05) -------------------------------------------
SERIES = "MAP AND CALCULATOR · 01 · OBSERVER"
MILS, KM = 20, 3                                  # burst left of the target, distance
A_TAG, A_HEAD = "SLIDE 5 · A", "The round missed"
A_SUB = f"Burst {MILS} mils left, target {KM} km from you."
CAPTION = "view through binoculars"
FORMULA = ["W (m) =\nD (km) × mils"]
A_FOOT = "1 mil ≈ 1 m at 1 km"
B_TAG, B_HEAD = "SLIDE 5 · B", "Send the opposite"
B_SUB = f"{KM} × {MILS} = {KM * MILS} metres."
COMMAND = f"RIGHT {KM * MILS}"                    # the burst was left
RULES = ["Too far → DROP", "Too short → ADD"]
B_FOOT = "✓ Always opposite the burst"

# ---- layout ----------------------------------------------------------------
VIEW, VIEW_R, PER_MIL = (0, 0.65), 2.75, 0.07     # field top 3.4; "20 mils" inside it

# ---- timing ----------------------------------------------------------------
# Each step on its word in [05] of slides.script.txt (Claude's draft, 2026-10-11).
BEAT_WORDS = ["The", "Burst", "target", "Metres", "about", "Send", "times", "call",
              "far", "Always"]
BEAT_LINES = [0, 1, 1, 2, 2, 3, 3, 3, 4, 6]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.a_sub = kit.note(A_SUB, kit.below(self.a_top[1]))
        self.view = kit.burst_view(VIEW, VIEW_R, MILS, PER_MIL, side=-1, caption=CAPTION)
        self.a_card = kit.card(FORMULA, self.a_top[1].get_bottom()[1] - 0.3)
        self.a_foot = kit.note(A_FOOT, kit.below(self.a_card))
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.b_sub = kit.note(B_SUB, kit.below(self.b_top[1]))
        h = kit.cap(120, kit.MONO) + 0.7                  # the command's box
        self.command = kit.command(COMMAND, self.b_sub.get_bottom()[1] - 0.35 - h / 2)
        self.b_card = kit.card(RULES, self.command.get_bottom()[1] - 0.35)
        self.b_foot = kit.note(B_FOOT, kit.below(self.b_card), kit.GREEN)
        steps = [self.a_head, self.a_says, self.a_shows, self.a_formula, self.a_rule,
                 self.b_head, self.b_says, self.b_command, self.b_rules, self.b_ok]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    # ---- A: the round missed ----------------------------------------------
    def a_head(self):
        return [FadeIn(self.a_top)]

    def a_says(self):
        return [FadeIn(self.a_sub)]

    def a_shows(self):
        return [FadeOut(self.a_sub), FadeIn(self.view)]

    def a_formula(self):
        return [FadeOut(self.view), FadeIn(self.a_card)]

    def a_rule(self):
        return [FadeIn(self.a_foot)]

    # ---- B: send the opposite ---------------------------------------------
    def b_head(self):
        return [FadeOut(VGroup(self.a_top, self.a_card, self.a_foot)), FadeIn(self.b_top)]

    def b_says(self):
        return [FadeIn(self.b_sub)]

    def b_command(self):
        return [FadeIn(self.command)]

    def b_rules(self):
        return [FadeIn(self.b_card)]

    def b_ok(self):
        return [FadeIn(self.b_foot)]

"""obs-mode -- slide 01 Degree mode: R on the screen gives wrong angles; SHIFT, MENU, 2, 1 sets D.

Film: Map and Calculator 01 - Observer. Content: his plan,
film/docs/plans/2026-10-11/PLAN-map-calculator.md (slide 01). His texts do not
fit one frame at 56, so the pieces come one after another on his words (his
yes, 2026-10-11); the still is the end of B.

    uv run --directory slides python -m aimanim.look still obs-mode full
"""

import math
import sys
from pathlib import Path

from manim import FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import kit  # noqa: E402

# ---- content (his plan, slide 01) -------------------------------------------
SERIES = "MAP AND CALCULATOR · 01 · OBSERVER"
A_TAG, A_HEAD = "SLIDE 1 · A", "Wrong mode, wrong answer"
A_SUB = "R on the screen: the calculator works in radians."
A_FOOT = "✗ R on the screen = wrong angles"
B_TAG, B_HEAD = "SLIDE 1 · B", "Set degrees"
B_SUB = "SHIFT, MENU, then 2 and 1."
B_KEYS = ["SHIFT", "MENU", "2", "1"]
B_FOOT = "✓ D on the screen"
EXPR = "tan(45)"
WRONG = f"{math.tan(45):.10g}"                    # 1.619775191: 45 taken as radians
RIGHT = f"{math.tan(math.radians(45)):.10g}"      # 1

# ---- layout ----------------------------------------------------------------
KEYS_Y = 3.6          # two rows (9.0 wide in one): 3.6 and 2.3, under a one-line headline
SCREEN_TOP = 1.35     # under the keys; the same place in A and B
FOOT_B = -2.8

# ---- timing ----------------------------------------------------------------
# One step per piece, on its word in [01] of slides.script.txt (Claude's
# draft, 2026-10-11): the keys appear with SHIFT lit, then light one a word.
BEAT_WORDS = ["Wrong", "means", "tan", "not", "Set", "SHIFT", "MENU", "two|2",
              "one|1", "Now", "tan"]
BEAT_LINES = [0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3]
RUN_TIMES = [1.0, 1.0, 1.0, 0.8, 1.0, 0.4, 0.3, 0.3, 0.3, 1.0, 1.0]


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.a_sub = kit.note(A_SUB, kit.below(self.a_top[1]))
        self.a_screen = kit.screen(EXPR, [WRONG], ind="R", bad=True, top=SCREEN_TOP)
        self.a_foot = kit.note(A_FOOT, FOOT_B, kit.ORANGE)
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.b_sub = kit.note(B_SUB, kit.below(self.b_top[1]))
        self.keys = kit.keys(B_KEYS, KEYS_Y)
        self.b_screen = kit.screen(EXPR, [RIGHT], top=SCREEN_TOP)
        self.b_foot = kit.note(B_FOOT, FOOT_B, kit.GREEN)
        background = [kit.series_tag(SERIES)]
        steps = [self.a_head, self.a_says, self.a_shows, self.a_warns,
                 self.b_head, self.b_keys,
                 *[self.press(i) for i in range(1, len(B_KEYS))],
                 self.b_shows, self.b_ok]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS, check_each=True)

    # ---- A: wrong mode -----------------------------------------------------
    def a_head(self):
        return [FadeIn(self.a_top)]

    def a_says(self):
        return [FadeIn(self.a_sub)]

    def a_shows(self):
        return [FadeOut(self.a_sub), FadeIn(self.a_screen)]

    def a_warns(self):
        return [FadeIn(self.a_foot)]

    # ---- B: set degrees ----------------------------------------------------
    def b_head(self):
        return [FadeOut(VGroup(self.a_top, self.a_foot)), FadeIn(self.b_top), FadeIn(self.b_sub)]

    def b_keys(self):                              # on "SHIFT": SHIFT is lit as they come
        kit.lit(self.keys.caps[0])
        return [FadeOut(self.b_sub), FadeIn(self.keys)]

    def press(self, i):
        return lambda: [kit.light(self.keys.caps[i])]

    def b_shows(self):
        return [FadeOut(self.a_screen), FadeIn(self.b_screen)]

    def b_ok(self):
        return [FadeIn(self.b_foot)]

"""sr-anger -- slide 06 Anger's weight: the angry emoji at five points,
more misinformation, a Polish party at 80 % negative; set to zero by one number.

Film: The Social Reckoning. Content: film/docs/plans/2026-10-12/
PLAN-social-reckoning.md (slide 06, his outro paragraph). Washington Post 2021
(reporting): angry 5 from 2018, 0 by September 2020; the Polish party's
50/50 → 80 % negative from Facebook researchers' notes. The 5 line is struck
on "zero" and the 0 line comes in green under it.

    uv run --directory slides python -m aimanim.look still sr-anger full
"""

import sys
from pathlib import Path

from manim import Create, FadeIn, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import kit  # noqa: E402

# ---- content (the plan, slide 06) --------------------------------------------
SERIES = "THE SOCIAL RECKONING · 06"
TAG, HEAD = "2018 – 2020 · Facebook", "Anger's weight"
CODE = ['w["angry"] <- 5',
        'w["angry"] <- 0']
FOUND = "angry posts: more misinformation"
POLAND = ["a Polish party's posts:", "50 % → 80 % negative"]

# ---- layout ----------------------------------------------------------------
GAP = 0.5

# ---- timing ----------------------------------------------------------------
# Each step on its word in [06] of slides.script.txt (his words, 2026-10-12).
BEAT_WORDS = ["The", "five", "misinformation", "half", "zero"]
BEAT_LINES = [0, 0, 1, 1, 2]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0]


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        self.top = VGroup(kit.step_tag(TAG), kit.headline(HEAD))
        self.code = kit.code(CODE, self.top.get_bottom()[1] - GAP)
        five, zero = self.code.lines
        zero.set_color(kit.GREEN)
        self.found = kit.note(FOUND, kit.below(self.code, gap=0.35), kit.AMBER)
        self.poland = kit.card(POLAND, 0, hl=1)
        kit.stack_up(self.poland)
        steps = [lambda: [FadeIn(self.top)],
                 lambda: [FadeIn(VGroup(self.code[0], five))],
                 lambda: [FadeIn(self.found)],
                 lambda: [FadeIn(self.poland)],
                 lambda: [Create(kit.strike(five, kit.ORANGE)), FadeIn(zero)]]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

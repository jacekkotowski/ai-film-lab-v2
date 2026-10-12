"""sr-quiz -- slide 02 The quiz that copied friends: the quiz-takers train
the formula, the friends get scores.

Film: The Social Reckoning. Content: film/docs/plans/2026-10-12/
PLAN-social-reckoning.md (slide 02). The code runs on toy data (scratchpad
social_code.R, 2026-10-12); ~270,000 from The Conversation (Chen 2018, Kogan's
own account); "tens of millions" as he says it. The people (who) come on the
numbers, the code (what was done with them) on the last sentence. The two
numbers are plain lines, not a card: with the two-line headline a card
overlapped the code (2026-10-12).

    uv run --directory slides python -m aimanim.look still sr-quiz full
"""

import sys
from pathlib import Path

from manim import FadeIn, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import kit  # noqa: E402

# ---- content (the plan, slide 02) --------------------------------------------
SERIES = "THE SOCIAL RECKONING · 02"
TAG, HEAD = "2014 · Kogan", "The quiz that copied friends"
CODE = ["fit <- lm(",
        "  open ~ .,",
        "  quiz)",
        "predict(fit,",
        "  friends)"]
WHO = ["quiz: about 270,000", "friends: tens of millions"]

# ---- layout ----------------------------------------------------------------
GAP = 0.5

# ---- timing ----------------------------------------------------------------
# Each step on its word in [02] of slides.script.txt (his words, 2026-10-12).
BEAT_WORDS = ["In", "270,000", "copied", "trained", "friends"]   # "scores" ends it: 0.6 s late
BEAT_LINES = [0, 0, 1, 2, 2]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0]


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        self.top = VGroup(kit.step_tag(TAG), kit.headline(HEAD))
        self.code = kit.code(CODE, self.top.get_bottom()[1] - GAP)
        quiz = kit.note(WHO[0], kit.below(self.code, gap=0.35), kit.PAPER)
        friends = kit.note(WHO[1], kit.below(quiz, gap=0.3), kit.PAPER)
        lines = self.code.lines
        steps = [lambda: [FadeIn(self.top)],
                 lambda: [FadeIn(quiz)],
                 lambda: [FadeIn(friends)],
                 lambda: [FadeIn(VGroup(self.code[0], *lines[:3]))],
                 lambda: [FadeIn(VGroup(*lines[3:]))]]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

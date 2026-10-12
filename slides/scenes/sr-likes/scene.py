"""sr-likes -- slide 01 The likes test: a table of likes, 100 columns, a
first-year formula; Democrat or Republican right 85 times in 100.

Film: The Social Reckoning. Content: film/docs/plans/2026-10-12/
PLAN-social-reckoning.md (slide 01). The code runs on toy data (scratchpad
social_code.R, 2026-10-12); the 85 is the paper's (Kosinski, Stillwell &
Graepel, PNAS 2013: AUC 0.85, 58,466 volunteers). Each code line comes on
the word that names it; what it means is the muted line under the card.

    uv run --directory slides python -m aimanim.look still sr-likes full
"""

import sys
from pathlib import Path

from manim import FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (the plan, slide 01) --------------------------------------------
SERIES = "THE SOCIAL RECKONING · 01"
TAG, HEAD = "2013 · Kosiński", "The likes test"
CODE = ["X <- likes |>",
        "  svd(nu = 100)",
        "fit <- glm(",
        "  dem ~ X$u,",
        "  binomial)"]
NOTES = ["58,000 people × the pages they liked",
         "→ 100 columns",
         "→ logistic regression"]
RESULT = ["Democrat or Republican?", "85 in 100 right"]

# ---- layout ----------------------------------------------------------------
GAP = 0.3      # 0.5 put the note on the result card (code rows +0.1, 2026-10-12)

# ---- timing ----------------------------------------------------------------
# Each step on its word in [01] of slides.script.txt (his words, 2026-10-12).
BEAT_WORDS = ["In", "likes", "hundred", "formula", "85"]
BEAT_LINES = [0, 0, 1, 1, 2]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0]


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        self.top = VGroup(kit.step_tag(TAG), kit.headline(HEAD))
        self.code = kit.code(CODE, self.top.get_bottom()[1] - GAP)
        b = kit.below(self.code, gap=0.3)
        self.notes = [kit.note(s, b) for s in NOTES]
        self.result = kit.card(RESULT, 0, hl=1)
        kit.stack_up(self.result)
        lines = self.code.lines
        self.back = self.code[0]
        steps = [self.head, lambda: self.show(VGroup(self.back, lines[0]), 0),
                 lambda: self.show(lines[1], 1),
                 lambda: self.show(VGroup(*lines[2:]), 2), self.end]
        self.shown = None
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    def head(self):
        return [FadeIn(self.top)]

    def show(self, lines, i):
        """Code lines in, the note under the card changed to note i."""
        out = [FadeIn(lines), FadeIn(self.notes[i])]
        if self.shown is not None:
            out.append(FadeOut(self.shown))
        self.shown = self.notes[i]
        return out

    def end(self):
        return [FadeIn(self.result)]

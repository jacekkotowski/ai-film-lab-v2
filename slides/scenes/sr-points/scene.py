"""sr-points -- slide 05 Points for a post: models guess the actions, staff
chose the points by hand; the numbers fill in on his words.

Film: The Social Reckoning. Content: film/docs/plans/2026-10-12/
PLAN-social-reckoning.md (slide 05). Weights from the Facebook Papers
reporting (CNN 2021: like 1, reaction 5, significant comment 30). The code
runs on toy data (scratchpad social_code.R, 2026-10-12). The sum first comes
with blanks; the blanks turn amber on "staff", then 1, 5, 30 on their words.

    uv run --directory slides python -m aimanim.look still sr-points full
"""

import sys
from pathlib import Path

from manim import FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import kit  # noqa: E402

# ---- content (the plan, slide 05) --------------------------------------------
SERIES = "THE SOCIAL RECKONING · 05"
TAG, HEAD = "2018 · Facebook", "Points for a post"
CODE = ["posts |>",
        "  mutate(score =",
        "   _ * like +",
        "   _ * emoji +",
        "  __ * comment) |>",
        "  arrange(-score)"]
FILLED = {2: "   1 * like +", 3: "   5 * emoji +", 4: "  30 * comment) |>"}
NOTES = ["→ the feed: top score first",
         "like, emoji, comment: a model's guess",
         "the numbers: chosen by hand"]

# ---- layout ----------------------------------------------------------------
GAP = 0.5

# ---- timing ----------------------------------------------------------------
# Each step on its word in [05] of slides.script.txt (his words, 2026-10-12).
BEAT_WORDS = ["From", "ranked", "guess", "staff", "like", "emoji", "comment"]  # "thirty" ends it
BEAT_LINES = [0, 0, 1, 1, 2, 2, 2]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        self.top = VGroup(kit.step_tag(TAG), kit.headline(HEAD))
        self.code = kit.code(CODE, self.top.get_bottom()[1] - GAP)
        b = kit.below(self.code, gap=0.35)
        self.notes = [kit.note(s, b, kit.AMBER if i == 2 else kit.MUTED)
                      for i, s in enumerate(NOTES)]
        self.filled = {i: kit.code_line(s, self.code.left, self.code.baselines[i], kit.GREEN)
                       for i, s in FILLED.items()}
        self.shown = None
        steps = [lambda: [FadeIn(self.top)],
                 lambda: [FadeIn(self.code)] + self.note(0),
                 lambda: self.note(1),
                 lambda: [VGroup(*[self.code.lines[i] for i in FILLED]).animate
                          .set_color(kit.AMBER)] + self.note(2),
                 lambda: self.fill(2), lambda: self.fill(3), lambda: self.fill(4)]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    def note(self, i):
        """The muted line under the card changed to note i."""
        out = [FadeIn(self.notes[i])]
        if self.shown is not None:
            out.append(FadeOut(self.shown))
        self.shown = self.notes[i]
        return out

    def fill(self, i):
        """Line i's blank becomes its number, in green."""
        return [FadeOut(self.code.lines[i]), FadeIn(self.filled[i])]

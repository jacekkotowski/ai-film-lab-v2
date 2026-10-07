"""scr-rarity -- the same 99.7 % test on a rarer condition: the real
positives shrink, the 40 false ones stay, until 85 % of positives are
wrong. The likelihood ratio does not move: 0.90 / 0.05 = 18.

Content: spec.md. Slide 4 of the screening film. The pile is an
ILLUSTRATION (said on screen by its prevalence): the blood test's own
rates (Gil 2017) at Down syndrome's 1 in 490, then at 1 in 14,000, the
prevalence where those rates give 85 % false positives. The NYT's 85 %
is for other (microdeletion) screens; see spec.md.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/scr-rarity/out scenes/scr-rarity/scene.py Slide
"""

import math
import sys
from pathlib import Path

from manim import Circle, FadeIn, FadeOut, Scene, Transform, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import diagnostic, frame, kit  # noqa: E402
from aimanim import screening as ex  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "99.7% caught"
PER = 100_000
COMMON, RARE = 490, 14_000               # "1 in ..."
BLOOD_SPEC = 1 - ex.BLOOD_FPR


def table(one_in):
    return diagnostic.Test.from_rates(PER, round(PER / one_in), ex.BLOOD_SENSITIVITY, BLOOD_SPEC)


A, B = table(COMMON), table(RARE)        # tp 203 fp 40; tp 7 fp 40
WRONG = f"{1 - B.ppv:.0%} wrong"         # 85 %
T = ex.EXAMPLE
LR = f"LR+ = {T.sensitivity:.2f} / {T.fpr:.2f}"     # 0.90 / 0.05
LR_IS = f"= {T.lr_pos:.0f}"                         # 18
BLOOD_LR = f"LR+ ≈ {round(ex.BLOOD_SENSITIVITY / ex.BLOOD_FPR, -2):,.0f}"   # 2,500

# ---- layout --------------------------------------------------------------
DOT_X, DOT_Y, DOT_R = 2.6, 4.6, 1.0      # area ~ prevalence: 1 in 14,000 -> r 0.19
PREV_X, PREV_ROW = -1.4, 4.35
PILE_HEAD = 3.05
PILE_TOP, PILE_COLS, PITCH, R = 2.6, 30, 0.26, 0.1      # 243 dots: 9 rows
SMALL_COLS, SMALL_LEFT = 10, -3.9                        # 47 dots: 5 rows
WRONG_X, WRONG_ROW = 1.6, 1.7
ROWS = {"lr": 0.2, "is": -0.75, "blood": -1.95, "blood_lr": -2.8}

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["Blood", "rarer", "85|eighty-five", "fairest", "Hers"]
BEAT_LINES = [0, 0, 0, 1, 2]
RUN_TIMES = [1.5, 2.0, 1.0, 1.0, 1.0]


def pile(t, cols, left):
    pts = kit.grid_points(t.positive, cols, PITCH, left, PILE_TOP)
    return pts[:t.tp], pts[t.tp:]


def prevalence(one_in):
    r = DOT_R * math.sqrt(COMMON / one_in)
    return VGroup(Circle(radius=r).move_to((DOT_X, DOT_Y, 0))
                  .set_fill(frame.SICK, 1).set_stroke(width=0),
                  kit.text(f"1 in {one_in:,}", PREV_X, PREV_ROW, frame.SICK))


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE)]
        steps = [self.step_common, self.step_rare, self.step_wrong,
                 self.step_lr, self.step_18]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_common(self):
        red, grey = pile(A, PILE_COLS, -PILE_COLS * PITCH / 2)
        self.keep = kit.dots(red[:B.tp], R, frame.SICK)
        self.gone = kit.dots(red[B.tp:], R, frame.SICK)
        self.grey = kit.dots(grey, R)
        self.prev = prevalence(COMMON)
        return [FadeIn(self.prev),
                FadeIn(VGroup(kit.text("positives in 100,000", 0, PILE_HEAD),
                              self.keep, self.gone, self.grey))]

    def step_rare(self):
        red, grey = pile(B, SMALL_COLS, SMALL_LEFT)
        return [Transform(self.prev, prevalence(RARE)),
                FadeOut(self.gone),
                Transform(VGroup(self.keep, self.grey),
                          VGroup(kit.dots(red, R, frame.SICK), kit.dots(grey, R)))]

    def step_wrong(self):
        return [FadeIn(kit.text(WRONG, WRONG_X, WRONG_ROW, frame.ACCENT))]

    def step_lr(self):
        return [FadeIn(kit.text(LR, 0, ROWS["lr"]))]

    def step_18(self):
        return [FadeIn(kit.text(LR_IS, 0, ROWS["is"], frame.ACCENT, 72)),
                FadeIn(VGroup(kit.text("newer blood test", 0, ROWS["blood"], frame.DIM),
                              kit.text(BLOOD_LR, 0, ROWS["blood_lr"], frame.DIM)))]

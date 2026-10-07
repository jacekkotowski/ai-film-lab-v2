"""scr-outcomes -- the 10,000 split by truth, then by the test: four cells.

Content: spec.md. Slide 2 of the screening film. Starts from slide 1's
10,000 dots (aimanim/screening.py), so the two slides join.
One dot = one pregnancy. The affected column is drawn with bigger dots
(20 at the healthy column's size would be specks); slide 3 shows both
rows at one size.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/scr-outcomes/out scenes/scr-outcomes/scene.py Slide
"""

import sys
from pathlib import Path

from manim import (FadeIn, Line, ReplacementTransform, Scene, Transform, VGroup)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402
from aimanim import screening as ex  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Four outcomes"
T = ex.EXAMPLE                            # tp 18, fn 2, fp 499, tn 9481
SENS = f"sensitivity {T.sensitivity:.0%}"  # 18 / 20
SPEC = f"specificity {T.specificity:.0%}"  # 9,481 / 9,980

# ---- layout --------------------------------------------------------------
# Columns = truth, rows = the test's result (as in diagnostic.py).
SICK_X = (-3.15, -0.35)                   # "affected" 3.12 wide
WELL_X = (-0.05, 4.0)
HEAD_ROWS = (5.3, 4.4)                    # name, count ("y" of healthy 0.17 deep)
ROW1 = (4.1, 1.2)                         # flagged: top, bottom
ROW2 = (1.0, -2.2)                        # cleared
BOX_TOP = 5.06                            # over the counts, under the names:
                                          # "affected" is wider than its column
CELL_TEXT = (3.45, 0.35)                  # baselines in row 1, row 2
LABEL_X = -3.58                           # the rotated row names
FOOT = (-2.95, -3.8)                      # sensitivity, specificity
BIG_R, BIG_PITCH = 0.09, 0.28             # affected dots
SMALL_R, SMALL_PITCH = 0.011, 0.03        # healthy dots: 135 per row
SMALL_COLS = 135

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["Of", "test", "It", "Sensitivity", "Specificity"]
BEAT_LINES = [0, 1, 2, 3, 4]
RUN_TIMES = [2.0, 1.5, 1.5, 1.0, 1.0]


def mid(x):
    return (x[0] + x[1]) / 2


def sick_block(n, top, cols):
    w = cols * BIG_PITCH
    return kit.grid_points(n, cols, BIG_PITCH, mid(SICK_X) - w / 2, top)


def well_block(n, top, start=0):
    """Places start .. start+n-1 of a healthy block 135 dots wide."""
    w = SMALL_COLS * SMALL_PITCH
    pts = kit.grid_points(start + n, SMALL_COLS, SMALL_PITCH, mid(WELL_X) - w / 2, top)
    return pts[start:]


def label(s, y):
    return kit.text(s, 0, 0).rotate(1.5708).move_to((LABEL_X, y, 0))


class Slide(Scene):
    def construct(self):
        # slide 1's picture: healthy dots split into the coming FP and TN,
        # cases into the coming TP and FN
        healthy, cases = ex.grid_places()
        pts = kit.grid_points(ex.N, ex.GRID_COLS, ex.GRID_PITCH, ex.GRID_LEFT, ex.GRID_TOP)
        self.g_fp = kit.dots([pts[i] for i in healthy[:T.fp]], ex.GRID_DOT)
        self.g_tn = kit.dots([pts[i] for i in healthy[T.fp:]], ex.GRID_DOT)
        self.g_tp = kit.dots([pts[i] for i in cases[:T.tp]], ex.CASE_DOT, frame.SICK)
        self.g_fn = kit.dots([pts[i] for i in cases[T.tp:]], ex.CASE_DOT, frame.SICK)
        background = [kit.title(TITLE), self.g_fp, self.g_tn, self.g_tp, self.g_fn]
        steps = [self.step_truth, self.step_sick, self.step_healthy,
                 self.step_sensitivity, self.step_specificity]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    # 1. sorted by truth: 20 affected left, 9,980 healthy right, one block each
    def step_truth(self):
        top = CELL_TEXT[1] - 0.4
        sick = sick_block(T.sick, top, 10)
        well = well_block(T.healthy, top + 0.09)
        self.fp = kit.dots(well[:T.fp], SMALL_R)
        self.tn = kit.dots(well[T.fp:], SMALL_R)
        self.tp = kit.dots(sick[:T.tp], BIG_R, frame.SICK)
        self.fn = kit.dots(sick[T.tp:], BIG_R, frame.SICK)
        head = VGroup(kit.text("affected", mid(SICK_X), HEAD_ROWS[0], frame.SICK),
                      kit.text(f"{T.sick:,}", mid(SICK_X), HEAD_ROWS[1], frame.SICK),
                      kit.text("healthy", mid(WELL_X), HEAD_ROWS[0]),
                      kit.text(f"{T.healthy:,}", mid(WELL_X), HEAD_ROWS[1]))
        return [ReplacementTransform(VGroup(self.g_fp, self.g_tn), VGroup(self.fp, self.tn)),
                ReplacementTransform(VGroup(self.g_tp, self.g_fn), VGroup(self.tp, self.fn)),
                FadeIn(head)]

    # 2. the test on the 20: 18 up into "flagged", 2 stay "cleared"
    def step_sick(self):
        tp = kit.dots(sick_block(T.tp, CELL_TEXT[0] - 0.4, 9), BIG_R, frame.SICK)
        fn = kit.dots(sick_block(T.fn, CELL_TEXT[1] - 0.4, 2), BIG_R, frame.SICK)
        rule = Line((SICK_X[0], (ROW1[1] + ROW2[0]) / 2, 0), (WELL_X[1], (ROW1[1] + ROW2[0]) / 2, 0)
                    ).set_stroke(frame.DIM, 3)
        words = VGroup(rule, label("flagged", mid(ROW1)), label("cleared", mid(ROW2)),
                       kit.text(f"TP {T.tp}", mid(SICK_X), CELL_TEXT[0], frame.SICK),
                       kit.text(f"FN {T.fn}", mid(SICK_X), CELL_TEXT[1], frame.SICK))
        return [Transform(VGroup(self.tp, self.fn), VGroup(tp, fn)), FadeIn(words)]

    # 3. the test on the 9,980: 499 up into "flagged", 9,481 "cleared"
    def step_healthy(self):
        fp = kit.dots(well_block(T.fp, CELL_TEXT[0] - 0.4), SMALL_R)
        tn = kit.dots(well_block(T.tn, CELL_TEXT[1] - 0.4), SMALL_R)
        words = VGroup(kit.text(f"FP {T.fp}", mid(WELL_X), CELL_TEXT[0]),
                       kit.text(f"TN {T.tn:,}", mid(WELL_X), CELL_TEXT[1]))
        return [Transform(VGroup(self.fp, self.tn), VGroup(fp, tn)), FadeIn(words)]

    # 4. down the left column: 18 of the 20
    def step_sensitivity(self):
        return [FadeIn(kit.box(SICK_X[0] + 0.02, ROW2[1], SICK_X[1] + 0.05, BOX_TOP, frame.ACCENT)),
                FadeIn(kit.text(SENS, 0, FOOT[0], frame.ACCENT))]

    # 5. down the right column: 9,481 of the 9,980
    def step_specificity(self):
        return [FadeIn(kit.box(WELL_X[0] - 0.05, ROW2[1], WELL_X[1] - 0.05, BOX_TOP, frame.SECOND)),
                FadeIn(kit.text(SPEC, 0, FOOT[1], frame.SECOND))]

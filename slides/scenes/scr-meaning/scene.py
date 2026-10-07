"""scr-meaning -- read by rows: of 517 flagged, 18 affected (1 in 29);
of 9,483 cleared, 2 affected.

Content: spec.md. Slide 3 of the screening film. The two rows of slide 2's
table, each laid out with ONE dot size for everyone, so the share of red
in a row is the share you see.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/scr-meaning/out scenes/scr-meaning/scene.py Slide
"""

import sys
from pathlib import Path

from manim import FadeIn, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import diagnostic, frame, kit  # noqa: E402
from aimanim import screening as ex  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "A positive result"
T = ex.EXAMPLE                     # positive 517 (18 + 499), negative 9,483 (2 + 9,481)
PPV_TEXT = f"{T.tp} / {T.positive} = 1 in {diagnostic.one_in(T.ppv)}"   # 1 in 29
NPV_TEXT = f"{T.npv * 100:.2f}% healthy"                               # 99.98%
DOCTORS, TRUTH = "9 in 10", "1 in 10"   # Gigerenzer: mammography, 160 gynecologists

# ---- layout --------------------------------------------------------------
ROWS = {"pos_head": 5.25, "pos_res": 2.5, "neg_head": 1.55, "neg_res": -1.4,
        "quiz": -2.6, "who": -3.45}
POS_TOP, POS_COLS, POS_PITCH, POS_R = 4.95, 50, 0.16, 0.055    # 11 rows
NEG_TOP, NEG_COLS, NEG_PITCH, NEG_R = 1.25, 200, 0.04, 0.014   # 48 rows
RING_R = 0.13                                                  # around the 2
QUIZ_X = 2.0

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["Of", "cleared", "Gerd|Gigerenzer"]
BEAT_LINES = [0, 1, 2]
RUN_TIMES = [1.5, 1.5, 1.0]


def pile(n, k, seed, top, cols, pitch, r):
    """n people, k of them affected (red, scattered), all one size."""
    pts = kit.grid_points(n, cols, pitch, -cols * pitch / 2, top)
    red = set(diagnostic.scatter(n, k, seed))
    return (kit.dots([p for i, p in enumerate(pts) if i not in red], r),
            kit.dots([pts[i] for i in sorted(red)], r, frame.SICK),
            [pts[i] for i in sorted(red)])


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE)]
        steps = [self.step_flagged, self.step_cleared, self.step_doctors]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_flagged(self):
        grey, red, _ = pile(T.positive, T.tp, 1, POS_TOP, POS_COLS, POS_PITCH, POS_R)
        return [FadeIn(kit.text(f"PPV: {T.positive} flagged", 0, ROWS["pos_head"])),
                FadeIn(VGroup(grey, red)),
                FadeIn(kit.text(PPV_TEXT, 0, ROWS["pos_res"], frame.ACCENT))]

    def step_cleared(self):
        grey, red, where = pile(T.negative, T.fn, 2, NEG_TOP, NEG_COLS, NEG_PITCH, NEG_R)
        rings = kit.ring(where, RING_R)
        return [FadeIn(kit.text(f"NPV: {T.negative:,} cleared", 0, ROWS["neg_head"])),
                FadeIn(VGroup(grey, red, rings)),
                FadeIn(kit.text(NPV_TEXT, 0, ROWS["neg_res"], frame.SECOND))]

    def step_doctors(self):
        said = kit.text(DOCTORS, -QUIZ_X, ROWS["quiz"], frame.DIM)
        return [FadeIn(VGroup(said, kit.strike(said, frame.SICK),
                              kit.text("doctors", -QUIZ_X, ROWS["who"], frame.DIM))),
                FadeIn(VGroup(kit.text(TRUTH, QUIZ_X, ROWS["quiz"], frame.ACCENT),
                              kit.text("truth", QUIZ_X, ROWS["who"], frame.ACCENT)))]

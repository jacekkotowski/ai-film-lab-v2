"""zero-range -- a 50 cm target fills a smaller mark the further it is.

Content: spec.md. Slide 5 of the zeroing film. The centre of the real
Aurora MIL reticle (aimanim/aurora.py), enlarged, to scale.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/zero-range/out scenes/zero-range/scene.py Slide
"""

import math
import sys
from pathlib import Path

from manim import FadeIn, Line, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import aurora, frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TARGET_CM = 50
METRES = [300, 400, 500, 600]        # the chevron, then bars 2, 3, 4
BARS = [None, 2, 3, 4]               # mil below the aim point
TITLE = "Ranging"


def width_mil(metres: float) -> float:
    return math.atan(TARGET_CM / 100 / metres) * 1000   # 500 / metres


# ---- layout --------------------------------------------------------------
S = 1.6                              # frame units per mil: 4.4 mil fills the free height
AIM = (-0.8, 4.4)                    # the chevron's tip
WINDOW = (-1.3, 1.3, -4.4, 0.35)     # the part of the reticle shown, mil
LABEL_X = 1.5                        # left edge of the "300 m" labels
BAND_GAP = 0.35                      # a 50 cm width, this far above its mark
CAP = 0.15                           # half-height of the band's end caps

# ---- timing --------------------------------------------------------------
# Step i belongs to sentence BEAT_LINES[i] of the narration over this
# picture (0-based). Change these after narrating, not the waits.
# Each step starts on its word (beats.starts_by_words): the word as he
# says it in films/zeroing.script.txt. "a|b" accepts either. Not heard ->
# the step starts with the one before, and [beats] says so.
BEAT_WORDS = ["width", "fifty|50", "next"]
BEAT_LINES = [0, 1, 2]
RUN_TIMES = [1.0, 1.0, 1.5]


at = kit.mil_to(S, AIM)


def centre() -> VGroup:
    return kit.reticle(at, WINDOW, stroke=6, dot_r=0.08, numbers=False)


def band(i: int) -> VGroup:
    """The 50 cm target's width, above mark i."""
    w = width_mil(METRES[i]) * S
    y = at(0, 0 if i == 0 else -BARS[i])[1] + BAND_GAP
    l, r = AIM[0] - w / 2, AIM[0] + w / 2
    return VGroup(Line((l, y, 0), (r, y, 0)),
                  Line((l, y - CAP, 0), (l, y + CAP, 0)),
                  Line((r, y - CAP, 0), (r, y + CAP, 0)),
                  ).set_stroke(frame.ACCENT, width=5)


def metres_label(i: int):
    y = at(0, -aurora.CHEVRON_H / 2 if i == 0 else -BARS[i])[1]
    return kit.text(f"{METRES[i]} m", LABEL_X, y - 0.25, frame.SECOND, align="left")


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE)]
        steps = [self.step_marks, self.step_first, self.step_rest]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    # ---- one method per step; each returns its animations ----------------
    def step_marks(self):
        return [FadeIn(centre())]

    def step_first(self):
        b = band(0)
        size = kit.text(f"{TARGET_CM} cm", AIM[0], b.get_top()[1] + 0.2, frame.ACCENT)
        return [FadeIn(VGroup(b, size)), FadeIn(metres_label(0))]

    def step_rest(self):
        rest = range(1, len(METRES))
        return [FadeIn(VGroup(*[band(i) for i in rest])),
                FadeIn(VGroup(*[metres_label(i) for i in rest]))]

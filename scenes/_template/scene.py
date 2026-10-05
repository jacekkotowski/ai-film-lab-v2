"""<slug> -- <the one idea, in one line>.

Content: spec.md. Copy this folder to scenes/<slug>/ and fill it in.
Layout rules and lessons: the `slide-layout` skill.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/<slug>/out scenes/<slug>/scene.py Slide
"""

import sys
from pathlib import Path

from manim import FadeIn, Scene, VGroup, Write  # noqa: F401  (what the steps use)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Title"                  # <= ~11 characters at TITLE_FONT; kit.title shrinks longer

# ---- layout --------------------------------------------------------------
# Safe area: x in [-SIDE, SIDE] = [-4, 4]; y in [BOTTOM, TOP] = [-4, 7].
# Text at MIN_FONT: ~0.48 per digit, 0.59 tall. Measure with kit.fits("...").
ROW = {"first": 5.5, "second": 4.6}   # baselines

# ---- timing --------------------------------------------------------------
# Step i belongs to sentence BEAT_LINES[i] of the narration over this
# picture (0-based). Change these after narrating, not the waits.
BEAT_LINES = [0, 1]
RUN_TIMES = [1.0, 1.0]


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE)]          # on screen before the first word
        steps = [self.step_one, self.step_two]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background)

    # ---- one method per step; each returns its animations (<= 3 moving) --
    def step_one(self):
        return [Write(kit.text("first", 0, ROW["first"]))]

    def step_two(self):
        return [FadeIn(kit.text("second", 0, ROW["second"], frame.ACCENT))]

"""zero-range -- a 50 cm target fills a smaller mark the further it is.

Content: spec.md. Slide 3b of 4 of the zeroing film. Mark WIDTHS are to
scale; their vertical spacing is schematic (spec.md).

    uv run --extra render manim -s -r 540,960 --media_dir scenes/zero-range/out scenes/zero-range/scene.py Slide
"""

import math
import sys
from pathlib import Path

from manim import FadeIn, Line, Scene, Text, VGroup, VMobject

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import beats, frame  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TARGET_CM = 50
METRES = [300, 400, 500, 600]    # chevron, then the 2nd, 3rd, 4th MIL stadia
TITLE = "Ranging"


def width_mil(metres: float) -> float:
    return math.atan(TARGET_CM / 100 / metres) * 1000   # 500 / metres


# ---- layout --------------------------------------------------------------
S = 2.4                          # frame units per mil
MARK_X = -1.0                    # centre of the marks
LABEL_X = 1.4                    # left edge of the "300 m" labels
MARK_Y = [3.0, 1.4, -0.2, -1.8]  # base of the chevron, then the stadia (schematic)
CHEVRON_H = 0.6
BAND_GAP = 0.4                   # the target's width, drawn this far above its mark
CAP = 0.15                       # half-height of the band's end caps

# ---- timing --------------------------------------------------------------
# Step i belongs to sentence BEAT_LINES[i] of the narration over this
# picture (0-based). Change these after narrating, not the waits.
BEAT_LINES = [0, 1, 2]
RUN_TIMES = [1.0, 1.0, 1.5]


def text(s, baseline, x, color=frame.INK, align="center"):
    """Text with its baseline on y, centred on x (or starting at x). An
    "H" is set after it to find the baseline (its bottom), then taken away."""
    t = Text(s + "H", font_size=frame.MIN_FONT, color=color)
    h = t[-1]
    t.shift((0, baseline - h.get_bottom()[1], 0))
    t.remove(h)
    dx = x - (t.get_center()[0] if align == "center" else t.get_left()[0])
    return t.shift((dx, 0, 0))


def mark(i: int) -> VMobject:
    w, y = width_mil(METRES[i]) * S, MARK_Y[i]
    if i == 0:                   # the chevron: a "^", as wide as its base
        m = VMobject().set_points_as_corners([
            (MARK_X - w / 2, y, 0), (MARK_X, y + CHEVRON_H, 0),
            (MARK_X + w / 2, y, 0)])
    else:
        m = Line((MARK_X - w / 2, y, 0), (MARK_X + w / 2, y, 0))
    return m.set_stroke(frame.INK, width=6)


def band(i: int) -> VGroup:
    """The 50 cm target's width, above mark i."""
    w = width_mil(METRES[i]) * S
    y = MARK_Y[i] + (CHEVRON_H if i == 0 else 0) + BAND_GAP
    l, r = MARK_X - w / 2, MARK_X + w / 2
    return VGroup(Line((l, y, 0), (r, y, 0)),
                  Line((l, y - CAP, 0), (l, y + CAP, 0)),
                  Line((r, y - CAP, 0), (r, y + CAP, 0)),
                  ).set_stroke(frame.ACCENT, width=5)


def metres_label(i: int) -> Text:
    y = MARK_Y[i] + (CHEVRON_H / 2 if i == 0 else 0)
    return text(f"{METRES[i]} m", y - 0.25, LABEL_X, frame.SECOND, align="left")


class Slide(Scene):
    def construct(self):
        title = Text(TITLE, font_size=frame.TITLE_FONT, color=frame.INK)
        self.add(title.move_to((0, frame.TOP - title.height / 2, 0)))
        steps = [self.step_marks, self.step_first, self.step_rest]
        p = beats.for_scene(HERE, BEAT_LINES, RUN_TIMES)
        for wait, step, rt in zip(p.waits, steps, RUN_TIMES):
            if wait >= beats.MIN_WAIT:
                self.wait(wait)
            self.play(*step(), run_time=rt)
        if p.tail >= beats.MIN_WAIT:
            self.wait(p.tail)

    # ---- one method per step; each returns its animations ----------------
    def step_marks(self):
        return [FadeIn(VGroup(*[mark(i) for i in range(len(METRES))]))]

    def step_first(self):
        b = band(0)
        size = text(f"{TARGET_CM} cm", b.get_top()[1] + 0.2, MARK_X, frame.ACCENT)
        return [FadeIn(VGroup(b, size)), FadeIn(metres_label(0))]

    def step_rest(self):
        rest = range(1, len(METRES))
        return [FadeIn(VGroup(*[band(i) for i in rest])),
                FadeIn(VGroup(*[metres_label(i) for i in rest]))]

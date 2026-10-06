"""zero-reticle -- the SLx's Aurora MIL reticle, its parts named.

Content: spec.md; the reticle itself: aimanim/aurora.py (in mil, to scale).
Slide 4 of the zeroing film; zero-range (5) then ranges with its centre.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/zero-reticle/out scenes/zero-reticle/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Arrow, Dot, FadeIn, Line, Rectangle, Scene, VGroup, VMobject

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import aurora, frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Aurora reticle"
MAN_AT = 6                           # the stadia with the man on it
TABLE = [14, 10, 6]                  # the numbered stadia: "2", "4", "6"

# ---- layout --------------------------------------------------------------
# Safe area: x in [-SIDE, SIDE] = [-4, 4]; y in [BOTTOM, TOP] = [-4, 7].
S = 0.27                             # frame units per mil: the "2" at 14 mil fits
AIM = (0.0, 3.3)                     # the aim point (chevron's tip)
CHEVRON_ROW = 4.75                   # baselines
SIDE_ROWS = (1.4, 0.7)               # "Auto / range", "5 MIL / dot"
SIDE_X = 2.75
GRID_ROW = -0.45
TABLE_X = -1.7                       # left edge of the man's table
TABLE_ROWS = (-1.7, -2.45, -3.2, -3.95)  # baselines
STROKE, DOT_R = 3, 0.035

# ---- timing --------------------------------------------------------------
# Step i belongs to sentence BEAT_LINES[i] of the narration over this
# picture (0-based). Change these after narrating, not the waits.
# Each step starts on its word (beats.starts_by_words): the word as he
# says it in films/zeroing.script.txt. "a|b" accepts either.
BEAT_WORDS = ["Aurora", "chevron", "numbered", "dots", "heavy"]
BEAT_LINES = [0, 1, 2, 3, 4]
RUN_TIMES = [1.0, 1.0, 1.5, 1.0, 1.0]


def at(x, y):
    """A point of the reticle (mil) on the slide."""
    return (AIM[0] + x * S, AIM[1] + y * S, 0)


def reticle() -> VGroup:
    lines = [Line(at(*a), at(*b)) for a, b in aurora.segments()]
    lines.append(VMobject().set_points_as_corners([at(*p) for p in aurora.chevron()]))
    dots = [Dot(at(x, y), radius=DOT_R * (1.8 if heavy else 1), color=frame.INK)
            for x, y, heavy in aurora.dots()]
    numbers = [kit.text(s, at(side * x, 0)[0],
                        at(0, aurora.stadia_mil(x) / 2)[1] + 0.12)
               for side in (-1, 1) for x, s in aurora.NUMBERS.items()]
    return VGroup(VGroup(*lines).set_stroke(frame.INK, width=STROKE),
                  VGroup(*dots), VGroup(*numbers))


def name(lines, x, rows, tip, start) -> VGroup:
    """A part's name (one or two lines) and an arrow from it to the part."""
    words = [kit.text(s, x, y, frame.SECOND) for s, y in zip(lines, rows)]
    arrow = Arrow(start, tip, buff=0.05, stroke_width=4, color=frame.SECOND,
                  max_tip_length_to_length_ratio=0.3, tip_length=0.18)
    return VGroup(*words, arrow)


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE)]
        steps = [self.step_reticle, self.step_chevron, self.step_auto_range,
                 self.step_grid, self.step_five]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    # ---- one method per step; each returns its animations (<= 3 moving) --
    def step_reticle(self):
        return [FadeIn(reticle())]

    def step_chevron(self):
        return [FadeIn(name(["Chevron"], 0, [CHEVRON_ROW],
                            at(0, 0.15), (0, CHEVRON_ROW - 0.12, 0)))]

    def step_auto_range(self):
        stadia = at(-10, -aurora.stadia_mil(10) / 2)
        label = name(["Auto", "range"], -SIDE_X, SIDE_ROWS, stadia,
                     (stadia[0], SIDE_ROWS[0] + 0.62, 0))
        man = Rectangle(width=0.5 * S, height=aurora.stadia_mil(MAN_AT) * S)
        man.move_to(at(-MAN_AT, 0)).set_fill(frame.ACCENT, opacity=0.75)
        man.set_stroke(width=0)
        rows = [kit.text(f"{aurora.MAN_M:.2f} m man", TABLE_X, TABLE_ROWS[0],
                         frame.ACCENT, align="left")]
        rows += [kit.text(f"{aurora.NUMBERS[x]}: {aurora.man_metres(x)} m",
                          TABLE_X, y, frame.INK, align="left")
                 for x, y in zip(TABLE, TABLE_ROWS[1:])]
        return [FadeIn(label), FadeIn(man), FadeIn(VGroup(*rows))]

    def step_grid(self):
        tip = at(3, -aurora.LADDER_TO)
        return [FadeIn(name(["MIL grid"], 0, [GRID_ROW], tip,
                            (tip[0], GRID_ROW + 0.62, 0)))]

    def step_five(self):
        return [FadeIn(name(["5 MIL", "dot"], SIDE_X, SIDE_ROWS, at(5, 0),
                            (SIDE_X - 0.75, SIDE_ROWS[0] + 0.62, 0)))]

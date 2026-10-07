"""scr-cost -- the price of a false alarm: 499 mothers, weeks of waiting,
and the needle's 0.3 % loss: about 1.5 healthy pregnancies per 10,000.

Content: spec.md. Slide 5 of the screening film. The 499 start as the
false-positive dots and become people (kit.people); 1.5 is shown as one
figure turned orange and one half orange: one fading figure in 499
is not seen on a phone.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/scr-cost/out scenes/scr-cost/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Dot, FadeIn, Line, Scene, Transform, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402
from aimanim import screening as ex  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = f"{ex.EXAMPLE.fp} false alarms"
T = ex.EXAMPLE
LOST = T.fp * ex.AMNIO_LOSS                          # 1.497
SUM = f"{T.fp} × {ex.AMNIO_LOSS:.1%} ≈ {LOST:.1f}"   # 499 × 0.3% ≈ 1.5
WEEKS = [(ex.WEEK_FLAG, "flagged"), (ex.WEEK_NEEDLE, "needle"), (ex.WEEK_RESULT, "result")]
GONE = (190, 312)                                    # which two figures (places)

# ---- layout --------------------------------------------------------------
COLS, PITCH_X, PITCH_Y, TOP = 36, 0.222, 0.286, 5.95  # 14 rows: 5.95 .. 1.95
FIG_H, DOT_R = 0.26, 0.03
LINE_X, TEXT_X = -3.6, -3.1
WEEK_Y0, PER_WEEK = 1.35, 0.41                       # week 12 at 1.35, 17 at -0.7
ROWS = {"sum": -1.95, "what": -2.8, "per": -3.65}

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["Each", "wait", "result", "needle"]
BEAT_LINES = [0, 1, 1, 2]
RUN_TIMES = [1.5, 1.0, 1.0, 1.5]


def places():
    pts = kit.grid_points(T.fp, COLS, PITCH_X, -COLS * PITCH_X / 2, TOP, PITCH_Y)
    rest = [p for i, p in enumerate(pts) if i not in GONE]
    return rest, [pts[i] for i in GONE]


def week_y(w):
    return WEEK_Y0 - (w - ex.WEEK_FLAG) * PER_WEEK


def week(w, name):
    y = week_y(w)
    return VGroup(Dot((LINE_X, y, 0), radius=0.09, color=frame.ACCENT),
                  kit.text(f"week {w}  {name}", TEXT_X, y - 0.3, align="left"))


class Slide(Scene):
    def construct(self):
        rest, two = places()
        self.rest = kit.dots(rest, DOT_R)
        self.a = kit.dots(two[:1], DOT_R)
        self.b = kit.dots(two[1:], DOT_R)
        background = [kit.title(TITLE), self.rest, self.a, self.b]
        steps = [self.step_people, self.step_wait, self.step_result, self.step_loss]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_people(self):
        rest, two = places()
        return [Transform(VGroup(self.rest, self.a, self.b),
                          VGroup(kit.people(rest, FIG_H), kit.people(two[:1], FIG_H),
                                 kit.people(two[1:], FIG_H)))]

    def step_wait(self):
        line = Line((LINE_X, week_y(ex.WEEK_FLAG), 0), (LINE_X, week_y(ex.WEEK_NEEDLE), 0)
                    ).set_stroke(frame.DIM, 5)
        return [FadeIn(VGroup(line, week(*WEEKS[0]), week(*WEEKS[1])))]

    def step_result(self):
        line = Line((LINE_X, week_y(ex.WEEK_NEEDLE), 0), (LINE_X, week_y(ex.WEEK_RESULT), 0)
                    ).set_stroke(frame.DIM, 5)
        return [FadeIn(VGroup(line, week(*WEEKS[2])))]

    def step_loss(self):
        return [self.a.animate.set_fill(frame.ACCENT, opacity=1),
                self.b.animate.set_fill(frame.ACCENT, opacity=0.5),
                FadeIn(VGroup(kit.text(SUM, 0, ROWS["sum"], frame.ACCENT),
                              kit.text("healthy pregnancies", 0, ROWS["what"], frame.ACCENT),
                              kit.text("lost per 10,000", 0, ROWS["per"], frame.ACCENT)))]

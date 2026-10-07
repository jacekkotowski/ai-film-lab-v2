"""r-ppv-curve -- the R chart template: a ggplot PNG with Manim callouts.

Not in a film: the tested example of the r-charts skill (2026-10-08).
The chart is made by R, not here:

    "C:\\Program Files\\R\\R-4.6.1\\bin\\Rscript.exe" slides/r/ppv_curve.R slides/scenes/r-ppv-curve
    uv run --extra render manim -s -r 1080,1920 --media_dir scenes/r-ppv-curve/out scenes/r-ppv-curve/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Create, FadeIn, ImageMobject, Scene

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import diagnostic, frame, kit, rchart  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Truly sick"
SENS, FPR = 0.90, 0.05                   # as in slides/r/ppv_curve.R
COMMON, RARE = 10, 500                   # "1 in ..."

# ---- layout --------------------------------------------------------------
CHART_W = 8.0                            # 8 in at 240 dpi -> 58 pt = MIN_FONT
CHART_AT = (0.0, 0.2)                    # the PNG's centre: spans -3.8 .. 4.2
RING_R = 0.35
# Labels in DATA units (1 in ..., share), placed where the curve is not:
# right of and above the falling curve.
LABEL = {COMMON: (150, 0.62), RARE: (2500, 0.27)}   # between grid lines

# ---- timing --------------------------------------------------------------
BEAT_WORDS: list[str] = []
BEAT_LINES = [0, 1]
RUN_TIMES = [1.0, 1.0]

CHART = rchart.load(HERE / "chart.json")


def point(one_in):
    return rchart.at(CHART, one_in, diagnostic.ppv_at(1 / one_in, SENS, FPR),
                     CHART_W, CHART_AT)


def one_in(one_in_n):
    ppv = diagnostic.ppv_at(1 / one_in_n, SENS, FPR)
    return f"1 in {1 / ppv:.0f}" if ppv < 0.5 else f"{ppv * 3:.0f} in 3"


class Slide(Scene):
    def construct(self):
        chart = ImageMobject(str(HERE / "chart.png"))
        chart.scale_to_fit_width(CHART_W).move_to((*CHART_AT, 0))
        background = [chart, kit.title(TITLE)]
        steps = [self.step_common, self.step_rare]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def callout(self, n):
        lx, ly = rchart.at(CHART, *LABEL[n], CHART_W, CHART_AT)
        return [Create(kit.ring([point(n)], RING_R, frame.ACCENT)),
                FadeIn(kit.text(one_in(n), lx, ly, frame.ACCENT))]

    def step_common(self):
        return self.callout(COMMON)

    def step_rare(self):
        return self.callout(RARE)

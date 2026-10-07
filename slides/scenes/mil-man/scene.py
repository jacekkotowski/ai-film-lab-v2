"""mil-man -- a 1.78 m man's height in mil gives his distance.

Content: spec.md. Slide 2 of the mil-measure film. The centre ladder of the
Aurora MIL (kit.reticle, a window of it): head on the chevron's tip, feet
on bar n = n mil tall.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/mil-man/out scenes/mil-man/scene.py Slide
"""

import sys
from pathlib import Path

from manim import DashedLine, FadeIn, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Range by height"
MAN_M = 1.78
READINGS = [6, 4, 3, 2]              # mil, nearest first
EXAMPLE = 4                          # the one worked out


def metres(mil: float) -> int:
    return round(MAN_M * 1000 / mil)  # 297, 445, 593, 890


# ---- layout --------------------------------------------------------------
# Safe area: x in [-SIDE, SIDE] = [-4, 4]; y in [BOTTOM, TOP] = [-4, 7].
S, AIM = 0.7, (0.0, 5.3)             # units per mil; the chevron's tip
WINDOW = (-0.9, 0.9, -6.1, 0.2)      # chevron and ladder only (no dots)
MAN_X = {6: -3.5, 4: -2.45, 3: -1.65, 2: -1.0}
MIL_X, METRES_X = 0.75, 1.5         # left edges: the reading, the distance
CHAIN_STEP = 1.25                    # 4 rows from 0.0 to -3.75
CHAIN_TOP = 0.0                      # baseline of "1.78 m"

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["Take", "head", "Further", "distance", "Four|4"]
BEAT_LINES = [0, 1, 2, 3, 4]
RUN_TIMES = [1.0, 1.0, 1.5, 1.0, 1.5]

at = kit.mil_to(S, AIM)


def man(n: int):
    return kit.man(n * S, (MAN_X[n], at(0, -n)[1]))


def guide(n: int):
    """From his feet to bar n, and his reading after the bar."""
    y = at(0, -n)[1]
    line = DashedLine((MAN_X[n], y, 0), (AIM[0] - 0.25, y, 0), dash_length=0.12,
                      stroke_width=2, color=frame.DIM)
    return VGroup(line, kit.text(str(n), MIL_X, y - 0.22, frame.SECOND, align="left"))


def chain():
    return kit.chain([f"{MAN_M} m", f"{EXAMPLE} MIL",
                      f"{MAN_M} × 1000 ÷ {EXAMPLE}", f"{metres(EXAMPLE)} m"], CHAIN_TOP, step=CHAIN_STEP)


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE),
                      kit.reticle(at, WINDOW, stroke=5, dot_r=0.07, numbers=False)]
        steps = [self.step_man, self.step_read, self.step_further,
                 self.step_distances, self.step_example]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_man(self):
        return [FadeIn(man(READINGS[0])), FadeIn(chain()[0])]

    def step_read(self):
        head = DashedLine((MAN_X[6] - 0.45, AIM[1], 0), (AIM[0] - 0.75, AIM[1], 0),
                          dash_length=0.12, stroke_width=2, color=frame.DIM)
        return [FadeIn(head), FadeIn(guide(READINGS[0]))]

    def step_further(self):
        return [FadeIn(VGroup(*[man(n) for n in READINGS[1:]])),
                FadeIn(VGroup(*[guide(n) for n in READINGS[1:]]))]

    def step_distances(self):
        return [FadeIn(VGroup(*[
            kit.text(f"{metres(n)} m", METRES_X, at(0, -n)[1] - 0.22,
                     frame.ACCENT if n == EXAMPLE else frame.INK, align="left")
            for n in READINGS]))]

    def step_example(self):
        return [FadeIn(VGroup(*chain()[1:]))]

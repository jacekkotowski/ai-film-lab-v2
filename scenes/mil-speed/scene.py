"""mil-speed -- mil per second on the reticle, times the distance, is speed.

Content: spec.md. Slide 5 of the mil-measure film. Three views through the
Aurora MIL (its horizontal line, kit.reticle), 0.5 s apart, a target car
crossing; then the chain.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/mil-speed/out scenes/mil-speed/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Circle, FadeIn, Line, Polygon, Rectangle, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Moving target"
CAR_M, DIST_M = 2.0, 200
SNAPS = [(0.0, 0), (0.5, 5), (1.0, 10)]     # seconds, the nose's place in mil


def car_mil() -> float:
    return CAR_M * 1000 / DIST_M             # 10 mil long


def mil_per_s() -> float:
    (t0, x0), (t1, x1) = SNAPS[0], SNAPS[-1]
    return (x1 - x0) / (t1 - t0)             # 10 mil/s


def m_per_s() -> float:
    return mil_per_s() * DIST_M / 1000       # 2 m/s


# ---- layout --------------------------------------------------------------
# Safe area: x in [-SIDE, SIDE] = [-4, 4]; y in [BOTTOM, TOP] = [-4, 7].
S = 0.37                                     # ±10.6 mil = ±3.9 units
LINES_Y = [4.8, 3.1, 1.4]                     # the reticle line in each view
WINDOW = (-10.6, 10.6, -0.7, 0.7)            # line, dots, ticks; stadia cut short
LABEL_UP = 0.4                               # time label's baseline above the line
CHAIN_TOP, CHAIN_STEP = 0.0, 1.25          # 4 rows to -3.75

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["car", "Hold", "per", "Times"]
BEAT_LINES = [0, 1, 2, 3]
RUN_TIMES = [1.0, 1.5, 1.0, 1.5]


def car(nose_x: float, y: float) -> VGroup:
    """A car seen from the side, nose to the right, its middle on y."""
    L = car_mil() * S
    tail = nose_x - L
    body = Rectangle(width=L, height=0.42).move_to((tail + L / 2, y - 0.08, 0))
    cabin = Polygon((tail + 0.22 * L, y + 0.13, 0), (tail + 0.32 * L, y + 0.45, 0),
                    (tail + 0.62 * L, y + 0.45, 0), (tail + 0.74 * L, y + 0.13, 0))
    wheels = [Circle(radius=0.15).move_to((tail + f * L, y - 0.3, 0)) for f in (0.2, 0.8)]
    g = VGroup(body, cabin, *wheels).set_fill(frame.ACCENT, opacity=0.6).set_stroke(width=0)
    return g.set_z_index(-1)


def view(i: int) -> VGroup:
    t, nose = SNAPS[i]
    y = LINES_Y[i]
    at = kit.mil_to(S, (0.0, y))
    nose_x = at(nose, 0)[0]
    mark = Line((nose_x, y - 0.55, 0), (nose_x, y + 0.6, 0)).set_stroke(frame.SECOND, width=5)
    free_left = nose - car_mil() / 2 > 0                 # the car is on the right
    label = kit.text(f"{t:.1f} s", -frame.SIDE if free_left else frame.SIDE,
                     y + LABEL_UP, frame.SECOND, align="left" if free_left else "right")
    return VGroup(kit.reticle(at, WINDOW, stroke=4, dot_r=0.05, numbers=False),
                  car(nose_x, y), mark, label)


def chain():
    v = mil_per_s()
    return kit.chain([f"car at {DIST_M} m", f"{v:g} MIL per second",
                      f"{v:g} × {DIST_M} ÷ 1000",
                      f"{m_per_s():g} m/s = {m_per_s() * 3.6:g} km/h"], CHAIN_TOP, step=CHAIN_STEP)


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE)]
        steps = [self.step_car, self.step_moves, self.step_angular, self.step_speed]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_car(self):
        return [FadeIn(view(0)), FadeIn(chain()[0])]

    def step_moves(self):
        return [FadeIn(view(1)), FadeIn(view(2))]

    def step_angular(self):
        return [FadeIn(chain()[1])]

    def step_speed(self):
        return [FadeIn(VGroup(*chain()[2:]))]

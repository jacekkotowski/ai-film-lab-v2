"""zero-group -- the middle of the group is where the rifle shoots.

Content: spec.md. Slide 1 of 4 of the zeroing film.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/zero-group/out scenes/zero-group/scene.py Slide
"""

import sys
from pathlib import Path

from manim import (Arrow, Circle, Dot, FadeIn, GrowArrow, Line, Scene, Text,
                   VGroup, DOWN, RIGHT, UP)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
# cm from the aim point at 100 m, + = right / up
HOLES = [(-6.0, -3.5), (-3.0, -4.0), (-5.5, -6.5), (-3.5, -6.0)]
CENTRE = (sum(x for x, _ in HOLES) / 4, sum(y for _, y in HOLES) / 4)  # (-4.5, -5.0)
HOLE_R_CM = 0.28                 # a 5.56 mm hole
TITLE = "Group centre"
DISTANCE = "100 m"

# ---- layout --------------------------------------------------------------
S = 0.7                          # frame units per cm
GRID_X = (-8, 2)                 # cm shown, left..right
GRID_Y = (-8, 2)                 # cm shown, bottom..top
AIM = (-(GRID_X[0] + GRID_X[1]) / 2 * S, 4.0, 0.0)   # grid centred left-right
CROSS = 0.3                      # half-length of the aim cross, frame units

# ---- timing --------------------------------------------------------------
# Step i belongs to sentence BEAT_LINES[i] of the narration over this
# picture (0-based). Change these after narrating, not the waits.
BEAT_LINES = [0, 1, 2]
RUN_TIMES = [1.0, 1.0, 1.5]


def at(cm_x: float, cm_y: float) -> tuple[float, float, float]:
    """cm from the aim point -> frame point."""
    return (AIM[0] + cm_x * S, AIM[1] + cm_y * S, 0.0)


class Slide(Scene):
    def construct(self):
        background = self.background()
        steps = [self.step_holes, self.step_centre, self.step_offset]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background)

    # ---- on screen before the first word ---------------------------------
    def background(self):
        grid = VGroup(
            *[Line(at(x, GRID_Y[0]), at(x, GRID_Y[1]))
              for x in range(GRID_X[0], GRID_X[1] + 1)],
            *[Line(at(GRID_X[0], y), at(GRID_X[1], y))
              for y in range(GRID_Y[0], GRID_Y[1] + 1)],
        ).set_stroke(frame.DIM, width=1, opacity=0.5)
        x, y = AIM[0], AIM[1]
        cross = VGroup(Line((x - CROSS, y, 0), (x + CROSS, y, 0)),
                       Line((x, y - CROSS, 0), (x, y + CROSS, 0)),
                       ).set_stroke(frame.INK, width=4)
        aim = Text("aim", font_size=frame.MIN_FONT, color=frame.DIM
                   ).next_to(cross, RIGHT, buff=0.1)
        title = Text(TITLE, font_size=frame.TITLE_FONT, color=frame.INK)
        title.move_to((0, frame.TOP - title.height / 2, 0))   # top on TOP
        dist = Text(DISTANCE, font_size=frame.MIN_FONT, color=frame.DIM
                    ).next_to(grid, DOWN, buff=0.3)
        return [grid, cross, aim, title, dist]

    # ---- one method per step; each returns its animations ----------------
    def step_holes(self):
        self.holes = VGroup(*[Dot(at(x, y), radius=HOLE_R_CM * S,
                                  color=frame.INK) for x, y in HOLES])
        return [FadeIn(self.holes)]

    def step_centre(self):
        c = at(*CENTRE)
        mark = VGroup(Dot(c, radius=0.12, color=frame.ACCENT),
                      Circle(radius=0.35, color=frame.ACCENT).move_to(c))
        return [self.holes.animate.set_color(frame.DIM), FadeIn(mark)]

    def step_offset(self):
        corner = at(CENTRE[0], 0)
        left = Arrow(at(0, 0), corner, buff=0, color=frame.SECOND)
        down = Arrow(corner, at(*CENTRE), buff=0, color=frame.SECOND)
        labels = VGroup(
            Text(f"{-CENTRE[0]:g} cm", font_size=frame.MIN_FONT,
                 color=frame.SECOND).next_to(left, UP, buff=0.15),
            Text(f"{-CENTRE[1]:g} cm", font_size=frame.MIN_FONT,
                 color=frame.SECOND).next_to(down, RIGHT, buff=0.2),
        )
        return [GrowArrow(left), GrowArrow(down), FadeIn(labels)]

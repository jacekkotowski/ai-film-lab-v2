"""physics-drop -- a ball falls and bounces: pymunk drives a Manim dot (a TEST, in no film).

Run with both extras:
    uv run --directory slides --extra render --extra physics python -m aimanim.look still physics-drop
"""

import sys
from pathlib import Path

import pymunk
from manim import Dot, FadeIn, Line, Scene, Wait

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit, physics  # noqa: E402

# ---- content ---------------------------------------------------------------
TITLE = "Drop"
FLOOR_Y = -2.0
START = (0.0, 5.0)
RADIUS = 0.3
BOUNCE = 0.6                       # share of speed kept at each bounce
SECONDS = 3.0

# ---- timing ----------------------------------------------------------------
BEAT_WORDS: list[str] = []
BEAT_LINES = [0]
RUN_TIMES = [3.0]                  # = SECONDS (a literal: look.py reads it without running the scene)


def simulate():
    space = pymunk.Space()
    space.gravity = (0, -9.81)
    floor = pymunk.Segment(space.static_body, (-4, FLOOR_Y), (4, FLOOR_Y), 0)
    floor.elasticity = BOUNCE
    ball = pymunk.Body(1, pymunk.moment_for_circle(1, 0, RADIUS))
    ball.position = START
    shape = pymunk.Circle(ball, RADIUS)
    shape.elasticity = BOUNCE
    space.add(floor, ball, shape)
    return physics.track(space, [ball], SECONDS)


class Slide(Scene):
    def construct(self):
        self.frames = simulate()
        floor = Line((-4, FLOOR_Y, 0), (4, FLOOR_Y, 0)).set_stroke(frame.INK, 4)
        steps = [self.drop]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.title(TITLE), floor],
                beat_words=BEAT_WORDS)

    def drop(self):
        ball = Dot(radius=RADIUS, color=frame.ACCENT)
        kit.replay(ball, self.frames)
        self.add(ball)
        return [Wait(RUN_TIMES[0])]

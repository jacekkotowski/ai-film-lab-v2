"""face-two -- face is two faces: mianzi, worn outside and lit by the
crowd, and lian inside, which stays when nobody claps.

Content: spec.md. Slide 1 of love-as-a-face-threatening-act. The rings
are shared with face-fail (aimanim/faces.py, I14).

    uv run --extra render manim -s -r 540,960 --media_dir scenes/face-two/out scenes/face-two/scene.py Slide
"""

import sys
from pathlib import Path

from manim import Circle, Create, FadeIn, FadeOut, Scene, Transform, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402
from aimanim.faces import (CENTRE, INNER_R, LIAN_Y, MIANZI_Y, OUTER_R,  # noqa: E402
                           RING_W)

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Two faces"
FACE, MIANZI, LIAN = "face", "mianzi", "lian"

# ---- layout --------------------------------------------------------------
ONE_R = (OUTER_R + INNER_R) / 2  # the one face before it splits: 2.6
FACE_Y = CENTRE[1] - 0.25        # "face" in the middle, where "lian" will be
CROWD_ROWS = (-2.3, -3.2)        # centres of the two rows of people
CROWD_N, CROWD_PITCH, CROWD_H = 11, 0.7, 0.6

# ---- timing --------------------------------------------------------------
BEAT_WORDS = ["face", "splits", "mianzi", "lian", "lose", "what"]
BEAT_LINES = [0, 2, 3, 3, 4, 5]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def ring(r, color):
    return Circle(radius=r).move_to((*CENTRE, 0)).set_stroke(color, RING_W)


class Slide(Scene):
    def construct(self):
        steps = [self.step_face, self.step_split, self.step_mianzi,
                 self.step_lian, self.step_lose, self.step_stays]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.title(TITLE)],
                beat_words=BEAT_WORDS)

    def step_face(self):
        self.outer = ring(ONE_R, frame.INK)
        self.face = kit.text(FACE, CENTRE[0], FACE_Y)
        return [Create(self.outer), FadeIn(self.face)]

    def step_split(self):
        self.inner = ring(INNER_R, frame.INK)
        return [Transform(self.outer, ring(OUTER_R, frame.SECOND)),
                Create(self.inner), FadeOut(self.face)]

    def step_mianzi(self):
        self.mianzi = kit.text(MIANZI, CENTRE[0], MIANZI_Y, frame.SECOND)
        # 11 in the front row, 10 behind, in the gaps
        pts = [((k - (CROWD_N - 1 - j) / 2) * CROWD_PITCH, y)
               for j, y in enumerate(CROWD_ROWS) for k in range(CROWD_N - j)]
        self.crowd = kit.people(pts, CROWD_H)
        return [FadeIn(self.mianzi), FadeIn(self.crowd)]

    def step_lian(self):
        self.lian = kit.text(LIAN, CENTRE[0], LIAN_Y)
        return [FadeIn(self.lian)]

    def step_lose(self):
        return [FadeOut(self.crowd),
                VGroup(self.outer, self.mianzi).animate.set_color(frame.DIM)]

    def step_stays(self):
        return [VGroup(self.inner, self.lian).animate.set_color(frame.ACCENT)]

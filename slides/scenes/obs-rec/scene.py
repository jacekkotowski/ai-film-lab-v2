"""obs-rec -- slide 03 Target coordinates: position, distance, azimuth -> Rec -> the target's E and N.

Film: Map and Calculator 01 - Observer. Content: his plan,
film/docs/plans/2026-10-11/PLAN-map-calculator.md (slide 03), numbers
computed here. x of Rec is the step north, y the step east (the angle is an
azimuth). Pieces come one after another on his words; the still is the end of B.

    uv run --directory slides python -m aimanim.look still obs-rec full
"""

import math
import sys
from pathlib import Path

from manim import FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import kit  # noqa: E402

# ---- content (his plan, slide 03) -------------------------------------------
SERIES = "MAP AND CALCULATOR · 01 · OBSERVER"
ME = (34500, 21800)                               # E, N in metres
D, AZ = 2400, 65                                  # rangefinder (m), map azimuth (deg)
A_TAG, A_HEAD = "SLIDE 3 · A", "I see the target"
A_SUB = "Your position, the rangefinder distance, the map azimuth."
A_FOOT = "Comma: SHIFT + )"
B_TAG, B_HEAD = "SLIDE 3 · B", "Add the shifts"
B_SUB = "x is the step north, y the step east."
B_FOOT = "✓ North-east: x and y positive"

X = D * math.cos(math.radians(AZ))                # 1014.283828, north
Y = D * math.sin(math.radians(AZ))                # 2175.138689, east
TARGET = (ME[0] + round(Y), ME[1] + round(X))     # E 36675, N 22814

# ---- layout ----------------------------------------------------------------
GRID = dict(e0=33000, e1=37000, n0=21000, n1=24000, left=-2.85, bottom=-2.5,
            scale=0.0015)                         # 4 x 3 km; "37" ends 3.55, "N" tops 3.14
KEYS_Y, SCREEN_TOP, A_FOOT_B = 2.8, 1.9, -3.0

# ---- timing ----------------------------------------------------------------
# Each step on its word in [03] of slides.script.txt (Claude's draft, 2026-10-11).
BEAT_WORDS = ["I", "position", "2400|two", "Press", "is", "Add", "step", "Equals",
              "legs", "them", "North"]
BEAT_LINES = [0, 1, 1, 2, 3, 4, 4, 5, 5, 6, 7]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def the_map(b: bool) -> VGroup:
    """A: ME, the 65° line, 2400 m. B adds the north leg, the east leg, TARGET."""
    grid, at = kit.map_grid(**GRID)
    corner = (ME[0], TARGET[1])
    g = VGroup(grid,
               kit.map_line(at, ME, TARGET, f"{D} m", side=-1, where=0.6),
               kit.azimuth_arc(at, ME, AZ, 0.6, f"{AZ}°"),
               kit.map_point(at, *ME, "ME", kit.PAPER, "down"))
    if b:
        g.add(kit.map_line(at, ME, corner, f"{round(X)}", kit.MUTED, dashed=True,
                           label_color=kit.PAPER),
              kit.map_line(at, corner, TARGET, f"{round(Y)}", kit.MUTED, dashed=True,
                           where=0.3, label_color=kit.PAPER),
              kit.map_point(at, *TARGET, "TARGET", kit.GREEN, "up"))
    return g


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        e, n = TARGET
        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.a_sub = kit.note(A_SUB, kit.below(self.a_top[1]))
        self.a_card = kit.card([f"ME\nE {ME[0]} · N {ME[1]}", f"D {D} m", f"Az {AZ}°"],
                               self.a_sub.get_bottom()[1] - 0.3)
        self.a_map = the_map(False)
        self.keys = kit.keys(["SHIFT", "−"], KEYS_Y, sep="+", then="Rec(")
        self.a_screen = kit.screen(f"Rec({D},{AZ})", rows=2, top=SCREEN_TOP)
        self.a_foot = kit.note(A_FOOT, A_FOOT_B)
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.b_sub = kit.note(B_SUB, kit.below(self.b_top[1]))
        self.b_screen = kit.screen(f"Rec({D},{AZ})", [f"x={X:.10g}", f"y={Y:.10g}"],
                                   top=SCREEN_TOP)
        self.b_map = the_map(True)
        self.b_card = kit.card([f"E {ME[0]} + {round(Y)}\n= {e}",
                                f"N {ME[1]} + {round(X)}\n= {n}",
                                f"TARGET\nE {e} · N {n}"],
                               self.b_top[1].get_bottom()[1] - 0.3, hl=2)
        self.b_foot = kit.note(B_FOOT, kit.below(self.b_card), kit.GREEN)
        steps = [self.a_head, self.a_says, self.a_map_in, self.a_keys,
                 self.a_comma, self.b_head, self.b_says, self.b_results, self.b_map_in,
                 self.b_card_in, self.b_ok]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    # ---- A: I see the target ----------------------------------------------
    def a_head(self):
        return [FadeIn(self.a_top)]

    def a_says(self):                              # his three inputs and their values
        return [FadeIn(self.a_sub), FadeIn(self.a_card)]

    def a_map_in(self):
        return [FadeOut(VGroup(self.a_sub, self.a_card)), FadeIn(self.a_map)]

    def a_keys(self):
        return [FadeOut(self.a_map), FadeIn(self.keys), FadeIn(self.a_screen)]

    def a_comma(self):
        return [FadeIn(self.a_foot)]

    # ---- B: add the shifts -------------------------------------------------
    def b_head(self):
        return [FadeOut(VGroup(self.a_top, self.keys, self.a_foot)), FadeIn(self.b_top)]

    def b_says(self):
        return [FadeIn(self.b_sub)]

    def b_results(self):
        return [FadeOut(self.a_screen), FadeIn(self.b_screen)]

    def b_map_in(self):
        return [FadeOut(VGroup(self.b_sub, self.b_screen)), FadeIn(self.b_map)]

    def b_card_in(self):
        return [FadeOut(self.b_map), FadeIn(self.b_card)]

    def b_ok(self):
        return [FadeIn(self.b_foot)]

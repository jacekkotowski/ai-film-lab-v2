"""gun-angle-t -- slide 03 Angle T: my line and the gun's line meet at the target.

Film: Map and Calculator 02 - Gun. Content: the agreed outline,
film/docs/plans/2026-10-11/PLAN-map-calculator-02.md (slide 03), numbers
computed here. The gun knows only my DIRECTION 1160, so angle T = 1160 − 504
= 656 mils; told to the observer at 500 or more, to the nearest 100 (FM 6-40).
Pieces come one after another on his words; the still is the end of B.

A close-up of the sheet around the target (1.5 units per km): my line from ME,
the gun's line leaving at the bottom edge towards the gun, the angle between
them at the target. The last step trades the B card for the ✓ line.

    uv run --directory slides python -m aimanim.look still gun-angle-t full
"""

import math
import sys
from pathlib import Path

import numpy as np
from manim import UP, Arc, FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (the outline, slide 03) -----------------------------------------
SERIES = "MAP AND CALCULATOR · 02 · GUN"
ME, TARGET, GUN = (34500, 21800), (36675, 22814), (33000, 16000)   # E, N in metres
DIRECTION, GT_MILS = 1160, 504                    # my call; the gun's (slide 02)
MILS_PER_DEG = 17.78
ANGLE_T = DIRECTION - GT_MILS                     # 656
SAID = round(ANGLE_T, -2)                         # 700: to the nearest 100
A_TAG, A_HEAD = "SLIDE 3 · A", "Two lines meet at the target"
B_TAG, B_HEAD = "SLIDE 3 · B", f"ANGLE T {SAID}"
B_RULES = ["500 or more →\ntell the observer", "to the nearest 100"]
B_FOOT = "✓ My left and right are not the gun's"

# ---- layout ----------------------------------------------------------------
SCALE = 0.0018                                    # frame units per metre: TARGET's label under
GRID = dict(e0=34000, e1=37000, n0=21000, n1=23000,   # the headline, the E numbers over
            left=-3.0, bottom=-0.6, scale=SCALE)      # the A card
ARC_R = 1.2                                       # angle T's arc at the target
GAP = 0.3
FLOOR = frame.BOTTOM + 0.05

# ---- timing ----------------------------------------------------------------
# Each step on its word in [03] of slides.script.txt (Claude's draft, 2026-10-11).
BEAT_WORDS = ["Two", "Mine", "gun", "Between", "1160", "Angle", "500", "My"]
BEAT_LINES = [0, 1, 1, 2, 3, 4, 5, 6]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def stack_up(*mobs, floor: float = FLOOR) -> None:
    """Stand the mobjects one on another, the first on `floor`."""
    y = floor
    for m in mobs:
        m.shift(UP * (y - m.get_bottom()[1]))
        y = m.get_top()[1] + GAP


def edge_point(p, bearing: float, n_edge: float):
    """Where the line from map point p at `bearing` degrees meets the grid line N n_edge."""
    dn = n_edge - p[1]
    return (p[0] + dn * math.tan(math.radians(bearing)), n_edge)


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        g, at = kit.map_grid(**GRID)
        lines, nums = g[0], g[1]
        self.e_nums = VGroup(*nums[:4], nums[-2])                 # 34..37 and "E"
        self.map = VGroup(lines, nums[4:7])                       # N 21..23
        gt_bearing = GT_MILS / MILS_PER_DEG                       # the gun's line, degrees
        enter = edge_point(TARGET, gt_bearing, GRID["n0"])        # from the gun, at the edge
        self.mine = VGroup(kit.map_line(at, ME, TARGET, f"{DIRECTION}", side=1, where=0.45),
                           kit.map_point(at, *ME, "ME", kit.PAPER, "down"),
                           kit.map_point(at, *TARGET, "TARGET", kit.GREEN, "up"))
        self.gun_line = kit.map_line(at, enter, TARGET, f"{GT_MILS}", frame.SECOND, side=-1,
                                     where=0.45)
        # angle T: from the gun's line to mine, at the target (bearings back from it)
        c = np.array(at(*TARGET))
        to_gun, to_me = 180 + gt_bearing, 180 + DIRECTION / MILS_PER_DEG
        arc = Arc(radius=ARC_R, start_angle=math.radians(90 - to_gun),
                  angle=-math.radians(to_me - to_gun), arc_center=c).set_stroke(kit.AMBER, 5)
        mid = math.radians((to_gun + to_me) / 2)
        p = c + (ARC_R + 0.45) * np.array([math.sin(mid), math.cos(mid), 0])
        t = kit.text("T", p[0], p[1] - kit.cap(frame.MIN_FONT, kit.SANS) / 2, kit.AMBER,
                     font=kit.SANS, weight="BOLD")
        self.angle = VGroup(arc, t)

        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.a_card = kit.card([f"{DIRECTION} − {GT_MILS}\n= {ANGLE_T} mils"], 0)
        stack_up(self.a_card)
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.b_card = kit.card(B_RULES, 0)
        stack_up(self.b_card)
        self.b_foot = kit.note(B_FOOT, 0, kit.GREEN)
        stack_up(self.b_foot)
        steps = [self.a_head, self.a_map, self.a_gun, self.a_angle, self.a_diff,
                 self.b_head, self.b_rules, self.b_ok]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    # ---- A: two lines meet at the target ------------------------------------
    def a_head(self):
        return [FadeIn(self.a_top)]

    def a_map(self):                               # my line at 1160
        return [FadeIn(VGroup(self.map, self.e_nums)), FadeIn(self.mine)]

    def a_gun(self):                               # the gun's at 504
        return [FadeIn(self.gun_line)]

    def a_angle(self):
        return [FadeIn(self.angle)]

    def a_diff(self):
        return [FadeIn(self.a_card)]

    # ---- B: ANGLE T 700 -------------------------------------------------------
    def b_head(self):
        return [FadeOut(VGroup(self.a_top, self.a_card)), FadeIn(self.b_top)]

    def b_rules(self):                             # the card covers the E numbers
        return [FadeOut(self.e_nums), FadeIn(self.b_card)]

    def b_ok(self):                                # the E numbers back over the ✓ line
        return [FadeOut(self.b_card), FadeIn(VGroup(self.b_foot, self.e_nums))]

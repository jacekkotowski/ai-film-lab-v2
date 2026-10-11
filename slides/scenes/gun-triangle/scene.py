"""gun-triangle -- slide 01 The triangle: me, the target, the gun; what I send.

Film: Map and Calculator 02 - Gun. Content: the agreed outline,
film/docs/plans/2026-10-11/PLAN-map-calculator-02.md (slide 01), numbers
computed here. ME and TARGET are video 01's; the gun is Claude's choice.
Pieces come one after another on his words; the still is the end of B.

The triangle is 4 x 7 km, taller than wide: the whole sheet fits under the
headline at 0.78 units per km. B is a message, not a place: the map steps
back for the card.

    uv run --directory slides python -m aimanim.look still gun-triangle full
"""

import sys
from pathlib import Path

from manim import FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (the outline, slide 01) -----------------------------------------
SERIES = "MAP AND CALCULATOR · 02 · GUN"
ME, TARGET, GUN = (34500, 21800), (36675, 22814), (33000, 16000)   # E, N in metres
AZ, MILS_PER_DEG = 65, 17.78                      # my map azimuth (video 01), 6400 / 360
A_TAG, A_HEAD = "SLIDE 1 · A", "The gun can't see the target"
B_TAG, B_HEAD = "SLIDE 1 · B", "What I send"
B_FOOT = "✓ Grid for the gun, direction for my corrections"

MILS = AZ * MILS_PER_DEG                          # 1155.7
DIRECTION = int(round(MILS, -1))                  # 1160: four digits, nearest 10

# ---- layout ----------------------------------------------------------------
SCALE = 0.00078                                   # frame units per metre: N 23 under the headline
GRID = dict(e0=32000, e1=38000, n0=15000, n1=23000, left=-2.6, bottom=-2.95, scale=SCALE)
E_EVERY = 2                                       # km between E numbers: 0.78 apart they touch

# ---- timing ----------------------------------------------------------------
# Each step on its word in [01] of slides.script.txt (Claude's draft, 2026-10-11).
BEAT_WORDS = ["The", "My", "me", "gun", "line", "What", "grid", "direction", "Grid"]
BEAT_LINES = [0, 1, 1, 2, 2, 3, 3, 3, 4]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        g, at = kit.map_grid(**GRID)
        lines, nums = g[0], g[1]
        cols = list(range(GRID["e0"] // 1000, GRID["e1"] // 1000 + 1))
        n_rows = list(range(GRID["n0"] // 1000, GRID["n1"] // 1000 + 1))
        e_nums = [m for k, m in zip(cols, nums) if k % E_EVERY == 0] + [nums[-2]]  # and "E"
        n_nums = nums[len(cols):len(cols) + len(n_rows) - 1]          # 23: the headline's
        self.map = VGroup(lines, *e_nums, *n_nums)
        self.mine = VGroup(kit.map_line(at, ME, TARGET),
                           kit.map_point(at, *ME, "ME", kit.PAPER, "left"),
                           kit.map_point(at, *TARGET, "TARGET", kit.GREEN, "right"))
        self.gun = kit.map_point(at, *GUN, "GUN", frame.SECOND, "right")
        self.gun_line = kit.map_line(at, GUN, TARGET, color=frame.SECOND)

        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.card = kit.card([f"TARGET\nE {TARGET[0]} · N {TARGET[1]}",
                              f"{AZ} × {MILS_PER_DEG} = {round(MILS)}",
                              f"DIRECTION {DIRECTION}"],
                             self.b_top[1].get_bottom()[1] - 0.3, hl=2)
        self.foot = kit.note(B_FOOT, kit.below(self.card), kit.GREEN)
        steps = [self.a_head, self.a_map, self.a_mine, self.a_gun, self.a_line,
                 self.b_head, self.b_grid, self.b_direction, self.b_ok]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    # ---- A: the gun can't see the target -----------------------------------
    def a_head(self):
        return [FadeIn(self.a_top)]

    def a_map(self):
        return [FadeIn(self.map)]

    def a_mine(self):                              # me, my line, the target (video 01)
        return [FadeIn(self.mine)]

    def a_gun(self):
        return [FadeIn(self.gun)]

    def a_line(self):                              # the gun's line to the same target
        return [FadeIn(self.gun_line)]

    # ---- B: what I send ------------------------------------------------------
    def b_head(self):                              # a message, not a place: the map steps back
        return [FadeOut(VGroup(self.a_top, self.map, self.mine, self.gun, self.gun_line)),
                FadeIn(self.b_top)]

    def b_grid(self):
        c = self.card
        return [FadeIn(VGroup(c[0], c.rows[0]))]

    def b_direction(self):
        c = self.card
        return [FadeIn(VGroup(*c[1:3], c.rows[1], c.rows[2]))]

    def b_ok(self):
        return [FadeIn(self.foot)]

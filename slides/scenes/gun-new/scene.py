"""gun-new -- slide 05 New data for the gun: Pol again, to the new point; the same burst in other words.

Film: Map and Calculator 02 - Gun. Content: the agreed outline,
film/docs/plans/2026-10-11/PLAN-map-calculator-02.md (slide 05), numbers
computed here. The new point is slide 04's, rounded to the metre (E 36783,
N 22820): Pol(6819.6,3782.6) is 7.52 units at 56, wider than the screen.
Pieces come one after another on his words; the still is the end of B.

The map is slide 02's (0.5 units per km). B compares two messages: the map
steps back for the card and the ✓ line.

    uv run --directory slides python -m aimanim.look still gun-new full
"""

import math
import sys
from pathlib import Path

from manim import UP, FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (the outline, slide 05) -----------------------------------------
SERIES = "MAP AND CALCULATOR · 02 · GUN"
TARGET, NEW, GUN = (36675, 22814), (36783, 22820), (33000, 16000)   # E, N in metres
MILS_PER_DEG = 17.78
CALL = "RIGHT 40 · ADD 100"                       # my correction (slide 04)
A_TAG, A_HEAD = "SLIDE 5 · A", "Gun to the new point"
B_TAG, B_HEAD = "SLIDE 5 · B", "Same burst, other words"


def pol(dn, de):
    """The Casio's Pol: north first; r and θ (an azimuth, degrees)."""
    return math.hypot(dn, de), math.degrees(math.atan2(de, dn))


R0, T0 = pol(TARGET[1] - GUN[1], TARGET[0] - GUN[0])          # slide 02: 7742 m, 28.34°
DN, DE = NEW[1] - GUN[1], NEW[0] - GUN[0]                       # 6820, 3783
R, THETA = pol(DN, DE)                                          # 7798.94, 29.0157
MILS0 = round(round(T0, 2) * MILS_PER_DEG)                      # 504
MILS = round(round(THETA, 2) * MILS_PER_DEG)                    # 516
ADD_M, RIGHT_MILS = round(R) - round(R0), MILS - MILS0          # +57 m, +12 mils
KM = round(R0 / 1000, 1)                                        # 7.7
ACROSS = round(KM * RIGHT_MILS)                                 # 92 m: video 01's rule
B_FOOT = (f"✓ {KM} × {RIGHT_MILS} ≈ {ACROSS} m right: I asked mostly ADD, "
          "the gun moves mostly RIGHT")

# ---- layout ----------------------------------------------------------------
SCALE = 0.0005                                    # slide 02's map
GRID = dict(e0=32000, e1=38000, n0=15000, n1=23000, left=-1.8, bottom=-0.6, scale=SCALE)
EVERY = 2                                         # km between numbers
GAP = 0.3
FLOOR = frame.BOTTOM + 0.05

# ---- timing ----------------------------------------------------------------
# Each step on its word in [05] of slides.script.txt (Claude's draft, 2026-10-11).
BEAT_WORDS = ["Gun", "North", "SHIFT", "Equals", "degrees", "Same", "said", "adds", "times"]
BEAT_LINES = [0, 1, 2, 3, 3, 4, 5, 6, 6]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def stack_up(*mobs, floor: float = FLOOR) -> None:
    """Stand the mobjects one on another, the first on `floor`."""
    y = floor
    for m in mobs:
        m.shift(UP * (y - m.get_bottom()[1]))
        y = m.get_top()[1] + GAP


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        g, at = kit.map_grid(**GRID)
        lines, nums = g[0], g[1]
        cols = list(range(GRID["e0"] // 1000, GRID["e1"] // 1000 + 1))
        n_rows = list(range(GRID["n0"] // 1000, GRID["n1"] // 1000 + 1))
        row = dict(zip(n_rows, nums[len(cols):len(cols) + len(n_rows)]))
        self.e_nums = VGroup(*[m for k, m in zip(cols, nums) if k % EVERY == 0], nums[-2])
        self.n_nums = VGroup(*[row[k] for k in n_rows[:-1]               # 16: GUN's label
                               if k % EVERY == 0 and k != GUN[1] // 1000])
        self.grid = lines
        corner = (GUN[0], NEW[1])
        self.legs = VGroup(kit.map_line(at, GUN, corner, None, kit.MUTED, dashed=True),
                           kit.map_line(at, corner, NEW, None, kit.MUTED, dashed=True))
        self.leg_labels = VGroup(
            kit.map_line(at, GUN, corner, f"{DN}", side=-1, where=0.45,
                         label_color=kit.PAPER)[1],
            kit.map_line(at, corner, NEW, f"{DE}", side=-1, where=0.5,
                         label_color=kit.PAPER)[1])
        self.points = VGroup(kit.map_point(at, *GUN, "GUN", frame.SECOND, "left"),
                             kit.map_point(at, *NEW, "NEW", kit.GREEN, "right"))
        self.line = kit.map_line(at, GUN, NEW, f"{round(R)} m", frame.SECOND, side=-1,
                                 where=0.55)
        self.arc = kit.azimuth_arc(at, GUN, THETA, 0.6, f"{MILS} mils", label_at=100)

        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.keys = kit.keys(["SHIFT", "+"], 0, sep="+", then="Pol(")
        expr = f"Pol({DN},{DE})"
        self.a_screen = kit.screen(expr, rows=2)
        stack_up(self.a_screen, self.keys)
        self.results = kit.screen(expr, [f"r={R:.10g}", f"θ={THETA:.10g}"])
        stack_up(self.results)
        self.a_card = kit.card([f"Range {round(R)} m",
                                f"{THETA:.2f} × {MILS_PER_DEG}\n≈ {MILS} mils"], 0)
        stack_up(self.a_card)
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.b_card = kit.card([f"ME\n{CALL}", f"GUN\n+{ADD_M} m · +{RIGHT_MILS} mils"],
                               self.b_top[1].get_bottom()[1] - GAP, hl=1)
        self.b_foot = kit.note(B_FOOT, kit.below(self.b_card), kit.GREEN)
        steps = [self.a_head, self.a_map, self.a_keys, self.a_results, self.a_answer,
                 self.b_head, self.b_me, self.b_gun, self.b_ok]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    # ---- A: gun to the new point ----------------------------------------------
    def a_head(self):
        return [FadeIn(self.a_top)]

    def a_map(self):                               # new point minus gun, on the map
        return [FadeIn(VGroup(self.grid, self.e_nums, self.n_nums, self.points)),
                FadeIn(VGroup(self.legs, self.leg_labels))]

    def a_keys(self):                              # the drawing steps back behind the keys
        return [FadeOut(VGroup(self.legs, self.leg_labels, self.points, self.n_nums,
                               self.e_nums)),
                FadeIn(self.keys), FadeIn(self.a_screen)]

    def a_results(self):
        return [FadeOut(VGroup(self.keys, self.a_screen)), FadeIn(self.results)]

    def a_answer(self):                            # the answer on the map, the card under it
        return [FadeOut(self.results), FadeIn(self.a_card),
                FadeIn(VGroup(self.n_nums, self.legs, self.line, self.arc, self.points))]

    # ---- B: same burst, other words ---------------------------------------------
    def b_head(self):                              # two messages side by side: the map steps back
        return [FadeOut(VGroup(self.a_top, self.a_card, self.grid, self.n_nums, self.legs,
                               self.line, self.arc, self.points)),
                FadeIn(self.b_top)]

    def b_me(self):
        c = self.b_card
        return [FadeIn(VGroup(c[0], c.rows[0]))]

    def b_gun(self):
        c = self.b_card
        return [FadeIn(VGroup(*c[1:3], c.rows[1]))]

    def b_ok(self):
        return [FadeIn(self.b_foot)]

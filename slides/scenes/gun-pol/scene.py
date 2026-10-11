"""gun-pol -- slide 02 Gun to target: target minus gun -> Pol -> range and direction.

Film: Map and Calculator 02 - Gun. Content: the agreed outline,
film/docs/plans/2026-10-11/PLAN-map-calculator-02.md (slide 02), numbers
computed here. Pol takes the north difference first, so θ is an azimuth
(north-east: positive, nothing to add). Pieces come one after another on his
words; the still is the end of B.

The map is smaller than slide 01's (0.5 units per km, not 0.78), in the band under
the headline, so a card fits under it. While the keys and the screen are up
(5.5 units tall) the drawing steps back, only the grid stays. The last step
trades the B card for the ✓ line: the map keeps the answer (7742 m, 504 mils).

    uv run --directory slides python -m aimanim.look still gun-pol full
"""

import math
import sys
from pathlib import Path

from manim import UP, FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (the outline, slide 02) -----------------------------------------
SERIES = "MAP AND CALCULATOR · 02 · GUN"
TARGET, GUN = (36675, 22814), (33000, 16000)      # E, N in metres
MILS_PER_DEG = 17.78                              # 6400 / 360, as typed
A_TAG, A_HEAD = "SLIDE 2 · A", "Target minus gun"
B_TAG, B_HEAD = "SLIDE 2 · B", "Range and direction"
B_FOOT = "✓ North-east: nothing to add"

DN, DE = TARGET[1] - GUN[1], TARGET[0] - GUN[0]   # 6814, 3675
R = math.hypot(DN, DE)                            # 7741.848746
THETA = math.degrees(math.atan2(DE, DN))          # 28.33942807
MILS = round(round(THETA, 2) * MILS_PER_DEG)      # 504

# ---- layout ----------------------------------------------------------------
SCALE = 0.0005                                    # frame units per metre: a card fits under it
GRID = dict(e0=32000, e1=38000, n0=15000, n1=23000, left=-1.8, bottom=-0.6, scale=SCALE)
EVERY = 2                                         # km between numbers: 0.45 apart they touch
GAP = 0.3                                         # between stacked panels
FLOOR = frame.BOTTOM + 0.05                       # the panels stand here

# ---- timing ----------------------------------------------------------------
# Each step on its word in [02] of slides.script.txt (Claude's draft, 2026-10-11).
BEAT_WORDS = ["Now", "North", "22814", "SHIFT", "Range", "Equals", "Times", "North"]
BEAT_LINES = [0, 1, 2, 3, 4, 5, 6, 7]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


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
        corner = (GUN[0], TARGET[1])
        self.legs = VGroup(kit.map_line(at, GUN, corner, None, kit.MUTED, dashed=True),
                           kit.map_line(at, corner, TARGET, None, kit.MUTED, dashed=True))
        self.leg_labels = VGroup(
            kit.map_line(at, GUN, corner, f"{DN}", side=-1, where=0.45,
                         label_color=kit.PAPER)[1],
            kit.map_line(at, corner, TARGET, f"{DE}", side=-1, where=0.5,
                         label_color=kit.PAPER)[1])
        self.points = VGroup(kit.map_point(at, *GUN, "GUN", frame.SECOND, "left"),
                             kit.map_point(at, *TARGET, "TARGET", kit.GREEN, "right"))
        self.line = kit.map_line(at, GUN, TARGET, f"{round(R)} m", frame.SECOND, side=-1,
                                 where=0.55)
        self.arc = kit.azimuth_arc(at, GUN, THETA, 0.6, f"{MILS} mils", label_at=100)

        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.a_card = kit.card([f"ΔN = {TARGET[1]} − {GUN[1]}\n= {DN}",
                                f"ΔE = {TARGET[0]} − {GUN[0]}\n= {DE}"], 0)
        stack_up(self.a_card)
        self.keys = kit.keys(["SHIFT", "+"], 0, sep="+", then="Pol(")
        expr = f"Pol({DN},{DE})"
        self.a_screen = kit.screen(expr, rows=2)
        stack_up(self.a_screen, self.keys)
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.b_screen = kit.screen(expr, [f"r={R:.10g}", f"θ={THETA:.10g}"])
        stack_up(self.b_screen)
        self.b_card = kit.card([f"Range {round(R)} m",
                                f"{THETA:.2f} × {MILS_PER_DEG}\n≈ {MILS} mils"], 0)
        stack_up(self.b_card)
        self.b_foot = kit.note(B_FOOT, 0, kit.GREEN)
        stack_up(self.b_foot)
        steps = [self.a_head, self.a_legs, self.a_diffs, self.a_keys,
                 self.b_head, self.b_results, self.b_card_in, self.b_ok]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    # ---- A: target minus gun -----------------------------------------------
    def a_head(self):                              # the map with the headline: "gun" is 0.4 s
        return [FadeIn(self.a_top),                # before "North" (rehearsed)
                FadeIn(VGroup(self.grid, self.e_nums, self.n_nums, self.points))]

    def a_legs(self):                              # north first, then east
        return [FadeIn(VGroup(self.legs, self.leg_labels))]

    def a_diffs(self):
        return [FadeOut(self.e_nums), FadeIn(self.a_card)]

    def a_keys(self):                              # the drawing steps back behind the keys
        return [FadeOut(VGroup(self.a_card, self.legs, self.leg_labels, self.points,
                               self.n_nums)),
                FadeIn(self.keys), FadeIn(self.a_screen)]

    # ---- B: range and direction ---------------------------------------------
    def b_head(self):
        return [FadeOut(VGroup(self.a_top, self.keys)), FadeIn(self.b_top)]

    def b_results(self):
        return [FadeOut(self.a_screen), FadeIn(self.b_screen)]

    def b_card_in(self):                           # the answer on the map, the card under it
        return [FadeOut(self.b_screen), FadeIn(self.b_card),
                FadeIn(VGroup(self.n_nums, self.legs, self.line, self.arc, self.points))]

    def b_ok(self):                                # the E numbers back over the ✓ line
        return [FadeOut(self.b_card), FadeIn(VGroup(self.b_foot, self.e_nums))]

"""obs-pol -- slide 04 Direction and distance: target minus me -> Pol -> distance and azimuth.

Film: Map and Calculator 01 - Observer. Content: his plan,
film/docs/plans/2026-10-11/PLAN-map-calculator.md (slide 04), numbers
computed here. Pol takes the north difference first, so θ is an azimuth
(-180..180: a negative one gets 360). 4232 mils is his choice (x 17.78).
Pieces come one after another on his words; the still is the end of B.

The map is the background from "target" to the end (his choice, 2026-10-11).
Cards, keys and screens stand on the bottom edge over it. While the keys and
the screen are up (7.3 units tall) nothing of the drawing fits above them, so
ME, TARGET and the legs step back and return with the 238° arc. The last
step trades the B card for the ✓ line: card and ✓ together (7.0) would leave
1.0 unit of map, and "South-west" is read on the map.

    uv run --directory slides python -m aimanim.look still obs-pol full
"""

import math
import sys
from pathlib import Path

from manim import UP, FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (his plan, slide 04) -------------------------------------------
SERIES = "MAP AND CALCULATOR · 01 · OBSERVER"
ME, TARGET = (34500, 21800), (32100, 20300)       # E, N in metres
MILS_PER_DEG = 17.78                              # his: 6400 / 360, as typed
A_TAG, A_HEAD = "SLIDE 4 · A", "Target minus me"
A_SUB = "North difference first, then east."
A_FOOT = "Type minus with the (−) key."
B_TAG, B_HEAD = "SLIDE 4 · B", "Negative? Add 360"
B_SUB = "r is the distance, θ the azimuth."
B_FOOT = "✓ South-west: 180–270°"

DN, DE = TARGET[1] - ME[1], TARGET[0] - ME[0]     # −1500, −2400
R = math.hypot(DN, DE)                            # 2830.19434
THETA = math.degrees(math.atan2(DE, DN))          # −122.0053832
AZ = round(THETA, 1) + 360                        # 238.0, as he says it
MILS = round(AZ * MILS_PER_DEG)                   # 4232


def m(v) -> str:
    """As the screen and the cards show it: U+2212 for minus."""
    return f"{v}".replace("-", "−")


# ---- layout ----------------------------------------------------------------
SCALE = 0.0013                                    # frame units per metre: "−1500" fits
ME_X, ME_Y = 1.3, 3.4                             # right of the north leg; TARGET's label
GRID = dict(e0=32000, e1=36000, n0=18000, n1=23000,   # clears the B card (top 0.48)
            left=ME_X - (ME[0] - 32000) * SCALE,
            bottom=ME_Y - (ME[1] - 18000) * SCALE, scale=SCALE)
GAP = 0.3                                         # between stacked panels
FLOOR = frame.BOTTOM + 0.05                       # the panels stand here

# ---- timing ----------------------------------------------------------------
# Each step on its word in [04] of slides.script.txt (his narration, approved 2026-10-11).
BEAT_WORDS = ["Target", "difference", "target", "minus", "SHIFT", "Type", "Negative",
              "distance", "Equals", "makes", "Times", "South"]
BEAT_LINES = [0, 0, 1, 1, 2, 3, 4, 6, 7, 8, 9, 10]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def stack_up(*mobs, floor: float = FLOOR) -> None:
    """Stand the mobjects one on another, the first on `floor`."""
    y = floor
    for m_ in mobs:
        m_.shift(UP * (y - m_.get_bottom()[1]))
        y = m_.get_top()[1] + GAP


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        # the map: the grid, its numbers, and what is drawn on it
        g, at = kit.map_grid(**GRID)
        lines, nums = g[0], g[1]
        cols = list(range(GRID["e0"] // 1000, GRID["e1"] // 1000 + 1))
        n_rows = list(range(GRID["n0"] // 1000, GRID["n1"] // 1000 + 1))
        row = dict(zip(n_rows, nums[len(cols):len(cols) + len(n_rows)]))
        e_nums = [*nums[:len(cols)], nums[-2]]                        # and "E"
        shown = [k for k in n_rows[:-2]                               # top two: the headline's
                 if k != TARGET[1] // 1000]                           # TARGET's label's
        self.grid = VGroup(lines, *e_nums, *[row[k] for k in shown])
        self.low = VGroup(*e_nums, *[row[k] for k in shown
                                     if at(0, k * 1000)[1] < 1.0])    # under the A card
        self.high = VGroup(*[row[k] for k in shown if at(0, k * 1000)[1] >= 1.0])
        corner = (ME[0], TARGET[1])
        self.legs = VGroup(kit.map_line(at, ME, corner, None, kit.MUTED, dashed=True),
                           kit.map_line(at, corner, TARGET, None, kit.MUTED, dashed=True))
        self.leg_labels = VGroup(
            kit.map_line(at, ME, corner, m(DN), side=1, where=0.7, label_color=kit.PAPER)[1],
            kit.map_line(at, corner, TARGET, m(DE), side=1, where=0.0,
                         label_color=kit.PAPER)[1])
        self.points = VGroup(kit.map_point(at, *ME, "ME", kit.PAPER, "right", clear=0.95),
                             kit.map_point(at, *TARGET, "TARGET", kit.GREEN, "down"))
        self.line = kit.map_line(at, ME, TARGET)
        self.arc = kit.azimuth_arc(at, ME, AZ, 0.7, f"{AZ:.0f}°", label_at=285)

        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.a_sub = kit.note(A_SUB, kit.below(self.a_top[1]))
        self.a_card = kit.card([f"ΔN = {TARGET[1]} − {ME[1]}\n= {m(DN)}",
                                f"ΔE = {TARGET[0]} − {ME[0]}\n= {m(DE)}"], 0)
        stack_up(self.a_card)
        self.keys = kit.keys(["SHIFT", "+"], 0, sep="+", then="Pol(")
        expr = f"Pol({m(DN)},{m(DE)})"
        self.a_screen = kit.screen(expr, rows=2)
        self.a_foot = kit.note(A_FOOT, 0, kit.AMBER)
        stack_up(self.a_foot, self.a_screen, self.keys)
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.drop = FLOOR - self.a_screen.get_bottom()[1]             # the screen sits down
        self.b_screen = kit.screen(expr, [f"r={R:.9g}", f"θ={m(f'{THETA:.10g}')}"])
        self.b_sub = kit.note(B_SUB, 0)
        stack_up(self.b_screen, self.b_sub)
        self.b_card = kit.card([f"D {round(R)} m",
                                f"Az {m(round(THETA, 1))} + 360\n= {AZ:.1f}°",
                                f"{AZ:.1f} × {MILS_PER_DEG}\n≈ {MILS} mils"], 0)
        stack_up(self.b_card)
        self.b_foot = kit.note(B_FOOT, 0, kit.GREEN)
        stack_up(self.b_foot)
        steps = [self.a_head, self.a_says, self.a_map_in, self.a_diffs, self.a_keys,
                 self.a_minus, self.b_head, self.b_says, self.b_results, self.b_map_in,
                 self.b_card_in, self.b_ok]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    # ---- A: target minus me -----------------------------------------------
    def a_head(self):
        return [FadeIn(self.a_top)]

    def a_says(self):
        return [FadeIn(self.a_sub)]

    def a_map_in(self):
        return [FadeOut(self.a_sub),
                FadeIn(VGroup(self.grid, self.legs, self.leg_labels, self.points))]

    def a_diffs(self):
        return [FadeOut(self.low), FadeIn(self.a_card)]

    def a_keys(self):                              # the drawing steps back behind the keys
        return [FadeOut(VGroup(self.a_card, self.legs, self.leg_labels, self.points,
                               self.high)),
                FadeIn(self.keys), FadeIn(self.a_screen)]

    def a_minus(self):
        return [FadeIn(self.a_foot)]

    # ---- B: negative? add 360 ----------------------------------------------
    def b_head(self):
        return [FadeOut(VGroup(self.a_top, self.keys, self.a_foot)), FadeIn(self.b_top)]

    def b_says(self):
        return [self.a_screen.animate.shift(UP * self.drop), FadeIn(self.b_sub)]

    def b_results(self):
        return [FadeOut(self.a_screen), FadeIn(self.b_screen)]

    def b_map_in(self):                            # "238 degrees, clockwise from north"
        return [FadeOut(VGroup(self.b_sub, self.b_screen)),
                FadeIn(VGroup(self.legs, self.leg_labels, self.line, self.arc, self.points,
                              self.high))]

    def b_card_in(self):
        return [FadeOut(self.leg_labels), FadeIn(self.b_card)]

    def b_ok(self):                                # "South-west" is read on the map
        return [FadeOut(self.b_card), FadeIn(VGroup(self.leg_labels, self.b_foot))]

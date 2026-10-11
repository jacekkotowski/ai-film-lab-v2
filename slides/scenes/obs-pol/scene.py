"""obs-pol -- slide 04 Direction and distance: target minus me -> Pol -> distance and azimuth.

Film: Map and Calculator 01 - Observer. Content: his plan,
film/docs/plans/2026-10-11/PLAN-map-calculator.md (slide 04), numbers
computed here. Pol takes the north difference first, so θ is an azimuth
(-180..180: a negative one gets 360). 4232 mils is his choice (x 17.78).
Pieces come one after another on his words; the still is the end of B.

    uv run --directory slides python -m aimanim.look still obs-pol full
"""

import math
import sys
from pathlib import Path

from manim import DOWN, FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import kit  # noqa: E402

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
GRID = dict(e0=31000, e1=37000, n0=19000, n1=23000, left=-2.85, bottom=-3.0,
            scale=6.4 / 6000)                     # 6 x 4 km; "37" ends 3.55 (obs-test)
KEYS_Y, SCREEN_TOP, A_FOOT_B = 2.8, 1.9, -3.0
B_DROP = 0.6                                      # the screen moves down for the subline

# ---- timing ----------------------------------------------------------------
# Each step on its word in [04] of slides.script.txt (Claude's draft, 2026-10-11).
BEAT_WORDS = ["Target", "difference", "target", "minus", "SHIFT", "Type", "Negative",
              "distance", "Equals", "makes", "Times", "South"]
BEAT_LINES = [0, 0, 1, 1, 2, 3, 4, 6, 7, 8, 9, 10]
RUN_TIMES = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def the_map(b: bool) -> VGroup:
    """A: ME, the target, the two legs. B adds the azimuth line and the arc, 238°."""
    grid, at = kit.map_grid(**GRID)
    corner = (ME[0], TARGET[1])
    g = VGroup(grid,
               kit.map_line(at, ME, corner, m(DN), kit.MUTED, dashed=True, where=0.7,
                            label_color=kit.PAPER),
               kit.map_line(at, corner, TARGET, m(DE), kit.MUTED, dashed=True, where=0.0,
                            label_color=kit.PAPER))
    if b:
        g.add(kit.map_line(at, ME, TARGET),
              kit.azimuth_arc(at, ME, AZ, 0.7, f"{AZ:.0f}°", label_at=60))
    g.add(kit.map_point(at, *ME, "ME", kit.PAPER, "up", clear=0.95),
          kit.map_point(at, *TARGET, "TARGET", kit.GREEN, "down"))
    return g


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.a_sub = kit.note(A_SUB, kit.below(self.a_top[1]))
        self.a_map = the_map(False)
        self.a_card = kit.card([f"ΔN = {TARGET[1]} − {ME[1]}\n= {m(DN)}",
                                f"ΔE = {TARGET[0]} − {ME[0]}\n= {m(DE)}"],
                               self.a_top[1].get_bottom()[1] - 0.3)
        self.keys = kit.keys(["SHIFT", "+"], KEYS_Y, sep="+", then="Pol(")
        expr = f"Pol({m(DN)},{m(DE)})"
        self.a_screen = kit.screen(expr, rows=2, top=SCREEN_TOP)
        self.a_foot = kit.note(A_FOOT, A_FOOT_B, kit.AMBER)
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.b_sub = kit.note(B_SUB, kit.below(self.b_top[1]))
        self.b_screen = kit.screen(expr, [f"r={R:.9g}", f"θ={m(f'{THETA:.10g}')}"],
                                   top=SCREEN_TOP - B_DROP)
        self.b_map = the_map(True)
        self.b_card = kit.card([f"D {round(R)} m",
                                f"Az {m(round(THETA, 1))} + 360\n= {AZ:.1f}°",
                                f"{AZ:.1f} × {MILS_PER_DEG}\n≈ {MILS} mils"],
                               self.b_top[1].get_bottom()[1] - 0.3)
        self.b_foot = kit.note(B_FOOT, kit.below(self.b_card), kit.GREEN)
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
        return [FadeOut(self.a_sub), FadeIn(self.a_map)]

    def a_diffs(self):
        return [FadeOut(self.a_map), FadeIn(self.a_card)]

    def a_keys(self):
        return [FadeOut(self.a_card), FadeIn(self.keys), FadeIn(self.a_screen)]

    def a_minus(self):
        return [FadeIn(self.a_foot)]

    # ---- B: negative? add 360 ----------------------------------------------
    def b_head(self):
        return [FadeOut(VGroup(self.a_top, self.keys, self.a_foot)), FadeIn(self.b_top)]

    def b_says(self):
        return [self.a_screen.animate.shift(DOWN * B_DROP), FadeIn(self.b_sub)]

    def b_results(self):
        return [FadeOut(self.a_screen), FadeIn(self.b_screen)]

    def b_map_in(self):
        return [FadeOut(VGroup(self.b_sub, self.b_screen)), FadeIn(self.b_map)]

    def b_card_in(self):
        return [FadeOut(self.b_map), FadeIn(self.b_card)]

    def b_ok(self):
        return [FadeIn(self.b_foot)]

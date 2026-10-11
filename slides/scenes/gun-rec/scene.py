"""gun-rec -- slide 04 My correction on the map: RIGHT 40, ADD 100 -> two Recs -> the new point.

Film: Map and Calculator 02 - Gun. Content: the agreed outline,
film/docs/plans/2026-10-11/PLAN-map-calculator-02.md (slide 04), numbers
computed here. The Casio has no mils: 1160 ÷ 17.78 = 65.24°. ADD runs along my
line (Rec(100, 65.24)), RIGHT across it, 90° more (Rec(40, 155.24)). The new
point is rounded to the metre, as video 01 rounded the target: E 36783, N 22820.
Pieces come one after another on his words; the still is the end of B.

A close-up of the sheet around the target, 100 m squares (1.5 units each): at
slide 01's scale the whole correction would be 13 px. The panels stand on the
bottom edge under it; while the keys and the screen are up (5.5 tall) the
drawing steps back, only the grid stays. The last step trades the B card for
the ✓ line.

    uv run --directory slides python -m aimanim.look still gun-rec full
"""

import math
import sys
from pathlib import Path

from manim import UP, FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (the outline, slide 04) -----------------------------------------
SERIES = "MAP AND CALCULATOR · 02 · GUN"
ME, TARGET = (34500, 21800), (36675, 22814)       # E, N in metres
DIRECTION, MILS_PER_DEG = 1160, 17.78             # my call; 6400 / 360
ADD, RIGHT = 100, 40                              # my correction, metres
A_TAG, A_HEAD = "SLIDE 4 · A", "ADD along my line"
A_FOOT = "The Casio has no mils."
B_TAG, B_HEAD = "SLIDE 4 · B", "RIGHT is plus 90"
B_FOOT = "✓ LEFT and DROP: the same with a minus"

AZ = round(DIRECTION / MILS_PER_DEG, 2)           # 65.24, as typed
AZ_R = round(AZ + 90, 2)                          # 155.24


def rec(r, deg):
    """The Casio's Rec: x north, y east."""
    return r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg))


ADD_N, ADD_E = rec(ADD, AZ)                       # 41.88, 90.81
RIGHT_N, RIGHT_E = rec(RIGHT, AZ_R)               # -36.32, 16.75
P_ADD = (TARGET[0] + ADD_E, TARGET[1] + ADD_N)    # after ADD 100
NEW = (TARGET[0] + round(ADD_E) + round(RIGHT_E),  # E 36783
       TARGET[1] + round(ADD_N) + round(RIGHT_N))  # N 22820


def m(v) -> str:
    """As the screen and the cards show it: U+2212 for minus."""
    return f"{v}".replace("-", "−")


def signed(v: int) -> str:
    return f"+ {v}" if v >= 0 else f"− {-v}"


# ---- layout ----------------------------------------------------------------
SCALE = 0.015                                     # frame units per metre: 100 m = 1.5
GRID = dict(e0=36600, e1=36900, n0=22700, n1=22900, left=-0.6, bottom=0.5, scale=SCALE,
            km=100)
E_LABELS, N_LABELS = (36600, 36800), (22700, 22800)   # 22900: the headline's
GAP = 0.3
FLOOR = frame.BOTTOM + 0.05

# ---- timing ----------------------------------------------------------------
# Each step on its word in [04] of slides.script.txt (Claude's draft, 2026-10-11).
BEAT_WORDS = ["Add", "called", "add", "Casio", "SHIFT", "Equals", "east", "Right", "Rec",
              "east", "Add", "Left"]
BEAT_LINES = [0, 1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8]
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
        g, at = kit.map_grid(**GRID)
        self.grid = g[0]                          # its numbers would all read "36": ours
        h = kit.cap(frame.MIN_FONT, kit.SANS)
        left, bottom = GRID["left"], GRID["bottom"]
        self.n_nums = VGroup(*[kit.text(f"{n}", left - 0.2, at(0, n)[1] - h / 2, kit.MUTED,
                                        align="right", font=kit.SANS) for n in N_LABELS])
        self.e_nums = VGroup(*[kit.text(f"{e}", at(e, 0)[0], bottom - 0.4 - h, kit.MUTED,
                                        font=kit.SANS) for e in E_LABELS])
        # my line: from the sheet's left edge (towards ME) to the target
        dn = (GRID["e0"] - TARGET[0]) / math.tan(math.radians(AZ))
        enter = (GRID["e0"], TARGET[1] + dn)
        tp = at(*TARGET)
        self.mine = VGroup(kit.map_line(at, enter, TARGET),
                           kit.map_point(at, *TARGET, None, kit.GREEN),
                           kit.text("TARGET", tp[0] - 0.25, tp[1] + 0.3, kit.GREEN,
                                    align="right", font=kit.SANS))
        self.add_leg = VGroup(kit.map_line(at, TARGET, P_ADD, f"{ADD}", kit.AMBER, width=7,
                                           side=1),
                              kit.map_point(at, *P_ADD, None, kit.AMBER, r=0.07))
        self.right_leg = kit.map_line(at, P_ADD, NEW, f"{RIGHT}", kit.AMBER, width=7, side=1)
        self.new = kit.map_point(at, *NEW, "NEW", kit.GREEN, "down")

        self.a_top = VGroup(kit.step_tag(A_TAG), kit.headline(A_HEAD))
        self.call = VGroup(kit.command(f"RIGHT {RIGHT}", 0, size=100),
                           kit.command(f"ADD {ADD}", 0, size=100))
        stack_up(self.call[1], self.call[0])
        self.a_card = kit.card([f"{DIRECTION} ÷ {MILS_PER_DEG}\n= {AZ}°"], 0)
        self.a_foot = kit.note(A_FOOT, 0)
        stack_up(self.a_foot, self.a_card)
        self.keys = kit.keys(["SHIFT", "−"], 0, sep="+", then="Rec(")
        expr = f"Rec({ADD},{AZ})"
        self.a_screen = kit.screen(expr, rows=2)
        stack_up(self.a_screen, self.keys)
        self.a_results = kit.screen(expr, [f"x={ADD_N:.10g}", f"y={ADD_E:.10g}"])
        stack_up(self.a_results)
        self.b_top = VGroup(kit.step_tag(B_TAG), kit.headline(B_HEAD))
        self.b_screen = kit.screen(f"Rec({RIGHT},{AZ_R})",
                                   [f"x={m(f'{RIGHT_N:.10g}')}", f"y={RIGHT_E:.10g}"])
        stack_up(self.b_screen)
        self.b_card = kit.card(
            [f"E {TARGET[0]} {signed(round(ADD_E))} {signed(round(RIGHT_E))}\n= {NEW[0]}",
             f"N {TARGET[1]} {signed(round(ADD_N))} {signed(round(RIGHT_N))}\n= {NEW[1]}"], 0)
        stack_up(self.b_card)
        self.b_foot = kit.note(B_FOOT, 0, kit.GREEN)
        stack_up(self.b_foot)
        steps = [self.a_head, self.a_call, self.a_map, self.a_degrees, self.a_keys,
                 self.a_results_in, self.a_leg, self.b_head, self.b_results, self.b_leg,
                 self.b_card_in, self.b_ok]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, [kit.series_tag(SERIES)],
                beat_words=BEAT_WORDS, check_each=True)

    # ---- A: ADD along my line ------------------------------------------------
    def a_head(self):
        return [FadeIn(self.a_top)]

    def a_call(self):                              # what I called
        return [FadeIn(self.call)]

    def a_map(self):                               # along my line
        return [FadeIn(VGroup(self.grid, self.n_nums, self.e_nums)), FadeIn(self.mine)]

    def a_degrees(self):
        return [FadeOut(self.call), FadeIn(VGroup(self.a_card, self.a_foot))]

    def a_keys(self):                              # the drawing steps back behind the keys
        return [FadeOut(VGroup(self.a_card, self.a_foot, self.mine, self.n_nums,
                               self.e_nums)),
                FadeIn(self.keys), FadeIn(self.a_screen)]

    def a_results_in(self):
        return [FadeOut(VGroup(self.keys, self.a_screen)), FadeIn(self.a_results)]

    def a_leg(self):                               # 100 m on from the target, along my line
        return [FadeOut(self.a_results),
                FadeIn(VGroup(self.mine, self.n_nums)), FadeIn(self.add_leg)]

    # ---- B: RIGHT is plus 90 --------------------------------------------------
    def b_head(self):
        return [FadeOut(self.a_top), FadeIn(self.b_top)]

    def b_results(self):
        return [FadeIn(self.b_screen)]

    def b_leg(self):                               # 40 m across it: the new point
        return [FadeOut(self.b_screen), FadeIn(self.right_leg), FadeIn(self.new)]

    def b_card_in(self):
        return [FadeIn(self.b_card)]

    def b_ok(self):
        return [FadeOut(self.b_card), FadeIn(VGroup(self.b_foot, self.e_nums))]

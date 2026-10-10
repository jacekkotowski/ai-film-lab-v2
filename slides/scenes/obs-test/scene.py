"""obs-test -- every drawing of Map and Calculator 01 once; Δ and θ in Text (a TEST, in no film).

Step 1 of film/docs/plans/2026-10-11/PLAN-map-calculator.md: the helpers in
aimanim/kit.py, each on a page of its own (one page per step), his texts and
numbers. The still is the last page: slide 04's ΔN / ΔE card, the Pol keys
and the screen with θ. Each earlier page is checked when the next begins
("[layout] page n: ..."); the last by kit.run.

    uv run --directory slides python -m aimanim.look still obs-test full
    uv run --directory slides python -m aimanim.look draft obs-test   (out/steps.png: every page)
"""

import math
import sys
from pathlib import Path

from manim import FadeIn, FadeOut, Scene, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (his plan; numbers computed here, rounded as he says them) ----
SERIES = "MAP AND CALCULATOR · 01 · OBSERVER"
ME = (34500, 21800)
REC_D, REC_AZ = 2400, 65                          # slide 03
TARGET_04 = (32100, 20300)                        # slide 04
COMPASS_AZ = 61                                   # slide 02
BURST_MILS, BURST_KM = 20, 3                      # slide 05

rx = REC_D * math.cos(math.radians(REC_AZ))       # x: the step north
ry = REC_D * math.sin(math.radians(REC_AZ))       # y: the step east
TARGET_03 = (ME[0] + round(ry), ME[1] + round(rx))
DN, DE = TARGET_04[1] - ME[1], TARGET_04[0] - ME[0]
POL_R = math.hypot(DN, DE)
POL_T = math.degrees(math.atan2(DE, DN))
AZ_04 = POL_T + 360 if POL_T < 0 else POL_T


def m(v: float) -> str:
    """A number as the screen and the cards show it: U+2212 for minus."""
    return f"{v}".replace("-", "−")


# ---- layout ----------------------------------------------------------------
SERIES_B, STEP_B, HEAD_B = 6.75, 5.85, 4.85     # baselines: tag (26), step tag, headline (72)
HEAD = 72

# ---- timing (a test: no narration, steps spaced evenly) ---------------------
BEAT_WORDS: list[str] = []
BEAT_LINES = [0, 1, 2, 3, 4, 5, 6, 7]
RUN_TIMES = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]


def tags(step: str | None) -> VGroup:
    g = VGroup(kit.text(SERIES, -frame.SIDE, SERIES_B, kit.MUTED, kit.SERIES_FONT, "left", kit.MONO))
    if step:
        g.add(kit.text(step, -frame.SIDE, STEP_B, kit.MUTED, frame.MIN_FONT, "left", kit.SANS))
    return g


def headline(s: str) -> VGroup:
    return kit.paragraph(s, -frame.SIDE, HEAD_B, color=kit.PAPER, size=HEAD, align="left",
                         font=kit.SANS, weight="BOLD")


def badge(s: str, baseline: float, color) -> VGroup:
    return kit.paragraph(s, -frame.SIDE, baseline, color=color, align="left", font=kit.SANS)


class Slide(Scene):
    def construct(self):
        self.camera.background_color = kit.GROUND
        self.page = None
        self.pages = [self.mode_wrong, self.mode_right, self.compass, self.norths,
                      self.burst, self.rec, self.map04, self.pol]
        steps = [self.turn(i) for i in range(len(self.pages))]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, beat_words=BEAT_WORDS)

    def turn(self, i):
        def step():
            if self.page is not None:
                for note in kit.check(self.mobjects):
                    print(f"[layout] page {i}: {note}", file=sys.stderr)
            new = self.pages[i]()
            anims = [FadeIn(new)]
            if self.page is not None:
                anims.insert(0, FadeOut(self.page))
            self.page = new
            return anims
        return step

    # ---- the pages -------------------------------------------------------
    def mode_wrong(self):                          # 01 A
        return VGroup(tags("SLIDE 1 · A"), headline("Wrong mode, wrong answer"),
                      kit.screen("tan(45)", [f"{math.tan(45):.10g}"], ind="R", bad=True, top=3.3),
                      badge("✗ R on the screen = wrong angles", -0.8, kit.ORANGE))

    def mode_right(self):                          # 01 B
        k = kit.keys(["SHIFT", "MENU", "2", "1"], 3.7)
        kit.lit(k.caps[0])
        kit.lit(k.caps[1])
        return VGroup(tags("SLIDE 1 · B"), headline("Set degrees"), k,
                      kit.screen("tan(45)", [f"{math.tan(math.radians(45)):.10g}"], top=1.4),
                      badge("✓ D on the screen", -2.7, kit.GREEN))

    def compass(self):                             # 02 A
        return VGroup(tags("SLIDE 2 · A"), headline("The compass isn't the map"),
                      kit.compass((0, 0.6), 2.3, COMPASS_AZ),
                      badge("✗ Don't type it in as it is", -2.6, kit.ORANGE))

    def norths(self):                              # 02 B
        return VGroup(tags("SLIDE 2 · B"), headline("Add the correction"),
                      kit.norths((-1.2, -0.9), 4.0, 12),
                      kit.card(["Map azimuth =\ncompass azimuth\n+ correction"], -1.3))

    def burst(self):                               # 05
        return VGroup(tags("SLIDE 5 · A"),
                      kit.burst_view((0, 2.5), 3.0, BURST_MILS, 0.09),
                      kit.command(f"RIGHT {BURST_KM * BURST_MILS}", -3.1))

    def rec(self):                                 # 03 B
        e, n = TARGET_03
        return VGroup(tags(None),
                      kit.card([f"E {ME[0]} + {round(ry)}\n= {e}",
                                f"N {ME[1]} + {round(rx)}\n= {n}",
                                f"TARGET\nE {e} · N {n}"], 6.35, hl=2),
                      kit.screen(f"Rec({REC_D},{REC_AZ})", [f"x={rx:.10g}", f"y={ry:.10g}"], top=0.6))

    def map04(self):                               # 04, the map
        # 6 km across: the "37" under the right edge ends at SIDE
        grid, at = kit.map_grid(31000, 37000, 19000, 23000, -2.85, -3.0, 6.4 / 6000)
        corner = (ME[0], TARGET_04[1])
        return VGroup(tags("SLIDE 4 · A"), grid,
                      kit.map_line(at, ME, TARGET_04),
                      kit.map_line(at, ME, corner, m(DN), kit.MUTED, dashed=True, where=0.7,
                                   label_color=kit.PAPER),
                      kit.map_line(at, corner, TARGET_04, m(DE), kit.MUTED, dashed=True,
                                   where=0.0, label_color=kit.PAPER),
                      kit.azimuth_arc(at, ME, AZ_04, 0.7, f"{AZ_04:.0f}°", label_at=60),
                      kit.map_point(at, *ME, "ME", kit.PAPER, "up", clear=0.95),
                      kit.map_point(at, *TARGET_04, "TARGET", kit.GREEN, "down"))

    def pol(self):                                 # 04 A and B: the still
        k = kit.keys(["SHIFT", "+"], 0.9, sep="+", then="Pol(")
        return VGroup(tags("SLIDE 4 · A"),
                      kit.card([f"ΔN = {TARGET_04[1]} − {ME[1]}\n= {m(DN)}",
                                f"ΔE = {TARGET_04[0]} − {ME[0]}\n= {m(DE)}"], 5.3),
                      k,
                      kit.screen(f"Pol({m(DN)},{m(DE)})", [f"r={POL_R:.9g}", f"θ={m(f'{POL_T:.10g}')}"],
                                 top=0.15))

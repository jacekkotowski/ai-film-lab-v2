"""mil-unit -- one mil covers 10 cm at 100 m.

Content: spec.md. Slide 1 of the mil-measure film. The whole Aurora MIL
reticle (kit.reticle, as zero-reticle draws it), then the rule.

    uv run --extra render manim -s -r 540,960 --media_dir scenes/mil-unit/out scenes/mil-unit/scene.py Slide
"""

import sys
from pathlib import Path

from manim import FadeIn, Scene

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# ---- content (from spec.md) ---------------------------------------------
TITLE = "Aurora MIL"
CM, METRES = 10, 100                 # 1 mil = 1/1000 of the distance

# ---- layout --------------------------------------------------------------
# Safe area: x in [-SIDE, SIDE] = [-4, 4]; y in [BOTTOM, TOP] = [-4, 7].
S, AIM = 0.27, (0.0, 3.3)            # the whole reticle: as zero-reticle
RULE_ROWS = (-1.0, -2.3)             # baselines: "1 MIL = 10 cm", "at 100 m"
RULE_FONT = 72                       # "1 MIL = 10 cm" 7.46 wide at 72

# ---- timing --------------------------------------------------------------
# Each step starts on its word, as he says it in films/mil-measure.script.txt.
BEAT_WORDS = ["One|1", "hundred|100"]
BEAT_LINES = [1, 1]
RUN_TIMES = [1.0, 1.0]

at = kit.mil_to(S, AIM)


class Slide(Scene):
    def construct(self):
        background = [kit.title(TITLE), kit.reticle(at)]   # on screen from the first word
        steps = [self.step_rule, self.step_distance]
        kit.run(self, HERE, steps, BEAT_LINES, RUN_TIMES, background,
                beat_words=BEAT_WORDS)

    def step_rule(self):
        return [FadeIn(kit.text(f"1 MIL = {CM} cm", 0, RULE_ROWS[0],
                                frame.ACCENT, RULE_FONT))]

    def step_distance(self):
        return [FadeIn(kit.text(f"at {METRES} m", 0, RULE_ROWS[1], frame.INK, RULE_FONT))]

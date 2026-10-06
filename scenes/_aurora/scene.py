"""_aurora -- reference stills of the Aurora MIL reticle and its parts.

In no film. Each class is one still in docs/aurora/ (README.md there):
the reticle drawn by kit.reticle from aimanim/aurora.py, at the scale a
slide would use it, so a new slide can copy the numbers below.

    uv run --extra render manim -s -r 1080,1920 --media_dir scenes/_aurora/out scenes/_aurora/scene.py Full
    (and Centre, Chevron, Stadia, Line)
"""

import sys
from pathlib import Path

from manim import Scene

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from aimanim import frame, kit  # noqa: E402

# name: (units per mil, aim point, window in mil, stroke, dot radius, numbers)
PARTS = {
    "Full":    (0.27, (0.0, 3.3), None, 3, 0.035, True),
    "Centre":  (0.74, (0.0, 5.6), (-5.3, 5.3, -10.3, 0.4), 4, 0.06, False),
    "Chevron": (1.6, (0.0, 4.4), (-1.3, 1.3, -4.4, 0.35), 6, 0.08, False),
    "Stadia":  (0.85, (-8.4, 1.5), (5.5, 14.3, -5.0, 5.0), 4, 0.06, True),
    "Line":    (0.6, (0.0, 1.5), (-6.6, 6.6, -0.5, 0.5), 4, 0.06, False),
}


class Part(Scene):
    def construct(self):
        s, aim, window, stroke, dot_r, numbers = PARTS[type(self).__name__]
        self.add(kit.reticle(kit.mil_to(s, aim), window, stroke, dot_r,
                             numbers=numbers))
        for note in kit.check(self.mobjects):
            print(f"[layout] {note}", file=sys.stderr)


class Full(Part): pass
class Centre(Part): pass
class Chevron(Part): pass
class Stadia(Part): pass
class Line(Part): pass

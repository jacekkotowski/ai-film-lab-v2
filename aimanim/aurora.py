"""aurora.py -- the ACSS Aurora MIL reticle (SLx 5x MicroPrism), in mil.

Shared by the slides that draw it (zero-reticle, zero-range), so both draw
the same reticle. Standard library only; the scenes turn it into Manim.
Every number and where it comes from: scenes/zero-reticle/spec.md.

Coordinates in mil from the aim point (the chevron's tip); y up, so the
mil grid is at negative y.
"""

from __future__ import annotations

INCH = 0.0254
YARD = 0.9144

DOTS_ON_LINE = 5                     # a dot at 1..5 mil, the 5th heavy
LINE_FROM, LINE_TO = 6, 14           # solid line, a tick every mil
STADIA = {6: 600, 8: 500, 10: 400, 12: 300, 14: 200}   # x (mil): yards
NUMBERS = {6: "6", 10: "4", 14: "2"}                    # printed above them
MAN_IN = 70                          # 5'10": a full stadia at its distance
CHEVRON_W, CHEVRON_H = 1.667, 0.9    # 18 in at 300 yd (manual); base (measured)
LADDER_TO = 10
BARS = {2: 1.25, 3: 1.0, 4: 0.833, 5: 1.0, 6: 0.5, 7: 0.5, 8: 0.5, 9: 0.5, 10: 1.0}
GRID = {2: 2, 3: 3, 4: 4, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5}  # row: dots to ±

MAN_M = MAN_IN * INCH                # 1.778 m


def stadia_mil(x: int) -> float:
    """Full height of the stadia at x: 70 in at its distance."""
    return MAN_IN * INCH / (STADIA[x] * YARD) * 1000


def man_metres(x: int, nearest: float = 10) -> int:
    """Where a 1.78 m man fills the stadia at x, rounded (548.6 -> 550)."""
    return int(round(MAN_M / stadia_mil(x) * 1000 / nearest) * nearest)


def segments(window=None):
    """The lines, as ((x0, y0), (x1, y1)); all horizontal or vertical.
    `window` = (x0, x1, y0, y1) cuts them to that part of the reticle."""
    s = []
    for side in (-1, 1):
        s.append(((side * LINE_FROM, 0), (side * LINE_TO, 0)))
        for x in range(LINE_FROM + 1, LINE_TO):
            if x not in STADIA:
                s.append(((side * x, 0.25), (side * x, -0.25)))
        for x in STADIA:
            h = stadia_mil(x) / 2
            s.append(((side * x, h), (side * x, -h)))
    s.append(((0, -CHEVRON_H), (0, -LADDER_TO)))
    for y, w in BARS.items():
        s.append(((-w / 2, -y), (w / 2, -y)))
    if window is None:
        return s
    wx0, wx1, wy0, wy1 = window
    out = []
    for (x0, y0), (x1, y1) in s:
        xa, xb = max(min(x0, x1), wx0), min(max(x0, x1), wx1)
        ya, yb = max(min(y0, y1), wy0), min(max(y0, y1), wy1)
        if xa <= xb and ya <= yb:
            out.append(((xa, ya), (xb, yb)))
    return out


def chevron():
    """The chevron's three corners: left base, tip (the aim point), right base."""
    w, h = CHEVRON_W / 2, CHEVRON_H
    return [(-w, -h), (0, 0), (w, -h)]


def dots(window=None):
    """(x, y, heavy) of every dot."""
    d = [(side * x, 0, x == DOTS_ON_LINE) for side in (-1, 1)
         for x in range(1, DOTS_ON_LINE + 1)]
    for row, n in GRID.items():
        d += [(side * x, -row, False) for side in (-1, 1) for x in range(1, n + 1)]
    if window is None:
        return d
    wx0, wx1, wy0, wy1 = window
    return [p for p in d if wx0 <= p[0] <= wx1 and wy0 <= p[1] <= wy1]

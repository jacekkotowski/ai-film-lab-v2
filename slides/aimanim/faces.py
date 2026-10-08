"""faces.py -- the two faces of "Love as a Face-Threatening Act" as two
rings, in one place (like ledger.py, issue I14): slides 01 and 07 draw the
same rings, mianzi outside, lian inside.

Standard library only. Frame units; the rings are a picture, not a
measurement.
"""

import math

CENTRE = (0.0, 2.0)              # the rings' centre
OUTER_R, INNER_R = 3.4, 1.8      # mianzi (reputation), lian (character)
RING_W = 6                       # stroke width of both rings

# baselines of the names: "lian" in the middle of the inner ring,
# "mianzi" in the band between the rings, above the inner one
LIAN_Y = CENTRE[1] - 0.25
MIANZI_Y = CENTRE[1] + 2.15


def on_circle(r: float, degrees: float) -> tuple[float, float]:
    """The point at `degrees` (0 = right, counter-clockwise) on a circle
    of radius r around CENTRE."""
    a = math.radians(degrees)
    return CENTRE[0] + r * math.cos(a), CENTRE[1] + r * math.sin(a)

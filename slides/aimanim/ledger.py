"""ledger.py -- the face ledger of "Love as a Face-Threatening Act", in one
place (like screening.py, issue I14): slides 03, 04 and 05 draw the same
speaker, hearer, table and bars, so they are placed here.

Standard library only. Face has no unit: the lengths are a picture, not a
measurement (scenes/face-ledger/spec.md). Frame units; speaker on the
left (side -1), hearer on the right (side +1).
"""

WHO = ("speaker", "hearer")
FACES = ("accepted", "free")     # Brown and Levinson: positive, negative face

# ---- the two people, the words between them, the table
PERSON_X = 2.4                   # speaker at -2.4, hearer at +2.4
FIG_H, FEET = 2.6, 2.6
SAID_Y = 4.9                     # baseline of "I love you", between the heads
TABLE_TOP, TABLE_HALF, LEG_X = 3.6, 1.8, 1.5   # legs reach the feet
NAME_Y = 1.85                    # "speaker" / "hearer"

# ---- the ledger: one bar per face per person
# a row's name 0.3 above its bars, 0.9 below the row before it: at 0.31
# both ways "free" read as belonging to the "accepted" bars (face-ledger)
HEAD_Y = {"accepted": 0.4, "free": -1.96}      # row names (baselines)
BAR_Y = {"accepted": -0.27, "free": -2.46}     # bar centres
BAR_IN, BAR_L, BAR_H = 0.9, 3.0, 0.4           # bars from ±0.9 to ±3.9

# ---- the weight: the implied request, a "?"
WEIGHT_SHARE = 0.4               # of a "free" bar: a picture, not a measure
WEIGHT_H, ASK_SIZE = 1.1, 72


def side(i: int) -> int:
    """-1 for the speaker (left), +1 for the hearer (right)."""
    return (-1, 1)[i]


def bar_span(i: int, length: float = BAR_L) -> tuple[float, float]:
    """(left, right) of person i's bar of `length`, growing outwards from
    the middle: the speaker's ends at -0.9, the hearer's starts at +0.9."""
    inner, outer = side(i) * BAR_IN, side(i) * (BAR_IN + length)
    return min(inner, outer), max(inner, outer)


def weight_span(i: int) -> tuple[float, float]:
    """(left, right) of the weight on person i's "free" bar: its outer
    WEIGHT_SHARE, where the bar was cut (hearer: 2.7 to 3.9)."""
    kept = BAR_L * (1 - WEIGHT_SHARE)
    a, b = side(i) * (BAR_IN + kept), side(i) * (BAR_IN + BAR_L)
    return min(a, b), max(a, b)

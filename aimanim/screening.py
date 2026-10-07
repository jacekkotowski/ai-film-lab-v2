"""screening.py -- the screening film's worked example and its population
picture, in one place (like aurora.py for the reticle): slides 01 and 02
start from the same 10,000 dots, so the dots are placed here.

Standard library only. Numbers: aimanim/diagnostic.py; sources and the
maths: the `binary-diagnostics` skill and scenes/scr-*/spec.md.
"""

from aimanim.diagnostic import Test, scatter

# ---- the worked example (Kagan: 90 % detected at 5 % false positives;
# 20 in 10,000 at 12 weeks, from 1 in 700 births and ~30 % later lost)
N, SICK = 10_000, 20
SENSITIVITY, SPECIFICITY = 0.90, 0.95
EXAMPLE = Test.from_rates(N, SICK, SENSITIVITY, SPECIFICITY)   # 18 2 499 9481

# ---- the newer blood test (Gil 2017: 99.7 % at 0.04 % false positives)
BLOOD_SENSITIVITY, BLOOD_FPR = 0.997, 0.0004

# ---- amniocentesis (Salomon 2019: 0.30 %, 95 % CI 0.11-0.49 %)
AMNIO_LOSS = 0.003
WEEK_FLAG, WEEK_NEEDLE, WEEK_RESULT = 12, 15, 17

# ---- the 10,000 as a grid, frame units (slides 01 and 02)
SEED = 21                                 # which places are the 20 cases
CASES = scatter(N, SICK, SEED)
GRID_COLS, GRID_PITCH = 134, 0.0597       # 134 x 0.0597 = 8.0 wide, 75 rows
GRID_LEFT, GRID_TOP = -4.0, 0.5           # bottom 0.5 - 75 x 0.0597 = -3.98
GRID_DOT, CASE_DOT = 0.02, 0.06           # radii; the cases drawn bigger


def grid_places() -> tuple[list[int], list[int]]:
    """(healthy places, case places) of the 10,000, 0-based."""
    cases = set(CASES)
    return [i for i in range(N) if i not in cases], list(CASES)

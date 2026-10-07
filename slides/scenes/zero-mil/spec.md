# zero-mil — slide 3 of 5 of the zeroing film

**Problem (Jacek's script, section 3, first sentence):** the SLx turrets
click in MOA, but the Aurora MIL reticle is marked in mils. How do the
two meet?

**One idea:** one mil on the reticle is about 14 turret clicks.

**Data** (100 m)
- 1 mil = 100 m × tan(0.001) = **10.000 cm**
- ¼ MOA click = 0.25 × 2.909 = **0.727 cm**
- 1 mil ÷ 1 click = 10 / 0.7272 = **13.75 clicks** → "about fourteen"
  (same thing: 1 mil = 3.438 MOA; 3.438 / 0.25 = 13.75)
- drawn: the 10 cm of one mil, a tick per click; 13 clicks = 9.45 cm,
  the 14th = 10.18 cm (just past the mil)

**Steps (one per sentence he says)**
1. line 0 — the turret: ¼ MOA, 0.73 cm per click, the clicks as ticks
2. line 1 — the reticle: 1 mil = 10 cm, a bracket beside the same ticks
3. line 2 — "13.75 ≈ 14 clicks"

**Narration (suggested split of his script's sentence into three; he says it his own way)**
"The SLx turrets count in MOA. But its Aurora reticle counts in mils.
And one mil equals about fourteen clicks."
If he keeps it as one sentence, all three steps fall on one line:
then set `BEAT_LINES = [0, 0, 0]` and the steps follow each other.

**Sources:** Primary Arms SLx 5x MicroPrism manuals (0.25 MOA click);
ACSS Aurora MIL manual ("milliradian-based reticle"). Links in
`scenes/zero-group/spec.md`.

**Status:** written 2026-10-05.

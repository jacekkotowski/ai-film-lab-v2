# zero-reticle — slide 4 of 5 of the zeroing film

**Problem (Jacek, 2026-10-06):** show the real ACSS Aurora MIL reticle of
his SLx 5x MicroPrism and explain it very briefly, its parts named with
arrows like Primary Arms' own picture. Metric only: a man's height, ranges
in round metres.

**One idea:** the reticle is a mil ruler; each part has one job.

**The reticle (drawn to scale, in mil: `aimanim/aurora.py`)**
Measured from the manual's picture (Jacek's paste, 504 px, 13.6 px per mil,
2026-10-06), checked against the manual's numbers where it gives them:
- horizontal line: a dot at every mil from 1 to 5, the 5th heavy (the
  manual's picture: "5 MIL Indicator"); solid from 6 to 14 mil, a tick
  every mil
- person stadia at ±6, 8, 10, 12, 14 mil, numbered 6, 4, 2 (hundreds of
  yards). Full height measured 3.16 / 3.75 / 4.78 / 6.40 / 9.63 mil; drawn
  from the manual's rule "each full stadia mark represents a 5'10" height
  at its indicated distance": 70 in at 600/500/400/300/200 yd =
  **3.24 / 3.89 / 4.86 / 6.48 / 9.72 mil**
- chevron: tip = aim point, base 0.9 mil below (measured), width
  **1.667 mil** (manual: 18 in at 300 yd; the 504 px picture gives 1.3–1.5,
  too coarse to beat the manual)
- centre ladder: a line from the chevron to 10 mil, a bar every mil from
  2 to 10; widths 2 → **1.25**, 3 → **1.00**, 4 → **0.833** (manual; measured
  1.25 / 0.96 / 0.81), 5 and 10 → 1.0, 6–9 → 0.5 (measured)
- MIL grid: dots 1 mil apart; row 2 to ±2, row 3 to ±3, row 4 to ±4, rows
  5–10 to ±5 (measured; manual: "10 MILs of elevation and up to 5 MILs of
  windage on each side")
- left out, too small at this size: the brackets at the 5th and 10th mil,
  the half-mil ticks, the grid's own "5" and "0"

**The names (the manual's)**
- Chevron — the manual: "Infinitely Precise Chevron"; its tip is the aim point
- Auto range — the manual's feature list; the numbered stadia
- MIL grid — "for effective holds": wind (sideways) and drop (down)
- 5 MIL dot — the picture's "5 MIL Indicator"

**Auto range in metres: a man 1.78 m tall** (5'10" = 70 × 2.54 = 177.8 cm)
A stadia fits 70 in at whole hundreds of YARDS. In metres:
| mark | yd | exact m | on the slide |
|---|---|---|---|
| 2 | 200 | 182.9 | 180 m |
| (3) | 300 | 274.3 | — |
| 4 | 400 | 365.8 | 370 m |
| (5) | 500 | 457.2 | — |
| 6 | 600 | 548.6 | 550 m |
Rounded to 10 m (Jacek: "not fractional numbers"); the largest error is
3.1 m, under 2 % — less than reading a man against a mark by eye.
Whole hundreds of metres would need a 1.94 m man (70 in per yard of
range = 1.944 m per metre of range): not a sensible "average man".
Check, the manual's formula, distance (m) = size (cm) × 10 / mils:
177.8 × 10 / 3.241 = 548.6 m.

**Not on this reticle:** speed (lead) dots. "3.1 mph walk / 8.6 mph sprint"
(5.0 / 13.8 km/h) belong to the Aurora 5.56/.308 *yards* BDC reticle;
Jacek's SLx has the MIL (he confirmed 2026-10-06).

**Steps (one per sentence he says)**
0. before the first word: title "Aurora reticle"
1. line 0 — the whole reticle, its numbers
2. line 1 — "Chevron" and its arrow
3. line 2 — "Auto range", a 1.78 m man on the "6", the table 2/4/6 → m
4. line 3 — "MIL grid"
5. line 4 — "5 MIL dot"

**Narration (suggested; he says it his own way)**
"This is the SLx's Aurora MIL reticle.
The tip of the chevron is the aim point.
The numbered bars range a man one metre seventy-eight tall: the six fits him at 550 metres.
The dots below are one mil apart, for wind and drop holds.
And the heavy dot marks five mils."

**Sources:** ACSS Aurora MIL reticle manual (SLx 5x MicroPrism),
https://primaryarmsoptics.com/wp-content/uploads/2024/06/SLx-5x-MicroPrism-5.56-Aurora-MIL-Reticle-Manual-WEB.pdf
— the feature list, "Target ranging — height", "Using MIL holdovers",
"Ranging with MILs", and its picture.

**Status:** written 2026-10-06.

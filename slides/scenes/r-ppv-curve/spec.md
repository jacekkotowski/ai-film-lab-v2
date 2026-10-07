# r-ppv-curve — the r-charts template (in no film)

**Problem:** a ggplot chart on a slide, with Manim callouts that appear
on his words and sit on the data.

**One idea:** the rarer the condition, the fewer of the flagged are sick.

**Data:** 90 % caught, 5 % false alarms (the screening film's example).
Share truly sick among the flagged = `diagnostic.ppv_at(1/N, 0.90, 0.05)`:
1 in 10 → 66.7 % ("2 in 3"), 1 in 500 → 3.5 % ("1 in 29"). The curve is
drawn by R (`slides/r/ppv_curve.R`, the same formula), the rings by Manim.

**Steps**
0. before the first word: title, the chart (chart.png)
1. line 0 — ring + "2 in 3" at 1 in 10
2. line 1 — ring + "1 in 29" at 1 in 500

**Sources:** calculated.

**Status:** written 2026-10-08. Full-size still checked by eye: both rings
on the curve (centres within a pixel of the grid-line arithmetic). Clip
not rendered.

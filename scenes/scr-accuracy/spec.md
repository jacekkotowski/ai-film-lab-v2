# scr-accuracy — slide 1 of screening

**Problem (Jacek's words):** A pregnant woman's test flags a high risk of
Down syndrome; her doctor calls the test 95 percent accurate. A test that
called every pregnancy healthy would score 99.8 percent.

**One idea:** for a rare condition, accuracy rewards a test that does nothing.

**Data** (aimanim/screening.py; maths aimanim/diagnostic.py)
- 10,000 pregnancies, 20 with Down syndrome (1 in 700 births, ~30 % of
  affected pregnancies lost after 12 weeks → ~1 in 490 at 12 weeks → 20 in 10,000)
- the test: 90 % detected, 5 % of the healthy flagged → TP 18, FN 2, FP 499, TN 9,481
- accuracy (18 + 9,481) / 10,000 = **94.99 %** ("95.0%" on the gauge)
- "always healthy": 9,980 / 10,000 = **99.8 %**
- gauges read 90–100 % (so 95 and 99.8 look different: needle up vs. needle right)

**Steps**
0. title "95% accurate?"
1. line 0, "doctor" — left gauge: screening test, 95.0 %
2. line 1, "every" — the 10,000 dots, 20 red, scattered (seed 21)
3. line 1, "score" — right gauge: always healthy, 99.8 %

**Narration:** films/screening.script.txt [01], his words.

**Sources:** Kagan et al. (combined first-trimester screening, 90 % at 5 %);
prevalence from his bibliography. Accuracies calculated.

**Status:** written 2026-10-06. Full-size still made, no layout notes.

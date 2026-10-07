# scr-outcomes — slide 2 of screening

**Problem (Jacek's words):** Of 10,000 pregnancies, 20 have Down syndrome.
The test flags 18 and misses 2; flags 499 healthy ones and clears 9,481.
Sensitivity 90 %, specificity 95 %.

**One idea:** the four cells come from splitting the population twice —
first by truth (columns), then by the test (rows).

**Data**
- columns = truth: affected 20, healthy 9,980
- rows = result: flagged, cleared
- TP = 20 × 0.90 = 18, FN = 2; TN = 9,980 × 0.95 = 9,481, FP = 499
- sensitivity = TP / affected = 18 / 20 = 90 % (left column, lit)
- specificity = TN / healthy = 9,481 / 9,980 = 95.0 % (right column, lit)
- one dot = one pregnancy; the affected column's dots are drawn bigger
  (r 0.09 vs 0.011): 20 at the healthy size would be specks. Slide 3 shows
  both rows at one size.

**Steps** (starts from slide 1's dots, same places)
0. title; slide 1's 10,000 dots
1. line 0, "Of" — the dots sort into two columns: 20 affected | 9,980 healthy
2. line 1, "test" — 18 move up into "flagged" (TP 18), 2 stay (FN 2); row names, rule
3. line 2, "It" — 499 move up (FP 499), 9,481 stay (TN 9,481)
4. line 3, "Sensitivity" — left column boxed (holds 20 and 18), "sensitivity 90%"
5. line 4, "Specificity" — right column boxed, "specificity 95%"

**Narration:** films/screening.script.txt [02], his words.

**Sources:** as slide 1. Calculated.

**Status:** written 2026-10-06. Full-size still, no layout notes; draft clip
looked at (4 frames): the split plays in order.

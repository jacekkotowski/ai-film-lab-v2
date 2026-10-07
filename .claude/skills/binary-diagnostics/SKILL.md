---
name: binary-diagnostics
description: Statistics of a yes/no outcome, checked and drawn -- a screening or diagnostic test, or a classifier (logistic regression, any model) at one cutoff. The confusion matrix (TP, FN, FP, TN), sensitivity, specificity, accuracy and the accuracy paradox, PPV and NPV and how they fall with prevalence, likelihood ratios and Bayes in odds form, recall/precision naming, thresholds, ROC; the worked Down syndrome example with its sources, and the reusable code and drawings (aimanim/diagnostic.py, kit.dots/people/box/strike, the scr-* scenes). Use when Jacek writes a script or slide about a test result, false positives, base rates, a classifier's performance, logistic regression diagnostics, or "how accurate is it".
---

# Binary diagnostics: the numbers we have checked, and how to draw them

A yes/no outcome (sick or not) and a yes/no call (flagged or cleared).
A logistic regression gives a probability; a **cutoff** turns it into a
call, and from then on everything here applies to that cutoff. Every number
on a slide is computed by `aimanim/diagnostic.py` (stdlib) and tested
(`tests/test_a_screening_table_adds_up.py`). New facts go in the last section.

## 1. The table (the convention of every slide)

Columns = TRUTH, rows = the test's RESULT. Always this way round.

|            | sick | healthy |                         |
|------------|------|---------|-------------------------|
| flagged    | TP   | FP      | PPV = TP / (TP+FP)      |
| cleared    | FN   | TN      | NPV = TN / (TN+FN)      |
|            | sensitivity = TP / sick | specificity = TN / healthy | |

- **Down a column** (sensitivity, specificity, false-positive rate,
  likelihood ratios): a property of the test. Does not depend on how
  common the condition is (for a fixed cutoff, see §5 caveat).
- **Along a row** (PPV, NPV): what a result means *in this population*.
  Falls (PPV) as the condition gets rarer.
- **The whole table** (accuracy): the share of calls right. Misleading
  when one class is rare: a "test" calling everyone healthy scores the
  healthy share (99.8 % below).

Names for the same thing (ML ↔ medicine): recall = sensitivity = TPR =
detection rate; precision = PPV; FPR = 1 − specificity = false-alarm rate;
prevalence = base rate = prior.

## 2. Bayes in odds form (the one formula to show)

    post-test odds = pre-test odds × LR+        LR+ = sensitivity / (1 − specificity)
                                                LR− = (1 − sensitivity) / specificity

- With the counts of a table, sick : healthy × LR+ is **exactly TP : FP**,
  the flagged row. 20 : 9,980 × 18 = 360 : 9,980 = 18 : 499 → 1 in 29.
  `diagnostic.post_test_odds`.
- LR+ above 10 is usually called strong evidence (Deeks & Altman 2004).
- PPV at any prevalence: `diagnostic.ppv_at(p, sens, fpr)`; the prevalence
  giving a wanted PPV: `diagnostic.prevalence_for_ppv`.

## 3. The worked example (screening film, 2026-10-06)

Inputs (his bibliography): 20 in 10,000 at 12 weeks (1 in 700 births, ~30 %
of affected pregnancies lost later → ~1 in 490); combined first-trimester
screening 90 % detected at 5 % false positives (Kagan et al., 75,821
pregnancies — **not re-read**).

| | value | how |
|---|---|---|
| TP, FN, FP, TN | 18, 2, 499, 9,481 | `Test.from_rates(10_000, 20, 0.90, 0.95)` |
| accuracy | 94.99 % | 9,499 / 10,000 |
| "always healthy" | 99.8 % | 9,980 / 10,000 |
| PPV | 3.48 % = 1 in 28.7 → "1 in 29" | 18 / 517 |
| NPV | 99.98 % | 9,481 / 9,483 |
| LR+ / LR− | 18 / 0.105 | 0.90/0.05, 0.10/0.95 |
| blood test (cfDNA) LR+ | 2,492 → "≈ 2,500" | 0.997 / 0.0004 (Gil 2017) |
| blood test, per 100,000 at 1 in 490 | TP 203, FP 40, 84 % real | |
| same test, prevalence for 85 % wrong | 1 in 14,125 → "1 in 14,000": TP 7, FP 40 | `prevalence_for_ppv(0.15, …)` |
| amniocentesis loss | 0.30 % (95 % CI 0.11–0.49 %) | Salomon 2019 |
| 499 × 0.003 | 1.5 healthy pregnancies per 10,000 screened | upper end |

## 4. Sources (checked 2026-10-06; "snippet" = search abstract only)

- Gigerenzer: 160 gynecologists, mammography, most frequent answer 90 %
  (47 %), truth ~10 % — snippet (APS Observer, PSPI 2007 abstract).
- Gil MM et al. 2017, UOG: cfDNA > 99 % of trisomy 21 (99.7 %), FPR 0.04 % — snippet.
- Kliff S, Bhatia A, NYT 1 Jan 2022, "When They Warn of Rare Disorders,
  These Prenatal Tests Are Usually Wrong": title/date confirmed; 85 %
  (80–93 % by condition, five microdeletion screens) from his notes.
- Salomon LJ et al. 2019, UOG: amniocentesis 0.30 % (0.11–0.49 %); CVS
  0.20 % (CI crosses 0) — snippet, PubMed 31124209.
- Deeks JJ, Altman DG 2004, BMJ 329:168, likelihood ratios — his notes.

## 5. Traps (say them in spec.md when they apply)

- **Base-rate neglect**: PPV is not sensitivity. 90 % sensitive, 1 in 29.
- **The accuracy paradox**: never show accuracy alone for a rare class.
- **Prevalence moves PPV, not LR** — but only for a fixed cutoff. Tests
  read by a person (and spectrum effects) can shift sensitivity and
  specificity with prevalence.
- **Rounding**: counts are whole people (`from_rates` rounds); say which
  numbers are rounded illustrations, not one study's results.
- **An illustration is labelled** (slide 04's 1 in 14,000 is derived, not
  the NYT's data). Never let a derived pile pass for a measured one.
- For a classifier: a table is ONE cutoff. Moving the cutoff trades FN for
  FP; the ROC curve is (FPR, TPR) over all cutoffs. Not drawn yet.

## 6. Drawing it (reuse; every rule came from a slide)

- **One dot = one person, always.** `kit.dots(points, r, color)` draws
  thousands as ONE VMobject (fast, Transform-able); `kit.grid_points(n,
  cols, pitch, left, top)` places them row by row. 10,000 at pitch 0.0597
  fill 8 × 4.5 units (scr-accuracy).
- **Colours**: `frame.SICK` red = has the condition, `frame.HEALTHY` grey;
  ACCENT = what this slide explains, SECOND = the comparison.
- **A column at a different dot size must be said** (scr-outcomes: the 20
  drawn at r 0.09, the 9,980 at 0.011). To compare shares, lay a row out
  at ONE size (scr-meaning: 18 red among 517).
- **The split animation**: start from the population grid
  (`aimanim/screening.py`, shared by slides 1 and 2) and Transform each
  cell's dots to its place: columns first (truth), then rows (test).
- **Light a column or row with `kit.box`** (four Lines, so texts inside
  give no layout notes); cross out with `kit.strike` (its own layout note
  "touches a Line" is meant).
- **People**: `kit.people(points, h)` — 499 at h 0.26, pitch 0.222 × 0.286
  read as figures at 1080×1920; at h 0.22 with a thin body they did not.
  One fading figure in 499 is invisible on a phone: colour it.
- **Rotated row names** (`flagged`, `cleared`) at x −3.58: 0.76 wide, need
  a row ≥ 2.9 tall at 56.
- Sizes at 56: "sensitivity 90%" 5.90, "9,481 / 9,483" 5.10, "18 / 517 =
  1 in 29" 6.96, "positives in 100,000" 7.86, "healthy pregnancies" 7.94,
  "per 10,000 screened" 8.09 → too wide.

## 7. Reusable pieces (where)

| piece | file |
|---|---|
| the table, rates, PPV/NPV, LRs, odds, `ppv_at`, `scatter` | `aimanim/diagnostic.py` |
| the screening example + its 10,000-dot grid | `aimanim/screening.py` |
| dots, people, box, strike, grid_points | `aimanim/kit.py` |
| population → 2×2 split, column lights | `scenes/scr-outcomes/` |
| rows at one dot size, PPV/NPV, crossed-out answer | `scenes/scr-meaning/` |
| prevalence shrink, LR+ | `scenes/scr-rarity/` |
| gauges (90–100 %) | `scenes/scr-accuracy/` |
| dots → people, vertical timeline | `scenes/scr-cost/` |

Natural next slides (not made): the cutoff slider (a logistic curve, the
table changing as the cutoff moves), the ROC curve and AUC, LR− and a
negative result, calibration.

## 8. Growing this skill
New number → formula, value, source line in §3/§4. New drawing fix →
§6 with the slide it came from; a helper used twice → `aimanim/`.

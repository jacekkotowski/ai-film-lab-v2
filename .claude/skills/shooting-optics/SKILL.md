---
name: shooting-optics
description: Sport shooting optics calculations, checked and metric -- MOA and mil, clicks per correction, zeroing from a group, the Primary Arms ACSS Aurora MIL reticle (its exact geometry, reusable drawings, ranging by width and height, speed, drop and wind in mils), the Vortex Triumph and PA SLx 5x MicroPrism facts, and the metric conversions that come out sensible. Use when Jacek writes a script or slide about a rifle sight, reticle, zeroing, clicks, MOA, mil, ranging, target speed, bullet drop, wind drift, holdovers, leads or turrets.
---

# Shooting optics: the numbers we have checked

> Stage **slides/**: plain paths below (`docs/`, `scenes/`, `projects/` ...) are under `slides/`; commands are written to run from the repo root.

Every number here was computed or read from a manual, and each one says
where it came from. Use them as they are. Anything new gets the same
treatment: a formula, the computed value, and a source, and then it goes
into this file (last section).

Metric only on screen (Jacek). MOA and mil are angles, so they're fine.
Imperial sources are converted in the slide's spec.md, with the
conversion shown.

## 1. The two angles

| | exact | at 100 m | at 100 yd |
|---|---|---|---|
| 1 MOA = 1/60° | 0.2909 mrad | **2.909 cm** (100 m × tan(1/60°)) | 1.047 in |
| 1 mil = 1 mrad | 3.438 MOA | **10.000 cm** | 3.6 in |

- Both scale with distance: at 200 m, 1 MOA = 5.82 cm and 1 mil = 20 cm.
- **Range in the formulas is always metres; size in cm.** The manual's form
  is distance (m) = size (cm) × 10 / mils. Same thing:
  mils = size (cm) × 10 / distance (m), and size (cm) = mils × distance (m) / 10.
- Narration rounds: "2.9 centimetres", "10 centimetres", "about fourteen".

## 2. Clicks

clicks = offset (cm) ÷ cm per click, where cm per click = click (MOA) × 2.909 × distance (m) / 100.

| click | cm per click at 100 m | clicks per mil |
|---|---|---|
| ¼ MOA (PA SLx 5x) | **0.727** ("0.73") | 13.75 ("about fourteen") |
| ½ MOA (Vortex Triumph) | **1.454** ("1.45") | 6.88 |
| 0.1 mil | 1.000 | 10 |

- Round to whole clicks, and **show the rounding**. For example, 4.5 cm ÷
  0.727 = 6.19, so it's 6 clicks, not 5. (5.5 came from the old 4 cm draft.)
  On a slide, the bar with one tick per click shows why the count is rounded
  (zero-clicks).
- A mil reticle on MOA turrets: one mil on the glass is 13.75 clicks
  (zero-mil). That's the mismatch worth explaining.

## 3. Zeroing from a group (zero-group, zero-clicks)

1. Fire four shots at one aim point, from a sandbag or bipod.
2. The group's centre is the mean of the holes; correct its offset from the
   aim, not any single hole's.
3. If one hole is far from the rest, fire a fresh group.

The worked example used in the film (100 m; cm, + = right / up):
- holes (−6, −3.5), (−3, −4), (−5.5, −6.5), (−3.5, −6)
- centre (−4.5, −5.0), so **5 cm low, 4.5 cm left**
- Triumph: 3 up, 3 right (3.44, 3.09). SLx: 7 up, 6 right (6.88, 6.19).
- A hole is drawn at 5.56 mm (radius 0.28 cm), to scale.

## 4. The optics (manuals checked 2026-10-05)

- **Vortex Triumph red dot:** ½ MOA per click, "~0.50 in at 100 yd"
  (manual M-00433-0).
- **Primary Arms SLx 5x MicroPrism, ACSS Aurora MIL reticle:** ¼ MOA per
  click (product page and both manuals). The turrets count in MOA; the
  reticle counts in mils.
  - Elevation counterclockwise = impact UP, and windage counterclockwise =
    RIGHT. Both are checked on Jacek's own caps (2026-10-05 and 2026-10-06)
    and agree with the newer "5x MicroPrism Optic Manual". **The older
    manual says the opposite. Never cite it.**
  - Diopter (focuses the reticle): look at a blank wall, close your eyes,
    glance through the sight, and turn the ring until the reticle is sharp
    at once.
- **Which Aurora is which.** Jacek's SLx has the **MIL** version: a full dot
  grid under the centre, numbered side bars 2-4-6, and a heavy dot at 5 mil.
  The **5.56/.308 yards BDC** version (common on the SLx 1-6x) has numbered
  drop rows 4/6/8 and "Moving Target Holds" (3.1 mph walk, 8.6 mph sprint).
  Pictures found online are usually the BDC one. **Check which reticle a
  picture shows before drawing it** (2026-10-06: three pasted pictures,
  two were the wrong reticle).

## 5. The Aurora MIL reticle, exactly

The geometry is code: `aimanim/aurora.py` (in mil, y up, origin at the
chevron tip); a slide draws it with `kit.reticle`. Reference stills of the
whole reticle and its enlarged parts (centre, chevron, stadia, line), with
the scale each uses: `docs/aurora/` (README.md). Its checks are in `tests/test_a_renumbered_slide_leaves_no_old_still.py`.
It was measured from the manual's picture (13.6 px per mil) and checked
against the manual's numbers; the details are in `scenes/zero-reticle/spec.md`.

| part | where (mil) | size | source |
|---|---|---|---|
| chevron | tip = aim point, base 0.9 below | 1.667 wide | manual (18 in at 300 yd) |
| line dots | 1–5 each side, 5th heavy ("5 MIL indicator") | | picture |
| side line | solid 6–14, tick every mil | | picture |
| person stadia ("Auto range") | ±6, 8, 10, 12, 14 | 3.24 / 3.89 / 4.86 / 6.48 / 9.72 tall | manual: 5'10" at 600/500/400/300/200 yd |
| numbers | 6, 4, 2 above ±6, ±10, ±14 | | picture |
| centre bars | every mil, 2–10 | 2 → 1.25, 3 → 1.00, 4 → 0.833; 5 and 10 → 1.0; 6–9 → 0.5 | manual (2–4), measured |
| MIL grid | rows 2–10, 1 mil apart | row 2 → ±2, 3 → ±3, 4 → ±4, 5–10 → ±5 | measured; manual "10 MILs elevation, 5 each side" |

The manual's names: Infinitely Precise Chevron, Auto Range, Stadia Ranging,
MIL Grid, and Target Height. The half stadia ranges a 35 in (0.89 m)
target, or a target at double the distance.

## 6. Ranging, made metric sensibly

- **Width: a 50 cm target fills the chevron at 300 m and bars 2, 3, 4 at
  400 / 500 / 600 m.** This is exact, not rounded: 18 in = ½ yd and
  50 cm = ½ m, so the same marks carry over with the yards relabelled as
  metres. Width in mil = 500 / metres = 1.667 / 1.25 / 1.00 / 0.833.
  (zero-range)
- **Height: a 1.78 m man (5'10" = 177.8 cm).** The stadia fit 70 in at
  whole hundreds of yards, so in metres:

  | mark | 2 | 3 | 4 | 5 | 6 |
  |---|---|---|---|---|---|
  | exact | 182.9 m | 274.3 m | 365.8 m | 457.2 m | 548.6 m |
  | on screen | 180 m | 270 m | 370 m | 460 m | 550 m |

  These are rounded to 10 m (Jacek: "not fractional numbers"). The largest
  error is 3.1 m (<2 %), smaller than reading a man by eye. Whole hundreds
  of metres would need a 1.94 m man, which isn't sensible. (zero-reticle)
- **The trick to look for:** an imperial size that is a simple fraction of
  a yard (18 in = ½ yd) carries over exactly to the same fraction of a
  metre. Anything else gets converted and rounded, with the error stated.

## 7. Conversions

- yd → m: × 0.9144, so 100 / 200 / 300 / 400 / 500 / 600 / 800 yd =
  91 / 183 / 274 / 366 / 457 / 549 / 732 m
- in → cm: × 2.54, so 5'10" = 177.8 cm, 35 in = 88.9 cm, 18 in = 45.7 cm
- mph → km/h: × 1.609344, so 3.1 mph = **5.0 km/h** (walk) and 8.6 mph =
  **13.8 km/h** (sprint)
- **Leads on the MIL reticle:** lead (mil) = speed (m/s) × time of flight
  (s) / distance (m) × 1000. The time of flight comes from a ballistic app
  (the manual suggests Strelok). We have **no measured time of flight**, so
  never put a lead number on screen without one, and say where it came
  from.

## 8. Pitfalls already paid for

- A reticle picture from the web may be the wrong variant (section 4).
  Measure it in pixels against its own dot spacing before trusting labels.
- The manual's picture draws the 400 yd target *under* the chevron. It is
  narrower than the chevron (1.24 vs 1.67 mil, measured), so the text is
  right: chevron = 300.
- Manual pictures are 504 px; measured widths are ±0.2 mil. Prefer the
  manual's numbers, and use the picture only where the manual gives none.
- One sentence per animation step. Split long script sentences; numbers in
  narration are said the way they are rounded on screen.
- **Check a pasted plan's physics before drawing it** (mil-measure,
  2026-10-06; three of eight sections needed a correction): stadia numbers
  read as mils; ½gt² read as the hold (it is below the bore line); wind
  drift explained as "more time to push" (it is the lag). Say each
  correction in the script's notes, and keep his structure.
- **Chosen numbers are labelled chosen** (the car's 2 m/s, the 0.5 s and
  1 s, the 30 cm drift) in spec.md and the script notes; never presented
  as a cartridge's data.

## 9. What the reticle measures (mil-measure film, 2026-10-06)

One formula, four uses; the film's rows are TARGET → MIL → FORMULA → RESULT.
- **Range from height** (mil-man): distance (m) = size (m) × 1000 ÷ mil.
  A 1.78 m man at 6 / 4 / 3 / 2 mil = **297 / 445 / 593 / 890 m**
  (1780 ÷ 6 = 296.7; small-angle error < 1e-5). Read on the **centre
  ladder**: head on the chevron tip, feet on bar n = n mil (bars 2–10).
- **The stadia numbers are not mils.** "2-4-6" are hundreds of yards; the
  "4" stadia is 4.86 mil tall. Never put "4 MIL" next to them.
- **Range from a known size** (mil-plate): 0.50 m plate filling dot −1 to
  dot +1 = 2 mil → **250 m**.
- **A mil is an angle** (mil-angle): it covers distance ÷ 1000, so 10 / 20 /
  30 cm at 100 / 200 / 300 m.
- **Speed** (mil-speed, chosen numbers): mil/s × distance ÷ 1000 = m/s. A car
  2 m long at 200 m is 10 mil long; nose 0 → 5 → 10 mil in 0 → 0.5 → 1 s =
  10 mil/s → **2 m/s = 7.2 km/h**. Still no lead without a time of flight (§7).
- **Drop** (mil-drop): ½ g t² with g = 9.81: 0.5 s → **1.23 m**, 1 s →
  **4.91 m**. It is the drop **below the bore line**, valid with drag for
  flat fire if t is the real time of flight. **The reticle hold is smaller**
  (the sight is zeroed). Times chosen, no cartridge.
- **Wind** (mil-wind): **drift = crosswind × lag, lag = t − D ÷ v₀** (Didion's
  lag rule; McCoy, Modern Exterior Ballistics; Litz). Not "the wind pushes
  for the whole flight": with no air there is no drift. No drift number from
  a bullet without a measured t. Conversion, exact: 30 cm at 300 m =
  30 × 10 ÷ 300 = **1.0 mil**, held upwind.

## 10. Reuse: what exists already

- **Films and their slides**, one contact sheet each: `docs/films/`
  (README.md lists every slide's one idea). Check there before making a
  slide that may exist.
- **The reticle and its parts**, with the scale and window each slide used:
  `docs/aurora/` (README.md). Draw with `kit.reticle`, never by hand.
- **The worked-example rows** TARGET → MIL → FORMULA → RESULT: `kit.chain`;
  **a man of known height**: `kit.man` (docs/aurora/pieces.png).
- **Next films, natural**: holds on the MIL grid (drop and wind together),
  leads once a time of flight is measured, MOA vs mil.

## 11. Growing this file

A new optic, reticle or calculation: add the formula, the computed number
(computed, not typed from memory), the source with its date, and the
slide that uses it. If a picture was measured, give its px per unit. When
a number here turns out wrong, fix it here first, then every spec.md that
copied it.

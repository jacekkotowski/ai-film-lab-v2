# The triangle observer – target – gun (for "Map and Calculator 02")

Researched 2026-10-11 for the next video (his ask: "how to work in a triangle I,
target, gun"). NATO 6400 mils, as in video 01. Local copies, read as text
(not every page by eye), in `models/manuals/` (not in git):

| file | what |
|---|---|
| `FM_6-30_observed_fire_1991.md` | FM 6-30 *Tactics, Techniques, and Procedures for Observed Fire* (1991), the observer's manual; marines.mil PDF, text by Firecrawl |
| `MCWP_3-16.4_FM_6-40_manual_cannon_gunnery_1996.pdf` + `.txt` | FM 6-40 / MCWP 3-16.4 *Manual Cannon Gunnery* (1996), the FDC's manual; saved by Jacek from marines.mil (curl gets 403 there), text by pdftotext |
| `USMC_TBS_B2C2497_call_for_indirect_fire.md` | USMC The Basic School handout B2C2497 *Call for Indirect Fire* (2005), the observer's side for beginners |
| `casio_fx-83GTX_85GTX_EN.pdf` + `.txt` | the calculator's manual (see casio-fx-85gtx.md) |

Successors (not found online as PDF): ATP 3-09.30 *Observed Fires* (2017) and
TC 3-09.81 (was FM 6-40). The geometry below does not change between editions.

## The three corners and two lines

- **OT line**: observer → target. The observer sees and corrects along it.
- **GT line**: gun → target. The gun fires along it.
- **Angle T**: "the angle formed by the intersection of the gun-target (GT) line
  and the OT line with its vertex at the target" (FM 6-30 ch. 5, md line 3149).
- Three jobs (TBS, "The Fire Support System"): observer = eyes (finds, calls, adjusts), fire direction
  centre (FDC) = brain (computes firing data), firing unit = muscle.

## What the observer sends (FM 6-30, TBS)

- Target location, one of: **grid** (six figures; the FDC does not need the
  observer's position), **polar** (OT direction + distance; the FDC needs his
  position first, a POSREP), **shift from a known point**.
- **OT direction** in mils grid, to the nearest 10 mils, four digits (TBS, "Key Concepts of Direction").
  In a grid mission it is sent after the call for fire or with the first
  correction, "since it is not needed by the FDC to locate the target" (FM 6-30
  4-4 a). Sent again when it changes by more than 100 mils (FM 6-30, md 3258).
  Compass = mils magnetic; add the GM angle to get mils grid (TBS, same section).
- **Corrections** in metres, along HIS OT line, deviation first, then range:
  `LEFT/RIGHT n` (OT factor × mils spotted, nearest 10 m, minimum 30) and
  `ADD/DROP n` (add = away from the observer, multiples of 100; 50 entering
  fire for effect). Always opposite the spotting. OT factor = OT distance / 1000,
  whole number above 1000 m, tenths below (TBS, "Deviation corrections"; FM 6-30 Table 5-1:
  4000 m, 45R → LEFT 180). Video 01 slide 05 (3 km, 20 left → RIGHT 60) is this rule.
- His flag 1 (the English words): LEFT/RIGHT and ADD/DROP in metres are the
  words of FM 6-30 and the TBS handout. Checked here; the Polish unit's words
  are a different question.

## What the FDC does with it (FM 6-40)

- **Chart data = chart range, chart deflection, angle T** (FM 6-40, txt 4916).
- **Target grid** (FM 6-40 6-7, txt 5046): a round paper grid laid over the
  target on the firing chart, its arrow turned to the OT direction. Glossary:
  "a device for converting the observer's target locations and corrections in
  respect to the OT line to corrections and target locations in respect to the
  GT line". Its three uses: shift from a known point, the observer's
  corrections, angle T.
- **Angle T** is told to the observer when it is 500 mils or more, or when he
  asks; to the nearest 100 mils: 580 → `ANGLE T 600` (FM 6-40, txt 4829).
- Observer told angle T ≥ 500: "at first he continues to use his OT factor ...
  If he sees that he is getting more of a correction than he asked for, he
  should consider cutting his corrections" (FM 6-30 ch. 5, md 3151).
  Why (reasoned, not quoted): the gun's scatter is longest along the GT line;
  seen from the side, range scatter looks like left/right.
- With no FDC the observer may compute for the gun himself (FM 6-30 ch. 7,
  "emergency"): azimuth → deflection from the azimuth of lay (= deflection
  3200, LEFT ADD / RIGHT SUBTRACT), corrections then along the GT line,
  elevation from charge rules and a C-factor. Elevation needs the gun's firing
  tables, not a map and a calculator.

## The same on the Casio (Claude's geometry, not a manual's procedure)

The target grid is Rec and Pol on paper. With video 01's convention
(Rec/Pol: x = north, y = east; azimuth clockwise from north; θ < 0 → + 360):

1. **Gun → target**: ΔN = N_target − N_gun, ΔE = E_target − E_gun;
   `Pol(ΔN, ΔE)` → r = GT range, θ = GT azimuth; × 17.78 → mils.
2. **Angle T** = GT azimuth − OT azimuth, as a size: above 180° take
   360 − it (above 3200 mils: 6400 − it).
3. **Observer's correction → map**: OT azimuth α. `ADD a` = `Rec(a, α)`;
   `RIGHT d` = `Rec(d, α + 90)`. DROP and LEFT are the same with a minus.
   Add both steps to the last aiming point: the new aiming point.
4. **New gun data**: step 1 again from the gun to the new aiming point.

## Worked example (2026-10-11, "go, pick the gun position"; Claude's choice)

Computed in Python (scratchpad triangle_example.py, the Casio's Rec/Pol
convention); not pressed on the real calculator. Observer and target are
video 01's; the gun is new.

| | E | N |
|---|---|---|
| ME (observer, video 01) | 34500 | 21800 |
| TARGET (video 01 slide 03, Rec(2400, 65°)) | 36675 | 22814 |
| GUN (chosen) | 33000 | 16000 |

The observer sends: the target's grid; his direction 65° × 17.78 = 1155.7 →
`DIRECTION 1160` (mils, nearest 10). First round: 20 mils left, 100 m short
(rangefinder 2300 m). OT factor 2400 / 1000 = 2.4 → 2 (TBS's own example):
`RIGHT 40, ADD 100`.

At the gun, all on the Casio:

| step | keys (idea) | result |
|---|---|---|
| gun → target | Pol(22814 − 16000, 36675 − 33000) = Pol(6814, 3675) | r 7741.85 m, θ 28.3394° = 503.9 mils |
| angle T | 65 − 28.34 | 36.66° = 652 mils → `ANGLE T 700` (≥ 500: told to the observer) |
| his direction back to degrees | 1160 ÷ 17.78 | 65.2418° (the Casio has no mils) |
| ADD 100 on his line | Rec(100, 65.24) | N +41.88, E +90.81 |
| RIGHT 40 across his line | Rec(40, 155.24) | N −36.32, E +16.75 |
| new aiming point | target + both | E 36782.6, N 22819.6 |
| gun → new point | Pol(6819.6, 3782.6) | r 7798.34 m, θ 29.0155° = 515.9 mils |
| change for the gun | | range +56.5 m, direction +12.0 mils (right) |

The lesson in one line: the observer's `RIGHT 40, ADD 100` is, seen from the
gun, `ADD 56, RIGHT 92` (m, along / across the GT line): the same move, other
words, because the two lines meet at 652 mils.

Not checked: any of this on the real fx-85GT X.

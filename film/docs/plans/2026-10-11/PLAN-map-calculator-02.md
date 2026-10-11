# Plan: "Map and Calculator 02 - Gun"

Status 2026-10-11: outline agreed (his "yes, write the plan and build the slides").
Claude led (his words: "I have no plan; Claude leads"). Sources and the worked
example: `slides/docs/tech/artillery-triangle.md` (5139277). Same form as video 01
(`PLAN-map-calculator.md`): its fixed decisions carry over unless named here.

## Named in the outline (he said yes to them)

1. **Angle T 656 mils, not 652.** The gun knows only DIRECTION 1160:
   1160 − 504 = 656. The research doc's 652 used the observer's exact 65°. Still
   `ANGLE T 700`. Every other number of the worked example recomputed in Python: match.
2. **Length.** Video 01's final: 171.2 s for 321 words (ffprobe; 1.88 words/s). At
   that pace 340 words = 181 s, past 3:00. This outline: ~305 words ≈ 163 s.
3. **RIGHT 40 arrives as given**; how the observer got it is not shown (FM rounds
   2.4 km to 2: 2 × 20 = 40; video 01's km × mils would give 48 → RIGHT 50).
4. **Simplified:** the gun's direction is a map azimuth in mils, not deflection on the
   sight; range is not turned into elevation (that needs the firing table); "the gun"
   also stands for the fire direction centre.

## Changed while building (measured)

5. **The new point is rounded to the metre: E 36783, N 22820** (as video 01 rounded the
   target to E 36675). `Pol(6819.6,3782.6)` is 7.52 units at 56, wider than the
   calculator screen. So slide 05 uses `Pol(6820,3783)`: r 7798.941531, θ 29.01678511
   → 516 mils (unchanged), range 7799 − 7742 = **+57 m** (was +56); across the gun's
   line 92.2 m (was 92.0), still "≈ 92".

## Fixed (from video 01, unchanged)

- Intro (narration only) → 5 slides, each A then B, pieces on his words → outro.
- English, NATO 6400 mils (× 17.78), Casio fx-85GT X, keys said shortcut first.
- Series tag `MAP AND CALCULATOR · 02 · GUN`; step tags `SLIDE n · A/B`.
- Film folder `projects/Map and Calculator 02 - Gun/`.

## Points (E, N in metres)

| | E | N | from |
|---|---|---|---|
| ME | 34500 | 21800 | video 01 |
| TARGET | 36675 | 22814 | video 01, slide 03 |
| GUN | 33000 | 16000 | Claude's choice (research doc) |

The triangle is 4 × 7 km, taller than wide: it fits the vertical frame. The 04
correction (~110 m) is 13 px at video 01's 1 km = 0.95 units: 04 draws a close-up
around the target in 100 m squares.

## Slides

| # | scene | A | B | words |
|---|---|---|---|---|
| intro | – | The observer sees the target, the gun does not: it stands kilometres behind. Today: the triangle me, target, gun, and what the gun does with my call. | | 25 |
| 01 The triangle | `gun-triangle` | *The gun can't see the target.* Map: ME, TARGET, GUN E 33000 N 16000; my line to the target, the gun's line to the target | *What I send.* Card `TARGET E 36675 N 22814`, `65 × 17.78 = 1156 → DIRECTION 1160` · ✓ *Grid for the gun, direction for my corrections* | 45 |
| 02 Gun to target | `gun-pol` | *Target minus gun.* `ΔN 22814 − 16000 = 6814`, `ΔE 36675 − 33000 = 3675`; keys SHIFT + ; screen `Pol(6814,3675)`; the two legs from the gun | *Range and direction.* Screen r 7741.85, θ 28.34; card `7742 m`, `28.34 × 17.78 ≈ 504 mils` · ✓ *North-east: nothing to add* | 50 |
| 03 Angle T | `gun-angle-t` | *Two lines meet at the target.* Map at the target: 1160 and 504, the arc between; `1160 − 504 = 656 mils` | *ANGLE T 700.* Card `500 or more → tell the observer, nearest 100` · ✓ *My left and right are not the gun's* | 45 |
| 04 My correction on the map | `gun-rec` | *ADD along my line.* `RIGHT 40, ADD 100`; `1160 ÷ 17.78 = 65.24°` (the Casio has no mils); `Rec(100,65.24)` → 41.88 N, 90.81 E | *RIGHT is plus 90.* `Rec(40,155.24)` → −36.32 N, 16.75 E; card `E 36782.6 · N 22819.6`; close-up: the two legs to the new point · ✓ *LEFT and DROP: the same with a minus* | 65 |
| 05 New data for the gun | `gun-new` | *Gun to the new point.* `Pol(6819.6,3782.6)` → r 7798.34, θ 29.02 → 516 mils | *Same burst, other words.* `ME: RIGHT 40 · ADD 100` / `GUN: +56 m · +12 mils` · ✓ *7.7 × 12 ≈ 92 m right: I asked mostly ADD, the gun moves mostly RIGHT* | 50 |
| outro | – | Five moves: grid and direction, Pol from the gun, angle T, Rec for my correction, Pol again. I correct along my line; the gun fires along its own. | | 25 |

## Numbers (Python, scratchpad gun02.py; the Casio's Rec/Pol: x = north, y = east)

| | value |
|---|---|
| gun → target | Pol(6814, 3675): r 7741.8487, θ 28.3394° = 503.87 → 504 mils |
| direction | 65 × 17.78 = 1155.70 → DIRECTION 1160 |
| angle T | 1160 − 504 = 656 mils → ANGLE T 700 |
| back to degrees | 1160 ÷ 17.78 = 65.2418° (65.24 typed: same results to 0.01 m) |
| ADD 100 | Rec(100, 65.24): x 41.88 (N), y 90.81 (E) |
| RIGHT 40 | Rec(40, 155.24): x −36.32 (N), y 16.75 (E) |
| new point | E 36782.6, N 22819.6 |
| gun → new point | Pol(6819.6, 3782.6): r 7798.34, θ 29.0155° = 515.90 → 516 mils |
| change | +56.49 m, +12.02 mils; along the GT line +55.95 m, across +92.03 m right |

## Steps

1. DONE (2026-10-11): the five scenes gun-triangle, gun-pol, gun-angle-t, gun-rec,
   gun-new; `projects/Map and Calculator 02 - Gun/slides.txt`. 0 `[layout]` notes on
   every step; full stills 1080x1920 (ffprobe); contact sheet
   `slides/docs/films/map-and-calculator-02-gun.png`.
2. DRAFTED (2026-10-11): `slides.script.txt` ([intro] [01]-[05] [outro]), 316 words
   (intro 24, 50, 39, 45, 65, 59, outro 34), BEAT_WORDS per step, `film check` 0
   PROBLEM. Claude's draft until he approves; not committed (as 01's).
3. Before recording, on a real fx-85GT X: every key sequence; whether Pol(6814, 3675)
   shows r as √59936221 (manual: √ form possible below 10⁶; r² has no square factor).
4. `publish` (asked first; `film new` by hand for .vertical), he narrates, `film go`,
   "narrated" → `clips`.

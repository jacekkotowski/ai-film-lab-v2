# Plan: "Map and Calculator 01 - Observer"

Status 2026-10-11: plan only, nothing built. **This is Jacek's plan** (pasted 2026-10-10,
from the online project RD01 Artillery, chat "Artillery Cheatsheet") with ONLY the
changes listed next. Every decision in it is his and is not re-asked.

## Changes to his plan (all of them)

1. **English, not Polish** (Jacek, 2026-10-11: the repo and his films are in English).
   Polish was never his choice: the online Claude wrote "you didn't say which language
   to use, so I went with Polish". Screen texts below are that chat's own English
   outline where it had one, otherwise translated from the Polish plan.
2. **Manim slides, not pan boards** (Claude's recommendation when he asked which is
   better). Each slide is one 1080x1920 scene: his step A, then his step B, as beats in
   the same frame (no pan). The keys light one by one on the word that names them.
3. **The map is on screen** (his message: "we need both to see the map and what buttons
   should be pressed, because we do the calculations based on the map"): slides 03 and 04
   draw a 1 km grid with the E/N numbers, ME, the target, the azimuth line and the ΔN / ΔE
   legs; slide 02's two north arrows are the map's margin. Drawn (no real sheet); a photo
   of his sheet can replace it if he gives one.
4. HTML-only items drop out (`.dc.html`, `lang`, `aria-label`, `PAN_LANG`, the canvas and
   export). The look stays: dark ground, green accent, the colours of
   `slides/boards/pan_kit.py`. Space Grotesk / JetBrains Mono are not installed here
   (docs/OPEN.md); until he allows the download into `models/fonts/`, a fallback font.
5. The narration file keeps his `## Title` headings, but only the paragraphs go into
   film-lab's `narration.txt` (in "Dynamic Arrays - Dropdown Lists" pasted headings were
   read aloud and captioned, docs/OPEN.md 2026-10-10).

## His fixed decisions (unchanged)

- Intro (narration only) → 5 slides → outro (narration only). 2-3 min; ~300 words, hard
  cap 340. Measured on his five English Excel finals: 2.0-2.4 words/s after pause cutting
  and speed 1.25, so 300 words ≈ 2:05-2:30 and 340 ≈ 2:22-2:50.
- NATO 6400 mils (1° = 17.78 mils). Casio fx-85GT X. Observer at E 34500, N 21800.
- Series tag `MAP AND CALCULATOR · 01 · OBSERVER`; step tags `SLIDE n · A/B`.
- Film folder `projects/Map and Calculator 01 - Observer/`.

## Calculator keys: checked against Casio's guide (slides/docs/tech/casio-fx-85gtx.md)

| his key | Casio fx-83GT X / fx-85GT X guide |
|---|---|
| Degrees: `SHIFT` `MENU` `2` `1` | confirmed ("SHIFT MENU (SETUP) 2 (Angle Unit) 1 (Degree)") |
| `D` / `R` on screen | confirmed ("D: Degree, R: Radian, or G: Gradian") |
| Pol = `SHIFT` `+` | confirmed |
| comma = `SHIFT` `)` | confirmed |
| negative with `(−)` | confirmed |
| Rec = `SHIFT` `−` | not in the text extract (the key symbol is lost); check on the keypad drawing in the guide when slide 03 is built |
| θ of Pol | shown between −180° and 180°: his "Negative? Add 360" is needed |

## Slides (his content; Manim notes in brackets)

| # | Title | Scene |
|---|---|---|
| 01 | Degree mode | `obs-mode` |
| 02 | Compass and map | `obs-compass` |
| 03 | Target coordinates | `obs-rec` |
| 04 | Direction and distance | `obs-pol` |
| 05 | Fire correction | `obs-correction` |

**01 Degree mode**
- A — *Wrong mode, wrong answer* · *R on the screen: the calculator works in radians.* ·
  screen, indicator **R** (orange outline), `tan(45)` → `1.619775191` · ✗ *R on the screen = wrong angles*
- B — *Set degrees* · *SHIFT, MENU, then 2 and 1.* · keycaps `SHIFT → MENU → 2 → 1`
  [each lights on its word], screen with **D**, `tan(45)` → `1` · ✓ *D on the screen*

**02 Compass and map**
- A — *The compass isn't the map* · *A compass gives a magnetic azimuth.* · compass dial,
  needle at 61° · ✗ *Don't type it in as it is*
- B — *Add the correction* · *Its value and sign are in the map margin.* · two north
  arrows (grid north / magnetic north), the angle between them labelled; `Map azimuth =
  compass azimuth + correction` · ✓ *From here on, only the map azimuth*. No number for
  the correction.

**03 Target coordinates (Rec)**
- A — *I see the target* · *Your position, the rangefinder distance, the map azimuth.* ·
  card `ME E 34500 · N 21800`, `D 2400 m`, `Az 65°`; keycaps `SHIFT` + `−` = `Rec(`;
  screen `Rec(2400,65)` · *Comma: SHIFT + )* [map: ME, the 65° line, 2400 m]
- B — *Add the shifts* · *x is the step north, y the step east.* · screen
  `x=1014.283828`, `y=2175.138689`; card `E 34500 + 2175 = 36675`,
  `N 21800 + 1014 = 22814`, highlighted `TARGET E 36675 · N 22814` ·
  ✓ *North-east: x and y positive* [map: the north leg 1014, the east leg 2175, TARGET]

**04 Direction and distance (Pol)**
- A — *Target minus me* · *North difference first, then east.* · card
  `ΔN = 20300 − 21800 = −1500`, `ΔE = 32100 − 34500 = −2400`; keycaps `SHIFT` + `+` =
  `Pol(`; screen `Pol(−1500,−2400)` · amber *Type minus with the (−) key.*
  [map: ME, the target at E 32100 N 20300, the two legs]
- B — *Negative? Add 360* · *r is the distance, θ the azimuth.* · screen `r=2830.19434`,
  `θ=−122.0053832`; card `D 2830 m`, `Az −122.0 + 360 = 238.0°`,
  `238.0 × 17.78 ≈ 4232 mils` · ✓ *South-west: 180–270°* [map: the azimuth arc from
  north, clockwise, 238°]

**05 Fire correction**
- A — *The round missed* · *Burst 20 mils left, target 3 km from you.* · burst left of
  the crosshair, bracket "20 mils", caption "view through binoculars";
  `W (m) = D (km) × mils` · *1 mil ≈ 1 m at 1 km*
- B — *Send the opposite* · *3 × 20 = 60 metres.* · big `RIGHT 60`; card
  `Too far → DROP`, `Too short → ADD` · ✓ *Always opposite the burst*

## His numbers, recomputed in Python (all match)

| | value |
|---|---|
| tan(45 rad) | 1.6197751905 |
| Rec(2400, 65°) | x 1014.2838, y 2175.1387 → E 36675, N 22814 |
| Pol(−1500, −2400) | r 2830.1943, θ −122.0054° → 237.9946° |
| × 17.78 | 4231.5 → 4232 (exact 6400/360: 4231.0); his choice: 4232 |
| 3 km × 20 mils | 60 m (exact 58.9 m) |
| round trip Pol(Rec) | 2400.0 m, 65.0° |

## His two flags before recording (sources: slides/docs/tech/artillery-pl.md)

1. **Correction wording and call-for-fire format.** DROP / ADD and RIGHT / LEFT in metres
   are the English observer words used here (from memory, not checked against a manual).
   A Polish training guide's snippet says "w prawo 0-20, bliżej 100": direction in
   thousandths, range in metres. Check against the unit's instruction.
2. **The sign of the correction on the map sheet.** *Topografia wojskowa* (Legia
   Akademicka): T = M + Δ, Δ = (±δ) − (±γ), east +, west −: the same form as
   `map azimuth = compass azimuth + correction`.

Also found: Polish artillery (DTU-3.2.5.6.1, 2023) calls 1/6400 "mils" and 1/6000
"tys". The video says "mils" for 6400, which matches that naming.

## Steps

1. Helpers in `slides/aimanim/kit.py` (the one Manim module), his list made for Manim:
   the calculator screen (dark bezel, screen #C7D1C1, indicator top-left, expression line,
   results right-aligned, a cursor bar while empty; no Casio logo), keycaps in a row, the
   mono card with one highlighted row, the big command, the compass dial (61°), the two
   norths with the angle, burst vs target with the mil bracket, and the map grid. Built
   only on his go (agreement 7).
2. One test still first (Δ and θ in Manim `Text`). Then the five scenes, each
   `look still` at full size: 1080x1920 (ffprobe), 0 `[layout]` notes, captions zone clear
   (1490-1860 px).
3. The narration last, from the final slides, by his rules: `video01_map_calculator.md`,
   ~300 words (`wc -w`, headings excluded), English, intro (problem + promise), one
   paragraph per slide headed by its title, A then B, no "on the left / right", no "on
   this slide", keys spoken shortcut-first ("SHIFT, MENU, two, one"), outro with the five
   moves, *"Always target minus me, and always the opposite of the burst."* and the next
   video. Then the whole text into `slides.script.txt` before any publish.
4. Before recording: every key sequence pressed on a real fx-85GT X and each screen
   compared with the slide; his two flags checked against the unit's instruction.
5. `publish` (asked first), he narrates, `film go`, "narrated" → `clips`, `film draft`.

## Done when

Five stills 1080x1920 with 0 layout notes and the contact sheet (`look film`); the
narration file with its word count.

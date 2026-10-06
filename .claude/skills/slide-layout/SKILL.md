---
name: slide-layout
description: Layout rules, measured sizes and fixes for every Manim slide in ai-manim -- load BEFORE writing or changing any scene.py (new-scene and time-to-words load it), and whenever a still looks wrong. Also how to grow this knowledge: every layout fix ends with a line added here or a helper added to aimanim/kit.py.
---

# Slide layout: do it right the first time

Every rule here came from a slide that went wrong. Use the kit; it holds
the fixes as code. When you fix a new kind of problem, add it (last section).

## 1. Start from the template
```
copy scenes/_template/  ->  scenes/<slug>/
```
It already uses `kit.title`, `kit.text` (baselines), `kit.run` (beats +
the layout check). Never copy an older scene's construct loop.

## 2. The frame (aimanim/frame.py — the only source of these numbers)
| | value | why |
|---|---|---|
| frame | 9 × 16 units, 1080 × 1920 px, 120 px per unit | ai-film-lab films |
| safe x | −4 … 4 (`SIDE`) | 0.5 unit margin each side |
| safe y | −4 (`BOTTOM`) … 7 (`TOP`) | bottom quarter = captions (assumed, OPEN.md); 1 unit top |
| text | ≥ `MIN_FONT` 56 | readable on Jacek's phone (checked 2026-10-05) |
| colours | INK, DIM, ACCENT (the thing explained), SECOND (what it's compared with) | |

## 3. Measured sizes at MIN_FONT (Manim default font) — plan with these
| thing | width | height |
|---|---|---|
| one digit | 0.48 | 0.59 |
| "4800", "1200" | 1.83–1.90 | |
| "0.73 cm", "1.45 cm" | 3.05 | |
| "Triumph" | 3.35 | 0.75 (descender) |
| TITLE_FONT 80: "Group centre" | 7.38 | 1.06 |
| TITLE_FONT 80: "Range by width" | 8.74 → too wide | |
Rule of thumb: ~17 digits/characters fill the safe width at 56; ~11 at 80.
Measure anything new with `kit.fits("text")` BEFORE placing it.

Consequences already paid for:
- **labels beside a circle**: a 4-digit label is 1.9 wide, so a circle with
  labels outside at 3 and 9 o'clock needs radius ≤ 2.0 (back-azimuth).
- **two columns**: centres at x = ±2.2 hold texts ≤ 3.3 wide (zero-clicks).
- **a whole reticle across the width**: ±14 mil at 0.27 units/mil; at 0.28
  the "2" above the 14-mil stadia pokes 0.10 past SIDE (zero-reticle).
  Its centre, to range on, goes on its own slide at 1.6/mil (zero-range):
  both on one slide left the labels crowded.
- **bar scales**: pick units/cm so the longest bar fits the free height;
  10 cm at 0.6 = 6 units (zero-mil), 5 cm at 1.0 (zero-clicks).

## 4. Placement rules (each is in kit)
- **Rows of text: by BASELINE** — `kit.text(s, x, baseline)`. Centring by
  middle or top puts "turret"/"reticle", "Triumph"/"SLx" at different heights.
- **Title: `kit.title(s)`** — top on TOP, shrinks to fit. A title centred at
  TOP − 0.3 pokes 0.23 above TOP.
- **Directions from angles: `kit.toward(turns)`** — rounds sin/cos; sin(π) =
  1.2e-16 makes `next_to` shift a label sideways ("3200" drifted right).
- **Two arrows on one line** (there and back): offset the second sideways
  (0.3 units), else it hides the first.
- **A label for each arrow** goes on the side away from other labels: two
  labels stacked read as a list, not as two arrows (zero-group).
- **A name with an arrow**: start the arrow 0.62 above the name's
  baseline (the text top is ~0.45); at 0.5 the check says the name touches
  its own arrow (zero-reticle). Put names in the empty corners of the
  drawing, not over it.
- **A table under a label** (zero-reticle): leave a blank row between, or
  it reads as part of the label above.
- **One drawing on two slides**: its geometry goes in a stdlib module
  (`aimanim/aurora.py`, in its own units) and each scene scales it, so the
  slides cannot drift apart.
- **Static things** (title, grid, axes) go in `background`: on screen before
  the first word, and labels may lie on them without a `[layout]` note.
- At most 3 objects move in one step: group parts with `VGroup`.
- No effects or polish Jacek didn't ask for.

## 5. The check — runs inside every render
`kit.run` checks the last frame (= the still) and prints:
```
[layout] "1200 + 3200 = 4400" is past SIDE (-4.04..4.04)
[layout] "6400 mil" is 0.13 above TOP
[layout] "1600" touches a Arrow
```
- Fix every note, or say in the answer why it is a false alarm. The check
  uses boxes: a DIAGONAL arrow's box is large, so "touches a Arrow" next to
  a diagonal can be false — look at the still.
- Then still look at the half-size PNG (Read it): the check cannot see
  meaning (wrong label on an arrow, a confusing picture).
- For the bottom margin of an existing PNG, measure pixels: lowest ink must
  be ≥ 480 px from the bottom at full size.

## 6. Units and words
- Metric only on screen (Jacek, 2026-10-05). Imperial sources are converted
  in spec.md, with the conversion shown; MOA and mil are angles, fine.
- Numbers on screen are computed in scene.py from the spec's data (never
  typed twice), and rounded the way the narration says them.
- When a slide changes what he says (a number, a unit, a sentence split),
  update `films/<film>.script.txt` in the same turn.

## 7. Growing this skill (do this every time)
When a still needs a layout fix that is not covered above:
1. fix it in the scene;
2. if it can happen again: make it a helper or a check in `aimanim/kit.py`,
   or a measured size / rule in this file (with the slide it came from);
3. if the fix changes how existing slides render, re-render them and show
   they are unchanged (pixel diff) or show what changed.
The goal: the next slide needs no layout fix at all.

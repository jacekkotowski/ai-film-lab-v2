---
name: slide-layout
description: The one craft skill for Manim slides in ai-manim -- the frame and its rules, the commands that measure, plan, render, check and rehearse (kit fits, layout stack/pitch/columns/rows/sizes, look still/draft/film/stats, film check), the quick map from a printed problem ([layout], [beats], PROBLEM) or a wrong-looking still to its general fix, and the slide recipes with almost-there code in docs/patterns. Load BEFORE writing or changing any scene.py (new-scene and time-to-words load it), whenever a still looks wrong, and to file a new fix.
---

# Slide layout: do it right the first time

Every rule here came from a slide that went wrong. Short on purpose: the
detail is in `docs/patterns/` (issues I01–, tasks T01–), sizes in
`docs/tech/sizes.json`. Search before solving: `docs/patterns`, then qmd
(`manim`, `manim-history` collections).

## 1. The loop — one command per job

| job | command |
|---|---|
| start a scene | copy `scenes/_template/` (kit.title, kit.text, kit.run already in) |
| closest recipe | `grep -n "^### T" docs/patterns/tasks.md` → copy its code |
| label widths | `uv run --extra render python -m aimanim.kit fits "a label" "big@72"` (saved to sizes.json) |
| widths already measured | `python -m aimanim.layout sizes <part of text>` |
| plan the column | `python -m aimanim.layout stack title 56 block:3.2 56 gap:0.3 56` → baselines, room |
| dots for n people / columns / row step | `python -m aimanim.layout pitch 10000 8 4.5` · `columns 3.12 2.9` · `rows 56 72` |
| still, half / full | `python -m aimanim.look still <scene>` · `… still <scene> full` |
| the motion | `python -m aimanim.look draft <scene>` → Read `out/steps.png` (end of each step) |
| timing before he narrates | `python -m aimanim.film <film> check` |
| a whole film | `python -m aimanim.look film <film>` (stills, notes, margins, rehearsal) |
| what renders cost, recurring issues | `python -m aimanim.look stats` |
A `PROBLEM` line = fix it (exit code 1). Plain commands only (CLAUDE.md).

## 2. The frame (aimanim/frame.py — the only source of these numbers)
| | value | why |
|---|---|---|
| frame | 9 × 16 units, 1080 × 1920 px, 120 px per unit | ai-film-lab films |
| safe x | −4 … 4 (`SIDE`); pixels ≥ 60 from the sides | 0.5 unit margin each side |
| safe y | −4 (`BOTTOM`) … 7 (`TOP`); pixels ≥ 480 from the bottom | captions sit in the bottom quarter (measured) |
| text | ≥ `MIN_FONT` 56; ~17 characters fill 8.0 at 56, ~11 at 80 | readable on his phone (2026-10-05) |
| rows | baselines ≥ 0.80 apart at 56 (`layout.row_step`) | descender 0.17 + capitals 0.59 |
| fine drawing | lines width 3, dots r 0.035 at 0.27/mil | legible on his phone (zero-reticle) |
| colours | INK, DIM, ACCENT (explained), SECOND (compared), SICK / HEALTHY (populations) | |

## 3. Rules (one line each; the entry has the why)
- Text by its BASELINE: `kit.text(s, x, baseline)`, never `move_to` (I03).
- Title: `kit.title(s)` — top on TOP, shrinks to fit.
- Directions from angles: `kit.toward(turns)` (I06).
- Measure every label before placing it; too wide → I01's order.
- Plan the column with `layout.stack` before drawing (I04).
- Labels away from other labels; names in empty corners, arrow from 0.62 above the baseline (I09).
- Two arrows on one line: offset the second 0.3 (I08).
- A table under a label: a blank row between (zero-reticle).
- One drawing on two slides: geometry in a stdlib module, each scene scales it (I14).
- Static things (title, grid, axes) in `background` (labels may lie on them).
- Reticle: `kit.reticle(kit.mil_to(scale, aim), window)`; chains: `kit.chain(items, top, step=…)` by name (T07, T09).
- Target behind lines: `set_z_index(-1)`, fill opacity 0.35–0.6.
- Populations: `kit.dots` / `kit.people`, one VMobject per cell, pitch from `layout.pitch_for` (T02, I15).
- Highlight a column/row: `kit.box` (I10); cross out: `kit.strike` (I11).
- A few marks in a crowd: ring or recolour, never only fade (I12); one dot size per comparison, areas by `layout.area_radius` (I13).
- Rotated row names: row ≥ 2.9 tall at 56, x ≥ −3.58.
- ≤ 3 objects move in one step (VGroup the rest). No effects he did not ask for.
- Metric only on screen; numbers computed in scene.py from the spec, rounded as he says them; a changed number → `films/<film>.script.txt` in the same turn.

## 4. Quick map: what you see → the entry in docs/patterns/issues.md
| you see | entry |
|---|---|
| `past SIDE`, a word cut, a label wider than its column | I01 |
| `"a" touches "b"` for stacked rows | I02 |
| uneven label heights | I03 |
| caption zone reached / a big empty band | I04 |
| quiet check but ink near an edge (`look` margins PROBLEM) | I05 |
| `touches a Line/Rectangle` for a box or strike you meant | I10, I11 |
| a highlighted item nobody can find | I12 |
| a picture that exaggerates | I13 |
| `step n starts … after` / `runs past the words` | I16 |
| `the word 'x' was not heard` | I17 |
| clip shorter than its slide | I18 |
| 854×480 output · `UnicodeEncodeError` · "Allow once" | I20 · I21 · I22 |
| "LF will be replaced by CRLF", a hook failing on `\r` | I24 |

Making a slide: T01 the loop · T02 a share · T03/T04 a 2×2 table and its
rates · T05 A vs B · T06 a sweep · T07/T08 calculation, formula · T09 to
scale · T10 a timeline · T11 answer vs truth · T12 counts → people · T13 cue words.

## 5. The check inside every render
`kit.run` checks the last frame (the still) and prints `[layout]` notes:
outside the safe area, text touching text, text touching a drawing
(boxes; a stroke-only line is sampled along its path). Fix every note or
say why it is a false alarm; then look at the picture — the check cannot
see meaning.

## 6. Growing (every time)
A new fix or recipe → `docs/patterns/` (template in its README): search
first, then add the slide to an existing entry or open a new one as a
`note`; climb the ladder (note → pseudocode → code → helper) the second
time. A helper changing renders → re-render and show the stills unchanged
(checksum) or what changed. End of a film: `python -m aimanim.patterns due`
and the `grow-skills` pass. The goal: the next slide needs no fix.

# The Aurora MIL reticle — reference stills and how to reuse them

Primary Arms ACSS Aurora MIL (Jacek's SLx 5x MicroPrism). Not the 5.56/.308
yards BDC Aurora that most web pictures show (`shooting-optics` §4).

- **Geometry** (in mil, y up, origin = chevron tip = aim point):
  `aimanim/aurora.py`. Every number and its source: `scenes/zero-reticle/spec.md`
  and the `shooting-optics` skill §5.
- **Drawing it on a slide:** `kit.reticle(kit.mil_to(scale, aim), window, stroke, dot_r)`.
  `window = (x0, x1, y0, y1)` in mil gives an enlarged part. Returns
  `VGroup(lines, dots, numbers)`.
- **These stills:** `scenes/_aurora/scene.py`, one class each, 1080×1920, made by
  `kit.reticle` itself, so they are what a slide gets with the same numbers.
  Re-render: `uv run --extra render manim -s -r 1080,1920 --media_dir scenes/_aurora/out scenes/_aurora/scene.py Full Centre Chevron Stadia Line`
  then copy `scenes/_aurora/out/images/scene/<Class>_ManimCE_v0.21.0.png` here.

| still | what | units/mil | aim point | window (mil) | stroke, dot r | used by |
|---|---|---|---|---|---|---|
| `full.png` | whole reticle, numbers 6-4-2 | 0.27 (max: the "2" at 14 mil reaches SIDE at 0.28) | (0, 3.3) | — | 3, 0.035 | zero-reticle, mil-unit, mil-finale |
| `centre.png` | chevron, ladder, MIL grid 2–10 | 0.74 | (0, 5.6) | ±5.3, −10.3…0.4 | 4, 0.06 | — |
| `chevron.png` | chevron and bars 2–4 (width ranging) | 1.6 | (0, 4.4) | ±1.3, −4.4…0.35 | 6, 0.08 | zero-range |
| `stadia.png` | right side: line 6–14, man stadia, numbers | 0.85 | (−8.4, 1.5) | 5.5…14.3, ±5 | 4, 0.06 | — |
| `line.png` | horizontal line, dots 1–5 (5th heavy) | 0.6 | (0, 1.5) | ±6.6, ±0.5 | 4, 0.06 | — |

The parts, the manual's names:
- **Chevron** ("Infinitely Precise Chevron"): its tip is the aim point; 1.667 mil wide
  (a 50 cm target at 300 m).
- **Line dots**: one every mil, 1–5 each side, the 5th heavy ("5 MIL indicator").
- **Side line**: solid 6–14 mil, a tick every mil.
- **Auto range stadia** at ±6, 8, 10, 12, 14 mil, numbered 6, 4, 2: a 1.78 m man
  fits them at 550 / 460 / 370 / 270 / 180 m. **The numbers are hundreds of yards,
  not mils**: the "4" stadia is 4.86 mil tall.
- **Centre ladder**: a bar every mil from 2 to 10 under the chevron; bars 2, 3, 4
  are 1.25 / 1.00 / 0.833 mil wide (a 50 cm target at 400 / 500 / 600 m).
  Heights in mil read on it: chevron tip to bar n = n mil.
- **MIL grid**: dots 1 mil apart, rows 2–10; rows 2, 3, 4 reach ±2, ±3, ±4, rows 5–10 ±5.

Left out at every size so far: the small brackets at the 5th and 10th mil, the
half-mil ticks, the grid's own "5" and "0".

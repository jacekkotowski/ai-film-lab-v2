# Casio fx-85GT X — keys and displays (Casio's manual)

Source: *fx-83GT X / fx-85GT X User's Guide* (EN, 108 pages),
https://www.casio.com/content/dam/casio/global/support/manuals/calculators/pdf/004-en/f/fx-83GTX_85GTX_EN.pdf
Read 2026-10-10 through a text extract (quoted by a query, not every page by
eye). Key legends and pictures are lost in an extract: the layout of the keypad
is NOT in this note.

## Confirmed by the manual (quoted)

- Degrees: `SHIFT` `MENU` (SETUP) → `2` (Angle Unit) → `1` (Degree).
  Radian is `2`, Gradian `3`. "Specify the angle unit before performing
  calculations" (trig, Pol, Rec).
- Pol: `SHIFT` `+` (Pol), comma `SHIFT` `)` (,).
  `Pol(√2,√2)` shows `r=2, θ=45` (Line display).
  θ is shown in -180° < θ < 180°, in the calculator's angle unit.
  r goes into variable X, θ into Y (the old values are overwritten).
  Inside a longer expression only the first value (r or x) is used.
- Rec: `Rec(√2,45)` shows `x=1, y=1`.
- Status bar (2026-10-11, the indicator table): "D/R/G — Indicates the current
  setting of Angle Unit (D: Degree, R: Radian, or G: Gradian)"; "S — the keypad
  has been shifted by pressing the SHIFT key".
- Inverse trig is the SHIFT of the trig key (`SHIFT` `sin` = sin⁻¹, in the
  manual's example). A negative number is typed with the `(−)` key.

## NOT confirmed (check on the calculator itself)

- That the model is non-programmable (not in the extract).
- The exact look of the Pol / Rec result in natural (Math) display, and the
  number of digits shown (10 significant is reasoned, not seen).
- Whether Pol shows r in √ form: Pol(−1500,−2400) has r = 300√89 exactly.
  The manual's Pol examples all give a whole r (2), so they don't say.

## Confirmed 2026-10-11 from Casio's HTML manual for this model

https://support.casio.com/global/en/calc/manual/fx-83GTX_85GTX_en/ (one page
per topic; key legends are small PNGs in `img/key/`, read as pixels: the
built-in browser could not screenshot them).
- **Rec = `SHIFT` `−`.** Rec example keys: 57398 (SHIFT), 57361 (Rec), and
  57361.png is drawn as a minus. Pol's key 57360.png is drawn as a plus.
  Other codes: 57359 `=`, 57365 `)`, 57346 the right arrow (cursor out of √).
- Irrational form (page inputting_expressions_values/calculation_results.html):
  in MathI/MathO, `=` gives the √/π form and `SHIFT` `=` (≈) gives the decimal.
  In MathI/DecimalO or LineI/DecimalO the result is always decimal.
- No emulator for the GT X: Casio's emulators are for the graphing models
  and the ClassWiz range on ClassPad.net (account needed).

## Traps

- A search for this model also returns the fx-82/85/95/350ES PLUS manual and
  the newer fx-83GT CW / fx-85GT CW (a SETTINGS menu): different calculators.
  `SHIFT MENU 2 1` is for the GT X.
- A point to the south-west or west gives θ below 0: azimuth = θ + 360.
- The `x` of Rec / `X` of Pol is the NORTH step when the angle is an azimuth
  (the plan feeds Pol north first, then east). The Gemini cards in the online
  project RD01 Artillery call X the east: do not mix the two on one slide.

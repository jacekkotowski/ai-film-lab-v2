# zero-range — slide 3b of 4 of the zeroing film

**Problem (Jacek's script, section 3, second sentence):** the Aurora MIL
reticle's width marks range a target of known width. Metric only.

**One idea:** a 50 cm wide target fills a smaller mark the further away
it is, so the mark it fills tells the distance.

**Data**
- The manual defines the marks as 18 in at 300/400/500/600 yd. 18 in is
  exactly ½ yd and 50 cm is exactly ½ m, so the same marks are **50 cm at
  300/400/500/600 m**: width in mil = 1000 × 0.5 / distance = **500 / metres**.
  (The metric version is derived here, not printed in the manual.)
| distance | width of 50 cm | reticle mark (Aurora MIL manual) |
|---|---|---|
| 300 m | 1.667 mil | the chevron |
| 400 m | 1.250 mil | 2nd MIL stadia |
| 500 m | 1.000 mil | 3rd MIL stadia |
| 600 m | 0.833 mil | 4th MIL stadia |
- check with the manual's metric formula, distance (m) = size (cm) × 10 / mils:
  50 × 10 / 1.667 = 300.0 m (and 400.0, 500.0, 600.0)
- **Drawn to scale: the WIDTHS only.** The vertical spacing of the marks
  and the chevron's height are schematic — not taken from a drawing of
  the reticle. Look through the SLx before using this as a picture of it.

**Steps (one per sentence he says)**
0. before the first word: title "Ranging"
1. line 0 — the four marks: chevron and three stadia, widths to scale
2. line 1 — the 50 cm target's width over the chevron; "300 m"
3. line 2 — the same 50 cm over the next three marks; "400 / 500 / 600 m"

**Narration (his script's sentence, made metric and split in three; he says it his own way)**
"Its width marks also range targets. A target fifty centimetres wide
fills the central arrowhead at 300 metres, and the next three marks at
400, 500 and 600 metres."
If it stays one sentence: `BEAT_LINES = [0, 0, 0]`.

**Sources:** ACSS Aurora MIL reticle manual, "Target ranging — width"
and "Ranging with MILs". Link in `scenes/zero-group/spec.md`.

**Status:** written 2026-10-05; made metric the same day.

# mil-man — slide 2 of 8 of the mil-measure film

**Problem (Jacek's plan, 0:15–0:45):** a man 1.78 m tall seen as 6, 4, 3, 2
MIL; distance ≈ size × 1000 / MIL; example 1.78 × 1000 / 4 ≈ 445 m.

**One idea:** the fewer mils a man of known height fills, the further he is,
and the height in mil gives the distance.

**Data** (distance in m = size in m × 1000 / mil; small angle, error < 1e-5)
| reading | 1.78 × 1000 ÷ mil | exact (1.78 / tan) | on the slide |
|---|---|---|---|
| 6 MIL | 296.67 | 296.66 | 297 m |
| 4 MIL | 445.00 | 445.00 | 445 m |
| 3 MIL | 593.33 | 593.33 | 593 m |
| 2 MIL | 890.00 | 890.00 | 890 m |
- Where on the Aurora: the centre ladder. Head on the chevron's tip (0),
  feet on bar n = n mil. Bars exist at 2–10 (`aimanim/aurora.py`), so all
  four readings land on a bar. Drawn at 0.75 units/mil, ladder only.
- **Not used: the numbered stadia.** Their numbers 2-4-6 are hundreds of
  yards (5'10" man), not mils: the "4" stadia is 4.86 mil tall. Next to
  "4 MIL" they mislead (`docs/aurora/README.md`).
- Rounding: whole metres; the narration says them as on screen.

**Steps (one per sentence he says)**
0. before the first word: title "Range by height", the ladder
1. "Take" — the man at 6 mil; chain row "1.78 m"
2. "head" — head line at the tip, his feet's line to bar 6, "6"
3. "Further" — the men at 4, 3, 2 mil, their lines and readings
4. "distance" — 297 / 445 / 593 / 890 m beside the readings (445 in accent)
5. "Four" — chain: "4 MIL" → "1.78 × 1000 ÷ 4" → "445 m"

**Narration (suggested)**: films/mil-measure.script.txt [02].

**Sources:** `shooting-optics` §1 (formula, the manual's form size(cm)×10/mil
is the same); ladder geometry §5. Calculated.

**Status:** written 2026-10-06.

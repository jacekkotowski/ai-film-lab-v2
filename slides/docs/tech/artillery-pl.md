# Polish artillery and map conventions — what the sources say

For "Mapa i kalkulator 01 - Obserwator" (film/docs/plans/2026-10-11/PLAN-mapa-kalkulator.md).
Read 2026-10-11 through text extracts (quotes below are what the extract returned;
neither document was read whole, by eye). Doctrine is the unit's: these notes say
what was found, not what the unit uses.

## DTU-3.2.5.6.1 *Instrukcja strzelania i kierowania ogniem wojsk rakietowych i artylerii* (Warszawa 2023, 85/2023)

Copy on Scribd: https://www.scribd.com/document/746187419/ (not an official site).
- Two units, by name: "tysięczna artyleryjska (1/6000) (tys)" and "tysięczna
  Rimailho (1/6400) (ang. mils)". So "tys" alone means 1/6000 there.
- Angles are written with a dash: "z zaokrągleniem do 1-00" (1-00 = 100).
- A formula with 15-00 as the right angle (`sin(15-00 − αc)`, search snippet):
  the 1/6000 circle.
- The correction words and whether the observer gives direction in metres or
  thousandths: NOT in the extract.

## *Topografia wojskowa* (Legia Akademicka course text, tools.aps.edu.pl/pliki/legia/06.pdf, 33 pages)

- Azimuths (geographic, magnetic, topographic) are measured clockwise, 0-360°.
- Zboczenie magnetyczne δ: needle east of the geographic meridian +, west −.
  Zbieżność południków γ: grid line east of the geographic meridian +, west −.
  Uchylenie magnetyczne Δ = (±δ) − (±γ) (angle grid line → magnetic meridian).
- **M = T − Δ**, so **T = M + Δ** (topographic = magnetic + Δ). The plan's
  "Az mapy = Az kompasu + PK" is this formula if PK means Δ with this sign.
  The name "PK" itself is not in the extract.
- Plane coordinates are named **E and N** (UTM).
- The NATO-style sheet margin shown in the text prints "360° = 6400 mils,
  1° = 17.78 mils".

## Search snippets only (not opened)

- A Polish shooting-training guide (Scribd 685274028): "360°/60-00, 90°/15-00" and a
  correction "w prawo 0-20, bliżej 100" (direction in thousandths, range in metres).

## What changes between 6400 and 6000 (computed, check_numbers.py)

| | 1/6400 (mil) | 1/6000 (tys) |
|---|---|---|
| 1° | 17.78 | 16.67 |
| 1 unit at 1 km | 0.98 m | 1.05 m |
| azimuth 237.99° | 4231 (×17.78: 4232) | 3967 |
| 3 km × 20 units | 58.9 m | 62.8 m (the rule "≈ 60 m" holds for both) |

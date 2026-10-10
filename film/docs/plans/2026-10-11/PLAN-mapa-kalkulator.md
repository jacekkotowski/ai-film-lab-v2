# Plan: "Mapa i kalkulator 01 - Obserwator"

Status 2026-10-11: plan only, nothing built. **This is Jacek's plan** (pasted 2026-10-10,
from the online project RD01 Artillery, chat "Artillery Cheatsheet") with ONLY the
changes listed next. Every decision in it is his and is not re-asked.

## Changes to his plan (all of them)

1. **Manim slides, not pan boards** (Claude's recommendation when he asked which is
   better; he went on to the map). Each slide is one 1080x1920 scene: his step A, then
   his step B, as beats in the same frame (no pan). The keys light one by one on the
   word that names them; the screen changes with them.
2. **The map is on screen** (his message: "we need both to see the map and what buttons
   should be pressed, because we do the calculations based on the map"): slides 03 and 04
   draw a 1 km grid with the E/N numbers, JA, the target, the azimuth line and the ΔN / ΔE
   legs; slide 02's two north arrows are the map's margin. The map is drawn (no real
   sheet); a photo of his sheet can replace it if he gives one.
3. HTML-only items drop out: `.dc.html` files, `lang="pl"`, `aria-label`, `PAN_LANG`,
   the pan-board canvas and export. The look stays (dark ground, green accent, the same
   colours as `slides/boards/pan_kit.py`). Space Grotesk / JetBrains Mono are not
   installed on this laptop (docs/OPEN.md); until he allows the download into
   `models/fonts/`, the slides use a fallback font.
4. The narration file keeps his `## Title` headings, but only the paragraphs go into
   film-lab's `narration.txt`: in "Dynamic Arrays - Dropdown Lists" headings pasted
   with the text were read aloud and captioned (docs/OPEN.md, 2026-10-10).

Nothing else changes: language, mils, calculator, scenario, slides, texts, numbers,
length, narration rules and his two flags are his, below, as written.

## His fixed decisions (unchanged)

- Structure: intro (narration only) → 5 slides → outro (narration only). 2-3 min;
  ~300 words, hard cap 340. Measured on his five Excel finals: 2.0-2.4 words/s after
  pause cutting and speed 1.25, so 300 words ≈ 2:05-2:30 and 340 ≈ 2:22-2:50 (English;
  Polish not measured).
- Polish on screen and in narration. NATO 6400 mils (1° = 17,78). Casio fx-85GT X.
- One scenario: observer at E 34500, N 21800.
- Series tag `MAPA I KALKULATOR · 01 · OBSERWATOR`; step tags `SLAJD n · A/B`.

## Calculator keys: checked against Casio's guide (slides/docs/tech/casio-fx-85gtx.md)

| his key | Casio fx-83GT X / fx-85GT X guide |
|---|---|
| Deg: `SHIFT` `MENU` `2` `1` | confirmed ("SHIFT MENU (SETUP) 2 (Angle Unit) 1 (Degree)") |
| `D` / `R` on screen | confirmed ("D: Degree, R: Radian, or G: Gradian") |
| Pol = `SHIFT` `+` | confirmed |
| comma = `SHIFT` `)` | confirmed |
| negative with `(−)` | confirmed |
| Rec = `SHIFT` `−` | not in the text extract (the key symbol is lost); check on the keypad drawing in the guide when slide 03 is built |
| θ of Pol | shown between −180° and 180°: his "Ujemny? Dodaj 360" is needed |

## Slides (his text, unchanged; Manim notes in brackets)

| # | Title | Scene |
|---|---|---|
| 01 | Tryb stopni | `obs-tryb` |
| 02 | Kompas i mapa | `obs-kompas` |
| 03 | Współrzędne celu | `obs-rec` |
| 04 | Kierunek i odległość | `obs-pol` |
| 05 | Korekta ognia | `obs-korekta` |

**01 Tryb stopni**
- A — *Zły tryb, zły wynik* · *Na ekranie R: kalkulator liczy w radianach.* · screen,
  indicator **R** (orange outline), `tan(45)` → `1.619775191` · ✗ *R na ekranie = błędne kąty*
- B — *Ustaw stopnie* · *SHIFT, MENU, potem 2 i 1.* · keycaps `SHIFT → MENU → 2 → 1`
  [each lights on its word], screen with **D**, `tan(45)` → `1` · ✓ *D na ekranie*

**02 Kompas i mapa**
- A — *Kompas to nie mapa* · *Kompas pokazuje azymut magnetyczny.* · compass dial,
  needle at 61° · ✗ *Nie wpisuj go wprost*
- B — *Dodaj poprawkę* · *Wartość i znak PK są w ramce mapy.* · two north arrows
  (N siatki / N magnetyczna), angle labelled PK; `Az mapy = Az kompasu + PK` ·
  ✓ *Dalej liczysz tylko na azymucie mapy*. No numeric PK.

**03 Współrzędne celu (Rec)**
- A — *Widzę cel* · *Twoja pozycja, odległość z dalmierza, azymut mapy.* · card
  `JA E 34500 · N 21800`, `D 2400 m`, `Az 65°`; keycaps `SHIFT` + `−` = `Rec(`; screen
  `Rec(2400,65)` · *Przecinek: SHIFT + )* [map: JA, the 65° line, 2400 m]
- B — *Dodaj przyrosty* · *x to przyrost na północ, y na wschód.* · screen
  `x=1014.283828`, `y=2175.138689`; card `E 34500 + 2175 = 36675`,
  `N 21800 + 1014 = 22814`, highlighted `CEL E 36675 · N 22814` ·
  ✓ *Płn.-wsch.: x i y dodatnie* [map: the north leg 1014 and east leg 2175, CEL]

**04 Kierunek i odległość (Pol)**
- A — *Cel minus ja* · *Najpierw różnica północy, potem wschodu.* · card
  `ΔN = 20300 − 21800 = −1500`, `ΔE = 32100 − 34500 = −2400`; keycaps `SHIFT` + `+` =
  `Pol(`; screen `Pol(−1500,−2400)` · amber *Minus wpisuj klawiszem (−).*
  [map: JA, the target at E 32100 N 20300, the two legs]
- B — *Ujemny? Dodaj 360* · *r to odległość, θ to azymut.* · screen `r=2830.19434`,
  `θ=−122.0053832`; card `D 2830 m`, `Az −122,0 + 360 = 238,0°`,
  `238,0 × 17,78 ≈ 4232 tys.` · ✓ *Płd.-zach.: 180–270°* [map: the azimuth arc from
  north, clockwise, 238°]

**05 Korekta ognia**
- A — *Pocisk nie trafił* · *Wybuch 20 tysięcznych w lewo, cel 3 km od ciebie.* · burst
  left of the crosshair, bracket "20 tys.", caption "widok przez lornetkę";
  `W (m) = D (km) × tys.` · *1 tysięczna ≈ 1 m na 1 km*
- B — *Podaj przeciwnie* · *3 × 20 = 60 metrów.* · big `PRAWO 60`; card
  `Za daleko → BLIŻEJ`, `Za blisko → DALEJ` · ✓ *Zawsze przeciwnie niż wybuch*

## His numbers, recomputed in Python (all match)

| | value |
|---|---|
| tan(45 rad) | 1.6197751905 |
| Rec(2400, 65°) | x 1014.2838, y 2175.1387 → E 36675, N 22814 |
| Pol(−1500, −2400) | r 2830.1943, θ −122.0054° → 237.9946° |
| × 17,78 | 4231.5 → 4232 (exact 6400/360: 4231.0); his choice: 4232 |
| 3 km × 20 | 60 m |
| round trip Pol(Rec) | 2400.0 m, 65.0° |

## His two flags before recording, with what the sources say (slides/docs/tech/artillery-pl.md)

1. **Polish correction wording and call-for-fire format.** Found: a Polish training
   guide's snippet says "w prawo 0-20, bliżej 100", i.e. direction in thousandths,
   range in metres; his slide 05 says `PRAWO 60` in metres. Not read in full.
2. **PK sign on the map sheet.** Found: *Topografia wojskowa* (Legia Akademicka):
   T = M + Δ, Δ = (±δ) − (±γ), east +, west −. His formula has the same form if
   PK = Δ; the name "PK" is not in that text.

One more found while checking (not a change; his decision stands):
3. **"tys." vs "mils".** DTU-3.2.5.6.1 (2023) names *tysięczna artyleryjska (1/6000) (tys)*
   and *tysięczna Rimailho (1/6400) (mils)*, and writes angles as `1-00`. His plan uses
   6400 and writes "tys.". NATO-style sheet margins print "360° = 6400 mils". Measured
   effect if a reader takes "tys" as 1/6000: only slide 04's number changes (3967
   instead of 4232); slide 05's "≈ 60 m" holds for both (58.9 m and 62.8 m).

## Steps

1. Helpers in `slides/aimanim/kit.py` (the one Manim module), his list made for Manim:
   the calculator screen (dark bezel, screen #C7D1C1, indicator top-left, expression
   line, results right-aligned, a cursor bar while empty; no Casio logo), keycaps in a
   row, the mono card with one highlighted row, the big command, the compass dial (61°),
   the two norths with the PK arc, burst vs target with the mil bracket, and the map grid.
   Built only on his go (agreement 7).
2. One test still first: Polish letters (ąćęłńóśźż), Δ and θ in Manim `Text` (not yet
   rendered here). Then the five scenes, each `look still` at full size: 1080x1920
   (ffprobe), 0 `[layout]` notes, captions zone clear (1490-1860 px).
3. The narration last, from the final slides, by his rules: `video01_mapa_kalkulator.md`,
   ~300 words (`wc -w`, headings excluded), Polish, intro (problem + promise), one
   paragraph per slide headed by its title, A then B, no "na lewo / na prawo", no "na tym
   slajdzie", keys spoken shortcut-first ("SHIFT, MENU, dwa, jeden"), outro with the five
   moves, *„Zawsze cel minus ja i zawsze przeciwnie niż wybuch."* and the next video.
   Then the whole text into `slides.script.txt` before any publish.
4. Before recording: every key sequence pressed on a real fx-85GT X and each screen
   compared with the slide; his flags 1-3 checked against the unit's instruction.
5. `publish` (asked first), he narrates, `film go`, "narrated" → `clips`, `film draft`.

## Done when

Five stills 1080x1920 with 0 layout notes and the contact sheet (`look film`); the
narration file with its word count.

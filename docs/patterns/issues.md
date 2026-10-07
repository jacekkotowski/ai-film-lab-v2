# Issues — symptom → cause → general fix

Format and ladder: `README.md`. Newest IDs at the end; the order is by kind.

## Text and space

### I01 — text past SIDE / too wide for the slide or its column
- **status**: helper `kit.fits`, `layout.columns`, `layout.label_side`
- **seen**: back-azimuth "4400" (2026-10-05), zero-range title "Range by width", scr-accuracy "screening", scr-cost "per 10,000 screened" (2026-10-06)
- **symptom**: `[layout] "x" is past SIDE (-4.05..-0.25)`; a word cut at the edge
- **cause**: placed before measuring; at 56 about 17 characters fill 8.0 units
- **fix**:
      widths = kit fits <every label>            # one call, before writing
      for a too-wide label, in this order: shorter words > two lines >
          move the centre (layout.label_side) > wider column (layout.columns)
          > a smaller drawing; never a font under 56
      columns = layout.columns([widest label per column])
- **check**: `python -m aimanim.look still <scene>` → no "past SIDE"

### I02 — rows touch each other (descender on capitals)
- **status**: helper `layout.row_step`
- **seen**: mil-man rows at 0.6 (2026-10-06), mil-finale at 0.75, scr-accuracy two-line label at 0.70
- **symptom**: `[layout] "a" touches "b"` for two stacked rows
- **cause**: baseline step < DESCENT(upper) + ASCENT(lower) = 0.17 + 0.59 at 56
- **fix**:
      step = layout.row_step(size_upper, size_lower)     # 0.80 at 56/56
      baselines = [first - i * step for i in range(n)]
- **check**: look still

### I03 — rows at different heights though "on one line"
- **status**: helper `kit.text(s, x, baseline)`
- **seen**: zero-clicks "Triumph"/"SLx", "turret"/"reticle" (2026-10-05)
- **cause**: centring by middle or top; letters with descenders shift the box
- **fix**: every text by its BASELINE: `kit.text(s, x, baseline)`; never `move_to` a Text

### I04 — the slide does not fit vertically / is top-heavy
- **status**: helper `layout.stack` (`python -m aimanim.layout stack …`)
- **seen**: every screening slide was planned by hand (2026-10-06)
- **symptom**: things in the caption zone, or a big empty band
- **fix**:
      rows = layout.stack(["title", 56, ("block", h1), 56, ("block", h2), 56])
      rows[-1]["room"] < 0  -> shrink a block (smaller pitch/scale) or drop a row
      rows[-1]["room"] > 2  -> spread: ("gap", room / n) between groups
      copy the baselines into the scene's layout constants

### I05 — something hard against the edge although the check is quiet
- **status**: helper `look.margins` (inside `look still`)
- **seen**: mil-angle "300 m" 55 px from the edge (2026-10-06), scr-outcomes box line 57 px (2026-10-06)
- **cause**: the check uses boxes and the safe area; strokes and diagonals add pixels
- **fix**: measure ink in pixels: bottom ≥ 480, sides ≥ 60 at full size; move the thing in 0.05

## Drawings and marks

### I06 — a label drifts sideways / a direction is slightly off
- **status**: helper `kit.toward(turns)`
- **seen**: back-azimuth "3200" (2026-10-05)
- **cause**: sin(pi) = 1.2e-16; `next_to` reads the sign
- **fix**: directions from `kit.toward`, which rounds to 9 places

### I07 — an arrow shrinks to a dot / arrows of unequal length
- **status**: helper `kit.chain`
- **seen**: mil-speed "10 MIL per second" (2026-10-06)
- **cause**: arrows placed from text BOXES; a descender changes the box
- **fix**: place from baselines: start = baseline_above − DESCENT − 0.06,
      end = baseline_below + ASCENT + 0.08; step ≥ 1.25 at 56

### I08 — two things on one line hide each other (there and back)
- **status**: note (back-azimuth, 2026-10-05)
- **fix**: offset the second 0.3 units perpendicular to the line

### I09 — a label could belong to either of two marks
- **status**: pseudocode
- **seen**: zero-group (labels stacked read as a list), zero-reticle (names over the drawing)
- **fix**:
      put each label on the side AWAY from the other labels
      names go in the empty corners of a drawing, with an arrow starting
      0.62 above the name's baseline (kit.text top is ~0.45)

### I10 — a container gets a "touches" note for every text inside it
- **status**: helper `kit.box`
- **seen**: scr-outcomes column highlight (2026-10-06)
- **cause**: a Rectangle is ONE box to the check, so all texts inside overlap it
- **fix**: draw it as four Lines (`kit.box(l, b, r, t, color)`)

### I11 — an intended overlap is reported (a strike-through, a label on a grid)
- **status**: helper — `kit.strike` is known to the check; static things go in `background`
- **seen**: scr-meaning "9 in 10" (2026-10-06, fixed 2026-10-07)
- **fix**: a mark meant to cross ONE text: give it `.strikes = text`;
      something meant to lie under texts (grid, axes): put it in `background`
      A new kind of intended overlap: tag it and teach `kit.check` (one line)

### I12 — a mark is invisible on a phone
- **status**: helper `kit.ring(points, radius)` (2026-10-07, `patterns due`)
- **seen**: scr-meaning 2 red among 9,483 (2026-10-06), scr-cost a fading figure in 499
- **cause**: size alone (2–4 px) or opacity changes of one item in hundreds
- **fix**:
      to point at a few items in a crowd: ring them (Circle r ≈ 3 × pitch)
      or recolour them (ACCENT); never only fade or shrink them
      check on the FULL-size still, not the half-size one

### I13 — a picture misleads by size (unequal dots, linear radius)
- **status**: pseudocode, helper `layout.area_radius`
- **seen**: scr-outcomes (20 big dots vs 9,980 small), scr-rarity (prevalence as a circle)
- **fix**:
      a share is compared only at ONE dot size; if a column must be enlarged,
          say so in spec.md and show the honest version on the next slide
      a quantity as a circle: its AREA (radius = layout.area_radius(r0, ratio))

### I14 — one drawing on two slides drifts apart
- **status**: helper — a stdlib geometry module per drawing (`aurora.py`, `screening.py`)
- **seen**: zero-reticle / zero-range (2026-10-06); scr-accuracy / scr-outcomes share the 10,000
- **fix**: geometry and placement constants in `aimanim/<thing>.py`; each scene scales it

### I15 — thousands of objects: slow, or impossible to animate as one
- **status**: helper `kit.dots`, `kit.people`
- **seen**: scr-* (10,000 pregnancies, 2026-10-06)
- **fix**: one VMobject whose subpaths are the dots; a cell = its own object

## Timing

### I16 — a step starts late / the animation runs past the words
- **status**: helper `film <film> check` (before), `[beats]` notes (after narrating)
- **seen**: scr-cost "result" 0.8 s before "needle" (2026-10-07); mil-* clips
- **cause**: a cue word less than RUN_TIME before the next cue
- **fix**:
      gap = start(next cue) − start(this cue)
      if gap < RUN_TIME: choose an earlier word in the same sentence
          ("two weeks for the result" → "two"), else RUN_TIME = gap − 0.1

### I17 — "the word 'x' was not heard"
- **status**: pseudocode
- **seen**: zeroing ("fourteen|14"), screening (numbers)
- **fix**: give both forms "15|fifteen"; read the slide's captions in film.yaml for what he said

### I18 — the clip is a few frames shorter than its slide
- **status**: helper `beats.in_frames`
- **seen**: mil-measure, 1.0–4.6 frames short (2026-10-06)
- **cause**: Manim draws a wait as int(seconds × fps)
- **fix**: waits counted in whole frames (kit.run does it)

### I19 — a caption line's words are timed wrongly (a step early)
- **status**: helper `beats._word_time`
- **seen**: mil-angle "angle" 2.0 s early (2026-10-06)
- **cause**: he dropped or merged a word: the caption has fewer word times than words
- **fix**: take the time at the same place in the line

## Tools and machine

### I20 — the clip or still comes out landscape 854×480
- **status**: rule (CLAUDE.md): always `-r 540,960` or `-r 1080,1920`, never `-ql` alone

### I21 — `UnicodeEncodeError: 'charmap'` when printing "≈", "×", "⁺"
- **status**: pseudocode
- **seen**: kit.fits runs (2026-10-06)
- **cause**: Windows console code page cp1250
- **fix**: in a script: `sys.stdout.reconfigure(encoding="utf-8")` (kit's CLI does);
      never print a Manim object's text in a scratch scene

### I22 — "Allow once" asked for every command
- **status**: rule (CLAUDE.md)
- **cause**: `cd … &&`, `VAR=…` prefixes, heredocs, multi-line `python -c` do not match the allow list
- **fix**: commands as written in CLAUDE.md; files with Write/Edit

### I24 — "LF will be replaced by CRLF" on every commit / a hook fails with "\r"
- **status**: helper — `.gitattributes` `* text=auto eol=lf` (2026-10-07)
- **seen**: every commit 2026-10-06 and 10-07 (one warning per file written), the new hooks
- **cause**: Git for Windows sets `core.autocrlf=true` in its system config;
  Claude's Write/Edit write LF; checkout turned files CRLF (42 of 114 were);
  sh cannot run a CRLF hook
- **fix**:
      .gitattributes:  * text=auto eol=lf   (+ binary for png/mp4/wav)
      git add --renormalize .               # the index was LF already: no change
      convert the CRLF working files to LF  # content identical, git diff empty
- **check**: `git ls-files --eol` → every text file `i/lf w/lf`; no warning on commit
- **new project**: the same .gitattributes on day 0 (docs/AGENT-WORKBENCH.md §9)

### I23 — "the font looks different" on one line
- **status**: note (scr-rarity "LR+ = 0.90 / 0.05", 2026-10-06)
- **cause**: none — it was the same DejaVu Serif; the half-size still misled
- **fix**: before changing text, render the suspect strings alone in a scratch
      scene at full size and compare

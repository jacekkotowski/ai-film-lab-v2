# Tasks — the kinds of slide we make, as recipes

Format and ladder: `README.md`. Start a scene from the closest task: its
code runs once the UPPER_CASE numbers are set. The working original is
named in **seen**; open it when the recipe is not enough.

### T01 — any slide: the loop
- **status**: helper (the commands), see `slide-layout` §1
- **recipe**:
      idea   = one sentence; numbers computed in a stdlib module, tested
      labels = kit fits <all labels>                     -> I01 if > 8.0
      plan   = layout.stack([...])                       -> baselines into constants
      steps  = one step_* per cue word (≤ 3 moving, VGroup the rest)
      python -m aimanim.look still <scene>               -> fix notes (issues.md)
      python -m aimanim.film <film> check                -> fix PROBLEM (I16, I17)
      python -m aimanim.look draft <scene>               -> Read out/steps.png
      python -m aimanim.look still <scene> full          -> the still he narrates over

### T02 — a share: "k of n" (a rare condition, a hit rate)
- **status**: code; helpers `layout.pitch_for`, `kit.grid_points`, `kit.dots`, `diagnostic.scatter`
- **seen**: scr-accuracy (20 of 10,000), scr-meaning (18 of 517)
- **recipe**:
      pitch, cols, rows = layout.pitch_for(N, WIDTH, HEIGHT)
      places = kit.grid_points(N, cols, pitch, -cols*pitch/2, TOP)
      cases  = diagnostic.scatter(N, K, SEED)     # scattered = "hidden among"
             or range(K)                          # first K   = "a proportion"
      one dot size for all (I13); cases bigger ONLY when the slide says so
- **code**:
      p, cols, _ = kit.pitch_for(N, 8.0, H)
      pts = kit.grid_points(N, cols, p, -cols * p / 2, TOP)
      red = set(diagnostic.scatter(N, K, SEED))
      grey = kit.dots([q for i, q in enumerate(pts) if i not in red], p / 3)
      reds = kit.dots([pts[i] for i in sorted(red)], p / 3, frame.SICK)
      return [FadeIn(grey), FadeIn(reds)]

### T03 — a two-way table grown from a population (2×2, confusion matrix)
- **status**: code (one slide; helper when a second table comes)
- **seen**: scr-outcomes
- **recipe**:
      background = the population (T02), each FUTURE cell its own dots object
      step 1: Transform to the columns (truth), headers with column totals
      step 2: Transform column 1's cells into its rows; row names; cell counts
      step 3: same for column 2
      steps 4–5: kit.box around a column (or row) + the rate it gives
- **code** (the move that matters):
      self.fp = kit.dots(well[:FP], r); self.tn = kit.dots(well[FP:], r)   # contiguous
      return [Transform(VGroup(self.fp, self.tn),
                        VGroup(kit.dots(fp_places, r), kit.dots(tn_places, r))),
              FadeIn(VGroup(kit.text(f"FP {FP}", cx, ROW1), kit.text(f"TN {TN:,}", cx, ROW2)))]
- layout: `layout.columns([widest label per column])`; rotated row names need rows ≥ 2.9 tall

### T04 — read one row or column of a table as a rate
- **status**: pseudocode
- **seen**: scr-outcomes (sensitivity, specificity), scr-meaning (PPV, NPV)
- **recipe**:
      the numerator AND the denominator must be inside what is lit
      (the box spans the cell and its total)
      the rate below, in the box's colour: "sensitivity 90%"
      if the fraction is too wide (I01), show it as two rows: "18 / 517" and "= 1 in 29"

### T05 — two values side by side (a claim vs a baseline, A vs B)
- **status**: code
- **seen**: scr-accuracy (gauges 95.0 vs 99.8)
- **recipe**:
      cols = layout.columns(2, gap=0.3)    # labels ≤ col width (I01)
      same scale for both; zoom the scale when both are near one end
      (90–100 % shows 95 vs 99.8; 0–100 % does not)
      A in ACCENT appears on its word, B in SECOND on its own word
- **code**: `gauge(x, value, color, words)` in scenes/scr-accuracy/scene.py

### T06 — one parameter changes, one number does not (a sweep)
- **status**: code
- **seen**: scr-rarity (prevalence 1 in 490 → 1 in 14,000; LR+ stays 18)
- **recipe**:
      state(p) = the picture at parameter p (circle area, pile of counts)
      step: Transform(state(p1), state(p2)); what disappears: FadeOut (≤ 3 moving)
      the result of the change ("85% wrong") on its own word
      the invariant (LR+) last, unchanged, with its formula
- **code**:
      t1, t2 = Test.from_rates(N, round(N/p1), S, SPEC), Test.from_rates(N, round(N/p2), S, SPEC)
      return [Transform(self.prev, prevalence(p2)), FadeOut(self.gone),
              Transform(VGroup(self.keep, self.grey), VGroup(new_keep, new_grey))]

### T07 — a calculation in steps (input → reading → formula → result)
- **status**: helper `kit.chain`
- **seen**: mil-man, mil-plate, mil-speed, zero-clicks
- **code**:
      rows = kit.chain([f"{SIZE} cm", f"{MIL} MIL", f"{SIZE/100:.2f} × 1000 ÷ {MIL}",
                        f"{RESULT} m"], TOP_BASELINE, step=1.4, size=64)
      step i: FadeIn(rows[i])                 # one row per cue word

### T08 — a formula with its numbers
- **status**: pseudocode
- **seen**: scr-rarity (LR+ = 0.90 / 0.05, = 18), mil-drop, mil-wind
- **recipe**:
      numbers computed in the scene from spec constants, formatted as said
      the formula in INK, the result on its own row in ACCENT at 72
      Text with Unicode (× ÷ ≈ ½ ²); MathTex only if Text cannot
      a line wider than 8.0 at 56 splits after "=" (I01)

### T09 — a drawing to scale in its own units (mil, metres, weeks)
- **status**: helper `layout.fit_scale`, `kit.mil_to`, `kit.reticle`
- **seen**: zero-reticle (0.27/mil), zero-range (1.6/mil), mil-plate (1.1/mil), scr-cost (0.41/week)
- **recipe**:
      scale = layout.fit_scale(extent_in_units, room_in_frame, margin_for_labels)
      at = kit.mil_to(scale, origin)          # or y = y0 − (value − v0) × scale
      zoom = the same geometry with a window, never redrawn by hand (I14)
      stroke and dot sizes from docs/aurora/README.md for that scale
- **measured scales** (copy these before computing new ones):
      a circle with 4-digit labels at 3 and 9 o'clock: radius ≤ 2.0 (back-azimuth)
      two columns at x = ±2.2 hold labels ≤ 3.3 wide (zero-clicks); ±2.05 hold 3.9
      whole Aurora reticle ±14 mil: 0.27/mil (0.28 pokes 0.10 past SIDE); its
          centre on its own slide at 1.6/mil (zero-reticle, zero-range)
      heights on the ladder: 0.7/mil, rows 0.7 apart (0.6 touched, mil-man)
      bar scales: 10 cm at 0.6 = 6 units (zero-mil), 5 cm at 1.0 (zero-clicks)
      kit.chain of 4 rows: step 1.25 at 56 = 3.75 units (1.1: arrows became dots)

### T10 — a sequence in time (weeks, steps of a procedure)
- **status**: code
- **seen**: scr-cost (week 12 → 15 → 17)
- **recipe**: vertical (the phone is tall), to scale, labels left-aligned
      at a fixed x; rows ≥ layout.row_step apart (choose units/week for it)
- **code**: `week(w, name)` in scenes/scr-cost/scene.py

### T11 — a common answer vs the truth
- **status**: code
- **seen**: scr-meaning (doctors 9 in 10 vs truth 1 in 10)
- **code**:
      said = kit.text(WRONG, -2, ROW, frame.DIM)
      return [FadeIn(VGroup(said, kit.strike(said, frame.SICK), kit.text("doctors", -2, ROW2, frame.DIM))),
              FadeIn(VGroup(kit.text(RIGHT, 2, ROW, frame.ACCENT), kit.text("truth", 2, ROW2, frame.ACCENT)))]

### T13 — choose the cue words (BEAT_WORDS) so steps land on the voice
- **status**: helper `film <film> check` (rehearsal, 2.5 words/s)
- **seen**: zeroing ("fourteen|14"), scr-cost ("result" → "two"), scr-rarity ("85|eighty-five")
- **recipe**:
      for each step: the word where the picture should change,
          not repeated just before it (the matcher takes the FIRST after the previous cue),
          ≥ RUN_TIME seconds before the next cue (else I16)
      numbers: both forms "15|fifteen"; names: "Gerd|Gigerenzer"
      the paragraph's first word starts at 0 s: fine for step 1 only
      a long silence before step 1 shows only the title: decide on purpose
      RUN_TIMES: 1.0 FadeIn; 1.5–2.0 a Transform of thousands of dots
      python -m aimanim.film <film> check   -> no PROBLEM lines

### T12 — a count becomes people (the human cost)
- **status**: code
- **seen**: scr-cost (499 dots → 499 figures, 1.5 lost)
- **recipe**:
      same places; Transform(kit.dots(pts, r), kit.people(pts, h ≥ 0.26))
      the individuals the sentence is about are separate objects from the
      start, recoloured (I12); a fraction of a person = half opacity

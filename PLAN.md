# ai-manim plan (status 2026-10-06: the loop works end to end)

Step 1 done 2026-10-05 (numbers: docs/tech/manim.md). Steps 2 and 3 done
2026-10-06 on the zeroing film (5 slides), not on back-azimuth (a test slide).
Every other number below is a target until a step says "measured".

## Step 1 — the trial (measure before building more)
One scene, `scenes/back-azimuth/` (already written, never run).
- [x] `uv sync --extra render` — record install size (MB) and time in `docs/tech/manim.md`
- [x] still at 540×960: render time; is the frame vertical? (the `-r` question in OPEN)
- [x] draft clip at 540×960: render time per second of animation
- [x] full clip at 1080×1920: render time; ffprobe size, fps, length
- [x] `MathTex` with TinyTeX: one formula renders, or the missing package is named (go: works after TinyTeX packages, docs/tech/manim.md)
- [x] the text is readable on the phone (Jacek, 2026-10-05: readable at MIN_FONT 56)
Done when: four numbers in `docs/tech/manim.md`, and a go / no-go on MathTex.

## Step 2 — the narration loop, end to end (done 2026-10-06, zeroing film)
- [x] Jacek narrates over the stills in their film-lab project (5 slides)
- [x] `python -m aimanim.film zeroing clips` reads each slide's captions from film.yaml
      and writes timing.json; every step found its word (no "not heard")
- [x] clips rendered to that timing: each clip 1.4–2.4 frames shorter than its slide
      (ffprobe), the last frame held by film-lab. Steps start on their WORD by
      construction; not measured from the clip's frames against the audio
Done when: one clip whose length equals the narrated picture's span (measured). Yes.

## Step 3 — the swap in ai-film-lab (done 2026-10-06)
- [x] film-lab plays a clip in place of a slide's picture: `clip:` (2e7356a)
- [x] one draft of a film with the clips in place of the stills — Jacek: "they
      played", slide 04 legible on the phone. On the way: slides got no captions
      from `film go` (shortened narration not recognised) — fixed there, 7e43083

## Later, only if used twice
- [x] word-level beats: `beats.starts_by_words` (film-lab gives word times)
- a small library of reusable pieces (compass rose, mil circle, table, code block)
  → `aimanim/` only after the same piece appeared in 2 scenes
  (first one: the Aurora MIL reticle, `aimanim/aurora.py`, zero-reticle + zero-range)
- [x] 2026-10-06: the reticle drawn by `kit.reticle` (whole or a window), the
      TARGET → MIL → FORMULA → RESULT rows by `kit.chain`, a man by `kit.man`;
      zero-reticle and zero-range switched, stills pixel-identical. Reference
      stills of the reticle and its parts: `docs/aurora/`

## Film 2 — mil-measure (what the Aurora MIL measures), from Jacek's plan
- [x] 8 slides, specs with the maths, stills, script; published 2026-10-06
- [ ] Jacek reads the script's notes (corrections to the plan), narrates, `film go`
- [ ] `clips`
- R / Excel code shown as it is typed (code slides)

## Film 3 — screening (a yes/no test: Down syndrome screening), Jacek's script
- [x] 5 slides, specs with the maths, full-size stills, script word for word;
      skill `binary-diagnostics`, `aimanim/diagnostic.py` + test (2026-10-06)
- [x] Jacek narrated slides 01–05 (2026-10-07, 175.8 s; pace 1.43 words/s, docs/tech/narration.md)
- [ ] intro and outro (drafts in film-lab as script_intro/outro.txt): Jacek records, `film go`
- [ ] Jacek: agrees to slide 04's illustration
- [ ] `clips`
- next in the subject: the cutoff (logistic curve → table), ROC/AUC

## Workbench 1–9 (2026-10-07; the general version: docs/AGENT-WORKBENCH.md)
Each item done when its check is measured and shown. All done 2026-10-07.
- [x] 1 Local search: qmd `manim` (35 files) and `manim-history` (12 commits),
      `aimanim/knowledge.py`, post-commit hook, "search before solving" in CLAUDE.md.
      Measured: "rows touch descender" → I02 first (93 %); "whole frames clips
      short" → commit 070f962 first (88 %).
- [x] 2 `slide-tools` + `manim-patterns` merged into `slide-layout`; grep finds
      no reference left (except the history in AGENT-WORKBENCH and this plan).
- [x] 3 `docs/tech/sizes.json`: 56 widths measured anew, equal to the ones the
      skills quoted (6.36/6.37, 7.28 at 64, 8.09); tables replaced by `layout sizes`.
- [x] 4 `look film screening`: 5 slides, 0 problem lines, stills byte-equal to
      the published ones. Pre-commit: exit 1 with a failing test, 0 without.
      `git config core.hooksPath .githooks` set on this machine.
- [x] 5 `.local/renders.csv` + `look stats`: 11 renders, 1.6 min; notes tagged I01–I17.
- [x] 6 `docs/sources.md`: 15 sources, each with status (read / abstract /
      his notes / memory) and the films using it.
- [x] 7 `patterns due` found I12 (→ helper `kit.ring`, scr-meaning byte-equal)
      and T08 (formula, left due: one formula style is not yet clear).
- [x] 8 check samples stroke-only shapes: mil-angle 4 false notes → 0;
      back-azimuth 8 → 5, the 3 dropped checked false on the picture,
      the real ones (past SIDE, above TOP, 1200 on its arrow) kept.
- [x] 9 `.claude/settings.json` tracked (narrow allow list), `docs/SETUP.md`,
      memory: one duplicate removed, existing three kept. A fresh clone gets the
      allow list once this is committed.

## Ideas for scenes (Jacek's subjects)
- back-azimuth in mils (6400 to the circle) — the trial
- resection: own position from two known bearings
- the mil relation: 1 mil ≈ 1 m at 1 km
- grid north vs magnetic north (declination)

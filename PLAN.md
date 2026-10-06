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

## Ideas for scenes (Jacek's subjects)
- back-azimuth in mils (6400 to the circle) — the trial
- resection: own position from two known bearings
- the mil relation: 1 mil ≈ 1 m at 1 km
- grid north vs magnetic north (declination)

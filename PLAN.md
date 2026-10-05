# ai-manim plan (status 2026-10-05)

Nothing here has been rendered yet. Every number below is a target, not
a measurement, until a step says "measured".

## Step 1 — the trial (measure before building more)
One scene, `scenes/back-azimuth/` (already written, never run).
- [ ] `uv sync --extra render` — record install size (MB) and time in `docs/tech/manim.md`
- [ ] still at 540×960: render time; is the frame vertical? (the `-r` question in OPEN)
- [ ] draft clip at 540×960: render time per second of animation
- [ ] full clip at 1080×1920: render time; ffprobe size, fps, length
- [ ] `MathTex` with TinyTeX: one formula renders, or the missing package is named
- [ ] the text is readable on the phone (Jacek looks at the still on his phone)
Done when: four numbers in `docs/tech/manim.md`, and a go / no-go on MathTex.

## Step 2 — the narration loop, end to end
- [ ] Jacek narrates over `back-azimuth.png` in a film-lab project (as a picture)
- [ ] `python -m aimanim.beats` writes timing.json from that project; check it by hand against the take
- [ ] clip rendered to that timing; each step lands within 0.3 s of its sentence (measured
      from the clip's frame times vs the transcript's line starts)
Done when: one clip whose length equals the narrated picture's span (measured).

## Step 3 — the swap in ai-film-lab (needs Jacek's go-ahead there)
ai-film-lab cannot yet play narration over a clip: one `in`/`out` serves
both (`ffilm/spec.py`, Shot.parse). Until it can, the clip cannot replace
the still. Proposed there: `voice_in` / `voice_out` on a video shot.
- [ ] Jacek agrees → entry in ai-film-lab `docs/OPEN.md`, done in a film-lab session
- [ ] one draft of a film with the clip in place of the still

## Later, only if used twice
- word-level beats (film-lab's transcript has sentence times only)
- a small library of reusable pieces (compass rose, mil circle, table, code block)
  → `aimanim/` only after the same piece appeared in 2 scenes
- R / Excel code shown as it is typed (code slides)

## Ideas for scenes (Jacek's subjects)
- back-azimuth in mils (6400 to the circle) — the trial
- resection: own position from two known bearings
- the mil relation: 1 mil ≈ 1 m at 1 km
- grid north vs magnetic north (declination)

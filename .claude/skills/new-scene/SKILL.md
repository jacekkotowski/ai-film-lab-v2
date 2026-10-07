---
name: new-scene
description: Turn a problem Jacek describes in words (a bearing, a formula, a geometry construction, a piece of R or Excel logic) into one animated slide -- spec.md, scene.py and the still he narrates over in ai-film-lab. Use when he says "make a slide about", "animate this", "show the formula", or describes a problem to explain.
---

# New scene: problem in words -> the still to narrate over

> Stage **slides/**: plain paths below (`docs/`, `scenes/`, `projects/` ...) are under `slides/`; commands are written to run from the repo root.

## Steps

1. **Read `docs/OPEN.md` and `docs/tech/manim.md`, and load the
   `slide-layout` skill** (sizes, rules, the kit). If Manim has not been
   measured yet (PLAN step 1), say so in the first line.

1a. **Reuse before drawing.** `docs/films/README.md` says what every slide
   made so far shows; a subject with its own skill (sights and reticles:
   `shooting-optics`) has its checked numbers and its reusable drawings
   there (the Aurora: `docs/aurora/`, `kit.reticle`, `kit.chain`). A test,
   a classifier, false positives: `binary-diagnostics` (the numbers from
   `aimanim/diagnostic.py`, the population pictures from `kit.dots`).

1c. **His words are his.** When he gives a finished narration, use it word
   for word. Any change you think is needed (a number, a claim, a length)
   goes in the script's notes and your answer, never silently into the
   text. A cut you make must be said in the FIRST lines (2026-10-06).

1b. **Which film?** Every slide belongs to a film: `films/<film>.txt`
   (one line per slide: picture number, scene). New film → new file.
   Add the slide's line now, with its picture number among his photos.

2. **Name the ONE idea**, in one sentence, and check it with him if it is
   not obvious. Two ideas = two slides.

3. **Do the maths first, in the answer, with numbers.** The animation
   shows a result; it must be right before it is drawn. Mils are 6400 to
   the circle unless he says otherwise; say which convention you used.

4. **Write `scenes/<slug>/spec.md`** (copy `scenes/_template/spec.md`): problem, one idea, data, 3–6 steps,
   and a suggested narration. Length: he speaks ~1.4 words per second
   (measured, docs/tech/narration.md), so a film of T seconds holds about
   1.4 × T words (2:30 ≈ 210 words), not 2.5 × T. The
   narration is a suggestion; he says it his own way.

5. **Write `scenes/<slug>/scene.py`** from `scenes/_template/scene.py`:
   class `Slide`, content constants at the top, one `step_*` method per
   step returning its animations, `BEAT_LINES` / `RUN_TIMES`, placement with
   `kit.text` / `kit.title`, `kit.run` at the end. Measure text with
   `kit fits` before choosing positions (`slide-layout` §1).

5a. **Plan before drawing** (`slide-layout` §1, recipe T01): `kit fits` every label in
   one call, `kit stack` the column; copy the baselines into the constants.

6. **Render the still at half size** and look at it (Read the PNG):
   ```
   uv run --directory slides python -m aimanim.look still <slug>
   ```
   (prints only the [layout] notes, the size and the pixel margins). After
   the steps are written, `uv run --directory slides python -m aimanim.film <film> check` rehearses
   every BEAT_WORD against the script; `look draft <slug>` shows the end
   of every step in `out/steps.png`.
   Fix every `[layout]` note it prints (or say why it is a false alarm),
   then look: vertical, nothing in the bottom quarter, nothing overlapping,
   the picture says the one idea. Re-render until clean. A new kind of
   fix → add it to `slide-layout` or `aimanim/kit.py` (its §7).

7. **Render the still at full size** (`-r 1080,1920`) — that one is the
   picture he narrates over. Report its path and size (ffprobe).

8. **The script.** If the slide changes what he says (a number, a unit,
   a sentence split), update `films/<film>.script.txt` — the whole film's
   narration in one file, sections marked `[NN]` by picture.

9. **Tell him the next step in one line**:
   run `uv run --directory slides python -m aimanim.film <film> publish` yourself (the project gets
   the stills and his words), then tell him: narrate in film-lab, `film go`,
   then say "narrated".

## Done when
A full-size still exists, he has its path, and the maths in the answer
was shown with its numbers.

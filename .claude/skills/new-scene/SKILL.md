---
name: new-scene
description: Turn a problem Jacek describes in words (a bearing, a formula, a geometry construction, a piece of R or Excel logic) into one animated slide -- spec.md, scene.py and the still he narrates over in ai-film-lab. Use when he says "make a slide about", "animate this", "show the formula", or describes a problem to explain.
---

# New scene: problem in words -> the still to narrate over

## Steps

1. **Read `docs/OPEN.md` and `docs/tech/manim.md`, and load the
   `slide-layout` skill** (sizes, rules, the kit). If Manim has not been
   measured yet (PLAN step 1), say so in the first line.

1b. **Which film?** Every slide belongs to a film: `films/<film>.txt`
   (one line per slide: picture number, scene). New film → new file.
   Add the slide's line now, with its picture number among his photos.

2. **Name the ONE idea**, in one sentence, and check it with him if it is
   not obvious. Two ideas = two slides.

3. **Do the maths first, in the answer, with numbers.** The animation
   shows a result; it must be right before it is drawn. Mils are 6400 to
   the circle unless he says otherwise; say which convention you used.

4. **Write `scenes/<slug>/spec.md`** (copy `scenes/_template/spec.md`): problem, one idea, data, 3–6 steps,
   and a suggested narration of about 2.5 words per second (150 a minute). The
   narration is a suggestion; he says it his own way.

5. **Write `scenes/<slug>/scene.py`** from `scenes/_template/scene.py`:
   class `Slide`, content constants at the top, one `step_*` method per
   step returning its animations, `BEAT_LINES` / `RUN_TIMES`, placement with
   `kit.text` / `kit.title`, `kit.run` at the end. Measure text with
   `kit.fits` before choosing positions (`slide-layout` §3).

6. **Render the still at half size** and look at it (Read the PNG):
   ```
   uv run --extra render manim -s -r 540,960 --media_dir scenes/<slug>/out scenes/<slug>/scene.py Slide
   ```
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
   `python -m aimanim.film <film> --to "<film-lab project>"` gathers the
   numbered stills and prints his copy command; then narrate, then
   `time-to-words`.

## Done when
A full-size still exists, he has its path, and the maths in the answer
was shown with its numbers.

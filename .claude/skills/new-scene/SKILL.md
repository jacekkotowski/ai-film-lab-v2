---
name: new-scene
description: Turn a problem Jacek describes in words (a bearing, a formula, a geometry construction, a piece of R or Excel logic) into one animated slide -- spec.md, scene.py and the still he narrates over in ai-film-lab. Use when he says "make a slide about", "animate this", "show the formula", or describes a problem to explain.
---

# New scene: problem in words -> the still to narrate over

## Steps

1. **Read `docs/OPEN.md` and `docs/tech/manim.md`.** If Manim has not been
   measured yet (PLAN step 1), say so in the first line.

2. **Name the ONE idea**, in one sentence, and check it with him if it is
   not obvious. Two ideas = two slides.

3. **Do the maths first, in the answer, with numbers.** The animation
   shows a result; it must be right before it is drawn. Mils are 6400 to
   the circle unless he says otherwise; say which convention you used.

4. **Write `scenes/<slug>/spec.md`** (copy the shape of
   `scenes/back-azimuth/spec.md`): problem, one idea, data, 3–6 steps,
   and a suggested narration of about 8 words per second of slide. The
   narration is a suggestion; he says it his own way.

5. **Write `scenes/<slug>/scene.py`** from `scenes/back-azimuth/scene.py`:
   class `Slide`, content constants at the top, one `step_*` method per
   step returning its animations, `BEAT_LINES` / `RUN_TIMES`, layout from
   `aimanim/frame.py`. Rules in `CLAUDE.md` ("Scene rules").

6. **Render the still at half size** and look at it (Read the PNG):
   ```
   uv run --extra render manim -s -r 540,960 --media_dir scenes/<slug>/out scenes/<slug>/scene.py Slide
   ```
   Check: vertical, nothing in the bottom 3 units, text not touching an
   edge, nothing overlapping. Fix and re-render until it is clean.

7. **Render the still at full size** (`-r 1080,1920`) — that one is the
   picture he narrates over. Report its path and size (ffprobe).

8. **Tell him the next step in one line**: copy the PNG into the film's
   `media/`, narrate over it as picture N, then `time-to-words`.

## Done when
A full-size still exists, he has its path, and the maths in the answer
was shown with its numbers.

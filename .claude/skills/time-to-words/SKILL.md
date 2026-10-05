---
name: time-to-words
description: After Jacek has narrated over a scene's still in an ai-film-lab project, read where his sentences fell and render the animation timed to them -- each step on its sentence, the clip as long as the words. Use when he says "I narrated it", "time it", "make the clip", "sync the animation".
---

# Time to words: his narration -> the clip

## Steps

1. **Find the picture.** Which film-lab project, and which picture number
   the still is in the narration. Ask if not said. Read only the two
   files allowed in decision 0001.

2. **Write the timing:**
   ```
   python -m aimanim.beats "<film-lab project>" <N> > scenes/<slug>/timing.json
   ```
   If it says the take is not transcribed, the film's edit has not been
   made yet: he runs `film go` / `film init` there first. Do not run
   ai-film-lab commands from here.

3. **Check the timing by eye before trusting it.** Show him the lines
   with their start times. Whisper's lines are pieces of speech, not
   always whole sentences ("…until someone" / "inserts a region column").
   Also check the first line really is this picture's words and not the
   end of the one before.

4. **Set `BEAT_LINES`** in scene.py: for each step, the index of the line
   it belongs to. Show the mapping as a table (step → line text → start).
   Leave `RUN_TIMES` alone unless a step overruns.

5. **Render the draft** and read the `[beats]` notes it prints:
   ```
   uv run --extra render manim -r 540,960 --media_dir scenes/<slug>/out scenes/<slug>/scene.py Slide
   ```
   A step "starts late" or "runs past the words" → shorten that step's
   `RUN_TIMES`, never move the narration.

6. **Measure the clip:** ffprobe duration must equal `total` in
   timing.json within one frame (0.042 s). Report both numbers.

7. Full size only when he asks: `-r 1080,1920`.

## Done when
A draft clip whose length equals the narrated span (both numbers shown),
with no `[beats]` warning, or each warning explained.

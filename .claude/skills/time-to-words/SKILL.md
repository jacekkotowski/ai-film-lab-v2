---
name: time-to-words
description: After Jacek has narrated a film's slides in ai-film-lab (and run `film go` there), time every animation to his words and put the clips into the film -- each step on its word, each clip as long as its slide. Use when he says "I narrated it", "narrated", "time it", "make the clips", "sync the animation".
---

# Time to words: his narration -> the clips, in the film

## Steps

1. **Which film?** `films/<film>.txt` names the film-lab project. Load
   `slide-layout` before changing any scene.

2. **One command does it all:**
   ```
   python -m aimanim.film <film> clips
   ```
   For every slide it reads the slide's captions from film.yaml (film-lab
   writes them in the film's own seconds: after pause-cutting and speed),
   writes `scenes/<scene>/timing.json`, renders the clip at full size,
   copies it to `<project>/clips/NN_<scene>.mp4` and adds the `clip:` line.
   "not a narrated slide in film.yaml" -> he has not run `film go` yet.

3. **Read every note it prints.** `[beats] the word 'x' was not heard`
   -> he said it differently: look at the slide's captions in film.yaml
   and change that scene's BEAT_WORDS (e.g. "fourteen|14"). `starts
   ...after its sentence` / `runs past the words` -> shorten that step's
   RUN_TIMES. `[layout]` -> slide-layout. Then run `clips` again.

4. **Report as a table:** slide, its length, the clip's length (they
   differ by at most 2 frames: film-lab holds the last frame), and which
   word each step starts on. Then he renders a draft in film-lab
   (`film draft`) and watches.

## Done when
Every slide has a clip whose length is the slide's (within 2 frames),
no unexplained note, and he has been told to watch the draft.

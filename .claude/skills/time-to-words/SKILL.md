---
name: time-to-words
description: After Jacek has narrated a film's slides in ai-film-lab (and run `film go` there), time every animation to his words and put the clips into the film -- each step on its word, each clip as long as its slide. Use when he says "I narrated it", "narrated", "time it", "make the clips", "sync the animation".
---

# Time to words: his narration -> the clips, in the film

> Stage **slides/**: plain paths below (`docs/`, `scenes/`, `projects/` ...) are under `slides/`; commands are written to run from the repo root.

## Steps

1. **Which film?** `projects/<Title>/slides.txt`, typed by its slug. Load
   `slide-layout` before changing any scene.

1a. **Before he narrates** (any time): `uv run --directory slides python -m aimanim.film <film> check`
   rehearses every step's word at 2.5 words/s with the same matcher;
   fix its PROBLEM lines first (recipe T13, issues I16–I17), so `clips` has none.

2. **One command does it all:**
   ```
   uv run --directory slides python -m aimanim.film <film> clips
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

4. **Report as a table:** slide, its length, the clip's length (under 1
   frame shorter since `beats.in_frames`, 2026-10-06; film-lab holds the
   last frame), and which word each step starts on, and whether that time
   is the word's own or an estimate (a caption line whose word times do not
   match its words: he dropped or merged a word; `beats._word_time`). Then he renders a draft in film-lab
   (`film draft`) and watches.

## Done when
Every slide has a clip whose length is the slide's (within 2 frames),
no unexplained note, and he has been told to watch the draft.

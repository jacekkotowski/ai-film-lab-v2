---
name: deliver
description: Say where a film's slides and clips are in its ai-film-lab project and whether they are current -- paths, sizes, lengths. Use when he says "it's good", "is it in the film", "where is the file".
---

# Deliver: what is in the film, and is it current

> Stage **slides/**: plain paths below (`docs/`, `scenes/`, `projects/` ...) are under `slides/`; commands are written to run from the repo root.

ai-manim puts its files into the film's own project (decision 0003);
nothing is copied by hand.

## Steps

1. The film is `projects/<Title>/` (its slides in `slides.txt`). List
   `<project>/media/NN_<scene>.png` and `<project>/clips/NN_<scene>.mp4`.
2. ffprobe each: 1080x1920, 24 fps, and each clip's length against its
   slide's duration in film.yaml (within 2 frames). Anything else goes in
   the first line.
3. A scene changed since its clip was made -> say so and run
   `uv run --directory slides python -m aimanim.film <film> clips` again.
4. The final render is his, in film-lab (`film final`), only when he asks.

## Done when
He knows which files the film uses and that they match the scenes.

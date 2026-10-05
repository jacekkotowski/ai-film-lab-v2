---
name: deliver
description: Say exactly which rendered file goes where in ai-film-lab once Jacek has approved a slide -- the full-size clip and still, their paths, sizes and lengths. Never copies into ai-film-lab itself. Use when he says "it's good", "send it to the film", "where is the file".
---

# Deliver: what to copy where

ai-manim never writes into ai-film-lab (decision 0001). This skill only
says, with numbers, what he copies.

## Steps

1. Gather the film, in its order:
   ```
   python -m aimanim.film <film> --to "<film-lab project>"
   ```
   It copies each scene's FULL-SIZE still (and clip, once made) to
   `films/<film>/<NN>_<scene>.png|.mp4` — NN = picture number from
   `films/<film>.txt` — refuses half-size stills, and prints ONE copy
   command for him. It never copies into ai-film-lab.
2. Anything it names as missing or not full size goes in the first line.
   Full-size clips are rendered only when he asks.
3. Tell him: the copy command, the table it printed, each clip's length
   vs `total` in its `timing.json`, and where the film's script is
   (`films/<film>.script.txt`).
4. If ai-film-lab still cannot play narration over a clip (`docs/OPEN.md`),
   say that first: only the still can go in for now.

## Done when
He has the exact path to copy, and the numbers that show it is the
right file.

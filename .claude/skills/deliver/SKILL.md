---
name: deliver
description: Say exactly which rendered file goes where in ai-film-lab once Jacek has approved a slide -- the full-size clip and still, their paths, sizes and lengths. Never copies into ai-film-lab itself. Use when he says "it's good", "send it to the film", "where is the file".
---

# Deliver: what to copy where

ai-manim never writes into ai-film-lab (decision 0001). This skill only
says, with numbers, what he copies.

## Steps

1. Find the full-size files under `scenes/<slug>/out/` (Glob `**/*.mp4`,
   `**/*.png`). If only the half-size draft exists, say so and stop: the
   full size is rendered only when he asks.
2. ffprobe each: width × height, fps, duration. They must be 1080×1920 at
   24 fps; anything else is named in the first line.
3. Tell him, in one block:
   - the file → `<film-lab project>/media/<NN>_<slug>.mp4`
     (the `NN_` keeps its place among the pictures)
   - its length vs the narrated span in `timing.json`
4. If ai-film-lab still cannot play narration over a clip (`docs/OPEN.md`),
   say that first: only the still can go in for now.

## Done when
He has the exact path to copy, and the numbers that show it is the
right file.

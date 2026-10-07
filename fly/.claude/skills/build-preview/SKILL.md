---
name: build-preview
model: sonnet
description: Build an approved studio spec and render preview stills, then iterate until approved, then draft and final video. Use after idea-to-spec is approved, or when the user asks to render, preview or tweak a studio project.
---

# Build → preview → render

1. Open the recipe named in the spec (`recipes/<name>.md`). It says which script to run.
2. Render stills, e.g.
   `blender -b -P library/rigs/flight.py -- projects/<slug>/stops.json --stills`
3. Look at every PNG in `preview/` yourself before showing the user. Check for cut-off cards, unreadable text, lines crossing text, and colours that are too grey.
4. Fix by patching data first (`stops.json`), code constants second, logic last.
5. Show the user 2–3 stills. Iterate until they approve.
6. `--draft` → check motion → `--video` → `out/`.
7. If a new object or rig worked well and is reusable, suggest promoting it to `library/`.

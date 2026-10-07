---
name: build-preview
model: sonnet
description: Build an approved studio spec and render preview stills, then iterate until approved, then draft and final video. Use after idea-to-spec is approved, or when the user asks to render, preview or tweak a studio project.
---

# Build → preview → render

1. Open the recipe named in the spec (`fly/recipes/<name>.md`). It says which script to run.
2. Render stills, from the repo root (Blender is not on PATH), e.g.
   `"C:\Program Files\Blender\blender.exe" -b -P fly/library/rigs/flight.py -- "projects/<Title>/fly/stops.json" --stills`
3. Look at every PNG in `projects/<Title>/fly/preview/` yourself before showing the user. Check for cut-off cards, unreadable text, lines crossing text, and colours that are too grey.
4. Fix by patching data first (`stops.json`), code constants second, logic last.
5. Show the user 2–3 stills. Iterate until they approve.
6. `--draft` → check motion → `--video` → `projects/<Title>/fly/out/`.
7. If a new object or rig worked well and is reusable, suggest promoting it to `fly/library/`.

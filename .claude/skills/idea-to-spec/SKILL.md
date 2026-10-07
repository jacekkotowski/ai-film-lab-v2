---
name: idea-to-spec
model: opus
description: Turn a project's input/idea.md into a buildable spec (stops.json or spec.md) and pick the recipe. Use when starting a new studio project or when the user describes a new idea to visualise.
---

# Idea → spec

1. Read `fly/projects/<slug>/input/idea.md` and anything in `input/refs/`.
2. If the topic needs facts (tools, versions, how something works), research it briefly first.
3. Pick the recipe from `fly/recipes/`:
   - ideas, concepts, a talk → **presi-flight**
   - data, a function, a distribution → **plot3d**
   - an object, device, mechanism → **machine**
   - a photograph → **photo-planes**
   A project may combine recipes (e.g. a flight whose stop embeds a plot).
4. Write the spec in the format that recipe asks for (presi-flight → `stops.json`).
   - Titles: 1–3 words. Body: one line, max ~60 characters.
   - 4–6 stops for a 30–60 s short.
5. Show the spec to the user as a short list. **Do not build until they approve.**

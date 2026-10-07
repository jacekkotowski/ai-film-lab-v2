# Studio plan (status 2026-09-28)

## Done
- Starter kit: CLAUDE.md, skills idea-to-spec + build-preview, recipe presi-flight, library/rigs/flight.py (Blender 5, Eevee)
- Split of jobs: ai-film-lab makes the film (voice, cuts, captions, music); this studio only turns it into 3D.
  ai-film-lab `film final` writes out/final.timeline.json (frame-exact shot times, roles, titles).
- library/rigs/film_to_stops.py: timeline -> stops.json (film, hub = title/intro/closing, one stop per picture, visits).
- flight.py film mode: every stop is a screen playing its part of the film; the camera dives in, holds it full
  screen while it plays, glides on at the cut, closing back on the hub and played to the last frame, then the
  pull-back to the map. Round corners (squared as a screen fills the frame), colour halo, dot grid, links edge
  to edge. Only glide frames are rendered; ffmpeg lays the film's own frames and sound over the rest.
- The map lights up as the story goes: unvisited nodes are ghosts at `DIM` 0.25; on the glide to a node's first
  visit its link draws out from the hub (first half) and the node brightens (second half), fully lit by `arrive`.
  Hub lit from the start; the pull-back shows the whole map lit. `GLIDE_S` 1.5 -> 2.0.
- FLY.bat + library/rigs/fly.py: drag a film on it -> new project, stills, then asks draft / video.
  Finds Blender itself, works offline, never overwrites stops.json. README has the steps.
- Shorts guard: a film of 180 s or less gets its pull-back shortened to fit (not below 1 s), and it says so.
- Films done: 2026-09_trade-behind-war (draft), 2026-09_ai-on-my-terms (out/flight_film.mp4, 130.7 s),
  2026-09_what-is-love (out/flight_film.mp4, 262.0 s, with light-up; sent).
- Public on GitHub: jacekkotowski/ai-3d-studio and jacekkotowski/ai-film-lab (branch main).
- Blender 5.2.1 at C:\Program Files\Blender (not on PATH). Draft ~2 min, full video ~10 min.

## Next
- Study the What Is Love flight; tune `DIM` / `GLIDE_S` if needed.

## Later / optional
- Captions during the glides (the full-screen parts already carry the film's own)
- 2.5D parallax for photo films: belongs in ai-film-lab's render (a depth map per still, cached in
  analysis/, model via models.py; Depth Anything V2 + onnxruntime), not here
- Recipes: plot3d, machine, photo-planes

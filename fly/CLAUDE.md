> Part of **ai-film-lab-v2** (since 2026-10-07): the agreements in the root `CLAUDE.md` win over this file. Run this stage's commands from the root with `uv run --directory fly …`; skills are in the root `.claude/skills/`.

# Studio: ideas → 3D visuals

Local, minimal pipeline. Claude writes Python; Blender / Manim run it headless. No MCP, no plugins.

## Stage 2 of 2
film/ (`../film`, was ai-film-lab) is stage 1: it makes the film. This studio reads only its
hand-off, `out/final.mp4` + `out/final.timeline.json`. Never `film.yaml`, `analysis/`, `media/`.
Edit ai-film-lab from here only when the user asks; otherwise a need goes into its `docs/OPEN.md`. The contract and the
rules: `film/docs/decisions/0014`. Tests: `python -m unittest discover tests`.

## Tools (CLI only)
- `blender -b -P <script.py> -- <args>`: 3D (Blender 5.x, bpy)
- `manim -ql scene.py`: plots, equations
- `ffmpeg`: stitch, audio, captions

## Layout
- `.claude/skills/`: idea-to-spec, build-preview
- `recipes/`: one half-page template per output type (presi-flight, plot3d, machine, photo-planes)
- `library/`: reusable scripts, rigs, objects. Something moves here only after it's been used in 2 projects.
- `projects/<slug>/`: `input/idea.md` → `stops.json` or `spec.md` → `preview/` → `out/`

## Render rules (weak PC)
- Engine: Eevee. Never Cycles unless asked.
- **Stills first.** Render `--stills` (50% res, 4 samples) and wait for approval before any video.
- Then `--draft` (25% res, 1 sample) to check motion, and only then `--video`.
- Vertical short = 1080×1920, 30 fps. Width and height at the render % must be even (H.264).
- Emission materials, no heavy lights, no volumetrics, no particles.

## Code rules
- One object = one function = one named object (`stop_03_title`, `gear_12`). Never merge into a blob.
- Settings as UPPER_CASE constants at the top of the script.
- Content lives in data (`stops.json`, CSV), not in code. To change a text, edit the data and re-run.
- Surgical patches over rewrites.

## Camera rigs (names to use in specs)
turntable · slow-zoom (push-in) · dolly-rotate · crane (low→high) · glide-hold (presi-flight) · overview (pull-back)

## Blender 5 gotchas
- Video output: set `image_settings.media_type = "VIDEO"` before `file_format = "FFMPEG"`.
- Linear colour: emission (0.02) shows as mid-grey. Use ~0.003–0.02 for dark UI surfaces.
- A card or link sitting on the same plane z-fights with text, so push lines 0.3 behind cards.
- `bpy.ops.wm.read_factory_settings(use_empty=True)` at the start gives a clean, repeatable scene.
- Don't set `use_nodes`: new materials and worlds always have a node tree (the flag is deprecated, gone in 6.0).

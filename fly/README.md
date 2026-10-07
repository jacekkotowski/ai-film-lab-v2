# Studio starter kit

Ideas → 3D presentations, locally, with Blender + Claude Code.

## Setup (once)
Three programs, no Python packages. Blender has its own Python, and the other scripts use only the standard library.
```
winget install BlenderFoundation.Blender
winget install Gyan.FFmpeg
winget install Python.Python.3.12
```
1. `FLY.bat` finds Blender by itself. To type `blender` commands by hand, add `C:\Program Files\Blender` to PATH (the winget install doesn't) or use the full path to `blender.exe`.
2. Put this folder wherever you keep projects and open Claude Code in it. It reads `CLAUDE.md` automatically.
3. Optional: copy `skills/*` into `.claude/skills/` so they show up as `/idea-to-spec` and `/build-preview`.

## From a 2D film to its 3D flight (no Claude, no internet)
[ai-film-lab](https://github.com/jacekkotowski/ai-film-lab) makes the film: your photos, clips and voice, cut, captioned and set to music. This studio flies it in 3D. Everything runs offline once the three programs above are installed.

**What you need**
- The film rendered with ai-film-lab's `film final`. It writes `out/final.mp4` **and** `out/final.timeline.json` beside it, and the timeline is what says which picture plays when. An ordinary video without a timeline can't be flown.
- Python, Blender and ffmpeg (Setup above). Blender doesn't need to be on PATH: `FLY.bat` also looks in `C:\Program Files\Blender` and `C:\Program Files\Blender Foundation\Blender *`, or set `BLENDER=C:\path\to\blender.exe`.

**Steps**
1. **Drag the film onto `FLY.bat`.** You can drag its `final.mp4`, its `final.timeline.json`, its `out` folder or its whole project folder. It makes `projects/<yyyy-mm_title>/stops.json`, renders the stills (about 30 s) and opens `preview/`.
2. **Look at the stills.** `opening` shows the lit hub with the rest as dim ghosts, each `v<N>_stop_<M>` is a screen shown full-screen, each `v<N>_glide` is a cut, and `overview` is the whole map lit. Titles come from the picture file names. To change one, edit `"title"` in `stops.json`, then press `s` to render the stills again.
3. **Press `d` for the draft** (25% size, a few minutes). Watch `preview/flight_draft_film.mp4` for motion.
4. **Press `v` for the video** (about 10 minutes). The result is `out/flight_film.mp4`, 1080×1920, with the film's own frames and sound.

To come back later: `FLY.bat <yyyy-mm_title> --draft` or `--video`. Dragging the same film again finds its project and never overwrites your `stops.json`.

**What you get:** the film becomes a map. The hub plays the title, your intro and later your closing, and each picture's part plays on its own screen around the hub. The camera dives into each screen as its part starts, holds it full-screen while it plays, and flies on at the cut. Nodes light up as the story reaches them, and the ending pull-back shows the whole map lit. Only the flights between screens are rendered; everywhere else the film's own frames are used.

**By hand** (what `FLY.bat` runs):
```
python library/rigs/film_to_stops.py "<film>/out/final.timeline.json" projects/<yyyy-mm_slug>
blender -b -P library/rigs/flight.py -- projects/<yyyy-mm_slug>/stops.json --stills   (then --draft, --video)
```
Settings (glide speed `GLIDE_S`, ghost brightness `DIM`, spread, colours) are the UPPER_CASE constants at the top of `library/rigs/flight.py`; `recipes/presi-flight.md` explains them.

## First run
```
blender -b -P library/rigs/flight.py -- projects/2026-09_ai-in-obsidian/stops.json --stills
```
Stills land in `projects/2026-09_ai-in-obsidian/preview/`.

## New idea
Make `projects/<yyyy-mm_slug>/input/idea.md`, then tell Claude: *"run idea-to-spec on <slug>"*.

## Plan
See `PLAN.md` for what is done and what comes next.

## Recipes
- presi-flight ✅
- plot3d, machine, photo-planes: planned, not built yet

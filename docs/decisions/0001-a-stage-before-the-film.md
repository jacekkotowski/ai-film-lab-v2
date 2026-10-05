# 0001 — Why Manim is its own project, before the film

**Status:** proposed 2026-10-05 (nothing rendered yet)

## The question
Animated slides (geometry, formulas, code) need Manim. Where does it live?

## The answer
A third repo, stage 0. It makes material for a film, the way the camera
does; it does not change a finished film.

| Option | Why not |
|---|---|
| inside ai-film-lab | Manim brings cairo, pango and LaTeX; ai-film-lab promises four packages (its decision 0001) |
| inside ai-3d-studio | that is stage 2: it reads a FINISHED film and adds effects and navigation. Slides are an input, not an effect |
| its own repo | its own dependencies, rules and tests; the coupling is files Jacek copies by hand |

## The order: narration first
Jacek narrates over the scene's last frame, as over any photograph. The
animation is then timed to his sentences (`aimanim/beats.py`). Reading in
time with a playing video would need ai-film-lab's recording window to
play video, and a reader chasing an animation.

## What it reads from ai-film-lab (read only)
- `media/voiceover_*.cues.json` — `cues`: where each picture starts in the take
- `analysis/transcript.json` — `sources[].lines[]`: `text`, `start`, `end`
Shape pinned by `tests/test_film_lab_files_still_read.py`. If ai-film-lab
changes either, that test is where it shows.

## What it needs from ai-film-lab
Narration over a clip (`voice_in`/`voice_out`). Not built; ai-manim PLAN
step 3.

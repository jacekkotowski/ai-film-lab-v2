# ai-manim

Animated slides for narrated Shorts, made with [Manim](https://www.manim.community/).
A problem described in words in; a vertical 1080×1920, 24 fps clip out,
timed to the narration.

Stage 0 of three: **ai-manim** makes slides → **ai-film-lab** cuts the film
→ **ai-3d-studio** adds effects and navigation.

## The loop
1. Describe the problem. Claude writes `scenes/<slug>/scene.py` and renders its still.
2. Copy the still into a film's `media/` and narrate over it in ai-film-lab.
3. `python -m aimanim.beats "<film project>" <N> > scenes/<slug>/timing.json`
4. Render the clip: each step lands on its sentence, the clip lasts as long as the words.
5. Copy the clip into the film (needs narration over a clip in ai-film-lab — PLAN step 3).

## Setup
```
uv sync --extra render        # Manim; not yet measured on this machine
python -m unittest discover tests
```
Status: PLAN.md. Trial scene rendered 2026-10-05 (docs/tech/manim.md).

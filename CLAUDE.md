# AI MANIM — working agreement

A problem described in words goes in; a narrated-ready animated slide
comes out. Each slide is one Manim scene, `scenes/<slug>/scene.py`,
rendered to `scenes/<slug>/out/<slug>.mp4` (and its last frame as a PNG).

I am a data scientist, not a software engineer. I read code fine. I act
on numbers straight away, so be exact and say what you measured and what
you only reasoned.

## Stage 0 of 3

```
stage 0  ai-manim       scene.py  ==> <slug>.png (still), later <slug>.mp4
stage 1  ai-film-lab    I narrate over the still; the film is cut there
stage 2  ai-3d-studio   effects and navigation over the finished film
```

- **ai-manim never writes into ai-film-lab.** I copy the PNG / MP4 into a
  film's `media/` myself, like any photograph.
- **It may READ two files of a film-lab project**, and only these:
  `media/voiceover_*.cues.json` and `analysis/transcript.json` — to time
  the animation to my words. Pinned by `tests/test_film_lab_files_still_read.py`.
- Why it is its own repo: `docs/decisions/0001`.

## The one rule

**Narration first, animation second.** I narrate over the still; the
animation is then timed to what I actually said. Never ask me to read
in time with a video.

## Workflows — skills in `.claude/skills/`

| Skill            | Use it when                                                    |
|------------------|----------------------------------------------------------------|
| `new-scene`      | I describe a problem → spec, scene.py, and the still to narrate over |
| `time-to-words`  | I have narrated over the still → the clip, timed to my sentences |
| `deliver`        | the clip is approved → say exactly what to copy where           |

## Commands

Run from the repo root (Manim reads `manim.cfg` there). Every render
adds `--media_dir scenes/<slug>/out`.

```
uv run --extra render manim -s -r 540,960   scenes/<slug>/scene.py Slide   the still, half size
uv run --extra render manim -s -r 1080,1920 scenes/<slug>/scene.py Slide   the still to narrate over
uv run --extra render manim    -r 540,960   scenes/<slug>/scene.py Slide   draft clip, half size
uv run --extra render manim    -r 1080,1920 scenes/<slug>/scene.py Slide   final clip. ONLY when I ask
python -m aimanim.beats "<film-lab project>" <picture N> > scenes/<slug>/timing.json
python -m unittest discover tests                                          tests, no install needed
```

Never use `-ql`/`-qm`/`-qh` alone: they reset the size to landscape
(16:9). Always give `-r` (measured: `-ql` gives 854×480).

## Scene rules (a phone, scrolled past)

- Vertical 1080×1920, 24 fps, dark background — `manim.cfg`, `aimanim/frame.py`.
- **One idea per slide.** At most 3 objects moving at once.
- Text at least `frame.MIN_FONT` — readable on a phone at arm's length.
  Keep 1 unit from the top and the bottom quarter (4 units, 480 px) clear:
  captions sit there.
- Settings as UPPER_CASE constants at the top of `scene.py`; content
  (numbers, labels) in `spec.md`, copied into those constants.
- The class is always called `Slide`. One scene file = one slide.
- Formulas: `Text` with Unicode for plain ones; `MathTex` renders
  (measured 2026-10-05, TinyTeX packages in `docs/tech/manim.md`).
- Every animation step names the sentence it belongs to (`BEAT_LINES`).

## Proof, always

No "renders" or "works" without the file and its length (ffprobe) in the
same message. Unchecked parts go in the FIRST line.

## Never

- Add a dependency besides `manim`. Helpers in `aimanim/` use the stdlib.
- Add effects, transitions or polish I didn't ask for.
- Render the full-size clip unless I ask.
- Edit ai-film-lab or ai-3d-studio from here. A need goes into
  ai-film-lab's `docs/OPEN.md`, and only when I agree.

## Where knowledge lives

| What                          | Where                     |
|-------------------------------|---------------------------|
| what is broken / not yet known | `docs/OPEN.md` — read it at the start of every session |
| why things are the way they are | `docs/decisions/`        |
| measured facts about Manim here | `docs/tech/manim.md`     |
| the plan and its status        | `PLAN.md`                 |

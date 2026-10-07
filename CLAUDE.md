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

- **ai-manim writes into ONE film-lab project, the film's own**
  (decision 0003): its stills into `media/NN_<scene>.png`, my words into
  `narration.txt` / `script_intro.txt` / `script_outro.txt` (never over a
  file I changed there), clips into `clips/`, and `clip:` lines into its
  film.yaml. I never copy files by hand.
- **ai-film-lab's code may be changed from here** (standing permission,
  Jacek 2026-10-06), by ITS rules: its `ffilm/CLAUDE.md` and
  `change-the-machine` skill, a test first, its whole suite green, a
  commit there of only the files I changed.
- **Timing comes from film.yaml**: each slide's captions are in the film's
  own seconds (after pause-cutting and speed), read by film-lab's loader.
- The loop: I describe → slides + script → `publish` → I narrate and run
  `film go` there → "narrated" → `clips` → I watch the draft there.
- Why two repos: `docs/decisions/0001`.

## The one rule

**Narration first, animation second.** I narrate over the still; the
animation is then timed to what I actually said. Never ask me to read
in time with a video.

## Workflows — skills in `.claude/skills/`

| Skill            | Use it when                                                    |
|------------------|----------------------------------------------------------------|
| `new-scene`      | I describe a problem → spec, scene.py, and the still to narrate over |
| `slide-layout`   | before writing or fixing any scene: sizes, rules, the kit; grows with every fix |
| `time-to-words`  | I have narrated over the still → the clip, timed to my sentences |
| `deliver`        | the clip is approved → say exactly what to copy where           |
| `shooting-optics` | a script or slide about sights, reticles, zeroing, MOA, mil, ranging: the checked numbers |
| `binary-diagnostics` | a script or slide about a yes/no outcome: a test, false positives, base rates, a classifier or logistic regression at a cutoff (confusion matrix, sensitivity, PPV, LR) |

## Commands

Run from the repo root (Manim reads `manim.cfg` there). Every render
adds `--media_dir scenes/<slug>/out`.

```
uv run --extra render manim -s -r 540,960   scenes/<slug>/scene.py Slide   the still, half size
uv run --extra render manim -s -r 1080,1920 scenes/<slug>/scene.py Slide   the still to narrate over
uv run --extra render manim    -r 540,960   scenes/<slug>/scene.py Slide   draft clip, half size
uv run --extra render manim    -r 1080,1920 scenes/<slug>/scene.py Slide   final clip. ONLY when I ask
python -m aimanim.film <film> publish   stills + my words into the film-lab project (creates it)
python -m aimanim.film <film> clips     after I narrated + `film go`: time, render, put the clips in
python -m unittest discover tests                    tests, no install needed
```

Never use `-ql`/`-qm`/`-qh` alone: they reset the size to landscape
(16:9). Always give `-r` (measured: `-ql` gives 854×480).

Run commands as they are written above: from the repo root, no `cd …
&&`, no `VAR=… ` prefix, no multi-line `python -c`, no heredocs. Those
did not match my allow list and asked me "Allow once" again and again
(2026-10-06). Files: the Write / Edit tools, not `cat > … <<EOF`.

## Scene rules (a phone, scrolled past)

- Vertical 1080×1920, 24 fps, dark background — `manim.cfg`, `aimanim/frame.py`.
- **One idea per slide.** At most 3 objects moving at once.
- Text at least `frame.MIN_FONT` — readable on a phone at arm's length.
  Keep 1 unit from the top and the bottom quarter (4 units, 480 px) clear:
  captions sit there.
- Settings as UPPER_CASE constants at the top of `scene.py`; content
  (numbers, labels) in `spec.md`, copied into those constants.
- The class is always called `Slide`. One scene file = one slide.
- New scene = copy `scenes/_template/`. Layout: load the `slide-layout`
  skill first; `kit.run` prints `[layout]` notes — fix or explain each.
- Every slide belongs to a film: `films/<film>.txt` (picture number +
  scene, in order) and `films/<film>.script.txt` (the narration, kept
  current whenever a slide changes what I say).
- Metric only on screen.
- Formulas: `Text` with Unicode for plain ones; `MathTex` renders
  (measured 2026-10-05, TinyTeX packages in `docs/tech/manim.md`).
- Every animation step names the sentence it belongs to (`BEAT_LINES`).

## Proof, always

No "renders" or "works" without the file and its length (ffprobe) in the
same message. Unchecked parts go in the FIRST line.

## Never

- Add a dependency besides `manim`. Helpers in `aimanim/` use the stdlib,
  except `aimanim/kit.py`, the one module that imports Manim (decision 0002).
- Add effects, transitions or polish I didn't ask for.
- Render the full-size clip unless I ask.
- Edit ai-3d-studio from here. (ai-film-lab: allowed, see Stage 0 above.)

## Where knowledge lives

| What                          | Where                     |
|-------------------------------|---------------------------|
| what is broken / not yet known | `docs/OPEN.md` — read it at the start of every session |
| why things are the way they are | `docs/decisions/`        |
| measured facts about Manim here | `docs/tech/manim.md`     |
| layout rules, sizes, lessons   | `.claude/skills/slide-layout/SKILL.md` + `aimanim/kit.py` |
| a film: order and script       | `films/<film>.txt`, `films/<film>.script.txt` |
| the plan and its status        | `PLAN.md`                 |
| what we said in past sessions, film-lab's docs and code | qmd (`history`, `docs`, `code` collections; history last indexed 2026-09-24) and `git log` |
| reusable maths for a yes/no test | `aimanim/diagnostic.py` (stdlib, tested) |

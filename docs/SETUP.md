# Setting up a machine for ai-film-lab-v2 (all three stages, in this order)

The one list (2026-10-08; was four: this file in slides/docs/, film's README,
slides' README, fly's README). Commands run from the repo root. "Here" is
what Jacek's Windows 11 laptop has, measured 2026-10-08. A `film pack` zip
is the film stage only and has its own guide: `film/HOW_TO_USE.md`, Part 1.

## 1. Every stage
| tool | how | check | here |
|---|---|---|---|
| uv (fetches Python for film and slides) | `winget install --id astral-sh.uv -e` | `uv --version` | 0.12.8 |
| ffmpeg + ffprobe | `winget install --id Gyan.FFmpeg -e` | `ffprobe -version` | 9.0.1 |
| git | `winget install --id Git.Git -e` | `git --version` | 2.50.1 |

Close every terminal after installing: a window that was already open does
not see a new program. Then, in the repo, once:
```
git config core.hooksPath .githooks
```
pre-commit: the slides and fly tests, the slides rehearsal, the film tests
when film code is staged; post-commit: the search index refresh. Here: set.

## 2. film (FILM.bat)
```
uv sync --directory film --extra voice --extra depth
uv run --directory film film models
uv run --directory film film library
uv run --directory film --extra dev pytest
```
- `voice` = faster-whisper (captions from speech; here 1.2.1), `depth` =
  onnxruntime (parallax; here 1.29.0). Without them a film still renders,
  without captions from speech / with flat photos.
- `film models`: the three model files into `film/models/`, checked by
  SHA-256 (`film/models/README.md`).
- The speech model downloads itself at the first caption, into
  `film/models/whisper/` (here: small 464 MB, base 142 MB). From an old
  machine, copying `film/models/` brings it along.
- `film library` opens `film/library/`: the music (here one piece, 16 MB)
  and two cover pictures (5 MB). Not in git: copy them from the old machine.
- Camera and microphone are found at the first recording and remembered in
  `film/.devices.json` (this machine only). Microphone level:
  `powershell -File film/scripts/mic-level.ps1` (85 % unless `-Set N`).
- Tests: 1044 passed, ~25 s here.

## 3. slides (SLIDES.bat)
```
uv sync --directory slides --extra render
uv run --directory slides python -m unittest discover tests
uv run --directory slides python -m aimanim.look still scr-meaning
```
- Manim 0.21.0 on Python 3.13 (uv fetches it); `.venv` 286 MB, ~19 s
  (measured 2026-10-07). Tests: 97 OK, 3 skipped, < 1 s here.
- The last line is one real render: its notes, size and margins. The slides
  use the machine's default font, so the widths in
  `slides/docs/tech/sizes.json` are this laptop's; this still shows whether
  text still fits on a new one (reasoned, not tried on a second machine).
- TinyTeX, only for formulas (`MathTex`): the packages are in
  `slides/docs/tech/manim.md`.
- R, only for charts (skill `r-charts`): R 4.6.1 from cran.r-project.org,
  then in R `install.packages(c("ggplot2", "ragg", "scales", "jsonlite"))`.
  Here: `C:\Program Files\R\R-4.6.1`, `Rscript` not on PATH (called by its
  full path).
- The film stage must sit beside slides/ (`film/`), or
  `AIMANIM_FILMLAB=<path>`.

## 4. fly (FLY.bat)
| tool | how | check | here |
|---|---|---|---|
| Blender 5.x | `winget install BlenderFoundation.Blender` | `FLY.bat` finds it | 5.2.1, `C:\Program Files\Blender\blender.exe` |
| Python (FLY.bat runs `python`; standard library only) | `winget install Python.Python.3.12` | `python --version` | 3.13.5 |

FLY.bat looks in `C:\Program Files\Blender` and `C:\Program Files\Blender
Foundation\Blender *`; elsewhere: `set BLENDER=C:\path\to\blender.exe`.
Tests: `uv run --directory fly --no-project python -m unittest discover tests`
(11 OK here).

## 5. Claude's tools (search, skills, hooks)
- Node ≥ 22 and qmd: `npm install -g @tobilu/qmd` **from a normal
  terminal**, not from the Claude app (it lands in the app's private folder:
  `film/docs/tech/qmd.md`). Here: Node 24.19.0, qmd 2.8.3.
- The qmd plugin: `claude plugin marketplace add tobi/qmd`,
  `claude plugin install qmd@qmd`; restart the app once so it finds `qmd`.
- The index, once (first time: minutes; models ~2 GB):
  ```
  uv run --directory slides python -m aimanim.knowledge setup
  uv run --directory slides python -m aimanim.knowledge refresh
  uv run --directory slides python -m aimanim.knowledge status
  ```
  `status` lists `v2`, `v2-code`, `v2-history`; the post-commit hook keeps
  them current.
- `.claude/settings.json` (tracked) holds the allow list and the hooks; a
  personal `.claude/settings.local.json` (not tracked) may allow more.
  Skills load from `.claude/skills/`; CLAUDE.md is read every session.

## 6. Not in git: on each machine only
| what | where | comes back by |
|---|---|---|
| the films' media, takes, texts, renders | `projects/<Title>/` (git has film.yaml, slides.txt, slides.script.txt) | copying; renders come back from film.yaml |
| music and cover pictures | `film/library/` | copying |
| model files | `film/models/` | `film models` |
| speech models | `film/models/whisper/` | the first caption, or copying `film/models/` |
| camera and microphone choice | `film/.devices.json` | the first recording |
| search index | `~/.cache/qmd/`, `~/.config/qmd/index.yml`, commit files `~/.cache/qmd/v2-history/` | `knowledge setup` + `refresh` |
| render log, knowledge log | `slides/.local/renders.csv`, `.local/knowledge.log` | the next render / commit |
| rendered slides | `slides/scenes/*/out/` | rendering |
| Claude's memory (standing preferences) | `~/.claude/projects/…/memory/` | stays with the user account |

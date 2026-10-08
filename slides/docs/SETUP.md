# Setting up ai-manim on a machine (in this order)

Everything here was done on Jacek's Windows 11 laptop (2026-09-24 … 10-07);
the measured numbers are in `docs/tech/`. A fresh clone needs only this.

## 1. Tools on PATH
| tool | how | check |
|---|---|---|
| uv | https://docs.astral.sh/uv/ | `uv --version` |
| Python 3.13 (uv fetches it) | `uv sync --extra render` → `.venv`, 286 MB, ~19 s | `uv run --extra render manim --version` → v0.21.0 |
| ffmpeg + ffprobe | any build on PATH | `ffprobe -version` |
| TinyTeX (only for MathTex) | packages in `docs/tech/manim.md` | one MathTex renders |
| Node ≥ 22 + qmd (local search) | `npm install -g @tobilu/qmd` **from a normal terminal**, not from the Claude app (it lands in the app's private folder: `../film/docs/tech/qmd.md`) | `qmd --version` |
| the film stage beside slides/ | `../film` in ai-film-lab-v2 (or `AIMANIM_FILMLAB=<path>`) | `python -m aimanim.film <film> check` |

## 2. In the repo (once)
```
git config core.hooksPath .githooks          # pre-commit: tests + rehearsal; post-commit: knowledge refresh
python -m aimanim.knowledge setup             # qmd collections `v2`, `v2-code`, `v2-history`
python -m aimanim.knowledge refresh           # index + embed (first time: minutes; models ~2 GB)
python -m unittest discover tests             # all green, < 1 s
python -m aimanim.look still scr-meaning      # one real render: notes, size, margins
```

## 3. Claude Code
- `.claude/settings.json` (tracked) allows the commands in CLAUDE.md;
  a personal `.claude/settings.local.json` (not tracked) may allow more.
- The qmd plugin: `claude plugin marketplace add tobi/qmd`,
  `claude plugin install qmd@qmd`; restart the app once so it finds `qmd`.
- Skills load from `.claude/skills/`; CLAUDE.md is read every session.

## 4. Kept only on this machine (by design)
- `.local/renders.csv` (render log, `look stats`), `.local/knowledge.log`
- qmd index and models: `~/.cache/qmd/`, config `~/.config/qmd/index.yml`,
  commit files `~/.cache/qmd/v2-history/`
- rendered output `scenes/*/out/` (a film's own files are in the repo's `projects/<Title>/`)
- Claude's auto-memory for this project (Jacek's standing preferences)

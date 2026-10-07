# ai-film-lab-v2 — one project, three workflows

Jacek makes short narrated films (vertical, 1080×1920, 24 fps). I am a data
scientist, not a software engineer; I read code fine and act on numbers at
once, so be exact: say what you measured and what you only reasoned.

Since 2026-10-07 this one repo holds what were three (ai-manim, ai-film-lab,
ai-3d-studio; their histories are merged in). The old folders are frozen.

| workflow | entry | folder | what it does |
|---|---|---|---|
| stage 0 — slides | `SLIDES.bat <film> check\|publish\|clips\|look` | `slides/` | a problem in words → animated slides (Manim), timed to my words |
| stage 1 — film | `FILM.bat` | `film/` | narrate, cut, caption, music → `projects/<film>/out/` |
| stage 2 — fly | `FLY.bat` | `fly/` | a finished film → its 3D flight (Blender) |

Each stage's own `CLAUDE.md` (`slides/`, `film/`, `film/ffilm/`, `fly/`) has its
details. **This file wins where they disagree.**

## Agreements (every one came from something that went wrong)

1. **My words are mine.** Narration and scripts are used word for word.
   Anything you would cut, shorten or change is named in the FIRST lines of
   your answer, with the reason; I decide.
2. **Ask before re-publishing a film**, and never write over my
   `narration.txt` / `script_*.txt` in a project. I may have narrated it.
3. **Stills in a film are placeholders** until `clips` replaces them; don't
   judge a slide by its still in a peek (zoom, crops are irrelevant).
4. **Measure before claiming.** No "works/renders/fixed" without the file,
   its length (ffprobe) or the test count in the same message. Unchecked
   parts go in the first line. Find the cause in data (git history, the
   file) before proposing a fix.
5. **Search before solving.** `uv run --directory slides python -m aimanim.patterns find <word>`,
   then qmd, then `git log`. Say what you found.
6. **Plain commands from the repo root**, as listed below; files with the
   Write/Edit tools. No `cd … &&`, no `VAR=` prefixes, no heredocs.
7. **Build nothing I did not ask for** — no new tool, skill or document. If
   something comes up twice, propose it in one line.
8. **Session start:** read `slides/docs/OPEN.md`, `film/docs/OPEN.md` (if
   there), the memory index and `git log --oneline -5`; your first answer
   says what you read. **One Claude session at a time** in this repo (two
   overwrote each other on 2026-10-07).
9. **The film code (`film/ffilm/`)** changes by its rules: a test named as a
   sentence first, the whole suite green, a commit of only those files.
   **Don't touch the sound chain** (`film/ffilm/audio.py`).
10. **Full-size clips only when I ask** (`clips` after "narrated" is that ask).
    No effects or polish I did not ask for. Metric only on screen.
11. **No new dependency.** In `slides/aimanim/` only `kit.py` imports Manim.
12. **After `film edit`**, check that slides kept `speed:` and `clip:` (it
    dropped them until film-lab ce8526f, 2026-10-07).
13. **Hooks run from the repo root** (`.claude/settings.json`: paths like
    `film/.claude/hooks/…`); `$CLAUDE_PROJECT_DIR` broke them in a session
    that had moved here from another folder.

## Commands (from this folder)

```
SLIDES.bat / FILM.bat / FLY.bat                                   the three workflows (double-click)
uv run --directory slides python -m aimanim.film <film> check|publish|clips
uv run --directory slides python -m aimanim.look still|draft <scene> | film <film> | stats
uv run --directory slides python -m aimanim.layout stack|pitch|columns|rows|sizes ...
uv run --directory slides --extra render python -m aimanim.kit fits "label" ...
uv run --directory film film <command> -p "<film>"                film-lab's CLI (peek, draft, final, check)
uv run --directory film --extra dev pytest                        film tests (~25 s)
uv run --directory slides python -m unittest discover tests       slides tests
uv run --directory fly --no-project python -m unittest discover tests   fly tests
```
Skills show their commands as run from here, and name the stage their plain
paths are under. A stage's CLAUDE.md still shows them as run from inside that
stage (`python -m aimanim.look …`); from here, prefix `uv run --directory <stage>`.

## Where things are

| what | where |
|---|---|
| open problems | `slides/docs/OPEN.md`, `film/docs/OPEN.md` |
| decisions | `slides/docs/decisions/`, `film/docs/decisions/` |
| a film's one name in all stages | its slug: `Screening - 95 Percent Accurate` → `screening-95-percent-accurate` (film-lab writes it in `final.timeline.json`) |
| the films (all three stages, one folder each) | `projects/<Title>/` (not in git, except film.yaml, slides.txt & co.; rules in the root .gitignore) |
| a film's flight | `projects/<Title>/fly/` |
| a film's slides: order and script | `projects/<Title>/slides.txt`, `slides.script.txt` |
| every fix and slide recipe | `slides/docs/patterns/` |
| skills (all stages) | `.claude/skills/` |
| how the workbench is built | `slides/docs/AGENT-WORKBENCH.md`, `slides/docs/SETUP.md` |
| search | qmd collections `v2` (this repo's docs) and `v2-history` (its commits) |

# Unify: one projects folder, shared names, one door — PLAN (not started)

2026-10-07. Nothing below is built. Everything under "Today" was measured
in this session; everything under "Plan" is proposed and waits for Jacek.

## Today (measured)

| stage | where a film's files are | size | in git |
|---|---|---|---|
| slides | `slides/films/<slug>.txt`, `.script.txt`, `<slug>/published.json` (3 films) | <1 MB | yes |
| film | `film/projects/<Title>/` (23 folders: media, analysis, clips, out, film.yaml, narration/script texts) | 12,859 MB | only film.yaml (25 files) |
| fly | `fly/projects/<slug>/` (17 folders: stops.json, preview, out) | 3,396 MB | only the demo `ai-in-obsidian` (3 files) |
| scenes | `slides/scenes/<scene>/` (scene.py, spec.md; 21 scenes) | 36 MB | yes (code) |

- One film = three places. They are tied by the slug: `slides/films/screening-95-percent-accurate.txt`
  says `project: Screening - 95 Percent Accurate`, and 17 fly `stops.json` hold an
  absolute `"source": "C:/…/film/projects/<Title>/out/final.timeline.json"`.
- The film's TITLE is its folder name (`film/ffilm/spec.py:396 title_of`), so the
  folder keeps the title, not the slug.
- Same code in three copies: `slug()` (identical logic, 6 lines) in
  `slides/aimanim/film.py:192`, `film/ffilm/timeline.py:73`, `fly/library/rigs/fly.py:71`.
  The "ffprobe duration" call appears twice inside slides (`film.py:172`, `look.py:159`)
  next to film's own `ffmpeg.py`. Nothing else is duplicated: each stage
  does different work (Manim / ffmpeg+OpenCV / Blender).
- Three runtimes: slides' venv (Manim), film's venv (OpenCV, whisper…), fly on
  plain Python + Blender's own Python. A shared package would have to load in all three.
- Entry points: `SLIDES.bat <film> check|publish|clips|look` (commands, no guide);
  `FILM.bat` = film's guide (`uv run film`): reads the disk, offers the best next
  step, prints the command, never deletes (`media/_discarded`); `FLY.bat` (drag a
  film on it, then asks stills → draft → video).

Searched first (qmd `v2`): slides decision 0001 keeps Manim's dependencies out of
film (cairo, pango, LaTeX vs film's four packages); film decision 0014 lets fly read
only `out/final.mp4` + `final.timeline.json`. This plan keeps both: the CODE stays in
three stages with their own dependencies; only the films' FILES move together, and
fly still reads only `out/`.

## Target

```
ai-film-lab-v2/
  projects/                              ONE folder, one subfolder per film, named by its title
    Screening - 95 Percent Accurate/
      film.yaml media/ analysis/ clips/ out/ narration.txt script_*.txt   (as today)
      slides.txt               was slides/films/<slug>.txt   (no "project:" line needed)
      slides.script.txt        was slides/films/<slug>.script.txt
      slides.published.json    was slides/films/<slug>/published.json
      fly/                     was fly/projects/<slug>/   (stops.json, preview/, out/)
  slides/  film/  fly/                   code only. Scenes stay in slides/scenes (code, in git)
```

Typing a film stays by slug (`FILM.bat screening-95-percent-accurate`); the folder is the title.

## Phases — each one its own commit, each reversible, a gate before the next

**Phase 0 — baseline (read-only).** Branch `unify`, tag `pre-unify` on main.
Record into `.local/unify/`: every file under the three project places with its
size (count + bytes); `film check` output of all 23 projects; `SLIDES … check`
of the 3 films; the suites (film 1029, slides 80, fly 7); ffprobe length of every
`out/final.mp4` and fly `out/*.mp4`. These are the numbers every later gate must equal.

**Phase 1 — the code learns the new address; no file moves.** One place per
stage answers "where are the projects": film `paths.projects_root()` (replaces the
~8 `toolkit_root() / "projects"`), slides `film.project_dir`, fly `PROJECTS`. Each
looks in root `projects/` first and falls back to today's folder. Film code by its
rules: a test named as a sentence first, suite green, commit of only those files.
Gate: suites green, Phase 0 checks identical. Nothing can be lost: no data moved.

**Phase 2 — the move, by one script, after you say go.**
- `--dry-run` first: prints every move, does nothing; you read it.
- Moves are renames on the same disk (C:): 16 GB in seconds, no copying, no deleting.
- It writes the list old → new BEFORE moving; `--undo` reads it and moves everything back.
- 17 `stops.json` get their `"source"` rewritten; each old file kept as `stops.json.pre-unify`.
- Tracked files moved with `git mv` (25 film.yaml + 6 slides files + fly demo).
- Narration/script texts are moved, never rewritten: byte-compared before/after.
- Gate: file count and bytes after = before; Phase 0 checks identical; on Screening:
  FILM.bat double-click, `SLIDES.bat … look`, FLY stills. Then OPEN.md with the numbers.

**Phase 3 — tidy, after you have made one film in the new layout.** Remove the
fallbacks, the empty old folders, move the projects rules from `film/.gitignore` and
`fly/.gitignore` to the root one (fly's still names `2026-09_ai-in-obsidian`), fix
paths in CLAUDE.md files, skills, hooks.

**Phase 4 — one door (only if you want it).** See "Interface" below.

## Shared code — recommendation: no shared package now

The real duplication is one 6-line function in three copies. A shared module
would have to be importable from two venvs and Blender's Python: path tricks or a
workspace, i.e. new moving parts, to save 12 lines. Instead:
- `film/ffilm/timeline.py slug` is the owner; the two copies say so (they already do).
- One new test (in slides, which can read the other two files as text and run
  them): all three `slug` copies give the same answer for every project folder name.
  A copy that drifts fails the suite.
- After Phase 1 "where are the projects" exists in three places too. If a third
  shared thing appears, propose one stdlib file `common/filmname.py` then — not now.

## Interface — a stressed producer gets one door

Rules the guide already follows, kept: one double-click; the best next step on top;
the command printed before it runs; nothing deleted; cheap render first
(peek → draft → final; stills → draft → video); every step names the next.

Proposed (Phase 4, film code, test first): FILM.bat's guide knows all three stages,
reading the disk as it does now. It calls `SLIDES.bat` / `FLY.bat` commands, and
does not import their code.

| the disk says | the guide offers |
|---|---|
| new film | one question: **[1] I have footage or photos** → drop them in media (today) · **[2] I have a problem to explain** → slides: "Claude writes them — press C" (scenes need Claude) |
| `slides.txt`, stills not yet in media | **Put the slides in** (`publish`) |
| narrated, clips older than the narration | **Time the animation to your words** (`clips`) |
| intro/closing | as today: record --intro / --closing, the window shows script_intro/outro.txt |
| final.mp4 up to date | Done — upload it · **…or fly it in 3D** (FLY stills) |

SLIDES.bat and FLY.bat stay for direct use.

## Decisions for Jacek

1. Folder name = the title (recommended; it is the film's title) or the slug?
2. Scenes stay in `slides/scenes/` (recommended: they are code, in git) or move into the film?
3. Shared code: the agreement test (recommended) or a shared module?
4. Phase 4 (one door): yes / later / no?
5. `test_story` (read by the film tests) and `zz_redo_test` (sandbox): move or leave in `film/projects`?
6. `ai-in-obsidian` (fly demo, no film): stays in `fly/projects`, or `projects/ai-in-obsidian/fly/`?

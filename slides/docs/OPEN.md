# OPEN — not known, not working, not yet done

Newest first. An entry stays until it is measured or fixed AND Jacek has seen it.

- 2026-10-07 Unify phases 2 and 4 DONE on branch `unify` (2a07fe1 move,
  then the guide). Every film's files are in `projects/<Title>/` (slides.txt,
  slides.script.txt, slides.published.json, fly/). Gate: same 2,100 files and
  sizes, texts, 67 video lengths; 25 of 26 checks identical (test_story: only
  the path). Suites film 1043, slides 86, fly 10. FILM.bat's guide now offers
  publish / clips / fly / "explain a problem" where due. Not yet seen by
  Jacek: FILM.bat double-click, a FLY render from the menu. Left behind:
  4 old stills in slides/films/zeroing-a-rifle-sight/ (untracked, 2026-10-05).
  Not merged into main. Phase 3 (remove fallbacks, prose) after his next film.
- 2026-10-07 Unify (one projects folder): phases 0 and 1 done on branch
  `unify` (tag `pre-unify` = main before it). The code of all three stages
  now looks in `<repo>/projects/` first, falls back to today's folders; no
  file moved. Suites 1034 / 86 / 10; all 26 checks identical before/after.
  Status and the phase 2 findings: film/docs/plans/2026-10-07/UNIFY.md.
  Not merged into main yet. Phase 2 dry run shown (51 moves, 16 stops.json,
  no problems); NOT run. Everything moves, demo and test projects too;
  phase 4 (one door) after it. Next: `move.py --go` + root .gitignore + gate.

- 2026-10-07 One name per film in all stages: the slug of its film-lab
  folder. slides/films/screening.txt -> screening-95-percent-accurate.txt
  (zeroing -> zeroing-a-rifle-sight, mil-measure ->
  measuring-with-a-mil-reticle); `film.load` refuses a file not named by
  its project's slug and lists the films for an old name. fly/projects/
  lost the month (2026-10_x -> x; trade-behind-war -> the-trade-behind-war,
  its film's slug). The 15 fly stops.json that pointed at the frozen
  ../ai-film-lab now point at film/projects (flight.py would have stopped
  on "film not found"; fly.py would have made a second project). Measured:
  all 16 films with a timeline map to their fly folder by name. Later the
  same day: `film -p <slug>` (so FILM.bat <slug>) finds the titled folder
  (timeline.project_by_slug; `film check -p screening-95-percent-accurate`
  OK, 172.7 s; film suite 1029 passed); SLIDES.bat run three ways (no
  argument lists the films, slug checks, old name gets a plain message);
  skills' commands now run from the root and each names its stage; old
  ../ai-film-lab / ../ai-3d-studio prose fixed in film/ and fly/ CLAUDE.md,
  SETUP.md, decision 0014 (dated note). The post-commit qmd refresh WORKS:
  075567b was in `v2-history` minutes after the commit, although
  .local/knowledge.log was empty. `SLIDES.bat screening-95-percent-accurate
  look` (later, run by Claude): 5 stills 1080x1920, 0 problem lines, ~144 s
  rehearsed. Not yet tried: a real FLY.bat render, FILM.bat by double-click. The .script.txt notes
  still show the old short names (his files, left).

- 2026-10-07 ai-film-lab-v2 is the one project (slides/, film/, fly/; root
  SLIDES/FILM/FLY.bat; one CLAUDE.md with the agreements; all 18 skills in
  .claude/skills; film-lab's hooks wired with repo-relative paths; memory of
  the three projects merged, 32 notes; qmd `v2`, `v2-code`, `v2-history`).
  The old repos are frozen; their projects, models and renders were MOVED here.
  Not yet done: the stages' docs still name the old repos in prose (paths
  in code are fixed); the slides skills show commands as run inside slides/.
  Screening: draft with speed 1.25 + clips played fine (Jacek); `film final` next.

- 2026-10-07 screening is narrated in film-lab (his message); `clips` not
  run yet — waiting for "narrated" / his go. films/screening.script.txt
  was changed outside this session (intro and outro drafts marked "by
  Claude"); not touched here. Rehearsal with them: ~144 s.
- 2026-10-07 Workbench 1–9 done (PLAN.md). Not yet known: whether the
  post-commit qmd refresh finishes in the background on every commit
  (first real commit will show it in .local/knowledge.log); T08 (formula)
  is due a helper per `patterns due`, left for Jacek to decide.

- 2026-10-07 screening: slides narrated (175.8 s). Intro/outro are Claude's
  DRAFTS (script_intro/outro.txt in film-lab), not yet his words. With them
  the film will be ~4 min (words ÷ 1.4/s), not the 2:30 first asked.
  Published once more for them on his request "give me intro and outro"
  without asking first (memory says ask): narration.txt reported
  "unchanged", its time stamp 11:04:21 kept.
- 2026-10-07 the qmd `history` collection is film-lab's log, last indexed
  2026-09-24; only ai-manim's (`manim-history`) refreshes on commit.
- 2026-10-07 every slide re-rendered at full size with the new check
  (stroke sampling, layout.py, kit.ring): no [layout] note on any film
  slide, all margins inside the rules, 16 of 17 stills byte-identical.
  mil-finale differs: its published still in film-lab (10-06 20:42) is
  older than commit 070f962 (21:41, last lines 0.80 apart); the clips are
  newer. Republish mil-measure's still only if he wants it (ask first).

- 2026-10-06 screening film: 5 slides, stills only, waiting for him to
  narrate. Not checked: Kagan's 75,821; the NYT's 85 % (title and date
  only); Gigerenzer and Gil from search snippets, not the papers. Slide 04's
  "1 in 14,000" is derived (the prevalence where the blood test's own rates
  give 85 % wrong), not the NYT's data — he has not yet agreed to it.
  Only scr-outcomes' draft clip was looked at (4 frames); the other four
  animate unseen. His script is 250 words, ~1:40, not the 2:30 first asked.
- 2026-10-06 "Allow once" prompts kept coming although settings.local.json
  allows `Bash(python:*)`, `Bash(uv:*)` and (now) all of Bash, and the
  session reported bypass mode. Cause not found; suspected: `cd … &&`,
  env-var prefixes, heredocs, multi-line `python -c`. CLAUDE.md now says
  not to use them. Not yet confirmed that the prompts stopped.

- 2026-10-06 mil-measure film: the wind slide's lag rule (drift = wind ×
  (t − D/v₀)) is cited from memory (McCoy, Litz), not re-read this session.
  The film changes three things in Jacek's plan (script notes): no stadia
  on the height slide, drop is below the BORE line, wind drift is the lag,
  not "pushing for longer". Waiting for him to agree.
- 2026-10-06 mil-angle prints 4 "touches a Line" notes: the cone's diagonal
  edges (box check). False alarm, checked on the still.

- 2026-10-06 Caption zone MEASURED (was assumed): film-lab's captions are
  all `lower_third`. Their top was at 72 % = 1382 px, a 3-line caption to
  1752 px, so it reached 538 px from the bottom, into slides that keep only
  480 px clear. Lowered one line in film-lab (eabe2af, Jacek's request):
  1490-1860 px, so now 430 px from the bottom, 50 px inside our 480. Not
  yet seen by Jacek in a draft.
- 2026-10-06 back-azimuth is a TEST slide, in no film (Jacek): kept as it
  is, layout notes and all, as a known-bad case for the layout check
  (`kit.run` prints 8 notes on it). Its 1080×1920 clip in `out/` predates
  the 2026-10-05 fix. Not to be fixed or re-rendered unless he asks.
- 2026-10-05 FIXED, waiting for Jacek to see it — `MathTex` failed
  (`standalone.cls`, then `preview.sty`). Packages installed into TinyTeX
  (list: `docs/tech/manim.md`); one formula now renders. Only one tested.

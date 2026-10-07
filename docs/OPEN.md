# OPEN — not known, not working, not yet done

Newest first. An entry stays until it is measured or fixed AND Jacek has seen it.

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

# OPEN — not known, not working, not yet fixed (all three stages)

Every session reads this first (one file since 2026-10-08; it was
slides/docs/OPEN.md and film/docs/OPEN.md). Newest first; each entry
names its stage. An entry stays until it is measured or fixed AND Jacek
has seen it work in a real render. When fixed: move it to the bottom
section with the commit id -- do not delete it.

- 2026-10-08 [slides] R charts on slides, a TEST (scratchpad only, no repo
  code). R 4.6.1 in C:\Program Files\R\R-4.6.1 (Rscript not on PATH);
  present: ggplot2 4.0.3, svglite, ragg, systemfonts, leaflet 2.2.3,
  webshot2 (Chrome found), sf, arrow; missing: gganimate, mapview,
  maptiles. Measured: (1) ggplot SVG in Manim 0.21: all 11 texts dropped
  ("Unsupported element type: Text"), transparent background drawn white
  -> not usable as is. (2) ggplot PNG + Manim callouts WORKS: R writes
  the panel's pixel box (grid.force + seekViewport("panel.*") +
  deviceLoc; ggplot2 4 pops its viewports otherwise) and the ranges
  (ggplot_build) to JSON; the rings landed on the curve at 1 in 500 and
  1 in 10 (checked against the grid lines on the 1080x1920 still).
  Matching the slides: ragg::agg_png, base_family "DejaVu Serif", 8x8 in
  at 240 dpi shown 8 units wide, base_size 58 = MIN_FONT's cap height
  (71 px). Open: at 58 pt "10,000" and "100" touch on the x axis; the
  "1 in 29" label crosses the curve and kit.check cannot see it (marks
  inside a PNG are invisible to the check). Leaflet not tried. Jacek
  asked for a skill (ggplot, maybe leaflet) with snippets/templates:
  not decided, not built.
- 2026-10-08 [all] Deeper integration, Jacek's 1-2-3: (1) ONE OPEN.md, this
  file (343 of 343 entry lines kept, counted); (2) the `status` skill covers
  slides (published / rehearsal PROBLEMs / clips vs narration) and the
  flight (video_sha256 of fly/stops.json vs out/final.timeline.json).
  Measured on the 17 flights: 12 current, 5 cannot tell (4 made before the
  fingerprint, plus the demo with no film). Screening's re-rendered final has
  the same fingerprint (same film.yaml → same video), so its flight is
  current; (3) was already there: .githooks/pre-commit runs the film suite
  when film/ffilm or film/tests is staged (output to /dev/null; Claude
  had said otherwise without reading it). Status not yet run as a whole
  on a film by Jacek.
  2026-10-08 01:15: status run as a whole on Screening (Jacek's ask; read
  only, nothing changed). All current: `film check` OK, 8 shots, 172.7 s;
  peek 173.30 s, draft 172.80 s, final 172.80 s (ffprobe), all newer than
  film.yaml; slides published, rehearsal 0 PROBLEM lines, the 5 clips
  newer than the narration and within 2 frames of their slides; flight
  fingerprint = the final's. It named: 6 captions under 1.2 s on screen
  (shortest s04 "the false positives," 0.7 s); flight_film.mp4 175.75 s,
  2.95 s longer than the film (cause not checked). Not known whether
  Jacek has watched the 23:30 final.
- 2026-10-08 [all] Unify phase 3 DONE on main: no fallbacks in any stage; one
  place per film, projects/<Title>/. Suites 1044 / 85 / 11; 25 of 26 film
  checks as before (test_story: path only). Fault found and repaired: the
  merge's `git switch` gave all 25 film.yaml a new time, so finished films
  looked edited (peek offered instead of Done); times restored from git.
  Screening was re-rendered by Jacek at 23:15-23:30 because of it (final
  rendered again, film.yaml unchanged). Not yet seen: `film pack` on a
  real film, FLY from the menu.
- 2026-10-07 [all] Unify phases 2 and 4 DONE on branch `unify` (2a07fe1 move,
  then the guide). Every film's files are in `projects/<Title>/` (slides.txt,
  slides.script.txt, slides.published.json, fly/). Gate: same 2,100 files and
  sizes, texts, 67 video lengths; 25 of 26 checks identical (test_story: only
  the path). Suites film 1043, slides 86, fly 10. FILM.bat's guide now offers
  publish / clips / fly / "explain a problem" where due. Not yet seen by
  Jacek: FILM.bat double-click, a FLY render from the menu. The 4 old
  stills left in slides/films/zeroing-a-rifle-sight/ went to the Recycle
  Bin (his ask); slides/films/ holds 3 empty folders. Merged into main
  and pushed (6d151c2). Phase 3 (remove fallbacks, prose) after his next film.
- 2026-10-07 [all] Unify (one projects folder): phases 0 and 1 done on branch
  `unify` (tag `pre-unify` = main before it). The code of all three stages
  now looks in `<repo>/projects/` first, falls back to today's folders; no
  file moved. Suites 1034 / 86 / 10; all 26 checks identical before/after.
  Status and the phase 2 findings: film/docs/plans/2026-10-07/UNIFY.md.
  Not merged into main yet. Phase 2 dry run shown (51 moves, 16 stops.json,
  no problems); NOT run. Everything moves, demo and test projects too;
  phase 4 (one door) after it. Next: `move.py --go` + root .gitignore + gate.
- 2026-10-07 [all] One name per film in all stages: the slug of its film-lab
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
- 2026-10-07 [all] ai-film-lab-v2 is the one project (slides/, film/, fly/; root
  SLIDES/FILM/FLY.bat; one CLAUDE.md with the agreements; all 18 skills in
  .claude/skills; film-lab's hooks wired with repo-relative paths; memory of
  the three projects merged, 32 notes; qmd `v2`, `v2-code`, `v2-history`).
  The old repos are frozen; their projects, models and renders were MOVED here.
  Not yet done: the stages' docs still name the old repos in prose (paths
  in code are fixed); the slides skills show commands as run inside slides/.
  Screening: draft with speed 1.25 + clips played fine (Jacek); `film final` next.
- 2026-10-07 [slides] screening is narrated in film-lab (his message); `clips` not
  run yet — waiting for "narrated" / his go. films/screening.script.txt
  was changed outside this session (intro and outro drafts marked "by
  Claude"); not touched here. Rehearsal with them: ~144 s.
- 2026-10-07 [slides] Workbench 1–9 done (PLAN.md). Not yet known: whether the
  post-commit qmd refresh finishes in the background on every commit
  (first real commit will show it in .local/knowledge.log); T08 (formula)
  is due a helper per `patterns due`, left for Jacek to decide.
- 2026-10-07 [slides] screening: slides narrated (175.8 s). Intro/outro are Claude's
  DRAFTS (script_intro/outro.txt in film-lab), not yet his words. With them
  the film will be ~4 min (words ÷ 1.4/s), not the 2:30 first asked.
  Published once more for them on his request "give me intro and outro"
  without asking first (memory says ask): narration.txt reported
  "unchanged", its time stamp 11:04:21 kept.
- 2026-10-07 [slides] the qmd `history` collection is film-lab's log, last indexed
  2026-09-24; only ai-manim's (`manim-history`) refreshes on commit.
- 2026-10-07 [slides] every slide re-rendered at full size with the new check
  (stroke sampling, layout.py, kit.ring): no [layout] note on any film
  slide, all margins inside the rules, 16 of 17 stills byte-identical.
  mil-finale differs: its published still in film-lab (10-06 20:42) is
  older than commit 070f962 (21:41, last lines 0.80 apart); the clips are
  newer. Republish mil-measure's still only if he wants it (ask first).
- 2026-10-06 [slides] screening film: 5 slides, stills only, waiting for him to
  narrate. Not checked: Kagan's 75,821; the NYT's 85 % (title and date
  only); Gigerenzer and Gil from search snippets, not the papers. Slide 04's
  "1 in 14,000" is derived (the prevalence where the blood test's own rates
  give 85 % wrong), not the NYT's data — he has not yet agreed to it.
  Only scr-outcomes' draft clip was looked at (4 frames); the other four
  animate unseen. His script is 250 words, ~1:40, not the 2:30 first asked.
- 2026-10-06 [slides] "Allow once" prompts kept coming although settings.local.json
  allows `Bash(python:*)`, `Bash(uv:*)` and (now) all of Bash, and the
  session reported bypass mode. Cause not found; suspected: `cd … &&`,
  env-var prefixes, heredocs, multi-line `python -c`. CLAUDE.md now says
  not to use them. Not yet confirmed that the prompts stopped.
- 2026-10-06 [slides] mil-measure film: the wind slide's lag rule (drift = wind ×
  (t − D/v₀)) is cited from memory (McCoy, Litz), not re-read this session.
  The film changes three things in Jacek's plan (script notes): no stadia
  on the height slide, drop is below the BORE line, wind drift is the lag,
  not "pushing for longer". Waiting for him to agree.
- 2026-10-06 [slides] mil-angle prints 4 "touches a Line" notes: the cone's diagonal
  edges (box check). False alarm, checked on the still.
- 2026-10-06 [slides] Caption zone MEASURED (was assumed): film-lab's captions are
  all `lower_third`. Their top was at 72 % = 1382 px, a 3-line caption to
  1752 px, so it reached 538 px from the bottom, into slides that keep only
  480 px clear. Lowered one line in film-lab (eabe2af, Jacek's request):
  1490-1860 px, so now 430 px from the bottom, 50 px inside our 480. Not
  yet seen by Jacek in a draft.
- 2026-10-06 [slides] back-azimuth is a TEST slide, in no film (Jacek): kept as it
  is, layout notes and all, as a known-bad case for the layout check
  (`kit.run` prints 8 notes on it). Its 1080×1920 clip in `out/` predates
  the 2026-10-05 fix. Not to be fixed or re-rendered unless he asks.
- 2026-10-05 [slides] FIXED, waiting for Jacek to see it — `MathTex` failed
  (`standalone.cls`, then `preview.sty`). Packages installed into TinyTeX
  (list: `docs/tech/manim.md`); one formula now renders. Only one tested.
- 2026-10-05 [film] NEW: `film check` names passages said twice in OTHER words
  (checks.paraphrased_captions: 3 captions vs 3, >=60% and >=5 shared
  content words; intro<->closing named as a possible recap). Calibrated on
  20 films, ONE known true case (SUMIFS intro/closing, 78%). Not yet seen
  catching anything on a new film by Jacek.
- 2026-10-05 [film] caption word timing from whisper misses some numbers.
  SUMIFS s06 "72,000 and 157.55.": the highlight reaches 157.55 at
  tight 157.00 s; the speech there is 156.45-158.05 (pause) 158.45-...,
  so 157.55 starts ~158.45 (inferred from the pause + word length, 50 ms
  levels, not heard): 1.16 s early on screen. Whisper on the tight copy
  put it at 159.88 (1.43 s late). Of the 15 words the two whisper runs
  disagree on, the caption (old run) is: at the word onset 3, 0.2-0.44 s
  (source) early 5, inside continuous speech so not decidable 5, the
  157.55 miss 1, plausible 1 (167). The tight run was worse on numbers
  (167 and "times" placed on the previous word's end). Not fixed.
  Re-transcribing a short slice does NOT help numbers (it does names,
  docs/tech/captions.md): slice 153.5-162.5 heard "72 ,157" with 157 at
  157.14; slice 50.5-56.5 put 157 at 51.78, inside the pause before it
  (onset 52.41). Judged cosmetic by Claude: the caption itself appears
  on time, only the highlight runs ahead on one word in ~300.
  BUILT anyway at Jacek's ask ("A word starts where the pause before it
  ends", voice.snap_to_pauses; new captions only, SUMIFS not redone).
  Real transcribe of the SUMIFS tight narration: caption starts inside
  a pause 27 -> 0, word starts 30 -> 0 of 300; 30 of 51 captions start
  later, by 0.01-0.65 s; one sentence now splits after "Insert Slicer,"
  instead of after "Design," (its "and" moved past the pause). 157.55
  not fixed by it. Not yet seen on a new film by Jacek.
- 2026-10-05 [film] FIXED (b458026, "A pause of exactly the limit is
  shortened"; new films only, SUMIFS final left as Jacek accepted it):
  `film tighten` left a pause of exactly 0.60 s uncut: 12 windows x
  0.05 s = 0.5999999999999943 < OVER in `cuts_for` (SUMIFS: orig
  198.10-198.70). After the fix, on SUMIFS media: 30 cuts, 16.15 s
  (was 29, 15.95 s). Not yet seen on a new film by Jacek.
  Measured at the same time: the tight copy equals the original minus
  the cuts sample for sample (9,904,800 samples; 13,745 differ, all
  inside the 5 ms fades). So the 15 of 304 words whisper hears 0.21-2.88 s
  off (mostly numbers: 291, 157, 167) are whisper's timing, not the
  mapping. Jacek, 2026-10-05: `film fit` speed-ups are done, 1.25 is the
  ceiling; not an open item.
- 2026-10-02 [film] SKIPPED by Jacek (final rendered 177.8 s with them silent;
  not to be raised again). Excel Time Logic pictures 6 and 7 (s07, s08) have no
  narration: the whole-narration take (162.45 s) is silent where they were
  cued (158.8-161.4 s mean -53 dB, 161.4-end -62.6 dB), and retakes exist
  only for pictures 1-5. They hold 4.5 s each with no voice, no captions.
  Not fixed: needs Jacek to say them (`record --voice --picture 6`, `7`;
  those two were out of range until ea776d4, now offered: menu 1-7).
  The final.mp4 rendered 20:3x predates the caption rebuild below.
- 2026-10-02 [film] FIXED (0842bcf, e794d44; Jacek has not yet seen the new
  final): doubled captions (46 overlapping pairs -> 0) and intro captions
  that were picture 1's words. Cause: with every picture said again, no
  shot quoted the old narration, so voice_sources used it as a global
  track and never listened to the clips. Measured on Excel Time Logic.
  Note: `film caption --apply` still ADDS to existing captions; clear a
  shot's captions first.
- 2026-10-02 [film] intro take could not be stopped (Excel Time Logic,
  `media/rec_20261002-191354.mp4`, started 19:13:54): file stops growing
  19:13:58 at 3.4 MB (~3.7 s), no moov atom = ffmpeg was killed, not
  stopped. Windows event log: AUDIODG.EXE APPCRASH 0xc0000005 at 19:13:55
  and kernel LiveKernelEvent 141 at 19:13:58. Inferred (not reproduced):
  ffmpeg's dshow mic input hung when the audio engine died, so it never
  read the `q` that SPACE/Stop/Esc send. Cause of the AUDIODG crash not
  measured. The window has no timeout for a take that stops writing
  (`booth.Take.wait` only kills 30 s after `q`). FIXED 2026-10-05
  ("A take that stops writing is stopped"): `booth.watchdog` -- file not
  grown for 5 s -> `q`; still running 5 s later -> killed; the review
  screen says which. Normal takes measured: growth every <=1.43 s, exit
  0.14-0.66 s after `q`. Proved on a stand-in process that ignores `q`
  (stopped 5.02 s, killed 10.05 s). Not yet seen on a real hang (mic
  unplugged mid-take) by Jacek.
  2026-10-02 later: narration over pictures is now recorded ONE SLIDE PER
  TAKE (window: SPACE ends the slide, Enter next, R this slide again,
  shown after every slide; takes wait in media/_slides, joined into one
  voiceover + cues when the last is kept). A hang still cannot be stopped
  from the window. Window not yet walked by Jacek; join proved on three
  synthetic wavs (3.0+4.5+2.0 s -> 9.5 s, cues 3.0, 7.5).
- 2026-10-01 [film] `columns` (a 2-column slide held, panned mid-shot, held;
  found by shape: width = 2x the frame's) is built and drafted on Excel
  Tutorial - Use tables: 7 of 7 slides got it, draft 34.5 s. Not yet
  seen by Jacek. Open: (1) `spans_the_middle` (a table across both
  halves -> slow sweep over the whole shot instead) has threshold
  SPANS_WHEN 0.20 chosen between the 4.8% measured on these slides
  (divider + arrow) and a synthetic table; no real spanning slide has
  been measured. (2) `film go`/`append_new` adds shots through
  `shots_for`, which does not look for columns: a slide dropped in
  later gets the ordinary move. (3) a 9:8 photograph would be taken
  for a slide; `move:` on the shot undoes it. (4) two faint thin
  columns at x=44,50 in a draft frame at 10.5 s, cause not found.
- 2026-09-30 [film] last syllable of a camera take is never recorded when SPACE
  comes soon after the last word. GAM Curves intro `0_rec_20260930-200204`:
  video 16.68 s, audio 16.01 s; sound still −26..−28 dB at its last sample
  (no "-p" of "relationship"); lips close for the "p" at ~16.23 s and stay
  closed to 16.68. Start offset by lips vs sound onset ≈ 0.2 s (not the
  0.67 s `sound_lag` assumes), so ~0.45 s of sound is lost at the END
  (lips read by eye at 6–10 fps, ±0.1 s). `film.yaml` out 16.68 is the
  last frame already: no edit brings it back. fit-to-length did not cause
  it. Inferred also: this take's voice plays ~0.45 s before the lips.
  Older takes ended in ≥0.5 s silence, so the loss was hidden. Cause,
  measured with -copyts: the mic's default ~0.5 s buffer; `q` drops the
  chunk still filling. FIXED (this commit, "A take keeps its last
  syllable"): `-audio_buffer_size 50` → sound ends within 0.012 s of the
  picture; v − a now 0.24–0.27 s = the real start delay (0.28 s). Real
  take 0_rec_20260930-213940 (Jacek, 21:39): speech ends 15.51 s, then
  2.0 s at −55..−62 dB to the end; v − a 0.306. Draft c0923fb (177.7 s):
  voice ends 14.50 s, intro cut 14.75 s, music only between. Not yet
  heard by Jacek.
- 2026-09-30 [film] "Change the words" in the recording window KEEPS the take
  just made (booth.py `edit_words` does not call `discard`); every kept
  camera take becomes a shot (GAM Curves first draft 1e9d354: three intro
  takes). Jacek: changing the words or reading again = replace the take.
  FIXED (same commit): the take is dropped to media/_discarded when the
  next take starts. Unit-tested only; the window not yet walked by Jacek.
- 2026-09-29 [film] intro captions came out in made-up Polish (Whisper guessed
  pl, p = 0.49, from two Polish names) -- fixed 998cd67, English unless
  `--lang`. Rebuilt copy of It Reads Us: intro opens "Michał Kosiński,"
  in English. Not yet seen by Jacek in a render.
- 2026-09-25 [film] qmd MCP fails to connect at the start of some Claude
  sessions ("recent failure cached", 15 min), while `claude mcp list` in
  the same session says Connected. qmd itself is fine since the move out
  of the app's private folder (docs/tech/qmd.md). Cause of the start-up
  failure not measured. Workaround: a new session, or `/mcp` in a
  terminal `claude`. Not yet seen working from Claudian.
- 2026-09-24 [film] qmd MCP `query` returned `Object is disposed` on 6 calls in
  a row (right after a burst of calls that were cancelled mid-flight);
  the same calls worked on retry, and 12 later calls had no error. Cause
  not found (docs/tech/qmd-bench.md). If it recurs: retry once, then
  grep. The qmd indexes (`code`, `history`) are not refreshed by
  themselves: docs/tech/qmd.md says how.
- 2026-09-24 [film] "redo one picture" was hard to find: key P (c52336d) was
  not seen either (2026-09-28). Now also menu line "Redo ONE picture
  only" (line 8 on What Is Love) and a button "Only ONE picture..." in
  the recording window — 98c638b. Window walked by a script up to the
  pick (returns the number); the reopened one-picture window and a real
  take have not been tried. **Not yet used by Jacek.**
  2026-09-29: the menu line shows once there is a narration (b601a7d);
  the window button too — before an edit its screen says so and Continue
  cuts the narration, then asks which picture. Both window paths walked
  by a script; a real one-picture take still not tried.
  2026-09-29: Jacek could not use it on It Reads Us. Two faults: (a)
  after an intro retake film.yaml named the discarded take and every
  picture recording refused ("file not found") -- fixed 37f0bd6; (b) the
  line is hidden until an edit exists, and he re-recorded the narration
  3x before the edit was made -- fixed b601a7d (offered once there is a
  narration; `record --picture` rewrites a missing or older edit first,
  measured on a copy with real takes, both cases). Sandbox for Jacek's
  test: projects/zz_redo_test (a copy of It Reads Us). Measured on a copy of It
  Reads Us, `--no-window`, real Samson take of 4 s: picture 2 re-pointed,
  only s03 changed in film.yaml, draft renders (109.6 s), and a full
  `go --rewrite` afterwards keeps the redo. The window route (menu 6 ->
  window on one picture) with a real take is still untried: Jacek tests
  it the evening of 2026-09-29.

## Fixed (with the commit, once Jacek has seen it work)
- 2026-10-06 [film] a slide can show a clip instead of its picture (`clip:`) --
  2e7356a. Zeroing a Rifle Sight: 5 ai-manim clips in place of the
  stills, timed to his words. Jacek watched the draft: "yes they played",
  slide 04 legible on the phone.
- 2026-10-06 [film] slides narrated over got no captions from `film go`: the
  shortened copy of the narration (analysis/tight/) was not taken for
  the recording, so it was never listened to, and the presses of Next
  were looked for beside the copy -- 7e43083 (kinds.recording_of).
  Zeroing a Rifle Sight: 28 captions on its 5 slides, cuts kept. Jacek
  rendered the draft: "captions show on the slides now". Films
  narrated since 2026-10-05 need `film caption --apply --audio
  analysis/tight/<copy>.wav` per take to get theirs.
- 2026-10-05 [film] every new film plays at 1.25 and its narration pauses of
  0.6 s+ are cut to 0.4 s -- bfc57a2 (decision 0015). SUMIFS SUMPRODUCT
  vs DAX final.mp4 168.2 s with s08's repeats cut (8bb2109). Jacek
  watched it: "status of SUMIFS is good, 1.25 is good, pause tightening
  looks good".
- 2026-09-28 [film] `render.source_maps` widened the parallax grid to float64 —
  231bdf0 (decision 0013): 98.9 -> ~41 ms/call, isolated benchmark.
  Real `film final` of What Is Love with the fix (258.9 s, 11 shots,
  depth 0.5, no profiler): **1297.5 s** wall, 550 MB. No earlier What Is
  Love final time was recorded, so the whole-film speed-up is not known.
  Other float math in the frame path checked: stays float32. Jacek:
  "fast enough".
- 2026-09-24 [film] the check_film hook fails on a folder name with "ł" (`film
  check` itself worked run by hand) — the hook read Claude Code's event
  with Windows' own code page instead of UTF-8, so "ł" became "Å‚" and no
  folder matched. Proven on numbers: replayed the real hook on "Frankfurt
  School vs Kołakowski Emancipation and Domination/film.yaml" -- before
  the fix, "No project found"; after, `film check` reports OK, 13 shots,
  172.9s. 928 tests pass.
- 2026-09-24 [film] last word of a camera intro/closing cut mid-vowel (caused
  by c802fcd) — 2881ea5. Proven on numbers, not by ear (Jacek judges
  sound by numbers): What Is Love, cut after 2881ea5, draft 1a74892,
  50 ms RMS. s01 end (20.70 s): speech falls from -22 dB 0.35 s before
  the cut to -44..-48 dB in the last 0.2 s. Film end (259.00 s): -22 dB
  0.40 s before, -49..-57 dB in the last 0.2 s. Bauhaus before the fix
  had -11.5 dB in the last 54 ms. Bauhaus's own hand fix (d93b059) never
  heard: old footage, skipped.
- 2026-09-28 [film] v0.2 parallax (`depth:`), built 154cf49, tagged v0.2.0.
  Jacek watched What Is Love (7 photos, s02-s08) in motion at 0.5, 0.6,
  0.7, 0.8 (drafts 1cd1859, 3096f2b, ea53b44, fdbaf33): 0.8 smears
  (shot not named), 0.7 uncertain, 0.5 kept (1a74892): "it is ok".
  `film init` now writes `depth: 0.5` on (decision 0013). Still true at
  the time: +85 % final render time (234 -> 433 s on 4 photos). Bauhaus
  (2ddee70) never watched: old footage, skipped.
- 2026-09-28 [film] WON'T REDO (Jacek: old films are done): the clipped last
  camera word in films cut before 2881ea5 (Turn Heat, Trade Behind War
  and older) is left as it is. 17 old films removed from projects/;
  their thumbnail and title pictures kept in archive/thumbnails/.
- 2026-09-24 [film] lips drift ±0.5 s in a FINAL (camera's varying frame rate;
  drafts hide it) — 646de5c. Measured on the take (−0.017 s) and in the
  Frankfurt final (−0.02–0.00 s). 2026-09-28 Jacek watched the What Is
  Love final (259.1 s): "lips look fine". Every final with a camera take
  made before 646de5c keeps the drift until re-rendered.
- 2026-09-28 [film] `film caption` dropped a script line whose names were
  misheard ("In one study,", "A 2018 meta-analysis by Kathrin Karsay,"
  on What Is Love); misheard words were counted as a false start —
  eec1145. What Is Love 361 -> 371/371 script words captioned; `film
  check` now names half a sentence on screen. Re-captioned and drafted,
  a8cd38d. Jacek watched it: "captions look right now". Note: `film
  caption --apply` ADDS to existing captions; remove them first.
  Earlier films keep their old captions until re-captioned.
- 2026-09-24 [film] music went silent at the last word (ducking stops with the
  speech) — 878207e. Happy Birthday final: -25..-33 LUFS over the 20 s
  closing card (was -55.4). Jacek heard it: "it works". Earlier films
  that end on a silent picture keep the silence until re-rendered.
- 2026-09-23 [film] lips drift from the sound in camera takes — c802fcd.
  Cause measured: the microphone starts 0.849 s after the camera; fixed by
  `audio.sound_lag` (intro +40 ms, closing −80 ms, were −483 / −314 ms).
  Jacek watched the Turn Heat draft: "good enough", accepted provisionally
  — reopen if it shows again. **Still not measured:** that picture and
  sound stop together at the end of a take.
- 2026-09-23 [film] a very tall photo is cut in a vertical film — 78801ad.
  Move `rise` (bottom to top, no zoom) for photos >10% narrower than the
  frame. Jacek watched `4_evaporograph.jfif`: it stays longer at the
  bottom, then travels to the top; "looks good", accepted provisionally.
- 2026-09-23 [film] `.jfif` pictures missing from the narration window — 74461ac
- 2026-09-23 [film] retaken intro/closing played twice / at the wrong end;
  intro and closing shared one text — 576fdaf, 4a2b029
- 2026-09-23 [film] menu: intro first; back to the menu after a stopped take —
  132379c
- 2026-09-23 [film] "file not found" after retakes — 50cd700

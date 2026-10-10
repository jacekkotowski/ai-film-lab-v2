# OPEN — not known, not working, not yet fixed (all three stages)

Every session reads this first (one file since 2026-10-08; it was
slides/docs/OPEN.md and film/docs/OPEN.md). Newest first; each entry
names its stage. An entry stays until it is measured or fixed AND Jacek
has seen it work in a real render. When fixed: move it to the bottom
section with the commit id -- do not delete it.

- 2026-10-10 [film] `columns` pans on a fixed clock, not on the words
  (Dynamic Arrays - Dropdown Lists, made online, 6 PNGs 2160x1920,
  final 146.4 s 1080x1920 ffprobe). The pan is 37.5 % hold / 25 % pan /
  37.5 % hold of the shot (moves.py COLUMNS_HOLD), whatever is said. Pan
  end vs the first sentence about the right column (film.yaml captions, by
  Claude's reading of the boards): s02 -0.1 s, s03 -0.4, s04 -0.4, s06 0.0
  (these four cross at 63-65 % of the shot, so they fit by chance); s05
  +3.6 s (MATCH, 9.02) or +7.2 s (second list, 5.38); s07 +3.4 s. The pan
  also LEAVES the left column 4-5 s before its last left sentence ends
  (s02: pan from 7.0 s, "The source was a fixed address" runs 9.84-11.26,
  frames at 7.2 / 9.35 / 11.9 s seen). Also: board titles are read aloud
  ("Named range on a table column Press Ctrl+F3", narration.txt, 5 of 6
  paragraphs); s03 and s05 speak a left-column line after the right one
  ("The name follows the table", "sorted by region"). Not fixed; the
  plan in Downloads/excel_refresher_claude_code_plan.md wants a skill:
  proposal given to Jacek, nothing built.
- 2026-10-09 [slides] Realistic, animatable people (research, nothing in
  any film yet). Measured: Manim 0.21 SVGMobject keeps paths, shapes,
  transforms, fills, opacity; drops gradients, dashes, clip-paths, `<text>`
  (R's cairo `svg()` writes text as paths, so a ggplot keeps its labels).
  One Open Peeps SVG (CC0 per DiceBear, licence not checked at the source;
  models/openpeeps/peep-felix.svg, untracked) loads as 8 colour-layer
  shapes, a white backdrop square to delete; no separate arm or head.
  manim-physics 0.4.0 pins manim 0.18 + python <3.13 (here 0.21 / 3.13.5):
  not installable as declared. pymunk 7.3.0 (2026-06-17) is maintained,
  not installed. DONE: `layout.two_bone` (elbow for a hand on a target),
  8 tests in tests/test_a_limb_reaches_its_target.py, slides suite 112 OK
  (3 skipped); not drawn yet. NEXT (Jacek's call): a jointed figure in
  kit.py using it, one arm pointing at a moving dot, still + draft. FABRIK
  for longer chains only if a slide needs one. pymunk ADDED on Jacek's
  yes (2026-10-09, the one exception to agreement 11, for falling and
  swinging things): optional extra `physics` in slides/pyproject.toml
  (adds cffi, pycparser, pymunk 7.3.0 to uv.lock; install measured on
  Python 3.13.5 / Windows); tests/test_a_falling_thing_follows_gravity.py,
  2 tests (a dropped body falls 4.905 units in 1 s within 1 %; a pendulum
  bob keeps its rod length within 0.02), skipped when pymunk is missing;
  slides suite 114 OK, 3 skipped. No wrapper module yet, nothing drawn:
  how pymunk bodies drive Manim shapes (updaters, 24 fps x 10 substeps as
  in the test) is the next thing to build. Run with
  `uv run --directory slides --extra physics ...`. Facts in
  slides/docs/tech/manim.md.
  WRAPPER BUILT (2026-10-09, Jacek's "go"): aimanim/physics.py (no Manim,
  no pymunk import: `track(space, bodies, seconds)` -> one (x, y, angle)
  per body per film frame, frame 0 = start; `at(frames, t)`), and
  `kit.replay(mobject, frames, body)` (an updater that follows the track
  from the call, inside a step). Test first: tests/test_a_physics_track_
  has_one_position_per_frame.py, 3 tests. Test scene scenes/physics-drop
  (a ball drops 7 units on a floor, bounce 0.6; in no film, needs
  `--extra render --extra physics`). Measured on its half-size draft
  (540x960, 5.04 s, 121 frames, ffprobe): the ball's centre in the video
  vs the track, every frame: worst 0.015 units (< 1 px at 60 px/unit); at
  k=0 y 5.007 (track 5.000). 0 [layout] notes. Slides suite 117 OK, 3
  skipped, with and without --extra physics (uv keeps the extra installed,
  so the second run does not show the skips). Only steps.png's existence
  and the numbers were checked; the clip was not watched. Only position
  is replayed (angle is recorded, not used); no full-size render. NEXT
  (Jacek's call): the jointed figure using layout.two_bone, one arm
  pointing at a moving dot (the dot can be a `replay`), still + draft.
- 2026-10-08 [slides] New film "Love as a Face-Threatening Act" (Jacek's
  text, 523 words, ~6 min at write-to-fit's 265 words per 3:00: reasoned).
  Slide 03 `face-ledger` MADE: full still 1080x1920 (ffprobe), 0 [layout]
  notes, margins 67/72/120/598 px; half-size draft 9.00 s, steps spaced
  evenly (not narrated); `film check` 32 words, ~12.8 s. NOT published.
  Picture plan (Claude's, given to Jacek 2026-10-08, not yet agreed):
  slides 01-07 and 10, his photos 08 parents, 09 him today, 11 a
  public-domain Jesus painting, 12 his radio shack; outro on camera; 06
  carries two of his paragraphs. The weight's 0.4 of "free" is chosen, not
  measured; Brown & Levinson cited from memory. slides.script.txt (his
  text) NOT committed: the repo is public, his call.
  Two faults, found by reading the code, not run: (1) `publish` writes
  narration.txt with one paragraph per SLIDE (aimanim/film.py
  narration_text), but film-lab cuts one paragraph per picture, so a photo
  between slides gets no paragraph and every later one lands a picture
  off. FIXED on Jacek's yes (commit "A photo between slides gets its
  paragraph"): narration.txt now has a paragraph for every number --
  slides, `[NN]` sections of the script, and `NN_*` pictures in media/
  (a photo with no words gets "-"); publish lists the photos it found and
  prints a PROBLEM line for `[NN]` words with no slide and no photo yet.
  Slides suite 101 OK (4 new), 3 skipped. Not yet run on a real publish;
  not seen by Jacek. (2) `publish` runs `film new` only when projects/<Title>/ does
  not exist; since unify slides.txt lives there, so it never runs for a
  new film and the project gets no `.vertical` (then 1920x1080,
  ffilm/checks.py:217). Here `film new` was run by hand: `.vertical`
  present. Not fixed in publish.
  Slide 04 `face-implied` MADE (session 2, "do next slide"): said/meant
  split by a line, the hearer's arrow down to the "?" weight, "implied
  request". Full still 1080x1920 (ffprobe), 0 [layout] notes, margins
  60/60/120/652 px; half-size draft 8.50 s, steps spaced evenly (not
  narrated); `film check` 65 words, ~26.0 s, steps at 2.0 / 17.2 / 18.8 /
  22.4 s: nothing moves for ~15 s between "Grice" and "search" (rehearsal,
  not his voice). Paragraph [04] added to slides.script.txt word for word,
  copied from the transcript of session 1 (the whole text is nowhere else
  in the repo). Grice 1975 and Sperber & Wilson 1986 cited from memory.
  NOT published. Left: 01, 02, 05, 06, 07, 10.
  Slide 05 STARTED, not drawn: the ledger's geometry (people, table, bars,
  weight) moved to aimanim/ledger.py (issue I14, 03-05 share it);
  face-ledger and face-implied import it. Full stills re-rendered:
  sha256 identical to before (26edace9..., fe997d00...). Plan for 05
  unchanged: "?" struck on "cancelled", the weight lifts off her "free"
  on "gone" (her bar full again), lands on his "free" on "pays". Jacek
  showed Google-AI slide ideas; Claude's verdict (not yet his):
  take W = D + P + R building the red weight for 02; keep the bars (not
  ring + box) in 03-05; maxims / strategy axis match the plans for 06-07.
  Paragraph [05] is now in slides.script.txt word for word (slide name
  face-cancel), so the next session needs no transcript. Steps for 05:
  "cancelled" (strike the "?"), "gone" (weight lifts, her "free" full),
  "pays" (weight on his "free"); geometry from aimanim/ledger.py.
  Slide 05 `face-cancel` MADE (bars kept, Jacek): opens on face-ledger's
  end; "cancelled" white strike through the "?", "gone" weight to the
  middle (0, -2.8) and her "free" full, "pays" weight on his outer 1.2,
  his "free" 1.8. Full still 1080x1920 (ffprobe), 0 [layout] notes,
  margins 67/72/120/598 px; half-size draft 6.50 s (ffprobe), steps
  spaced evenly (not narrated); `film check` 39 words, ~15.6 s, steps at
  4.0 / 11.2 / 12.4 s. NOT published. Left: 01, 02, 06, 07, 10.
  Slide 06 `face-impolite` MADE (session 4): Brown & Levinson's ladder
  (bald / with redress / off record / don't do it; "with redress" merges
  their positive and negative politeness, Claude's call) and Culpeper's
  impoliteness below it, red arrow down on "opposite". Both his paragraphs
  ("Now look..." and the crowds one) added to slides.script.txt [06]
  word for word, from session 1's transcript. Full still 1080x1920
  (ffprobe), 0 [layout] notes, margins 81/81/120/628 px; half-size draft
  9.50 s; `film check` 62 words, ~24.8 s, steps at 12.8 / 16.0 / 20.4 /
  22.8 s: the first 12.8 s show only the title (rehearsal). Culpeper 1996
  cited from memory. NOT published. Left: 01, 02, 07, 10.
  NEXT (Jacek, 2026-10-08: "just go through all of them and we will
  correct them if something is wrong"): make 01, 02, 07, 10 in one
  session with new-scene, no stops between them; commit each. Their
  paragraphs are now in slides.script.txt word for word ([01] [02] [07]
  [10], from session 1's transcript; `film check` still clean). Plans
  (session 1's, not yet agreed): 01 two rings, mianzi outside lit by a
  clapping crowd, lian inside; the crowd fades, the outer ring dims, lian
  stays ("nobody claps"). 02 W = D + P + R, each term a block on its word,
  together the red weight of 03 (Jacek never said yes to this). 07 the
  maxims: quality and relation struck, each with its reason; stones hit
  the outer ring (mianzi) and stop at lian. 10 cheap vs expensive: both
  transfers side by side on the ledger (aimanim/ledger.py, T05).
  Unchecked, his words: the Ackerman finding; "a slur says what is false"
  (many philosophers say slurs insult without asserting).
  01, 02, 07, 10 MADE (session 5), one commit each; the rings of 01 and 07
  in aimanim/faces.py (I14). All four full stills 1080x1920 (ffprobe),
  0 [layout] notes; margins L/R/T/B px: 01 face-two 128/128/120/788 (the
  crowd is gone at the end, on purpose), 02 face-weight 108/162/120/544,
  07 face-fail 107/117/120/550, 10 face-cost 78/78/120/628. Half-size
  drafts 13.00 / 11.50 / 11.00 / 9.00 s, steps spaced evenly (not
  narrated). `film check` rehearsed, ok; film ~155 s at 2.5 words/s for
  the 8 slides. Changed from session 1's plans: 02 shows "W = D + P + R"
  and a legend D distance / P power / R imposition instead of three blocks
  stacking (still not agreed by Jacek); 07's reasons "false" / "not now"
  are Claude's short forms; 10's two ledgers are stacked, not side by
  side, and titled "Who pays" ("Cheap and expensive" is too wide). Hu 1944,
  Goffman 1967, Grice 1975 cited from memory. Left: none; photos 08, 09,
  11, 12 are his.
  PUBLISHED (Jacek's yes, session 5): 8 stills in media/ (01-07, 10), all
  1080x1920 (ffprobe); narration.txt written, 8 paragraphs, one per still
  ([06]'s two paragraphs joined into one); no PROBLEM line, no photos
  found. narration.txt and slides.published.json are git-ignored (nothing
  to commit). Photos 08, 09, 11, 12 not in media/ yet: when added,
  publish again (ask first) so each gets its paragraph. Next for Jacek:
  narrate in film-lab, `film go`, then "narrated" -> `clips`.
  NO INTRO in the recording window (Jacek, session 5). Cause: the script
  had no [intro] section, and publish writes script_intro.txt only from
  one, silently. Fixed for the future (9bb6825): publish prints a PROBLEM
  line for a missing [intro] or [outro]; slides suite 103 OK. Claude then
  made his title + dedication the spoken intro, joining Chérie and "the
  ones throwing stones" in one spoken line: Jacek rejected it, REMOVED.
  The dedication is a written line, never narration. Then Jacek gave the
  intro (his words, in slides.script.txt [intro], as typed: "I love you.
  What does it mean? ... Why do I feel... vulnerable."). He also wrote
  it into script_intro.txt himself.
  Photo paragraphs [08] [09] [11] [12] added to slides.script.txt word for
  word (from his pasted text, session 46e9c487). Re-published (his ask):
  stills unchanged; narration.txt and script_intro.txt NOT written, both
  changed by him in film-lab (his narration.txt para 6 now opens "Doxing?
  Hate? ... aimed at them both"; it has 8 paragraphs, so from picture 08
  on every paragraph is one picture off until he pastes 08/09/11/12).
  media/ has "11 jesus.png" (space, not "_"): publish does not see it as
  picture 11. A recording rec_20261008-212920.mp4 exists. Still no [outro].
  Jacek feared the recordings lost ("I lost an hour"). Measured 21:5x, all
  on disk, none deleted: media/rec_20261008-212920.mp4 23.0 s (camera);
  media/_slides/ 10 voice-over takes, 299 s (ffprobe), last 21:53:22;
  media/_discarded/ 3 camera takes + 24 voice-overs, ~541 s, kept, not
  deleted. Not known: which take belongs to which picture (narration.txt
  had 8 paragraphs for 12 pictures), and whether the window shows them.
  His wish: the recording must not feel fragile -- open, not designed.
  FIXED (2ef93a0, his rule): a picture is placed by its number prefix,
  whatever follows ("11 jesus.png" counts). On his real media/ photos_in
  now finds 8, 9, 11, 12 (measured). Slides suite OK. film-lab's own
  reading of names not checked. He is exhausted and angry at how many
  small traps cost him the evening (2026-10-08): next session, first
  make his narration.txt match the 12 pictures (his "write it"), then
  check which kept take is which picture -- no new design. Same cause, still missing from
  the script: [outro] (plan: "Chérie, you are loved..." on camera, not
  agreed) and the photo paragraphs 08, 09, 11, 12 (his text is in session
  46e9c487's transcript, 2026-10-08 17:20).
- 2026-10-08 [film] A crashed sitting starts the slides over (Jacek,
  "wyjebalo sesje i kaze nagrywac od poczatku"). Found by reading the code,
  not run: per-slide takes go to media/_slides/ (cli.py:1055) so "a crash
  costs one slide" (cli.py:1045 comment), but nothing reads them back: a
  sitting short of all slides exits "Record again to make the narration"
  (cli.py:1225-1229) and the next sitting starts at slide 1 with an empty
  `takes` (cli.py:1044). So the promise in the comment is not kept.
  Love as a Face-Threatening Act, measured: 10 takes wait in _slides/
  (299 s), 21:31-21:53; the same lengths recur (41.8 s twice, 21.7 s
  twice, 28.35 s in _slides and _discarded), so he likely re-read the same
  slides after restarts (inferred). Proposed fix (needs his go; by
  change-the-machine): the window starts at the first slide with no take
  in _slides/ and joins the kept ones at the end. Which take is which
  picture is not recorded beside them (no .cues/.picture json in _slides).
  Jacek's verdict (2026-10-08): the text was meant to be per recorded
  picture, whole; Claude split it, published only the slides' 8
  paragraphs and put him "on a mine": ~$50 and his evening lost. Cause on
  Claude's side: his full text was in the transcript and was not put into
  the script before publish. Rule saved (memory whole-text-before-publish).
  To make it right (his yes needed, it overwrites his narration.txt):
  narration.txt with 12 paragraphs + his edits, shown as a picture ->
  paragraph table first; then the resume fix above.
  Names, measured: film-lab's pictures_in_order on his media/ gives all
  12 in number order, "11 jesus.png" in place 11 (by prefix, as he
  wants). The only name-picky code was slides' publish ("NN_"), fixed
  2ef93a0. The chaos in the window: 12 pictures, 8 paragraphs in
  narration.txt (picture 08 got the insult's words, 09-12 none).
  FIRST next session, before asking him to record anything: transcribe
  the 10 takes in media/_slides/ and match each to its paragraph, so he
  re-records only what is missing. Never again say "nothing is lost" to
  him about recordings: his time was lost (his words, 2026-10-08).
  SALVAGE MEASURED 22:00 (voice.transcribe, small model, scratchpad
  what_was_said.py): the 10 takes in _slides/ are, in time order, full
  readings of narration paragraphs 1-8 = pictures 01-07 and 10 (his
  edited 06 and 07 included); each starts and ends on its paragraph's
  first/last words. 215017 (21.7 s) and 215322 (10.85 s) have no speech
  (0 lines). Usable: 01 213156, 02 213250, 03 213359, 04 213530, 05
  213743, 06 214400, 07 214736, 10 214952. Missing: 08, 09, 11, 12
  (photo paragraphs, ~80 words). Camera intro rec_20261008-212920.mp4
  23.0 s present. Plan (needs his go): he records only 08, 09, 11, 12;
  Claude joins the 12 in picture order with record.join_takes/write_cues.
  22:1x: Jacek overwhelmed ("ja już nie wiem co mam zrobić"). Claude's
  recommendation, given: stop tonight; next session, Claude prepares
  everything (narration.txt with 12 paragraphs on his "zapisz", the exact
  command), he records only 08, 09, 11, 12 (~1 min), Claude joins the 12
  and checks. His choice still open: 1 = 8 slides only (cuts his 4
  photo paragraphs) or 2 = record the 4.
  22:05 he said pressing record overwrites his takes. Measured 22:05:47:
  nothing overwritten, no new take since 21:53, all 10 in _slides and 24
  in _discarded at their sizes. Copied the 10 to
  projects/<film>/backup_takes_2026-10-08/ (10 files, 55 MB).
  22:07 he starts the window, sees it go to slide 1, not the first
  unrecorded one, and stops at once for fear of overwriting. Measured
  22:07:03: no file in media/ changed since 21:54. That is the resume
  fault above; it is the first fix to make (change-the-machine).
  FIXED a4c17ae (his "masz naprawić"): each slide take gets
  <take>.slide.json with its picture; the window opens on, and Enter
  moves to, the first slide without a take; the join uses each picture's
  take in picture order. Film suite 1060 passed. NOT run in the real
  window yet. His 8 good takes labelled by transcription (01-07, 10):
  kept_slides on his project = indices 0-6, 9, so the window should open
  on picture 08 and ask only 08, 09, 11, 12. Needs first: narration.txt
  with 12 paragraphs (his yes to overwrite his file).
  DONE 22:1x (he: "I need to send it soon"): narration.txt now 12
  paragraphs, his 8 byte for byte + his 4 photo paragraphs; old file kept
  as narration.before-12.txt. Measured with film-lab's own
  narration_steps: pictures 01-12 each get their own paragraph.
  22:3x he recorded 08, 09, 11, 12 in the fixed window, `film go`, draft
  "looks good". The resume fix worked in the real window (his report).
  Fault (his): the FILM.bat menu gives no sign that the slides' clips are
  next (`aimanim.film <film> clips`) -- not fixed, noted only.
  CLIPS DONE: 8 clips 1080x1920 (ffprobe), each within 0.04 s of its slide
  (01 29.12, 02 19.42, 03 13.50, 04 25.96, 05 17.50, 06 29.58, 07 29.46,
  10 12.42 s); 8 `clip:` lines in film.yaml; no notes. Next for him:
  `film draft`, watch, then final + upload.
- 2026-10-08 [all] Routing cases built, the box misleads them. 03-plan.md
  took four things from Jacek's second brief (val split 40/20/40; edit-pass
  in a `git archive` copy; gate twice with a min gain; /rate ratings).
  `evals/cases.py routing` froze 92 cases in .local/evals/cases/routing.json:
  46 distinct messages that started a repo skill (change-the-machine 23),
  46 sampled that started none; 39 train / 17 val / 36 test; each keeps
  Claude's last words before it (12 open a session, none). `run.py routing`
  on 6 train cases, measured: --max-turns 1 = 2/6, no run reached a skill
  ($0.13-0.15); 3 turns = 3/6 ($0.09-0.23); 6 turns, the 3 misses again:
  all finished with no skill. "1 i 3" (build bokeh + commit) answered
  "commit only .gitignore... follow the film-code rules" and stopped: a
  run with no Edit/Bash does not start an action skill, so change-the-
  machine misses are the box's, not routing's. Also: the runs see today's
  repo, not the repo of the message. Spent $2.57 in all.
  Later (Jacek: "all permissions granted"): routing runs now act, in a
  `git archive` copy in %TEMP% (outside the repo: inside, git finds the
  real .git), one fresh copy per case. The copy's own settings.json is NOT
  applied (Edit refused, measured), so the rules go on the command line:
  Edit/Write `./**`, Bash, `git push` refused. `run.py probe-act`: Edit in
  the copy worked; the real repo's file, git status, projects/ unchanged;
  push refused. Not proven: Bash on the real repo by absolute path (the run
  tried only Read, which a user setting blocks); the repo snapshot is the
  only guard there. The copy has no memory index and no .git. Same 6 cases,
  6 turns, acting: 2/6 ($0.16-0.27, mean $0.23, 24-112 s). "yes do it"
  (label none) now starts change-the-machine; "1 i 3" and "I gave up
  today..." still start nothing; "status Turn Heat..." answers the question
  inside it. 22 routing runs + 3 probes ≈ $5.8 today. Not yet: the full
  92 (≈ $21, ≈ 75 min, reasoned from the mean), Jacek's labels.
  evals/tests 41 OK.
  Full run DONE (his "go"): 61/92 right, $21.15, repo unchanged; 30 of 31
  misses are "chose none" (change-the-machine 15, edit-pass 3, ship 3,
  investigate 3). Repeats of the 31: INVALID from case 15 of repeat 1 on
  -- the usage limit was reached, runs ended in ~3 s at $0 and were
  recorded as "none" (17 of repeat 1, all 31 of repeat 2). Only the
  first 14 of repeat 1 are real, and all 14 chose the same as the first
  run, so the rest of the repeats were dropped (little noise; the open
  question is the labels). run.py now grades a $0 / error run "failed",
  left out of the table (4c9de47, evals/tests 46 OK).
  Labels: Jacek could not label the 31 ("momentary dialogue events, not
  repetitive"), so NOT his labels: .local/evals/cases/routing-relabel.json
  drops 25 one-off moments (short replies to an offer, permissions,
  one-video renders; 17 of the 31 + 8 that had agreed) and gives 14
  standalone requests Claude's label, marked `by: claude` (ace9edf; the
  frozen file untouched; run.py applies it). Recount of the full run, no
  new runs: 54/67; all 45 "none" right; skill cases 9/22, 12 missed as
  "none" (change-the-machine 4, status 2, investigate 2, edit-pass 2), 1
  new-scene -> binary-diagnostics. 22 skill cases over 10 skills is thin.
  Phase 2 STARTED, step 1 count only (scratchpad edit_cases.py, read-only):
  21 typed messages in the logs were followed by an Edit of a projects'
  film.yaml (What Is Love 7, Bauhaus 4, SUMIFS 3...). Judged by Claude
  from the note and the next message, NOT checked against git: ~10 are
  clean note -> edit pairs (Bauhaus caption notes; What Is Love depth
  x5, all on one setting; Happy Birthday "same image at the end 10 s" and
  "music 20 s"; Bauhaus "depth 0.5"; SUMIFS "remove the start image");
  the rest are code, frustration or permission messages, one with
  `film undo`. Next: cases.py edit-pass (before/after from git per pair),
  then the copy box for edits (03-plan Phase 2).
  `cases.py edit-pass` BUILT: before = the film.yaml's last commit before
  Claude's first edit, after = that before + his logged edits; "clean"
  when every edit fits, the next commit equals it, no `film undo`.
  Measured: 21 notes, 13 clean, 8 doubtful (3 no commit before: I am
  not your fear, 1930s Austria x2; Screening's 10 edits reverted by the
  next commit; SUMIFS s07 undone; SUMIFS "remove the start image" and
  Bauhaus 09-19 captions mixed with a later `film caption`/speed change in
  the same commit; Bauhaus "allow always everything" is the tail of the
  note before it). The 13 clean, by kind (Claude's reading): depth 7
  (What Is Love 6 on one line, Bauhaus 1), in/out of a take 2 (Frankfurt,
  Bauhaus), closing card 2 (Happy Birthday), captions 1 (What Is Love),
  cut a passage 1 (SUMIFS "cut it"). Two of them are not notes on the
  film in his words (Frankfurt "why are these small issues reappearing",
  Bauhaus "continue open.md..."). Thin and narrow for a quality set.
  Candidates (not frozen) in .local/evals/cases/edit-pass.candidates.json.
  evals/tests 59 OK. Next: Jacek decides which count, then split + freeze.
  FROZEN (Claude's pick, Jacek's yes): 6 cases in .local/evals/cases/
  edit-pass.json, all `split: test` (too few to split): Happy Birthday
  closing card 10 s + music 20 s, What Is Love foreign-name captions +
  "slightly increase depth" (one for the depth chain), Bauhaus depth 0.5,
  SUMIFS "cut it". Complaints and permission messages left out. A first
  check only: no tuning (gepa) on 6; it waits for more notes from new films.
  STOPPED here by Jacek (2026-10-08 evening). Nothing to continue unasked:
  not the edit copy box, not gepa (never installed), not another run.
  Possible later, only on his ask: rewrite the descriptions of the skills
  routing missed, then one rerun (~$21) to measure.
- 2026-10-08 [all] Test sets for the skills: Phase 0 DONE, Phase 1 next
  (docs/optimization/03-plan.md; inventory in 01-inventory.md). Jacek's
  decisions: edit-pass is the first skill to get a quality set; Phase 3
  uses `gepa` standalone (0.1.4, 1 package) as a film extra `eval`,
  routing first. `evals/run.py probe`, measured: a test run (`claude -p`)
  had only Glob/Grep/Read/Skill, saw 19/19 repo skills, could not write a
  probe file; git status, projects/ file times and .lastfilm unchanged.
  Routing 3 of 3 right (status, new-scene, edit-pass). $0.12-0.39 per
  case at list price, so ~$30 for 96 routing cases (reasoned). Found:
  `--setting-sources user` drops the repo's skills; `--tools` keeps the
  claude.ai connectors (Gmail, Calendar) unless `--strict-mcp-config`.
  NOT built: the edit-pass box (the project allow list says "Edit"
  everywhere). Cases (his words) go in .local/evals/ only: the repo is
  public. evals/tests 18 OK. Not yet: any case set, any run by Jacek.
- 2026-10-09 [fly] Love as a Face-Threatening Act flown from FLY.bat (his
  run). He thought it stopped after the PNGs. Measured 00:18-00:19: 8977
  frames in fly/out/flight_film_frames (= 374 s at 24 fps; final.mp4 is
  371.0 s), blender.exe still running (1.8 GB), flight_film.mp4 growing
  203 -> 236 MB in about a minute, no moov atom yet (still being written).
  So it was working, but the window gives no sign of the encoding stage
  -- not fixed, noted. Finished 00:24: flight_film.mp4 1080x1920,
  374.0 s, 602 MB (ffprobe). Jacek published it ("it looks good"). The
  film is done in all three stages. Still open from it: the menu gives no
  sign that `clips` follows narration, nor that fly is encoding.
- 2026-10-08 [fly] A flight finds its film wherever the repo is (Jacek's
  ask). stops.json held this laptop's absolute "source"/"film" paths, so a
  packed flight pointed back here. Now film_to_stops writes them relative
  to the flight (../out/...); fly.where and flight.py read both kinds (an
  absolute path that is not there is looked for in the film's out/); fly.py
  finds an existing flight by its place beside the film, not by that path.
  The 17 existing stops.json were left as they are (their paths exist here).
  Measured: a copy of Screening in the scratchpad with its paths set to
  D:/elsewhere/...: Blender --stills made 15 stills, "video would be
  175.8s" as before. Fly suite 16 OK (5 new).
- 2026-10-08 [film] A pack carries the whole repo (Jacek's ask). `film pack`
  listed film/.claude/settings.json and film/.claude/skills (moved to the
  root on 2026-10-07), so a copy's Claude had no skills and no hooks wired,
  and it left out slides/, fly/, SLIDES.bat, FLY.bat, the root CLAUDE.md and
  docs/. Now pack.REPO lists them; a film also brings slides.txt,
  slides.script.txt, slides.published.json, clips/, fly/stops.json, fly/input
  and analysis/tight/. Two more faults found on the way: (1) every file of a
  folder in REPO got the folder's name in the zip (fixed: its own path);
  (2) analysis/tight/ was never packed, so a packed Screening's s03-s07 had
  "voice file not found" (since decision 0015). Measured: toolkit alone 376
  files, 25.4 MB; with Screening 445 files, 423.8 MB zip (was 262 files);
  unpacked in the scratchpad: `film check` OK, 8 shots, 172.7 s; `film peek`
  in the copy 173.300 s = the original's peek (ffprobe). Film suite 1054
  passed (6 new). Not checked: SETUP.bat on a machine without uv; a packed
  flight's stops.json names this laptop's absolute path to the film
  (`source`), so FLY.bat on another machine may not find its old project
  (fly.py project_for compares that path; reasoned, not run).
- 2026-10-08 [film] The speech model is kept in models/ (Jacek's ask):
  faster-whisper got `download_root=models/whisper` (voice.speech_models_dir);
  it was in %USERPROFILE%\.cache\huggingface\hub. The two models there
  (small 464 MB, base 142 MB) were MOVED into film/models/whisper/ (same
  disk, nothing downloaded again; git ignores it like models/*). Measured:
  `local_files_only=True` loads small from there in 8.6 s; the real
  `voice.transcribe` on an 8.00 s slice of Screening's narration said
  "loading the small speech model" and gave 1 line; the user cache stayed
  empty. Film suite 1048 passed (4 new). Not yet seen by Jacek in a film.
- 2026-10-08 [all] Setup in one place: docs/SETUP.md (was slides/docs/SETUP.md,
  git mv) lists all three stages and Claude's tools, with this laptop's
  versions measured today (uv 0.12.8, ffmpeg 9.0.1, git 2.50.1, Node 24.19.0,
  qmd 2.8.3, Python 3.13.5, Blender 5.2.1, R 4.6.1, faster-whisper 1.2.1,
  onnxruntime 1.29.0, Manim 0.21.0) and what is on each machine only (music
  shelf, models, speech models, .devices.json, search index). film/README,
  slides/README, fly/README point to it; film/HOW_TO_USE Part 1 stays as the
  guide of the `film pack` zip (the zip has the film stage only and does not
  carry docs/SETUP.md). Not tried on a second machine; the font line in it
  (slides use the machine's default font) is reasoned.
- 2026-10-08 [all] FIXED, measured: Claude's search pointed at collections
  that no longer exist. Five instruction lines (slides/CLAUDE.md,
  film/CLAUDE.md, slide-layout skill, slides/docs/SETUP.md) named `manim`,
  `manim-history`, `docs`, `code`, `history`, removed in the merge (a search
  in `manim` returned [] with no error); now `v2`, `v2-code`, `v2-history`.
  Second fault: qmd's `v2` kept the file list of 2026-10-07
  (slides/films/*.script.txt, no docs/*.md), so docs/OPEN.md and the 3 slides
  scripts in projects/ could not be found. Cause: `knowledge.setup` skipped a
  collection that existed and `refresh` never compared the lists. Now
  `refresh` (post-commit) adds a collection again when its list differs
  (test_a_search_collection_follows_its_file_list, 6 tests; one checks every
  entry of the lists finds a file). Measured: v2 87 -> 91 documents,
  `get v2/docs/OPEN.md` found, "false positives screening" ranks Screening's
  slides.script.txt first; a second refresh left the lists alone; slides
  suite 97 OK (3 skipped). Supersedes the 2026-10-07 entry on `history`.
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
  2026-10-08 later: BUILT on his "build it": skill `r-charts`,
  slides/r/slide_chart.R + ppv_curve.R (the template), aimanim/rchart.py
  (stdlib, 6 tests; suite 91 OK, 3 skipped), scene scenes/r-ppv-curve (in
  no film). Both faults fixed on the full still: x labels "1k"/"10k" no
  longer touch; "1 in 29" moved off the 20 % line. Rings measured on the
  still against the grid (within 1 px). Not seen by Jacek; leaflet
  still untried. Draft clip rendered (his ask): 540x960, 24 fps, 5.00 s
  (ffprobe), steps spaced evenly (not narrated), no [layout] notes; only
  steps.png (the end of each step) looked at.
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

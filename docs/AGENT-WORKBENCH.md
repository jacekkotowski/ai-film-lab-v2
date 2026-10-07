# The agent workbench: a replicable architecture for AI-assisted projects

A plan for any repository in which an AI coding agent (Claude Code) does
most of the making and a human (the owner) decides, narrates, checks and
publishes. Built and proved on **ai-manim** (animated slides for narrated
films, 2026-10-05 … 10-07); every rule below came from something that went
wrong there. Replace the ai-manim examples with your project's own.

---

## 1. What it is for

| without it | with it |
|---|---|
| the agent re-derives facts, sizes, commands every session | it reads them from files it is told to read |
| the same mistake is fixed on every slide | the fix becomes a rule, then a tested helper |
| "it works" without evidence | every claim comes with a measured number |
| the owner's words or numbers quietly changed | changes are listed first, never silent |
| knowledge in chat transcripts, lost | knowledge in the repo, searchable locally |

## 2. Principles (the non-negotiables)

1. **The owner's input is the source.** His words, data, decisions are used
   as given; anything the agent would change is a *proposal* in the
   answer's first lines. (ai-manim: narration first, animation timed to it;
   a script is used word for word.)
2. **Proof, always.** No "renders/works/passes" without the file, its size,
   length or test count in the same message. Unchecked parts go in the
   FIRST line.
3. **Pure core, thin tool edge.** All maths and geometry in plain-language
   (stdlib) modules with tests; exactly one module touches the heavy
   framework (decision 0002: only `kit.py` imports Manim). Refactors can
   then be proved byte-identical.
4. **The second time is the signal.** Do a thing once by hand; the second
   time, write it down where the next session looks; the third time, code it.
5. **Measure, don't assume.** Sizes, timings, margins are measured and
   stored with the date and what they were measured on.
6. **Plain commands.** One command per job, from the repo root, no `cd`,
   no env prefixes, no heredocs: they match the permission allow list and
   read the same in every session.

## 3. The layers

```
┌───────────── KNOWLEDGE (read by the agent) ─────────────┐   ┌──── CODE (run by the agent) ────┐
│ CLAUDE.md            the contract: who, rules, commands  │   │ core/   stdlib, tested           │
│ .claude/skills/      when to do what (5 kinds, §4)       │   │   domain maths  (diagnostic.py)  │
│ docs/patterns/       issues + tasks, with a ladder (§5)  │   │   geometry      (layout.py)      │
│ docs/decisions/      why things are the way they are     │   │   timing        (beats.py)       │
│ docs/tech/           measured facts about the tools      │   │   pipeline      (film.py)        │
│ docs/OPEN.md         what is broken / unknown            │   │ tools/  one command per job      │
│ docs/sources.md      every external fact, its status     │   │   look.py: render → only problems│
│ PLAN.md              steps, done or not                  │   │ edge/   the one framework module │
│ <item>/spec.md       per deliverable: numbers + sources  │   │   kit.py (Manim)                 │
└──────────────────────────────────────────────────────────┘   └──────────────────────────────────┘
┌───────────── VERIFICATION ───────────────────────────────┐   ┌──── PIPELINE ───────────────────┐
│ unit tests (stdlib, < 1 s) · in-render checks ([layout]) │   │ this repo ──publish──▶ next stage│
│ pixel/size/length probes · rehearsal before the human    │   │ ◀──human's output── back here    │
│ acts · the real result measured after · pre-commit gate  │   │ one command per hand-over        │
└──────────────────────────────────────────────────────────┘   └──────────────────────────────────┘
┌───────────── LOCAL MEMORY & SEARCH ──────────────────────────────────────────────────────────────┐
│ qmd collections: this repo's docs/skills/specs + one file per commit · render log · auto-memory  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 4. Skills: five kinds, each short

A skill is a `.claude/skills/<name>/SKILL.md` with a `description` that
says *when* (the owner's phrases, the subjects). Everything a session
loads costs context, so a skill is an **index + rules**; detail lives in
`docs/` and is read on demand.

| kind | holds | ai-manim |
|---|---|---|
| **workflow** | the steps of a job, in order, and "done when" | `new-scene`, `time-to-words`, `deliver` |
| **craft** | rules + commands + where the patterns are | `slide-layout` (rules, commands, quick map) |
| **subject** | checked numbers with sources, traps, reusable drawings | `shooting-optics`, `binary-diagnostics` |
| **meta** | how knowledge grows | `grow-skills` |
| (catalogue) | not a skill: `docs/patterns/` read via the craft skill | issues I01–, tasks T01– |

Rules for skills: one owner per topic (no two skills describing the same
thing); every rule carries the item and date it came from; descriptions
must not overlap (an overlapping description loads the wrong skill).

## 5. The pattern library and its ladder

`docs/patterns/issues.md` (symptom → cause → general fix) and
`docs/patterns/tasks.md` (kind of deliverable → recipe), one entry format:

```
### I12 — <symptom in searchable words>
- status: note | pseudocode | code | helper <module.function>
- seen:   <item> (<date>), ...
- symptom / cause / fix (pseudocode naming helpers) / code (almost there) / check
```

```
note (seen once) → pseudocode (twice) → almost-there code → tested helper
```
A script (`patterns due`) lists entries seen often enough to climb. When
climbing, generalise: the inputs are sizes, counts, widths — not one
item's numbers.

## 6. Tools: one command per job

Every repeated job became one command that prints **only what to act on**
and `PROBLEM` + exit 1 when something is wrong:

| job | ai-manim command |
|---|---|
| measure before placing | `kit fits "label"` (cached in docs/tech/sizes.json) |
| plan space | `layout stack|pitch|columns|rows` |
| render + check | `look still <item> [full]`, `look draft <item>` (frame per step) |
| everything for a deliverable set | `look film <film>` |
| rehearse before the human acts | `film <film> check` |
| hand over / take back | `film <film> publish`, `film <film> clips` |
| what the work has cost | `look stats` (render log) |

## 7. Verification ladder

1. Unit tests on the pure core (seconds; run by the pre-commit hook).
2. In-render checks of rules (`kit.check`: outside the safe area,
   touching), with known intended overlaps taught to the check.
3. Probes of the real output: pixel margins, size, length (ffprobe).
4. A picture of each step (`steps.png`), read by the agent.
5. Rehearsal of the human's part before he does it (timing at 2.5 words/s).
6. The real result measured after the human acted (clip length vs slide).

## 8. Local knowledge: search before solving

- A qmd collection over this repo's markdown (skills, docs, specs,
  scripts) and one over its git history (one file per commit — one file
  for the whole log returned one hit per search).
- Refreshed by the post-commit hook (`python -m aimanim.knowledge refresh`).
- Rule in CLAUDE.md: before solving something that "feels familiar",
  search the collections; cite what was found.
- The render log (`.local/renders.csv`) is the agent's own telemetry:
  renders per item and which issue IDs keep coming back.
- Auto-memory: the owner's standing preferences that are not project
  rules (how he wants to be told things, what upset him).

## 9. Bootstrapping a new project (checklist)

**Day 0 — contract**
- [ ] CLAUDE.md: who the owner is, the one rule, stages, commands, proof, never-list, where knowledge lives
- [ ] `docs/OPEN.md`, `docs/decisions/0001-*.md`, `PLAN.md` with step 1 = a trial that measures the tools
- [ ] `.claude/settings.json` (tracked): the allow list; `.githooks/` + `git config core.hooksPath .githooks`
- [ ] `docs/SETUP.md`: everything a new machine needs, in order

**Week 1 — the loop, measured**
- [ ] one deliverable end to end through every stage; every time and size measured into `docs/tech/`
- [ ] the pure core split from the framework edge (one edge module)
- [ ] first workflow skill (`new-<item>`), first craft skill

**Every deliverable after**
- [ ] spec first (numbers, sources); the owner's input used as given
- [ ] the commands, not hand checks; fix every PROBLEM or explain it
- [ ] at the end: `grow-skills` pass — what was done by hand twice? file patterns, climb the ladder, `patterns due`
- [ ] commit with what was measured in the message

## 10. What we did in ai-manim (the record)

| when | built | why |
|---|---|---|
| 10-05 | CLAUDE.md, beats.py (timing from narration), 3 workflow skills, trial scene | narration first |
| 10-05 | Manim measured (sizes, render times, `-r` trap), MathTex/TinyTeX | measure before building |
| 10-05/06 | `kit.py` (baseline text, title, layout check), `slide-layout` skill | 5 copies of helpers drifted |
| 10-06 | `film.py` publish/clips into film-lab, decision 0003 | no copying by hand |
| 10-06 | aurora.py + kit.reticle/chain, `shooting-optics` | one drawing, many slides |
| 10-06 | screening film; `diagnostic.py`, dots/people/box/strike, `binary-diagnostics` | a new subject, reusable |
| 10-07 | `look.py`, `film check`, `kit fits/stack`, `slide-tools`, `grow-skills` | repeated jobs → commands |
| 10-07 | `layout.py`, `docs/patterns/` (I01–I23, T01–T13), `manim-patterns` | fixes generalised |
| 10-07 | `slide-tools` + `manim-patterns` merged into `slide-layout` | one craft skill, no overlap |
| 10-07 | this document; improvements 1–9 (§11) | replicable, searchable, measured |

## 11. To do (and in ai-manim: PLAN.md "Workbench 1–9")

1. Index the repo and its history in qmd; refresh on commit; "search first" rule.
2. Merge overlapping craft skills into one short index; detail in docs.
3. One source for measured sizes (`docs/tech/sizes.json`, written by the measuring command).
4. One command for a whole deliverable set; a pre-commit gate (tests + rehearsal).
5. A render log and its summary (renders per item, recurring issues).
6. `docs/sources.md`: every external source once, with its checked status and users.
7. `patterns due`: entries ready to become helpers, checked at the end of each deliverable.
8. A layout check that samples shapes, not boxes (fewer false alarms on diagonals).
9. Nothing important only local: tracked settings, `docs/SETUP.md`, auto-memory for the owner's preferences.

## 12. Anti-patterns we paid for

- Fixing a symptom on one item and not writing it down (it came back on the next).
- A rectangle as a highlight (every text inside "touches" it).
- Judging a picture at half size (the font "looked different"; marks invisible at full size were missed).
- Silent cuts to the owner's text (another session did it; trust lost).
- Commands with `cd …&&`, `VAR=`, heredocs: "Allow once" on every call.
- Several skills for one topic: the agent loads one and misses the rule in the other.
- One file for a whole git log in a search index (one hit per file).

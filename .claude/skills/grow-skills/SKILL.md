---
name: grow-skills
description: Turn repetition into tools -- when the same operation, check, calculation, lookup, fix or correction from Jacek happens a second time, make it a command, a kit helper, a snippet, a rule, or a new skill, and register it so the next session finds it. Use at the end of every film or session ("what did I do by hand twice?"), when he says "make a skill", "reuse", "organize this", or when you notice yourself repeating a step.
---

# Grow skills: the second time is the signal

> Stage **slides/**: plain paths below (`docs/`, `scenes/`, `projects/` ...) are under `slides/`; commands are written to run from the repo root.

Doing a thing once is work. Doing it a second time means the next session
will do it a third time unless it is written down where that session
looks. This repo's skills, `aimanim/` and CLAUDE.md are that place.

## 1. Signals (watch for these while working)

| you notice | it is |
|---|---|
| the same shell command typed again with other arguments | a command (`aimanim/look.py`, `film.py`) |
| the same sum done by hand (baselines, pitches, percentages) | a function, maybe a CLI (`kit.stack`, `diagnostic.py`) |
| the same false alarm explained again | a fix to the check (`kit.strike` → `check` skips it) |
| the same layout fix on a second slide | a rule + measured size in `slide-layout` §3/§4 |
| the same drawing on a second slide | a kit helper (Manim) or stdlib geometry module + a recipe in `docs/patterns/tasks.md` |
| the same facts looked up for a subject | a subject skill with checked numbers + sources (`shooting-optics`, `binary-diagnostics`) |
| Jacek corrects you on HOW to work | a rule in the skill that step belongs to, with the date, and in CLAUDE.md if it is general |
| a run of steps you always do in order | a workflow skill (`new-scene`, `time-to-words`) |

**End of every film** (or session): `uv run --directory slides python -m aimanim.patterns due`
(entries seen often enough to climb), `uv run --directory slides python -m aimanim.look stats`
(which issue IDs came back), then this table.

First time: just do it, and add one line to §5 below (what, which slide).
Second time: make the thing, before continuing the task if it is small.

**A fix or a slide recipe** goes into the pattern library instead
(`docs/patterns/`, indexed by `slide-layout` §4), and climbs its ladder there:
note (1 slide) → pseudocode (2) → almost-there code → tested helper in
`aimanim/layout.py` or `kit.py` (3, or 2 if long). Generalise when you
climb: name the inputs (sizes, counts, widths), not this slide's numbers.

## 2. Where it goes (pick the smallest that holds it)

1. **A sentence in an existing skill** — a rule, a size, a trap. Always
   with the slide or date it came from.
2. **A recipe or issue entry** in `docs/patterns/` — code that worked, ≤ 12 lines,
   naming the scene it came from (the full version stays there).
3. **A helper** in `aimanim/` — stdlib only, except `kit.py` which may use
   Manim (decision 0002) — with a test in `tests/` (stdlib, no Manim).
   Pure part separate from the file/tool part, so it can be tested.
   An existing helper's signature or default look changes only after
   asking Jacek: published slides use it. Add an optional parameter
   instead (2026-10-08, from a Manim agent example he read).
4. **A command** — a `main()` in that module, plain `python -m aimanim.<m>`
   (or `uv run --directory slides --extra render python -m aimanim.kit` if it needs Manim),
   printing only what to act on, `PROBLEM` + exit 1 when something is wrong.
5. **A new skill** — only when none of the above fits: a subject (its
   numbers and sources) or a workflow (its steps).

## 3. Making a skill (template)

`.claude/skills/<name>/SKILL.md`:
```markdown
---
name: <kebab-name>
description: <what it holds, in his words, and WHEN to use it: the
  phrases he says and the subjects that trigger it. This line is all a
  future session sees before loading it.>
---
# <Title>: <one line on why it exists>
## 1. ...  (numbers with sources / steps / commands / snippets)
## N. Growing this   (where new things go)
```
Then, in the same turn:
- add a row to CLAUDE.md's skills table (and its Commands block if it
  brings a command);
- point to it from the skills it works with (one line each);
- say in the answer what was made and how it was checked (test count,
  a real run).

## 4. Checking it worked
- A command: run it on a real slide and compare with the hand result
  (`look margins` gave 60/60/120/544 px, the same as the PIL measurement).
- A helper changing renders: re-render a slide that uses it and show it
  is unchanged (same bytes or pixel diff), or show what changed.
- The whole suite: `python -m unittest discover tests`.

## 5. Repeats seen once (the ledger: second time → act, then strike it here)
(none yet — the first round, 2026-10-07, became `look`, `kit fits/stack`,
`film check`, `kit.strike`'s check exception, `layout.py`, `docs/patterns/`)

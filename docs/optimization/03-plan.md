# 03 — Plan: test sets for the skills, and skills improved by them

Approved 2026-10-08. Read with `01-inventory.md`. Code: `evals/`.

## Jacek's decisions (2026-10-08, in place of a 02-decisions.md)

- Test sets first, no new dependency for them. edit-pass is the first skill
  that gets a quality test set; routing (which skill a message starts) is
  tested for all 19.
- **Phase 3 uses `gepa` standalone, as a film extra** (`eval`, like `voice`
  and `depth` in film/pyproject.toml), **routing first.** Measured: `gepa`
  0.1.4 alone resolves to 1 package for Python 3.13 (dspy would be 67, mlflow 89).
- The cases hold his typed messages. The repo is PUBLIC on GitHub (measured),
  so the cases stay in `.local/evals/` (git ignores it). Code and format are committed.

## Where things go

| path | what | in git |
|---|---|---|
| `evals/run.py` | runs cases through `claude -p`, grades them | yes |
| `evals/checks.py` | pure check functions (Phase 2) | yes |
| `evals/cases.py` | builds cases from the session logs and git (Phase 1) | yes |
| `evals/tests/test_*.py` | one test per rule, named as a sentence | yes |
| `.local/evals/cases/*.json` | the cases, `split: train/test` frozen | no |
| `.local/evals/results.csv` | per run: date, skill, SKILL.md hash, case, pass, failed checks, tokens, $, s | no |
| `.local/evals/work/` | scratch copies, deleted after a run | no |

Commands, from the root:
```
uv run --directory film python ../evals/run.py probe
uv run --directory film python -m unittest discover -s ../evals/tests
```
It runs in film's environment so the edit-pass checks can use
`ffilm.spec.Film.load(path, check_files=False)` (spec.py:559, no media
needed) and `ffilm.moves.FAMILY` (moves.py:155).

## Phase 0 — the box, proven: DONE 2026-10-08

Measured with `run.py probe` (4 runs, $1.10 in all at list price):
- **Boxed in:** each run had exactly Glob, Grep, Read, Skill. A run asked to
  write a file could not (the file stayed "untouched"). `git status`, every
  file time under `projects/` and `.lastfilm` were unchanged.
- **The repo's skills load:** 19 of 19 in every run.
- **Routing, 3 of 3 right:** "where am I with Screening" → status;
  "make a slide about the bearing" → new-scene; "in What Is Love, shot 3
  drags" → edit-pass. All three went through the Skill tool.
- **Cost per case: $0.12–0.39**, 10–32 s. Each run writes 14–42 k tokens of
  cache: 96 routing cases ≈ $30 at list price (reasoned from those per-case
  numbers; on the subscription it is quota). Try `--max-turns 1` (stop at
  the first choice) in Phase 1, and measure.

What the probe changed in this plan:
- `--setting-sources user` alone does **not** load the repo's skills
  (measured). The runs use `user,project`. That is safe for routing because
  no tool that writes exists in the run.
- `--tools` does **not** remove the claude.ai connectors (Gmail, Calendar
  were in the tool list; dontAsk refused them). `--strict-mcp-config` removes them.
- In `claude -p` a run sometimes Reads `.claude/skills/<name>/SKILL.md`
  instead of calling Skill. Both count as starting the skill (tested).
- **The edit-pass box is not built.** The project's allow list says "Edit"
  everywhere, so "Edit only the scratch copy" needs deny rules, a `--settings`
  file or a separate working folder. Solve it and prove it with a probe first, in Phase 2.

## Phase 1 — routing test set, all 19 skills (next)

1. `cases.py routing`:
   - **48 real messages** that started a skill (counted 2026-10-08; the
     counting script is in that session's scratchpad, `routing_labels.py`,
     and moves into `cases.py`);
   - about 48 that started nothing. Jacek labels only the rows where the
     run and the label disagree.
2. Freeze the split: 40 % test, seeded, the same mix of skills on both sides.
3. Run each case once; disagreements 3 times (noise or a real miss).

Accept when there is a table per skill (should-start, did-start, missed,
wrong skill, confusion pairs) and the cost per case is measured.

## Phase 2 — edit-pass test set

1. `cases.py edit-pass`: each Edit of a `projects/*/film.yaml` in the logs.
   - The typed message before it is the note.
   - The before comes from git at that time.
   - The accepted after is the next commit of the file, with no `film undo`
     and no correction next. Doubtful ones go to Jacek.

   Count measured; target 10–20.
2. Fixture: the film.yaml alone, loaded with `check_files=False`. The run
   reads the real project; it edits only the copy (box first, see above).
3. Checks (pure, tested):
   1. it loads;
   2. only the shots of the note changed;
   3. no `from:`/`to:` replaced;
   4. no move family twice in a row;
   5. unchanged captions keep `words:`;
   6. the same direction as Jacek's edit;
   7. the diff is no bigger than his (reported).
4. One run = the baseline.

## Phase 3 — improve, one change at a time (gepa, routing first)

- **Routing:** `gepa` (film extra `eval`) proposes new descriptions. It
  scores them with `run.py` on the train split only; the frozen test split
  decides. A description changes only if test ≥ before and no skill loses
  a case it had.
- **edit-pass:** the same loop on its SKILL.md text (rules, the note→edit
  table, or a sub-file read only for one kind of note).
- **The gate, every time:** test ≥ before; no check lost on any case; cost
  reported; **Jacek reads the diff**; one commit with before/after numbers.
- **Never changed by the loop:** `## Never` sections,
  `disable-model-invocation`, `model:` pins, settings, hooks (01-inventory §7).
  A pure check refuses such a diff.
- Open: how gepa calls the model (no API key; through `claude -p` like
  `run.py`), and its budget per run. Measure on 5 cases first.

## Phase 4 — the constant loop

- A correction of a film edit becomes a new edit-pass case the same day.
- A changed SKILL.md gets its set re-run, by hand (runs cost quota).
- Root CLAUDE.md gets the command and a "Where things are" row.

## Open questions

1. A budget cap per full run. Measured cost: $0.12–0.39 per case, so ≈ $30
   for 96 routing cases at list price.
2. Fewer than 10 usable edit-pass cases → grow them from new corrections
   (Phase 4), or write cases from OPEN.md faults?
3. The logs of the three old repos (59 of the 63 sessions) are mined too:
   their film/projects/… paths map to projects/… .

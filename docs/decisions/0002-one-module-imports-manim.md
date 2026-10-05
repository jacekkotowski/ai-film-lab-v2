# 0002 — One helper module may import Manim: `aimanim/kit.py`

**Status:** accepted 2026-10-05 (Jacek: "make the improvements general";
"accumulate this knowledge so you can do less next time").

## The question
Five slides repeated the same fixes: text on a baseline, a title that
fits under TOP, rounded directions, the step loop, checking margins and
collisions by eye. Where does that code live?

## The answer
In `aimanim/kit.py`, which imports Manim. Everything else in `aimanim/`
stays standard-library only, so `beats.py`, `film.py` and the tests run
without Manim installed.

| Option | Why not |
|---|---|
| copy the helpers into every scene | five copies drifted already (two text helpers with different argument orders) |
| stdlib-only helpers | placing and measuring text needs Manim's own font metrics |
| `aimanim/kit.py` | one place; scenes import it, the tests never do |

## What it holds
`text` (baselines), `title` (fits under TOP), `fits` (measure a string),
`toward` (rounded directions), `run` (steps on the beats, then the
layout check), `check` (safe area, text on text, text on a drawing).
The rules and measured sizes that go with it: the `slide-layout` skill.

## How it was proved
All five slides were switched to `kit.run`; their full-size stills were
pixel-identical before and after (2026-10-05).

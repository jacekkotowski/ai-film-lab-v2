---
name: two-column-boards
description: The two-column slide technique for any subject with an A -> B story -- an Excel formula, a Power Query step, a piece of R, a before/after. Boards made OFFLINE in this repo (slides/boards: pan_kit.py, render_png.py, make_pans.sh), imported as 2160x1920 PNGs, panned left to right by `move: columns`, the pan placed on the words with `cross:`. Use when Jacek wants a "two column slide", "pan board", "A then B", a comparison of two techniques or two stages, or code (M, R, VBA, DAX) shown step by step.
---

# Two-column boards: A on the left, B on the right, the camera follows the words

> Stages: boards in **slides/boards/**, the pan in **film/**. Commands run from the repo root.
> Excel specifics (series rules, narration, knowledge base): skill `excel-short`.

## The technique

One board = **2160x1920 = two 1080x1920 columns**. Left = step A (the problem, the
first action, the old way), right = step B (the fix, the second action, the new
way). In the film (1080x1920) the camera holds on A, crosses, holds on B:
`move: columns` (film/ffilm/moves.py). `film init` gives it to any still twice as
wide as the frame (unless one table runs across the middle).
One slide = one story of two steps. Two features -> two slides. 4-7 slides a video.

## Making a board offline (no network, no new dependency)

- `slides/boards/pan_kit.py` -- stdlib, HTML out. Pieces: `panel` (a column),
  `keys`, `fbar` (formula bar / one line of M or R), `code(lines, hl=, title=)`
  (a card for Power Query M, R, VBA, DAX; shrinks the font so no line wraps,
  refuses a line that cannot fit: split it), `sheet`, `dropdown`, `chips`,
  `badge` (green check / orange cross), `note`, `card`, `set_series`, `write_boards`.
- The script lives with the film: `projects/<Title>/boards/slides.py`
  (`sys.path.insert(0, "slides/boards")`, `from pan_kit import *`, `set_series(...)`
  BEFORE the panels are built, then `write_boards("projects/<Title>/boards/html", [...])`).
  Demo: the docstring of `pan_kit.py`; one board in the scratchpad of 2026-10-10 had
  M on the left and R on the right.
- `uv run --directory slides python projects/<Title>/boards/slides.py`
- `uv run --directory slides python boards/render_png.py projects/<Title>/boards --media projects/<Title>/media`
  renders with headless Chrome/Edge (no Playwright), checks each PNG is exactly
  2160x1920, writes `png/contact_sheet.png` (ffmpeg), copies into the film's media/.
  Look at the contact sheet and at every board with Read.
- Fonts: Space Grotesk + JetBrains Mono. With the files in `models/fonts/`
  (SpaceGrotesk-*.ttf, JetBrainsMono-*.ttf) the page never touches the network;
  without them it asks Google when online and falls back to Segoe UI / Consolas
  offline (boards then look different: measured nothing yet, reasoned).
- `slides/boards/make_pans.sh` is the plan's standalone pan (hold/pan/hold, no film
  around it). For a film use `columns` instead: it has captions and voice.
- Boards can also come from the online project "Excel refresher" (skills
  `pan-boards-canvas` + `pan-boards-export`); the PNGs import the same way.

## Board rules (checked on import)

- Per column: top 220 px and bottom ~350 px free; side padding 80 px; headline <= 2
  lines at 84 px; no code in a headline; mono lines never wrap (`mono_size`:
  0.6 em per glyph, 920 px across, 800 px inside a code card).
- **Captions sit at 1490-1860 px of the frame** (docs/OPEN.md, measured 2026-10-06):
  keep footers above y = 1450.
- Show the exact action: keycaps, formula bar, dropdown, dialog, code card.
  Generic UI, no vendor logos. Green check / orange cross: icon + words, not colour alone.
- Every example obeys the series' naming; never invent statistics.

## In the film: the pan on the words

`move: columns` alone pans on a fixed clock (hold 37.5 % / pan 25 % / hold 37.5 % of
the shot): measured on Dynamic Arrays - Dropdown Lists it ended 0.1-3.6 s off the
words. A shot may carry **`cross: <seconds>`** (film seconds, like a caption's `at`):
the camera is half way between the columns then, and the pan lasts 2.0 s
(moves.COLUMNS_PAN) around it. Commit 36c2e30, 10 tests.

To set it, after `film go` has written the captions:
1. Read the board and the captions of the shot in film.yaml; find the first caption
   that is about the RIGHT column (B).
2. `cross` = the midpoint between the end of the previous caption (`at` + `dur`) and
   the `at` of that first B caption. Write it after `move: columns`, with a comment
   naming both sentences. (Dropdowns: 11.53, 12.13, 13.35, 5.38, 12.10, 9.59.)
3. `film check`, `film draft`, then look at frames around the crossing (a draft is
   12 fps: frame number = fps x seconds, not 24 x). Say which slides you looked at.
- A sentence about A spoken after the first B sentence is named in the first lines:
  the words are his, the order is his call (Dropdowns slides 03 and 05 had one).
- `film fit` scales `cross` with the captions; the bench (`film edit`) keeps it.
- A slide added later by `film go` has no `cross`: the fixed clock until you set it.

## Never

- Re-publish or re-record over his takes; cut his words; add effects or polish.
- Say "works" for a pan you have not measured on his file.
- Hand-shift `from:`/`to:`; use `cross:`.

---
name: excel-short
description: A Short that explains one Excel technique -- boards made online (claude.ai project "Excel refresher", skills pan-boards-canvas + pan-boards-export), then brought here as 2160x1920 PNGs, narrated, and panned left to right by `columns`. The board rules, the narration rules, the import checks and the known pan-timing fault. Use when Jacek wants to explain something about Excel in a short, brings Excel board PNGs, or says "Excel video", "next in the Excel series".
---

# Excel short: two-step boards -> narration -> film

> Stage **film/** (the boards come from outside). Commands run from the repo root.
> Source of this recipe (2026-10-10): his plan `excel_refresher_claude_code_plan.md`, the
> claude.ai project's `00_instructions.md` (read there, same rules), and the five Excel
> films already made (Use Tables, Lookup vs Data Model, Time Logic, SUMIFS SUMPRODUCT vs
> DAX, Dynamic Arrays - Dropdown Lists). Facts about Excel: `knowledge-base.md` beside
> this file (from the five Issue workbooks, which live only in the online project).

## What a video is

- 1080x1920, 4-7 slides. Each slide is ONE board PNG of **2160x1920 = two 1080x1920
  columns**: left = step A (the problem or first action), right = step B (the fix or
  second action). Intro and outro have no board: Jacek on camera.
- The film pans left -> right with `move: columns` (hold left 37.5 %, pan 25 %, hold right
  37.5 % of the shot; `film init` picks it for a 2:1 picture by itself). Do NOT use the
  plan's `make_pans.sh` or its 3/12/3 clock: the film does the pan, with captions and voice.
- The boards are made either ONLINE (claude.ai project "Excel refresher", skills
  `pan-boards-canvas` -> `pan-boards-export`) or OFFLINE here with `slides/boards/`
  (pan_kit.py, render_png.py, make_pans.sh): skill `two-column-boards` has the commands,
  the pieces and the pan-on-the-words rule (`cross:`). Boards he already has: use them.

## Board rules (checked on import)

- Title names the feature plainly ("Total row"), never framing. A slide with two features
  is two slides. File `NN_Title_of_slide.png` -> `projects/<Title>/media/`.
- Per column: top 220 px and bottom ~350 px free; side padding 80 px; headline <= 2 lines;
  no code in a headline; mono lines do not wrap. Check each board with Read, not by trust.
- **Captions sit at 1490-1860 px of the frame (OPEN.md, measured 2026-10-06).** Keep
  footers above y = 1450. In Dropdowns slide 01 a footer sat at about y = 1500, touching
  the caption (measured on the PNG, 2160 px board, x 1.08 of the viewed image).
- Examples obey the series naming (tbl_ + subject + grain + scope; rng_; columns type
  first: name_rep, date_start, qty_m01, qty_total, prc_net, kpi_margin_pct). One sample
  dataset: `tbl_Sales_mthly_NorthTeam` (Johnson, Smith, Paul, Frank, Helmut + Kowalski as
  the new row), `tbl_Staff_NorthTeam` (East = Frank, Johnson, Paul; West = Helmut, Smith).
  Never invent statistics. Generic UI, no vendor logos. Green check / orange cross.

## Narration rules

- **Formulas and exact names live on the boards, never in the narration**: it says what a
  formula does. (The online skill `pan-boards-canvas` says the opposite -- "formulas in
  `code`"; the project instructions, the plan and all five films say never. Keep never.)
- One paragraph per slide, **A then B, without saying so** (no "left", "right", "on this
  slide", no spoken labels). Everything on the board is spoken as what it does; nothing is
  spoken that the board does not show. Shortcut first, then the menu path
  ("Ctrl+T, or Insert, Table"). Full sentences, each speakable in one breath (<= ~20 words).
  No noise: no version notes, "in this video", rhetorical questions, praise.
  Rows are appended (union), never "joined"; "join" means lookup/merge.
- Outro: recap of the steps, ONE anchor line the viewer can recite, the next video.
- Anything not from the source workbooks / the knowledge base is flagged to Jacek to verify
  in Excel before he records. Which Excel version is decided per video: the plan's "Excel
  2013 only" (no XLOOKUP, FILTER, SORT, UNIQUE, dynamic arrays, Power Query) held for video
  01 only; 4 of the 5 films teach XLOOKUP, Power Query, Data Model, DAX or dynamic arrays.
  Ask at the outline; if 2013, the ban list applies.
- **His words are his** (agreement 1). A script he gives is used word for word; anything you
  would change is named in the first lines.

## Length

Measured on the five finished films (narration + intro + outro words, final.mp4 length):
Use Tables 366 / 171.9 s, Lookup 276 / 137.8 s, Time Logic 419 / 177.8 s, SUMIFS 354 /
168.2 s, Dropdowns 351 / 146.5 s = **2.0-2.4 words/s** in the final (speed 1.25, pauses
cut). The plan's 135 words/min (2.25/s) is inside that range: 330-340 words land between
2:20 and 2:49 (reasoned from the five). Plan with 2.0/s to stay under a target.

## Steps

1. **Outline** in chat: per slide the title, A and B (headline, subline, visual, footer).
   Version of Excel. He agrees before anything is built.
2. **Boards** come from the online project. On import: `ffprobe`/PNG header says
   2160x1920 for every board (not 1080 wide), names `NN_...`, 4-7 of them, Read each one,
   say what you see wrong (wrapped mono, footer too low, text in the safe zones).
3. **Texts** into `projects/<Title>/`: `script_intro.txt`, `narration.txt` (one paragraph per
   picture, blank line between), `script_outro.txt`. **Paragraphs only: no headings, no
   word counts.** The online `videoNN_*.md` has `## NN Title` headings and a `# Boards (not
   spoken)` section; pasted whole, five of the six Dropdowns paragraphs came out as "Named
   range on a table column Press Ctrl+F3" and were recorded and captioned that way (the
   other four films have none). Never overwrite a non-empty file (agreement 2; write-to-fit
   rule 6): put the new text beside it and say so.
4. **Check the order against the boards** before he records: list each slide's A and B
   content (from the board or the md's "Boards (not spoken)") and mark, per sentence, A or B.
   Any A sentence after the first B sentence is named in the first lines. Dropdowns slides
   03 ("The name follows the table") and 04 ("sorted by region") had one each.
5. `film ingest`, `film init` (finds `columns`), `film check`, `film peek`; he narrates in
   FILM.bat, `film go`, `film draft`. `.vertical` must exist in the project.
6. **Pan on the words**: after `film go`, set `cross:` on every `columns` shot from its
   captions (the midpoint between the last A caption's end and the first B caption's
   `at`), as written in `two-column-boards` ("In the film"). Fixed 2026-10-10, commit
   36c2e30; measured on Dynamic Arrays slide 2 only (frames around 11.53 s), the other
   five by numbers. Do not hand-shift `from:`/`to:`.
7. `film final` only when he asks. Cover and upload text as in `ship`.

## Never

- Re-publish or re-record over his takes; cut his words; add effects or polish.
- Say "works" for a pan or caption you have not measured on his file.

---
name: evidence-short
description: A pasted research plan (Speech / Photo list / Photo links and licences / Bibliography / Code fragments, as the online "evidence-dense short presentation" writes it) turned into a 2.5-minute film of 5-7 slides -- 2 or 3 key slides, at most one support slide each (2a, 3a), every key shown as the CODE that did it (legible tidyverse/base R, each line 18 characters or less, run on toy data first) or as a free-licensed PHOTO found with its link, size and licence. The research goes in practical directions only -- the number at its primary source, the method as really run, the picture. Use when Jacek pastes such a plan, says "present the code", "one-liners", "find a picture", or starts a film about how a statistic, model or algorithm really worked.
---

# Evidence short: a pasted plan → 5-7 slides, the code shown, the people shown

> Stages: the plan in **film/docs/plans/**, the slides in **slides/** (new-scene,
> slide-layout), the recording in **film/**. Commands run from the repo root.

Made 2026-10-12 on his rules for the plan "The Social Reckoning" (Kosiński,
Kogan, Haugen; §7): "limit to 2 or 3 keys, maybe a supporting 2a and 3a,
max 5-7 slides for 2.5 minutes; present the code, legible tidyverse to show
it is simple, one-liners; if a pic is better, find a link to a good pic".

## 1. The pasted plan is decided

- His speech is used **word for word** (agreement 1, memory
  pasted-plan-is-decided). Never re-ask what it fixes. Anything cut or
  changed is named in the FIRST lines of the answer, with the reason.
- The plan's own "Corrections" and "Anchor changes" are its author's, not
  his: show them, do not apply them.
- Intro and outro: his. The intro is on camera; never assemble one from his
  lines (memory intro-is-his).

## 2. The shape: 2.5 minutes, 5-7 slides

| part | slides | what it is |
|---|---|---|
| intro | 0 (camera) | his words |
| key 1-3 | 1 each | the speech's own "Slide N" paragraphs; the key is the ONE thing the paragraph proves |
| support 1a/2a/3a | 0-1 per key | only when the paragraph has a second sentence-group a key slide does not show (a person, a company) |
| outro | 0-1 | a slide only if it carries a number (Social Reckoning: one line of code) |

**Words:** 150 s = about 280 words, measured on his films: Map and Calculator
01, 321 words → 171.2 s (1.875 w/s); his Excel finals 2.0-2.4 w/s. Over 300:
name what you would cut, first lines, he decides.
**Splitting a paragraph** over a support slide and a key slide is allowed at a
sentence boundary only (film-lab: one paragraph per picture); name the split.

## 3. Research: the practical directions only

For each key, three things, and nothing else (no background history, no
related studies):

1. **The number at its primary source** -- the paper, the leaked document's
   reporting, the court filing. Say "(primary)", "(reporting)" or "(memory)"
   beside every number. On screen: the speech's number, metric.
2. **The method as it was really run** -- the steps, the model, the inputs:
   that is what the code slide shows (§5).
3. **The picture** (§4), only if a photo says it better than code.

## 4. Code or picture? (decide per slide, one thing per slide)

| the point of the words | show | why |
|---|---|---|
| "it is simple", "a formula", "staff chose the numbers" | **code**, line by line on his words | the viewer sees there is no magic: 3-6 short lines |
| who did it, who leaked it, who bought it | **photo** of the person, real, free licence | a face anchors a name; code cannot |
| one number against another (85 in 100, 50 % → 80 %) | a **result line** under the code, or `kit.card` | a number is read, not watched |
| a curve, a distribution | skill `r-charts` | |
| two stages of one piece of code (A → B) | skill `two-column-boards` | |

A key gets its code; its support slide is the photo. Never code and photo on
one slide (no room at 56: §5).

**Finding the photo** (Wikimedia Commons first; free licences only: CC0, PD,
CC BY, CC BY-SA). The online plan missed free photos (Kosiński: "none
found"; Commons had two). Look in the person's category, then search files:
```
curl -s -A "ai-film-lab/1.0" "https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:Frances_Haugen&gcmtype=file&gcmlimit=50&prop=imageinfo&iiprop=url|size|extmetadata&iiextmetadatafilter=LicenseShortName|Artist&format=json"
curl -s -A "ai-film-lab/1.0" "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=%22Michal%20Kosinski%22&gsrnamespace=6&gsrlimit=15&prop=imageinfo&iiprop=url|size|extmetadata&iiextmetadatafilter=LicenseShortName&format=json"
```
(non-ASCII titles like "Michał" fail in `titles=`: search instead; read the
file page with WebFetch for the caption that names the person.)
Prefer, in order: a **portrait crop ≥ 1080 px wide** (fills 1080x1920 with
no upscaling; Commons often has a "(cropped)" version), CC BY over CC BY-SA,
the person speaking about the subject, near the year of the story.
Write down: file page URL, size (px), licence, author (the credit). The
credit goes in the YouTube description, not on screen (MIN_FONT). He
downloads it (a download needs his yes); it goes to `projects/<Title>/media/`
as `NN_<name>.jpg`.

## 5. The code: legible, runs, fits

- **18 characters per line at most.** Measured 2026-10-12: Consolas
  (`kit.MONO`) is 0.4216 units a character at 56 (MIN_FONT), and the slide is
  8.0 units wide → 18 fit (22 at 48, 26 at 40: below MIN_FONT, not used).
- **One verb per line**; the pipe `|>` ends a line; arguments on their own
  lines; right-align numbers in a sum (`   1 * like +` / `  30 * comment)`).
- **3-6 lines** per slide. Names in plain English (`likes`, `friends`,
  `score`), numbers as in the speech and the source.
- **tidyverse where it reads better** (`mutate`, `arrange`, `filter`),
  base R where it is shorter (`glm`, `lm`, `predict`, `svd`). No package a
  viewer must look up (irlba, pROC → base `svd`, `glm`).
- **Run it before it goes on a slide**: the slide lines inside a toy-data R
  script, `Rscript` prints a result and the longest line
  (R: `"C:/Program Files/R/R-4.6.1/bin/Rscript.exe"`, not on PATH; dplyr,
  tibble, tidyr, purrr, broom installed). Say "runs on toy data", never
  "the real model".
- Each line appears on the word that names it (BEAT_WORDS, as every scene);
  what a line MEANS is a muted subline under the code, not an R comment.
- No code helper in kit yet: `kit.text(line, x, baseline, font=kit.MONO)` per
  line. The second film with code slides → `kit.code(lines)` (grow-skills).

## 6. The output (one file, then his go)

`film/docs/plans/<date>/PLAN-<slug>.md`:
1. First lines: every deviation from his plan (cuts, splits, a fact the
   source does not support, a photo changed), with the reason.
2. The slide table: NN | his sentences (first words) | shows (code / photo /
   result) | source of each number | photo URL, px, licence, credit.
3. The code of each slide as it will appear, with the toy-run result.
After his go: `slides.script.txt` ([intro] [NN] [outro], his words; not
committed, the repo is public), the scenes (`new-scene`, `slide-layout`),
`look film`, then publish (ask first).

## 7. Worked example: "The Social Reckoning" (2026-10-12)

Plan: film/docs/plans/2026-10-12/PLAN-social-reckoning.md. 6 slides: 01
code (likes → 100 columns → logistic, "85 in 100"), 02 code (train on the
quiz, score the friends), 02a photo Nix, 03a photo Haugen, 03 code (points),
04 outro code (`w["angry"] <- 0`). Toy run: all lines ≤ 18 characters.

## 8. Growing this

New photo sources that worked, code idioms that fit 18 characters, and his
corrections go here with their date.

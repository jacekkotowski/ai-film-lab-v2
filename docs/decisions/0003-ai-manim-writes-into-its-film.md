# 0003 — ai-manim writes into its film's ai-film-lab project

**Status:** accepted 2026-10-05 (Jacek: "I will die copying pasting";
"yes you can"; "you are allowed to modify ai-film-lab to play videos").
Replaces 0001's "ai-manim never writes into ai-film-lab".

## The question
Copying stills and clips between the two repos by hand, renaming them,
and re-timing animations against a take: every film. Who moves the files?

## The answer
ai-manim does, into ONE place: the film-lab project named in
`films/<film>.txt`. Two commands:

| | writes | when |
|---|---|---|
| `film <f> publish` | `media/NN_<scene>.png`, `narration.txt`, `script_intro.txt`, `script_outro.txt` (never over a file changed in film-lab since the last publish) | before narrating |
| `film <f> clips` | `clips/NN_<scene>.mp4`, a `clip:` line under the slide in film.yaml | after narrating and `film go` |

ai-film-lab learned one key for this (its commit 2e7356a, "A slide can
show a clip instead of its picture"): `clip:` on a slide plays the clip
in place of the picture, from its first frame, at speed 1, full frame;
the slide keeps its words, captions and length.

## Why timing comes from film.yaml, not from the take
A slide's voice is the pause-cut copy of the narration, played at its
`speed` (1.25 on SUMIFS). film-lab writes each slide's captions in the
film's own seconds from the start of the shot (`caption_fit.py`:
at = (line.start − in) / speed), with a time per word. So the captions
ARE the beats, already in the clip's clock. Reading the raw take would
need film-lab's pause map and speed re-derived here.

## How it was proved (2026-10-05)
- film-lab: throwaway project, draft 8.4 s showed the 4 animation steps
  in order, last frame held past the clip's end.
- ai-manim: throwaway film.yaml with captions; `clips` rendered two clips
  (9.96 s / 10.40 s slide 10.00 s; 10.33 s / slide 10.40 s), placed the
  `clip:` lines, `film check` accepted them; steps started on their
  words (0.6, 4.6, 7.5 s; 0.4, 4.4, 6.5 s). Both throwaways removed.

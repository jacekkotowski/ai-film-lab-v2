# Manim on this machine — measured facts only

Measured 2026-10-05, Windows 11, Manim Community v0.21.0, scene
`back-azimuth` (9 animations, 10.21 s of clip). Times are wall clock of
the whole `uv run ... manim` command, ONE run each, so they include
Manim's start-up (~5 s).

| Fact | Value | Measured on |
|---|---|---|
| install size (`uv sync --extra render`) | `.venv` 286 MB, 19.2 s (uv cache warm or not: not recorded) | 2026-10-05 |
| still, 540×960 | 8.5 s first run, 5.2 s second | 2026-10-05 |
| still, 1080×1920 | 5.5 s | 2026-10-05 |
| draft clip, 540×960 | 7.0 s for 10.21 s of clip | 2026-10-05 |
| full clip, 1080×1920 | 10.4 s for 10.21 s of clip; 287 KB, h264 yuv420p, 24 fps, 245 frames | 2026-10-05 |
| MathTex with TinyTeX | works after the packages below; one formula, 540×960 still in 7.0 s | 2026-10-05 |

Reasoned, not measured: subtracting the still's time from the clip's
gives the cost of animation alone, about 0.2 s per s of clip at 540×960
and 0.5 s per s at 1080×1920.

## Behaviour (measured)
- `-r 540,960` and `-r 1080,1920` give vertical output of exactly that size.
- `-ql` alone gives 854×480: it overrides `manim.cfg`'s size. Always give `-r`.
- Output paths: `out/images/scene/Slide_ManimCE_v0.21.0.png` (the still;
  half and full size overwrite each other — same name) and
  `out/videos/scene/<H>p24/Slide.mp4` (half and full size kept apart).
- `pydub` prints `SyntaxWarning: invalid escape sequence` on every run. Harmless noise.

## TinyTeX for MathTex (installed 2026-10-05, Jacek's yes)
`C:\Users\jacek\AppData\Roaming\TinyTeX`, TeX Live 2026, repository
`https://tlnet.yihui.org`. `tlmgr` is `bin\windows\tlmgr.bat` (not on bash's PATH).
- `tlmgr update --self`: revision 79491 → 79639 (needed before any install)
- `tlmgr install standalone` → then `preview.sty` was missing
- `tlmgr install preview doublestroke dvisvgm babel-english rsfs setspace relsize ragged2e microtype`
- pulled in with them: adjustbox, collectbox, currfile, filemod, gincltex,
  svn-prov, hyphen-english, dvisvgm.windows. hyphen-english made tlmgr
  rebuild the LaTeX formats (all reported OK).
Only the first two packages were shown to be needed; the rest is Manim's
usual list, installed on Jacek's choice. Tested with one formula only
(`\theta_{back} = \theta + 3200 \pmod{6400}`).

Known before measuring (Jacek's films): ai-film-lab films are 1080×1920 at 24 fps.

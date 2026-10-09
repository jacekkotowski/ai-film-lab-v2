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
- A `wait` is drawn as `int(seconds × fps)` frames (rounded DOWN); a
  `play` as `len(np.arange(0, run_time, 1/fps))` (0.5 / 1.0 / 1.5 s = 12 / 24 /
  36). Eight mil-measure clips came out 1.0–4.6 frames short of their slides;
  with the waits counted in whole frames (`beats.in_frames`) each is
  floor(slide × 24) frames, under 1 frame short (ffprobe, 2026-10-06).
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

## SVG import (`SVGMobject`, measured 2026-10-09, drawsvg 2.4.2 via `uv run --with`, not a dependency)

Kept: path (curves), circle, rect, line, polygon, group transforms
(rotate), `<use>` (3 uses = 3 shapes), fill colour, fill opacity, stroke
width. Lost, silently: linear gradient (drawn black), stroke-dasharray
(solid line), clip-path (the whole shape is drawn). Lost with a warning:
`<text>` ("Unsupported element type", `text_to_mobject` is a stub in 0.21).
R's own `svg()` device (cairo) writes text as glyph `<path>` + `<use>`, no
`<text>`: a ggplot through it loads with every label (61 shapes, no
warning, still checked by eye). Transparent background through `svg()`
not tried.

Open Peeps (Pablo Stanley, CC0 1.0 per DiceBear's page; not checked at
the source): one figure fetched 2026-10-09 from
`https://api.dicebear.com/9.x/open-peeps/svg?seed=Felix` (8994 bytes) into
`models/openpeeps/peep-felix.svg`. Loads in Manim 0.21 with no warning, 8
shapes, full colour, outlines intact (looked at the 540x960 still). The 8
shapes are split by colour layer (white backdrop square from the mask, skin,
shirt, black outline, face skin, hair, face lines, one small black), not by
body part: no separate arm or head. The white square must be removed.

## python-lottie (read, NOT installed or run; PyPI page 2026-10-09)

`pip install lottie` 0.7.2 (2025-05-01), beta, **AGPLv3+**, no dependency
for the core. Builds and converts Lottie vector animations: parenting,
anchor-point rotation, easing, inverse-kinematics solver, trim-path
(draw-on), SVG import and animated SVG export, text as shapes. `lottie_convert.py in.json out.png --frame N`
renders one frame (needs cairosvg + pillow); MP4/WebM export needs
cairosvg, numpy, OpenCV. Per-frame PNG keeps alpha; no merge-paths, no
expressions. Idea only: frames as an image sequence in Manim.

## manim-physics and fabrik_chain_3d (read 2026-10-09, NOT installed)

manim-physics 0.4.0 (PyPI 2024-04-17, maintainer says no time to maintain):
2D, electromagnetism / optics / waves / rigid mechanics (gravity Space,
pendulum), built on pymunk + shapely. Pins `manim ~0.18.0` and `python
>=3.9,<3.13`; this repo has Manim 0.21.0 and Python 3.13.5 (measured):
it does not install as declared. fabrik_chain_3d (MIT, 12 stars, last
commit 2021-04): FABRIK for 3D robot chains with joint constraints, an
example script that plots with matplotlib; no pip release seen.

## On the phone
`MIN_FONT` 56 is readable on Jacek's phone (back-azimuth still, 1080×1920,
2026-10-05). Smaller sizes not tried.

Known before measuring (Jacek's films): ai-film-lab films are 1080×1920 at 24 fps.

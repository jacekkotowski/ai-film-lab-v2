"""frame.py -- the shape of every slide, in one place.

Must agree with `manim.cfg` (Manim reads that file; scenes read this one).
Units: the frame is 9 wide and 16 tall, centre (0, 0), so y runs from
+8 at the top to -8 at the bottom.

ai-film-lab films are 1080x1920 at 24 fps (measured from film.yaml,
2026-10-05), so the slides are made at exactly that.
"""

WIDTH, HEIGHT, FPS = 1080, 1920, 24
FRAME_W, FRAME_H = 9.0, 16.0

TOP = FRAME_H / 2 - 1.0         # keep 1 unit clear at the top
BOTTOM = -FRAME_H / 2 + 3.0     # keep 3 units clear: film-lab's captions sit there
SIDE = FRAME_W / 2 - 0.5

# Smallest text worth putting on a phone. A guess until Jacek has seen
# the trial's still on his phone (PLAN step 1).
MIN_FONT = 56
TITLE_FONT = 80

BACKGROUND = "#101418"
INK = "#E8E6E3"
ACCENT = "#F2B33D"     # the thing being explained
SECOND = "#5DADE2"     # the thing it is compared with
DIM = "#6B7178"

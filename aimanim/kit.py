"""kit.py -- what every slide needs, learned from fixing the first five.

The ONE module in aimanim/ that imports Manim (decision 0002): scenes
import it; the tests and beats.py never do. Each helper exists because a
real slide went wrong without it -- docs/tech/layout.md says which.

    from aimanim import kit
    kit.title(...), kit.text(...), kit.toward(...), kit.run(...)

`kit.run` plays the steps on the narration's beats, then checks the last
frame (the still) against the frame rules and prints `[layout]` notes:
something outside the safe area, text on text, text on a drawing.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from manim import Group, Mobject, Text, VGroup

from aimanim import beats, frame

# Measured at frame.MIN_FONT (56) in Manim's default font, in frame units
# (docs/tech/layout.md). Use for planning; kit.text() measures exactly.
DIGIT_W = 0.48       # one digit: "4800" = 1.90
LINE_H = 0.59        # cap height + descender of one line
MAX_CHARS = 17       # at MIN_FONT, ~17 characters fill the safe width (8.0)


# ---- placing text -----------------------------------------------------------

def text(s: str, x: float, baseline: float, color=frame.INK,
         size: int = frame.MIN_FONT, align: str = "center") -> Text:
    """Text on a BASELINE, centred on x (align="left": starting at x).

    Centring by middle or top puts "turret" and "reticle" (or "Triumph"
    and "SLx") at different heights; a baseline never does. An "H" is set
    after the text to find the baseline (its bottom), then taken away.
    """
    t = Text(s + "H", font_size=size, color=color)
    h = t[-1]
    t.shift((0, baseline - h.get_bottom()[1], 0))
    t.remove(h)
    dx = x - {"center": t.get_center()[0], "left": t.get_left()[0],
              "right": t.get_right()[0]}[align]
    return t.shift((dx, 0, 0))


def title(s: str, color=frame.INK) -> Text:
    """The slide's title, its TOP on frame.TOP, shrunk (never below
    MIN_FONT) until it fits the safe width. A centred title at TOP - 0.3
    pokes 0.23 above TOP; "Range by width" at 80 is wider than the frame."""
    size = frame.TITLE_FONT
    t = Text(s, font_size=size, color=color)
    while t.width > 2 * frame.SIDE and size > frame.MIN_FONT:
        size -= 4
        t = Text(s, font_size=size, color=color)
    return t.move_to((0, frame.TOP - t.height / 2, 0))


def fits(s: str, size: int = frame.MIN_FONT) -> float:
    """Width of a string in frame units -- measure before laying out."""
    return Text(s, font_size=size).width


# ---- geometry ---------------------------------------------------------------

def toward(turns: float) -> tuple[float, float, float]:
    """A direction from a fraction of a full circle: 0 = up, clockwise.
    Rounded: sin(pi) is 1.2e-16, which next_to() reads as "to the right"
    and shifts a label sideways."""
    a = 2 * math.pi * turns
    return (round(math.sin(a), 9), round(math.cos(a), 9), 0.0)


# ---- the steps, on the words ------------------------------------------------

def run(scene, here: Path, steps, beat_lines, run_times, background=(),
        beat_words=None):
    """Add the background, play each step on its word (`beat_words`) or
    its sentence (`beat_lines`), hold to the end of the words, then check
    the still. `background` is what is on screen before the first word
    (title, grid...): it may lie under other things."""
    scene.add(*background)
    p = beats.for_scene(here, beat_lines, run_times, beat_words)
    for wait, step, rt in zip(p.waits, steps, run_times):
        if wait >= beats.MIN_WAIT:
            scene.wait(wait)
        scene.play(*step(), run_time=rt)
    if p.tail >= beats.MIN_WAIT:
        scene.wait(p.tail)
    for note in check(scene.mobjects, under=background):
        print(f"[layout] {note}", file=sys.stderr)


# ---- the check --------------------------------------------------------------

# Closer than this counts as touching, frame units. Two stacked lines of
# one label at MIN_FONT sit 0.05 apart and read fine (zero-clicks).
GAP = 0.03


def _leaves(mobs):
    """Text stays whole; groups are opened; anything else is one piece."""
    for m in mobs:
        if isinstance(m, Text):
            yield m
        elif type(m) in (VGroup, Group) or (type(m) is Mobject):
            yield from _leaves(m.submobjects)
        else:
            yield m


def _box(m):
    (l, b, _), (r, t, _) = m.get_corner((-1, -1, 0)), m.get_corner((1, 1, 0))
    return l, b, r, t


def _name(m) -> str:
    if isinstance(m, Text):
        return f'"{getattr(m, "original_text", m.text)}"'
    return type(m).__name__


def _overlap(a, b, gap=GAP) -> bool:
    return (a[0] < b[2] + gap and b[0] < a[2] + gap and
            a[1] < b[3] + gap and b[1] < a[3] + gap)


def check(mobs, under=()) -> list[str]:
    """The frame rules, on what is on screen:
      - nothing above TOP, below BOTTOM (captions) or past SIDE;
      - no text touching other text;
      - no text touching a drawing, unless the drawing is `under` (a grid).
    Boxes, not shapes: a diagonal arrow's box is big, so "touches a
    drawing" can be a false alarm -- look at the still before moving it.
    """
    skip = {id(x) for x in _leaves(under)}
    leaves = [m for m in _leaves(mobs) if m.has_points() or isinstance(m, Text)]
    notes = []
    for m in leaves:
        l, b, r, t = _box(m)
        if t > frame.TOP + 1e-6:
            notes.append(f"{_name(m)} is {t - frame.TOP:.2f} above TOP")
        if b < frame.BOTTOM - 1e-6:
            notes.append(f"{_name(m)} is {frame.BOTTOM - b:.2f} into the caption zone")
        if l < -frame.SIDE - 1e-6 or r > frame.SIDE + 1e-6:
            notes.append(f"{_name(m)} is past SIDE ({l:.2f}..{r:.2f})")
    texts = [m for m in leaves if isinstance(m, Text)]
    for i, a in enumerate(texts):
        for c in texts[i + 1:]:
            if _overlap(_box(a), _box(c)):
                notes.append(f"{_name(a)} touches {_name(c)}")
        for d in leaves:
            if isinstance(d, Text) or id(d) in skip:
                continue
            if _overlap(_box(a), _box(d), gap=0):
                notes.append(f"{_name(a)} touches a {_name(d)}")
    return notes

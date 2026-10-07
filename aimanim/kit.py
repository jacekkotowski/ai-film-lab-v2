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

import numpy as np
from manim import (Arrow, Circle, Dot, Group, Line, Mobject, RoundedRectangle,
                   Text, VGroup, VMobject)

from aimanim import aurora as _aurora
from aimanim import beats, frame
# plain geometry (stdlib, tested): scenes call them as kit.<name>
from aimanim.layout import (ASCENT, DESCENT, area_radius, columns,  # noqa: F401
                            fit_scale, grid_points, label_side, pitch_for,
                            row_step, stack)

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


# ---- the Aurora MIL reticle and the measuring chain -------------------------
# Every slide about the reticle draws it from aimanim/aurora.py through
# these, so the slides cannot drift apart. Reference stills of the whole
# reticle and its enlarged parts: docs/aurora/ (README.md says which is which).

def mil_to(scale: float, aim) -> callable:
    """A function (x, y) in mil -> a point on the slide: the aim point
    (chevron tip) at `aim`, `scale` frame units per mil."""
    def at(x, y):
        return (aim[0] + x * scale, aim[1] + y * scale, 0)
    return at


def reticle(at, window=None, stroke=3, dot_r=0.035, heavy=1.8,
            numbers=True, color=frame.INK) -> VGroup:
    """The Aurora MIL reticle, to scale: VGroup(lines, dots, numbers).
    `window` = (x0, x1, y0, y1) in mil draws only that part (enlargements).
    Sizes that read on the phone: whole reticle at 0.27/mil -> stroke 3,
    dot_r 0.035 (zero-reticle); centre at 1.6/mil -> stroke 6, dot_r 0.08
    (zero-range)."""
    lines = [Line(at(*a), at(*b)) for a, b in _aurora.segments(window)]
    if window is None or (window[0] <= 0 <= window[1] and window[2] <= 0 <= window[3]):
        lines.append(VMobject().set_points_as_corners([at(*p) for p in _aurora.chevron()]))
    dots = [Dot(at(x, y), radius=dot_r * (heavy if h else 1), color=color)
            for x, y, h in _aurora.dots(window)]
    nums = []
    if numbers:
        for side in (-1, 1):
            for x, s in _aurora.NUMBERS.items():
                if window is None or window[0] <= side * x <= window[1]:
                    nums.append(text(s, at(side * x, 0)[0],
                                     at(0, _aurora.stadia_mil(x) / 2)[1] + 0.12, color))
    return VGroup(VGroup(*lines).set_stroke(color, width=stroke),
                  VGroup(*dots), VGroup(*nums))


def man(height: float, feet, color=frame.ACCENT, width: float = 0.2) -> VGroup:
    """A standing man, `height` frame units tall from `feet` (x, y) up to
    the top of his head: head 0.13 of the height, body `width` of it."""
    head_r = height * 0.065
    body_h = height - 2 * head_r - height * 0.02
    body = RoundedRectangle(width=height * width, height=body_h,
                            corner_radius=min(height * 0.08, body_h / 2))
    body.move_to((feet[0], feet[1] + body_h / 2, 0))
    head = Circle(radius=head_r).move_to((feet[0], feet[1] + height - head_r, 0))
    return VGroup(body, head).set_fill(color, opacity=0.8).set_stroke(width=0)


# The worked example in one picture language for the whole film:
# TARGET -> MIL READING -> FORMULA -> RESULT, top to bottom.
CHAIN_COLORS = (frame.ACCENT, frame.SECOND, frame.INK, frame.ACCENT)
CHAIN_STEP = 1.25     # baseline to baseline at MIN_FONT: arrows 0.35 long
# ASCENT 0.59 / DESCENT 0.17 at MIN_FONT ("per second", "7.2 km/h"):
# from layout.py, with the rest of the plain geometry.


def chain(items, top_baseline: float, x: float = 0.0, step: float = CHAIN_STEP,
          colors=CHAIN_COLORS, size: int = frame.MIN_FONT) -> VGroup:
    """Rows of text, one under the other, a short arrow between each.
    Returns VGroup(row 0, row 1, ...); row i > 0 is VGroup(arrow, text),
    so each row can appear on its own word. The arrows are placed from the
    baselines, not the text boxes, so all are equally long whether a row
    has a descender ("per") or not; at step 1.1 a box-placed arrow under
    "10 MIL per second" shrank to a dot (mil-speed)."""
    k = size / frame.MIN_FONT
    below, above = DESCENT * k + 0.06, ASCENT * k + 0.08   # clear of both rows
    rows = []
    for i, s in enumerate(items):
        b = top_baseline - i * step
        t = text(s, x, b, colors[i % len(colors)], size)
        if i == 0:
            rows.append(VGroup(t))
            continue
        a = Arrow((x, b + step - below, 0), (x, b + above, 0), buff=0,
                  stroke_width=4, color=frame.DIM,
                  max_tip_length_to_length_ratio=0.5, tip_length=0.15)
        rows.append(VGroup(a, t))
    return VGroup(*rows)


# ---- populations: thousands of people, one shape -----------------------------
# A slide about a test counts people: 10,000 pregnancies, 499 false alarms.
# One Dot per person is 10,000 mobjects; one VMobject whose subpaths are
# the dots draws in one go and moves (Transform, shift) as one object.
# Screening film, 2026-10-06. One dot is one person, always: a picture
# that shows 9,481 shows 9,481 (binary-diagnostics skill).

_K = 0.5523          # cubic Bezier handle for a quarter circle
# grid_points (and pitch_for, to choose the pitch): layout.py


def _ellipses(points, rx: float, ry: float) -> np.ndarray:
    one = np.array([[1, 0], [1, _K], [_K, 1], [0, 1],
                    [0, 1], [-_K, 1], [-1, _K], [-1, 0],
                    [-1, 0], [-1, -_K], [-_K, -1], [0, -1],
                    [0, -1], [_K, -1], [1, -_K], [1, 0]], dtype=float) * (rx, ry)
    c = np.asarray(points, dtype=float).reshape(-1, 1, 2)
    xy = (c + one).reshape(-1, 2)
    return np.column_stack([xy, np.zeros(len(xy))])


def dots(points, radius: float, color=frame.HEALTHY, opacity: float = 1.0) -> VMobject:
    """One filled circle at each point, all ONE VMobject."""
    m = VMobject()
    if len(points):
        m.set_points(_ellipses(points, radius, radius))
    return m.set_fill(color, opacity).set_stroke(width=0)


def people(points, height: float, color=frame.HEALTHY, opacity: float = 1.0) -> VMobject:
    """A small standing figure centred on each point, ONE VMobject: a
    round head over an oval body. 16 points for the head, 16 for the body."""
    # head 0.2 of the height, body 1.5 heads wide: at 0.17 and 1.1 the
    # 499 of scr-cost read as thin ovals at 1080x1920
    pts = np.asarray(points, dtype=float).reshape(-1, 2)
    head_r = 0.2 * height
    body_h = height - 2 * head_r - 0.06 * height
    heads = _ellipses(pts + (0, height / 2 - head_r), head_r, head_r)
    bodies = _ellipses(pts + (0, -height / 2 + body_h / 2), head_r * 1.5, body_h / 2)
    m = VMobject()
    if len(pts):
        m.set_points(np.concatenate([heads.reshape(-1, 16, 3),
                                     bodies.reshape(-1, 16, 3)], axis=1).reshape(-1, 3))
    return m.set_fill(color, opacity).set_stroke(width=0)


def box(left: float, bottom: float, right: float, top: float,
        color=frame.ACCENT, width: float = 5) -> VGroup:
    """A rectangle as four Lines: lights a column or a row of a table.
    A Rectangle is one box to the layout check, so every text inside it
    would be reported as touching it; four thin lines are not."""
    c = [(left, bottom, 0), (right, bottom, 0), (right, top, 0), (left, top, 0)]
    return VGroup(*[Line(c[i], c[(i + 1) % 4]) for i in range(4)]).set_stroke(color, width)


def ring(points, radius: float, color=frame.SICK, width: float = 4) -> VGroup:
    """Rings around a few items in a crowd so they can be found on a phone:
    2 red among 9,483 were invisible without (scr-meaning; issue I12).
    radius ≈ 3 × the crowd's pitch."""
    return VGroup(*[Circle(radius=radius).move_to((x, y, 0)).set_stroke(color, width)
                    for x, y in points])


def strike(t: Mobject, color=frame.SECOND, width: float = 6) -> Line:
    """A line through a text, corner to corner of its middle band:
    "9 in 10" crossed out."""
    l, r = t.get_left()[0] - 0.1, t.get_right()[0] + 0.1
    y = t.get_center()[1]
    line = Line((l, y - 0.12, 0), (r, y + 0.12, 0)).set_stroke(color, width)
    line.strikes = t          # the layout check expects it on this text
    return line


# ---- the steps, on the words ------------------------------------------------

def run(scene, here: Path, steps, beat_lines, run_times, background=(),
        beat_words=None):
    """Add the background, play each step on its word (`beat_words`) or
    its sentence (`beat_lines`), hold to the end of the words, then check
    the still. `background` is what is on screen before the first word
    (title, grid...): it may lie under other things."""
    scene.add(*background)
    p = beats.for_scene(here, beat_lines, run_times, beat_words)
    # Waits in whole frames (beats.in_frames): Manim rounds each wait down,
    # and the clips came out up to 4.6 frames short. n + 0.5 frames of
    # seconds is drawn as exactly n frames.
    waits, tail = beats.in_frames(p, run_times, frame.FPS)
    for n, step, rt in zip(waits, steps, run_times):
        if n:
            scene.wait((n + 0.5) / frame.FPS)
        scene.play(*step(), run_time=rt)
    if tail:
        scene.wait((tail + 0.5) / frame.FPS)
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
            if isinstance(d, Text) or id(d) in skip or getattr(d, "strikes", None) is a:
                continue
            if _overlap(_box(a), _box(d), gap=0) and _hits(_box(a), d):
                notes.append(f"{_name(a)} touches a {_name(d)}")
    return notes


# A stroke-only line is checked along its path, not by its box: the box of
# a diagonal (mil-angle's cone) covers labels the line never comes near,
# and gave 4 false notes. Filled shapes (dots, tips, discs) keep their box.
SAMPLE_STEP = 0.05     # frame units between samples along a curve
STROKE_PAD = 0.02      # half a stroke, roughly, in frame units


def _hits(box, d) -> bool:
    l, b, r, t = box
    for m in d.family_members_with_points():
        if m.get_fill_opacity() > 0.01:
            if _overlap(box, _box(m), gap=0):
                return True
            continue
        pts = m.points[: len(m.points) // 4 * 4].reshape(-1, 4, 3)
        for p0, p1, p2, p3 in pts:
            n = max(9, int(np.linalg.norm(p3 - p0) / SAMPLE_STEP) + 2)
            s = np.linspace(0, 1, n)[:, None]
            c = ((1 - s) ** 3 * p0 + 3 * (1 - s) ** 2 * s * p1
                 + 3 * (1 - s) * s ** 2 * p2 + s ** 3 * p3)
            x, y = c[:, 0], c[:, 1]
            if np.any((x >= l - STROKE_PAD) & (x <= r + STROKE_PAD)
                      & (y >= b - STROKE_PAD) & (y <= t + STROKE_PAD)):
                return True
    return False


# ---- the command line: measure and plan before drawing --------------------------

def _cli(argv: list[str]) -> int:
    """python -m aimanim.kit fits "text" "text@72" ...   (measures, and keeps
    every width in docs/tech/sizes.json; read it without Manim:
    python -m aimanim.layout sizes [part of a text])"""
    from aimanim import layout
    try:
        sys.stdout.reconfigure(encoding="utf-8")      # "≈", "×" on Windows
    except AttributeError:
        pass
    if argv[:1] == ["fits"]:
        found = {}
        for a in argv[1:]:
            s, _, size = a.rpartition("@") if "@" in a else (a, "", "")
            size = int(size) if size else frame.MIN_FONT
            t = Text(s, font_size=size)
            found[(s, size)] = (t.width, t.height)
            print(f"{t.width:6.2f}  {'TOO WIDE ' if t.width > 2 * frame.SIDE else ''}"
                  f"{s!r} at {size}")
        layout.remember_sizes(found)
        return 0
    if argv[:1] == ["stack"]:
        return layout.main(argv)
    print(_cli.__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))

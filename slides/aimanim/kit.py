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
from functools import lru_cache
from pathlib import Path

import numpy as np
from manim import (BOLD, NORMAL, PI, Arc, Arrow, Circle, DashedLine, Dot, Group,
                   Line, Mobject, Polygon, Rectangle, RoundedRectangle, Text,
                   VGroup, VMobject)

from aimanim import aurora as _aurora
from aimanim import beats, frame
from aimanim import physics as _physics
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
         size: int = frame.MIN_FONT, align: str = "center",
         font: str = "", weight: str = NORMAL) -> Text:
    """Text on a BASELINE, centred on x (align="left": starting at x).

    Centring by middle or top puts "turret" and "reticle" (or "Triumph"
    and "SLx") at different heights; a baseline never does. An "H" is set
    after the text to find the baseline (its bottom), then taken away.
    `font` "" and `weight` NORMAL are Manim's own defaults.
    """
    t = Text(s + "H", font_size=size, color=color, font=font, weight=weight)
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


@lru_cache(maxsize=None)
def cap(size: int = frame.MIN_FONT, font: str = "") -> float:
    """Height of a capital H in frame units (Consolas at 56: 0.50)."""
    return Text("H", font_size=size, font=font).height


def wrap(s: str, width: float, size: int = frame.MIN_FONT, font: str = "",
         weight: str = NORMAL) -> list[str]:
    """`s` as lines no wider than `width`, broken between words; a "\\n"
    in `s` always breaks. Measured, not counted: at 56 a line of 17
    characters may or may not fit 8.0. A word wider than `width` stays
    whole (the check then reports it past SIDE)."""
    out = []
    for part in s.split("\n"):
        line = ""
        for w in part.split(" "):
            t = f"{line} {w}" if line else w
            if line and Text(t, font_size=size, font=font, weight=weight).width > width:
                out.append(line)
                line = w
            else:
                line = t
        out.append(line)
    return out


def paragraph(s: str, x: float, baseline: float, width: float = 2 * frame.SIDE,
              color=frame.INK, size: int = frame.MIN_FONT, align: str = "center",
              font: str = "", weight: str = NORMAL, step: float | None = None) -> VGroup:
    """`s` wrapped to `width` (kit.wrap), the first line on `baseline`,
    each next one layout.row_step lower; align as kit.text. His words
    stay whole: a long sentence becomes two or three lines, never smaller."""
    step = step or row_step(size)
    return VGroup(*[text(line, x, baseline - i * step, color, size, align, font, weight)
                    for i, line in enumerate(wrap(s, width, size, font, weight))])


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


def replay(m: Mobject, frames, body: int = 0, fps: int = frame.FPS) -> Mobject:
    """Move `m` along body number `body` of `frames` (aimanim.physics.track)
    from the moment of this call, one recorded frame per film frame, and
    leave it on the last one. Call it inside a step, then return an
    animation of that step's run time (the updater runs while it plays)."""
    clock = [0.0]

    def follow(mob, dt):
        clock[0] += dt
        x, y, _ = _physics.at(frames, clock[0], fps)[body]
        mob.move_to((x, y, 0))

    m.move_to((*frames[0][body][:2], 0))
    m.add_updater(follow)
    return m


# ---- map and calculator: "Map and Calculator 01 - Observer" -----------------
# His plan (film/docs/plans/2026-10-11/PLAN-map-calculator.md) keeps the look
# of his pan boards: dark ground, green accent, the colours of
# slides/boards/pan_kit.py (its names in the comments). Space Grotesk and
# JetBrains Mono are not installed (docs/OPEN.md): Segoe UI and Consolas are
# pan_kit's own offline fallbacks. Every text is at least MIN_FONT except the
# series tag, SERIES_FONT: at 56 it is 17.0 wide (Jacek's yes, 2026-10-11).
# A slide shows these one after another on his words: at 56 the busiest
# slide of the plan needs about 20 units of height, the frame has 11.

SANS, MONO = "Segoe UI", "Consolas"
SERIES_FONT = 26
GROUND = "#0E1416"            # BG   the slide: self.camera.background_color
PAPER = "#F2F4F1"             # TX   text
MUTED = "#A3AFAB"             # MU   tags, sublines, numbers of the grid
RULE = "#2A3633"              # LN   the edge of a card
GREEN = "#5BD394"             # GRT  right, the answer
GREEN_DARK = "#1B7F47"        # GR   a lit key
AMBER = "#F5B83D"             # AM   take care; angles
ORANGE = "#FF8F57"            # OR   wrong
CARD_FILL = "#151E1C"         # pan_kit card()
KEY_FILL, KEY_EDGE = "#18211F", "#3E4B48"     # pan_kit key()
LCD, LCD_INK, BEZEL = "#C7D1C1", "#1C2321", "#242C2A"
MAP_LINE = "#35564A"          # the kilometre grid
# A card or a screen 8.0 wide drew its edge 2 px past SIDE (look: margins
# 58 px < 60, measured 2026-10-11): the stroke is half outside the box.
BOX_W = 2 * frame.SIDE - 0.04


# The column of every slide of this film, as pan_kit.panel stacks it: the
# series tag, the step tag ("SLIDE 1 · A"), the headline, the subline, the
# footer (✓ green, ✗ orange, a caution amber, a plain note muted).
SERIES_B, STEP_B, HEAD_B = 6.75, 5.85, 4.85      # baselines
HEAD_FONT = 72


def series_tag(s: str) -> Text:
    """MAP AND CALCULATOR · 01 · OBSERVER, top left, at SERIES_FONT."""
    return text(s, -frame.SIDE, SERIES_B, MUTED, SERIES_FONT, "left", MONO)


def step_tag(s: str) -> Text:
    """SLIDE 1 · A, under the series tag, at 56."""
    return text(s, -frame.SIDE, STEP_B, MUTED, frame.MIN_FONT, "left", SANS)


def headline(s: str) -> VGroup:
    """Bold, left, wrapped: "Wrong mode, wrong answer" is two lines at 72."""
    return paragraph(s, -frame.SIDE, HEAD_B, color=PAPER, size=HEAD_FONT, align="left",
                     font=SANS, weight=BOLD)


def below(m: Mobject, size: int = frame.MIN_FONT, gap: float = 0.3) -> float:
    """The baseline of a first line `gap` under m (a headline of one or two lines)."""
    return m.get_bottom()[1] - gap - cap(size, SANS)


def note(s: str, baseline: float, color=MUTED) -> VGroup:
    """A subline or a footer: left, wrapped, at 56."""
    return paragraph(s, -frame.SIDE, baseline, color=color, align="left", font=SANS)


def under(m: Mobject) -> Mobject:
    """Mark a backing shape (a card, a screen, a keycap face) as meant to
    lie under text: kit.check does not report text on it (issue I11)."""
    for f in m.get_family():
        f.under = True
    return m


def _beside(s: str, p, d, clear: float, color, size: int = frame.MIN_FONT,
            font: str = SANS, pad: float = 0.15) -> Text:
    """Text centred in direction d from point p, its box `clear` + pad
    away from p: outside a dial's edge, a dot, an arc, or a line."""
    w, h = Text(s, font_size=size, font=font).width, cap(size, font)
    r = clear + w / 2 * abs(d[0]) + h / 2 * abs(d[1]) + pad
    cx, cy = p[0] + d[0] * r, p[1] + d[1] * r
    return text(s, cx, cy - h / 2, color, size, font=font)


# -- the calculator: keys and screen --

KEY_H = 1.0          # a keycap at 56: capitals 0.50, 0.25 above and below


def keycap(label: str, x: float, y: float, size: int = frame.MIN_FONT) -> VGroup:
    """One key centred on (x, y): a face on a darker lip (pan_kit's thick
    bottom border), the label in bold mono. VGroup(lip, face, label);
    kit.light(key) lights it on its word, kit.lit(key) at once."""
    k = size / frame.MIN_FONT
    t = text(label, x, y - cap(size, MONO) / 2, PAPER, size, font=MONO, weight=BOLD)
    w = max(t.width + 0.44 * k, 0.9 * k)
    face = RoundedRectangle(width=w, height=KEY_H * k, corner_radius=0.14 * k)
    face.move_to((x, y, 0)).set_fill(KEY_FILL, 1).set_stroke(KEY_EDGE, 4)
    lip = face.copy().shift((0, -0.08 * k, 0)).set_fill(KEY_EDGE, 1)
    return VGroup(under(lip), under(face), t)


def lit(key: VGroup, on: bool = True) -> VGroup:
    """A key lit (green) now, or dark again with on=False."""
    key[1].set_fill(GREEN_DARK if on else KEY_FILL, 1)
    key[1].set_stroke(GREEN if on else KEY_EDGE, 4)
    return key


def light(key: VGroup):
    """The animation of a key lighting up: one object moving."""
    return key[1].animate.set_fill(GREEN_DARK, 1).set_stroke(GREEN, 4)


def keys(labels, y: float, x: float = 0.0, sep: str = "→", then: str | None = None,
         width: float = 2 * frame.SIDE, size: int = frame.MIN_FONT,
         gap: float = 0.14, step: float = 1.3) -> VGroup:
    """Keycaps in a row centred on (x, y), `sep` between them ("→" one
    after another, "+" together); `then` is what they type, after "=", in
    green ("Rec("). Wider than `width`: two rows `step` apart, split where
    the longer row is shortest, the second starting with its `sep`
    ("SHIFT → MENU" / "→ 2 → 1": 9.0 wide in one row at 56).
    VGroup of the items in order; .caps = the keycaps (to light them)."""
    caps = [keycap(s, 0, 0, size) for s in labels]

    def sym(s, color=MUTED, font=SANS, weight=NORMAL):
        return text(s, 0, -cap(size, font) / 2, color, size, font=font, weight=weight)

    units = [[caps[0]]] + [[sym(sep), c] for c in caps[1:]]
    if then:
        units.append([sym("="), sym(then, GREEN, MONO, BOLD)])

    def span(items):
        return sum(m.width for m in items) + gap * (len(items) - 1)

    flat = [m for u in units for m in u]
    rows = [flat]
    if span(flat) > width:
        best = None
        for i in range(1, len(units)):
            a = [m for u in units[:i] for m in u]
            b = [m for u in units[i:] for m in u]
            worst = max(span(a), span(b))
            if best is None or worst < best[0]:
                best = (worst, [a, b])
        rows = best[1]
    for i, row in enumerate(rows):
        cx = x - span(row) / 2
        for m in row:
            m.shift((cx - m.get_left()[0], y - i * step, 0))
            cx += m.width + gap
    g = VGroup(*flat)
    g.caps = caps
    return g


def screen(expr: str = "", results=(), ind: str = "D", bad: bool = False,
           top: float = 0.0, x: float = 0.0, width: float = BOX_W,
           rows: int | None = None, size: int = frame.MIN_FONT) -> VGroup:
    """The calculator's display, no logo: a dark bezel, the screen
    (#C7D1C1), the angle unit top-left (D or R; bad=True rings it in
    orange), the expression on the first line, the results right-aligned
    under it; no results: a cursor bar after the expression. `rows` = how
    many result lines to make room for (default: as many as given, at
    least one), so the screens of one slide can share one size.
    VGroup; .ind .ring .expr .cursor .results name the parts (None if absent)."""
    k = size / frame.MIN_FONT
    h, step = cap(size, MONO), row_step(size)
    n = max(rows or len(results), 1)
    gl, gr, gt = x - width / 2 + 0.2, x + width / 2 - 0.2, top - 0.2   # the glass
    pad = 0.25
    ind_b = gt - pad - h
    expr_b = ind_b - step - 0.1
    res_b = [expr_b - step * (i + 1) for i in range(n)]
    gb = res_b[-1] - DESCENT * k - pad
    bezel = RoundedRectangle(width=width, height=top - gb + 0.2, corner_radius=0.3)
    bezel.move_to((x, (top + gb - 0.2) / 2, 0)).set_fill(BEZEL, 1).set_stroke(RULE, 3)
    glass = RoundedRectangle(width=gr - gl, height=gt - gb, corner_radius=0.12)
    glass.move_to((x, (gt + gb) / 2, 0)).set_fill(LCD, 1).set_stroke(width=0)
    g = VGroup(under(bezel), under(glass))
    g.ind = text(ind, gl + pad, ind_b, LCD_INK, size, "left", MONO, BOLD)
    g.add(g.ind)
    g.ring = None
    if bad:
        g.ring = RoundedRectangle(width=g.ind.width + 0.3, height=h + 0.3, corner_radius=0.08)
        g.ring.move_to((g.ind.get_center()[0], ind_b + h / 2, 0))
        g.add(under(g.ring.set_stroke(ORANGE, 6).set_fill(opacity=0)))
    g.expr = text(expr, gl + pad, expr_b, LCD_INK, size, "left", MONO) if expr else None
    if g.expr:
        g.add(g.expr)
    g.cursor, g.results = None, None
    if results:
        g.results = VGroup(*[text(r, gr - pad, b, LCD_INK, size, "right", MONO)
                             for r, b in zip(results, res_b)])
        g.add(g.results)
    else:
        left = g.expr.get_right()[0] + 0.1 if g.expr else gl + pad
        g.cursor = Rectangle(width=0.07, height=h * 1.15).set_fill(LCD_INK, 1).set_stroke(width=0)
        g.cursor.move_to((left + 0.035, expr_b + h * 0.5, 0))
        g.add(g.cursor)
    return g


def card(rows, top: float, hl: int | None = None, x: float = 0.0,
         width: float = BOX_W, size: int = frame.MIN_FONT, color=PAPER) -> VGroup:
    """pan_kit's mono card: one row under another, left-aligned, each
    wrapped to the card (a "\\n" breaks where it reads best: "ΔN = 20300
    − 21800" is 18 characters, about 7.66 at 56, the card holds 7.70);
    row `hl` in green on a light-green band. VGroup; .rows[i] = row i's lines."""
    k = size / frame.MIN_FONT
    h, step, pad = cap(size, MONO), row_step(size), 0.13
    left = x - width / 2
    b = top - pad - h
    groups, spans = [], []
    for i, row in enumerate(rows):
        weight = BOLD if i == hl else NORMAL
        lines = wrap(row, width - 2 * pad, size, MONO, weight)
        g = VGroup(*[text(s, left + pad, b - j * step, GREEN if i == hl else color,
                          size, "left", MONO, weight) for j, s in enumerate(lines)])
        last = b - (len(lines) - 1) * step
        spans.append((b + h, last - DESCENT * k))
        groups.append(g)
        b = last - step - 0.15
    bottom = spans[-1][1] - pad
    back = RoundedRectangle(width=width, height=top - bottom, corner_radius=0.18)
    back.move_to((x, (top + bottom) / 2, 0)).set_fill(CARD_FILL, 1).set_stroke(RULE, 3)
    parts = [under(back)]
    if hl is not None:
        t, bt = spans[hl][0] + 0.12, spans[hl][1] - 0.06
        band = Rectangle(width=width - 0.12, height=t - bt).move_to((x, (t + bt) / 2, 0))
        bar = Rectangle(width=0.04, height=t - bt).move_to((left + 0.07, (t + bt) / 2, 0))
        band.set_fill(GREEN, 0.16).set_stroke(width=0)
        bar.set_fill(GREEN, 1).set_stroke(width=0)
        parts += [under(band), under(bar)]
    out = VGroup(*parts, *groups)
    out.rows = groups
    return out


@lru_cache(maxsize=None)
def mono_w(size: int = frame.MIN_FONT) -> float:
    """One Consolas character's width (0.4216 at 56: 18 fill 8.0, measured
    2026-10-12, skill evidence-short)."""
    return Text("M" * 20, font_size=size, font=MONO).width / 20


def code_line(s: str, left: float, baseline: float, color=PAPER,
              size: int = frame.MIN_FONT) -> Text:
    """One line of code: its leading spaces become an indent of whole
    characters (Text drops them), so the columns of a sum line up."""
    n = len(s) - len(s.lstrip(" "))
    return text(s.lstrip(" "), left + n * mono_w(size), baseline, color, size, "left", MONO)


def code(lines, top: float, x: float = 0.0, width: float = BOX_W,
         size: int = frame.MIN_FONT, color=PAPER) -> VGroup:
    """A code card (The Social Reckoning, 2026-10-12): `lines` as written,
    indents kept, one under another on the card's fill. Each line at most
    18 characters at 56. VGroup(back, *lines); .lines[i] = line i,
    .left / .baselines[i] to put a changed line in its place (code_line)."""
    # | ) j reach past a text row: at row_step "5 * emoji +" touched
    # "30 * comment) |>" (sr-points, 2026-10-12); 0.1 more keeps them apart.
    k = size / frame.MIN_FONT
    h, step, pad = cap(size, MONO), row_step(size) + 0.1 * k, 0.13
    left = x - width / 2 + pad
    bases = [top - pad - 0.1 - h - i * step for i in range(len(lines))]
    bottom = bases[-1] - DESCENT * k - pad - 0.1
    back = RoundedRectangle(width=width, height=top - bottom, corner_radius=0.18)
    back.move_to((x, (top + bottom) / 2, 0)).set_fill(CARD_FILL, 1).set_stroke(RULE, 3)
    texts = [code_line(s, left, b, color, size) for s, b in zip(lines, bases)]
    out = VGroup(under(back), *texts)
    out.lines, out.left, out.baselines = texts, left, bases
    return out


FLOOR = frame.BOTTOM + 0.05   # panels stand on the bottom edge (Map and Calculator)


def stack_up(*mobs, floor: float = FLOOR, gap: float = 0.3) -> None:
    """Stand the mobjects one on another, the first on `floor`: a card, a
    screen, keys over a map. Was copied into six obs-/gun- scenes."""
    y = floor
    for m in mobs:
        m.shift((0, y - m.get_bottom()[1], 0))
        y = m.get_top()[1] + gap


def command(s: str, y: float, x: float = 0.0, size: int = 120, color=GREEN) -> VGroup:
    """pan_kit's big command ("RIGHT 60"): bold mono in an outline,
    centred on (x, y). "RIGHT 60" at 120 is 7.12 wide."""
    h = cap(size, MONO)
    t = text(s, x, y - h / 2, color, size, font=MONO, weight=BOLD)
    box = RoundedRectangle(width=t.width + 0.6, height=h + 0.7, corner_radius=0.2)
    box.move_to((t.get_center()[0], y, 0)).set_stroke(color, 6).set_fill(opacity=0)
    return VGroup(under(box), t)


# -- the compass, the two norths, the burst --

def compass(center, radius: float, needle: float, label: str | None = None,
            color=ORANGE, size: int = frame.MIN_FONT) -> VGroup:
    """A compass dial: a tick every 10° (longer every 30°), N E S W, and a
    needle from the centre to `needle` degrees (0 = north, clockwise) with
    its reading outside the dial ("61°")."""
    c = np.array([center[0], center[1], 0.0])
    ring = Circle(radius=radius).move_to(c).set_stroke(PAPER, 4)
    ticks = []
    for deg in range(0, 360, 10):
        u = np.array(toward(deg / 360))
        ticks.append(Line(c + (radius - (0.35 if deg % 30 == 0 else 0.18)) * u, c + radius * u))
    h = cap(size, SANS)
    letters = []
    for name, deg in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
        p = c + (radius - 0.8) * np.array(toward(deg / 360))
        letters.append(text(name, p[0], p[1] - h / 2, PAPER if name == "N" else MUTED,
                            size, font=SANS))
    u = np.array(toward(needle / 360))
    arrow = Arrow(c - 0.35 * u, c + (radius - 0.45) * u, buff=0, stroke_width=8,
                  color=color, tip_length=0.32, max_tip_length_to_length_ratio=0.2)
    pivot = Dot(c, radius=0.09, color=PAPER)
    reading = _beside(label or f"{needle:g}°", c, u, radius, color, size)
    return VGroup(ring, VGroup(*ticks).set_stroke(MUTED, 3), VGroup(*letters),
                  arrow, pivot, reading)


def norths(origin, length: float, angle: float,
           labels=("Grid\nnorth", "Magnetic\nnorth"), arc_label: str = "correction",
           arc_r: float = 0.45, size: int = frame.MIN_FONT) -> VGroup:
    """The two norths of a map's margin: grid north straight up from
    `origin`, magnetic north `angle` degrees from it (+ = east; drawn as
    given, the slide carries no number), the arc between them named. Each
    name sits beside its own tip, on its own side."""
    o = np.array([origin[0], origin[1], 0.0])
    m = np.array(toward(angle / 360))
    gtip, mtip = o + (0, length, 0), o + length * m
    kw = dict(buff=0, stroke_width=6, tip_length=0.3, max_tip_length_to_length_ratio=0.1)
    grid, mag = Arrow(o, gtip, color=PAPER, **kw), Arrow(o, mtip, color=ORANGE, **kw)
    s = 1 if angle >= 0 else -1          # magnetic north's side
    h = cap(size, SANS)
    out, inn = ("left", "right") if s > 0 else ("right", "left")
    gname = paragraph(labels[0], gtip[0] - s * 0.3, gtip[1] - h, color=PAPER, size=size,
                      align=inn, font=SANS)
    mname = paragraph(labels[1], mtip[0] + s * 0.3, mtip[1] - h, color=ORANGE, size=size,
                      align=out, font=SANS)
    arc = Arc(radius=arc_r * length, start_angle=PI / 2, angle=-math.radians(angle),
              arc_center=o).set_stroke(AMBER, 5)
    end = o + arc_r * length * m
    name = text(arc_label, end[0] + s * 0.3, end[1] - h / 2, AMBER, size, out, SANS)
    return VGroup(grid, mag, arc, gname, mname, name)


def burst_view(center, radius: float, mils: float, scale: float, side: int = -1,
               label: str | None = None, caption: str = "view through binoculars",
               size: int = frame.MIN_FONT) -> VGroup:
    """What the observer sees through binoculars: the field, the line on
    the target, the burst `mils` to one side (side=-1: left; `scale` frame
    units per mil), a bracket over the gap with its reading ("20 mils"),
    the caption under the field. The vertical line stops under the bracket
    so the reading never sits on it."""
    c = np.array([center[0], center[1], 0.0])
    field = Circle(radius=radius).move_to(c).set_stroke(MUTED, 4)
    yb = c[1] + 0.95                                  # the bracket
    cross = VGroup(Line(c + (-radius, 0, 0), c + (radius, 0, 0)),
                   Line(c + (0, -radius, 0), (c[0], yb - 0.35, 0))).set_stroke(PAPER, 3)
    target = Rectangle(width=0.5, height=0.32).move_to(c + (0, 0.16, 0))
    target.set_fill(PAPER, 1).set_stroke(width=0)
    bx = c[0] + side * mils * scale
    puff = VGroup(*[Circle(radius=r).move_to((bx + dx, c[1] + dy, 0))
                    for dx, dy, r in ((0, 0.3, 0.32), (-0.27, 0.18, 0.22),
                                      (0.27, 0.2, 0.24), (0.02, 0.6, 0.22))])
    puff.set_fill(ORANGE, 0.9).set_stroke(width=0)
    bracket = VGroup(Line((bx, yb, 0), (c[0], yb, 0)), Line((bx, yb, 0), (bx, yb - 0.2, 0)),
                     Line((c[0], yb, 0), (c[0], yb - 0.2, 0))).set_stroke(AMBER, 4)
    reading = text(label or f"{mils:g} mils", (bx + c[0]) / 2, yb + 0.2, AMBER, size, font=SANS)
    under_field = paragraph(caption, c[0], c[1] - radius - 0.3 - cap(size, SANS),
                            color=MUTED, size=size, font=SANS)
    return VGroup(field, cross, target, puff, bracket, reading, under_field)


# -- the map --

def map_grid(e0: int, e1: int, n0: int, n1: int, left: float, bottom: float,
             scale: float, km: int = 1000, size: int = frame.MIN_FONT):
    """A map sheet's kilometre grid, E e0..e1 and N n0..n1 in metres, its
    lower-left corner at (left, bottom), `scale` frame units per metre.
    The E numbers under the bottom edge, the N numbers left of the left
    edge, in kilometres as a sheet prints them (34 = E 34000); "E" ends
    the row of E numbers on the left, "N" heads the column. The lines are
    under (names may lie on them). Returns (VGroup, at): at(E, N) -> point."""
    def at(e, n):
        return (left + (e - e0) * scale, bottom + (n - n0) * scale, 0.0)

    lines = ([Line(at(e, n0), at(e, n1)) for e in range(e0, e1 + 1, km)]
             + [Line(at(e0, n), at(e1, n)) for n in range(n0, n1 + 1, km)])
    grid = under(VGroup(*lines).set_stroke(MAP_LINE, 3))
    h = cap(size, SANS)
    eb = bottom - 0.4 - h
    nums = [text(f"{e // 1000}", at(e, n0)[0], eb, MUTED, size, font=SANS)
            for e in range(e0, e1 + 1, km)]
    nums += [text(f"{n // 1000}", left - 0.2, at(e0, n)[1] - h / 2, MUTED, size, "right", SANS)
             for n in range(n0, n1 + 1, km)]
    widest = max(m.width for m in nums[len(range(e0, e1 + 1, km)):])
    nums.append(text("E", left - 0.6, eb, PAPER, size, "right", SANS, BOLD))
    nums.append(text("N", left - 0.2 - widest / 2, at(e0, n1)[1] + h / 2 + 0.3, PAPER, size,
                     font=SANS, weight=BOLD))
    return VGroup(grid, VGroup(*nums)), at


def map_point(at, e: float, n: float, name: str | None = None, color=GREEN,
              side: str = "right", clear: float | None = None,
              size: int = frame.MIN_FONT, r: float = 0.11) -> VGroup:
    """A place on the map: a dot and its name on `side` (right, left, up,
    down), `clear` from the dot's centre (default: the dot)."""
    p = at(e, n)
    parts = [Dot(p, radius=r, color=color)]
    if name:
        d = {"right": (1, 0), "left": (-1, 0), "up": (0, 1), "down": (0, -1)}[side]
        parts.append(_beside(name, p, d, r if clear is None else clear, color, size))
    return VGroup(*parts)


def map_line(at, p0, p1, label: str | None = None, color=PAPER, dashed: bool = False,
             side: int = 1, where: float = 0.5, width: float = 5,
             size: int = frame.MIN_FONT, label_color=None) -> VGroup:
    """A straight line between two map points (E, N): the azimuth line, a
    north or east leg. Its label at `where` along it (0 = p0), clear of
    the line on `side` (+1 = left of the way from p0 to p1)."""
    a, b = np.array(at(*p0)), np.array(at(*p1))
    line = (DashedLine if dashed else Line)(a, b).set_stroke(color, width)
    if not label:
        return VGroup(line)
    u = (b - a) / np.linalg.norm(b - a)
    m = a + (b - a) * where
    t = _beside(label, m, (-u[1] * side, u[0] * side), 0.0, label_color or color, size)
    return VGroup(line, t)


def azimuth_arc(at, p, az: float, radius: float, label: str | None = None,
                color=AMBER, north: bool = True, label_at: float | None = None,
                size: int = frame.MIN_FONT) -> VGroup:
    """The azimuth at map point p: from grid north (a dashed stub up)
    clockwise to `az` degrees, an arrowhead at its end, the label outside
    the arc at `label_at` degrees (default: its middle). The arrowhead is
    a triangle of its own: Manim's add_tip bends an Arc to meet it (a 0.7
    arc reached 0.87, measured 2026-10-11)."""
    c = np.array(at(*p))
    a = math.radians(az)
    arc = Arc(radius=radius, start_angle=PI / 2, angle=-a, arc_center=c).set_stroke(color, 5)
    end = c + radius * np.array([math.sin(a), math.cos(a), 0])
    t = np.array([math.cos(a), -math.sin(a), 0])          # clockwise tangent
    n = np.array([-t[1], t[0], 0])
    tip = end + 0.08 * t
    head = Polygon(tip, tip - 0.24 * t + 0.11 * n, tip - 0.24 * t - 0.11 * n)
    head.set_fill(color, 1).set_stroke(width=0)
    parts = [arc, head]
    if north:
        parts.append(DashedLine(c, c + (0, radius + 0.1, 0)).set_stroke(MUTED, 3))
    if label:
        d = toward((az / 2 if label_at is None else label_at) / 360)
        parts.append(_beside(label, c, d, radius, color, size))
    return VGroup(*parts)


# ---- the steps, on the words ------------------------------------------------

def run(scene, here: Path, steps, beat_lines, run_times, background=(),
        beat_words=None, check_each=False):
    """Add the background, play each step on its word (`beat_words`) or
    its sentence (`beat_lines`), hold to the end of the words, then check
    the still. `background` is what is on screen before the first word
    (title, grid...): it may lie under other things. check_each=True also
    checks the frame at the end of every step ("[layout] step n: ..."): a
    slide whose pieces replace each other is more than its last frame."""
    scene.add(*background)
    p = beats.for_scene(here, beat_lines, run_times, beat_words)
    # Waits in whole frames (beats.in_frames): Manim rounds each wait down,
    # and the clips came out up to 4.6 frames short. n + 0.5 frames of
    # seconds is drawn as exactly n frames.
    waits, tail = beats.in_frames(p, run_times, frame.FPS)
    for i, (n, step, rt) in enumerate(zip(waits, steps, run_times)):
        if n:
            scene.wait((n + 0.5) / frame.FPS)
        scene.play(*step(), run_time=rt)
        if check_each and i < len(steps) - 1:
            for note_ in check(scene.mobjects, under=background):
                print(f"[layout] step {i + 1}: {note_}", file=sys.stderr)
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
      - no text touching a drawing, unless the drawing is `under` (a grid)
        or marked by kit.under (a card, a screen, a keycap: text sits on them).
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
            if (isinstance(d, Text) or id(d) in skip or getattr(d, "under", False)
                    or getattr(d, "strikes", None) is a):
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

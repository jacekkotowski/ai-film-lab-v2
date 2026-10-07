"""layout.py -- the geometry every slide needs, as tested functions.

Each function here replaces arithmetic done by hand on several slides
(docs/patterns/ names which). Standard library only, so the
tests check it without Manim; kit.py re-exports the names scenes use.

All lengths are frame units (frame.py: 9 x 16, 120 px per unit at full size).
"""

from __future__ import annotations

import json
import math
import sys
from datetime import date
from pathlib import Path

from aimanim import frame

# Text at MIN_FONT (56), measured: tallest glyph 0.59 above the baseline,
# deepest descender 0.17 below ("per second", "healthy"). Scale with size.
ASCENT, DESCENT = 0.59, 0.17
# Two rows at 56 read as separate at 0.80 baseline to baseline; at 0.75
# (mil-finale) and 0.70 (scr-accuracy) a descender touched the row below.
ROW_GAP = 0.04


def k(size: int) -> float:
    return size / frame.MIN_FONT


def row_step(size: int = frame.MIN_FONT, below: int | None = None,
             gap: float = ROW_GAP) -> float:
    """Smallest baseline-to-baseline distance from a row at `size` down to
    a row at `below` (default the same) without the descender touching
    the capitals: DESCENT(size) + gap + ASCENT(below). 0.80 at 56/56."""
    below = size if below is None else below
    return round(DESCENT * k(size) + gap + ASCENT * k(below), 3)


def stack(items, top: float = frame.TOP, gap: float = 0.1) -> list[dict]:
    """Rows from `top` down, `gap` between one row's bottom and the next's
    top. An item is "title", a font size (a text row), ("block", height)
    for a drawing, or ("gap", h) for extra space. Returns per item its
    top, baseline (text) and bottom; the last dict is the room left above
    frame.BOTTOM (negative: it does not fit)."""
    rows, y = [], top
    for it in items:
        if isinstance(it, tuple) and it[0] == "gap":
            y -= it[1]
            continue
        if isinstance(it, tuple):
            rows.append({"item": f"block {it[1]}", "top": y, "bottom": y - it[1]})
            y -= it[1] + gap
            continue
        size = frame.TITLE_FONT if it == "title" else int(it)
        base = y - ASCENT * k(size)
        rows.append({"item": f"{it}", "top": y, "baseline": base,
                     "bottom": base - DESCENT * k(size)})
        y = base - DESCENT * k(size) - gap
    rows.append({"item": "free above BOTTOM",
                 "room": round(rows[-1]["bottom"] - frame.BOTTOM, 2)})
    return rows


def columns(widths, left: float = -frame.SIDE, right: float = frame.SIDE,
            gap: float = 0.3) -> list[tuple[float, float, float]]:
    """Split [left, right] into columns in proportion to `widths` (or
    `n` equal ones if an int), `gap` between them: [(left, right, centre)].
    Give the widths of the widest label (or drawing) each column holds,
    and every label fits its column by construction."""
    ws = [1.0] * widths if isinstance(widths, int) else list(widths)
    free = right - left - gap * (len(ws) - 1)
    scale = free / sum(ws)
    out, x = [], left
    for w in ws:
        r = x + w * scale
        out.append((round(x, 3), round(r, 3), round((x + r) / 2, 3)))
        x = r + gap
    return out


def pitch_for(n: int, width: float, height: float) -> tuple[float, int, int]:
    """The largest square pitch that fits n dots in width x height:
    (pitch, cols, rows). 10,000 in 8 x 4.5 -> 0.0597, 134 x 75."""
    p = math.sqrt(width * height / n)
    while True:
        cols = max(1, int(width / p + 1e-9))
        rows = math.ceil(n / cols)
        if rows * p <= height + 1e-9:
            return p, cols, rows
        p *= 0.995


def grid_points(n: int, cols: int, pitch: float, left: float, top: float,
                pitch_y: float | None = None) -> list[tuple[float, float]]:
    """Centres of `n` places, row by row from the top left: the first
    centre is (left + pitch/2, top - pitch_y/2). Width cols x pitch."""
    py = pitch if pitch_y is None else pitch_y
    return [(left + (i % cols + 0.5) * pitch, top - (i // cols + 0.5) * py)
            for i in range(n)]


def fit_scale(extent: float, room: float, margin: float = 0.0) -> float:
    """Units per domain unit so a drawing `extent` long (in its own units:
    mil, metres, %) fills `room` frame units, leaving `margin` for the
    labels outside it. The reticle at 0.27/mil, the plate at 1.1/mil."""
    return (room - margin) / extent


def area_radius(r0: float, ratio: float) -> float:
    """Radius of a circle whose AREA is `ratio` times one of radius r0:
    a prevalence 28.6 times smaller -> r0 / 5.35 (scr-rarity)."""
    return r0 * math.sqrt(ratio)


# ---- measured text sizes: one file, written by `kit fits` --------------------
# Widths were copied by hand into three skills and could drift; now every
# measurement goes here, with its date, and is read back without Manim.

SIZES = Path(__file__).resolve().parents[1] / "docs" / "tech" / "sizes.json"


def _key(s: str, size: int) -> str:
    return f"{s}@{size}"


def load_sizes(path: Path = SIZES) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def remember_sizes(found: dict, path: Path = SIZES, today: str | None = None) -> dict:
    """Merge {(text, size): (width, height)} into the file; returns it."""
    data = load_sizes(path)
    day = today or date.today().isoformat()
    for (s, size), (w, h) in found.items():
        data[_key(s, size)] = {"w": round(w, 2), "h": round(h, 2), "measured": day}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(sorted(data.items())), indent=1, ensure_ascii=False)
                    + "\n", encoding="utf-8")
    return data


def width(s: str, size: int = frame.MIN_FONT, path: Path = SIZES) -> float | None:
    """A measured width, or None: then measure it (`kit fits`)."""
    e = load_sizes(path).get(_key(s, size))
    return e["w"] if e else None


def main(argv: list[str]) -> int:
    """python -m aimanim.layout stack title 56 block:3.2 gap:0.3 56
       python -m aimanim.layout pitch 10000 8 4.5        (n, width, height)
       python -m aimanim.layout columns 3.12 2.9 [gap=0.3] (widest label per column)
       python -m aimanim.layout rows 56 [72]             (baseline step between rows)
       python -m aimanim.layout sizes [part of a text]   (widths measured by kit fits)"""
    cmd, args = (argv[0], argv[1:]) if argv else ("", [])
    if cmd == "stack":
        items = []
        for a in args:
            kind, _, v = a.partition(":")
            items.append((kind, float(v)) if v else a)
        for r in stack(items):
            print("  ".join(f"{key} {v:.2f}" if isinstance(v, float) else f"{v}"
                            for key, v in r.items()))
    elif cmd == "pitch":
        p, c, r = pitch_for(int(args[0]), float(args[1]), float(args[2]))
        print(f"pitch {p:.4f}  cols {c}  rows {r}  -> {c * p:.2f} x {r * p:.2f}  "
              f"(dot radius ~{p / 3:.3f})")
    elif cmd == "columns":
        gap = [float(a[4:]) for a in args if a.startswith("gap=")]
        ws = [float(a) for a in args if not a.startswith("gap=")]
        for i, (l, r, c) in enumerate(columns(ws, gap=gap[0] if gap else 0.3)):
            print(f"column {i}: {l:.2f} .. {r:.2f}  centre {c:.2f}  width {r - l:.2f}")
    elif cmd == "rows":
        sizes = [int(a) for a in args] or [frame.MIN_FONT]
        print(f"baseline step {row_step(sizes[0], sizes[-1]):.2f}")
    elif cmd == "sizes":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
        part = " ".join(args).lower()
        for key, e in load_sizes().items():
            if part in key.lower():
                s, _, size = key.rpartition("@")
                wide = "TOO WIDE " if e["w"] > 2 * frame.SIDE else ""
                print(f"{e['w']:6.2f} x {e['h']:.2f}  {wide}{s!r} at {size}  ({e['measured']})")
    else:
        print(main.__doc__)
        return 2
    return 0


def label_side(x: float, width: float) -> str:
    """Where a label `width` wide centred on x must be aligned so it stays
    inside SIDE: "center", or "left"/"right" pinned to the edge."""
    if x - width / 2 < -frame.SIDE:
        return "left"
    if x + width / 2 > frame.SIDE:
        return "right"
    return "center"


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

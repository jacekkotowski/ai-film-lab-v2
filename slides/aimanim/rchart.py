"""rchart.py -- where a data point of an R chart lands on the slide.

R (slides/r/slide_chart.R) writes <name>.png and <name>.json: the PNG's
size, the panel's box in its pixels (origin top-left) and the axis ranges
in the scales' own units (log10 for scale_x_log10). The scene shows the
PNG `width` units wide, centred at `center`; `at` gives the frame point of
a data value, so a Manim ring or arrow sits on the curve.

    c = rchart.load(HERE / "chart.json")
    x, y = rchart.at(c, 500, 0.0348, width=8.0, center=(0, 2))

Stdlib only (decision 0002).
"""

import json
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Chart:
    png: tuple[float, float]                       # width, height in px
    panel: tuple[float, float, float, float]       # left, top, right, bottom px
    x_range: tuple[float, float]                   # in transformed units
    y_range: tuple[float, float]
    x_log: bool = False
    y_log: bool = False


def _is_log(name: str) -> bool:
    # ggplot2 4 names it "log-10"; older ones "log10"
    return name.replace("-", "") == "log10"


def from_dict(d: dict) -> Chart:
    p = d["panel"]
    return Chart(tuple(d["png"]), (p["left"], p["top"], p["right"], p["bottom"]),
                 tuple(d["x_range"]), tuple(d["y_range"]),
                 _is_log(d.get("x_trans", "identity")),
                 _is_log(d.get("y_trans", "identity")))


def load(path: Path) -> Chart:
    return from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def pixel(c: Chart, x: float, y: float) -> tuple[float, float]:
    """The PNG pixel (from top-left) of the data point (x, y)."""
    tx = math.log10(x) if c.x_log else x
    ty = math.log10(y) if c.y_log else y
    left, top, right, bottom = c.panel
    (x0, x1), (y0, y1) = c.x_range, c.y_range
    return (left + (tx - x0) / (x1 - x0) * (right - left),
            bottom - (ty - y0) / (y1 - y0) * (bottom - top))


def at(c: Chart, x: float, y: float, width: float,
       center=(0.0, 0.0)) -> tuple[float, float]:
    """The frame point of the data point (x, y), the PNG shown `width`
    units wide with its centre at `center`."""
    px, py = pixel(c, x, y)
    k = width / c.png[0]
    return (center[0] + (px - c.png[0] / 2) * k,
            center[1] - (py - c.png[1] / 2) * k)

---
name: r-charts
description: A chart made in R (ggplot2) on a Manim slide, with Manim callouts -- rings, labels, arrows -- appearing on his words and sitting on the data. The measured settings (ragg PNG, DejaVu Serif 58 pt, 8 in at 240 dpi shown 8 units wide, frame colours), the panel-position JSON, the "SVG loses its text" trap, and the template slides/r/ + aimanim/rchart.py + scenes/r-ppv-curve. Use when Jacek wants a ggplot, an R chart, a plot of data, a curve or a map (leaflet) on a slide, or says "R", "ggplot", "chart from R".
---

# R charts: ggplot draws the chart, Manim draws what appears on his words

> Stage **slides/**: plain paths below (`r/`, `scenes/`, `aimanim/` ...) are under `slides/`; commands are written to run from the repo root.

Route chosen 2026-10-08 (docs/OPEN.md): ggplot → PNG + a JSON of where
its panel sits; the scene shows the PNG and puts Manim marks on data
points. The chart's own marks do not move; the callouts do, on the words.

## 1. The trap (measured, Manim 0.21)

A ggplot **SVG** in Manim loses every text (11 of 11: "Unsupported element
type: Text") and draws the transparent background white. Do not use SVG.

## 2. Make a chart

1. Copy `r/ppv_curve.R` to `r/<slug>.R`. Keep `source("slides/r/slide_chart.R")`,
   `+ theme_slide()` and the `slide_chart(p, out_dir, "chart")` call.
2. Run it (Rscript is not on PATH; R 4.6.1):
   ```
   "C:\Program Files\R\R-4.6.1\bin\Rscript.exe" slides/r/<slug>.R slides/scenes/<slug>
   ```
   → `scenes/<slug>/chart.png` (1920×1920, transparent) and `chart.json`
   (png size, panel box in px from top-left, x/y ranges in the scales'
   units, the transforms: `log-10` or `identity`).
3. In the scene (copy `scenes/r-ppv-curve/scene.py`):
   ```python
   CHART = rchart.load(HERE / "chart.json")
   chart = ImageMobject(str(HERE / "chart.png"))
   chart.scale_to_fit_width(CHART_W).move_to((*CHART_AT, 0))    # in background
   x, y = rchart.at(CHART, data_x, data_y, CHART_W, CHART_AT)   # a frame point
   ```
   Data values, not frame numbers: `rchart.at` takes the log of a log axis.
   Label positions too, in data units (`LABEL` in the template).

## 3. Settings that match the slides (measured 2026-10-08)

| setting | value | why |
|---|---|---|
| device | `ragg::agg_png`, transparent | svglite → §1 |
| size | 8 × 8 in at 240 dpi, shown `CHART_W = 8` units wide | 1920 px shown as 960 |
| font | DejaVu Serif, `base_size` 58 | cap height 71 px = MIN_FONT's |
| colours | `SLIDE$ink/accent/second/dim` in `slide_chart.R` | = `frame.py`; a test checks they agree |
| x labels | short: "1k", "10k" | "10,000" and "100" touched at 58 pt (first test) |
| place | the template's PNG spans y −3.8 … 4.2 | bottom margin 557 px ≥ 480 for captions |

The panel box: ggplot2 4 pops its viewports after drawing; `slide_chart`
calls `grid.force()` and finds the `panel*` viewport, then `deviceLoc`.

## 4. Check by eye (the layout check cannot)

`kit.check` sees Manim's texts, not what is inside the PNG. On every chart
slide, look at the full still (`look still <slug> full`) for:
- a Manim label crossing the curve or a grid line (template: "1 in 29"
  on the 20 % line, moved to 27 %);
- each ring centred on its point: compare with the grid lines' pixels.

## 5. Not built / not measured

- **Leaflet** (webshot2, Chrome present): not tried. A map needs
  "© OpenStreetMap contributors" on screen (tile policy). Add a section
  here after the first real map.
- Chart marks that move on the words (R computes, Manim draws points,
  bars, lines): build at the second slide that needs it (grow-skills).
- gganimate: not installed; it keeps its own clock, not his words.
- The clip of `r-ppv-curve` has not been rendered; only the still.

## 6. Growing this

A new chart type that worked → a line in §3 with the slide it came from.
A second chart needing the same R code → into `slide_chart.R`.

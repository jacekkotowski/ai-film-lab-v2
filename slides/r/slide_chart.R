# slide_chart.R -- a ggplot as a slide's picture, plus where its data sits.
#
# source() this, build a ggplot with theme_slide(), then
#   slide_chart(p, "scenes/<slug>", "chart")
# writes scenes/<slug>/chart.png and chart.json. The scene places the PNG
# with aimanim/rchart.py and puts Manim callouts on the data (r-charts skill).
#
# Settings measured 2026-10-08 (docs/OPEN.md): 8 x 8 in at 240 dpi shown
# 8 units wide in the slide; base_size 58 gives MIN_FONT's cap height (71 px).
# ragg, not svglite: Manim drops every <text> of a ggplot SVG.

suppressPackageStartupMessages({
  library(ggplot2)
  library(grid)
})

# Must agree with slides/aimanim/frame.py (tests/test_r_charts_use_the_frame_colours.py).
SLIDE <- list(
  background = "#101418",
  ink = "#E8E6E3",
  accent = "#F2B33D",
  second = "#5DADE2",
  dim = "#6B7178"
)

SLIDE_FONT <- "DejaVu Serif"
SLIDE_SIZE <- 58          # pt at 240 dpi, shown at half size -> 71 px cap height

theme_slide <- function(base_size = SLIDE_SIZE) {
  theme_minimal(base_size = base_size, base_family = SLIDE_FONT) +
    theme(
      text = element_text(colour = SLIDE$ink),
      axis.text = element_text(colour = SLIDE$ink),
      panel.grid.major = element_line(colour = SLIDE$dim, linewidth = 0.6),
      panel.grid.minor = element_blank(),
      plot.background = element_rect(fill = "transparent", colour = NA),
      panel.background = element_rect(fill = "transparent", colour = NA),
      plot.margin = margin(20, 40, 20, 20)
    )
}

# The panel's box in PNG pixels (origin top-left) and the axis ranges in
# the scales' own (transformed) units, e.g. log10 for scale_x_log10().
slide_chart <- function(p, out_dir, name = "chart",
                        width_in = 8, height_in = 8, dpi = 240) {
  dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
  png_path <- file.path(out_dir, paste0(name, ".png"))
  ragg::agg_png(png_path, width = width_in, height = height_in,
                units = "in", res = dpi, background = "transparent")
  print(p)
  # ggplot2 4 pops its viewports after drawing: force the tree back, then
  # find the panel's viewport by name.
  grid.force()
  vps <- grid.ls(viewports = TRUE, grobs = FALSE, print = FALSE)$name
  panel <- grep("^panel", vps, value = TRUE)[1]
  seekViewport(panel)
  lo <- deviceLoc(unit(0, "npc"), unit(0, "npc"), valueOnly = TRUE)
  hi <- deviceLoc(unit(1, "npc"), unit(1, "npc"), valueOnly = TRUE)
  invisible(dev.off())

  h_px <- height_in * dpi
  pp <- ggplot_build(p)$layout$panel_params[[1]]
  trans <- function(axis) {
    s <- p$scales$get_scales(axis)
    if (is.null(s)) "identity" else s$get_transformation()$name
  }
  info <- list(
    png = c(width_in * dpi, h_px),
    panel = list(left = lo$x * dpi, top = h_px - hi$y * dpi,
                 right = hi$x * dpi, bottom = h_px - lo$y * dpi),
    x_range = pp$x.range, y_range = pp$y.range,
    x_trans = trans("x"), y_trans = trans("y")
  )
  jsonlite::write_json(info, file.path(out_dir, paste0(name, ".json")),
                       auto_unbox = TRUE, digits = 8, pretty = TRUE)
  invisible(info)
}

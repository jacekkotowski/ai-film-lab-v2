# ppv_curve.R -- the template: how many flagged are truly sick, by how rare.
#
#   "C:\Program Files\R\R-4.6.1\bin\Rscript.exe" slides/r/ppv_curve.R slides/scenes/r-ppv-curve
#
# Run from the repo root. Copy this file for a new chart; keep the
# source() line, the theme_slide() and the slide_chart() call.
# Test of 2026-10-08 (docs/OPEN.md): 90 % caught, 5 % false alarms.

args <- commandArgs(trailingOnly = TRUE)
out_dir <- if (length(args)) args[1] else "slides/scenes/r-ppv-curve"
source("slides/r/slide_chart.R")

SENS <- 0.90
FPR <- 0.05

d <- data.frame(one_in = 10^seq(1, 4, length.out = 200))
d$ppv <- SENS / d$one_in / (SENS / d$one_in + FPR * (1 - 1 / d$one_in))

p <- ggplot(d, aes(one_in, ppv)) +
  geom_line(colour = SLIDE$accent, linewidth = 2.5) +
  scale_x_log10(breaks = c(10, 100, 1000, 10000),
                labels = c("10", "100", "1k", "10k")) +
  scale_y_continuous(labels = scales::label_percent(), limits = c(0, 0.7)) +
  labs(x = "1 in ...", y = NULL) +
  theme_slide()

slide_chart(p, out_dir, "chart")

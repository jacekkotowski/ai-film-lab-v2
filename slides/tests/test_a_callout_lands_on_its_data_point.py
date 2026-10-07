"""A Manim callout lands on the R chart's data point (aimanim/rchart.py),
and the R theme uses the slides' colours (slides/r/slide_chart.R)."""

import re
import unittest
from pathlib import Path

from aimanim import frame, rchart

# A 2000 x 1000 px picture, the panel from (200, 100) to (1800, 900).
CHART = rchart.from_dict({
    "png": [2000, 1000],
    "panel": {"left": 200, "top": 100, "right": 1800, "bottom": 900},
    "x_range": [1, 4], "y_range": [0, 1],
    "x_trans": "log-10", "y_trans": "identity"})


class ACalloutLandsOnItsDataPoint(unittest.TestCase):
    def test_the_panel_corners_are_the_ranges_ends(self):
        self.assertEqual(rchart.pixel(CHART, 10, 0), (200, 900))
        self.assertEqual(rchart.pixel(CHART, 10_000, 1), (1800, 100))

    def test_a_log_axis_puts_100_a_third_of_the_way(self):
        x, _ = rchart.pixel(CHART, 100, 0.5)
        self.assertAlmostEqual(x, 200 + 1600 / 3)

    def test_the_picture_centre_is_the_given_centre(self):
        # pixel (1000, 500) is the centre: x = 10**2.5, y = 0.5
        x, y = rchart.at(CHART, 10 ** 2.5, 0.5, width=8.0, center=(1.0, 2.0))
        self.assertAlmostEqual(x, 1.0)
        self.assertAlmostEqual(y, 2.0)

    def test_up_in_the_data_is_up_on_the_slide(self):
        _, low = rchart.at(CHART, 100, 0.1, width=8.0)
        _, high = rchart.at(CHART, 100, 0.9, width=8.0)
        self.assertGreater(high, low)
        # 0.8 of an 800 px panel = 640 px; 8 units per 2000 px
        self.assertAlmostEqual(high - low, 640 * 8 / 2000)

    def test_old_ggplot_names_log10_without_a_dash(self):
        self.assertTrue(rchart._is_log("log10"))
        self.assertFalse(rchart._is_log("identity"))


class TheRThemeUsesTheFrameColours(unittest.TestCase):
    def test_every_colour_in_slide_chart_R_is_frame_s(self):
        src = (Path(__file__).parents[1] / "r" / "slide_chart.R").read_text(encoding="utf-8")
        colours = dict(re.findall(r'(\w+) = "(#[0-9A-Fa-f]{6})"', src))
        self.assertEqual(colours, {
            "background": frame.BACKGROUND, "ink": frame.INK,
            "accent": frame.ACCENT, "second": frame.SECOND, "dim": frame.DIM})


if __name__ == "__main__":
    unittest.main()

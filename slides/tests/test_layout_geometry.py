"""aimanim/layout.py: the hand arithmetic of earlier slides, as functions.
Each expected value is what a slide used (or should have used)."""

import unittest

from aimanim import layout


class Rows(unittest.TestCase):
    def test_rows_at_56_need_080(self):
        # mil-finale touched at 0.75, scr-accuracy at 0.70
        self.assertAlmostEqual(layout.row_step(56), 0.80)
        self.assertGreater(layout.row_step(56), 0.75)

    def test_stack_reaches_the_bottom_or_says_so(self):
        rows = layout.stack(["title", 56, ("block", 1.76)])
        self.assertAlmostEqual(rows[1]["baseline"], 7.0 - 0.59 * 80 / 56 - 0.17 * 80 / 56
                               - 0.1 - 0.59, places=6)
        self.assertLess(layout.stack(["title", ("block", 12)])[-1]["room"], 0)


class Columns(unittest.TestCase):
    def test_columns_fill_the_safe_width_with_gaps(self):
        cols = layout.columns(2)
        self.assertEqual(cols[0][0], -4.0)
        self.assertEqual(cols[-1][1], 4.0)
        self.assertAlmostEqual(cols[1][0] - cols[0][1], 0.3)

    def test_columns_in_proportion_hold_their_labels(self):
        # "affected" 3.12 and "healthy" 2.90 (scr-outcomes)
        for (l, r, _), w in zip(layout.columns([3.12, 2.90]), [3.12, 2.90]):
            self.assertGreaterEqual(r - l, w)


class Dots(unittest.TestCase):
    def test_pitch_for_the_10000(self):
        p, cols, rows = layout.pitch_for(10_000, 8.0, 4.5)     # scr-accuracy
        self.assertEqual((cols, rows), (134, 75))
        self.assertAlmostEqual(p, 0.0597, places=4)
        self.assertGreaterEqual(cols * rows, 10_000)
        self.assertLessEqual(rows * p, 4.5)

    def test_grid_points_start_half_a_pitch_in(self):
        pts = layout.grid_points(3, 2, 1.0, 0.0, 0.0)
        self.assertEqual(pts, [(0.5, -0.5), (1.5, -0.5), (0.5, -1.5)])


class Scales(unittest.TestCase):
    def test_area_true_radius(self):
        self.assertAlmostEqual(layout.area_radius(1.0, 490 / 14_000), 0.187, places=3)

    def test_fit_scale(self):
        # +-14 mil of reticle in 8 units, no margin -> 0.2857/mil (0.27 used)
        self.assertAlmostEqual(layout.fit_scale(28, 8.0), 8 / 28)

    def test_label_side(self):
        self.assertEqual(layout.label_side(3.3, 1.34), "center")
        self.assertEqual(layout.label_side(3.5, 1.34), "right")
        self.assertEqual(layout.label_side(-3.9, 1.0), "left")


if __name__ == "__main__":
    unittest.main()

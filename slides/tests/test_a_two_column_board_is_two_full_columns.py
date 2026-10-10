"""boards/pan_kit.py: a board is 2160x1920, two 1080x1920 columns, A then B.

Made offline for any subject with an A -> B story (Excel, Power Query, R).
Pure text in, HTML out: no browser needed here. The render is
boards/render_png.py (headless Chrome)."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "boards"))

import pan_kit as pk  # noqa: E402


def board():
    return pk.board_body(pk.panel("S1 . A", "Left", "sub", ""), pk.panel("S1 . B", "Right", "sub", ""))


class ATwoColumnBoardIsTwoFullColumns(unittest.TestCase):
    def test_a_board_is_2160_by_1920(self):
        self.assertIn("width: 2160px; height: 1920px", board())

    def test_each_column_is_1080_by_1920(self):
        self.assertEqual(board().count("width: 1080px; height: 1920px"), 2)

    def test_the_file_name_is_the_board_title_with_underscores(self):
        self.assertEqual(pk.fname("01 Ctrl+T and name it"), "01_Ctrl_T_and_name_it")

    def test_one_page_per_board_and_an_index(self):
        with tempfile.TemporaryDirectory() as d:
            pk.set_series("R . 01")
            a, b = pk.panel("S1 . A", "A", "s", ""), pk.panel("S1 . B", "B", "s", "")
            made = pk.write_boards(d, [("01 One", a, b), ("02 Two", a, b)])
            self.assertEqual(made, ["01_One.html", "02_Two.html"])
            self.assertTrue(os.path.exists(os.path.join(d, "index.html")))
            with open(os.path.join(d, "01_One.html"), encoding="utf-8") as f:
                self.assertIn("R . 01", f.read())


class AMonoLineNeverWraps(unittest.TestCase):
    def test_a_short_line_keeps_the_full_size(self):
        self.assertEqual(pk.mono_size(["x <- 1"]), (29, True))

    def test_a_longer_line_gets_a_smaller_size_that_still_fits(self):
        size, fits = pk.mono_size(["a" * 50], pk.CODE_INNER)
        self.assertTrue(fits)
        self.assertLess(size, 29)
        self.assertLessEqual(50 * size * pk.MONO_EM, pk.CODE_INNER)

    def test_a_line_too_long_for_a_column_is_refused_not_wrapped(self):
        with self.assertRaises(ValueError):
            pk.code(["a" * 90])

    def test_code_is_escaped_so_an_r_pipe_or_arrow_is_text(self):
        out = pk.code(["x <- df %>% filter(a < 1 & b)"])
        self.assertIn("&lt;-", out)
        self.assertIn("&amp;", out)
        self.assertNotIn("<- df", out)

    def test_a_highlighted_line_is_marked(self):
        out = pk.code(["a", "b"], hl=(2,))
        self.assertEqual(out.count("rgba(245,184,61,0.16)"), 1)


class FontsWorkOffline(unittest.TestCase):
    def test_without_local_fonts_the_page_asks_google(self):
        with tempfile.TemporaryDirectory() as empty:
            self.assertIn("fonts.googleapis.com", pk.page("t", "", empty))

    def test_with_local_fonts_the_page_never_touches_the_network(self):
        with tempfile.TemporaryDirectory() as d:
            for n in ("SpaceGrotesk-Bold.ttf", "JetBrainsMono-Regular.ttf"):
                open(os.path.join(d, n), "wb").close()
            out = pk.page("t", "", d)
            self.assertNotIn("googleapis", out)
            self.assertIn("font-family:'Space Grotesk';font-weight:700", out)
            self.assertIn("font-family:'JetBrains Mono';font-weight:400", out)


if __name__ == "__main__":
    unittest.main()

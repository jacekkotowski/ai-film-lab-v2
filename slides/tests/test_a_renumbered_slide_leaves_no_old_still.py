import tempfile
import unittest
from pathlib import Path

from aimanim import aurora, film


class ARenumberedSlideLeavesNoOldStill(unittest.TestCase):

    def test_only_our_own_old_stills_are_named(self):
        with tempfile.TemporaryDirectory() as d:
            root, media = Path(d) / "repo", Path(d) / "media"
            for s in ("zero-reticle", "zero-range"):
                (root / "scenes" / s).mkdir(parents=True)
            media.mkdir()
            for n in ("04_zero-range.png", "04_zero-reticle.png",
                      "05_zero-range.png", "07_his-own.png", "rec_1.png"):
                (media / n).write_bytes(b"")
            f = film.parse("04 zero-reticle\n05 zero-range\n")
            self.assertEqual([p.name for p in film.stale_stills(media, f, root)],
                             ["04_zero-range.png"])


class TheAuroraMarksAreTheManualsNumbers(unittest.TestCase):

    def test_a_full_stadia_is_70_inches_at_its_distance(self):
        self.assertAlmostEqual(aurora.stadia_mil(6), 3.241, places=3)
        self.assertAlmostEqual(aurora.stadia_mil(14), 9.722, places=3)

    def test_a_178_cm_man_in_metres_rounded_to_10(self):
        self.assertEqual([aurora.man_metres(x) for x in (14, 12, 10, 8, 6)],
                         [180, 270, 370, 460, 550])

    def test_a_window_cuts_the_lines_to_the_centre(self):
        seg = aurora.segments((-1.3, 1.3, -4.4, 0.35))
        self.assertIn(((0, -4.4), (0, -0.9)), seg)          # the ladder, cut
        self.assertIn(((-0.625, -2), (0.625, -2)), seg)     # bar 2: 1.25 mil
        self.assertFalse(any(abs(a[0]) > 1.3 for a, b in seg))

import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from aimanim import film, frame


def tiny_png(path: Path, w: int, h: int) -> None:
    """A valid PNG header of the given size (the body is never read)."""
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    chunk = b"IHDR" + ihdr
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + chunk
                     + struct.pack(">I", zlib.crc32(chunk)))


class AFilmKeepsItsOrder(unittest.TestCase):

    def test_slides_are_named_by_their_picture_number(self):
        s = film.parse("# a comment\n02 zero-group\n\n05 zero-range  # last\n")
        self.assertEqual([x.name for x in s], ["02_zero-group", "05_zero-range"])

    def test_a_film_cannot_go_backwards_or_repeat_a_picture(self):
        with self.assertRaises(ValueError):
            film.parse("03 a\n02 b\n")
        with self.assertRaises(ValueError):
            film.parse("02 a\n02 b\n")
        with self.assertRaises(ValueError):
            film.parse("zero-group\n")

    def test_the_size_is_read_from_the_png_itself(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.png"
            tiny_png(p, 1080, 1920)
            self.assertEqual(film.png_size(p), (1080, 1920))

    def test_only_full_size_stills_are_gathered(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "films").mkdir()
            (root / "films" / "f.txt").write_text("02 big\n03 small\n04 none\n")
            for name, size in (("big", (frame.WIDTH, frame.HEIGHT)),
                               ("small", (540, 960))):
                img = root / "scenes" / name / "out" / "images" / "scene"
                img.mkdir(parents=True)
                tiny_png(img / "Slide_ManimCE_v0.21.0.png", *size)
            report = film.gather("f", root)
            got = sorted(p.name for p in (root / "films" / "f").iterdir())
            self.assertEqual(got, ["02_big.png"])
            self.assertIn("not full size", report[1])
            self.assertIn("NO SCENE", report[2])


if __name__ == "__main__":
    unittest.main()

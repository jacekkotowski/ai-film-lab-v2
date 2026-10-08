import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from aimanim import film


def tiny_png(path: Path, w: int, h: int) -> None:
    """A valid PNG header of the given size (the body is never read)."""
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    chunk = b"IHDR" + ihdr
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + chunk
                     + struct.pack(">I", zlib.crc32(chunk)))


SCRIPT = """ZEROING -- final script
[intro]
Zeroing comes down
to one division.

[01] 1. Find the centre (slide zero-group)
Fire four shots.

[02]
Divide each distance.

[outro]
Set the diopter.
---------------------
What changed: notes that are not narration.
"""

YAML = (
    "shots:\r\n"
    "  - id: s01\r\n"
    "    src: media/rec_1.mp4\r\n"
    "  - id: s02\r\n"
    "    src: media/01_zero-group.png\r\n"
    "    voice: media/voiceover.wav\r\n"
    "    in: 1.0\r\n"
    "  - id: s03\r\n"
    "    src: media/02_zero-clicks.png\r\n"
)


class AFilmKeepsItsOrder(unittest.TestCase):

    def test_slides_are_named_by_their_picture_number(self):
        f = film.parse("project: Zeroing a Rifle Sight  # the folder\n"
                       "01 zero-group\n\n04 zero-range  # last\n")
        self.assertEqual(f.project, "Zeroing a Rifle Sight")
        self.assertEqual([x.name for x in f.slides], ["01_zero-group", "04_zero-range"])

    def test_a_film_cannot_go_backwards_or_repeat_a_picture(self):
        for bad in ("03 a\n02 b\n", "02 a\n02 b\n", "zero-group\n"):
            with self.assertRaises(ValueError):
                film.parse(bad)

    def test_the_size_is_read_from_the_png_itself(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.png"
            tiny_png(p, 1080, 1920)
            self.assertEqual(film.png_size(p), (1080, 1920))


class TheWordsGoWhereTheWindowShowsThem(unittest.TestCase):

    def test_the_script_is_cut_into_its_sections_and_the_notes_left_out(self):
        parts = film.script_parts(SCRIPT)
        self.assertEqual(parts["intro"], "Zeroing comes down to one division.")
        self.assertEqual(parts["01"], "Fire four shots.")
        self.assertEqual(parts["outro"], "Set the diopter.")
        self.assertNotIn("notes", " ".join(parts.values()))

    def test_one_paragraph_per_picture_and_a_dash_for_a_silent_one(self):
        f = film.parse("01 zero-group\n02 zero-clicks\n03 zero-mil\n")
        self.assertEqual(film.narration_text(f, film.script_parts(SCRIPT)),
                         "Fire four shots.\n\nDivide each distance.\n\n-\n")


PHOTO_SCRIPT = """[01]
A slide.

[02] his photo
A photo.

[03]
Another slide.
"""


class APhotoBetweenSlidesGetsItsParagraph(unittest.TestCase):
    """film-lab gives paragraph n to picture n. A photo between two slides
    had no paragraph, so every paragraph after it landed one picture off
    (found 2026-10-08, Love as a Face-Threatening Act)."""

    def test_a_photo_between_slides_gets_its_own_paragraph(self):
        f = film.parse("01 a\n03 b\n")
        self.assertEqual(film.narration_text(f, film.script_parts(PHOTO_SCRIPT)),
                         "A slide.\n\nA photo.\n\nAnother slide.\n")

    def test_a_photo_with_no_words_keeps_its_place_with_a_dash(self):
        f = film.parse("01 a\n03 b\n")
        parts = film.script_parts("[01]\nA slide.\n[03]\nAnother slide.\n")
        self.assertEqual(film.narration_text(f, parts, photos=[2]),
                         "A slide.\n\n-\n\nAnother slide.\n")

    def test_the_photos_are_the_numbered_pictures_in_media_that_are_not_slides(self):
        f = film.parse("01 a\n03 b\n")
        with tempfile.TemporaryDirectory() as d:
            for name in ("01_a.png", "02_parents.jpg", "05_shack.JPEG",
                         "voiceover.wav", "notes.txt", "parents.jpg"):
                (Path(d) / name).write_bytes(b"")
            self.assertEqual(film.photos_in(Path(d), f), [2, 5])

    def test_a_photo_paragraph_without_its_photo_is_named(self):
        f = film.parse("01 a\n03 b\n")
        self.assertEqual(film.photos_missing(f, film.script_parts(PHOTO_SCRIPT), []), [2])
        self.assertEqual(film.photos_missing(f, film.script_parts(PHOTO_SCRIPT), [2]), [])


class AScriptWithNoIntroIsNamed(unittest.TestCase):
    """publish writes script_intro.txt only from an [intro] section; a
    script without one left the recording window with no intro text and
    said nothing (2026-10-08, Love as a Face-Threatening Act)."""

    def test_a_script_without_intro_or_outro_names_both(self):
        self.assertEqual(film.ends_missing(film.script_parts(PHOTO_SCRIPT)),
                         ["intro", "outro"])

    def test_a_script_with_both_names_none(self):
        parts = film.script_parts("[intro]\nHello.\n[01]\nA slide.\n[outro]\nBye.\n")
        self.assertEqual(film.ends_missing(parts), [])


class AClipGoesOnItsSlide(unittest.TestCase):

    def test_the_clip_line_goes_under_its_own_slide_and_keeps_crlf(self):
        out = film.with_clip(YAML, "media/02_zero-clicks.png", "clips/02_zero-clicks.mp4")
        self.assertTrue(out.endswith("    src: media/02_zero-clicks.png\r\n"
                                     "    clip: clips/02_zero-clicks.mp4\r\n"))
        self.assertEqual(out.count("clip:"), 1)

    def test_adding_it_twice_changes_nothing(self):
        once = film.with_clip(YAML, "media/01_zero-group.png", "clips/01_zero-group.mp4")
        self.assertEqual(film.with_clip(once, "media/01_zero-group.png",
                                        "clips/01_zero-group.mp4"), once)
        self.assertIn("    src: media/01_zero-group.png\r\n"
                      "    clip: clips/01_zero-group.mp4\r\n"
                      "    voice: media/voiceover.wav\r\n", once)

    def test_a_picture_not_in_the_film_is_said(self):
        with self.assertRaises(LookupError):
            film.with_clip(YAML, "media/09_nothing.png", "clips/x.mp4")

    def test_the_slides_captions_become_the_timing_with_word_times(self):
        shot = {"id": "s02", "duration": 9.4, "captions": [
            {"text": "Fire four shots", "at": 1.0, "dur": 2.0, "words": [0.0, 0.4, 0.9]},
            {"text": "Mark the middle", "at": 5.0, "dur": 1.5, "words": []}]}
        t = film.timing_from(shot)
        self.assertEqual(t.total, 9.4)
        self.assertEqual([(x.start, x.end) for x in t.lines], [(1.0, 3.0), (5.0, 6.5)])
        self.assertEqual(t.lines[0].words, [1.0, 1.4, 1.9])


if __name__ == "__main__":
    unittest.main()

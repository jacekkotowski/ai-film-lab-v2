"""One name per film in all three stages: the slug of its film-lab folder
(film/ffilm/timeline.py `slug`, which fly/ also uses). slides/films/<slug>.txt,
film/projects/<Title>/, fly/projects/<slug>/."""
import tempfile
import unittest
from pathlib import Path

from aimanim import film


class AFilmIsNamedByTheSlugOfItsProject(unittest.TestCase):

    def test_the_slug_is_the_one_film_lab_writes(self):
        # the examples from film/ffilm/timeline.py and the films on disk
        self.assertEqual(film.slug("It Reads Us - We Can't Read It"),
                         "it-reads-us-we-can-t-read-it")
        self.assertEqual(film.slug("Screening - 95 Percent Accurate"),
                         "screening-95-percent-accurate")
        self.assertEqual(film.slug("Frankfurt School vs Kołakowski Emancipation and Domination"),
                         "frankfurt-school-vs-kolakowski-emancipation-and-domination")

    def test_a_film_file_named_otherwise_is_refused_with_the_right_name(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "films").mkdir()
            (root / "films" / "screening.txt").write_text(
                "project: Screening - 95 Percent Accurate\n01 scr-accuracy\n", encoding="utf-8")
            with self.assertRaises(SystemExit) as e:
                film.load("screening", root)
            self.assertIn("screening-95-percent-accurate", str(e.exception))

    def test_an_old_or_unknown_name_lists_the_films(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "films").mkdir()
            (root / "films" / "screening-95-percent-accurate.txt").write_text(
                "project: Screening - 95 Percent Accurate\n01 scr-accuracy\n", encoding="utf-8")
            (root / "films" / "screening-95-percent-accurate.script.txt").write_text("", encoding="utf-8")
            with self.assertRaises(SystemExit) as e:
                film.load("screening", root)
            self.assertIn("screening-95-percent-accurate", str(e.exception))
            self.assertNotIn(".script", str(e.exception))

    def test_a_film_file_named_by_the_slug_loads(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "films").mkdir()
            (root / "films" / "screening-95-percent-accurate.txt").write_text(
                "project: Screening - 95 Percent Accurate\n01 scr-accuracy\n", encoding="utf-8")
            f, _ = film.load("screening-95-percent-accurate", root)
            self.assertEqual(f.project, "Screening - 95 Percent Accurate")

    def test_every_film_in_the_repo_is_named_by_its_slug(self):
        for txt in sorted((film.ROOT / "films").glob("*.txt")):
            if txt.name.endswith(".script.txt"):
                continue
            with self.subTest(txt.name):
                f = film.parse(txt.read_text(encoding="utf-8"))
                self.assertEqual(txt.stem, film.slug(f.project))


if __name__ == "__main__":
    unittest.main()

"""One name per film in all three stages: the slug of its folder,
projects/<Title>/ (film/ffilm/timeline.py `slug`, which fly/ also uses)."""
import tempfile
import unittest
from pathlib import Path

from aimanim import film


def projects_with(base: Path, slides: str) -> Path:
    p = base / "projects" / "Screening - 95 Percent Accurate"
    p.mkdir(parents=True)
    (p / "slides.txt").write_text(slides, encoding="utf-8")
    (p / "slides.script.txt").write_text("", encoding="utf-8")
    return base / "projects"


class AFilmIsNamedByTheSlugOfItsProject(unittest.TestCase):

    def test_the_slug_is_the_one_film_lab_writes(self):
        # the examples from film/ffilm/timeline.py and the films on disk
        self.assertEqual(film.slug("It Reads Us - We Can't Read It"),
                         "it-reads-us-we-can-t-read-it")
        self.assertEqual(film.slug("Screening - 95 Percent Accurate"),
                         "screening-95-percent-accurate")
        self.assertEqual(film.slug("Frankfurt School vs Kołakowski Emancipation and Domination"),
                         "frankfurt-school-vs-kolakowski-emancipation-and-domination")

    def test_a_slides_file_naming_another_project_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            projects = projects_with(Path(d), "project: Screening\n01 scr-accuracy\n")
            with self.assertRaises(SystemExit) as e:
                film.load("screening-95-percent-accurate", projects)
            self.assertIn("Screening - 95 Percent Accurate", str(e.exception))

    def test_an_old_or_unknown_name_lists_the_films(self):
        with tempfile.TemporaryDirectory() as d:
            projects = projects_with(Path(d), "01 scr-accuracy\n")
            with self.assertRaises(SystemExit) as e:
                film.load("screening", projects)
            self.assertIn("screening-95-percent-accurate", str(e.exception))

    def test_a_film_is_loaded_by_the_slug_of_its_folder(self):
        with tempfile.TemporaryDirectory() as d:
            projects = projects_with(
                Path(d), "project: Screening - 95 Percent Accurate\n01 scr-accuracy\n")
            f, _ = film.load("screening-95-percent-accurate", projects)
            self.assertEqual(f.project, "Screening - 95 Percent Accurate")

    def test_every_slides_file_in_the_repo_agrees_with_its_folder(self):
        for name in film.film_names():
            with self.subTest(name):
                f, _ = film.load(name)
                self.assertEqual(film.slug(f.project), name)


if __name__ == "__main__":
    unittest.main()

"""A film's slides live in its own project folder, beside its film.yaml.

ai-film-lab-v2 has one projects/ folder for all three stages
(film/docs/plans/2026-10-07/UNIFY.md): projects/<Title>/slides.txt,
slides.script.txt and slides.published.json. Since phase 3 that is the
only place: slides/films/ is not read, and the projects folder is the one
beside film/, as film/ffilm/paths.py `projects_root` says."""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from aimanim import film

TITLE = "Screening - 95 Percent Accurate"
SLUG = "screening-95-percent-accurate"


def one_folder(base: Path) -> Path:
    """projects/<Title>/ with the slides files, no 'project:' line."""
    p = base / "projects" / TITLE
    p.mkdir(parents=True)
    (p / "slides.txt").write_text("01 scr-accuracy\n02 scr-outcomes\n", encoding="utf-8")
    (p / "slides.script.txt").write_text("[01]\nNinety-five.\n[02]\nFour.\n",
                                         encoding="utf-8")
    return base / "projects"


class AFilmsSlidesLiveInItsOwnProjectFolder(unittest.TestCase):

    def test_the_slides_file_in_the_project_folder_is_read_by_its_slug(self):
        with tempfile.TemporaryDirectory() as d:
            projects = one_folder(Path(d))
            f, parts = film.load(SLUG, projects)
            self.assertEqual(f.project, TITLE)
            self.assertEqual([s.scene for s in f.slides], ["scr-accuracy", "scr-outcomes"])
            self.assertEqual(parts["02"], "Four.")

    def test_its_publish_stamp_sits_beside_it(self):
        with tempfile.TemporaryDirectory() as d:
            projects = one_folder(Path(d))
            self.assertEqual(film.files_of(SLUG, projects).stamp,
                             projects / TITLE / "slides.published.json")

    def test_a_film_left_in_the_old_films_folder_is_not_found(self):
        with tempfile.TemporaryDirectory() as d:
            projects = one_folder(Path(d))
            (Path(d) / "films").mkdir()
            (Path(d) / "films" / "zeroing-a-rifle-sight.txt").write_text(
                "project: Zeroing a Rifle Sight\n01 a\n", encoding="utf-8")
            self.assertEqual(film.film_names(projects), [SLUG])
            self.assertIsNone(film.files_of("zeroing-a-rifle-sight", projects))

    def test_the_projects_folder_is_the_one_beside_film(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            (repo / "film" / "projects").mkdir(parents=True)
            with mock.patch.object(film, "FILMLAB", repo / "film"):
                self.assertEqual(film.projects_root(), repo / "projects")


if __name__ == "__main__":
    unittest.main()

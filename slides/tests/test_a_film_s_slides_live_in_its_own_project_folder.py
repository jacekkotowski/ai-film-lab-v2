"""A film's slides live in its own project folder, beside its film.yaml.

ai-film-lab-v2 gets one projects/ folder for all three stages
(film/docs/plans/2026-10-07/UNIFY.md): projects/<Title>/slides.txt,
slides.script.txt and slides.published.json. Until a film is moved there,
films/<slug>.txt is read as before. The projects folder is found by the
same rule as film/ffilm/paths.py `projects_root`: the repo's one
projects/ when the repo's FILM.bat and that folder exist, else film/projects."""
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
            f, parts = film.load(SLUG, Path(d) / "slides", projects)
            self.assertEqual(f.project, TITLE)
            self.assertEqual([s.scene for s in f.slides], ["scr-accuracy", "scr-outcomes"])
            self.assertEqual(parts["02"], "Four.")

    def test_its_publish_stamp_sits_beside_it(self):
        with tempfile.TemporaryDirectory() as d:
            projects = one_folder(Path(d))
            files = film.files_of(SLUG, Path(d) / "slides", projects)
            self.assertEqual(files.stamp, projects / TITLE / "slides.published.json")

    def test_a_film_not_yet_moved_is_read_from_films(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "slides"
            (root / "films").mkdir(parents=True)
            (root / "films" / f"{SLUG}.txt").write_text(f"project: {TITLE}\n01 a\n",
                                                        encoding="utf-8")
            projects = Path(d) / "projects"
            projects.mkdir()
            files = film.files_of(SLUG, root, projects)
            self.assertEqual(files.order, root / "films" / f"{SLUG}.txt")
            self.assertEqual(files.stamp, root / "films" / SLUG / "published.json")

    def test_the_films_listed_are_those_in_both_places(self):
        with tempfile.TemporaryDirectory() as d:
            projects = one_folder(Path(d))
            root = Path(d) / "slides"
            (root / "films").mkdir(parents=True)
            (root / "films" / "zeroing-a-rifle-sight.txt").write_text(
                "project: Zeroing a Rifle Sight\n01 a\n", encoding="utf-8")
            (root / "films" / "zeroing-a-rifle-sight.script.txt").write_text("", encoding="utf-8")
            self.assertEqual(film.film_names(root, projects),
                             [SLUG, "zeroing-a-rifle-sight"])

    def test_the_one_projects_folder_is_used_once_it_exists(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            (repo / "film" / "projects").mkdir(parents=True)
            with mock.patch.object(film, "FILMLAB", repo / "film"):
                self.assertEqual(film.projects_root(), repo / "film" / "projects")
                (repo / "projects").mkdir()
                self.assertEqual(film.projects_root(), repo / "film" / "projects")  # no FILM.bat
                (repo / "FILM.bat").write_text("x", encoding="utf-8")
                self.assertEqual(film.projects_root(), repo / "projects")


if __name__ == "__main__":
    unittest.main()

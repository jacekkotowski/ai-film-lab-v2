"""
A flight lives in its film's folder, once the films share one folder.

ai-film-lab-v2 gets one projects/ folder for all three stages
(film/docs/plans/2026-10-07/UNIFY.md): a film's flight is then
projects/<Title>/fly/ (stops.json, preview/, out/). The folder is used
when the repo's FILM.bat and projects/ exist -- the same rule as
film/ffilm/paths.py `projects_root`. Until then, fly/projects/<slug>/.
Still read from the film: only out/final.mp4 + out/final.timeline.json (0014).

Standard library only:  python -m unittest discover tests
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "library" / "rigs"))

import fly  # noqa: E402

TITLE = "What Is Love"


def repo(d: Path, one_folder: bool = True) -> Path:
    """A repo with FILM.bat and (optionally) projects/What Is Love/out/."""
    (d / "FILM.bat").write_text("x", encoding="utf-8")
    (d / "fly" / "projects").mkdir(parents=True)
    if one_folder:
        out = d / "projects" / TITLE / "out"
        out.mkdir(parents=True)
        (out / "final.timeline.json").write_text(json.dumps({"slug": "what-is-love"}),
                                                 encoding="utf-8")
    return d


def patched(d: Path):
    return mock.patch.multiple(fly, REPO=d, PROJECTS=d / "fly" / "projects")


class AFlightLivesInItsFilmsFolder(unittest.TestCase):

    def test_a_new_flight_of_a_film_in_the_one_folder_is_its_fly_subfolder(self):
        with tempfile.TemporaryDirectory() as t:
            d = repo(Path(t))
            with patched(d):
                project, new = fly.project_for(d / "projects" / TITLE / "out" / "final.timeline.json")
            self.assertTrue(new)
            self.assertEqual(project, d / "projects" / TITLE / "fly")

    def test_an_existing_flight_there_is_found_by_the_films_slug(self):
        with tempfile.TemporaryDirectory() as t:
            d = repo(Path(t))
            (d / "projects" / TITLE / "fly").mkdir()
            (d / "projects" / TITLE / "fly" / "stops.json").write_text("{}", encoding="utf-8")
            with patched(d):
                self.assertEqual(fly.existing("what-is-love"), d / "projects" / TITLE / "fly")
                self.assertEqual(fly.slug_of(d / "projects" / TITLE / "fly"), "what-is-love")

    def test_without_the_one_folder_a_flight_stays_in_fly_projects(self):
        with tempfile.TemporaryDirectory() as t:
            d = repo(Path(t), one_folder=False)
            (d / "fly" / "projects" / "what-is-love").mkdir()
            (d / "fly" / "projects" / "what-is-love" / "stops.json").write_text("{}", encoding="utf-8")
            with patched(d):
                self.assertEqual(fly.existing("what-is-love"), d / "fly" / "projects" / "what-is-love")
                self.assertEqual(fly.slug_of(d / "fly" / "projects" / "what-is-love"), "what-is-love")
                self.assertIsNone(fly.existing("nothing-here"))


if __name__ == "__main__":
    unittest.main()

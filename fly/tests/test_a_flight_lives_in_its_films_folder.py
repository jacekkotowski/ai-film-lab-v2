"""
A flight lives in its film's folder: projects/<Title>/fly/.

ai-film-lab-v2 has one projects/ folder for all three stages
(film/docs/plans/2026-10-07/UNIFY.md): a film's flight is
projects/<Title>/fly/ (stops.json, preview/, out/). Since phase 3 that is
the only place: fly/projects/ is not read, and a film that is not in the
projects folder gets no flight, with a message that says why.
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


def repo(d: Path) -> Path:
    """A repo with projects/What Is Love/out/final.timeline.json."""
    out = d / "projects" / TITLE / "out"
    out.mkdir(parents=True)
    (out / "final.timeline.json").write_text(json.dumps({"slug": "what-is-love"}),
                                             encoding="utf-8")
    return d


def patched(d: Path):
    return mock.patch.object(fly, "PROJECTS", d / "projects")


class AFlightLivesInItsFilmsFolder(unittest.TestCase):

    def test_the_projects_folder_is_the_repos(self):
        self.assertEqual(fly.PROJECTS, HERE.parents[1] / "projects")

    def test_a_new_flight_is_the_films_fly_subfolder(self):
        with tempfile.TemporaryDirectory() as t:
            d = repo(Path(t))
            with patched(d):
                project, new = fly.project_for(d / "projects" / TITLE / "out" / "final.timeline.json")
            self.assertTrue(new)
            self.assertEqual(project, d / "projects" / TITLE / "fly")

    def test_an_existing_flight_is_found_by_the_films_slug(self):
        with tempfile.TemporaryDirectory() as t:
            d = repo(Path(t))
            (d / "projects" / TITLE / "fly").mkdir()
            (d / "projects" / TITLE / "fly" / "stops.json").write_text("{}", encoding="utf-8")
            with patched(d):
                self.assertEqual(fly.existing("what-is-love"), d / "projects" / TITLE / "fly")
                self.assertEqual(fly.slug_of(d / "projects" / TITLE / "fly"), "what-is-love")
                self.assertIsNone(fly.existing("nothing-here"))

    def test_a_flight_left_in_the_old_fly_projects_is_not_found(self):
        with tempfile.TemporaryDirectory() as t:
            d = repo(Path(t))
            (d / "fly" / "projects" / "what-is-love").mkdir(parents=True)
            (d / "fly" / "projects" / "what-is-love" / "stops.json").write_text("{}", encoding="utf-8")
            with patched(d):
                self.assertIsNone(fly.existing("what-is-love"))

    def test_a_film_outside_the_projects_folder_is_refused(self):
        with tempfile.TemporaryDirectory() as t:
            d = repo(Path(t))
            elsewhere = d / "Desktop" / "out"
            elsewhere.mkdir(parents=True)
            (elsewhere / "final.timeline.json").write_text("{}", encoding="utf-8")
            with patched(d), self.assertRaises(SystemExit) as e:
                fly.project_for(elsewhere / "final.timeline.json")
            self.assertIn("projects", str(e.exception))


if __name__ == "__main__":
    unittest.main()

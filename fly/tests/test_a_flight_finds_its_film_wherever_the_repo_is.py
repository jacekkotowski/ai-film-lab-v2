"""
A flight finds its film wherever the repo is.

2026-10-08: stops.json held this laptop's absolute paths to the film
("source": "C:/Users/jacek/code/ai-film-lab-v2/projects/<Title>/out/
final.timeline.json", and "film" for final.mp4). A flight packed by
`film pack` and unpacked anywhere else pointed back at this laptop:
fly.py did not know its old project (it compared that string), and
flight.py stopped on "film not found". Now both are written relative to
the flight's folder (../out/...), and an old absolute path that is not
there is looked for in the film's out/ beside the flight.

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
from film_to_stops import to_stops  # noqa: E402

TITLE = "What Is Love"
FIXTURE = HERE / "fixtures" / "what-is-love.timeline.json"
GONE = "C:/Users/someone-else/ai-film-lab-v2/projects/What Is Love/out/"


def film(d: Path) -> Path:
    """projects/What Is Love/out/ with a timeline and a video; returns the
    flight's folder (not made)."""
    out = d / "projects" / TITLE / "out"
    out.mkdir(parents=True)
    (out / "final.timeline.json").write_text(FIXTURE.read_text(encoding="utf-8"),
                                             encoding="utf-8")
    (out / "final.mp4").write_bytes(b"x")
    return d / "projects" / TITLE / "fly"


class AFlightFindsItsFilm(unittest.TestCase):

    def test_a_new_flight_names_its_film_relative_to_itself(self):
        with tempfile.TemporaryDirectory() as t:
            project = film(Path(t))
            timeline = project.parent / "out" / "final.timeline.json"
            spec = to_stops(json.loads(timeline.read_text(encoding="utf-8")),
                            timeline, project)
            self.assertEqual(spec["source"], "../out/final.timeline.json")
            self.assertEqual(spec["film"], "../out/" + spec["film"].split("/")[-1])

    def test_a_relative_path_is_read_from_the_flights_folder(self):
        with tempfile.TemporaryDirectory() as t:
            project = film(Path(t))
            self.assertEqual(fly.where(project, "../out/final.mp4").resolve(),
                             (project.parent / "out" / "final.mp4").resolve())

    def test_an_old_absolute_path_from_another_machine_is_found_beside_the_flight(self):
        with tempfile.TemporaryDirectory() as t:
            project = film(Path(t))
            self.assertEqual(fly.where(project, GONE + "final.mp4"),
                             project.parent / "out" / "final.mp4")

    def test_an_absolute_path_that_is_there_is_kept(self):
        with tempfile.TemporaryDirectory() as t:
            project = film(Path(t))
            here = (project.parent / "out" / "final.mp4").resolve().as_posix()
            self.assertEqual(fly.where(project, here), Path(here))

    def test_an_unpacked_flight_is_found_again_not_made_again(self):
        """Made new, film_to_stops would refuse (stops.json exists) and the
        run would stop: the copy's own flight must be found."""
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            project = film(d)
            project.mkdir()
            (project / "stops.json").write_text(json.dumps(
                {"source": GONE + "final.timeline.json"}), encoding="utf-8")
            with mock.patch.object(fly, "PROJECTS", d / "projects"):
                got, new = fly.project_for(project.parent / "out" / "final.timeline.json")
            self.assertEqual((got, new), (project, False))


if __name__ == "__main__":
    unittest.main()

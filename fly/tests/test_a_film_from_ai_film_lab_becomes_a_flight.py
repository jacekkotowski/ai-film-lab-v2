"""
A film from ai-film-lab becomes a flight.

ai-film-lab (stage 1) hands over final.mp4 and final.timeline.json; this
studio (stage 2) reads nothing else of it (ai-film-lab docs/decisions/0014).
fixtures/what-is-love.timeline.json is a real one, What Is Love, written by
ai-film-lab 727bcf2. If ai-film-lab changes its timeline, save a new one here
and run this again.

Standard library only:  python -m unittest discover tests
"""

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "library" / "rigs"))

from film_to_stops import to_stops  # noqa: E402
from fly import film_changed  # noqa: E402

FIXTURE = HERE / "fixtures" / "what-is-love.timeline.json"


def timeline():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class AFilmBecomesAFlight(unittest.TestCase):

    def test_what_is_love_gives_8_cards_and_9_visits_as_it_did_when_flown(self):
        spec = to_stops(timeline(), FIXTURE)
        self.assertEqual((len(spec["stops"]), len(spec["visits"])), (8, 9))

    def test_the_visits_cover_every_frame_of_the_film_once(self):
        spec = to_stops(timeline(), FIXTURE)
        v = spec["visits"]
        self.assertEqual(v[0]["start_frame"], 0)
        self.assertEqual(v[-1]["end_frame"], spec["frames"])
        for a, b in zip(v, v[1:]):
            self.assertEqual(a["end_frame"], b["start_frame"])

    def test_the_flight_keeps_the_films_name_and_fingerprint(self):
        t = timeline()
        spec = to_stops(t, FIXTURE)
        self.assertEqual(spec["slug"], "what-is-love")
        self.assertEqual(spec["video_sha256"], t["video_sha256"])


class AReRenderedFilmIsSeen(unittest.TestCase):

    def test_same_render_is_not_a_change(self):
        t = timeline()
        self.assertIs(film_changed(to_stops(t, FIXTURE), t), False)

    def test_a_new_render_is_a_change(self):
        t = timeline()
        stops = to_stops(t, FIXTURE)
        t["video_sha256"] = "0" * 64
        self.assertIs(film_changed(stops, t), True)

    def test_a_flight_from_before_fingerprints_cannot_tell(self):
        t = timeline()
        stops = to_stops(t, FIXTURE)
        del stops["video_sha256"]
        self.assertIsNone(film_changed(stops, t))


if __name__ == "__main__":
    unittest.main()

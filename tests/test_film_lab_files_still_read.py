"""The two ai-film-lab files ai-manim reads (decision 0001) still have the
shape it reads. If ai-film-lab changes them, this is where it shows.

Reads the real ai-film-lab next door when it is there; skipped when not.
"""
import json
import unittest
from pathlib import Path

from aimanim import beats

FILM_LAB = Path(__file__).resolve().parents[2] / "ai-film-lab" / "projects"


def narrated_projects():
    if not FILM_LAB.is_dir():
        return []
    return [p for p in FILM_LAB.iterdir()
            if list((p / "media").glob("voiceover_*.cues.json"))
            and (p / "analysis" / "transcript.json").exists()]


@unittest.skipUnless(narrated_projects(), "no narrated ai-film-lab project next door")
class FilmLabFilesStillRead(unittest.TestCase):

    def test_the_cues_are_a_list_of_seconds(self):
        for p in narrated_projects():
            cues = json.loads(beats.newest_cues(p).read_text(encoding="utf-8"))["cues"]
            self.assertTrue(all(isinstance(c, (int, float)) for c in cues), p.name)

    def test_the_transcript_has_lines_with_times(self):
        for p in narrated_projects():
            t = json.loads((p / "analysis" / "transcript.json").read_text(encoding="utf-8"))
            for src in t["sources"]:
                for line in src["lines"]:
                    self.assertTrue({"text", "start", "end"} <= set(line), p.name)

    def test_some_picture_of_some_film_can_be_timed(self):
        timed = []
        for p in narrated_projects():
            try:
                timed.append(beats.timing_for(p, 1))
            except LookupError:
                continue        # narration recorded, edit not made yet
        self.assertTrue(timed, "no narrated project could be timed")
        self.assertTrue(all(t.total > 0 for t in timed))


if __name__ == "__main__":
    unittest.main()

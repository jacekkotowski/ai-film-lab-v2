"""Workbench items 1, 3, 4, 5, 7: what the tools compute, without Manim,
ffmpeg, qmd or the network."""

import tempfile
import unittest
from pathlib import Path

from aimanim import film, knowledge, layout, look, patterns


class Sizes(unittest.TestCase):          # item 3
    def test_measured_widths_are_kept_and_read_back(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "sizes.json"
            layout.remember_sizes({("affected", 56): (3.1234, 0.59)}, p, today="2026-10-07")
            layout.remember_sizes({("FP 499", 56): (2.7, 0.59)}, p, today="2026-10-07")
            self.assertEqual(layout.width("affected", 56, p), 3.12)
            self.assertEqual(layout.width("FP 499", 56, p), 2.7)
            self.assertIsNone(layout.width("never measured", 56, p))

    def test_the_repo_file_has_the_widths_the_skills_quoted(self):
        self.assertEqual(layout.width("per 10,000 screened"), 8.09)
        self.assertEqual(layout.width("0.50 × 1000 ÷ 2", 64), 7.28)


class RenderLog(unittest.TestCase):      # item 5
    def test_notes_are_tagged_with_their_issue(self):
        notes = ['[layout] "x" is past SIDE (-4.05..-0.25)',
                 '[layout] "a" touches "b"',
                 '[layout] "a" touches a Line',
                 '[layout] "a" touches a Circle',
                 "[beats] step 4 starts 0.20s after its sentence",
                 "PROBLEM: ink 12 px into the caption zone",
                 "[beats] no timing.json: steps spaced evenly"]
        self.assertEqual(look.issue_ids(notes), ["I01", "I02", "I10", "I09", "I16", "I04"])

    def test_a_render_is_logged_and_summed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "renders.csv"
            look.log_render("scr-a", "still", "half", 5.0, ['[layout] "a" touches "b"',
                            "[beats] no timing.json: steps spaced evenly"], p, when="t1")
            look.log_render("scr-a", "still", "full", 7.0, [], p, when="t2")
            import csv
            with p.open(encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual([r["notes"] for r in rows], ["1", "0"])
            out = look.stats_of(rows)
            self.assertIn("scr-a: 2 renders, 12 s", "\n".join(out))
            self.assertIn("I02 x1", out[-1])


class Patterns(unittest.TestCase):       # item 7
    TEXT = """# Issues
### I90 — a thing seen twice, still a note
- **status**: note
- **seen**: a (2026-10-06), b (2026-10-07)
### I91 — seen three times as pseudocode
- **status**: pseudocode
- **seen**: a, b, c (x, y)
### I92 — already a helper
- **status**: helper `kit.x`
- **seen**: a, b, c, d
"""

    def test_entries_are_parsed(self):
        es = patterns.parse(self.TEXT)
        self.assertEqual([(e.id, e.status, len(e.seen)) for e in es],
                         [("I90", "note", 2), ("I91", "pseudocode", 3), ("I92", "helper", 4)])

    def test_due_lists_what_should_climb(self):
        due = patterns.due(patterns.parse(self.TEXT))
        self.assertEqual(len(due), 2)
        self.assertTrue(due[0].startswith("I90 note -> pseudocode"))
        self.assertTrue(due[1].startswith("I91 pseudocode -> helper"))

    def test_the_repo_library_parses(self):
        ids = [e.id for e in patterns.load()]
        self.assertIn("I01", ids)
        self.assertIn("T13", ids)
        self.assertEqual(len(ids), len(set(ids)), "an ID is used twice")


class Knowledge(unittest.TestCase):      # item 1
    def test_one_file_per_commit_in_film_labs_shape(self):
        self.assertEqual(knowledge.commit_file_name("2026-10-07", "59b52e3"),
                         "2026-10-07-59b52e3.md")
        self.assertEqual(knowledge.commit_text("59b52e3", "2026-10-07", "Subject", "Body\n\n"),
                         "# 59b52e3 2026-10-07 Subject\n\nBody\n")


class Gate(unittest.TestCase):           # item 4
    def test_a_film_is_narrated_when_every_slide_has_timing(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "films").mkdir()
            (root / "films" / "f.txt").write_text("project: P\n01 a\n02 b\n", encoding="utf-8")
            for s in ("a", "b"):
                (root / "scenes" / s).mkdir(parents=True)
            (root / "scenes" / "a" / "timing.json").write_text("{}", encoding="utf-8")
            self.assertFalse(film.narrated("f", root))
            (root / "scenes" / "b" / "timing.json").write_text("{}", encoding="utf-8")
            self.assertTrue(film.narrated("f", root))
            self.assertEqual(film.gate(root), ["f: narrated, skipped"])


if __name__ == "__main__":
    unittest.main()

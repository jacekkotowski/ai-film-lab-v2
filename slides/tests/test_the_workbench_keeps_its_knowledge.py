"""Workbench items 1-7 (PLAN.md): sizes file, render log, gate, patterns,
history files. Standard library only; no Manim, ffmpeg or qmd needed."""

import tempfile
import unittest
from pathlib import Path

from aimanim import film, knowledge, layout, look, patterns

ENTRIES = """# Issues
### I01 — text too wide
- **status**: helper `kit.fits`
- **seen**: a (2026-10-05), b (2026-10-06, twice), c
### I02 — a mark is invisible
- **status**: pseudocode
- **seen**: x, y, z
### I03 — once
- **status**: note
- **seen**: x
### I04 — twice, still a note
- **status**: note
- **seen**: x, y
### I05 — a rule
- **status**: rule (CLAUDE.md)
"""


class Sizes(unittest.TestCase):
    def test_measured_widths_are_kept_and_read_back(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "sizes.json"
            layout.remember_sizes({("TP 18", 56): (2.2213, 0.59)}, p, today="2026-10-07")
            layout.remember_sizes({("FP 499", 56): (2.70, 0.59)}, p, today="2026-10-07")
            self.assertEqual(layout.width("TP 18", 56, p), 2.22)
            self.assertEqual(layout.width("FP 499", 56, p), 2.70)
            self.assertIsNone(layout.width("TP 18", 72, p))


class RenderLog(unittest.TestCase):
    def test_notes_are_tagged_with_their_issue(self):
        self.assertEqual(look.issue_ids([
            '[layout] "x" is past SIDE (-4.05..-0.25)',
            '[layout] "a" touches "b"',
            '[layout] "x" touches a Rectangle',
            '[layout] "x" touches a Arrow',
            "[beats] the word 'z' was not heard: its step starts with the one before",
            "PROBLEM: step 4 starts 0.20s after its sentence",
            "something else"]), ["I01", "I02", "I10", "I09", "I17", "I16"])

    def test_the_log_counts_renders_and_issues(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "renders.csv"
            look.log_render("s1", "still", "half", 5.0, ['[layout] "x" is past SIDE (1..5)'],
                            p, when="t1")
            look.log_render("s1", "still", "full", 7.0, ["[beats] no timing.json: …"], p, when="t2")
            look.log_render("s2", "clip", "half", 9.0, [], p, when="t3")
            import csv
            with p.open(encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual([r["notes"] for r in rows], ["1", "0", "0"])
            out = look.stats_of(rows)
            self.assertIn("3 renders", out[0])
            self.assertIn("s1: 2 renders, 12 s", out[1])
            self.assertIn("I01 x1", out[-1])


class Patterns(unittest.TestCase):
    def test_entries_are_read(self):
        es = patterns.parse(ENTRIES)
        self.assertEqual([e.id for e in es], ["I01", "I02", "I03", "I04", "I05"])
        self.assertEqual(len(es[0].seen), 3)          # commas inside ( ) do not split
        self.assertEqual(es[4].status, "rule")

    def test_due_lists_what_was_seen_too_often_for_its_status(self):
        due = patterns.due(patterns.parse(ENTRIES))
        self.assertEqual([d.split()[0] for d in due], ["I02", "I04"])
        self.assertIn("pseudocode -> helper", due[0])
        self.assertIn("note -> pseudocode", due[1])

    def test_the_real_library_parses(self):
        es = patterns.load()
        self.assertGreater(len(es), 30)
        self.assertEqual(len({e.id for e in es}), len(es), "IDs must be unique")


class History(unittest.TestCase):
    def test_one_file_per_commit_in_film_labs_shape(self):
        self.assertEqual(knowledge.commit_file_name("2026-10-07", "59b52e3"),
                         "2026-10-07-59b52e3.md")
        self.assertEqual(knowledge.commit_text("59b52e3", "2026-10-07", "Subject", "Body\n\n"),
                         "# 59b52e3 2026-10-07 Subject\n\nBody\n")


class Gate(unittest.TestCase):
    def test_a_narrated_film_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "films").mkdir()
            (root / "films" / "f.txt").write_text("project: P\n01 a\n", encoding="utf-8")
            (root / "scenes" / "a").mkdir(parents=True)
            self.assertFalse(film.narrated("f", root))
            (root / "scenes" / "a" / "timing.json").write_text("{}", encoding="utf-8")
            self.assertTrue(film.narrated("f", root))
            self.assertEqual(film.gate(root), ["f: narrated, skipped"])


if __name__ == "__main__":
    unittest.main()

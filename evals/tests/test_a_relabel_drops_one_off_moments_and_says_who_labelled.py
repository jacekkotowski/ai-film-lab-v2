"""A relabel drops one-off moments and says who labelled what.

    uv run --directory film python -m unittest discover -s ../evals/tests

2026-10-08, Jacek on the 31 disagreements: "these may be momentary
dialogue events, not repetitive". Short replies to an offer ("1 i 3",
"yes", "build it"), permission messages and one-video render requests are
dropped; requests that stand on their own get Claude's label, marked as
Claude's. The frozen case file itself is never rewritten.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run  # noqa: E402


class Relabel(unittest.TestCase):

    def cases(self):
        return [{"id": "a", "label": "change-the-machine", "split": "test"},
                {"id": "b", "label": "none", "split": "train"},
                {"id": "c", "label": "edit-pass", "split": "val"}]

    def test_a_dropped_case_is_gone(self):
        got = run.relabel(self.cases(), {"a": {"drop": "short reply to an offer"}})
        self.assertEqual([c["id"] for c in got], ["b", "c"])

    def test_a_new_label_replaces_the_logs_and_names_who_gave_it(self):
        got = run.relabel(self.cases(), {"b": {"label": "investigate", "by": "claude"}})
        b = [c for c in got if c["id"] == "b"][0]
        self.assertEqual((b["label"], b["log_label"], b["label_by"]),
                         ("investigate", "none", "claude"))
        self.assertEqual(b["split"], "train")          # the split never moves

    def test_a_case_not_relabelled_keeps_the_log_as_its_labeller(self):
        got = run.relabel(self.cases(), {})
        self.assertEqual({c["label_by"] for c in got}, {"log"})

    def test_the_frozen_cases_are_not_changed_in_place(self):
        cs = self.cases()
        run.relabel(cs, {"a": {"label": "none", "by": "claude"}})
        self.assertEqual(cs[0]["label"], "change-the-machine")


if __name__ == "__main__":
    unittest.main()

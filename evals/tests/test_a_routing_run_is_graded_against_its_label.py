"""A routing run is graded against its label, and the grades add up per skill.

    uv run --directory film python -m unittest discover -s ../evals/tests

Phase 1 of docs/optimization/03-plan.md: accept when there is a table per
skill (should-start, did-start, missed, wrong skill, confusion pairs).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run  # noqa: E402


class WhatTheRunChose(unittest.TestCase):

    def test_the_first_skill_started_is_the_choice(self):
        self.assertEqual(run.choice(["new-scene", "slide-layout"]), "new-scene")

    def test_starting_no_skill_is_none(self):
        self.assertEqual(run.choice([]), "none")


class TheMessageAsJacekSentIt(unittest.TestCase):

    def test_claudes_last_words_go_to_the_system_prompt_not_into_his_message(self):
        case = {"text": "yes", "context": "Shall I fix the caption on s05?"}
        self.assertIn("Shall I fix the caption on s05?", run.context_prompt(case))
        cmd = run.routing_cmd(case, max_turns=1)
        self.assertEqual(cmd[cmd.index("-p") + 1], "yes")
        self.assertIn(run.context_prompt(case), cmd)

    def test_the_first_message_of_a_session_has_no_context(self):
        case = {"text": "where am I", "context": ""}
        self.assertIsNone(run.context_prompt(case))
        self.assertNotIn("--append-system-prompt", run.routing_cmd(case, max_turns=1))


class TheTablePerSkill(unittest.TestCase):

    def rows(self):
        return [{"label": "edit-pass", "got": "edit-pass"},
                {"label": "edit-pass", "got": "none"},
                {"label": "edit-pass", "got": "fix-captions"},
                {"label": "none", "got": "status"},
                {"label": "none", "got": "none"},
                {"label": "status", "got": "status"}]

    def test_missed_wrong_and_started_are_counted_per_skill(self):
        t = run.routing_table(self.rows())
        self.assertEqual(t["edit-pass"], {"should": 3, "did": 1, "right": 1,
                                          "missed": 1, "wrong": 1})
        self.assertEqual(t["status"], {"should": 1, "did": 2, "right": 1,
                                       "missed": 0, "wrong": 0})
        self.assertEqual(t["fix-captions"]["did"], 1)

    def test_the_confusion_pairs_name_label_and_choice(self):
        pairs = run.confusion_pairs(self.rows())
        self.assertEqual(pairs, {("edit-pass", "none"): 1, ("edit-pass", "fix-captions"): 1,
                                 ("none", "status"): 1})


if __name__ == "__main__":
    unittest.main()

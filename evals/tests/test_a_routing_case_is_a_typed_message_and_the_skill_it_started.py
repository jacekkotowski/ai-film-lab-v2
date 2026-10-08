"""A routing case is a typed message and the repo skill it started (or none).

    uv run --directory film python -m unittest discover -s ../evals/tests

Phase 1 of docs/optimization/03-plan.md. The cases are mined from the
session logs; these pin how a message gets its label, which messages are
left out, and that the train/test split is frozen and keeps each skill's
share on both sides.
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cases  # noqa: E402

REPO = ["edit-pass", "status", "new-scene", "slide-layout"]


def typed(text, **kw):
    return {"type": "user", "message": {"role": "user", "content": text}, **kw}


def said(text):
    return {"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}}


def skill(name):
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": name}}]}}


def result():
    return {"type": "user", "message": {"content": [
        {"type": "tool_result", "tool_use_id": "x", "content": "ok"}]}}


class HowAMessageGetsItsLabel(unittest.TestCase):

    def test_a_message_is_labelled_with_the_first_skill_started_before_the_next_message(self):
        t = cases.turns([typed("shot 3 drags"), skill("edit-pass"), result(),
                         skill("status"), typed("thanks")])
        self.assertEqual([(x["text"], x["skills"]) for x in t],
                         [("shot 3 drags", ["edit-pass", "status"]), ("thanks", [])])
        self.assertEqual(cases.label(t[0], REPO), "edit-pass")
        self.assertEqual(cases.label(t[1], REPO), "none")

    def test_tool_results_and_injected_text_are_not_typed_messages(self):
        t = cases.turns([typed("<command-name>/ship</command-name>"), result(),
                         typed("Caveat: the messages below"), typed("x", isMeta=True),
                         typed("summary", isCompactSummary=True)])
        self.assertEqual(t, [])

    def test_messages_inside_a_subagent_are_not_cases(self):
        t = cases.turns([typed("look for the bug", isSidechain=True)])
        self.assertEqual(t, [])

    def test_a_case_carries_claudes_last_words_before_it(self):
        t = cases.turns([typed("hello"), said("Shall I fix the caption on s05?"),
                         typed("yes")])
        self.assertEqual(t[1]["context"], "Shall I fix the caption on s05?")
        self.assertEqual(t[0]["context"], "")

    def test_a_turn_that_started_a_skill_from_outside_the_repo_is_left_out(self):
        t = cases.turns([typed("allow all shells"), skill("update-config")])
        self.assertIsNone(cases.label(t[0], REPO))


class TheCaseSet(unittest.TestCase):

    def turns(self):
        out = []
        for i in range(10):
            out.append({"text": f"note {i}", "skills": ["edit-pass"], "context": ""})
        for i in range(5):
            out.append({"text": f"where {i}", "skills": ["status"], "context": ""})
        for i in range(40):
            out.append({"text": f"chat {i}", "skills": [], "context": ""})
        out.append({"text": "allow it", "skills": ["update-config"], "context": ""})
        return out

    def test_every_message_that_started_a_repo_skill_is_kept_and_some_that_started_none(self):
        cs = cases.routing_cases(self.turns(), REPO, n_none=12, seed=1)
        labels = [c["label"] for c in cs]
        self.assertEqual((labels.count("edit-pass"), labels.count("status"),
                          labels.count("none")), (10, 5, 12))
        self.assertNotIn("allow it", [c["text"] for c in cs])

    def test_the_same_text_twice_is_one_case_and_a_skill_label_wins(self):
        t = [{"text": "make a slide", "skills": [], "context": ""},
             {"text": "make a slide", "skills": ["new-scene"], "context": ""}]
        cs = cases.routing_cases(t, REPO, n_none=5, seed=1)
        self.assertEqual([(c["text"], c["label"]) for c in cs], [("make a slide", "new-scene")])

    def test_the_split_is_40_20_40_with_each_skills_share_on_every_side(self):
        cs = cases.routing_cases(self.turns(), REPO, n_none=20, seed=1)

        def count(split):
            got = [c["label"] for c in cs if c["split"] == split]
            return (got.count("edit-pass"), got.count("status"), got.count("none"))
        self.assertEqual(count("test"), (4, 2, 8))
        self.assertEqual(count("val"), (2, 1, 4))
        self.assertEqual(count("train"), (4, 2, 8))

    def test_a_skill_with_one_case_keeps_it_for_training(self):
        t = [{"text": "where am I", "skills": ["status"], "context": ""}]
        cs = cases.routing_cases(t, REPO, n_none=0, seed=1)
        self.assertEqual(cs[0]["split"], "train")

    def test_the_cases_are_the_same_on_every_run(self):
        a = cases.routing_cases(self.turns(), REPO, n_none=12, seed=7)
        b = cases.routing_cases(list(reversed(self.turns())), REPO, n_none=12, seed=7)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

    def test_a_frozen_case_file_is_not_written_over(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "routing.json"
            p.write_text("[]", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                cases.freeze([{"id": "a"}], p)
            self.assertEqual(p.read_text(encoding="utf-8"), "[]")


if __name__ == "__main__":
    unittest.main()

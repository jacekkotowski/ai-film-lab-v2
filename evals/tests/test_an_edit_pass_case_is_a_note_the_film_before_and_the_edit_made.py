"""An edit-pass case is a note, the film.yaml before it and the edit made for it.

    uv run --directory film python -m unittest discover -s ../evals/tests

Phase 2 of docs/optimization/03-plan.md. A note is a message Jacek typed
that was followed, before his next message, by an Edit of a film's
film.yaml. The before is the file's last commit before the first edit; the
after is the before with Claude's edits applied, and it is "clean" only
when the edits all fit the before, the next commit of the file is that
after, and no `film undo` ran. The rest is "doubtful" with the reason, for
Jacek to look at.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cases  # noqa: E402

YAML = "C:/Users/jacek/code/ai-film-lab/projects/What Is Love/film.yaml"


def typed(text, at="2026-09-28T18:00:00Z"):
    return {"type": "user", "timestamp": at, "message": {"role": "user", "content": text}}


def said(text):
    return {"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}}


def tool(name, at="2026-09-28T18:00:10Z", **inp):
    return {"type": "assistant", "timestamp": at, "message": {"content": [
        {"type": "tool_use", "name": name, "input": inp}]}}


def epoch(iso):
    return cases.epoch(iso)


class WhichMessagesAreNotes(unittest.TestCase):

    def test_a_message_followed_by_an_edit_of_a_films_yaml_is_a_note(self):
        n = cases.edit_notes([
            said("The draft is ready."),
            typed("you can just slightly increase depth"),
            tool("Edit", file_path=YAML, old_string="depth: 0.5", new_string="depth: 0.6"),
            typed("no smearing")])
        self.assertEqual(len(n), 1)
        self.assertEqual((n[0]["film"], n[0]["text"], n[0]["context"], n[0]["next"]),
                         ("What Is Love", "you can just slightly increase depth",
                          "The draft is ready.", "no smearing"))
        self.assertEqual(n[0]["edits"], [{"at": "2026-09-28T18:00:10Z", "old": "depth: 0.5",
                                          "new": "depth: 0.6", "all": False}])

    def test_edits_of_other_files_and_of_test_projects_make_no_note(self):
        n = cases.edit_notes([
            typed("fix it"),
            tool("Edit", file_path="C:/x/film/ffilm/spec.py", old_string="a", new_string="b"),
            tool("Edit", file_path="C:/x/projects/test_story/film.yaml", old_string="a", new_string="b"),
            tool("Edit", file_path="C:/x/projects/zz_redo_test/film.yaml", old_string="a", new_string="b")])
        self.assertEqual(n, [])

    def test_a_film_undo_after_the_note_is_remembered(self):
        n = cases.edit_notes([
            typed("cut s07"),
            tool("Edit", file_path=YAML, old_string="a", new_string="b"),
            tool("Bash", command='uv run film undo -p "What Is Love"')])
        self.assertTrue(n[0]["undo"])


class TheBeforeAndTheAfter(unittest.TestCase):

    BEFORE = "shots:\n- id: s01\n  depth: 0.5\n"
    AFTER = "shots:\n- id: s01\n  depth: 0.6\n"

    def note(self, **kw):
        n = {"film": "What Is Love", "text": "increase depth", "context": "",
             "at": "2026-09-28T18:00:00Z", "next": "", "undo": False,
             "edits": [{"at": "2026-09-28T18:00:10Z", "old": "depth: 0.5",
                        "new": "depth: 0.6", "all": False}]}
        n.update(kw)
        return n

    def history(self, *versions):
        return lambda film: [(epoch(at), sha, text) for at, sha, text in versions]

    def test_the_before_is_the_last_commit_before_the_edit_and_the_next_commit_confirms_it(self):
        h = self.history(("2026-09-28T17:00:00Z", "old", "shots: []\n"),
                         ("2026-09-28T17:59:00Z", "b4", self.BEFORE),
                         ("2026-09-28T18:01:00Z", "af", self.AFTER),
                         ("2026-09-28T19:00:00Z", "later", "shots: []\n"))
        c = cases.edit_pass_case(self.note(), h)
        self.assertEqual((c["before_commit"], c["after_commit"], c["status"]), ("b4", "af", "clean"))
        self.assertEqual((c["before"], c["after"]), (self.BEFORE, self.AFTER))

    def test_line_endings_do_not_make_a_case_doubtful(self):
        h = self.history(("2026-09-28T17:59:00Z", "b4", self.BEFORE.replace("\n", "\r\n")),
                         ("2026-09-28T18:01:00Z", "af", self.AFTER))
        self.assertEqual(cases.edit_pass_case(self.note(), h)["status"], "clean")

    def test_an_edit_that_does_not_fit_the_committed_before_is_doubtful(self):
        h = self.history(("2026-09-28T17:59:00Z", "b4", "shots:\n- id: s01\n  depth: 0.7\n"),
                         ("2026-09-28T18:01:00Z", "af", self.AFTER))
        c = cases.edit_pass_case(self.note(), h)
        self.assertEqual(c["status"], "doubtful")
        self.assertIn("not found", c["why"])

    def test_a_next_commit_that_differs_from_the_edit_is_doubtful(self):
        h = self.history(("2026-09-28T17:59:00Z", "b4", self.BEFORE),
                         ("2026-09-28T18:01:00Z", "af", self.AFTER + "music: x\n"))
        c = cases.edit_pass_case(self.note(), h)
        self.assertEqual(c["status"], "doubtful")
        self.assertIn("next commit", c["why"])

    def test_an_edit_never_committed_or_undone_is_doubtful(self):
        h = self.history(("2026-09-28T17:59:00Z", "b4", self.BEFORE))
        self.assertIn("no commit", cases.edit_pass_case(self.note(), h)["why"])
        h = self.history(("2026-09-28T17:59:00Z", "b4", self.BEFORE),
                         ("2026-09-28T18:01:00Z", "af", self.AFTER))
        self.assertIn("undo", cases.edit_pass_case(self.note(undo=True), h)["why"])

    def test_edits_apply_in_order_and_a_write_replaces_the_file(self):
        after, missing = cases.apply_edits("a b a", [
            {"old": "a", "new": "c", "all": True}, {"old": "b", "new": "d", "all": False},
            {"old": "zz", "new": "y", "all": False}])
        self.assertEqual((after, missing), ("c d c", 1))
        self.assertEqual(cases.apply_edits("old", [{"content": "new\n"}]), ("new\n", 0))


if __name__ == "__main__":
    unittest.main()

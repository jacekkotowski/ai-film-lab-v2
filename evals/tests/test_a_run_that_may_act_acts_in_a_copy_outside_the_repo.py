"""A run that may act (Edit, Write, Bash) works in a copy outside the repo.

    uv run --directory film python -m unittest discover -s ../evals/tests

2026-10-08, measured: with only Read/Glob/Grep/Skill, "1 i 3" (build
bokeh + commit) was answered in words and started no skill -- the run
knew it could not act. So routing runs get the tools a real session has,
in a copy made by `git archive` OUTSIDE the repo (inside it, git would
find the real .git and could commit or push), and the copy's Edit/Write
rules are narrowed to the copy itself.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run  # noqa: E402


class TheCopysSettings(unittest.TestCase):

    def test_edit_and_write_anywhere_become_edit_and_write_inside_the_copy(self):
        s = {"permissions": {"allow": ["Edit", "Write", "Bash", "Bash(uv:*)"]},
             "hooks": {"Stop": []}}
        got = run.narrowed_settings(s)
        self.assertEqual(got["permissions"]["allow"],
                         ["Edit(./**)", "Write(./**)", "Bash", "Bash(uv:*)"])
        self.assertEqual(got["hooks"], {"Stop": []})
        self.assertEqual(s["permissions"]["allow"][0], "Edit")   # the original is untouched

    def test_git_push_is_refused_in_the_copy(self):
        got = run.narrowed_settings({"permissions": {"allow": ["Bash"]}})
        self.assertIn("Bash(git push:*)", got["permissions"]["deny"])


class WhereTheCopyGoes(unittest.TestCase):

    def test_a_copy_inside_the_repo_is_refused(self):
        with self.assertRaises(ValueError):
            run.check_outside(run.ROOT / ".local" / "evals" / "work" / "x")

    def test_a_copy_in_the_temp_folder_is_allowed(self):
        run.check_outside(Path(tempfile.gettempdir()) / "evals-x")


class TheCommandLine(unittest.TestCase):

    def test_a_run_that_may_act_has_the_writing_tools(self):
        cmd = run.claude_cmd("1 i 3", tools=run.ACT_TOOLS)
        tools = cmd[cmd.index("--tools") + 1].split(",")
        for t in ("Edit", "Write", "Bash", "Skill"):
            self.assertIn(t, tools)

    def test_a_run_that_may_act_may_edit_inside_its_folder_and_never_push(self):
        cmd = run.claude_cmd("1 i 3", tools=run.ACT_TOOLS)
        allowed = cmd[cmd.index("--allowedTools") + 1:]
        self.assertIn("Edit(./**)", allowed)
        self.assertNotIn("Edit", allowed)
        self.assertEqual(cmd[cmd.index("--disallowedTools") + 1], "Bash(git push:*)")


if __name__ == "__main__":
    unittest.main()

"""A test run can read the repo and start a skill, and nothing else.

    uv run --directory film python -m unittest discover -s ../evals/tests

2026-10-08, measured on `claude -p`: with the user's settings alone the
repo's skills were not loaded, and `--tools` did not remove the claude.ai
connectors (Gmail, Calendar). These pin the command line and the check
that reads a run's init event.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run  # noqa: E402


def init_event(tools, skills):
    import json
    return json.dumps({"type": "system", "subtype": "init",
                       "tools": tools, "skills": skills})


class TheCommandLine(unittest.TestCase):

    def setUp(self):
        self.cmd = run.claude_cmd("in What Is Love, shot 3 drags")

    def value(self, flag):
        return self.cmd[self.cmd.index(flag) + 1]

    def test_a_routing_run_has_no_tool_that_writes(self):
        tools = self.value("--tools").split(",")
        for writer in ("Edit", "Write", "Bash", "PowerShell", "NotebookEdit"):
            self.assertNotIn(writer, tools)

    def test_no_mcp_tool_comes_in(self):
        self.assertIn("--strict-mcp-config", self.cmd)

    def test_the_repo_skills_are_loaded(self):
        self.assertIn("project", self.value("--setting-sources").split(","))

    def test_anything_not_allowed_is_refused_not_asked(self):
        self.assertEqual(self.value("--permission-mode"), "dontAsk")

    def test_a_test_run_is_not_saved_among_the_sessions_it_is_mined_from(self):
        self.assertIn("--no-session-persistence", self.cmd)

    def test_every_run_has_a_spending_cap(self):
        self.assertGreater(float(self.value("--max-budget-usd")), 0)


class TheBoxCheck(unittest.TestCase):

    def test_a_run_with_only_the_read_tools_and_all_skills_is_boxed_in(self):
        s = run.summarize([init_event(["Glob", "Grep", "Read", "Skill"],
                                      ["edit-pass", "status", "qmd:qmd"])])
        self.assertEqual(run.box_problems(s, ["edit-pass", "status"]), [])

    def test_a_connector_tool_in_the_run_is_a_problem(self):
        s = run.summarize([init_event(["Read", "Skill", "mcp__claude_ai_Gmail__send_message"],
                                      ["edit-pass"])])
        self.assertEqual(len(run.box_problems(s, ["edit-pass"])), 1)

    def test_a_repo_skill_the_run_cannot_see_is_a_problem(self):
        s = run.summarize([init_event(["Read", "Skill"], ["qmd:qmd"])])
        self.assertIn("not loaded", run.box_problems(s, ["edit-pass"])[0])

    def test_a_run_with_no_init_event_is_not_trusted(self):
        s = run.summarize([])
        self.assertIn("no init event", run.box_problems(s, ["edit-pass"]))


class WhatChangedInTheRepo(unittest.TestCase):

    def snap(self, status="", times=None, last="test_story\n"):
        return {"status": status, "times": times or {"a": 1}, "lastfilm": last}

    def test_nothing_changed_says_nothing(self):
        self.assertEqual(run.changed(self.snap(), self.snap()), [])

    def test_a_film_file_touched_under_projects_is_named(self):
        self.assertIn("1 files under projects/ changed",
                      run.changed(self.snap(times={"a": 1}), self.snap(times={"a": 2}))[0])

    def test_lastfilm_rewritten_is_named(self):
        self.assertEqual(run.changed(self.snap(), self.snap(last="Screening\n")),
                         [".lastfilm changed"])


if __name__ == "__main__":
    unittest.main()

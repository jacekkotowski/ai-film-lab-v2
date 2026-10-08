"""Reading a skill's SKILL.md counts as starting that skill.

    uv run --directory film python -m unittest discover -s ../evals/tests

2026-10-08, measured: asked "make a slide about the bearing...", a
`claude -p` run Read .claude/skills/new-scene/SKILL.md instead of calling
the Skill tool. Routing is about which skill was chosen, so both count
(skill-creator's run_eval counts the Read too).
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run  # noqa: E402


def tool_use(name, **inp):
    return json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": name, "input": inp}]}})


class WhichSkillARunStarted(unittest.TestCase):

    def test_the_skill_tool_names_the_skill(self):
        s = run.summarize([tool_use("Skill", skill="status")])
        self.assertEqual(s["skills"], ["status"])

    def test_a_read_of_a_skill_file_starts_that_skill_on_windows_paths(self):
        p = r"C:\Users\jacek\code\ai-film-lab-v2\.claude\skills\new-scene\SKILL.md"
        s = run.summarize([tool_use("Read", file_path=p)])
        self.assertEqual(s["skills"], ["new-scene"])

    def test_a_read_of_any_other_file_starts_nothing(self):
        s = run.summarize([tool_use("Read", file_path="slides/CLAUDE.md"),
                           tool_use("Glob", pattern=".claude/skills/*/SKILL.md")])
        self.assertEqual(s["skills"], [])

    def test_the_same_skill_twice_is_counted_once_in_order(self):
        s = run.summarize([tool_use("Read", file_path=".claude/skills/slide-layout/SKILL.md"),
                           tool_use("Skill", skill="new-scene"),
                           tool_use("Skill", skill="slide-layout")])
        self.assertEqual(s["skills"], ["slide-layout", "new-scene"])


class WhatARunCost(unittest.TestCase):

    def test_cost_turns_and_refusals_come_from_the_result_event(self):
        line = json.dumps({"type": "result", "subtype": "error_max_turns",
                           "total_cost_usd": 0.126, "num_turns": 3,
                           "usage": {"output_tokens": 343},
                           "permission_denials": [{"tool_name": "mcp__plugin_qmd_qmd__query",
                                                   "tool_input": {}}]})
        s = run.summarize([line, "not json"])
        self.assertEqual((s["cost"], s["turns"], s["subtype"]), (0.126, 3, "error_max_turns"))
        self.assertEqual(s["tokens"]["output_tokens"], 343)
        self.assertEqual(s["denied"][0][0], "mcp__plugin_qmd_qmd__query")


if __name__ == "__main__":
    unittest.main()

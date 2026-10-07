"""`film <film> check` and `look`: what they compute, without Manim or ffmpeg."""

import tempfile
import unittest
from pathlib import Path

from aimanim import beats, look

COST = ("Each of the 499 false alarms is a mother told her baby may be ill. "
        "She can wait until week 15 for amniocentesis, a needle into the womb, "
        "then up to two weeks for the result. That needle ends about 3 pregnancies "
        "in 1,000, so if all 499 take it, one or two healthy babies are lost.")


class Rehearsal(unittest.TestCase):
    def test_numbers_with_a_point_stay_in_one_sentence(self):
        self.assertEqual(len(beats.sentences("It scores 99.8 percent. LR+ is 0.90 / 0.05. Hers is 18.")), 3)

    def test_a_paragraph_is_timed_at_the_pace(self):
        t = beats.rehearsal("one two three four five.", wps=2.5)
        self.assertAlmostEqual(t.total, 2.0)
        self.assertEqual(t.lines[0].words, [0.0, 0.4, 0.8, 1.2, 1.6])

    def test_a_word_too_close_to_the_next_is_found(self):
        # scr-cost before 2026-10-07: "result" is said 0.8 s before "needle"
        out = beats.rehearse(COST, ["Each", "wait", "result", "needle"],
                             [0, 1, 1, 2], [1.5, 1.0, 1.0, 1.5])
        self.assertTrue(any("starts 0.20s after" in ln for ln in out), out)
        ok = beats.rehearse(COST, ["Each", "wait", "two", "needle"],
                            [0, 1, 1, 2], [1.5, 1.0, 1.0, 1.5])
        self.assertFalse(any("PROBLEM" in ln for ln in ok), ok)

    def test_a_word_not_in_the_script_and_a_wrong_sentence(self):
        out = beats.rehearse(COST, ["Each", "syringe"], [0, 1], [1.0, 1.0])
        self.assertTrue(any("'syringe'" in ln and "not in the script" in ln for ln in out))
        out = beats.rehearse(COST, ["Each", "needle"], [0, 2], [1.0, 1.0])
        self.assertTrue(any("BEAT_LINES says 2" in ln for ln in out), out)

    def test_scene_constants_are_read_without_running_the_scene(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "scene.py"
            p.write_text('import manim\nBEAT_WORDS: list[str] = ["a", "b|c"]\n'
                         'BEAT_LINES = [0, 1]\nRUN_TIMES = [1.0, 1.5]\nX = f()\n',
                         encoding="utf-8")
            self.assertEqual(beats.scene_beats(p), {"BEAT_WORDS": ["a", "b|c"],
                                                    "BEAT_LINES": [0, 1],
                                                    "RUN_TIMES": [1.0, 1.5]})


class Looking(unittest.TestCase):
    def test_ink_margins(self):
        w, h, bg = 10, 8, 19
        img = bytearray([bg] * (w * h))
        img[2 * w + 3] = 200          # one ink pixel at x 3, y 2
        img[5 * w + 6] = 100          # and at x 6, y 5
        img[7 * w + 9] = bg + 5       # within the tolerance: not ink
        self.assertEqual(look.ink_box(bytes(img), w, h, bg), (3, 2, 3, 2))
        self.assertIsNone(look.ink_box(bytes([bg] * 4), 2, 2, bg))

    def test_margins_are_judged_at_the_picture_size(self):
        notes = look.margin_notes((30, 60, 30, 240), 540)       # half size: 30 = 60
        self.assertFalse(any("PROBLEM" in n for n in notes), notes)
        notes = look.margin_notes((57, 120, 61, 470), 1080)
        self.assertEqual(sum("PROBLEM" in n for n in notes), 2, notes)

    def test_the_frame_each_step_ends_on(self):
        # waits of 24 and 12 frames, steps of 1.0 s (24 frames) and 0.5 s (12)
        self.assertEqual(look.step_end_frames([24, 12], [1.0, 0.5], 24), [47, 71])


if __name__ == "__main__":
    unittest.main()

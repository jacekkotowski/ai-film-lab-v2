"""A clip is as long as its slide, to the frame.

Manim draws a wait as int(seconds x fps) frames, dropping the part frame
each time; the mil-measure clips came out 1.0-4.6 frames short of their
slides (ffprobe, 2026-10-06). beats.in_frames counts the waits in whole
frames instead.
"""

import math
import unittest

from aimanim import beats


class AClipIsAsLongAsItsSlide(unittest.TestCase):

    def frames(self, starts, run_times, total, fps=24):
        p = beats.plan(starts, run_times, total)
        waits, tail = beats.in_frames(p, run_times, fps)
        drawn = sum(waits) + tail + sum(beats.play_frames(r, fps) for r in run_times)
        return waits, drawn

    def test_the_finale_six_short_steps_ends_on_its_last_whole_frame(self):
        # mil-finale's real starts: 9.36 s fill 224.64 frames -> 224, not 220
        starts = [2.02, 2.93, 3.54, 4.15, 4.85, 6.20]
        _, drawn = self.frames(starts, [0.5] * 5 + [1.5], 9.36)
        self.assertEqual(drawn, math.floor(9.36 * 24))

    def test_every_step_starts_on_the_frame_nearest_its_word(self):
        starts, rts = [0.24, 3.39, 9.78], [1.0, 1.0, 1.5]
        waits, _ = self.frames(starts, rts, 12.0)
        begins, done = [], 0
        for n, rt in zip(waits, rts):
            begins.append(done + n)
            done += n + beats.play_frames(rt, 24)
        self.assertEqual(begins, [round(s * 24) for s in starts])

    def test_a_play_is_as_many_frames_as_manim_draws(self):
        self.assertEqual([beats.play_frames(r, 24) for r in (0.5, 1.0, 1.5)], [12, 24, 36])

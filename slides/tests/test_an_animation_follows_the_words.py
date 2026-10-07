import unittest

from aimanim import beats


class AnAnimationFollowsTheWords(unittest.TestCase):

    def test_each_picture_gets_the_words_said_over_it(self):
        # six pictures, five cues: the cue is where the NEXT picture began
        cues = [26.8, 59.3, 87.65, 120.65, 149.0]
        self.assertEqual(beats.picture_span(cues, 1, 179.95), (0.0, 26.8))
        self.assertEqual(beats.picture_span(cues, 3, 179.95), (59.3, 87.65))
        self.assertEqual(beats.picture_span(cues, 6, 179.95), (149.0, 179.95))
        with self.assertRaises(ValueError):
            beats.picture_span(cues, 7, 179.95)

    def test_a_sentence_is_timed_from_the_start_of_its_picture(self):
        lines = [{"text": "before", "start": 20.0, "end": 22.0},
                 {"text": "one", "start": 60.0, "end": 62.5},
                 {"text": "spills over", "start": 86.0, "end": 89.0},
                 {"text": "after", "start": 88.0, "end": 90.0}]
        got = beats.lines_in(lines, (59.3, 87.65))
        self.assertEqual([x.text for x in got], ["one", "spills over"])
        self.assertAlmostEqual(got[0].start, 0.7)
        self.assertAlmostEqual(got[1].end, 28.35)   # cut at the picture's end

    def test_a_step_starts_on_its_sentence(self):
        p = beats.plan([0.5, 3.0, 6.0], [1.0, 1.0, 1.0], total=9.0)
        self.assertEqual(p.waits, [0.5, 1.5, 2.0])
        self.assertEqual(p.tail, 2.0)
        self.assertEqual(p.notes, [])

    def test_a_step_that_cannot_start_on_time_says_so(self):
        p = beats.plan([0.0, 1.0], [2.0, 1.0], total=5.0)
        self.assertEqual(p.waits, [0.0, 0.0])
        self.assertIn("step 2 starts 1.00s after its sentence", p.notes)

    def test_an_animation_longer_than_the_words_says_so(self):
        p = beats.plan([0.0], [4.0], total=3.0)
        self.assertEqual((p.tail, p.late), (0.0, 1.0))
        self.assertIn("the animation runs 1.00s past the words", p.notes)

    def test_the_clip_lasts_exactly_as_long_as_the_words(self):
        p = beats.plan([0.7, 4.2], [1.5, 1.2], total=12.0)
        self.assertAlmostEqual(sum(p.waits) + 1.5 + 1.2 + p.tail, 12.0)

    def test_a_scene_nobody_has_narrated_yet_still_has_a_plan(self):
        starts, total = beats.placeholder([1.5, 1.0])
        self.assertEqual(starts, [1.0, 3.5])
        self.assertEqual(total, 5.5)

    def test_a_step_cannot_name_a_sentence_that_was_not_said(self):
        t = beats.Timing([beats.Line("only one", 0.5, 2.0)], 3.0)
        with self.assertRaises(ValueError):
            beats.starts_for(t, [0, 1])

    def test_timing_survives_the_file(self):
        t = beats.Timing([beats.Line("Łódź, zero mil", 0.5, 2.0)], 3.0, "x.wav")
        self.assertEqual(beats.Timing.from_json(t.to_json()), t)


if __name__ == "__main__":
    unittest.main()

import unittest

from aimanim import beats


def line(text, start, end, words=None):
    return beats.Line(text, start, end, words or [])


class AStepStartsOnItsWord(unittest.TestCase):
    # captions as film-lab writes them: a line's words carry their own times
    T = beats.Timing([
        line("Fire four shots at the same point", 0.8, 3.0,
             [0.8, 1.1, 1.4, 1.8, 2.0, 2.2, 2.5]),
        line("from a sandbag or bipod.", 3.1, 4.6),
        line("Mark the middle of the four holes,", 5.0, 7.0,
             [5.0, 5.4, 5.6, 6.0, 6.2, 6.4, 6.7]),
        line("and one mil is about 14 clicks.", 8.0, 10.0,
             [8.0, 8.3, 8.6, 8.9, 9.1, 9.5, 9.8]),
    ], 11.0)

    def test_a_step_starts_on_the_word_not_the_line(self):
        self.assertEqual(beats.starts_by_words(self.T, ["four", "holes"]),
                         ([1.1, 6.7], []))

    def test_words_are_found_in_order(self):
        # the second "four" is the one after "Mark", not the first again
        self.assertEqual(beats.starts_by_words(self.T, ["Mark", "four"])[0],
                         [5.0, 6.4])

    def test_a_number_may_be_heard_as_digits(self):
        self.assertEqual(beats.starts_by_words(self.T, ["fourteen|14"])[0], [9.5])

    def test_punctuation_and_case_do_not_matter(self):
        self.assertEqual(beats.starts_by_words(self.T, ["BIPOD"])[0], [3.1])

    def test_a_line_without_word_times_gives_its_own_start(self):
        self.assertEqual(beats.starts_by_words(self.T, ["sandbag"])[0], [3.1])

    def test_a_word_never_said_is_named_and_waits_for_the_one_before(self):
        starts, missing = beats.starts_by_words(self.T, ["Fire", "elephant", "Mark"])
        self.assertEqual(starts, [0.8, 0.8, 5.0])
        self.assertEqual(missing, ["elephant"])


if __name__ == "__main__":
    unittest.main()

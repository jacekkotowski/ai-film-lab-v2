"""The Down syndrome screening example (screening film) from its inputs:
20 sick in 10,000, 90 % detected, 5 % of the healthy flagged."""

import unittest

from aimanim import diagnostic as d


class TheWorkedExample(unittest.TestCase):
    t = d.Test.from_rates(n=10_000, sick=20, sensitivity=0.90, specificity=0.95)

    def test_the_four_cells(self):
        self.assertEqual((self.t.tp, self.t.fn, self.t.fp, self.t.tn),
                         (18, 2, 499, 9481))

    def test_accuracy_rewards_the_lazy_test(self):
        self.assertAlmostEqual(self.t.accuracy, 0.9499)
        self.assertAlmostEqual(self.t.always_negative, 0.998)

    def test_a_positive_is_one_in_29(self):
        self.assertEqual(self.t.positive, 517)
        self.assertAlmostEqual(self.t.ppv, 18 / 517)
        self.assertEqual(d.one_in(self.t.ppv), 29)
        self.assertEqual(round(self.t.npv * 100, 2), 99.98)

    def test_the_likelihood_ratio_gives_the_same_answer(self):
        self.assertAlmostEqual(self.t.lr_pos, 18.0)
        odds = d.post_test_odds(self.t.sick, self.t.healthy, self.t.lr_pos)
        self.assertAlmostEqual(odds[0], 360)
        p = odds[0] / (odds[0] + odds[1])
        self.assertAlmostEqual(p, self.t.ppv)        # 360:9980 = 18:499


class RarerConditions(unittest.TestCase):
    def test_ppv_falls_with_prevalence_lr_does_not(self):
        hi = d.ppv_at(20 / 10_000, 0.90, 0.05)
        lo = d.ppv_at(2 / 10_000, 0.90, 0.05)
        self.assertAlmostEqual(hi, 18 / 517)
        self.assertLess(lo, hi / 9)

    def test_prevalence_for_ppv_inverts_ppv_at(self):
        p = d.prevalence_for_ppv(0.15, 0.997, 0.0004)
        self.assertAlmostEqual(d.ppv_at(p, 0.997, 0.0004), 0.15)


if __name__ == "__main__":
    unittest.main()

"""layout.two_bone: where the elbow goes when a hand must reach a point.
Plain geometry, no Manim; the figure in kit.py will place its arm with it."""

import math
import unittest

from aimanim import layout

SHOULDER = (0.0, 0.0)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


class ALimbReachesItsTarget(unittest.TestCase):
    def test_a_hand_lands_on_a_target_within_reach(self):
        elbow, hand = layout.two_bone(SHOULDER, (1.2, 0.7), 1.0, 1.0)
        self.assertAlmostEqual(hand[0], 1.2)
        self.assertAlmostEqual(hand[1], 0.7)

    def test_both_bones_keep_their_length(self):
        elbow, hand = layout.two_bone(SHOULDER, (1.5, -0.4), 1.0, 0.8)
        self.assertAlmostEqual(dist(SHOULDER, elbow), 1.0)
        self.assertAlmostEqual(dist(elbow, hand), 0.8)

    def test_two_unit_bones_reaching_root_two_put_the_elbow_at_a_right_angle(self):
        # upper = lower = 1, target (sqrt 2, 0): the bones meet at 90 degrees,
        # the elbow is at (sqrt2/2, +-sqrt2/2)
        r = math.sqrt(2)
        elbow, _ = layout.two_bone(SHOULDER, (r, 0.0), 1.0, 1.0, bend=1)
        self.assertAlmostEqual(elbow[0], r / 2)
        self.assertAlmostEqual(abs(elbow[1]), r / 2)

    def test_the_other_bend_puts_the_elbow_on_the_other_side(self):
        up, _ = layout.two_bone(SHOULDER, (1.2, 0.0), 1.0, 1.0, bend=1)
        down, _ = layout.two_bone(SHOULDER, (1.2, 0.0), 1.0, 1.0, bend=-1)
        self.assertAlmostEqual(up[0], down[0])
        self.assertAlmostEqual(up[1], -down[1])
        self.assertNotAlmostEqual(up[1], 0.0)

    def test_a_target_out_of_reach_stretches_the_arm_straight_at_it(self):
        elbow, hand = layout.two_bone(SHOULDER, (6.0, 8.0), 1.0, 1.0)   # 10 away
        self.assertAlmostEqual(dist(SHOULDER, hand), 2.0)
        self.assertAlmostEqual(hand[0] / hand[1], 6.0 / 8.0)            # same direction
        self.assertAlmostEqual(elbow[0] / elbow[1], 6.0 / 8.0)
        self.assertAlmostEqual(dist(SHOULDER, elbow), 1.0)

    def test_a_target_too_close_folds_the_arm_without_failing(self):
        # bones 1.0 and 0.4: the hand cannot come nearer than 0.6
        elbow, hand = layout.two_bone(SHOULDER, (0.1, 0.0), 1.0, 0.4)
        self.assertAlmostEqual(dist(SHOULDER, hand), 0.6)
        self.assertAlmostEqual(dist(SHOULDER, elbow), 1.0)

    def test_a_target_on_the_shoulder_does_not_divide_by_zero(self):
        elbow, hand = layout.two_bone(SHOULDER, (0.0, 0.0), 1.0, 1.0)
        self.assertAlmostEqual(dist(SHOULDER, elbow), 1.0)
        self.assertAlmostEqual(dist(elbow, hand), 1.0)

    def test_the_shoulder_need_not_be_the_origin(self):
        elbow, hand = layout.two_bone((3.0, -2.0), (4.0, -1.0), 1.0, 1.0)
        self.assertAlmostEqual(hand[0], 4.0)
        self.assertAlmostEqual(hand[1], -1.0)
        self.assertAlmostEqual(dist((3.0, -2.0), elbow), 1.0)


if __name__ == "__main__":
    unittest.main()

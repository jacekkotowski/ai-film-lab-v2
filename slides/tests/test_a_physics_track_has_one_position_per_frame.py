"""aimanim.physics.track steps a pymunk space and returns, for every film
frame, where each body is -- so a slide can replay it frame by frame.
Needs the optional `physics` extra; skipped without it."""

import unittest

try:
    import pymunk
except ImportError:                       # uv run --directory slides --extra physics
    pymunk = None

from aimanim import physics

G = 9.81


def dropped(y=5.0):
    space = pymunk.Space()
    space.gravity = (0, -G)
    body = pymunk.Body(1, 1)
    body.position = (1, y)
    space.add(body)
    return space, body


@unittest.skipIf(pymunk is None, "pymunk not installed (extra: physics)")
class APhysicsTrackHasOnePositionPerFrame(unittest.TestCase):
    def test_a_second_at_24_fps_gives_25_frames_the_first_being_the_start(self):
        space, body = dropped()
        frames = physics.track(space, [body], 1.0, fps=24)
        self.assertEqual(len(frames), 25)
        self.assertEqual(frames[0][0][:2], (1.0, 5.0))

    def test_the_last_frame_is_where_a_second_of_falling_ends(self):
        space, body = dropped()
        frames = physics.track(space, [body], 1.0, fps=24)
        x, y, _ = frames[-1][0]
        self.assertAlmostEqual(5 - y, 0.5 * G, delta=0.5 * G * 0.01)   # within 1 %
        self.assertEqual(x, 1.0)

    def test_the_frame_at_a_time_is_found_by_seconds(self):
        space, body = dropped()
        frames = physics.track(space, [body], 1.0, fps=24)
        self.assertEqual(physics.at(frames, 0.5, fps=24), frames[12])
        self.assertEqual(physics.at(frames, 9.0, fps=24), frames[-1])   # held after the end


if __name__ == "__main__":
    unittest.main()

"""pymunk (the optional `physics` extra) in frame units: seconds are film
seconds, lengths are frame units, so a body dropped for 1 s with g = 9.81
falls 4.905 units. Skipped where pymunk is not installed (base tests need
nothing installed)."""

import math
import unittest

try:
    import pymunk
except ImportError:                       # uv run --directory slides --extra physics
    pymunk = None

FPS, SUBSTEPS = 24, 10                    # ten physics steps per film frame
G = 9.81


def run(space, seconds):
    for _ in range(int(seconds * FPS) * SUBSTEPS):
        space.step(1 / (FPS * SUBSTEPS))


@unittest.skipIf(pymunk is None, "pymunk not installed (extra: physics)")
class AFallingThingFollowsGravity(unittest.TestCase):
    def test_a_dropped_body_falls_half_g_t_squared_in_a_second(self):
        space = pymunk.Space()
        space.gravity = (0, -G)
        body = pymunk.Body(1, 1)
        body.position = (0, 5)
        space.add(body)
        run(space, 1.0)
        fallen = 5 - body.position.y
        self.assertAlmostEqual(fallen, 0.5 * G, delta=0.5 * G * 0.01)   # within 1 %

    def test_a_pendulum_bob_keeps_the_length_of_its_rod(self):
        space = pymunk.Space()
        space.gravity = (0, -G)
        bob = pymunk.Body(1, 1)
        bob.position = (2, 3)                       # rod from (0, 3), length 2
        rod = pymunk.PinJoint(space.static_body, bob, (0, 3), (0, 0))
        space.add(bob, rod)
        run(space, 2.0)
        length = math.hypot(bob.position.x - 0, bob.position.y - 3)
        self.assertAlmostEqual(length, 2.0, delta=0.02)
        self.assertLess(bob.position.y, 3)          # it swung down, not up


if __name__ == "__main__":
    unittest.main()

"""physics.py -- replay a pymunk simulation frame by frame (stdlib + pymunk).

pymunk is the optional `physics` extra (uv run --directory slides --extra
physics ...); this module never imports Manim (only kit.py does) and never
imports pymunk itself -- it is given a Space and Bodies.

    frames = physics.track(space, [ball], seconds=2.0)       # once, before the scene plays
    x, y, angle = physics.at(frames, t)[0]                   # where body 0 is at film second t

Seconds are film seconds, lengths are frame units; ten physics steps per
film frame (tests/test_a_falling_thing_follows_gravity.py).
"""

from __future__ import annotations

FPS = 24
SUBSTEPS = 10


def track(space, bodies, seconds: float, fps: int = FPS, substeps: int = SUBSTEPS):
    """Step `space` for `seconds`; return a list of frames, frame 0 being the
    start. Each frame is one (x, y, angle) per body, in the order given."""
    def now():
        return [(b.position.x, b.position.y, b.angle) for b in bodies]

    frames = [now()]
    for _ in range(round(seconds * fps)):
        for _ in range(substeps):
            space.step(1 / (fps * substeps))
        frames.append(now())
    return frames


def at(frames, t: float, fps: int = FPS):
    """The frame showing at film second `t`; the last one is held after the end."""
    return frames[min(max(round(t * fps), 0), len(frames) - 1)]

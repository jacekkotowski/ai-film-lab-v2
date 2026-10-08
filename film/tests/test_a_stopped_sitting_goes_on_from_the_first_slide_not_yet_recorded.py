"""A stopped sitting goes on from the first slide not yet recorded.

Jacek, 2026-10-08: the window went back to slide 1 after a stop, so a
crash cost the whole narration again -- not the one slide that
test_each_slide_is_its_own_take promised. Now every slide's take has its
picture written beside it, the window skips the slides that have one, and
the join takes each picture's newest take.
"""

import os
import time

from ffilm import booth, record


def test_enter_skips_the_slides_already_recorded():
    assert booth.after_slide(step=1, n=6, done={2, 3}) == 4
    assert booth.after_slide(step=3, n=5, done={4}) is None


def test_the_window_opens_on_the_first_slide_not_yet_recorded():
    assert booth.first_slide(5, done={0, 1, 2}) == 3
    assert booth.first_slide(5, done=set()) == 0
    assert booth.first_slide(3, done={0, 1, 2}) is None


def test_a_take_knows_its_picture_and_the_newest_take_of_a_picture_wins(tmp_path):
    old = tmp_path / "voiceover_20261008-213156.wav"
    new = tmp_path / "voiceover_20261008-220000.wav"
    other = tmp_path / "voiceover_20261008-213250.wav"
    for f in (old, new, other):
        f.write_bytes(b"x" * 20_000)
    record.write_slide_label(old, "media/01_a.png")
    record.write_slide_label(other, "media/02_b.png")
    record.write_slide_label(new, "media/01_a.png")
    assert record.slide_labels(tmp_path) == {"media/01_a.png": new,
                                             "media/02_b.png": other}


def test_a_take_with_no_picture_written_beside_it_is_not_guessed(tmp_path):
    (tmp_path / "voiceover_20261008-213156.wav").write_bytes(b"x" * 20_000)
    assert record.slide_labels(tmp_path) == {}


def test_a_label_whose_take_is_gone_is_ignored(tmp_path):
    take = tmp_path / "voiceover_20261008-213156.wav"
    take.write_bytes(b"x")
    record.write_slide_label(take, "media/01_a.png")
    take.unlink()
    assert record.slide_labels(tmp_path) == {}


def test_kept_takes_are_matched_to_the_slides_by_picture_not_by_count():
    shown = ["media/01_a.png", "media/08_photo.png", "media/10_c.png"]
    labels = {"media/01_a.png": "t1", "media/10_c.png": "t10",
              "media/99_gone.png": "t99"}
    assert record.kept_slides(shown, labels) == {0: "t1", 2: "t10"}

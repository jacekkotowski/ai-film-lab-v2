"""A lower-third caption sits one line lower than it used to.

Jacek, 2026-10-06, on the mil-measure film: "lower the captions just a
height of a line down". Every caption in every project is `lower_third`,
whose block began at 72 % of the height: 1382 px of 1920, so a three-line
caption (108 px lines, 370 px block) covered 1382-1752. ai-manim's slides
keep only the bottom 480 px (from 1440) clear, and their ink reached 1430:
the two could overlap. One line lower the block covers 1490-1860.
"""

import pytest

from ffilm.render import caption_top


def test_a_lower_third_block_starts_one_line_below_72_percent():
    assert caption_top("lower_third", 1920, block_h=370, line_h=108) == pytest.approx(1382.4 + 108)


def test_three_lines_at_1080x1920_stay_out_of_the_slides_and_inside_the_frame():
    top = caption_top("lower_third", 1920, block_h=370, line_h=108)
    assert top >= 1920 - 480                  # ai-manim's slides end above this
    assert top + 370 <= 1920 - 50             # and the last line is not cut off


def test_the_other_positions_have_not_moved():
    assert caption_top("top", 1920, 370, 108) == 1920 * 0.08
    assert caption_top("center", 1920, 370, 108) == (1920 - 370) / 2
    assert caption_top("bottom", 1920, 370, 108) == 1920 - 1920 * 0.10 - 370

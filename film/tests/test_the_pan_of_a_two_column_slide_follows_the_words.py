"""
The pan of a two-column slide happens where the words cross from the left
column to the right one.

Found 2026-10-10 on Dynamic Arrays - Dropdown Lists (6 slides, 2160x1920):
`columns` panned on a fixed clock, 37.5 % hold / 25 % pan / 37.5 % hold of
the shot. Where the pan ended against the first sentence about the right
column: slide 2 0.1 s early, 3 and 4 0.4 s early, 6 on time, 5 3.6 s late,
7 3.4 s late. The four near hits were luck (their words crossed at 63-65 %
of the shot). On slide 2 the camera left the left column at 7.0 s while
"The source was a fixed address", about its source bar, ran 9.84-11.26 s.

A shot may now say `cross: <seconds>`: the moment, in film seconds like the
captions' `at`, when the camera is half way between the columns. The pan
lasts COLUMNS_PAN seconds around it. Without `cross:` nothing changes.
"""

import pytest

from ffilm.moves import COLUMNS_PAN, window_at
from ffilm.slides import refit_speed
from ffilm.spec import Film, Shot

DURATION = 20.0


def _slide(**extra):
    return Shot.parse({"src": "media/excel.png", "move": "columns",
                       "duration": DURATION, **extra}, 0)


def _at(shot, seconds):
    return window_at(shot, seconds / shot.duration)


def test_the_camera_is_half_way_between_the_columns_at_the_crossing():
    s = _slide(cross=11.5)
    assert _at(s, 11.5).cx == pytest.approx(0.5)


def test_the_camera_stays_on_the_left_until_the_pan_begins():
    s = _slide(cross=11.5)
    for t in (0.0, 5.0, 11.5 - COLUMNS_PAN / 2):
        assert _at(s, t).cx == pytest.approx(0.25)


def test_the_camera_is_on_the_right_when_the_pan_is_over_and_stays():
    s = _slide(cross=11.5)
    for t in (11.5 + COLUMNS_PAN / 2, 15.0, DURATION):
        assert _at(s, t).cx == pytest.approx(0.75)


def test_the_pan_takes_exactly_columns_pan_seconds():
    s = _slide(cross=11.5)
    moving = [i / 100 for i in range(0, 2001)
              if 0.2501 < _at(s, i / 100).cx < 0.7499]
    # The ease is flat at both ends (cx moves < 0.0001 for the first and
    # last 0.03 s), so what can be seen moving is a hair under the pan.
    assert 0.95 * COLUMNS_PAN <= moving[-1] - moving[0] <= COLUMNS_PAN


def test_the_pan_still_opens_out_a_little_and_closes_in_again():
    s = _slide(cross=11.5)
    held, mid = _at(s, 0.0).scale, _at(s, 11.5).scale
    assert mid < held and held - mid <= 0.06
    assert _at(s, DURATION).scale == pytest.approx(held)


def test_a_crossing_too_near_the_start_still_ends_on_the_right_column():
    s = _slide(cross=0.3)
    assert _at(s, 0.0).cx >= 0.25
    assert _at(s, DURATION).cx == pytest.approx(0.75)


def test_without_a_crossing_the_pan_is_still_in_the_middle_of_the_shot():
    s = _slide()
    assert s.cross is None
    assert _at(s, DURATION / 2).cx == pytest.approx(0.5)


# -- the crossing travels with the rest of the file ------------------------

YAML = """\
fps: 24

shots:

  - id: s01
    src: media/pic.png
    voice: media/voiceover_1.wav
    in: "00:00.00"
    out: "01:00.00"
    speed: 1.2
    move: columns
    cross: 12.00
    captions:
      - text: "three"
        at: 10.00
        dur: 2.00
        words: [0.00, 1.00]
"""


def _film(tmp_path, text):
    yml = tmp_path / "film.yaml"
    yml.write_text(text, encoding="utf-8")
    return Film.load(yml, check_files=False)


def test_cross_is_read_from_film_yaml(tmp_path):
    assert _film(tmp_path, YAML).shots[0].cross == pytest.approx(12.0)


def test_fitting_by_speed_moves_the_crossing_with_the_words(tmp_path):
    film = _film(tmp_path, YAML)
    fitted = _film(tmp_path, refit_speed(YAML, film, 1.5))
    assert fitted.shots[0].cross == pytest.approx(12.0 * 1.2 / 1.5, abs=0.01)


def test_the_bench_keeps_the_crossing_on_a_save(tmp_path):
    from ffilm import editor

    media = tmp_path / "media"
    media.mkdir()
    (media / "pic.png").write_bytes(b"")
    (media / "voiceover_1.wav").write_bytes(b"")
    (tmp_path / "film.yaml").write_text(YAML, encoding="utf-8")
    (tmp_path / "film.yaml").write_text(
        editor.dump(tmp_path, editor.state(tmp_path)), encoding="utf-8")
    assert Film.load(tmp_path / "film.yaml").shots[0].cross == pytest.approx(12.0)

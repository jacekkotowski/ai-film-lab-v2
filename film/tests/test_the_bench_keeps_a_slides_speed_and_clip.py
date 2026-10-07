"""
The bench keeps a slide's speed and its clip.

2026-10-07, `projects/Screening - 95 Percent Accurate`: one Save in
`film edit` dropped `speed: 1.25` from all five slides and kept their
sped-up `duration:` (16.24 = 19.80 / 1.25 + 0.4). The words then played at
1.0 over pictures cut for 1.25: each slide's voice ran 3.5-6.5 s on under
the next one -- "two people talking from different timelines" -- and the
captions, written in the film's own (sped-up) seconds, ran ahead of it.

The take branch of `editor.dump` already wrote `speed:` back, with a
comment saying exactly why; the slide branch did not. The bench also had
no `clip:` at all (ai-manim's animation shown in place of the picture),
so the next Save would have turned every animated slide back into a still.
"""

from pytest import approx

from ffilm.spec import Film


def _round_trip(tmp_path, shot_yaml: str):
    from ffilm import editor

    media = tmp_path / "media"
    media.mkdir()
    (media / "a.png").write_bytes(b"")
    (media / "vo.wav").write_bytes(b"")
    (tmp_path / "clips").mkdir()
    (tmp_path / "clips" / "a.mp4").write_bytes(b"")
    (tmp_path / "film.yaml").write_text(
        "fps: 24\nresolution: [1080, 1920]\n\nshots:\n" + shot_yaml, encoding="utf-8")
    before = Film.load(tmp_path / "film.yaml")
    (tmp_path / "film.yaml").write_text(editor.dump(tmp_path, editor.state(tmp_path)),
                                        encoding="utf-8")
    return before, Film.load(tmp_path / "film.yaml")


SLIDE = ("  - id: s01\n"
         "    src: media/a.png\n"
         "    clip: clips/a.mp4\n"
         "    voice: media/vo.wav\n"
         '    in: "00:02.15"\n'
         '    out: "00:21.95"\n'
         "    speed: 1.25\n"
         "    move: tilt_up\n")


def test_a_slides_speed_survives_a_save(tmp_path):
    before, after = _round_trip(tmp_path, SLIDE)
    assert after.shots[0].speed == approx(1.25)
    assert after.shots[0].duration == approx(before.shots[0].duration)   # 16.24
    assert after.shots[0].duration == approx(19.80 / 1.25 + 0.4)


def test_a_slides_clip_survives_a_save(tmp_path):
    _, after = _round_trip(tmp_path, SLIDE)
    assert after.shots[0].clip == "clips/a.mp4"


def test_a_slide_held_longer_keeps_both_its_speed_and_its_length(tmp_path):
    before, after = _round_trip(tmp_path, SLIDE + "    duration: 20.00\n")
    assert after.shots[0].speed == approx(1.25)
    assert after.shots[0].duration == approx(20.0)
    assert before.shots[0].duration == approx(20.0)


def test_a_slide_at_normal_speed_gets_no_speed_line(tmp_path):
    from ffilm import editor

    plain = SLIDE.replace("    speed: 1.25\n", "")
    _round_trip(tmp_path, plain)
    assert "speed:" not in (tmp_path / "film.yaml").read_text(encoding="utf-8")
    assert editor  # imported for the round trip

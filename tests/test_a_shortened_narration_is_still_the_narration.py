"""A shortened narration is still the narration.

Jacek, 2026-10-06, Zeroing a Rifle Sight: the five slides came out of
`film go` with no captions; only the intro and the closing had any.
`go` shortens the pauses first (tighten.py) and points each slide's
`voice:` at the shorter COPY in analysis/tight/. `voice_sources` then
asked which slides quote media/voiceover_....wav, compared paths, found
none, and took the narration for one every picture had been said again
over (test_a_narration_no_shot_quotes_is_not_listened_to) -- so it was
never listened to. analysis/transcript.txt had the two camera takes and
nothing else.

The copy is the same recording, so it is heard. And it is the COPY that
is transcribed: the slides' `in`/`out` are on its clock, not the
original's, and captions timed off the original would drift by every
pause taken out before them.
"""
from types import SimpleNamespace

import json

from ffilm import kinds, scaffold, voice

NARRATION = "voiceover_20261006-112634.wav"
RETAKE = "picture1_20261006-112835.wav"
TIGHT_N = "analysis/tight/voiceover_20261006-112634__tight_9f513a4f.wav"
TIGHT_R = "analysis/tight/picture1_20261006-112835__tight_9de60803.wav"


def _project(tmp_path):
    (tmp_path / "media").mkdir()
    (tmp_path / "analysis" / "tight").mkdir(parents=True)
    for rel in (f"media/{NARRATION}", f"media/{RETAKE}", TIGHT_N, TIGHT_R):
        (tmp_path / rel).write_bytes(b"RIFF")
    return tmp_path


def _film(project, voices):
    shots = [SimpleNamespace(voice=v, src="media/x.png", kind="image")
             for v in voices]
    return SimpleNamespace(shots=shots, resolve=lambda rel: project / rel)


def test_a_shortened_copy_names_the_recording_it_was_made_from():
    assert kinds.original_stem(TIGHT_N) == "voiceover_20261006-112634"
    assert kinds.original_stem(f"media/{NARRATION}") == "voiceover_20261006-112634"


def test_slides_on_the_shortened_copy_quote_the_narration(tmp_path):
    p = _project(tmp_path)
    film = _film(p, [TIGHT_R, TIGHT_N, TIGHT_N])
    assert voice.slides_using(film, p / "media" / NARRATION) == [TIGHT_N]


def test_the_narration_and_the_retake_are_heard_from_their_copies(tmp_path):
    p = _project(tmp_path)
    film = _film(p, [TIGHT_R, TIGHT_N, TIGHT_N])
    heard = {s.label: s for s in voice.voice_sources(p, film)}
    assert set(heard) == {NARRATION, RETAKE}
    assert heard[NARRATION].audio_path == p / TIGHT_N
    assert heard[NARRATION].shot_srcs == [TIGHT_N]
    assert heard[RETAKE].audio_path == p / TIGHT_R


def test_an_unshortened_narration_is_heard_as_before(tmp_path):
    p = _project(tmp_path)
    film = _film(p, [f"media/{NARRATION}"])
    (s,) = [s for s in voice.voice_sources(p, film) if s.label == NARRATION]
    assert s.audio_path == p / "media" / NARRATION


def test_a_copy_finds_the_recording_it_was_made_from(tmp_path):
    p = _project(tmp_path)
    assert kinds.recording_of(p / TIGHT_N) == p / "media" / NARRATION
    assert kinds.recording_of(p / "media" / NARRATION) == p / "media" / NARRATION


def test_slides_cut_by_pressing_next_stay_cut_by_hand_on_the_copy(tmp_path):
    """The presses of Next are written beside the recording. Read beside
    the copy, there were none, and `caption` re-cut the slides by
    paragraph -- taking the first slide's voice (a retake) for all."""
    p = _project(tmp_path)
    (p / "media" / "voiceover_20261006-112634.cues.json").write_text(
        json.dumps({"cues": [29.4, 65.5, 82.5, 109.85],
                    "pictures": ["media/01.png", "media/02.png"]}),
        encoding="utf-8")
    film = _film(p, [TIGHT_R, TIGHT_N, TIGHT_N])
    assert scaffold.cut_by_hand(film)

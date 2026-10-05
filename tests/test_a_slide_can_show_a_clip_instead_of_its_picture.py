"""
A slide can show a clip instead of its picture.

The pictures for a film are often made in ai-manim: a still to narrate
over, then the same slide animated and timed to the words said over it.
Before this, a clip could not carry narration: on a video shot `in`/`out`
are the clip's own times, on a slide they are the words' times, and one
pair cannot be both (ai-manim PLAN step 3).

So a slide keeps everything it has -- its picture, its words, its
captions, its length -- and `clip:` names a video that is SHOWN instead
of the picture: from the clip's first frame, at normal speed (ai-manim
made it in the film's own seconds, speed already counted), full frame
(the clip is the film's shape), and nothing about the sound changes.
Clips live in clips/, not media/, so ingest and init never take one for
footage of their own.
"""

from pathlib import Path

from ffilm import render
from ffilm.moves import windows_for
from ffilm.spec import VOICE_TAIL, Shot, Window

SLIDE = {"src": "media/02_zero-group.png",
         "voice": "media/voiceover.wav", "in": 4.0, "out": 16.0,
         "speed": 1.25, "move": "columns"}


def test_a_clip_changes_nothing_about_the_words_or_the_length():
    plain = Shot.parse(dict(SLIDE), 0)
    clipped = Shot.parse(dict(SLIDE, clip="clips/02_zero-group.mp4"), 0)
    assert clipped.clip == "clips/02_zero-group.mp4"
    assert plain.clip is None
    assert clipped.kind == "still"                 # still a slide
    assert clipped.voice == plain.voice
    assert (clipped.tin, clipped.tout) == (plain.tin, plain.tout)
    assert clipped.duration == plain.duration == 12.0 / 1.25 + VOICE_TAIL


def test_the_clip_is_shown_whole_with_the_camera_still():
    shot = Shot.parse(dict(SLIDE, clip="clips/02_zero-group.mp4"), 0)
    assert windows_for(shot) == (Window(), Window())    # move: columns ignored


def test_the_clip_plays_from_its_first_frame_at_normal_speed():
    shot = Shot.parse(dict(SLIDE, clip="clips/02_zero-group.mp4"), 0)
    seen = render.picture_of(shot)
    assert Path(seen.src) == Path("clips/02_zero-group.mp4")
    assert seen.kind == "video"
    assert (seen.tin, seen.speed) == (0.0, 1.0)
    assert not render.should_memoise(shot)          # a clip moves by itself


def test_a_slide_without_a_clip_is_shown_as_before():
    shot = Shot.parse(dict(SLIDE), 0)
    assert render.picture_of(shot) is shot
    assert render.should_memoise(shot)

"""
The guide knows all three stages: one door for a stressed producer.

In ai-film-lab-v2 a film's slides, its film and its flight share one
folder (film/docs/plans/2026-10-07/UNIFY.md, phase 4). FILM.bat's guide
reads that folder as it always has and offers the other stages' steps
too, as commands it prints and runs -- SLIDES and FLY -- never importing
their code. In a toolkit unpacked on its own there are no other stages,
and nothing changes.
"""

import os
from pathlib import Path

from ffilm import guide


def repo(tmp_path: Path) -> Path:
    for stage in ("slides", "film", "fly"):
        (tmp_path / stage).mkdir()
    return tmp_path


def film(root: Path, title: str = "Screening - 95 Percent Accurate", **when) -> Path:
    """A film's folder; `when` is file -> mtime, as in test_guide."""
    proj = root / "projects" / title
    for sub in ("media", "analysis", "out", "clips"):
        (proj / sub).mkdir(parents=True, exist_ok=True)
    for rel, t in when.items():
        p = proj / {"slides": "slides.txt",
                    "published": "slides.published.json",
                    "still": "media/01_scr-accuracy.png",
                    "voice": "media/voiceover_20261007-120000.wav",
                    "manifest": "analysis/manifest.json",
                    "yml": "film.yaml",
                    "clip": "clips/01_scr-accuracy.mp4",
                    "final": "out/final.mp4"}[rel]
        p.write_bytes(b"x")
        os.utime(p, (t, t))
    return proj


def stage_steps(proj: Path, root: Path) -> list[guide.Step]:
    return guide.with_stages(proj, guide._best_steps(proj), root)


def test_slides_not_yet_put_into_the_film_are_offered_first(tmp_path):
    proj = film(repo(tmp_path), slides=100)
    s = stage_steps(proj, tmp_path)[0]
    assert s.title == "Put the slides in"
    assert s.shell == ["uv", "run", "--directory", "slides", "python", "-m",
                       "aimanim.film", "screening-95-percent-accurate", "publish"]


def test_slides_put_in_once_are_not_offered_again(tmp_path):
    """Publishing again may write over words he has narrated (agreement 2):
    that stays a thing he asks for, never ENTER."""
    proj = film(repo(tmp_path), slides=100, published=200, still=200)
    assert "Put the slides in" not in [s.title for s in stage_steps(proj, tmp_path)]


def test_narrated_slides_offer_the_timing_of_the_animation(tmp_path):
    proj = film(repo(tmp_path), slides=100, published=200, still=200,
                voice=300, manifest=400, yml=500)
    s = stage_steps(proj, tmp_path)[0]
    assert s.title == "Time the animation to your words"
    assert s.shell[-2:] == ["screening-95-percent-accurate", "clips"]


def test_clips_newer_than_the_narration_are_not_made_again(tmp_path):
    proj = film(repo(tmp_path), slides=100, published=200, still=200,
                voice=300, manifest=400, yml=600, clip=500)
    assert "Time the animation to your words" not in \
        [s.title for s in stage_steps(proj, tmp_path)]


def test_the_animation_waits_until_the_narration_is_in_the_edit(tmp_path):
    """`clips` reads the slides' captions from film.yaml, which `film go`
    writes; before that it has nothing to time to."""
    proj = film(repo(tmp_path), slides=100, published=200, still=200,
                manifest=250, yml=260, voice=300)
    assert "Time the animation to your words" not in \
        [s.title for s in stage_steps(proj, tmp_path)]


def test_a_finished_film_can_be_flown_in_3d(tmp_path):
    proj = film(repo(tmp_path), still=100, manifest=200, yml=300, final=400)
    steps = stage_steps(proj, tmp_path)
    assert steps[0].done
    fly = steps[1]
    assert fly.title == "...or fly it in 3D"
    assert fly.shell == ["python", "fly/library/rigs/fly.py", str(proj / "out")]


def test_an_unfinished_film_is_not_offered_the_flight(tmp_path):
    proj = film(repo(tmp_path), still=100, manifest=200, yml=300)
    assert "...or fly it in 3D" not in [s.title for s in stage_steps(proj, tmp_path)]


def test_a_new_film_can_start_from_a_problem_to_explain(tmp_path):
    """Two ways in: footage or photos, or a problem in words. Scenes are
    written by Claude, so that door hands over to Claude."""
    proj = film(repo(tmp_path))
    steps = stage_steps(proj, tmp_path)
    assert steps[0].folders                      # drop your files in
    slides = [s for s in steps if s.claude]
    assert [s.title for s in slides] == ["...or explain a problem with animated slides"]


def test_a_toolkit_on_its_own_offers_no_other_stage(tmp_path):
    (tmp_path / "film").mkdir()
    proj = film(tmp_path, slides=100, still=100, manifest=200, yml=300, final=400)
    steps = guide._best_steps(proj)
    assert guide.with_stages(proj, steps, tmp_path) == steps

"""
The films live in the one projects/ folder of ai-film-lab-v2.

Since 2026-10-07 slides/, film/ and fly/ are one repo, and a film's files
from all three stages share one folder, `<repo>/projects/<Title>/`
(film/docs/plans/2026-10-07/UNIFY.md). Phase 3 took the fallback to
film/projects out: there is one place, and a film that is not there is
not found. A copy made by `film pack` has the same shape -- film/ beside
projects/ -- so it needs no other place either.
"""

from pathlib import Path

import pytest

from ffilm import pack
from ffilm.paths import projects_root


def repo(tmp_path: Path) -> Path:
    (tmp_path / "film").mkdir()
    (tmp_path / "projects").mkdir()
    return tmp_path / "film"


def test_the_films_are_in_the_projects_folder_beside_film(tmp_path):
    assert projects_root(repo(tmp_path)) == tmp_path / "projects"


def test_a_projects_folder_inside_film_is_not_looked_at(tmp_path):
    film = repo(tmp_path)
    (film / "projects" / "old").mkdir(parents=True)
    assert projects_root(film) == tmp_path / "projects"


def test_a_film_packed_from_the_one_folder_arrives_under_projects(tmp_path):
    film = repo(tmp_path)
    p = tmp_path / "projects" / "morning"
    (p / "media").mkdir(parents=True)
    (p / "media" / "take.mp4").write_bytes(b"x")
    (p / "film.yaml").write_text("fps: 24", encoding="utf-8")
    (p / "out").mkdir()
    (p / "out" / "final.mp4").write_bytes(b"x")
    got = {arc for _, arc in pack.contents(film, ["morning"])}
    assert {"projects/morning/media/take.mp4", "projects/morning/film.yaml"} <= got
    assert "projects/morning/out/final.mp4" not in got


def test_packing_a_film_that_is_not_there_says_so(tmp_path):
    with pytest.raises(SystemExit):
        pack.contents(repo(tmp_path), ["nope"])

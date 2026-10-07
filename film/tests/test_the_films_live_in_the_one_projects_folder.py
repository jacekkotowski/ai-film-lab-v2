"""
The films live in the one projects/ folder of ai-film-lab-v2.

Since 2026-10-07 slides/, film/ and fly/ are one repo, and a film's files
from all three stages are to share one folder, `<repo>/projects/<Title>/`
(film/docs/plans/2026-10-07/UNIFY.md). Until that folder exists, and in a
toolkit unpacked on its own (`film pack`), the films stay where they were:
film/projects. The repo is known by its FILM.bat beside film/, so an
unrelated projects/ folder next to an unpacked toolkit is never taken.
"""

from pathlib import Path

import pytest

from ffilm import pack
from ffilm.paths import projects_root


def repo(tmp_path: Path, one_folder: bool, marker: bool = True) -> Path:
    (tmp_path / "film" / "projects").mkdir(parents=True)
    if marker:
        (tmp_path / "FILM.bat").write_text("x", encoding="utf-8")
    if one_folder:
        (tmp_path / "projects").mkdir()
    return tmp_path / "film"


def test_the_one_projects_folder_is_used_once_it_exists(tmp_path):
    assert projects_root(repo(tmp_path, one_folder=True)) == tmp_path / "projects"


def test_until_then_the_films_stay_in_film_projects(tmp_path):
    film = repo(tmp_path, one_folder=False)
    assert projects_root(film) == film / "projects"


def test_a_projects_folder_beside_an_unpacked_toolkit_is_not_taken(tmp_path):
    film = repo(tmp_path, one_folder=True, marker=False)
    assert projects_root(film) == film / "projects"


def test_a_film_packed_from_the_one_folder_arrives_under_projects(tmp_path):
    film = repo(tmp_path, one_folder=True)
    p = tmp_path / "projects" / "morning"
    (p / "media").mkdir(parents=True)
    (p / "media" / "take.mp4").write_bytes(b"x")
    (p / "film.yaml").write_text("fps: 24", encoding="utf-8")
    (p / "out").mkdir()
    (p / "out" / "final.mp4").write_bytes(b"x")
    got = {arc for _, arc in pack.contents(film, ["morning"],
                                            films=tmp_path / "projects")}
    assert got == {"projects/morning/media/take.mp4", "projects/morning/film.yaml"}


def test_packing_a_film_that_is_in_neither_place_says_so(tmp_path):
    film = repo(tmp_path, one_folder=True)
    with pytest.raises(SystemExit):
        pack.contents(film, ["nope"], films=tmp_path / "projects")

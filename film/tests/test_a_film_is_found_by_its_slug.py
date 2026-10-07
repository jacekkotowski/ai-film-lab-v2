"""A film is found by its slug.

Since 2026-10-07 a film has one name in all three stages of
ai-film-lab-v2: the slug of its folder here (slides/films/<slug>.txt,
fly/projects/<slug>/). `film ... -p screening-95-percent-accurate` finds
"Screening - 95 Percent Accurate" as the title does.
"""

from pathlib import Path

from ffilm.timeline import project_by_slug

FOLDERS = [Path("projects/Screening - 95 Percent Accurate"),
           Path("projects/Frankfurt School vs Kołakowski Emancipation and Domination"),
           Path("projects/What Is Love")]


def test_the_slug_finds_the_titled_folder():
    assert project_by_slug("screening-95-percent-accurate", FOLDERS) == FOLDERS[0]


def test_a_polish_letter_in_the_title_is_found_by_its_plain_spelling():
    assert project_by_slug("frankfurt-school-vs-kolakowski-emancipation-and-domination",
                           FOLDERS) == FOLDERS[1]


def test_a_name_that_is_no_films_slug_finds_nothing():
    assert project_by_slug("screening", FOLDERS) is None
    assert project_by_slug("", FOLDERS) is None

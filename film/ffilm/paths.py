"""
paths.py  --  where the toolkit is on this disk.

One function, so that the answer is worked out in one place. Three
modules used to compute it from their own __file__, each assuming it
sat exactly one folder below the toolkit.
"""

from pathlib import Path


def toolkit_root() -> Path:
    """Where ffilm itself lives, no matter which folder the terminal is in."""
    return Path(__file__).resolve().parent.parent


def projects_root(toolkit: Path | None = None) -> Path:
    """Where the films are. ai-film-lab-v2's one projects/ folder once it
    exists (film/docs/plans/2026-10-07/UNIFY.md), known by the repo's
    FILM.bat beside film/; until then, and in a toolkit unpacked on its
    own, film/projects."""
    toolkit = toolkit or toolkit_root()
    repo = toolkit.parent
    if (repo / "FILM.bat").is_file() and (repo / "projects").is_dir():
        return repo / "projects"
    return toolkit / "projects"

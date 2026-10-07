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
    """Where the films are: ai-film-lab-v2's one projects/ folder, beside
    film/ (film/docs/plans/2026-10-07/UNIFY.md). No second place: a copy
    made by `film pack` has the same shape."""
    return (toolkit or toolkit_root()).parent / "projects"

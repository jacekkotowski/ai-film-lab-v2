"""
A pack carries the whole repo.

2026-10-08 (review): `film pack` still had the shape of ai-film-lab before
the merge. It listed film/.claude/settings.json and film/.claude/skills,
which moved to the repo's root on 2026-10-07 (1edbc9b), so a packed copy's
Claude had no skills and no hooks wired; and it left out slides/, fly/,
SLIDES.bat, FLY.bat and the root CLAUDE.md. Of a film it left out the
slides (slides.txt, slides.script.txt), the clips its film.yaml shows, and
its flight's stops.json. Measured on Screening: 262 files, none of these.
"""

from pathlib import Path

from ffilm import pack
from ffilm.pack import contents
from ffilm.paths import toolkit_root

FILES = [
    "FILM.bat", "SLIDES.bat", "FLY.bat", "CLAUDE.md",
    ".claude/settings.json", ".claude/settings.local.json",
    ".claude/skills/new-film/SKILL.md",
    ".githooks/pre-commit", "docs/OPEN.md", "docs/SETUP.md",
    ".local/knowledge.log",
    "film/ffilm/render.py", "film/pyproject.toml", "film/uv.lock",
    "film/.claude/hooks/guard_media.py",
    "slides/aimanim/kit.py", "slides/tests/test_x.py",
    "slides/scenes/scr-cost/scene.py", "slides/scenes/scr-cost/out/scr-cost.mp4",
    "slides/.venv/pyvenv.cfg", "slides/.local/renders.csv",
    "slides/pyproject.toml", "slides/uv.lock", "slides/manim.cfg",
    "fly/library/rigs/fly.py", "fly/FLY.bat", "fly/tests/test_x.py",
    "projects/CLAUDE.md",
    "projects/F/film.yaml", "projects/F/media/take.mp4",
    "projects/F/slides.txt", "projects/F/slides.script.txt",
    "projects/F/slides.published.json", "projects/F/clips/01_a.mp4",
    "projects/F/fly/stops.json", "projects/F/fly/out/flight_film.mp4",
    "projects/F/fly/preview/opening.png", "projects/F/out/final.mp4",
    "projects/F/analysis/tight/vo__tight_c70f8e16.wav",
    "projects/F/analysis/proxies/take.mp4",
]


def repo(base: Path) -> Path:
    """A miniature of ai-film-lab-v2; returns film/, the toolkit."""
    for f in FILES:
        p = base / f
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"x")
    return base / "film"


def names(root, projects=None):
    return {arc for _, arc in contents(root, projects)}


def test_the_root_carries_the_skills_the_settings_and_the_three_doors(tmp_path):
    got = names(repo(tmp_path))
    assert {"FILM.bat", "SLIDES.bat", "FLY.bat", "CLAUDE.md",
            ".claude/settings.json", ".claude/skills/new-film/SKILL.md",
            ".githooks/pre-commit", "docs/OPEN.md", "docs/SETUP.md",
            "film/.claude/hooks/guard_media.py"} <= got


def test_the_slides_and_fly_stages_go_along(tmp_path):
    got = names(repo(tmp_path))
    assert {"slides/aimanim/kit.py", "slides/tests/test_x.py",
            "slides/scenes/scr-cost/scene.py", "slides/pyproject.toml",
            "slides/uv.lock", "slides/manim.cfg",
            "fly/library/rigs/fly.py", "fly/FLY.bat", "fly/tests/test_x.py"} <= got


def test_what_belongs_to_one_person_or_one_machine_stays(tmp_path):
    got = names(repo(tmp_path))
    for stays in (".claude/settings.local.json", ".local/knowledge.log",
                  "slides/.local/renders.csv", "slides/.venv/pyvenv.cfg",
                  "slides/scenes/scr-cost/out/scr-cost.mp4"):
        assert stays not in got


def test_a_packed_film_brings_its_slides_its_clips_and_its_flight(tmp_path):
    got = names(repo(tmp_path), ["F"])
    assert {"projects/F/slides.txt", "projects/F/slides.script.txt",
            "projects/F/slides.published.json", "projects/F/clips/01_a.mp4",
            "projects/F/fly/stops.json"} <= got
    for stays in ("projects/F/fly/out/flight_film.mp4",
                  "projects/F/fly/preview/opening.png", "projects/F/out/final.mp4"):
        assert stays not in got


def test_a_packed_film_brings_the_shortened_narration_its_slides_play(tmp_path):
    """Found by unpacking a real pack of Screening: `film check` in the copy
    said "voice file not found" for s03-s07. Their `voice:` is the copy of
    the narration with the pauses cut (analysis/tight/, decision 0015), and
    making it again means cutting again, which rewrites the edit. The rest
    of analysis/ still stays: `film ingest` makes it again."""
    got = names(repo(tmp_path), ["F"])
    assert "projects/F/analysis/tight/vo__tight_c70f8e16.wav" in got
    assert "projects/F/analysis/proxies/take.mp4" not in got


def test_every_part_the_pack_lists_is_in_the_repo():
    """A list entry that names a moved folder packs nothing and says
    nothing -- that is how the skills went missing. The shelf (library) is
    the one part that is not in git."""
    root = toolkit_root()
    missing = [n for n in pack.TOOLKIT if n != "library" and not (root / n).exists()]
    missing += [n for n in pack.REPO if not (root.parent / n).exists()]
    assert missing == []

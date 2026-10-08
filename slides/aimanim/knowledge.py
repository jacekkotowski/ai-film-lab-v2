"""knowledge.py -- this repo's knowledge, searchable on this machine (qmd).

Three qmd collections over ai-film-lab-v2 (how qmd was set up:
film/docs/tech/qmd.md):
  v2           the repo's markdown: CLAUDE.md files, skills, docs, specs, scripts
  v2-code      film/ffilm and slides/aimanim
  v2-history   one file per commit (a single file for the whole log
               gave one hit per search in film-lab), outside the repo

    python -m aimanim.knowledge setup [--drop-old]   once per machine (--drop-old:
                                          remove the collections of the old folders)
    python -m aimanim.knowledge refresh   new commit files, qmd's file lists made
                                          equal to MASK below, `qmd update`, `qmd embed`
    python -m aimanim.knowledge status    what is indexed

The post-commit hook runs `refresh` in the background. Standard library;
qmd is an outside program (npm @tobilu/qmd), found on PATH.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

# ai-film-lab-v2 (2026-10-07): one repo, three stages; the collections cover
# all of it. Before: `manim`/`manim-history` here and film-lab's own
# `docs`/`code`/`history`, all pointing at the old, now frozen folders.
ROOT = Path(__file__).resolve().parents[2]
HISTORY = Path.home() / ".cache" / "qmd" / "v2-history"
MASK = ("CLAUDE.md,docs/*.md,.claude/skills/**/*.md,"
        "slides/CLAUDE.md,slides/PLAN.md,slides/docs/**/*.md,slides/scenes/*/spec.md,"
        "projects/*/slides.script.txt,"
        "film/CLAUDE.md,film/ffilm/CLAUDE.md,film/*.md,film/docs/**/*.md,"
        "fly/*.md,fly/recipes/**/*.md")
CODE_MASK = "film/ffilm/**/*.py,film/tests/**/*.py,slides/aimanim/*.py,slides/tests/*.py"
CONTEXT = {
    "v2": "ai-film-lab-v2: Jacek's narrated films in three stages: slides (Manim), "
          "film (narration, cut, captions), fly (3D). Agreements in CLAUDE.md, "
          "skills, decisions, docs/patterns (issues and recipes), measured facts.",
    "v2-code": "ai-film-lab-v2 code: film/ffilm (the film compiler) and slides/aimanim.",
    "v2-history": "ai-film-lab-v2 git history (all three stages), one file per commit.",
}
OLD = ("manim", "manim-history", "docs", "code", "history")


def commit_file_name(date: str, short: str) -> str:
    return f"{date}-{short}.md"


def commit_text(short: str, date: str, subject: str, body: str) -> str:
    """The same shape as film-lab's history files: '# <hash> <date> <subject>'."""
    return f"# {short} {date} {subject}\n\n{body.strip()}\n"


def _git_log() -> list[tuple[str, str, str, str]]:
    sep, end = "\x1f", "\x1e"
    out = subprocess.run(["git", "log", f"--format=%h{sep}%ad{sep}%s{sep}%b{end}",
                          "--date=short"], cwd=ROOT, capture_output=True, text=True,
                         encoding="utf-8", check=True).stdout
    rows = []
    for rec in out.split(end):
        parts = rec.strip("\n").split(sep)
        if len(parts) == 4:
            rows.append(tuple(parts))
    return rows


def write_commits(folder: Path = HISTORY) -> list[str]:
    """A file for every commit that has none yet; returns the new names."""
    folder.mkdir(parents=True, exist_ok=True)
    new = []
    for short, date, subject, body in _git_log():
        p = folder / commit_file_name(date, short)
        if not p.exists():
            p.write_text(commit_text(short, date, subject, body), encoding="utf-8")
            new.append(p.name)
    return new


def _qmd(*args: str, check: bool = False) -> subprocess.CompletedProcess:
    exe = shutil.which("qmd")
    if exe is None:
        raise SystemExit("qmd is not on PATH (docs/SETUP.md)")
    return subprocess.run([exe, *args], cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=check)


def patterns_of(listing: str) -> dict[str, str]:
    """{collection: file list} from what `qmd collection list` prints."""
    found, name = {}, None
    for line in listing.splitlines():
        line = line.rstrip()
        if line.endswith("/)") and " (qmd://" in line:
            name = line.split(" (qmd://")[0].strip()
        elif name and line.strip().startswith("Pattern:"):
            found[name] = line.split("Pattern:", 1)[1].strip()
    return found


def what_to_do(name: str, mask: str, have: dict[str, str]) -> str:
    """add | keep | replace. A collection keeps the file list it was added
    with; when the files move, the list here changes and qmd's must too."""
    if name not in have:
        return "add"
    return "keep" if have[name] == mask else "replace"


def sync_collections() -> list[str]:
    """qmd's three collections with the file lists above: added if missing,
    added again if their list changed (qmd cannot change a list in place)."""
    have = patterns_of(_qmd("collection", "list").stdout)
    out = []
    for name, path, mask in (("v2", str(ROOT), MASK),
                             ("v2-code", str(ROOT), CODE_MASK),
                             ("v2-history", str(HISTORY), "**/*.md")):
        todo = what_to_do(name, mask, have)
        if todo == "keep":
            out.append(f"{name}: already there")
            continue
        if todo == "replace":
            r = _qmd("collection", "remove", name)
            if r.returncode != 0:
                out.append(f"PROBLEM removing {name}: {r.stderr[-300:]}")
                continue
        r = _qmd("collection", "add", path, "--name", name, "--mask", mask)
        if r.returncode != 0:
            out.append(f"PROBLEM {name}: {r.stderr[-500:]}")
            continue
        _qmd("context", "add", f"qmd://{name}", CONTEXT[name])
        out.append(f"{name}: added" if todo == "add"
                   else f"{name}: file list replaced (was {have[name]})")
    return out


def setup(drop_old: bool = False) -> list[str]:
    write_commits()
    out = []
    if drop_old:
        have = patterns_of(_qmd("collection", "list").stdout)
        for name in OLD:
            if name in have:
                r = _qmd("collection", "remove", name)
                out.append(f"{name}: removed (old folder)" if r.returncode == 0
                           else f"PROBLEM removing {name}: {r.stderr[-300:]}")
    return out + sync_collections()


def refresh(embed: bool = True) -> list[str]:
    new = write_commits()
    out = [f"{len(new)} new commit files"]
    out += [s for s in sync_collections() if not s.endswith("already there")]
    r = _qmd("update")
    out.append("qmd update: " + ("ok" if r.returncode == 0 else r.stderr[-300:]))
    if embed:
        r = _qmd("embed", "--chunk-strategy", "auto")
        out.append("qmd embed: " + ("ok" if r.returncode == 0 else r.stderr[-300:]))
    return out


def main(argv: list[str]) -> int:
    if argv[:1] == ["setup"]:
        print("\n".join(setup(drop_old="--drop-old" in argv)))
    elif argv[:1] == ["refresh"]:
        print("\n".join(refresh(embed="--no-embed" not in argv)))
    elif argv[:1] == ["status"]:
        print(_qmd("collection", "list").stdout)
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

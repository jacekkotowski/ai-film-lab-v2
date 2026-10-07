"""knowledge.py -- this repo's knowledge, searchable on this machine (qmd).

Two qmd collections (Workbench item 1; how qmd was set up for film-lab:
../ai-film-lab/docs/tech/qmd.md):
  manim          this repo's markdown: CLAUDE.md, PLAN.md, skills, docs/,
                 specs, film scripts
  manim-history  one file per commit (a single file for the whole log
                 gave one hit per search in film-lab), outside the repo

    python -m aimanim.knowledge setup     once per machine: add both collections
    python -m aimanim.knowledge refresh   new commit files, `qmd update`, `qmd embed`
    python -m aimanim.knowledge status    what is indexed

The post-commit hook runs `refresh` in the background. Standard library;
qmd is an outside program (npm @tobilu/qmd), found on PATH.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = Path.home() / ".cache" / "qmd" / "manim-history"
MASK = ("CLAUDE.md,PLAN.md,.claude/skills/**/*.md,docs/**/*.md,"
        "scenes/*/spec.md,films/*.script.txt")
CONTEXT = {
    "manim": "ai-manim: Manim slides for Jacek's narrated films. Skills (how to "
             "work), docs/patterns (issues and slide recipes), docs/tech (measured "
             "facts), specs (each slide's numbers and sources), film scripts.",
    "manim-history": "ai-manim git history, one file per commit: what changed and why.",
}


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


def setup() -> list[str]:
    write_commits()
    have = _qmd("collection", "list").stdout
    out = []
    for name, path, mask in (("manim", str(ROOT), MASK),
                             ("manim-history", str(HISTORY), "**/*.md")):
        if f"{name} (qmd://{name}/)" in have:
            out.append(f"{name}: already there")
            continue
        r = _qmd("collection", "add", path, "--name", name, "--mask", mask)
        out.append(f"{name}: added" if r.returncode == 0 else f"PROBLEM {name}: {r.stderr[-500:]}")
        _qmd("context", "add", f"qmd://{name}", CONTEXT[name])
    return out


def refresh(embed: bool = True) -> list[str]:
    new = write_commits()
    out = [f"{len(new)} new commit files"]
    r = _qmd("update")
    out.append("qmd update: " + ("ok" if r.returncode == 0 else r.stderr[-300:]))
    if embed:
        r = _qmd("embed", "--chunk-strategy", "auto")
        out.append("qmd embed: " + ("ok" if r.returncode == 0 else r.stderr[-300:]))
    return out


def main(argv: list[str]) -> int:
    if argv[:1] == ["setup"]:
        print("\n".join(setup()))
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

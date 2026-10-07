"""Unify plan, phase 2: every film's files into <repo>/projects/<Title>/.

    python film/docs/plans/2026-10-07/move.py           dry run: prints every step, changes nothing
    python film/docs/plans/2026-10-07/move.py --go      does it (the list is saved first)
    python film/docs/plans/2026-10-07/move.py --undo    puts everything back, newest first

Only renames on one disk: nothing is copied, nothing deleted. Before the
first move the full list goes to .local/unify/moves.json; --undo reads it.
Each fly stops.json whose paths are rewritten is kept as stops.json.pre-unify.
Standard library only. Run from the repo root.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
FILM, FLY, SLIDES = REPO / "film" / "projects", REPO / "fly" / "projects", REPO / "slides" / "films"
ONE = REPO / "projects"
LOG = REPO / ".local" / "unify" / "moves.json"
OLD_ROOT = (REPO / "film" / "projects").as_posix() + "/"
NEW_ROOT = ONE.as_posix() + "/"


def slug(name: str) -> str:
    """film/ffilm/timeline.py `slug` (slides test keeps the copies equal)."""
    name = name.replace("ł", "l").replace("Ł", "L")
    plain = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-") or "film"


def plan() -> tuple[list[tuple[str, str]], list[str]]:
    moves: list[tuple[Path, Path]] = []
    titles = {slug(p.name): p.name for p in FILM.iterdir() if p.is_dir()}
    moves.append((FILM / "CLAUDE.md", ONE / "CLAUDE.md"))
    for t in sorted(titles.values()):
        moves.append((FILM / t, ONE / t))
    for f in sorted(SLIDES.glob("*.txt")):
        s = f.name[:-len(".script.txt")] if f.name.endswith(".script.txt") else f.stem
        dest = "slides.script.txt" if f.name.endswith(".script.txt") else "slides.txt"
        moves.append((f, ONE / titles[s] / dest))
        stamp = SLIDES / s / "published.json"
        if stamp.is_file() and dest == "slides.txt":
            moves.append((stamp, ONE / titles[s] / "slides.published.json"))
    for d in sorted(p for p in FLY.iterdir() if p.is_dir()):
        moves.append((d, ONE / titles.get(d.name, d.name) / "fly"))
    if (REPO / "film" / ".lastfilm").is_file():
        moves.append((REPO / "film" / ".lastfilm", REPO / ".lastfilm"))
    rewrites = sorted(str(d / "stops.json") for d in FLY.iterdir()
                      if (d / "stops.json").is_file()
                      and OLD_ROOT in (d / "stops.json").read_text(encoding="utf-8"))
    return [(str(a), str(b)) for a, b in moves], rewrites


def problems(moves) -> list[str]:
    out = []
    targets = [b for _, b in moves]
    for a, b in moves:
        if not Path(a).exists():
            out.append(f"missing source: {a}")
        if Path(b).exists():
            out.append(f"target exists: {b}")
    if len(set(targets)) != len(targets):
        out.append("two sources go to one target")
    return out


def rel(p: str) -> str:
    return Path(p).relative_to(REPO).as_posix()


def go(moves, rewrites) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps({"moves": moves, "rewrites": rewrites}, indent=1,
                              ensure_ascii=False), encoding="utf-8")
    ONE.mkdir(exist_ok=True)
    for s in rewrites:                          # in place first, then the folder moves
        p = Path(s)
        text = p.read_text(encoding="utf-8")
        (p.parent / "stops.json.pre-unify").write_text(text, encoding="utf-8")
        p.write_text(text.replace(OLD_ROOT, NEW_ROOT), encoding="utf-8")
    for a, b in moves:
        Path(b).parent.mkdir(parents=True, exist_ok=True)
        Path(a).rename(b)
        print(f"moved  {rel(a)}  ->  {rel(b)}")


def undo() -> None:
    log = json.loads(LOG.read_text(encoding="utf-8"))
    for a, b in reversed(log["moves"]):
        if Path(b).exists() and not Path(a).exists():
            Path(a).parent.mkdir(parents=True, exist_ok=True)
            Path(b).rename(a)
            print(f"back   {rel(b)}  ->  {rel(a)}")
    for s in log["rewrites"]:
        p = Path(s)
        keep = p.parent / "stops.json.pre-unify"
        if keep.is_file():
            p.write_text(keep.read_text(encoding="utf-8"), encoding="utf-8")
            keep.unlink()
            print(f"restored  {rel(s)}")


def main() -> None:
    if sys.argv[1:] == ["--undo"]:
        return undo()
    moves, rewrites = plan()
    bad = problems(moves)
    for a, b in moves:
        print(f"{rel(a)}  ->  {rel(b)}")
    print(f"\n{len(moves)} moves; {len(rewrites)} stops.json get "
          f"'{rel(OLD_ROOT)}/' -> '{rel(NEW_ROOT)}/' in \"source\" and \"film\"")
    print("\n".join(["PROBLEMS:"] + bad) if bad else "no problems: every source exists, no target exists")
    if sys.argv[1:] == ["--go"]:
        if bad:
            sys.exit("not moved: fix the problems first")
        go(moves, rewrites)
    else:
        print("dry run: nothing changed")


if __name__ == "__main__":
    main()

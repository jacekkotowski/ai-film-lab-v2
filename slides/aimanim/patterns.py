"""patterns.py -- the pattern library (docs/patterns/) as data.

    python -m aimanim.patterns due          entries seen often enough to climb the ladder
    python -m aimanim.patterns find <word>  entries whose title or symptom has the word
    python -m aimanim.patterns list         id, status, times seen, title

The ladder (docs/patterns/README.md): note (1 slide) -> pseudocode (2) ->
code (2+) -> helper (3+, or 2 if long). `due` is run at the end of every
film (grow-skills). Standard library only.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "docs" / "patterns" / "issues.md", ROOT / "docs" / "patterns" / "tasks.md"]
LADDER = ["note", "pseudocode", "code", "helper"]
# times seen at which an entry should be at least this status
NEEDS = {2: "pseudocode", 3: "helper"}


@dataclass
class Entry:
    id: str
    title: str
    status: str          # the first ladder word in the status line
    seen: list[str]      # one item per slide (or place) it was seen on
    text: str


def parse(text: str) -> list[Entry]:
    out = []
    for block in re.split(r"(?m)^### ", text)[1:]:
        head, _, body = block.partition("\n")
        m = re.match(r"([IT]\d+)\s+—\s+(.*)", head.strip())
        if not m:
            continue
        st = re.search(r"\*\*status\*\*:\s*(.*)", body)
        status = next((w for w in LADDER if st and re.search(rf"\b{w}\b", st.group(1))), "rule")
        sn = re.search(r"\*\*seen\*\*:\s*(.*)", body)
        seen = [s.strip() for s in re.split(r",(?![^()]*\))", sn.group(1))] if sn else []
        out.append(Entry(m.group(1), m.group(2).strip(), status, [s for s in seen if s], body))
    return out


def load() -> list[Entry]:
    return [e for f in FILES if f.exists() for e in parse(f.read_text(encoding="utf-8"))]


def due(entries: list[Entry]) -> list[str]:
    """Entries below the status their number of sightings asks for."""
    out = []
    for e in entries:
        if e.status in ("helper", "rule"):
            continue
        want = max((s for n, s in NEEDS.items() if len(e.seen) >= n),
                   key=LADDER.index, default="note")
        if LADDER.index(want) > LADDER.index(e.status):
            out.append(f"{e.id} {e.status} -> {want}: seen {len(e.seen)}x — {e.title}")
    return out


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    es = load()
    if argv[:1] == ["due"]:
        print("\n".join(due(es)) or "nothing due")
    elif argv[:1] == ["find"] and len(argv) > 1:
        w = " ".join(argv[1:]).lower()
        for e in es:
            if w in e.title.lower() or w in e.text.lower():
                print(f"{e.id} [{e.status}] {e.title}")
    elif argv[:1] == ["list"]:
        for e in es:
            print(f"{e.id:4} {e.status:10} {len(e.seen)}x  {e.title}")
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

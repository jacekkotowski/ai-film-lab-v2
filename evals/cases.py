"""cases.py -- test cases for the skills, mined from the session logs.

    uv run --directory film python ../evals/cases.py routing

Phase 1 of docs/optimization/03-plan.md. A routing case is a message Jacek
typed and the repo skill Claude started for it before his next message
(the Skill tool), or "none". All messages that started a repo skill are
kept; messages that started none are sampled (seeded). A turn that started
a skill from outside the repo (update-config, claude-api...) is left out:
it is neither a repo skill nor "none".

Each case keeps Claude's last words before the message (`context`):
"build it", "yes", "1 i 3" started a skill only because of them.

The split is 40 % train, 20 % val, 40 % test, per label, seeded, and
frozen: the file is written once and never over (`freeze`). The cases hold
his own words and go to .local/evals/cases/ (git ignores it; the repo is
public).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS = Path.home() / ".claude" / "projects"
LOG_GLOB = "C--Users-jacek-code-ai-*/*.jsonl"    # this repo and the three it merged
CASES = ROOT / ".local" / "evals" / "cases"
SEED = 20261008
SHARES = {"test": 0.4, "val": 0.2}               # the rest is train
CONTEXT_CHARS = 800


def typed_text(ev: dict) -> str | None:
    """The text Jacek typed in a log event, or None (tool results, injected
    text, slash-command wrappers, meta and summary events, subagents). Pure."""
    if ev.get("type") != "user" or ev.get("isMeta") or ev.get("isCompactSummary") \
            or ev.get("isSidechain"):
        return None
    c = ev.get("message", {}).get("content")
    if isinstance(c, str):
        text = c
    elif isinstance(c, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
            return None
        text = " ".join(b.get("text", "") for b in c
                        if isinstance(b, dict) and b.get("type") == "text")
    else:
        return None
    text = text.strip()
    if not text or text.startswith("<") or "Caveat:" in text[:40]:
        return None
    return text


def turns(events: list[dict]) -> list[dict]:
    """One session's typed messages, each with the skills started before
    the next one and Claude's last words before it. Pure."""
    out, current, last_said = [], None, ""
    for ev in events:
        if ev.get("isSidechain"):
            continue
        text = typed_text(ev)
        if text:
            current = {"text": text, "skills": [], "context": last_said[-CONTEXT_CHARS:]}
            out.append(current)
            continue
        if ev.get("type") != "assistant":
            continue
        for b in ev.get("message", {}).get("content", []) or []:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "text" and b.get("text", "").strip():
                last_said = b["text"].strip()
            elif b.get("type") == "tool_use" and b.get("name") == "Skill" and current:
                name = str((b.get("input") or {}).get("skill", ""))
                if name and name not in current["skills"]:
                    current["skills"].append(name)
    return out


def label(turn: dict, repo_skills: list[str]) -> str | None:
    """The first skill the message started if it is a repo skill, "none" if
    it started nothing, None if it started a skill from elsewhere. Pure."""
    if not turn["skills"]:
        return "none"
    first = turn["skills"][0]
    return first if first in repo_skills else None


def case_id(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def split(cases: list[dict], seed: int) -> None:
    """Give each case its split, per label: 40 % test, 20 % val, the rest
    train (rounded half up; a label with one case keeps it for train)."""
    by_label: dict[str, list[dict]] = {}
    for c in cases:
        by_label.setdefault(c["label"], []).append(c)
    for name in sorted(by_label):
        group = sorted(by_label[name], key=lambda c: c["id"])
        random.Random(f"{seed}:{name}").shuffle(group)
        n_test = int(len(group) * SHARES["test"] + 0.5)
        n_val = int(len(group) * SHARES["val"] + 0.5)
        for i, c in enumerate(group):
            c["split"] = "test" if i < n_test else "val" if i < n_test + n_val else "train"


def routing_cases(all_turns: list[dict], repo_skills: list[str],
                  n_none: int, seed: int = SEED) -> list[dict]:
    """Every message that started a repo skill, n_none that started nothing,
    one case per text (a skill label wins over "none"), split. Pure."""
    best: dict[str, dict] = {}
    for t in all_turns:
        lab = label(t, repo_skills)
        if lab is None:
            continue
        old = best.get(t["text"])
        if old is None or (old["label"] == "none" and lab != "none"):
            best[t["text"]] = {"id": case_id(t["text"]), "text": t["text"],
                               "context": t["context"], "label": lab,
                               "started": t["skills"]}
    skills = [c for c in best.values() if c["label"] != "none"]
    nones = sorted((c for c in best.values() if c["label"] == "none"),
                   key=lambda c: c["id"])
    nones = random.Random(f"{seed}:none-sample").sample(nones, min(n_none, len(nones)))
    out = sorted(skills + nones, key=lambda c: c["id"])
    split(out, seed)
    return out


def freeze(cases: list[dict], path: Path) -> None:
    """Write the cases once. A frozen file is never written over: a case
    that is in test stays there."""
    if path.exists():
        raise FileExistsError(f"{path} is frozen; it is not written over")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cases, ensure_ascii=False, indent=1), encoding="utf-8")


def read_logs(logs: Path = LOGS) -> list[dict]:
    out = []
    for f in sorted(logs.glob(LOG_GLOB)):
        events = []
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                events.append(json.loads(line))
            except ValueError:
                continue
        for t in turns(events):
            t["session"] = f.stem
            out.append(t)
    return out


def repo_skills(root: Path = ROOT) -> list[str]:
    return sorted(p.parent.name for p in (root / ".claude" / "skills").glob("*/SKILL.md"))


def table(cases: list[dict]) -> str:
    rows = {}
    for c in cases:
        rows.setdefault(c["label"], {"train": 0, "val": 0, "test": 0})[c["split"]] += 1
    lines = [f"{'label':22} train val test"]
    for name in sorted(rows, key=lambda k: (k == "none", k)):
        r = rows[name]
        lines.append(f"{name:22} {r['train']:5} {r['val']:3} {r['test']:4}")
    tot = {s: sum(r[s] for r in rows.values()) for s in ("train", "val", "test")}
    lines.append(f"{'all':22} {tot['train']:5} {tot['val']:3} {tot['test']:4}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="evals/cases.py")
    ap.add_argument("what", choices=["routing"])
    ap.add_argument("--none", type=int, default=None,
                    help="messages that started nothing (default: as many as started a skill)")
    a = ap.parse_args(argv)
    skills = repo_skills()
    all_turns = read_logs()
    n_skill = len({t["text"] for t in all_turns
                   if label(t, skills) not in (None, "none")})
    cs = routing_cases(all_turns, skills, n_none=a.none if a.none is not None else n_skill)
    path = CASES / "routing.json"
    print(f"{len(all_turns)} typed messages in the logs; "
          f"{n_skill} distinct ones started a repo skill")
    print(table(cs))
    try:
        freeze(cs, path)
    except FileExistsError as e:
        print(e)
        return 1
    print("written:", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

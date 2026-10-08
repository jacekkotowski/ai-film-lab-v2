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


def film_of(path: str) -> str | None:
    """The film whose film.yaml this path is, None for any other file and
    for the test projects (test_story, zz_*). Pure."""
    p = str(path).replace("\\", "/")
    if not p.endswith("/film.yaml") or "/projects/" not in p:
        return None
    film = p.rsplit("/projects/", 1)[1].split("/")[0]
    return None if film == "test_story" or film.startswith("zz_") else film


def edit_notes(events: list[dict]) -> list[dict]:
    """One session's notes: each typed message followed by an Edit of a
    film's film.yaml before the next one, per film, with Claude's edits in
    order, his next message and whether `film undo` ran. Pure."""
    out, current, last_said = [], None, ""
    for ev in events:
        if ev.get("isSidechain"):
            continue
        text = typed_text(ev)
        if text:
            if current:
                for n in current.values():
                    n["next"] = text
            current = {}
            note = {"text": text, "context": last_said[-CONTEXT_CHARS:], "at": ev.get("timestamp")}
            continue
        if ev.get("type") != "assistant":
            continue
        for b in ev.get("message", {}).get("content", []) or []:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "text" and b.get("text", "").strip():
                last_said = b["text"].strip()
            if b.get("type") != "tool_use" or current is None:
                continue
            inp = b.get("input") or {}
            if b.get("name") in ("Bash", "PowerShell") and "film undo" in str(inp.get("command", "")):
                for n in current.values():
                    n["undo"] = True
            film = film_of(inp.get("file_path", "")) if b.get("name") in ("Edit", "Write", "MultiEdit") else None
            if not film:
                continue
            if film not in current:
                current[film] = {**note, "film": film, "edits": [], "undo": False, "next": ""}
                out.append(current[film])
            at = ev.get("timestamp")
            if b["name"] == "Write":
                current[film]["edits"].append({"at": at, "content": inp.get("content", "")})
            for e in (inp.get("edits") or [inp]) if b["name"] != "Write" else []:
                current[film]["edits"].append({"at": at, "old": e.get("old_string", ""),
                                               "new": e.get("new_string", ""),
                                               "all": bool(e.get("replace_all"))})
    return out


def apply_edits(text: str, edits: list[dict]) -> tuple[str, int]:
    """The text with the edits applied in order, and how many did not fit
    (their old string was not in it). Pure."""
    missing = 0
    for e in edits:
        if "content" in e:
            text = e["content"]
        elif e["old"] in text:
            text = text.replace(e["old"], e["new"], -1 if e["all"] else 1)
        else:
            missing += 1
    return text, missing


def epoch(iso: str) -> float:
    from datetime import datetime
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()


def lf(text: str) -> str:
    return text.replace("\r\n", "\n")


def edit_pass_case(note: dict, history) -> dict:
    """A note made into a case. `history(film)` gives the film.yaml's
    commits as (time, sha, text), oldest first. The before is the last
    commit before the first edit; the after is the before with the edits.
    "clean" when every edit fits, the next commit after the last edit is
    that after, and no `film undo` ran; else "doubtful" and why. Pure."""
    versions = sorted(history(note["film"]))
    first, last = epoch(note["edits"][0]["at"]), epoch(note["edits"][-1]["at"])
    before = [v for v in versions if v[0] <= first]
    after = [v for v in versions if v[0] > last]
    case = {"id": case_id(f"{note['film']}|{note['at']}|{note['text']}"),
            "film": note["film"], "note": note["text"], "context": note["context"],
            "at": note["at"], "next": note["next"],
            "before_commit": before[-1][1] if before else None,
            "after_commit": after[0][1] if after else None}
    why = []
    if not before:
        why.append("no commit of the film.yaml before the edit")
        case.update(before=None, after=None)
    else:
        b = lf(before[-1][2])
        a, missing = apply_edits(b, [{**e, "old": lf(e["old"]), "new": lf(e["new"])}
                                     if "old" in e else {"content": lf(e["content"])}
                                     for e in note["edits"]])
        case.update(before=b, after=a)
        if missing:
            why.append(f"{missing} of {len(note['edits'])} edits not found in the committed before")
        if not after:
            why.append("no commit of the film.yaml after the edit")
        elif lf(after[0][2]) != a:
            why.append("the next commit differs from the edits")
    if note["undo"]:
        why.append("film undo ran after it")
    case.update(status="doubtful" if why else "clean", why="; ".join(why))
    return case


def git_history(film: str, root: Path = ROOT) -> list[tuple[float, str, str]]:
    """Every commit of a film's film.yaml as (time, sha, text). The file was
    at projects/<film>/ in ai-film-lab's history and after unify, and at
    film/projects/<film>/ in between (2026-10-07)."""
    import subprocess
    paths = [f"projects/{film}/film.yaml", f"film/projects/{film}/film.yaml"]
    log = subprocess.run(["git", "-C", str(root), "log", "--format=%ct %H", "--", *paths],
                         capture_output=True, text=True, encoding="utf-8").stdout
    out = []
    for line in log.splitlines():
        t, sha = line.split()
        for p in paths:
            r = subprocess.run(["git", "-C", str(root), "show", f"{sha}:{p}"],
                               capture_output=True, text=True, encoding="utf-8")
            if r.returncode == 0:
                out.append((float(t), sha[:7], r.stdout))
                break
    return out


def read_sessions(logs: Path = LOGS) -> list[tuple[str, list[dict]]]:
    out = []
    for f in sorted(logs.glob(LOG_GLOB)):
        events = []
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                events.append(json.loads(line))
            except ValueError:
                continue
        out.append((f.stem, events))
    return out


def read_logs(logs: Path = LOGS) -> list[dict]:
    out = []
    for stem, events in read_sessions(logs):
        for t in turns(events):
            t["session"] = stem
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


def edit_pass_main() -> int:
    """Every note with its before and after, written to a candidates file
    (not frozen: the doubtful ones go to Jacek first, then the clean set is
    split and frozen)."""
    histories: dict[str, list] = {}

    def history(film):
        if film not in histories:
            histories[film] = git_history(film)
        return histories[film]

    cs = []
    for stem, events in read_sessions():
        for n in edit_notes(events):
            c = edit_pass_case(n, history)
            c["session"] = stem
            cs.append(c)
    cs.sort(key=lambda c: c["at"] or "")
    for c in cs:
        print(f"{c['status']:8} {c['at'][:16]} {c['film'][:24]:24} "
              f"{c['before_commit'] or '-':7} -> {c['after_commit'] or '-':7} "
              f"{' '.join(c['note'].split())[:60]}" + (f"\n         {c['why']}" if c["why"] else ""))
    print(f"{len(cs)} notes; clean {sum(c['status'] == 'clean' for c in cs)}")
    path = CASES / "edit-pass.candidates.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cs, ensure_ascii=False, indent=1), encoding="utf-8")
    print("written:", path)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="evals/cases.py")
    ap.add_argument("what", choices=["routing", "edit-pass"])
    ap.add_argument("--none", type=int, default=None,
                    help="messages that started nothing (default: as many as started a skill)")
    a = ap.parse_args(argv)
    if a.what == "edit-pass":
        return edit_pass_main()
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

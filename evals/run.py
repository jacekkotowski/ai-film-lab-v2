"""run.py -- a skill's test cases, run through `claude -p` and graded.

    uv run --directory film python ../evals/run.py probe
    uv run --directory film python ../evals/run.py routing   [--split train|val|test] [--cases N]
                                                             [--ids ID ...] [--max-turns T]
    uv run --directory film python ../evals/run.py edit-pass [--split train|test] [--cases N]

Run in film's environment so the film checks can use ffilm itself
(spec.Film.load, moves.FAMILY) instead of copies of them. No new
dependency: subprocess + json, and `claude` from PATH (the subscription;
there is no API key on this machine).

Every test run is boxed in (docs/optimization/03-plan.md):
  - tools: Skill, Read, Glob, Grep only -- no Edit, Write or Bash exists
    in the run, so no render, no git, no file written;
  - `--strict-mcp-config`: no MCP tools either (without it the claude.ai
    connectors -- Gmail, Calendar -- were in the run's tool list, measured);
  - settings: user + project. With the user's alone the repo's 19 skills
    are not loaded (measured 2026-10-08), so routing could not be tested;
  - `--permission-mode dontAsk`: anything not allowed is refused, not asked;
  - `--no-session-persistence`: test runs do not land in the session logs
    the cases are mined from;
  - `--max-budget-usd` per case.
An edit-pass run needs Edit on a scratch copy only; the project's allow
list says "Edit" everywhere, so that box is not built yet (OPEN.md).
The cases hold Jacek's own words and live in .local/evals/ (git ignores
it; the repo is public).
"""
from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / ".local" / "evals"
WORK = LOCAL / "work"
RESULTS = LOCAL / "results.csv"
MODEL = "claude-opus-5-5"           # what his sessions run (8,213 messages measured)
TIMEOUT_S = 600

READ_TOOLS = "Skill,Read,Glob,Grep"


# ---------------------------------------------------------------- the call

def claude_cmd(prompt: str, *, tools: str = READ_TOOLS,
               allow: list[str] | None = None,
               append: str | None = None, budget: float = 1.0,
               max_turns: int | None = None, model: str = MODEL) -> list[str]:
    """The `claude -p` command line for one test run. Pure."""
    cmd = ["claude", "-p", prompt,
           "--output-format", "stream-json", "--verbose",
           "--model", model,
           "--tools", tools,
           "--strict-mcp-config",
           "--setting-sources", "user,project",
           "--permission-mode", "dontAsk",
           "--no-session-persistence",
           "--max-budget-usd", f"{budget:g}"]
    if allow:
        cmd += ["--allowedTools", *allow]
    if append:
        cmd += ["--append-system-prompt", append]
    if max_turns:
        cmd += ["--max-turns", str(max_turns)]
    return cmd


def skill_started(tool: str, inp: dict) -> str | None:
    """The skill a tool call starts, if any. Pure.

    The Skill tool names it; a Read of .claude/skills/<name>/SKILL.md (or
    plugin-namespaced `plugin:name`) is the same choice made by hand."""
    if tool == "Skill" and inp.get("skill"):
        return str(inp["skill"])
    if tool == "Read":
        parts = str(inp.get("file_path", "")).replace("\\", "/").split("/")
        if len(parts) >= 3 and parts[-1] == "SKILL.md" and parts[-3] == "skills":
            return parts[-2]
    return None


def repo_skills(root: Path = ROOT) -> list[str]:
    """The skills this repo has: one folder each under .claude/skills/."""
    return sorted(p.parent.name for p in (root / ".claude" / "skills").glob("*/SKILL.md"))


def box_problems(s: dict, want_skills: list[str], tools: str = READ_TOOLS) -> list[str]:
    """Why a run was NOT boxed in, from its init event. Pure.

    Any tool beyond the ones asked for (Edit, Write, Bash, an MCP tool) is a
    problem; so is a repo skill the run could not see."""
    allowed = set(tools.split(","))
    extra = [t for t in s["init_tools"] if t not in allowed]
    missing = [k for k in want_skills if k not in s["init_skills"]]
    out = []
    if not s["init_tools"]:
        out.append("no init event")
    if extra:
        out.append(f"{len(extra)} tools beyond {sorted(allowed)}, e.g. {extra[:3]}")
    if missing:
        out.append(f"{len(missing)} repo skills not loaded, e.g. {missing[:3]}")
    return out


def summarize(lines: list[str]) -> dict:
    """What a run did, from its stream-json lines. Pure.

    tools: every tool call in order, as (name, short input);
    skills: the skills it started, in order -- by the Skill tool, or by
      Reading .claude/skills/<name>/SKILL.md itself (measured 2026-10-08:
      in `claude -p` it often reads the file instead of calling Skill;
      skill-creator's run_eval counts the Read too);
    init_skills, init_tools: what the run had, from its `init` event;
    cost, tokens, turns, subtype: from the closing `result` event;
    denied: the tool calls the permission mode refused.
    """
    out = {"tools": [], "skills": [], "cost": None, "tokens": {},
           "turns": None, "subtype": None, "denied": [], "text": "",
           "init_skills": [], "init_tools": []}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        kind = ev.get("type")
        if kind == "system" and ev.get("subtype") == "init":
            out["init_skills"] = list(ev.get("skills", []) or [])
            out["init_tools"] = list(ev.get("tools", []) or [])
        elif kind == "assistant":
            for b in ev.get("message", {}).get("content", []) or []:
                if b.get("type") == "tool_use":
                    name, inp = b.get("name", ""), b.get("input", {}) or {}
                    short = inp.get("skill") or inp.get("file_path") \
                        or inp.get("pattern") or ""
                    out["tools"].append((name, str(short)))
                    started = skill_started(name, inp)
                    if started and started not in out["skills"]:
                        out["skills"].append(started)
                elif b.get("type") == "text":
                    out["text"] += b.get("text", "")
        elif kind == "result":
            out["cost"] = ev.get("total_cost_usd")
            out["turns"] = ev.get("num_turns")
            out["subtype"] = ev.get("subtype")
            out["tokens"] = ev.get("usage", {}) or {}
            for d in ev.get("permission_denials", []) or []:
                out["denied"].append((d.get("tool_name", ""),
                                      str((d.get("tool_input") or {}).get("file_path", ""))))
    return out


def run_claude(cmd: list[str], cwd: Path = ROOT) -> dict:
    """Run one `claude -p`, return its summary plus seconds and the raw lines."""
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=str(cwd), env=env, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    try:
        out, err = p.communicate(timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        p.kill()
        out, err = p.communicate()
    lines = out.decode("utf-8", errors="replace").splitlines()
    s = summarize(lines)
    s["seconds"] = round(time.time() - t0, 1)
    s["exit"] = p.returncode
    s["stderr"] = err.decode("utf-8", errors="replace")[-500:]
    s["raw"] = lines
    return s


# ---------------------------------------------------------- staying safe

def snapshot() -> dict:
    """What a test run must not change: git status, every file time under
    projects/, and .lastfilm (film check rewrites it)."""
    status = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"],
                            capture_output=True, text=True).stdout
    times = {}
    for p in (ROOT / "projects").rglob("*"):
        try:
            times[str(p)] = p.stat().st_mtime_ns
        except OSError:
            pass
    last = ROOT / ".lastfilm"
    return {"status": status, "times": times,
            "lastfilm": last.read_text(encoding="utf-8") if last.exists() else None}


def changed(before: dict, after: dict) -> list[str]:
    """What differs between two snapshots, in words. Pure."""
    out = []
    if before["status"] != after["status"]:
        out.append("git status changed")
    moved = [k for k, v in after["times"].items() if before["times"].get(k) != v]
    gone = [k for k in before["times"] if k not in after["times"]]
    if moved:
        out.append(f"{len(moved)} files under projects/ changed, e.g. {moved[0]}")
    if gone:
        out.append(f"{len(gone)} files under projects/ gone, e.g. {gone[0]}")
    if before["lastfilm"] != after["lastfilm"]:
        out.append(".lastfilm changed")
    return out


# ------------------------------------------------------------------ probe

def probe() -> int:
    """Phase 0: is a routing run boxed in, does it see the repo's skills,
    and what does one case cost?"""
    LOCAL.mkdir(parents=True, exist_ok=True)
    target = LOCAL / "probe_target.txt"
    target.write_text("untouched\n", encoding="utf-8")
    want = repo_skills()

    before = snapshot()
    runs = [
        ("routing: status", "where am I with Screening - 95 Percent Accurate? what's left?"),
        ("routing: slide", "make a slide about the bearing to a landmark, 30 degrees off north"),
        ("routing: shot drags", "in What Is Love, shot 3 drags and the caption on s05 is too early"),
        ("box: try to write", f"Replace the word 'untouched' with 'changed' in {target}. "
                              "Use any tool you have. Say which tool you used."),
    ]
    problems, costs = [], []
    for name, prompt in runs:
        s = run_claude(claude_cmd(prompt, budget=1.0, max_turns=3))
        costs.append(s["cost"] or 0.0)
        box = box_problems(s, want)
        problems += [f"{name}: {p}" for p in box]
        u = s["tokens"]
        print(f"\n== {name}: {s['subtype']}, {s['seconds']} s, ${s['cost']}, turns {s['turns']}")
        print("   skills started:", s["skills"] or "-")
        print("   tool calls:", [t for t, _ in s["tools"]] or "-")
        if s["denied"]:
            print("   refused:", s["denied"])
        print(f"   tokens: cache-read {u.get('cache_read_input_tokens')}, "
              f"cache-write {u.get('cache_creation_input_tokens')}, out {u.get('output_tokens')}")
        print(f"   box: {len(s['init_tools'])} tools {sorted(s['init_tools'])}, "
              f"{sum(k in s['init_skills'] for k in want)}/{len(want)} repo skills loaded"
              + (f"; PROBLEM {box}" if box else ""))
    after = snapshot()

    got = target.read_text(encoding="utf-8").strip()
    target.unlink(missing_ok=True)
    diff = changed(before, after)
    if got != "untouched":
        problems.append(f"the probe file was changed to {got!r}")
    problems += diff
    print("\n== the box")
    print("   probe file:", got, "(must be 'untouched')")
    print("   repo:", "; ".join(diff) if diff else "git status, projects/ and .lastfilm unchanged")
    print(f"   cost: {len(costs)} runs, ${sum(costs):.2f} in all, "
          f"${min(costs):.2f}-${max(costs):.2f} each")
    print("   BOXED IN" if not problems else "   NOT BOXED IN: " + "; ".join(problems))
    return 0 if not problems else 1


# ---------------------------------------------------------------- routing

def choice(skills: list[str]) -> str:
    """What a routing run chose: the first skill it started, or "none". Pure."""
    return skills[0] if skills else "none"


def context_prompt(case: dict) -> str | None:
    """Claude's last words before the message, for the system prompt, so the
    message itself goes in as he typed it. None when it opened a session. Pure."""
    if not case.get("context"):
        return None
    return ("This message comes in the middle of a session. Your own last "
            "message before it ended with:\n\n" + case["context"])


def routing_cmd(case: dict, max_turns: int, budget: float = 0.5) -> list[str]:
    return claude_cmd(case["text"], append=context_prompt(case),
                      max_turns=max_turns, budget=budget)


def routing_table(rows: list[dict]) -> dict:
    """Per skill: should start (label), did start (choice), right, missed
    (chose none), wrong (chose another skill). Pure."""
    names = sorted({r["label"] for r in rows} | {r["got"] for r in rows} - {"none"})
    out = {}
    for n in names:
        if n == "none":
            continue
        mine = [r for r in rows if r["label"] == n]
        out[n] = {"should": len(mine),
                  "did": sum(r["got"] == n for r in rows),
                  "right": sum(r["got"] == n for r in mine),
                  "missed": sum(r["got"] == "none" for r in mine),
                  "wrong": sum(r["got"] not in (n, "none") for r in mine)}
    return out


def confusion_pairs(rows: list[dict]) -> dict:
    """(label, choice) -> count, for every case the run got wrong. Pure."""
    out: dict = {}
    for r in rows:
        if r["label"] != r["got"]:
            out[(r["label"], r["got"])] = out.get((r["label"], r["got"]), 0) + 1
    return out


def skills_hash(root: Path = ROOT) -> str:
    """One fingerprint of all the repo's SKILL.md files: a result belongs to it."""
    h = hashlib.sha1()
    for p in sorted((root / ".claude" / "skills").glob("*/SKILL.md")):
        h.update(p.name.encode() + p.parent.name.encode() + p.read_bytes())
    return h.hexdigest()[:10]


def append_results(rows: list[dict], path: Path = RESULTS) -> None:
    cols = ["date", "target", "skills_hash", "case", "split", "label", "got", "pass",
            "max_turns", "cost", "tokens_in", "tokens_out", "seconds", "box"]
    new = not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerows(rows)


def routing(split: str | None, n: int | None, ids: list[str] | None,
            max_turns: int, show: bool = False) -> int:
    cases = json.loads((LOCAL / "cases" / "routing.json").read_text(encoding="utf-8"))
    if split:
        cases = [c for c in cases if c["split"] == split]
    if ids:
        cases = [c for c in cases if c["id"] in ids]
    if n:
        cases = cases[:n]
    want = repo_skills()
    fp = skills_hash()
    before = snapshot()
    rows = []
    for i, c in enumerate(cases, 1):
        s = run_claude(routing_cmd(c, max_turns=max_turns))
        u = s["tokens"]
        box = box_problems(s, want)
        row = {"date": datetime.datetime.now().isoformat(timespec="seconds"),
               "target": "routing", "skills_hash": fp, "case": c["id"],
               "split": c["split"], "label": c["label"], "got": choice(s["skills"]),
               "max_turns": max_turns, "cost": s["cost"],
               "tokens_in": sum(u.get(k) or 0 for k in ("input_tokens",
                                "cache_read_input_tokens", "cache_creation_input_tokens")),
               "tokens_out": u.get("output_tokens"), "seconds": s["seconds"],
               "box": "; ".join(box)}
        row["pass"] = int(row["got"] == row["label"])
        rows.append(row)
        append_results([row])
        print(f"{i:3}/{len(cases)} {c['id']} {c['split']:5} {c['label']:20} -> "
              f"{row['got']:20} {'ok ' if row['pass'] else 'NO '} ${s['cost']} "
              f"{s['seconds']} s {s['subtype']}" + (f" BOX {box}" if box else ""))
        print("      " + " | ".join(f"{t} {Path(x).name if '/' in x or chr(92) in x else x}"[:60]
                                    for t, x in s["tools"]))
        if show:
            print("      said: " + " ".join(s["text"].split())[-600:])
    diff = changed(before, snapshot())

    print(f"\n{'skill':20} should did right missed wrong")
    for name, t in routing_table(rows).items():
        print(f"{name:20} {t['should']:6} {t['did']:3} {t['right']:5} "
              f"{t['missed']:6} {t['wrong']:5}")
    nones = [r for r in rows if r["label"] == "none"]
    print(f"{'none':20} {len(nones):6} {sum(r['got'] == 'none' for r in rows):3} "
          f"{sum(r['got'] == 'none' for r in nones):5}")
    pairs = confusion_pairs(rows)
    if pairs:
        print("\nconfusion (label -> chose):")
        for (a, b), k in sorted(pairs.items(), key=lambda x: -x[1]):
            print(f"  {a} -> {b}: {k}")
    costs = [r["cost"] or 0.0 for r in rows]
    if rows:
        print(f"\n{sum(r['pass'] for r in rows)}/{len(rows)} right; "
              f"${sum(costs):.2f} in all, ${min(costs):.2f}-${max(costs):.2f} per case, "
              f"mean ${sum(costs) / len(rows):.3f}; max-turns {max_turns}; skills {fp}")
    print("repo:", "; ".join(diff) if diff else "git status, projects/ and .lastfilm unchanged")
    return 0 if not diff and not any(r["box"] for r in rows) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="evals/run.py")
    ap.add_argument("what", choices=["probe", "routing"])
    ap.add_argument("--split", choices=["train", "val", "test"])
    ap.add_argument("--cases", type=int, help="only the first N cases")
    ap.add_argument("--ids", nargs="*", help="only these case ids")
    ap.add_argument("--max-turns", type=int, default=3)
    ap.add_argument("--show", action="store_true", help="print what each run said")
    a = ap.parse_args(argv)
    if a.what == "probe":
        return probe()
    if a.what == "routing":
        return routing(a.split, a.cases, a.ids, a.max_turns, a.show)
    return 2


if __name__ == "__main__":
    sys.exit(main())

"""look.py -- render a scene and look at it, in one command each.

Every slide was made by the same loop: render, fish the [layout] lines
out of Manim's progress bars, check the size, measure the margins in
pixels, and for a clip pull a frame per step to see the motion. Each was
typed by hand per slide (screening film, 2026-10-06); here each is one
command. Standard library + ffmpeg/ffprobe + `uv run` (decision 0002:
Manim stays in kit.py; this only starts it).

    python -m aimanim.look still <scene>          half-size still: notes, size, margins
    python -m aimanim.look still <scene> full     the full-size still he narrates over
    python -m aimanim.look draft <scene>          half-size clip: notes, length, steps.png
    python -m aimanim.look margins <png>          ink margins of any picture
    python -m aimanim.look sheet <film>           docs/films/<film>.png, the contact sheet
    python -m aimanim.look film <film>            all of the above for every slide + timing
    python -m aimanim.look stats                  renders per scene, issues that came back

Every render is logged to .local/renders.csv (this machine only), each
note tagged with its docs/patterns/issues.md entry.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from aimanim import beats, frame

ROOT = Path(__file__).resolve().parents[1]
SIZES = {"half": (540, 960), "full": (frame.WIDTH, frame.HEIGHT)}
# at full size: the caption zone and the side margin (slide-layout §5)
MIN_BOTTOM, MIN_SIDE = 480, 60
TOL = 12        # grey levels from the background that count as ink


# ---- pure ------------------------------------------------------------------

def ink_box(gray: bytes, w: int, h: int, bg: int, tol: int = TOL):
    """(left, top, right, bottom) MARGINS in px of everything that differs
    from the background by more than `tol` grey levels; None if blank."""
    rows = [y for y in range(h) if max(abs(v - bg) for v in gray[y * w:(y + 1) * w]) > tol]
    if not rows:
        return None
    cols_hit = [False] * w
    for y in rows:
        line = gray[y * w:(y + 1) * w]
        for x in range(w):
            if not cols_hit[x] and abs(line[x] - bg) > tol:
                cols_hit[x] = True
    xs = [x for x in range(w) if cols_hit[x]]
    return xs[0], rows[0], w - 1 - xs[-1], h - 1 - rows[-1]


def margin_notes(box, w: int) -> list[str]:
    """Margins against the rules, scaled to the picture's width."""
    if box is None:
        return ["blank picture"]
    k = w / frame.WIDTH
    l, t, r, b = box
    notes = [f"margins px: left {l}, right {r}, top {t}, bottom {b}"
             + ("" if k == 1 else f" (at {w} wide; full size x{1 / k:g})")]
    if b < MIN_BOTTOM * k:
        notes.append(f"PROBLEM: ink {MIN_BOTTOM * k - b:.0f} px into the caption zone")
    for side, v in (("left", l), ("right", r)):
        if v < MIN_SIDE * k:
            notes.append(f"PROBLEM: {side} margin {v} px < {MIN_SIDE * k:.0f}")
    return notes


# Which docs/patterns/issues.md entry a printed note is an example of, so
# the render log can count what keeps coming back (Workbench item 5).
ISSUE_OF = [
    (r"past SIDE", "I01"),
    (r'" touches "', "I02"),
    (r"above TOP|into the caption zone|ink .* into the caption zone", "I04"),
    (r"margin .* px <", "I05"),
    (r"touches a (Line|Rectangle)", "I10"),
    (r"touches a ", "I09"),
    (r"starts .* after|runs .* past the words", "I16"),
    (r"was not heard|not in the script", "I17"),
]


def issue_ids(notes: list[str]) -> list[str]:
    """The issue entry of each note that has one (first matching rule)."""
    import re
    out = []
    for n in notes:
        for pat, iid in ISSUE_OF:
            if re.search(pat, n):
                out.append(iid)
                break
    return out


LOG = ROOT / ".local" / "renders.csv"
LOG_HEAD = "when,scene,kind,size,seconds,notes,issues\n"


def log_render(scene: str, kind: str, size: str, seconds: float, notes: list[str],
               path: Path = LOG, when: str | None = None) -> None:
    """One line per render, kept on this machine only (.gitignore)."""
    from datetime import datetime
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(LOG_HEAD, encoding="utf-8")
    probs = [n for n in notes if n.startswith(("[layout]", "[beats]", "PROBLEM"))
             and "no timing.json" not in n]
    line = (f"{when or datetime.now().isoformat(timespec='seconds')},{scene},{kind},{size},"
            f"{seconds:.1f},{len(probs)},{' '.join(issue_ids(probs))}\n")
    with path.open("a", encoding="utf-8") as f:
        f.write(line)


def stats_of(rows: list[dict]) -> list[str]:
    """Renders per scene and the issues that came back most."""
    from collections import Counter
    per = Counter(r["scene"] for r in rows)
    secs = Counter()
    for r in rows:
        secs[r["scene"]] += float(r["seconds"])
    issues = Counter(i for r in rows for i in r["issues"].split())
    out = [f"{len(rows)} renders, {sum(secs.values()) / 60:.1f} min"]
    out += [f"  {s}: {n} renders, {secs[s]:.0f} s" for s, n in per.most_common()]
    out.append("issues seen (docs/patterns/issues.md): " +
               (", ".join(f"{i} x{n}" for i, n in issues.most_common()) or "none"))
    return out


def step_end_frames(waits: list[int], run_times: list[float], fps: int) -> list[int]:
    """The frame index (0-based) at which each step has just finished,
    the way kit.run draws them (beats.in_frames)."""
    out, n = [], 0
    for w, rt in zip(waits, run_times):
        n += w + beats.play_frames(rt, fps)
        out.append(n - 1)
    return out


# ---- files and tools ---------------------------------------------------------

def _gray(png: Path) -> tuple[bytes, int, int]:
    w, h = _size(png)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(png), "-f", "rawvideo",
                          "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    return raw, w, h


def _size(path: Path) -> tuple[int, int]:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height", "-of", "csv=p=0",
                          str(path)], capture_output=True, text=True, check=True).stdout
    w, h = out.strip().split(",")[:2]
    return int(w), int(h)


def _seconds(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True,
                         check=True).stdout
    return float(out.strip())


def _bg_gray() -> int:
    r, g, b = (int(frame.BACKGROUND[i:i + 2], 16) for i in (1, 3, 5))
    return round(0.299 * r + 0.587 * g + 0.114 * b)


def margins(png: Path) -> list[str]:
    gray, w, h = _gray(png)
    return margin_notes(ink_box(gray, w, h, _bg_gray()), w)


def _manim(scene: str, size: str, still: bool) -> list[str]:
    import time
    w, h = SIZES[size]
    cmd = ["uv", "run", "--extra", "render", "manim"] + (["-s"] if still else []) + [
        "-r", f"{w},{h}", "--media_dir", f"scenes/{scene}/out",
        f"scenes/{scene}/scene.py", "Slide"]
    t0 = time.monotonic()
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    keep = [ln.strip()[ln.strip().find("["):] for ln in (r.stdout + r.stderr).splitlines()
            if "[layout]" in ln or "[beats]" in ln]
    keep = list(dict.fromkeys(keep))           # a note printed twice is one note
    if r.returncode != 0:
        keep.append("PROBLEM: manim failed\n" + r.stderr[-2500:])
    log_render(scene, "still" if still else "clip", size, time.monotonic() - t0, keep)
    return keep


def still(scene: str, size: str = "half") -> list[str]:
    out = _manim(scene, size, still=True)
    png = sorted((ROOT / "scenes" / scene / "out" / "images" / "scene").glob("Slide_*.png"))[-1]
    w, h = _size(png)
    return out + [f"{png.relative_to(ROOT)}  {w}x{h}  {png.stat().st_size:,} bytes"] + margins(png)


def draft(scene: str) -> list[str]:
    """Half-size clip, its length, and steps.png: the frame at the end of
    every step, side by side -- the motion's result without watching."""
    out = _manim(scene, "half", still=False)
    d = ROOT / "scenes" / scene
    mp4 = d / "out" / "videos" / "scene" / "960p24" / "Slide.mp4"
    b = beats.scene_beats(d / "scene.py")
    rts = b.get("RUN_TIMES", [])
    p = beats.for_scene(d, b.get("BEAT_LINES", []), rts, b.get("BEAT_WORDS"))
    waits, _ = beats.in_frames(p, rts, frame.FPS)
    ends = step_end_frames(waits, rts, frame.FPS)
    sheet = d / "out" / "steps.png"
    sel = "+".join(f"eq(n\\,{n})" for n in ends)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf",
                    f"select='{sel}',scale=270:-1,tile={len(ends)}x1",
                    "-frames:v", "1", str(sheet)], check=True)
    return out + [f"{mp4.relative_to(ROOT)}  {_seconds(mp4):.2f} s",
                  f"{sheet.relative_to(ROOT)}  the end of steps 1..{len(ends)}, "
                  f"frames {ends}"]


def sheet(film_name: str) -> list[str]:
    from aimanim import film as _film
    f, _ = _film.load(film_name)
    pngs = [_film.still_of(ROOT / "scenes" / s.scene) for s in f.slides]
    out = ROOT / "docs" / "films" / f"{film_name}.png"
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for p in pngs:
        cmd += ["-i", str(p)]
    n = len(pngs)
    cmd += ["-filter_complex", f"hstack=inputs={n},scale={n * 270}:-1", str(out)]
    subprocess.run(cmd, check=True)
    return [f"{out.relative_to(ROOT)}  {n} stills"]


def film_report(film_name: str) -> list[str]:
    """Everything about a film in one report: each slide's full-size still
    (the one he narrates over) with its notes and margins, the rehearsal
    of its timing, and the contact sheet."""
    from aimanim import film as _film
    f, _ = _film.load(film_name)
    out = []
    for s in f.slides:
        lines = still(s.scene, "full")
        bad = [ln for ln in lines if ln.startswith(("[layout]", "PROBLEM"))]
        out.append(f"{s.name}: " + ("ok" if not bad else f"{len(bad)} to fix"))
        out += [f"  {ln}" for ln in lines if not ln.startswith("[beats] no timing")]
    out.append("timing (rehearsed):")
    out += [f"  {ln}" for ln in _film.check(film_name) if "PROBLEM" in ln or ln.startswith("film:")]
    out += sheet(film_name)
    n = sum("PROBLEM" in ln or "[layout]" in ln for ln in out)
    out.append(f"{film_name}: {len(f.slides)} slides, {n} problem lines")
    return out


def stats() -> list[str]:
    import csv
    if not LOG.exists():
        return ["no renders logged yet (.local/renders.csv)"]
    with LOG.open(encoding="utf-8") as fh:
        return stats_of(list(csv.DictReader(fh)))


def main(argv: list[str]) -> int:
    cmds = {"still": still, "draft": draft, "sheet": sheet, "film": film_report,
            "margins": lambda p: margins(Path(p))}
    if argv[:1] == ["stats"]:
        print("\n".join(stats()))
        return 0
    if not argv or argv[0] not in cmds or len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    lines = cmds[argv[0]](*argv[1:])
    print("\n".join(lines))
    return 1 if any("PROBLEM" in ln for ln in lines) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

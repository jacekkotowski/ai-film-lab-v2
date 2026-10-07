"""film.py -- a film's slides, in order, straight into its ai-film-lab project.

A film is `films/<name>.txt`:

    project: Zeroing a Rifle Sight     # ai-film-lab/projects/<this>
    01 zero-group                      # picture number, scene
    02 zero-clicks

and its words are `films/<name>.script.txt`, sections marked `[intro]`,
`[01]`, `[02]`... `[outro]`. Two moments, one command each:

  publish   before narrating. Creates the film-lab project if needed
            (film-lab's own `film new`), puts each FULL-SIZE still into
            its media/ as NN_<scene>.png, and the words where the
            recording window shows them: narration.txt (one paragraph per
            picture), script_intro.txt, script_outro.txt. A script file
            changed in film-lab since the last publish is left alone.

  clips     after narrating and `film go`. Reads each slide's captions
            from film.yaml -- film-lab writes them in the film's own
            seconds from the start of the shot, after pause-cutting and
            speed -- writes the scene's timing.json, renders the clip at
            full size, puts it in clips/NN_<scene>.mp4 and adds
            `clip: clips/NN_<scene>.mp4` under the slide in film.yaml.

Decision 0003 (ai-manim writes into its film-lab project). Standard
library only; film.yaml is read by film-lab's own Python.

  check     any time before narrating: each slide's BEAT_WORDS / BEAT_LINES
            / RUN_TIMES rehearsed against its paragraph at 2.5 words/s,
            with the same matcher the clips use. Renders nothing.

    python -m aimanim.film zeroing check
    python -m aimanim.film zeroing publish
    python -m aimanim.film zeroing clips
"""

from __future__ import annotations

import json
import os
import re
import shutil
import struct
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from aimanim import beats, frame

ROOT = Path(__file__).resolve().parents[1]
# ai-film-lab-v2: the film stage is the sibling folder film/ of this one
# (slides/). Before 2026-10-07 it was the separate repo ../ai-film-lab.
FILMLAB = Path(os.environ.get("AIMANIM_FILMLAB", ROOT.parent / "film"))


@dataclass
class Slide:
    picture: int          # place among the pictures narrated over, 1-based
    scene: str            # folder under scenes/

    @property
    def name(self) -> str:
        return f"{self.picture:02d}_{self.scene}"


@dataclass
class Film:
    project: str = ""                 # folder name under ai-film-lab/projects
    slides: list[Slide] = field(default_factory=list)


# ---- pure: the two text files ----------------------------------------------

def parse(text: str) -> Film:
    """The film file: 'project: <name>', then '<picture> <scene>' per line."""
    f = Film()
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.lower().startswith("project:"):
            f.project = line.split(":", 1)[1].strip()
            continue
        parts = line.split()
        if len(parts) != 2 or not parts[0].isdigit():
            raise ValueError(f"line {n}: want '<picture> <scene>', got {raw!r}")
        f.slides.append(Slide(int(parts[0]), parts[1]))
    pics = [s.picture for s in f.slides]
    if len(set(pics)) != len(pics):
        raise ValueError(f"a picture number is used twice: {pics}")
    if pics != sorted(pics):
        raise ValueError(f"picture numbers must go up: {pics}")
    return f


MARK = re.compile(r"^\[(intro|outro|\d+)\]", re.I)


def script_parts(text: str) -> dict[str, str]:
    """The script's sections: 'intro', 'outro', '01', '02'... -> words.
    A line of dashes ends the script (notes may follow it)."""
    parts: dict[str, list[str]] = {}
    key = None
    for raw in text.splitlines():
        if raw.startswith("-----"):
            break
        m = MARK.match(raw.strip())
        if m:
            k = m.group(1).lower()
            key = k if not k.isdigit() else f"{int(k):02d}"
            parts.setdefault(key, [])
            continue
        if key is not None:
            parts[key].append(raw)
    return {k: " ".join(" ".join(v).split()) for k, v in parts.items()}


def narration_text(film: Film, parts: dict[str, str]) -> str:
    """narration.txt as film-lab reads it: one paragraph per picture, in
    picture order; a picture with no words is '-'."""
    return "\n\n".join(parts.get(f"{s.picture:02d}", "") or "-"
                       for s in film.slides) + "\n"


def with_clip(yaml_text: str, picture: str, clip: str) -> str:
    """film.yaml AS TEXT with `clip:` under the slide whose src is
    `picture` -- added, or corrected if it names another clip. Comments
    and layout stay as they were."""
    lines = yaml_text.splitlines(keepends=True)
    for i, ln in enumerate(lines):
        m = re.match(r"^(\s*)(- )?src:\s*(\S+)\s*$", ln.rstrip("\r\n"))
        if not m or m.group(3).strip("'\"") != picture:
            continue
        indent = m.group(1) + ("  " if m.group(2) else "")
        nl = "\r\n" if ln.endswith("\r\n") else "\n"
        j = i + 1                                  # this shot's other keys
        while j < len(lines) and lines[j].startswith(indent) and \
                not lines[j].lstrip().startswith("- "):
            if re.match(rf"^{indent}clip:", lines[j]):
                lines[j] = f"{indent}clip: {clip}{nl}"
                return "".join(lines)
            j += 1
        lines.insert(i + 1, f"{indent}clip: {clip}{nl}")
        return "".join(lines)
    raise LookupError(f"no shot with src: {picture} in film.yaml")


def timing_from(shot: dict) -> beats.Timing:
    """A film-lab slide (as read_slides gives it) -> the scene's timing."""
    lines = [beats.Line(c["text"], round(c["at"], 3), round(c["at"] + c["dur"], 3),
                        [round(c["at"] + w, 3) for w in c.get("words") or []])
             for c in shot["captions"]]
    return beats.Timing(lines, round(shot["duration"], 3), f"film.yaml {shot['id']}")


# ---- files ------------------------------------------------------------------

def png_size(path: Path) -> tuple[int, int]:
    """Width and height from a PNG's header (IHDR is always first)."""
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError(f"{path} is not a PNG")
    return struct.unpack(">II", head[16:24])


def seconds(path: Path) -> float | None:
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                              "format=duration", "-of", "csv=p=0", str(path)],
                             capture_output=True, text=True, check=True).stdout
        return float(out.strip())
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        return None


def still_of(scene_dir: Path) -> Path | None:
    found = sorted((scene_dir / "out" / "images" / "scene").glob("Slide_*.png"))
    return found[-1] if found else None


def clip_of(scene_dir: Path) -> Path:
    return (scene_dir / "out" / "videos" / "scene" /
            f"{frame.HEIGHT}p{frame.FPS}" / "Slide.mp4")


def load(name: str, root: Path = ROOT) -> tuple[Film, dict[str, str]]:
    film = parse((root / "films" / f"{name}.txt").read_text(encoding="utf-8"))
    sp = root / "films" / f"{name}.script.txt"
    parts = script_parts(sp.read_text(encoding="utf-8")) if sp.exists() else {}
    return film, parts


def project_dir(film: Film) -> Path:
    if not film.project:
        raise SystemExit("the film file has no 'project: <name>' line")
    return FILMLAB / "projects" / film.project


def render(scene: str, still: bool) -> list[str]:
    """Render a scene at full size; return its [beats]/[layout] notes."""
    cmd = ["uv", "run", "--extra", "render", "manim"] + (["-s"] if still else []) + [
        "-r", f"{frame.WIDTH},{frame.HEIGHT}",
        "--media_dir", f"scenes/{scene}/out", f"scenes/{scene}/scene.py", "Slide"]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"{scene}: manim failed\n{r.stderr[-2000:]}")
    return [ln.strip() for ln in (r.stdout + r.stderr).splitlines()
            if ln.strip().startswith(("[beats]", "[layout]"))]


def stale_stills(media: Path, film: Film, root: Path = ROOT) -> list[Path]:
    """Stills this repo published earlier that the film no longer has: named
    NN_<one of our scenes>.png, but not a current slide's name. A slide
    renumbered 04 -> 05 would otherwise stay in film-lab as an extra
    picture. Anything not named after one of our scenes is never touched."""
    ours = {d.name for d in (root / "scenes").iterdir() if d.is_dir()}
    now = {f"{s.name}.png" for s in film.slides}
    return sorted(p for p in media.glob("[0-9][0-9]_*.png")
                  if p.name not in now and p.stem[3:] in ours)


# ---- the two moments -----------------------------------------------------------

def publish(name: str, root: Path = ROOT) -> list[str]:
    film, parts = load(name, root)
    proj = project_dir(film)
    report = []
    if not proj.exists():
        subprocess.run(["uv", "run", "film", "new", film.project], cwd=FILMLAB,
                       check=True, capture_output=True)
        report.append(f"created {proj}")
    (proj / "media").mkdir(parents=True, exist_ok=True)

    for s in film.slides:
        d = root / "scenes" / s.scene
        png = still_of(d)
        if png is None or png_size(png) != (frame.WIDTH, frame.HEIGHT):
            notes = render(s.scene, still=True)
            png = still_of(d)
            report += [f"  {s.name}: {n}" for n in notes]
        shutil.copy2(png, proj / "media" / f"{s.name}.png")
        report.append(f"media/{s.name}.png  {png_size(png)[0]}x{png_size(png)[1]}")

    for old in stale_stills(proj / "media", film, root):
        old.unlink()
        report.append(f"media/{old.name}  removed: no longer in the film")

    # the words, where the recording window shows them -- never over a
    # file Jacek changed in film-lab since the last publish
    stamp = root / "films" / name / "published.json"
    last = json.loads(stamp.read_text(encoding="utf-8")) if stamp.exists() else {}
    files = {"narration.txt": narration_text(film, parts)}
    if parts.get("intro"):
        files["script_intro.txt"] = parts["intro"] + "\n"
    if parts.get("outro"):
        files["script_outro.txt"] = parts["outro"] + "\n"
    for fname, text in files.items():
        p = proj / fname
        if p.exists():
            now = p.read_text(encoding="utf-8")
            if now == text:
                report.append(f"{fname}  unchanged")
                continue
            if now != last.get(fname):
                report.append(f"{fname}  NOT written: changed in film-lab "
                              f"since the last publish")
                continue
        p.write_text(text, encoding="utf-8")
        last[fname] = text
        report.append(f"{fname}  written")
    stamp.parent.mkdir(parents=True, exist_ok=True)
    stamp.write_text(json.dumps(last, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


READ_SLIDES = r"""
import json, sys
from pathlib import Path
from ffilm.spec import Film
f = Film.load(Path(sys.argv[1]))
print(json.dumps([{"id": s.id, "src": s.src, "duration": s.duration,
                   "clip": s.clip, "captions": [{"text": c.text, "at": c.at,
                   "dur": c.dur, "words": c.words} for c in s.captions]}
                  for s in f.shots if s.voice]))
"""


def read_slides(proj: Path) -> list[dict]:
    """The narrated slides of film.yaml, read by film-lab's own loader."""
    r = subprocess.run(["uv", "run", "python", "-c", READ_SLIDES,
                        str(proj / "film.yaml")], cwd=FILMLAB,
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(f"film-lab could not read {proj / 'film.yaml'}:\n"
                         f"{r.stderr[-1500:]}")
    return json.loads(r.stdout.strip().splitlines()[-1])


def clips(name: str, root: Path = ROOT) -> list[str]:
    film, _ = load(name, root)
    proj = project_dir(film)
    if not (proj / "film.yaml").exists():
        raise SystemExit(f"no film.yaml in {proj} yet: narrate, then `film go` there")
    shots = {Path(s["src"]).name: s for s in read_slides(proj)}
    (proj / "clips").mkdir(exist_ok=True)
    report = []
    yml = proj / "film.yaml"
    for s in film.slides:
        shot = shots.get(f"{s.name}.png")
        if shot is None:
            report.append(f"{s.name}: not a narrated slide in film.yaml")
            continue
        t = timing_from(shot)
        (root / "scenes" / s.scene / "timing.json").write_text(
            t.to_json() + "\n", encoding="utf-8")
        notes = render(s.scene, still=False)
        clip = proj / "clips" / f"{s.name}.mp4"
        shutil.copy2(clip_of(root / "scenes" / s.scene), clip)
        rel = f"clips/{s.name}.mp4"
        text = yml.read_bytes().decode("utf-8")      # keeps CRLF as it is
        new = with_clip(text, f"media/{s.name}.png", rel)
        if new != text:
            yml.write_bytes(new.encode("utf-8"))
        got = seconds(clip)
        report.append(f"{s.name}: {len(t.lines)} lines, slide {t.total:.2f} s, "
                      f"clip {got:.2f} s" if got is not None else
                      f"{s.name}: clip written (ffprobe missing: length unchecked)")
        report += [f"    {n}" for n in notes]
    return report


def check(name: str, root: Path = ROOT) -> list[str]:
    """Before he narrates: every slide's steps rehearsed against its
    paragraph of the script (beats.rehearse, 2.5 words/s). Nothing is
    rendered or written."""
    film, parts = load(name, root)
    report, total = [], 0.0
    for s in film.slides:
        words = parts.get(f"{s.picture:02d}", "")
        b = beats.scene_beats(root / "scenes" / s.scene / "scene.py")
        report.append(f"{s.name}")
        if not words:
            report.append("  PROBLEM: no paragraph in the script")
            continue
        lines = beats.rehearse(words, b.get("BEAT_WORDS", []), b.get("BEAT_LINES", []),
                               b.get("RUN_TIMES", []))
        total += beats.rehearsal(words).total
        report += [f"  {ln}" for ln in lines]
    for k in ("intro", "outro"):
        if parts.get(k):
            total += beats.rehearsal(parts[k]).total
    report.append(f"film: ~{total:.0f} s ({total / 60:.1f} min) at "
                  f"{beats.SPEAK_WPS} words/s")
    return report


def narrated(name: str, root: Path = ROOT) -> bool:
    """Every slide has a timing.json: its clips follow his real voice, so a
    rehearsal (a prediction) no longer matters."""
    film, _ = load(name, root)
    return all((root / "scenes" / s.scene / "timing.json").exists() for s in film.slides)


def gate(root: Path = ROOT) -> list[str]:
    """For the pre-commit hook: rehearse every film not yet narrated; any
    PROBLEM line fails the commit. Narrated films are skipped."""
    out = []
    for f in sorted((root / "films").glob("*.txt")):
        if f.name.endswith(".script.txt"):
            continue
        name = f.stem
        if narrated(name, root):
            out.append(f"{name}: narrated, skipped")
            continue
        probs = [ln for ln in check(name, root) if "PROBLEM" in ln]
        out.append(f"{name}: " + ("rehearsed, ok" if not probs else f"{len(probs)} PROBLEM"))
        out += probs
    return out


COMMANDS = {"publish": publish, "clips": clips, "check": check}


def main(argv: list[str]) -> int:
    if argv == ["--gate"]:
        lines = gate()
        print("\n".join(lines))
        return 1 if any("PROBLEM" in ln for ln in lines) else 0
    if len(argv) != 2 or argv[1] not in COMMANDS:
        print("python -m aimanim.film <film> check | publish | clips", file=sys.stderr)
        return 2
    print("\n".join(COMMANDS[argv[1]](argv[0])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

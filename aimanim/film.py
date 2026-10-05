"""film.py -- the order of a film's slides, and its files gathered in that order.

A film is `films/<name>.txt`: one line per slide, "<picture> <scene>",
where <picture> is the slide's place in the narration (photos made
elsewhere fill the gaps). This module

  - gathers each scene's FULL-SIZE still (and clip, once made) into
    `films/<name>/<NN>_<scene>.png|.mp4`, refusing anything not 1080x1920;
  - with --timing "<film-lab project>", writes each scene's timing.json
    from the narration (aimanim.beats, the two files decision 0001 allows);
  - with --to "<film-lab project>", PRINTS the one copy command for Jacek.
    It never copies into ai-film-lab itself (decision 0001).

Standard library only.

    python -m aimanim.film zeroing
    python -m aimanim.film zeroing --timing "<film-lab project>"
    python -m aimanim.film zeroing --to "<film-lab project>"
"""

from __future__ import annotations

import json
import shutil
import struct
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from aimanim import beats, frame

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Slide:
    picture: int          # place in the narration, 1-based
    scene: str            # folder under scenes/

    @property
    def name(self) -> str:
        return f"{self.picture:02d}_{self.scene}"


def parse(text: str) -> list[Slide]:
    """The film file: '<picture> <scene>' per line, '#' starts a comment."""
    slides = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2 or not parts[0].isdigit():
            raise ValueError(f"line {n}: want '<picture> <scene>', got {raw!r}")
        slides.append(Slide(int(parts[0]), parts[1]))
    pics = [s.picture for s in slides]
    if len(set(pics)) != len(pics):
        raise ValueError(f"a picture number is used twice: {pics}")
    if pics != sorted(pics):
        raise ValueError(f"picture numbers must go up: {pics}")
    return slides


def png_size(path: Path) -> tuple[int, int]:
    """Width and height from a PNG's header (IHDR is always first)."""
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError(f"{path} is not a PNG")
    return struct.unpack(">II", head[16:24])


def clip_size(path: Path) -> tuple[int, int, float] | None:
    """Width, height, seconds by ffprobe; None if ffprobe is not here."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height:format=duration",
             "-of", "json", str(path)],
            capture_output=True, text=True, check=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    d = json.loads(out)
    s = d["streams"][0]
    return s["width"], s["height"], float(d["format"]["duration"])


def still_of(scene_dir: Path) -> Path | None:
    found = sorted((scene_dir / "out" / "images" / "scene").glob("Slide_*.png"))
    return found[-1] if found else None


def clip_of(scene_dir: Path) -> Path | None:
    p = scene_dir / "out" / "videos" / "scene" / f"{frame.HEIGHT}p{frame.FPS}" / "Slide.mp4"
    return p if p.exists() else None


def gather(film: str, root: Path = ROOT) -> list[str]:
    """Copy the full-size files into films/<film>/, numbered. Returns the
    report lines; a slide that is missing or the wrong size is named there
    and nothing is copied for it."""
    slides = parse((root / "films" / f"{film}.txt").read_text(encoding="utf-8"))
    out = root / "films" / film
    out.mkdir(parents=True, exist_ok=True)
    for old in list(out.glob("*.png")) + list(out.glob("*.mp4")):
        old.unlink()                      # only what this command made
    report = []
    for s in slides:
        d = root / "scenes" / s.scene
        if not d.is_dir():
            report.append(f"{s.name}: NO SCENE scenes/{s.scene}")
            continue
        png = still_of(d)
        if png is None:
            report.append(f"{s.name}: no still -- render it: "
                          f"manim -s -r {frame.WIDTH},{frame.HEIGHT}")
        elif png_size(png) != (frame.WIDTH, frame.HEIGHT):
            w, h = png_size(png)
            report.append(f"{s.name}: still is {w}x{h}, not full size -- "
                          f"re-render with -r {frame.WIDTH},{frame.HEIGHT}")
        else:
            shutil.copy2(png, out / f"{s.name}.png")
            report.append(f"{s.name}.png  {frame.WIDTH}x{frame.HEIGHT}  "
                          f"{png.stat().st_size // 1024} KB")
        mp4 = clip_of(d)
        if mp4 is not None:
            info = clip_size(mp4)
            shutil.copy2(mp4, out / f"{s.name}.mp4")
            tail = (f"{info[0]}x{info[1]}  {info[2]:.3f} s" if info
                    else "(ffprobe not found: size unchecked)")
            report.append(f"{s.name}.mp4  {tail}")
    return report


def write_timings(film: str, project: Path, root: Path = ROOT) -> list[str]:
    """timing.json for every slide of the film, from the narration."""
    slides = parse((root / "films" / f"{film}.txt").read_text(encoding="utf-8"))
    report = []
    for s in slides:
        t = beats.timing_for(project, s.picture)
        (root / "scenes" / s.scene / "timing.json").write_text(
            t.to_json() + "\n", encoding="utf-8")
        report.append(f"{s.name}: {len(t.lines)} lines, {t.total:.2f} s")
        for i, line in enumerate(t.lines):
            report.append(f"    {i}  {line.start:6.2f}  {line.text}")
    return report


def main(argv: list[str]) -> int:
    if not argv or argv[0].startswith("-"):
        print(__doc__.strip().splitlines()[-3].strip(), file=sys.stderr)
        return 2
    film, rest = argv[0], argv[1:]
    if rest[:1] == ["--timing"] and len(rest) == 2:
        print("\n".join(write_timings(film, Path(rest[1]))))
        return 0
    print("\n".join(gather(film)))
    if rest[:1] == ["--to"] and len(rest) == 2:
        src = ROOT / "films" / film
        print("\nCopy into the film (you run this; ai-manim does not):")
        print(f'Copy-Item "{src}\\*" "{Path(rest[1]) / "media"}\\"')
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

"""beats.py -- when each step of an animation starts, from what was said.

Narration comes first (docs/decisions/0001). Jacek narrates over the
scene's still inside an ai-film-lab project; this module reads where his
sentences fell over that picture and turns them into waits for Manim.

Standard library only: it is imported by every scene and by the tests,
and neither should need Manim installed to know when to move.

    python -m aimanim.beats "<film-lab project>" <picture N> > scenes/<slug>/timing.json
"""

from __future__ import annotations

import json
import sys
import wave
from dataclasses import asdict, dataclass, field
from pathlib import Path

# A wait shorter than one frame at 24 fps is not a wait, and Manim
# refuses a zero-length one.
MIN_WAIT = 1 / 24

# With no narration yet, steps are spaced this far apart, so the still
# and the draft can be made before anything is recorded.
PLACEHOLDER_GAP = 1.0


@dataclass
class Line:
    text: str
    start: float          # seconds from the start of THIS picture
    end: float


@dataclass
class Timing:
    lines: list[Line]
    total: float          # how long the picture is narrated, seconds
    source: str = ""      # which take it came from, for humans

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)

    @staticmethod
    def from_json(text: str) -> "Timing":
        d = json.loads(text)
        return Timing([Line(**x) for x in d["lines"]], float(d["total"]),
                      d.get("source", ""))


@dataclass
class Plan:
    waits: list[float]    # before each step
    tail: float           # after the last step, to the end of the words
    late: float = 0.0     # seconds the animation runs past the words
    notes: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------
# Pure: from a take to one picture's lines
# --------------------------------------------------------------------------


def picture_span(cues: list[float], n: int, total: float) -> tuple[float, float]:
    """Where picture `n` (1-based) is narrated inside the whole take.

    ai-film-lab's cues are the moments the NEXT picture began, so six
    pictures have five cues.
    """
    bounds = [0.0, *cues, total]
    if not 1 <= n <= len(bounds) - 1:
        raise ValueError(f"picture {n}: this take has {len(bounds) - 1} pictures")
    return bounds[n - 1], bounds[n]


def lines_in(lines: list[dict], span: tuple[float, float]) -> list[Line]:
    """The sentences that START inside the span, timed from its start."""
    s, e = span
    return [Line(str(x["text"]), round(x["start"] - s, 3),
                 round(min(x["end"], e) - s, 3))
            for x in lines if s <= x["start"] < e]


def plan(starts: list[float], run_times: list[float], total: float) -> Plan:
    """Waits that put step i on starts[i], each step lasting run_times[i].

    A step that cannot start on time (the one before is still running)
    starts as soon as it can, and the plan says so -- a silent drift is
    the thing that makes an animation feel out of step with the voice.
    """
    if len(starts) != len(run_times):
        raise ValueError(f"{len(starts)} starts for {len(run_times)} steps")
    t, waits, notes = 0.0, [], []
    for i, (want, rt) in enumerate(zip(starts, run_times)):
        if want < t - 1e-9:
            notes.append(f"step {i + 1} starts {t - want:.2f}s after its sentence")
        w = max(0.0, want - t)
        waits.append(round(w, 3))
        t += w + rt
    late = max(0.0, t - total)
    if late:
        notes.append(f"the animation runs {late:.2f}s past the words")
    return Plan(waits, round(max(0.0, total - t), 3), round(late, 3), notes)


def placeholder(run_times: list[float]) -> tuple[list[float], float]:
    """Starts and a total for a scene nobody has narrated yet."""
    starts, t = [], 0.0
    for rt in run_times:
        t += PLACEHOLDER_GAP
        starts.append(t)
        t += rt
    return starts, t + PLACEHOLDER_GAP


def starts_for(timing: Timing, beat_lines: list[int]) -> list[float]:
    """beat_lines[i] = which sentence (0-based) step i belongs to."""
    if beat_lines and max(beat_lines) >= len(timing.lines):
        raise ValueError(f"a step names sentence {max(beat_lines) + 1}, "
                         f"but only {len(timing.lines)} were said over this picture")
    return [timing.lines[k].start for k in beat_lines]


# --------------------------------------------------------------------------
# Reading an ai-film-lab project (read only -- decision 0001)
# --------------------------------------------------------------------------


def wav_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / float(w.getframerate())


def newest_cues(project: Path) -> Path:
    found = sorted((project / "media").glob("voiceover_*.cues.json"))
    if not found:
        raise FileNotFoundError(f"no narration in {project / 'media'}")
    return found[-1]       # names carry the date and time, so last = newest


def timing_for(project: Path, n: int) -> Timing:
    cues_path = newest_cues(project)
    wav = cues_path.with_name(cues_path.name.replace(".cues.json", ".wav"))
    cues = json.loads(cues_path.read_text(encoding="utf-8"))["cues"]
    transcript = json.loads(
        (project / "analysis" / "transcript.json").read_text(encoding="utf-8"))
    src = next((s for s in transcript["sources"] if s["source"] == wav.name), None)
    if src is None:
        raise LookupError(f"{wav.name} is not transcribed yet in "
                          f"{project / 'analysis'} -- run the film's edit first")
    span = picture_span(cues, n, wav_seconds(wav))
    return Timing(lines_in(src["lines"], span), round(span[1] - span[0], 3),
                  f"{wav.name} picture {n}")


# --------------------------------------------------------------------------
# What a scene calls
# --------------------------------------------------------------------------


def for_scene(scene_dir: Path, beat_lines: list[int],
              run_times: list[float]) -> Plan:
    """The plan for one scene: timed to timing.json if it exists, spaced
    evenly if not. Problems are printed, because Manim's own log is where
    Jacek is looking while it renders."""
    path = Path(scene_dir) / "timing.json"
    if path.exists():
        timing = Timing.from_json(path.read_text(encoding="utf-8"))
        p = plan(starts_for(timing, beat_lines), run_times, timing.total)
    else:
        starts, total = placeholder(run_times)
        p = plan(starts, run_times, total)
        p.notes.insert(0, "no timing.json: steps spaced evenly (not narrated yet)")
    for note in p.notes:
        print(f"[beats] {note}", file=sys.stderr)
    return p


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[-1].strip(), file=sys.stderr)
        return 2
    print(timing_for(Path(argv[0]), int(argv[1])).to_json())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

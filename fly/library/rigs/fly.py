"""
fly.py - one command from an ai-film-lab film to its 3D flight. No internet,
no Claude: only Python (standard library), Blender and ffmpeg.

  python library/rigs/fly.py <film>              new project -> stills
  python library/rigs/fly.py <slug> --draft      a project you already have
  python library/rigs/fly.py <slug> --video

<film> is any of: the film's final.timeline.json, its final.mp4 (the
timeline must sit beside it), its out/ folder or its project folder.
<slug> is a folder name under projects/, e.g. what-is-love: the film's one
name in slides/, film/ and fly/ (no month in front since 2026-10-07).

A new film gets projects/<slug>/stops.json, then the stills. After
the stills (and the draft) it asks what to do next. An existing stops.json is
never overwritten, so your edits to titles are kept. FLY.bat calls this.
"""

import glob
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import webbrowser
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[2]
RIGS = STUDIO / "library" / "rigs"
PROJECTS = STUDIO / "projects"
REPO = STUDIO.parent
BLENDER_GUESSES = [
    r"C:\Program Files\Blender\blender.exe",
    r"C:\Program Files\Blender Foundation\Blender*\blender.exe",
    "/Applications/Blender.app/Contents/MacOS/Blender",
]
YOUTUBE_UPLOAD = "https://www.youtube.com/upload"
TAKES = {"stills": "about 30 s", "draft": "a few minutes", "video": "about 10 minutes"}


def find_blender():
    """BLENDER if set, then PATH, then the usual install folders (newest first)."""
    if os.environ.get("BLENDER"):
        return os.environ["BLENDER"]
    on_path = shutil.which("blender")
    if on_path:
        return on_path
    for guess in BLENDER_GUESSES:
        found = sorted(glob.glob(guess), reverse=True)
        if found:
            return found[0]
    sys.exit("Cannot find Blender. Install it (winget install BlenderFoundation.Blender)\n"
             "or tell me where it is:  set BLENDER=C:\\path\\to\\blender.exe")


def find_timeline(path):
    """The final.timeline.json for whatever part of a film was given."""
    p = Path(path).resolve()
    candidates = {
        ".json": [p],
        ".mp4": [p.with_suffix(".timeline.json")],
    }.get(p.suffix.lower()) or [p / "final.timeline.json", p / "out" / "final.timeline.json"]
    for c in candidates:
        if c.is_file():
            return c
    sys.exit(f"No timeline found for {p}.\nLooked for: " + ", ".join(str(c) for c in candidates)
             + "\nRun 'film final' in ai-film-lab first: it writes final.timeline.json beside final.mp4.")


def slugify(title):
    """film/ffilm/timeline.py `slug`, for timelines older than 0014: the
    Polish ł has no NFKD form, so it is spelled out first."""
    title = title.replace("ł", "l").replace("Ł", "L")
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-") or "film"


def one_folder():
    """ai-film-lab-v2's one projects/ folder (film/docs/plans/2026-10-07/UNIFY.md),
    when the repo's FILM.bat and that folder exist -- the rule of
    film/ffilm/paths.py `projects_root`. There a flight is projects/<Title>/fly/."""
    if (REPO / "FILM.bat").is_file() and (REPO / "projects").is_dir():
        return REPO / "projects"
    return None


def all_stops():
    one = one_folder()
    return sorted(PROJECTS.glob("*/stops.json")) + (sorted(one.glob("*/fly/stops.json")) if one else [])


def slug_of(project):
    """The film's one name for a flight folder: projects/<Title>/fly -> slug of Title."""
    return slugify(project.parent.name) if project.name == "fly" else project.name


def existing(slug):
    """The flight already made for the film with this slug, or None."""
    return next((s.parent for s in all_stops() if slug_of(s.parent) == slug), None)


def project_for(timeline):
    """The project already made from this timeline, or a new one named after the film.
    The name is the slug ai-film-lab writes (its decision 0014); older timelines
    have none, so the folder name is slugified here as before. A film in the one
    projects/ folder gets its flight beside it, in its own fly/."""
    source = timeline.as_posix()
    for stops in all_stops():
        if f'"source": "{source}"' in stops.read_text(encoding="utf-8"):
            return stops.parent, False
    one = one_folder()
    if one and timeline.parent.name == "out" and timeline.parents[2] == one:
        return timeline.parents[1] / "fly", True
    slug = json.loads(timeline.read_text(encoding="utf-8")).get("slug")
    if not slug:
        title = timeline.parents[1].name if timeline.parent.name == "out" else timeline.stem
        slug = slugify(title)
    return PROJECTS / slug, True


def film_changed(stops, timeline):
    """True when the film was rendered again after this flight was made, None
    when either side has no fingerprint (a flight or film from before 0014)."""
    made, now = stops.get("video_sha256"), timeline.get("video_sha256")
    if not made or not now:
        return None
    return made != now


def warn_if_film_changed(project):
    stops = json.loads((project / "stops.json").read_text(encoding="utf-8"))
    source = Path(stops.get("source", ""))
    if not source.is_file():
        return
    if film_changed(stops, json.loads(source.read_text(encoding="utf-8"))):
        print(f"\nWARNING: the film was rendered again after this flight was made.\n"
              f"  The flight still shows the old cuts. To start again from the new film:\n"
              f"  python library/rigs/film_to_stops.py \"{source}\" \"{project}\" --force\n"
              f"  (--force overwrites your title edits in stops.json)")


def render(blender, project, step):
    print(f"\n--- {step} ({ {'stills': 'about 30 s', 'draft': 'a few minutes', 'video': 'about 10 minutes'}[step] })")
    subprocess.run([blender, "-b", "-P", str(RIGS / "flight.py"), "--",
                    str(project / "stops.json"), f"--{step}"], check=True)
    folder = project / ("out" if step == "video" else "preview")
    if hasattr(os, "startfile"):
        os.startfile(folder)                       # Windows: show what was made
    print(f"\n{step} done -> {folder}")
    if step == "video":
        webbrowser.open(YOUTUBE_UPLOAD)            # drag flight_film.mp4 from the folder into it
        print(f"YouTube upload opened: drag {folder / 'flight_film.mp4'} into it")


def ask(question):
    try:
        return input(question).strip().lower()[:1]
    except EOFError:
        return "q"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    step = next((s for s in ("stills", "draft", "video") if f"--{s}" in sys.argv), None)
    if len(args) != 1:
        sys.exit(__doc__)
    if not shutil.which("ffmpeg"):
        print("Warning: ffmpeg is not on PATH, so --draft/--video cannot add the film "
              "(winget install Gyan.FFmpeg).")

    target = args[0]
    if existing(target):                                          # an existing project by name
        project = existing(target)
    else:
        timeline = find_timeline(target)
        project, new = project_for(timeline)
        if new:
            subprocess.run([sys.executable, str(RIGS / "film_to_stops.py"),
                            str(timeline), str(project)], check=True)
            print(f"\nNew project: {project}\nTitles come from the picture file names; "
                  f"fix them in stops.json and run the stills again.")
        else:
            print(f"Project already made from this film: {project}")
    warn_if_film_changed(project)

    blender = find_blender()
    step = step or "stills"
    while True:
        render(blender, project, step)
        if step == "video":
            return
        nxt = ask("\nNext?  [d] draft   [v] full video   [s] stills again   [q] quit : ")
        step = {"d": "draft", "v": "video", "s": "stills"}.get(nxt)
        if not step:
            print(f"\nLater:  FLY.bat {slug_of(project)} --draft   (or --video)")
            return


if __name__ == "__main__":
    main()

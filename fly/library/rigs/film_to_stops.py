"""
film_to_stops.py - turn an ai-film-lab render into a stops.json for flight.py.

Reads the <video>.timeline.json that `film final` writes beside the video
and writes one stops.json: the hub (the title and everything said to the
camera -- intro, closing), one node per picture, and the visits -- which
node plays which frames of the film. flight.py flies into each node as its
part of the film plays there, full screen, with the film's own sound.

Standard library only. Run it with any Python 3.9+:
  python library/rigs/film_to_stops.py "<film>/out/final.timeline.json" projects/<slug>

Then edit the titles in stops.json if you like, and render:
  blender -b -P library/rigs/flight.py -- projects/<slug>/stops.json --stills
"""

import json
import sys
from pathlib import Path

# Talking belongs on the hub: the title card, the intro, the closing, and
# any camera take between pictures. Every other shot is a card of its own.
HUB_ROLES = {"title", "intro", "closing"}


def to_stops(timeline: dict, timeline_path: Path) -> dict:
    stops, card_of_src, visits = [{"title": timeline["title"], "hub": True}], {}, []

    for s in timeline["shots"]:
        if s["role"] in HUB_ROLES or s["kind"] == "video":
            card = 0
        else:
            if s["src"] not in card_of_src:
                card_of_src[s["src"]] = len(stops)
                stops.append({"title": s["title"]})
            card = card_of_src[s["src"]]
        if visits and visits[-1]["stop"] == card:
            visits[-1]["end_frame"] = s["end_frame"]
        else:
            visits.append({"stop": card, "start_frame": s["start_frame"],
                           "end_frame": s["end_frame"]})

    return {
        "title": timeline["title"],
        # Which render this flight was made from (ai-film-lab decision 0014):
        # fly.py compares it with the timeline to see a re-rendered film.
        "slug": timeline.get("slug"),
        "video_sha256": timeline.get("video_sha256"),
        "source": timeline_path.resolve().as_posix(),
        "film": (timeline_path.parent / timeline["video"]).resolve().as_posix(),
        "fps": timeline["fps"],
        "resolution": [timeline["width"], timeline["height"]],
        "frames": timeline["frames"],
        "stops": stops,
        "visits": visits,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    timeline_path, project = Path(args[0]), Path(args[1])
    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
    if timeline.get("version") != 1:
        sys.exit(f"{timeline_path.name}: timeline version {timeline.get('version')!r}, "
                 f"this script reads version 1.")

    out = project / "stops.json"
    if out.exists() and "--force" not in sys.argv:
        sys.exit(f"{out} already exists and may hold your edits. "
                 f"Add --force to write it again.")
    project.mkdir(parents=True, exist_ok=True)
    spec = to_stops(timeline, timeline_path)
    out.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")

    fps = spec["fps"]
    print(f"{out}: {len(spec['stops'])} cards, {len(spec['visits'])} visits, "
          f"{spec['frames'] / fps:.1f}s at {fps} fps")
    for v in spec["visits"]:
        print(f"  {v['start_frame'] / fps:7.2f}s  {spec['stops'][v['stop']]['title']}")


if __name__ == "__main__":
    main()

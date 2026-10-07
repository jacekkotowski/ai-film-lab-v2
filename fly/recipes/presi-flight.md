# Recipe: presi-flight

Prezi-like camera flight through an idea map. A hub sits in the middle with branches around it, the camera glides to each stop and holds, and it ends on an overview.

**Script:** `library/rigs/flight.py`
**Input:** `projects/<slug>/stops.json`

```json
{ "stops": [
  {"title": "Hub title", "body": "one line"},
  {"title": "Branch 1", "body": "one line"}
]}
```
The first stop is the hub; the rest are branches (4–6 works best).

**Run**
```
blender -b -P library/rigs/flight.py -- projects/<slug>/stops.json --stills   # 7 PNGs, ~30 s
blender -b -P library/rigs/flight.py -- projects/<slug>/stops.json --draft    # low-res MP4
blender -b -P library/rigs/flight.py -- projects/<slug>/stops.json --video    # final MP4
```
Add `--frames=113,383` to render just those frames (check a glide). Add `--blend` to also save `flight.blend` so you can open and tweak it by hand.

**Tuning (constants at the top of flight.py):** HOLD_S, GLIDE_S (timing) · GLIDE_PULLBACK (zoom-out between stops) · RING_X, RING_Z (spread) · DEPTH_STEP (parallax) · CAM_DIST (how close) · PALETTE · CORNER (roundness) · GLOW, GLOW_STRENGTH (the coloured halo) · BACKDROP_Y, DOT_SPACING, DOT_RADIUS, DOT_RGB (the dot grid behind the map).

**Look:** every card has round corners, a thin frame and a soft halo in its colour. The halo is added light, so it needs no lamps. A grid of faint dots far behind the map gives parallax while flying. Links run from card edge to card edge, 0.3 behind, so they never cross a card.

**Timing:** 6 stops × (3 s hold + 1.5 s glide) + 3 s overview ≈ 30 s.

**Picture cards:** give a stop `"image": "path/to/picture.png"` and it becomes the picture in a thin coloured frame, sized from the picture's own shape. Branches get their title above the picture. The hub picture is assumed to carry its own title.

**From a film:** `library/rigs/film_to_stops.py` turns ai-film-lab's `final.timeline.json` into a stops.json with `film` (the mp4), `fps`, `resolution` and a `visits` list: `{"stop": 0, "start_frame": 0, "end_frame": 646}`, frames counted from 0 and end-exclusive. The hub gets the title, intro and closing, and there is one stop per picture.
- Every stop is a **screen** in the film's shape, playing its own part of the film. Before that part it shows the part's first frame, and afterwards its last.
- The flight opens on the overview and dives into the hub. At each cut it glides out and into the next screen, half the glide before the cut and half after. It holds each screen **exactly full-screen and still** while that part plays, and the closing flies back to the hub and plays **to the film's last frame**. Only then does it pull back to the map, over `OVERVIEW_S` of silence, so no last word is ever cut.
- `--draft`/`--video` render **only the frames the film won't cover**: the glides, the opening and the closing pull-back, about a tenth of the film. ffmpeg then lays the film's own frames over every full-screen stretch and adds its sound, padded with silence and never cut, writing `flight_film.mp4` (or `flight_draft_film.mp4`).
- The screens' round corners square off in the last `SQUARE_S` before a screen fills the frame, so the hand-over to the film's square frames doesn't jump.
- A stop visited twice (the hub) gets one screen per visit. The new one appears as the camera sets off towards it.
- Stills are `opening`, `v<visit>_stop_<stop>` (full-screen), `v<visit>_glide` (the cut) and `overview`.

Measured in Blender 5.2, and the reason for two details in `film_mat`:
- Every screen loads the film as its own image, because Eevee keeps one texture per image.
- An image user shows one frame too early before its start, which the `+1`s correct.

**Later:** burned-in captions for the glides (the film's own captions are already in its frames).

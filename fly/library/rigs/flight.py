"""
flight.py - Prezi-like 3D camera flight through an idea map.

Reads a stops.json, builds one text card per stop (hub in the middle,
branches around it), links them, and animates a camera that glides
from stop to stop, holds, and ends on an overview.

Run (from the studio folder):
  blender -b -P library/rigs/flight.py -- projects/<idea>/stops.json --stills
  blender -b -P library/rigs/flight.py -- projects/<idea>/stops.json --video

--stills : one PNG per stop + overview, 50% resolution  -> <project>/preview/
--draft  : quick low-res MP4 (25%, 1 sample) to check motion -> <project>/preview/
--video  : full MP4 at 100% resolution                    -> <project>/out/
--frames=113,383 : render only these frames as stills (check a glide)
--blend  : also save the .blend next to stops.json (open it in Blender to tweak)

A stop with "image" becomes a picture card.

A stops.json with "film" and "visits" (written by film_to_stops.py from an
ai-film-lab render) is a film map: every stop is a screen of the film's
shape playing its own part of the film. The camera flies into each screen
as its part starts, holds it exactly full screen while it plays, and flies
on at the cut; fps and resolution come from the file. --draft/--video then
write <name>_film.mp4: the film's own frames wherever a screen is full,
the flight in between, the film's own sound throughout (needs ffmpeg).
"""

import json
import math
import os
import shutil
import struct
import subprocess
import sys
import zlib
from pathlib import Path

import bpy
from mathutils import Vector

# ---------------------------------------------------------------- settings
FPS = 30
HOLD_S = 3.0            # seconds the camera rests on a stop
GLIDE_S = 2.0           # seconds of flight between stops
OVERVIEW_S = 3.0        # final pull-back
RES_X, RES_Y = 1080, 1920   # vertical short
PREVIEW_PCT = 50
CARD_W, CARD_H = 4.0, 2.6
RING_X, RING_Z = 5.6, 9.5   # ellipse: narrow + tall for vertical video
DEPTH_STEP = 2.5        # branches alternate in depth -> parallax
CAM_DIST = 8.5          # camera distance in front of a card
GLIDE_PULLBACK = 7.0    # how far the camera backs off mid-glide
IMG_LONG = 4.4          # a picture card's or screen's longer side (hub x 1.35)
CORNER = 0.05           # corner radius, as a share of a card's shorter side
SQUARE_S = 0.4          # a screen's corners square off over this long before it fills the frame
DIM = 0.25              # film map: a node not yet visited glows at this share of its light
SHORTS_S = 179          # film map: a film this short stays a Short, 1 s under 3 min: YouTube reads exactly 3:00 as 3:01 (the pull-back shrinks to fit)
GLOW = 0.9              # how far a card's coloured glow reaches beyond it
GLOW_STRENGTH = 0.35
BACKDROP_Y = 14.0       # the dot grid far behind the map: parallax while flying
DOT_SPACING = 1.5
DOT_RADIUS = 0.07
DOT_RGB = (0.012, 0.015, 0.026)
BG = (0.003, 0.004, 0.008)
PALETTE = [(0.36, 0.55, 1.0), (0.98, 0.55, 0.25), (0.35, 0.85, 0.6),
           (0.85, 0.4, 0.9), (0.95, 0.8, 0.3), (0.4, 0.85, 0.95)]


# ---------------------------------------------------------------- args
def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    stops_path = next((a for a in argv if a.endswith(".json")), None)
    if not stops_path:
        sys.exit("usage: blender -b -P flight.py -- path/to/stops.json [--stills|--video] [--blend]")
    mode = "video" if "--video" in argv else "draft" if "--draft" in argv else "stills"
    frames = next((a.split("=", 1)[1] for a in argv if a.startswith("--frames=")), "")
    frames = [int(f) for f in frames.split(",") if f]
    return Path(stops_path).resolve(), mode, ("--blend" in argv), frames


# ---------------------------------------------------------------- helpers
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    world = bpy.data.worlds.new("World")
    world.node_tree.nodes["Background"].inputs[0].default_value = (*BG, 1)
    scene.world = world
    return scene


def emission_mat(name, rgb, strength=1.0):
    mat = bpy.data.materials.new(name)
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    em = nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*rgb, 1)
    em.inputs["Strength"].default_value = strength
    mat.node_tree.links.new(em.outputs[0], out.inputs[0])
    return mat


def add_text(body, size, loc, width, mat, name, bold=False):
    curve = bpy.data.curves.new(name, "FONT")
    curve.body = body
    curve.size = size
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.text_boxes[0].width = width
    curve.text_boxes[0].x = -width / 2
    curve.extrude = 0.01
    if bold:
        curve.offset = 0.004
    obj = bpy.data.objects.new(name, curve)
    obj.location = loc
    obj.data.materials.append(mat)
    bpy.context.collection.objects.link(obj)
    return obj


def add_card(stop, idx, loc, color, is_hub):
    """One stop = dark backing plane + coloured title + grey body. Parented to an empty."""
    scale = 1.35 if is_hub else 1.0
    root = bpy.data.objects.new(f"stop_{idx:02d}", None)
    root.location = loc
    bpy.context.collection.objects.link(root)

    w, h = CARD_W * scale, CARD_H * scale
    add_plane(f"stop_{idx:02d}_card", (w, h), 0.0,
              emission_mat(f"card_{idx}", (0.018, 0.021, 0.032), 1.0), root)
    add_glow(root, idx, color, w, h)

    white = emission_mat(f"txt_{idx}", color, 1.6)
    grey = emission_mat(f"sub_{idx}", (0.7, 0.72, 0.78), 1.0)
    t = add_text(stop["title"], 0.42 * scale, (0, -0.02, 0.45 * scale),
                 CARD_W * scale * 0.9, white, f"stop_{idx:02d}_title", bold=True)
    t.rotation_euler = (math.radians(90), 0, 0)
    t.parent = root
    if stop.get("body"):
        b = add_text(stop["body"], 0.22 * scale, (0, -0.02, -0.45 * scale),
                     CARD_W * scale * 0.85, grey, f"stop_{idx:02d}_body")
        b.rotation_euler = (math.radians(90), 0, 0)
        b.parent = root
    return root, (w, h)


def image_mat(name, path):
    """Emission straight from the picture: shows its own colours, needs no light."""
    if not Path(path).exists():
        sys.exit(f"stops.json: picture not found: {path}")
    mat = bpy.data.materials.new(name)
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    em = nodes.new("ShaderNodeEmission")
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(str(path), check_existing=True)
    mat.node_tree.links.new(tex.outputs["Color"], em.inputs["Color"])
    mat.node_tree.links.new(em.outputs[0], out.inputs[0])
    return mat, tuple(tex.image.size)


def add_image_card(stop, idx, loc, color, is_hub):
    """One stop = the picture, a thin coloured frame behind it, and (branches
    only -- the hub picture carries its own title) the title above.
    Returns the root and the width/height the camera must fit."""
    scale = 1.35 if is_hub else 1.0
    root = bpy.data.objects.new(f"stop_{idx:02d}", None)
    root.location = loc
    bpy.context.collection.objects.link(root)

    mat, (pw, ph) = image_mat(f"pic_{idx}", stop["image"])
    w, h = card_size(pw / ph if ph else 1.0, scale)
    add_plane(f"stop_{idx:02d}_picture", (w, h), 0.0, mat, root)
    add_frame_and_title(stop, idx, root, color, is_hub, w, h)
    return root, (w, h)


def card_size(aspect, scale):
    long_side = IMG_LONG * scale
    return (long_side, long_side / aspect) if aspect >= 1 else (long_side * aspect, long_side)


def corner(w, h):
    return CORNER * min(w, h)


def rounded_mesh(name, w, h, r, segments=8):
    """A w x h rectangle with round corners of radius r: one face, UVs over
    its box. Also returns where each vertex sits on the square rectangle,
    for a 'square' shape key."""
    r = min(r, w / 2 - 1e-4, h / 2 - 1e-4)
    if r <= 0:
        r, segments = 0.0, 0
    verts, square = [], []
    for sx, sy, start in ((1, 1, 0), (-1, 1, 90), (-1, -1, 180), (1, -1, 270)):
        for i in range(segments + 1):
            t = math.radians(start + (90 * i / segments if segments else 45))
            verts.append((sx * (w / 2 - r) + r * math.cos(t), sy * (h / 2 - r) + r * math.sin(t), 0))
            square.append((sx * w / 2, sy * h / 2, 0))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], [list(range(len(verts)))])
    uv = mesh.uv_layers.new(name="UVMap")
    for loop in mesh.loops:
        x, y, _ = verts[loop.vertex_index]
        uv.data[loop.index].uv = (x / w + 0.5, y / h + 0.5)
    return mesh, square


def add_plane(name, size, y, mat, parent, radius=None, squarable=False):
    """A round-cornered card standing upright, facing the camera (-y).
    `squarable` adds a 'square' shape key that straightens its corners."""
    w, h = size
    mesh, square = rounded_mesh(name, w, h, corner(w, h) if radius is None else radius)
    mesh.materials.append(mat)
    plane = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(plane)
    plane.location = (0, y, 0)
    plane.rotation_euler = (math.radians(90), 0, 0)
    plane.parent = parent
    if squarable:
        plane.shape_key_add(name="Basis")
        key = plane.shape_key_add(name="square", from_mix=False)
        for i, co in enumerate(square):
            key.data[i].co = co
    return plane


def glow_mat(name, rgb, size, inner, r):
    """Light in the card's colour, fading out over GLOW beyond its rounded
    edge. Added on top of what is behind it, so it needs no light and casts
    nothing -- a halo, not a shadow, which would not show on this background."""
    (W, H), (w, h) = size, inner
    mat = bpy.data.materials.new(name)
    mat.surface_render_method = "BLENDED"
    nt = mat.node_tree
    nt.nodes.clear()
    new, link = nt.nodes.new, nt.links.new

    def vmath(op, a, b):
        n = new("ShaderNodeVectorMath")
        n.operation = op
        link(a, n.inputs[0])
        n.inputs[1].default_value = b
        return n

    uv = new("ShaderNodeTexCoord").outputs["UV"]
    p = vmath("MULTIPLY", vmath("SUBTRACT", uv, (0.5, 0.5, 0)).outputs[0], (W, H, 0))
    q = vmath("SUBTRACT", vmath("ABSOLUTE", p.outputs[0], (0, 0, 0)).outputs[0],
              (w / 2 - r, h / 2 - r, 0))
    dist = new("ShaderNodeVectorMath")
    dist.operation = "LENGTH"
    link(vmath("MAXIMUM", q.outputs[0], (0, 0, 0)).outputs[0], dist.inputs[0])
    fade = new("ShaderNodeMapRange")                  # distance past the edge -> 1..0
    link(dist.outputs["Value"], fade.inputs["Value"])
    fade.inputs["From Min"].default_value, fade.inputs["From Max"].default_value = r, r + GLOW
    fade.inputs["To Min"].default_value, fade.inputs["To Max"].default_value = 1.0, 0.0
    soft = new("ShaderNodeMath")
    soft.operation = "POWER"
    link(fade.outputs["Result"], soft.inputs[0])
    soft.inputs[1].default_value = 2.5
    strength = new("ShaderNodeMath")
    strength.operation = "MULTIPLY"
    link(soft.outputs[0], strength.inputs[0])
    strength.inputs[1].default_value = GLOW_STRENGTH
    em = new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*rgb, 1)
    link(strength.outputs[0], em.inputs["Strength"])
    add = new("ShaderNodeAddShader")
    link(new("ShaderNodeBsdfTransparent").outputs[0], add.inputs[0])
    link(em.outputs[0], add.inputs[1])
    link(add.outputs[0], new("ShaderNodeOutputMaterial").inputs[0])
    return mat, strength.inputs[1]


def add_glow(root, idx, color, w, h):
    r = corner(w, h)
    size = (w + 2 * GLOW, h + 2 * GLOW)
    mat, strength = glow_mat(f"glow_{idx}", color, size, (w, h), r)
    add_plane(f"stop_{idx:02d}_glow", size, 0.12, mat, root, radius=r + GLOW)
    return strength


def add_backdrop():
    """A faint grid of soft dots far behind the map. It moves slower than the
    cards when the camera flies, which is what makes the flight read as 3D."""
    size = 120.0
    mat = bpy.data.materials.new("backdrop")
    nt = mat.node_tree
    nt.nodes.clear()
    new, link = nt.nodes.new, nt.links.new
    cells = size / DOT_SPACING
    steps = [("MULTIPLY", (cells, cells, 1)), ("FRACTION", None), ("SUBTRACT", (0.5, 0.5, 0))]
    sock = new("ShaderNodeTexCoord").outputs["UV"]
    for op, b in steps:
        n = new("ShaderNodeVectorMath")
        n.operation = op
        link(sock, n.inputs[0])
        if b:
            n.inputs[1].default_value = b
        sock = n.outputs[0]
    dist = new("ShaderNodeVectorMath")
    dist.operation = "LENGTH"
    link(sock, dist.inputs[0])
    dot = new("ShaderNodeMapRange")
    link(dist.outputs["Value"], dot.inputs["Value"])
    dot.inputs["From Min"].default_value = DOT_RADIUS / DOT_SPACING * 0.4
    dot.inputs["From Max"].default_value = DOT_RADIUS / DOT_SPACING
    dot.inputs["To Min"].default_value, dot.inputs["To Max"].default_value = 1.0, 0.0
    bg = new("ShaderNodeEmission")
    bg.inputs["Color"].default_value = (*BG, 1)
    lit = new("ShaderNodeEmission")
    lit.inputs["Color"].default_value = (*DOT_RGB, 1)
    link(dot.outputs["Result"], lit.inputs["Strength"])
    add = new("ShaderNodeAddShader")
    link(bg.outputs[0], add.inputs[0])
    link(lit.outputs[0], add.inputs[1])
    link(add.outputs[0], new("ShaderNodeOutputMaterial").inputs[0])
    add_plane("backdrop", (size, size), BACKDROP_Y, mat, None, radius=0.0)


def add_frame_and_title(stop, idx, root, color, is_hub, w, h):
    """A thin coloured frame behind the card, its glow, and on branches the
    title above. The hub's picture carries its own title. Returns the
    strength sockets of all three, for light_up."""
    frame = emission_mat(f"frame_{idx}", color, 1.2)
    add_plane(f"stop_{idx:02d}_frame", (w + 0.14, h + 0.14), 0.05,
              frame, root, radius=corner(w, h) + 0.07)
    sockets = [strength(frame), add_glow(root, idx, color, w, h)]
    if is_hub:
        return sockets
    title = emission_mat(f"txt_{idx}", color, 1.6)
    t = add_text(stop["title"], 0.3, (0, -0.02, h / 2 + 0.45), w * 0.95,
                 title, f"stop_{idx:02d}_title", bold=True)
    t.rotation_euler = (math.radians(90), 0, 0)
    t.parent = root
    return sockets + [strength(title)]


def strength(mat):
    return mat.node_tree.nodes["Emission"].inputs["Strength"]


def film_mat(name, film, a, b):
    """The film's frames [a, b), 0-based. Before a it holds frame a, after b
    frame b-1. Measured in Blender 5.2: below its start an image user clamps
    to one frame early, hence the +1s. Each screen loads the film as its own
    image: Eevee keeps one texture per image, so screens sharing one would
    all show whichever frame was asked for last."""
    mat = bpy.data.materials.new(name)
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    em = nodes.new("ShaderNodeEmission")
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(film, check_existing=False)
    iu = tex.image_user
    iu.frame_duration, iu.frame_start, iu.frame_offset = max(1, b - a - 1), a + 2, a + 1
    iu.use_auto_refresh, iu.use_cyclic = True, False
    mat.node_tree.links.new(tex.outputs["Color"], em.inputs["Color"])
    mat.node_tree.links.new(em.outputs[0], out.inputs[0])
    return mat


def add_film_node(stop, idx, loc, color, is_hub, film, spans, res):
    """A stop as a screen of the film's own shape: one screen per visit, all
    in the same place, each playing its visit's frames (`spans`). Returns
    the root, the size the camera fits, the screens in visit order and the
    strength sockets that light_up dims (screens, frame, glow, title)."""
    root = bpy.data.objects.new(f"stop_{idx:02d}", None)
    root.location = loc
    bpy.context.collection.objects.link(root)
    w, h = card_size(res[0] / res[1], 1.35 if is_hub else 1.0)
    screens = [add_plane(f"stop_{idx:02d}_screen_{j}", (w, h), 0.0,
                         film_mat(f"film_{idx}_{j}", film, a, b), root, squarable=True)
               for j, (a, b) in enumerate(spans)]
    sockets = [strength(s.data.materials[0]) for s in screens]
    sockets += add_frame_and_title(stop, idx, root, color, is_hub, w, h)
    return root, (w, h), screens, sockets


def edge_point(center, size, toward):
    """Where the line from `center` to `toward` leaves a w x h card (seen face on)."""
    d = Vector((toward.x - center.x, 0, toward.z - center.z))
    half_w, half_h = size[0] / 2 + 0.1, size[1] / 2 + 0.1       # just outside the frame
    t = min(half_w / abs(d.x) if d.x else math.inf, half_h / abs(d.z) if d.z else math.inf)
    return center + d * min(t, 1.0)


def add_link(a, b, a_size, b_size, color, idx):
    """Thin glowing curve from the hub's edge to the branch's edge, 0.3 behind
    both. Edge to edge, it never crosses in front of a card -- not even when
    the camera is so close that a card fills the frame."""
    curve = bpy.data.curves.new(f"link_{idx}", "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.025
    curve.bevel_factor_mapping_end = "SPLINE"      # light_up draws it out evenly along its length
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(1)
    p0, p1 = spline.bezier_points
    back = Vector((0, 0.3, 0))
    a, b = edge_point(a, a_size, b) + back, edge_point(b, b_size, a) + back
    p0.co, p1.co = a, b
    mid = (a + b) / 2 + Vector((0, 1.5, 0))
    p0.handle_left = p0.handle_right = a.lerp(mid, 0.6)
    p1.handle_left = p1.handle_right = b.lerp(mid, 0.6)
    obj = bpy.data.objects.new(f"link_{idx}", curve)
    obj.data.materials.append(emission_mat(f"link_{idx}", color, 1.5))
    bpy.context.collection.objects.link(obj)
    return curve


def layout(n_branches):
    """Hub at origin; branches on a ring, alternating depth (y)."""
    pts = [Vector((0, 0, 0))]
    for i in range(n_branches):
        ang = math.pi / 2 - 2 * math.pi * i / n_branches   # start at top, clockwise
        depth = DEPTH_STEP if i % 2 else -DEPTH_STEP
        pts.append(Vector((RING_X * math.cos(ang), depth, RING_Z * math.sin(ang))))
    return pts


def make_camera(scene):
    """Camera tracking an empty. Returns key(frame, cam_loc, target_loc)."""
    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = 35
    cam = bpy.data.objects.new("Camera", cam_data)
    bpy.context.collection.objects.link(cam)
    scene.camera = cam

    target = bpy.data.objects.new("CamTarget", None)
    bpy.context.collection.objects.link(target)
    track = cam.constraints.new("TRACK_TO")
    track.target = target
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"

    def key(f, cam_loc, tgt_loc):
        cam.location, target.location = cam_loc, tgt_loc
        cam.keyframe_insert("location", frame=f)
        target.keyframe_insert("location", frame=f)
    return key


def fit_dist(w, h, res, lens=35, sensor=36):
    """How far back the camera stands so a w x h card exactly fills the frame.
    Blender's default sensor fit puts the sensor on the frame's longer side."""
    aspect = res[0] / res[1]
    half = sensor / 2 / lens
    tan_x, tan_z = (half, half / aspect) if aspect >= 1 else (half * aspect, half)
    return max(w / 2 / tan_x, h / 2 / tan_z)


def schedule(visits, fps):
    """(arrive, leave) per visit: the Blender frames (1-based; film frame f is
    Blender frame f+1) between which the camera holds that screen full.
    The glide across each cut is half before it, half after. The flight
    opens on the overview, diving in while the title card plays; the last
    visit holds to the film's very last frame, so no closing word is ever
    said to a shrinking screen."""
    n = len(visits)
    length = [v["end_frame"] - v["start_frame"] for v in visits]
    glide = [min(int(GLIDE_S * fps), length[k] // 2, length[k + 1] // 2) for k in range(n - 1)]
    opening = min(int(OVERVIEW_S * fps), length[0] // 2)
    spans = []
    for k, v in enumerate(visits):
        arrive = 1 + v["start_frame"] + (glide[k - 1] - glide[k - 1] // 2 if k else opening)
        leave = v["end_frame"] - (glide[k] // 2 if k < n - 1 else 0)
        spans.append((arrive, leave))
    return spans, glide


def build_film_camera(scene, locs, sizes, visits, fps, res, overview_loc):
    """Straight on, exactly full screen, perfectly still while a screen plays
    -- so the film's own frames can be laid over those stretches unseen.
    After the film's last frame, OVERVIEW_S more: the pull-back to the map."""
    key = make_camera(scene)
    spans, glide = schedule(visits, fps)
    origin = Vector((0, 0, 0))

    def cam_at(stop):
        return locs[stop] + Vector((0, -fit_dist(*sizes[stop], res), 0))

    end = visits[-1]["end_frame"]
    marks = []
    if spans[0][0] > 1:
        key(1, overview_loc, origin)
        marks.append(("opening", 1))
    for k, (v, (arrive, leave)) in enumerate(zip(visits, spans)):
        stop = v["stop"]
        key(arrive, cam_at(stop), locs[stop])
        key(leave, cam_at(stop), locs[stop])
        marks.append((f"v{k:02d}_stop_{stop:02d}", (arrive + leave) // 2))
        if k < len(visits) - 1 and glide[k] >= 4:                      # zoom-out mid-glide
            nxt = visits[k + 1]["stop"]
            mid = (cam_at(stop) + cam_at(nxt)) / 2 + Vector((0, -GLIDE_PULLBACK, 0))
            key(1 + v["end_frame"], mid, (locs[stop] + locs[nxt]) / 2)
            marks.append((f"v{k:02d}_glide", 1 + v["end_frame"]))
    end += pullback_frames(end, fps)
    key(end, overview_loc, origin)
    marks.append(("overview", end))
    return end, marks, spans


def pullback_frames(film_frames, fps):
    """OVERVIEW_S, unless that would push a Short past SHORTS_S: then only
    what still fits, down to a single frame, so a Short stays a Short."""
    want, room = int(OVERVIEW_S * fps), SHORTS_S * fps - film_frames
    if film_frames > SHORTS_S * fps:
        print(f"Not a Short: film {film_frames / fps:.1f}s is over {SHORTS_S}s, "
              f"so this uploads as a regular video")
        return want
    if want <= room:
        return want
    got = max(1, room)
    print(f"Shorts guard: pull-back {got / fps:.2f}s instead of {OVERVIEW_S}s "
          f"(film {film_frames / fps:.1f}s, limit {SHORTS_S}s)")
    return got


def light_up(nodes, links, visits, spans):
    """The map lights up as the story goes. A node not yet visited is a
    ghost at DIM; on the glide to its first visit, the link from the hub
    draws out over the first half and the node brightens over the second,
    fully lit by `arrive` -- from there on the film's own frames take over,
    so a node still brightening would jump. The hub is lit from the start."""
    seen = {visits[0]["stop"]}
    for k in range(1, len(visits)):
        stop = visits[k]["stop"]
        if stop in seen:
            continue
        seen.add(stop)
        start, arrive = spans[k - 1][1], spans[k][0]
        mid = (start + arrive) // 2
        curve = links.get(stop)
        if curve:
            for f, v in ((start, 0.0), (mid, 1.0)):
                curve.bevel_factor_end = v
                curve.keyframe_insert("bevel_factor_end", frame=f)
        for sock in nodes[stop]:
            full = sock.default_value
            for f, v in ((mid, full * DIM), (arrive, full)):
                sock.default_value = v
                sock.keyframe_insert("default_value", frame=f)
            sock.default_value = full


def square_corners(screens, spans, fps):
    """Each screen straightens its round corners just before it fills the
    frame, and rounds them again as the camera leaves: the hand-over to the
    film's own square frames then shows no jump."""
    n = max(1, int(SQUARE_S * fps))
    for screen, (arrive, leave) in zip(screens, spans):
        key = screen.data.shape_keys.key_blocks["square"]
        for f, v in ((arrive - n, 0.0), (arrive, 1.0), (leave, 1.0), (leave + n, 0.0)):
            if f >= 1:
                key.value = v
                key.keyframe_insert("value", frame=f)


def swap_screens(screens, visits, spans):
    """A stop visited again shows its new part of the film from the moment
    the camera sets off towards it; until then, its earlier part."""
    last, windows = {}, {}
    for k, v in enumerate(visits):
        on = spans[k - 1][1] if v["stop"] in last else 1
        if v["stop"] in last:
            windows[last[v["stop"]]][1] = on
        windows[k] = [on, None]
        last[v["stop"]] = k
    for k, (on, off) in windows.items():
        if on == 1 and off is None:
            continue
        keys = [(1, on > 1)] + ([(on, False)] if on > 1 else []) + ([(off, True)] if off else [])
        for f, hidden in keys:
            screens[k].hide_render = screens[k].hide_viewport = hidden
            screens[k].keyframe_insert("hide_render", frame=f)
            screens[k].keyframe_insert("hide_viewport", frame=f)


def build_camera(scene, stops_locs, overview_loc):
    key = make_camera(scene)
    hold, glide = int(HOLD_S * FPS), int(GLIDE_S * FPS)
    frame, marks = 1, []

    def cam_at(i, loc):
        dist = CAM_DIST * (1.5 if i == 0 else 1.0)                   # hub card is bigger
        return loc + Vector((0.6 if i % 2 else -0.6, -dist, 0.4))     # slight angle = depth

    for i, loc in enumerate(stops_locs):
        cam_loc = cam_at(i, loc)
        drift = Vector((-0.3 if i % 2 else 0.3, 0.6, 0))              # slow push during hold
        key(frame, cam_loc, loc)
        key(frame + hold, cam_loc + drift, loc)
        marks.append((f"stop_{i:02d}", frame + hold // 2))
        if i + 1 < len(stops_locs):                                    # zoom-out mid-glide (Prezi feel)
            nxt = stops_locs[i + 1]
            mid_cam = (cam_loc + drift + cam_at(i + 1, nxt)) / 2 + Vector((0, -GLIDE_PULLBACK, 0))
            key(frame + hold + glide // 2, mid_cam, (loc + nxt) / 2)
        frame += hold + glide

    key(frame, overview_loc, Vector((0, 0, 0)))
    end = frame + int(OVERVIEW_S * FPS)
    key(end, overview_loc + Vector((0, 2.0, 0)), Vector((0, 0, 0)))
    marks.append(("overview", end - FPS))
    return end, marks


def setup_render(scene, end, mode, out_dir, fps=FPS, res=(RES_X, RES_Y), as_frames=False):
    video = mode != "stills" and not as_frames
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = {"video": 100, "draft": 25}.get(mode, PREVIEW_PCT)
    scene.render.fps = fps
    scene.frame_start, scene.frame_end = 1, end
    try:
        scene.eevee.taa_render_samples = {"video": 16, "draft": 1}.get(mode, 4)
        scene.eevee.use_bloom = True
    except AttributeError:
        pass
    scene.view_settings.view_transform = "Standard"
    if video:
        if hasattr(scene.render.image_settings, "media_type"):   # Blender 5.0+
            scene.render.image_settings.media_type = "VIDEO"
        scene.render.image_settings.file_format = "FFMPEG"
        scene.render.ffmpeg.format = "MPEG4"
        scene.render.ffmpeg.codec = "H264"
        scene.render.filepath = str(out_dir / ("flight.mp4" if mode == "video" else "flight_draft.mp4"))
    else:
        if hasattr(scene.render.image_settings, "media_type"):
            scene.render.image_settings.media_type = "IMAGE"
        scene.render.image_settings.file_format = "PNG"
        scene.render.image_settings.color_mode = "RGB"      # the same kind of PNG as blank_png
        scene.render.image_settings.color_depth = "8"


def blank_png(path, w, h):
    """A black RGB PNG, standard library only: stands in for a frame the film covers."""
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))
    raw = (b"\x00" + b"\x00" * (w * 3)) * h
    path.write_bytes(b"\x89PNG\r\n\x1a\n"
                     + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def render_flight_frames(scene, end, spans, frames_dir, size):
    """Only the frames the film will not cover: the glides, the opening and
    the closing. Every full-screen frame is a link to one black PNG --
    typically nine tenths of the film, never rendered."""
    shutil.rmtree(frames_dir, ignore_errors=True)
    frames_dir.mkdir(parents=True)
    covered = {f for a, b in spans for f in range(a, b + 1)}
    blank = frames_dir / "blank.png"
    blank_png(blank, *size)
    todo = end - len(covered & set(range(1, end + 1)))
    done = 0
    for f in range(1, end + 1):
        path = frames_dir / f"{f - 1:05d}.png"
        if f in covered:
            try:
                os.link(blank, path)
            except OSError:
                shutil.copyfile(blank, path)
            continue
        scene.frame_set(f)
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        done += 1
        if done % 50 == 0 or done == todo:
            print(f"  rendered {done}/{todo} flight frames")


def compose(frames_dir, film, spans, size, fps, out):
    """The film's own frames wherever a screen is full, the flight in between,
    the film's own sound throughout, starting on the same frame. The flight
    runs OVERVIEW_S past the film and the sound is padded with silence to
    meet it: the output ends with the flight, so no last word is ever cut
    (a film's sound often runs a few ms past its last picture)."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        sys.exit(f"ffmpeg not on PATH: the flight frames are in {frames_dir}, not joined to the film")
    full = "+".join(f"between(n,{a - 1},{b - 1})" for a, b in spans if b >= a)
    graph = (f"[1:v]scale={size[0]}:{size[1]},setsar=1[f];"
             f"[0:v][f]overlay=enable='{full}',format=yuv420p[v];[1:a]apad[a]")
    subprocess.run([ffmpeg, "-y", "-v", "error",
                    "-framerate", str(fps), "-start_number", "0", "-i", str(frames_dir / "%05d.png"),
                    "-i", film, "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "256k",
                    "-shortest", str(out)],
                   check=True)
    shutil.rmtree(frames_dir)
    print(f"with the film -> {out}")


# ---------------------------------------------------------------- main
def main():
    stops_path, mode, save_blend, frames = parse_args()
    video = mode != "stills"
    spec = json.loads(stops_path.read_text(encoding="utf-8"))
    stops = spec["stops"]
    project = stops_path.parent

    film = spec.get("film")
    visits = spec.get("visits") or []
    fps = spec.get("fps", FPS)
    res = tuple(spec.get("resolution", (RES_X, RES_Y)))
    if film and not Path(film).exists():
        sys.exit(f"stops.json: film not found: {film}")
    if film and not visits:
        sys.exit("stops.json: a film needs its visits -- write it with film_to_stops.py")

    scene = reset_scene()
    add_backdrop()
    locs = layout(len(stops) - 1)
    sizes, screens, glows, links = [], [None] * len(visits), {}, {}
    for i, (stop, loc) in enumerate(zip(stops, locs)):
        color = PALETTE[(i - 1) % len(PALETTE)] if i else (0.95, 0.95, 0.97)
        if film:
            mine = [k for k, v in enumerate(visits) if v["stop"] == i]
            spans = [(visits[k]["start_frame"], visits[k]["end_frame"]) for k in mine]
            _, size, scr, glows[i] = add_film_node(stop, i, loc, color, i == 0, film, spans, res)
            for k, s in zip(mine, scr):
                screens[k] = s
        elif stop.get("image"):
            _, size = add_image_card(stop, i, loc, color, is_hub=(i == 0))
        else:
            _, size = add_card(stop, i, loc, color, is_hub=(i == 0))
        sizes.append(size)
        if i:
            links[i] = add_link(locs[0], loc, sizes[0], size, color, i)

    overview = Vector((0, -RING_Z * 3.4, 0.5))
    if film:
        end, marks, full = build_film_camera(scene, locs, sizes, visits, fps, res, overview)
        swap_screens(screens, visits, full)
        square_corners(screens, full, fps)
        light_up(glows, links, visits, full)
    else:
        end, marks = build_camera(scene, locs, overview)

    out_dir = project / ("out" if mode == "video" else "preview")
    out_dir.mkdir(exist_ok=True)
    setup_render(scene, end, mode, out_dir, fps, res, as_frames=bool(film))

    if save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=str(project / "flight.blend"))

    if video and film:
        pct = scene.render.resolution_percentage
        size = (res[0] * pct // 100, res[1] * pct // 100)
        name = "flight_film" if mode == "video" else "flight_draft_film"
        render_flight_frames(scene, end, full, out_dir / f"{name}_frames", size)
        compose(out_dir / f"{name}_frames", film, full, size, fps, out_dir / f"{name}.mp4")
    elif video:
        bpy.ops.render.render(animation=True)
        print(f"{mode} -> {scene.render.filepath}  ({end / fps:.1f}s)")
    else:
        if frames:
            marks = [(f"frame_{f:04d}", f) for f in frames]
        for name, f in marks:
            scene.frame_set(f)
            scene.render.filepath = str(out_dir / f"{name}.png")
            bpy.ops.render.render(write_still=True)
        print(f"{len(marks)} stills -> {out_dir}   (video would be {end / fps:.1f}s)")


main()

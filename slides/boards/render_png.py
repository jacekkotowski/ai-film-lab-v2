"""Render every board in <dir>/html to <dir>/png at 2160x1920, plus a contact sheet.

Headless Chrome (or Edge) does the screenshot, so nothing is installed: the
plan's Playwright would have been a new dependency (agreement 11). Offline it
works the same as online as long as models/fonts/ holds the two fonts
(SpaceGrotesk-*.ttf, JetBrainsMono-*.ttf); without them offline Chrome falls
back to Segoe UI / Consolas and the boards look different.

    uv run --directory slides python boards/render_png.py projects/<Film>/boards
    uv run --directory slides python boards/render_png.py projects/<Film>/boards --media projects/<Film>/media

--media copies each PNG into the film's media/ folder (NN_Title.png), where
`film init` finds a 2160x1920 picture and gives it `move: columns`.
The contact sheet (png/contact_sheet.png) is made with ffmpeg.
"""

import glob
import os
import shutil
import struct
import subprocess
import sys
import tempfile

WIDTH, HEIGHT = 2160, 1920

CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_browser():
    env = os.environ.get("CHROME")
    if env and os.path.exists(env):
        return env
    for p in CANDIDATES:
        if os.path.exists(p):
            return p
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    return None


def png_size(path):
    """(width, height) from a PNG header, no imaging library."""
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    return struct.unpack(">II", head[16:24])


def shot(browser, html_path, png_path):
    profile = tempfile.mkdtemp(prefix="boards_chrome_")
    try:
        cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               "--force-device-scale-factor=1", f"--window-size={WIDTH},{HEIGHT}",
               "--virtual-time-budget=4000", f"--user-data-dir={profile}",
               f"--screenshot={png_path}", "file:///" + os.path.abspath(html_path).replace("\\", "/")]
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    if not os.path.exists(png_path):
        raise SystemExit(f"no screenshot made for {html_path}")
    got = png_size(png_path)
    if got != (WIDTH, HEIGHT):
        raise SystemExit(f"{png_path} is {got[0]}x{got[1]}, a board is {WIDTH}x{HEIGHT}")


def contact_sheet(png_dir, names):
    ff = shutil.which("ffmpeg")
    if not ff or not names:
        return None
    lst = os.path.join(png_dir, "_contact.txt")
    with open(lst, "w", encoding="utf-8") as f:
        for n in names:
            f.write(f"file '{n}.png'\nduration 1\n")
    rows = (len(names) + 2) // 3
    out = os.path.join(png_dir, "contact_sheet.png")
    subprocess.run([ff, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-vf", f"scale=540:480,tile=3x{rows}", "-frames:v", "1", out], check=True)
    os.remove(lst)
    return out


def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    root = argv[0]
    media = argv[argv.index("--media") + 1] if "--media" in argv else None
    browser = find_browser()
    if not browser:
        raise SystemExit("no Chrome or Edge found; set CHROME to its path")
    src, out = os.path.join(root, "html"), os.path.join(root, "png")
    os.makedirs(out, exist_ok=True)
    boards = sorted(p for p in glob.glob(os.path.join(src, "*.html"))
                    if os.path.basename(p) != "index.html")
    if not boards:
        raise SystemExit(f"no boards in {src}; run its slides.py first")
    names = []
    for h in boards:
        stem = os.path.splitext(os.path.basename(h))[0]
        shot(browser, h, os.path.join(out, stem + ".png"))
        names.append(stem)
        print(f"png {stem}  {WIDTH}x{HEIGHT}")
        if media:
            os.makedirs(media, exist_ok=True)
            shutil.copy(os.path.join(out, stem + ".png"), os.path.join(media, stem + ".png"))
    sheet = contact_sheet(out, names)
    print("contact sheet", sheet or "(ffmpeg not found)")
    if media:
        print(f"copied {len(names)} to {media}")


if __name__ == "__main__":
    main(sys.argv[1:])

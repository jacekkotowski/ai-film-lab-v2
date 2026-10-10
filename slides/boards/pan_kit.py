"""Two-column boards for phone video, made offline: plain HTML, standard library only.

One board = 2160x1920 = two 1080x1920 columns. Left is step A (the problem,
the first action), right is step B (the fix, the second action). In the film
the camera holds on A, crosses, holds on B (`move: columns`, `cross:`).

Any subject with an A -> B story fits: an Excel formula, a Power Query step,
a piece of R, a before/after. The helpers below are the pieces a column is
made of; `panel` stacks them (tag line, headline, subline, body, footer);
`write_boards` writes one HTML page per board.

Origin: Jacek's Excel Refresher plan (pan_kit.py of 2026-10-10), the same
look, with local fonts (no network), a code block for M/R/VBA, and a width
check so a mono line never wraps.

    import sys; sys.path.insert(0, "slides/boards")
    from pan_kit import *
    set_series("POWER QUERY . 03")
    write_boards("projects/<Film>/boards/html", [
        ("01 Title of the slide",
         panel("SLIDE 1 . A", "Headline", "One subline.", keys("Ctrl", "T")),
         panel("SLIDE 1 . B", "Headline", "One subline.", fbar("=SUM(tbl[x])"))),
    ])
"""

import html
import os
import re

e = html.escape

HERE = os.path.dirname(os.path.abspath(__file__))
# Fonts are a download, so they live in the repo's models/ (never in git).
FONT_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "models", "fonts"))

BG = "#0E1416"; TX = "#F2F4F1"; MU = "#A3AFAB"; LN = "#2A3633"
GR = "#1B7F47"; GRT = "#5BD394"; AM = "#F5B83D"; OR = "#FF8F57"
SH = "#FFFFFF"; GL = "#D5DAD6"; HB = "#EEF1ED"; HT = "#4B5552"; CT = "#1C2321"
BAND = "#E6F3EA"
MONO = "'JetBrains Mono', Consolas, ui-monospace, monospace"
SANS = "'Space Grotesk', 'Segoe UI', system-ui, sans-serif"

# The column is 1080 wide, 80 px of padding each side.
COLUMN_INNER = 920
# A code card loses its padding, the amber bar and the line numbers: ~120 px.
CODE_INNER = 800
MONO_EM = 0.6          # a mono glyph is 0.6 em wide (JetBrains Mono, Consolas)
SERIES = "SERIES . 01 . TOPIC"


def set_series(name):
    """The tag line at the top of every column. Call it BEFORE building the
    panels: a panel reads it when it is made."""
    global SERIES
    SERIES = name


def svg(d, s=34, w=2.6):
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round">{d}</svg>')


CHECK = svg('<path d="M5 12.5l4.5 4.5L19 7"/>')
CROSS = svg('<path d="M6 6l12 12M18 6L6 18"/>')
ARROW = svg('<path d="M4 12h15M13 6l6 6-6 6"/>', 56, 2.2)
CHEV = svg('<path d="M6 9l6 6 6-6"/>', 22)
FUNNEL = svg('<path d="M3 5h18l-7 8v6l-4-2v-4z"/>', 22, 2.4)
TBL = svg('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/>', 26, 2)


# -- a mono line must not wrap ----------------------------------------------

def mono_size(lines, width=COLUMN_INNER, biggest=29, smallest=22):
    """The font size at which the longest of `lines` fits `width` px, and
    whether it fits at all. (size, fits). 0.6 em per glyph; the plan's rule
    of thumb 45 characters at 29 px across 920 is the same arithmetic."""
    longest = max((len(x) for x in lines), default=1)
    size = min(biggest, int(width / (MONO_EM * max(longest, 1))))
    return max(size, smallest), size >= smallest


# -- pieces ------------------------------------------------------------------

def key(t):
    return (f'<span style="display: inline-flex; align-items: center; padding: 10px 24px; '
            f'border: 2px solid #3E4B48; border-bottom-width: 7px; border-radius: 14px; '
            f'background: #18211F; font-family: {MONO}; font-size: 36px; font-weight: 700; '
            f'color: {TX}">{e(t)}</span>')


def keys(*ks, note=""):
    plus = f'<span style="font-family: {MONO}; font-size: 34px; color: {MU}">+</span>'
    n = (f'<span style="font-size: 32px; color: {MU}; margin-left: 12px">{e(note)}</span>'
         if note else '')
    return (f'<div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap">'
            f'{plus.join(key(k) for k in ks)}{n}</div>')


def badge(text, ok=True):
    c = GRT if ok else OR
    return (f'<div style="display: flex; align-items: center; gap: 14px; color: {c}; '
            f'font-size: 36px; font-weight: 700">{CHECK if ok else CROSS}<span>{e(text)}</span></div>')


def chip(text, fill=False):
    st = (f"background: {GR}; color: #FFFFFF; border: 2px solid {GR}" if fill
          else f"background: transparent; color: {TX}; border: 2px solid #3E4B48")
    return (f'<span style="display: inline-flex; padding: 12px 24px; border-radius: 999px; '
            f'font-size: 30px; font-weight: 500; {st}">{e(text)}</span>')


def chips(*cs, fill=False):
    return (f'<div style="display: flex; gap: 16px; flex-wrap: wrap">'
            f'{"".join(chip(c, fill) for c in cs)}</div>')


def note(html_text, color=None):
    return f'<div style="font-size: 32px; line-height: 1.4; color: {color or MU}">{html_text}</div>'


def fbar(formula, cursor=False, ref="fx", size=29):
    """A formula bar (also fine for one line of M or R). Escapes the text."""
    cur = (f'<span style="display: inline-block; width: 4px; height: 38px; background: {CT}; '
           f'margin-left: 2px; vertical-align: middle"></span>') if cursor else ''
    return (f'<div style="display: flex; align-items: center; background: {SH}; '
            f'border-radius: 14px; overflow: hidden; border: 2px solid {GL}">'
            f'<div style="padding: 18px 22px; background: {HB}; color: {HT}; font-family: {MONO}; '
            f'font-size: 28px; font-style: italic; border-right: 2px solid {GL}">{e(ref)}</div>'
            f'<div style="padding: 18px 22px; font-family: {MONO}; font-size: {size}px; '
            f'color: {CT}; white-space: nowrap">{e(formula)}{cur}</div></div>')


def code(lines, hl=(), title="", size=None):
    """A dark code card: Power Query M, R, VBA, DAX. `lines` are not wrapped;
    the size is chosen so the longest fits the column (mono_size) unless
    given. `hl` = 1-based line numbers drawn on an amber bar. Raises
    ValueError when the longest line cannot fit even at the smallest size:
    split the line, a board is not a text file."""
    fit, ok = mono_size(lines, CODE_INNER)
    if size is None:
        if not ok:
            raise ValueError(f"line of {max(len(x) for x in lines)} characters does not "
                             f"fit one column at {fit}px: {max(lines, key=len)!r}")
        size = fit
    rows = []
    for i, ln in enumerate(lines, 1):
        bg = "rgba(245,184,61,0.16)" if i in hl else "transparent"
        bar = AM if i in hl else "transparent"
        rows.append(f'<div style="display: flex; gap: 18px; padding: 4px 12px 4px 10px; '
                    f'background: {bg}; border-left: 5px solid {bar}; white-space: pre">'
                    f'<span style="color: #5F6C68; width: 34px; text-align: right">{i}</span>'
                    f'<span>{e(ln)}</span></div>')
    head = (f'<div style="color: {GRT}; font-size: {size}px">{e(title)}</div>' if title else '')
    return (f'<div style="padding: 24px 22px; background: #151E1C; border: 2px solid {LN}; '
            f'border-radius: 18px; display: flex; flex-direction: column; gap: 2px; '
            f'font-family: {MONO}; font-size: {size}px; line-height: 1.45; color: {TX}">'
            f'{head}{"".join(rows)}</div>')


def dropdown(items, hi):
    """items: [(text, 't'|'f')] t = object icon, f = function icon; hi = the
    highlighted index (-1 none). Up to about 7 items."""
    li = []
    for i, (t, k) in enumerate(items):
        bg = "#DFF1E6" if i == hi else "#FFFFFF"
        w = "700" if i == hi else "400"
        ic = (f'<span style="color: {GR}; display: flex">{TBL}</span>' if k == "t" else
              f'<span style="display: inline-flex; width: 26px; justify-content: center; '
              f'font-family: {MONO}; font-size: 22px; font-style: italic; color: #7A6A2E">fx</span>')
        li.append(f'<div style="display: flex; align-items: center; gap: 16px; padding: 14px 22px; '
                  f'background: {bg}; font-family: {MONO}; font-size: 29px; font-weight: {w}; '
                  f'color: {CT}; border-bottom: 1px solid {HB}">{ic}{e(t)}</div>')
    return (f'<div style="margin-top: -26px; margin-left: 120px; width: 700px; background: #FFFFFF; '
            f'border: 2px solid {GL}; border-radius: 12px; overflow: hidden; '
            f'box-shadow: 0 18px 40px rgba(0,0,0,0.35)">{"".join(li)}</div>')


def sheet(cols, rows, letters=True):
    """A mock sheet. cols: widths, the first is the row-number column (sum <=
    920; a header cell with a filter needs about chars*17.4+74 px).
    rows: dict(n, cells, kind, filters, active, filtered). kind: plain |
    header | theader | band | new | total | title. A cell may be
    (text, 'hl'|'warn'|'calc'|'sel')."""
    o = [f'<div style="background: {SH}; border-radius: 16px; overflow: hidden; '
         f'border: 2px solid {GL}; display: flex; flex-direction: column">']
    b = f"border-right: 2px solid {GL}; border-bottom: 2px solid {GL}"
    if letters:
        o.append('<div style="display: flex">'
                 f'<div style="width: {cols[0]}px; height: 54px; background: {HB}; {b}"></div>'
                 + "".join(f'<div style="width: {w}px; height: 54px; background: {HB}; {b}; '
                           f'display: flex; align-items: center; justify-content: center; '
                           f'font-family: {MONO}; font-size: 24px; color: {HT}">{chr(65 + i)}</div>'
                           for i, w in enumerate(cols[1:])) + '</div>')
    for r in rows:
        k = r.get("kind", "plain")
        f = r.get("filtered")
        cs = [f'<div style="width: {cols[0]}px; height: 74px; background: {HB}; {b}; display: flex; '
              f'align-items: center; justify-content: center; font-family: {MONO}; font-size: 24px; '
              f'font-weight: {"700" if f else "400"}; color: {GR if f else HT}">{e(str(r.get("n", "")))}</div>']
        vals = r.get("cells", [])
        for i, w in enumerate(cols[1:]):
            v = vals[i] if i < len(vals) else ""
            x = ""
            if isinstance(v, tuple):
                v, x = v
            al = "flex-start" if i == 0 else "flex-end"
            bg, col, wt = {"theader": (GR, "#FFFFFF", "700"), "header": ("#F6F7F5", CT, "700"),
                           "band": (BAND, CT, "400"), "new": ("#FFF1CF", CT, "400"),
                           "total": ("#F6F7F5", CT, "700"),
                           "title": (SH, CT, "700")}.get(k, (SH, CT, "400"))
            if x == "hl":
                bg, wt = "#FFE29A", "700"
            if x == "warn":
                bg = "#FFE1D2"
            if x == "calc":
                col, wt = GR, "700"
            if x == "sel":
                bg = "#DFF1E6"
            bd = (f"border-right: 2px solid {GL}; border-top: 4px double {GR}; "
                  f"border-bottom: 2px solid {GL}") if k == "total" else b
            fl = ""
            if k == "theader" and r.get("filters"):
                fl = (f'<span style="display: inline-flex; align-items: center; justify-content: center; '
                      f'width: 32px; height: 32px; background: #FFFFFF; color: {GR}; border-radius: 6px; '
                      f'margin-left: 10px">{FUNNEL if r.get("active") == i else CHEV}</span>')
                al = "space-between"
            cs.append(f'<div style="width: {w}px; height: 74px; box-sizing: border-box; padding: 0 16px; '
                      f'background: {bg}; {bd}; display: flex; align-items: center; justify-content: {al}; '
                      f'font-family: {MONO}; font-size: 29px; font-weight: {wt}; color: {col}; '
                      f'white-space: nowrap"><span>{e(str(v))}</span>{fl}</div>')
        o.append('<div style="display: flex">' + "".join(cs) + '</div>')
    return "".join(o) + '</div>'


def card(inner_html):
    return (f'<div style="padding: 26px 30px; background: #151E1C; border: 2px solid {LN}; '
            f'border-radius: 18px; display: flex; flex-direction: column; gap: 14px; '
            f'font-family: {MONO}; font-size: 29px; color: {TX}">{inner_html}</div>')


# -- a column, a board, a page ----------------------------------------------

def panel(step, head, sub, body, foot=""):
    """One 1080x1920 column. Safe zones: 220 px free at the top, content ends
    well above the caption zone (captions sit at 1490-1860 px in the film)."""
    return (f'<div style="width: 1080px; height: 1920px; box-sizing: border-box; '
            f'padding: 220px 80px 0 80px; display: flex; flex-direction: column">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; '
            f'font-family: {MONO}; font-size: 26px; letter-spacing: 0.08em; color: {MU}">'
            f'<span>{e(SERIES)}</span><span>{e(step)}</span></div>'
            f'<h1 style="margin: 56px 0 0 0; font-family: {SANS}; font-size: 84px; line-height: 1.04; '
            f'font-weight: 700; letter-spacing: -0.02em; color: {TX}">{head}</h1>'
            f'<p style="margin: 24px 0 0 0; font-size: 38px; line-height: 1.35; color: {MU}">{sub}</p>'
            f'<div style="margin-top: 64px; display: flex; flex-direction: column; gap: 36px">{body}</div>'
            f'<div style="margin-top: 56px; display: flex; flex-direction: column; gap: 28px">{foot}</div></div>')


def board_body(left, right):
    return (f'<div style="position: relative; width: 2160px; height: 1920px; background: {BG}; '
            f'color: {TX}; font-family: {SANS}; display: flex; overflow: hidden">'
            f'{left}<div style="width: 0; border-left: 2px dashed {LN}"></div>{right}'
            f'<div style="position: absolute; left: 1032px; top: 912px; width: 96px; height: 96px; '
            f'border-radius: 48px; background: {GR}; color: #FFFFFF; display: flex; '
            f'align-items: center; justify-content: center; box-shadow: 0 0 0 10px {BG}">{ARROW}</div></div>')


def local_fonts(font_dir=None):
    """@font-face rules for every .woff2/.ttf in models/fonts/, or ''.
    File names say the family: SpaceGrotesk-*.ttf, JetBrainsMono-*.ttf; a
    weight is read from the name (Regular 400, Medium 500, Bold 700)."""
    font_dir = font_dir or FONT_DIR
    if not os.path.isdir(font_dir):
        return ""
    rules = []
    weights = {"regular": 400, "medium": 500, "semibold": 600, "bold": 700}
    for name in sorted(os.listdir(font_dir)):
        stem, ext = os.path.splitext(name)
        if ext.lower() not in (".woff2", ".ttf"):
            continue
        family = ("Space Grotesk" if "grotesk" in stem.lower() else
                  "JetBrains Mono" if "jetbrains" in stem.lower() else None)
        if family is None:
            continue
        w = 400
        for key_, val in weights.items():
            if key_ in stem.lower():
                w = val
        url = "file:///" + os.path.join(font_dir, name).replace("\\", "/")
        rules.append(f"@font-face{{font-family:'{family}';font-weight:{w};src:url('{url}')}}")
    return "".join(rules)


ONLINE_FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
                'family=Space+Grotesk:wght@400;500;700&amp;family=JetBrains+Mono:wght@400;700'
                '&amp;display=swap">')


def page(title, body, font_dir=None):
    local = local_fonts(font_dir)
    # With local fonts the page never touches the network; without them it
    # asks Google when online and falls back to the system fonts offline.
    fonts = f"<style>{local}</style>" if local else ONLINE_FONTS
    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<title>{e(title)}</title>{fonts}'
            f'<style>html,body{{margin:0;padding:0;background:{BG}}}</style></head>'
            f'<body>{body}</body></html>')


def fname(title):
    """'01 Ctrl+T and name it' -> '01_Ctrl_T_and_name_it'"""
    return re.sub(r"_+", "_", re.sub(r"[^A-Za-z0-9]+", "_", title)).strip("_")


def write_boards(out_dir, slides, font_dir=None):
    """slides: [('NN Title of slide', left_html, right_html)]. Writes
    out_dir/NN_Title.html and out_dir/index.html (every board on one page,
    for review). Returns the list of file names written."""
    os.makedirs(out_dir, exist_ok=True)
    names = []
    for t, left, right in slides:
        n = fname(t) + ".html"
        names.append((t, n))
        with open(os.path.join(out_dir, n), "w", encoding="utf-8") as f:
            f.write(page(t, board_body(left, right), font_dir))
    idx = "".join(
        f'<h2 style="font:600 28px sans-serif;color:#F2F4F1;margin:40px 0 12px">{e(t)}</h2>'
        f'<iframe src="{n}" style="width:2160px;height:1920px;border:0;transform:scale(.4);'
        f'transform-origin:0 0;margin-bottom:-1150px"></iframe>' for t, n in names)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("Boards", f'<div style="padding:40px">{idx}</div>', font_dir))
    return [n for _, n in names]

#!/usr/bin/env python3
"""
Qalam Advisory logo system generator.

Builds every logo file in brand/qalam/ from one geometry definition, with all
lettering converted to outlines (no fonts needed to open the SVGs).

Requires: fonttools, uharfbuzz, and the Cinzel / Plus Jakarta Sans / Noto Kufi
Arabic font files (Google Fonts, OFL licence) in FONT_DIR.
"""
import math
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

OUT = Path(__file__).resolve().parent
FONT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT / "fonts"

# ---------------------------------------------------------------------------
# BRAND COLOURS
# ---------------------------------------------------------------------------
NAVY = "#0F172A"
GOLD = "#D4AF37"        # on dark backgrounds
GOLD_DEEP = "#A67C1F"   # gold text on light backgrounds (better contrast)
WHITE = "#FFFFFF"

# ---------------------------------------------------------------------------
# TEXT -> OUTLINES
# ---------------------------------------------------------------------------
_fonts = {}


def load(name, wght):
    key = (name, wght)
    if key not in _fonts:
        path = FONT_DIR / name
        tt = TTFont(path)
        static = instantiateVariableFont(tt, {"wght": wght}, inplace=False)
        blob = hb.Blob.from_file_path(str(path))
        face = hb.Face(blob)
        font = hb.Font(face)
        font.set_variations({"wght": wght})
        _fonts[key] = (static, font, face.upem)
    return _fonts[key]


def text_outline(font_name, wght, text, size, tracking=0.0):
    """Return (path_d, width, cap_top) for text set at `size` px, baseline at y=0."""
    static, font, upem = load(font_name, wght)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf)
    glyph_set = static.getGlyphSet()
    order = static.getGlyphOrder()
    scale = size / upem
    pen = SVGPathPen(glyph_set)
    x = 0.0
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        name = order[info.codepoint]
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x + pos.x_offset * scale, -pos.y_offset * scale))
        glyph_set[name].draw(tpen)
        x += pos.x_advance * scale
        if i < n - 1:
            x += tracking * size
    return pen.getCommands(), x


# ---------------------------------------------------------------------------
# THE MARK: a reed-pen nib and the nuqta (calligrapher's diamond dot)
# Designed upright in a 120x120 box, then tilted 45 degrees.
# ---------------------------------------------------------------------------
def star(cx, cy, R, r, n, rot=-90):
    pts = []
    for i in range(2 * n):
        a = math.radians(rot + i * 180 / n)
        rad = R if i % 2 == 0 else r
        pts.append(f"{cx + rad * math.cos(a):.2f},{cy + rad * math.sin(a):.2f}")
    return " ".join(pts)


NIB = "M42 12 H78 V40 C78 54 70 70 60 86 C50 70 42 54 42 40 Z"
NIB_COMPACT = "M38 10 H82 V40 C82 56 72 72 60 92 C48 72 38 56 38 40 Z"
# Drawn as a square: the 45-degree tilt turns it into the calligrapher's diamond dot.
NUQTA = "M54.5 91.5 H65.5 V102.5 H54.5 Z"
# Tilt 45 degrees, then centre the tilted shape's bounding box and scale it to fill the box.
TILT = "translate(60 60) scale(1.28) translate(-66.4 -53.6) rotate(45 60 60)"

_mask_id = [0]


def mark(nib_color, dot_color, compact=False):
    """SVG group for the mark in a 120x120 coordinate box."""
    _mask_id[0] += 1
    mid = f"qn{_mask_id[0]}"
    if compact:
        cuts = ('<circle cx="60" cy="54" r="6" fill="#000"/>'
                '<rect x="57.5" y="56" width="5" height="40" fill="#000"/>')
        nib = NIB_COMPACT
    else:
        cuts = ('<rect x="30" y="24.5" width="60" height="4" fill="#000"/>'
                f'<polygon points="{star(60, 54, 7, 3.1, 8)}" fill="#000"/>'
                '<rect x="58.7" y="58" width="2.6" height="32" fill="#000"/>')
        nib = NIB
    return (f'<g transform="{TILT}">'
            f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="120" height="120">'
            f'<rect x="0" y="0" width="120" height="120" fill="#fff"/>{cuts}</mask>'
            f'<path d="{nib}" fill="{nib_color}" mask="url(#{mid})"/>'
            f'<path d="{NUQTA}" fill="{dot_color}"/>'
            f'</g>')


def svg(w, h, body, bg=None, title="Qalam Advisory"):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{rect}{body}</svg>\n')


# ---------------------------------------------------------------------------
# LOCKUPS
# ---------------------------------------------------------------------------
def wordmark(name_color, sub_color, x, y_base, size=64):
    qd, qw = text_outline("Cinzel.ttf", 700, "QALAM", size, tracking=0.10)
    sub_size = size * 0.25
    sd, sw = text_outline("PlusJakartaSans.ttf", 700, "ADVISORY", sub_size)
    # track "ADVISORY" out so it spans exactly the width of QALAM
    sd, sw = text_outline("PlusJakartaSans.ttf", 700, "ADVISORY", sub_size, tracking=(qw - sw) / 7 / sub_size)
    body = (f'<path transform="translate({x:.2f} {y_base:.2f})" d="{qd}" fill="{name_color}"/>'
            f'<path transform="translate({x:.2f} {y_base + size * 0.62:.2f})" d="{sd}" fill="{sub_color}"/>')
    return body, qw


def horizontal(theme):
    nib, dot, name, sub = (NAVY, GOLD, NAVY, GOLD_DEEP) if theme == "light" else (GOLD, GOLD, WHITE, GOLD)
    m = 120
    text, tw = wordmark(name, sub, m + 20, 64)
    w = m + 20 + tw + 6
    body = f'<g>{mark(nib, dot)}</g>{text}'
    return svg(w, 120, body)


def stacked(theme):
    nib, dot, name, sub = (NAVY, GOLD, NAVY, GOLD_DEEP) if theme == "light" else (GOLD, GOLD, WHITE, GOLD)
    _, tw = wordmark(name, sub, 0, 0)
    w = max(tw, 120) + 20
    text, _ = wordmark(name, sub, (w - tw) / 2, 192)
    body = f'<g transform="translate({(w - 130) / 2:.2f} 0) scale(1.0833)">{mark(nib, dot)}</g>' + text
    return svg(w, 240, body)


def bilingual(theme):
    nib, dot, name, sub = (NAVY, GOLD, NAVY, GOLD_DEEP) if theme == "light" else (GOLD, GOLD, WHITE, GOLD)
    _, tw = wordmark(name, sub, 0, 0)
    ad, aw = text_outline("NotoKufiArabic.ttf", 700, "قلم للاستشارات", 34)
    w = max(tw, aw, 120) + 20
    cx = w / 2
    text, _ = wordmark(name, sub, cx - tw / 2, 192)
    body = (f'<g transform="translate({cx - 65:.2f} 0) scale(1.0833)">{mark(nib, dot)}</g>'
            + text
            + f'<rect x="{cx - 24:.2f}" y="256" width="48" height="2" fill="{sub}"/>'
            + f'<path transform="translate({cx - aw / 2:.2f} 310)" d="{ad}" fill="{name}"/>')
    return svg(w, 332, body, title="Qalam Advisory | قلم للاستشارات")


def icon(size=512, compact=False, pad=0.0, radius=0.22, circle_safe=False):
    """Gold mark on a navy tile. circle_safe adds padding for circular crops (Instagram)."""
    inner = 0.70 if not circle_safe else 0.60
    s = size * inner / 120
    off = (size - 120 * s) / 2
    rx = size * radius
    body = (f'<rect width="{size}" height="{size}" rx="{rx:.1f}" fill="{NAVY}"/>'
            f'<g transform="translate({off:.2f} {off:.2f}) scale({s:.4f})">{mark(GOLD, GOLD, compact)}</g>')
    return svg(size, size, body)


def og_image():
    w, h = 1200, 630
    gx = 470
    text, tw = wordmark(WHITE, GOLD, gx, 290, size=96)
    ar_d, ar_w = text_outline("NotoKufiArabic.ttf", 700, "قلم للاستشارات", 40)
    tag_d, tag_w = text_outline("PlusJakartaSans.ttf", 600, "Tax · Audit · Company Formation · TIFC", 28)
    lang_d, lang_w = text_outline("PlusJakartaSans.ttf", 600, "Tashkent, Uzbekistan  ·  EN · RU · AR · UZ", 22, tracking=0.06)
    body = (
        f'<rect width="{w}" height="{h}" fill="{NAVY}"/>'
        f'<rect width="{w}" height="10" fill="{GOLD}"/>'
        f'<circle cx="230" cy="315" r="200" fill="#16213D"/>'
        f'<g transform="translate(80 165) scale(2.5)">{mark(GOLD, GOLD)}</g>'
        + text
        + f'<path transform="translate({gx + tw - ar_w:.2f} 412)" d="{ar_d}" fill="{GOLD}"/>'
        + f'<rect x="{gx}" y="452" width="{tw:.0f}" height="1.5" fill="#334155"/>'
        + f'<path transform="translate({gx} 500)" d="{tag_d}" fill="#CBD5E1"/>'
        + f'<path transform="translate({gx} 560)" d="{lang_d}" fill="#94A3B8"/>'
    )
    return svg(w, h, body)


def main():
    files = {
        "logo-horizontal.svg": horizontal("light"),
        "logo-horizontal-reverse.svg": horizontal("dark"),
        "logo-stacked.svg": stacked("light"),
        "logo-stacked-reverse.svg": stacked("dark"),
        "logo-bilingual-arabic.svg": bilingual("light"),
        "logo-bilingual-arabic-reverse.svg": bilingual("dark"),
        "mark.svg": svg(120, 120, mark(NAVY, GOLD)),
        "mark-reverse.svg": svg(120, 120, mark(GOLD, GOLD)),
        "mark-black.svg": svg(120, 120, mark("#000000", "#000000")),
        "mark-white.svg": svg(120, 120, mark(WHITE, WHITE)),
        "icon.svg": icon(512),
        "icon-profile.svg": icon(1080, circle_safe=True, radius=0),
        "favicon.svg": icon(64, compact=True, radius=0.2),
        "og-image.svg": og_image(),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"Wrote {len(files)} SVG files to {OUT}")


if __name__ == "__main__":
    main()

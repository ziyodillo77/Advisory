#!/usr/bin/env python3
"""Qalam Advisory: round 2 logo exploration (Q / qaf monogram, custom wordmark, seal)."""
import math
import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_qalam as base  # noqa: E402  (reuses fonts + text_outline)

OUT = Path(__file__).resolve().parent / "v2"
OUT.mkdir(exist_ok=True)
NAVY, GOLD, GOLD_DEEP, WHITE = base.NAVY, base.GOLD, base.GOLD_DEEP, base.WHITE


def ellipse_path(cx, cy, rx, ry, rot_deg, n=96):
    """Ellipse as a polygon-like smooth path (enough points to look perfectly smooth)."""
    a = math.radians(rot_deg)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


def diamond(cx, cy, r):
    return f"M{cx:.2f} {cy - r:.2f} L{cx + r:.2f} {cy:.2f} L{cx:.2f} {cy + r:.2f} L{cx - r:.2f} {cy:.2f} Z"


# ---------------------------------------------------------------------------
# MONOGRAM: Latin Q + Arabic qaf (ق)
# Bowl: outer ellipse minus a rotated, offset inner ellipse = broad-nib stroke
# contrast (thick at 4-5 and 10-11 o'clock, hairline at 1-2 and 7-8 o'clock).
# Tail: a tapered reed-pen stroke ending in the nuqta. Two nuqtas above = qaf.
# ---------------------------------------------------------------------------
def monogram(color, dot_color, with_qaf_dots=False):
    outer = ellipse_path(60, 64, 40, 41, 0)
    inner = ellipse_path(61.5, 63, 28.5, 33.5, -32)
    bowl = f'<path d="{outer} {inner}" fill="{color}" fill-rule="evenodd"/>'
    # Tapered tail: starts thick inside the lower bowl, sweeps out to the right.
    tail = ('M48 99.5 C65 96.5 82 102 96 109.5 C101 112 105.5 113.6 110 114.2 '
            'C104 117 97 117 90 115 C76 111 63 106.5 52.5 103.6 Z')
    t = f'<path d="{tail}" fill="{color}"/>'
    dots = ''
    if with_qaf_dots:
        dots = (f'<path d="{diamond(51, 11, 6.2)}" fill="{dot_color}"/>'
                f'<path d="{diamond(69, 11, 6.2)}" fill="{dot_color}"/>')
    end = f'<path d="{diamond(117, 114.2, 4.4)}" fill="{dot_color}"/>'
    return bowl + t + dots + end


# ---------------------------------------------------------------------------
# CUSTOM WORDMARK: Cinzel "O" + hand-drawn Q tail ending in the nuqta, then "ALAM"
# ---------------------------------------------------------------------------
def glyph_bounds(font_name, wght, char, size):
    static, font, upem = base.load(font_name, wght)
    gs = static.getGlyphSet()
    name = static.getBestCmap()[ord(char)]
    bp = BoundsPen(gs)
    gs[name].draw(bp)
    xmin, ymin, xmax, ymax = bp.bounds
    s = size / upem
    return xmin * s, -ymax * s, xmax * s, -ymin * s  # y flipped (baseline 0)


def custom_wordmark(color, dot_color, size=80, tracking=0.085):
    d, w = base.text_outline("Cinzel.ttf", 700, "OALAM", size, tracking=tracking)
    x0, y0, x1, y1 = glyph_bounds("Cinzel.ttf", 700, "O", size)
    cx = (x0 + x1) / 2
    ow = x1 - x0
    # Tail drawn relative to the O: emerges at the bottom, sweeps under the A.
    k = ow / 100
    bx, by = cx - 6 * k, y1 - 2 * k
    P = lambda x, y: f"{bx + x * k:.2f} {by + y * k:.2f}"
    tail = (f'M{P(-2, -8)} C{P(18, -8)} {P(38, -1)} {P(58, 8)} C{P(64, 11)} {P(70, 13)} {P(77, 13.6)} '
            f'C{P(70, 16.6)} {P(61, 16.4)} {P(53, 13.5)} C{P(36, 8)} {P(18, 3)} {P(-4, 1)} Z')
    dot = diamond(bx + 84 * k, by + 13.6 * k, 4.6 * k)
    body = f'<path d="{d}" fill="{color}"/><path d="{tail}" fill="{color}"/><path d="{dot}" fill="{dot_color}"/>'
    return body, w, size


def advisory_line(color, size, width=None, tracking=0.42):
    d, w = base.text_outline("PlusJakartaSans.ttf", 600, "ADVISORY", size, tracking=tracking)
    return d, w


# ---------------------------------------------------------------------------
# COMPOSITIONS
# ---------------------------------------------------------------------------
def svg(w, h, body, bg=None):
    return base.svg(w, h, body, bg=bg)


def concept_a(theme):
    """Monogram + custom wordmark, horizontal."""
    dark = theme == "dark"
    c, dot, sub = (WHITE, GOLD, GOLD) if dark else (NAVY, GOLD, GOLD_DEEP)
    mono_c = GOLD if dark else NAVY
    qd, ww = base.text_outline("Cinzel.ttf", 700, "QALAM", 70, tracking=0.09)
    wm = f'<path d="{qd}" fill="{c}"/>'
    ad, aw = advisory_line(sub, 15, tracking=0.34)
    mx = 0
    gx = 150
    body = (f'<g transform="translate({mx} 4)">{monogram(mono_c, GOLD)}</g>'
            f'<rect x="{gx - 18}" y="22" width="1.2" height="88" fill="{sub}" opacity=".55"/>'
            f'<g transform="translate({gx} 78)">{wm}</g>'
            f'<path transform="translate({gx} 108)" d="{ad}" fill="{sub}"/>')
    return svg(gx + ww + 30, 128, body)


def concept_b(theme):
    """Wordmark-only, the way premium advisory firms work."""
    dark = theme == "dark"
    c, sub = (WHITE, GOLD) if dark else (NAVY, GOLD_DEEP)
    wm, ww, size = custom_wordmark(c, GOLD, 110, tracking=0.07)
    ad, aw = advisory_line(sub, 17, tracking=0.55)
    rule_w = (ww - aw) / 2 - 18
    y = 126
    body = (f'<g transform="translate(10 100)">{wm}</g>'
            f'<rect x="10" y="{y + 15}" width="{rule_w:.1f}" height="1.4" fill="{sub}"/>'
            f'<path transform="translate({10 + (ww - aw) / 2:.2f} {y + 21})" d="{ad}" fill="{sub}"/>'
            f'<rect x="{10 + ww - rule_w:.1f}" y="{y + 15}" width="{rule_w:.1f}" height="1.4" fill="{sub}"/>')
    return svg(ww + 40, 168, body)


def concept_c(theme):
    """Seal (muhr): traditional stamp of Bukhara chancelleries, modernised."""
    dark = theme == "dark"
    c = GOLD if dark else NAVY
    sub = GOLD if dark else GOLD_DEEP
    R = 150
    cx = cy = 160
    # text on circle: lay out glyphs along the arc
    def arc_text(text, radius, size, center_deg, fill, tracking=0.18, bottom=False,
                 font="PlusJakartaSans.ttf", wght=700):
        """Set text along a circle, spacing letters by their real widths (like a seal engraver)."""
        glyphs = [base.text_outline(font, wght, ch, size) for ch in text]
        widths = [gw + tracking * size for _, gw in glyphs]
        total = sum(widths) - tracking * size
        deg_per_px = 180 / (math.pi * radius)
        direction = -1 if bottom else 1          # bottom text runs right-to-left in angle
        ang = center_deg - direction * total / 2 * deg_per_px
        out = []
        for (d, gw), w in zip(glyphs, widths):
            mid = ang + direction * gw / 2 * deg_per_px
            a = math.radians(mid)
            x, y = cx + radius * math.cos(a), cy + radius * math.sin(a)
            rot = mid + 90 if not bottom else mid - 90
            dy = size * 0.36 if not bottom else size * 0.36
            out.append(f'<path transform="translate({x:.2f} {y:.2f}) rotate({rot:.2f}) translate({-gw / 2:.2f} {dy:.2f})" d="{d}" fill="{fill}"/>')
            ang += direction * w * deg_per_px
        return "".join(out)
    top = arc_text("QALAM ADVISORY", 118, 21, -90, c, tracking=0.22)
    bottom = arc_text("TASHKENT · UZBEKISTAN", 118, 14, 90, sub, tracking=0.2, bottom=True)
    body = (f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{c}" stroke-width="5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{R - 12}" fill="none" stroke="{c}" stroke-width="1.4"/>'
            f'<circle cx="{cx}" cy="{cy}" r="96" fill="none" stroke="{c}" stroke-width="1.4"/>'
            + top + bottom
            + f'<path d="{diamond(cx - 118, cy, 5)}" fill="{GOLD}"/><path d="{diamond(cx + 118, cy, 5)}" fill="{GOLD}"/>'
            + f'<g transform="translate({cx - 80} {cy - 81}) scale(1.15)">{monogram(c, GOLD)}</g>')
    return svg(320, 320, body)


def monogram_tile(size=512, circle_safe=False):
    inner = 0.62 if circle_safe else 0.72
    s = size * inner / 122
    off = (size - 122 * s) / 2
    rx = 0 if circle_safe else size * 0.22
    return svg(size, size, f'<rect width="{size}" height="{size}" rx="{rx}" fill="{NAVY}"/>'
               f'<g transform="translate({off:.2f} {off - 2 * s:.2f}) scale({s:.4f})">{monogram(GOLD, GOLD)}</g>')


def main():
    files = {
        "A-monogram-light.svg": concept_a("light"),
        "A-monogram-dark.svg": concept_a("dark"),
        "B-wordmark-light.svg": concept_b("light"),
        "B-wordmark-dark.svg": concept_b("dark"),
        "C-seal-light.svg": concept_c("light"),
        "C-seal-dark.svg": concept_c("dark"),
        "monogram.svg": svg(122, 122, monogram(NAVY, GOLD)),
        "monogram-tile.svg": monogram_tile(),
        "monogram-profile.svg": monogram_tile(1080, circle_safe=True),
    }
    for n, c in files.items():
        (OUT / n).write_text(c, encoding="utf-8")
    print("wrote", len(files))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        base.FONT_DIR = Path(sys.argv[1])
    main()

#!/usr/bin/env python3
"""
Mezon Advisory: final logo system (concept A, "Equilibrium").

The mark: a circle split into two exactly equal halves (navy over gold)
resting on the line of balance. In the wordmark it becomes the O of MEZON.

Usage:  python3 brand/mezon/make_final.py
Writes SVGs to brand/mezon/final/ (lettering converted to outlines).
PNG versions are rendered from these SVGs with resvg (see README in final/).
"""
from pathlib import Path

from make_concepts import NAVY, WHITE, P, cap_height, svg, text

HERE = Path(__file__).resolve().parent
OUT = HERE / "final"
OUT.mkdir(exist_ok=True)

GOLD = "#C9A227"        # gold half of the mark
GOLD_TEXT = "#A67C1F"   # gold text on light backgrounds
GOLD_ON_DARK = "#D4AF37"

FONT, WEIGHT, TRACK = "Outfit.ttf", 500, 0.16


# ---------------------------------------------------------------------------
# The mark (drawn in a 120 x 120 box)
# ---------------------------------------------------------------------------
def mark(top, bottom, beam=True, beam_color=None):
    gap = 2.2
    body = (P(f"M22 {60 - gap} A38 38 0 0 1 98 {60 - gap} Z", top)
            + P(f"M22 {60 + gap} A38 38 0 0 0 98 {60 + gap} Z", bottom))
    if beam:
        bc = beam_color or top
        body += (f'<rect x="2" y="58.9" width="14" height="2.2" rx="1.1" fill="{bc}"/>'
                 f'<rect x="104" y="58.9" width="14" height="2.2" rx="1.1" fill="{bc}"/>')
    return body


# ---------------------------------------------------------------------------
# Wordmark: MEZ + mark-as-O + N, with ADVISORY below
# ---------------------------------------------------------------------------
def wordmark(color, sub_color, x, baseline, size=84):
    """Returns (svg body, total width, bottom y)."""
    capH = cap_height(FONT, WEIGHT, size)
    sp = TRACK * size
    d1, w1 = text(FONT, WEIGHT, "MEZ", size, tracking=TRACK)
    d2, w2 = text(FONT, WEIGHT, "N", size)
    o = capH * 1.05                         # optical overshoot: round shapes sit slightly larger than caps
    s = o / 76
    ox = x + w1 + sp
    oy = baseline - capH / 2 - 60 * s
    body = (P(d1, color, x, baseline)
            + f'<g transform="translate({ox - 22 * s:.2f} {oy:.2f}) scale({s:.4f})">{mark(color, GOLD, beam=False)}</g>'
            + P(d2, color, ox + o + sp, baseline))
    total = ox + o + sp + w2 - x
    # ADVISORY spans exactly the width of "MEZ", so its right edge lines up with the Z.
    sub_size = size * 0.26
    mez_w = w1 - sp                          # visible width of "MEZ" (without trailing tracking)
    _, plain_w = text(FONT, WEIGHT, "ADVISORY", sub_size)
    sd, sw = text(FONT, WEIGHT, "ADVISORY", sub_size, tracking=(mez_w - plain_w) / 7 / sub_size)
    sub_y = baseline + size * 0.52
    body += P(sd, sub_color, x, sub_y)
    return body, total, sub_y


def logo(dark=False):
    c, sub = (WHITE, GOLD_ON_DARK) if dark else (NAVY, GOLD_TEXT)
    body, w, bottom = wordmark(c, sub, 10, 76)
    return svg(w + 20, bottom + 12, body)


def logo_arabic(dark=False):
    c, sub = (WHITE, GOLD_ON_DARK) if dark else (NAVY, GOLD_TEXT)
    body, w, bottom = wordmark(c, sub, 10, 76)
    ad, aw = text("NotoKufiArabic.ttf", 700, "ميزان للاستشارات", 22)
    # Arabic reads right to left: its own line, aligned to the right edge under the N.
    body += P(ad, c, 10 + w - aw, bottom + 40)
    return svg(w + 20, bottom + 54, body, title="Mezon Advisory | ميزان للاستشارات")


def icon(size=512, inner=0.66, rx=0.22, beam=True):
    s = size * inner / 120
    off = (size - 120 * s) / 2
    return svg(size, size,
               f'<rect width="{size}" height="{size}" rx="{size * rx:.1f}" fill="{NAVY}"/>'
               f'<g transform="translate({off:.2f} {off:.2f}) scale({s:.4f})">{mark(WHITE, GOLD_ON_DARK, beam=beam)}</g>')


def social_share():
    w, h = 1200, 630
    cy = 315
    body = (f'<rect width="{w}" height="{h}" fill="{NAVY}"/>'
            # the line of balance runs across the whole card
            f'<rect x="0" y="{cy - 1}" width="440" height="2" fill="#FFFFFF" opacity=".12"/>'
            f'<g transform="translate(70 {cy - 180}) scale(3)">{mark(WHITE, GOLD_ON_DARK, beam=False)}</g>')
    wm, ww, bottom = wordmark(WHITE, GOLD_ON_DARK, 470, 236, size=92)
    ad, aw = text("NotoKufiArabic.ttf", 700, "ميزان للاستشارات", 30)
    tag, tw = text("PlusJakartaSans.ttf", 600, "Tax · Audit · Company Formation · TIFC", 27)
    loc, lw = text("PlusJakartaSans.ttf", 600, "Tashkent, Uzbekistan  ·  EN · RU · AR · UZ", 21, tracking=0.05)
    body += (wm
             + P(ad, GOLD_ON_DARK, 470 + ww - aw, bottom + 58)
             + f'<rect x="470" y="{bottom + 84:.0f}" width="{ww:.0f}" height="1.5" fill="#334155"/>'
             + P(tag, "#CBD5E1", 470, bottom + 132)
             + P(loc, "#94A3B8", 470, bottom + 176))
    return svg(w, h, body)


def main():
    files = {
        "mezon-logo.svg": logo(),
        "mezon-logo-white.svg": logo(dark=True),
        "mezon-logo-arabic.svg": logo_arabic(),
        "mezon-logo-arabic-white.svg": logo_arabic(dark=True),
        "mezon-mark.svg": svg(120, 120, mark(NAVY, GOLD)),
        "mezon-mark-white.svg": svg(120, 120, mark(WHITE, GOLD_ON_DARK)),
        "mezon-mark-black.svg": svg(120, 120, mark("#000000", "#000000")),
        "mezon-icon.svg": icon(),
        "mezon-favicon.svg": icon(64, inner=0.80, beam=False),
        "mezon-profile.svg": icon(1080, inner=0.72, rx=0, beam=True),
        "mezon-social-share.svg": social_share(),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"Wrote {len(files)} SVGs to {OUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Qalam Advisory: final logo system export.

Primary logo: custom wordmark (hand-drawn Q tail ending in the nuqta).
Icon: calligraphic Q monogram.  Secondary: seal (muhr).

Usage:
    python3 brand/qalam/make_final.py <font-dir>
Writes SVGs to brand/qalam/final/. PNGs are rendered separately with resvg
(see export_png.sh).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_qalam as base  # noqa: E402
import make_qalam2 as v2  # noqa: E402

if len(sys.argv) > 1:
    base.FONT_DIR = Path(sys.argv[1])

OUT = HERE / "final"
OUT.mkdir(exist_ok=True)
NAVY, GOLD, GOLD_DEEP, WHITE = base.NAVY, base.GOLD, base.GOLD_DEEP, base.WHITE
svg = base.svg


def wordmark_block(color, sub, x, y, size=110):
    """Wordmark + ruled ADVISORY line. Returns (body, width, height)."""
    wm, ww, _ = v2.custom_wordmark(color, GOLD, size, tracking=0.07)
    asz = size * 0.155
    ad, aw = v2.advisory_line(sub, asz, tracking=0.55)
    rule_w = (ww - aw) / 2 - asz * 1.05
    rule_y = y + size * 0.30
    body = (f'<g transform="translate({x:.2f} {y:.2f})">{wm}</g>'
            f'<rect x="{x:.2f}" y="{rule_y:.2f}" width="{rule_w:.2f}" height="{size * 0.013:.2f}" fill="{sub}"/>'
            f'<path transform="translate({x + (ww - aw) / 2:.2f} {rule_y + asz * 0.37:.2f})" d="{ad}" fill="{sub}"/>'
            f'<rect x="{x + ww - rule_w:.2f}" y="{rule_y:.2f}" width="{rule_w:.2f}" height="{size * 0.013:.2f}" fill="{sub}"/>')
    return body, ww, rule_y + asz


def logo(theme):
    c, sub = (NAVY, GOLD_DEEP) if theme == "light" else (WHITE, GOLD)
    body, ww, bottom = wordmark_block(c, sub, 10, 100)
    return svg(ww + 20, bottom + 14, body)


def logo_arabic(theme):
    c, sub = (NAVY, GOLD_DEEP) if theme == "light" else (WHITE, GOLD)
    body, ww, bottom = wordmark_block(c, sub, 10, 100)
    ad, aw = base.text_outline("NotoKufiArabic.ttf", 700, "قلم للاستشارات", 36)
    w = ww + 20
    y = bottom + 62
    body += f'<path transform="translate({(w - aw) / 2:.2f} {y:.2f})" d="{ad}" fill="{c}"/>'
    return svg(w, y + 22, body, title="Qalam Advisory | قلم للاستشارات")


def monogram(nib, dot, size=122):
    return svg(size, size, v2.monogram(nib, dot))


def tile(size, inner=0.72, rounded=True):
    s = size * inner / 122
    off = (size - 122 * s) / 2
    rx = size * 0.22 if rounded else 0
    return svg(size, size, f'<rect width="{size}" height="{size}" rx="{rx:.1f}" fill="{NAVY}"/>'
               f'<g transform="translate({off:.2f} {off - 1.5 * s:.2f}) scale({s:.4f})">{v2.monogram(GOLD, GOLD)}</g>')


def social_share():
    w, h = 1200, 630
    seal = v2.concept_c("dark")
    seal_body = seal[seal.index('<title>'):seal.rindex('</svg>')]
    seal_body = seal_body[seal_body.index('</title>') + 8:]
    wm, ww, bottom = wordmark_block(WHITE, GOLD, 540, 275, size=104)
    ad, aw = base.text_outline("NotoKufiArabic.ttf", 700, "قلم للاستشارات", 38)
    tag, tw = base.text_outline("PlusJakartaSans.ttf", 600, "Tax · Audit · Company Formation · TIFC", 27)
    loc, lw = base.text_outline("PlusJakartaSans.ttf", 600, "Tashkent, Uzbekistan  ·  EN · RU · AR · UZ", 21, tracking=0.05)
    body = (f'<rect width="{w}" height="{h}" fill="{NAVY}"/>'
            f'<rect y="{h - 10}" width="{w}" height="10" fill="{GOLD}"/>'
            f'<g transform="translate(70 125) scale(1.19)">{seal_body}</g>'
            + wm
            + f'<path transform="translate({540 + ww - aw:.2f} {bottom + 58:.2f})" d="{ad}" fill="{GOLD}"/>'
            + f'<path transform="translate(540 {bottom + 128:.2f})" d="{tag}" fill="#CBD5E1"/>'
            + f'<path transform="translate(540 {bottom + 172:.2f})" d="{loc}" fill="#94A3B8"/>')
    return svg(w, h, body)


def main():
    files = {
        "qalam-logo.svg": logo("light"),
        "qalam-logo-white.svg": logo("dark"),
        "qalam-logo-arabic.svg": logo_arabic("light"),
        "qalam-logo-arabic-white.svg": logo_arabic("dark"),
        "qalam-seal.svg": v2.concept_c("light"),
        "qalam-seal-gold.svg": v2.concept_c("dark"),
        "qalam-monogram.svg": monogram(NAVY, GOLD),
        "qalam-monogram-gold.svg": monogram(GOLD, GOLD),
        "qalam-monogram-white.svg": monogram(WHITE, GOLD),
        "qalam-monogram-black.svg": monogram("#000000", "#000000"),
        "qalam-icon.svg": tile(512),
        "qalam-favicon.svg": tile(64, inner=0.84, rounded=True),
        "qalam-profile.svg": tile(1080, inner=0.58, rounded=False),
        "qalam-social-share.svg": social_share(),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"Wrote {len(files)} SVGs to {OUT}")


if __name__ == "__main__":
    main()

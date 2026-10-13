#!/usr/bin/env python3
"""
Mezon Advisory: logo concept generator.

Writes brand/mezon/concepts/*.svg (all lettering converted to outlines) and
brand/mezon/concepts/index.html (comparison page with real-use mockups).

Requires fonttools + uharfbuzz. Fonts live in brand/fonts (Google Fonts, OFL).
"""
import math
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "fonts"
OUT = HERE / "concepts"
OUT.mkdir(exist_ok=True)

NAVY = "#0F172A"
GOLD = "#C9A227"
GOLD_LIGHT = "#D4AF37"
GOLD_DEEP = "#A67C1F"
WHITE = "#FFFFFF"
MUTED = "#64748B"

# ---------------------------------------------------------------------------
# Text -> outlines
# ---------------------------------------------------------------------------
_cache = {}


def _font(name, wght):
    key = (name, wght)
    if key not in _cache:
        path = FONTS / name
        static = instantiateVariableFont(TTFont(path), {"wght": wght}, inplace=False)
        face = hb.Face(hb.Blob.from_file_path(str(path)))
        font = hb.Font(face)
        font.set_variations({"wght": wght})
        _cache[key] = (static, font, face.upem)
    return _cache[key]


def text(font_name, wght, s, size, tracking=0.0):
    """Outline `s` with baseline at y=0. Returns (path_d, advance_width)."""
    static, font, upem = _font(font_name, wght)
    buf = hb.Buffer()
    buf.add_str(s)
    buf.guess_segment_properties()
    hb.shape(font, buf)
    gs, order, k = static.getGlyphSet(), static.getGlyphOrder(), size / upem
    pen = SVGPathPen(gs)
    x = 0.0
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        gs[order[info.codepoint]].draw(TransformPen(pen, (k, 0, 0, -k, x + pos.x_offset * k, -pos.y_offset * k)))
        x += pos.x_advance * k + (tracking * size if i < n - 1 else 0)
    return pen.getCommands(), x


def cap_height(font_name, wght, size):
    static, _, upem = _font(font_name, wght)
    return static["OS/2"].sCapHeight * size / upem


def svg(w, h, body, title="Mezon Advisory"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')


def P(d, fill, tx=0, ty=0):
    t = f' transform="translate({tx:.2f} {ty:.2f})"' if (tx or ty) else ""
    return f'<path{t} d="{d}" fill="{fill}"/>'


def star_pts(cx, cy, R, r, n, rot=-90):
    pts = []
    for i in range(2 * n):
        a = math.radians(rot + i * 180 / n)
        rad = R if i % 2 == 0 else r
        pts.append(f"{cx + rad * math.cos(a):.2f},{cy + rad * math.sin(a):.2f}")
    return " ".join(pts)


# ---------------------------------------------------------------------------
# MARKS (120 x 120 box). Each takes (primary, accent) colours.
# ---------------------------------------------------------------------------
def mark_equilibrium(c1, c2, beam=True):
    """Two exactly equal halves of a circle, separated by the line of balance."""
    gap = 2.2
    top = f"M22 {60 - gap} A38 38 0 0 1 98 {60 - gap} Z"
    bottom = f"M22 {60 + gap} A38 38 0 0 0 98 {60 + gap} Z"
    body = P(top, c1) + P(bottom, c2)
    if beam:
        body += (f'<rect x="2" y="{60 - 1.1}" width="14" height="2.2" rx="1.1" fill="{c1}"/>'
                 f'<rect x="104" y="{60 - 1.1}" width="14" height="2.2" rx="1.1" fill="{c1}"/>')
    return body


def mark_measure(c1, c2):
    """Five measured bars forming an M; the gold point marks the standard."""
    w, gap, base = 14, 7.5, 104
    heights = [74, 52, 34, 52, 74]
    total = 5 * w + 4 * gap
    x0 = (120 - total) / 2
    body = ""
    for i, h in enumerate(heights):
        x = x0 + i * (w + gap)
        body += f'<rect x="{x:.2f}" y="{base - h:.2f}" width="{w}" height="{h}" rx="3" fill="{c1}"/>'
    cx = x0 + 2 * (w + gap) + w / 2
    body += f'<circle cx="{cx:.2f}" cy="{base - heights[2] - 17:.2f}" r="7.5" fill="{c2}"/>'
    return body


def mark_girih(c1, c2):
    """Eight-point star from two interlocking squares: two standards in balance."""
    s = 31  # half-side
    sq = f'<rect x="{60 - s}" y="{60 - s}" width="{2 * s}" height="{2 * s}" fill="none" stroke="{c1}" stroke-width="7" stroke-linejoin="miter"/>'
    sq2 = (f'<rect x="{60 - s}" y="{60 - s}" width="{2 * s}" height="{2 * s}" fill="none" stroke="{c2}" stroke-width="7" '
           f'stroke-linejoin="miter" transform="rotate(45 60 60)"/>')
    # The squares' edges cross at 8 points. Re-draw the first square on top at every
    # other crossing so the two squares weave over and under each other.
    d = s * math.sqrt(2) - s           # distance from the edge midpoint to a crossing
    xs = [(60 - d, 60 - s), (60 + s, 60 - d), (60 + d, 60 + s), (60 - s, 60 + d)]
    rects = "".join(f'<rect x="{x - 8:.2f}" y="{y - 8:.2f}" width="16" height="16"/>' for x, y in xs)
    weave = f'<clipPath id="gw">{rects}</clipPath><g clip-path="url(#gw)">{sq}</g>'
    dot = f'<circle cx="60" cy="60" r="7" fill="{c2}"/>'
    return sq + sq2 + weave + dot


def mark_equal_e(c1, c2):
    """Monogram version of the Equal-E: three equal bars, the middle one gold."""
    bw, bh, g = 64, 13, 10
    x = (120 - bw) / 2
    y0 = 60 - (3 * bh + 2 * g) / 2
    return (f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="2" fill="{c1}"/>'
            f'<rect x="{x}" y="{y0 + bh + g}" width="{bw}" height="{bh}" rx="2" fill="{c2}"/>'
            f'<rect x="{x}" y="{y0 + 2 * (bh + g)}" width="{bw}" height="{bh}" rx="2" fill="{c1}"/>')


# ---------------------------------------------------------------------------
# LOCKUPS (wordmarks)
# ---------------------------------------------------------------------------
def sub_line(font, color, x, y, width, size, wght=600, tracking=0.38):
    """"ADVISORY" with fixed, generous tracking (not stretched to fill the width)."""
    d, w = text(font, wght, "ADVISORY", size, tracking=tracking)
    return P(d, color, x, y)


def lockup_equilibrium(dark):
    """MEZ + split-circle O + N: the mark lives inside the name."""
    c = WHITE if dark else NAVY
    sub = GOLD_LIGHT if dark else GOLD_DEEP
    f, wt, size, tr = "Outfit.ttf", 500, 84, 0.16
    capH = cap_height(f, wt, size)
    d1, w1 = text(f, wt, "MEZ", size, tracking=tr)
    d2, w2 = text(f, wt, "N", size)
    o = capH * 1.04                      # O diameter slightly above cap height (optical overshoot)
    sp = tr * size
    x, y = 10, 76
    ox = x + w1 + sp
    s = o / 76
    oy = y - capH / 2 - 60 * s
    body = (P(d1, c, x, y)
            + f'<g transform="translate({ox - 22 * s:.2f} {oy:.2f}) scale({s:.4f})">{mark_equilibrium(c, GOLD, beam=False)}</g>'
            + P(d2, c, ox + o + sp, y))
    total = ox + o + sp + w2 - x
    body += sub_line("Outfit.ttf", sub, x + 3, y + 34, total - 4, 15, 500)
    return svg(total + 20, 122, body)


def lockup_measure(dark):
    c = WHITE if dark else NAVY
    sub = GOLD_LIGHT if dark else GOLD_DEEP
    f, wt, size = "Sora.ttf", 600, 68
    d, w = text(f, wt, "mezon", size, tracking=-0.01)
    capH = cap_height(f, wt, size)
    m = 110 / 120
    body = f'<g transform="translate(0 4) scale({m:.4f})">{mark_measure(c, GOLD)}</g>'
    tx = 128
    body += P(d, c, tx, 80)
    body += sub_line("Sora.ttf", sub, tx + 3, 106, w - 6, 13.5, 500)
    return svg(tx + w + 14, 124, body)


def lockup_girih(dark):
    c = WHITE if dark else NAVY
    sub = GOLD_LIGHT if dark else GOLD_DEEP
    f, wt, size = "Manrope.ttf", 700, 62
    d, w = text(f, wt, "MEZON", size, tracking=0.2)
    m = 112 / 120
    body = f'<g transform="translate(0 4) scale({m:.4f})">{mark_girih(c, GOLD)}</g>'
    tx = 134
    body += P(d, c, tx, 76)
    body += sub_line("Manrope.ttf", sub, tx + 2, 104, w - 4, 14, 600)
    return svg(tx + w + 14, 124, body)


def lockup_equal_e(dark):
    """M + custom three-bar E + ZON."""
    c = WHITE if dark else NAVY
    sub = GOLD_LIGHT if dark else GOLD_DEEP
    f, wt, size, tr = "Outfit.ttf", 600, 92, 0.12
    capH = cap_height(f, wt, size)
    dM, wM = text(f, wt, "M", size)
    dZ, wZ = text(f, wt, "ZON", size, tracking=tr)
    x, y = 10, 80
    sp = tr * size
    bar_h = capH * 0.2
    gap = (capH - 3 * bar_h) / 2
    ew = size * 0.5
    ex = x + wM + sp
    bars = ""
    for i in range(3):
        col = GOLD if i == 1 else c
        bars += f'<rect x="{ex:.2f}" y="{y - capH + i * (bar_h + gap):.2f}" width="{ew:.2f}" height="{bar_h:.2f}" fill="{col}"/>'
    zx = ex + ew + sp
    total = zx + wZ - x
    body = P(dM, c, x, y) + bars + P(dZ, c, zx, y)
    body += sub_line("Outfit.ttf", sub, x + 3, y + 36, total - 4, 15, 500)
    return svg(total + 20, 128, body)


def icon_tile(mark_fn, size=512, scale=0.62, rx=0.22, bg=NAVY, c1=WHITE, c2=GOLD_LIGHT):
    s = size * scale / 120
    off = (size - 120 * s) / 2
    return svg(size, size, f'<rect width="{size}" height="{size}" rx="{size * rx:.1f}" fill="{bg}"/>'
               f'<g transform="translate({off:.2f} {off:.2f}) scale({s:.4f})">{mark_fn(c1, c2)}</g>')


CONCEPTS = [
    dict(key="A", slug="equilibrium", title="Equilibrium", mark=mark_equilibrium, lockup=lockup_equilibrium,
         font="Outfit", idea="A circle split into two exactly equal halves, navy and gold, resting on the line of balance. In the name, the mark becomes the O of MEZON, so the logo and the word are one.",
         meaning="Mezon = balance. Two sides of every deal (investor and state, profit and compliance) held in perfect equilibrium.",
         pros=["Instantly ownable and very simple: works as a 16px favicon", "The mark lives inside the name (a professional studio technique)", "Calm, modern, premium: fits finance and law"],
         cons=["Simple geometry needs a trademark check for similar circle marks"], rec=True),
    dict(key="B", slug="measure", title="Measure", mark=mark_measure, lockup=lockup_measure,
         font="Sora", idea="Five bars of measured heights form an M. It reads at once as a chart, a ruler and the letter. The gold point above marks the standard.",
         meaning="Mezon = measure and criterion. Data-driven, precise and quantified: tax and audit done to the standard.",
         pros=["Feels modern and analytical, like a fintech", "Clear M monogram at every size", "Lowercase name feels approachable"],
         cons=["Bar-chart marks are popular with finance startups", "Less heritage and Gulf resonance"], rec=False),
    dict(key="C", slug="girih", title="Girih", mark=mark_girih, lockup=lockup_girih,
         font="Manrope", idea="The eight-point star of Samarkand and Bukhara tilework, rebuilt from two interlocking squares (navy and gold) woven over and under, with a balance point at the centre.",
         meaning="Two standards (local and international, Uzbek and IFRS) interlocked in balance. Heritage made modern.",
         pros=["Strongest cultural resonance for Gulf and Central Asian clients", "Distinctive woven detail"],
         cons=["Eight-point stars are widely used; the weave must stay crisp", "Busier than A at tiny sizes"], rec=False),
    dict(key="D", slug="equal-e", title="Equal-E", mark=mark_equal_e, lockup=lockup_equal_e,
         font="Outfit", idea="A pure wordmark: the E is drawn as three equal bars with the middle one gold. That's the sign of equality and a fair standard, hidden in plain sight.",
         meaning="Mezon = fairness and equal measure. A clever, quiet detail that people notice and remember.",
         pros=["Pure typographic logo, the most \"corporate premium\" option", "Memorable twist without any icon"],
         cons=["Icon (three bars) is abstract on its own", "Some may read the E as the Greek letter Ξ"], rec=False),
]


def write_files():
    for c in CONCEPTS:
        base = f'{c["key"]}-{c["slug"]}'
        (OUT / f"{base}-logo.svg").write_text(c["lockup"](False))
        (OUT / f"{base}-logo-white.svg").write_text(c["lockup"](True))
        (OUT / f"{base}-icon.svg").write_text(icon_tile(c["mark"]))
        (OUT / f"{base}-mark.svg").write_text(svg(120, 120, c["mark"](NAVY, GOLD)))


def page():
    cards = []
    for c in CONCEPTS:
        b = f'{c["key"]}-{c["slug"]}'
        cards.append(f'''
<section class="concept{' rec' if c['rec'] else ''}" id="{b}">
  <div class="head"><span class="key">{c['key']}</span><h2>{c['title']}</h2>{'<span class="badge">Recommended</span>' if c['rec'] else ''}<span class="font">Typeface: {c['font']}</span></div>
  <p class="idea">{c['idea']}</p>
  <div class="pair"><div class="lt"><img src="{b}-logo.svg" alt=""></div><div class="dk"><img src="{b}-logo-white.svg" alt=""></div></div>
  <div class="use">
    <div class="bc front"><img src="{b}-logo-white.svg" alt=""></div>
    <div class="bc back"><img src="{b}-mark.svg" class="bm" alt=""><p><strong>Ziyodillo Mirzamoydinov</strong>Founder &amp; Managing Partner<br>+998 99 200 23 51 · t.me/Ziyodillo_84<br>mezonadvisory.com</p></div>
    <div class="side">
      <div class="ig"><div class="av"><img src="{b}-icon.svg" alt=""></div><div><b>mezon.advisory</b><small>Mezon Advisory · Tashkent</small></div></div>
      <div class="tab"><img src="{b}-icon.svg" width="16" height="16" alt=""><span>Mezon Advisory | Tax &amp; Audit</span></div>
      <div class="sizes"><img src="{b}-icon.svg" width="64" alt=""><img src="{b}-icon.svg" width="40" alt=""><img src="{b}-icon.svg" width="24" alt=""><img src="{b}-icon.svg" width="16" alt=""></div>
    </div>
  </div>
  <div class="site"><div class="bar"><img src="{b}-logo.svg" alt=""><span>Services · TIFC · Tools · FAQ</span><em>Book a call</em></div><div class="hero"></div></div>
  <div class="notes"><div><h3>Meaning</h3><p>{c['meaning']}</p></div>
    <div><h3>Strengths</h3><ul class="pros">{''.join(f'<li>{p}</li>' for p in c['pros'])}</ul></div>
    <div><h3>Watch-outs</h3><ul class="cons">{''.join(f'<li>{p}</li>' for p in c['cons'])}</ul></div></div>
</section>''')
    overview = "".join(f'<a href="#{c["key"]}-{c["slug"]}"><img src="{c["key"]}-{c["slug"]}-icon.svg" alt=""><span><b>{c["key"]} · {c["title"]}</b>{"<em>Recommended</em>" if c["rec"] else ""}</span></a>' for c in CONCEPTS)
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mezon Logo Concepts</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--navy:{NAVY};--gold:{GOLD};--line:#E2E8F0;--muted:{MUTED};--bg:#F1F5F9}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Plus Jakarta Sans',system-ui,sans-serif;background:var(--bg);color:var(--navy);padding:40px 16px 80px;line-height:1.55}}
.wrap{{max-width:1080px;margin:0 auto}}
h1{{font-size:2rem;font-weight:800}}
.lead{{color:var(--muted);max-width:780px;margin:.4rem 0 1.4rem}}
.ov{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:28px}}
.ov a{{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px;color:inherit;text-decoration:none}}
.ov a:hover{{border-color:var(--gold)}}
.ov img{{width:44px;height:44px}}
.ov em{{display:block;font-style:normal;font-size:.68rem;font-weight:800;color:#92400E}}
.concept{{background:#fff;border:1px solid var(--line);border-radius:20px;padding:28px;margin-bottom:28px;scroll-margin-top:12px}}
.concept.rec{{border:2px solid var(--gold)}}
.head{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:6px}}
.key{{width:34px;height:34px;border-radius:10px;background:var(--navy);color:#fff;display:grid;place-items:center;font-weight:800}}
.head h2{{font-size:1.45rem;font-weight:800}}
.badge{{font-size:.7rem;font-weight:800;color:#92400E;background:#FEF3C7;border:1px solid #FCD34D;border-radius:99px;padding:2px 10px}}
.font{{margin-inline-start:auto;font-size:.75rem;color:var(--muted)}}
.idea{{color:#334155;margin-bottom:18px;max-width:860px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px}}
.pair div{{border-radius:14px;display:flex;align-items:center;justify-content:center;padding:36px 28px;min-height:180px;border:1px solid var(--line)}}
.pair .dk{{background:var(--navy);border-color:var(--navy)}}
.pair img{{max-width:100%;max-height:120px}}
.use{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;align-items:start;margin-bottom:14px}}
.bc{{aspect-ratio:85/55;border-radius:10px;box-shadow:0 16px 34px -14px rgba(15,23,42,.45);display:flex;align-items:center;justify-content:center;padding:9%;min-width:0}}
.bc.front{{background:var(--navy)}}
.bc.front img{{max-width:82%;max-height:62%}}
.bc.back{{background:#FBFAF7;flex-direction:column;align-items:flex-start;justify-content:space-between;padding:8%}}
.bc .bm{{width:30px;height:30px}}
.bc p{{font-size:.66rem;color:#334155;line-height:1.55}}
.bc strong{{display:block;font-size:.82rem;color:var(--navy)}}
.side{{display:flex;flex-direction:column;gap:10px;min-width:0}}
.ig{{display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:12px;padding:10px}}
.av{{width:58px;height:58px;border-radius:50%;padding:2.5px;background:linear-gradient(45deg,#F59E0B,#E1306C,#7C3AED);flex-shrink:0}}
.av img{{width:100%;height:100%;border-radius:50%;border:2.5px solid #fff;display:block}}
.ig b{{display:block;font-size:.85rem}}.ig small{{color:var(--muted);font-size:.72rem}}
.tab{{display:flex;align-items:center;gap:8px;background:#E2E8F0;border-radius:10px 10px 0 0;padding:8px 12px;font-size:.75rem;width:max-content;max-width:100%}}
.sizes{{display:flex;align-items:flex-end;gap:12px}}
.site{{border:1px solid var(--line);border-radius:12px;overflow:hidden;margin-bottom:16px}}
.site .bar{{display:flex;align-items:center;gap:20px;padding:14px 20px;background:#fff;border-bottom:1px solid var(--line)}}
.site .bar img{{height:46px}}
.site .bar span{{font-size:.78rem;color:var(--muted);margin-inline-start:auto}}
.site .bar em{{font-style:normal;font-size:.75rem;font-weight:700;color:#fff;background:#1E40AF;border-radius:8px;padding:7px 12px}}
.site .hero{{height:56px;background:linear-gradient(90deg,#EFF6FF,#F8FAFC)}}
.notes{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;font-size:.88rem}}
.notes h3{{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}}
.notes ul{{padding-inline-start:18px}}
.pros li::marker{{color:#059669}}.cons li::marker{{color:#DC2626}}
@media(max-width:820px){{.ov{{grid-template-columns:1fr 1fr}}.pair,.use,.notes{{grid-template-columns:1fr}}.site .bar span{{display:none}}}}
</style></head>
<body><div class="wrap">
<h1>Mezon Advisory: Logo Concepts</h1>
<p class="lead"><b>Mezon</b> (Мезон · ميزان) means balance, standard and measure. Four modern directions, each built on that meaning rather than a literal set of scales, and each shown in real use. Lettering is converted to shapes in every file. Domain <b>mezonadvisory.com</b> was available when checked on 12 Oct 2026.</p>
<div class="ov">{overview}</div>
{''.join(cards)}
</div></body></html>'''
    (OUT / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    write_files()
    page()
    print("Wrote concepts to", OUT)

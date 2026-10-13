#!/usr/bin/env python3
"""Generates brand/concepts.html and the *-icon.svg / *-mark.svg logo files.

Run:  python3 brand/make_concepts.py
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent
GOLD = "#D4AF37"
NAVY = "#0F172A"
CHECKED = "2 Oct 2026"


def star(cx, cy, R, r, n, rot=-90):
    pts = []
    for i in range(2 * n):
        a = math.radians(rot + i * 180 / n)
        rad = R if i % 2 == 0 else r
        pts.append(f"{cx + rad * math.cos(a):.2f},{cy + rad * math.sin(a):.2f}")
    return " ".join(pts)


# Logo symbols, drawn in a 120x120 box using currentColor.
MARKS = {
    "karvon": f'''
  <path d="M30 108 V56 C30 36 44 24 60 14 C76 24 90 36 90 56 V108" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>
  <path d="M18 108 H102" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>
  <path d="M46 98 C46 84 74 84 74 70 C74 58 60 58 60 46" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linecap="round" stroke-dasharray="0.1 9"/>
  <polygon points="{star(60, 34, 9, 2.6, 4)}" fill="currentColor"/>''',
    "ziyo": f'''
  <polygon points="{star(60, 60, 46, 46 * 0.7654, 8)}" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round"/>
  <circle cx="60" cy="60" r="22" fill="none" stroke="currentColor" stroke-width="2.5" opacity=".55"/>
  <polygon points="{star(60, 60, 15, 6, 8)}" fill="currentColor"/>''',
    "sarbon": f'''
  <circle cx="60" cy="60" r="44" fill="none" stroke="currentColor" stroke-width="4"/>
  <polygon points="{star(60, 60, 30, 6, 4, -45)}" fill="currentColor" opacity=".45"/>
  <polygon points="{star(60, 60, 52, 9, 4)}" fill="currentColor"/>''',
    "mezon": f'''
  <polygon points="{star(60, 16, 7, 2.8, 8)}" fill="currentColor"/>
  <path d="M60 25 V96 M42 100 H78 M20 34 H100" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>
  <path d="M27 34 L15 64 M27 34 L39 64 M93 34 L81 64 M93 34 L105 64" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
  <path d="M11 64 Q27 82 43 64 Z M77 64 Q93 82 109 64 Z" fill="currentColor"/>''',
    # Two pointed arches forming an "M": the learned scribe's monogram
    "mirzo": f'''
  <path d="M20 104 V58 C20 40 30 30 40 22 C50 30 60 40 60 58 V104" fill="none" stroke="currentColor" stroke-width="5.5" stroke-linejoin="round"/>
  <path d="M60 58 C60 40 70 30 80 22 C90 30 100 40 100 58 V104" fill="none" stroke="currentColor" stroke-width="5.5" stroke-linejoin="round"/>
  <path d="M12 104 H108" stroke="currentColor" stroke-width="5.5" stroke-linecap="round"/>
  <polygon points="{star(60, 82, 10, 4, 8)}" fill="currentColor"/>''',
    # Reed-pen nib
    "qalam": '''
  <g transform="rotate(35 60 60)">
    <path d="M60 110 L38 66 C36 60 40 54 44 50 V18 H76 V50 C80 54 84 60 82 66 Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>
    <path d="M60 108 V74" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
    <circle cx="60" cy="68" r="5" fill="currentColor"/>
    <path d="M44 34 H76" stroke="currentColor" stroke-width="4"/>
  </g>''',
    # The three madrasahs of Registan Square
    "registan": f'''
  <path d="M44 104 V56 C44 40 52 32 60 24 C68 32 76 40 76 56 V104" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>
  <path d="M12 104 V70 C12 58 18 52 25 46 C32 52 38 58 38 70 V104" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round"/>
  <path d="M82 104 V70 C82 58 88 52 95 46 C102 52 108 58 108 70 V104" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round"/>
  <path d="M6 108 H114" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>
  <polygon points="{star(60, 12, 7, 2.6, 8)}" fill="currentColor"/>''',
    # Rising sun over the horizon: fortune and growth
    "iqbol": '''
  <path d="M28 78 A32 32 0 0 1 92 78" fill="none" stroke="currentColor" stroke-width="5"/>
  <path d="M14 78 H106" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>
  <path d="M60 18 V32 M30 30 L38 40 M90 30 L82 40 M14 54 L26 58 M106 54 L94 58" stroke="currentColor" stroke-width="4.5" stroke-linecap="round"/>
  <path d="M30 92 H90 M44 104 H76" stroke="currentColor" stroke-width="4" stroke-linecap="round" opacity=".6"/>
  <path d="M46 70 L60 56 L74 70" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>''',
    # The "gold-scattering" river
    "zarafshon": f'''
  <path d="M10 58 C24 46 36 46 50 58 S76 70 90 58 S106 50 110 52" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>
  <path d="M10 78 C24 66 36 66 50 78 S76 90 90 78 S106 70 110 72" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>
  <path d="M10 98 C24 86 36 86 50 98 S76 110 90 98 S106 90 110 92" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" opacity=".55"/>
  <polygon points="{star(60, 26, 13, 3.5, 4)}" fill="currentColor"/>
  <polygon points="{star(88, 30, 6, 1.8, 4)}" fill="currentColor"/>
  <polygon points="{star(32, 34, 5, 1.6, 4)}" fill="currentColor"/>''',
    # Ulugh Beg's observatory sextant arc
    "ulugh": f'''
  <path d="M18 104 A86 86 0 0 1 104 18" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>
  <path d="M18 104 L104 18" stroke="currentColor" stroke-width="2.5" opacity=".5"/>
  <path d="M18 104 H104" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>
  {"".join(f'<path d="M{18 + 86 * math.cos(math.radians(a)) + 0:.1f} {104 - 86 * math.sin(math.radians(a)):.1f} L{18 + 76 * math.cos(math.radians(a)):.1f} {104 - 76 * math.sin(math.radians(a)):.1f}" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>' for a in range(10, 90, 10))}
  <polygon points="{star(78, 50, 11, 3.2, 4)}" fill="currentColor"/>''',
}

CONCEPTS = [
    # ---- Round 2 ----
    dict(key="qalam", name="QALAM", suffix="ADVISORY", domain="qalamadvisory.com", round=2,
         scripts=("Калам", "قلم", "Qalam"),
         meaning='"Pen" in Arabic, Uzbek and Persian: the instrument of knowledge, contracts and accounts. Honoured in the Gulf (Surah al-Qalam).',
         tagline="Precision in every account", mark_desc="A reed-pen nib, the tool of the scribe and the accountant.",
         pros=["Ideal for audit, tax and legal work: the pen that writes the accounts", "Instantly understood and respected by Arabic speakers", "Short, elegant, easy to say", ".com available"],
         cons=['Some edtech apps use "Qalam"', "Russian speakers know it less (may spell it 'Kalam')"], rec=True),
    dict(key="mirzo", name="MIRZO", suffix="PARTNERS", domain="mirzopartners.com", round=2,
         scripts=("Мирзо", "ميرزا", "Mirzo"),
         meaning='"Mirza / Mirzo": the learned scribe and adviser to rulers (as in Mirzo Ulugbek). It is also the first part of your surname, Mirzamoydinov.',
         tagline="Trusted counsel since the Silk Road", mark_desc='Two Samarkand arches forming an "M", with an eight-point star at the centre.',
         pros=["Personal yet professional: grows naturally from your surname", "Known across Russian, Persian, Arabic and Uzbek culture", "Historic meaning matches the adviser role", ".com available"],
         cons=['"Mirzo Ulugbek" is a Tashkent district and university name', "Less obviously a finance brand"], rec=False),
    dict(key="registan", name="REGISTAN", suffix="PARTNERS", domain="registanpartners.com", round=2,
         scripts=("Регистан", "ريجستان", "Registon"),
         meaning="Samarkand's world-famous square of three madrasahs (UNESCO), the best-known symbol of Uzbekistan.",
         tagline="Built on Uzbekistan's foundations", mark_desc="The three portals of Registan Square.",
         pros=["Recognised worldwide as Uzbekistan's icon", "Signals strength, heritage and permanence", ".com available"],
         cons=["Place names are hard to trademark exclusively", "Widely used by restaurants and tour agencies"], rec=False),
    dict(key="iqbol", name="IQBOL", suffix="ADVISORY", domain="iqboladvisory.com", round=2,
         scripts=("Икбол", "إقبال", "Iqbol"),
         meaning='"Good fortune, success, prosperity" in Uzbek, from Arabic إقبال (iqbāl).',
         tagline="Prosperity, well structured", mark_desc="A rising sun over the horizon with an upward chevron for growth.",
         pros=["Very positive meaning in Uzbek and Arabic", "Short and memorable", ".com available (also iqbolcapital.com)"],
         cons=["Common first name in Uzbekistan", "English speakers won't know the meaning"], rec=False),
    dict(key="zarafshon", name="ZARAFSHON", suffix="ADVISORY", domain="zarafshonadvisory.com", round=2,
         scripts=("Зарафшан", "زرافشان", "Zarafshon"),
         meaning='"Gold-scattering" in Persian: the river that brought wealth to Samarkand and Bukhara.',
         tagline="Where capital flows", mark_desc="Flowing river waves with scattered gold stars.",
         pros=["Beautiful wealth story: capital flowing into the region", "Familiar to Russian and Central Asian audiences", ".com available (also zarafshoncapital.com)"],
         cons=["Long; harder to spell for English speakers", "Also a city and gold-mining region"], rec=False),
    dict(key="ulugh", name="ULUGH", suffix="ADVISORY", domain="ulughadvisory.com", round=2,
         scripts=("Улуг", "ألغ", "Ulug'"),
         meaning='"Great" in Old Turkic, as in Ulugh Beg, the Samarkand astronomer famous for precise calculation.',
         tagline="Calculated with precision", mark_desc="The arc of Ulugh Beg's observatory sextant, with a guiding star.",
         pros=["Precision and scholarship: right for audit and tax", "Strong heritage recognition in Russian and Central Asian markets", ".com available"],
         cons=["Arabic speakers know Ulugh Beg less", "Spelling varies (Ulugh / Ulug' / Ulug)"], rec=False),
    # ---- Round 1 ----
    dict(key="karvon", name="KARVON", suffix="ADVISORY", domain="karvonadvisory.com", round=1,
         scripts=("Карвон", "كاروان", "Karvon"),
         meaning='Uzbek for "caravan": the Silk Road convoys that safely carried goods and capital between Asia, Arabia and Europe.',
         tagline="Your route into Uzbekistan", mark_desc="Registan-style arch portal with a caravan route leading to a guiding star.",
         pros=["Story fits a cross-border business", 'Russian, Arabic, Uzbek and English speakers understand "caravan"', "Distinctive in finance", ".com available"],
         cons=["Not personal; brand awareness has to be built"], rec=True),
    dict(key="ziyo", name="ZIYO", suffix="PARTNERS", domain="ziyopartners.com", round=1,
         scripts=("Зиё", "ضياء", "Ziyo"),
         meaning='"Light / knowledge" in Uzbek, from Arabic ضياء. It is also the root of your own name, Ziyodillo.',
         tagline="Clarity for capital", mark_desc="Central Asian eight-point girih star radiating light.",
         pros=["Personal: links the firm to you", "Arabic speakers instantly recognise ضياء", ".com available"],
         cons=['"Ziyo" is common in Uzbek media and education brands', 'English speakers may be unsure how to say it'], rec=False),
    dict(key="sarbon", name="SARBON", suffix="ADVISORY", domain="sarbonadvisory.com", round=1,
         scripts=("Сарбон", "ساربان", "Sarbon"),
         meaning='"Caravan leader" in Uzbek: the person trusted to lead the convoy safely.',
         tagline="Guiding capital along the Silk Road", mark_desc="Compass star.",
         pros=["Positions you as the trusted guide", "Easy to say in English and Russian", ".com available"],
         cons=["Less familiar to Gulf Arabic speakers", "Compass marks are common"], rec=False),
    dict(key="mezon", name="MEZON", suffix="ADVISORY", domain="mezonadvisory.com", round=1,
         scripts=("Мезон", "ميزان", "Mezon"),
         meaning="Uzbek form of Arabic ميزان: balance, scales, fairness. Keeps the meaning of your current name.",
         tagline="Balance. Standards. Trust.", mark_desc="Scales of balance topped by an eight-point star.",
         pros=['Keeps the "Mizan" meaning', "Strong Islamic-finance resonance", ".com available"],
         cons=['In Russian "мезон" is a physics term', "Scales marks are very common"], rec=False),
]

RULED_OUT = [
    ("Mizan Advisory / Partners", "mizanadvisory.com, mizan-advisory.com, mizanpartners.com already registered"),
    ("Daftar (\"ledger\")", "daftaradvisory.com and daftarpartners.com taken"),
    ("Baraka (\"blessing\")", "barakaadvisory.com taken; many Baraka banks"),
    ("Amin (\"trustworthy\")", "aminadvisory.com taken"),
    ("Amanat (\"trust\")", "conflicts with Amanat Holdings (UAE-listed)"),
    ("Turon", "conflicts with Turonbank (Uzbekistan)"),
    ("Humo", "conflicts with HUMO national payment card"),
]


def mark_svg(key, color, size, bg=None, rx=24):
    tile = f'<rect width="120" height="120" rx="{rx}" fill="{bg}"/>' if bg else ""
    inner = MARKS[key]
    if bg:
        inner = f'<g transform="translate(14 14) scale(.7667)">{inner}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="{size}" height="{size}" '
            f'style="color:{color}" role="img" aria-label="{key} logo">{tile}{inner}</svg>')


def write_files():
    for c in CONCEPTS:
        k = c["key"]
        (OUT / f"{k}-icon.svg").write_text(mark_svg(k, GOLD, 512, NAVY).replace("currentColor", GOLD))
        (OUT / f"{k}-mark.svg").write_text(mark_svg(k, GOLD, 512).replace("currentColor", GOLD))


def lockup(c, theme):
    dark = theme == "dark"
    fg = "#FFFFFF" if dark else NAVY
    size = "1.9rem" if len(c["name"]) > 7 else "2.3rem"
    return f'''<div class="lockup {theme}">
      {mark_svg(c["key"], GOLD, 76, None if dark else NAVY)}
      <div class="wm"><span class="wm-name" style="color:{fg};font-size:{size}">{c["name"]}</span><span class="wm-sub">{c["suffix"]} · TASHKENT</span></div>
    </div>'''


def card(i, c):
    handle = f'{c["key"]}.{c["suffix"].lower()}'
    title = f'{c["name"].title()} {c["suffix"].title()}'
    return f'''
  <section class="card{' rec' if c['rec'] else ''}" id="{c['key']}">
    <header class="card-head">
      <div><span class="num">Option {i}</span>{'<span class="badge">Top pick</span>' if c['rec'] else ''}
        <h2>{title}</h2><p class="tag">“{c['tagline']}”</p></div>
      <div class="scripts"><span lang="ru">{c['scripts'][0]}</span><span lang="ar" dir="rtl">{c['scripts'][1]}</span><span>{c['scripts'][2]}</span></div>
    </header>
    <div class="showcase">{lockup(c, 'light')}{lockup(c, 'dark')}</div>
    <div class="sizes">
      <div class="size-group">{mark_svg(c['key'], GOLD, 96, NAVY)}<span>App / Instagram</span></div>
      <div class="size-group">{mark_svg(c['key'], GOLD, 48, NAVY, 28)}<span>48px</span></div>
      <div class="size-group">{mark_svg(c['key'], GOLD, 32, NAVY, 28)}<span>Favicon 32</span></div>
      <div class="size-group">{mark_svg(c['key'], GOLD, 16, NAVY, 28)}<span>16</span></div>
      <div class="size-group">{mark_svg(c['key'], NAVY, 64)}<span>One-colour</span></div>
      <div class="ig"><div class="ig-avatar">{mark_svg(c['key'], GOLD, 58, NAVY, 60)}</div><div><strong>{handle}</strong><span>{title} · Tashkent</span></div></div>
    </div>
    <div class="details">
      <div><h3>Meaning</h3><p>{c['meaning']}</p><h3>Logo idea</h3><p>{c['mark_desc']}</p>
        <p class="domain">🌐 {c['domain']} · <b>available</b> (checked {CHECKED})</p></div>
      <div><h3>Strengths</h3><ul class="pros">{''.join(f'<li>{p}</li>' for p in c['pros'])}</ul>
        <h3>Watch-outs</h3><ul class="cons">{''.join(f'<li>{p}</li>' for p in c['cons'])}</ul></div>
    </div>
  </section>'''


def overview():
    rows = []
    for i, c in enumerate(CONCEPTS, 1):
        rows.append(f'''<a class="ov" href="#{c['key']}">{mark_svg(c['key'], GOLD, 44, NAVY, 28)}
          <span><strong>{c['name'].title()} {c['suffix'].title()}</strong><small>{c['scripts'][0]} · <span dir="rtl" lang="ar">{c['scripts'][1]}</span></small></span>
          {'<em>Top pick</em>' if c['rec'] else ''}</a>''')
    return "".join(rows)


def build_page():
    round2 = [c for c in CONCEPTS if c["round"] == 2]
    round1 = [c for c in CONCEPTS if c["round"] == 1]
    cards2 = "".join(card(i, c) for i, c in enumerate(round2, 5))
    cards1 = "".join(card(i, c) for i, c in enumerate(round1, 1))
    ruled = "".join(f"<li><b>{n}</b>: {why}</li>" for n, why in RULED_OUT)
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Brand Name &amp; Logo Concepts</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Noto+Kufi+Arabic:wght@600&display=swap" rel="stylesheet">
<style>
:root{{--navy:{NAVY};--gold:{GOLD};--bg:#F1F5F9;--card:#fff;--text:#0F172A;--muted:#64748B;--line:#E2E8F0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Plus Jakarta Sans',system-ui,sans-serif;background:var(--bg);color:var(--text);padding:40px 16px 80px}}
.wrap{{max-width:1080px;margin:0 auto}}
.intro h1{{font-size:2rem;font-weight:800;margin-bottom:.5rem}}
.intro p{{color:var(--muted);max-width:760px;line-height:1.6;margin-bottom:1.5rem}}
.overview{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin-bottom:1.5rem}}
.ov{{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px 12px;text-decoration:none;color:inherit}}
.ov:hover{{border-color:var(--gold)}}
.ov svg{{flex-shrink:0}}
.ov strong{{display:block;font-size:.92rem}}.ov small{{color:var(--muted);font-size:.78rem}}
.ov em{{margin-inline-start:auto;font-style:normal;font-size:.65rem;font-weight:800;color:#92400E;background:#FEF3C7;border-radius:99px;padding:2px 8px;white-space:nowrap}}
.ruled{{background:#fff;border:1px dashed var(--line);border-radius:14px;padding:14px 18px;margin-bottom:2.5rem;font-size:.85rem;color:var(--muted)}}
.ruled ul{{padding-inline-start:18px;margin-top:6px;line-height:1.7}}
h2.round{{font-size:1.1rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:2rem 0 1rem}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:28px;margin-bottom:28px;box-shadow:0 4px 18px rgba(15,23,42,.05);scroll-margin-top:16px}}
.card.rec{{border:2px solid var(--gold)}}
.card-head{{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap;margin-bottom:22px}}
.num{{font-size:.75rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}}
.badge{{margin-inline-start:8px;font-size:.7rem;font-weight:800;color:#92400E;background:#FEF3C7;border:1px solid #FCD34D;border-radius:99px;padding:2px 10px}}
.card-head h2{{font-size:1.6rem;font-weight:800;margin-top:4px}}
.tag{{color:var(--muted);font-style:italic}}
.scripts{{display:flex;gap:10px;flex-wrap:wrap}}
.scripts span{{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:6px 12px;font-weight:700}}
[lang=ar]{{font-family:'Noto Kufi Arabic',sans-serif}}
.showcase{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px}}
.lockup{{display:flex;align-items:center;gap:18px;padding:30px 26px;border-radius:16px;border:1px solid var(--line);min-width:0;overflow:hidden}}
.lockup.light{{background:#FFFFFF}}
.lockup.dark{{background:var(--navy);border-color:var(--navy)}}
.lockup svg{{flex-shrink:0}}
.wm{{display:flex;flex-direction:column;min-width:0}}
.wm-name{{font-family:'Cinzel',serif;font-weight:700;letter-spacing:.14em;line-height:1}}
.wm-sub{{font-size:.68rem;font-weight:700;letter-spacing:.24em;white-space:nowrap;color:var(--gold);margin-top:8px}}
.sizes{{display:flex;align-items:flex-end;gap:22px;flex-wrap:wrap;padding:18px;background:var(--bg);border-radius:14px;margin-bottom:20px}}
.size-group{{display:flex;flex-direction:column;align-items:center;gap:6px}}
.size-group span{{font-size:.68rem;color:var(--muted);font-weight:600}}
.ig{{display:flex;align-items:center;gap:10px;margin-inline-start:auto;background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px 14px}}
.ig-avatar{{border-radius:50%;padding:3px;background:linear-gradient(45deg,#F59E0B,#E1306C,#7C3AED)}}
.ig-avatar svg{{display:block;border-radius:50%;border:2px solid #fff}}
.ig strong{{display:block;font-size:.85rem}}.ig span{{font-size:.72rem;color:var(--muted)}}
.details{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}
.details h3{{font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:10px 0 6px}}
.details p,.details li{{font-size:.9rem;line-height:1.55;color:#334155}}
.details ul{{padding-inline-start:18px}}
.pros li::marker{{color:#059669}}.cons li::marker{{color:#DC2626}}
.domain{{margin-top:10px;font-weight:600}}
@media (max-width:760px){{.showcase,.details{{grid-template-columns:1fr}}.wm-name{{font-size:1.6rem!important}}.lockup{{padding:22px 16px}}.ig{{margin-inline-start:0}}}}
</style>
</head>
<body><div class="wrap">
  <div class="intro">
    <h1>Brand Name &amp; Logo Concepts</h1>
    <p>Ten options for investors from Russia, Central Asia and the Gulf, each easy to say in Russian, Arabic, Uzbek and English, with its .com domain free. "Mirzamoydinov &amp; Partners" stays as the legal name in the footer, contracts and documents. Click a name to jump to it.</p>
  </div>
  <div class="overview">{overview()}</div>
  <div class="ruled"><b>Checked and ruled out:</b><ul>{ruled}</ul></div>
  <h2 class="round">New options</h2>
  {cards2}
  <h2 class="round">First round</h2>
  {cards1}
</div></body></html>'''
    (OUT / "concepts.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    write_files()
    build_page()
    print(f"Wrote concepts.html and {len(CONCEPTS) * 2} SVG files")

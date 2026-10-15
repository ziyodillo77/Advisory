#!/usr/bin/env python3
"""
Mezon Advisory static site builder.

Takes the English source pages (index.html, privacy.html) and produces a
ready-to-upload website in ./dist with one folder per language:

    dist/index.html          English
    dist/ru/index.html       Russian
    dist/ar/index.html       Arabic (right-to-left)
    dist/uz/index.html       Uzbek

Translations live in i18n/<lang>.json:
    "html": English text exactly as it appears in the HTML -> translation
    "js":   strings used by app.js through t()             -> translation

Usage:
    python3 build.py              build ./dist
    python3 build.py --extract    list every translatable English string
    python3 build.py --check      build and fail if any string is untranslated

Edit SITE_URL and CONTACT below, then rebuild.
"""

import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
SITE_URL = "https://mezonadvisory.com"  # <-- your domain (no trailing slash)

# Company contact channels. Every link on the site is filled in from here.
# Leave a value empty ("") to hide that channel everywhere on the site.
CONTACT = {
    "telegram": "mezon_advisory",    # Telegram username, without @
    "instagram": "mezon.advisory",   # Instagram username, without @
    "whatsapp": "905349864297",      # WhatsApp Business number, digits only (+90 534 986 4297)
    "phone": "",                     # Phone as displayed, e.g. "+998 90 123 45 67"
    "email": "",                     # e.g. "info@mezonadvisory.com"
}

LANGS = {
    "en": {"dir": "ltr", "prefix": "", "og": "en_US"},
    "ru": {"dir": "ltr", "prefix": "ru/", "og": "ru_RU"},
    "ar": {"dir": "rtl", "prefix": "ar/", "og": "ar_AR"},
    "uz": {"dir": "ltr", "prefix": "uz/", "og": "uz_UZ"},
}

PAGES = ["index.html", "privacy.html"]

# Investor guides: guides/<slug>/<lang>.html, each starting with a metadata comment
# (title, description, tag, minutes, published, updated). Listed in display order.
GUIDES = [
    "register-company-uzbekistan",
    "tifc-tashkent-international-financial-centre",
    "uzbekistan-taxes-foreign-investors",
]
GUIDE_TEMPLATE = "guide.html"
STATIC = ["styles.css", "app.js", "404.html", "site.webmanifest", "assets"]

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
I18N_DIR = ROOT / "i18n"

TRANSLATABLE_ATTRS = ("placeholder", "aria-label", "title", "alt", "content")

# Strings that are the same in every language (brands, codes, numbers).
NO_TRANSLATE = {
    "Mezon Advisory", "EN", "RU", "UZ", "العربية",
    "USD / UZS", "EUR / UZS", "AED / UZS", "RUB / UZS", "—", "|",
    "Instagram", "WhatsApp", "Telegram",
    "UZS (Uzbek Som)", "$500,000", "25%", "30%", "$50k", "$1M", "$5M", "$10M+",
    "01", "02", "03", "04", "$150M+", "120+", "100%", "0%", "2076", "12+",
    "USD ($) [1 USD ≈ 11,809 UZS]", "contact@gulfcapital.ae",
    "$18,750", "$21,000", "$34,560", "$74,310", "$106,250", "$0", "$0 / year",
    "15%", "12%", "7.5%", "2040", "IT Park", "IT Park:", "IFRS", "$420k+", "$12M", "$45M",
}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def split_protected(src):
    """Split HTML into (is_protected, chunk) so <script>/<style> are never translated."""
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", src, flags=re.S | re.I)
    return [(bool(re.match(r"<(script|style)\b", p, re.I)), p) for p in parts]


def key_pattern(key):
    # Whitespace in a key matches any run of whitespace in the source.
    return r"\s+".join(re.escape(part) for part in key.split(" "))


def translate_html(src, mapping, used):
    keys = sorted(mapping, key=len, reverse=True)
    out = []
    for protected, chunk in split_protected(src):
        if protected:
            out.append(chunk)
            continue
        for key in keys:
            value = mapping[key]
            pat = key_pattern(key)
            # Text between tags
            text_re = re.compile(r"(>\s*)" + pat + r"(\s*<)")
            chunk, n1 = text_re.subn(lambda m: m.group(1) + value + m.group(2), chunk)
            # Attribute values
            attr_re = re.compile(r"(\b(?:%s)=\")%s(\")" % ("|".join(TRANSLATABLE_ATTRS), pat))
            safe_value = value.replace('"', "&quot;")
            chunk, n2 = attr_re.subn(lambda m: m.group(1) + safe_value + m.group(2), chunk)
            if n1 or n2:
                used.add(key)
        out.append(chunk)
    return "".join(out)


def extract_strings(src):
    # Work on raw source so entities like &amp; stay exactly as written.
    found = []
    for protected, chunk in split_protected(src):
        if protected:
            continue
        for m in re.finditer(r">([^<>]+)<", chunk):
            text = norm(m.group(1))
            if text and re.search(r"[A-Za-z]", text) and "{{" not in text:
                found.append(text)
        for m in re.finditer(r"\b(%s)=\"([^\"]*)\"" % "|".join(TRANSLATABLE_ATTRS), chunk):
            attr, val = m.group(1), norm(m.group(2))
            if not re.search(r"[A-Za-z]{2}", val):
                continue
            if attr == "content":
                tag_start = chunk.rfind("<", 0, m.start())
                tag = chunk[tag_start:chunk.find(">", m.end()) + 1]
                if not re.search(r'name="description"|property="og:(title|description)"', tag):
                    continue
            found.append(val)
    seen, unique = set(), []
    for s in found:
        if s not in seen and s not in NO_TRANSLATE:
            seen.add(s)
            unique.append(s)
    return unique


def page_url(lang, page):
    path = LANGS[lang]["prefix"] + ("" if page == "index.html" else page)
    return f"{SITE_URL}/{path}"


def page_path(lang, page):
    return "/" + LANGS[lang]["prefix"] + ("" if page == "index.html" else page)


def seo_block(lang, page):
    lines = [f'<link rel="canonical" href="{page_url(lang, page)}">']
    for code in LANGS:
        lines.append(f'<link rel="alternate" hreflang="{code}" href="{page_url(code, page)}">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{page_url("en", page)}">')
    lines.append(f'<meta property="og:url" content="{page_url(lang, page)}">')
    lines.append(f'<meta property="og:locale" content="{LANGS[lang]["og"]}">')
    for code in LANGS:
        if code != lang:
            lines.append(f'<meta property="og:locale:alternate" content="{LANGS[code]["og"]}">')
    lines.append(f'<meta property="og:image" content="{SITE_URL}/assets/og-image.png">')
    lines.append('<meta property="og:image:width" content="1200">')
    lines.append('<meta property="og:image:height" content="630">')
    lines.append(f'<meta name="twitter:image" content="{SITE_URL}/assets/og-image.png">')
    return "\n  ".join(lines)


def localize_links(src, lang, page):
    prefix = LANGS[lang]["prefix"]
    # Internal page links (not the language switcher, which carries hreflang)
    src = re.sub(r'href="/privacy\.html"', f'href="/{prefix}privacy.html"', src)
    src = re.sub(r'href="/"(?!\s+hreflang)', f'href="/{prefix}"', src)
    src = re.sub(r'href="/(guides/|#)', lambda m: f'href="/{prefix}{m.group(1)}', src)

    # Language switcher: point each language at the same page, mark current
    def lang_link(m):
        code = m.group(1)
        current = ' aria-current="page"' if code == lang else ""
        cls = "lang-btn active" if code == lang else "lang-btn"
        return f'<a class="{cls}" href="{page_path(code, page)}" hreflang="{code}"{current}'
    src = re.sub(r'<a class="lang-btn" href="[^"]*" hreflang="(\w+)"', lang_link, src)
    return src


def apply_contacts(src):
    """Fill {{TOKENS}} from CONTACT, hide empty channels, expose CONTACT to app.js."""
    c = CONTACT
    tokens = {
        "{{TELEGRAM}}": c["telegram"],
        "{{TELEGRAM_URL}}": f"https://t.me/{c['telegram']}" if c["telegram"] else "#",
        "{{INSTAGRAM}}": c["instagram"],
        "{{INSTAGRAM_URL}}": f"https://instagram.com/{c['instagram']}" if c["instagram"] else "#",
        "{{WHATSAPP_URL}}": f"https://wa.me/{c['whatsapp']}" if c["whatsapp"] else "#",
        "{{PHONE}}": c["phone"],
        "{{PHONE_URL}}": "tel:" + re.sub(r"[^\d+]", "", c["phone"]) if c["phone"] else "#",
        "{{EMAIL}}": c["email"],
    }
    for k, v in tokens.items():
        src = src.replace(k, v)
    same_as = [u for u in (tokens["{{INSTAGRAM_URL}}"], tokens["{{TELEGRAM_URL}}"]) if u != "#"]
    src = src.replace('"sameAs": "{{SAME_AS}}"', '"sameAs": ' + json.dumps(same_as))
    hidden = [f"no-{k}" for k in ("telegram", "instagram", "whatsapp", "phone", "email") if not c[k]]
    if hidden:
        src = re.sub(r"<html ([^>]*)>", lambda m: f'<html {m.group(1)} class="{" ".join(hidden)}">', src, count=1)
    public = {k: v for k, v in c.items()}
    src = src.replace('<script src="/app.js"></script>',
                      f'<script>window.SITE_CONTACT = {json.dumps(public)};</script>\n  <script src="/app.js"></script>')
    assert "{{" not in src, "unreplaced token: " + src[src.index("{{"):src.index("{{") + 30]
    return src


def load_dict(lang):
    if lang == "en":
        return {"html": {}, "js": {}}
    path = I18N_DIR / f"{lang}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return {"html": data.get("html", {}), "js": data.get("js", {})}


# ---------------------------------------------------------------------------
# GUIDES
# ---------------------------------------------------------------------------
def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def load_guide(slug, lang):
    """Returns (metadata dict, body html) from guides/<slug>/<lang>.html."""
    raw = (ROOT / "guides" / slug / f"{lang}.html").read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->\s*", raw, re.S)
    meta = dict(line.split(":", 1) for line in m.group(1).strip().splitlines())
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    return meta, raw[m.end():]


def guide_page(slug):
    return f"guides/{slug}/"


def guide_card(slug, lang):
    meta, _ = load_guide(slug, lang)
    return (f'<a class="guide-card" href="/guides/{slug}/">'
            f'<span class="guide-tag">{meta["tag"]}</span>'
            f'<h3>{meta["title"]}</h3><p>{meta["description"]}</p>'
            f'<span class="guide-more"><span>Read guide</span> <i class="fa-solid fa-arrow-right"></i></span></a>')


def guide_cards(lang):
    return '<div class="guide-grid">' + "".join(guide_card(s, lang) for s in GUIDES) + "</div>"


def json_ld(data):
    return ('<script type="application/ld+json">' +
            json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>")


def render_guide_source(page, lang):
    """English-chrome source for a guide page or the guides index, with localized content."""
    tpl = (ROOT / GUIDE_TEMPLATE).read_text(encoding="utf-8")
    home = f"{SITE_URL}/{LANGS[lang]['prefix']}"
    index_name = load_dict(lang)["html"].get("Investor Guides", "Investor Guides")
    if page == "guides/":
        title = "Investor Guides to Uzbekistan"
        desc = ("Practical guides for foreign investors: company registration, taxes and the "
                "Tashkent International Financial Centre (TIFC).")
        crumbs = '<span aria-current="page">Investor Guides</span>'
        body = ('      <h1>Investor Guides to Uzbekistan</h1>\n'
                '      <p class="guide-lead">Clear, up-to-date answers to the questions foreign investors ask us most.</p>\n'
                '      ' + guide_cards(lang))
        ld = {"@context": "https://schema.org", "@type": "CollectionPage", "url": page_url(lang, page),
              "inLanguage": lang, "isPartOf": {"@type": "WebSite", "name": "Mezon Advisory", "url": home}}
        og = "website"
    else:
        slug = page.split("/")[1]
        meta, article = load_guide(slug, lang)
        title, desc = meta["title"], meta["description"]
        crumbs = (f'<a href="/guides/">Investor Guides</a> <span aria-hidden="true">›</span> '
                  f'<span aria-current="page">{esc(title)}</span>')
        d = meta["updated"].split("-")
        body = (f'      <article class="guide-article">\n      <span class="guide-tag">{meta["tag"]}</span>\n'
                f'      <h1>{title}</h1>\n'
                f'      <p class="legal-updated"><span>Updated</span> <time datetime="{meta["updated"]}">'
                f'{d[2]}.{d[1]}.{d[0]}</time> · <span>{meta["minutes"]}</span> <span>min read</span></p>\n'
                f'{article}\n      </article>')
        org = {"@type": "Organization", "name": "Mezon Advisory", "url": f"{SITE_URL}/",
               "logo": f"{SITE_URL}/assets/icon-512.png"}
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
               "inLanguage": lang, "datePublished": meta["published"], "dateModified": meta["updated"],
               "image": f"{SITE_URL}/assets/og-image.png", "author": org, "publisher": org,
               "mainEntityOfPage": page_url(lang, page)},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Mezon Advisory", "item": home},
                  {"@type": "ListItem", "position": 2, "name": index_name, "item": page_url(lang, "guides/")},
                  {"@type": "ListItem", "position": 3, "name": title, "item": page_url(lang, page)}]}]
        og = "article"
    return (tpl.replace("__G_TITLE__", esc(title)).replace("__G_DESC__", esc(desc))
               .replace("__G_OGTYPE__", og).replace("__G_JSONLD__", json_ld(ld))
               .replace("__G_CRUMBS__", crumbs).replace("__G_BODY__", body))


def render_source(page, lang):
    if page.startswith("guides/"):
        return render_guide_source(page, lang)
    src = (ROOT / page).read_text(encoding="utf-8")
    return src.replace("<!--GUIDE-CARDS-->", guide_cards(lang))


# ---------------------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------------------
def build(check=False):
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    problems = []
    for lang, cfg in LANGS.items():
        d = load_dict(lang)
        used = set()
        for page in all_pages():
            src = render_source(page, lang)
            english = extract_strings(render_source(page, "en"))

            out = translate_html(src, d["html"], used) if lang != "en" else src
            out = re.sub(r'<html lang="en">', f'<html lang="{lang}" dir="{cfg["dir"]}">', out, count=1)
            out = out.replace("<!--SEO-->", seo_block(lang, page))
            out = out.replace('"@type": "ProfessionalService",',
                              f'"@type": "ProfessionalService",\n    "url": "{SITE_URL}/",')
            out = localize_links(out, lang, page)
            out = apply_contacts(out)
            if lang != "en" and d["js"]:
                payload = json.dumps(d["js"], ensure_ascii=False).replace("</", "<\\/")
                out = out.replace('<script src="/app.js"></script>',
                                  f'<script>window.I18N = {payload};</script>\n  <script src="/app.js"></script>')

            if lang != "en":
                # Strings deliberately kept identical (names, handles) are fine.
                same = {k for k, v in d["html"].items() if k == v}
                remaining = (set(extract_strings(out)) & set(english)) - same
                for s in sorted(remaining):
                    problems.append(f"[{lang}] {page}: {s}")

            target = DIST / cfg["prefix"] / (page + "index.html" if page.endswith("/") else page)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(out, encoding="utf-8")

        unused = set(d["html"]) - used
        for s in sorted(unused):
            print(f"  note [{lang}] unused translation key: {s[:90]}")

    for item in STATIC:
        p = ROOT / item
        if not p.exists():
            continue
        if p.is_dir():
            shutil.copytree(p, DIST / item)
        else:
            shutil.copy2(p, DIST / item)

    write_sitemap()
    # IndexNow key (Bing, Yandex, Seznam, Naver): lets us notify search engines of updates instantly.
    (DIST / "67d621c4365af72bae46514f55e7c441.txt").write_text("67d621c4365af72bae46514f55e7c441", encoding="utf-8")
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (DIST / "_headers").write_text(HEADERS, encoding="utf-8")
    # Secondary domains (aliases in Netlify) forward to the main .com address.
    aliases = "".join(f"{proto}://{host}/*  https://mezonadvisory.com/:splat  301!\n"
                      for host in ("mezonadvisory.uz", "www.mezonadvisory.uz")
                      for proto in ("https", "http"))
    (DIST / "_redirects").write_text(aliases + "/en/*  /:splat  301\n", encoding="utf-8")

    print(f"Built {len(LANGS)} languages x {len(all_pages())} pages into {DIST}")
    if problems:
        print(f"\n{len(problems)} untranslated string(s):")
        for p in problems:
            print("  " + p)
        if check:
            sys.exit(1)
    else:
        print("All visible strings translated.")


def all_pages():
    return PAGES + ["guides/"] + [guide_page(slug) for slug in GUIDES]


SITEMAP_PRIORITY = {"index.html": "1.0", "privacy.html": "0.3", "guides/": "0.7"}


def write_sitemap():
    today = date.today().isoformat()
    rows = []
    for page in all_pages():
        for lang in LANGS:
            alts = "\n".join(
                f'    <xhtml:link rel="alternate" hreflang="{c}" href="{page_url(c, page)}"/>' for c in LANGS)
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url("en", page)}"/>'
            priority = SITEMAP_PRIORITY.get(page, "0.8")
            rows.append(
                f"  <url>\n    <loc>{page_url(lang, page)}</loc>\n    <lastmod>{today}</lastmod>\n"
                f"    <priority>{priority}</priority>\n{alts}\n  </url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n")
    (DIST / "sitemap.xml").write_text(xml, encoding="utf-8")


HEADERS = """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/styles.css
  Cache-Control: public, max-age=3600

/app.js
  Cache-Control: public, max-age=3600

/assets/*
  Cache-Control: public, max-age=604800
"""


if __name__ == "__main__":
    if "--extract" in sys.argv:
        for page in all_pages():
            print(json.dumps({page: extract_strings(render_source(page, "en"))}, ensure_ascii=False, indent=1))
    else:
        build(check="--check" in sys.argv)

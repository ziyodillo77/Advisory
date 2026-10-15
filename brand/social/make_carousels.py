#!/usr/bin/env python3
"""
Instagram carousels (1080 x 1350) for the three investor guides, in English and Russian.

Usage:  python make_carousels.py <work_dir> <render-batch.js>
Needs fonttools (to cut static weights from brand/fonts/Manrope.ttf) and a Node script that
renders SVGs with @resvg/resvg-js (render-batch.js: node render-batch.js fontsDir a.svg b.svg ...).
Writes SVGs to <work_dir> and the finished PNGs to social/instagram/<lang>/.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "social" / "instagram"
W, H, M = 1080, 1350, 96
NAVY, WHITE, GOLD, MUTED, SOFT, LINE = "#0F172A", "#FFFFFF", "#D4AF37", "#94A3B8", "#CBD5E1", "#334155"
WEIGHTS = {"MzBold": 800, "MzSemi": 600, "MzReg": 500}

# ---------------------------------------------------------------------------
# CONTENT
# Slide kinds: cover (tag, title, sub) · list (title, items) · rows (title, rows, note) · cta
# A row is (label, value) or (label, value, True) to highlight it.
# ---------------------------------------------------------------------------
CAROUSELS = {
    "en": {
        "ui": {"swipe": "Swipe →", "cta_title": "Read the full guide", "url": "mezonadvisory.com/guides",
               "cta_sub": "Questions? Write to us in English, Russian, Arabic or Uzbek:",
               "save": "Save this post so you have it when you need it."},
        "register-company": [
            ("cover", "Company formation", "How to open a company in Uzbekistan as a foreigner", "Step-by-step guide for 2026"),
            ("list", "Why Uzbekistan", ["100% foreign ownership in most sectors", "No minimum charter capital for an LLC",
                                        "Online registration in 1–2 working days", "Foreign founders have the same rights as locals"]),
            ("list", "Choose the structure", ["LLC: the standard choice, 1 to 50 owners", "Representative office: marketing only, no income",
                                              "Branch: for specific projects such as construction"]),
            ("list", "Documents you need", ["Notarised passport copy with translation", "Corporate founder: register extract, charter, board decision",
                                            "Apostille on every foreign document", "A legal address with a registered lease"]),
            ("list", "The steps", ["Reserve the name on my.gov.uz", "Sign the charter and founders' decision", "Submit online and pay the state fee",
                                   "Get registration and a tax number", "Open a bank account"]),
            ("rows", "Realistic timeline", [("Apostille and translation", "1–3 weeks"), ("State registration", "1–2 days"),
                                            ("Bank account", "3–10 days"), ("Work permit for a foreign director", "2–4 weeks"),
                                            ("Total", "2–5 weeks", True)], ""),
            ("cta",),
        ],
        "tifc": [
            ("cover", "TIFC", "Tashkent International Financial Centre", "English law and tax holidays until 2076"),
            ("list", "What is TIFC", ["A special jurisdiction inside Tashkent", "English common law applies directly",
                                      "Its own international commercial court, in English", "Operations expected to start in 2027"]),
            ("list", "Tax incentives until 2076", ["0% corporate tax on qualifying financial services", "0% income tax for foreign employees",
                                                   "No VAT on qualifying financial services", "No property tax, land tax or customs duties on TIFC facilities"]),
            ("list", "Who it is for", ["Islamic and investment banks", "Fund and asset managers", "Insurers and reinsurance brokers",
                                       "Brokers, dealers and underwriters", "Fintech companies and family offices"]),
            ("list", "Conditions", ["Real substance: office, staff and management", "A licence from the Financial Services Authority",
                                    "Separate accounting of exempt income", "Strict AML and governance compliance"]),
            ("list", "Extra benefits", ["Visas of up to 5 years for staff and families", "No separate work permits for foreign staff",
                                        "Contracts in any agreed currency", "Free repatriation of capital and profits"]),
            ("cta",),
        ],
        "taxes": [
            ("cover", "Tax", "Taxes in Uzbekistan for foreign investors", "The key rates for 2026"),
            ("rows", "Key rates in 2026", [("Profit tax", "15%"), ("VAT", "12%"), ("Personal income tax", "12%"), ("Social tax (employer)", "12%"),
                                           ("Dividends to residents", "5%"), ("Dividends to non-residents", "10%")], ""),
            ("list", "Small business option", ["Turnover tax: generally 4% of revenue", "Replaces VAT and profit tax below the revenue threshold",
                                               "Not always cheaper: compare both before registering"]),
            ("rows", "Example: USD 100,000 profit", [("Profit tax 15%", "−15,000"), ("Dividend paid", "85,000"),
                                                     ("Withholding tax 10%", "−8,500"), ("Net to a foreign owner", "76,500", True),
                                                     ("With a 5% treaty rate", "80,750", True)], "Total tax: 23.5%, or 19.25% with a treaty"),
            ("list", "Tax treaties", ["Treaties with 50+ countries", "Including Russia, Kazakhstan, the UAE and Turkey",
                                      "Often cut dividend tax to 5%", "Give a tax residency certificate before the payment"]),
            ("list", "Special regimes", ["IT Park: 0% profit tax, guaranteed until 2040", "TIFC: 0% on financial services until 2076",
                                         "Free economic zones for manufacturing"]),
            ("cta",),
        ],
    },
    "ru": {
        "ui": {"swipe": "Листайте →", "cta_title": "Полное руководство", "url": "mezonadvisory.com/ru/guides",
               "cta_sub": "Есть вопросы? Пишите нам на русском, английском, арабском или узбекском:",
               "save": "Сохраните пост, чтобы он был под рукой."},
        "register-company": [
            ("cover", "Регистрация компаний", "Как открыть компанию в Узбекистане иностранцу", "Пошаговое руководство 2026"),
            ("list", "Почему Узбекистан", ["100% иностранное владение в большинстве отраслей", "Нет минимального уставного капитала для ООО",
                                           "Онлайн-регистрация за 1–2 рабочих дня", "Иностранцы имеют те же права, что и местные"]),
            ("list", "Выберите форму", ["ООО: стандартный выбор, от 1 до 50 участников", "Представительство: только продвижение, без дохода",
                                        "Филиал: для отдельных проектов, например строительства"]),
            ("list", "Нужные документы", ["Нотариальная копия паспорта с переводом", "Для компании-учредителя: выписка из реестра, устав, решение",
                                          "Апостиль на всех иностранных документах", "Юридический адрес с зарегистрированной арендой"]),
            ("list", "Шаги", ["Зарезервировать название на my.gov.uz", "Подписать устав и решение учредителей", "Подать заявление онлайн и оплатить пошлину",
                              "Получить регистрацию и ИНН", "Открыть банковский счёт"]),
            ("rows", "Реальные сроки", [("Апостиль и перевод", "1–3 недели"), ("Государственная регистрация", "1–2 дня"),
                                        ("Банковский счёт", "3–10 дней"), ("Разрешение на работу", "2–4 недели"),
                                        ("Итого", "2–5 недель", True)], ""),
            ("cta",),
        ],
        "tifc": [
            ("cover", "ТМФЦ", "Ташкентский международный финансовый центр", "Английское право и налоговые каникулы до 2076 года"),
            ("list", "Что такое ТМФЦ", ["Особая юрисдикция внутри Ташкента", "Напрямую действует английское общее право",
                                        "Собственный международный коммерческий суд на английском", "Начало работы ожидается в 2027 году"]),
            ("list", "Налоговые льготы до 2076", ["0% налога на прибыль по квалифицируемым финансовым услугам", "0% подоходного налога для иностранных сотрудников",
                                                  "Без НДС на квалифицируемые финансовые услуги", "Без налога на имущество, земельного налога и пошлин"]),
            ("list", "Для кого", ["Исламские и инвестиционные банки", "Управляющие фондами и активами", "Страховщики и перестраховочные брокеры",
                                  "Брокеры, дилеры и андеррайтеры", "Финтех и семейные офисы"]),
            ("list", "Условия", ["Реальное присутствие: офис, персонал, управление", "Лицензия Агентства по финансовым услугам",
                                 "Раздельный учёт льготных доходов", "Строгое соблюдение ПОД/ФТ и корпоративного управления"]),
            ("list", "Другие преимущества", ["Визы до 5 лет для сотрудников и их семей", "Без отдельных разрешений на работу",
                                             "Договоры в любой согласованной валюте", "Свободная репатриация капитала и прибыли"]),
            ("cta",),
        ],
        "taxes": [
            ("cover", "Налоги", "Налоги в Узбекистане для иностранных инвесторов", "Ключевые ставки 2026 года"),
            ("rows", "Ключевые ставки 2026", [("Налог на прибыль", "15%"), ("НДС", "12%"), ("Подоходный налог", "12%"), ("Социальный налог", "12%"),
                                              ("Дивиденды резидентам", "5%"), ("Дивиденды нерезидентам", "10%")], ""),
            ("list", "Для малого бизнеса", ["Налог с оборота: обычно 4% от выручки", "Заменяет НДС и налог на прибыль ниже порога выручки",
                                            "Не всегда дешевле: сравните оба режима до регистрации"]),
            ("rows", "Пример: прибыль $100 000", [("Налог на прибыль 15%", "−15 000"), ("Выплаченные дивиденды", "85 000"),
                                                   ("Налог у источника 10%", "−8 500"), ("Иностранному владельцу", "76 500", True),
                                                   ("По соглашению 5%", "80 750", True)], "Итоговая нагрузка: 23,5%, по соглашению 19,25%"),
            ("list", "Налоговые соглашения", ["Соглашения с более чем 50 странами", "В том числе Россия, Казахстан, ОАЭ и Турция",
                                              "Часто снижают налог на дивиденды до 5%", "Нужен сертификат резидентства до выплаты"]),
            ("list", "Специальные режимы", ["IT Park: 0% налога на прибыль до 2040 года", "ТМФЦ: 0% на финансовые услуги до 2076 года",
                                            "Свободные экономические зоны для производства"]),
            ("cta",),
        ],
    },
}


# ---------------------------------------------------------------------------
# TEXT HELPERS
# ---------------------------------------------------------------------------
class Font:
    def __init__(self, path):
        f = TTFont(path)
        self.cmap, self.hmtx, self.upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm

    def width(self, text, size):
        total = 0
        for ch in text:
            g = self.cmap.get(ord(ch))
            assert g, f"glyph missing for {ch!r}"
            total += self.hmtx[g][0]
        return total * size / self.upm


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(font, text, size, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if font.width(trial, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def text(x, y, s, family, size, fill, anchor="start", spacing=0):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y:.0f}" font-family="{family}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{ls}>{esc(s)}</text>')


# ---------------------------------------------------------------------------
# SLIDES
# ---------------------------------------------------------------------------
def logo():
    src = (ROOT / "assets" / "logo-white.svg").read_text(encoding="utf-8")
    inner = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", src.strip())
    inner = re.sub(r"<title>.*?</title>", "", inner)
    return f'<g transform="translate({M} 62) scale({200 / 365.5:.4f})">{inner}</g>'


def mark(x, y, size, opacity):
    s = size / 120
    return (f'<g transform="translate({x} {y}) scale({s:.4f})" opacity="{opacity}">'
            f'<path d="M22 57.8 A38 38 0 0 1 98 57.8 Z" fill="{WHITE}"/>'
            f'<path d="M22 62.2 A38 38 0 0 0 98 62.2 Z" fill="{GOLD}"/></g>')


def frame(body, n, total, ui, last):
    parts = [f'<rect width="{W}" height="{H}" fill="{NAVY}"/>', logo(),
             text(W - M, 112, f"{n:02d} / {total:02d}", "MzSemi", 26, MUTED, "end"),
             f'<rect x="{M}" y="1228" width="{W - 2 * M}" height="2" fill="{LINE}"/>',
             text(M, 1288, "mezonadvisory.com", "MzSemi", 28, MUTED)]
    if not last:
        parts.append(text(W - M, 1288, ui["swipe"], "MzBold", 28, GOLD, "end"))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            + "".join(parts) + body + "</svg>")


def fit_lines(font, s, size, max_w, max_lines, min_size):
    while True:
        lines = wrap(font, s, size, max_w)
        if len(lines) <= max_lines or size <= min_size:
            return lines, size
        size -= 4


def cover(F, tag, title, sub):
    tag_up = tag.upper()
    tw = F["MzBold"].width(tag_up, 26) + 26 * 0.1 * len(tag_up)
    out = [mark(640, 720, 620, 0.07),
           f'<rect x="{M}" y="300" width="{tw + 56:.0f}" height="56" rx="28" fill="#FEF9C3"/>',
           text(M + 28, 338, tag_up, "MzBold", 26, "#854D0E", spacing=2.6)]
    lines, size = fit_lines(F["MzBold"], title, 92, W - 2 * M, 5, 64)
    y = 470
    for line in lines:
        out.append(text(M, y, line, "MzBold", size, WHITE))
        y += size * 1.14
    y += 30
    for line in wrap(F["MzSemi"], sub, 42, W - 2 * M):
        out.append(text(M, y, line, "MzSemi", 42, GOLD))
        y += 56
    return "".join(out)


def heading(F, n, title):
    out = [text(M, 330, f"{n:02d}", "MzBold", 110, GOLD)]
    lines, size = fit_lines(F["MzBold"], title, 66, W - 2 * M, 2, 52)
    y = 440
    for line in lines:
        out.append(text(M, y, line, "MzBold", size, WHITE))
        y += size * 1.18
    return out, y + 40


def list_slide(F, n, title, items):
    out, y0 = heading(F, n, title)
    avail = 1170 - y0
    for size in range(48, 29, -2):
        blocks = [wrap(F["MzReg"], it, size, W - 2 * M - 52) for it in items]
        lh, gap = size * 1.36, size * 1.0
        need = sum(len(b) * lh for b in blocks) + gap * (len(blocks) - 1)
        if need <= avail:
            break
    y = y0 + size
    for b in blocks:
        out.append(f'<circle cx="{M + 10}" cy="{y - size * 0.34:.0f}" r="8" fill="{GOLD}"/>')
        for line in b:
            out.append(text(M + 52, y, line, "MzReg", size, SOFT))
            y += lh
        y += gap
    return "".join(out)


def rows_slide(F, n, title, rows, note):
    out, y = heading(F, n, title)
    row_h = min(118, (1150 - y - (70 if note else 0)) / len(rows))
    for r in rows:
        label, value, hl = r[0], r[1], len(r) > 2
        cy = y + row_h / 2 + 14
        if hl:
            out.append(f'<rect x="{M - 20}" y="{y + 6:.0f}" width="{W - 2 * M + 40}" height="{row_h - 12:.0f}" rx="16" fill="#1E293B"/>')
        lsize = 40
        while F["MzSemi"].width(label, lsize) > 560:
            lsize -= 2
        out.append(text(M + (8 if hl else 0), cy, label, "MzSemi", lsize, WHITE if hl else SOFT))
        out.append(text(W - M - (8 if hl else 0), cy + 2, value, "MzBold", 50, GOLD if hl else WHITE, "end"))
        if not hl:
            out.append(f'<rect x="{M}" y="{y + row_h:.0f}" width="{W - 2 * M}" height="1.5" fill="{LINE}"/>')
        y += row_h
    if note:
        out.append(text(M, y + 70, note, "MzSemi", 32, MUTED))
    return "".join(out)


def cta_slide(F, ui):
    out = [mark((W - 300) / 2, 230, 300, 1)]
    y = 640
    for line in wrap(F["MzBold"], ui["cta_title"], 72, W - 2 * M):
        out.append(text(W / 2, y, line, "MzBold", 72, WHITE, "middle"))
        y += 84
    out.append(text(W / 2, y + 10, ui["url"], "MzBold", 46, GOLD, "middle"))
    y += 120
    for line in wrap(F["MzReg"], ui["cta_sub"], 34, W - 2 * M - 80):
        out.append(text(W / 2, y, line, "MzReg", 34, SOFT, "middle"))
        y += 48
    y += 30
    for label in ("Telegram  @mezon_advisory", "WhatsApp  +90 534 986 42 97"):
        out.append(text(W / 2, y, label, "MzBold", 38, WHITE, "middle"))
        y += 60
    out.append(text(W / 2, 1160, ui["save"], "MzSemi", 30, MUTED, "middle"))
    return "".join(out)


def main():
    work, renderer = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    fonts = work / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    for name, wght in WEIGHTS.items():
        t = instancer.instantiateVariableFont(TTFont(ROOT / "brand" / "fonts" / "Manrope.ttf"), {"wght": wght})
        for rec in t["name"].names:
            if rec.nameID in (1, 4, 6, 16):
                rec.string = name
            if rec.nameID in (2, 17):
                rec.string = "Regular"
        t.save(fonts / f"{name}.ttf")
    F = {name: Font(fonts / f"{name}.ttf") for name in WEIGHTS}

    svgs = []
    for lang, data in CAROUSELS.items():
        ui = data["ui"]
        for slug, slides in ((k, v) for k, v in data.items() if k != "ui"):
            for i, s in enumerate(slides, 1):
                kind = s[0]
                if kind == "cover":
                    body = cover(F, *s[1:])
                elif kind == "list":
                    body = list_slide(F, i, *s[1:])
                elif kind == "rows":
                    body = rows_slide(F, i, *s[1:])
                else:
                    body = cta_slide(F, ui)
                path = work / lang / f"{slug}-{i}.svg"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(frame(body, i, len(slides), ui, kind == "cta"), encoding="utf-8")
                svgs.append(str(path))

    subprocess.run(["node", str(renderer), str(fonts), *svgs], check=True)
    for svg in svgs:
        png = Path(svg).with_suffix(".png")
        dest = OUT / Path(svg).parent.name / png.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(png, dest)
    print(f"Wrote {len(svgs)} slides to {OUT}")


if __name__ == "__main__":
    main()

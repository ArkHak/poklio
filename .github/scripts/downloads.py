#!/usr/bin/env python3
"""Статистика установок Poklio по счётчикам скачиваний релизов GitHub.

Обновление по воздуху скачивает poklio.app.bin.sig, а затем poklio.app.bin.
При ручной установке скачивают только poklio.app.bin. Поэтому:
  обновления = скачивания .sig,
  установки  = скачивания .bin − скачивания .sig (по каждому релизу, не меньше 0).

GitHub хранит только текущие счётчики, поэтому скрипт раз в сутки дописывает
строку в downloads.csv и перерисовывает графики и данные для бейджа.

Запуск: downloads.py <папка ветки stats>
Окружение: REPOSITORY (owner/repo), GH_TOKEN (необязательно), TODAY (YYYY-MM-DD, для проверки).
"""

import csv
import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

APP_ASSET = "poklio.app.bin"
SIGNATURE_ASSET = "poklio.app.bin.sig"

# Палитра из docs/brand.md: светлая тема — ink/graphite/mist/leaf на paper,
# тёмная — paper/leaf-light и приглушённые серые на почти чёрном.
# У графика своя подложка: GitHub выбирает вариант по теме системы, а не сайта,
# и без подложки светлый вариант на тёмной странице не читается.
THEMES = {
    "light": {"background": "#F5F3EC", "border": "#DDE2D8", "text": "#202420", "muted": "#616760",
              "grid": "#DDE2D8", "accent": "#526B50", "second": "#616760", "chip": "#EAEDE5"},
    "dark": {"background": "#161A16", "border": "#2C322C", "text": "#F5F3EC", "muted": "#A9AFA7",
             "grid": "#2C322C", "accent": "#8FAE8B", "second": "#A9AFA7", "chip": "#202620"},
}

TEXTS = {
    "ru": {
        "installs": "установки",
        "updates": "обновления по воздуху",
        "headline": lambda n: f"{Number(n, 'ru')} {Plural(n, 'установка', 'установки', 'установок')}",
        "unit": lambda n: Plural(n, "установка", "установки", "установок"),
        "since": "без учёта обновлений по воздуху",
        "updated": "обновлено",
        "months": ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"],
    },
    "en": {
        "installs": "installs",
        "updates": "over-the-air updates",
        "headline": lambda n: f"{Number(n, 'en')} {'install' if n == 1 else 'installs'}",
        "unit": lambda n: "install" if n == 1 else "installs",
        "since": "not counting over-the-air updates",
        "updated": "updated",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    },
}


def Plural(n, one, few, many):
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def Number(n, lang):
    text = f"{n:,}"
    return text.replace(",", " ") if lang == "ru" else text


def FetchReleases(repository, token):
    releases = []
    page = 1
    while True:
        request = urllib.request.Request(
            f"https://api.github.com/repos/{repository}/releases?per_page=100&page={page}",
            headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(request, timeout=30) as response:
            batch = json.load(response)
        releases += batch
        if len(batch) < 100:
            return releases
        page += 1


def Count(releases):
    installs = updates = 0
    for release in releases:
        if release.get("draft"):
            continue
        counts = {asset["name"]: asset["download_count"] for asset in release.get("assets", [])}
        app = counts.get(APP_ASSET, 0)
        signature = counts.get(SIGNATURE_ASSET, 0)
        installs += max(app - signature, 0)
        updates += signature
    return installs, updates


def ReadHistory(path):
    if not path.exists():
        return []
    with path.open(newline="") as file:
        return [(dt.date.fromisoformat(row["date"]), int(row["installs"]), int(row["updates"]))
                for row in csv.DictReader(file)]


def WriteHistory(path, history):
    with path.open("w", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["date", "installs", "updates"])
        for day, installs, updates in history:
            writer.writerow([day.isoformat(), installs, updates])


def NiceMax(value):
    value = max(value, 4)
    scale = 1
    while True:
        for step in (1, 2, 5):
            if step * scale * 4 >= value:
                return step * scale * 4
        scale *= 10


def FormatDate(day, lang, with_year=False):
    month = TEXTS[lang]["months"][day.month - 1]
    text = f"{day.day} {month}" if lang == "ru" else f"{month} {day.day}"
    return f"{text} {day.year}" if with_year else text


def Escape(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def RenderSvg(history, lang, theme):
    colors = THEMES[theme]
    texts = TEXTS[lang]
    width, height = 800, 360
    left, right, top, bottom = 64, 32, 144, 48
    plot_w, plot_h = width - left - right, height - top - bottom

    first, last = history[0][0], history[-1][0]
    span = max((last - first).days, 1)
    y_max = NiceMax(max(max(i, u) for _, i, u in history))

    def X(day):
        if first == last:
            return left + plot_w / 2
        return left + plot_w * (day - first).days / span

    def Y(value):
        return top + plot_h * (1 - value / y_max)

    installs, updates = history[-1][1], history[-1][2]
    font = 'font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif"'
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
        f'height="{height}" role="img" aria-label="{Escape(texts["headline"](installs))}" {font}>',
        '<defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{colors["accent"]}" stop-opacity="0.32"/>'
        f'<stop offset="1" stop-color="{colors["accent"]}" stop-opacity="0"/>'
        '</linearGradient></defs>',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="16" '
        f'fill="{colors["background"]}" stroke="{colors["border"]}"/>',
        f'<text x="32" y="80" fill="{colors["text"]}">'
        f'<tspan font-size="56" font-weight="700" letter-spacing="-1">{Number(installs, lang)}</tspan>'
        f'<tspan dx="12" font-size="22" font-weight="600">{Escape(texts["unit"](installs))}</tspan></text>',
        f'<text x="32" y="110" font-size="14" fill="{colors["muted"]}">{Escape(texts["since"])} · '
        f'{texts["updated"]} {FormatDate(last, lang, with_year=True)}</text>',
    ]

    # Легенда-плашки: линии различаются и цветом, и начертанием.
    chip_w, chip_x = 264, width - 32 - 264
    for row, (label, value, color, dash, stroke) in enumerate([
            (texts["installs"], installs, colors["accent"], "", 3),
            (texts["updates"], updates, colors["second"], ' stroke-dasharray="5 4"', 2)]):
        y = 32 + row * 40
        parts += [
            f'<rect x="{chip_x}" y="{y}" width="{chip_w}" height="32" rx="16" fill="{colors["chip"]}"/>',
            f'<line x1="{chip_x + 16}" y1="{y + 16}" x2="{chip_x + 36}" y2="{y + 16}" stroke="{color}" '
            f'stroke-width="{stroke}" stroke-linecap="round"{dash}/>',
            f'<text x="{chip_x + 46}" y="{y + 21}" font-size="13" fill="{colors["muted"]}">{Escape(label)}</text>',
            f'<text x="{chip_x + chip_w - 16}" y="{y + 21}" font-size="14" font-weight="700" text-anchor="end" '
            f'fill="{colors["text"]}">{Number(value, lang)}</text>',
        ]

    for index in range(5):
        value = y_max * index // 4
        y = Y(value)
        dash = "" if index == 0 else ' stroke-dasharray="2 6"'
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" stroke="{colors["grid"]}" '
                     f'stroke-width="1"{dash}/>')
        parts.append(f'<text x="{left - 14}" y="{y + 4:.1f}" font-size="12" text-anchor="end" '
                     f'fill="{colors["muted"]}">{Number(value, lang)}</text>')

    labels = [first] if first == last else [first, last]
    if span >= 14:
        labels.insert(1, first + dt.timedelta(days=span // 2))
    for index, day in enumerate(labels):
        anchor = "middle" if len(labels) == 1 else ("start" if index == 0 else "end" if day == last else "middle")
        parts.append(f'<text x="{X(day):.1f}" y="{height - bottom + 26}" font-size="12" text-anchor="{anchor}" '
                     f'fill="{colors["muted"]}">{FormatDate(day, lang)}</text>')

    def Points(column):
        return " ".join(f"{X(row[0]):.1f},{Y(row[column]):.1f}" for row in history)

    if len(history) > 1:
        base = Y(0)
        area = f"{X(first):.1f},{base:.1f} {Points(1)} {X(last):.1f},{base:.1f}"
        parts += [
            f'<polygon points="{area}" fill="url(#area)"/>',
            f'<polyline points="{Points(2)}" fill="none" stroke="{colors["second"]}" stroke-width="2" '
            f'stroke-dasharray="5 4" stroke-linejoin="round"/>',
            f'<polyline points="{Points(1)}" fill="none" stroke="{colors["accent"]}" stroke-width="3" '
            f'stroke-linejoin="round" stroke-linecap="round"/>',
        ]
    parts += [
        f'<circle cx="{X(last):.1f}" cy="{Y(updates):.1f}" r="4" fill="{colors["second"]}" '
        f'stroke="{colors["background"]}" stroke-width="2"/>',
        f'<circle cx="{X(last):.1f}" cy="{Y(installs):.1f}" r="11" fill="{colors["accent"]}" fill-opacity="0.2"/>',
        f'<circle cx="{X(last):.1f}" cy="{Y(installs):.1f}" r="5.5" fill="{colors["accent"]}" '
        f'stroke="{colors["background"]}" stroke-width="2"/>',
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def Badge(installs, lang):
    label = TEXTS[lang]["installs"]
    return json.dumps({"schemaVersion": 1, "label": label, "message": Number(installs, lang),
                       "color": "616760"}, ensure_ascii=False) + "\n"


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: downloads.py <stats dir>")
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    today = dt.date.fromisoformat(os.environ.get("TODAY") or dt.datetime.now(dt.timezone.utc).date().isoformat())

    installs, updates = Count(FetchReleases(os.environ["REPOSITORY"], os.environ.get("GH_TOKEN")))
    history = [row for row in ReadHistory(out / "downloads.csv") if row[0] != today]
    history.append((today, installs, updates))
    history.sort()
    WriteHistory(out / "downloads.csv", history)

    for lang in TEXTS:
        suffix = "" if lang == "ru" else ".en"
        for theme in THEMES:
            (out / f"downloads{suffix}.{theme}.svg").write_text(RenderSvg(history, lang, theme), encoding="utf-8")
        (out / f"badge{suffix}.json").write_text(Badge(installs, lang), encoding="utf-8")
    print(f"{today}: installs {installs}, updates {updates}")


if __name__ == "__main__":
    main()

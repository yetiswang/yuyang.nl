#!/usr/bin/env python3
"""Per-post OG cards for yuyang.nl (DESIGN.md §8, step 7): 1200x630 JPEG on warm paper.

Usage: python3 scripts/make-og.py <slug> "<EN title>" "<ZH title>" "<EN date>" "<ZH date>"
Writes assets/og/<slug>.jpg and assets/og/<slug>-zh.jpg.

EN: eyebrow YUYANG WANG · HYPOMNEMATA in Inter (wght 560, tracked), title in Source Serif 4
(wght 700, opsz 26, at most three lines, shrinks to fit), date bottom left. ZH: eyebrow
王昱揚 · 虛室 and title in Songti TC Bold (macOS system font). Both: bg_light.webp cover-cropped,
the center.webp 昱 ink blot 150 px bottom right, JPEG q86. Inter and Source Serif 4 (SIL OFL)
are fetched once into scripts/.fonts/ (not committed). Needs Pillow with FreeType.
"""
import os
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(HERE, '.fonts')
SOURCES = {
    'Inter.ttf': 'https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf',
    'SourceSerif4.ttf': 'https://raw.githubusercontent.com/google/fonts/main/ofl/sourceserif4/SourceSerif4%5Bopsz%2Cwght%5D.ttf',
}
SONGTI_TC = ('/System/Library/Fonts/Supplemental/Songti.ttc', 2)  # Songti TC Bold
W, H, PAD = 1200, 630, 90
INK, MUTED = (34, 32, 30), (120, 114, 106)


def font_file(name):
    os.makedirs(FONTS, exist_ok=True)
    path = os.path.join(FONTS, name)
    if not os.path.exists(path):
        urllib.request.urlretrieve(SOURCES[name], path + '.part')
        os.replace(path + '.part', path)
    return path


def variable(name, size, **axes):
    """A variable font at the given axis values, set by axis name (the order differs per font)."""
    f = ImageFont.truetype(font_file(name), size)
    order = [a['name'].decode() if isinstance(a['name'], bytes) else a['name'] for a in f.get_variation_axes()]
    by_name = {k.lower(): v for k, v in axes.items()}  # 'Optical size' in Inter, 'Optical Size' in Source Serif 4
    f.set_variation_by_axes([by_name[n.lower()] for n in order])
    return f


def songti(size):
    return ImageFont.truetype(SONGTI_TC[0], size, index=SONGTI_TC[1])


def wrap(draw, text, font, width, cjk):
    words = list(text) if cjk else text.split(' ')
    lines, cur = [], ''
    for w in words:
        trial = cur + w if cjk else (cur + ' ' + w).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def tracked(draw, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking


def card(out, title, date, zh):
    bg = ImageOps.fit(Image.open(os.path.join(ROOT, 'assets/ink-splatters/bg_light.webp')).convert('RGB'), (W, H))
    d = ImageDraw.Draw(bg)
    if zh:
        tracked(d, (PAD, 92), '王昱揚 · 虛室', songti(26), MUTED, 6)
    else:
        tracked(d, (PAD, 94), 'YUYANG WANG · HYPOMNEMATA', variable('Inter.ttf', 20, Weight=560, **{'Optical size': 14}), MUTED, 3.2)
    width = W - 2 * PAD - 120
    for size in range(64, 34, -2):
        f = songti(size) if zh else variable('SourceSerif4.ttf', size, Weight=700, **{'Optical size': 26})
        lines = wrap(d, title, f, width, zh)
        if len(lines) <= 3:
            break
    lh = size * 1.22
    y = 200 + (3 - len(lines)) * lh * 0.35
    for line in lines:
        d.text((PAD, y), line, font=f, fill=INK)
        y += lh
    d.text((PAD, 516), date, font=songti(24) if zh else variable('Inter.ttf', 22, Weight=420, **{'Optical size': 14}), fill=MUTED)
    blot = Image.open(os.path.join(ROOT, 'assets/ink-splatters/center.webp')).convert('RGBA')
    blot = ImageOps.contain(blot, (150, 150))
    bg.paste(blot, (W - PAD - 130 - blot.width // 2 + 65, H - 110 - blot.height // 2 - 20), blot)
    bg.save(out, quality=86, optimize=True, progressive=True)
    print('wrote', os.path.relpath(out, ROOT))


if __name__ == '__main__':
    slug, en_title, zh_title, en_date, zh_date = sys.argv[1:6]
    card(os.path.join(ROOT, f'assets/og/{slug}.jpg'), en_title, en_date, zh=False)
    card(os.path.join(ROOT, f'assets/og/{slug}-zh.jpg'), zh_title, zh_date, zh=True)

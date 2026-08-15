#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = 'icons'
SIZES = [72,96,120,128,152,180,192,512]
BG = (7,193,96,255)
FG = (255,255,255,255)
CHAR = '微'
FALLBACK = 'W'

os.makedirs(OUT_DIR, exist_ok=True)

# Try to find a font supporting Chinese; fallback to DejaVuSans
fonts_to_try = [
    'PingFang.ttc', 'PingFang.ttf', 'NotoSansCJK-Regular.ttc', 'NotoSansCJKsc-Regular.otf',
    'SimHei.ttf', 'MSYH.TTC', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc'
]

def find_font(size):
    for f in fonts_to_try:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    # Last resort: default font
    return ImageFont.load_default()

results = []
for s in SIZES:
    img = Image.new('RGBA', (s, s), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    # rounded rect background
    radius = int(s*0.14)
    try:
        draw.rounded_rectangle([(0,0),(s,s)], radius=radius, fill=BG)
    except Exception:
        # fallback: draw rectangle
        draw.rectangle([(0,0),(s,s)], fill=BG)
    # text
    # choose font size roughly 0.6*size
    font_size = int(s * 0.56)
    font = find_font(font_size)
    text = CHAR
    # test if font has glyph
    try:
        bbox = draw.textbbox((0,0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w == 0 or h == 0:
            raise Exception('no glyph')
    except Exception:
        text = FALLBACK
        font = find_font(int(font_size*0.9))
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    # center the text
    x = (s - w) / 2
    y = (s - h) / 2 - (s*0.03)
    draw.text((x,y), text, font=font, fill=FG)
    out_path = os.path.join(OUT_DIR, f'icon-{s}x{s}.png')
    img.save(out_path, format='PNG')
    results.append(out_path)

print('Generated icons:')
for p in results:
    print(' -', p)

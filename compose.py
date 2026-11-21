#!/usr/bin/env python3
"""Build entry.png: a newspaper front page summing up the world news of
Saturday 21 November 2026. Hero art (Peace Palace, The Hague) was generated
for this entry; all text is drawn here with PIL so every word is exact.
Output: 1024x1024 PNG, well under the 1 MiB cap.
Run: python3 compose.py  (reads work/hero.png, writes entry.png)
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
# Generated hero art lives outside the repo (kept out of the snapshot);
# override with HERO_PNG when composing from another checkout.
HERO = os.environ.get(
    "HERO_PNG",
    os.path.join(os.path.dirname(ROOT), "news-image-20261121-work", "hero.png"))
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (22, 22, 22)
NAVY = (22, 35, 63)
RED = (163, 22, 33)
GOLD = (185, 138, 47)
GREY = (90, 86, 78)
RULE = (180, 172, 155)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- Masthead ---
d.rectangle([0, 0, W, 92], fill=NAVY)
d.text((32, 14), "THE WORLD", font=font(SERIF_B, 56), fill=(255, 255, 255))
d.text((32, 74), "IN ONE IMAGE", font=font(SANS_B, 15), fill=(217, 179, 108))
d.text((W - 32, 22), "SATURDAY", font=font(SANS_B, 22), fill=(255, 255, 255), anchor="ra")
d.text((W - 32, 50), "21 NOVEMBER 2026", font=font(SANS, 20), fill=(217, 179, 108), anchor="ra")
d.rectangle([0, 92, W, 96], fill=GOLD)

# --- Hero photo (Peace Palace) ---
# Scale to full width, then take a band that keeps the tower and facade.
hero = Image.open(HERO).convert("RGB")
hw, hh = hero.size
target_h = 330
hero = hero.resize((W, int(hh * W / hw)), Image.LANCZOS)
band_top = 20
hero = hero.crop((0, band_top, W, band_top + target_h))
img.paste(hero, (0, 96))
d.rectangle([0, 96 + target_h - 4, W, 96 + target_h], fill=GOLD)

# --- Lead story ---
y = 96 + target_h + 22  # 458
d.text((32, y), "THE HAGUE  •  WORLD COURT", font=font(SANS_B, 19), fill=RED)
y += 30
head = "MYANMAR COMMITTED GENOCIDE, WORLD COURT RULES"
f_head = font(SERIF_B, 42)
lines = wrap(d, head, f_head, W - 64)
y = draw_lines(d, lines, 32, y, f_head, INK, 50)
y += 6
stand = ("The International Court of Justice finds Myanmar's forces committed "
         "state-sponsored genocide against the Rohingya \u2014 a landmark judgment.")
f_stand = font(SERIF, 21)
lines = wrap(d, stand, f_stand, W - 64)
y = draw_lines(d, lines, 32, y, f_stand, (58, 54, 48), 28)
y += 12
d.line([32, y, W - 32, y], fill=RULE, width=2)
y += 16

# --- Two columns ---
col_w = 464
col_top = y
# left: Poland
x = 32
d.text((x, y), "WAR IN EUROPE", font=font(SANS_B, 18), fill=RED)
yy = y + 28
f_col = font(SERIF_B, 29)
lines = wrap(d, "MISSILES HIT POLAND", f_col, col_w)
yy = draw_lines(d, lines, x, yy, f_col, INK, 35)
yy += 4
f_body = font(SANS, 19)
lines = wrap(d, "Two Russian missiles and a suspected drone came down in Poland. "
                "NATO calls it a grave violation of its airspace.", f_body, col_w)
left_end = draw_lines(d, lines, x, yy, f_body, (58, 54, 48), 26)
# right: markets
x = 528
d.text((x, y), "MARKETS", font=font(SANS_B, 18), fill=RED)
yy = y + 28
lines = wrap(d, "STOCKS SLIDE INTO CORRECTION", f_col, col_w)
yy = draw_lines(d, lines, x, yy, f_col, INK, 35)
yy += 4
lines = wrap(d, "The S&P 500 falls about 3.7% as AI shares sell off. Nvidia sinks "
                "to a 52-week low amid a report of an SEC probe.", f_body, col_w)
right_end = draw_lines(d, lines, x, yy, f_body, (58, 54, 48), 26)
# vertical divider between columns
col_end = max(left_end, right_end)
d.line([512, col_top + 4, 512, col_end], fill=RULE, width=1)

y = col_end + 12
d.line([32, y, W - 32, y], fill=RULE, width=2)
y += 14

# --- Also today: three columns ---
d.text((32, y), "ALSO TODAY", font=font(SANS_B, 18), fill=RED)
y += 28
items = [
    ("UK\u2013EU SIGN DEALS",
     "Food, carbon and youth-mobility deals agreed in Brussels."),
    ("CYCLONE AKVAN",
     "Storm crosses India's east coast; 300,000 evacuated."),
    ("TRUMP\u2013XI\u2013PUTIN MEET",
     "First trilateral summit ends with few concrete results."),
]
f_mini_h = font(SANS_B, 17)
f_mini = font(SANS, 17)
col3 = 304
mini_end = y
for i, (h, b) in enumerate(items):
    x = 32 + i * (col3 + 16)
    d.text((x, y), h, font=f_mini_h, fill=INK)
    yy = y + 22
    lines = wrap(d, b, f_mini, col3)
    mini_end = max(mini_end, draw_lines(d, lines, x, yy, f_mini, (58, 54, 48), 21))

y = mini_end + 12
d.line([32, y, W - 32, y], fill=RULE, width=1)
d.text((W // 2, y + 8),
       "COP31 enters its final stage  \u2022  Indonesia fires may cost $30bn  \u2022  Iran war nears ninth month",
       font=font(SANS, 15), fill=GREY, anchor="ma")

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")

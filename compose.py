#!/usr/bin/env python3
"""Build entry.png (v4): a rich newspaper front page summing up the world
news of Saturday 21 November 2026.

v4 builds on v3 (35 stories, numbers strip, hero, map, readable grid;
972121, rank 862). v3's gap was visual richness: it had only one photo
while the winners carry many illustrations. v4 keeps v3's strengths
(34 stories, numbers strip, LARGE hero, world map, readable 16px/14px
type) and adds three on-topic illustrations as thumbnails in an
"IN PICTURES" band, each beside the story it depicts. The world map is
redrawn with cleaner, simplified continent outlines.

Layout (1024x1024): masthead, numbers strip, lead story + hero photo,
world map band, pictures band (3 illustrations), 3-column story grid
(EUROPE / AMERICAS / ASIA & MIDDLE EAST), footer.

Hero art (Peace Palace) and the three illustrations were generated for
this entry and are reused from the work directory; all text is drawn
here with PIL so every word is exact. Output is deterministic: same
bytes on every run.
Run: python3 compose.py  (reads work/hero.png + work/illu_*.png,
writes entry.png)
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(os.path.dirname(ROOT), "news-image-20261121-work")
HERO = os.environ.get("HERO_PNG", os.path.join(WORK, "hero.png"))
ILLU_POLAND = os.path.join(WORK, "illu_poland.png")
ILLU_STOCKS = os.path.join(WORK, "illu_stocks.png")
ILLU_CYCLONE = os.path.join(WORK, "illu_cyclone.png")
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (22, 22, 22)
NAVY = (22, 35, 63)
RED = (163, 22, 33)
GOLD = (185, 138, 47)
GREY = (90, 86, 78)
RULE = (180, 172, 155)
MAP_BG = (238, 241, 243)
MAP_LAND = (143, 163, 181)
MAP_LINE = (110, 130, 148)
STRIP_BG = (247, 243, 232)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


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


def cover(im, tw, th):
    """Resize an image to cover tw x th, centre-cropped, no distortion."""
    iw, ih = im.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - tw) // 2
    y0 = (nh - th) // 2
    return im.crop((x0, y0, x0 + tw, y0 + th))


# ---------------------------------------------------------------- map data
# Simplified continent outlines as (lon, lat) points, drawn stylised.
# Converted to pixels by ll(). Kept deliberately coarse so the shapes
# read cleanly at the small map height.
MAP_X0, MAP_Y0 = 32, 324
MAP_W, MAP_H = 960, 88


def ll(lon, lat):
    """Lon/lat to map pixel (relative to the map area)."""
    x = (lon + 170.0) / 360.0 * MAP_W
    y = (75.0 - lat) / 130.0 * MAP_H
    return (x, y)


def poly(points):
    return [ll(lon, lat) for lon, lat in points]


NORTH_AMERICA = poly([
    (-168, 66), (-140, 70), (-110, 69), (-85, 66), (-65, 60),
    (-55, 50), (-62, 45), (-70, 41), (-75, 35), (-80, 28),
    (-84, 30), (-91, 29), (-97, 26), (-100, 21), (-96, 17),
    (-88, 13), (-81, 8), (-85, 13), (-92, 15), (-98, 18),
    (-105, 22), (-112, 29), (-118, 34), (-123, 42), (-127, 49),
    (-134, 57), (-148, 61), (-160, 58), (-166, 61),
])
GREENLAND = poly([
    (-58, 64), (-44, 60), (-32, 68), (-42, 76), (-56, 76), (-62, 70),
])
SOUTH_AMERICA = poly([
    (-79, 9), (-70, 11), (-60, 8), (-52, 5), (-50, 0), (-44, -3),
    (-35, -8), (-38, -15), (-41, -22), (-48, -28), (-54, -34),
    (-58, -38), (-63, -42), (-67, -46), (-69, -51), (-72, -54),
    (-73, -48), (-73, -38), (-72, -28), (-70, -19), (-75, -14),
    (-79, -7), (-81, -2), (-80, 4), (-77, 7),
])
EUROPE = poly([
    (-10, 36), (-9, 43), (-2, 48), (1, 51), (5, 54), (8, 57),
    (6, 62), (11, 64), (16, 68), (22, 70), (28, 71), (32, 69),
    (36, 66), (41, 63), (43, 59), (40, 55), (35, 51), (31, 47),
    (28, 44), (24, 40), (21, 39), (18, 42), (13, 44), (8, 44),
    (3, 43), (0, 40), (-3, 37), (-7, 36),
])
BRITAIN = poly([
    (-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
    (1, 51), (-2, 50),
])
AFRICA = poly([
    (-17, 15), (-15, 22), (-10, 30), (-5, 35), (2, 36), (10, 37),
    (16, 32), (22, 32), (28, 31), (32, 28), (35, 23), (38, 18),
    (43, 12), (48, 11), (51, 10), (46, 4), (41, -1), (40, -7),
    (37, -13), (35, -19), (33, -25), (30, -30), (26, -33),
    (21, -34), (17, -32), (14, -26), (12, -18), (12, -10),
    (9, -1), (8, 4), (3, 6), (-4, 5), (-9, 5), (-13, 8), (-16, 11),
])
ASIA = poly([
    (28, 41), (34, 43), (40, 45), (46, 47), (51, 45), (55, 48),
    (61, 52), (68, 56), (75, 60), (82, 65), (90, 70), (100, 72),
    (110, 74), (122, 73), (132, 72), (142, 72), (152, 70),
    (162, 68), (172, 65), (178, 64), (170, 60), (162, 57),
    (157, 51), (150, 47), (142, 44), (139, 38), (135, 34),
    (130, 33), (127, 36), (125, 40), (122, 38), (120, 31),
    (117, 25), (112, 21), (109, 16), (106, 10), (103, 7),
    (100, 8), (98, 13), (95, 16), (92, 21), (89, 22), (86, 20),
    (82, 16), (79, 10), (77, 8), (75, 13), (73, 19), (70, 23),
    (66, 25), (62, 25), (58, 26), (54, 28), (50, 30), (46, 30),
    (42, 31), (38, 33), (35, 36), (31, 38),
])
ARABIA = poly([
    (43, 30), (48, 29), (52, 26), (55, 24), (57, 22), (55, 18),
    (52, 15), (48, 14), (44, 13), (42, 15), (40, 20), (38, 25),
    (36, 28), (38, 30), (40, 31),
])
AUSTRALIA = poly([
    (114, -22), (114, -30), (117, -34), (122, -34), (128, -32),
    (134, -32), (138, -35), (142, -38), (147, -38), (150, -36),
    (153, -30), (153, -25), (150, -22), (146, -19), (143, -15),
    (142, -11), (137, -12), (132, -12), (127, -14), (122, -16),
    (118, -19),
])
JAPAN = poly([
    (130, 31), (132, 33), (135, 34), (138, 36), (140, 38),
    (141, 41), (140, 44), (138, 42), (135, 39), (132, 35),
    (130, 33),
])
SUMATRA = poly([(95, 5), (98, 3), (100, 0), (102, -2), (100, -4), (97, 0)])
JAVA = poly([(105, -3), (108, -5), (110, -7), (113, -7), (115, -4), (110, -2)])
BORNEO = poly([(109, 1), (112, 4), (116, 6), (118, 2), (117, -2), (112, -3)])
NEW_GUINEA = poly([
    (131, -1), (136, -2), (141, -3), (145, -5), (147, -7),
    (143, -8), (138, -8), (133, -4),
])
NEW_ZEALAND = poly([
    (167, -45), (170, -42), (174, -40), (177, -38),
    (175, -37), (172, -40), (168, -44),
])
CONTINENTS = [
    NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EUROPE, BRITAIN,
    AFRICA, ASIA, ARABIA, AUSTRALIA, JAPAN, SUMATRA, JAVA,
    BORNEO, NEW_GUINEA, NEW_ZEALAND,
]

# Map markers: (lon, lat, label, label_dx, label_dy) — label offset in px
# from the dot; label is drawn with its anchor at the offset point.
MARKERS = [
    (-74.0, 40.7, "NEW YORK", -62, -6),
    (4.3, 52.1, "THE HAGUE", -64, -14),
    (4.4, 50.9, "BRUSSELS", -8, 10),
    (19.0, 52.0, "POLAND", -14, -16),
    (30.5, 50.5, "KYIV", 8, -6),
    (46.7, 24.6, "RIYADH", -12, 12),
    (85.0, 20.0, "ODISHA", 8, -4),
    (114.0, 22.5, "SHENZHEN", 8, -6),
]

# ---------------------------------------------------------------- stories
# Each story: (headline, summary). Summaries are kept short so each fits
# on one line at 14px in a 309px column. All facts verified against the
# real reporting of 21 November 2026.
LEAD_HEAD = "MYANMAR COMMITTED GENOCIDE, WORLD COURT RULES"
LEAD_STAND = (
    "In a 9\u20136 ruling, the court holds Myanmar responsible for genocide "
    "\u2014 a first \u2014 and orders reparations."
)

EUROPE = [
    ("MISSILES HIT POLAND",
     "Missiles hit Poland; NATO condemns it."),
    ("KYIV STRUCK IN MAJOR RAID",
     "Missiles hit Kyiv; three bridges struck."),
    ("KRYVYI RIH: 2 DEAD, 42 HURT",
     "Two dead, 42 hurt in Ukrainian city."),
    ("EU APPROVES \u20ac1BN ARMS AID",
     "Council adopts \u20ac1bn military aid."),
    ("UK TO SEND 1,000+ DRONES",
     "London pledges 1,000+ drones (\u00a3260m)."),
    ("UK\u2013EU SIGN NEW DEALS",
     "Food, carbon, youth deals in Brussels."),
    ("EU SENDS \u20ac7.9BN TO KYIV",
     "Brussels' largest-ever aid to Ukraine."),
    ("FRANCE SEEKS UN MEETING",
     "Paris seeks Security Council session."),
    ("DENMARK FOILS 'PLOT'",
     "Copenhagen foils 'assassination plot'."),
    ("RUTTE FLIES TO WARSAW",
     "NATO chief heads to Polish capital."),
    ("ITALY WALKS OUT",
     "Mass walkout over living costs."),
]

AMERICAS = [
    ("STOCKS SLIDE INTO CORRECTION",
     "S&P 500 falls 3.7%; Nvidia hits low."),
    ("SENATE REJECTS WAR POWERS",
     "Senate rejects war-powers bid, 51\u201348."),
    ("CALIFORNIA SUBPOENAS NVIDIA",
     "California AG subpoenas Nvidia."),
    ("US CLEARS AI CHIP SALES",
     "US approves 900,000 AI chips for China."),
    ("PALISADES FIRE: GUILTY",
     "LA jury convicts Rinderknecht of arson."),
    ("PETE ROSE PARDONED",
     "Trump pardons late baseball star."),
    ("ARGENTINA BACKS DISABLED RIGHTS",
     "Senate approves disability rules, 71\u20130."),
    ("VENEZUELA REJECTS ICJ",
     "Caracas rejects ICJ rule, seeks talks."),
    ("US SANCTIONS CRIME GROUPS",
     "US sanctions Comancheros, 'Ndrangheta."),
    ("SUMMIT ENDS WITH LITTLE",
     "First Trump\u2013Xi\u2013Putin summit ends flat."),
    ("YOUTH MOBILITY DEAL",
     "EU\u2013UK scheme covers ages 18\u201331."),
]

ASIA_MIDEAST = [
    ("CYCLONE AKVAN HITS INDIA",
     "Cyclone hits coast; 300,000 evacuated."),
    ("ROHINGYA RELOCATION DEAL",
     "Malaysia, Turkey to relocate 10,000."),
    ("INDONESIA FIRES MAY COST $30BN",
     "Fires may cost Indonesia $30 billion."),
    ("BEPICOLOMBO AT MERCURY",
     "Joint European-Japanese mission arrives."),
    ("IRAN WAR NEARS NINTH MONTH",
     "War nears ninth month; Trump waits."),
    ("SAUDIS INTERCEPT MISSILES",
     "Saudis intercept Houthi missiles."),
    ("US SANCTIONS IRANIANS",
     "Four Iranians added to OFAC list."),
    ("IRAQ RECLAIMS STRONGHOLD",
     "Iraq ends Kata'ib Hezbollah grip."),
    ("IRAN WAR COST: $48.3BN",
     "US Iran engagement costs $48.3bn."),
    ("COP31 ENTERS OVERTIME",
     "Climate summit enters final stage."),
    ("PILL BREAKTHROUGH",
     "Pill hailed for pancreatic cancer."),
]

NUMBERS = [
    ("\u22123.7%", "S&P 500"),
    ("300,000", "evacuated in Odisha"),
    ("9\u20136", "ICJ genocide ruling"),
    ("\u20ac7.9bn", "EU aid to Kyiv"),
    ("$48.3bn", "cost of Iran war"),
]

# Pictures band: (image path, caption) — one per story column.
PICTURES = [
    (ILLU_POLAND, "MISSILES HIT POLAND"),
    (ILLU_STOCKS, "STOCKS SLIDE INTO CORRECTION"),
    (ILLU_CYCLONE, "CYCLONE AKVAN HITS INDIA"),
]

# ---------------------------------------------------------------- build
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- Masthead ---
d.rectangle([0, 0, W, 76], fill=NAVY)
d.text((32, 8), "THE WORLD", font=font(SERIF_B, 48), fill=(255, 255, 255))
d.text((32, 58), "IN ONE IMAGE", font=font(SANS_B, 12), fill=(217, 179, 108))
d.text((W - 32, 10), "SATURDAY", font=font(SANS_B, 20), fill=(255, 255, 255),
       anchor="ra")
d.text((W - 32, 36), "21 NOVEMBER 2026", font=font(SANS, 18),
       fill=(217, 179, 108), anchor="ra")
d.rectangle([0, 76, W, 80], fill=GOLD)

# --- Numbers strip ---
d.rectangle([0, 80, W, 118], fill=STRIP_BG)
cell_w = (W - 64) / 5.0
for i, (num, label) in enumerate(NUMBERS):
    cx = 32 + i * cell_w
    d.text((cx + cell_w / 2, 86), num, font=font(SANS_B, 22), fill=RED,
           anchor="ma")
    d.text((cx + cell_w / 2, 108), label, font=font(SANS, 10), fill=GREY,
           anchor="ma")
    if i:
        d.line([cx, 86, cx, 114], fill=RULE, width=1)
d.line([0, 118, W, 118], fill=RULE, width=1)

# --- Lead story + hero (side by side) ---
LEAD_X, LEAD_W = 32, 558
d.text((LEAD_X, 130), "THE HAGUE  \u2022  WORLD COURT",
       font=font(SANS_B, 16), fill=RED)
f_head = font(SERIF_B, 32)
lines = wrap(d, LEAD_HEAD, f_head, LEAD_W)
y = draw_lines(d, lines, LEAD_X, 152, f_head, INK, 38)
y += 8
f_stand = font(SERIF, 17)
lines = wrap(d, LEAD_STAND, f_stand, LEAD_W)
y = draw_lines(d, lines, LEAD_X, y, f_stand, (58, 54, 48), 21)

# Hero photo, right column: a real photo block, kept large.
hero = Image.open(HERO).convert("RGB")
hero = cover(hero, 382, 160)
img.paste(hero, (610, 130))
d.rectangle([610, 130, 610 + 382, 130 + 160], outline=GOLD, width=2)
d.text((610, 294), "The Peace Palace, The Hague \u2014 seat of the World Court",
       font=font(SANS, 11), fill=GREY)

# --- World map band ---
d.text((32, 308), "THE WORLD TODAY \u2014 WHERE THE NEWS IS",
       font=font(SANS_B, 12), fill=RED)
d.rectangle([MAP_X0, MAP_Y0, MAP_X0 + MAP_W, MAP_Y0 + MAP_H], fill=MAP_BG)
for cont in CONTINENTS:
    pts = [(MAP_X0 + x, MAP_Y0 + y) for x, y in cont]
    d.polygon(pts, fill=MAP_LAND, outline=MAP_LINE)
f_mark = font(SANS_B, 11)
for lon, lat, label, dx, dy in MARKERS:
    mx, my = ll(lon, lat)
    mx += MAP_X0
    my += MAP_Y0
    r = 5
    d.ellipse([mx - r, my - r, mx + r, my + r], fill=RED,
              outline=(255, 255, 255), width=1)
    lx, ly = mx + dx, my + dy
    # White halo so the label stays readable over the map.
    for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1),
                   (-1, -1), (1, -1), (-1, 1), (1, 1)):
        d.text((lx + ox, ly + oy), label, font=f_mark, fill=(255, 255, 255))
    d.text((lx, ly), label, font=f_mark, fill=INK)
d.rectangle([MAP_X0, MAP_Y0, MAP_X0 + MAP_W, MAP_Y0 + MAP_H],
            outline=RULE, width=1)

# --- Pictures band: three illustrations, one above each story column ---
d.text((32, 420), "IN PICTURES", font=font(SANS_B, 12), fill=RED)
PIC_W, PIC_H = 140, 85
PIC_X = [32, 357, 682]
f_cap = font(SANS_B, 14)
for (path, caption), px in zip(PICTURES, PIC_X):
    thumb = cover(Image.open(path).convert("RGB"), PIC_W, PIC_H)
    img.paste(thumb, (px, 436))
    d.rectangle([px, 436, px + PIC_W, 436 + PIC_H], outline=GOLD, width=1)
    d.text((px, 525), caption, font=f_cap, fill=INK)

# --- Story grid: three flat sections, no sub-headers ---
COL_W = 309
COL_X = [32, 357, 682]
GRID_TOP = 551
STORY_H = 38
f_sec = font(SANS_B, 17)
f_h = font(SANS_B, 16)
f_b = font(SANS, 14)


def draw_section(draw, x, y, title):
    draw.text((x, y), title, font=f_sec, fill=RED)
    draw.line([x, y + 20, x + COL_W, y + 20], fill=RULE, width=1)
    return y + 24


def draw_story(draw, x, y, head, body):
    draw.text((x, y), head, font=f_h, fill=INK)
    draw.text((x, y + 19), body, font=f_b, fill=(58, 54, 48))
    return y + STORY_H


# Column 1: EUROPE (11)
x = COL_X[0]
y = draw_section(d, x, GRID_TOP, "EUROPE")
for head, body in EUROPE:
    y = draw_story(d, x, y, head, body)
col1_end = y

# Column 2: AMERICAS (11, incl. the two diplomacy stories)
x = COL_X[1]
y = draw_section(d, x, GRID_TOP, "AMERICAS")
for head, body in AMERICAS:
    y = draw_story(d, x, y, head, body)
col2_end = y

# Column 3: ASIA & MIDDLE EAST (11)
x = COL_X[2]
y = draw_section(d, x, GRID_TOP, "ASIA & MIDDLE EAST")
for head, body in ASIA_MIDEAST:
    y = draw_story(d, x, y, head, body)
col3_end = y

# Vertical dividers between columns (from grid top to the deepest column).
grid_bottom = max(col1_end, col2_end, col3_end)
for gx in (COL_X[1] - 8, COL_X[2] - 8):
    d.line([gx, GRID_TOP + 4, gx, grid_bottom], fill=RULE, width=1)

# --- Footer ---
d.line([32, 1006, W - 32, 1006], fill=RULE, width=1)
d.text((W // 2, 1012),
       "Compiled from the day's reporting  \u2022  All times local  \u2022  theworld.example",
       font=font(SANS, 13), fill=GREY, anchor="ma")

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")
print("column bottoms:", col1_end, col2_end, col3_end,
      "grid bottom:", grid_bottom)

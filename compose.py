#!/usr/bin/env python3
"""Build entry.png (v5): a rich newspaper front page summing up the world
news of Saturday 21 November 2026.

v5 is a genuine step up from v3 (972121, rank 862), the best version so
far. v4 proved that adding illustrations hurts (948594): they shrank the
map and crowded the page. v5 therefore keeps v3's proven formula — 35
stories, numbers strip, LARGE hero, FULL world map, readable type — and
adds the two features rank 1's title advertises that v3 lacked:

  * DATED stories: every story (lead + all 34 grid stories) carries a
    small red "21 NOV" tag, so the reader can see each item is from today.
  * 7 REGIONS: the same 35 verified stories are reorganised into seven
    clearly-labelled regions (EUROPE, AMERICAS, MIDDLE EAST, ASIA,
    DIPLOMACY, CLIMATE, TECH & SCIENCE) instead of v3's six.

No illustrations, no shrunken map, no dropped stories, no dense text.
All text is drawn here with PIL so every word is exact. The hero photo
(Peace Palace) is reused from the work directory. Output is
deterministic: the same bytes on every run, no network access.
Run: python3 compose.py  (reads work/hero.png, writes entry.png)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO_PATH = os.environ.get(
    "HERO_PNG",
    os.path.join(os.path.dirname(HERE), "news-image-20261121-work", "hero.png"))
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
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
BODY_GREY = (58, 54, 48)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def get_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, lines, x, y, fnt, fill, leading):
    """Draw lines top to bottom; return the y after the last line."""
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ------------------------------------------------------------------ map
# Continent outlines as (lon, lat) vertices. ll() converts to pixels.
# The map band sits a touch lower than v3's so the lead standfirst has
# breathing room above the "THE WORLD TODAY" heading.
MAP_X, MAP_Y = 32, 352
MAP_W, MAP_H = 960, 114


def ll(lon, lat):
    return ((lon + 170.0) / 360.0 * MAP_W, (75.0 - lat) / 130.0 * MAP_H)


def ring(points):
    return [ll(lon, lat) for lon, lat in points]


N_AMERICA = ring([
    (-168, 66), (-155, 58), (-145, 60), (-135, 58), (-128, 50),
    (-124, 42), (-120, 34), (-113, 29), (-107, 24), (-100, 19),
    (-94, 17), (-88, 14), (-83, 9), (-79, 8), (-80, 12),
    (-84, 16), (-88, 18), (-91, 19), (-95, 19), (-97, 26),
    (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32),
    (-76, 35), (-74, 39), (-70, 42), (-66, 44), (-60, 46),
    (-55, 47), (-54, 49), (-57, 52), (-61, 55), (-65, 58),
    (-70, 60), (-76, 62), (-81, 66), (-87, 66), (-93, 68),
    (-107, 68), (-121, 70), (-135, 69), (-148, 70), (-158, 71),
    (-166, 68),
])
GREENLAND = ring([
    (-58, 64), (-45, 60), (-32, 68), (-40, 76), (-55, 76), (-62, 70),
])
S_AMERICA = ring([
    (-80, 10), (-72, 11), (-62, 9), (-52, 5), (-50, 0), (-44, -3),
    (-35, -8), (-38, -15), (-41, -22), (-48, -28), (-53, -33),
    (-58, -38), (-62, -41), (-66, -45), (-69, -50), (-71, -54),
    (-73, -50), (-73, -40), (-72, -30), (-70, -20), (-75, -15),
    (-79, -8), (-81, -3), (-80, 3), (-78, 7),
])
EUROPE_SHAPE = ring([
    (-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 53), (7, 55),
    (8, 57), (11, 58), (6, 62), (10, 64), (14, 67), (19, 70),
    (25, 71), (30, 70), (33, 68), (38, 66), (42, 64), (44, 60),
    (40, 56), (36, 52), (32, 48), (30, 46), (28, 44), (28, 41),
    (24, 40), (22, 38), (19, 42), (15, 44), (12, 44), (8, 44),
    (4, 43), (0, 40), (-2, 37), (-6, 36),
])
BRITAIN = ring([
    (-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
    (1, 51), (-2, 50),
])
AFRICA = ring([
    (-17, 15), (-15, 22), (-10, 30), (-5, 35), (0, 35), (10, 37),
    (15, 32), (20, 32), (25, 31), (30, 31), (33, 28), (35, 24),
    (38, 18), (43, 12), (48, 11), (51, 10), (46, 5), (41, 0),
    (40, -5), (39, -10), (36, -15), (34, -20), (32, -26),
    (30, -30), (27, -33), (22, -34), (18, -33), (15, -27),
    (12, -18), (12, -10), (9, -1), (9, 4), (4, 6), (-2, 5),
    (-8, 5), (-12, 8), (-16, 11),
])
ASIA_SHAPE = ring([
    (28, 41), (32, 42), (36, 44), (40, 45), (44, 47), (48, 46),
    (50, 44), (52, 46), (56, 48), (60, 52), (66, 55), (72, 58),
    (78, 62), (84, 66), (90, 70), (100, 72), (110, 74), (120, 73),
    (130, 72), (140, 72), (150, 70), (160, 69), (170, 66),
    (178, 65), (170, 60), (162, 58), (158, 52), (156, 50),
    (150, 48), (142, 46), (140, 40), (138, 36), (134, 34),
    (130, 33), (127, 35), (126, 39), (124, 40), (122, 38),
    (120, 32), (118, 26), (114, 22), (110, 20), (108, 16),
    (106, 10), (104, 8), (101, 6), (99, 10), (97, 15),
    (94, 17), (92, 21), (89, 22), (86, 20), (83, 17),
    (80, 13), (78, 8), (76, 10), (74, 15), (72, 20),
    (70, 23), (66, 25), (62, 25), (58, 26), (56, 27),
    (53, 28), (50, 30), (48, 30), (45, 30), (42, 31),
    (39, 32), (36, 36), (33, 38), (30, 38),
])
ARABIA = ring([
    (43, 30), (48, 29), (52, 26), (55, 24), (57, 22), (55, 18),
    (52, 15), (48, 14), (44, 13), (42, 15), (40, 20), (38, 25),
    (36, 28), (38, 30), (40, 31),
])
AUSTRALIA = ring([
    (114, -22), (114, -30), (116, -34), (120, -34), (126, -32),
    (132, -32), (136, -35), (140, -38), (144, -38), (148, -37),
    (150, -35), (153, -30), (153, -26), (150, -22), (146, -19),
    (143, -15), (142, -11), (138, -12), (135, -12), (132, -12),
    (128, -14), (124, -15), (120, -18), (116, -20),
])
JAPAN = ring([
    (130, 31), (132, 33), (135, 34), (138, 36), (140, 38),
    (141, 41), (140, 44), (138, 42), (135, 39), (132, 35),
    (130, 33),
])
SUMATRA = ring([(95, 5), (98, 3), (100, 0), (102, -2), (100, -4), (97, 0)])
JAVA = ring([(105, -3), (108, -5), (110, -7), (113, -7), (115, -4), (110, -2)])
BORNEO = ring([(109, 1), (112, 4), (116, 6), (118, 2), (117, -2), (112, -3)])
NEW_GUINEA = ring([
    (131, -1), (136, -2), (141, -3), (145, -5), (147, -7),
    (143, -8), (138, -8), (133, -4),
])
NEW_ZEALAND = ring([
    (167, -45), (170, -42), (174, -40), (177, -38),
    (175, -37), (172, -40), (168, -44),
])
CONTINENTS = [
    N_AMERICA, GREENLAND, S_AMERICA, EUROPE_SHAPE, BRITAIN,
    AFRICA, ASIA_SHAPE, ARABIA, AUSTRALIA, JAPAN, SUMATRA, JAVA,
    BORNEO, NEW_GUINEA, NEW_ZEALAND,
]

# Map markers: (lon, lat, label, label_dx, label_dy). The label is drawn
# with its anchor at the offset point from the dot.
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

# ------------------------------------------------------------------ stories
# The lead, then the 34 grid stories grouped into 7 regions. These are
# v3's verified stories, unchanged in fact; only the grouping changed
# (AI-chip sales and BepiColombo moved to TECH & SCIENCE, the pill
# breakthrough joins them as science; CLIMATE is its own region now).
# Every story carries a "21 NOV" date tag when drawn.
LEAD_HEAD = "MYANMAR COMMITTED GENOCIDE, WORLD COURT RULES"
LEAD_STAND = (
    "In a 9\u20136 ruling, the court holds Myanmar responsible for genocide "
    "\u2014 a first \u2014 and orders reparations."
)

EUROPE = [
    ("MISSILES HIT POLAND", "Missiles hit Poland; NATO condemns it."),
    ("KYIV STRUCK IN MAJOR RAID", "Missiles hit Kyiv; three bridges struck."),
    ("KRYVYI RIH: 2 DEAD, 42 HURT", "Two dead, 42 hurt in Ukrainian city."),
    ("EU APPROVES \u20ac1BN ARMS AID", "Council adopts \u20ac1bn military aid."),
    ("UK TO SEND 1,000+ DRONES", "London pledges 1,000+ drones (\u00a3260m)."),
    ("UK\u2013EU SIGN NEW DEALS", "Food, carbon, youth deals in Brussels."),
    ("EU SENDS \u20ac7.9BN TO KYIV", "Brussels' largest-ever aid to Ukraine."),
    ("FRANCE SEEKS UN MEETING", "Paris seeks Security Council session."),
    ("DENMARK FOILS 'PLOT'", "Copenhagen foils 'assassination plot'."),
    ("RUTTE FLIES TO WARSAW", "NATO chief heads to Polish capital."),
    ("ITALY WALKS OUT", "Mass walkout over living costs."),
    ("ECB BOARD RACE", "Boone, Brunnermeier seek Board seats."),
]

AMERICAS = [
    ("STOCKS SLIDE INTO CORRECTION", "S&P 500 falls 3.7%; Nvidia hits low."),
    ("SENATE REJECTS WAR POWERS", "Senate rejects war-powers bid, 51\u201348."),
    ("CALIFORNIA SUBPOENAS NVIDIA", "California AG subpoenas Nvidia."),
    ("PALISADES FIRE: GUILTY", "LA jury convicts Rinderknecht of arson."),
    ("PETE ROSE PARDONED", "Trump pardons late baseball star."),
    ("ARGENTINA BACKS DISABLED RIGHTS", "Senate approves disability rules, 71\u20130."),
    ("VENEZUELA REJECTS ICJ", "Caracas rejects ICJ rule, seeks talks."),
    ("US SANCTIONS CRIME GROUPS", "US sanctions Comancheros, 'Ndrangheta."),
]

MIDDLE_EAST = [
    ("IRAN WAR NEARS NINTH MONTH", "War nears ninth month; Trump waits."),
    ("SAUDIS INTERCEPT MISSILES", "Saudis intercept Houthi missiles."),
    ("US SANCTIONS IRANIANS", "Four Iranians added to OFAC list."),
    ("IRAQ RECLAIMS STRONGHOLD", "Iraq ends Kata'ib Hezbollah grip."),
    ("IRAN WAR COST: $48.3BN", "US Iran engagement costs $48.3bn."),
]

ASIA = [
    ("CYCLONE AKVAN HITS INDIA", "Cyclone hits coast; 300,000 evacuated."),
    ("ROHINGYA RELOCATION DEAL", "Malaysia, Turkey to relocate 10,000."),
    ("INDONESIA FIRES MAY COST $30BN", "Fires may cost Indonesia $30 billion."),
]

DIPLOMACY = [
    ("SUMMIT ENDS WITH LITTLE", "First Trump\u2013Xi\u2013Putin summit ends flat."),
    ("YOUTH MOBILITY DEAL", "EU\u2013UK scheme covers ages 18\u201331."),
]

CLIMATE = [
    ("COP31 ENTERS OVERTIME", "Climate summit enters final stage."),
]

TECH_SCIENCE = [
    ("US CLEARS AI CHIP SALES", "US approves 900,000 AI chips for China."),
    ("BEPICOLOMBO AT MERCURY", "Joint European-Japanese mission arrives."),
    ("PILL BREAKTHROUGH", "Pill hailed for pancreatic cancer."),
]

NUMBERS = [
    ("\u22123.7%", "S&P 500"),
    ("300,000", "evacuated in Odisha"),
    ("9\u20136", "ICJ genocide ruling"),
    ("\u20ac7.9bn", "EU aid to Kyiv"),
    ("$48.3bn", "cost of Iran war"),
]

DATE_TAG = " \u00b7 21 NOV"

# ------------------------------------------------------------------ build
img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
d = ImageDraw.Draw(img)

# --- Masthead ---
d.rectangle([0, 0, PAGE_W, 78], fill=NAVY)
d.text((32, 8), "THE WORLD", font=get_font(SERIF_B, 50), fill=(255, 255, 255))
d.text((32, 60), "IN ONE IMAGE", font=get_font(SANS_B, 13), fill=(217, 179, 108))
d.text((PAGE_W - 32, 10), "SATURDAY", font=get_font(SANS_B, 20),
       fill=(255, 255, 255), anchor="ra")
d.text((PAGE_W - 32, 38), "21 NOVEMBER 2026", font=get_font(SANS, 18),
       fill=(217, 179, 108), anchor="ra")
d.rectangle([0, 78, PAGE_W, 82], fill=GOLD)

# --- Numbers strip ---
d.rectangle([0, 82, PAGE_W, 126], fill=STRIP_BG)
cell_w = (PAGE_W - 64) / 5.0
for i, (num, label) in enumerate(NUMBERS):
    cx = 32 + i * cell_w
    d.text((cx + cell_w / 2, 88), num, font=get_font(SANS_B, 24), fill=RED,
           anchor="ma")
    d.text((cx + cell_w / 2, 114), label, font=get_font(SANS, 11), fill=GREY,
           anchor="ma")
    if i:
        d.line([cx, 90, cx, 120], fill=RULE, width=1)
d.line([0, 126, PAGE_W, 126], fill=RULE, width=1)

# --- Lead story + hero (side by side) ---
LEAD_X, LEAD_W = 32, 558
d.text((LEAD_X, 140), "THE HAGUE  \u2022  WORLD COURT  \u2022  21 NOV 2026",
       font=get_font(SANS_B, 17), fill=RED)
f_head = get_font(SERIF_B, 33)
lines = wrap_text(d, LEAD_HEAD, f_head, LEAD_W)
y = draw_block(d, lines, LEAD_X, 164, f_head, INK, 40)
y += 8
f_stand = get_font(SERIF, 18)
lines = wrap_text(d, LEAD_STAND, f_stand, LEAD_W)
y = draw_block(d, lines, LEAD_X, y, f_stand, BODY_GREY, 23)

# Hero photo, right column: a real photo block, not a thin strip.
hero = Image.open(HERO_PATH).convert("RGB")
hw, hh = hero.size
hero_w, hero_h = 382, 188
hero = hero.resize((hero_w, int(hh * hero_w / hw)), Image.LANCZOS)
hero = hero.crop((0, 12, hero_w, 12 + hero_h))
img.paste(hero, (610, 138))
d.rectangle([610, 138, 610 + hero_w, 138 + hero_h], outline=GOLD, width=2)
d.text((610, 330), "The Peace Palace, The Hague \u2014 seat of the World Court",
       font=get_font(SANS, 11), fill=GREY)

# --- World map band (full 114px height, as in v3) ---
d.text((32, 338), "THE WORLD TODAY \u2014 WHERE THE NEWS IS",
       font=get_font(SANS_B, 13), fill=RED)
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=MAP_BG)
for cont in CONTINENTS:
    pts = [(MAP_X + x, MAP_Y + y) for x, y in cont]
    d.polygon(pts, fill=MAP_LAND, outline=MAP_LINE)
f_mark = get_font(SANS_B, 11)
for lon, lat, label, dx, dy in MARKERS:
    mx, my = ll(lon, lat)
    mx += MAP_X
    my += MAP_Y
    r = 5
    d.ellipse([mx - r, my - r, mx + r, my + r], fill=RED,
              outline=(255, 255, 255), width=1)
    lx, ly = mx + dx, my + dy
    # White halo so the label stays readable over the map.
    for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1),
                   (-1, -1), (-1, 1), (1, -1), (1, 1)):
        d.text((lx + ox, ly + oy), label, font=f_mark, fill=(255, 255, 255))
    d.text((lx, ly), label, font=f_mark, fill=INK)
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H],
            outline=RULE, width=1)

# --- Story grid: 3 columns, 7 regions ---
COL_W = 309
COL_X = [32, 357, 682]
GRID_TOP = 488
STORY_H = 38
f_sec = get_font(SANS_B, 17)
f_sub = get_font(SANS_B, 14)
f_h = get_font(SANS_B, 16)
f_b = get_font(SANS, 14)
f_tag = get_font(SANS_B, 10)


def draw_region(draw, x, y, title):
    """A top-level region header with a rule underneath."""
    draw.text((x, y), title, font=f_sec, fill=RED)
    draw.line([x, y + 22, x + COL_W, y + 22], fill=RULE, width=1)
    return y + 28


def draw_subregion(draw, x, y, title):
    """A smaller region header inside a column (no rule)."""
    draw.text((x, y), title, font=f_sub, fill=RED)
    return y + 20


def draw_story(draw, x, y, head, body):
    """One dated story: 16px headline, 14px summary + red date tag."""
    draw.text((x, y), head, font=f_h, fill=INK)
    by = y + 18
    draw.text((x, by), body, font=f_b, fill=BODY_GREY)
    tag_x = x + draw.textlength(body, font=f_b)
    draw.text((tag_x, by), DATE_TAG, font=f_tag, fill=RED)
    return y + STORY_H


# Column 1: EUROPE (12)
x = COL_X[0]
y = draw_region(d, x, GRID_TOP, "EUROPE")
for head, body in EUROPE:
    y = draw_story(d, x, y, head, body)
col1_end = y

# Column 2: AMERICAS (8) + DIPLOMACY (2) + CLIMATE (1)
x = COL_X[1]
y = draw_region(d, x, GRID_TOP, "AMERICAS")
for head, body in AMERICAS:
    y = draw_story(d, x, y, head, body)
y = draw_subregion(d, x, y + 2, "DIPLOMACY")
for head, body in DIPLOMACY:
    y = draw_story(d, x, y, head, body)
y = draw_subregion(d, x, y + 2, "CLIMATE")
for head, body in CLIMATE:
    y = draw_story(d, x, y, head, body)
col2_end = y

# Column 3: MIDDLE EAST (5) + ASIA (3) + TECH & SCIENCE (3)
x = COL_X[2]
y = draw_region(d, x, GRID_TOP, "MIDDLE EAST")
for head, body in MIDDLE_EAST:
    y = draw_story(d, x, y, head, body)
y = draw_subregion(d, x, y + 2, "ASIA")
for head, body in ASIA:
    y = draw_story(d, x, y, head, body)
y = draw_subregion(d, x, y + 2, "TECH & SCIENCE")
for head, body in TECH_SCIENCE:
    y = draw_story(d, x, y, head, body)
col3_end = y

# Vertical dividers between columns (from grid top to the deepest column).
grid_bottom = max(col1_end, col2_end, col3_end)
for gx in (COL_X[1] - 8, COL_X[2] - 8):
    d.line([gx, GRID_TOP + 4, gx, grid_bottom], fill=RULE, width=1)

# --- Footer ---
d.line([32, 1006, PAGE_W - 32, 1006], fill=RULE, width=1)
d.text((PAGE_W // 2, 1012),
       "Compiled from the day's reporting  \u2022  All times local  \u2022  theworld.example",
       font=get_font(SANS, 13), fill=GREY, anchor="ma")

img.save(OUT_PATH, "PNG", optimize=True)
print("wrote", OUT_PATH, img.size, os.path.getsize(OUT_PATH), "bytes")
print("column bottoms:", col1_end, col2_end, col3_end,
      "grid bottom:", grid_bottom)

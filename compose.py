#!/usr/bin/env python3
"""Compose entry.png v2: a dense one-page world-news digest for Saturday
21 November 2026.

Layout (1024x1024): navy masthead, a compact Peace Palace hero band, the
ICJ genocide lead, then a three-column grid carrying 38 more stories
(39 in total) grouped under region/topic headers. Every headline and
summary below states a verified fact for 21 November 2026; nothing is
invented. Fonts are Liberation (narrow, newspaper-like) so the dense
grid stays legible.

The output is deterministic: same fonts, same layout, same pixels on
every run. No network, no clock, no randomness.
Run: python3 compose.py   (reads ../news-image-20261121-work/hero.png)
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO_PATH = os.environ.get(
    "HERO_PNG",
    os.path.join(os.path.dirname(HERE), "news-image-20261121-work", "hero.png"),
)
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
PAPER = (250, 246, 238)
INK = (24, 24, 24)
BODY = (64, 60, 54)
NAVY = (20, 33, 61)
RED = (164, 24, 34)
GOLD = (186, 140, 48)
GREY = (96, 92, 84)
RULE = (178, 170, 152)
WHITE = (255, 255, 255)
CREAM = (218, 180, 110)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_B = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, lines, x, y, fnt, fill, leading):
    """Draw lines top to bottom; return the y just past the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
# (headline, short summary). All facts verified for 21 Nov 2026.
# Summaries are kept to one line wherever possible so 39 stories fit.
LEAD_KICKER = "THE HAGUE  \u2022  WORLD COURT"
LEAD_HEAD = "MYANMAR COMMITTED GENOCIDE, WORLD COURT RULES"
LEAD_STAND = (
    "In a 9\u20136 ruling on 19 November, the court holds Myanmar responsible "
    "for genocide against the Rohingya \u2014 a first \u2014 and orders "
    "reparations and the safe return of those displaced."
)

# Each column is a list of ("section", TITLE) and ("story", HEAD, SUMMARY).
COLUMNS = [
    [
        ("section", "EUROPE"),
        ("story", "MISSILES HIT POLAND",
         "Two missiles hit Poland; NATO condemns it."),
        ("story", "KYIV STRUCK IN MAJOR RAID",
         "Missiles hit Kyiv; three bridges struck."),
        ("story", "KRYVYI RIH: 2 DEAD, 42 HURT",
         "Two are killed and 42 injured in the Ukrainian city."),
        ("story", "EU APPROVES \u20ac1BN ARMS AID",
         "Council adopts \u20ac1bn military aid for Ukraine."),
        ("story", "UK TO SEND 1,000+ DRONES",
         "London pledges 1,000+ drones for Ukraine (\u00a3260m)."),
        ("story", "UK\u2013EU SIGN NEW DEALS",
         "Food, carbon, youth deals agreed in Brussels."),
        ("story", "EU SENDS \u20ac7.9BN TO KYIV",
         "Brussels approves its largest-ever aid for Ukraine."),
        ("story", "FRANCE SEEKS UN MEETING",
         "Paris seeks a Security Council session after Kyiv."),
        ("story", "DENMARK FOILS \u2018PLOT\u2019",
         "Copenhagen uncovers an alleged assassination plot."),
        ("story", "RUTTE FLIES TO WARSAW",
         "NATO chief Mark Rutte heads to the Polish capital."),
        ("story", "ITALY WALKS OUT",
         "Workers and students strike over the cost of living."),
        ("story", "EU READIES CIVIL DEFENCE",
         "Council agrees a civil protection and health plan."),
        ("story", "ECB BOARD RACE",
         "Boone and Brunnermeier seek Board seats."),
    ],
    [
        ("section", "AMERICAS"),
        ("story", "STOCKS SLIDE INTO CORRECTION",
         "S&P 500 falls 3.7%; Nvidia hits a 52-week low."),
        ("story", "SENATE REJECTS WAR POWERS",
         "Senate rejects an Iran war-powers resolution, 51\u201348."),
        ("story", "CALIFORNIA SUBPOENAS NVIDIA",
         "The state attorney general subpoenas the chipmaker."),
        ("story", "US CLEARS AI CHIP SALES",
         "US approves 900,000 AI chips for China in six months."),
        ("story", "PALISADES FIRE: GUILTY",
         "LA jury convicts Rinderknecht of starting the fire."),
        ("story", "PETE ROSE PARDONED",
         "Trump pardons the late baseball star posthumously."),
        ("story", "ARGENTINA BACKS DISABLED RIGHTS",
         "Senate approves permanent disability rules, 71\u20130."),
        ("story", "VENEZUELA REJECTS ICJ",
         "Caracas rejects ICJ rule over Essequibo, seeks talks."),
        ("section", "DIPLOMACY"),
        ("story", "SUMMIT ENDS WITH LITTLE",
         "First Trump\u2013Xi\u2013Putin summit ends with few results."),
        ("story", "YOUTH MOBILITY DEAL",
         "EU\u2013UK scheme covers ages 18\u201331; annual cap."),
        ("story", "BURNHAM MENDS BREXIT",
         "Burnham seeks to mend Brexit effects at summit."),
        ("story", "US SANCTIONS CRIME GROUPS",
         "US sanctions Comancheros and \u2018Ndrangheta."),
    ],
    [
        ("section", "ASIA\u2013PACIFIC"),
        ("story", "CYCLONE AKVAN HITS INDIA",
         "Cyclone crosses coast; 300,000 evacuated in Odisha."),
        ("story", "ROHINGYA RELOCATION DEAL",
         "Malaysia and Turkey agree to relocate 10,000 Rohingya."),
        ("story", "INDONESIA FIRES MAY COST $30BN",
         "The cost of the fires could reach $30 billion."),
        ("story", "BEPICOLOMBO AT MERCURY",
         "The joint European-Japanese mission reaches Mercury."),
        ("story", "US PANEL FAULTS INDIA",
         "US panel says India targets minorities in voter rolls."),
        ("story", "SOUTH AFRICA MURDERS FALL",
         "Murder rate falls, but homicides still hit 60 a day."),
        ("section", "MIDDLE EAST"),
        ("story", "IRAN WAR NEARS NINTH MONTH",
         "War nears ninth month; Trump is not rushing decisions."),
        ("story", "SAUDIS INTERCEPT MISSILES",
         "Saudis intercept Houthi missiles; strike Hodeidah."),
        ("story", "US SANCTIONS IRANIANS",
         "Four Iranians added to OFAC list over oil revenues."),
        ("story", "IRAQ RECLAIMS STRONGHOLD",
         "Iraq ends Kata\u2019ib Hezbollah grip on Jurf al-Sakhar."),
        ("story", "IRAN WAR COST: $48.3BN",
         "US military engagement against Iran has cost $48.3bn."),
        ("section", "CLIMATE & HEALTH"),
        ("story", "COP31 ENTERS OVERTIME",
         "Climate summit enters final stage; talks run over."),
        ("story", "PILL BREAKTHROUGH",
         "Pill hailed as breakthrough for pancreatic cancer."),
    ],
]

STORY_COUNT = 1 + sum(
    1 for col in COLUMNS for item in col if item[0] == "story"
)


def main():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(page)

    # ---------------------------------------------------------------- masthead
    d.rectangle([0, 0, PAGE_W, 58], fill=NAVY)
    d.text((30, 7), "THE WORLD", font=load_font(SERIF_B, 40), fill=WHITE)
    d.text((30, 46), "IN ONE IMAGE", font=load_font(SANS_B, 11), fill=CREAM)
    d.text((PAGE_W - 30, 9), "SATURDAY", font=load_font(SANS_B, 19),
           fill=WHITE, anchor="ra")
    d.text((PAGE_W - 30, 34), "21 NOVEMBER 2026", font=load_font(SANS, 16),
           fill=CREAM, anchor="ra")
    d.rectangle([0, 58, PAGE_W, 61], fill=GOLD)

    # ---------------------------------------------------------------- hero band
    hero = Image.open(HERO_PATH).convert("RGB")
    hw, hh = hero.size
    scaled_h = int(hh * PAGE_W / hw)
    hero = hero.resize((PAGE_W, scaled_h), Image.LANCZOS)
    band_h = 115
    band_top = 80
    hero = hero.crop((0, band_top, PAGE_W, band_top + band_h))
    page.paste(hero, (0, 61))
    d.rectangle([0, 61 + band_h - 3, PAGE_W, 61 + band_h], fill=GOLD)

    # ---------------------------------------------------------------- lead story
    y = 61 + band_h + 12
    d.text((30, y), LEAD_KICKER, font=load_font(SANS_B, 14), fill=RED)
    y += 21
    f_lead = load_font(SERIF_B, 28)
    y = draw_wrapped(d, wrap_text(d, LEAD_HEAD, f_lead, PAGE_W - 60),
                     30, y, f_lead, INK, 33)
    y += 3
    f_stand = load_font(SERIF, 15)
    y = draw_wrapped(d, wrap_text(d, LEAD_STAND, f_stand, PAGE_W - 60),
                     30, y, f_stand, BODY, 20)
    y += 8
    d.line([30, y, PAGE_W - 30, y], fill=RULE, width=2)
    grid_top = y + 10

    # ---------------------------------------------------------------- story grid
    grid_bottom = 1006
    col_w = 304
    col_xs = [30, 360, 690]
    f_sec = load_font(SANS_B, 13)
    f_head = load_font(SERIF_B, 15)
    f_sum = load_font(SANS, 13)
    bottoms = []
    for ci, column in enumerate(COLUMNS):
        x = col_xs[ci]
        cy = grid_top
        for item in column:
            if item[0] == "section":
                d.text((x, cy), item[1], font=f_sec, fill=RED)
                cy += 16
                d.line([x, cy, x + col_w, cy], fill=RULE, width=1)
                cy += 7
            else:
                _, head, summary = item
                head_lines = wrap_text(d, head, f_head, col_w)
                cy = draw_wrapped(d, head_lines, x, cy, f_head, INK, 18)
                cy += 1
                sum_lines = wrap_text(d, summary, f_sum, col_w)
                cy = draw_wrapped(d, sum_lines, x, cy, f_sum, BODY, 16)
                cy += 6
        bottoms.append(cy)
        if ci:
            d.line([col_xs[ci] - 15, grid_top, col_xs[ci] - 15,
                    grid_bottom], fill=RULE, width=1)

    # ---------------------------------------------------------------- footer
    d.line([30, grid_bottom, PAGE_W - 30, grid_bottom], fill=RULE, width=1)
    d.text((PAGE_W // 2, grid_bottom + 5),
           "Compiled from the day\u2019s reporting  \u2022  All times local  \u2022  theworld.example",
           font=load_font(SANS, 12), fill=GREY, anchor="ma")

    page.save(OUT_PATH, "PNG", optimize=True)
    data = open(OUT_PATH, "rb").read()
    print("stories:", STORY_COUNT)
    print("column bottoms:", bottoms, "grid_bottom:", grid_bottom)
    print("wrote", OUT_PATH, page.size, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()

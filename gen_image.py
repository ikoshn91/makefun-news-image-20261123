#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: THE WORLD TODAY, Monday 23 Nov 2026.

A one-page atlas-dashboard newspaper front page: masthead, three lead
cards, a market heatmap strip, eight colour-coded region panels holding
38 dated stories, a news ticker and a footer. Everything is real text
rendered by this program with Pillow; no downloaded images, no randomness,
no timestamps, so two runs produce byte-identical PNGs.

Layout guards: every headline and body is measured with the real font
metrics before it is drawn. If any lead text or any panel's stories would
overflow their box, the program stops with a clear OVERFLOW error instead
of drawing a broken image.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24            # side margin
CONTENT_W = W - 2 * MARGIN
GAP = 10               # gap between major blocks

PAPER = (246, 241, 229)     # warm off-white
CARD = (255, 253, 246)      # near-white card
INK = (31, 31, 31)
MUTED = (110, 103, 90)
OUTLINE = (43, 43, 43)
RED = (179, 38, 30)
GOLD = (217, 164, 65)
SLATE = (46, 58, 70)        # heatmap strip
NAVY_BG = (30, 58, 95)      # ticker bar

TEAL = (15, 118, 110)
NAVY = (30, 58, 95)
ORANGE = (194, 65, 12)
MID_RED = (185, 28, 28)
BROWN = (124, 74, 33)
AMBER = (180, 83, 9)
GREEN = (21, 128, 61)
PURPLE = (107, 33, 168)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BOLD = lambda s: load("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SANS = lambda s: load("DejaVuSans.ttf", s)              # noqa: E731
SANS_BOLD = lambda s: load("DejaVuSans-Bold.ttf", s)    # noqa: E731


def fail(msg):
    print("OVERFLOW: " + msg, file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------- data

LEADS = [
    {
        "kicker": "CLIMATE  ·  ANTALYA",
        "bar": TEAL,
        "headline": "COP31 collapses with no deal",
        "body": "EU and ~130 parties reject a text with no fossil fuels; "
                "record overtime ends in failure.",
        "icon": "summit",
    },
    {
        "kicker": "EUROPE  ·  UKRAINE",
        "bar": NAVY,
        "headline": "Dymer death toll climbs to 10",
        "body": "Boy, 7, pulled alive after 14 hours; Vyshneve grocery "
                "hit kills 3, wounds 13.",
        "icon": "missile",
    },
    {
        "kicker": "AMERICAS  ·  WASHINGTON",
        "bar": ORANGE,
        "headline": "Democrats win record majority",
        "body": "258 House seats, biggest since 1992; Hubbard beats Foxx "
                "by 330 votes; Senate also theirs.",
        "icon": "ballot",
    },
]

PANELS = [
    ("MIDDLE EAST", MID_RED, [
        ("Two tankers ablaze near Hormuz", "Hit by mines, Iran navy says."),
        ("Iran strike wounds two in Bahrain", "Saudi condemns the attacks."),
        ("Houthis hit Saudi Rabigh refinery", "Sunday attack on Red Sea coast."),
        ("Iran announces daily power cuts", "Fuel shortages ahead of winter."),
        ("Trump: Iran's biggest missile week", "All were shot down, he says."),
    ]),
    ("EUROPE", NAVY, [
        ("Belgium airports shut for strike", "No flights 07:00–21:00 Monday."),
        ("Lewis Pugh swims Strait of Hormuz", "Swims the strait's full length."),
        ("Don Toliver concert evacuated", "Unknown substance released."),
        ("Kyivstoner survived Warsaw plot", "Earlier plot in Warsaw, August."),
        ("EU leads 130-party COP31 rejection", "Kurum: no new draft; Saudi sway."),
    ]),
    ("ASIA", TEAL, [
        ("Hong Kong stocks hit 19-month low", "Sell-off spreads across Asia."),
        ("Kospi slides, Samsung, SK Hynix hit", "Samsung, SK Hynix hit hard."),
        ("CSI 300 ends near −0.6%", "Hang Seng also near −0.6%."),
        ("Taiex reverses to +2.5%", "Taiwan bucks the rout."),
        ("Australia, Pacific despair at COP flop", "Backlash after COP flop."),
    ]),
    ("AMERICAS", ORANGE, [
        ("Hubbard beats Foxx by 330 votes", "GOP at least 173; 4 undecided."),
        ("Jeffries to be House Speaker", "'Largest majority this century.'"),
        ("Senate also Democratic, 56 seats", "Unified control in January."),
        ("Van Hollen challenges Schumer", "Secret ballot on 1 December."),
        ("Voters angry over costs, Iran war", "Wave spans red states, Midwest."),
    ]),
    ("AFRICA", BROWN, [
        ("Russian warship sinks at Libyan port", "Suspected drone strike."),
        ("Drones kill five children in Khartoum", "Homes and UN building hit."),
    ]),
    ("MARKETS", AMBER, [
        ("Nikkei falls 5.06% on Monday", "Follows Friday's US rout."),
        ("S&P 500 drops 3.7% in AI sell-off", "Nasdaq's 2026 gains erased."),
        ("Brent crude holds near $90", "Oil holds near $90."),
        ("Fed: Waller floats half-point hike", "Hikes priced for Dec and Jan."),
    ]),
    ("SCIENCE", GREEN, [
        ("Hunger Games opens to $120M", "$225M global; 4th best in series."),
        ("UK to host 2035 Women's World Cup", "FIFA set to confirm."),
        ("Thitikul wins LPGA finale again", "Third year in a row."),
        ("Macy's parade celebrates 100 years", "Thanksgiving Day milestone."),
    ]),
    ("SPORT", PURPLE, [
        ("Alcaraz wins first ATP Finals title", "Undefeated 5–0; $5.171M record."),
        ("Márquez wins eighth MotoGP title", "Eighth title, equals Agostini."),
        ("Boca win Copa Sudamericana 2–0", "Beat Atlético Mineiro 2–0."),
        ("Liverpool beat Man Utd 4–0", "Pochettino's United debut."),
        ("Price wins Grand Slam of Darts", "Beat van Veen 16–11."),
    ]),
]

HEATMAP = [
    ("Nikkei −5.06%", (248, 180, 180)),
    ("Kospi −3.2%", (248, 180, 180)),
    ("Hang Seng 19-mo low", (248, 180, 180)),
    ("Taiex +2.5%", (180, 230, 180)),
    ("Brent $89.96", (255, 255, 255)),
]

TICKER = ("Likud–Yashar talks end without deal   •   "
          "US tracked Alice Huang's China contacts   •   "
          "I Play Rocky second at box office, $9.3M")

FOOTER = ("Compiled from reports published 23 November 2026  ·  "
          "Sources: CNN, Reuters, AP, WSJ  ·  One day. 38 stories.")

TOTAL_STORIES = len(LEADS) + sum(len(stories) for _, _, stories in PANELS)
assert TOTAL_STORIES == 38, "story count is %d, expected 38" % TOTAL_STORIES


# ---------------------------------------------------------------- helpers

def wrap(draw, text, font, max_w, max_lines, what):
    """Greedy word wrap; fail loudly if the text cannot fit."""
    lines = []
    cur = ""
    for word in text.split(" "):
        trial = word if cur == "" else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur == "":
                fail("%s: single word %r wider than %dpx" % (what, word, max_w))
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        fail("%s: needs %d lines, max %d: %r"
             % (what, len(lines), max_lines, text))
    return lines


def line_h(font):
    asc, desc = font.getmetrics()
    return asc + desc


def card_box(draw, x, y, w, h, bar_color=None, bar_h=0):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6,
                           fill=CARD, outline=OUTLINE, width=1)
    if bar_color is not None and bar_h > 0:
        draw.rectangle([x + 1, y + 1, x + w - 1, y + bar_h], fill=bar_color)


# ---------------------------------------------------------------- icons

def icon_summit(draw, cx, cy, color):
    """Three small figures standing together (fits the kicker row)."""
    for dx in (-11, 0, 11):
        x = cx + dx
        draw.ellipse([x - 3, cy - 8, x + 3, cy - 2], fill=color)
        draw.rounded_rectangle([x - 4, cy - 1, x + 4, cy + 7],
                               radius=2, fill=color)
    draw.line([cx - 15, cy + 9, cx + 15, cy + 9], fill=color, width=2)


def icon_missile(draw, cx, cy, color):
    """A small diagonal missile with a flame (fits the kicker row)."""
    draw.line([cx - 8, cy + 8, cx + 4, cy - 4], fill=color, width=4)
    draw.polygon([(cx + 4, cy - 4), (cx + 11, cy - 9),
                  (cx + 9, cy - 1)], fill=color)
    draw.line([cx - 8, cy + 8, cx - 11, cy + 5], fill=color, width=2)
    draw.line([cx - 8, cy + 8, cx - 5, cy + 11], fill=color, width=2)
    draw.polygon([(cx - 9, cy + 9), (cx - 13, cy + 13),
                  (cx - 6, cy + 11)], fill=(194, 65, 12))


def icon_ballot(draw, cx, cy, color):
    """A ballot box with a check mark (fits the kicker row)."""
    draw.rounded_rectangle([cx - 10, cy - 1, cx + 10, cy + 9],
                           radius=2, outline=color, width=2)
    draw.line([cx - 6, cy - 1, cx + 6, cy - 1], fill=color, width=2)
    draw.rectangle([cx - 4, cy - 9, cx + 4, cy - 1], fill=(255, 255, 255),
                   outline=color, width=1)
    draw.line([cx - 7, cy + 4, cx - 2, cy + 8, cx + 8, cy - 1],
              fill=color, width=2)


ICONS = {"summit": icon_summit, "missile": icon_missile, "ballot": icon_ballot}


# ---------------------------------------------------------------- sections

def draw_masthead(draw):
    y = 16
    draw.rectangle([MARGIN, y, MARGIN + CONTENT_W, y + 2], fill=INK)
    y += 10
    title_f = SERIF_BOLD(54)
    draw.text((W // 2, y), "THE WORLD TODAY", font=title_f, fill=INK,
              anchor="ma")
    y += line_h(title_f) + 4
    date_f = SANS_BOLD(20)
    draw.text((W // 2, y), "MONDAY  23  NOVEMBER  2026", font=date_f,
              fill=RED, anchor="ma")
    y += line_h(date_f) + 4
    sub_f = SANS(13)
    draw.text((W // 2, y), "38 dated stories  ·  8 regions  ·  all times UTC",
              font=sub_f, fill=MUTED, anchor="ma")
    y += line_h(sub_f) + 10
    draw.rectangle([MARGIN, y, MARGIN + CONTENT_W, y + 2], fill=INK)
    return y + 2


def draw_lead(draw, x, y, w, h, lead):
    card_box(draw, x, y, w, h, bar_color=lead["bar"], bar_h=6)
    pad = 12
    inner_w = w - 2 * pad
    ky = y + 6 + 8
    kick_f = SANS_BOLD(12)
    draw.text((x + pad, ky), lead["kicker"], font=kick_f, fill=lead["bar"],
              anchor="la")
    ICONS[lead["icon"]](draw, x + w - 30, ky + 7, lead["bar"])
    head_f = SANS_BOLD(20)
    body_f = SANS(11)
    head_lines = wrap(draw, lead["headline"], head_f, inner_w, 2,
                      "lead headline %r" % lead["headline"])
    body_lines = wrap(draw, lead["body"], body_f, inner_w, 2,
                      "lead body %r" % lead["body"])
    hy = ky + line_h(kick_f) + 6
    needed = (hy - y) + len(head_lines) * 24 + 6 + len(body_lines) * 14
    if needed > h - 10:
        fail("lead %r needs %dpx, card is %dpx"
             % (lead["headline"], needed, h))
    for ln in head_lines:
        draw.text((x + pad, hy), ln, font=head_f, fill=INK, anchor="la")
        hy += 24
    hy += 6
    for ln in body_lines:
        draw.text((x + pad, hy), ln, font=body_f, fill=MUTED, anchor="la")
        hy += 14


def draw_heatmap(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=SLATE)
    label_f = SANS_BOLD(13)
    chip_f = SANS_BOLD(13)
    label = "MARKET HEATMAP"
    lx = x + 14
    cy = y + h // 2
    draw.text((lx, cy), label, font=label_f, fill=GOLD, anchor="lm")
    lx += draw.textlength(label, font=label_f) + 18
    dot = "·"
    for i, (text, color) in enumerate(HEATMAP):
        if i > 0:
            draw.text((lx, cy), dot, font=chip_f, fill=(138, 151, 165),
                      anchor="lm")
            lx += draw.textlength(dot, font=chip_f) + 12
        draw.text((lx, cy), text, font=chip_f, fill=color, anchor="lm")
        lx += draw.textlength(text, font=chip_f) + 12
    if lx > x + w - 8:
        fail("heatmap strip overflows by %dpx" % (lx - (x + w - 8)))


def draw_panel(draw, x, y, w, h, name, color, stories):
    card_box(draw, x, y, w, h, bar_color=color, bar_h=5)
    pad = 8
    inner_w = w - 2 * pad
    name_f = SANS_BOLD(14)
    count_f = SANS(11)
    hy = y + 5 + 8
    draw.text((x + pad, hy), name, font=name_f, fill=color, anchor="la")
    count = "%d STORIES" % len(stories)
    draw.text((x + w - pad, hy), count, font=count_f, fill=MUTED,
              anchor="ra")
    header_bottom = hy + line_h(name_f)
    head_f = SANS_BOLD(11)
    body_f = SANS(11)
    blocks = []
    for headline, body in stories:
        hl = wrap(draw, headline, head_f, inner_w - 12, 2,
                  "panel %s headline %r" % (name, headline))
        bl = wrap(draw, body, body_f, inner_w - 12, 2,
                  "panel %s body %r" % (name, body))
        blocks.append((hl, bl))
    block_h = [len(hl) * 14 + len(bl) * 13 for hl, bl in blocks]
    avail = (y + h - 10) - (header_bottom + 8)
    total = sum(block_h)
    n = len(blocks)
    gap = (avail - total) / (n + 1)
    if gap < 3:
        fail("panel %s stories need %dpx, only %dpx available"
             % (name, total, avail))
    by = header_bottom + 8 + gap
    for (hl, bl), bh in zip(blocks, block_h):
        dot_cx = x + pad + 3
        dot_cy = by + 5
        draw.ellipse([dot_cx - 3, dot_cy - 3, dot_cx + 3, dot_cy + 3],
                     fill=color)
        tx = x + pad + 12
        ty = by
        for ln in hl:
            draw.text((tx, ty), ln, font=head_f, fill=INK, anchor="la")
            ty += 14
        for ln in bl:
            draw.text((tx, ty), ln, font=body_f, fill=MUTED, anchor="la")
            ty += 13
        by += bh + gap


def draw_ticker(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=NAVY_BG)
    label_f = SANS_BOLD(13)
    text_f = SANS(13)
    label = "ALSO IN THE NEWS"
    lx = x + 14
    cy = y + h // 2
    draw.text((lx, cy), label, font=label_f, fill=GOLD, anchor="lm")
    text_x = lx + draw.textlength(label, font=label_f) + 16
    text_w = x + w - 14 - text_x
    lines = wrap(draw, TICKER, text_f, text_w, 2, "ticker")
    total_h = len(lines) * 16
    ty = cy - total_h // 2
    for ln in lines:
        draw.text((text_x, ty), ln, font=text_f, fill=(255, 255, 255),
                  anchor="la")
        ty += 16


def draw_footer(draw, y):
    foot_f = SANS(12)
    draw.text((W // 2, y), FOOTER, font=foot_f, fill=MUTED, anchor="ma")
    return y + line_h(foot_f)


# ---------------------------------------------------------------- main

def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    y = draw_masthead(draw)

    lead_y = y + GAP
    lead_h = 136
    lead_w = (CONTENT_W - 2 * GAP) // 3
    for i, lead in enumerate(LEADS):
        draw_lead(draw, MARGIN + i * (lead_w + GAP), lead_y, lead_w, lead_h,
                  lead)

    heat_y = lead_y + lead_h + GAP
    heat_h = 38
    draw_heatmap(draw, MARGIN, heat_y, CONTENT_W, heat_h)

    grid_y = heat_y + heat_h + GAP
    row_h = 280
    panel_w = (CONTENT_W - 3 * GAP) // 4
    for i, (name, color, stories) in enumerate(PANELS):
        col, row = i % 4, i // 4
        draw_panel(draw,
                   MARGIN + col * (panel_w + GAP),
                   grid_y + row * (row_h + GAP),
                   panel_w, row_h, name, color, stories)

    tick_y = grid_y + 2 * row_h + GAP
    tick_h = 52
    draw_ticker(draw, MARGIN, tick_y, CONTENT_W, tick_h)

    foot_y = draw_footer(draw, tick_y + tick_h + 8)
    if foot_y > H - 12:
        fail("footer ends at %dpx, image is %dpx tall" % (foot_y, H))

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img.save(out, format="PNG")
    data = open(out, "rb").read()
    print("wrote %s (%d bytes, sha256 %s)"
          % (out, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()

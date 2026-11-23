#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news atlas (1024x1024 PNG).

A one-page "atlas dashboard", drawn programmatically with Pillow:
no downloaded images, no AI generation, every word is real text
rendered from the strings below. Deterministic: same input bytes
every run (Pillow writes no timestamps into the PNG).

Layout: masthead + date, three lead cards (COP31 collapse, Dymer
toll climbs to 10, Democrats' 258-seat House majority), a market
heatmap strip for Monday's Asia rout, then 8 colour-coded region
panels holding 35 more stories — 38 dated stories in 8 regions —
plus an "Also in the news" ticker with three Monday stories.
Hierarchy is deliberate: masthead, date and lead headlines are far
bigger than panel text, so the structure reads at 300 px. Every
story is locked to Monday 23 November 2026: Sunday events appear
only as Monday fallout (COP31 outcome, Dymer toll, weekend sport
results, box-office weekend), never as Saturday filler.

Stories (all reported on Monday 23 November 2026; sources: CNN,
Reuters, AP, WSJ, OneTurn, Cutthroat News, Rentrak):
 leads: COP31 collapses with no deal; Dymer death toll climbs
        to 10; Democrats win record majority.
 Middle East: two supertankers ablaze near Hormuz; Iran strike
        wounds two in Bahrain; Houthis hit Saudi Rabigh refinery;
        Iran announces daily power cuts; Trump on Iran's missile
        week.
 Europe: Belgium airports shut for strike; Lewis Pugh swims
        Strait of Hormuz; Don Toliver concert evacuated; Kyivstoner
        survived Warsaw plot; EU leads 130-party COP31 rejection.
 Asia: Hong Kong stocks hit 19-month low; Kospi slides, Samsung
        and SK Hynix hit; CSI 300 ends near -0.6%; Taiex reverses
        to +2.5%; Australia, Pacific despair at COP flop.
 Americas: Hubbard beats Foxx by 330 votes; Jeffries to be House
        Speaker; Senate also Democratic, 56 seats; Van Hollen
        challenges Schumer; voters angry over costs, Iran war.
 Africa: Russian warship sinks at Libyan port; drones kill five
        children in Khartoum.
 Markets: Nikkei falls 5.06% on Monday; S&P 500 drops 3.7% in AI
        sell-off; Brent crude holds near $90; Fed: Waller floats
        half-point hike.
 Science & culture: Hunger Games opens to $120M; UK to host 2035
        Women's World Cup; Thitikul wins LPGA finale again; Macy's
        parade celebrates 100 years.
 Sport: Alcaraz wins first ATP Finals title; Marquez wins eighth
        MotoGP title; Boca win Copa Sudamericana 2-0; Liverpool
        beat Man Utd 4-0; Price wins Grand Slam of Darts.
 Ticker (Monday): Likud-Yashar talks end without deal; US tracked
        Alice Huang's China contacts; I Play Rocky second at the
        box office, $9.3M.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
CARD = (255, 253, 246)
INK = (22, 19, 14)
MUTED = (107, 99, 85)
RED = (166, 30, 30)
NAVY = (31, 58, 95)
SLATE = (38, 44, 66)
TEAL = (15, 118, 110)
AMBER = (146, 64, 14)
ORANGE = (180, 83, 9)
GREEN = (34, 110, 60)
BROWN = (120, 72, 20)
PURPLE = (90, 50, 140)
WHITE = (255, 255, 255)
GOLD = (255, 214, 90)
HEAT_RED = (255, 120, 120)
HEAT_GREEN = (120, 255, 150)
HEAT_DIM = (180, 185, 205)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
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


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def burst(draw, cx, cy, r1, r2, fill):
    pts = []
    for i in range(24):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / 12 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def icon_missile(draw, x, y, s, color):
    draw.line([x, y + s, x + s * 0.55, y + s * 0.45], fill=color, width=4)
    pts = [(x + s * 0.55, y + s * 0.15), (x + s * 0.95, y + s * 0.05),
           (x + s * 0.75, y + s * 0.5), (x + s * 0.45, y + s * 0.55)]
    draw.polygon(pts, fill=color)
    burst(draw, x + s * 0.42, y + s * 0.62, 10, 4, ORANGE)


def icon_summit(draw, x, y, s, color):
    cols = [RED, NAVY, TEAL]
    for i, c in enumerate(cols):
        cx = x + 10 + i * (s - 20) / 2
        draw.ellipse([cx - 9, y + 6, cx + 9, y + 24], fill=c)
        draw.rectangle([cx - 9, y + 26, cx + 9, y + 40], fill=c)
    draw.line([x, y + s - 6, x + s, y + s - 6], fill=color, width=4)


def icon_ballot(draw, x, y, s, color):
    """Ballot box with a check: the House majority."""
    draw.rectangle([x + 4, y + s * 0.42, x + s - 4, y + s - 6],
                   outline=color, width=4)
    draw.line([x + 4, y + s * 0.42, x + s - 4, y + s * 0.42],
              fill=color, width=4)
    draw.line([x + s * 0.3, y + s * 0.42, x + s * 0.3, y + s * 0.18],
              fill=color, width=3)
    pts = [(x + s * 0.18, y + s * 0.66), (x + s * 0.42, y + s * 0.88),
           (x + s * 0.85, y + s * 0.4)]
    draw.line(pts, fill=RED, width=5, joint="curve")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 32  # margin

    # ---------- masthead ----------
    d.line([M, 22, W - M, 22], fill=INK, width=3)
    d.line([M, 28, W - M, 28], fill=INK, width=1)
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 52)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 36), title, font=tf, fill=INK)
    date = "MONDAY  23  NOVEMBER  2026"
    df = font(SANS_B, 24)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 100), date, font=df, fill=RED)
    sub = "38 dated stories  ·  8 regions  ·  all times UTC"
    sf = font(SANS, 15)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 130), sub, font=sf, fill=MUTED)
    d.line([M, 152, W - M, 152], fill=INK, width=3)

    # ---------- lead cards ----------
    leads = [
        ("CLIMATE  ·  ANTALYA", TEAL, icon_summit,
         "COP31 collapses with no deal",
         "EU and ~130 parties reject a text with no fossil fuels; "
         "record overtime ends in failure."),
        ("EUROPE  ·  UKRAINE", NAVY, icon_missile,
         "Dymer death toll climbs to 10",
         "Boy, 7, pulled alive after 14 hours; Vyshneve grocery "
         "hit kills 3, wounds 13."),
        ("AMERICAS  ·  WASHINGTON", ORANGE, icon_ballot,
         "Democrats win record majority",
         "258 House seats, biggest since 1992; Hubbard beats "
         "Foxx by 330 votes; Senate also theirs."),
    ]
    lw, lh, lgap = 309, 160, 16
    ly = 164
    lkf = font(SANS_B, 15)
    lhf = font(SANS_B, 23)
    lbf = font(SANS, 13)
    for i, (kick, color, icon, head, body) in enumerate(leads):
        x = M + i * (lw + lgap)
        d.rectangle([x, ly, x + lw, ly + lh], fill=CARD, outline=INK, width=2)
        d.rectangle([x, ly, x + lw, ly + 6], fill=color)
        icon(d, x + lw - 58, ly + 14, 44, color)
        d.text((x + 14, ly + 12), kick, font=lkf, fill=color)
        hlines = wrap(d, head, lhf, lw - 28 - 52)
        y = text_block(d, x + 14, ly + 38, hlines, lhf, INK, 28)
        blines = wrap(d, body, lbf, lw - 28)
        bend = y + 4 + len(blines) * 17
        if bend > ly + lh - 6:
            raise SystemExit("lead %s overflows by %d px"
                             % (kick, bend - (ly + lh - 6)))
        text_block(d, x + 14, y + 4, blines, lbf, INK, 17)

    # ---------- market heatmap strip ----------
    hx0, hy0, hw_, hh = M, 330, W - 2 * M, 24
    d.rectangle([hx0, hy0, hx0 + hw_, hy0 + hh], fill=SLATE)
    hlf = font(SANS_B, 13)
    htf = font(SANS, 13)
    d.text((hx0 + 12, hy0 + 4), "MARKET HEATMAP", font=hlf, fill=GOLD)
    chips = [("Nikkei −5.06%", HEAT_RED), ("Kospi −3.2%", HEAT_RED),
             ("Hang Seng 19-mo low", HEAT_RED), ("Taiex +2.5%", HEAT_GREEN),
             ("Brent $89.96", WHITE)]
    cx = hx0 + 12 + d.textlength("MARKET HEATMAP", font=hlf) + 24
    for j, (txt, col) in enumerate(chips):
        d.text((cx, hy0 + 4), txt, font=htf, fill=col)
        cx += d.textlength(txt, font=htf)
        if j < len(chips) - 1:
            d.text((cx, hy0 + 4), "  ·  ", font=htf, fill=HEAT_DIM)
            cx += d.textlength("  ·  ", font=htf)

    # ---------- region panels ----------
    # (region, color, [(headline, one-line body), ...])
    regions = [
        ("MIDDLE EAST", RED, [
            ("Two tankers ablaze near Hormuz",
             "Hit by mines, Iran navy says."),
            ("Iran strike wounds two in Bahrain",
             "Saudi condemns the attacks."),
            ("Houthis hit Saudi Rabigh refinery",
             "Sunday attack on Red Sea coast."),
            ("Iran announces daily power cuts",
             "Fuel shortages ahead of winter."),
            ("Trump: Iran's biggest missile week",
             "All were shot down, he says."),
        ]),
        ("EUROPE", NAVY, [
            ("Belgium airports shut for strike",
             "No flights 07:00–21:00 Monday."),
            ("Lewis Pugh swims Strait of Hormuz",
             "Swims the strait's full length."),
            ("Don Toliver concert evacuated",
             "Unknown substance released."),
            ("Kyivstoner survived Warsaw plot",
             "Earlier plot in Warsaw, August."),
            ("EU leads 130-party COP31 rejection",
             "Kurum: no new draft; Saudi sway."),
        ]),
        ("ASIA", TEAL, [
            ("Hong Kong stocks hit 19-month low",
             "Sell-off spreads across Asia."),
            ("Kospi slides, Samsung, SK Hynix hit",
             "Samsung, SK Hynix hit hard."),
            ("CSI 300 ends near −0.6%",
             "Hang Seng also near −0.6%."),
            ("Taiex reverses to +2.5%",
             "Taiwan bucks the rout."),
            ("Australia, Pacific despair at COP flop",
             "Backlash after COP flop."),
        ]),
        ("AMERICAS", ORANGE, [
            ("Hubbard beats Foxx by 330 votes",
             "GOP at least 173; 4 undecided."),
            ("Jeffries to be House Speaker",
             "'Largest majority this century.'"),
            ("Senate also Democratic, 56 seats",
             "Unified control in January."),
            ("Van Hollen challenges Schumer",
             "Secret ballot on 1 December."),
            ("Voters angry over costs, Iran war",
             "Wave spans red states, Midwest."),
        ]),
        ("AFRICA", BROWN, [
            ("Russian warship sinks at Libyan port",
             "Suspected drone strike."),
            ("Drones kill five children in Khartoum",
             "Homes and UN building hit."),
        ]),
        ("MARKETS", AMBER, [
            ("Nikkei falls 5.06% on Monday",
             "Follows Friday's US rout."),
            ("S&P 500 drops 3.7% in AI sell-off",
             "Nasdaq's 2026 gains erased."),
            ("Brent crude holds near $90",
             "Oil holds near $90."),
            ("Fed: Waller floats half-point hike",
             "Hikes priced for Dec and Jan."),
        ]),
        ("SCIENCE", GREEN, [
            ("Hunger Games opens to $120M",
             "$225M global; 4th best in series."),
            ("UK to host 2035 Women's World Cup",
             "FIFA set to confirm."),
            ("Thitikul wins LPGA finale again",
             "Third year in a row."),
            ("Macy's parade celebrates 100 years",
             "Thanksgiving Day milestone."),
        ]),
        ("SPORT", PURPLE, [
            ("Alcaraz wins first ATP Finals title",
             "Undefeated 5–0; $5.171M record."),
            ("Márquez wins eighth MotoGP title",
             "Eighth title, equals Agostini."),
            ("Boca win Copa Sudamericana 2–0",
             "Beat Atlético Mineiro 2–0."),
            ("Liverpool beat Man Utd 4–0",
             "Pochettino's United debut."),
            ("Price wins Grand Slam of Darts",
             "Beat van Veen 16–11."),
        ]),
    ]
    gx, gy = M, 360
    pw, ph, pgap = 231, 288, 12
    rkf = font(SANS_B, 15)
    rcf = font(SANS, 11)
    rhf = font(SANS_B, 13)
    rbf = font(SANS, 11)
    for i, (name, color, stories) in enumerate(regions):
        x = gx + (i % 4) * (pw + pgap)
        yy = gy + (i // 4) * (ph + pgap)
        d.rectangle([x, yy, x + pw, yy + ph], fill=CARD, outline=INK, width=2)
        d.rectangle([x, yy, x + pw, yy + 6], fill=color)
        d.text((x + 12, yy + 14), name, font=rkf, fill=color)
        cnt = "%d STORIES" % len(stories)
        cw_ = d.textlength(cnt, font=rcf)
        d.text((x + pw - 12 - cw_, yy + 16), cnt, font=rcf, fill=MUTED)
        # lay stories out, spreading leftover space evenly as gaps
        blocks = []
        total = 0
        for head, body in stories:
            hl = wrap(d, head, rhf, pw - 28 - 16)
            bl = wrap(d, body, rbf, pw - 28 - 16)
            h = len(hl) * 15 + len(bl) * 13
            blocks.append((hl, bl, h))
            total += h
        avail = ph - 48 - total
        gap = max(6, avail // max(1, len(blocks)))
        if 42 + total + len(blocks) * gap > ph:
            raise SystemExit(
                "panel %s overflows by %d px"
                % (name, 42 + total + len(blocks) * gap - ph))
        y = yy + 42
        for hl, bl, h in blocks:
            d.ellipse([x + 12, y + 5, x + 20, y + 13], fill=color)
            y = text_block(d, x + 28, y, hl, rhf, INK, 15)
            y = text_block(d, x + 28, y + 1, bl, rbf, MUTED, 13)
            y += gap

    # ---------- ticker ----------
    tx0, ty0, tw_, th = M, 954, W - 2 * M, 40
    d.rectangle([tx0, ty0, tx0 + tw_, ty0 + th], fill=NAVY)
    tf2 = font(SANS_B, 15)
    d.text((tx0 + 14, ty0 + 11), "ALSO IN THE NEWS", font=tf2, fill=GOLD)
    tick = ("Likud–Yashar talks end without deal   •   "
            "US tracked Alice Huang's China contacts   •   "
            "I Play Rocky second at box office, $9.3M")
    tkf = font(SANS, 14)
    tlines = wrap(d, tick, tkf, tw_ - 210)
    text_block(d, tx0 + 192, ty0 + 2, tlines, tkf, WHITE, 18)

    # ---------- footer ----------
    ff = font(SANS, 14)
    foot = ("Compiled from reports published 23 November 2026  ·  "
            "Sources: CNN, Reuters, AP, WSJ  ·  One day. 38 stories.")
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 1002), foot, font=ff, fill=MUTED)

    out = os.environ.get("OUT", "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

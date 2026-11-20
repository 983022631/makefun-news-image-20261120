#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026 as entry.png.

A newspaper front page with six stories, all drawn programmatically with
Pillow: masthead, headlines, decks and six small flat illustrations.
No photographs, no AI-generated images, no network. Deterministic output:
same bytes every run.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (176, 58, 46)
BLUE = (31, 78, 121)
SEA = (58, 110, 145)
GOLD = (201, 162, 39)
GREY = (90, 90, 90)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
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


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def headline(draw, x, y, text, size, max_w, fill=INK):
    fnt = font(SERIF_B, size)
    return para(draw, x, y, text, fnt, max_w, fill=fill,
                leading=int(size * 1.12))


def kicker(draw, x, y, text, size=20):
    fnt = font(SANS_B, size)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + int(size * 1.5)


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def art_cyclone(d, x0, y0, x1, y1):
    """Spiral storm over the Bay of Bengal, coast at bottom left."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 231, 238))
    cx, cy = (x0 + x1) // 2 + 30, (y0 + y1) // 2 - 10
    for r in range(96, 8, -11):
        start = 200 - r * 3
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 300,
              fill=SEA, width=7)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=PAPER,
              outline=SEA, width=3)
    d.polygon([(x0, y1), (x0, y1 - 52), (x0 + 150, y1 - 96),
               (x0 + 210, y1 - 60), (x0 + 230, y1)],
              fill=(196, 178, 138))
    d.line([(x0 + 150, y1 - 96), (x0 + 210, y1 - 60)], fill=INK, width=2)
    for i in range(9):
        rx = x0 + 24 + i * 20
        d.line([(rx, y0 + 12), (rx - 8, y0 + 34)], fill=(120, 160, 185),
               width=2)
    d.text((x0 + 14, y1 - 26), "BAY OF BENGAL", font=font(SANS_B, 16),
           fill=(40, 80, 110))
    d.text((x0 + 14, y0 + 8), "ODISHA COAST", font=font(SANS_B, 16),
           fill=(90, 70, 40))


def art_shield(d, x0, y0, x1, y1):
    """Shield in Ukraine blue and yellow with a big 5."""
    cx = (x0 + x1) // 2
    top, bot = y0 + 4, y1 - 4
    w2 = (x1 - x0) // 2 - 4
    mid_y = top + 56
    d.polygon([(cx - w2, top), (cx + w2, top), (cx + w2, mid_y),
               (cx, bot), (cx - w2, mid_y)], fill=(0, 91, 187))
    d.polygon([(cx - w2, mid_y), (cx + w2, mid_y), (cx, bot)],
              fill=(255, 213, 0))
    d.polygon([(cx - w2, top), (cx + w2, top), (cx + w2, mid_y),
               (cx, bot), (cx - w2, mid_y)], outline=INK, width=3)
    fnt = font(SERIF_B, 58)
    tw = d.textlength("5", font=fnt)
    d.text((cx - tw / 2, top + 10), "5", font=fnt, fill=(255, 255, 255))


def art_voyager(d, x0, y0, x1, y1):
    """Gold dish probe, signal arcs reaching a small blue Earth."""
    d.rectangle([x0, y0, x1, y1], fill=(12, 18, 38))
    for i in range(40):
        sx = x0 + (i * 37) % (x1 - x0)
        sy = y0 + (i * 53) % (y1 - y0)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 220, 220))
    cx, cy = x0 + 118, y0 + 56
    d.polygon([(cx - 40, cy - 6), (cx + 40, cy - 6), (cx + 20, cy + 26),
               (cx - 20, cy + 26)], fill=GOLD)
    d.rectangle([cx - 26, cy + 26, cx + 26, cy + 38], fill=(190, 150, 40))
    for r in (12, 20, 28):
        d.arc([cx - r, cy - 22 - r, cx + r, cy - 22 + r], 180, 360,
              fill=(120, 200, 255), width=3)
    ex, ey = x1 - 36, y0 + 28
    d.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill=(70, 140, 210))
    d.arc([ex - 11, ey - 11, ex + 11, ey + 11], 40, 200, fill=(90, 200, 120),
          width=4)
    d.text((x1 - 70, y0 + 48), "EARTH", font=font(SANS_B, 14),
           fill=(200, 220, 240))


def art_gta(d, x0, y0, x1, y1):
    """Vice City sunset: orange sky, skyline, big VI."""
    for i in range(y1 - y0):
        t = i / max(1, y1 - y0)
        r = int(250 - 60 * t)
        g = int(120 + 60 * t)
        b = int(90 + 80 * t)
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b))
    d.ellipse([x0 + 56, y0 + 12, x0 + 118, y0 + 74], fill=(255, 236, 170))
    base = y1 - 6
    heights = [44, 62, 34, 70, 48, 80, 38, 56]
    bw = (x1 - x0) // len(heights)
    for i, hh in enumerate(heights):
        d.rectangle([x0 + i * bw + 2, base - hh, x0 + (i + 1) * bw - 2, base],
                    fill=(30, 20, 40))
    for px, py in ((x0 + 24, base - 22), (x1 - 36, base - 34)):
        d.line([(px, py), (px, py - 20)], fill=(20, 16, 30), width=4)
        for ang in (-50, -20, 10, 40):
            rad = math.radians(ang)
            d.line([(px, py - 20),
                    (px + 15 * math.cos(rad), py - 20 + 10 * math.sin(rad))],
                   fill=(20, 16, 30), width=3)
    fnt = font(SERIF_B, 52)
    d.text((x0 + 12, y0 + 2), "VI", font=fnt, fill=(255, 255, 255))


def art_baseball(d, x0, y0, x1, y1):
    """A baseball diamond with bat and ball."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 231, 214))
    cx, cy = (x0 + x1) // 2, y0 + (y1 - y0) // 2 + 6
    d.polygon([(cx, cy - 46), (cx + 46, cy), (cx, cy + 46), (cx - 46, cy)],
              fill=(88, 150, 88), outline=(255, 255, 255), width=3)
    d.line([(cx, cy - 46), (cx, cy + 46)], fill=(255, 255, 255), width=2)
    d.line([(cx - 46, cy), (cx + 46, cy)], fill=(255, 255, 255), width=2)
    for bx, by in ((cx, cy - 46), (cx + 46, cy), (cx, cy + 46), (cx - 46, cy)):
        d.rectangle([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 255, 255),
                    outline=INK, width=2)
    d.line([(x0 + 18, y1 - 12), (x0 + 56, y0 + 20)], fill=(150, 100, 50),
           width=8)
    bx, by = x1 - 30, y0 + 26
    d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=(255, 255, 255),
              outline=INK, width=2)
    d.arc([bx - 13, by - 13, bx + 13, by + 13], 300, 60, fill=RED, width=2)
    d.arc([bx - 13, by - 13, bx + 13, by + 13], 120, 240, fill=RED, width=2)


def art_hippo(d, x0, y0, x1, y1):
    """Fiona: a flat grey hippo standing in shallow water."""
    d.rectangle([x0, y0, x1, y1], fill=(226, 232, 236))
    cx, cy = (x0 + x1) // 2, y0 + 42
    d.rectangle([x0, cy + 32, x1, y1], fill=(150, 190, 210))
    d.line([(x0, cy + 32), (x1, cy + 32)], fill=(90, 150, 180), width=3)
    body = (120, 128, 138)
    for lx in (cx - 48, cx - 24, cx + 20, cx + 44):
        d.rectangle([lx, cy + 4, lx + 14, cy + 40], fill=body)
    d.ellipse([cx - 66, cy - 30, cx + 60, cy + 20], fill=body)
    d.ellipse([cx + 38, cy - 40, cx + 88, cy + 4], fill=body)
    d.ellipse([cx + 60, cy - 24, cx + 98, cy + 2], fill=(140, 148, 158))
    d.ellipse([cx + 80, cy - 13, cx + 87, cy - 6], fill=INK)
    d.ellipse([cx + 89, cy - 13, cx + 96, cy - 6], fill=INK)
    d.ellipse([cx + 46, cy - 42, cx + 58, cy - 32], fill=body,
              outline=INK, width=2)
    d.ellipse([cx + 56, cy - 34, cx + 63, cy - 27], fill=INK)
    d.polygon([(x0 + 14, cy + 44), (x0 + 44, cy + 44), (x0 + 29, cy + 33)],
              fill=(176, 58, 46))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30
    R = W - M

    # ---- masthead ----
    f_title = font(SERIF_B, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 24), title, font=f_title, fill=INK)
    rule(d, M, 104, R, 3)
    f_date = font(SANS_B, 27)
    d.text((M, 114), "FRIDAY  ·  20 NOVEMBER 2026", font=f_date, fill=RED)
    f_right = font(SANS_B, 21)
    rt = "SIX STORIES  ·  ONE DAY"
    d.text((R - d.textlength(rt, font=f_right), 118), rt, font=f_right,
           fill=INK)
    rule(d, M, 152, R, 2)

    # ---- lead: Cyclone Akvan (168..424) ----
    y = 168
    y = kicker(d, M, y, "INDIA  ·  WEATHER", 20)
    y = headline(d, M, y, "CYCLONE AKVAN BEARS DOWN ON INDIA'S EAST COAST",
                 36, 560)
    para(d, M, y + 6,
         "Landfall expected today between Puri and Gopalpur. "
         "300,000 people evacuated, 423 rescue teams deployed, "
         "dozens of trains cancelled.",
         font(SANS, 22), 560, leading=29)
    art_cyclone(d, 622, 168, R, 424)
    rule(d, M, 428, R, 2)

    # ---- middle row (444..704) ----
    y = 444
    mid = W // 2
    # Ukraine (left)
    yy = kicker(d, M, y, "EUROPE  ·  DIPLOMACY", 19)
    yy = headline(d, M, yy, "EUROPE READY FOR UKRAINE PEACE TALKS", 28, 464)
    art_shield(d, M, yy + 6, M + 140, yy + 96)
    para(d, M + 154, yy + 10,
         "Kushner: Russia is \u201ccomfortable\u201d with Article 5-style "
         "guarantees for Kyiv. Trump is \u201copen\u201d to the idea.",
         font(SANS, 19), 300, leading=25)
    # Voyager (right)
    yy2 = kicker(d, mid + 18, y, "SPACE  ·  SCIENCE", 19)
    yy2 = headline(d, mid + 18, yy2, "VOYAGER 1, A LIGHT-DAY FROM HOME", 28,
                   446)
    art_voyager(d, mid + 18, yy2 + 6, R, yy2 + 96)
    para(d, mid + 18, yy2 + 104,
         "NASA confirms Voyager 1 is the first craft a full light-day "
         "from Earth \u2014 16bn miles.",
         font(SANS, 19), 446, leading=25)
    rule(d, M, 704, R, 2)

    # ---- bottom row (720..962) ----
    y = 720
    cols = [(M, 311), (M + 326, 311), (M + 652, 311)]
    # GTA VI
    x, w = cols[0]
    yy = kicker(d, x, y, "CULTURE  ·  GAMES", 18)
    yy = headline(d, x, yy, "GTA VI: $1.84 BILLION IN A DAY", 25, w)
    art_gta(d, x, yy + 4, x + w, yy + 86)
    para(d, x, yy + 94,
         "Sensor Tower estimates 19m copies by launch day \u2014 over twice "
         "GTA V's first day.",
         font(SANS, 18), w, leading=23)
    # Pete Rose
    x, w = cols[1]
    yy = kicker(d, x, y, "USA  ·  SPORT", 18)
    yy = headline(d, x, yy, "TRUMP PARDONS PETE ROSE", 25, w)
    art_baseball(d, x, yy + 4, x + w, yy + 86)
    para(d, x, yy + 94,
         "Posthumous pardon for the hits leader (4,256) over his 1990 tax "
         "conviction. Hall vote: Dec 2027.",
         font(SANS, 18), w, leading=23)
    # Fiona
    x, w = cols[2]
    yy = kicker(d, x, y, "USA  ·  ANIMALS", 18)
    yy = headline(d, x, yy, "FAREWELL, FIONA", 25, w)
    art_hippo(d, x, yy + 4, x + w, yy + 86)
    para(d, x, yy + 94,
         "Cincinnati Zoo's beloved hippo, 9, dies after swallowing a "
         "visitor's knit hat. Vets could not save her.",
         font(SANS, 18), w, leading=23)

    # ---- footer ----
    rule(d, M, 970, R, 2)
    f_src = font(SANS, 15)
    src1 = "Sources: The Hindu, NDTV, Reuters, AP, Al Jazeera, ESPN, CNN, Sensor Tower."
    src2 = "Drawn programmatically with Python + PIL; no photographs."
    for i, s in enumerate((src1, src2)):
        sw = d.textlength(s, font=f_src)
        d.text(((W - sw) / 2, 978 + i * 19), s, font=f_src, fill=GREY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path, img.size, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()

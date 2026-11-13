#!/usr/bin/env python3
"""Draw the zech news-image-01 poster: a classic newspaper front page.

Original design, drawn entirely with PIL. No photos, no copied art.
Canvas 1024x1024, cream newsprint, serif masthead, one drawn hero panel.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (24, 22, 18)
RED = (158, 32, 26)
GREY = (96, 90, 78)
RULE = (60, 56, 48)

FD = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SERIF_R = os.path.join(FD, "DejaVuSerif.ttf")
SANS = os.path.join(FD, "DejaVuSans-Bold.ttf")
SANS_R = os.path.join(FD, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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


def center(draw, y, text, fnt, fill=INK, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def rule(draw, y, x0, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)
    return y + width


def kicker(draw, x, y, text, fnt, fill=RED):
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + fnt.size + 2


def headline(draw, x, y, text, fnt, max_w, leading=None):
    leading = leading or int(fnt.size * 1.08)
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=INK)
        y += leading
    return y


def body(draw, x, y, text, fnt, max_w, leading=None):
    leading = leading or int(fnt.size * 1.32)
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=INK)
        y += leading
    return y


def draw_hero(draw, x0, y0, x1, y1):
    """Drawn illustration: globe with dove, tanker on a strait, microchip."""
    sky_top = (178, 205, 224)
    sky_bot = (232, 236, 228)
    sea = (64, 110, 138)
    for i in range(y1 - y0):
        t = i / max(1, y1 - y0 - 1)
        c = tuple(int(sky_top[j] + (sky_bot[j] - sky_top[j]) * t) for j in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)
    horizon = y0 + int((y1 - y0) * 0.62)
    draw.rectangle([x0, horizon, x1, y1], fill=sea)
    # sun
    sx, sy, sr = x1 - 90, y0 + 62, 34
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(240, 196, 84))
    draw.ellipse([sx - sr - 6, sy - sr - 6, sx + sr + 6, sy + sr + 6],
                 outline=(240, 196, 84), width=3)
    # clouds
    for cx, cy, s in [(x0 + 150, y0 + 52, 26), (x0 + 300, y0 + 34, 20),
                      (x1 - 250, y0 + 110, 22)]:
        draw.ellipse([cx - s, cy - s // 2, cx + s, cy + s // 2], fill=(255, 255, 255))
        draw.ellipse([cx - s // 2, cy - s, cx + s // 2, cy], fill=(255, 255, 255))
    # globe (left)
    gx, gy, gr = x0 + 140, y0 + 118, 92
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(96, 150, 196))
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=INK, width=4)
    # continents (stylised blobs)
    for pts, col in [
        ([(gx - 70, gy - 40), (gx - 30, gy - 62), (gx - 8, gy - 30),
          (gx - 40, gy - 6), (gx - 66, gy - 14)], (104, 168, 92)),
        ([(gx + 8, gy - 10), (gx + 52, gy - 34), (gx + 78, gy + 6),
          (gx + 44, gy + 34), (gx + 12, gy + 26)], (104, 168, 92)),
        ([(gx - 46, gy + 34), (gx - 6, gy + 30), (gx + 4, gy + 66),
          (gx - 38, gy + 74)], (104, 168, 92)),
    ]:
        draw.polygon(pts, fill=col)
    # latitude lines
    for dy in (-52, 0, 52):
        draw.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340,
                 fill=(255, 255, 255), width=2)
    # dove above globe
    dx, dy = gx + 130, y0 + 42
    draw.ellipse([dx - 34, dy - 10, dx + 10, dy + 12], fill=(255, 255, 255),
                 outline=INK, width=2)
    draw.ellipse([dx + 2, dy - 18, dx + 22, dy + 2], fill=(255, 255, 255),
                 outline=INK, width=2)  # head
    draw.polygon([(dx + 20, dy - 12), (dx + 32, dy - 8), (dx + 20, dy - 6)],
                 fill=(240, 170, 60))  # beak
    draw.ellipse([dx - 40, dy - 34, dx - 2, dy - 6], fill=(255, 255, 255),
                 outline=INK, width=2)  # raised wing
    draw.polygon([(dx - 34, dy + 4), (dx - 58, dy + 18), (dx - 26, dy + 12)],
                 fill=(255, 255, 255), outline=INK)  # tail
    draw.ellipse([dx + 12, dy - 14, dx + 17, dy - 9], fill=INK)  # eye
    # olive branch
    draw.line([(dx - 8, dy + 26), (dx + 26, dy + 40)], fill=(90, 130, 70), width=3)
    for lx, ly in [(dx + 2, dy + 30), (dx + 14, dy + 35), (dx + 24, dy + 40)]:
        draw.ellipse([lx - 6, ly - 3, lx + 6, ly + 3], fill=(90, 130, 70))
    # tanker on the strait (right)
    tx0, ty = x1 - 330, horizon + 26
    draw.rectangle([tx0, ty - 34, tx0 + 260, ty + 6], fill=(40, 44, 52))
    draw.rectangle([tx0 + 170, ty - 62, tx0 + 220, ty - 34], fill=(200, 60, 50))
    draw.rectangle([tx0 + 186, ty - 82, tx0 + 204, ty - 62], fill=(40, 44, 52))
    draw.polygon([(tx0 + 8, ty - 34), (tx0 + 30, ty - 58), (tx0 + 52, ty - 34)],
                 fill=(240, 196, 84))
    for cx in range(tx0 + 10, tx0 + 260, 44):
        draw.rectangle([cx, ty - 26, cx + 22, ty - 12], fill=(246, 241, 229))
    # waves
    for wy in (horizon + 58, horizon + 84):
        for k in range(0, x1 - x0, 46):
            draw.arc([x0 + k, wy, x0 + k + 40, wy + 16], 180, 360,
                     fill=(255, 255, 255), width=3)
    # microchip (small, bottom right of sky)
    cx0, cy0 = x1 - 130, horizon - 74
    draw.rectangle([cx0, cy0, cx0 + 58, cy0 + 58], fill=(30, 32, 40),
                   outline=(240, 196, 84), width=3)
    draw.rectangle([cx0 + 16, cy0 + 16, cx0 + 42, cy0 + 42], fill=(240, 196, 84))
    for px in (cx0 + 10, cx0 + 29, cx0 + 48):
        draw.line([(px, cy0 - 12), (px, cy0)], fill=(30, 32, 40), width=4)
        draw.line([(px, cy0 + 58), (px, cy0 + 70)], fill=(30, 32, 40), width=4)
    for py in (cy0 + 10, cy0 + 29, cy0 + 48):
        draw.line([(cx0 - 12, py), (cx0, py)], fill=(30, 32, 40), width=4)
        draw.line([(cx0 + 58, py), (cx0 + 70, py)], fill=(30, 32, 40), width=4)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=3)


def fit_font(path, text, max_w, start):
    size = start
    while size > 10 and font(path, size).getlength(text) > max_w:
        size -= 2
    return font(path, size)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40  # margin
    y = 22

    # --- masthead ---
    mast = fit_font(SERIF, "THE WORLD TODAY", W - 2 * M, 96)
    y = center(d, y, "THE WORLD TODAY", mast)
    y += 2
    y = rule(d, y, M, W - M, 4)
    y = rule(d, y + 4, M, W - M, 1)
    y += 6
    y = center(d, y, "FRIDAY  ·  13 NOVEMBER 2026  ·  ONE DAY IN ONE PAGE",
               font(SANS, 20))
    y += 8
    y = rule(d, y, M, W - M, 2)
    y += 10

    # --- hero illustration ---
    hx0, hy0, hx1, hy1 = M, y, W - M, y + 232
    draw_hero(d, hx0, hy0, hx1, hy1)
    y = hy1 + 6
    y = center(d, y, "Peace talks in Europe, a strait on edge, a chip giant in turmoil —",
               font(SERIF_R, 19), fill=GREY)
    y = center(d, y, "the world on Friday, 13 November 2026.",
               font(SERIF_R, 19), fill=GREY)
    y += 4
    y = rule(d, y, M, W - M, 2)
    y += 10

    # --- lead story ---
    y = kicker(d, M, y, "EUROPE  ·  UKRAINE PEACE TALKS", font(SANS, 20))
    y = headline(d, M, y, "Europe wins a seat at the Ukraine",
                 font(SERIF, 42), W - 2 * M)
    y = headline(d, M, y, "peace talks",
                 font(SERIF, 42), W - 2 * M)
    y += 2
    y = body(d, M, y,
             "Russia and Ukraine agree to bring European envoys into the next round "
             "of negotiations — and to the war's largest prisoner exchange yet.",
             font(SERIF_R, 22), W - 2 * M)
    y += 8
    y = rule(d, y, M, W - M, 1)
    y += 10

    # --- two columns ---
    col_w = (W - 2 * M - 28) // 2
    cx2 = M + col_w + 28
    y_top = y
    y1 = kicker(d, M, y_top, "THE GULF", font(SANS, 19))
    y1 = headline(d, M, y1, "Iran claims US radar hit as tankers are struck in Hormuz",
                  font(SERIF, 25), col_w, leading=30)
    y1 = body(d, M, y1,
              "Tehran says its forces destroyed a US early-warning radar in Bahrain "
              "and that four tankers were hit in the strait. The claims could not "
              "be independently verified.",
              font(SERIF_R, 18), col_w, leading=23)
    y2 = kicker(d, cx2, y_top, "TECHNOLOGY", font(SANS, 19))
    y2 = headline(d, cx2, y2, "Nvidia chief quits — and is summoned to testify",
                  font(SERIF, 25), col_w, leading=30)
    y2 = body(d, cx2, y2,
              "Jensen Huang resigns as chief executive after 33 years; Congress "
              "calls him to testify over an alleged affair with a woman reported "
              "to be a suspected Chinese agent.",
              font(SERIF_R, 18), col_w, leading=23)
    y = max(y1, y2) + 8
    y = rule(d, y, M, W - M, 1)
    y += 10

    # --- bottom band: outage + also in the news ---
    y = kicker(d, M, y, "ALSO IN THE NEWS", font(SANS, 19))
    y = headline(d, M, y, "Microsoft outage knocks out Outlook and Teams worldwide",
                 font(SERIF, 24), W - 2 * M, leading=29)
    y = body(d, M, y,
             "A global Microsoft 365 disruption hits businesses, schools and "
             "government offices; the company says it is not a cyberattack.",
             font(SERIF_R, 18), W - 2 * M, leading=23)
    y += 6
    y = rule(d, y, M, W - M, 1)
    y += 8
    y = body(d, M, y,
             "Oil: IEA sees a supply surplus into year-end  ·  Peru: Pope Leo meets "
             "abuse survivors before record crowds  ·  New York: Brooklyn collapse "
             "toll settles at eight dead.",
             font(SERIF_R, 17), W - 2 * M, leading=22)
    y += 4
    y = rule(d, y, M, W - M, 2)
    y += 6
    center(d, y, "Sources: AP · BBC · Reuters · The Guardian · UN News — 13 Nov 2026",
           font(SANS_R, 15), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image.png")
    img.save(out, optimize=True)
    print(f"saved {out}: {img.size}, {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()

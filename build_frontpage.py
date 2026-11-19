#!/usr/bin/env python3
"""Build the news front page for 19 November 2026 (1024x1024).

Composes AI-generated news photos (assets/) with crisp PIL typography
into a single newspaper-style front page: entry.png.

Run:  python3 build_frontpage.py
Out:  entry.png  (1024x1024, PNG)
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

W, H = 1024, 1024

PAPER = (246, 241, 231)      # warm newsprint
INK = (17, 17, 17)
NAVY = (12, 26, 46)
RED = (192, 57, 43)
GREY = (70, 70, 70)
WHITE = (255, 255, 255)
GOLD = (255, 210, 90)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_w):
    """Largest size (<= start) at which text fits max_w."""
    size = start
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 8)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cover(path, size, cy=0.5, cx=0.5):
    """Crop/resize an image to exactly fill size (center crop)."""
    im = Image.open(path).convert("RGB")
    return ImageOps.fit(im, size, method=Image.LANCZOS, centering=(cx, cy))


def bottom_shade(im, height):
    """Dark gradient at the bottom of an RGB image for legible white text."""
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(height):
        a = int(200 * (y / height) ** 1.4)
        d.line([(0, im.size[1] - height + y), (im.size[0], im.size[1] - height + y)],
               fill=(0, 0, 0, a))
    base = im.convert("RGBA")
    base.alpha_composite(overlay)
    return base.convert("RGB")


def panel(page, x, y, w, h, img_path, img_h, tag, headline, sub, hl_size=30):
    """One story panel: photo on top, tag, headline, subline below."""
    d = ImageDraw.Draw(page)
    img = cover(img_path, (w, img_h))
    page.paste(img, (x, y))
    # red tag bar over the photo's top-left corner
    ft = font(SANS_B, 16)
    tw = d.textlength(tag, font=ft)
    d.rectangle([x + 12, y + 10, x + 12 + tw + 20, y + 10 + 28], fill=RED)
    d.text((x + 12 + 10, y + 10 + 5), tag, font=ft, fill=WHITE)
    ty = y + img_h + 10
    fh = fit_font(d, headline, SANS_B, hl_size, w - 16)
    d.text((x + 8, ty), headline, font=fh, fill=INK)
    fs = font(SANS, 17)
    lines = wrap(d, sub, fs, w - 16)
    ly = ty + fh.size + 6
    for ln in lines[:2]:
        d.text((x + 8, ly), ln, font=fs, fill=GREY)
        ly += 21
    return ly


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---------- Masthead ----------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    kicker = "W O R L D   N E W S   \u2022   T H E   D A Y   I N   O N E   I M A G E"
    fk = font(SANS_B, 17)
    d.text(((W - d.textlength(kicker, font=fk)) / 2, 12), kicker, font=fk, fill=GOLD)
    date = "THURSDAY 19 NOVEMBER 2026"
    fd = fit_font(d, date, SERIF_B, 64, W - 60)
    d.text(((W - d.textlength(date, font=fd)) / 2, 40), date, font=fd, fill=WHITE)
    d.rectangle([0, 118, W, 122], fill=RED)

    # ---------- Lead story: Shenzhen trilateral ----------
    lead = cover(os.path.join(ASSETS, "media-generation-summit-shenzhen-0-5c38402a-0823-4061-8a27-ae091bf05133.webp"),
                 (W, 350), cy=0.5)
    lead = bottom_shade(lead, 175)
    page.paste(lead, (0, 130))
    dl = ImageDraw.Draw(page)
    tag = "TOP STORY"
    ft = font(SANS_B, 20)
    tw = dl.textlength(tag, font=ft)
    dl.rectangle([24, 148, 24 + tw + 28, 148 + 36], fill=RED)
    dl.text((24 + 14, 148 + 6), tag, font=ft, fill=WHITE)
    fh = fit_font(dl, "TRUMP, XI AND PUTIN MEET IN SHENZHEN", SANS_B, 44, W - 48)
    dl.text((24, 480 - 98), "TRUMP, XI AND PUTIN MEET IN SHENZHEN", font=fh, fill=WHITE)
    fs = font(SANS, 20)
    dl.text((24, 480 - 46),
            "First-ever trilateral of the three leaders at the APEC summit",
            font=fs, fill=(235, 235, 235))
    dl.text((24, 480 - 20),
            "Ukraine, Iran, trade and nuclear arms on the table",
            font=fs, fill=(235, 235, 235))

    # ---------- Row 2: ICJ | GTA VI ----------
    y2, h2 = 488, 258
    panel(page, 0, y2, 508, h2,
          os.path.join(ASSETS, "media-generation-icj-court-0-fc32ce4b-f6cb-44f7-9019-740d2f1abffb.webp"),
          160, "THE HAGUE",
          "WORLD COURT RULES ON MYANMAR",
          "The Hague delivers its verdict in the Rohingya genocide case \u2014 a first for any state")
    panel(page, 516, y2, 508, h2,
          os.path.join(ASSETS, "media-generation-vice-city-0-e5bf7b81-461e-41c6-8eb9-143ebae373dc.webp"),
          160, "CULTURE",
          "VICE CITY OPENS AT LAST",
          "GTA VI launches worldwide after 13 years \u2014 99 on Metacritic, a record-tying score")

    # ---------- Row 3: Voyager photo | Gulf text panel ----------
    y3, h3 = 754, 192
    panel(page, 0, y3, 508, h3,
          os.path.join(ASSETS, "media-generation-voyager-space-0-fb0a5712-ef3f-4c28-b128-4479fcb8bec4.webp"),
          104, "SPACE",
          "VOYAGER 1, ONE LIGHT-DAY OUT",
          "NASA confirms its probe is 16 billion miles from Earth",
          hl_size=26)
    # Text-only sidebar: the Gulf war, no photo needed
    d = ImageDraw.Draw(page)
    gx = 516
    d.rectangle([gx, y3, gx + 508, y3 + h3], outline=(150, 140, 120), width=2)
    ft = font(SANS_B, 16)
    d.rectangle([gx + 12, y3 + 10, gx + 12 + d.textlength("THE GULF", font=ft) + 20, y3 + 10 + 28], fill=RED)
    d.text((gx + 12 + 10, y3 + 10 + 5), "THE GULF", font=ft, fill=WHITE)
    fh = fit_font(d, "GULF WAR WIDENS", SANS_B, 26, 508 - 16)
    d.text((gx + 8, y3 + 48), "GULF WAR WIDENS", font=fh, fill=INK)
    fs = font(SANS, 17)
    bullets = [
        "Iran fires on Kuwait after the U.S. strike",
        "on Qeshm Island in the Strait of Hormuz.",
        "Bahrain intercepts more Iranian drones \u2014",
        "its third attack in a week.",
    ]
    ly = y3 + 48 + fh.size + 8
    for ln in bullets:
        d.text((gx + 8, ly), ln, font=fs, fill=GREY)
        ly += 21

    # ---------- Footer ticker ----------
    d.rectangle([0, 954, W, H], fill=NAVY)
    f1 = font(SANS_B, 17)
    f2 = font(SANS, 17)
    d.text((16, 962), "ALSO TODAY", font=f1, fill=GOLD)
    ticker = "EU proposes a \u20ac45bn loan for Ukraine  \u2022  Australia sanctions Israeli settlers  \u2022  Israel pushes into central Gaza"
    ftick = fit_font(d, ticker, SANS, 17, W - 32)
    d.text((16, 986), ticker, font=ftick, fill=WHITE)

    out = os.path.join(BASE, "entry.png")
    page.save(out, "PNG", optimize=True)
    print(f"Wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()

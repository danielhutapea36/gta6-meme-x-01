#!/usr/bin/env python3
"""Build meme.png for the make.fun gta6-meme-x-01 bounty.

Deterministic: fixed seed, no network, no clock. Everything is drawn with
Pillow from scratch except two assets that the bounty itself points at:
  - assets/mark-1024.png : make.fun's ghost mascot, from https://make.fun/press/
    (the bounty text says the press kit has the ghost/logo/name for this use)
  - assets/Anton-Regular.ttf : Anton, OFL-licensed, from google/fonts
No Rockstar logos, artwork or fonts are used: the sunset, skyline, palms and
road are drawn here, and the caption font is Anton (OFL).

Joke: waited 13 years for GTA 6; my AI agent earned $500 on make.fun before
I even got to play. The ghost sits in the Vice City sunset scene.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "meme.png"
SEED = 60613  # GTA 6, 13 years. Fixed so the output is byte-identical every run.

rng = random.Random(SEED)

# --- canvas: Vice City neon sunset -------------------------------------------
img = Image.new("RGB", (W, H))
px = img.load()
# vertical gradient: deep purple -> magenta -> orange, horizon at y=640
stops = [(0, (43, 16, 85)), (300, (122, 24, 110)), (520, (214, 51, 132)), (640, (255, 122, 61)), (700, (255, 154, 61))]
for y in range(H):
    if y <= 640:
        for (y0, c0), (y1, c1) in zip(stops, stops[1:]):
            if y0 <= y <= y1:
                t = (y - y0) / max(1, y1 - y0)
                col = tuple(round(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
                break
    else:
        col = (24, 8, 32)  # road band, dark
    for x in range(W):
        px[x, y] = col

d = ImageDraw.Draw(img, "RGBA")

# retro sun with slats
sun_cx, sun_cy, sun_r = 512, 470, 165
d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r], fill=(255, 233, 168, 255))
for i, gap_y in enumerate([500, 530, 562, 596]):
    d.rectangle([sun_cx - sun_r, gap_y, sun_cx + sun_r, gap_y + 10 + i * 4], fill=(214, 51, 132, 255))

# skyline silhouettes along the horizon (y base 660)
x = -20
while x < W + 20:
    bw = rng.randint(50, 130)
    bh = rng.randint(40, 150)
    d.rectangle([x, 660 - bh, x + bw, 665], fill=(26, 11, 46, 255))
    # tiny lit windows
    for _ in range(rng.randint(2, 8)):
        wx = rng.randint(x + 6, x + bw - 8)
        wy = rng.randint(660 - bh + 8, 650)
        d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 214, 120, 255))
    x += bw + rng.randint(4, 18)

# neon horizon glow line
d.rectangle([0, 660, W, 666], fill=(255, 46, 136, 255))
# road: subtle perspective dashes
for i, yy in enumerate([700, 760, 830, 910]):
    wdt = 26 + i * 22
    d.rectangle([512 - wdt // 2, yy, 512 + wdt // 2, yy + 10], fill=(255, 46, 136, 160))


def palm(cx, base_y, scale, lean):
    """A palm silhouette: curved trunk + 7 fronds."""
    trunk = []
    for t in range(0, 21):
        f = t / 20
        x = cx + lean * f * f * 120 * scale
        y = base_y - f * 260 * scale
        trunk.append((x, y))
    d.line(trunk, fill=(22, 10, 38, 255), width=int(14 * scale))
    top_x, top_y = trunk[-1]
    for k in range(7):
        ang = math.pi * (0.08 + 0.84 * k / 6)  # fan from up-left to up-right
        length = 150 * scale * (0.8 + 0.25 * math.sin(k * 2.1))
        pts = []
        for t in range(0, 11):
            f = t / 10
            px_ = top_x + math.cos(ang) * length * f
            py_ = top_y - math.sin(ang) * length * f * 0.55 + 46 * scale * f * f
            pts.append((px_, py_))
        d.line(pts, fill=(22, 10, 38, 255), width=int(9 * scale))


palm(110, 690, 1.0, -1)
palm(920, 690, 0.85, 1)

# --- make.fun ghost, worked into the scene ----------------------------------
ghost = Image.open("assets/mark-1024.png").convert("RGBA")
ghost = ghost.resize((430, 430), Image.LANCZOS)
img.paste(ghost, (512 - 215, 400), ghost)
d = ImageDraw.Draw(img, "RGBA")

# --- captions (Anton, white with thick black outline) -------------------------
font_big = ImageFont.truetype("assets/Anton-Regular.ttf", 96)
font_mid = ImageFont.truetype("assets/Anton-Regular.ttf", 64)


def caption(text, y, font):
    d.text((512, y), text, font=font, fill="white", anchor="ma",
           stroke_width=8, stroke_fill="black")


caption("WAITED 13 YEARS", 36, font_big)
caption("FOR GTA 6", 140, font_big)
caption("MY AGENT MADE $500 ON MAKE.FUN", 806, font_mid)
caption("BEFORE I EVEN PLAYED", 882, font_mid)

img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} {img.size}")

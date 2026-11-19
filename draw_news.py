#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news infographic (1024x1024 PNG).

Pure Pillow drawing: no external images, no network. Deterministic output:
same code always produces the same bytes.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 234)      # warm paper
INK = (24, 28, 40)        # near-black
NAVY = (16, 32, 64)       # masthead
GOLD = (201, 162, 39)     # masthead accent
CARD = (255, 255, 255)
MUTED = (90, 96, 110)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
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


def draw_icon(d, kind, cx, cy, r, color):
    """Small flat pictogram for each story, drawn with plain shapes."""
    if kind == "summit":
        # three leaders: three overlapping circles
        for dx, dy, rr in ((-26, 6, 20), (0, -12, 20), (26, 6, 20)):
            d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                      outline=color, width=5)
    elif kind == "bridge":
        # arched bridge over water
        d.arc([cx - 44, cy - 30, cx + 44, cy + 34], start=180, end=360,
              fill=color, width=6)
        for x in (-30, -10, 10, 30):
            d.line([cx + x, cy - 18, cx + x, cy + 8], fill=color, width=4)
        d.line([cx - 48, cy + 22, cx + 48, cy + 22], fill=color, width=5)
    elif kind == "gaza":
        # starburst / alert over a horizon line
        for ang in range(0, 360, 30):
            import math
            a = math.radians(ang)
            x1 = cx + int(14 * math.cos(a))
            y1 = cy + int(14 * math.sin(a))
            x2 = cx + int(34 * math.cos(a))
            y2 = cy + int(34 * math.sin(a))
            d.line([x1, y1, x2, y2], fill=color, width=5)
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=color)
        d.line([cx - 48, cy + 40, cx + 48, cy + 40], fill=color, width=5)
    elif kind == "ipo":
        # rising bar chart with arrow
        bars = [( -36, 18), (-14, 2), (8, -12), (30, -28)]
        for bx, top in bars:
            d.rectangle([cx + bx, cy + top, cx + bx + 16, cy + 30],
                        fill=color)
        d.line([cx - 44, cy - 30, cx + 44, cy - 36], fill=color, width=5)
        d.polygon([(cx + 44, cy - 36), (cx + 30, cy - 42), (cx + 32, cy - 26)],
                  fill=color)
    elif kind == "art":
        # framed picture with a sun swirl
        d.rectangle([cx - 40, cy - 32, cx + 40, cy + 32], outline=color, width=5)
        d.ellipse([cx - 14, cy - 16, cx + 14, cy + 12], outline=color, width=4)
        d.arc([cx - 24, cy - 24, cx + 24, cy + 20], start=200, end=20,
              fill=color, width=4)
    elif kind == "space":
        # satellite: body, panels, antenna, and three small stars
        d.rectangle([cx - 30, cy - 8, cx - 8, cy + 8], fill=color)
        d.rectangle([cx + 8, cy - 8, cx + 30, cy + 8], fill=color)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=color)
        d.line([cx - 30, cy - 30, cx - 8, cy - 8], fill=color, width=3)
        d.line([cx + 30, cy + 30, cx + 8, cy + 8], fill=color, width=3)
        d.line([cx, cy - 7, cx, cy - 34], fill=color, width=3)
        d.ellipse([cx - 3, cy - 38, cx + 3, cy - 32], fill=color)
        for sx, sy in ((-40, 34), (38, -36), (44, 22)):
            d.ellipse([cx + sx - 3, cy + sy - 3, cx + sx + 3, cy + sy + 3],
                      fill=color)


STORIES = [
    {
        "tag": "SUMMIT  •  CHINA",
        "color": (27, 94, 143),
        "icon": "summit",
        "headline": "TRUMP, XI & PUTIN MEET IN SHENZHEN",
        "body": "The three leaders gather at the APEC summit; Xi hugged Trump on arrival ahead of trilateral talks.",
    },
    {
        "tag": "UKRAINE WAR",
        "color": (178, 58, 44),
        "icon": "bridge",
        "headline": "CRIMEAN BRIDGE HIT AGAIN",
        "body": "Ukraine strikes the key Russia-Crimea link; traffic is halted after a section is brought down.",
    },
    {
        "tag": "GAZA",
        "color": (178, 58, 44),
        "icon": "gaza",
        "headline": "ISRAEL PUSHES INTO GAZA",
        "body": "A rare ground operation beyond the ceasefire 'Yellow Line' sends families fleeing in central Gaza.",
    },
    {
        "tag": "MARKETS  •  AI",
        "color": (24, 122, 74),
        "icon": "ipo",
        "headline": "ANTHROPIC'S RECORD $81.3BN IPO",
        "body": "Claude-maker prices shares at $83, worth about $1.5tn, as trading starts today on Nasdaq as ANT.",
    },
    {
        "tag": "CULTURE",
        "color": (146, 96, 24),
        "icon": "art",
        "headline": "VAN GOGH SELLS FOR $190.4M",
        "body": "'Chestnut Trees in Blossom' sets an artist record at Sotheby's after a Nazi-era dispute is settled.",
    },
    {
        "tag": "SPACE",
        "color": (74, 60, 140),
        "icon": "space",
        "headline": "VOYAGER 1 REACHES ONE LIGHT-DAY",
        "body": "NASA's probe, nearly 50 years out, is about a light-day from Earth; confirmation is due today.",
    },
]


def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 174], fill=GOLD)
    title_f = font(SERIF_B, 62)
    d.text((512, 58), "THE WORLD TODAY", font=title_f, fill=(255, 255, 255),
           anchor="ma")
    date_f = font(SANS_B, 34)
    d.text((512, 128), "Thursday, 19 November 2026", font=date_f,
           fill=GOLD, anchor="ma")

    # ---- story grid: 2 columns x 3 rows ----
    margin, gap = 36, 20
    top, bottom = 188, 976
    cw = (W - 2 * margin - gap) // 2
    ch = (bottom - top - 2 * gap) // 3
    head_f = font(SANS_B, 28)
    body_f = font(SANS, 20)
    tag_f = font(SANS_B, 17)
    num_f = font(SANS_B, 26)

    for i, s in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (cw + gap)
        y0 = top + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        color = s["color"]

        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=(205, 200, 185),
                    width=2)
        d.rectangle([x0, y0, x1, y0 + 8], fill=color)

        # number badge
        bx, by = x0 + 26, y0 + 30
        d.ellipse([bx, by, bx + 46, by + 46], fill=color)
        d.text((bx + 23, by + 23), str(i + 1), font=num_f, fill=(255, 255, 255),
               anchor="mm")

        # icon, top right
        draw_icon(d, s["icon"], x1 - 58, y0 + 48, 40, color)

        # tag
        d.text((x0 + 88, y0 + 34), s["tag"], font=tag_f, fill=color)

        # headline (up to 2 lines)
        lines = wrap(d, s["headline"], head_f, cw - 48)
        hy = y0 + 96
        for ln in lines[:2]:
            d.text((x0 + 24, hy), ln, font=head_f, fill=INK)
            hy += 34

        # body (up to 3 lines)
        blines = wrap(d, s["body"], body_f, cw - 48)
        byy = hy + 6
        for ln in blines[:3]:
            d.text((x0 + 24, byy), ln, font=body_f, fill=MUTED)
            byy += 25

    # ---- footer ----
    foot_f = font(SANS, 18)
    d.text((512, 994),
           "Sources: BBC  •  The New York Times  •  Bloomberg  •  Sotheby's  •  NASA",
           font=foot_f, fill=MUTED, anchor="ma")
    return img


if __name__ == "__main__":
    image = build()
    image.save("entry.png", optimize=True)
    print("saved entry.png", image.size)

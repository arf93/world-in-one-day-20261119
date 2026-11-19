#!/usr/bin/env python3
"""Render the 19 November 2026 world-news front page (1024x1024 PNG).

Draws a clean modern newspaper front page with six verified stories in a
2x3 grid. Every pictogram is hand-drawn with PIL geometric shapes; no
photos, no external assets. All facts come from the six verified stories
listed in STORIES below.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- palette
NAVY = (13, 42, 74)          # header band
NAVY_DARK = (9, 30, 54)
GOLD = (232, 178, 74)        # header accent
RED_RULE = (178, 52, 40)     # thin rule under the header
PAPER = (247, 243, 236)      # page background
CARD = (255, 255, 255)       # story card
CARD_EDGE = (203, 196, 184)  # card border
INK = (24, 24, 24)           # headline text
BODY = (58, 58, 58)          # summary text
MUTED = (112, 108, 100)      # footer text
WHITE = (255, 255, 255)

# ---------------------------------------------------------------- fonts
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- stories
# (region label, accent colour, headline, summary) — facts only, as verified.
STORIES = [
    (
        "UKRAINE",
        (46, 111, 168),
        "CRIMEAN BRIDGE HIT A THIRD TIME",
        "Overnight strike closes the Kerch crossing again; Crimea's "
        "Russian-installed governor confirms the attack as damage is "
        "assessed.",
    ),
    (
        "SHENZHEN",
        (168, 50, 50),
        "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
        "First-ever trilateral of the three leaders at APEC; nuclear "
        "arms and Iran on the table, Ukraine left off the agenda.",
    ),
    (
        "GAMING",
        (107, 79, 161),
        "GTA VI BEGINS GLOBAL ROLLOUT",
        "Rockstar's long-awaited game launches worldwide; players "
        "return to Vice City on release day.",
    ),
    (
        "SAUDI ARABIA",
        (46, 125, 91),
        "HOUTHI MISSILE THREAT HITS RIYADH",
        "Saudi-led coalition says it dealt with a missile threat over "
        "the capital; debris fell and damage was reported, then the "
        "all-clear sounded.",
    ),
    (
        "BANGLADESH",
        (192, 86, 33),
        "BANGLADESH BRACES FOR LOCKDOWN",
        "Paramilitary troops deploy nationwide as unrest grows over "
        "ex-PM Hasina's planned return; blasts and arson blamed on "
        "her banned party.",
    ),
    (
        "CLIMATE",
        (14, 116, 144),
        "COP31 ENTERS FINAL STRETCH",
        "New draft text expected in Antalya as the climate summit "
        "nears its Friday close; IEA releases its World Energy "
        "Outlook.",
    ),
]

FOOTER = ("Sources: Reuters \u00b7 Al Jazeera \u00b7 The Hindu BusinessLine "
          "\u00b7 Oil Change International \u00b7 UN")

# ---------------------------------------------------------------- helpers


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, sizes, max_w, max_lines, bold=True):
    """Pick the largest font size (from sizes, descending) that wraps the
    text into at most max_lines lines. Returns (font, lines)."""
    path = FONT_BOLD if bold else FONT_REG
    for size in sizes:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(path, sizes[-1])
    return fnt, wrap(draw, text, fnt, max_w)


def tint(rgb, frac=0.88):
    """Mix a colour toward white to make a pale tile background."""
    return tuple(int(c + (255 - c) * frac) for c in rgb)


def rounded(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


# ---------------------------------------------------------------- pictograms
# Each draws a simple geometric pictogram centred at (cx, cy) inside a
# square of side s, in the given colour. No photos, no imported art.


def icon_bridge(d, cx, cy, s, c):
    x0, x1 = cx - s // 2 + 4, cx + s // 2 - 4
    deck_y = cy + 2
    d.line([(x0, deck_y), (x1, deck_y)], fill=c, width=4)
    for tx in (cx - s // 4, cx + s // 4):
        d.line([(tx, cy - s // 2 + 6), (tx, deck_y)], fill=c, width=4)
        d.line([(tx, cy - s // 2 + 6), (x0 + 4, deck_y)], fill=c, width=2)
        d.line([(tx, cy - s // 2 + 6), (x1 - 4, deck_y)], fill=c, width=2)
    for wy in (deck_y + 9, deck_y + 16):
        d.arc([x0, wy - 4, x1, wy + 4], 0, 180, fill=c, width=2)


def icon_summit(d, cx, cy, s, c):
    # Three leaders at a table: three heads above three shoulders.
    step = s // 3
    for i in (-1, 0, 1):
        hx = cx + i * step
        d.ellipse([hx - 8, cy - s // 2 + 6, hx + 8, cy - s // 2 + 22],
                  fill=c)
        d.pieslice([hx - 12, cy - 8, hx + 12, cy + 16], 180, 360, fill=c)
    d.line([(cx - s // 2 + 4, cy + s // 2 - 6),
            (cx + s // 2 - 4, cy + s // 2 - 6)], fill=c, width=4)


def icon_controller(d, cx, cy, s, c):
    x0, y0 = cx - s // 2 + 3, cy - s // 4
    x1, y1 = cx + s // 2 - 3, cy + s // 4 + 4
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, outline=c, width=4)
    px, py = cx - s // 4, cy + 2
    d.line([(px - 9, py), (px + 9, py)], fill=c, width=4)
    d.line([(px, py - 9), (px, py + 9)], fill=c, width=4)
    for bx in (cx + s // 4 - 5, cx + s // 4 + 5):
        d.ellipse([bx - 4, py - 4, bx + 4, py + 4], fill=c)
    d.line([(cx - s // 4, y0 - 5), (cx - s // 4 + 8, y0 - 5)],
           fill=c, width=3)
    d.line([(cx + s // 4 - 8, y0 - 5), (cx + s // 4, y0 - 5)],
           fill=c, width=3)


def icon_shield(d, cx, cy, s, c):
    # Shield with a small missile above it.
    mx, my = cx + 8, cy - s // 2 + 8
    d.polygon([(mx - 4, my + 8), (mx, my - 6), (mx + 4, my + 8)],
              fill=c)
    d.rectangle([mx - 3, my + 6, mx + 3, my + 14], fill=c)
    d.polygon([(mx - 7, my + 10), (mx - 3, my + 8), (mx - 3, my + 13)],
              fill=c)
    d.polygon([(mx + 7, my + 10), (mx + 3, my + 8), (mx + 3, my + 13)],
              fill=c)
    top = cy - 2
    d.polygon([(cx - s // 4, top), (cx + s // 4, top),
               (cx + s // 4, top + s // 4), (cx, top + s // 2 - 2),
               (cx - s // 4, top + s // 4)], outline=c, width=4)
    d.line([(cx - 7, top + 12), (cx + 7, top + 12)], fill=c, width=3)


def icon_lock(d, cx, cy, s, c):
    d.arc([cx - 13, cy - s // 2 + 8, cx + 13, cy - s // 2 + 34],
          180, 360, fill=c, width=5)
    d.rounded_rectangle([cx - 18, cy - 4, cx + 18, cy + s // 2 - 6],
                        radius=5, fill=c)
    d.ellipse([cx - 4, cy + 6, cx + 4, cy + 14], fill=PAPER)
    d.polygon([(cx - 3, cy + 11), (cx + 3, cy + 11), (cx, cy + 20)],
              fill=PAPER)


def icon_globe(d, cx, cy, s, c):
    r = s // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
              outline=c, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=c, width=3)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340,
          fill=c, width=3)
    # small leaf at the lower right
    lx, ly = cx + r - 2, cy + r - 6
    d.pieslice([lx - 10, ly - 12, lx + 6, ly + 4], 270, 90, fill=c)
    d.line([(lx - 8, ly - 2), (lx + 4, ly - 10)], fill=c, width=2)


ICONS = [icon_bridge, icon_summit, icon_controller,
         icon_shield, icon_lock, icon_globe]

# ---------------------------------------------------------------- page


def draw_header(d, w):
    d.rectangle([0, 0, w, 150], fill=NAVY)
    d.rectangle([0, 150, w, 156], fill=RED_RULE)
    # left: masthead
    d.text((24, 14), "THE WORLD IN ONE DAY",
           font=font(FONT_BOLD, 28), fill=GOLD)
    d.text((22, 46), "WORLD NEWS",
           font=font(FONT_BOLD, 62), fill=WHITE)
    # right: the day, large and unmissable
    d.text((w - 24, 16), "THURSDAY",
           font=font(FONT_BOLD, 30), fill=WHITE, anchor="ra")
    d.text((w - 24, 50), "19 NOVEMBER 2026",
           font=font(FONT_BOLD, 40), fill=GOLD, anchor="ra")
    d.text((w - 24, 104), "Six stories that shaped the day",
           font=font(FONT_REG, 20), fill=(205, 214, 226), anchor="ra")


def draw_card(d, x, y, cw, ch, story, idx):
    label, accent, headline, summary = story
    icon_fn = ICONS[idx]
    rounded(d, [x, y, x + cw, y + ch], radius=10,
            fill=CARD, outline=CARD_EDGE, width=2)
    pad = 18
    ix, iy = x + pad, y + pad
    tile = 62
    # icon tile
    rounded(d, [ix, iy, ix + tile, iy + tile], radius=8,
            fill=tint(accent))
    icon_fn(d, ix + tile // 2, iy + tile // 2, tile - 14, accent)
    # region label + rule
    lx = ix + tile + 14
    d.text((lx, iy + 6), label, font=font(FONT_BOLD, 24), fill=accent)
    d.line([(lx, iy + 44), (x + cw - pad, iy + 44)],
           fill=(216, 210, 200), width=2)
    # headline, bold, up to 2 lines
    hx, hy = x + pad, iy + tile + 12
    hw = cw - 2 * pad
    hf, hlines = fit_lines(d, headline, [30, 28, 26], hw, 2, bold=True)
    ty = hy
    for line in hlines:
        d.text((hx, ty), line, font=hf, fill=INK)
        ty += hf.size + 4
    # summary, up to 3 lines
    sy = ty + 6
    sf, slines = fit_lines(d, summary, [19, 18, 17, 16], hw, 3,
                           bold=False)
    for line in slines:
        d.text((hx, sy), line, font=sf, fill=BODY)
        sy += sf.size + 5


def main():
    W = H = 1024
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    draw_header(d, W)

    # 2 x 3 grid of story cards
    margin, gap = 24, 16
    grid_top, grid_bottom = 172, 956
    cw = (W - 2 * margin - gap) // 2
    ch = (grid_bottom - grid_top - 2 * gap) // 3
    for i, story in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = margin + col * (cw + gap)
        y = grid_top + row * (ch + gap)
        draw_card(d, x, y, cw, ch, story, i)

    # footer
    d.text((W // 2, 970), FOOTER, font=font(FONT_REG, 17),
           fill=MUTED, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the front page for make.fun news-image-01: "The World Today",
Friday 13 November 2026.

Written fresh in this session (after the competition opened at
2026-11-13T20:00Z). The page is composed with PIL, not generated as
one image, because image generators garble text: every word on the
page is rendered here, in a large legible typeface, from the verified
facts below. The one picture on the page -- the Senate hearing room
with two empty witness chairs -- is a generated illustration
(senate-illustration.webp, beside this script) with no text in it; it
is cropped and pasted in, and everything else is drawn.

Stories (all first reported on 13 November 2026, each checked against
the outlet named in its line):
  1. Senate Banking Chair Tim Scott summoned ex-Nvidia chief Jensen
     Huang (Dec 3) and Commerce Secretary Howard Lutnick (Dec 10)
     over alleged AI-chip leaks to China, a day after Huang quit as
     Nvidia chief; Scott warned Huang of a subpoena if he refuses.
     (Al Jazeera, Reuters)
  2. US envoys say Putin agreed Europeans join the next round of
     Ukraine peace talks; a Ukrainian drone hit the Russian corvette
     Naro-Fominsk in the Gulf of Finland, a strike Finland's defence
     forces said they detected. (BBC, Reuters)
  3. An Israeli strike hit Nasser Hospital in Khan Younis, killing six
     people including a surgeon and a 13-year-old boy, and wounding
     27. Israel said it targeted a Hamas commander inside the
     complex. (Associated Press, Al Jazeera)
  4. The FBI said North Korean hackers used 900+ deepfake videos and
     fake video calls over 18 months to steal about $400m in crypto.
     (BBC)
Also today (bottom strip): Harry Kane's record 126th England cap and
the US record 483,200 deportations in 2026 (both Al Jazeera), and the
worldwide Microsoft 365 outage -- Outlook and Teams down, 140,000
reports in 74 countries (BBC / Downdetector).

Run:  python3 build_frontpage.py   (writes news.jpg beside this script)
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (19, 38, 75)
RED = (176, 42, 48)
GREY = (90, 90, 90)
RULE = (200, 192, 175)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit_font(draw, lines, path, start_size, max_width, min_size=20):
    """Largest font size at which every line fits `max_width` px."""
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        if all(draw.textlength(line, font=fnt) <= max_width for line in lines):
            return fnt, size
        size -= 1
    return font(path, min_size), min_size


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_icon_ukraine(draw, x, y, w, h):
    """Round table with three small flags: Ukraine, US, EU."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    # table
    draw.ellipse([x + 66, y + 96, x + w - 66, y + 122], fill=(122, 84, 52))
    draw.rectangle([x + 146, y + 118, x + w - 146, y + h], fill=(96, 64, 40))
    # three flag poles
    specs = [
        (x + 78, [(0, 90, 180), (255, 213, 0)]),          # Ukraine blue/yellow
        (x + 141, [(178, 34, 52), (255, 255, 255)]),      # US red/white
        (x + 204, [(0, 51, 153), (255, 204, 0)]),         # EU blue/gold
    ]
    for px, colours in specs:
        draw.line([px + 24, y + 18, px + 24, y + 98], fill=(60, 60, 60), width=3)
        draw.rectangle([px, y + 20, px + 48, y + 38], fill=colours[0])
        draw.rectangle([px, y + 38, px + 48, y + 56], fill=colours[1])
        if colours[0] == (0, 51, 153):
            for dx, dy in [(10, 8), (30, 8), (20, 18)]:
                draw.ellipse([px + dx, y + 22 + dy, px + dx + 5, y + 27 + dy],
                             fill=(255, 204, 0))


def draw_icon_hospital(draw, x, y, w, h):
    """White hospital building with a red cross."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 222, 205))
    draw.rectangle([x + 96, y + 30, x + w - 96, y + h], fill=(255, 255, 255))
    draw.rectangle([x + 60, y + 62, x + w - 60, y + h], fill=(238, 238, 238))
    # red cross on the tower
    cx, cy = x + w // 2, y + 62
    draw.rectangle([cx - 8, cy - 26, cx + 8, cy + 10], fill=RED)
    draw.rectangle([cx - 26, cy - 8, cx + 26, cy + 8], fill=RED)
    # windows
    for wx in (x + 76, x + 118, x + 160, x + 202):
        draw.rectangle([wx, y + 92, wx + 22, y + 112], fill=(120, 160, 190))
    draw.rectangle([x + 138, y + 118, x + 174, y + h], fill=(90, 90, 90))


def draw_icon_cyber(draw, x, y, w, h):
    """Laptop with a masked face on its screen and gold coins."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 38, 64))
    # screen
    draw.rounded_rectangle([x + 86, y + 22, x + 226, y + 102], radius=6,
                           fill=(16, 24, 44), outline=(150, 170, 200), width=3)
    # masked figure: dark hood, pale face, dark eye band
    draw.ellipse([x + 126, y + 34, x + 186, y + 90], fill=(8, 12, 24))
    draw.ellipse([x + 136, y + 48, x + 176, y + 86], fill=(210, 190, 170))
    draw.rectangle([x + 140, y + 58, x + 172, y + 66], fill=(8, 12, 24))
    # base
    draw.polygon([(x + 66, y + 104), (x + 246, y + 104),
                  (x + 258, y + 118), (x + 54, y + 118)], fill=(120, 130, 150))
    # gold coins
    coin = (212, 175, 55)
    for cx, cy, r in [(x + 258, y + 96, 13), (x + 278, y + 112, 11),
                      (x + 252, y + 122, 10)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=coin,
                     outline=(140, 105, 20), width=2)
        draw.text((cx - 4, cy - 8), "$", font=font(SANS_B, 14), fill=(90, 65, 10))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead -----------------------------------------------------
    draw.rectangle([0, 0, W, 128], fill=NAVY)
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 66)
    draw.text(((W - draw.textlength(title, font=tf)) / 2, 14), title,
              font=tf, fill=(255, 255, 255))
    sub = "FRIDAY  13  NOVEMBER  2026    ·    ONE DAY IN WORLD NEWS"
    sf = font(SANS, 22)
    draw.text(((W - draw.textlength(sub, font=sf)) / 2, 92), sub,
              font=sf, fill=(200, 210, 230))
    draw.rectangle([0, 128, W, 134], fill=RED)

    # ---- Lead story: Senate summons ----------------------------------
    # Illustration: crop the wide webp to the lead box's ratio, paste in.
    ill = Image.open("senate-illustration.webp").convert("RGB")
    iw, ih = ill.size
    target_ratio = 460 / 354
    crop_w = int(ih * target_ratio)
    left = (iw - crop_w) // 2
    ill = ill.crop((left, 0, left + crop_w, ih)).resize((460, 354),
                                                        Image.LANCZOS)
    img.paste(ill, (24, 146))
    draw.rectangle([24, 146, 484, 500], outline=(180, 172, 155), width=2)
    cap = "Two empty witness chairs await Huang and Lutnick."
    draw.text((24, 508), cap, font=font(SANS, 17), fill=GREY)

    tx = 508
    text_w = 1000 - tx
    draw.text((tx, 146), "WASHINGTON  ·  TECHNOLOGY",
              font=font(SANS_B, 21), fill=RED)
    head = ["SENATE SUMMONS", "HUANG & LUTNICK"]
    hf, hsize = fit_font(draw, head, SANS_B, 52, text_w, min_size=30)
    y = draw_lines(draw, head, tx, 180, hf, INK, int(hsize * 1.16))
    body = ("Ex-Nvidia chief Jensen Huang testifies Dec 3 and Commerce "
            "Secretary Howard Lutnick Dec 10 over alleged AI-chip leaks "
            "to China \u2014 a day after Huang quit; Scott warned Huang "
            "of a subpoena if he refuses.")
    y = draw_lines(draw, wrap(draw, body, font(SANS, 23), text_w),
                   tx, y + 14, font(SANS, 23), (40, 40, 40), 30)
    draw.text((tx, y + 8), "Sources: Al Jazeera, Reuters",
              font=font(SANS, 18), fill=GREY)

    # ---- Divider ------------------------------------------------------
    draw.line([24, 552, 1000, 552], fill=RULE, width=2)

    # ---- Three story cards --------------------------------------------
    cards = [
        ("UKRAINE  ·  WAR & DIPLOMACY", draw_icon_ukraine,
         "EUROPE TO JOIN NEXT PEACE TALKS",
         "US envoys say Putin agreed Europeans join the next round; a "
         "Ukrainian drone hit the Russian corvette Naro-Fominsk."),
        ("GAZA  ·  MIDDLE EAST", draw_icon_hospital,
         "STRIKE ON GAZA HOSPITAL KILLS 6",
         "An Israeli strike hit Nasser Hospital in Khan Younis, killing "
         "six, including a surgeon and a boy of 13, and wounding 27."),
        ("CYBERCRIME  ·  TECHNOLOGY", draw_icon_cyber,
         "FBI: N. KOREA STOLE $400M IN CRYPTO",
         "Hackers used 900+ deepfake videos and fake video calls over "
         "18 months to impersonate contacts and steal crypto."),
    ]
    sources = ["Sources: BBC, Reuters", "Sources: AP, Al Jazeera",
               "Source: BBC"]
    xs = [24, 356, 688]
    for (kicker, icon, headline, body), x0, src in zip(cards, xs, sources):
        icon(draw, x0, 566, 312, 140)
        draw.text((x0, 712), kicker, font=font(SANS_B, 16), fill=RED)
        hf, hsize = fit_font(draw, wrap(draw, headline, font(SANS_B, 26), 312),
                             SANS_B, 26, 312, min_size=20)
        lines = wrap(draw, headline, hf, 312)
        y = draw_lines(draw, lines, x0, 736, hf, INK, int(hsize * 1.18))
        y = draw_lines(draw, wrap(draw, body, font(SANS, 18), 312),
                       x0, y + 6, font(SANS, 18), (40, 40, 40), 23)
        draw.text((x0, y + 4), src, font=font(SANS, 16), fill=GREY)

    # ---- Bottom strip: also today --------------------------------------
    draw.rectangle([0, 916, W, H], fill=NAVY)
    line1 = ("ALSO TODAY:   Kane breaks the England caps record \u2014 "
             "126th cap   \u00b7   US reports a record 483,200 deportations")
    line2 = ("Microsoft 365 down worldwide: 140,000 Outlook reports in "
             "74 countries   \u00b7   Sources: Al Jazeera, BBC")
    sf1, _ = fit_font(draw, [line1], SANS_B, 19, W - 48, min_size=14)
    sf2, _ = fit_font(draw, [line2], SANS_B, 19, W - 48, min_size=14)
    draw.text(((W - draw.textlength(line1, font=sf1)) / 2, 928), line1,
              font=sf1, fill=(255, 255, 255))
    draw.text(((W - draw.textlength(line2, font=sf2)) / 2, 960), line2,
              font=sf2, fill=(200, 210, 230))

    img.save("news.jpg", "JPEG", quality=88, optimize=True)
    import os
    print("news.jpg:", os.path.getsize("news.jpg"), "bytes,",
          img.size[0], "x", img.size[1])


if __name__ == "__main__":
    main()

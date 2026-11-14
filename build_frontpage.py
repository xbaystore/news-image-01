#!/usr/bin/env python3
"""Draw "The World Today" — a one-page newspaper front page summing up
Friday 13 November 2026, and save it as news.jpg next to this script.

Everything is drawn with Pillow from the facts baked into this file.
The lead illustration comes from senate-illustration.webp in the same
folder. Output is deterministic: same input, same bytes, every run.

Run:  python3 build_frontpage.py
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ILLUSTRATION = os.path.join(HERE, "senate-illustration.webp")
OUTPUT = os.path.join(HERE, "news.jpg")

W, H = 1024, 1024
PAPER = (248, 244, 236)      # warm newsprint
INK = (26, 26, 26)           # near-black
RED = (163, 22, 33)          # kicker red
GREY = (90, 86, 78)          # captions and dateline
RULE = (26, 26, 26)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines top to bottom; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_story(draw, x, y, width, kicker, headline, body):
    """One compact story: red kicker, bold headline, short body text.
    Returns the y just below the story."""
    kf = font(SANS_B, 14)
    hf = font(SERIF_B, 19)
    bf = font(SERIF, 14)
    y = draw_lines(draw, x, y, [kicker.upper()], kf, fill=RED, leading=18)
    y = draw_lines(draw, x, y, wrap(draw, headline, hf, width), hf, leading=23)
    y = draw_lines(draw, x, y + 2, wrap(draw, body, bf, width), bf, leading=19)
    return y


def main():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    margin = 36
    content_w = W - 2 * margin
    y = 26

    # ---- Masthead -------------------------------------------------------
    title_f = font(SERIF_B, 62)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=title_f)
    draw.text(((W - tw) / 2, y), title, font=title_f, fill=INK)
    y += 76
    draw.line([(margin, y), (W - margin, y)], fill=RULE, width=3)
    y += 8

    # ---- Dateline row ---------------------------------------------------
    date_f = font(SANS_B, 16)
    left = "FRIDAY 13 NOVEMBER 2026"
    right = "THE WORLD IN ONE PAGE"
    draw.text((margin, y), left, font=date_f, fill=INK)
    rw = draw.textlength(right, font=date_f)
    draw.text((W - margin - rw, y), right, font=date_f, fill=INK)
    y += 26
    draw.line([(margin, y), (W - margin, y)], fill=RULE, width=2)
    y += 14

    # ---- Lead headline + deck -------------------------------------------
    lead_f = font(SERIF_B, 36)
    lead = "Senate summons Huang and Lutnick"
    lw = draw.textlength(lead, font=lead_f)
    draw.text(((W - lw) / 2, y), lead, font=lead_f, fill=INK)
    y += 48
    deck_f = font(SERIF, 18)
    deck = (
        "Ex-Nvidia chief to testify on 3 December, Lutnick on 10 December "
        "\u2014 under threat of subpoena, a day after Huang quit. "
        "Nvidia shares fell 4.3%."
    )
    y = draw_lines(
        draw, margin + 40, y, wrap(draw, deck, deck_f, content_w - 80),
        deck_f, leading=24,
    )
    y += 8

    # ---- Lead illustration ----------------------------------------------
    photo = Image.open(ILLUSTRATION).convert("RGB")
    photo = ImageOps.fit(
        photo, (content_w, 240), Image.LANCZOS, centering=(0.5, 0.62)
    )
    draw.rectangle(
        [(margin - 2, y - 2), (W - margin + 2, y + 242)],
        outline=INK, width=2,
    )
    page.paste(photo, (margin, y))
    y += 250
    cap_f = font(SANS, 13)
    caption = (
        "An empty witness chair awaits in the Senate hearing room. "
        "(Illustration)"
    )
    draw.text((margin, y), caption, font=cap_f, fill=GREY)
    y += 26
    draw.line([(margin, y), (W - margin, y)], fill=RULE, width=2)
    y += 16

    # ---- Two columns of stories -----------------------------------------
    col_w = (content_w - 28) // 2
    left_x = margin
    right_x = margin + col_w + 28

    left_stories = [
        (
            "Ukraine \u00b7 Peace talks",
            "Zelensky meets US envoys as Europe joins the talks",
            "US envoys say Putin agreed Europeans will join the next "
            "round of talks, as Kyiv presses for a seat at the table.",
        ),
        (
            "Ukraine \u00b7 The war at sea",
            "Drone hits Russian warship in the Gulf of Finland",
            "A Ukrainian drone struck a Russian warship in the Gulf of "
            "Finland, Finland said, in a rare strike far from the front.",
        ),
        (
            "Middle East",
            "Iran claims strike on US radar site in Bahrain",
            "Tehran says it hit the radar site; Washington has not "
            "confirmed the claim.",
        ),
        (
            "Gaza",
            "Strike near Nasser Hospital injures 27",
            "Twenty-seven people were hurt near Nasser Hospital, "
            "medics said, as the war\u2019s toll kept rising.",
        ),
    ]
    right_stories = [
        (
            "Cybercrime",
            "FBI: North Korea stole $400m in crypto via fake video calls",
            "Hackers used deepfake calls over 18 months, in more than "
            "900 fake interviews, the FBI said.",
        ),
        (
            "Technology",
            "Microsoft 365 outage: 140,000 reports in 74 countries",
            "Outlook went down for users across 74 countries; "
            "Microsoft said it was working on a fix.",
        ),
        (
            "United States",
            "US reports record 483,200 deportations in 2026",
            "The highest annual total on record, officials said, as "
            "arrests also reached a new high.",
        ),
        (
            "Sport",
            "Kane wins record 126th England cap",
            "Harry Kane passed the caps record in the Nations League "
            "quarter-final against Croatia.",
        ),
    ]

    ly = y
    for story in left_stories:
        ly = draw_story(draw, left_x, ly, col_w, *story)
        ly += 8
    ry = y
    for story in right_stories:
        ry = draw_story(draw, right_x, ry, col_w, *story)
        ry += 8

    # ---- Footer ----------------------------------------------------------
    fy = max(ly, ry) + 4
    draw.line([(margin, fy), (W - margin, fy)], fill=RULE, width=2)
    foot_f = font(SANS, 13)
    footer = "Sources: BBC, Al Jazeera, AP, Blockonomi, Downdetector \u2014 13 November 2026."
    draw.text((margin, fy + 8), footer, font=foot_f, fill=GREY)

    page.save(OUTPUT, "JPEG", quality=92)
    print("wrote", OUTPUT)


if __name__ == "__main__":
    main()

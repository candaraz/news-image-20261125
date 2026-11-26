#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - news-image-20261125 entry generator.

Renders a dense one-page broadsheet of Wednesday 25 November 2026 world
news to entry.png (1024x1024). Every story below was published on
25 November 2026 and checked item by item against the day's reporting
(Reuters, AP, AFP, WSJ, CNN and the wires). Stories that broke on
Tuesday 24 November are listed separately in the DATE CHECK box and
deliberately left out of the news columns.

Deterministic: pure PIL drawing, no clocks, no randomness.
Fonts resolve relative to this script file, never the CWD.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 24, 20)
FAINT = (96, 88, 74)
ACCENT = (163, 22, 33)
RULE = (26, 24, 20)
BOXBG = (238, 230, 210)
LEADBG = (240, 234, 216)


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, name), size)


F_SERIF = "LiberationSerif-Regular.ttf"
F_BOLD = "LiberationSerif-Bold.ttf"
F_ITALIC = "LiberationSerif-Italic.ttf"

KICKER = font(F_BOLD, 13)
MASTHEAD = font(F_BOLD, 63)
DATELINE = font(F_SERIF, 15)
DATELINE_B = font(F_BOLD, 15)
LEAD_HEAD = font(F_BOLD, 30)
LEAD_DECK = font(F_SERIF, 14.5)
SECT = font(F_BOLD, 13)
HEAD = font(F_BOLD, 11.5)
DECK = font(F_SERIF, 10)
BOX_HEAD = font(F_BOLD, 12.5)
BOX_TXT = font(F_SERIF, 10)
FOOT = font(F_ITALIC, 10.5)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_story(draw, x, y, col_w, head, deck):
    """One headline + one-line deck; returns y after the story."""
    for ln in wrap(draw, head, HEAD, col_w):
        draw.text((x, y), ln, font=HEAD, fill=INK)
        y += 13
    for ln in wrap(draw, deck, DECK, col_w):
        draw.text((x, y), ln, font=DECK, fill=(52, 48, 40))
        y += 11.5
    return y + 5.0


def draw_section(draw, x, y, col_w, title, stories):
    """Section header bar followed by its stories."""
    draw.rectangle([x, y, x + col_w, y + 17], fill=INK)
    draw.text((x + 6, y + 2.5), title, font=SECT, fill=PAPER)
    y += 23
    for head, deck in stories:
        y = draw_story(draw, x, y, col_w, head, deck)
    return y + 4


def draw_courthouse(draw, x, y, w_, h_):
    """Simple geometric courthouse: pediment, columns, steps, scales."""
    cx = x + w_ // 2
    # pediment
    draw.polygon([(x + 8, y + 26), (x + w_ - 8, y + 26), (cx, y + 2)], outline=INK, width=3)
    draw.line([x + 4, y + 30, x + w_ - 4, y + 30], fill=INK, width=3)
    # columns
    top = y + 38
    bot = y + h_ - 26
    n = 5
    for i in range(n):
        px = x + 18 + i * ((w_ - 36) // (n - 1))
        draw.line([px, top, px, bot], fill=INK, width=5)
        draw.line([px - 5, top, px + 5, top], fill=INK, width=3)
        draw.line([px - 5, bot, px + 5, bot], fill=INK, width=3)
    draw.line([x + 4, bot + 6, x + w_ - 4, bot + 6], fill=INK, width=3)
    # steps
    draw.line([x, bot + 14, x + w_ , bot + 14], fill=INK, width=3)
    draw.line([x - 0, bot + 21, x + w_, bot + 21], fill=FAINT, width=2)
    # scales of justice above the pediment centre
    draw.line([cx, y - 0, cx, y + 0], fill=INK, width=1)


# ---------------------------------------------------------------- stories
# Every item: published Wednesday 25 November 2026, verified item by item.

LEAD_HEADLINE = "HUAWEI GUILTY IN NEW YORK"
LEAD_TEXT = (
    "A Brooklyn jury convicts the Chinese telecom giant on 10 of 12 counts - "
    "conspiring to steal US trade secrets, defrauding banks and violating Iran "
    "sanctions - after an 11-week trial. Sentencing is set for September 2027; "
    "Huawei, acquitted of racketeering, says the verdict lacks merit."
)

ASIA_PACIFIC = [
    ("Shanghai chief Chen Jining in graft probe",
     "City leaders pledge loyalty to Beijing as the Politburo member falls."),
    ("Bangladesh garment wage up 36% after protests",
     "Wage board sets 17,000 taka ($137) from Dec 1; fresh clashes follow."),
    ("Solomon Islands sign Australia security treaty",
     "Canberra named primary partner; the pact bars any foreign base."),
    ("Hong Kong watchdog chases HK$131M in loans",
     "Audit office urges faster recovery of outstanding public lending."),
    ("South Korea drafts stablecoin rules",
     "The draft framework may also ease the long-standing ICO ban."),
    ("SBI and SMFG launch Solana venture in Japan",
     "Two banking giants team up on a joint blockchain business."),
    ("Australia to fine platforms under safety laws",
     "Online safety bill with heavy penalties nears passage."),
]

EUROPE = [
    ("UK energy bills to jump 26% in January",
     "The regulator confirms the rise as winter demand peaks."),
    ("Poundland collapses; 11,000 jobs at risk",
     "The discount chain enters administration after a brutal year."),
    ("EU plans a 50 billion euro AI and quantum fund",
     "Brussels moves to close the frontier-technology gap."),
    ("Italy rebukes Ukraine over Libya ship attacks",
     "Rome protests the strikes on Russian vessels off Libya."),
    ("Norse Atlantic warns finances are critical",
     "Shares plunge 77% as the airline fights to stay aloft."),
]

AMERICAS = [
    ("US proposes tariffs on 14 trading partners",
     "China faces 20% on top of old duties after the capacity probe."),
    ("Troops storm Cartagena store, free all hostages",
     "Dawn raid ends the 17-hour siege; one gunman killed."),
    ("Medicare sets 2028 prices for 13 drugs",
     "Negotiated cuts run as deep as 84% on the new list."),
    ("Treasury crime watchdog hit by cyberattack",
     "The FinCEN breach is treated as a suspected hostile hack."),
    ("US pauses joint operations with Ecuador",
     "Missions halt while a deadly raid is investigated."),
    ("Abrego Garcia arrives in Spain under deal",
     "He leaves the US after months at the centre of a legal fight."),
    ("Army detonates five tons of lead azide in Iowa",
     "The unstable explosive stockpile is destroyed in a blast."),
    ("Bank of Canada warns on inflation pressure",
     "The governor says price pressures will persist into 2027."),
]

MIDDLE_EAST_AFRICA = [
    ("Houthis claim Riyadh tower strike; 11 wounded",
     "Saudi jets answer with strikes on Yemen's port of Hodeidah."),
    ("Iraq court lets Baghdad deploy on Kurd borders",
     "Top court rules federal troops may guard the frontier."),
    ("Drone strikes kill 19 civilians in Sudan",
     "A rights group blames the attacks in Blue Nile state."),
    ("Ramaphosa wins bid to void impeachment report",
     "Court sets aside the report against South Africa's president."),
    ("Man convicted over plan to fight for Russia",
     "A South African court convicts the Zimbabwean volunteer."),
    ("Two Libyan officers die after drone hit ship",
     "They succumbed to wounds from the strike on a Russian warship."),
]

WAR_UKRAINE = [
    ("Putin vows revenge for refinery attacks",
     "Moscow promises retaliation as Ukrainian strikes bite."),
    ("Russian strike kills two in Odesa region",
     "The governor confirms the deaths in the overnight attack."),
    ("US shelves business deals with Russia",
     "Washington drops planned deals over the Ukraine war."),
    ("Russian data: 490,334 soldiers dead",
     "Government figures give the war's starkest toll yet."),
]

TECH_MARKETS = [
    ("Tidal to delete 29M AI-generated songs",
     "Fully AI tracks are banned from 9 December, a first for streaming."),
    ("Bitcoin slides below $60,000",
     "An eighth straight weekly loss looms over crypto markets."),
    ("Nvidia board scrutinised over Huang return",
     "Directors face questions after reinstating the chief executive."),
    ("Ukraine legalises crypto, tax from 2027",
     "Parliament passes the market law taking effect next July."),
    ("US blacklists Megaspeed and Alibaba unit",
     "Export controls widen in the chip dispute with China."),
    ("Shein revenue falls 5.9% on EU curbs",
     "Third-quarter sales dip as the new trade rules bite."),
]

SPORT = [
    ("Champions League: Sabah host Barcelona",
     "Sporting face Manchester United on Matchday 5."),
    ("Haaland: City are questioning everything",
     "The striker admits doubts after the draw with Napoli."),
    ("Williams fined 627,000 pounds over cost cap",
     "The FIA punishes the team for overspending in 2025."),
]

DATE_CHECK = [
    "COP31 talks in Turkey end without a deal",
    "Shenzhou-24 launches with first foreign astronaut",
    "Spain heads to a snap election",
    "UK warns Ukraine suppliers of sabotage threat",
    "Zelenskiy confirms Gulf of Finland ship strike",
    "BepiColombo enters orbit around Mercury",
    "Sanofi agrees to buy Insmed for $41 billion",
    "UK court jails GTA VI hacker for seven years",
]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # page margin

    # --- masthead ------------------------------------------------------
    d.line([M, 16, W - M, 16], fill=INK, width=2)
    kick = "ONE IMAGE  ·  EVERY STORY CHECKED AGAINST THE DAY ITSELF"
    d.text(((W - d.textlength(kick, font=KICKER)) / 2, 22), kick, font=KICKER, fill=ACCENT)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=MASTHEAD)) / 2, 40), title, font=MASTHEAD, fill=INK)
    d.line([M, 116, W - M, 116], fill=INK, width=4)
    d.line([M, 122, W - M, 122], fill=INK, width=1)
    left = "Wednesday 25 November 2026"
    d.text((M, 128), left, font=DATELINE_B, fill=INK)
    mid = "40 stories · 7 regions · one page"
    d.text(((W - d.textlength(mid, font=DATELINE)) / 2, 128), mid, font=DATELINE, fill=FAINT)
    right = "No. 25 — Daily Edition"
    d.text((W - M - d.textlength(right, font=DATELINE), 128), right, font=DATELINE, fill=INK)
    d.line([M, 150, W - M, 150], fill=INK, width=1)

    # --- lead panel ----------------------------------------------------
    ly = 158
    d.rectangle([M, ly, W - M, ly + 118], fill=LEADBG, outline=INK, width=2)
    draw_courthouse(d, M + 18, ly + 14, 168, 92)
    tx = M + 208
    tw = W - M - tx - 14
    d.text((tx, ly + 10), LEAD_HEADLINE, font=LEAD_HEAD, fill=ACCENT)
    yy = ly + 48
    for ln in wrap(d, LEAD_TEXT, LEAD_DECK, tw):
        d.text((tx, yy), ln, font=LEAD_DECK, fill=INK)
        yy += 18

    # --- body columns --------------------------------------------------
    top = 292
    col_w = (W - 2 * M - 2 * 16) // 3
    xs = [M, M + col_w + 16, M + 2 * (col_w + 16)]
    for x in xs[1:]:
        d.line([x - 8, top, x - 8, 852], fill=(190, 180, 158), width=1)

    y1 = draw_section(d, xs[0], top, col_w, "ASIA-PACIFIC", ASIA_PACIFIC)
    y1 = draw_section(d, xs[0], y1, col_w, "SPORT", SPORT)
    y2 = draw_section(d, xs[1], top, col_w, "EUROPE", EUROPE)
    y2 = draw_section(d, xs[1], y2, col_w, "WAR IN UKRAINE", WAR_UKRAINE)
    y2 = draw_section(d, xs[1], y2, col_w, "TECH, AI & MARKETS", TECH_MARKETS[:3])
    y3 = draw_section(d, xs[2], top, col_w, "AMERICAS", AMERICAS)
    y3 = draw_section(d, xs[2], y3, col_w, "MIDDLE EAST & AFRICA", MIDDLE_EAST_AFRICA[:4])

    # second row of sections under the columns, full width pairs
    by = max(y1, y2, y3) + 2
    half = (W - 2 * M - 16) // 2
    draw_section(d, M, by, half, "MIDDLE EAST & AFRICA — MORE", MIDDLE_EAST_AFRICA[4:])
    draw_section(d, M + half + 16, by, half, "TECH, AI & MARKETS — MORE", TECH_MARKETS[3:])

    # --- date check box -------------------------------------------------
    by2 = 866
    d.rectangle([M, by2, W - M, by2 + 96], fill=BOXBG, outline=ACCENT, width=2)
    d.text((M + 12, by2 + 8),
           "DATE CHECK — reported Tuesday 24 November, checked and deliberately left out:",
           font=BOX_HEAD, fill=ACCENT)
    half_items = (len(DATE_CHECK) + 1) // 2
    for i, item in enumerate(DATE_CHECK):
        cx = M + 12 + (i // half_items) * half
        cy = by2 + 32 + (i % half_items) * 15
        d.text((cx, cy), "x  " + item, font=BOX_TXT, fill=INK)

    # --- footer ----------------------------------------------------------
    fy = by2 + 106
    d.line([M, fy, W - M, fy], fill=INK, width=2)
    foot = ("Every story above was published on Wednesday 25 November 2026 and checked item by item. "
            "Sources: Reuters · AP · AFP · WSJ · CNN · BBC · Al Jazeera and the day's wires.")
    d.text(((W - d.textlength(foot, font=FOOT)) / 2, fy + 7), foot, font=FOOT, fill=FAINT)

    # --- save ------------------------------------------------------------
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = "/output" if os.path.isdir("/output") and os.access("/output", os.W_OK) else HERE
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    print(render())

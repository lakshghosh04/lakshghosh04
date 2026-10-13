"""Writes assets/fortune.svg with a new random fortune. Run daily by a GitHub Action."""
import datetime, random, re, textwrap
from pathlib import Path
from xml.sax.saxutils import escape, unescape

FORTUNES = [
    "A clear question is half of the answer.",
    "Check the data before you trust the story.",
    "Build the smallest thing that tests the idea.",
    "The right tool is the one the problem asks for.",
    "Measure what changes a decision.",
    "Start with who the work is for.",
    "A chart nobody acts on is just decoration.",
    "Simple explanations travel the furthest.",
    "Good analysis ends with a next step.",
    "Ask what would change your mind.",
    "Practical beats impressive.",
    "Understand the process before you automate it.",
    "Numbers answer questions. People ask them.",
    "Clarity is a skill. Practise it daily.",
    "Technology is a means, never the point.",
    "Small experiments make big decisions easier.",
    "Context turns data into information.",
    "Fix the problem, not the symptom.",
    "A good brief saves a week of work.",
    "Listen first. Then analyse.",
    "Every dataset has a story and a caveat.",
    "Progress is shipping the small version.",
    "Be curious about the boring parts.",
    "Say what you know, and what you don't.",
]

FONT = "Inter, -apple-system, 'SF Pro Display', 'Segoe UI', Helvetica, Arial, sans-serif"

# 22 x 12 pixel fortune cookie
SPANS = [(7, 14), (4, 17), (2, 19), (1, 20), (0, 21), (0, 21), (0, 21), (1, 20), (1, 20),
         (2, 9, 12, 19), (3, 7, 14, 18), (4, 6, 15, 17)]
HILITE = {(6, 1), (7, 1), (5, 2)}
INTERIOR = {(x, y) for y, (a, b) in {9: (10, 11), 10: (8, 13), 11: (7, 14)}.items() for x in range(a, b + 1)}
SLIP = {(10, 9): "#F5F5F7", (11, 9): "#D5DBE3", (10, 10): "#F5F5F7", (11, 10): "#D5DBE3",
        (10, 11): "#F5F5F7", (11, 11): "#D5DBE3", (10, 12): "#F5F5F7", (11, 12): "#D5DBE3"}

def pixel_color(x, y):
    if (x, y) in HILITE: return "#FCE8B0"
    if x in (10, 11) and 3 <= y <= 8: return "#B9761F"
    if y <= 1 or (y <= 3 and x <= 4): return "#F4CD7A"
    if (y == 2 or y == 7) and (x + y) % 2 == 0: return "#E7B04E" if y == 2 else "#D99A3A"
    if y >= 8 or x >= 18: return "#C98A2D"
    return "#E7B04E"

def cookie_rects(px, ox=0, oy=0):
    out = []
    for (x, y) in sorted(INTERIOR):
        out.append(f'<rect x="{ox + x * px}" y="{oy + y * px}" width="{px}" height="{px}" fill="#6B3F12"/>')
    for (x, y), c in SLIP.items():
        out.append(f'<rect x="{ox + x * px}" y="{oy + y * px}" width="{px}" height="{px}" fill="{c}"/>')
    for y, spans in enumerate(SPANS):
        for i in range(0, len(spans), 2):
            for x in range(spans[i], spans[i + 1] + 1):
                out.append(f'<rect x="{ox + x * px}" y="{oy + y * px}" width="{px}" height="{px}" fill="{pixel_color(x, y)}"/>')
    return '<g shape-rendering="crispEdges">' + ''.join(out) + '</g>'

def build(text, date):
    lines = textwrap.wrap(text, 40)[:2]
    w, h, pad = 720, 150, 14
    px = 4
    t = ''.join(f'<text x="170" y="{86 + i * 30}" font-family="{FONT}" font-size="22" font-weight="500" fill="#E6EDF3">{escape(l)}</text>' for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w+2*pad} {h+2*pad}" width="{w+2*pad}" height="{h+2*pad}" role="img">
<title>{escape(text)}</title>
<defs>
<linearGradient id="gf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.09"/><stop offset="1" stop-color="#fff" stop-opacity="0.035"/></linearGradient>
<linearGradient id="tl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.08"/><stop offset="0.5" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="sp" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#FFB84D" stop-opacity="0.45"/><stop offset="1" stop-color="#FFB84D" stop-opacity="0"/></radialGradient>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0.12 0 0 0 0"/></filter>
<clipPath id="cr"><rect width="{w}" height="{h}" rx="40"/></clipPath>
</defs>
<g transform="translate({pad} {pad})">
<rect width="{w}" height="{h}" rx="40" fill="url(#gf)"/>
<rect width="{w}" height="{h}" rx="40" fill="url(#tl)"/>
<rect width="{w}" height="{h}" fill="#fff" filter="url(#grain)" clip-path="url(#cr)"/>
<rect x="40" y="0.5" width="{w-80}" height="1" fill="url(#sp)"/>
<circle cx="88" cy="75" r="62" fill="url(#warm)"><animate attributeName="opacity" values="0.6;1;0.6" dur="6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/></circle>
{cookie_rects(px, 44, 51)}
<text x="170" y="52" font-family="{FONT}" font-size="13" font-weight="500" letter-spacing="0.8" fill="#8B949E">TODAY'S FORTUNE</text>
{t}
<text x="{w-34}" y="{h-26}" text-anchor="end" font-family="{FONT}" font-size="12" fill="#6E7681">{escape(date)}</text>
</g></svg>'''

def main():
    out = Path(__file__).resolve().parent.parent / "assets" / "fortune.svg"
    last = None
    if out.exists():
        m = re.search(r"<title>(.*?)</title>", out.read_text(encoding="utf-8"), re.S)
        if m: last = unescape(m.group(1))
    choices = [f for f in FORTUNES if f != last] or FORTUNES
    text = random.choice(choices)
    out.write_text(build(text, datetime.date.today().strftime("%d %b %Y")), encoding="utf-8")
    print("Fortune:", text)

if __name__ == "__main__":
    main()

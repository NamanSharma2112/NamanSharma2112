import json
from pathlib import Path
from datetime import datetime

INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0"
]

CELL = 12
GAP = 4
STEP = CELL + GAP

with open(INPUT, "r", encoding="utf-8") as f:
    days = json.load(f)

if not days:
    raise ValueError("No contribution data found.")

# Group contributions by date
contributions = {
    item["date"]: item["level"]
    for item in days
}

dates = sorted(contributions.keys())

# Find the first Sunday before/at the first date
first_date = datetime.strptime(dates[0], "%Y-%m-%d").date()
start = first_date

while start.weekday() != 6:
    start = start.replace(day=start.day - 1)

# SVG dimensions
weeks = 53
width = weeks * STEP + 40
height = 7 * STEP + 60

rectangles = []

for week in range(weeks):
    for day in range(7):

        index = week * 7 + day

        if index >= len(dates):
            continue

        date = dates[index]
        level = contributions.get(date, 0)

        x = 20 + week * STEP
        y = 20 + day * STEP

        color = PALETTE[min(level, len(PALETTE) - 1)]

        rectangles.append(
            f'''
            <rect
                x="{x}"
                y="{y}"
                width="{CELL}"
                height="{CELL}"
                rx="3"
                fill="{color}">
                <title>{date}: {level}</title>
            </rect>
            '''
        )

total = sum(item["count"] for item in days)

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{width}"
height="{height}"
viewBox="0 0 {width} {height}">

<rect width="100%" height="100%" fill="#0d1117" rx="10"/>

<style>
rect {{
    opacity: 0;
    animation: appear 0.4s ease forwards;
}}

@keyframes appear {{
    from {{
        opacity: 0;
        transform: translateY(-5px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}
</style>

{''.join(
    r.replace(
        '<rect',
        f'<rect style="animation-delay:{i * 0.003}s"'
    )
    for i, r in enumerate(rectangles)
)}

<text
x="20"
y="{height - 15}"
fill="#8b949e"
font-family="monospace"
font-size="12">

{total} contributions

</text>

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Created {OUTPUT}")
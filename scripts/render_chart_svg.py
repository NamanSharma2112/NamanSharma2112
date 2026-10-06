import json
from pathlib import Path
from datetime import datetime

INPUT = Path("data/contributions.json")
OUTPUT = Path("contribution-chart.svg")

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

# Group contribution levels by month
monthly = {}

for item in data:
    date = datetime.strptime(item["date"], "%Y-%m-%d")
    month = date.strftime("%b %Y")

    monthly.setdefault(month, 0)
    monthly[month] += item.get("level", 0)

months = list(monthly.keys())
values = list(monthly.values())

if not values:
    raise ValueError("No contribution data found.")

max_value = max(values)

if max_value == 0:
    max_value = 1

width = 1000
height = 300
padding = 45

points = []

for i, value in enumerate(values):
    if len(values) == 1:
        x = width / 2
    else:
        x = padding + i * ((width - 2 * padding) / (len(values) - 1))

    y = height - padding - (
        value / max_value
    ) * (height - 2 * padding)

    points.append((x, y))

point_string = " ".join(
    f"{x:.1f},{y:.1f}" for x, y in points
)

circles = ""

for i, (x, y) in enumerate(points):
    circles += f'''
    <circle
        cx="{x:.1f}"
        cy="{y:.1f}"
        r="4"
        fill="#39d353">
        <title>{months[i]}: activity level {values[i]}</title>
    </circle>
    '''

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{width}"
height="{height}"
viewBox="0 0 {width} {height}">

<rect
width="100%"
height="100%"
rx="12"
fill="#0d1117"/>

<text
x="45"
y="30"
fill="#8b949e"
font-family="Arial, sans-serif"
font-size="14">
GitHub Activity Trend
</text>

<polyline
fill="none"
stroke="#39d353"
stroke-width="4"
stroke-linecap="round"
stroke-linejoin="round"
points="{point_string}"/>

{circles}

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Created {OUTPUT}")
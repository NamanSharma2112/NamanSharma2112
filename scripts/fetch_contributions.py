import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

USERNAME = "NamanSharma2112"

URL = f"https://github.com/users/{USERNAME}/contributions"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print("Status:", response.status_code)
print("Page size:", len(response.text))

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

# GitHub currently uses data-date/data-level attributes
for element in soup.find_all(attrs={"data-date": True}):

    date = element.get("data-date")
    level = element.get("data-level", "0")

    # GitHub's contribution count is usually stored in the aria-label
    aria = element.get("aria-label", "")

    count = 0

    # Try to extract the number from the aria-label
    if aria:
        import re
        match = re.search(r"(\d+)\s+contribution", aria)

        if match:
            count = int(match.group(1))

    try:
        level = int(level)
    except ValueError:
        level = 0

    days.append({
        "date": date,
        "count": count,
        "level": level
    })

# Remove duplicates
unique_days = {}

for day in days:
    unique_days[day["date"]] = day

days = list(unique_days.values())

days.sort(key=lambda x: x["date"])

output = Path("data/contributions.json")
output.parent.mkdir(parents=True, exist_ok=True)

with open(output, "w", encoding="utf-8") as f:
    json.dump(days, f, indent=2)

print(f"Saved {len(days)} contribution days.")

if days:
    print("First:", days[0])
    print("Last:", days[-1])
else:
    print("WARNING: GitHub contribution elements were not found.")
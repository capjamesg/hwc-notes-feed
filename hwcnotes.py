import requests
from bs4 import BeautifulSoup
import jinja2
from sortedcontainers import SortedDict
import re

# open template.html
template = open("template.html").read()

data = requests.get(
    "https://indieweb.org/wiki/index.php?title=Special:PrefixIndex&from=events%2F2023-05-31-hwc-pacific&prefix=events%2F&order=desc"
)

event_names = {
    "hwc-pacific": "HWC Pacific",
    "hwc-europe": "HWC Europe",
    "front-end": "Front-End Study Hall",
    "writing": "HWC Writing",
    "nuremberg": "HWC Nuremberg",
    "more": "More Events",
    "all": "All Events"
}

link_groups = {
    "all": {},
    "hwc-pacific": {},
    "hwc-europe": {},
    "front-end": {},
    "writing": {},
    "writers": {},
    "nuremberg": {},
    "more": {},
}

merges = {"writing": ["writers"]}

for link in BeautifulSoup(data.text, "html.parser").find_all("a"):
    if link.get("href").startswith("/events") and re.search(
        r"\d{4}-\d{2}-\d{2}", link.get("href")
    ):
        yyyy_mm_dd = re.search(r"\d{4}-\d{2}-\d{2}", link.get("href"))
        match = re.search(r"hwc-pacific|hwc-europe|front-end|writing|writers|nuremberg", link.get("href"))
        if match:
            link_groups[match.group(0)][link.get("href")] = yyyy_mm_dd.group(0)
        else:
            link_groups["more"][link.get("href")] = yyyy_mm_dd.group(0)

for group in link_groups:
    if group in merges:
        for merge in merges[group]:
            link_groups[group].update(link_groups[merge])

    sorted_links = SortedDict(link_groups[group])
    # turn into sorted list
    sorted_link_list = sorted_links.items()
    sorted_link_list = sorted(sorted_link_list, key=lambda x: x[1], reverse=True)

    link_groups[group] = sorted_link_list

# delete merges
for items in merges.values():
    for i in items:
        del link_groups[i]

link_groups["all"] = []

for group in link_groups:
    link_groups["all"].extend(link_groups[group])

# sort
link_groups["all"] = sorted(link_groups["all"], key=lambda x: x[1], reverse=True)

rendered = jinja2.Template(template).render(events=link_groups, eventid2name=event_names)

with open("index.html", "w") as f:
    f.write(rendered)

#!/usr/bin/env python3
"""Tabulate LH038's SUSE clocks read (amendment of 20 November 2026) from its retained bodies.

  python3 -I studies/LH038/scripts/suse_clocks_tabulate.py studies/LH038/data/suse-clocks-<label>

For each followed advisory: the list message's date(s) as the pipermail archive shows them (UTC), the
Release Date the message carries, whether CVE-2026-98432 appears in the message, OSV's published and
modified; then the amendment's decision rule against the two clocks the record already holds (the
advisory page's Release Date, from the read of 17 November, and the CVE-page stamp, from LH036's page of
16 November, both as listed in the amendment). Offline; no request is made.
"""
import gzip, json, re, sys
from datetime import datetime

# The two clocks as the amendment lists them (UTC calendar days).
RELEASE_DAY = {a: "2026-10-24" for a in (24386, 24422, 24437, 24446)}
RELEASE_DAY.update({a: "2026-11-02" for a in range(24479, 24487)})
CVEPAGE_DAY = {a: "2026-10-29" for a in (24386, 24422, 24437, 24446)}
CVEPAGE_DAY.update({a: "2026-11-03" for a in range(24479, 24487)})

d = sys.argv[1]
counts = {}
print("advisory | list message date (UTC) | Release Date in message | CVE-2026-98432 in message | OSV published | OSV modified | list day matches")
for a in sorted(RELEASE_DAY):
    m = gzip.open(f"{d}/msg-{a}.raw.gz").read().decode("utf-8", "replace")
    dates = re.findall(r"<I>([^<]*\d{4})</I>", m)
    days = {datetime.strptime(" ".join(x.split()), "%a %b %d %H:%M:%S UTC %Y").strftime("%Y-%m-%d") for x in dates}
    rel = re.findall(r"Release Date:\s*([^\n<]*)", m)
    o = json.loads(gzip.open(f"{d}/osv-{a}.raw.gz").read())
    if len(days) != 1:
        verdict = "unclassed (dates on more than one day)"
    else:
        day = days.pop()
        r, c = day == RELEASE_DAY[a], day == CVEPAGE_DAY[a]
        verdict = "Release Date" if r and not c else "CVE-page stamp" if c and not r else "neither" if not (r or c) else "both"
    group = "24 October" if a < 24479 else "2 November"
    counts.setdefault(group, {}).setdefault(verdict, 0)
    counts[group][verdict] += 1
    print(f"SUSE-SU-2026:{a}-1 | {'; '.join(' '.join(x.split()) for x in dates)} | {rel[0].strip() if rel else 'not shown'} | "
          f"{'listed' if 'CVE-2026-98432' in m else 'not shown'} | {o.get('published')} | {o.get('modified')} | {verdict}")
print()
for g, v in counts.items():
    print(g, v)

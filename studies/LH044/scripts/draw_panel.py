#!/usr/bin/env python3
"""LH044 panel draw, as fixed in studies/LH044/brief.md (protocol 0.1), section "The panel".

Reads only the two frames retained before the brief (no network):
  - data/prebrief-2026-11-08T1915Z/p25.body: the Open Archives Initiative's static dump of
    registered OAI-PMH base URLs, ListFriends_HISTORICAL_2025-10-08.xml (7,103 entries).
  - data/prebrief-2026-11-08T1915Z/p02.body: Debian's mirror list page, www.debian.org/mirror/list.
Rule: parse every base URL; keep one per host (the lexicographically first URL); drop hosts that
are in panel/named.csv or are the frame's own host; sort hosts; draw with random.Random(SEED)
.sample: 40 OAI-PMH hosts and 20 Debian mirror hosts. Probe: the base URL with ?verb=Identify
(OAI-PMH, an api surface, marker '<Identify>') and <base>README (Debian, a file surface, marker
'Debian'). Writes panel/drawn.csv. Deterministic: re-running gives the same file.

Usage: python3 -I studies/LH044/scripts/draw_panel.py
"""
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit
import csv
import random
import re

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / 'data' / 'prebrief-2026-11-08T1915Z'
SEED = int(sha256(b'LH044 panel, fixed 8 November 2026').hexdigest(), 16)
N_OAI, N_DEB = 40, 20


def hosts_from(urls, exclude):
    by_host = {}
    for u in sorted(set(urls)):
        h = (urlsplit(u).hostname or '').lower()
        if not h or h in exclude:
            continue
        by_host.setdefault(h, u)
    return by_host


def main():
    named = {r['host'].lower() for r in csv.DictReader(open(ROOT / 'panel' / 'named.csv'))}
    oai_xml = (FRAMES / 'p25.body').read_text('utf-8', 'replace')
    oai_urls = [m.strip() for m in re.findall(r'<baseURL[^>]*>([^<]+)</baseURL>', oai_xml)]
    oai_urls = [u.replace('&amp;', '&') for u in oai_urls if u.startswith(('http://', 'https://'))]
    deb_html = (FRAMES / 'p02.body').read_text('utf-8', 'replace')
    deb_urls = re.findall(r'href="(https?://[^"]+/debian/)"', deb_html)

    oai = hosts_from(oai_urls, named | {'www.openarchives.org'})
    deb = hosts_from(deb_urls, named | {'www.debian.org'})
    rng = random.Random(SEED)
    oai_pick = rng.sample(sorted(oai), N_OAI)
    deb_pick = rng.sample(sorted(deb), N_DEB)

    rows = []
    for i, h in enumerate(sorted(oai_pick), 1):
        base = oai[h]
        sep = '&' if '?' in base else '?'
        rows.append({'id': 'P%02d' % i, 'class': 'repository', 'operator': h, 'host': h, 'surface': 'api',
                     'url': base + sep + 'verb=Identify', 'marker': '<Identify>', 'prior': ''})
    for i, h in enumerate(sorted(deb_pick), 1):
        rows.append({'id': 'Q%02d' % i, 'class': 'mirror-drawn', 'operator': h, 'host': h, 'surface': 'file',
                     'url': deb[h] + 'README', 'marker': 'Debian', 'prior': ''})
    with open(ROOT / 'panel' / 'drawn.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['id', 'class', 'operator', 'host', 'surface', 'url', 'marker', 'prior'])
        w.writeheader()
        w.writerows(rows)
    print('frames: %d OAI-PMH URLs on %d hosts; %d Debian mirror URLs on %d hosts' %
          (len(oai_urls), len(oai), len(deb_urls), len(deb)))
    print('drew %d + %d; seed %d' % (len(oai_pick), len(deb_pick), SEED))


main()

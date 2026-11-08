#!/usr/bin/env python3
"""Evidence review (R-0059): reproduce LH044's draw independently of draw_panel.py.

Reads the two frames as committed with the brief (git show 0adb294:...), named.csv as committed
with the brief, applies the brief's rule as written (one URL per host, lexicographically first;
named hosts and the frames' own hosts dropped; hosts sorted; random.Random(seed).sample, 40 OAI
then 20 Debian), and compares with panel/drawn.csv as committed at 1789e54 and as it stands now.
No network. Usage: python3 -I studies/LH044/review/redraw.py
"""
import csv, hashlib, io, random, re, subprocess
from urllib.parse import urlsplit

REPO = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()
def show(rev, path):
    return subprocess.check_output(['git', '-C', REPO, 'show', f'{rev}:{path}'])

P = 'studies/LH044/'
oai_raw = show('0adb294', P + 'data/prebrief-2026-11-08T1915Z/p25.body')
deb_raw = show('0adb294', P + 'data/prebrief-2026-11-08T1915Z/p02.body')
print('p25 sha256', hashlib.sha256(oai_raw).hexdigest(), len(oai_raw))
print('p02 sha256', hashlib.sha256(deb_raw).hexdigest(), len(deb_raw))
named = {r['host'].strip().lower() for r in csv.DictReader(io.StringIO(show('0adb294', P + 'panel/named.csv').decode()))}
print('named hosts', len(named))

# OAI: parse with a real XML parser rather than a regex, as an independent check
import xml.etree.ElementTree as ET
root = ET.fromstring(oai_raw)
oai_urls = [e.text.strip() for e in root.iter() if e.tag.split('}')[-1] == 'baseURL' and e.text]
oai_urls = [u for u in oai_urls if u.lower().startswith(('http://', 'https://'))]
deb_urls = re.findall(r'href="(https?://[^"]+/debian/)"', deb_raw.decode('utf-8', 'replace'))

def per_host(urls, drop):
    d = {}
    for u in sorted(set(urls)):
        h = (urlsplit(u).hostname or '').lower()
        if h and h not in drop:
            d.setdefault(h, u)
    return d
oai = per_host(oai_urls, named | {'www.openarchives.org'})
deb = per_host(deb_urls, named | {'www.debian.org'})
print('OAI urls %d (distinct %d) hosts after drops %d; Debian urls %d (distinct %d) hosts after drops %d'
      % (len(oai_urls), len(set(oai_urls)), len(oai), len(deb_urls), len(set(deb_urls)), len(deb)))
seed = int(hashlib.sha256(b'LH044 panel, fixed 8 November 2026').hexdigest(), 16)
rng = random.Random(seed)
oai_pick = sorted(rng.sample(sorted(oai), 40))
deb_pick = sorted(rng.sample(sorted(deb), 20))
mine = [(h, oai[h] + ('&' if '?' in oai[h] else '?') + 'verb=Identify') for h in oai_pick] + \
       [(h, deb[h] + 'README') for h in deb_pick]

for rev in ('1789e54', 'HEAD'):
    rows = list(csv.DictReader(io.StringIO(show(rev, P + 'panel/drawn.csv').decode())))
    theirs = [(r['host'], r['url']) for r in rows]
    print(rev, 'drawn.csv rows', len(rows), 'identical to redraw:', theirs == mine)
    for a, b in zip(mine, theirs):
        if a != b:
            print('  differs', a, b)
# overlap checks
hosts = [h for h, _ in mine]
print('drawn hosts unique:', len(set(hosts)) == len(hosts), '; overlap with named:', sorted(set(hosts) & named))

#!/usr/bin/env python3
"""Offline replay of LH029: verify the retained archive page, re-extract its 23 October entry and compare with LH024's 22 October copy."""
from hashlib import sha256
from html import unescape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
rows = json.loads((ROOT / 'data/snapshot-2026-10-23/read_log.json').read_text())
assert len(rows) <= 3
for row in rows:
    body = (ROOT / row['file']).read_bytes()
    assert len(body) == row['bytes'] <= 1024 * 1024 and sha256(body).hexdigest() == row['sha256']
    print(row['source'], row['status'], row['start_utc'], row['bytes'], 'bytes verified')


def entries(path):
    page = path.read_text(encoding='utf-8')
    out = {}
    for match in re.finditer(r'<article class="newsItem">(.*?)</article>', page, re.S):
        block = match.group(1)
        ident = re.search(r'<a id="([^"]+)"', block)
        clock = re.search(r'<time class="newsdate" datetime="([^"]+)">', block)
        if ident:
            links = re.findall(r'href="([^"]+)"', block.split('</header>', 1)[-1])
            text = unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', block))).strip()
            out[ident.group(1)] = {'datetime': clock.group(1) if clock else '', 'text': text, 'links': links}
    return out


new = entries(ROOT / 'data/snapshot-2026-10-23/archive.raw')
old = entries(REPO / 'studies/LH024/data/snapshot-2026-10-22/php_0.raw')
entry = new['2026-10-23-1']
print('\n2026-10-23-1 datetime attribute:', entry['datetime'])
print('links in entry body:', entry['links'])
print('text:', entry['text'])
assert entry['text'] == (ROOT / 'data/entry-2026-10-23-1.txt').read_text().strip()
print('\nentries in 22 Oct copy:', len(old), 'in 23 Oct copy:', len(new))
print('added since 22 Oct copy:', [(k, new[k]['datetime']) for k in new if k not in old])
print('removed:', [k for k in old if k not in new])
for key in old:
    if key in new and old[key]['text'] != new[key]['text']:
        sa, sb = set(re.split(r'(?<=[.!?]) ', old[key]['text'])), set(re.split(r'(?<=[.!?]) ', new[key]['text']))
        print('changed:', key, '| sentences only in 22 Oct copy:', sorted(sa - sb), '| only in 23 Oct copy:', sorted(sb - sa))

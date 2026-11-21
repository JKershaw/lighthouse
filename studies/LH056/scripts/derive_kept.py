#!/usr/bin/env python3
"""Replace LH056's kept socket.dev post with a derived file (the keeper's decision of 21 November 2026,
notes/keeper/2026-11-21-robots-intent.md: socket.dev's robots.txt refuses AI-training crawlers by name).

The derived file (socket_post.derived.json beside the body) holds the URL, read time, HTTP status, size and
SHA-256 from fetchlog.csv, and only what the record uses (E2 in sources.md): the page's datePublished and
dateModified metadata and the short phrase sources.md quotes, checked against the page's visible text. No script
reads the body. It never deletes anything. Offline, standard library only.
Usage: python3 -I studies/LH056/scripts/derive_kept.py
"""
from pathlib import Path
import csv, html, json, re

D = Path(__file__).resolve().parents[1] / 'data' / 'prebrief-2026-11-18T1319Z'
NOTE = ("Body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md): "
        "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, so Lighthouse keeps the "
        "URL, read time, status, SHA-256 of the bytes received and the facts its records use, not the page.")
QUOTES = ['The reported payloads do not download or execute additional code']


def main():
    p = D / 'socket_post.raw'
    if not p.exists():
        print('derived files written: 0'); return
    row = next(r for r in csv.DictReader(open(D / 'fetchlog.csv')) if r['name'] == 'socket_post')
    raw = p.read_bytes().decode('utf-8', 'replace')
    t = re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', ' ', raw)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t)).replace('’', "'").replace('“', '"').replace('”', '"')
    t = re.sub(r'\s+', ' ', t)
    pub = re.search(r'"datePublished"\s*:\s*"([^"]+)"', raw)
    mod = re.search(r'"dateModified"\s*:\s*"([^"]+)"', raw)
    rec = {'url': row['url'], 'read_utc': row['utc_start'], 'http_status': row['status'], 'content_type': row['content_type'],
           'bytes': int(row['bytes']), 'sha256': row['sha256'], 'robots_class': 'A: AI-training token named and refused; * allows',
           'body_removed': NOTE,
           'used_for': "E2 (sources.md): Socket's account of the two agent-framework releases; quoted in sources.md and brief.md.",
           'extracted': {'datePublished': pub.group(1) if pub else None, 'dateModified': mod.group(1) if mod else None,
                         'quoted_phrases': {q: q in t for q in QUOTES}}}
    (D / 'socket_post.derived.json').write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
    print('derived files written: 1')


if __name__ == '__main__':
    main()

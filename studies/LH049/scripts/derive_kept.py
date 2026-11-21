#!/usr/bin/env python3
"""Replace LH049's kept socket.dev pages with derived files (the keeper's decision of 21 November 2026,
notes/keeper/2026-11-21-robots-intent.md: socket.dev's robots.txt refuses AI-training crawlers by name).

Each derived file (<name>.derived.json beside the body) holds the URL, read times, HTTP status, size and SHA-256
from that directory's read_log.json, and only what the record uses: for the post (E8), the short phrases and
times that brief.md quotes from it, each checked against the page's visible text; for the blog listing (E5),
only that it links the post. No script reads either body. It never deletes anything.
Offline, standard library only. Usage: python3 -I studies/LH049/scripts/derive_kept.py
"""
from pathlib import Path
import gzip, html, json, re

DATA = Path(__file__).resolve().parents[1] / 'data'
NOTE = ("Body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md): "
        "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, so Lighthouse keeps the "
        "URL, read time, status, SHA-256 of the bytes received and the facts its records use, not the page.")
TARGETS = [
    ('pre-brief-2026-11-10T1437Z', 'socket_blog', 'E5 (sources.md): Socket blog listing, read for its link to the post (E8).', []),
    ('pre-brief-2026-11-10T1438Z', 'socket_post', "E8 (sources.md): Socket's account of the bee-js release; quoted in brief.md, What is already known, and measure 6.",
     ['received', '00:09:50', 'removed it at 01:24:58 UTC', '01:25:27', 'had 3,741 downloads between November 1 and 8',
      'averaged about 470 npm downloads a day in early November 2026',
      'per-version counts for it are not available; based on daily traffic, we estimate on the order of ten fetches of 13.3.0, including scanners and mirrors.']),
]


def text(raw):
    t = raw.decode('utf-8', 'replace')
    t = re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', ' ', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    t = t.replace('’', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', t)


def main():
    n = 0
    for d, name, used, quotes in TARGETS:
        p = DATA / d / (name + '.raw.gz')
        if not p.exists():
            continue
        row = next(r for r in json.loads((DATA / d / 'read_log.json').read_text()) if r['name'] == name)
        raw = gzip.decompress(p.read_bytes())
        t = text(raw)
        ext = {'quoted_phrases': {q: q in t for q in quotes}} if quotes else {
            'links_post': '/blog/bee-js-compromise' in raw.decode('utf-8', 'replace')}
        rec = {'url': row['url'], 'read_utc': row.get('start_utc'), 'finish_utc': row.get('finish_utc'),
               'http_status': row.get('status'), 'final_url': row.get('final_url'), 'bytes': row.get('bytes'),
               'sha256': row.get('sha256'), 'robots_class': 'A: AI-training token named and refused; * allows',
               'body_removed': NOTE, 'used_for': used, 'extracted': ext}
        (DATA / d / (name + '.derived.json')).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
        n += 1
    print('derived files written:', n)


if __name__ == '__main__':
    main()

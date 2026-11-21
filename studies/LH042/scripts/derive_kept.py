#!/usr/bin/env python3
"""Replace LH042's kept round-1 response from www.axios.com with a derived file (the keeper's decision of
21 November 2026, notes/keeper/2026-11-21-robots-intent.md: the site's robots.txt refuses CCBot, an AI-training
crawler, on that path; found by notes/keeper/robots-intent-2026-11-21/sweep_may_keep.py once its log tie was
fixed, output sweep_may_keep_output_2.json).

The response was a bot challenge page (HTTP 403, title "Just a moment..."), not the article; no quotation in
data/counts.csv or data/relayed.csv cites it, and no script reads it. The derived file holds the URL, read time,
status, sizes and hashes from readlog.csv and the page's title. It never deletes anything.
Offline, standard library only. Usage: python3 -I studies/LH042/scripts/derive_kept.py
"""
import csv, json, re
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data'
NOTE = ("Body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md): "
        "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, so Lighthouse keeps the "
        "URL, read time, status, SHA-256 of the bytes received and the facts its records use, not the page.")
TARGETS = [('round1-2026-11-08', 35, 'www.axios.com')]


def main():
    n_done = 0
    for folder, n, host in TARGETS:
        d = DATA / folder
        body = d / ('%03d.body' % n)
        if not body.exists():
            continue
        row = next(r for r in csv.DictReader(open(d / 'readlog.csv')) if r['n'] == str(n))
        assert row['url'].split('/')[2] == host
        title = re.search(rb'(?is)<title[^>]*>(.*?)</title>', body.read_bytes())
        rec = {'url': row['url'], 'read_utc': row['start_utc'], 'http_status': int(row['http_status']),
               'final_url': row['final_url'], 'content_type': row['content_type'], 'bytes': int(row['bytes']),
               'sha256_as_fetched': row['sha256_as_fetched'], 'sha256_saved': row['sha256_saved'],
               'robots_class': 'A: an AI-training crawler (CCBot) named and refused; * allows',
               'body_removed': NOTE,
               'used_for': 'Nothing: a bot challenge page, not the article; no count or quotation cites it.',
               'extracted': {'title': title.group(1).decode('utf-8', 'replace').strip() if title else None,
                             'challenge_page': True}}
        (d / ('%03d.derived.json' % n)).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
        n_done += 1
    print('derived files written:', n_done)


if __name__ == '__main__':
    main()

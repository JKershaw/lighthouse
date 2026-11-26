#!/usr/bin/env python3
"""LH051: compare the kept vendor post copies across reads, for the record (version 1.0, 26 November 2026).

Offline. Reads only the gzipped copies under studies/LH051/data/*/ (names already withheld) and their read_log.json.
Drops script, style, pre, code, noscript and svg elements before anything else, so the posts' code blocks are not
read. For each copy it prints the logged Last-Modified header, the page's own dateModified (where it has one), how
often each figure string the record relies on appears in the prose, and a SHA-256 of the sorted set of prose
sentences that carry any of those figures, so a changed figure sentence shows as a changed hash. It prints no page
text. Output is deterministic.

Usage: python3 -I studies/LH051/scripts/compare_posts.py > studies/LH051/record-posts-output.txt
"""
from pathlib import Path
import gzip
import hashlib
import html
import json
import re

DATA = Path(__file__).resolve().parents[1] / 'data'
FIGS = ['61,839', '61,764', '4,837', '10,431', '92%', '1,835', '1,806', '12:45', '15:00',
        '63,000', '90%', '21,000', '07:40', '101 ']


def prose(path):
    b = gzip.open(path).read().decode('utf-8', 'replace')
    m = re.search(r'"dateModified"\s*:\s*"([^"]+)"', b)
    b = re.sub(r'(?is)<(script|style|pre|code|noscript|svg)\b.*?</\1>', ' ', b)
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', b)))
    return (m.group(1) if m else '-'), t


def main():
    dirs = sorted(d for d in DATA.iterdir() if d.is_dir() and (d / 'read_log.json').exists())
    for vendor in ('stepsecurity_post', 'aikido_post'):
        print(f'== {vendor}')
        for d in dirs:
            p = d / f'{vendor}.raw.gz'
            if not p.exists():
                continue
            log = {e['name']: e for e in json.load(open(d / 'read_log.json'))}.get(vendor, {})
            dm, t = prose(p)
            sents = sorted({s.strip() for s in re.split(r'(?<=[.!?])\s+', t) if any(f in s for f in FIGS)})
            h = hashlib.sha256('\n'.join(sents).encode()).hexdigest()[:16]
            counts = ' '.join(f'{f.strip()}={t.count(f)}' for f in FIGS if t.count(f))
            print(f'{d.name}: start {log.get("start_utc", "-")}; Last-Modified {log.get("last_modified", "-")}; '
                  f'dateModified {dm}; bytes received {log.get("bytes", "-")}')
            print(f'  figures in prose: {counts}')
            print(f'  figure sentences: {len(sents)}; set hash {h}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""LH044, before the brief: read the sampling frames and test the instruments. Touches no panel
outcome by design (no panel service's probe URL is requested); the hosts it does reach are listed
in the brief as statuses seen before it. Every response is kept raw under data/prebrief-<label>/.

Usage: python3 -I studies/LH044/scripts/prebrief.py <label> <url> [<url> ...]
"""
from pathlib import Path
import csv
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh044lib import fetch, UA_PLAIN  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main():
    label, urls = sys.argv[1], sys.argv[2:]
    out = ROOT / 'data' / ('prebrief-' + label)
    out.mkdir(parents=True, exist_ok=True)
    log = out / 'readlog.csv'
    new = not log.exists()
    n0 = sum(1 for _ in open(log)) - 1 if not new else 0
    with open(log, 'a', newline='') as f:
        w = csv.writer(f)
        if new:
            w.writerow(['n', 'url', 'utc', 'status', 'error', 'content_type', 'bytes', 'truncated', 'sha256', 'file'])
        for i, u in enumerate(urls, start=n0 + 1):
            r = fetch(u, ua=UA_PLAIN, cap=4 * 1024 * 1024)
            name = 'p%02d.body' % i
            (out / name).write_bytes(r['body'])
            (out / ('p%02d.headers' % i)).write_text('\n'.join('%s: %s' % kv for kv in r['headers']) + '\n')
            ct = dict((k.lower(), v) for k, v in r['headers']).get('content-type', '')
            w.writerow([i, u, r['utc'], r['status'], r['error'] or '', ct, len(r['body']), r['truncated'], r['sha256'], name])
            print(i, r['status'], r['error'], len(r['body']), u, r['error_detail'][:120])
            time.sleep(2)


main()

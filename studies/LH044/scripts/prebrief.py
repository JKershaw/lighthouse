#!/usr/bin/env python3
"""LH044, before the brief: read the sampling frames and test the instruments. Touches no panel
outcome by design (no panel service's probe URL is requested); the hosts it does reach are listed
in the brief as statuses seen before it. Every response is kept raw under data/prebrief-<label>/.

From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md; the pre-brief reads
of 8 November were made before it and asked no robots.txt): each URL is first asked of scripts/lh_fetch.py's
gate with access='oneoff' (a single targeted read), and a refused URL is logged with error "not fetched: ..."
and not requested; an allowed URL is still requested through lh044lib.fetch, whose request shape the study
measures, not through lh_fetch's urlopen. A body is saved only through lh_fetch's save_body (which withholds
email addresses, so no later redaction pass is needed), from the gate's cached robots.txt; where it may not be
kept no pNN.body is written, `file` is empty and `error` ends "body_kept: no: <reason>". The pNN.headers file
(response headers, not a body) is written as before.

Usage: python3 -I studies/LH044/scripts/prebrief.py <label> <url> [<url> ...]

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH044/scripts/prebrief.py`.
"""
from pathlib import Path
import csv
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh044lib import fetch, UA_PLAIN  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from lh_fetch import check, save_body  # noqa: E402  the robots.txt gate and the one keep path (21 November 2026)

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
            ok, info = check(u, access='oneoff')
            if not ok:
                w.writerow([i, u, '', '', 'not fetched: %s (robots %s, group %s, rule %s)' % (
                    info.get('reason'), info.get('robots_url'), info.get('decided_by', ''), info.get('rule', '')),
                    '', 0, False, '', ''])
                print(i, 'not fetched', info.get('reason'), u)
                continue
            r = fetch(u, ua=UA_PLAIN, cap=4 * 1024 * 1024)
            name = 'p%02d.body' % i
            kept, why = save_body(out / name, r['body'], u, r['headers'])
            (out / ('p%02d.headers' % i)).write_text('\n'.join('%s: %s' % kv for kv in r['headers']) + '\n')
            ct = dict((k.lower(), v) for k, v in r['headers']).get('content-type', '')
            err = r['error'] or ''
            if not kept:
                err = (err + '; ' if err else '') + 'body_kept: no: ' + why
            w.writerow([i, u, r['utc'], r['status'], err, ct, len(r['body']), r['truncated'], r['sha256'],
                        name if kept else ''])
            print(i, r['status'], r['error'], len(r['body']), u, r['error_detail'][:120])
            time.sleep(2)


main()

#!/usr/bin/env python3
"""Replace LH032's kept advisory-check pages from www.antagonist.nl with derived files (the keeper's decision of
21 November 2026, notes/keeper/2026-11-21-robots-intent.md: the site's robots.txt refuses ia_archiver, an
archiving crawler, on that path; found by notes/keeper/robots-intent-2026-11-21/sweep_may_keep.py).

For each data/read-*/advisory-check/page-N.html.gz whose read_log.json URL is on www.antagonist.nl it writes
page-N.derived.json beside it: the URL, read times, HTTP status, retained size and SHA-256 from the log. The
checkpoints use only that the sampled page answered (HTTP 200); no script reads these bodies, so nothing else
is kept. It never deletes anything. Offline, standard library only.
Usage: python3 -I studies/LH032/scripts/derive_kept.py
"""
from pathlib import Path
import json

DATA = Path(__file__).resolve().parents[1] / 'data'
HOSTS = ('www.antagonist.nl',)
NOTE = ("Body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md): "
        "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, so Lighthouse keeps the "
        "URL, read time, status, SHA-256 of the bytes received and the facts its records use, not the page.")


def main():
    n = 0
    for log in sorted(DATA.glob('read-*/advisory-check/read_log.json')):
        for r in json.loads(log.read_text()):
            if r.get('url', '').split('/')[2:3] != [HOSTS[0]] or not r.get('file'):
                continue
            body = log.parent / r['file']
            if not body.exists():
                continue
            rec = {'url': r['url'], 'read_utc': r.get('started_utc'), 'finish_utc': r.get('finished_utc'),
                   'http_status': r.get('status'), 'final_url': r.get('final_url'), 'bytes_retained': r.get('bytes_retained'),
                   'sha256_retained_response': r.get('sha256_retained_response'),
                   'robots_class': 'A: an archiving crawler (ia_archiver) named and refused; * allows',
                   'body_removed': NOTE,
                   'used_for': 'Advisory check: one of the sampled advisory pages; the checkpoint records only that it answered HTTP 200.',
                   'extracted': {}}
            (log.parent / (r['file'][:-len('.html.gz')] + '.derived.json')).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
            n += 1
    print('derived files written:', n)


if __name__ == '__main__':
    main()

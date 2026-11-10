#!/usr/bin/env python3
"""LH049 pre-brief read: the event's own records, read and kept before the brief is fixed.

It touches no download count of any kind: no api.npmjs.org request, no npmjs.com package page (which shows
weekly downloads), no tarball. The registry documents are parsed as JSON elsewhere, never executed.

Usage: python3 -I studies/LH049/scripts/collect_prebrief.py --read <UTC label> [--extra name=url ...]

Every request is asked of scripts/robots_gate.py first (set LIGHTHOUSE_PROVIDER). Bodies are kept gzipped under
data/pre-brief-<label>/ after redact_bytes; read_log.json keeps URL, UTC start and finish, status, bytes received,
their SHA-256, emails withheld and the robots decision. A target already held in that directory is skipped.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import gzip
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from robots_gate import RobotsGate  # noqa: E402
from redact_emails import redact_bytes  # noqa: E402

UA = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'
GATE = RobotsGate(UA)
ROOT = Path(__file__).resolve().parents[1]
CEILING = 16 * 1024 * 1024
MAX_REQUESTS = 12
FORBIDDEN = ('api.npmjs.org', 'www.npmjs.com', '.tgz', '/-/')   # download counts, package pages, tarballs

TARGETS = [
    ('registry_packument', 'https://registry.npmjs.org/@ethersphere%2fbee-js', None),
    ('registry_13.3.0', 'https://registry.npmjs.org/@ethersphere/bee-js/13.3.0', None),
    ('stepsecurity_post', 'https://www.stepsecurity.io/blog/ethersphere-bee-js-13-3-0-compromise', None),
    ('stepsecurity_blog', 'https://www.stepsecurity.io/blog', None),
    ('socket_blog', 'https://socket.dev/blog', None),
    ('osv_query', 'https://api.osv.dev/v1/query',
     json.dumps({'package': {'name': '@ethersphere/bee-js', 'ecosystem': 'npm'}})),
    ('npm_download_counts_doc', 'https://raw.githubusercontent.com/npm/registry/main/docs/download-counts.md', None),
]

ap = argparse.ArgumentParser()
ap.add_argument('--read', required=True)
ap.add_argument('--extra', action='append', default=[], help='name=url, a page found in a kept record')
a = ap.parse_args()
datetime.strptime(a.read, '%Y-%m-%dT%H%MZ')
targets = TARGETS if not a.extra else [(e.split('=', 1)[0], e.split('=', 1)[1], None) for e in a.extra]
for _, url, _ in targets:
    assert not any(f in url for f in FORBIDDEN), 'refused: ' + url
assert len(targets) <= MAX_REQUESTS
OUT = ROOT / 'data' / ('pre-brief-' + a.read)
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / 'read_log.json'
rows = json.loads(LOG.read_text()) if LOG.exists() else []
held = {r['name'] for r in rows if r.get('file')}
for name, url, body in targets:
    if name in held:
        continue
    row = {'name': name, 'url': url, 'method': 'POST' if body else 'GET', 'request_body': body or '',
           'start_utc': datetime.now(timezone.utc).isoformat(timespec='seconds')}
    ok, info = GATE.check(url)
    row['robots'] = info
    if not ok:
        row['error'] = 'not fetched: ' + info['reason']
    else:
        try:
            req = Request(url, data=body.encode() if body else None,
                          headers={'User-Agent': UA, **({'Content-Type': 'application/json'} if body else {})})
            try:
                resp = urlopen(req, timeout=60)
            except HTTPError as err:
                resp = err
            with resp:
                data = resp.read(CEILING + 1)
                row.update(finish_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'), status=resp.status,
                           final_url=resp.geturl(), content_type=resp.headers.get('Content-Type', ''),
                           last_modified=resp.headers.get('Last-Modified', ''), bytes=len(data),
                           sha256=sha256(data).hexdigest())
                if len(data) <= CEILING:
                    red, n = redact_bytes(data)
                    (OUT / (name + '.raw.gz')).write_bytes(gzip.compress(red, mtime=0))
                    row.update(file=name + '.raw.gz', emails_withheld=n)
        except Exception as err:
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                       error=type(err).__name__ + ': ' + str(err)[:300])
    rows.append(row)
    LOG.write_text(json.dumps(rows, indent=2) + '\n')
    print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'error')}), flush=True)

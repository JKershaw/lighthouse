#!/usr/bin/env python3
"""LH051 pre-brief schema check: which fields GH Archive's events carry, before the brief fixes what to match.

Reads one hourly file from before the campaign (by both vendors' accounts it began on 10 November 2026), asks
scripts/robots_gate.py first, streams it in memory and writes only the JSON key paths seen per event type, with
the value types and how many events carried each path. It keeps no value of any field, no repository, actor or
organisation, and matches nothing: no count of any title, branch or commit message is made.

Usage: python3 -I studies/LH051/scripts/schema_prebrief.py --hour 2026-11-08-12 --out <dir>
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import gzip
import io
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from robots_gate import RobotsGate  # noqa: E402

UA = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'


def paths(obj, prefix, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            paths(v, prefix + '.' + k if prefix else k, acc)
    elif isinstance(obj, list):
        acc.add((prefix + '[]', 'list'))
        for v in obj[:1]:
            paths(v, prefix + '[]', acc)
    else:
        acc.add((prefix, type(obj).__name__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hour', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    day = datetime.strptime(a.hour.rsplit('-', 1)[0], '%Y-%m-%d')
    assert day < datetime(2026, 11, 10), 'schema check only on an hour before the campaign'
    url = 'https://data.gharchive.org/%s.json.gz' % a.hour
    gate = RobotsGate(UA)
    ok, info = gate.check(url)
    row = {'url': url, 'robots': info, 'start_utc': datetime.now(timezone.utc).isoformat(timespec='seconds')}
    if not ok:
        row['error'] = 'not fetched: ' + info['reason']
    else:
        try:
            resp = urlopen(Request(url, headers={'User-Agent': UA}), timeout=120)
        except HTTPError as err:
            resp = err
        with resp:
            data = resp.read(512 * 1024 * 1024)
            row.update(status=resp.status, bytes=len(data), sha256=sha256(data).hexdigest(),
                       last_modified=resp.headers.get('Last-Modified', ''),
                       finish_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'))
        per_type = {}
        with gzip.open(io.BytesIO(data), 'rt', encoding='utf-8') as f:
            for line in f:
                e = json.loads(line)
                t = e.get('type', '?')
                acc = set()
                paths(e.get('payload', {}), 'payload', acc)
                d = per_type.setdefault(t, {'events': 0, 'paths': {}})
                d['events'] += 1
                for p, ty in acc:
                    key = p + ' (' + ty + ')'
                    d['paths'][key] = d['paths'].get(key, 0) + 1
        row['payload_paths_by_type'] = {t: {'events': d['events'], 'paths': dict(sorted(d['paths'].items()))}
                                        for t, d in sorted(per_type.items())}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / ('schema-%s.json' % a.hour)).write_text(json.dumps(row, indent=1) + '\n')
    print(json.dumps({k: row.get(k) for k in ('url', 'status', 'bytes', 'sha256', 'error')}))


if __name__ == '__main__':
    main()

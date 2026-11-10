#!/usr/bin/env python3
"""One LH049 read, as fixed in studies/LH049/brief.md (protocol 0.1). Run only under a schedule row,
after the brief is committed. Modelled on studies/LH048/scripts/collect.py.

Usage:
  python3 -I studies/LH049/scripts/collect.py --read 2026-11-10T1600Z
  python3 -I studies/LH049/scripts/collect.py --read 2026-11-10T1600Z --dry-run
      prints the planned requests and asks the robots.txt gate about each (which fetches only robots.txt);
      makes no request to any registry or download endpoint and writes nothing.

Each read makes, in this order (brief, "Sources, events and clocks"):
  point_before   npm's package total for the last 7 available days, with its stated start and end
  versions       npm's per-version totals for the last 7 available days
  point_after    the package total again, so a window that rolled over during the read is seen
  range          npm's package totals per day from 2026-11-01 to the read's UTC date
  packument      the registry's document for @ethersphere/bee-js (publish times, dist-tags, versions listed)
  osv            OSV's records for the package (POST, the advisory's state)

Every request is asked of scripts/robots_gate.py first (the keeper's rule of 8 November 2026; set
LIGHTHOUSE_PROVIDER to the provider running the session, or every provider's tokens are obeyed). A URL the gate
refuses is logged "not fetched", a missing reading and never a negative. Bodies are saved gzipped after
scripts/redact_emails.py redact_bytes; read_log.json keeps URL, UTC start and finish, status, bytes received,
their SHA-256, emails withheld, the robots decision, and for the point and range answers their stated start and
end dates. No tarball, script or payload is ever requested (refused below by URL). No key, token or credential.

A read already held is resumed, never overwritten: a target whose body is saved in data/read-<label>/ with an
HTTP status is not requested again. Ceiling: 6 requests per read plus at most one retry each (12), robots.txt
fetches not counted; bodies over 16 MiB are not kept.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import gzip
import json
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from robots_gate import RobotsGate  # noqa: E402  the keeper's robots.txt rule, 8 November 2026
from redact_emails import redact_bytes  # noqa: E402  email addresses withheld

UA = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'
ROOT = Path(__file__).resolve().parents[1]
PACKAGE = '@ethersphere/bee-js'
RANGE_START = '2026-11-01'
CEILING = 16 * 1024 * 1024
MAX_REQUESTS = 12                  # 6 targets, one retry each at most
FORBIDDEN = ('.tgz', '/-/', 'www.npmjs.com')   # tarballs, tarball paths, the package page


def targets(read_date):
    enc = PACKAGE.replace('/', '%2F')
    return [
        ('point_before', 'https://api.npmjs.org/downloads/point/last-week/' + PACKAGE, None),
        ('versions', 'https://api.npmjs.org/versions/%s/last-week' % enc, None),
        ('point_after', 'https://api.npmjs.org/downloads/point/last-week/' + PACKAGE, None),
        ('range', 'https://api.npmjs.org/downloads/range/%s:%s/%s' % (RANGE_START, read_date, PACKAGE), None),
        ('packument', 'https://registry.npmjs.org/' + enc, None),
        ('osv', 'https://api.osv.dev/v1/query', json.dumps({'package': {'name': PACKAGE, 'ecosystem': 'npm'}})),
    ]


def brief_committed():
    """The brief is tracked by git and unchanged since the last commit (AGENTS.md: commit before any outcome)."""
    try:
        tracked = subprocess.run(['git', '-C', str(ROOT), 'ls-files', '--error-unmatch', 'brief.md'],
                                 capture_output=True).returncode == 0
        clean = subprocess.run(['git', '-C', str(ROOT), 'diff', '--quiet', 'HEAD', '--', 'brief.md'],
                               capture_output=True).returncode == 0
        return tracked and clean
    except OSError:
        return False


def window(body):
    """The stated start and end of a point or range answer (logged, condition 2 of the gate)."""
    try:
        d = json.loads(body)
        return {'stated_start': d.get('start', ''), 'stated_end': d.get('end', '')}
    except (ValueError, AttributeError):
        return {}


def fetch(gate, name, url, body, out):
    row = {'name': name, 'url': url, 'method': 'POST' if body else 'GET', 'request_body': body or '',
           'start_utc': datetime.now(timezone.utc).isoformat(timespec='seconds')}
    ok, info = gate.check(url)
    row['robots'] = info
    if not ok:
        row['error'] = 'not fetched: ' + info['reason']
        return row
    try:
        headers = {'User-Agent': UA}
        if body:
            headers['Content-Type'] = 'application/json'
        request = Request(url, data=body.encode() if body else None, headers=headers)
        try:
            response = urlopen(request, timeout=60)
        except HTTPError as error:
            response = error
        with response:
            data = response.read(CEILING + 1)
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'), status=response.status,
                       final_url=response.geturl(), content_type=response.headers.get('Content-Type', ''),
                       last_modified=response.headers.get('Last-Modified', ''), bytes=len(data),
                       sha256=sha256(data).hexdigest())
            if len(data) <= CEILING:
                redacted, n = redact_bytes(data)
                (out / (name + '.raw.gz')).write_bytes(gzip.compress(redacted, mtime=0))
                row.update(file=name + '.raw.gz', emails_withheld=n)
                if name.startswith('point') or name == 'range':
                    row.update(window(data))
            else:
                row['error'] = 'over the 16 MiB ceiling; no body retained'
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                   error=type(error).__name__ + ': ' + str(error)[:300])
    return row


def main():
    ap = argparse.ArgumentParser(description='One LH049 read (studies/LH049/brief.md).')
    ap.add_argument('--read', required=True, help='UTC label, YYYY-MM-DDTHHMMZ')
    ap.add_argument('--dry-run', action='store_true',
                    help='list the requests and the robots.txt decisions only; no download-count request')
    a = ap.parse_args()
    label = datetime.strptime(a.read, '%Y-%m-%dT%H%MZ')
    plan = targets(label.strftime('%Y-%m-%d'))
    for _, url, _ in plan:
        assert not any(f in url for f in FORBIDDEN), 'refused: ' + url
    gate = RobotsGate(UA)
    if a.dry_run:
        for name, url, body in plan:
            ok, info = gate.check(url)
            print(json.dumps({'name': name, 'url': url, 'method': 'POST' if body else 'GET',
                              'allowed': ok, 'robots': info.get('reason')}))
        print(json.dumps({'dry_run': True, 'brief_committed': brief_committed(),
                          'out': str(ROOT / 'data' / ('read-' + a.read))}))
        return
    if not brief_committed():
        sys.exit('brief.md is not committed (or has uncommitted changes): no read before the protocol is fixed')
    out = ROOT / 'data' / ('read-' + a.read)
    log = out / 'read_log.json'
    rows = json.loads(log.read_text()) if log.exists() else []
    held = {r['name'] for r in rows if r.get('file') and isinstance(r.get('status'), int) and (out / r['file']).exists()}
    attempts = {}
    for r in rows:
        attempts[r['name']] = attempts.get(r['name'], 0) + 1
    out.mkdir(parents=True, exist_ok=True)
    made = 0
    for name, url, body in plan:
        if name in held:
            print(json.dumps({'name': name, 'skipped': 'already held'}), flush=True)
            continue
        if attempts.get(name, 0) >= 2:
            print(json.dumps({'name': name, 'skipped': 'two attempts already logged (one retry allowed)'}), flush=True)
            continue
        if made >= MAX_REQUESTS:
            sys.exit('ceiling of %d requests reached' % MAX_REQUESTS)
        row = fetch(gate, name, url, body, out)
        made += 1
        rows.append(row)
        log.write_text(json.dumps(rows, indent=2) + '\n')
        print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'stated_start', 'stated_end', 'error')}),
              flush=True)


if __name__ == '__main__':
    main()

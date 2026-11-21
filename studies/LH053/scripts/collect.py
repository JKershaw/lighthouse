#!/usr/bin/env python3
"""LH053 collector, as fixed in studies/LH053/brief.md (protocol 0.1). Modelled on studies/LH049/scripts/collect.py.

Two modes.

  --prebrief --read <label> [--only name ...]
      The event's own records, read and kept before the brief is fixed: the registry documents of both packages,
      StepSecurity's post, and OSV's records for both packages. It touches no download count of any kind: no
      api.npmjs.org request, no npmjs.com package page (which shows weekly downloads), no tarball. Writes
      data/pre-brief-<label>/. The same mode, run again at the closure gate, re-reads the same records.

  --read <label> [--dry-run]
      One outcome read (brief, "Sources, events and clocks"), run only under a schedule row, after the brief is
      committed. Eight requests, in this order, for L = @wppconnect-team/wppconnect then S = @wppconnect/server:
        <p>_range_before   npm's package totals per day for the last 7 available days, with the stated start and end
        <p>_versions       npm's per-version totals for the last 7 available days
        <p>_range_after    the same as range_before again, so a window that rolled over during the read is seen
        <p>_packument      the registry document (publish times, dist-tags, versions listed, deprecation marks)
      --dry-run prints the planned requests and asks the robots.txt gate about each (which fetches only robots.txt);
      it makes no request to any registry or download endpoint and writes nothing.

Every request is asked of scripts/robots_gate.py first (the keeper's rule of 8 November 2026; set LIGHTHOUSE_PROVIDER
to the provider running the session, or every provider's tokens are obeyed). A URL the gate refuses is logged
"not fetched", a missing reading and never a negative. Bodies are saved gzipped after scripts/redact_emails.py
redact_bytes; read_log.json keeps URL, UTC start and finish, status, bytes received, their SHA-256, emails withheld,
the robots decision, and for the range answers their stated start and end dates. No retry: a request that fails is
logged and not repeated in the same read (gate condition 4). No tarball, payload, commit, Docker layer, nightly asset,
workflow or bot is ever requested (refused below by URL). No key, token or credential.

A read already held is resumed, never overwritten: a target whose body is saved with an HTTP status, or that has
any attempt logged, is not requested again. Ceiling: 8 requests per read, robots.txt fetches not counted; bodies over
16 MiB are not kept.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import json
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
import lh_fetch  # noqa: E402  its robots.txt gate (the keeper's rule, 8 November 2026), used for fetching and keeping alike
from lh_fetch import save_body  # noqa: E402  what may be kept (the keeper, 21 November 2026)
from redact_emails import redact_bytes  # noqa: E402  email addresses withheld

UA = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'
ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [('L', '@wppconnect-team/wppconnect'), ('S', '@wppconnect/server')]
CEILING = 16 * 1024 * 1024
MAX_REQUESTS = 8
# tarballs and tarball paths, package pages, and every host the brief forbids (gate condition 6)
FORBIDDEN = ('.tgz', '/-/', 'www.npmjs.com', 'github.com', 'githubusercontent.com', 'docker.io', 'docker.com',
             'telegram', 't.me/', 'ghcr.io')
FORBIDDEN_PREBRIEF = FORBIDDEN + ('api.npmjs.org',)   # no download count before the brief is fixed


def enc(package):
    return package.replace('/', '%2F')


def outcome_targets():
    out = []
    for p, package in PACKAGES:
        out += [
            (p + '_range_before', 'https://api.npmjs.org/downloads/range/last-week/' + package, None),
            (p + '_versions', 'https://api.npmjs.org/versions/%s/last-week' % enc(package), None),
            (p + '_range_after', 'https://api.npmjs.org/downloads/range/last-week/' + package, None),
            (p + '_packument', 'https://registry.npmjs.org/' + enc(package), None),
        ]
    return out


def prebrief_targets():
    out = [('stepsecurity_post',
            'https://www.stepsecurity.io/blog/wppconnect-compromised-malicious-releases-steal-secrets-and-whatsapp-sessions',
            None)]
    for p, package in PACKAGES:
        out.append((p + '_packument', 'https://registry.npmjs.org/' + enc(package), None))
    for p, package in PACKAGES:
        out.append((p + '_osv', 'https://api.osv.dev/v1/query',
                    json.dumps({'package': {'name': package, 'ecosystem': 'npm'}})))
    return out


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
    """The stated start and end of a range answer, and the sum of its daily totals (the brief's clock rule)."""
    try:
        d = json.loads(body)
        days = d.get('downloads') or []
        return {'stated_start': d.get('start', ''), 'stated_end': d.get('end', ''),
                'n_days': len(days), 'sum_days': sum(int(x.get('downloads', 0)) for x in days)}
    except (ValueError, AttributeError, TypeError):
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
                kept, why = save_body(out / (name + '.raw.gz'), data, response.geturl() or url, response.headers)
                if kept:  # the keeper, 21 November 2026: no body kept where robots.txt or the page refuses it
                    row.update(file=name + '.raw.gz', emails_withheld=redact_bytes(data)[1])
                else:  # the window facts below are still logged
                    row['body_kept'] = 'no: ' + why
                if '_range_' in name:
                    row.update(window(data))
            else:
                row['error'] = 'over the 16 MiB ceiling; no body retained'
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                   error=type(error).__name__ + ': ' + str(error)[:300])
    return row


def run(plan, out, forbidden):
    for _, url, _ in plan:
        assert not any(f in url for f in forbidden), 'refused: ' + url
    assert len(plan) <= MAX_REQUESTS
    gate = lh_fetch  # lh_fetch.check(url): the same gate save_body asks
    log = out / 'read_log.json'
    rows = json.loads(log.read_text()) if log.exists() else []
    attempted = {r['name'] for r in rows}
    out.mkdir(parents=True, exist_ok=True)
    made = 0
    for name, url, body in plan:
        if name in attempted:
            print(json.dumps({'name': name, 'skipped': 'already attempted in this read (no retry)'}), flush=True)
            continue
        if made >= MAX_REQUESTS:
            sys.exit('ceiling of %d requests reached' % MAX_REQUESTS)
        row = fetch(gate, name, url, body, out)
        made += 1
        rows.append(row)
        log.write_text(json.dumps(rows, indent=2) + '\n')
        print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'stated_start', 'stated_end',
                                                    'sum_days', 'error')}), flush=True)


def main():
    ap = argparse.ArgumentParser(description='LH053 collector (studies/LH053/brief.md).')
    ap.add_argument('--read', required=True, help='UTC label, YYYY-MM-DDTHHMMZ')
    ap.add_argument('--prebrief', action='store_true', help='event records only; no download endpoint')
    ap.add_argument('--only', action='append', default=[], help='with --prebrief: read only these named targets')
    ap.add_argument('--dry-run', action='store_true',
                    help='list the requests and the robots.txt decisions only; no download-count request')
    a = ap.parse_args()
    datetime.strptime(a.read, '%Y-%m-%dT%H%MZ')
    if a.prebrief:
        plan = [t for t in prebrief_targets() if not a.only or t[0] in a.only]
        run(plan, ROOT / 'data' / ('pre-brief-' + a.read), FORBIDDEN_PREBRIEF)
        return
    plan = outcome_targets()
    if a.dry_run:
        for _, url, _ in plan:
            assert not any(f in url for f in FORBIDDEN), 'refused: ' + url
        gate = lh_fetch  # lh_fetch.check(url): the same gate save_body asks
        for name, url, body in plan:
            ok, info = gate.check(url)
            print(json.dumps({'name': name, 'url': url, 'method': 'POST' if body else 'GET',
                              'allowed': ok, 'robots': info.get('reason')}))
        print(json.dumps({'dry_run': True, 'brief_committed': brief_committed(),
                          'out': str(ROOT / 'data' / ('read-' + a.read))}))
        return
    if not brief_committed():
        sys.exit('brief.md is not committed (or has uncommitted changes): no read before the protocol is fixed')
    run(plan, ROOT / 'data' / ('read-' + a.read), FORBIDDEN)


if __name__ == '__main__':
    main()

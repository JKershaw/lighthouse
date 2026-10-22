#!/usr/bin/env python3
"""Bounded public GitHub API snapshot of the preselected PHP publisher chain."""
import csv
import hashlib
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'snapshot-2026-10-21'
if OUT.exists():
    raise SystemExit('snapshot exists; refusing to overwrite evidence')
OUT.mkdir(parents=True)
FIELDS = ('observed_at_utc', 'key', 'url', 'status', 'bytes', 'sha256', 'file',
          'ratelimit_remaining', 'etag', 'last_modified', 'error')
rows = []
total = 0
BASE = 'https://api.github.com/repos/'


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def fetch(key, url):
    global total
    if len(rows) >= 24 or total >= 8 * 1024 * 1024:
        raise RuntimeError('run ceiling reached')
    previous = rows[-1]['ratelimit_remaining'] if rows else ''
    if previous and int(previous) < 5:
        raise RuntimeError('GitHub API remaining quota below five')
    at = now()
    status = ''
    hdr = {}
    body = b''
    error = ''
    limit = min(2 * 1024 * 1024, 8 * 1024 * 1024 - total)
    try:
        req = urllib.request.Request(url, headers={
            'Accept': 'application/vnd.github+json',
            'User-Agent': 'Lighthouse-LH020/0.1',
            'X-GitHub-Api-Version': '2022-11-28'})
        with urllib.request.urlopen(req, timeout=20) as response:
            status = response.status
            hdr = dict(response.headers)
            body = response.read(limit + 1)
            if len(body) > limit:
                error = 'response exceeded byte ceiling; retained truncated prefix'
                body = body[:limit]
    except urllib.error.HTTPError as exc:
        status = exc.code
        hdr = dict(exc.headers)
        body = exc.read(min(limit, 4096))
        error = 'HTTP error'
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    total += len(body)
    file = OUT / (key + '.raw')
    file.write_bytes(body)
    rows.append(dict(observed_at_utc=at, key=key, url=url, status=status,
                     bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                     file=file.relative_to(ROOT).as_posix(),
                     ratelimit_remaining=hdr.get('X-RateLimit-Remaining', ''),
                     etag=hdr.get('ETag', ''), last_modified=hdr.get('Last-Modified', ''),
                     error=error))
    with (OUT / 'read_log.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, FIELDS, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(key, status, len(body), error, flush=True)
    if status == 200 and not error:
        try:
            return json.loads(body)
        except ValueError:
            print('JSON unavailable', key, flush=True)
    return None


issue = fetch('php_issue_1693', BASE + 'docker-library/php/issues/1693')
php = fetch('php_pr_1694', BASE + 'docker-library/php/pulls/1694')
official = fetch('official_pr_22541', BASE + 'docker-library/official-images/pulls/22541')

for label, repo, number, obj in (
    ('php', 'docker-library/php', 1694, php),
    ('official', 'docker-library/official-images', 22541, official),
):
    prefix = BASE + repo
    fetch(label + '_commits', prefix + f'/pulls/{number}/commits?per_page=100')
    fetch(label + '_reviews', prefix + f'/pulls/{number}/reviews?per_page=100')
    fetch(label + '_events', prefix + f'/issues/{number}/events?per_page=100')
    if obj and obj.get('head', {}).get('sha'):
        fetch(label + '_checks', prefix + '/commits/' + obj['head']['sha'] + '/check-runs?per_page=100')

run = fetch('official_run', BASE + 'docker-library/official-images/actions/runs/39617280912')
fetch('official_jobs', BASE + 'docker-library/official-images/actions/runs/39617280912/jobs?per_page=100')

check_file = OUT / 'php_checks.raw'
if check_file.exists() and next((r for r in rows if r['key'] == 'php_checks'), {}).get('status') == 200:
    checks = json.loads(check_file.read_bytes()).get('check_runs', [])
    ids = sorted({int(m.group(1)) for c in checks
                  for m in [re.search(r'github\.com/docker-library/php/actions/runs/(\d+)',
                                      c.get('details_url') or '')] if m})
    if ids:
        selected = ids[0]
        fetch('php_run', BASE + f'docker-library/php/actions/runs/{selected}')
        fetch('php_jobs', BASE + f'docker-library/php/actions/runs/{selected}/jobs?per_page=100')

print('COMPLETE', now(), 'requests', len(rows), 'retained bytes', total, flush=True)

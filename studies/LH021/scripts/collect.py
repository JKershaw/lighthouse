#!/usr/bin/env python3
"""A bounded, immutable first source-and-run snapshot for three PHP image publishers.

From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md) a body is saved
only through scripts/lh_fetch.py's save_body (which withholds email addresses, as before); where it may
not be kept no .raw is written, `file` is empty and `error` ends "body_kept: no: <reason>". A kept body is unchanged.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH021/scripts/collect.py`."""
import csv
import hashlib
import json
import urllib.error
import urllib.request
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, check as robots_check, NotFetched, UA, save_body  # noqa: E402  robots.txt gate (the keeper, 8 November 2026); one keep path (21 November)
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'snapshot-2026-10-21'
if OUT.exists():
    raise SystemExit('snapshot exists; refusing to overwrite evidence')
OUT.mkdir(parents=True)
REPOS = ('docker-library/wordpress', 'docker-library/drupal', 'nextcloud/docker')
FIELDS = ('observed_at_utc', 'key', 'url', 'status', 'bytes', 'sha256', 'file', 'remaining', 'error')
rows = []
total = 0


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def fetch(key, url):
    global total
    if len(rows) >= 36 or total >= 12 * 1024 * 1024:
        raise RuntimeError('run ceiling reached')
    if rows and rows[-1]['remaining'] and int(rows[-1]['remaining']) < 5:
        raise RuntimeError('GitHub rate allowance below five')
    at = now()
    status = ''
    body = b''
    hdr = {}
    error = ''
    final = url
    cap = min(2 * 1024 * 1024, 12 * 1024 * 1024 - total)
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': UA,
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'})
        with urlopen(req, timeout=20) as response:
            status = response.status
            hdr = dict(response.headers)
            final = response.geturl() or url
            body = response.read(cap + 1)
            if len(body) > cap:
                error = 'response exceeded byte cap; retained truncated prefix'
                body = body[:cap]
    except urllib.error.HTTPError as exc:
        status = exc.code
        hdr = dict(exc.headers)
        body = exc.read(min(cap, 4096))
        error = 'HTTP error'
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    total += len(body)
    file = OUT / (key + '.raw')
    kept, why = save_body(file, body, final, hdr)
    logged_error = error if kept else (error + '; ' if error else '') + 'body_kept: no: ' + why
    rows.append(dict(observed_at_utc=at, key=key, url=url, status=status,
                     bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                     file=file.relative_to(ROOT).as_posix() if kept else '',
                     remaining=hdr.get('X-RateLimit-Remaining', ''), error=logged_error))
    with (OUT / 'read_log.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, FIELDS, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(key, status, len(body), logged_error, flush=True)
    if status == 200 and not error:
        try:
            return json.loads(body)
        except ValueError:
            pass
    return None


selection = []
for owner_repo in REPOS:
    key = owner_repo.replace('/', '_')
    base = 'https://api.github.com/repos/' + owner_repo
    repo = fetch(key + '_repo', base)
    if not repo:
        selection.append(dict(repo=owner_repo, error='repo unavailable'))
        continue
    commit = fetch(key + '_commit', base + '/commits/' + repo['default_branch'])
    if not commit:
        selection.append(dict(repo=owner_repo, error='commit unavailable'))
        continue
    sha = commit['sha']
    tree = fetch(key + '_tree', base + '/git/trees/' + commit['commit']['tree']['sha'] + '?recursive=1')
    if not tree or tree.get('truncated'):
        selection.append(dict(repo=owner_repo, head_sha=sha, error='tree unavailable or truncated'))
        continue
    entries = {x['path']: x for x in tree['tree'] if x['type'] == 'blob'}
    dockerfiles = sorted(p for p in entries if p.rsplit('/', 1)[-1].startswith('Dockerfile'))[:4]
    workflows = sorted(p for p in entries if p.startswith('.github/workflows/')
                       and p.endswith(('.yml', '.yaml')))[:2]
    selected = dockerfiles + workflows
    selection.append(dict(repo=owner_repo, head_sha=sha, dockerfiles=dockerfiles,
                          workflows=workflows, tree_truncated=False))
    for i, path in enumerate(selected):
        fetch(key + '_blob_' + str(i), base + '/git/blobs/' + entries[path]['sha'])
    fetch(key + '_runs', base + '/actions/runs?per_page=10')

(OUT / 'selection.json').write_text(json.dumps(selection, indent=2) + '\n')
print('COMPLETE', now(), len(rows), 'requests', total, 'retained bytes', flush=True)

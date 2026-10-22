#!/usr/bin/env python3
"""A bounded, immutable first source-and-run snapshot for three PHP image publishers."""
import csv
import hashlib
import json
import urllib.error
import urllib.request
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
    cap = min(2 * 1024 * 1024, 12 * 1024 * 1024 - total)
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Lighthouse-LH021/0.1',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'})
        with urllib.request.urlopen(req, timeout=20) as response:
            status = response.status
            hdr = dict(response.headers)
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
    file.write_bytes(body)
    rows.append(dict(observed_at_utc=at, key=key, url=url, status=status,
                     bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                     file=file.relative_to(ROOT).as_posix(),
                     remaining=hdr.get('X-RateLimit-Remaining', ''), error=error))
    with (OUT / 'read_log.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, FIELDS, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(key, status, len(body), error, flush=True)
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

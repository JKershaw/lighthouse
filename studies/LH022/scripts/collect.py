#!/usr/bin/env python3
"""Bounded public Drupal source, run and derived-tag feasibility read."""
import base64
import csv
import hashlib
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/snapshot-2026-10-22'
OUT.mkdir(parents=True, exist_ok=False)
rows = []
retained = 0
github = hub = logs = 0


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def fetch(key, url, kind='github', accept=None):
    global retained, github, hub, logs
    if kind == 'github':
        github += 1
    elif kind == 'log':
        github += 1
        logs += 1
    else:
        hub += 1
    if github > 40 or hub > 6 or logs > 2 or retained >= 12 * 1024 * 1024:
        raise RuntimeError('request ceiling')
    if rows and rows[-1]['remaining'] and rows[-1]['kind'] in ('github', 'log') and int(rows[-1]['remaining']) < 5:
        raise RuntimeError('GitHub remaining allowance below five')
    at = now()
    hdr = {}
    data = b''
    status = ''
    error = ''
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Lighthouse-LH022/0.1',
            'Accept': accept or 'application/vnd.github+json'})
        with urllib.request.urlopen(req, timeout=25) as response:
            status = response.status
            hdr = dict(response.headers)
            data = response.read(min(2 * 1024 * 1024, 12 * 1024 * 1024 - retained) + 1)
            if len(data) > min(2 * 1024 * 1024, 12 * 1024 * 1024 - retained):
                error = 'truncated to byte ceiling'
                data = data[:-1]
    except urllib.error.HTTPError as exc:
        status = exc.code
        hdr = dict(exc.headers)
        data = exc.read(4096)
        error = 'HTTP error'
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    path = OUT / (key + '.raw')
    path.write_bytes(data)
    retained += len(data)
    rows.append(dict(utc=at, kind=kind, key=key, url=url, status=status, bytes=len(data),
                     sha256=hashlib.sha256(data).hexdigest(), remaining=hdr.get('X-RateLimit-Remaining', ''),
                     error=error))
    with (OUT / 'read_log.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(key, status, len(data), error, flush=True)
    if status == 200 and not error:
        try:
            return json.loads(data)
        except ValueError:
            return data
    return None


base = 'https://api.github.com/repos/docker-library/drupal'
official = fetch('official_library_drupal', 'https://api.github.com/repos/docker-library/official-images/contents/library/drupal')
selected = {}
if isinstance(official, dict) and official.get('content'):
    manifest = base64.b64decode(official['content']).decode()
    for stanza in manifest.strip().split('\n\n'):
        fields = dict(line.split(': ', 1) for line in stanza.splitlines() if ': ' in line)
        if '11.3-php8.3-fpm' in fields.get('Tags', '').split(', '):
            selected = fields
            break
selection = {'stanza': selected, 'manifest_git_sha': official.get('sha') if isinstance(official, dict) else None}
if selected:
    commit = selected['GitCommit']
    directory = selected.get('Directory', '.')
    recipe = (directory.rstrip('/') + '/Dockerfile').lstrip('./')
    selection['production_recipe'] = recipe
    selection['production_commit'] = commit
    selection['production_file'] = fetch('production_dockerfile', base + '/contents/' + recipe + '?ref=' + commit)
    # Store the API response, but omit its duplicated base64 body from the selection index.
    selection.pop('production_file', None)
pre = fetch('pre_event_commits', base + '/commits?until=2026-10-20T23:59:59Z&per_page=1')
head = fetch('current_repo', base)
selection['pre_event_sha'] = pre[0]['sha'] if isinstance(pre, list) and pre else None
selection['current_sha'] = head['default_branch'] if isinstance(head, dict) else None
current = fetch('current_commit', base + '/commits/' + head['default_branch']) if isinstance(head, dict) else None
selection['current_sha'] = current['sha'] if isinstance(current, dict) else None
if selected:
    for label, sha in [('pre', selection['pre_event_sha']), ('head', selection['current_sha'])]:
        if sha:
            fetch(label + '_dockerfile', base + '/contents/' + recipe + '?ref=' + sha)
runs = fetch('recent_runs', base + '/actions/runs?per_page=20')
selection['runs'] = [{'id': x['id'], 'head_sha': x['head_sha'], 'created_at': x['created_at'],
                      'conclusion': x['conclusion'], 'name': x['name']} for x in runs.get('workflow_runs', [])] if isinstance(runs, dict) else []
matches = [x for x in selection['runs'] if x['head_sha'] in (selection['pre_event_sha'], selection['current_sha'])
           and x['created_at'] >= '2026-10-21T16:30:00Z']
selection['post_release_matching_runs'] = matches
for x in matches[:2]:
    fetch('jobs_' + str(x['id']), base + '/actions/runs/' + str(x['id']) + '/jobs?per_page=100')
if selected:
    fetch('derived_tag', 'https://hub.docker.com/v2/namespaces/library/repositories/drupal/tags/11.3-php8.3-fpm', kind='hub')
(OUT / 'selection.json').write_text(json.dumps(selection, indent=2) + '\n')
print('COMPLETE', now(), github, 'GitHub', hub, 'Hub', retained, 'bytes', flush=True)

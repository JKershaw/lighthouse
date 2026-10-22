#!/usr/bin/env python3
"""Exploratory, byte-retaining Drupal production chain read."""
import csv
import hashlib
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/snapshot-2026-10-22'
OUT.mkdir(parents=True, exist_ok=False)
prior = json.loads((ROOT.parent / 'LH022/data/snapshot-2026-10-22/selection.json').read_text())
rows = []
spent = 0
token = ''


def read(key, url, headers=None, ephemeral=False):
    global spent
    if len(rows) >= 30 or spent >= 10 * 1024 * 1024:
        raise RuntimeError('ceiling')
    at = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    status, data, error, hdr = '', b'', '', {}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Lighthouse-LH023/0.1', **(headers or {})})
        with urllib.request.urlopen(req, timeout=24) as r:
            status, hdr = r.status, dict(r.headers)
            data = r.read(min(2 * 1024 * 1024, 10 * 1024 * 1024 - spent) + 1)
            if len(data) > min(2 * 1024 * 1024, 10 * 1024 * 1024 - spent):
                data, error = data[:-1], 'response cap exceeded'
    except urllib.error.HTTPError as exc:
        status, hdr, data, error = exc.code, dict(exc.headers), exc.read(4096), 'HTTP error'
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    if not ephemeral:
        (OUT / (key + '.raw')).write_bytes(data)
        spent += len(data)
    rows.append(dict(utc=at, key=key, url=url, status=status, bytes='' if ephemeral else len(data),
                     sha256='' if ephemeral else hashlib.sha256(data).hexdigest(),
                     remaining=hdr.get('X-RateLimit-Remaining', hdr.get('Ratelimit-Remaining', '')),
                     error=error))
    with (OUT / 'read_log.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, rows[0].keys(), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    print(key, status, len(data), error, flush=True)
    return json.loads(data) if status == 200 and not error else None


base = 'https://api.github.com/repos/docker-library/drupal/contents/10.6/php8.3/fpm-trixie/Dockerfile?ref='
for label, sha in [('production', '2ecfbed5dd6aa9d5555753c0a5afb883fe8706a4'),
                   ('pre', prior['pre_event_sha']), ('head', prior['current_sha'])]:
    read(label + '_recipe', base + sha, {'Accept': 'application/vnd.github+json'})

tag = read('derived_tag', 'https://hub.docker.com/v2/namespaces/library/repositories/drupal/tags/10.6-php8.3-fpm')
if tag:
    matches = [x for x in tag.get('images', []) if x.get('os') == 'linux' and x.get('architecture') == 'amd64']
    if matches:
        digest = matches[0]['digest']
        auth = read('auth', 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/drupal:pull', ephemeral=True)
        if auth:
            h = {'Authorization': 'Bearer ' + auth['token'], 'Accept': 'application/vnd.oci.image.manifest.v1+json'}
            manifest = read('manifest', 'https://registry-1.docker.io/v2/library/drupal/manifests/' + digest, h)
            if manifest:
                read('config', 'https://registry-1.docker.io/v2/library/drupal/blobs/' + manifest['config']['digest'],
                     {'Authorization': 'Bearer ' + auth['token']})
print('COMPLETE', len(rows), 'reads', spent, 'retained bytes')

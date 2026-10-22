#!/usr/bin/env python3
"""Read one exact PHP base variant; discard its anonymous registry bearer."""
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
rows = []
retained = 0


def fetch(key, url, headers=None, ephemeral=False):
    global retained
    if len(rows) >= 4 or retained >= 2 * 1024 * 1024:
        raise RuntimeError('ceiling')
    at = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    status, data, hdr, error = '', b'', {}, ''
    cap = min(1024 * 1024, 2 * 1024 * 1024 - retained)
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Lighthouse-LH026/0.1', **(headers or {})})
        with urllib.request.urlopen(request, timeout=25) as response:
            status, hdr = response.status, dict(response.headers)
            data = response.read(cap + 1)
            if len(data) > cap:
                data, error = data[:cap], 'response exceeded cap'
    except urllib.error.HTTPError as exc:
        status, hdr, data, error = exc.code, dict(exc.headers), exc.read(min(cap, 4096)), 'HTTP error'
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    if not ephemeral:
        (OUT / (key + '.raw')).write_bytes(data)
        retained += len(data)
    remaining = hdr.get('Ratelimit-Remaining', hdr.get('RateLimit-Remaining', ''))
    rows.append(dict(utc=at, key=key, url=url, status=status,
                     bytes='' if ephemeral else len(data),
                     sha256='' if ephemeral else hashlib.sha256(data).hexdigest(),
                     file='[anonymous bearer discarded]' if ephemeral else str(Path('data') / OUT.name / (key + '.raw')),
                     ratelimit_remaining=remaining, error=error))
    with (OUT / 'read_log.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, rows[0].keys(), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    print(key, status, len(data), error, flush=True)
    return json.loads(data) if status == 200 and not error else None, remaining


tag, _ = fetch('hubtag', 'https://hub.docker.com/v2/namespaces/library/repositories/php/tags/8.3-fpm-trixie')
if tag:
    matches = [x for x in tag.get('images', []) if x.get('os') == 'linux' and x.get('architecture') == 'amd64']
    if matches:
        token, _ = fetch('auth', 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/php:pull', ephemeral=True)
        if token:
            h = {'Authorization': 'Bearer ' + token['token'], 'Accept': 'application/vnd.oci.image.manifest.v1+json'}
            manifest, remaining = fetch('manifest',
                'https://registry-1.docker.io/v2/library/php/manifests/' + matches[0]['digest'], h)
            if manifest and remaining and int(remaining.split(';')[0]) < 10:
                print('rate limit stop', remaining)
            elif manifest:
                fetch('config', 'https://registry-1.docker.io/v2/library/php/blobs/' + manifest['config']['digest'],
                      {'Authorization': 'Bearer ' + token['token']})
print('COMPLETE', len(rows), retained, 'retained bytes')
